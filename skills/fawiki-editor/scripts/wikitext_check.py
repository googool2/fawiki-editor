#!/usr/bin/env python3
"""wikitext_check — structural checks for fa.wiki article wikitext.

Offline and deterministic. Uses mwparserfromhell for template discovery when
it is installed and falls back to a regex scanner otherwise.

Usage:
  wikitext_check.py ARTICLE.wikitext [--json] [--strict]
Exit codes: 0 no errors, 1 errors found (or warnings with --strict), 2 usage error.

Checks (E = error, W = warning, I = info):
  WC01 E unbalanced [[ ]]          WC09 W English section heading
  WC02 E unbalanced {{ }}          WC10 W English namespace (Category:, File:)
  WC03 E <ref> without </ref>      WC11 W heading level skipped / level-1 heading
  WC04 E refs but no {{پانویس}}    WC12 W malformed heading (= counts differ)
  WC05 E no [[رده:...]]            WC13 W bare URL as a whole reference
  WC06 E no bold title in lead     WC14 I {{مدرک}} placeholders still present
  WC07 W unknown template          WC15 W same ref name, different content
  WC08 W English template name     WC16 W line starts with a space (renders as <pre>)
  WC17 W no references at all      WC18 W legacy interlanguage link ([[en:...]])
  WC19 W edit-toolbar sample text   WC20 W deprecated template / English image option
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fawiki_common import __version__, utf8_stdio, find_protected_spans, line_at, load_json, read_input, try_mwparser  # noqa: E402

DATA = load_json("templates.json")
KNOWN = {n.replace("_", " ").strip() for n in DATA["known_templates"]}
EN2FA = {k.lower(): v for k, v in DATA["english_to_persian"].items()}
HEAD_EN2FA = {k.lower(): v for k, v in DATA["english_headings"].items()}
HEAD_FA_STD = DATA["nonstandard_headings"]
DEPRECATED = DATA["deprecated_templates"]
LEFTOVERS = DATA["toolbar_leftovers"]
NS_EN2FA = DATA["english_namespaces"]
REFLIST_NAMES = {n.lower() for n in DATA["reflist_templates"]}
CITATION_NEEDED = set(DATA["citation_needed_templates"])
DISAMBIG = set(DATA["disambiguation_templates"])
LANG_CODES = set(DATA["interlanguage_prefixes"])
MAGIC_PREFIXES = ("#", "subst:", "safesubst:", "msgnw:", "int:", "raw:")
MAGIC_WORDS = {w.lower() for w in DATA["magic_words"]}


@dataclass
class Issue:
    code: str
    severity: str
    line: int
    message: str


def _blank_opaque(text: str) -> str:
    """Replace comments/nowiki/pre/code/math with spaces (keeps offsets & newlines)."""
    out = list(text)
    for s, e, kind in find_protected_spans(text):
        if kind in ("comment", "nowiki", "pre", "code", "source", "syntaxhighlight", "math", "chem", "score", "templatedata"):
            for k in range(s, e):
                if out[k] != "\n":
                    out[k] = " "
    return "".join(out)


def _balance(text: str, open_s: str, close_s: str, code: str, label: str) -> list[Issue]:
    issues, stack = [], []
    tok = re.compile(re.escape(open_s) + "|" + re.escape(close_s))
    for m in tok.finditer(text):
        if m.group() == open_s:
            stack.append(m.start())
        elif stack:
            stack.pop()
        else:
            issues.append(Issue(code, "E", line_at(text, m.start()), f"'{close_s}' without matching '{open_s}' ({label})"))
    for pos in stack:
        snippet = text[pos:pos + 40].split("\n")[0]
        issues.append(Issue(code, "E", line_at(text, pos), f"'{open_s}' never closed ({label}): {snippet}"))
    return issues


def _template_names(text: str) -> list[tuple[str, int]]:
    mw = try_mwparser()
    names: list[tuple[str, int]] = []
    if mw is not None:
        try:
            code = mw.parse(text)
            cursor = 0
            for t in code.filter_templates(recursive=True):
                raw = str(t.name)
                pos = text.find("{{" + raw, cursor if cursor < len(text) else 0)
                if pos == -1:
                    pos = text.find(raw)
                names.append((raw.strip(), line_at(text, max(pos, 0))))
            return names
        except Exception:  # noqa: BLE001 - malformed input: fall back to regex
            names = []
    for m in re.finditer(r"\{\{(?!\{)\s*([^{}|\n]+?)\s*(?=\||\}\}|\n)", text):
        names.append((m.group(1), line_at(text, m.start())))
    return names


def _norm(name: str) -> str:
    n = re.sub(r"<!--.*?-->", "", name).replace("_", " ").strip()
    n = re.sub(r"^(?:الگو|Template)\s*:\s*", "", n, flags=re.IGNORECASE)
    n = re.sub(r"\s+", " ", n)
    return n[:1].upper() + n[1:] if n[:1].isascii() else n


def check(text: str) -> list[Issue]:
    issues: list[Issue] = []
    clean = _blank_opaque(text)
    is_redirect = bool(re.match(r"\s*#(?:REDIRECT|تغییرمسیر|تغییر_مسیر)", clean, re.IGNORECASE))

    issues += _balance(clean, "[[", "]]", "WC01", "wikilink")
    issues += _balance(clean, "{{", "}}", "WC02", "template")

    # WC03: <ref ...> ... </ref> pairing (self-closing refs are fine)
    opens = []
    for m in re.finditer(r"<ref\b([^>]*?)(/?)>|</ref\s*>", clean, re.IGNORECASE):
        if m.group(0).lower().startswith("</"):
            if opens:
                opens.pop()
            else:
                issues.append(Issue("WC03", "E", line_at(clean, m.start()), "</ref> without opening <ref>"))
        elif m.group(2) != "/":
            if opens:
                issues.append(Issue("WC03", "E", line_at(clean, opens[-1]), "<ref> not closed before the next <ref>"))
                opens.pop()
            opens.append(m.start())
    for pos in opens:
        issues.append(Issue("WC03", "E", line_at(clean, pos), "<ref> without </ref>"))

    templates = _template_names(clean)
    tnames = {_norm(n) for n, _ in templates}
    has_refs = bool(re.search(r"<ref\b", clean, re.IGNORECASE))
    has_reflist = bool(re.search(r"<references\s*/?>", clean, re.IGNORECASE)) or any(
        n.lower() in REFLIST_NAMES for n in tnames)
    if has_refs and not has_reflist:
        issues.append(Issue("WC04", "E", 1, "article has <ref> tags but no {{پانویس}} (or <references/>) to display them"))
    if not has_refs and not is_redirect:
        issues.append(Issue("WC17", "W", 1, "no <ref> citations: fa.wiki articles need reliable sources (ویکی‌پدیا:تأییدپذیری)"))

    if not is_redirect and not re.search(r"\[\[\s*(?:رده|Category)\s*:", clean, re.IGNORECASE):
        issues.append(Issue("WC05", "E", line_at(clean, len(clean)), "no category: add at least one [[رده:...]] at the end"))

    # WC06: bold title in the first prose paragraph
    if not is_redirect and not (tnames & DISAMBIG):
        lead = _first_paragraph(clean)
        if lead is None:
            issues.append(Issue("WC06", "E", 1, "no lead paragraph found before the first heading"))
        elif not re.search(r"'''[^'\n]+?'''", lead[1]):
            issues.append(Issue("WC06", "E", lead[0], "lead sentence has no bold title ('''عنوان''')"))

    # WC07/WC08/WC14: template names
    seen = set()
    for raw, line in templates:
        n = _norm(raw)
        low = n.lower()
        if not n or n in seen:
            continue
        seen.add(n)
        if low.startswith(MAGIC_PREFIXES) or low.split(":")[0] in MAGIC_WORDS or "{" in n or n.startswith("{"):
            continue
        if low in EN2FA:
            fa = EN2FA[low]
            hint = fa if fa.startswith("(") else "{{" + fa + "}}"
            issues.append(Issue("WC08", "W", line, f"English template {{{{{n}}}}} → {hint}"))
        elif n in DEPRECATED:
            issues.append(Issue("WC20", "W", line, f"{{{{{n}}}}} is deprecated → use {{{{{DEPRECATED[n]}}}}}"))
        elif n in CITATION_NEEDED:
            pass
        elif n not in KNOWN:
            issues.append(Issue("WC07", "W", line, f"unknown template {{{{{n}}}}}: not in the skill's list; verify it exists on fa.wiki"))
    cn = sum(1 for raw, _ in templates if _norm(raw) in CITATION_NEEDED)
    if cn:
        issues.append(Issue("WC14", "I", 1, f"{cn} {{{{مدرک}}}} placeholder(s): find a reliable source or remove the claim"))

    issues += _check_headings(clean)

    # WC10 / WC18: namespaces and legacy interlanguage links
    for m in re.finditer(r"\[\[\s*:?\s*([A-Za-z][A-Za-z -]*?)\s*:", clean):
        prefix = m.group(1)
        if prefix.title() in NS_EN2FA:
            issues.append(Issue("WC10", "W", line_at(clean, m.start()), f"[[{prefix}:...]] → use [[{NS_EN2FA[prefix.title()]}:...]]"))
        elif prefix.lower() in LANG_CODES and not clean[m.start():m.start() + 4].startswith("[[:"):
            issues.append(Issue("WC18", "W", line_at(clean, m.start()), f"legacy interlanguage link [[{prefix}:...]]: fa.wiki uses Wikidata sitelinks; remove it"))

    # WC13 / WC15: reference content
    named: dict[str, str] = {}
    for m in re.finditer(r"<ref\b([^>/]*)>(.*?)</ref\s*>", text, re.IGNORECASE | re.DOTALL):
        body = m.group(2).strip()
        if re.fullmatch(r"\[?\s*https?://\S+\s*\]?", body):
            issues.append(Issue("WC13", "W", line_at(text, m.start()), "bare URL reference: wrap it in {{یادکرد وب}} (scripts/cite_builder.py)"))
        nm = re.search(r"name\s*=\s*[\"']?([^\"'>]+?)[\"']?\s*(?:group|$)", m.group(1).strip() + " ")
        if nm and body:
            key = nm.group(1).strip()
            if key in named and named[key] != body:
                issues.append(Issue("WC15", "W", line_at(text, m.start()), f"ref name \"{key}\" reused with different content"))
            named.setdefault(key, body)

    # WC19 / WC20: toolbar leftovers and English image options
    for junk in LEFTOVERS:
        pos = text.find(junk)
        if pos != -1:
            issues.append(Issue("WC19", "W", line_at(text, pos), f"edit-toolbar sample text left in the article: {junk}"))
    for m in re.finditer(r"\[\[\s*(?:پرونده|File|Image|تصویر)\s*:[^\]\n]*?\|\s*(thumb|thumbnail|left|right|center|upright)\s*(?=[|\]])", clean, re.IGNORECASE):
        fa = {"thumb": "بندانگشتی", "thumbnail": "بندانگشتی", "left": "چپ", "right": "راست", "center": "وسط", "upright": "ایستاده"}[m.group(1).lower()]
        issues.append(Issue("WC20", "W", line_at(clean, m.start()), f"image option «{m.group(1)}» → «{fa}»"))

    # WC16: accidental preformatted lines
    for m in re.finditer(r"^ +\S[^\n]*", clean, re.MULTILINE):
        issues.append(Issue("WC16", "W", line_at(clean, m.start()), "line starts with a space and will render as a code box"))

    order = {"E": 0, "W": 1, "I": 2}
    issues.sort(key=lambda i: (order[i.severity], i.line, i.code))
    return issues


def _first_paragraph(clean: str):
    blank = list(clean)
    for s0, e0, kind in find_protected_spans(clean):
        drop = kind in ("template", "comment", "table", "table-cell", "magic") or (
            kind == "link" and re.match(r"\[\[\s*(?:پرونده|File|Image|تصویر|رده|Category)\s*:", clean[s0:e0], re.I))
        if drop:
            for k in range(s0, e0):
                if blank[k] != "\n":
                    blank[k] = " "
    lines = "".join(blank).split("\n")
    buf, start = [], None
    for idx, ln in enumerate(lines, 1):
        s = ln.strip()
        if re.match(r"=+[^=].*=+$", s):
            break
        prose = re.sub(r"\{\{[^{}]*\}\}", "", s)
        prose = re.sub(r"\[\[(?:پرونده|File|Image|تصویر|رده|Category)\s*:[^\]]*\]\]", "", prose, flags=re.I).strip()
        if not prose or prose.startswith(("{{", "}}", "|", "{|", "__", "<!--")) or s.startswith("|"):
            if buf:
                break
            continue
        if start is None:
            start = idx
        buf.append(s)
    return (start, " ".join(buf)) if buf else None


def _check_headings(clean: str) -> list[Issue]:
    issues, prev = [], 1
    for m in re.finditer(r"^(=+)([^=\n].*?)(=+)[ \t]*$", clean, re.MULTILINE):
        lo, title, ro = len(m.group(1)), m.group(2).strip(), len(m.group(3))
        line = line_at(clean, m.start())
        if lo != ro:
            issues.append(Issue("WC12", "W", line, f"heading has {lo} '=' on the left and {ro} on the right: {title}"))
        level = min(lo, ro)
        if level == 1:
            issues.append(Issue("WC11", "W", line, "level-1 heading (= … =) is reserved for the page title; use =="))
        elif level > prev + 1:
            issues.append(Issue("WC11", "W", line, f"heading level jumps from {prev} to {level}: {title}"))
        prev = level
        fa = HEAD_EN2FA.get(title.lower()) or HEAD_FA_STD.get(title.replace("\u200c", "‌"))
        if fa and fa != title:
            issues.append(Issue("WC09", "W", line, f"non-standard heading «{title}» → «{fa}»"))
        if "[[" in title or "{{" in title:
            issues.append(Issue("WC11", "W", line, f"no links or templates in headings: {title}"))
    return issues


def format_report(issues: list[Issue], name: str) -> str:
    e = sum(i.severity == "E" for i in issues)
    w = sum(i.severity == "W" for i in issues)
    out = [f"wikitext_check: {name}: {e} error(s), {w} warning(s), {len(issues) - e - w} info"]
    out += [f"  L{i.line:<4} {i.severity} {i.code} {i.message}" for i in issues]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Structural checks for fa.wiki wikitext")
    ap.add_argument("file", nargs="?", default="-")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--version", action="version", version=f"wikitext_check {__version__}")
    utf8_stdio()
    a = ap.parse_args(argv)
    try:
        text = read_input(a.file)
    except OSError as e:
        print(f"cannot read {a.file}: {e}", file=sys.stderr)
        return 2
    issues = check(text)
    name = "stdin" if a.file == "-" else Path(a.file).name
    if a.json:
        print(json.dumps({"file": name, "issues": [asdict(i) for i in issues],
                          "parser": "mwparserfromhell" if try_mwparser() else "regex"},
                         ensure_ascii=False, indent=2))
    else:
        print(format_report(issues, name))
    bad = any(i.severity == "E" for i in issues) or (a.strict and any(i.severity == "W" for i in issues))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
