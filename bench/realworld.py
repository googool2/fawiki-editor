#!/usr/bin/env python3
"""Real-world rehearsal on a folder of real fa.wiki articles (kept OUTSIDE this repo).

For every *.wikitext / *.txt file: copy it to a temp folder, run `fawiki.py apply` (every
rule, no selection) and `undo`, and check mechanically that
  - protected regions are byte-identical after apply,
  - the template/link inventory and the newline count are unchanged,
  - undo restores the file byte for byte and leaves no backup files behind.
Every automatic change is written to OUT/changes.jsonl for hand labeling (bench/label.py).

The output quotes article text, so OUT must be outside the repository.

Usage: python bench/realworld.py CORPUS_DIR OUT_DIR [--tag v0.2.0]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "skills" / "fawiki-editor" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from bench import inventory, protected_chunks  # noqa: E402
from fa_lint import lint  # noqa: E402
from fawiki_common import __version__  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus")
    ap.add_argument("out")
    ap.add_argument("--tag", default=__version__)
    a = ap.parse_args()
    corpus, out = Path(a.corpus), Path(a.out)
    if HERE.parent.resolve() in out.resolve().parents or out.resolve() == HERE.parent.resolve():
        print("OUT must be outside the repository (it quotes article text)", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in corpus.iterdir() if p.suffix in (".wikitext", ".txt"))
    rows, failures, per_file = [], [], []
    t_total = 0.0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for src in files:
            work = tmp / src.name
            shutil.copy2(src, work)
            raw = work.read_bytes()
            text = raw.decode("utf-8")
            t0 = time.perf_counter()
            res = lint(text)
            t_total += time.perf_counter() - t0
            for c in res.changes:
                rows.append({"file": src.name, "kind": src.suffix[1:], **c.__dict__})
            p = subprocess.run([sys.executable, str(SCRIPTS / "fawiki.py"), "apply", work.name], cwd=tmp,
                               capture_output=True, text=True, encoding="utf-8")
            applied = work.read_bytes().decode("utf-8")
            problems = []
            if p.returncode != 0:
                problems.append(f"apply exit {p.returncode}: {p.stderr.strip()[:120]}")
            if applied != res.fixed:
                problems.append("apply result differs from lint()")
            if protected_chunks(text) != protected_chunks(applied):
                problems.append("protected region changed")
            if src.suffix == ".wikitext" and inventory(text) != inventory(applied):
                problems.append("template/link inventory changed")
            if text.count("\n") != applied.count("\n"):
                problems.append("newline count changed")
            if res.changes:
                q = subprocess.run([sys.executable, str(SCRIPTS / "fawiki.py"), "undo", work.name], cwd=tmp,
                                   capture_output=True, text=True, encoding="utf-8")
                if q.returncode != 0 or work.read_bytes() != raw:
                    problems.append("undo not byte-identical")
            if list(tmp.glob(src.name + ".fawiki*")):
                problems.append("backup files left behind")
            work.unlink()
            per_file.append({"file": src.name, "kind": src.suffix[1:], "chars": len(text),
                             "changes": len(res.changes), "warnings": len(res.warnings),
                             "per_1k_chars": round(1000 * len(res.changes) / max(len(text), 1), 2)})
            failures += [{"file": src.name, "problem": pr} for pr in problems]
    (out / "changes.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    summary = {"tag": a.tag, "files": len(files), "changes": len(rows), "failures": failures,
               "lint_seconds_total": round(t_total, 2), "by_kind": {}}
    for kind in ("wikitext", "txt"):
        rates = [f["per_1k_chars"] for f in per_file if f["kind"] == kind]
        if rates:
            q = statistics.quantiles(rates, n=4) if len(rates) > 1 else [rates[0]] * 3
            summary["by_kind"][kind] = {"files": len(rates), "chars": sum(f["chars"] for f in per_file if f["kind"] == kind),
                                        "changes": sum(f["changes"] for f in per_file if f["kind"] == kind),
                                        "per_1k_median": round(statistics.median(rates), 2),
                                        "per_1k_p25": round(q[0], 2), "per_1k_p75": round(q[2], 2),
                                        "per_1k_min": min(rates), "per_1k_max": max(rates)}
    (out / f"summary-{a.tag}.json").write_text(json.dumps({**summary, "per_file": per_file}, ensure_ascii=False, indent=2),
                                               encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "failures"}, ensure_ascii=False, indent=2))
    print(f"mechanical failures: {len(failures)}")
    for f in failures[:20]:
        print(f"  {f['file']}: {f['problem']}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
