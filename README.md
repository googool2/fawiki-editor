# fawiki-editor

**An Agent Skill that helps Claude write, translate, review and lint articles for Persian
Wikipedia ([fa.wikipedia.org](https://fa.wikipedia.org)) the way fa.wiki expects.**

[فارسی](README.fa.md)

## The problem

General-purpose models write Persian Wikipedia text that looks fine but gets reverted or
deleted: Arabic «ي/ك» instead of Persian «ی/ک», missing نیم‌فاصله (ZWNJ), Latin digits,
English templates (`{{cite web}}`, `{{Reflist}}`), invented citations, promotional tone,
topics that fail notability, and translations without attribution. fa.wiki even has a
speedy-deletion criterion (ع۱۵) for unreviewed LLM text, whose signs include fake ISBNs and
dead links.

This skill is the **Persian layer**. It packs fa.wiki's own conventions (شیوه‌نامه,
orthography, titles, dates, Persian citation and infobox templates, notability and deletion
practice) into references Claude reads on demand, plus deterministic scripts so mechanical
fixes never depend on the model's memory.

## What's inside

| Path | What it does |
|---|---|
| `SKILL.md` | The workflow: identify the task, notability gate, sourcing rules, run the scripts, deliver with an AI-use notice |
| `references/` | `orthography.md`, `titles.md`, `dates-numbers.md`, `citations.md`, `infoboxes.md`, `article-structure.md`, `notability-deletion.md`, `translation.md`; every rule cites a fa.wiki page or fa.wiki tool code, or is tagged `[UNVERIFIED]` |
| `scripts/fa_lint.py` | Fixes Persian orthography in prose only: ی/ک, ۰-۹, ٬ ٫ ٪, ZWNJ for می/ها/ترین, هٔ, ، ؛ ؟ « », spacing, a curated misspelling list. Never touches `{{ }}`, `[[ ]]`, `<ref>`, `<nowiki>`, URLs, comments or table attributes. Prints a diff and a report |
| `scripts/wikitext_check.py` | Structural checks: unbalanced brackets, unclosed `<ref>`, missing `{{پانویس}}`, no category, no bold title, unknown/English templates, non-standard headings, legacy interlanguage links |
| `scripts/cite_builder.py` | Builds `{{یادکرد وب/کتاب/ژورنال}}` from a URL, DOI or ISBN (the only script allowed to use the network; `--offline` gives a skeleton with TODO fields) |
| `scripts/infobox_builder.py` | Builds ten common fa.wiki infoboxes from simple YAML/JSON |
| `examples/` | A clean article, a broken one with 10 deliberate errors, a translation before/after |
| `tests/` | pytest suite (protected-region guarantees, every rule, every script) |
| `evals/` | Trigger evals and output scenarios with acceptance criteria |
| `docs/research-summary.md` | Where every rule came from, and what still needs live verification |

## Install

Requirements: Python 3.10+. Optional: `pip install mwparserfromhell` (better template
detection; everything works without it).

**Claude Code: as a personal skill**

```bash
git clone https://github.com/googool2/fawiki-editor ~/.claude/skills/fawiki-editor
```

**Claude Code: as a plugin**

```text
/plugin marketplace add googool2/fawiki-editor
/plugin install fawiki-editor@fawiki-tools
```

Use one method, not both, to avoid a duplicate skill.

**claude.ai**: build a zip whose top-level folder is `fawiki-editor/`, then upload it under
Settings → Capabilities → Skills:

```bash
git archive --format=zip --prefix=fawiki-editor/ -o fawiki-editor.zip HEAD
```

**Codex CLI**: clone into the user skills folder (per the Codex skills docs, `~/.agents/skills`):

```bash
git clone https://github.com/googool2/fawiki-editor ~/.agents/skills/fawiki-editor
```

## Usage

Just ask, in Persian or English:

- «یه مقاله ویکی‌پدیا فارسی درباره پل خواجو بنویس»
- «این مقاله رو طبق شیوه‌نامه ویکی‌فا چک کن»
- «این مقاله انگلیسی رو برای ویکی‌فا ترجمه کن»
- «یادکرد وب برای این لینک بساز: https://…»
- «چرا مقاله‌م حذف شد؟»

The scripts also work on their own:

```bash
python3 scripts/fa_lint.py draft.wikitext            # report + diff, file untouched
python3 scripts/fa_lint.py draft.wikitext --fix      # apply
python3 scripts/wikitext_check.py draft.wikitext     # exit 1 on structural errors
python3 scripts/cite_builder.py 978-964-8165-81-4 --offline
python3 scripts/infobox_builder.py --template film --skeleton
```

## Before / after

From [`examples/translation-before-after.md`](examples/translation-before-after.md):

```wikitext
'''Lake Urmia''' is an [[endorheic lake|endorheic]] [[salt lake]] in [[Iran]].<ref>{{cite web |url=https://www.britannica.com/place/Lake-Urmia |title=Lake Urmia |website=Encyclopaedia Britannica |access-date=12 March 2024}}</ref>
== References ==
{{Reflist}}
[[Category:Lakes of Iran]]
```

becomes

```wikitext
'''دریاچهٔ ارومیه''' یک [[دریاچهٔ بسته|دریاچهٔ بستهٔ]] شور در [[ایران]] است.<ref>{{یادکرد وب
| عنوان = Lake Urmia
| نشانی = https://www.britannica.com/place/Lake-Urmia
| وبگاه = Encyclopaedia Britannica
| کد زبان = en
| تاریخ بازبینی = 2024-03-12
}}</ref>
== منابع ==
{{پانویس}}
[[رده:دریاچه‌های ایران]]
```

plus an edit summary that credits `[[:en:Lake Urmia]]` and discloses AI help, the talk-page
box `{{صفحه ترجمه‌شده|en|Lake Urmia}}`, and a list of link targets the user must confirm.

## Limitations

- **No live access to fa.wiki during research.** wikipedia.org was unreachable from the
  build environment. Rules come from search-engine excerpts of fa.wiki pages and from the
  source code of fa.wiki's own tools (the cosmetic-changes bot, the ابرابزار gadget port and
  the اشتباه‌یاب lists in PersianWikipedia/fawikibot, plus the citer citation generator).
  Anything tagged `[LOW]` or `[UNVERIFIED]` should be checked on the live page; the full list
  is in `docs/research-summary.md`.
- Infobox parameter names are mostly `[LOW]` confidence; compare them with the template docs.
- The linter is conservative on purpose: it leaves link labels and template parameters alone
  and only warns on ambiguous patterns («تر», «ه ی», straight quotes, honorifics).
- The scripts cannot tell whether a page, category or template exists on fa.wiki.
- The skill never edits Wikipedia. You publish, and you stay responsible for the text.

## Relation to Wikipedia-AI-Skills

[fuzheado/Wikipedia-AI-Skills](https://github.com/fuzheado/Wikipedia-AI-Skills) covers
general Wikimedia tooling: AST-based wikitext parsing, CS1 citations, quality assessment,
OAuth and APIs. fawiki-editor does not duplicate that. It adds what is specific to Persian
Wikipedia, works on its own, and tells Claude to use `wikimedia-wikitext` from that collection
for AST-level work when it is installed.

## Development

```bash
pip install pytest mwparserfromhell
python3 -m pytest -q
python3 scripts/fa_lint.py README.fa.md --check   # the Persian README must stay lint-clean
```

## Credits and license

MIT (see `LICENSE`). The verb-stem list (`scripts/data/verb_stems.json`) and the misspelling
subset (`scripts/data/dictation.json`) come from
[PersianWikipedia/fawikibot](https://github.com/PersianWikipedia/fawikibot) (MIT, © Persian
Wikipedia), with line-level attribution inside the files. Citation parameter names were checked
against [5j9/citer](https://github.com/5j9/citer).
