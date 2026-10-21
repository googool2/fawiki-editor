# fawiki-editor v0.2.0

A Claude skill for writing, translating and reviewing **Persian Wikipedia** (fa.wikipedia.org)
articles the way fa.wiki expects: style guide, Persian templates, real sources only.

## Install

```text
/plugin marketplace add googool2/fawiki-editor
/plugin install fawiki-editor@fawiki-tools
```
Or copy `skills/fawiki-editor` into `~/.claude/skills/`.

## What it does
- Notability verdict before drafting; `{{مدرک}}` instead of invented citations.
- en.wiki → fa.wiki translation with Persian templates, edit-summary attribution and the
  `{{صفحه ترجمه‌شده}}` talk-page box.
- `fawiki.py scan | apply | undo`: deterministic orthography fixes (ی/ک, ۰-۹, نیم‌فاصله, هٔ,
  ، ؛ ؟ «») that never touch templates, links, refs or URLs, with a byte-exact undo.
- Citation builder (URL/DOI/ISBN, `--offline`), ten infobox templates, structure checks.

## Measured
- 88 real fa.wiki articles, every automatic change labeled by hand: 12 wrong of 759 before the
  rehearsal fixes, **0 wrong of 742** in v0.2.0; protected regions never changed.
- 18 headless agent runs: **95.7%** of checks passed with the skill vs **76.8%** without.
- Synthetic benchmark green on Linux, macOS and Windows, Python 3.10 and 3.13.

## Honest note
The agent gain (+18.9 points) is short of the +20 we aimed for and costs about twice as many
tokens; in the writing task the skill never stated a notability verdict (SKILL.md is fixed,
not yet re-measured). Rules were researched without live access to fa.wiki, and no native
fa.wiki editor has reviewed the skill yet.

Full list: [CHANGELOG](https://github.com/googool2/fawiki-editor/blob/main/CHANGELOG.md)
