# Citations on fa.wiki: `<ref>`, `{{پانویس}}`, `{{پک}}`, `{{یادکرد …}}`

Load this file when you add, convert or review citations. Every rule has a tag and a source.
**Tags:** [V] = a search excerpt of the fa.wiki page confirmed it · [C] = read in code that writes
fa.wiki wikitext (file and line linked) · [LOW] = from a search summary only · [UNVERIFIED] = no source found.
Code sources: **citer** (the fa.wiki citation generator by 5j9/Dalba, `main` @ `fab6d27`, 2026-10-19)
and **fawikibot** (`master` @ `04dde6d`). Research date: 2026-10-21. fa.wiki pages change, so treat
[LOW] parameter names as provisional.

> **Live check, 2026-10-21** (`bench/live_check.py`): every web and news parameter below was found in the live templates. Five were not: `{{یادکرد کتاب}}` `نویسنده`, `ترجمه` and `{{یادکرد ژورنال}}` `نویسنده`, `جلد`, `ناشر` are missing from TemplateData, the template source and the invoked module (`citation/CS1/fa/dispatch`), yet citer emits them. They are kept (citer is fa.wiki's own tool) but marked **[CONFLICT]**; if one shows an «پارامتر ناشناخته» error in preview, use `نام خانوادگی` for an unsplit author, `دیگران=ترجمهٔ …` for a translator, and `دوره` for a journal volume.

## Contents
[1 Ground rules](#1-ground-rules) · [2 `<ref>`](#2-ref-and-named-refs) · [3 `{{پانویس}}`](#3-پانویس-reference-list) · [4 `{{پک}}`](#4-short-footnotes-پک) · [5 Dates/authors/IDs](#5-dates-author-numbering-identifiers) · [6 یادکرد وب](#6-یادکرد-وب) · [7 یادکرد کتاب](#7-یادکرد-کتاب) · [8 یادکرد ژورنال](#8-یادکرد-ژورنال) · [9 یادکرد خبر](#9-یادکرد-خبر) · [10 EN→FA table](#10-english--persian-conversion-table) · [11 Anti-fabrication](#11-anti-fabrication) · [12 Tools](#12-tools)

---

## 1. Ground rules

| Rule | Tag / source |
|---|---|
| The style page is **«ویکی‌پدیا:شیوه ارجاع به منابع»**. No page «شیوه یادکرد منابع» exists. It is based on the Chicago style: citations go in numbered footnotes. Harvard, Vancouver, APA and other styles are also accepted. | [V] [شیوه ارجاع][shive] |
| Burden of proof: «مسئولیت ارائه مدرک، با ویرایشگری است که مطلب را اضافه می‌کند یا بازیابی می‌کند». | [V] [تأییدپذیری][verif] |
| Quotes and any challenged or likely-to-be-challenged material need an inline citation. | [V] [تأییدپذیری][verif] |
| Wikipedia (any language) and its mirrors are not reliable sources. | [LOW] [منابع معتبر][rs] |
| Templates are Persian-named (`{{یادکرد وب}}`, not `{{Cite web}}`). Persian and English parameter names are interchangeable "according to the list". A citation with `|زبان=en` is routed to the English CS1 module. | [V] [الگو:Cite journal][t-journal], [پودمان CS1/fa][cs1] |
| Use Persian names for core fields. Use English names only for identifiers (`doi`, `pmid`…), because English core names inside `{{یادکرد …}}` are not confirmed. | recommendation; core English aliases [LOW] |

## 2. `<ref>` and named refs

| Rule | Tag / source |
|---|---|
| Put the full citation inside `<ref>…</ref>` directly after the claim, with no line break before it. Placement relative to punctuation is [UNVERIFIED] for fa.wiki. The bot joins a ref to the text before it (`\n<ref`→`<ref`) and joins adjacent refs (`</ref>\n<ref`→`</ref><ref`). | [C] [fcc L118, L465][fccl115] |
| Named refs: define once as `<ref name="x">…</ref>`, reuse as `<ref name="x" />`. Names are case-sensitive, must not be purely numeric and must be unique. Quote the name if it contains spaces or special characters. | [V] [راهنما:پانویس‌ها][help-fn] |
| citer's output form is `<ref name="…">{{یادکرد …}}‏</ref>`, with U+200F (RLM) before `</ref>`. The RLM keeps an LTR citation from breaking the RTL line. | [C] [citer L211][g207] |
| With short footnotes, don't bundle several sources in one ref; repeat the footnote instead. | [V] [شیوه ارجاع][shive] |

```wikitext
تهران پایتخت ایران است.<ref name="iran-capital">{{یادکرد وب | عنوان=… | نشانی=… | تاریخ بازبینی=…}}</ref>
…این شهر بزرگ‌ترین شهر کشور است.<ref name="iran-capital" />
```

## 3. `{{پانویس}}` (reference list)

| Param | Effect | Tag / source |
|---|---|---|
| *(none)* | `{{پانویس}}` under `== منابع ==`. The bot rewrites `<references/>`, `{{Reflist}}`, `{{References}}` and `{{پانویس‌ها}}` to `{{پانویس`. | [C] [fcc L403-L404][fcc403] |
| `۲` (1st positional) | number of columns: `{{پانویس|۲}}`. The bot sets `|۲` automatically when the page has more than 7 refs. | [V] [الگو:پانویس][t-pan]; [C] [fcc L412-L420][fcc405] |
| `عرض=` | column width in em, e.g. `{{پانویس|عرض=۳۰}}` | [V] [الگو:پانویس][t-pan]; [C] [fcc L417][fcc405] |
| `چپ‌چین=بله` | left-aligned list for LTR (e.g. English) sources. Combines with columns: `{{پانویس|۲|چپ‌چین=بله}}` | [V] [الگو:پانویس][t-pan]; [C] [fcc L407, L420][fcc405] |
| `گروه=` | list for a ref group, e.g. `{{پانویس|گروه=پانویس}}` with `<ref group="پانویس">` | [C] [fcc L419][fcc405]; semantics [LOW] |
| ~~`اندازه=`~~ | **Obsolete.** The bot still writes `اندازه=کوچک`/`ریز`, but the doc says the parameter has no effect any more. Don't emit it. | [C] [fcc L408][fcc405] vs [V] [الگو:پانویس][t-pan] |

If `== منابع ==` exists without `{{پانویس}}`, the bot inserts it ([C] [fcc L432-L434][fcc432]).
`wikitext_check.py` reports this as **WC04**.

## 4. Short footnotes `{{پک}}`

The شیوه ارجاع page calls short footnotes "the preferred method on fa.wiki" ([V] [شیوه ارجاع][shive],
[الگو:پانویس کوتاه‌شده][t-pk]). Full `<ref>{{یادکرد …}}</ref>` citations are also normal. When an
article already uses one system, keep it [UNVERIFIED: general practice, not quoted].

| Item | Tag / source |
|---|---|
| Syntax: `<ref>{{پک | نام‌خانوادگی۱ | نام‌خانوادگی۲ | سال | ک=عنوان | زبان=en | ص=صفحه}}‏</ref>`. Up to 4 surnames are positional, then the year. | [C] [citer L46-L52, L204][g46]; [V] [الگو:پانویس کوتاه‌شده][t-pk] |
| `ک=` short title of the work; `ص=` page(s). | [V] [الگو:پانویس کوتاه‌شده][t-pk] |
| `{{پک/بن}}` when there is no author. | [C] [citer L52][g46] |
| Surnames and year must match the full citation in منابع, or the link between them breaks. | [V] [شیوه ارجاع][shive] |

Layout with short footnotes (a synthesis, not a quote): `{{پانویس}}` under `== پانویس ==`, and the
full `* {{یادکرد …}}` lines under `== منابع ==`.

```wikitext
…در سال ۱۳۲۰ منتشر شد.<ref>{{پک | Farrell | 2009 | ک=… | زبان=en | ص=12}}‏</ref>
== پانویس ==
{{پانویس}}
== منابع ==
* {{یادکرد کتاب | نام خانوادگی=Farrell | نام=… | عنوان=… | سال=2009 | …}}
```
(The `{{پک | Farrell | 2009` start is from [citer test L188][t188]. The rest is placeholders.)

## 5. Dates, author numbering, identifiers

- **Gregorian dates:** citer writes `تاریخ=` and `تاریخ بازبینی=` as ISO `YYYY-MM-DD` with Latin digits, e.g. `تاریخ=2020-06-07` ([C] [citer L125-L131, L197-L198][g125]). The یادکرد وب doc prefers ISO 8601 ([LOW] [الگو:یادکرد وب][t-web]). Another summary of the same doc says day–month–year for تاریخ بازبینی ([LOW]). **Default: emit ISO.**
- **Access date** must include the day. A future or implausibly old access date raises an error ([V] [خطاهای الگوی یادکرد][errors]). Give it only when there is a URL ([C] [citer L197-L198][g197]).
- **Iranian books:** use the calendar printed in the source, e.g. the Solar Hijri year ([V] [راهنما:ارجاع][erja]). Put it in `سال=`. citer writes `سال=1386` ([C] [test L28-L34][t28]); the شیوه ارجاع sample writes `سال = ۱۳۷۹` ([V] [شیوه ارجاع][shive]). Both forms occur. Whether the date validator accepts a Persian-digit Solar date in `تاریخ=` (e.g. `۱۵ فروردین ۱۴۰۲`) is **[UNVERIFIED]**; use `سال=` for Solar years.
- **Author numbering uses Persian digits:** `نام خانوادگی۱`, `نام۱`, `نام خانوادگی۲`, `نام۲`… With a single author, no digit: `نام خانوادگی=`, `نام=`. With no first/last split: `نویسنده=` (or `نویسنده۱=`…) ([C] [citer L215-L236][g215], [test L43][t43]).
- **Identifiers stay English** inside Persian templates: `doi`, `doi-access=free`, `pmid`, `pmc` (no "PMC" prefix), `issn`, `oclc`, `jstor`, `jstor-access=free` ([C] [citer L136-L160][g136]). ISBN is `شابک` ([C] [citer L133-L134][g125]).
- Page ranges use an en dash: `صفحه=17–19` ([C] [test L219-L224][t219]).

## 6. `{{یادکرد وب}}`
Source: [الگو:یادکرد وب][t-web]. citer also maps news pages to یادکرد وب ([C] [citer L23-L27][g23]).

| Param | Meaning | Required | Tag / source |
|---|---|---|---|
| `نشانی` (alt `پیوند`) | URL | **yes** | [V] [راهنما:ارجاع][erja] ("اجباری"); [C] [webcite.py L155][wc151], [citer L170][g167] |
| `عنوان` | page title | **yes** | [V] [راهنما:ارجاع][erja]; [C] [citer L86][g80] |
| `نام خانوادگی`/`نام` or `نویسنده` | author | no | [C] [citer L215-L236][g215] |
| `تاریخ` | publication date | no | [C] [citer L125-L129][g125] |
| `وبگاه` | website name | no | [C] [citer L100-L102][g92] |
| `اثر` | work (site/agency that differs from the publisher) | no | [V] (doc examples, [راهنما:ارجاع][erja]) |
| `ناشر` | publisher | recommended | [V] [راهنما:ارجاع][erja]; [C] [citer L107-L108][g107] |
| `تاریخ بازبینی` | access date | with a URL to a specific page | [C] [citer L197-L198][g197]; alias `تاریخ بازدید` [LOW] |
| `کد زبان` | ISO code (`en`, `ar`, `fr`). Changes formatting (Latin punctuation and digits) | no | [V] [الگو:یادکرد وب][t-web]; [C] [citer L188-L189][g186] |
| `زبان` | only appends "(language)" | no | [V] (contrast with کد زبان) |
| `نشانی بایگانی` (alt `پیوند بایگانی`) | archive URL; needs `تاریخ بایگانی` | no | [V]; [C] [webcite.py L151][wc151], [citer L181][g175] |
| `تاریخ بایگانی` | archive date | with archive URL | [C] [citer L182][g175] |
| `پیوند مرده` | `آری` / `نه` (is the original URL dead?) | no | [C] [citer L183][g175]; [V] (value `نه`) |
| `نقل قول`, `قالب`, `صفحه` | quote, format, page | no | [LOW] |

Copied example: citer's expected output, [test L311][t311]. citer fills `تاریخ بازبینی=` with the
day it runs; the test strips that value, and it is shown here as `…`.
```wikitext
{{یادکرد وب | عنوان=اصل هفتاد و سوم | ناشر=پایگاه اطلاع رسانی شورای نگهبان - shora-gc.ir | تاریخ=2020-06-07 | پیوند=https://www.shora-gc.ir/fa/news/1815/%D8%A7%D8%B5%D9%84-%D9%87%D9%81%D8%AA%D8%A7%D8%AF-%D9%88-%D8%B3%D9%88%D9%85 | کد زبان=fa | تاریخ بازبینی=…}}
```

## 7. `{{یادکرد کتاب}}`
Sources: [الگو:Cite book (fa doc)][t-book], [راهنما:ارجاع][erja].

| Param | Meaning | Required | Tag / source |
|---|---|---|---|
| `عنوان` | book title | **yes** | [C] [citer L80-L86][g80] |
| `نام خانوادگی`/`نام` (`…۱`, `…۲`), `نویسنده` | author(s) | recommended | [C] [citer L215-L236][g215]; [V] |
| `نام خانوادگی ویراستار`/`نام ویراستار`, `ویراستار` | editor | no | [C] [citer L54-L57][g54] |
| `ترجمه` | translator(s), joined with «، » and « و ». `مترجم` is **[UNVERIFIED]** | no | [C] [citer L59-L60, L239-L249][g59]; [V] [راهنما:ارجاع][erja] |
| `دیگران` | others (illustrator, preface) | no | [C] [citer L62-L63][g59] |
| `فصل` | chapter | no | [C] [citer L81-L84, L104-L105][g80] |
| `ترجمه عنوان` | translated title | no | [LOW] |
| `ناشر` | publisher | recommended | [C] [citer L107-L108][g107]; [V] |
| `مکان` | place of publication | no | [C] [citer L110-L111][g107]; [V] |
| `ویرایش`, `سری`, `جلد` | edition, series, volume | no | [C] [citer L113-L120][g113] |
| `سال` / `تاریخ` | year / full date | recommended | [C] [citer L125-L131][g125] |
| `شابک` | ISBN; hyphens optional. Auto-linked | recommended | [C] [citer L133-L134][g125], [isbn_fix.py L144][isbn144]; [V] |
| `صفحه` | page(s) cited. `صفحه‌ها` is **[UNVERIFIED]** | no | [C] [citer L207-L210][g207] |
| `نشانی`/`پیوند`, `تاریخ بازبینی` | URL, access date (only with a URL) | no | [C] [citer L167-L170, L197][g167] |
| `زبان` | language code | no | [C] [citer L190-L191][g186] |
| `oclc` | OCLC number | no | [C] [citer L153-L154][g136] |

Copied example: citer's expected output, [test L28-L34][t28] (Iranian book, Solar year, two translators).
```wikitext
{{یادکرد کتاب | نام خانوادگی=لانسکی | نام=ویکی | ترجمه=فیروزه دالکی و مژگان امیرفروغی | دیگران=کی وایت (تصويرگر) | عنوان=101 راه برای اینکه پدر بهتری باشید | ناشر=پیک ادبیات | مکان=تهران - تهران | سال=1386 | شابک=978-964-8165-81-4 | زبان=fa}}
```
(The source data has an Arabic ي in «تصويرگر». Fix it to ی when you reuse the example.)

## 8. `{{یادکرد ژورنال}}`
Sources: [الگو:Cite journal][t-journal], [راهنما:ارجاع][erja].

| Param | Meaning | Required | Tag / source |
|---|---|---|---|
| `عنوان` | article title | **yes** | [C] [citer L80-L86][g80] |
| `ژورنال` | journal name | **yes** | [C] [citer L92-L98][g92] |
| `نام خانوادگی۱`/`نام۱`… | authors | recommended | [C] [citer L215-L236][g215] |
| `جلد` / `شماره` | volume / issue (`دوره` [LOW]) | no | [C] [citer L119-L123][g113] |
| `صفحه` | pages, en-dash range | no | [C] [citer L162-L165][g162] |
| `سال` / `تاریخ` | date | recommended | [C] [citer L125-L131][g125] |
| `ناشر` | publisher | no | [C]; [V] [ویکی‌پدیا:مگ‌ایران][magiran] |
| `doi` (+`doi-access=free`) | DOI; prefer it to a URL | no | [C] [citer L145-L151][g136]; [V] [Cite journal][t-journal] |
| `pmid`, `pmc`, `issn`, `jstor` | identifiers | no | [C] [citer L136-L160][g136] |
| `پیوند`, `زبان`, `تاریخ بازبینی` | URL, language, access date | no | [C] [citer L167-L198][g167] |

Copied example: citer's expected output, [test L219-L224][t219] (`تاریخ بازبینی` value stripped by the test).
```wikitext
{{یادکرد ژورنال | عنوان=زندگی نامه علمی دکتر کاووس حسن لی | ژورنال=شعر | شماره=62 | سال=1387 | صفحه=17–19 | پیوند=https://www.noormags.ir/view/fa/articlepage/454096 | زبان=fa | تاریخ بازبینی=…}}
```
A citer test with a DOI and ten numbered authors is at [test L329][t329].

## 9. `{{یادکرد خبر}}`
No excerpt of the template's own doc page was found. citer does not emit it. The parameters below
come from the یادکرد خبر sample in [راهنما:ارجاع][erja] only.

| Param | Meaning | Required | Tag |
|---|---|---|---|
| `نشانی`, `عنوان` | URL, headline | **yes** | [V] |
| `نام خانوادگی`, `نام` | author | no | [V] |
| `خبرگزاری` | news agency | no | [V] name listed; exact spelling [LOW] |
| `ناشر` | outlet / publisher | no | [V] |
| `تاریخ` | publication date. The sample says «تاریخ انتشار», which is unconfirmed as a parameter | recommended | [LOW] |
| `تاریخ بازبینی` | access date | recommended | [V] |
| `نشانی بایگانی`, `تاریخ بایگانی`, `کد زبان` | archive, language | no | [V] |
| `کار` (newspaper/work) | — | — | **[UNVERIFIED]**: never seen. Use `اثر` or `ناشر` |

Skeleton (placeholders, **not** a copied example). If unsure, `{{یادکرد وب}}` is the safe fallback (citer's choice).
```wikitext
{{یادکرد خبر | نام خانوادگی=<…> | نام=<…> | عنوان=<تیتر خبر> | نشانی=<URL> | خبرگزاری=<…> | ناشر=<…> | تاریخ=YYYY-MM-DD | تاریخ بازبینی=YYYY-MM-DD | کد زبان=fa}}
```

## 10. English → Persian conversion table
Use this when translating en.wiki citations. Convert names; keep values (ISO dates, URLs, IDs) as they are.

| en.wiki | fa.wiki | Tag / source |
|---|---|---|
| `{{cite web}}` / `{{cite book}}` / `{{cite journal}}` | `{{یادکرد وب}}` / `{{یادکرد کتاب}}` / `{{یادکرد ژورنال}}` | [C] [citer L23-L27, L42][g23] |
| `{{cite news}}` | `{{یادکرد خبر}}` (or `{{یادکرد وب}}`) | [V] [راهنما:ارجاع][erja] |
| `{{reflist}}` / `<references/>` | `{{پانویس}}` | [C] [fcc L403-L404][fcc403] |
| `{{sfn}}` | `{{پک}}` | [V] [الگو:پانویس کوتاه‌شده][t-pk] |
| `url` | `نشانی` (or `پیوند`) | [C] [webcite.py L155][wc151], [citer L170][g167] |
| `title` | `عنوان` | [C] [citer L86][g80] |
| `access-date` | `تاریخ بازبینی` | [C] [citer L198][g197] |
| `website` / `work` | `وبگاه` / `اثر` | [C] [citer L102][g92] / [V] |
| `publisher` | `ناشر` | [C] [citer L108][g107] |
| `last` / `first` (`last2`…) | `نام خانوادگی` / `نام` (`نام خانوادگی۲`…) | [C] [citer L215-L236][g215] |
| `author` | `نویسنده` | [C] [citer L221][g215] |
| `editor-last` / `editor-first` | `نام خانوادگی ویراستار` / `نام ویراستار` | [C] [citer L54-L57][g54] |
| `date` / `year` | `تاریخ` / `سال` | [C] [citer L125-L131][g125] |
| `language` | `کد زبان` in یادکرد وب; `زبان` elsewhere | [C] [citer L186-L192][g186] |
| `archive-url` / `archive-date` | `نشانی بایگانی` / `تاریخ بایگانی` | [C] [webcite.py L151][wc151], [citer L181-L182][g175] |
| `url-status` | `پیوند مرده` (`dead`→`آری`, `live`→`نه`) | name/values [C] [citer L183][g175]; value mapping [LOW] |
| `isbn` | `شابک` | [C] [citer L134][g125] |
| `location` | `مکان` | [C] [citer L111][g107] |
| `page` / `pages` | `صفحه` | [C] [citer L165, L207-L208][g162] |
| `volume` / `issue` | `جلد` / `شماره` | [C] [citer L120, L123][g113] |
| `journal` | `ژورنال` | [C] [citer L98][g92] |
| `translator` | `ترجمه` | [C] [citer L60][g59] |
| `edition` / `chapter` / `series` / `others` | `ویرایش` / `فصل` / `سری` / `دیگران` | [C] [citer L105-L117, L63][g113] |
| `trans-title` / `quote` | `ترجمه عنوان` / `نقل قول` | [LOW] |
| `agency` | `خبرگزاری` (یادکرد خبر) | [LOW] |
| `doi`, `pmid`, `pmc`, `issn`, `oclc`, `jstor` | unchanged | [C] [citer L136-L160][g136] |

Translation rule: verify each source yourself. For a claim whose source you did not check, cite the
source-language article with `{{یادکرد-ویکی}}`. Blanket notes like «(ویکی‌پدیای انگلیسی)» are wrong
([V] [خودآموز (ترجمه)][trans-tut]).

## 11. Anti-fabrication

- **Never invent** a URL, ISBN, DOI, page number, date, author, publisher or quotation. If a field is unknown, leave it empty or omit it. Do not "complete" it from memory.
- fa.wiki speedy criterion **ع۱۵** (pages created with LLMs without human review) lists fake citations as a sign: «پیوندهای بیرونی که در بدو ورود مرده هستند، شابک‌های دارای جمع‌آزمای نامعتبر، و شناساگر اشیاء دیجیتال (DOI) غیرقابل حل» ([V] [معیارهای حذف سریع][csd]). The page also says one sign alone is not proof ([LOW]).
- ویکی‌پدیا:مدل‌های زبانی بزرگ: all LLM text must be reviewed by editors before use, and any LLM use must be disclosed in the edit summary ([V] [مدل‌های زبانی بزرگ][llm]). The page warns that LLM articles can contain fake references ([LOW]).
- A claim with no source you can show: write `{{مدرک}}` after it, or leave it out. For contentious claims about living people, remove them; don't tag them ([V], see `article-structure.md` §8).
- Check an ISBN's checksum before use. `cite_builder.py` rejects a bad one: `invalid ISBN (checksum failed)` ([C] [cite_builder.py](../scripts/cite_builder.py) `normalize_isbn`).
- Copy titles exactly as the source prints them. Do not translate a foreign title into `عنوان=`; use `ترجمه عنوان=` [LOW] for a translation.

## 12. Tools

**`scripts/cite_builder.py`** builds a `{{یادکرد …}}` from a URL, DOI or ISBN. It is the only
networked script, and it never invents data: fields it cannot read are left empty and listed as TODO.
```
python3 scripts/cite_builder.py https://www.example.com/news/1          # fetch page metadata
python3 scripts/cite_builder.py 10.1000/xyz123                          # Crossref (DOI)
python3 scripts/cite_builder.py 978-964-00-1234-5                       # Open Library (ISBN)
python3 scripts/cite_builder.py URL --offline                           # skeleton, TODO fields
python3 scripts/cite_builder.py URL --type news --ref --name irna1      # wrap in <ref name=…>
python3 scripts/cite_builder.py URL --set title="عنوان" --set date=2024-05-01
```
Exit codes: 0 ok, 1 lookup failed (skeleton still printed), 2 bad input. Fill every TODO from the
source itself or ask the user. Parameter names live in `scripts/data/citations.json`.

**`scripts/wikitext_check.py`** codes for citations: **WC03** `<ref>` not closed · **WC04** refs
but no `{{پانویس}}` · **WC13** bare URL as the whole ref (wrap it in یادکرد وب) · **WC14** `{{مدرک}}`
placeholders remain · **WC15** same ref name, different content · **WC17** no refs at all ·
**WC08** English template name such as `{{Cite web}}`.

[shive]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه_ارجاع_به_منابع
[erja]: https://fa.wikipedia.org/wiki/راهنما:ارجاع
[help-fn]: https://fa.wikipedia.org/wiki/راهنما:پانویس‌ها
[t-pan]: https://fa.wikipedia.org/wiki/الگو:پانویس
[t-pk]: https://fa.wikipedia.org/wiki/الگو:پانویس_کوتاه‌شده
[t-web]: https://fa.wikipedia.org/wiki/الگو:یادکرد_وب
[t-book]: https://fa.wikipedia.org/wiki/الگو:Cite_book
[t-journal]: https://fa.wikipedia.org/wiki/الگو:Cite_journal
[cs1]: https://fa.wikipedia.org/wiki/پودمان:Citation/CS1/fa/توضیحات
[errors]: https://fa.wikipedia.org/wiki/راهنما:خطاهای_الگوی_یادکرد
[magiran]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:مگ‌ایران
[verif]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری
[rs]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_معتبر
[csd]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع
[llm]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:مدل‌های_زبانی_بزرگ
[trans-tut]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)
[g23]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L23-L42
[g46]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L46-L52
[g54]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L54-L57
[g59]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L59-L63
[g80]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L80-L90
[g92]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L92-L102
[g107]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L107-L111
[g113]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L104-L123
[g125]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L125-L134
[g136]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L136-L160
[g162]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L162-L165
[g167]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L167-L173
[g175]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L175-L184
[g186]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L186-L192
[g197]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L197-L198
[g207]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L206-L211
[g215]: https://github.com/5j9/citer/blob/main/lib/generator_fa.py#L215-L236
[t28]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L28-L34
[t43]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L43
[t188]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L188
[t219]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L219-L224
[t311]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L311
[t329]: https://github.com/5j9/citer/blob/main/tests/test_fa.py#L329
[fccl115]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L118
[fcc403]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L403-L404
[fcc405]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L405-L420
[fcc432]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L432-L434
[wc151]: https://github.com/PersianWikipedia/fawikibot/blob/master/webcite.py#L151-L155
[isbn144]: https://github.com/PersianWikipedia/fawikibot/blob/master/isbn_fix.py#L144
