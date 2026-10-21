---
name: fawiki-editor
description: >-
  Use this skill for ANY task about Persian Wikipedia — ویکی‌پدیای فارسی، ویکی‌پدیا فارسی،
  ویکی‌فا، fa.wikipedia.org, fawiki: writing a new مقاله ویکی‌پدیا, translating an English
  Wikipedia article for ویکی‌فا, reviewing or checking a draft against شیوه‌نامه ویکی‌فا,
  fixing ویکی‌متن / wikitext (رسم‌الخط، نیم‌فاصله، ی/ک، ارقام), building a یادکرد
  (یادکرد وب/کتاب/ژورنال) or جعبه اطلاعات, judging سرشناسی, or explaining why an
  article was deleted (حذف سریع، حذف شد). Trigger even when the request is casual, e.g.
  «مقاله ویکی‌پدیا بنویس»، «یادکرد بساز»، «چرا مقاله‌م پاک شد». Ships fa.wiki rules and
  deterministic checkers (fa_lint, wikitext_check, cite_builder, infobox_builder). Not for:
  Persian blog posts, letters or other non-Wikipedia writing; English Wikipedia with no
  Persian angle; general history questions; wikitext for private non-Wikipedia wikis.
license: MIT
compatibility: Python 3.10+ (stdlib; mwparserfromhell optional). Network is used only by scripts/cite_builder.py without --offline.
---

# fawiki-editor

The Persian layer on top of general Wikipedia know-how: fa.wiki's own style guide,
Persian templates, approved orthography, title/date conventions, notability and deletion
practice. Rules live in `references/`; mechanical work is done by `scripts/`.

`SKILL_DIR` below means the directory that contains this file. Run scripts as
`python3 SKILL_DIR/scripts/<name>.py`. Write drafts to a file (e.g. `draft.wikitext`)
so the scripts can read them.

## Non-negotiable rules

These protect the user from having their work deleted and protect fa.wiki from bad text.

1. **Never edit Wikipedia directly.** Output is wikitext the user reviews and publishes
   themselves. Do not log in, call edit APIs or submit forms, even if tools allow it.
2. **Never invent sources.** No made-up URLs, ISBNs, DOIs, page numbers, quotes, dates
   or authors. Fake citations are an explicit sign for speedy deletion under **ع۱۵**
   (LLM text without human review). If you cannot name a real source you are confident
   about, write the claim with `{{مدرک}}` or leave it out — and tell the user which claims
   still need a source. "I could not find a source for X" is a valid answer.
3. **Translations always carry attribution**: an edit summary that names and links the
   source article, plus `{{صفحه ترجمه‌شده|en|<exact source title>}}` on the *talk page*
   (not in the article). See `references/translation.md`.
4. **Respect fa.wiki's AI guidance.** fa.wiki has no comprehensive AI policy, but its
   pages say LLM output must be reviewed by a human, purely LLM-generated content must
   not be published, and AI use must be disclosed in the edit summary. Show the user the
   «یادآوری» below with every draft or translation.
5. **Do not hand-fix orthography.** Run `fa_lint.py`; it is deterministic, protects
   templates/links/refs/URLs, and is traceable to fa.wiki rules. Manual "fixes" drift.

## Step 1 — identify the task

| User wants… | Task | Read first |
|---|---|---|
| a new article («یه مقاله درباره X بنویس») | **write** | notability-deletion.md §1, article-structure.md |
| an en.wiki article in Persian | **translate** | translation.md, citations.md §English→Persian |
| a draft checked («طبق شیوه‌نامه چک کن») | **review** | orthography.md (only to explain findings) |
| a citation for a URL/DOI/ISBN («یادکرد بساز») | **cite** | citations.md |
| an infobox | **infobox** | infoboxes.md |
| to know why an article was deleted | **deletion** | notability-deletion.md §5–§9 |

Load only the reference you need. Other references: `titles.md` (naming, disambiguation,
transliteration), `dates-numbers.md` (calendars, month names, digits).

## Step 2 — run the workflow

### Write a new article
1. **Notability gate first.** Walk the checklist in `references/notability-deletion.md`
   §1 with the user: ≥2 independent, reliable, secondary sources with significant
   coverage? Own website, press releases and paid advertorials (رپورتاژ آگهی) do not count.
   If sources are not enough, say plainly that the article will probably be deleted, and
   suggest what coverage would change that. Do not draft a promotional or unsourced page.
2. **Collect sources** from the user or from tools you actually have. Build each citation
   with `cite_builder.py` (below); never type citation fields from memory. A `<ref>` says
   "this source supports this sentence", so only attach one when you (or the user) have
   seen that the source says it. Well-known works you believe cover the topic but have not
   opened go in the reply as **leads to check** (author + title only), not as `<ref>`s;
   the claim keeps `{{مدرک}}` until the user verifies it.
3. **Draft** using the skeleton in `references/article-structure.md`: bold title in the
   first sentence, short lead, sections, `== منابع ==` + `{{پانویس}}`, categories.
   Every claim has a `<ref>` or `{{مدرک}}`.
4. **Tone:** encyclopedic and neutral. No value words without attribution (no
   «بزرگ‌ترین»، «برجسته»، «بی‌نظیر» unless a cited source says it and the text says who).
   No honorifics (حضرت، مرحوم، شادروان…). For living people, contentious claims need
   strong sources or must go.
5. **Check** (Step 3), fix, repeat until clean.

### Translate from en.wiki
1. Notability still applies: en.wiki having an article is not proof for fa.wiki.
2. Rewrite in natural Persian; do not calque English syntax.
3. Convert templates and parameters (`{{cite web}}`→`{{یادکرد وب}}`, `{{Reflist}}`→
   `{{پانویس}}`, `[[Category:]]`→`[[رده:]]`, infobox → its fa template). Keep source
   titles in their original language with `کد زبان`/`زبان`.
4. Link only to fa.wiki titles you are sure exist; list the rest for the user to verify.
   Never invent fa category names; propose and flag them. No `[[en:…]]` links (Wikidata).
5. Deliver the edit summary and talk-page template from `references/translation.md` §6.
   A worked example is in `examples/translation-before-after.md`.

### Review a draft
1. Save the user's text to a file and run **both** scripts (Step 3).
2. Report findings grouped as: **orthography** (from fa_lint), **structure** (from
   wikitext_check), **content** (your reading: unsourced claims, peacock or weasel words,
   NPOV, BLP, notability risk, missing lead/categories). Cite the reference for each
   content point.
3. Offer the corrected wikitext = `fa_lint` output + your structural/content fixes, then
   re-run both scripts on it and show they pass.

### Build a citation
```bash
python3 SKILL_DIR/scripts/cite_builder.py "https://example.com/article"   # fetches metadata
python3 SKILL_DIR/scripts/cite_builder.py "10.1000/xyz" --ref --name smith2020
python3 SKILL_DIR/scripts/cite_builder.py "978-964-..." --offline          # no network
python3 SKILL_DIR/scripts/cite_builder.py URL --offline --set title="…" --set date=2024-05-01
```
Use `--offline` when the sandbox has no internet. Fields the script reports as TODO must
come from the source itself (ask the user or open the page); never guess them. An ISBN
that fails the checksum is rejected — do not "repair" it.

### Build an infobox
```bash
python3 SKILL_DIR/scripts/infobox_builder.py --list
python3 SKILL_DIR/scripts/infobox_builder.py --template film --skeleton
python3 SKILL_DIR/scripts/infobox_builder.py data.yaml     # keys: Persian names or English aliases
```
Most parameter names are marked [LOW] confidence (see the NOTE the script prints): tell
the user to compare with the template's documentation page before publishing.

### Explain a deletion
Use the diagnostic table in `references/notability-deletion.md` §8: map what the user
describes (own sources only, advertising tone, copied text, untranslated text, AI text,
no claim of importance…) to the likely criterion (e.g. ع۱۱, ع۱۲, ع۱۵, م۲, م۷), link the
fa.wiki page, and give the honest next steps from §9 (ask the deleting admin, find
independent coverage, disclose conflicts of interest per «ویکی‌پدیا:تعارض منافع»). Never
promise restoration.

## Step 3 — check every wikitext you hand over

```bash
python3 SKILL_DIR/scripts/fa_lint.py draft.wikitext -o draft.fixed.wikitext
python3 SKILL_DIR/scripts/wikitext_check.py draft.fixed.wikitext
```
- `fa_lint.py` prints each change (rule id, line, before → after) and a diff; `--check`
  exits 1 if anything would change, `--fix` rewrites in place, `--json` for parsing.
  Warnings (FWxx) are never auto-fixed: decide each one yourself.
- `wikitext_check.py` prints errors (E: brackets, unclosed `<ref>`, no `{{پانویس}}`, no
  category, no bold title) and warnings (W: unknown/English templates, non-standard
  headings, legacy interlanguage links, bare-URL refs…). Exit 1 on errors.
- Hand over only text with **0 errors** and **0 fa_lint changes**. Show the user a short
  summary of both reports (counts + anything you could not fix and why), not the raw
  dump, unless they ask.
- If the only lint changes are whitespace, say so briefly; it is not worth an edit alone.

If the [Wikipedia-AI-Skills](https://github.com/fuzheado/Wikipedia-AI-Skills) collection
is installed, use its `wikimedia-wikitext` skill for AST-level parsing or bulk template
surgery, and its citation/quality skills for general (non-Persian) tasks. This skill
works without it; `wikitext_check.py` also uses `mwparserfromhell` when present.

## Step 4 — deliver

Keep the reply short and in the user's language (usually Persian). Use this order:

1. The wikitext in one fenced block.
2. Check results: «fa_lint: ۰ تغییر — wikitext_check: ۰ خطا، N هشدار» plus any open items.
3. **What the user must verify**: claims marked `{{مدرک}}`, link targets and categories
   you could not confirm, infobox parameter names, TODO citation fields.
4. For translations: the edit summary and the talk-page template.
5. The notice:

> **یادآوری:** این متن با کمک هوش مصنوعی تهیه شده است. پیش از انتشار، تک‌تک ادعاها و
> منابع را خودتان بررسی کنید و از وجود و درستی هر منبع مطمئن شوید؛ متن را به زبان و سبک
> خودتان بازنویسی کنید؛ و در خلاصهٔ ویرایش صراحتاً ذکر کنید که از هوش مصنوعی کمک
> گرفته‌اید. انتشار متنی که صرفاً با مدل زبانی تولید شده و بازبینی نشده، ممکن است به حذف
> سریع مقاله (معیار ع۱۵) بینجامد.

## Quick reference

| Script | Purpose | Network |
|---|---|---|
| `scripts/fa_lint.py` | Persian orthography fixes outside protected regions (ی/ک, digits ۰-۹ ٬ ٫, نیم‌فاصله for می/ها/ترین, هٔ, ، ؛ ؟ « », spacing, curated misspellings) | never |
| `scripts/wikitext_check.py` | structure: brackets, refs, پانویس, رده, bold lead, templates, headings | never |
| `scripts/cite_builder.py` | `{{یادکرد وب/کتاب/ژورنال}}` from URL / DOI / ISBN | only without `--offline` |
| `scripts/infobox_builder.py` | 10 fa.wiki infoboxes from YAML/JSON | never |

`fa_lint.py --list-rules` lists every rule; sources are in `references/orthography.md`.
Research provenance and open questions: `docs/research-summary.md`.

## Known limits

- fa.wiki pages could not be fetched live while this skill was built; rules come from
  search excerpts of fa.wiki pages and from the code of fa.wiki's own tools. Items marked
  [LOW] or [UNVERIFIED] in the references should be checked on the live page when they
  matter.
- `fa_lint` is deliberately conservative: it does not touch link labels, template
  parameters or quotations inside templates, and it only warns about ambiguous cases
  («تر», straight quotes, «ه ی», honorifics, slash dates).
- The scripts cannot tell whether a fa.wiki page, category or template exists.
