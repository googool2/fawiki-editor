# Dates and numbers on fa.wiki

Purpose: how to write dates (Solar Hijri, Gregorian, lunar Hijri), calendar abbreviations, decades, centuries, ordinals and numbers in fa.wiki prose and citations, and how to handle calendar conversion safely.

Tags:
- **[V]**: a quote or close paraphrase from the fa.wiki page.
- **[C]**: read in the source of a tool (citer, fawikibot).
- **[LOW]**: from a search summary only.
- **[UNVERIFIED]**: no source found.

Researched 2026-10-21. The main page is DATES = [ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها و اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد). It is a guideline. It covers numbers, dates, time, units, currency and coordinates, but several of its sections were not retrievable (see §9).

## Contents
1. [Which calendar](#1-which-calendar)
2. [Date format](#2-date-format)
3. [Month names](#3-month-names)
4. [Calendar abbreviations](#4-calendar-abbreviations)
5. [Decades, centuries, ordinals](#5-decades-centuries-ordinals)
6. [Numbers in prose](#6-numbers-in-prose)
7. [Dates in citations and templates](#7-dates-in-citations-and-templates)
8. [Conversion guidance (Solar ↔ Gregorian ↔ lunar)](#8-conversion-guidance)
9. [Known gaps / UNVERIFIED](#9-known-gaps--unverified)

Linter: `scripts/fa_lint.py` handles digits (FA03/FA04), ٪ (FA06), ٫ (FA07) and ٬ (FA08). It only **warns** on slash or hyphen dates (FW04), «۱۹۷۰ها» decades (FW07) and English-derived month names (FW08). Everything else in this file is manual (Claude). Templates and `<ref>` contents are never touched by the linter.

## 1. Which calendar

| Rule | Source | Tag |
|---|---|---|
| A contemporary article that uses the Solar Hijri (هجری خورشیدی) calendar **does not need** a Gregorian equivalent: «در دروان معاصر اگر در مقاله‌ای از تقویم هجری خورشیدی استفاده شده، نیازی به نوشتن معادل میلادی برای آن نیست». | [ویکی‌پدیا:گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی) | [V] |
| An older RfC noted that DATES had not yet fixed «شیوه دقیقی برای استفاده از تقویم هجری خورشیدی». Expect variation between articles. | [نظرخواهی/علامت اختصاری گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/علامت_اختصاری_گاهشماری_هجری_خورشیدی) | [V] |
| In citations, use the calendar printed in the source itself, e.g. Solar Hijri for books published in Iran. | [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) | [V] |
| Practical default, drawn from the two rules above: Iranian topics → Solar Hijri; non-Iranian topics → Gregorian; pre-modern Islamic topics → follow the sources (often lunar Hijri). Keep one calendar consistently within an article. | synthesis | [UNVERIFIED] |
| The exact format for a dual date (e.g. Solar plus Gregorian in parentheses) is not stated in what was retrieved. Do not invent one; copy the pattern already used in the article. | — | [UNVERIFIED] |

## 2. Date format

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Day in digits, month as a word, year in digits, in day-month-year order. | ۲۹ آذر ۱۳۹۵ | آذر ۲۹، ۱۳۹۵ | [گاهشماری هجری خورشیدی § شیوهٔ نگارش](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی); [شیوه‌نامه § تاریخ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | manual (Claude) |
| No slash, hyphen or comma between date parts: «از خط فاصله برای جداسازی اجزای تاریخ استفاده نکنید». | ۲۹ تیر ۱۳۶۸ | ۲۹/۴/۱۳۶۸، ۱۳۶۸-۴-۲۹ | [DATES § قالب تاریخ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | FW04 (warn) |
| No leading zero on the day. | ۷ آوریل ۲۰۱۱ | ۰۷ آوریل ۲۰۱۱ | [DATES](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Write the day as a digit, not as an ordinal or a word, unless the sentence starts with the date. | ۱۷ شهریور | هفدهم شهریور (mid-sentence) | [DATES](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Persian digits in prose dates. | ۱۹۹۹ | 1999 | [DATES § ارقام](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | FA03/FA04 |
| Proper names that contain a date keep their form: «اسم‌های خاص هیچ‌گاه عوض نمی‌شوند». | خیابان ۱۷ شهریور | خیابان هفدهم شهریور | [DATES § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Link a date only if it has a real relation to the subject: «به تاریخ‌ها تنها زمانی پیوند داده شود که رابطه‌ای میان موضوع مطلب و تاریخ مورد نظر وجود داشته باشد». An architect's birth year: no link. A film's release year: may be linked. | ۱۳۵۷ | [[۱۳۵۷]] (birth year) | [DATES § پیوند](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد); [پیونددهی § تاریخ‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/پیونددهی) | [V] [LOW] | manual (Claude) |

## 3. Month names

**Solar Hijri** (standardised forms) [LOW], from [DATES § ماه‌های شمسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد):
فروردین، اردیبهشت، خرداد، تیر، مرداد، شهریور، مهر، آبان، آذر، دی، بهمن، اسفند

**Gregorian, Iranian usage (French-derived).** Source: [DATES § نام ماه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد).

| # | Form to use | Tag | # | Form to use | Tag |
|---|---|---|---|---|---|
| 1 | ژانویه | [V] | 7 | ژوئیه | [V] |
| 2 | فوریه | [V] | 8 | اوت | [V] |
| 3 | مارس | [LOW] | 9 | سپتامبر | [LOW] |
| 4 | آوریل | [LOW] (appears in the page's example «۷ آوریل ۲۰۱۱» [V]) | 10 | اکتبر | [LOW] |
| 5 | مه | [V] | 11 | نوامبر | [LOW] |
| 6 | ژوئن | [V] | 12 | دسامبر | [LOW] |

- [LOW] rows are completions of the standard list. A 2026-10-21 search summary of DATES confirmed that the French-derived forms are the standard for Iranian Persian, without quoting each name.
- Avoid the English-derived forms جون، جولای، آگوست، آپریل، مارچ. The page mentions them as alternates [V/LOW]. Linter: **FW08**.
- Misspellings: ژوییه → ژوئیه, دیسامبر → دسامبر ([FCC L255-L257](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L255-L257)) [C]. Linter: FA50.
- Afghan Persian has its own list (جنوری، فبروری، مارچ…) [V partial]. When to use it is [UNVERIFIED].

**Lunar Hijri month names:** not covered by the retrieved MOS text [UNVERIFIED]. For spelling, see the article [ماه‌های هجری قمری](https://fa.wikipedia.org/wiki/ماه‌های_هجری_قمری) (an article, not a guideline) and copy the forms used in reliable sources.

## 4. Calendar abbreviations
Source: [ویکی‌پدیا:شیوه‌نامه/کوته‌نوشت](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/کوته‌نوشت), except where another link is given.

| Calendar | Form | Notes | Tag |
|---|---|---|---|
| Lunar Hijri | ه‍.ق | ه‍ is ه in its joining form (ه + ZWJ U+200D). «ه.ق» with a plain ه is marked wrong. No final dot. A 2026-10-21 search summary also named ه‍.ق as the standard. | [LOW] |
| Solar Hijri | ه‍.ش / ه‍.خ / ش / خ | Four forms are in use, and the RfC closed with «هیچ اجماعی وجود ندارد». **Never change one into another.** Keep the form the article already uses. کوته‌نوشت prefers ه‍.ش / ه‍.خ. | [V] ([نظرخواهی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/علامت_اختصاری_گاهشماری_هجری_خورشیدی), [گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی)) |
| Gregorian | م | The page prefers dropping the final dot. | [LOW] |
| Before Christ | ق.م | «ق.م.» and «ق م» are marked wrong. The article «پیش از میلاد» also uses «پ.م.», so it is unclear whether a trailing dot is wrong. | [LOW] |
| General | — | No space after an internal abbreviation dot: «ر.ک.», not «ر. ک.». The abbreviation dot «جزو سجاوندی‌ها محسوب نمی‌شود». At sentence end, do not double the dot. | [V] / [LOW] |

**Which to prefer:** spelling out (هجری قمری, هجری خورشیدی, میلادی) avoids the abbreviation dispute entirely. No source says this is preferred [UNVERIFIED], but nothing forbids it.

## 5. Decades, centuries, ordinals

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Decades: «دههٔ» + the year. | دههٔ ۱۹۸۰ | ۱۹۷۰ها، ۱۹۷۰‌ها | [DATES § دهه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | FW07 |
| Centuries and millennia are usually spelled out: «سده‌ها و هزاره‌ها معمولاً با حروف نوشته می‌شوند». The same page also shows «سدهٔ ۱۹ میلادی», so do not "correct" existing digit centuries; write new ones in words. | سدهٔ هفتم هجری قمری | — | [DATES § سده](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] (inconsistent) | manual (Claude) |
| Ordinals are spelled out: «برای نوشتن اعداد ترتیبی از حروف استفاده می‌شود». | پنجم | ۵ام | [DATES § اعداد ترتیبی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Regnal numbers are ordinals in words. | مهرداد دوم، لوئی نهم | مهرداد ۲ | [DATES § اعداد ترتیبی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Lead of a biography: name, birth and death dates, nationality, main roles. Birth and death **places** go in the body, not inside the date parentheses. The exact parenthesis pattern (e.g. «زادهٔ … – درگذشتهٔ …») was not found. | — | — | [شیوه‌نامه/زندگی‌نامه‌ها § بخش آغازین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/زندگی‌نامه‌ها) | [LOW] / [UNVERIFIED] | manual (Claude) |

## 6. Numbers in prose

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Persian digits only: «ارقام به شکل فارسی نوشته می‌شوند: ۱۲۳۴۵۶۷۸۹۰ - نه به شکل عربی … یا لاتین». | ۴۵۶ | 456، ٤٥٦ | [DATES § ارقام](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | FA03, FA04 |
| Spell out zero to nine in prose: «ارقام میان صفر تا نه به شکل حروف نوشته می‌شوند». Never in formulas. | سه شهر، ۱۲ شهر | ۳ شهر | [DATES § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Thousands separator ٬ (U+066C). A comma never groups digits. | ۲۴٬۷۰۰٬۰۰۰ | ۲۴,۷۰۰,۰۰۰، ۲۴،۷۰۰ | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | FA08 |
| Decimal separator ٫ (U+066B), never «/». | ۳٫۵ | ۳.۵، ۳/۵ | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [جداکننده هزارگان](https://fa.wikipedia.org/wiki/جداکننده_هزارگان) | [V] | FA07 |
| Percent: the word «درصد» in non-scientific prose. ٪ (not %) in scientific/technical text, tables and infoboxes, to the left of the number. | ۲۰ درصد; ۲۰٪ (table) | ۲۰% | [DATES § درصد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) (search excerpt) | [LOW] | FA06 (glyph only) |
| Iranian traditional units (من، مثقال، ذرع، چارک) have their own section on DATES. Its content was not retrieved. | — | — | [DATES § یکاهای ایرانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [LOW] | — |
| Spacing between a number and its unit (۵ کیلومتر vs ۵کیلومتر), unit symbols, currency and coordinates. The page covers these, but no rule text was retrieved. Write a normal space (۵ کیلومتر) and follow the article's existing style. | — | — | [DATES](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [UNVERIFIED] | manual (Claude) |

## 7. Dates in citations and templates

| Point | Detail | Source | Tag |
|---|---|---|---|
| Format citer emits | citer, fa.wiki's citation generator, writes `تاریخ` (publication) and `تاریخ بازبینی` (access date) as ISO `YYYY-MM-DD` in **Latin digits**, e.g. `تاریخ=2020-06-07`. If it receives only a year, it writes `سال=`. If it receives a date as a string, it passes it through unchanged. | [citer L126-L131](https://github.com/5j9/citer/blob/fab6d27f123de6dc63e0becba67828839e396f5d/lib/generator_fa.py#L126-L131), [L197-L198](https://github.com/5j9/citer/blob/fab6d27f123de6dc63e0becba67828839e396f5d/lib/generator_fa.py#L197-L198) | [C] |
| ISO preference | The یادکرد وب doc says dates should preferably follow ISO 8601. | [الگو:یادکرد وب](https://fa.wikipedia.org/wiki/الگو:یادکرد_وب) | [LOW] |
| Access date | Must include the **day**. A future or very old access date raises an error. Add it only when there is a URL to a specific page (citer adds it only when `url` is set). | [راهنما:خطاهای الگوی یادکرد](https://fa.wikipedia.org/wiki/راهنما:خطاهای_الگوی_یادکرد); [citer L197-L198](https://github.com/5j9/citer/blob/fab6d27f123de6dc63e0becba67828839e396f5d/lib/generator_fa.py#L197-L198) | [V] [C] |
| Archive date | `تاریخ بایگانی` goes with `نشانی بایگانی`/`پیوند بایگانی`, also ISO. | [citer L175-L182](https://github.com/5j9/citer/blob/fab6d27f123de6dc63e0becba67828839e396f5d/lib/generator_fa.py#L175-L182) | [C] |
| Solar-dated sources | It is unknown whether the CS1 date validator accepts `۱۵ فروردین ۱۴۰۲` or `۱۴۰۲/۰۱/۱۵` in `تاریخ`. Safest: `سال=۱۳۸۶` (year only) for Solar-dated books, which follows the source calendar rule above. A verbatim citer test emits `سال=1387` (Latin digits) for a Solar year, so Latin digits in parameters are fine. | C-research open question; [citer tests](https://github.com/5j9/citer/blob/fab6d27f123de6dc63e0becba67828839e396f5d/tests/test_fa.py#L219-L223) | [LOW] [C] |
| Linter | Digits inside `{{یادکرد …}}` are never converted (templates are protected). Do not convert them by hand either. | [FCC L520-L541](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L520-L541) (the bot converts the other way, to Latin, in English citations) | [C] |
| Infobox dates | `{{جعبه اطلاعات زندگی‌نامه}}` uses `زادروز` with age templates such as «تاریخ تولد و سن», and `تاریخ درگذشت`. | [الگو:جعبه اطلاعات زندگی‌نامه](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_زندگی‌نامه) | [V] |
| Maintenance tags | `{{مدرک\|تاریخ=…}}` / `{{نیازمند منبع\|تاریخ=}}` take month and year in words. Whether that means «مهر ۱۴۰۵» or «اکتبر ۲۰۲۶» is unconfirmed, and a bot may auto-fill it. | [الگو:مدرک](https://fa.wikipedia.org/wiki/الگو:مدرک) | [LOW] |

## 8. Conversion guidance
*This is skill guidance, not fa.wiki policy. The calendar facts here (Nowruz boundary, 11-day drift, +621/622) are general knowledge and are not sourced from fa.wiki [UNVERIFIED]. Only points 1 and 5 carry fa.wiki sources.*

**Do not compute exact-day Solar ↔ Gregorian ↔ lunar conversions in your head.** Getting one day wrong produces a false fact. The year boundary of the Solar calendar falls at the March equinox (Nowruz, around 20–21 March), and lunar Hijri years drift about 11 days a year against both. Mental arithmetic fails exactly at those edges.

Order of preference:
1. **Use the date exactly as the source gives it, in the source's calendar.** This matches the citation rule ([راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع)) [V].
2. If the article's calendar differs and an equivalent is needed, take the equivalent from a **reliable source that states it**, and cite that source.
3. If you must convert, use a deterministic algorithm or library run as code (e.g. a Python Jalali/Hijri conversion package), never estimation. State in the edit summary or talk page that the date was converted. Lunar Hijri conversions can differ by a day or two because they depend on moon sighting, so flag them as approximate.
4. **Year-only conversion:** a Solar year overlaps two Gregorian years (e.g. ۱۳۵۷ ≈ ۱۹۷۸–۱۹۷۹). Without the month, write both years or keep the source's year. Do not pick one. Solar year + 621 or + 622 depending on the month is the basic arithmetic, but use it only for year ranges.
5. For contemporary Iranian topics a Gregorian equivalent is not required ([گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی)) [V]. Leaving it out is better than guessing.
6. When reviewing, treat any Solar/Gregorian pair that was not sourced or not computed by code as **unverified** and flag it.

## 9. Known gaps / [UNVERIFIED]
- Number–unit spacing, unit symbols, currency and coordinate formats (DATES covers them; no text was retrieved).
- The dual-date pattern (Solar with Gregorian in parentheses, or lunar with Gregorian).
- Lunar Hijri month-name spellings and the lunar date format.
- The biography birth/death parenthesis format.
- Whether Afghan month names should be used in Afghanistan-related articles.
- The CS1 validator's handling of Solar and Persian-digit dates. The `{{مدرک}}` date format.
- BC abbreviation: ق.م vs پ.م. and the trailing dot. The four Solar abbreviations have no consensus.
- Six of the twelve Gregorian month names are [LOW] completions (§3).
