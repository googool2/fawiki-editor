#!/usr/bin/env python3
"""fawiki — one entry point for the fawiki-editor scripts (stdlib only, offline).

Sub-commands:
  scan FILE      plan: orthography changes (with ids) + structure issues; writes nothing
  report FILE    the same as one compact line per rule / check (for a model to read)
  apply FILE     apply changes (all, or --only 3-7,9 / --rules FA20-FA23), with backup
  undo FILE      restore the backup made by the last apply, byte for byte
  check FILE     structure checks only (wikitext_check)
  cite ...       build a {{یادکرد …}} (cite_builder; the only networked tool)
  infobox ...    build an infobox (infobox_builder)

Safety: scan never writes. apply saves FILE.fawiki.bak and FILE.fawiki.json (SHA-256 of the
original and the result) and replaces FILE last. undo refuses if FILE changed since apply
(--force overrides). Warnings (FWxx) are never applied. Protected names (README, LICENSE,
CLAUDE.md, .env*, files under .git/.github/.claude) are refused.

Exit codes: 0 ok, 1 findings (scan/check/report) or refused action, 2 usage error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fa_lint  # noqa: E402
import wikitext_check  # noqa: E402
from fawiki_common import __version__, read_input, utf8_stdio, write_text_atomic  # noqa: E402

PROTECTED_NAMES = ("readme", "license", "claude.md", "changelog")
PROTECTED_DIRS = {".git", ".github", ".claude"}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(file: str) -> tuple[Path, Path, Path]:
    p = Path(file)
    return p, p.with_name(p.name + ".fawiki.bak"), p.with_name(p.name + ".fawiki.json")


def _refuse_protected(p: Path) -> str | None:
    low = p.name.lower()
    if low.startswith(PROTECTED_NAMES) or low.startswith(".env"):
        return f"refusing to modify protected file {p.name}"
    if PROTECTED_DIRS & set(p.resolve().parts):
        return f"refusing to modify a file under {', '.join(sorted(PROTECTED_DIRS))}"
    return None


def _lint_opts(a) -> tuple[set[str], set[int] | None]:
    rules = fa_lint.parse_ranges(a.rules, "rule", fa_lint.RULE_IDS) if a.rules else set(fa_lint.RULE_IDS)
    if getattr(a, "disable", None):
        rules -= fa_lint.parse_ranges(a.disable, "rule", fa_lint.RULE_IDS)
    only = fa_lint.parse_ranges(a.only, "id") if getattr(a, "only", None) else None
    return rules, only


def cmd_scan(a, compact: bool = False) -> int:
    text = read_input(a.file)
    rules, _ = _lint_opts(a)
    md = a.file.lower().endswith(".md")
    res = fa_lint.lint(text, rules, markdown=md)
    issues = [] if md else wikitext_check.check(text)
    name = Path(a.file).name
    if a.json:
        print(json.dumps({"version": __version__, "file": name,
                          "changes": [c.__dict__ for c in res.changes], "warnings": res.warnings,
                          "issues": [i.__dict__ for i in issues]}, ensure_ascii=False, indent=2))
    elif compact:
        print(fa_lint.format_summary(res, name))
        print(_compact_issues(issues, name))
    else:
        print(fa_lint.format_report(res, name))
        print(wikitext_check.format_report(issues, name))
        if res.changes:
            print(f"next: fawiki.py apply {a.file}            # all {len(res.changes)} change(s)")
            print(f"      fawiki.py apply {a.file} --only 1-{min(3, len(res.changes))}   # a subset, by id")
    errors = any(i.severity == "E" for i in issues)
    return 1 if res.changes or errors else 0


def _compact_issues(issues, name: str) -> str:
    e = sum(i.severity == "E" for i in issues)
    w = sum(i.severity == "W" for i in issues)
    out = [f"wikitext_check {__version__}: {name}: {e} error(s), {w} warning(s)"]
    groups: dict[str, list] = {}
    for i in issues:
        groups.setdefault((i.severity, i.code), []).append(i)
    for (sev, code), items in groups.items():
        lines = fa_lint._ranges([i.line for i in items])
        out.append(f"  {sev} {code} x{len(items)} lines {lines}: {items[0].message[:110]}")
    return "\n".join(out)


def cmd_apply(a) -> int:
    p, bak, journal = _paths(a.file)
    why = _refuse_protected(p)
    if why:
        print(why, file=sys.stderr)
        return 1
    if journal.exists() and not a.force:
        print(f"{journal.name} exists: run 'fawiki.py undo {a.file}' first, or pass --force", file=sys.stderr)
        return 1
    raw = p.read_bytes()
    text = read_input(a.file)
    rules, only = _lint_opts(a)
    md = a.file.lower().endswith(".md")
    plan = fa_lint.lint(text, rules, markdown=md)
    if only is not None:
        known = {c.id: c for c in plan.changes}
        missing = sorted(only - set(known))
        if missing:
            print(f"unknown change id(s) {fa_lint._ranges(missing)}: run 'fawiki.py scan' with the same options",
                  file=sys.stderr)
            return 1
        res = fa_lint.lint(text, rules, markdown=md, select=only)
        drift = [c.id for c in res.changes if (c.rule, c.line, c.before) != (known[c.id].rule, known[c.id].line, known[c.id].before)]
        if drift or {c.id for c in res.changes} != only:
            print("selected changes depend on skipped ones; apply them together or re-scan", file=sys.stderr)
            return 1
    else:
        res = plan
    if res.fixed == text:
        print("nothing to apply")
        return 0
    if a.dry_run:
        print(fa_lint.format_report(res, p.name))
        return 0
    shutil.copy2(p, bak)
    new_bytes = res.fixed.encode("utf-8")
    journal.write_text(json.dumps({"version": __version__, "file": p.name, "original_sha256": _sha(raw),
                                   "result_sha256": _sha(new_bytes), "changes": len(res.changes),
                                   "ids": [c.id for c in res.changes]}, indent=2), encoding="utf-8")
    write_text_atomic(p, res.fixed)
    print(fa_lint.format_summary(res, p.name))
    issues = [] if md else wikitext_check.check(res.fixed)
    print(_compact_issues(issues, p.name))
    print(f"backup: {bak.name}  (undo: fawiki.py undo {a.file})")
    return 0


def cmd_undo(a) -> int:
    p, bak, journal = _paths(a.file)
    if not journal.exists() or not bak.exists():
        print(f"no backup for {p.name} (expected {bak.name} and {journal.name})", file=sys.stderr)
        return 1
    meta = json.loads(journal.read_text(encoding="utf-8"))
    current = _sha(p.read_bytes()) if p.exists() else None
    if current != meta["result_sha256"] and not a.force:
        print(f"{p.name} changed after apply; undo would discard those edits. Use --force to restore anyway.",
              file=sys.stderr)
        return 1
    if _sha(bak.read_bytes()) != meta["original_sha256"]:
        print(f"{bak.name} does not match the journal; not restoring", file=sys.stderr)
        return 1
    tmp = p.with_name(p.name + ".fawiki.tmp")
    shutil.copy2(bak, tmp)
    tmp.replace(p)
    bak.unlink()
    journal.unlink()
    print(f"restored {p.name} ({meta['changes']} change(s) undone, sha256 {meta['original_sha256'][:12]}…)")
    return 0


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("cite", "infobox"):
        mod = __import__("cite_builder" if argv[0] == "cite" else "infobox_builder")
        return mod.main(argv[1:])
    ap = argparse.ArgumentParser(prog="fawiki.py", description="fawiki-editor tools",
                                 epilog="cite ... and infobox ... forward to cite_builder.py / infobox_builder.py")
    ap.add_argument("--version", action="version", version=f"fawiki-editor {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(sp, only=False):
        sp.add_argument("file")
        sp.add_argument("--rules", help="rule ids or ranges, e.g. FA01,FA20-FA23")
        sp.add_argument("--disable", help="rule ids or ranges to skip")
        if only:
            sp.add_argument("--only", help="change ids or ranges from scan, e.g. 1-4,9")
        return sp

    for name, helptext in (("scan", "plan only; writes nothing"), ("report", "compact summary")):
        sp = common(sub.add_parser(name, help=helptext))
        sp.add_argument("--json", action="store_true")
    sp = common(sub.add_parser("apply", help="apply changes with a backup"), only=True)
    sp.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    sp.add_argument("--force", action="store_true", help="overwrite an existing backup")
    sp = sub.add_parser("undo", help="restore the last backup")
    sp.add_argument("file")
    sp.add_argument("--force", action="store_true", help="restore even if the file changed after apply")
    sp = sub.add_parser("check", help="structure checks only")
    sp.add_argument("file")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--strict", action="store_true")
    sub.add_parser("cite", help="build a citation (see cite_builder.py -h)")
    sub.add_parser("infobox", help="build an infobox (see infobox_builder.py -h)")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "scan":
            return cmd_scan(a)
        if a.cmd == "report":
            return cmd_scan(a, compact=True)
        if a.cmd == "apply":
            return cmd_apply(a)
        if a.cmd == "undo":
            return cmd_undo(a)
        if a.cmd == "check":
            return wikitext_check.main([a.file] + (["--json"] if a.json else []) + (["--strict"] if a.strict else []))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    except OSError as e:
        print(f"{e.filename or a.file}: {e.strerror}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
