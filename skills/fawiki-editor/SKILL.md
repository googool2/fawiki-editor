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
compatibility: Python 3.10+ (stdlib; mwparserfromhell optional). Only `fawiki.py cite` without --offline uses the network.
---

# fawiki-editor

fa.wiki's own conventions (شیوه‌نامه, orthography, Persian templates, notability, deletion)
plus deterministic scripts. `F` = `python3 SKILL_DIR/scripts/fawiki.py`, where `SKILL_DIR`
is the folder holding this file. Keep replies short; let the scripts do mechanical work.

## Rules that are not negotiable
1. **Never edit Wikipedia.** Output is wikitext the user reviews and publishes.
2. **Never invent sources**: no made-up URLs, ISBNs, DOIs, pages, quotes, dates or authors.
   Fake citations are a listed sign for speedy deletion **ع۱۵**. Without a real source,
   write `{{مدرک}}` or drop the claim, and say which claims need sources.
3. **Translations carry attribution**: an edit summary naming and linking the source, and
   `{{صفحه ترجمه‌شده|en|<title>}}` on the talk page (`translation.md`).
4. **AI use is disclosed.** fa.wiki pages require human review of LLM text and disclosure
   in the edit summary. Show the «یادآوری» below with every draft.
5. **Do not hand-fix orthography**; run the scripts. Warnings (FWxx) are never auto-applied.

## 1. Identify the task, then read only what it needs
| Task | Read |
|---|---|
| write a new article | `references/workflows.md` §Write, `notability-deletion.md` §1, `article-structure.md` |
| translate from en.wiki | §Translate, `translation.md`, `citations.md` |
| review a draft | §Review (`orthography.md` only to explain findings) |
| citation / infobox | §Build a citation / §Build an infobox |
| why was it deleted | §Explain a deletion, `notability-deletion.md` §5–§9 |

Also: `titles.md` (naming, disambiguation, transliteration), `dates-numbers.md`.

## 2. Check loop for every wikitext you hand over
```bash
F scan draft.wikitext        # plan: changes with ids + structure issues; writes nothing
F apply draft.wikitext       # all changes (or --only 1-4,9 / --rules FA20-FA23); keeps a backup
F report draft.wikitext      # compact recheck: one line per rule / check code
F undo draft.wikitext        # restore the pre-apply file byte for byte
```
Hand over only text with **0 fa_lint changes and 0 structure errors**. Summarize the
reports in two lines; don't paste raw output unless asked. Whitespace-only changes are not
worth an edit on their own. If Wikipedia-AI-Skills is installed, use its
`wikimedia-wikitext` skill for AST-level template surgery.

## 3. When the user has to decide
For a warning, a doubtful fact, or a link or category that may not exist: say what it is,
where (line), why it matters (rule and reference), the options, then ask one plain
question in the user's language. No jokes, no pet names. No answer means no change.

## 4. Deliver (in the user's language, usually Persian)
1. The wikitext in one fenced block.
2. Check result, e.g. «fa_lint: ۰ تغییر — wikitext_check: ۰ خطا، ۱ هشدار».
3. What the user must verify: `{{مدرک}}` claims, unconfirmed links and categories,
   infobox parameter names, TODO citation fields, sources listed as leads.
4. Translations: the edit summary and the talk-page template.
5. This notice:

> **یادآوری:** این متن با کمک هوش مصنوعی تهیه شده است. پیش از انتشار، تک‌تک ادعاها و
> منابع را خودتان بررسی کنید و از وجود و درستی هر منبع مطمئن شوید؛ متن را به زبان و سبک
> خودتان بازنویسی کنید؛ و در خلاصهٔ ویرایش صراحتاً ذکر کنید که از هوش مصنوعی کمک
> گرفته‌اید. انتشار متنی که صرفاً با مدل زبانی تولید شده و بازبینی نشده، ممکن است به حذف
> سریع مقاله (معیار ع۱۵) بینجامد.

## Limits
Rules come from search excerpts of fa.wiki pages and from fa.wiki's own tool code (no live
page reads during research); `[LOW]`/`[UNVERIFIED]` items in the references deserve a live
check when they matter. The scripts cannot tell whether a page, category or template exists.
