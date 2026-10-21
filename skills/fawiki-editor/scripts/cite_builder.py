#!/usr/bin/env python3
"""cite_builder — build a Persian citation template from a URL, DOI or ISBN.

This is the only script in the skill that may use the network, and only
when --offline is NOT given. It never invents data: any field it cannot read
from the source (or from what you typed) is left empty and listed as TODO.

Usage:
  cite_builder.py https://www.example.com/news/1        # fetch page metadata
  cite_builder.py 10.1000/xyz123                        # Crossref lookup
  cite_builder.py 978-964-00-1234-5                     # Open Library lookup
  cite_builder.py URL --offline                         # no network: skeleton
  cite_builder.py URL --type news --ref --name irna1    # wrap in <ref name=...>
  cite_builder.py URL --set title="عنوان" --set date=2024-05-01

Exit codes: 0 ok, 1 lookup failed (skeleton still printed), 2 bad input.
Parameter names: scripts/data/citations.json (sources in references/citations.md).
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fawiki_common import __version__, utf8_stdio, load_json  # noqa: E402

SPEC = load_json("citations.json")
UA = "fawiki-editor-cite-builder/0.1 (https://github.com/googool2/fawiki-editor)"
DOI_RE = re.compile(r"(?:https?://(?:dx\.)?doi\.org/|doi:\s*)?(10\.\d{4,9}/[^\s\"<>]+)", re.IGNORECASE)
Fetcher = Callable[[str], bytes]


# --------------------------------------------------------------------- input
def normalize_isbn(raw: str) -> str | None:
    s = re.sub(r"[\s\-‐]", "", raw.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))).upper()
    s = re.sub(r"^ISBN:?", "", s)
    if re.fullmatch(r"\d{9}[\dX]", s):
        total = sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(s))
        return s if total % 11 == 0 else None
    if re.fullmatch(r"97[89]\d{10}", s):
        total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(s))
        return s if total % 10 == 0 else None
    return None


def detect(source: str) -> tuple[str, str]:
    """Return (kind, value) with kind in {'doi', 'isbn', 'url'}."""
    s = source.strip()
    m = DOI_RE.fullmatch(s) or (DOI_RE.match(s) if "doi.org/" in s.lower() or s.lower().startswith("doi:") else None)
    if m:
        return "doi", m.group(1).rstrip(".")
    if re.fullmatch(r"(?:ISBN:?\s*)?[\d۰-۹Xx\-‐\s]{10,17}", s, re.IGNORECASE):
        if not normalize_isbn(s):
            raise ValueError(f"invalid ISBN (checksum failed): {s}")
        shown = re.sub(r"^ISBN:?\s*", "", s, flags=re.IGNORECASE)
        return "isbn", shown.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")).replace(" ", "-")
    if re.match(r"https?://", s, re.IGNORECASE):
        return "url", s
    raise ValueError(f"not a URL, DOI or ISBN: {s}")


# ------------------------------------------------------------------ fetching
def http_fetch(url: str, timeout: float = 15.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - http(s) only
        return r.read(2_000_000)


class _Meta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, list[str]] = {}
        self.title, self.lang, self._in_title, self._ld, self.jsonld = "", "", False, False, []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "meta":
            key = (a.get("property") or a.get("name") or a.get("itemprop") or "").lower()
            if key and a.get("content"):
                self.meta.setdefault(key, []).append(a["content"].strip())
        elif tag == "title":
            self._in_title = True
        elif tag == "script" and "ld+json" in a.get("type", ""):
            self._ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._ld:
            self.jsonld.append(data)


def _first(meta: dict, *keys: str) -> str:
    for k in keys:
        if meta.get(k):
            return html.unescape(meta[k][0])
    return ""


def _jsonld_objects(chunks: list[str]) -> list[dict]:
    out = []
    for c in chunks:
        try:
            data = json.loads(c)
        except ValueError:
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                out.append(o)
                stack.extend(o.get("@graph", []) if isinstance(o.get("@graph"), list) else [])
    return out


def from_html(raw: bytes, url: str) -> dict:
    text = raw.decode("utf-8", errors="replace")
    p = _Meta()
    p.feed(text)
    m = p.meta
    f = {"url": url}
    f["title"] = _first(m, "citation_title", "og:title", "twitter:title", "dc.title") or html.unescape(p.title.strip())
    authors = m.get("citation_author", []) or m.get("author", []) or m.get("article:author", [])
    f["authors"] = [a for a in authors if not a.startswith("http")]
    f["date"] = _first(m, "citation_publication_date", "article:published_time", "datepublished", "dc.date", "date")[:10]
    f["website"] = _first(m, "og:site_name", "application-name")
    f["language"] = (_first(m, "og:locale", "dc.language", "language") or p.lang)[:2].lower()
    is_news = _first(m, "og:type").lower() == "article" and bool(m.get("article:published_time"))
    for o in _jsonld_objects(p.jsonld):
        t = o.get("@type")
        types = t if isinstance(t, list) else [t]
        if any(x in ("NewsArticle", "ReportageNewsArticle") for x in types):
            is_news = True
        if any(x in ("NewsArticle", "Article", "BlogPosting", "ReportageNewsArticle") for x in types):
            f["title"] = f["title"] or str(o.get("headline", ""))
            f["date"] = f["date"] or str(o.get("datePublished", ""))[:10]
            au = o.get("author")
            names = [x.get("name", "") for x in (au if isinstance(au, list) else [au]) if isinstance(x, dict)]
            f["authors"] = f["authors"] or [n for n in names if n]
            pub = o.get("publisher")
            if isinstance(pub, dict) and not f.get("publisher"):
                f["publisher"] = pub.get("name", "")
    f["_kind"] = "web"  # citer also emits یادکرد وب for news; یادکرد خبر params are unverified
    f["_is_news"] = is_news
    return f


def from_crossref(raw: bytes, doi: str) -> dict:
    msg = json.loads(raw.decode("utf-8"))["message"]
    parts = (msg.get("issued") or msg.get("published-print") or msg.get("published-online") or {}).get("date-parts", [[]])[0]
    date = "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(parts)) if parts else ""
    f = {
        "doi": doi, "title": (msg.get("title") or [""])[0],
        "journal": (msg.get("container-title") or [""])[0], "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""), "pages": msg.get("page", ""), "date": date,
        "publisher": msg.get("publisher", ""), "language": msg.get("language", ""),
        "_people": [(a.get("family", ""), a.get("given", "")) for a in msg.get("author", [])],
    }
    f["_kind"] = "book" if msg.get("type", "").startswith("book") else "journal"
    return f


def from_openlibrary(raw: bytes, isbn: str) -> dict:
    data = json.loads(raw.decode("utf-8")).get(f"ISBN:{isbn}")
    if not data:
        raise LookupError(f"ISBN {isbn} not found in Open Library")
    return {
        "isbn": isbn, "title": data.get("title", ""),
        "authors": [a.get("name", "") for a in data.get("authors", [])],
        "publisher": "، ".join(p.get("name", "") for p in data.get("publishers", [])),
        "location": "، ".join(p.get("name", "") for p in data.get("publish_places", [])),
        "year": data.get("publish_date", ""), "_kind": "book",
    }


def lookup(kind: str, value: str, fetch: Fetcher) -> dict:
    if kind == "url":
        return from_html(fetch(value), value)
    if kind == "doi":
        return from_crossref(fetch("https://api.crossref.org/works/" + urllib.parse.quote(value)), value)
    key = normalize_isbn(value)
    data = from_openlibrary(fetch(f"https://openlibrary.org/api/books?bibkeys=ISBN:{key}&format=json&jscmd=data"), key)
    data["isbn"] = value
    return data


# ------------------------------------------------------------------ building
_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def build(fields: dict, kind: str, access_date: str | None = None) -> tuple[str, list[str], list[str]]:
    """Return (template_wikitext, missing_required, missing_recommended) for citation `kind`.

    Only values present in `fields` are written; nothing is guessed.
    """
    spec = SPEC["templates"][kind]
    pmap = spec["params"]
    rows: list[tuple[str, str]] = []
    people = [p for p in fields.get("_people") or [] if any(p)][: SPEC["max_authors"]]
    authors = [a for a in fields.get("authors", []) if a][: SPEC["max_authors"]]
    present: set[str] = set()
    for key in spec["order"]:
        if key in ("last", "first"):
            if key == "last" and people:
                for i, (last, first) in enumerate(people, 1):
                    n = str(i).translate(_FA_DIGITS)
                    rows.append((pmap["last"] + n, last))
                    rows.append((pmap["first"] + n, first))
                present.add("author")
            continue
        if key == "author":
            if authors and not people:
                rows.append((pmap["author"], "، ".join(authors)))
                present.add("author")
            continue
        val = fields.get(key, "")
        if key == "access_date" and not val and fields.get("url"):
            val = access_date or dt.date.today().isoformat()
        if val:
            rows.append((pmap[key], str(val).strip()))
            present.add(key)
        elif key in spec["required"]:
            rows.append((pmap[key], ""))
    missing = [pmap[k] for k in spec["required"] if k not in present]
    recommended = [pmap[k] for k in spec.get("recommended", []) if k not in present]
    body = "\n".join(f"| {name} = {val}".rstrip() for name, val in rows)
    return "{{" + spec["template"] + "\n" + body + "\n}}", missing, recommended


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build a Persian {{یادکرد ...}} template")
    ap.add_argument("source", help="URL, DOI or ISBN")
    ap.add_argument("--offline", action="store_true", help="no network; fill only what is known")
    ap.add_argument("--type", choices=["auto", "web", "news", "book", "journal"], default="auto")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="add/override a field (keys: " + ", ".join(SPEC["field_keys"]) + ")")
    ap.add_argument("--access-date", help="YYYY-MM-DD (default: today; only written when there is a URL)")
    ap.add_argument("--ref", action="store_true", help="wrap in <ref>…</ref>")
    ap.add_argument("--name", help="ref name (implies --ref)")
    ap.add_argument("--inline", action="store_true", help="single-line output")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--version", action="version", version=f"cite_builder {__version__}")
    utf8_stdio()
    a = ap.parse_args(argv)

    try:
        kind, value = detect(a.source)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    fields: dict = {kind: value}
    status, note = 0, ""
    if not a.offline:
        try:
            fields.update(lookup(kind, value, lambda u: http_fetch(u, a.timeout)))
        except (urllib.error.URLError, OSError, LookupError, ValueError, KeyError) as e:
            status, note = 1, f"lookup failed ({e}); printed an offline skeleton instead"
    for kv in a.set:
        k, _, v = kv.partition("=")
        if k == "author":
            fields["authors"] = [x.strip() for x in v.split(";") if x.strip()]
        else:
            fields[k.strip()] = v.strip()
    cite = a.type if a.type != "auto" else fields.get("_kind") or {"doi": "journal", "isbn": "book"}.get(kind, "web")
    tpl, todo, recommended = build(fields, cite, a.access_date)
    if a.inline:
        tpl = re.sub(r"\n\| ([^=\n]+?) = ?", r" | \1=", tpl).replace("\n}}", "}}")
    if a.ref or a.name:
        tpl = (f'<ref name="{a.name}">' if a.name else "<ref>") + tpl + "</ref>"
    if a.json:
        print(json.dumps({"template": tpl, "type": cite, "missing_required": todo,
                          "missing_recommended": recommended, "offline": a.offline, "note": note},
                         ensure_ascii=False, indent=2))
    else:
        print(tpl)
        if note:
            print("NOTE: " + note, file=sys.stderr)
        if todo:
            print("TODO required (fill from the source itself, never guess): " + "، ".join(todo), file=sys.stderr)
        if recommended:
            print("recommended if the source shows them: " + "، ".join(recommended), file=sys.stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())
