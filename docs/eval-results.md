# Eval results (2026-10-21)

Runs used the `skill-creator` tooling: `scripts/run_eval.py` for triggering and paired
subagent runs (with the skill vs. without any skill) for outputs. Raw transcripts are not
committed; this page records the numbers and what they showed.

## 1. Triggering (`evals/triggers.json`)

10 prompts (5 should trigger, 5 should not), 3 runs each, `claude -p`, threshold 0.5.

| Description version | Result | Runs |
|---|---|---|
| v0 (first draft) | see note | — |
| v1 (current: front-loaded Persian trigger words, "Use this skill for ANY task about Persian Wikipedia …") | **10/10 passed** | should-trigger 15/15 runs, should-not 0/15 runs |

Note on v0: the first two runs used `--num-workers 10` and scored 5/10. That number is not
valid: `run_eval.py` puts every worker's temporary skill command, all with the same
description, into one `.claude/commands/` folder, so a run often invoked *another* worker's
copy and was scored as "not triggered". With one worker the measurement is clean. The
serial v0 result is: V0_RESULT.

Harder near-miss set (`evals/triggers-hard.json`, 4 should / 4 should-not, e.g. an English
request about fawiki notability vs. a Persian Instagram caption or a fa.wiki dump script):
HARD_RESULT.

## 2. Output scenarios (`evals/outputs.json`, scenarios 1–3)

| Scenario | With skill | Without skill |
|---|---|---|
| 1. Write a stub on پل خواجو (offline) | 7/7 | 5/7 |
| 2. Review `article-bad.wikitext` | 5/5 | 3/5 |
| 3. Translate the Lake Urmia excerpt | 5/5 | 4/5 |
| **Pass rate** | **100%** | **70% ± 10%** |
| Time per run | 101.8 s ± 10.7 | 65.7 s ± 26.0 |
| Tokens per run | 87.9k ± 5.1k | 57.7k ± 4.6k |

Every final wikitext (both configurations) passed `wikitext_check.py` with 0 errors and
`fa_lint.py --check` with 0 changes, so the scripts confirmed structure and orthography for
all six outputs. The difference is in what the baseline does not know:

- **Attribution and AI disclosure.** Only the skill runs gave a `{{صفحه ترجمه‌شده}}` talk-page
  template, an edit summary crediting `[[:en:Lake Urmia]]`, and the «یادآوری» notice.
- **Notability.** Only the skill run checked سرشناسی (and warned that «پل خواجو» probably
  already has an article) before drafting.
- **Sources.** The baseline attached three books it had not opened to specific claims. The
  skill run cited nothing it could not verify offline, tagged claims `{{مدرک}}`, and listed
  the same books as leads to check. This is the behaviour fa.wiki's ع۱۵ criterion and
  تأییدپذیری call for; SKILL.md now states the "leads, not refs" rule explicitly.
- **Templates untouched.** In the review task the baseline edited a parameter inside
  `{{یادکرد وب}}` (`کد زبان` → `زبان`); the skill run left the citation byte-identical and
  fixed orthography through `fa_lint.py`.

Cost: the skill adds about 36 s and 30k tokens per task, mostly reading SKILL.md and one or
two references and running the scripts.

## 3. Deterministic checks

- `article-bad.wikitext`: `fa_lint.py` + `wikitext_check.py` report exactly the 10 planted
  errors (FA01, FA02, FA40, FA04, FA21, FA20, FA30; WC06, WC03, WC05).
- `article-good.wikitext`: 0 lint changes, 0 structural errors or warnings.
- `README.fa.md`: passes `fa_lint.py --check`.
- `pytest`: all tests pass, including byte-identity of 20+ kinds of protected region.
