# fawiki-editor: design (one page)

## Job
Help an editor produce Persian Wikipedia (fa.wikipedia.org) wikitext that survives review:
correct Persian orthography, fa.wiki templates and structure, real sources only, attribution
for translations, and an honest notability call before anyone writes a page that will be
deleted. Output is always wikitext for the user to publish; the skill never edits Wikipedia.

## Triggers
Persian or English requests that name or clearly mean Persian Wikipedia: «مقاله ویکی‌پدیا
بنویس»، «طبق شیوه‌نامه ویکی‌فا چک کن»، «برای ویکی‌فا ترجمه کن»، «یادکرد بساز»، «جعبه
اطلاعات»، «چرا مقاله‌م حذف شد»، "fawiki", "Persian Wikipedia draft". Not: Persian text that
is not for Wikipedia (blogs, letters, captions), English Wikipedia with no Persian angle,
general questions about Iran or about Wikipedia statistics, private MediaWiki installs.

## Success numbers
| # | Metric | Target |
|---|---|---|
| 1 | Trigger accuracy, `evals/triggers.json` + `evals/triggers-hard.json`, 3 runs each | ≥ 90% |
| 2 | Protected regions byte-identical after the most aggressive apply (synthetic benchmark) | 100% |
| 3 | Wrong automatic changes on real fa.wiki text (hand-labeled rehearsal) | 0 |
| 4 | `undo` restores the file byte for byte | 100% |
| 5 | Agent value: assertion pass rate with the skill minus without (headless runs) | ≥ +20 points |

## Safety design
The only thing the skill changes on disk is a draft file the user gave it, through
`fawiki.py apply`.

1. **Plan** (`scan`, the default): report and diff, writes nothing. Every change gets an id.
2. **Apply** (`apply`, optionally `--only 3-7,9` or `--rules FA20-FA23`): saves
   `<file>.fawiki.bak` and a journal with the SHA-256 of the original and of the result,
   then writes the new file last.
3. **Undo** (`undo`): restores the backup only if the file still matches the journal's
   result hash, so later manual edits are never clobbered (`--force` overrides).

Uncertain cases are warnings (FWxx) that are never applied: no answer means no change.
Protected regions (never modified): templates `{{…}}`, links `[[…]]`, `<ref>`, `<nowiki>`,
`<pre>`, `<math>`, `<syntaxhighlight>`, `<gallery>`, `<poem>`, comments, URLs and external
links, ISBN/PMID/RFC, magic words, signatures, table syntax and attributes, lines starting
with a space, Arabic/Urdu/Kurdish/Pashto blocks, and Markdown code in `.md` files. A
post-run assertion fails loudly if any protected byte or newline changed.

When the user must decide (a warning, a doubtful fact, a link target that may not exist),
Claude states what it is, where (line), why it matters (rule and source), the options, then
asks one plain question, in the user's language, without jokes or pet names.

## Skill vs plugin
One skill: all jobs share one trigger domain and one rule set. SKILL.md stays near 1.5k
tokens; task-specific detail lives in `references/` and loads on demand. A plugin wrapper
(`.claude-plugin/`) only adds distribution. Split into several skills only if a job gets
its own triggers (for example a bulk "fix a whole category" mode).

## Out of scope
Editing or logging in to Wikipedia, checking whether pages/categories/templates exist live,
spell-checking beyond a curated list, rewriting prose style.
