#!/usr/bin/env python3
"""Label every automatic change from bench/realworld.py as correct / debatable / wrong.

The labels encode a hand review of each change (done once, by reading every change in
context). Writing the judgment down as rules makes the count repeatable on new versions.
Rules look at the change and at its line in the corpus; no article text is stored here.

Usage: python bench/label.py CORPUS_DIR OUT_DIR/changes.jsonl [--json OUT.json]
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

FA = "آاأإءئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیةۀ"
ALWAYS_CORRECT = {  # reviewed: every instance in the corpus was a plain improvement
    "FA00", "FA01", "FA02", "FA03", "FA05", "FA06", "FA08", "FA09", "FA10", "FA11", "FA12", "FA13",
    "FA14", "FA15", "FA16", "FA20", "FA21", "FA23", "FA30", "FA31", "FA32", "FA33", "FA41", "FA43",
    "FA44", "FA50",
}


def latin_dominant(line: str, frag: str) -> bool:
    i = line.find(frag)
    window = line[max(0, i - 60): i + len(frag) + 40] if i >= 0 else line
    window = re.sub(r"\[?https?://\S+", " ", window)
    latin = len(re.findall(r"[A-Za-z]", window))
    persian = len(re.findall(f"[{FA}]", window))
    return latin > persian


def label(c: dict, line: str) -> tuple[str, str]:
    rule, before, after = c["rule"], c["before"], c["after"]
    if rule in ALWAYS_CORRECT:
        return "correct", ""
    if rule == "FA04":
        digits = re.search(r"\d+", before)
        frag = before.strip(" '()[].:") if not digits else before[digits.start():digits.end()]
        if latin_dominant(line, frag):
            return "wrong", "Latin digits inside an English phrase or bibliography"
        if "]]" in before and "[[" not in line.split(frag)[0][-40:]:
            return "debatable", "text of a broken link"
        return "correct", ""
    if rule == "FA07":
        m = re.search(r"[۰-۹]+\.([۰-۹]+)", before)
        if m and (len(m.group(1)) == 3 or before.count(".") > 1):
            return "wrong", "dot used as a thousands separator, not a decimal point"
        if re.search(r"(نسخه|نسخهٔ|ویرایش|version)\s*$", line.split(before.split(".")[0])[0][-15:]):
            return "debatable", "version number, not a decimal"
        if m and len(m.group(1)) == 2 and len(before.split(".")[0].strip("«»() ")) >= 3:
            return "debatable", "probably a mistyped thousands group"
        return "correct", ""
    if rule == "FA22":
        word = before.split()[0] if before.split() else before
        if word in ("بخش", "قدرت", "انگیز", "گذار"):
            return "debatable", "second half of a split compound: only partly fixed"
        return "correct", ""
    if rule == "FA40":
        if re.search(r"\.\s+\.$", before) or re.search(r"\.\.\s+\.", before):
            return "wrong", "joined a full stop to an ellipsis"
        if re.search(r"[^\s" + FA + r"\]»)\"'.0-9۰-۹،]\s+[،.]", before):
            return "debatable", "symbol or formula before the mark"
        return "correct", ""
    if rule == "FA42":
        m = re.search(f"([{FA}]+)([.:])([{FA}]+)", before)
        if m and m.group(2) == "." and (len(m.group(1).split()[-1]) == 1 or len(m.group(3)) == 1):
            return ("wrong", "split an abbreviation") if re.fullmatch(r"[هق]", m.group(1)[-1:] + "") and len(m.group(3)) == 1 \
                else ("debatable", "space between initials")
        return "correct", ""
    return "debatable", "no rule reviewed yet"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus")
    ap.add_argument("changes")
    ap.add_argument("--json")
    ap.add_argument("--show", choices=["wrong", "debatable"], help="print these changes")
    ap.add_argument("--context", type=int, default=0, help="with --show: also print N characters around each change")
    a = ap.parse_args()
    lines_cache: dict[str, list[str]] = {}
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    shown = []
    for raw in Path(a.changes).read_text(encoding="utf-8").splitlines():
        c = json.loads(raw)
        if c["file"] not in lines_cache:
            lines_cache[c["file"]] = (Path(a.corpus) / c["file"]).read_text(encoding="utf-8").split("\n")
        line = lines_cache[c["file"]][c["line"] - 1]
        verdict, why = label(c, line)
        counts[c["rule"]][verdict] += 1
        if a.show == verdict:
            shown.append(f"{c['rule']} «{c['before']}» → «{c['after']}»  ({why})")
            if a.context:
                i = max(line.find(c["before"]), 0)
                shown.append(f"    {c['file']} L{c['line']}: …{line[max(0, i - a.context): i + len(c['before']) + a.context]}…")
    total = collections.Counter()
    for v in counts.values():
        total.update(v)
    n = sum(total.values())
    print(f"{n} changes: correct {total['correct']}, debatable {total['debatable']}, wrong {total['wrong']} "
          f"({100 * total['wrong'] / max(n, 1):.1f}% wrong)")
    for rule in sorted(counts):
        v = counts[rule]
        if v["wrong"] or v["debatable"]:
            print(f"  {rule}: correct {v['correct']}, debatable {v['debatable']}, wrong {v['wrong']}")
    for s in shown:
        print("   ", s.replace("‌", "␌"))
    if a.json:
        Path(a.json).write_text(json.dumps({"total": dict(total), "changes": n,
                                            "by_rule": {k: dict(v) for k, v in counts.items()}}, indent=2),
                                encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
