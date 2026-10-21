# Infoboxes (جعبه اطلاعات) on fa.wiki

Load this file when you add, translate or review an infobox.
**Tags:** [V] = the name or rule appeared in a search excerpt of the cited fa.wiki page · [C] = read in
fawikibot code (`master` @ `04dde6d`) · [LOW] = search summary only · [UNVERIFIED] = no source.
Research date: 2026-10-21.

> **Read before use.**
> 1. The choice of these 10 infoboxes as the most-used ones is **[UNVERIFIED]**: no transclusion counts were reachable.
> 2. Parameter names come from search excerpts, not from TemplateData, so even [V] names are provisional. **Treat every parameter name as [LOW] until it is checked.** Before you publish, ask the user to compare the infobox with the live template's doc page (links below), or with
>    `https://fa.wikipedia.org/w/api.php?action=templatedata&titles=الگو:<نام الگو>`.
> 3. "Core" means **core (recommended)**. The research did not confirm that any parameter is *required*.
> 4. Leave a field out rather than guess its value. Every value needs a source in the article body.

## Contents
[1 Guideline](#1-guideline) · [2 Builder script](#2-builder-script) · [3 Index](#3-index) ·
[4 زندگی‌نامه](#4-جعبه-اطلاعات-زندگی‌نامه) · [5 منطقه مسکونی](#5-جعبه-اطلاعات-منطقه-مسکونی) ·
[6 روستای ایران](#6-جعبه-اطلاعات-روستای-ایران) · [7 شرکت](#7-جعبه-اطلاعات-شرکت) · [8 فیلم](#8-جعبه-اطلاعات-فیلم) ·
[9 کتاب](#9-جعبه-اطلاعات-کتاب) · [10 دانشگاه](#10-جعبه-اطلاعات-دانشگاه) · [11 کشور](#11-جعبه-اطلاعات-کشور) ·
[12 آلبوم](#12-جعبه-اطلاعات-آلبوم) · [13 هنرمند موسیقی](#13-جعبه-اطلاعات-هنرمند-موسیقی) ·
[14 Other boxes](#14-other-boxes-short-notes) · [15 Translating an en.wiki infobox](#15-translating-an-enwiki-infobox)

## 1. Guideline

| Rule | Tag / source |
|---|---|
| The guideline page is **«راهنما:جعبه اطلاعات»**. No «ویکی‌پدیا:جعبه اطلاعات» page was found. | [V] [راهنما:جعبه اطلاعات][guide] |
| Infoboxes are **optional**: neither required nor forbidden. | [V] [راهنما:جعبه اطلاعات][guide] |
| An infobox goes **at the top of the article**. Order: hatnotes → maintenance tags → **infobox** → image → sidebars → lead text. | [V] [guide][guide]; [V] [شیوه‌نامه/صفحه‌آرایی][layout] |
| Put the lead **directly after `}}`**, with no blank line. The bot deletes a blank line after the infobox. | [C] [fcc L449-L455][fcc449] |
| Flags generally don't belong in infoboxes (exceptions: ships, sports events). | [V] [راهنما:جعبه اطلاعات][guide] |
| New infobox templates derive from the Persian base `{{جعبه اطلاعات}}`, not the English `{{Infobox}}`. | [V] [الگو:جعبه اطلاعات][base] |
| Biographies: take care with living people (BLP). Don't put religion or sect in the infobox. | [LOW] |
| The fa patrol bot warns when the en.wiki counterpart has an Infobox and the fa article has no `{{جعبه…`. | [C] [zzfawikipatroler_core.py L599-L607][patrol] |
| Multi-value fields (e.g. several actors) use `{{فهرست ساده|…}}`. | [V] [الگو:جعبه اطلاعات فیلم][film] |

Layout (synthesis):
```wikitext
{{جعبه اطلاعات …
| پارامتر = مقدار
}}
'''عنوان مقاله''' …
```

## 2. Builder script

`scripts/infobox_builder.py` builds these boxes offline from YAML or JSON. Keys may be Persian
parameter names or the English aliases shown by `--list`. Lists become `{{فهرست ساده|…}}`. It never
fills in data you did not give it.
```
python3 scripts/infobox_builder.py --list                        # supported boxes + aliases
python3 scripts/infobox_builder.py --template film --skeleton    # empty box, every known param
python3 scripts/infobox_builder.py data.yaml                     # data.yaml has a 'template:' key
python3 scripts/infobox_builder.py data.json --template company --strict   # exit 1 if core params missing
```
Its parameter maps (`scripts/data/infoboxes.json`) follow this file, so they carry the same
uncertainty. The live doc page wins.

Skeletons below are on one line to save space. In an article, put one `| param = value` per line, as in §4.

## 3. Index

| Template (exact name) | Use for | Doc page |
|---|---|---|
| `{{جعبه اطلاعات زندگی‌نامه}}` | people in general | [link][bio] |
| `{{جعبه اطلاعات منطقه مسکونی}}` | cities, towns, divisions (all countries) | [link][settle] |
| `{{جعبه اطلاعات روستای ایران}}` | Iranian villages (wraps منطقه مسکونی) | [link][village] |
| `{{جعبه اطلاعات شرکت}}` | companies (NGOs/international bodies: `{{جعبه اطلاعات سازمان}}`) | [link][company] |
| `{{جعبه اطلاعات فیلم}}` | films | [link][film] |
| `{{جعبه اطلاعات کتاب}}` | books | [link][book] |
| `{{جعبه اطلاعات دانشگاه}}` | universities | [link][uni] |
| `{{جعبه اطلاعات کشور}}` | countries | [link][country] |
| `{{جعبه اطلاعات آلبوم}}` | music albums | [link][album] |
| `{{جعبه اطلاعات هنرمند موسیقی}}` | singers, bands | [link][music] |

## 4. `{{جعبه اطلاعات زندگی‌نامه}}`
[Doc][bio]. Treat this as the canonical name [V]. «جعبه اطلاعات شخص» did not resolve: a 2020 move
proposal exists, but its outcome is unknown [LOW]. `جعبه زندگینامه` is a redirect [LOW]. The doc page
also documents an English `{{Infobox person}}` parameter block [V].

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام` | display name | core | [V] |
| `تصویر`, `alt`, `توضیح تصویر` | image, alt text, caption | core | [V] |
| `نام تولد` | birth name | — | [V] |
| `زادروز` | birth date (age templates such as «تاریخ تولد و سن») | core | [V] |
| `زادگاه` | birthplace | core | [V] |
| `تاریخ درگذشت`, `مکان درگذشت` | death date, place | core if deceased | [V] |
| `ملیت`, `پیشه` | nationality, occupation | core | [V] |
| `شناخته‌شده برای` | known for (ZWNJ spelling [LOW]) | — | [V] |
| `آرامگاه`/`مدفن`, `همسر`, `فرزندان`, `والدین`, `تحصیلات`, `سال‌های فعالیت`, `امضا`, `کارهای برجسته` | misc | — | [LOW] |
| `پودمان` (child box gets `جاسازی‌کردن = بله`) | embed a specialised box | — | [LOW] |

```wikitext
{{جعبه اطلاعات زندگی‌نامه
| نام =
| تصویر =
| توضیح تصویر =
| زادروز =
| زادگاه =
| تاریخ درگذشت =
| مکان درگذشت =
| ملیت =
| پیشه =
}}
```

## 5. `{{جعبه اطلاعات منطقه مسکونی}}`
[Doc][settle]. **`{{جعبه اطلاعات شهر ایران}}` is deprecated.** Use منطقه مسکونی for all settlements
and divisions ([V] [الگو:جعبه اطلاعات شهر ایران][iran-city]). Old شهر ایران parameters, useful only for
reading old articles: `استان`, `شهرستان`, `بخش`, `جمعیت`, `ارتفاع`, `پیش‌شماره`, `پلاک اتومبیل`, `شهردار` [V].

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `نام رسمی` | name, official name | core | [V] |
| `نوع منطقه مسکونی` | settlement type (شهر، روستا…) | core | [V] |
| `نوع زیربخش` / `نام زیربخش` | subdivision type/name (country, province…) | core | names [V]; numbering (`نوع زیربخش۱`?) [UNVERIFIED] |
| `کل جمعیت` | total population (needs a census source) | core | [V] |
| `ارتفاع متر` | elevation in metres | — | [V] |
| `تراکم جمعیت کیلومتر مربع` | density; the value `auto` computes it | — | [V] |
| postal / area code | — | — | names [UNVERIFIED] |

```wikitext
{{جعبه اطلاعات منطقه مسکونی | نام = | نام رسمی = | نوع منطقه مسکونی = | نوع زیربخش = | نام زیربخش = | کل جمعیت = | ارتفاع متر = }}
```

## 6. `{{جعبه اطلاعات روستای ایران}}`
[Doc][village]. A wrapper around منطقه مسکونی. Population can come automatically from the
Statistical Centre of Iran (SCI) code through a module, with Wikidata P1010 as fallback [V concept].

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `نام رسمی` | name | core | [LOW] |
| `استان`, `شهرستان`, `بخش`, `دهستان` | administrative chain (all "suggested") | core | [V] |
| SCI code param (`کد آماری`?) | statistical code; fills population | — | name **[UNVERIFIED]** |
| population, census year | latest SCI census | — | names **[UNVERIFIED]** |
| `دهیار`, area, elevation, phone code, website | misc (area and elevation need a source) | — | [LOW] |

```wikitext
{{جعبه اطلاعات روستای ایران | نام = | استان = | شهرستان = | بخش = | دهستان = }}
```

## 7. `{{جعبه اطلاعات شرکت}}`
[Doc][company]

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `لوگو`, `نوع`, `صنعت` | name, logo, type, industry | core | [V] |
| `بنیان‌گذاری` | founding date | core | [V] |
| `بنیان‌گذار` / `بنیان‌گذاران` | founder(s); plural form for more than one | core | [V] |
| `دفتر مرکزی` (also `شهر دفتر مرکزی`, `کشور دفتر مرکزی`) | headquarters | core | [V] |
| `محصولات`, `درآمد`, `شمار کارکنان` (not `کارکنان`) | products, revenue, employees | — | [V] |
| `مادر` (leave `مالک` empty for subsidiaries), `نام تجاری`, `وبگاه` | parent, brand, website | — | [V] |

```wikitext
{{جعبه اطلاعات شرکت | نام = | لوگو = | نوع = | صنعت = | بنیان‌گذاری = | بنیان‌گذار = | دفتر مرکزی = | وبگاه = }}
```

## 8. `{{جعبه اطلاعات فیلم}}`
[Doc][film]. The title parameter is `عنوان`, not `نام` [V].

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `عنوان`, `تصویر` | title, poster | core | [V] |
| `کارگردان`, `تهیه‌کننده`, `نویسنده`, `بازیگران` | director, producer, writer, cast | core | [V] |
| `موسیقی`, `فیلم‌بردار`, `تدوین`, `استودیو`, `توزیع‌کننده` | music, cinematography, editing, studio, distributor | — | [V] |
| `کشور`, `زبان` | country, language | core | [V] |
| `مدت زمان`, budget, box office | runtime, budget, gross | — | [LOW] |

```wikitext
{{جعبه اطلاعات فیلم | عنوان = | تصویر = | کارگردان = | تهیه‌کننده = | نویسنده = | بازیگران = {{فهرست ساده|…|…}} | کشور = | زبان = }}
```

## 9. `{{جعبه اطلاعات کتاب}}`
[Doc][book]

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام کتاب` (doc comment: `نام` or `عنوان` also work) | title | core | [V] |
| `تصویر`, `نویسنده` | cover, author | core | [V] |
| `برگرداننده` | translator | — | [V] |
| `کشور`, `زبان اصلی`, `سبک`, `موضوع` | country, original language, genre, subject | — | [V] |
| `ناشر`, `تاریخ نشر`, `شابک` | publisher, publication date, ISBN | core | [V] |
| `تعداد_صفحات` | page count (spelled inconsistently in the doc) | — | [LOW] |

```wikitext
{{جعبه اطلاعات کتاب | نام کتاب = | تصویر = | نویسنده = | برگرداننده = | زبان اصلی = | ناشر = | تاریخ نشر = | شابک = }}
```

## 10. `{{جعبه اطلاعات دانشگاه}}`
[Doc][uni]. Rules from the doc [V]: give `تأسیس` in Solar Hijri, with the Gregorian year in
parentheses for foreign universities. `نوع` is one of سراسری (دولتی)، سراسری (غیرانتفاعی)، آزاد، خصوصی،
پیام‌نور، جامع علمی-کاربردی. Staff and student counts are numbers. Write «ندارد» for missing deputies.

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `نام_لاتین` (underscore) | name, Latin name | core | [V] |
| `شعار`, `نوع`, `تأسیس`, `بنیانگذاران` | motto, type, founded, founders | core: نوع، تأسیس | [V] |
| `رئیس`, `دانشجویان` | president, students | — | [V] |
| `نشانی`, `موقعیت`, `شهر`, `کشور` | address, location, city, country | core: شهر، کشور | [V] |
| `وبگاه` / `وب‌سایت` | website (both seen) | — | [LOW] |

```wikitext
{{جعبه اطلاعات دانشگاه | نام = | نام_لاتین = | نوع = | تأسیس = | رئیس = | شهر = | کشور = }}
```

## 11. `{{جعبه اطلاعات کشور}}`
[Doc][country]. The search summary was "partial and messy", so all Persian names here are **[LOW]**.
The same page documents the English `{{Infobox country}}` block (`common_name`, `capital`,
`official_languages`, `government_type`, `area_km2`, `population_estimate`, `currency`) [V].
Countries rarely need a new article; you will usually be editing an existing box.

| Param | Meaning | Tag |
|---|---|---|
| `نام بومی`, `نام رسمی`, `نام رایج` (also `نام عادی`?) | native, official, common name | [LOW] |
| `تصویر پرچم`, `تصویر نشان` | flag, emblem | [LOW] |
| `پایتخت`, `بزرگ‌ترین شهر` | capital, largest city | [LOW] |
| `زبان رسمی` / `زبان‌های رسمی`, `نوع حکومت` | official language(s), government | [LOW] |
| `واحد پول`, `کد واحد پول` | currency, currency code | [LOW] |

Skeleton: copy the parameter list from the live doc page. None is given here because the names are unconfirmed.

## 12. `{{جعبه اطلاعات آلبوم}}`
[Doc][album]

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `نوع`, `هنرمند` | name, type (studio, live…), artist | core | [V] |
| `جلد`, `توضیح تصویر` | cover image, caption | — | [V] |
| `پخش` | release date | core | [V] |
| `ضبط`, `استودیو`, `سبک`, `زمان` | recorded, studio, genre, length | — | [V] |
| `زبان`, `ناشر` (record label), `تهیه‌کننده`, `کارگردان` | language, label, producer, director | — | [V] |

```wikitext
{{جعبه اطلاعات آلبوم | نام = | نوع = | هنرمند = | جلد = | پخش = | سبک = | ناشر = }}
```

## 13. `{{جعبه اطلاعات هنرمند موسیقی}}`
[Doc][music]

| Param | Meaning | Core | Tag |
|---|---|---|---|
| `نام`, `تصویر` | name, image | core | [UNVERIFIED] (assumed from other boxes) |
| `پیش‌زمینه` | `خواننده_تک`/`solo_singer` or `گروه`/`group_or_band`; sets the box colour | core | [V] |
| `سبک`, `ساز`, `سازهای برجسته` | genre, instrument(s), notable instruments | — | [V] |
| `سال‌های فعالیت` | years active | core | [V] |
| `ناشر` | record label (there is no `شرکت ضبط`) | — | [V] |

```wikitext
{{جعبه اطلاعات هنرمند موسیقی | نام = | تصویر = | پیش‌زمینه = خواننده_تک | سبک = | ساز = | سال‌های فعالیت = | ناشر = }}
```

## 14. Other boxes (short notes)

- **`{{جعبه اطلاعات بازیگر}}`** ([doc][actor]): `نام`, `تصویر`, `توضیح تصویر`, `نام اصلی`, `زمینه فعالیت`, `تاریخ تولد`, `محل تولد`, `تاریخ مرگ`, `محل مرگ`, `ملیت`, `سال‌های فعالیت`, `وب‌گاه`, `جوایز` [V]. The full form adds `همسر`, `فرزندان`, `مدفن` and per-award parameters (اسکار، سیمرغ بلورین…) [LOW]. **Note:** it uses `تاریخ تولد`/`محل تولد`, while زندگی‌نامه uses `زادروز`/`زادگاه`, so don't copy names between the two. The skeleton header reads «جعبه اطلاعات هنرپیشه», probably a redirect [LOW].
- **`{{جعبه اطلاعات ورزشکار}}`** ([doc][athlete]): `قد به سانتی‌متر`, `موقعیت`, `باشگاه`, `تیم` [V].
- **`{{Infobox football biography}}`** (doc reached through [الگو:جعبه اطلاعات مربی فوتبال][football]): an English-named template with **English parameters** on fa.wiki: `youthclubs1`/`youthyears1`, `years1`/`clubs1`/`caps1`/`goals1`, `nationalyears1`/`nationalteam1`/`nationalcaps1`/`nationalgoals1` [LOW]. A Persian-named equivalent is [UNVERIFIED]. This is one place where an English template name is normal, so a WC07/WC08 warning here may be a false alarm.
- **`{{جعبه اطلاعات سمت رسمی}}`** ([doc][office]) describes an **office**, not a person: `پیشین`, `جانشین`, `مدت تصدی`, `نخستین متصدی` [V]. For politicians, `{{جعبه اطلاعات سیاست‌مدار}}` (with `حزب سیاسی`) is [LOW]. `{{Infobox officeholder}}` exists, with parameter language unknown [LOW].

## 15. Translating an en.wiki infobox

1. Find the fa template by topic in §3. Don't paste the English `{{Infobox …}}`: `wikitext_check.py` flags English template names (**WC08**) and unknown templates (**WC07**).
2. Map each parameter by **meaning**, using the tables above and the live doc page. Names differ between boxes (see the بازیگر note).
3. Persian prose values follow the style rules (Persian digits, Solar dates where the article uses them; see `orthography.md`). Keep file names, URLs and codes as they are.
4. Drop any value that the fa article body does not support with a source.
5. Ask the user to check the result against the template's doc page, because of the caveat at the top.

[guide]: https://fa.wikipedia.org/wiki/راهنما:جعبه_اطلاعات
[layout]: https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی
[base]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات
[bio]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_زندگی‌نامه
[settle]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_منطقه_مسکونی
[iran-city]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_شهر_ایران
[village]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_روستای_ایران
[company]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_شرکت
[film]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_فیلم
[book]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_کتاب
[uni]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_دانشگاه/توضیحات
[country]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_کشور
[album]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_آلبوم
[music]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_هنرمند_موسیقی
[actor]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_بازیگر
[athlete]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_ورزشکار
[football]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_مربی_فوتبال
[office]: https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_سمت_رسمی
[fcc449]: https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L449-L455
[patrol]: https://github.com/PersianWikipedia/fawikibot/blob/master/Need2convert/zzfawikipatroler_core.py#L599-L607
