# Changelog

All notable changes to fawiki-editor. Dates are UTC.

## Versioning policy

Semantic versioning, read from the point of view of someone's draft:

- **Major**: could change *what gets modified* in a way users must re-review: a protected
  region that is no longer protected, a warning that becomes an automatic fix, a changed
  command or output format.
- **Minor**: new rules, checks, templates or features. Never looser safety: a minor release
  may protect more, warn more or fix more *clearly unambiguous* cases, never less.
- **Patch**: bug fixes, data corrections (template/parameter names), docs.

## [0.2.0] - 2026-10-21

### Added
- `fawiki.py` command with `scan | report | apply | undo | check | cite | infobox` and
  `--version`. `apply` keeps `FILE.fawiki.bak` plus a SHA-256 journal; `undo` restores byte
  for byte and refuses if the file changed after `apply`. Protected file names are refused.
- Change ids with ranges (`--only 1-4,9`) and rule ranges (`--rules FA20-FA23`); a grouped
  one-line-per-rule summary for models.
- Synthetic benchmark (`bench/bench.py`) with planted errors and traps; CI on Linux, macOS
  and Windows with Python 3.10 and 3.13; `docs/design.md`.

### Changed
- Standard plugin layout: the skill now lives in `skills/fawiki-editor/`.
- SKILL.md trimmed to about 1.5k tokens; task detail moved to `references/workflows.md`.
- Writes are atomic, CRLF line endings are preserved, output is UTF-8 on every console.
- `wikitext_check` treats CRLF input like LF (headings were missed on Windows files).

## [0.1.0] - 2026-10-21

### Added
- First version: SKILL.md, eight sourced reference files, `fa_lint.py`, `wikitext_check.py`,
  `cite_builder.py`, `infobox_builder.py`, examples, pytest suite, trigger and output evals.
