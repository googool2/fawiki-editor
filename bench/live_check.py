#!/usr/bin/env python3
"""Live checks against fa.wikipedia.org (needs network; run in CI or locally).

  templates OUT_DIR   Compare every template and parameter name the skill emits
                      (scripts/data/infoboxes.json, citations.json, templates.json)
                      with fa.wiki: does the template exist (or redirect), what does
                      its TemplateData list, does the template or CS1 module source
                      mention the parameter? Writes templates.json + templates.md.
  fetch OUT_DIR [--n 60] [--min-bytes 3000] [--titles FILE]
                      Download the current wikitext of random articles (namespace 0,
                      no redirects, no disambiguation pages) plus a manifest with
                      titles and revision ids for attribution. With --titles, fetch the
                      articles listed in FILE (one title per line) instead.

The skill itself never uses the network; this is a maintenance tool only.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "skills" / "fawiki-editor" / "scripts" / "data"
API = "https://fa.wikipedia.org/w/api.php"
EN_API = "https://en.wikipedia.org/w/api.php"
UA = "fawiki-editor-bench/0.2 (https://github.com/googool2/fawiki-editor; maintenance checks)"
CS1_MODULES = ["پودمان:Citation/CS1/fa/Configuration", "پودمان:Citation/CS1/Configuration"]


def api(endpoint: str = API, **params) -> dict:
    params = {"format": "json", "formatversion": "2", "maxlag": "5", **params}
    url = endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            if data.get("error", {}).get("code") == "maxlag":
                time.sleep(5 * (attempt + 1))
                continue
            return data
        except OSError:
            time.sleep(2 ** attempt)
    raise SystemExit(f"API unreachable: {url[:120]}")


def page_source(title: str) -> str:
    d = api(action="query", prop="revisions", rvprop="content", rvslots="main", titles=title, redirects="1")
    pages = d.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        return ""
    return pages[0]["revisions"][0]["slots"]["main"]["content"]


def template_info(name: str) -> dict:
    title = "الگو:" + name if not name.startswith(("الگو:", "Template:")) else name
    q = api(action="query", titles=title, redirects="1", prop="info")
    page = q.get("query", {}).get("pages", [{}])[0]
    redirects = q.get("query", {}).get("redirects", [])
    info = {"name": name, "exists": not page.get("missing", False), "resolved": page.get("title", title),
            "redirect": bool(redirects), "templatedata": False, "params": [], "required": [], "aliases": {}}
    if not info["exists"]:
        return info
    td = api(action="templatedata", titles=info["resolved"], lang="fa")
    tpages = td.get("pages", {})
    for p in (tpages.values() if isinstance(tpages, dict) else tpages):
        params = p.get("params", {}) or {}
        info["templatedata"] = bool(params)
        for pname, spec in params.items():
            info["params"].append(pname)
            if spec.get("required"):
                info["required"].append(pname)
            for al in spec.get("aliases", []) or []:
                info["aliases"][al] = pname
    src = page_source(info["resolved"])
    info["source_params"] = sorted(set(re.findall(r"\{\{\{\s*([^{}|=\n]+?)\s*[|}]", src)))
    info["uses_module"] = "#invoke" in src
    return info


def all_params(info: dict) -> list[str]:
    return sorted(set(info["params"]) | set(info["aliases"]) | set(info.get("source_params", [])))


def classify(param: str, info: dict, cs1_text: str = "") -> str:
    known = set(info["params"]) | set(info["aliases"]) | set(info.get("source_params", []))
    if param in known:
        return "confirmed"
    if cs1_text and re.search(r"['\"]" + re.escape(param) + r"['\"]", cs1_text):
        return "confirmed (CS1 module)"
    return "not found"


def cmd_templates(out: Path) -> int:
    infoboxes = json.loads((DATA / "infoboxes.json").read_text(encoding="utf-8"))["infoboxes"]
    citations = json.loads((DATA / "citations.json").read_text(encoding="utf-8"))["templates"]
    known = json.loads((DATA / "templates.json").read_text(encoding="utf-8"))
    cs1 = {m: page_source(m) for m in CS1_MODULES}
    cs1_text = "\n".join(cs1.values())
    report = {"infoboxes": {}, "citations": {}, "known_templates": {}, "english_targets": {}}
    for key, box in infoboxes.items():
        info = template_info(box["template"])
        rows = {}
        for _en, fa in box["params"].items():
            status = classify(fa, info) if info["exists"] else "template missing"
            near = difflib.get_close_matches(fa, info["params"] + info.get("source_params", []), n=2, cutoff=0.6)
            rows[fa] = {"status": status, "suggest": [n for n in near if n != fa]}
        report["infoboxes"][key] = {"template": box["template"], "info": {k: v for k, v in info.items() if k != "source_params"},
                                    "params": rows, "td_required": info["required"], "all_params": all_params(info)}
        time.sleep(0.2)
    for key, spec in citations.items():
        info = template_info(spec["template"])
        rows = {}
        for _k, fa in spec["params"].items():
            st = classify(fa, info, cs1_text) if info["exists"] else "template missing"
            rows[fa] = {"status": st}
        report["citations"][key] = {"template": spec["template"], "exists": info["exists"], "params": rows,
                                    "all_params": all_params(info)}
    for name in known["known_templates"]:
        if name.isascii():
            continue
        q = api(action="query", titles="الگو:" + name, redirects="1")
        page = q.get("query", {}).get("pages", [{}])[0]
        report["known_templates"][name] = "missing" if page.get("missing") else ("redirect → " + page["title"] if q["query"].get("redirects") else "exists")
    for en, fa in known["english_to_persian"].items():
        ll = api(EN_API, action="query", titles="Template:" + en, redirects="1", prop="langlinks", lllang="fa")
        links = ll.get("query", {}).get("pages", [{}])[0].get("langlinks", [])
        linked = links[0]["title"].split(":", 1)[-1] if links else None
        if fa.startswith("("):
            report["english_targets"][f"{en} → (none)"] = f"en.wiki interlanguage link: {linked}" if linked else "exists"
            continue
        q = api(action="query", titles="الگو:" + fa, redirects="1")
        page = q.get("query", {}).get("pages", [{}])[0]
        target = page.get("title", "").split(":", 1)[-1]
        status = "missing" if page.get("missing") else "exists"
        if linked and linked != target and linked != fa:
            status += f"; en.wiki interlanguage link: {linked}"
        report["english_targets"][f"{en} → {fa}"] = status
    out.mkdir(parents=True, exist_ok=True)
    (out / "templates.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# Live template check", ""] + [f"- {m}: {len(t)} characters" for m, t in cs1.items()] + [""]
    for section in ("infoboxes", "citations"):
        md.append(f"## {section}")
        for key, r in report[section].items():
            rows = r["params"]
            ok = sum(v["status"].startswith("confirmed") for v in rows.values())
            md.append(f"### {r['template']}: {ok}/{len(rows)} confirmed"
                      + (f" (TemplateData: {'yes' if r.get('info', {}).get('templatedata') else 'no'})" if section == "infoboxes" else ""))
            missing = False
            for p, v in rows.items():
                if not v["status"].startswith("confirmed"):
                    missing = True
                    md.append(f"- `{p}`: {v['status']}" + (f"; close: {', '.join(v.get('suggest', []))}" if v.get("suggest") else ""))
            if missing:
                md.append("- all parameters on fa.wiki: " + " · ".join(r["all_params"][:150]))
    md.append("## known_templates not existing")
    md += [f"- {k}: {v}" for k, v in report["known_templates"].items() if v != "exists"]
    md.append("## english_to_persian targets missing or differing from the interlanguage link")
    md += [f"- {k}: {v}" for k, v in report["english_targets"].items() if v != "exists"]
    (out / "templates.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


def fetch_titles(out: Path, titles_file: Path) -> list[dict]:
    got: list[dict] = []
    titles = [t.strip() for t in titles_file.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]
    for i in range(0, len(titles), 20):
        r = api(action="query", titles="|".join(titles[i:i + 20]), redirects="1", prop="info|revisions",
                rvprop="ids|content", rvslots="main")
        for p in r.get("query", {}).get("pages", []):
            if p.get("missing"):
                print(f"missing: {p.get('title')}")
                continue
            rev = p["revisions"][0]
            fname = f"{len(got) + 1:03d}.wikitext"
            (out / fname).write_text(rev["slots"]["main"]["content"], encoding="utf-8")
            got.append({"file": fname, "title": p["title"], "revid": rev["revid"], "bytes": p["length"]})
    return got


def cmd_fetch(out: Path, n: int, min_bytes: int, titles: str | None = None) -> int:
    out.mkdir(parents=True, exist_ok=True)
    got: list[dict] = fetch_titles(out, Path(titles)) if titles else []
    seen: set[int] = set()
    while not titles and len(got) < n:
        r = api(action="query", generator="random", grnnamespace="0", grnfilterredir="nonredirects", grnlimit="50",
                prop="info|pageprops|revisions", rvprop="ids|content", rvslots="main", ppprop="disambiguation")
        for p in r.get("query", {}).get("pages", []):
            if p["pageid"] in seen or "disambiguation" in p.get("pageprops", {}) or p.get("length", 0) < min_bytes:
                continue
            seen.add(p["pageid"])
            rev = p["revisions"][0]
            text = rev["slots"]["main"]["content"]
            fname = f"{len(got) + 1:03d}.wikitext"
            (out / fname).write_text(text, encoding="utf-8")
            got.append({"file": fname, "title": p["title"], "revid": rev["revid"], "bytes": p["length"]})
            if len(got) >= n:
                break
        time.sleep(0.5)
    (out / "MANIFEST.json").write_text(json.dumps({"source": "fa.wikipedia.org (CC BY-SA 4.0), " + ("listed" if titles else "random") + " articles",
                                                   "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                                   "articles": got}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"fetched {len(got)} articles, {sum(a['bytes'] for a in got)} bytes")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("templates")
    t.add_argument("out")
    f = sub.add_parser("fetch")
    f.add_argument("out")
    f.add_argument("--n", type=int, default=60)
    f.add_argument("--min-bytes", type=int, default=3000)
    f.add_argument("--titles")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    return cmd_templates(Path(a.out)) if a.cmd == "templates" else cmd_fetch(Path(a.out), a.n, a.min_bytes, a.titles)


if __name__ == "__main__":
    sys.exit(main())
