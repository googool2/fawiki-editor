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

## [Unreleased]

## [0.2.1] - 2026-10-22

### Fixed (from live runs on current fa.wiki articles)
Four runs of `.github/workflows/live.yml` on 2026-10-21 (240 random current articles, every
change read by hand). With the v0.2.0 rules, 109 of 668 changes on 120 articles were wrong, all
in one article; after the fixes below, 0 of 475 on another 120. Counts: `bench/live-results.json`.
- **FA01/FA02** changed ي/ك/ى inside Uyghur place names (109 changes in one article). The masker
  now protects runs of Arabic-script words that contain letters Persian never uses (Uyghur,
  Kurdish, Urdu, Pashto, Sindhi, Kazakh), including neighbouring words with ي/ك/ى joined by
  spaces, parentheses or direction marks. New synthetic trap and regression tests.
- **FA42** inserted spaces inside chains of initials and acronyms («آ.ای.اچ.» → «آ.ای. اچ.»,
  «دی.آی.سی.ای»). Chains of three or more short segments are left alone; two initials
  («اچ.جی.») still get a space. It also no longer puts a space after a namespace colon in plain
  text («ویکی‌پدیا:شیوه‌نامه»), which linting the new review docs showed.
- **FA40** removed the space in list items that start with a dot (`* .us` → `*.us`; renders the
  same). It now skips `*` and `#`.

### Fixed (template and parameter names, checked live)
`bench/live_check.py templates` compares every name the skill emits with the live TemplateData,
template source and invoked module.
- Infoboxes: 117 of 123 parameter names confirmed. Fixed: film `مدت زمان` → `مدت`; country
  `نام رایج` → `نام عادی`, `تصویر نشان` → `تصویر نشان ملی`, `زبان‌های رسمی` → `زبان(های) رسمی`;
  musical artist `پیش‌زمینه` → `پس‌زمینه`, and `سازهای برجسته` removed (no such parameter). All
  ten boxes are now confidence `LIVE`; `references/infoboxes.md` tags each checked name [LIVE].
- `{{کنترل مرجعیت}}` and `{{تک}}` do not exist on fa.wiki. Authority control maps to
  `{{داده‌های کتابخانه‌ای}}`; Short description to `{{توصیف کوتاه}}`; en `{{References}}` to
  `{{بدون منبع}}` (its interlanguage link).
- **Unresolved:** `{{یادکرد کتاب}}` `نویسنده`, `ترجمه` and `{{یادکرد ژورنال}}` `نویسنده`, `جلد`,
  `ناشر` are missing from TemplateData, the template source and the invoked module, but
  fa.wiki's citer tool emits them. Left unchanged and listed as a question for reviewers.

### Added
- `.github/workflows/live.yml`: monthly live check (template names, 60 random current articles,
  a fixed regression list in `bench/live-titles.txt`). `bench/label.py --context`.
- Review kit: `docs/review/REVIEWING.md` (every rule in Persian, how votes are used),
  `docs/review/call-fa.md` (a draft call for reviewers; not posted), and an issue form.

### Changed
- `bench/label.py`: FA01/FA02 inside another language now count as wrong (they were labeled
  correct), and the Latin-context test ignores templates, link targets and tags (it had called
  5 correct digit fixes wrong). Labels on the 88-article corpus are unchanged: 12 wrong before
  the v0.2.0 fixes, 0 after.

### Measured
- Re-measured the writing task on the released v0.2.0 SKILL.md (3 headless runs, same harness,
  model, prompt and grader): 7 of 7 checks in every run, including a reasoned notability verdict
  that the first round never gave. Combined with the earlier review and translation runs, checks
  passed rise from 95.7% to 100% with the skill (76.8% without), a gain of +23 points.
- `bench/agents.py --configs` runs a single setting; `bench/charts.py` plots the current numbers.

## [0.2.0] - 2026-10-21

### Added
- `fawiki.py` command with `scan | report | apply | undo | check | cite | infobox` and
  `--version`. `apply` keeps `FILE.fawiki.bak` plus a SHA-256 journal; `undo` restores byte
  for byte and refuses if the file changed after `apply`. Protected file names are refused.
- Change ids with ranges (`--only 1-4,9`) and rule ranges (`--rules FA20-FA23`); a grouped
  one-line-per-rule summary for models.
- Synthetic benchmark (`bench/bench.py`) with planted errors and traps; CI on Linux, macOS
  and Windows with Python 3.10 and 3.13; `docs/design.md`.

### Fixed (from the real-world rehearsal)
Ran every rule on 88 real fa.wiki articles (48 wikitext, 40 plain text) and labeled all 759
automatic changes by hand: 738 correct, 9 debatable, **12 wrong (1.6%)**. Root causes, fixed:
- **FA04** turned Latin digits into Persian ones inside English bibliographies and titles
  (`''Journal'' 15(3): 296–313`). It now skips numbers where Latin letters dominate the line.
- **FA07** read «۷۰۰.۰۰۰ یورو» (dot as thousands separator) as a decimal. Three-digit groups
  are now left alone and reported as the new warning **FW09**; version numbers after
  «نسخه/ویرایش» are skipped too.
- **FA40** glued a full stop onto an ellipsis («و... .» → «و....»).
- **FA42** split the abbreviation «ه.ق» and initials («ی.س.باخ»); it now needs two letters on
  each side of «.» or «:».
After the fixes, the same corpus gives 742 changes: 738 correct, 4 debatable, **0 wrong**, and
0 mechanical failures (protected regions intact, undo byte-identical for every file).

### Changed
- Standard plugin layout: the skill now lives in `skills/fawiki-editor/`.
- SKILL.md trimmed to about 1.5k tokens; task detail moved to `references/workflows.md`.
- Writes are atomic, CRLF line endings are preserved, output is UTF-8 on every console.
- `wikitext_check` treats CRLF input like LF (headings were missed on Windows files).

## [0.1.0] - 2026-10-21

### Added
- First version: SKILL.md, eight sourced reference files, `fa_lint.py`, `wikitext_check.py`,
  `cite_builder.py`, `infobox_builder.py`, examples, pytest suite, trigger and output evals.
