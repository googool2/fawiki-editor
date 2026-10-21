# Article structure on fa.wiki: order, headings, links, maintenance tags

Load this file when you build a new article, restructure one, or review layout.
**Tags:** [V] = a search excerpt of the cited fa.wiki page confirmed it · [C] = read in fawikibot's
cosmetic-changes bot (`fa_cosmetic_changes_core.py`, `master` @ `04dde6d`, the «زیباسازی» bot that ran
on fa.wiki articles) · [LOW] = search summary only · [UNVERIFIED] = no source found. Research date: 2026-10-21.
The layout guideline is [ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی][layout]. It is a guideline («پیروی از مفادش
توصیه می‌شود اما جزو سیاست‌ها نیست»), not a policy [V].

## Contents
[1 Order of elements](#1-order-of-elements) · [2 Minimal skeleton](#2-minimal-skeleton) ·
[3 Lead](#3-lead) · [4 Headings](#4-headings) · [5 End sections](#5-end-sections) ·
[6 Bottom block: navbox → stub → sort key → categories](#6-bottom-block-navbox--stub--sort-key--categories) ·
[7 Links and interlanguage links](#7-links-and-interlanguage-links) · [8 Maintenance templates](#8-maintenance-templates) ·
[9 Translation attribution](#9-translation-attribution) · [10 Namespaces and images](#10-namespaces-and-images) ·
[11 wikitext_check codes](#11-wikitext_check-codes)

## 1. Order of elements

| # | Element | Wikitext | Tag / source |
|---|---|---|---|
| 1 | Hatnotes / disambiguation notes | hatnote templates (fa names not researched) | order [V] [صفحه‌آرایی][layout]; names [UNVERIFIED] |
| 2 | Maintenance tags | `{{سرشناسی}}`, `{{بدون منبع}}` … (§8) | [V] [صفحه‌آرایی][layout]; `{{سرشناسی}}` "at the top" [V] [الگو:سرشناسی][t-notab] |
| 3 | Infobox | `{{جعبه اطلاعات …}}` (see `infoboxes.md`) | [V] [راهنما:جعبه اطلاعات][ibox] |
| 4 | Image, sidebars | `[[پرونده:…]]` | [V] [صفحه‌آرایی][layout] |
| 5 | Lead | starts directly after the infobox's `}}`, with no blank line | [V] [layout]; [C] [L449-L455][c449] |
| 6 | Table of contents | automatic | [V] [layout] |
| 7 | Body sections | `== … ==` | [LOW] [layout] |
| 8 | End sections | جستارهای وابسته → پانویس / منابع → برای مطالعهٔ بیشتر → پیوند به بیرون | [V] [layout] (see §5) |
| 9 | Navboxes | `{{<الگوی ناوبری>}}` | [LOW] [layout] |
| 10 | Stub templates | `{{خرد}}` / `{{<موضوع>-خرد}}` | [V] [الگو:خرد][t-stub] (see §6 conflict) |
| 11 | Sort key | `{{ترتیب‌پیش‌فرض:…}}` | [LOW] [layout]; [C] [L625-L660][c626] |
| 12 | Categories | `[[رده:…]]` | [LOW] [layout]; [C] [L596-L623][c598] |

## 2. Minimal skeleton

A generic template. **Replace every `…` and `<…>` before publishing.** Unfilled placeholders are a
listed sign under speedy criterion ع۱۵ (LLM pages without human review) ([LOW] [معیارهای حذف سریع][csd];
see `notability-deletion.md` §5). Leave out any section you have no content for.

```wikitext
{{جعبه اطلاعات <نوع>
| نام = …
}}
'''عنوان مقاله''' … است.<ref name="<نام>">{{یادکرد وب | عنوان=… | نشانی=… | تاریخ بازبینی=…}}</ref> …

== <بخش اصلی> ==
{{اصلی|<مقالهٔ اصلی>}}
[[پرونده:<نام پرونده>|بندانگشتی|<توضیح تصویر>]]
…<ref>{{یادکرد کتاب | نام خانوادگی=… | نام=… | عنوان=… | ناشر=… | سال=… | صفحه=…}}</ref>

=== <زیربخش> ===
…<ref name="<نام>" />

== جستارهای وابسته ==
* [[<مقالهٔ موجود>]]

== منابع ==
{{پانویس}}

== برای مطالعهٔ بیشتر ==
* {{یادکرد کتاب | …}}

== پیوند به بیرون ==
* <پیوند رسمی>

{{<الگوی ناوبری>}}

{{<موضوع>-خرد}}
{{ترتیب‌پیش‌فرض:<کلید مرتب‌سازی فارسی>}}

[[رده:<ردهٔ فارسی>]]
[[رده:<ردهٔ فارسی>]]
```
Build citations with `scripts/cite_builder.py` and infoboxes with `scripts/infobox_builder.py`. Never
fill a field from memory (see `citations.md` §11).

## 3. Lead

| Rule | Tag / source |
|---|---|
| Bold the subject (`'''…'''`) at its first natural mention, ideally in the first sentence. Only that first mention is bold. | [LOW] [بخش آغازین][lead] |
| Don't link the bold title. | [LOW] [راهنمایی برای نوشتن مقاله‌های بهتر][better] |
| The first sentence is a short definition, unless the title is self-descriptive. | [LOW] [lead] |
| The lead stands alone and summarises the article, with a few sentences for each main section. It doesn't tease later content. | [LOW] [lead] |
| Length: normally no more than 3–4 paragraphs. Guide: under 15,000 characters → 1–2 paragraphs; 15,000–30,000 → 2–3; over 30,000 → 3–4. | [LOW] [lead] (numbers from a summary) |
| Biographies: name (and title), birth and death dates, nationality, main roles. Birth and death **places** go in the body unless relevant to notability. The exact format inside the date parentheses is [UNVERIFIED]. | [LOW] [شیوه‌نامه/زندگی‌نامه‌ها][bios] |
| Citations in the lead: no fa.wiki-specific rule found [UNVERIFIED]. Quotes and challenged claims always need an inline citation, in the lead too. | [V] [تأییدپذیری][verif] |
| Heavy linking in the lead discourages reading. | [LOW] [پیونددهی][links] |

Checks: **WC06** (no bold title in the lead).

## 4. Headings

**Rules.** Main sections use level 2 (`==`). Never use level 1, which is reserved for the page title.
Don't skip levels. Headings are unique within a page ([LOW] [layout]). **No links in headings**:
«پیوند را در عنوان بخشی از مقاله جای ندهید». Put `{{اصلی}}` or `{{همچنین ببینید}}` under the heading
instead ([V] [layout]). The bot writes `== عنوان ==` with single spaces ([C] [L119][c119]) and strips
quotes and bold inside headings ([C] [L336-L341][c336]).

**Standard end-section names, and the variants the bot renames** ([C] [L366-L376][c366]):

| Write | The bot renames these to it |
|---|---|
| `منابع` | منبع، منبع‌ها، مراجع، مرجع، مرجع‌ها، رفرنس(‌ها)، ارجاع(‌ها)، برگرفته از، منابع و یادداشت‌ها، فهرست مراجع، لیست مراجع، فهرست ارجاع(‌ها) |
| `جستارهای وابسته` | همچنین ببینید، ببینید، مطالب مرتبط، مطلب مرتبط، جستارهای مرتبط / دیگر / مشابه |
| `پیوند به بیرون` | لینک‌های خارجی، پیوندهای بیرونی، پیوند(‌های) خارجی، لینک(‌های) به بیرون |
| `پانویس` | پانویس‌ها. Also پاورقی / پاورقی‌ها → `پانویس‌ها`: the bot is inconsistent here, so write `پانویس` |
| `نگارخانه` | گالری، نگارستان |
| `فهرست` | لیست |

English headings (`References`, `See also`, `External links`) → **WC09**. Level problems → **WC11**;
unequal `=` counts → **WC12**.

## 5. End sections

Order: **جستارهای وابسته → یادداشت‌ها / پانویس / منابع → برای مطالعهٔ بیشتر → پیوند به بیرون** ([V] [layout]).
One revision of the page puts پانویس before منابع. پانویس and منابع may be one section.

| Section | Rules | Tag / source |
|---|---|---|
| `جستارهای وابسته` | Relevant links only, in a balanced number. **No red links and no disambiguation pages «به هیچ وجه»**. A suitable navbox is better than a list. | [V] [layout] |
| `منابع` | Holds `{{پانویس}}` (cited sources and explanatory notes). Separating notes from references is optional. The bot inserts `{{پانویس}}` under `== منابع ==` if it is missing ([C] [L432-L434][c432]). With short footnotes: `{{پانویس}}` under `== پانویس ==` and full citations under `== منابع ==` (see `citations.md` §4). | [LOW] [layout] |
| `برای مطالعهٔ بیشتر` | Alphabetical. Must not duplicate منابع or پیوند به بیرون. | [LOW] [layout] |
| `پیوند به بیرون` | Singular heading preferred. Must not duplicate منابع: a source you cite belongs in منابع as a citation. Sister-project boxes go here (e.g. `{{ویکی‌انبار|…}}`, `{{ویکی‌انبار-رده|…}}` ([C] [L441-L443][c441])), except ویکی‌واژه and ویکی‌نبشته. No external links in body text. | [LOW] [layout] |

## 6. Bottom block: navbox → stub → sort key → categories

Recommended order, with three sources agreeing:
1. **Navboxes**, then
2. **stub templates**: «در پایین‌ترین بخش مقاله، پس از بخش «پیوند به بیرون»، اگر الگوی ناوبری وجود داشت، زیر الگوهای ناوبری و بالای رده‌ها» ([V] [الگو:خرد][t-stub]),
3. **`{{ترتیب‌پیش‌فرض:…}}`**, then
4. **categories**. The layout sample has this order ([LOW] [layout]). The bot moves stubs and then the sort key to just above the first `[[رده:` ([C] [L596-L660][c598]).

⚠ **Conflict:** [ویکی‌پدیا:رده‌بندی][cat] says categories come «در پایان متن و پیش از الگوهای خرد», i.e. categories *before* stubs, because stub templates add categories themselves ([LOW]). Follow the order above, which the bot enforces. If the user's article or a reviewer uses the other order, don't fight over it.

- Write the sort key as `{{ترتیب‌پیش‌فرض:…}}`. The bot converts `DEFAULTSORT`/`ترتیب` to this form ([C] [L439][c439]) and **deletes** a sort key that is Latin-only ([C] [L440][c440]). Use a Persian key, e.g. family name first for people [UNVERIFIED: convention].
- Category names are Persian. The bot deletes Latin-only category names ([C] [L482][c482]) and sorts categories in Persian alphabetical order ([C] [L543-L594][c543]).
- At least one category is required → **WC05**.
- Use no more than **4** stub templates per article ([V] [الگو:خرد][t-stub], [ویکی‌پدیا:مقاله خرد][stubpage]).

## 7. Links and interlanguage links

| Rule | Tag / source |
|---|---|
| Link a term once, at its first occurrence. Captions, infoboxes, templates and tables are exceptions: each table row should make sense on its own. | [LOW] [پیونددهی][links] |
| Avoid overlinking; it hurts readers and screen-reader users. | [LOW] [links] |
| Link dates and years only when they are meaningfully related to the subject: «به تاریخ‌ها تنها زمانی پیوند داده شود که رابطه‌ای میان موضوع مطلب و تاریخ مورد نظر وجود داشته باشد». | [V] [تاریخ‌ها و اعداد][dates]; [LOW] [links] |
| Link to the most specific article, or to a section. | [LOW] [شیوه‌نامه][mos] |
| No links in headings (§4). Don't link the bold title (§3). | [V] / [LOW] |
| Write `[[الف]]`, not `[[الف|الف]]`; external links use single brackets `[https://… متن]`. The bot fixes both. | [C] [L473-L479][c473] |
| **Interlanguage links come from Wikidata sitelinks.** Don't add `[[en:…]]` lines; bots remove them and move them to Wikidata. | [LOW] [راهنما:پیوند بین زبان‌ها][interlang], [ویکی‌پدیا:ویکی‌داده][wd] |
| For a red link to an article that exists only in another language, `{{پیوند با میان‌ویکی}}` exists. Check its doc page for parameters. | [LOW] [الگو:پیوند با میان‌ویکی][iwlink] |

Checks: **WC18** (legacy `[[en:…]]` link), **WC01** (unbalanced `[[ ]]`).

## 8. Maintenance templates

| Template | Use | Params / placement | Tag / source |
|---|---|---|---|
| `{{مدرک}}` (page title «الگو:نیازمند منبع»; `{{نیازمند منبع}}` also works) | a single claim needs a source; placed right after the claim | `توضیح=` (reason), `تاریخ=` (month and year in words; the exact calendar is [LOW]): `{{مدرک|توضیح=…|تاریخ=…}}` | [V] [الگو:مدرک][t-cn], [ویکی‌پدیا:نیازمند منبع][cnpage] |
| `{{بدون منبع}}` | the whole article cites nothing («این مقاله به هیچ منبع و مرجعی استناد نمی‌کند»). Recommended instead of deletion. The bot renames `{{Unreferenced}}`, `{{منبع}}`, `{{بی منبع}}` and similar to it ([C] [L444][c444]). | top of article; params [UNVERIFIED] | [V] [منابع مستقل][indep] |
| `{{سرشناسی}}` | notability unclear; adds «رده:مقاله‌های با سرشناسی مشکوک». Topic variant: `{{سرشناسی|موسیقی}}`. Remove it once there are at least two reliable sources with significant coverage. | top of article | [V] [الگو:سرشناسی][t-notab] |
| `{{خرد}}` / `{{<موضوع>-خرد}}` (e.g. `{{ستاره‌شناسی-خرد}}`) | short article | bottom block (§6); at most 4; anyone may remove it after adequate expansion | [V] [الگو:خرد][t-stub] |
| `{{ابهام‌زدایی}}` | **disambiguation pages only** | bottom of the page, before categories; specialised variants exist (names, places, stations, airports) | [LOW] [الگو:ابهام‌زدایی][t-dab] |

- **BLP:** contentious unsourced or poorly sourced material about living people must be **removed**, not tagged: «نباید به آن‌ها برچسب مدرک زد یا به صفحهٔ بحث مقاله منتقلشان کرد» ([V] [زندگی‌نامه زندگان][blp]).
- When Claude writes text, `{{مدرک}}` is a last resort: find a source or leave the claim out. **WC14** counts leftover `{{مدرک}}` tags.

## 9. Translation attribution

- Attribution goes in the **edit summary**, naming the source wiki and linking the source article ([V] [راهنما:ترجمه][trans]).
- Optionally, add `{{صفحه ترجمه‌شده|<کد زبان>|<عنوان دقیق مقالهٔ مبدأ>}}` on the article's **talk page** (بحث), never in the article. Example: `{{صفحه ترجمه‌شده|en|Exact English title}}`. Copy the source title exactly ([V] [الگو:صفحه ترجمه‌شده][t-trans]).
- Details, optional parameters and ready-made edit summaries: `translation.md` §2.

## 10. Namespaces and images

| Use | Not | Tag / source |
|---|---|---|
| `[[رده:…]]` | `[[Category:…]]` | [C] [L354][c354] |
| `[[پرونده:…]]` | `[[File:…]]`, `[[Image:…]]`, `[[تصویر:…]]` | [C] [L356, L424-L425][c354] |
| `{{نام الگو}}` (no prefix) | `{{Template:…}}`, `{{الگو:…}}` in a transclusion | [C] [L355][c354] |
| image options `بندانگشتی`, `چپ`, `راست`, `وسط`, `پیوند=` | `thumb`, `left`, `right`, `center`, `link=` | [C] [L426-L430][c426] |

Example: `[[پرونده:<نام پرونده>.jpg|بندانگشتی|چپ|<توضیح تصویر>]]`. Put an image in the section it
illustrates ([LOW] [mos]). Checks: **WC10** (English namespace).

## 11. wikitext_check codes

Run `python3 scripts/wikitext_check.py article.wiki` (add `--strict` to fail on warnings).

| Code | Meaning | Section |
|---|---|---|
| WC01 / WC02 | unbalanced `[[ ]]` / `{{ }}` | §7 |
| WC03 | `<ref>` without `</ref>` | `citations.md` §2 |
| WC04 | refs but no `{{پانویس}}` | §5 |
| WC05 | no `[[رده:…]]` | §6 |
| WC06 | no bold title in the lead | §3 |
| WC07 / WC08 | unknown template / English template name | `infoboxes.md` §15 |
| WC09 | English or non-standard heading | §4 |
| WC10 | English namespace (`Category:`, `File:`) | §10 |
| WC11 / WC12 | heading level skipped or level 1 / malformed heading | §4 |
| WC13 | bare URL as a whole ref | `citations.md` §12 |
| WC14 | `{{مدرک}}` placeholders remain | §8 |
| WC17 | no refs at all | `citations.md` §1 |
| WC18 | legacy interlanguage link `[[en:…]]` | §7 |

[layout]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی
[lead]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/بخش_آغازین
[links]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/پیونددهی
[dates]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد
[mos]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه
[bios]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/زندگی‌نامه‌ها
[better]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:راهنمایی_برای_نوشتن_مقاله‌های_بهتر
[cat]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:رده‌بندی
[ibox]: https://fa.wikipedia.org/wiki/راهنما:جعبه_اطلاعات
[verif]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری
[blp]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:زندگی‌نامه_زندگان
[csd]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع
[indep]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_مستقل
[cnpage]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیازمند_منبع
[stubpage]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:مقاله_خرد
[trans]: https://fa.wikipedia.org/wiki/راهنما:ترجمه
[interlang]: https://fa.wikipedia.org/wiki/راهنما:پیوند_بین_زبان‌ها
[wd]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:ویکی‌داده
[iwlink]: https://fa.wikipedia.org/wiki/الگو:پیوند_با_میان‌ویکی
[t-cn]: https://fa.wikipedia.org/wiki/الگو:مدرک
[t-notab]: https://fa.wikipedia.org/wiki/الگو:سرشناسی
[t-stub]: https://fa.wikipedia.org/wiki/الگو:خرد
[t-dab]: https://fa.wikipedia.org/wiki/الگو:ابهام‌زدایی
[t-trans]: https://fa.wikipedia.org/wiki/الگو:صفحه_ترجمه‌شده
[c119]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L119
[c336]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L336-L341
[c354]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L354-L356
[c366]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L366-L376
[c426]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L424-L430
[c432]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L432-L434
[c439]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L439
[c440]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L440
[c441]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L441-L443
[c444]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L444
[c449]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L449-L455
[c473]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L473-L479
[c482]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L482
[c543]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L543-L594
[c598]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L596-L660
[c626]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L625-L660
