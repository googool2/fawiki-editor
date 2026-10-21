#!/usr/bin/env python3
"""fa_lint — deterministic Persian orthography fixer for fa.wiki wikitext.

No LLM, no network. Fixes only prose: everything inside {{ }}, [[ ]], <ref>,
<nowiki>, comments, URLs, table attributes, etc. stays byte-identical (see
fawiki_common.find_protected_spans; verified after every run). Problems seen
inside protected regions, and risky patterns, are reported as warnings only.

Usage:
  fa_lint.py ARTICLE.wikitext            # report + unified diff, file untouched
  fa_lint.py ARTICLE.wikitext --fix      # rewrite the file in place
  fa_lint.py ARTICLE.wikitext --check    # exit 1 if anything would change
  fa_lint.py - < in.txt -o out.txt       # stdin -> fixed text in out.txt
  fa_lint.py README.fa.md                # *.md: Markdown code is protected too
  fa_lint.py --list-rules

Exit codes: 0 ok / nothing to change, 1 changes needed (--check), 2 usage error.
Every rule's source is listed in references/orthography.md.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fawiki_common import (  # noqa: E402
    NON_JOINING, PERSIAN_LETTERS, PH_CLASS, PH_RE, ZWNJ, Masked, __version__, load_json, read_input,
    utf8_stdio, write_text_atomic,
)

L = PERSIAN_LETTERS
FA = f"[{L}]"
HARAKAT = "ً-ٰٕ"
NOT_LETTER_AFTER = rf"(?![{L}{HARAKAT}])"
NOT_LETTER_BEFORE = rf"(?<![{L}{HARAKAT}{ZWNJ}])"
# End of a word for suffix rules: not followed by a letter or ZWNJ.
EOW = rf"(?![{L}{HARAKAT}{ZWNJ}])"

_STEMS = load_json("verb_stems.json")
_PAST = "|".join(sorted(_STEMS["past"].split("|"), key=len, reverse=True))
_PRESENT = "|".join(sorted(_STEMS["present"].split("|"), key=len, reverse=True))
_MI_EXCEPTIONS = set(_STEMS["exceptions"]) | {
    "میزان", "میانه", "میراث", "میهن", "میدان", "میلاد", "میوه", "میلیون", "میمون", "میرزا",
    "مینا", "میشل", "میکروب", "میدانی",  # «دان» is handled apart in AbarAbzar.py L1156-L1161
}
_DICT = load_json("dictation.json")["entries"]
_JOINED_TAR = {"بیش", "کم", "به", "مه", "که"}  # بیشتر، کمتر، بهتر… are written joined


@dataclass
class Rule:
    id: str
    name: str
    pattern: re.Pattern
    repl: str | Callable[[re.Match], str]
    desc: str


@dataclass
class Change:
    id: int
    rule: str
    name: str
    line: int
    before: str
    after: str


@dataclass
class Result:
    original: str
    fixed: str
    changes: list[Change] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)

    @property
    def whitespace_only(self) -> bool:
        return self.fixed != self.original and re.sub(r"\s", "", self.fixed) == re.sub(r"\s", "", self.original)


def _r(id_, name, pattern, repl, desc, flags=re.MULTILINE):
    return Rule(id_, name, re.compile(pattern, flags), repl, desc)


# ------------------------------------------------------------- replacements
_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹")


def _presentation(m: re.Match) -> str:
    out = unicodedata.normalize("NFKC", m.group(0))
    return out.replace("ك", "ک").replace("ي", "ی").replace("ى", "ی")


def _latin_digits(m: re.Match) -> str:
    tok = m.group(0)
    if re.search(rf"[A-Za-z{PH_CLASS}_@#&=\\/]", tok):
        return tok  # code, versions, model names, paths, placeholders
    before = m.string[max(0, m.start() - 40):m.start()]
    after = m.string[m.end():m.end() + 3]
    if re.search(r"[A-Za-z][\w.+-]*[ \t]*$", before) or re.match(r"[ \t]*[A-Za-z]", after):
        return tok  # "Windows 10", "10 GB": number belongs to a Latin phrase
    return tok.translate(_DIGITS)


def _join(m: re.Match) -> str:
    prev, suffix = m.group(1), m.group(2)
    return prev + ("" if prev[-1] in NON_JOINING else ZWNJ) + suffix


def _tarin(m: re.Match) -> str:
    word, suffix = m.group(1), m.group(2)
    if word in _JOINED_TAR:
        return word + suffix
    return word + ("" if word[-1] in NON_JOINING else ZWNJ) + suffix


def _mi(m: re.Match) -> str:
    prefix, sep, rest = m.group("pre"), m.group("sep"), m.group("rest")
    if not sep and (prefix + rest in _MI_EXCEPTIONS or "می" + rest in _MI_EXCEPTIONS):
        return m.group(0)
    return prefix + ZWNJ + rest


def _curly(m: re.Match) -> str:
    return "«" + m.group(1).strip() + "»"


_DICT_RE = re.compile(
    NOT_LETTER_BEFORE + "(" + "|".join(re.escape(e["wrong"]) for e in sorted(_DICT, key=lambda e: -len(e["wrong"]))) + ")" + NOT_LETTER_AFTER
)
_DICT_MAP = {e["wrong"]: e["right"] for e in _DICT}

RULES: list[Rule] = [
    # --- characters ---------------------------------------------------------
    _r("FA09", "control-chars", "[\x00-\x08\x0b\x0c\x0e-\x1f\x7f﻿]", "", "remove control characters and BOM"),
    _r("FA00", "presentation-forms", "[ﭐ-﷏ﹰ-ﻼ]|ڪ", _presentation,
       "Arabic presentation forms / ڪ → standard letters"),
    _r("FA01", "arabic-yeh", "[يى]", "ی", "Arabic ي/ى → Persian ی"),
    _r("FA02", "arabic-kaf", "ك", "ک", "Arabic ك → Persian ک"),
    _r("FA03", "arabic-indic-digits", "[٠-٩]+", lambda m: m.group(0).translate(_AR_DIGITS),
       "Arabic-Indic ٠-٩ → Persian ۰-۹"),
    _r("FA04", "latin-digits", r"[^\s«»()\[\]،؛؟!\"'*:|]*[0-9][^\s«»()\[\]،؛؟!\"'*:|]*", _latin_digits,
       "Latin digits in Persian prose → ۰-۹ (skips tokens/phrases with Latin letters)"),
    _r("FA06", "persian-percent", "(?<=[۰-۹])[ \t]?%", "٪", "% after Persian digits → ٪"),
    _r("FA07", "persian-decimal", r"(?<=[۰-۹])\.(?=[۰-۹])", "٫", "decimal point between Persian digits → ٫"),
    _r("FA08", "persian-thousands", "(?<=[۰-۹]),(?=[۰-۹]{3}(?![۰-۹]))", "٬",
       "thousands comma between Persian digits → ٬"),
    _r("FA05", "kashida", f"(?<={FA})ـ+(?={FA})", "", "remove tatweel ـ between letters"),
    # --- ZWNJ hygiene ------------------------------------------------------
    _r("FA10", "zwnj-duplicate", f"{ZWNJ}{{2,}}", ZWNJ, "collapse repeated ZWNJ"),
    _r("FA11", "zwnj-space", rf"[ \t]*{ZWNJ}[ \t]+|[ \t]+{ZWNJ}", " ", "ZWNJ next to a space → plain space"),
    _r("FA12", "zwnj-after-nonjoining", f"(?<=[{NON_JOINING}]){ZWNJ}", "", "redundant ZWNJ after a non-joining letter"),
    _r("FA13", "zwnj-edge",
       rf"(?:(?<=^)|(?<=[^{L}{HARAKAT}{PH_CLASS}])){ZWNJ}|{ZWNJ}(?=$|[^{L}{HARAKAT}{PH_CLASS}])",
       "", "ZWNJ not between two letters (kept next to [[links]])"),
    # --- ezafe / heh -------------------------------------------------------
    _r("FA14", "heh-hamza", rf"ۀ|هٓ|ه[ \t]*ء{EOW}|ه[ \t]+ٔ", "هٔ", "ۀ / هٓ / هء / ه ء → هٔ"),
    _r("FA15", "heh-ye-ezafe", rf"(?<={FA})ه{ZWNJ}ی{EOW}", "هٔ", "ezafe written ه‌ی → هٔ"),
    _r("FA16", "heh-yi", rf"ه{ZWNJ}[ئی]ی{EOW}", f"ه{ZWNJ}ای", "ه‌ئی / ه‌یی → ه‌ای"),
    # --- ZWNJ insertion ----------------------------------------------------
    _r("FA20", "zwnj-mi",
       NOT_LETTER_BEFORE + rf"(?P<pre>ن?می)(?P<sep>[ \t]?)(?P<rest>(?:{_PAST})(?:م|ی|یم|ید|ند|ه|)|(?:{_PRESENT}|دان)(?:م|ی|د|یم|ید|ند)|توان)"
       + NOT_LETTER_AFTER, _mi, "(ن)می + known verb stem → می‌/نمی‌ (stem list from fa.wiki's ابرابزار)"),
    _r("FA21", "zwnj-ha", rf"({FA})[ \t]+(ها|های|هایی|هایم|هایت|هایش|هایمان|هایتان|هایشان){EOW}",
       _join, "plural ها after a space → ‌ها (no ZWNJ after non-joining letters)"),
    _r("FA22", "zwnj-tarin", rf"([{L}]+)[ \t]+(ترین|ترینِ){EOW}", _tarin, "superlative ترین after a space → ‌ترین"),
    _r("FA23", "zwnj-heh-suffix", rf"(?<=[{L}])(?<!ک)(ه)[ \t]+(ای|ایم|اید|اند|ام){EOW}", _join,
       "silent ه + ای/ام/ایم/اید/اند → ه‌ای …"),
    # --- punctuation characters -------------------------------------------
    _r("FA30", "persian-comma", rf"(?<={FA})[ \t]*,(?![\d,])[ \t]*", "، ", "Latin comma after a Persian word → ،"),
    _r("FA31", "persian-semicolon", rf"(?<={FA})[ \t]*;[ \t]*", "؛ ", "Latin semicolon after a Persian word → ؛"),
    _r("FA32", "persian-question", rf"(?<={FA})[ \t]*\?", "؟", "Latin ? after a Persian word → ؟"),
    _r("FA33", "curly-quotes", rf"[“„]([^”“\n{PH_CLASS}]*{FA}[^”“\n{PH_CLASS}]*)”", _curly, "“…” around Persian → «…»"),
    # --- spacing -----------------------------------------------------------
    _r("FA40", "space-before-punct", r"(?<=\S)[ \t]+(?=[.،؛؟!:)»](?:\s|$|[^.\d]))", "",
       "no space before . ، ؛ ؟ ! : ) »"),
    _r("FA41", "space-after-open", r"(?<=[«(])[ \t]+", "", "no space after « ("),
    _r("FA42", "space-after-punct", rf"(?<={FA})([،؛؟.:])(?={FA})", r"\1 ", "one space after punctuation between Persian words"),
    _r("FA43", "double-space", r"(?<=\S)[ \t]{2,}(?=[^\s=])", " ", "collapse runs of spaces (not before =)"),
    _r("FA44", "trailing-space", r"[ \t]+$", "", "strip trailing whitespace"),
    # --- dictionary --------------------------------------------------------
    Rule("FA50", "dictation", _DICT_RE, lambda m: _DICT_MAP[m.group(1)],
         "curated unambiguous misspellings (fa.wiki اشتباه‌یاب subset, scripts/data/dictation.json)"),
]
RULE_IDS = {r.id for r in RULES}

# ------------------------------------------------------------------ warnings
_FW = [
    ("FW02", re.compile(rf"([{L}{ZWNJ}]+)[ \t]+(تر|تری){EOW}"),
     lambda m: m.group(1) not in _JOINED_TAR, "possible comparative «{0}»: ‌تر? («تر» can also mean 'wet')"),
    ("FW03", re.compile(rf"\"[^\"\n{PH_CLASS}]*{FA}[^\"\n{PH_CLASS}]*\""), None, "straight quotes «{0}»: fa.wiki uses « »"),
    ("FW04", re.compile(r"(?<![\d۰-۹])[۰-۹0-9]{1,4}[/\-][۰-۹0-9]{1,2}[/\-][۰-۹0-9]{1,4}(?![\d۰-۹])"), None,
     "date «{0}» with / or -: write «۲۹ آذر ۱۳۹۵» style in prose"),
    ("FW05", re.compile(rf"(?<={FA})ه[ \t]+ی{EOW}"), None, "«{0}»: ezafe after silent ه is written هٔ (check meaning)"),
    ("FW06", re.compile(rf"{NOT_LETTER_BEFORE}(?:حضرت|شادروان|مرحوم|زنده{ZWNJ}یاد|زنده یاد|علیه{ZWNJ}السلام){NOT_LETTER_AFTER}|\((?:ع|ره|ص|س)\)"),
     None, "honorific «{0}»: avoid per NPOV (fa.wiki اشتباه‌یاب epithet list)"),
    ("FW07", re.compile(rf"[۰-۹]{{4}}{ZWNJ}?ها{EOW}"), None, "decade «{0}»: write «دههٔ ۱۹۸۰»"),
    ("FW08", re.compile(rf"{NOT_LETTER_BEFORE}(?:جولای|آگوست|آپریل|جون|فبروری){NOT_LETTER_AFTER}"), None,
     "month «{0}»: use French forms (ژوئیه، اوت، آوریل، ژوئن، فوریه)"),
]


def _warnings(masked: Masked) -> list[dict]:
    out = []
    for s, _e, kind, chunk in masked.protected(("link", "template", "extlink")):
        body = re.sub(r"(?:https?:)?//\S+", "", chunk)
        if re.search("[يىك]", body):
            out.append({"rule": "FW01", "line": masked.original.count("\n", 0, s) + 1,
                        "message": f"Arabic ي/ك inside {kind} (not changed): {chunk[:60]}"})
    for code, rx, cond, msg in _FW:
        for m in rx.finditer(masked.text):
            if cond is None or cond(m):
                out.append({"rule": code, "line": masked.line_of(masked.text, m.start()),
                            "message": msg.format(masked.unmask(m.group(0)))})
    out.sort(key=lambda w: (w["line"], w["rule"]))
    return out


def _context(text: str, start: int, end: int) -> tuple[int, int]:
    s = max(text.rfind(" ", 0, start) + 1, text.rfind("\n", 0, start) + 1, start - 25)
    e = text.find(" ", end)
    e = len(text) if e == -1 else e
    nl = text.find("\n", end)
    if nl != -1:
        e = min(e, nl)
    return s, min(e, end + 25)


def lint(text: str, enabled: set[str] | None = None, markdown: bool = False,
         select: set[int] | None = None) -> Result:
    """Lint `text`. Every candidate change gets an id in application order (rule order,
    then position). With `select`, only those ids are applied; the rest stay as they are."""
    masked = Masked(text, markdown=markdown)
    cur = masked.text
    res = Result(original=text, fixed=text)
    counter = [0]
    for rule in RULES:
        if enabled is not None and rule.id not in enabled:
            continue
        hits: list[tuple[int, int, str, int]] = []

        def sub(m: re.Match, rule=rule) -> str:
            new = m.expand(rule.repl) if isinstance(rule.repl, str) else rule.repl(m)
            if new == m.group(0):
                return new
            counter[0] += 1
            if select is not None and counter[0] not in select:
                return m.group(0)
            hits.append((m.start(), m.end(), new, counter[0]))
            return new

        new_text = rule.pattern.sub(sub, cur)
        if new_text == cur:
            continue
        for start, end, new, cid in hits:
            cs, ce = _context(cur, start, end)
            res.changes.append(Change(cid, rule.id, rule.name, masked.line_of(cur, start),
                                      masked.unmask(cur[cs:ce]), masked.unmask(cur[cs:start] + new + cur[end:ce])))
        cur = new_text
    # Safety net (as fa.wiki's cosmetic bot does): protected spans must survive intact and in order.
    if PH_RE.findall(cur) != PH_RE.findall(masked.text) or cur.count("\n") != masked.text.count("\n"):
        raise RuntimeError("internal error: a rule touched a protected region or a newline")
    res.fixed = masked.unmask(cur)
    res.warnings = _warnings(Masked(res.fixed, markdown=markdown))
    res.changes.sort(key=lambda c: c.id)
    return res


def parse_ranges(spec: str, kind: str = "id", universe: set[str] | None = None) -> set:
    """'3-5,9' -> {3,4,5,9}; for rules 'FA20-FA23,FA40' -> matching existing rule ids."""
    out: set = set()
    for part in filter(None, (p.strip() for p in spec.split(","))):
        lo, _, hi = part.partition("-")
        if kind == "id":
            a, b = int(lo), int(hi or lo)
            if a < 1 or b < a:
                raise ValueError(f"bad id range: {part}")
            out |= set(range(a, b + 1))
        else:
            lo, hi = lo.upper(), (hi or lo).upper()
            m1, m2 = re.fullmatch(r"([A-Z]+)(\d+)", lo), re.fullmatch(r"([A-Z]+)(\d+)", hi)
            if not m1 or not m2 or m1.group(1) != m2.group(1):
                raise ValueError(f"bad rule range: {part}")
            nums = range(int(m1.group(2)), int(m2.group(2)) + 1)
            hit = {r for r in (universe or set()) if r.startswith(m1.group(1))
                   and r[len(m1.group(1)):].isdigit() and int(r[len(m1.group(1)):]) in nums}
            if not hit:
                raise ValueError(f"no rule matches: {part}")
            out |= hit
    return out


def _ranges(nums: list[int]) -> str:
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if i == j else f"{nums[i]}-{nums[j]}")
        i = j + 1
    return ",".join(parts)


def format_summary(res: Result, name: str = "input") -> str:
    """One line per rule: count, change ids (as ranges) and lines. Short enough for a model."""
    out = [f"fa_lint {__version__}: {name}: {len(res.changes)} change(s), {len(res.warnings)} warning(s)"
           + (" [whitespace-only]" if res.whitespace_only else "")]
    groups: dict[str, list[Change]] = {}
    for c in res.changes:
        groups.setdefault(c.rule, []).append(c)
    for rule, cs in groups.items():
        ex = cs[0]
        out.append(f"  {rule} {ex.name:<22} x{len(cs):<3} ids {_ranges([c.id for c in cs]):<10} "
                   f"lines {_ranges([c.line for c in cs])}  e.g. «{ex.before.replace(ZWNJ, '␌')}» → «{ex.after.replace(ZWNJ, '␌')}»")
    wgroups: dict[str, list[dict]] = {}
    for w in res.warnings:
        wgroups.setdefault(w["rule"], []).append(w)
    for rule, ws in wgroups.items():
        out.append(f"  {rule} warning x{len(ws)} lines {_ranges([w['line'] for w in ws])}: {ws[0]['message']}")
    return "\n".join(out)


def format_report(res: Result, name: str = "input") -> str:
    lines_changed = len({c.line for c in res.changes})
    head = (f"fa_lint: {name}: {len(res.changes)} change(s) on {lines_changed} line(s), "
            f"{len(res.warnings)} warning(s)")
    if res.whitespace_only:
        head += " [whitespace-only: not worth an edit on its own]"
    out = [head]
    for c in sorted(res.changes, key=lambda c: (c.line, c.id)):
        out.append(f"  #{c.id:<3} L{c.line:<4} {c.rule} {c.name:<22} «{c.before.replace(ZWNJ, '␌')}» → «{c.after.replace(ZWNJ, '␌')}»")
    for w in res.warnings:
        out.append(f"  L{w['line']:<4} {w['rule']} warning                {w['message']}")
    if any(ZWNJ in (c.before + c.after) for c in res.changes):
        out.append("  (␌ marks a ZWNJ / نیم‌فاصله in this report only)")
    return "\n".join(out)


def unified_diff(res: Result, name: str = "input") -> str:
    return "".join(difflib.unified_diff(
        res.original.splitlines(keepends=True), res.fixed.splitlines(keepends=True),
        fromfile=f"a/{name}", tofile=f"b/{name}"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Persian orthography linter for fa.wiki wikitext")
    ap.add_argument("file", nargs="?", default="-", help="wikitext file or - for stdin")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--fix", action="store_true", help="rewrite FILE in place")
    g.add_argument("--check", action="store_true", help="exit 1 if changes are needed")
    ap.add_argument("-o", "--output", help="write fixed text here")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--no-diff", action="store_true", help="report only")
    ap.add_argument("--markdown", action="store_true", help="protect Markdown code (auto for *.md)")
    ap.add_argument("--rules", help="rule ids or ranges to run, e.g. FA01,FA20-FA23 (default: all)")
    ap.add_argument("--disable", help="rule ids or ranges to skip")
    ap.add_argument("--only", help="apply only these change ids, e.g. 1-4,9 (ids from a plain run)")
    ap.add_argument("--summary", action="store_true", help="one line per rule instead of one per change")
    ap.add_argument("--list-rules", action="store_true")
    ap.add_argument("--version", action="version", version=f"fa_lint {__version__}")
    utf8_stdio()
    a = ap.parse_args(argv)

    if a.list_rules:
        for r in sorted(RULES, key=lambda r: r.id):
            print(f"{r.id}  {r.name:<22} {r.desc}")
        for code, _rx, _c, msg in _FW:
            print(f"{code}  warning                {msg.replace('{0}', '…')}")
        return 0
    try:
        enabled = parse_ranges(a.rules, "rule", RULE_IDS) if a.rules else set(RULE_IDS)
        if a.disable:
            enabled -= parse_ranges(a.disable, "rule", RULE_IDS)
        select = parse_ranges(a.only, "id") if a.only else None
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    if a.fix and a.file == "-":
        print("--fix needs a file path", file=sys.stderr)
        return 2
    try:
        text = read_input(a.file)
    except OSError as e:
        print(f"cannot read {a.file}: {e}", file=sys.stderr)
        return 2
    res = lint(text, enabled, markdown=a.markdown or a.file.lower().endswith(".md"), select=select)
    name = "stdin" if a.file == "-" else Path(a.file).name

    if a.json:
        print(json.dumps({"file": name, "changed": res.fixed != res.original,
                          "whitespace_only": res.whitespace_only,
                          "changes": [c.__dict__ for c in res.changes], "warnings": res.warnings},
                         ensure_ascii=False, indent=2))
    else:
        print(format_summary(res, name) if a.summary else format_report(res, name))
        if not a.no_diff and not a.summary and res.fixed != res.original:
            print(unified_diff(res, name), end="")
    if a.output:
        write_text_atomic(a.output, res.fixed)
    if a.fix and res.fixed != res.original:
        write_text_atomic(a.file, res.fixed)
    return 1 if a.check and res.fixed != res.original else 0


if __name__ == "__main__":
    sys.exit(main())
