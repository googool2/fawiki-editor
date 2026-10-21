#!/usr/bin/env python3
"""Does the skill help an agent? Headless `claude -p` runs, with vs without the skill.

Each run gets a fresh folder (outside the repo) with the task's input files; the
"with_skill" folder also has `.claude/skills/fawiki-editor`. Same prompt, same tools, same
model. Grading is mechanical (see GRADERS). Results are appended to OUT/runs.jsonl after
every run, so a crash loses nothing; `--resume` skips finished runs.

Usage: python bench/agents.py OUT_DIR [--reps 3] [--tasks write,review,translate]
                              [--model claude-opus-5-5] [--workers 3] [--resume]
Then:  python bench/agents.py OUT_DIR --summarize > bench/agents-results.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "skills" / "fawiki-editor"
sys.path.insert(0, str(SKILL / "scripts"))
from fa_lint import lint  # noqa: E402
from wikitext_check import check  # noqa: E402

TOOLS = ["Read", "Glob", "Grep", "Write", "Edit", "Bash(python3:*)"]
BAD = "\n".join((SKILL / "examples" / "article-bad.wikitext").read_text(encoding="utf-8").split("\n")[1:])
EN = ("'''Lake Urmia''' is an [[endorheic lake|endorheic]] [[salt lake]] in [[Iran]].<ref>{{cite web "
      "|url=https://www.britannica.com/place/Lake-Urmia |title=Lake Urmia |website=Encyclopaedia Britannica "
      "|access-date=12 March 2024}}</ref> The lake is located between the provinces of [[West Azerbaijan Province|"
      "West Azerbaijan]] and [[East Azerbaijan Province|East Azerbaijan]].\n\n== References ==\n{{Reflist}}\n\n"
      "[[Category:Lakes of Iran]]")
TASKS = {
    "write": {"files": {}, "out": "article.wikitext", "prompt":
              "یه مقاله ویکی‌پدیا فارسی کوتاه (خرد) درباره پل خواجو در اصفهان بنویس. اینترنت ندارم، پس فقط از "
              "منابعی استفاده کن که مطمئنی. ویکی‌متن نهایی را در فایل article.wikitext همین پوشه ذخیره کن و بعد "
              "پاسخت را به من بده."},
    "review": {"files": {"article.wikitext": BAD}, "out": "corrected.wikitext", "prompt":
               "مقالهٔ فایل article.wikitext را قبل از انتشار طبق شیوه‌نامه ویکی‌فا بازبینی کن. نسخهٔ اصلاح‌شده را "
               "در فایل corrected.wikitext ذخیره کن و فهرست ایرادها را در پاسخت بده. اینترنت ندارم."},
    "translate": {"files": {"source-en.wikitext": EN}, "out": "translation.wikitext", "prompt":
                  "متن انگلیسی فایل source-en.wikitext (بخشی از مقالهٔ Lake Urmia در ویکی‌پدیای انگلیسی) را برای "
                  "ویکی‌فا ترجمه کن. ویکی‌متن فارسی را در فایل translation.wikitext ذخیره کن و هر چیزی که برای "
                  "انتشار لازم است در پاسخت بگو. اینترنت ندارم."},
}
REF_BRIT = re.search(r'<ref name="britannica">.*?</ref>', BAD, re.S).group(0)


def _clean(text: str) -> tuple[int, int]:
    return len(lint(text).changes), sum(i.severity == "E" for i in check(text))


def grade(task: str, out: str | None, reply: str) -> dict[str, bool]:
    g: dict[str, bool] = {"output file written": out is not None}
    out = out or ""
    changes, errors = _clean(out) if out else (99, 99)
    g["fa_lint: 0 changes"] = changes == 0
    g["wikitext_check: 0 errors"] = errors == 0
    g["AI use disclosed to the user"] = "هوش مصنوعی" in reply
    if task == "write":
        g["bold title in lead"] = "'''پل خواجو'''" in out or "'''پل خواجوی" in out
        g["no unverifiable citation details (URL/ISBN/DOI/page) offline"] = not re.search(
            r"https?://|شابک|isbn|doi\s*=|\|\s*صفحه\s*=\s*\S", out, re.I)
        g["notability discussed"] = "سرشناس" in reply
    elif task == "review":
        g["citation template left byte-identical"] = REF_BRIT in out
        g["peacock word «زیباترین» removed"] = "زیباترین" not in out
        g["unpublished source (interview) not kept as a ref"] = not re.search(r"<ref>[^<]*کوهنورد", out)
    else:
        g["{{یادکرد وب}} used, no {{cite web}}"] = "{{یادکرد وب" in out and "cite web" not in out.lower()
        g["source URL kept exactly"] = "https://www.britannica.com/place/Lake-Urmia" in out
        g["no [[Category:]] / [[en:]] links"] = not re.search(r"\[\[\s*(Category|en)\s*:", out)
        g["talk-page template {{صفحه ترجمه‌شده}} given"] = "صفحه ترجمه‌شده" in reply
        g["edit summary credits the source article"] = bool(re.search(r"\[\[:en:Lake[ _]Urmia", reply))
    return g


def clean_env() -> dict:
    """Inherited CLAUDE*/ANTHROPIC_BASE_URL variables would tie the child to this session."""
    return {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE") or k == "ANTHROPIC_BASE_URL")}


def run_one(out_dir: Path, task: str, cfg: str, rep: int, model: str, lock: threading.Lock) -> dict:
    work = out_dir / "runs" / f"{task}-{cfg}-{rep}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for name, text in TASKS[task]["files"].items():
        (work / name).write_text(text, encoding="utf-8")
    if cfg == "with_skill":
        shutil.copytree(SKILL, work / ".claude" / "skills" / "fawiki-editor")
    cmd = ["claude", "-p", TASKS[task]["prompt"], "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project", "--strict-mcp-config", "--model", model,
           "--allowedTools", *TOOLS]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=work, env=clean_env(), capture_output=True, text=True,
                           encoding="utf-8", timeout=900)
        stdout, rc = p.stdout, p.returncode
    except subprocess.TimeoutExpired as e:
        stdout, rc = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), -9
    (work / "transcript.jsonl").write_text(stdout, encoding="utf-8")
    final, used_skill = {}, False
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "result":
            final = ev
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use" and (c.get("name") == "Skill" or "SKILL.md" in json.dumps(c.get("input", {}))):
                    used_skill = True
    outf = work / TASKS[task]["out"]
    out_text = outf.read_text(encoding="utf-8") if outf.exists() else None
    reply = final.get("result", "") or ""
    g = grade(task, out_text, reply)
    u = final.get("usage", {})
    row = {"task": task, "config": cfg, "rep": rep, "exit": rc, "used_skill": used_skill,
           "passed": sum(g.values()), "total": len(g), "grades": g,
           "turns": final.get("num_turns"), "seconds": round(final.get("duration_ms", (time.time() - t0) * 1000) / 1000, 1),
           "cost_usd": final.get("total_cost_usd"),
           "tokens": sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                                                 "cache_read_input_tokens"))}
    with lock:
        with open(out_dir / "runs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{task:<9} {cfg:<13} rep{rep} {row['passed']}/{row['total']} turns={row['turns']} "
          f"{row['seconds']}s ${row['cost_usd']} skill={used_skill}", flush=True)
    return row


def summarize(out_dir: Path) -> dict:
    rows = [json.loads(x) for x in (out_dir / "runs.jsonl").read_text(encoding="utf-8").splitlines()]
    res: dict = {"runs": len(rows), "by_task": {}, "overall": {}}

    def stats(rs, key):
        vals = [r[key] for r in rs if r.get(key) is not None]
        return {"median": round(statistics.median(vals), 3), "min": min(vals), "max": max(vals)} if vals else None

    for cfg in ("with_skill", "without_skill"):
        rs = [r for r in rows if r["config"] == cfg]
        res["overall"][cfg] = {"pass_rate": round(sum(r["passed"] for r in rs) / max(sum(r["total"] for r in rs), 1), 3),
                               "seconds": stats(rs, "seconds"), "turns": stats(rs, "turns"),
                               "tokens": stats(rs, "tokens"), "cost_usd": stats(rs, "cost_usd"),
                               "total_cost_usd": round(sum(r["cost_usd"] or 0 for r in rs), 2),
                               "skill_used_runs": sum(r["used_skill"] for r in rs), "runs": len(rs)}
    for task in TASKS:
        res["by_task"][task] = {}
        for cfg in ("with_skill", "without_skill"):
            rs = [r for r in rows if r["task"] == task and r["config"] == cfg]
            if not rs:
                continue
            per_assert: dict[str, int] = {}
            for r in rs:
                for k, v in r["grades"].items():
                    per_assert[k] = per_assert.get(k, 0) + int(v)
            res["by_task"][task][cfg] = {"pass_rate": round(sum(r["passed"] for r in rs) / sum(r["total"] for r in rs), 3),
                                         "runs": len(rs), "assertions_passed": per_assert,
                                         "seconds_median": stats(rs, "seconds")["median"],
                                         "turns_median": stats(rs, "turns")["median"] if stats(rs, "turns") else None,
                                         "cost_median": stats(rs, "cost_usd")["median"] if stats(rs, "cost_usd") else None}
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--tasks", default="write,review,translate")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--summarize", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if HERE.parent.resolve() in out.resolve().parents:
        print("OUT must be outside the repository", file=sys.stderr)
        return 2
    if a.summarize:
        print(json.dumps(summarize(out), ensure_ascii=False, indent=2))
        return 0
    out.mkdir(parents=True, exist_ok=True)
    done = set()
    if a.resume and (out / "runs.jsonl").exists():
        done = {(r["task"], r["config"], r["rep"]) for r in map(json.loads, (out / "runs.jsonl").read_text(encoding="utf-8").splitlines())}
    jobs = [(t, c, r) for r in range(1, a.reps + 1) for t in a.tasks.split(",") for c in ("with_skill", "without_skill")
            if (t, c, r) not in done]
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(lambda j: run_one(out, *j, a.model, lock), jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
