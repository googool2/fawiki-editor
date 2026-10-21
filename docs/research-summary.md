# fawiki-editor — Stage-0 research summary: fa.wikipedia policies and conventions

Research date: 2026-10-21. This is an **index of rules with sources**, not a restatement of policy. Every row has a source and a confidence tag. Re-verify before release (§6).

## 1. Method & limitations

> **Read this first.** wikipedia.org, and every mirror and archive, was **blocked from the research environment** (fa.wikipedia.org fetches failed with DNS `ENOTFOUND`). **No policy page was read in full.**

- **Pages.** WebSearch was restricted to `fa.wikipedia.org` (extended mode). It returns engine excerpts or summaries tied to a URL. Quotes may be trimmed, paraphrased, cached or out of date. Section names are as the excerpts reported them.
- **Code.** The code was read but not executed. It shows what the tools *do*, not what policy *says*. All links point to `master`, except citer.
  - From PersianWikipedia/fawikibot @ `04dde6d`:
    - **FCC** = `fa_cosmetic_changes_core.py`, the cosmetic-changes bot.
    - **AA** = `AbarAbzar.py`, a Python port of the ابرابزار gadget.
    - **CD** = `CheckDictation.py` + `checkdictation-fa/`, the اشتباه‌یاب backend. **WWD** is its wrong-word list.
  - **PT** = ebraminio/persiantools @ `06900ef` (2013).
  - **citer** = 5j9/citer @ `fab6d27` (2026-10-19), the current fa citation generator.
  - brothersincode/virastar was used for comparison only.
- **Tags.**
  - **[V]**: a Persian quote or close paraphrase was returned for that URL.
  - **[C]**: verified in code at the linked lines.
  - **[LOW]**: search summary only, or an inference.
  - **[UNVERIFIED]**: no source found.
  - `[V] [C]` means both.
- **Code points.** Only ی 1740, ي 1610, ٬ 1644 and ٫ 1643 are quoted from pages. Every other character mapping comes from tool code.
- **Status.** The MOS (شیوه‌نامه) is a **guideline (رهنمود), not a policy**.
- **Rows.** Rows that bundle several rules share one source and one tag.

## 2. Page-title corrections vs. the original brief

| Brief / assumed | fa.wiki actual | Source | Tag |
|---|---|---|---|
| ویکی‌پدیا:اثبات‌پذیری | **ویکی‌پدیا:تأییدپذیری** («اثبات‌پذیر» appears only in prose on other pages) | [تأییدپذیری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری) | [V] |
| ویکی‌پدیا:شیوه یادکرد منابع | **ویکی‌پدیا:شیوه ارجاع به منابع** (no page with the brief's title was found) | [شیوه ارجاع به منابع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه_ارجاع_به_منابع) | [V] |
| {{ترجمه}} | **{{صفحه ترجمه‌شده}}**, placed on the **talk** page | [الگو:صفحه ترجمه‌شده](https://fa.wikipedia.org/wiki/الگو:صفحه_ترجمه‌شده) | [V] |
| {{جعبه اطلاعات شخص}} | **{{جعبه اطلاعات زندگی‌نامه}}**. «شخص» did not resolve; a 2020 move proposal has an unknown outcome. | [الگو:جعبه اطلاعات زندگی‌نامه](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_زندگی‌نامه) | [V] |
| ویکی‌پدیا:جعبه اطلاعات | **راهنما:جعبه اطلاعات** | [راهنما:جعبه اطلاعات](https://fa.wikipedia.org/wiki/راهنما:جعبه_اطلاعات) | [V] |
| {{جعبه اطلاعات شهر ایران}} | **Deprecated.** Use **{{جعبه اطلاعات منطقه مسکونی}}** for all settlements. | [الگو:جعبه اطلاعات شهر ایران](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_شهر_ایران) | [V] |
| BLP page | **ویکی‌پدیا:زندگی‌نامه زندگان** | [زندگی‌نامه زندگان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:زندگی‌نامه_زندگان) | [V] |
| Words to watch | **ویکی‌پدیا:شیوه‌نامه/واژه‌هایی که باید مواظب استفاده از آن‌ها بود**. Alternate slug: `…/واژه‌هایی_که_باید_از_آن‌ها_دوری_گزید`. | [page](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/واژه‌هایی_که_باید_مواظب_استفاده_از_آن‌ها_بود) | [V] |
| ویکی‌پدیا:ترجمه | **راهنما:ترجمه** plus **ویکی‌پدیا:خودآموز (ترجمه)**. Whether ویکی‌پدیا:ترجمه exists is unconfirmed. | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) | [V] |
| {{citation needed}} | **{{مدرک}}**, which resolves to the page «الگو:نیازمند منبع» | [الگو:مدرک](https://fa.wikipedia.org/wiki/الگو:مدرک) | [V] |
| {{Reflist}} / `<references/>` | **{{پانویس}}**. The bot rewrites the others to it. | [FCC L403-404](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L403-L404) | [C] |
| {{Infobox}} base | **{{جعبه اطلاعات}}** | [الگو:جعبه اطلاعات](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات) | [V] |
| PROD / AfD / db-* | **حذف زمان‌دار** / **نظرخواهی برای حذف** («نبح») / **{{حس-…}}** | [حذف زمان‌دار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:حذف_زمان‌دار), [الگو:الگوهای حذف سریع](https://fa.wikipedia.org/wiki/الگو:الگوهای_حذف_سریع) | [V] |

## 3. Rules by area

### 3.1 Manual of Style: orthography (رسم‌الخط)
| Rule | Source | Tag |
|---|---|---|
| The MOS is a guideline (رهنمود), not a policy. Following it is recommended. | [سیاست‌ها و رهنمودها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سیاست‌ها_و_رهنمودها) | [V] |
| The baseline is the Academy's دستور خط («برگرفته از کتاب دستور خط فرهنگستان») | [دستور خط § intro](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| املای برخی واژه‌ها follows the Academy's دستور خط فارسی and فرهنگ املایی | [املای برخی واژه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/املای_برخی_واژه‌ها) | [LOW] |
| Formal register: no first person and no colloquial contractions | [شیوه‌نامه § TOC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [LOW] |
| Use Persian ی (1740) and ک; never Arabic ي (1610) or ك | [شیوه‌نامه § کد صحیح نویسه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [FCC L129-140](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L129-L140) | [V] [C] |
| Arabic-language text keeps Arabic letters. Wrap it in {{عبارت عربی}} or {{آغاز عربی}}…{{پایان عربی}}. | [شیوه‌نامه § Arabic text](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [LOW] |
| Ezafe after silent ه in body text is ه + ٔ (خانهٔ), not خانه / خانه ی / خانه‌ی. The precomposed ۀ is banned. | [شیوه‌نامه § اضافه پس از «ه» ناملفوظ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| دستور خط: use «-ٔ» after silent ه «به جز در عنوان مقاله‌ها» | [دستور خط § کسرهٔ اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| می / همی always take ZWNJ (می‌رود، همی‌گوید). Applying this to نمی‌ is an inference [LOW]. | [دستور خط § می و همی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| Plural ها never takes a full space. Joined and ZWNJ forms are both correct (کتابها / کتاب‌ها). | [دستور خط § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| ZWNJ before ها is mandatory for: foreign words; stem emphasis; many teeth (حساسیت‌ها); ط/ظ endings; silent ه (خانه‌ها); pronounced ه after a joining letter (فقیه‌ها) | same §; [نیم‌فاصله § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| تر / ترین always take ZWNJ, except بهتر، مهتر، کهتر، بیشتر، کمتر | [نیم‌فاصله § تر و ترین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| Pronoun suffixes ـم ـت ـش ـمان ـتان ـشان are written joined | [نیم‌فاصله § ضمیرهای متصل](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| ی / ای / ام after silent ه, consonant ی or vowel ای take ZWNJ (خانه‌ای، کشتی‌ای، کشتی‌ام). After ا/و, «یی» is joined (دانشجویی). | [نیم‌فاصله § ی پایانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله); [دستور خط § میانجی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| بی / هم prefixes take ZWNJ, except in lexicalised words (بیهوده، همسایه، همکار). This needs a whitelist. | [نیم‌فاصله § بی / هم](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| Compounds take ZWNJ (دست‌کم، سیب‌زمینی، دل‌انگیز). Per-word disputes go to an RfC [LOW]. | [نیم‌فاصله § کلمات مرکب](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| Preposition به is written separately (به‌سختی), except in بدین، بدان، بدو، بدیشان | [دستور خط § به](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| ZWNJ is typed with Shift+Space | [نیم‌فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] |
| Names such as بهنام and بهروز take no ZWNJ | same | [LOW] |
| Copula (است / ام…) ZWNJ rules: the section «صورت‌های متصل فعل بودن» exists, but its text was not retrieved | same | [UNVERIFIED] |
| Hamza seat follows the preceding vowel: ئ (هیئت), أ (تأثیر), ؤ (مؤسسه). مسئله and مسئول take ئ as exceptions (garbled excerpt). | [شیوه‌نامه § همزه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [دستور خط § همزهٔ میانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [LOW] |
| Tanvin is allowed only on Arabic-origin words, where pronounced, in text and titles. It is wrong on Persian or European words (گاهاً، تلفناً، زباناً). | [دستور خط § تنوین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| ة becomes ت before tanvin (موقتاً). Otherwise ة → ت if pronounced /t/, or ه if /e/. | [دستور خط § ة](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| Use Persian digits ۰–۹, not Arabic ٠–٩ or Latin 0–9. The code points differ even where glyphs look alike. | [تاریخ‌ها و اعداد § ارقام](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| اتاق, not اطاق; امپراتور, not امپراطور. The page rule ([شیوه عبارات عربی § طای مؤلف](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه_عبارات_عربی)) is [LOW]; the code lists confirm it. | [WWD L41](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L41), [L52](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L52) | [C] |

### 3.2 Manual of Style: punctuation
| Rule | Source | Tag |
|---|---|---|
| Quotes use only «». Use them for direct quotes, and for names or terms only on first use. | [نشانه‌های نگارشی § گیومه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی) | [V] |
| ؛ is a pause between comma and full stop, with few uses. ؟ is not used for indirect questions, and repeated ؟؟ is unsuitable. | same § نقطه‌ویرگول, § علامت سؤال | [V] |
| Never use ، or , to group digits | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| Single marks (. ، ؛ ؟ !) attach left and take one space after. Paired marks take a space outside and none inside. (Only the group names منفرد / مزدوج are quoted.) | [شیوه‌نامه § نشانه‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [LOW] |
| Avoid nested parentheses except in formulas | [نشانه‌های نگارشی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی) | [LOW] |
| An explicit rule to use ، ؛ ؟ instead of , ; ? is only implied. The tools enforce it (§3.17). | — | [UNVERIFIED] |
| No space after an internal abbreviation dot: «ر.ک.», not «ر. ک.» | [کوته‌نوشت § فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/کوته‌نوشت) | [V] |

### 3.3 Manual of Style: dates & numbers
| Rule | Source | Tag |
|---|---|---|
| Date format is day (digits), month (word), year (digits): «۲۹ آذر ۱۳۹۵» | [گاهشماری هجری خورشیدی § شیوهٔ نگارش](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی) | [V] |
| No slash, hyphen or comma between date parts. The day is a digit, not an ordinal, unless the sentence starts with the date. No leading zero (۰۷ → ۷). | [تاریخ‌ها و اعداد § قالب تاریخ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| Gregorian months (Iran usage) include ژانویه، فوریه، مه، ژوئن، ژوئیه، اوت. Afghan forms (جنوری، فبروری، مارچ) and جون/جولای/آگوست are noted. | same § نام ماه‌ها | [V] |
| The other six month names were not quoted. آوریل appears in a DATES example, and دسامبر in [FCC L255-257](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L255-L257). | — | [UNVERIFIED] |
| Solar months use the standard forms فروردین … اسفند | same § ماه‌های شمسی | [LOW] |
| Contemporary solar-calendar articles need no Gregorian equivalent | [گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی) | [V] |
| Abbreviations: ه‍.ق، ه‍.ش، ه‍.خ (joined ه‍, no final dot; «ه.ق» is wrong). Gregorian «م». BC «ق.م» («ق.م.» and «ق م» are wrong). | [کوته‌نوشت § تاریخ, table](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/کوته‌نوشت) | [LOW] |
| Four solar abbreviations exist (ه‍.خ، ه‍.ش، خ، ش). The RfC on choosing one found no consensus. | [نظرخواهی/علامت اختصاری…](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/علامت_اختصاری_گاهشماری_هجری_خورشیدی) | [V] |
| Centuries and millennia are usually spelled out (سدهٔ هفتم هجری قمری) | [تاریخ‌ها و اعداد § سده](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| Ordinals are spelled out (پنجم, not ۵ام; مهرداد دوم). Decades are written «دههٔ ۱۹۸۰», not «۱۹۷۰ها». | same § اعداد ترتیبی, § دهه | [V] |
| Spell out 0–9 in prose. Never spell out digits in formulas. Proper names keep their digits (خیابان ۱۷ شهریور). | same § اعداد | [V] |
| Thousands separator ٬ (U+066C, 1644), e.g. ۲۴٬۷۰۰٬۰۰۰. Decimal separator ٫ (U+066B, 1643), never «/». | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [جداکننده هزارگان](https://fa.wikipedia.org/wiki/جداکننده_هزارگان) | [V] |
| Number–unit spacing; percent and currency rules | [تاریخ‌ها و اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [UNVERIFIED] |
| Link a date only when it is related to the subject | same § پیوند | [V] |

### 3.4 Manual of Style: titles and formatting of works
| Rule | Source | Tag |
|---|---|---|
| No ezafe hamza (هٔ) in titles ("to make search easier"). No اعراب (diacritics) in the main title. | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| Related RfCs: [2014 هٔ RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/تغییر_شیوه‌نامه_برای_بکارگیری_«هٔ»_در_عنوان_مقاله‌ها) (summarised as no consensus to allow); [title-clause RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/تغییر_بند_سیاست_عنوان_صفحه‌ها) (outcome unknown); [minimal-diacritics RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_اعراب_در_عنوان_مقالات_ابهام‌دار_به_شرط_موجود_بودن_تغییرمسیر_بدون_اعراب) (status unclear) | links in cell | [LOW] |
| Tanvin is allowed in titles | [RfC § جمع‌بندی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_تنوین_در_عنوان_مقاله) | [V] |
| Titles follow دستور خط spacing and ZWNJ (اسکی‌محله; عادل‌ها, not عادلها or عادل ها) | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| Titles use Persian characters, with no # $ & * | same; [قواعد نام‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری) | [LOW] |
| In running text, italicise books, films, albums, plays, TV series and periodicals. Put «» around songs, short poems, short stories, articles and episodes. Scriptures and legal documents get neither. | [قالب‌بندی متون § عنوان آثار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/قالب‌بندی_متون) | [V] |

### 3.5 Manual of Style: transliteration and foreign names
| Rule | Source | Tag |
|---|---|---|
| Criterion is wide use in Persian reference works. Keep an established form; otherwise follow native pronunciation. Give common alternates in the lead. | [قواعد نام‌گذاری (فارسی‌سازی نام‌های خارجی)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_(فارسی‌سازی_نام‌های_خارجی)) | [LOW] |
| If no established form exists: IPA first, then the IPA → Persian guide (Pinyin table included). If there is no Persian written record: the Academy's 1381 «شیوه‌نامه ضبط اعلام». Per-language pages exist; a word-specific consensus overrides them. | [نویسه‌گردانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نویسه‌گردانی); [راهنما:الفبای آوانگاری…](https://fa.wikipedia.org/wiki/راهنما:الفبای_آوانگاری_بین‌المللی_فارسی); [نگارش نام‌های خارجی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نگارش_نام‌های_خارجی); [آلمانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:زبان_و_زبان‌شناسی/نویسه‌گردانی_آلمانی) | [LOW] |
| An English-letter → Persian table (e.g. for "th") | — | [UNVERIFIED] |

### 3.6 Manual of Style: links
| Rule | Source | Tag |
|---|---|---|
| Link a term once, at first occurrence. This does not apply to captions, infoboxes, templates or tables. Avoid overlinking, especially in the lead. | [پیونددهی § پیوند تکراری, § پیوند بیش از حد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/پیونددهی) | [LOW] |
| Don't link dates or years unless relevant (an architect's birth year: no; a film's release year: may). The پیونددهی § تاریخ‌ها version is [LOW]. | [تاریخ‌ها و اعداد § پیوند](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| Link the most specific article, or a section of it. Sources go in منابع as citations, not in پیوند به بیرون. No external links in body text. | [شیوه‌نامه § پیوند](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [LOW] |
| No links in section headings. Use {{اصلی}} or {{همچنین ببینید}} under the heading instead. | [صفحه‌آرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی) | [V] |
| Don't link the bolded title in the first sentence | [راهنمایی برای نوشتن مقاله‌های بهتر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:راهنمایی_برای_نوشتن_مقاله‌های_بهتر) | [LOW] |

### 3.7 Manual of Style: lead section
| Rule | Source | Tag |
|---|---|---|
| Bold the subject once, at first natural mention. The first sentence is a short definition unless the title is self-descriptive. The lead stands alone and summarises every main section. | [بخش آغازین § پررنگ‌کردن](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/بخش_آغازین) | [LOW] |
| Lead length by article size: <15k characters → 1–2 paragraphs; 15–30k → 2–3; >30k → 3–4 | same § طول بخش آغازین | [LOW] |
| Biography lead: name, dates, nationality, main roles. Birth and death places go in the body. Consider privacy for the living. | [زندگی‌نامه‌ها § بخش آغازین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/زندگی‌نامه‌ها) | [LOW] |
| Exact format of the birth/death parenthesis, e.g. «(زادهٔ … – درگذشتهٔ …)» | — | [UNVERIFIED] |

### 3.8 Manual of Style: layout and section order
| Rule | Source | Tag |
|---|---|---|
| Top of page: hatnotes → maintenance tags → infobox → image → sidebars → lead → TOC | [صفحه‌آرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی) | [V] |
| End sections: جستارهای وابسته → پانویس / منابع (may be one section) → برای مطالعهٔ بیشتر → پیوند به بیرون → navboxes | same § بخش‌های پایانی | [V] |
| After navboxes: stub → {{ترتیب‌پیش‌فرض}} → categories (from the sample layout) | same § نمونه | [LOW] |
| جستارهای وابسته: relevant links only; no red or dab links «به هیچ وجه»; a navbox is preferred over a list | same § جستارهای وابسته | [V] |
| «منابع» is the common heading; separating notes is optional. برای مطالعهٔ بیشتر is alphabetical with no duplicates. Use the singular «پیوند به بیرون»; sister-project links go there except ویکی‌واژه / ویکی‌نبشته. | same § منابع, § پیوند به بیرون | [LOW] |
| Level-2 headings for main sections. Never level 1, no skipped levels, headings unique. Images go in the section they illustrate. | same; [راهنما:بخش](https://fa.wikipedia.org/wiki/راهنما:بخش) | [LOW] |
| At most four stub templates, placed below navboxes and above categories | [الگو:خرد](https://fa.wikipedia.org/wiki/الگو:خرد); [مقاله خرد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:مقاله_خرد) | [V] |
| Categories «در پایان متن و پیش از الگوهای خرد». This conflicts with the stub row above (see §5). | [رده‌بندی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:رده‌بندی) | [LOW] |

### 3.9 Naming conventions (قواعد نام‌گذاری)
| Rule | Source | Tag |
|---|---|---|
| Use the common name from reliable Persian sources. The ideal title is «کوتاه، معمولی، قابل تمایز و قابل شناختن». | [قواعد نام‌گذاری § عنوان ایدئال](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری) | [V] |
| Use the singular, unless the name is always plural in Persian | same § مفرد و جمع | [V] |
| Parenthetical disambiguation only when natural disambiguation is impossible, and only to disambiguate | [ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی) | [V] |
| One space before the parenthesis («کازابلانکا (فیلم)»); the simplest qualifier («موز (اسطوره)»); the primary topic gets the bare title; a single-use name gets no parentheses | same | [V] |
| Films: «فیلم» plus the release year | [(فیلم‌ها)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_(فیلم‌ها)) | [LOW] |
| Places: parentheses, not a comma. Same-named Iranian villages take the شهرستان in parentheses. | [(اسامی جغرافیایی)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_(اسامی_جغرافیایی)) | [LOW] |
| People: given + family name, with redirects. Pseudonyms: as reliable sources use them. No honorifics unless unambiguous and better known. Keep «سید» unless widely known without it. | [(اشخاص)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_(اشخاص)) | [LOW] |

### 3.10 Notability (سرشناسی) and subject guidelines
| Rule | Source | Tag |
|---|---|---|
| Significant (direct, detailed, non-passing) coverage in independent reliable sources gives a presumption, not a guarantee. Notability is not temporary. | [سرشناسی § رهنمود عمومی, § پوشش قابل توجه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی) | [LOW] |
| Sources need to exist, not necessarily be cited («تنها نیازمندِ وجود منابع…») | [سرشناسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی) | [V] |
| Sources should be secondary, multiple and independent. Non-independent sources never establish notability. | same; [منابع مستقل](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_مستقل) | [LOW] |
| Notability ≠ importance; it is a property of the topic, not the article | same; [الگو:سرشناسی](https://fa.wikipedia.org/wiki/الگو:سرشناسی) | [V] |
| Tag with {{سرشناسی}} (topic form {{سرشناسی\|موسیقی}}). Remove the tag once ≥2 reliable sources with significant coverage are cited. | [الگو:سرشناسی § usage](https://fa.wikipedia.org/wiki/الگو:سرشناسی) | [V] |
| People, basic criterion: multiple independent secondary sources (thin ones may combine). Primary sources don't establish notability. | [سرشناسی (افراد) § معیار پایه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(افراد)) | [LOW] |
| People: a significant contribution that «بخشی از تاریخ آن علم/رشته شده است» | same § معیارهای تکمیلی | [V] |
| People: national or provincial office holders and legislators (local office is not enough); athletes; entertainers; one-event people; voice actors (دوبلورها) | same | [LOW] |
| Organisations: local media alone is not enough; ≥1 regional or wider source needed; routine coverage excluded | [سرشناسی (سازمان‌ها و شرکت‌ها)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(سازمان‌ها_و_شرکت‌ها)) | [LOW] |
| Web: no article only to describe a site. Must meet one of three criteria: non-trivial independent works, a known award, or a respected independent medium. | [سرشناسی (وب)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(وب)) | [V] |
| [Books](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(کتاب‌ها)): major award, or course use at ≥2 institutions. [Films](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(فیلم‌ها)): wide release + ≥2 national critics, or coverage ≥5 years later. [Music](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(موسیقی)): ≥2 albums on a notable label, gold, award or nomination. [Sports](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(ورزش‌ها)): club sites and blogs are not independent. | links in cell | [LOW] |
| Other subject guidelines exist: [دانشگاهیان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(دانشگاهیان)), [جغرافیا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(جغرافیا)), [رویدادها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سرشناسی_(رویدادها)) | links in cell | [LOW] |
| Content of the RfC on keeping or deleting Iran/Afghanistan biographies | [RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/اصلاح_روند_حذف_یا_ماندگاری_مقاله‌های_افراد_مرتبط_با_ایران_و_افغانستان) | [UNVERIFIED] |

### 3.11 Verifiability, NOR, NPOV, BLP, words to watch, maintenance tags
| Rule | Source | Tag |
|---|---|---|
| The threshold for inclusion is verifiability, not truth. The burden is on whoever adds or restores material. | [تأییدپذیری § lead, § مسئولیت ارائه منبع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری) | [V] |
| Unsourced material may be challenged and removed. Quotes and challenged (or likely-challenged) material need an inline citation. | same | [V] |
| Self-published sources are mostly unacceptable (except an established, already-published expert). Wikipedia in any language, and its mirrors, are not sources. | same (ویکی‌پدیا:خودچاپ‌کرده); [منابع معتبر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_معتبر) | [LOW] |
| منابع معتبر is a guideline and restates the adder's burden | [منابع معتبر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_معتبر) | [V] |
| No original research, and no synthesis across or within sources. Simple calculations are allowed. NOR, NPOV and V are read together. | [تحقیق دست‌اول ممنوع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تحقیق_دست‌اول_ممنوع) | [LOW] |
| NPOV: present all published reliable views fairly and proportionately. Due weight follows prominence; tiny-minority views go only in their own articles. | [دیدگاه بی‌طرف § lead, § وزن نامتناسب](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دیدگاه_بی‌طرف) | [V] |
| No false balance for minority views. Attribute opinions in the text; don't state them as fact. | same | [V] |
| BLP: remove contentious material about living or recently dead people at once, whatever its tone, if it is unsourced or poorly sourced, OR or synthesis, or self-published (unless by the subject) | [زندگی‌نامه زندگان § lead](https://fa.wikipedia.org/wiki/ویکی‌پدیا:زندگی‌نامه_زندگان) | [V] |
| BLP: don't tag it {{مدرک}} or move it to the talk page. Whoever restores it carries the burden. Disputes go to «…/تابلوی اعلانات». | same; [نیازمند منبع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیازمند_منبع) | [V] |
| Words to watch: no word is always banned. Puffery (§ تکلف) such as تحسین‌آمیز، خیره‌کننده، زیبا، بهترین is acceptable only as an attributed opinion. | [واژه‌هایی که باید مواظب…](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/واژه‌هایی_که_باید_مواظب_استفاده_از_آن‌ها_بود) | [LOW] |
| Use contentious labels (فرقه، نژادپرست، تروریست، مبارز آزادی) sparingly. For weasel words (برخی مردم می‌گویند…), name the source or restate as verifiable fact. | same; [الفاظ طفره‌آمیز](https://fa.wikipedia.org/wiki/الفاظ_طفره‌آمیز) | [LOW] |
| A fuller Persian peacock list (برجسته، افسانه‌ای…). Don't invent one. | — | [UNVERIFIED] |
| {{مدرک}} takes `تاریخ` and `توضیح` (the exact date format is [LOW]) | [الگو:مدرک](https://fa.wikipedia.org/wiki/الگو:مدرک) | [V] |
| {{بدون منبع}} (whole article unreferenced) is recommended instead of deletion, together with {{منبع مستقل}} | [منابع مستقل](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_مستقل) | [V] |
| {{یک منبع}} marks reliance on one source. {{ابهام‌زدایی}} goes at the bottom of dab pages, before categories. | [مقالات با یک منبع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:مقالات_با_یک_منبع); [الگو:ابهام‌زدایی](https://fa.wikipedia.org/wiki/الگو:ابهام‌زدایی) | [LOW] |
| Is {{منبع}} a separate template? FCC rewrites it to {{بدون منبع}} ([FCC L441-448](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L441-L448)). | — | [UNVERIFIED] |

### 3.12 Citation style and citation templates
| Rule | Source | Tag |
|---|---|---|
| The guide is Chicago-based with numbered footnotes. Harvard, Vancouver and APA are accepted. | [شیوه ارجاع به منابع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه_ارجاع_به_منابع) | [V] |
| Short footnotes with {{پک}} pointing to full citations in منابع are "the preferred method". Surname and year must match. Don't bundle; repeat the footnote. | same; [الگو:پانویس کوتاه‌شده](https://fa.wikipedia.org/wiki/الگو:پانویس_کوتاه‌شده) | [V] |
| `<ref>{{پک\|Surname\|Year\|ک=Title\|زبان=en\|ص=Page}}‏</ref>`; use {{پک/بن}} when there is no author; citer adds an RLM before `</ref>` | [citer L46-52](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L46-L52), [L223-240](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L223-L240) | [C] |
| Named refs: define once and reuse `<ref name="x" />`. Names are case-sensitive, unique and not purely numeric; quote names with spaces. | [راهنما:پانویس‌ها](https://fa.wikipedia.org/wiki/راهنما:پانویس‌ها) | [V] |
| The reference list is {{پانویس}} under `== منابع ==`. The bot inserts it when missing and joins refs to the preceding text. | [FCC L122-124](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L122-L124), [L432-434](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L432-L434), [L465](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L465) | [C] |
| {{پانویس}} options: `\|۲` (columns; the bot adds it above 7 refs), `عرض=۳۰`, `چپ‌چین=بله` | [الگو:پانویس](https://fa.wikipedia.org/wiki/الگو:پانویس); [FCC L407-420](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L407-L420) | [V] [C] |
| `اندازه=` "no longer has any effect", so don't emit it (FCC still writes it) | [الگو:پانویس](https://fa.wikipedia.org/wiki/الگو:پانویس); [FCC L408](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L408) | [V] [C] |
| `گروه=` exists in bot code, but its documented meaning is unclear | [FCC L419](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L419) | [LOW] |
| Use the calendar printed in the source (e.g. Solar Hijri for books published in Iran) | [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) | [V] |
| The CS1 module is پودمان:Citation/CS1/fa. `زبان=en` routes the citation to the English module. Persian and English parameter names are interchangeable "per the list". | [پودمان:Citation/CS1/fa/توضیحات](https://fa.wikipedia.org/wiki/پودمان:Citation/CS1/fa/توضیحات); [الگو:Cite journal](https://fa.wikipedia.org/wiki/الگو:Cite_journal) | [V] |
| Identifiers stay English inside Persian templates: `doi`, `pmid`, `pmc`, `issn`, `oclc`, `jstor`, `*-access=free` | [citer L141-170](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L141-L170) | [C] |
| Whether `url`/`title`/`access-date` are accepted inside {{یادکرد …}} is unknown. Emit Persian names for core fields. | — | [LOW] |
| Access date must include the day. Future or very old dates raise an error. | [راهنما:خطاهای الگوی یادکرد](https://fa.wikipedia.org/wiki/راهنما:خطاهای_الگوی_یادکرد) | [V] |
| Dates in ISO `YYYY-MM-DD` (citer output; the یادکرد وب doc prefers ISO 8601). Author parameters are numbered with Persian digits (`نام خانوادگی۱`). | [citer L172-176](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L172-L176); [test L43](https://github.com/5j9/citer/blob/fab6d27/tests/test_fa.py#L43) | [C] |
| Archive: `نشانی بایگانی` or `پیوند بایگانی`, plus `تاریخ بایگانی`. URL: `نشانی` or `پیوند`. | [webcite.py L151-155](https://github.com/PersianWikipedia/fawikibot/blob/master/webcite.py#L151-L155), [L186-188](https://github.com/PersianWikipedia/fawikibot/blob/master/webcite.py#L186-L188) | [C] |
| {{یادکرد وب}} requires `نشانی` (or `پیوند`) and `عنوان` | [الگو:یادکرد وب](https://fa.wikipedia.org/wiki/الگو:یادکرد_وب); [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) | [V] [C] |
| یادکرد وب optional parameters: `نام خانوادگی`/`نام`/`نویسنده`, `تاریخ`, `وبگاه`, `اثر`, `ناشر`, `تاریخ بازبینی` | [citer L101](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L101), [L234](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L234) | [C] |
| `کد زبان` (ISO code) changes formatting; `زبان` only appends "(language)". `پیوند مرده` takes `آری` / `نه`. | [الگو:یادکرد وب](https://fa.wikipedia.org/wiki/الگو:یادکرد_وب); [citer L208](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L208) | [V] [C] |
| Aliases not confirmed: `تاریخ بازدید` (= `تاریخ بازبینی`), `نقل قول`, `قالب`, `صفحه` (وب), `ترجمه عنوان`, `شهر` (کتاب), `دوره` (ژورنال) | [یادکرد وب](https://fa.wikipedia.org/wiki/الگو:یادکرد_وب); [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع); [Cite journal](https://fa.wikipedia.org/wiki/الگو:Cite_journal) | [LOW] |
| {{یادکرد کتاب}}: `عنوان` is required. Also `نام خانوادگی`/`نام`, `نویسنده`, the editor set, `دیگران`, `فصل`, `ناشر`, `مکان`, `ویرایش`, `سری`, `جلد`, `سال`/`تاریخ`, `صفحه`, `زبان`, `oclc`. | [citer L54-60](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L54-L60), [test L28-33](https://github.com/5j9/citer/blob/fab6d27/tests/test_fa.py#L28-L33) | [C] |
| The translator parameter is **`ترجمه`** (names joined with «، » / « و ») | same; [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) | [V] [C] |
| `مترجم` and `صفحه‌ها` were never seen | — | [UNVERIFIED] |
| `شابک`: digits, hyphens optional, auto-linked | [الگو:Cite book](https://fa.wikipedia.org/wiki/الگو:Cite_book); [isbn_fix.py L144](https://github.com/PersianWikipedia/fawikibot/blob/master/isbn_fix.py#L144) | [V] [C] |
| {{یادکرد ژورنال}}: `عنوان` and `ژورنال` are required. Also `جلد`, `شماره`, `صفحه` (en-dash range `17–19`), `سال`. Prefer `doi` over a URL. | [citer L95-99](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L95-L99), [L127-130](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L127-L130) | [C] |
| citer does not emit {{یادکرد خبر}}; it maps news to یادکرد وب | [citer L23-37](https://github.com/5j9/citer/blob/fab6d27/lib/generator_fa.py#L23-L37) | [C] |
| یادکرد خبر: `نشانی`, `عنوان`, `نام خانوادگی`, `نام`, `ناشر`, `تاریخ بازبینی`, archive parameters, `کد زبان` | [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) | [V] |
| یادکرد خبر: `خبرگزاری` spelling and `تاریخ انتشار` (vs `تاریخ`) | same | [LOW] |
| یادکرد خبر: `کار` (work) was never seen; use `اثر` or `ناشر` | — | [UNVERIFIED] |

### 3.13 Infoboxes
| Rule | Source | Tag |
|---|---|---|
| Infoboxes are optional and go at the top of the article. No flags, except for ships and sport events. | [راهنما:جعبه اطلاعات](https://fa.wikipedia.org/wiki/راهنما:جعبه_اطلاعات) | [V] |
| New infoboxes derive from {{جعبه اطلاعات}}, not {{Infobox}} | [الگو:جعبه اطلاعات](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات) | [V] |
| No blank line after the infobox's `}}` (the bot removes it) | [FCC L449-455](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L449-L455) | [C] |
| Biographies: take BLP care, and no religion or sect in the infobox | [زندگی‌نامه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/زندگی‌نامه‌ها) | [LOW] |
| The patrol bot flags articles lacking `{{جعبه…` when the enwiki article has an infobox | [zzfawikipatroler_core.py L599-607](https://github.com/PersianWikipedia/fawikibot/blob/master/Need2convert/zzfawikipatroler_core.py#L599-L607) | [C] |
| "Top 10 infoboxes by usage": no transclusion counts were reachable | — | [UNVERIFIED] |
| زندگی‌نامه: `نام`, `تصویر`, `alt`, `توضیح تصویر`, `نام تولد`, `زادروز`, `زادگاه`, `تاریخ درگذشت`, `مکان درگذشت`, `ملیت`, `پیشه`, `شناخته‌شده برای` | [الگو:جعبه اطلاعات زندگی‌نامه](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_زندگی‌نامه) | [V] |
| زندگی‌نامه misc: `آرامگاه`/`مدفن`, `همسر`, `فرزندان`, `والدین`, `تحصیلات`, `سال‌های فعالیت`, `امضا`, `پودمان`. Is {{جعبه زندگینامه}} a redirect? | same | [LOW] |
| منطقه مسکونی: `نام`, `نام رسمی`, `نوع منطقه مسکونی`, `نوع زیربخش`/`نام زیربخش`, `کل جمعیت`, `ارتفاع متر`, `تراکم جمعیت کیلومتر مربع=auto` | [الگو:جعبه اطلاعات منطقه مسکونی](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_منطقه_مسکونی) | [V] |
| منطقه مسکونی subdivision numbering (`…۱`) and postal / area-code parameter names. روستای ایران statistical-code and census-year parameter names (`کد آماری`?). | same; [روستای ایران](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_روستای_ایران) | [UNVERIFIED] |
| Legacy شهر ایران parameters (for reading old articles only): `استان`, `شهرستان`, `بخش`, `جمعیت`, `ارتفاع`, `پیش‌شماره`, `پلاک اتومبیل`, `شهردار` | [الگو:جعبه اطلاعات شهر ایران](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_شهر_ایران) | [V] |
| روستای ایران (wraps منطقه مسکونی): `استان`, `شهرستان`, `بخش`, `دهستان`. The SCI code auto-fills population, falling back to Wikidata P1010. | [الگو:جعبه اطلاعات روستای ایران](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_روستای_ایران) | [V] |
| شرکت: `نام`, `لوگو`, `نوع`, `صنعت`, `بنیان‌گذاری`, `بنیان‌گذار(ان)`, `دفتر مرکزی`, `محصولات`, `درآمد`, `شمار کارکنان`, `مادر`, `نام تجاری`, `وبگاه`. NGOs use {{جعبه اطلاعات سازمان}}. | [الگو:جعبه اطلاعات شرکت](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_شرکت) | [V] |
| فیلم: `عنوان` (not `نام`), `کارگردان`, `تهیه‌کننده`, `نویسنده`, `بازیگران`, `موسیقی`, `فیلم‌بردار`, `تدوین`, `کشور`, `زبان`. Multiple values via {{فهرست ساده}}. | [الگو:جعبه اطلاعات فیلم](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_فیلم) | [V] |
| کتاب: `نام کتاب` (or `نام` / `عنوان`), `نویسنده`, `برگرداننده` (translator), `کشور`, `زبان اصلی`, `سبک`, `موضوع`, `ناشر`, `تاریخ نشر`, `شابک` | [الگو:جعبه اطلاعات کتاب](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_کتاب) | [V] |
| Unconfirmed parameters: فیلم `مدت زمان`, budget, gross; کتاب `تعداد_صفحات`; دانشگاه `وبگاه` vs `وب‌سایت`; کشور Persian parameters (`نام رسمی`, `پایتخت`…; the English {{Infobox country}} block is documented [V]) | [فیلم](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_فیلم); [کتاب](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_کتاب); [کشور](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_کشور) | [LOW] |
| ورزشکار: `قد به سانتی‌متر`, `موقعیت`, `باشگاه`, `تیم` | [الگو:جعبه اطلاعات ورزشکار](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_ورزشکار) | [V] |
| Footballers: {{Infobox football biography}} with English parameters (`clubs1`, `caps1`, `nationalteam1`…). A Persian wrapper is [UNVERIFIED]. | [page](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_مربی_فوتبال) | [LOW] |
| دانشگاه: `نام`, `نام_لاتین`, `شعار`, `نوع` (six listed values), `تأسیس` (Solar Hijri), `بنیانگذاران`, `رئیس`, `دانشجویان`, `شهر`, `کشور` | [الگو:جعبه اطلاعات دانشگاه/توضیحات](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_دانشگاه/توضیحات) | [V] |
| آلبوم: `نام`, `نوع`, `هنرمند`, `جلد`, `پخش`, `ضبط`, `استودیو`, `سبک`, `زمان`, `زبان`, `ناشر` (label), `تهیه‌کننده` | [الگو:جعبه اطلاعات آلبوم](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_آلبوم) | [V] |
| هنرمند موسیقی: `پیش‌زمینه` (`خواننده_تک` / `گروه`), `سبک`, `ساز`, `سال‌های فعالیت`, `ناشر` (no `شرکت ضبط`) | [الگو:جعبه اطلاعات هنرمند موسیقی](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_هنرمند_موسیقی) | [V] |
| بازیگر: `تاریخ تولد`, `محل تولد`, `تاریخ مرگ`, `محل مرگ` (unlike زندگی‌نامه), `زمینه فعالیت`, `جوایز`. Its full form and the هنرپیشه redirect are [LOW]. | [الگو:جعبه اطلاعات بازیگر](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_بازیگر) | [V] |
| سمت رسمی (describes the office): `پیشین`, `جانشین`, `مدت تصدی`, `نخستین متصدی`. {{جعبه اطلاعات سیاست‌مدار}} and {{Infobox officeholder}} are [LOW]. | [الگو:جعبه اطلاعات سمت رسمی](https://fa.wikipedia.org/wiki/الگو:جعبه_اطلاعات_سمت_رسمی) | [V] |

### 3.13a Live check of template and parameter names (2026-10-21)
`bench/live_check.py templates`, run by `.github/workflows/live.yml` on GitHub's runners (wikipedia.org
is reachable there), compared every template and parameter name the skill emits with TemplateData,
the template source (`{{{param|`) and the module each template invokes.

| Result | Tag |
|---|---|
| Infoboxes: 117 of 123 builder parameters confirmed, including زندگی‌نامه misc parameters, منطقه مسکونی numbering (`نوع زیربخش۱`…), کتاب `تعداد_صفحات`, دانشگاه `وبگاه` | [LIVE] |
| Fixed: فیلم runtime is `مدت`; کشور uses `نام عادی`, `تصویر نشان ملی`, `زبان(های) رسمی`; هنرمند موسیقی uses `پس‌زمینه` (not `پیش‌زمینه`) and has no notable-instruments parameter | [LIVE] |
| `{{کنترل مرجعیت}}` and `{{تک}}` do not exist. en Authority control ↔ `{{داده‌های کتابخانه‌ای}}`; Short description ↔ `{{توصیف کوتاه}}`; en `{{References}}` ↔ `{{بدون منبع}}` (interlanguage links) | [LIVE] |
| یادکرد کتاب `نویسنده`, `ترجمه`; یادکرد ژورنال `نویسنده`, `جلد`, `ناشر`: not in TemplateData, source or `citation/CS1/fa/dispatch`, but emitted by citer | [CONFLICT] |

### 3.14 Speedy deletion, timed deletion, AfD, new-page patrol
| Rule | Source | Tag |
|---|---|---|
| Prefixes: ع general, م articles, ت redirects, پ files, ر categories, ک user pages | [معیارهای حذف سریع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع) | [LOW] |
| Templates {{حس-<code>}} (English {{db-…}} aliases work). The generic {{حذف سریع}} or {{حس\|1=…}} adds the page to «رده:مقاله‌های نامزد حذف سریع». | [الگو:الگوهای حذف سریع](https://fa.wikipedia.org/wiki/الگو:الگوهای_حذف_سریع); [الگو:حذف سریع/توضیحات](https://fa.wikipedia.org/wiki/الگو:حذف_سریع/توضیحات) | [V] |
| ع۱ nonsense (excludes poor writing, fiction and hoaxes); ع۲ test pages; ع۳ vandalism and blatant hoaxes | [معیارهای حذف سریع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع) | [V] |
| ع۵ block evasion with no substantial edits by others; ع۷ author request ({{حذف سریع\|درخواست کاربر}}); ع۱۲ copyvio with no clean version (if unsure, use «حق تکثیر مشکوک») | same | [V] |
| ع۴ repost after discussion; ع۶ technical (incl. dabs with 0–1 entries); ع۸ dependent pages; ع۹ WMF; ع۱۰ attack; ع۱۱ advertising (rewrite preferred) | same | [LOW] |
| ع۱۵ «صفحه‌های ایجاد شده با مدل‌های زبانی بزرگ بدون بازبینی انسانی». Signs: chatbot text, cutoff disclaimers, «[تاریخ تولد]» placeholders. One sign alone is not proof. | same | [LOW] |
| ع۱۵ citation signs: links dead on arrival, ISBNs with bad checksums, unresolvable DOIs | same | [V] |
| م۲ foreign-language duplicate of another project (being non-Persian alone is no ground). م۳ no content, but «مقاله‌های بسیار کوتاه که بافت لازم را داشته باشند» can be valid stubs. | same | [V] |
| م۷ no indication of importance. Any credible claim, even unsourced, prevents deletion. «اهمیت، استاندارد بسیار پایین‌تری نسبت به سرشناسی است». | same; [ادعای باورپذیر اهمیت](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ادعای_باورپذیر_اهمیت) | [V] |
| م۱ no context; م۹ music (no importance AND no artist article); م۱۰ duplicate; م۱۱ invented. Also ت۲, ت۳, پ۱, ر۱ (empty 4 days), ک۱, ک۲. | same | [LOW] |
| Not seen: ع۱۳, ع۱۴, م۴–م۶, م۸ | — | [UNVERIFIED] |
| A page qualifies only if every revision does. State the criterion and notify the creator. If in doubt, use AfD. | same; [سیاست حذف](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سیاست_حذف) | [LOW] |
| {{حذف زمان‌دار}}: an admin deletes **10 days** after nomination (changed from 7 by RfC). Anyone but the author may remove the tag, after which only AfD can delete. Articles, dabs and lists only; once per article; never alongside AfD. | [حذف زمان‌دار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:حذف_زمان‌دار) | [V] |
| AfD («نبح», {{نظرخواهی برای حذف}}): ≥7 days (168 h); arguments, not votes; no consensus → keep | [نظرخواهی برای حذف](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی_برای_حذف); [فرایند حذف](https://fa.wikipedia.org/wiki/ویکی‌پدیا:فرایند_حذف) | [LOW] |
| Top newcomer deletion reasons: no notability; copying («…مجاز نیستید متنی را از یک جای دیگر … کپی کنید»); too few sources | [متداول‌ترین دلایل…](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع/متداول‌ترین_دلایل_حذف_مقالات_تازه‌کاران) | [V] |
| Patrol: attacks and copyvio first; give the creator a chance; draftifying is not deletion; don't draftify after 90 days. {{نقض حق تکثیر}} takes the source URL. | [گشت‌زن](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گشت‌زن); [پیش‌نویس‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:پیش‌نویس‌ها) | [LOW] |
| {{فاقد محتوا}}: if the page is still empty 10 days after tagging, a speedy tag may follow | [الگو:فاقد محتوا](https://fa.wikipedia.org/wiki/الگو:فاقد_محتوا) | [V] |

### 3.15 Translation
| Rule | Source | Tag |
|---|---|---|
| License attribution = source language + link to the original **in the edit summary**. The template records only the origin, not the sources. | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) | [V] |
| {{صفحه ترجمه‌شده\|<lang>\|<exact source title>}} goes on the **talk** page. Optional `بخش`, `بخشی`, `بی‌رده`. The newest box goes on top, before the first thread. | [الگو:صفحه ترجمه‌شده](https://fa.wikipedia.org/wiki/الگو:صفحه_ترجمه‌شده) | [V] |
| Revision-ID parameter names (`نسخه`…) are unconfirmed. The talk template and history copy are optional. | same; [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) | [LOW] |
| Check cited sources yourself; otherwise cite the source wiki case by case with {{یادکرد-ویکی}}, not a blanket «(ویکی‌پدیا انگلیسی و…)». Write readable Persian, and prefer official Persian translations of sources. | [خودآموز (ترجمه)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)) | [V] |
| Machine translation is acceptable only as a starting point. Unedited MT left as an article is «بدتر از هیچ چیز». | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) | [V] |
| Content Translation is for extended-confirmed users only (30 days + 500 edits). Publishing unreviewed output can cost the right or lead to a creation block. Output is not final; titles are not translated. | [ابزار ترجمه محتوا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابزار_ترجمه_محتوا); [سطوح دسترسی کاربری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سطوح_دسترسی_کاربری) | [V] |
| Abandoned machine translations usually get {{حذف زمان‌دار}} | [ابزار ترجمه محتوا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابزار_ترجمه_محتوا) | [V] |
| Cleanup templates: {{اصلاح ترجمه}}, {{تمیزکاری ترجمه}}, {{ترجمه تقریبی}} (possible MT) | [صفحه‌های نیازمند ترجمه به فارسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:صفحه‌های_نیازمند_ترجمه_به_فارسی) | [LOW] |
| A dedicated MT policy page or percentage cap was not found | — | [UNVERIFIED] |

### 3.16 AI / LLM policy status
| Rule | Source | Tag |
|---|---|---|
| fa.wiki has no comprehensive AI-use policy. Closest guidance: don't create new articles from scratch with LLMs (mirrors en:WP:NEWLLM; whether a fa page exists is unclear). | [هوش مصنوعی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:هوش_مصنوعی) | [LOW] |
| AI output is not citable. ChatGPT output is treated as public domain. AI-looking unblock requests may be declined. | same | [LOW] |
| All LLM text must be reviewed and confirmed by editors before use. Don't publish content created solely with an LLM. | [مدل‌های زبانی بزرگ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:مدل‌های_زبانی_بزرگ) | [V] |
| Editors who are unaware of the risks, or lack competence for the task, must not use LLMs. The page warns of fabricated content and fake references. | same | [V] |
| **Disclose** any LLM use to generate or modify text **in the edit summary**. Non-transparent use in talk comments or summaries is «به‌شدت ممنوع». | same | [V] |
| Status of that page (policy, guideline or «انشا» essay) | same | [UNVERIFIED] |
| Speedy criterion ع۱۵ covers unreviewed LLM pages (§3.14). The Perseus LLM-translation tool and {{ترجمه با کمک مدل‌های بزرگ زبانی}} are discussion only. | [معیارهای حذف سریع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع); [قهوه‌خانه/اجرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قهوه‌خانه/اجرایی) | [LOW] |
| An AI maintenance template or an adoption RfC was not found | — | [UNVERIFIED] |

### 3.17 fa.wiki tools: what they actually enforce
The gadget was likely seeded by persiantools: AA reproduces PT's functions verbatim [LOW, inferred]. Compare [PT L226-259](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L226-L259) with [AA L1146-1197](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1146-L1197).

| Behaviour | Source | Tag |
|---|---|---|
| Gadget order: normalizeZwnj → quotation → dictation → toStandardPersianCharacters → applyOrthography → complexVerbs → applyZwnj → punctuation → normalizeZwnj. FCC discards whitespace-only edits. | [AA L1346-1356](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1346-L1356); [FCC L820-822](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L820-L822) | [C] |
| Folds ي ى ك and presentation forms → ی ک. FCC protects templates, refs and URLs, but **not** links. | [FCC L129-140](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L129-L140) | [C] |
| PT/AA also fold ہ ە ھ → ه and ۍ ې → ی, and AA maps ە → ه‌ (risky for Kurdish and Urdu). CD strips {{عربی}}…{{پایان عربی}}, {{به عربی}}, {{lang-ar}} and {{اردو}} first. | [PT L130-145](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L130-L145); [AA L1032-1048](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1032-L1048); [CD L353-354](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L353-L354) | [C] |
| PT converts digits to Persian, % → ٪ and . → ٫ with no context guard; AA's `run()` never calls this. FCC never converts digits in prose, but does Persian → Latin in ISBN/ISSN/PMID and English cite templates. | [PT L147-155](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L147-L155); [FCC L58-100](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L58-L100), [L520-541](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L520-L541) | [C] |
| ۀ / هٓ / هء → هٔ and ه‌ئی → ه‌ای. PT/AA also do `ه ی → هٔ`, which is risky: FCC's consonantal-ه list `sametH` is never used. AA adds هٔ to «درباره» and «صفحه ۱۲». | [PT L157-170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170); [FCC L41](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L41), [L136](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L136); [AA L1120-1122](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1120-L1122) | [C] |
| Word lists for hamza (موسسه→مؤسسه, تاثیر→تأثیر; on final hamza: «اجماعی وجود ندارد»), alef (حتا→حتی, ا→آ; FCC's version is disabled as buggy) and tanvin (کاملا→کاملاً; اولا and سوما skipped) | [AA L126-225](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L126-L225), [L966](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L966); [FCC L40](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L40), [L186-192](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L186-L192) | [C] |
| No fa tool removes kashida from prose (CD strips it only before spell-checking) | [CD L364](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L364) | [C] |
| Removes control characters and BOM. Unicode spaces → space. FCC turns bidi marks and RLM into ZWNJ, then cleans up. `&zwnj;` and {{فم}} → ZWNJ. | [AA L1056](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1056); [FCC L287-291](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L287-L291), [L436](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L436) | [C] |
| ZWNJ cleanup: collapse duplicates; remove after non-joiners, next to spaces or punctuation, and at line edges. FCC keeps `[[…]]‌ها` via placeholders; PT/AA wrongly delete it. | [PT L71-79](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L71-L79); [AA L1000-1028](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1000-L1028); [FCC L292-294](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L292-L294), [L816-841](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L816-L841) | [C] |
| (ن)می + whitelisted verb stem + ending → ZWNJ; exceptions میستری، میگوی، میدوی | [PT L195-237](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L195-L237); [AA L1146-1165](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1146-L1165), [L1203-1209](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1203-L1209) | [C] |
| FCC handles only نمی (it dropped «می» for false positives). AA's complex-verb rule has known bugs (در گذشته، بر گردن). | [FCC L37-38](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L37-L38), [L197](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L197); [AA L1126-1143](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1126-L1143) | [C] |
| space + ها/های… → ZWNJ. « ترین» → ZWNJ always; « تر» only after an adjective whitelist (تر also means "wet"). | [PT L241-242](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L241-L242); [AA L1169-1175](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1169-L1175), [L977-989](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L977-L989) | [C] |
| ه + ام/ای/ایم/اید/اند → ZWNJ, with «است» excluded on purpose. FCC applies this only after past-participle stems. | [PT L253-256](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L253-L256); [FCC L200-206](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L200-L206) | [C] |
| Compound dictionaries; personal-name joining (حمید رضا→حمیدرضا, X آباد); Arabic compounds (علی‌رغم); و-compounds (رفت‌وآمد, گفت و گو→گفتگو, جستجو) | [AA L246-537](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L246-L537), [L884-905](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L884-L905); [FCC L145-216](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L145-L216) | [C] |
| ? ; , → ؟ ؛ ، after a Persian letter. Spacing: none before a mark, one after, none inside ( « [, a space before an opening «. `!` is never touched (`<!--`, `!!`). | [AA L1220-1269](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1220-L1269), [L1342](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1342); [PT L264-278](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L264-L278) | [C] |
| Latin quotes → «» per line when Persian is adjacent (never `'`, which is wiki italics). Repeated ؟ is collapsed. | [AA L775-862](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L775-L862), [L1334-1338](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1334-L1338) | [C] |
| Protected zones: comments, headers, pre, source, refs, URLs, tables, links, files, nested templates. `reverting()` restores math, source, score and `<!--ابر-->` blocks. | [FCC L868-997](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L868-L997), [L761-802](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L761-L802) | [C] |
| Headings: پانویس(ها)→پانویس, همچنین ببینید→جستارهای وابسته, منبع/مراجع→منابع, لینک‌های خارجی→پیوند به بیرون, گالری→نگارخانه | [FCC L366-376](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L366-L376) | [C] |
| Namespace aliases (رده:, پرونده:); image options (بندانگشتی, چپ…); {{DEFAULTSORT}}→{{ترتیب‌پیش‌فرض:}}; {{Commons}}→{{ویکی‌انبار}} | [FCC L354-358](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L354-L358), [L424-448](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L424-L448) | [C] |
| Deletes Latin-only categories and an ASCII DEFAULTSORT. Sorts categories. Puts stubs → DEFAULTSORT → categories at the end. | [FCC L440](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L440), [L482](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L482), [L543-660](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L543-L660) | [C] |
| CD reports honorifics, typos, misspellings, bad wikicode, nonstandard characters, colloquialisms, profanity, unbalanced «» and dab links. It matches whole words only, exempts the page title, treats >4 repeats as intentional, and loads lists from ویکی‌پدیا:اشتباه‌یاب/فهرست. | [CD L631-640](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L631-L640), [L388-404](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L388-L404), [L617-618](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L617-L618), [L651-662](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L651-L662) | [C] |
| Forbidden honorifics ((ع)، (ره)، حضرت، امام، آیت‌الله، مرحوم، زنده‌یاد، دکتر، پروفسور…) and colloquial forms (میخونه، خونه، دیگه) | [WWD L769](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L769); [slang L1-16](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_slang_word_dict.txt#L1-L16) | [C] |
| Misspelling sample: برگذار→برگزار, خبرگذاری→خبرگزاری, تلوزیون→تلویزیون, بعنوان→به‌عنوان, آنرا→آن را, گزارشات→گزارش‌ها, هیات→هیئت, سوال→سؤال, فن‌آوری→فناوری | WWD [L100](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L100), [L265](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L265), [L187](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L187), [L116](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L116), [L9](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L9), [L700](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L700), [L618](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L618), [L339](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L339), [L417](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L417) | [C] |
| ISBN magic links → {{شابک}}, or {{ISBN\|…\|en}} in a Latin context | [isbn_fix.py L113-148](https://github.com/PersianWikipedia/fawikibot/blob/master/isbn_fix.py#L113-L148) | [C] |

## 4. Consolidated [UNVERIFIED] / [LOW] list (needs live verification)

**[UNVERIFIED]: no source found**
- [ ] **Orthography and punctuation:** copula ZWNJ rules ([نیم‌فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) § صورت‌های متصل فعل بودن); an explicit rule to use ، ؛ ؟ instead of , ; ?
- [ ] **Dates and numbers:** the full Gregorian month list; number–unit spacing, percent and currency rules
- [ ] **Transliteration, lead and words to watch:** an English → Persian letter table; the birth/death parenthesis format; a fuller peacock-word list
- [ ] **Templates:** whether {{منبع}} is a separate template; {{بدون منبع}} parameters; `مترجم`, `صفحه‌ها`, یادکرد خبر `کار`; whether date validators accept Persian-digit or Solar dates (`۱۵ فروردین ۱۴۰۲`)
- [ ] **Infoboxes:** usage ranking (`Special:MostTranscludedPages`); ~~منطقه مسکونی subdivision numbering~~ (confirmed live, §3.13a) and postal codes; روستای ایران statistical-code and census-year parameters; whether «جعبه اطلاعات شخص» is a redirect; a Persian football wrapper
- [ ] **Deletion:** ع۱۳, ع۱۴, م۴–م۶, م۸; content of the Iran/Afghanistan biographies RfC
- [ ] **Translation and AI:** whether ویکی‌پدیا:ترجمه exists; any MT policy or cap; status banner of [مدل‌های زبانی بزرگ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:مدل‌های_زبانی_بزرگ) (policy / guideline / «انشا»); an AI maintenance template and an adoption RfC

**[LOW]: summary only, quote needed**
- [ ] **شیوه‌نامه:** formal register; Arabic-text templates; hamza seat rule; punctuation spacing; § پیوند (most specific; external links); banned title characters; image placement
- [ ] **دستور خط and نیم‌فاصله:** مسئله / مسئول; inference for نمی‌; بهنام / بهروز; read نیم‌فاصله § ها in full (joined vs ZWNJ)
- [ ] **Other style pages:** نشانه‌های نگارشی (nested parentheses); املای برخی واژه‌ها (sources); شیوه عبارات عربی (اتاق table); solar month forms; کوته‌نوشت (ه‍.ق / ه‍.ش, «م», «ق.م»)
- [ ] **Titles:** outcomes of the هٔ RfCs (2014 and title-clause) and the اعراب RfC
- [ ] **Naming and transliteration:** قواعد نام‌گذاری subpages (فیلم‌ها, اسامی جغرافیایی, اشخاص); فارسی‌سازی, نویسه‌گردانی, نگارش نام‌های خارجی and per-language pages
- [ ] **Links and lead:** پیونددهی (link once, overlinking, dates); don't link the bolded title; بخش آغازین (bold, definition, summary, length table); زندگی‌نامه‌ها (lead; religion in infobox)
- [ ] **Layout:** صفحه‌آرایی (post-navbox order; منابع / مطالعهٔ بیشتر / پیوند به بیرون; heading levels); رده‌بندی (category vs stub order)
- [ ] **Notability:** سرشناسی (GNG, secondary sources); subject pages افراد, سازمان‌ها, کتاب‌ها, فیلم‌ها, موسیقی, ورزش‌ها, دانشگاهیان, جغرافیا, رویدادها
- [ ] **Sourcing and words to watch:** تأییدپذیری (self-published sources); منابع معتبر (expert exception; Wikipedia not a source); تحقیق دست‌اول ممنوع (whole page); words-to-watch page (whole page)
- [ ] **Maintenance templates:** {{مدرک}} `تاریخ` format; {{یک منبع}}; {{ابهام‌زدایی}} placement
- [ ] **Citations** ([پودمان:Citation/CS1/fa/Configuration](https://fa.wikipedia.org/wiki/پودمان:Citation/CS1/fa/Configuration)): English aliases inside یادکرد; `تاریخ بازدید`, `نقل قول`, `قالب`, `ترجمه عنوان`, `شهر`, `دوره`, `خبرگزاری`, `تاریخ انتشار`; {{پانویس\|گروه=}}
- [x] **Infoboxes, builder parameters:** زندگی‌نامه misc, فیلم runtime, کتاب page count, دانشگاه website, کشور Persian parameters: checked live 2026-10-21 (§3.13a)
- [ ] **Infoboxes, other:** {{جعبه زندگینامه}} redirect; football biography; سیاست‌مدار; officeholder; هنرپیشه
- [ ] **Deletion:** prefix list; ع۴, ع۶, ع۸–ع۱۱; م۱, م۹–م۱۱; ت / پ / ر / ک; all-criteria rules; ع۱۵ title, signs, adoption RfC (is «یادکرد ساختگی» part of it?); AfD 7-day minimum; patrol / draftify rules; {{نقض حق تکثیر}}
- [ ] **Translation and AI:** {{صفحه ترجمه‌شده}} revision parameters; optional talk template; cleanup templates; claims on [هوش مصنوعی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:هوش_مصنوعی); whether «ساخت مقاله با مدل‌های زبانی بزرگ» exists on fa; the Perseus discussion
- [ ] **Tools:** does the live gadget (`MediaWiki:Gadget-Extra-Editbuttons-persianwikitools.js`, `-persiantools.js`, `-dictionary.js`) still match the AA port? Are FCC's template aliases still current redirects?

## 5. Conflicts between sources

| Topic | Says one thing | Says another | Working resolution |
|---|---|---|---|
| ها: joined vs ZWNJ | [دستور خط § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط): both correct; ZWNJ mandatory in 6 cases [V] | [نیم‌فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله): «همیشه باید پیوسته نوشت» [V] (probably "never a full space"); PT/AA insert ZWNJ [C] | A full space is always an error. Accept joined or ZWNJ; require ZWNJ in the 6 cases. |
| Stub vs category order | [صفحه‌آرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی) [LOW], [الگو:خرد](https://fa.wikipedia.org/wiki/الگو:خرد) [V], FCC [C]: stubs **above** categories | [رده‌بندی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:رده‌بندی): categories «پیش از الگوهای خرد» [LOW] | Follow the majority (stub → DEFAULTSORT → categories); re-check. |
| بنیانگذار vs بنیان‌گذار | [WWD L130](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L130) → بنیان‌گذار; {{جعبه اطلاعات شرکت}} uses `بنیان‌گذار` [V] | AA L646 prefers بنیانگذار [C]; {{جعبه اطلاعات دانشگاه}} uses `بنیانگذاران` [V] | Warn only in prose. Infobox parameter names must match each template exactly. |
| هٔ in titles | شیوه‌نامه § عنوان bans it [V]; the 2014 RfC found no consensus to allow it [LOW] | The later «تغییر بند سیاست عنوان صفحه‌ها» RfC has an unknown outcome [LOW] | Keep the ban; re-check before hard-coding. |
| حذف زمان‌دار period | [حذف زمان‌دار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:حذف_زمان‌دار): **10 days**, changed from 7 by RfC [V] | [فرایند حذف](https://fa.wikipedia.org/wiki/ویکی‌پدیا:فرایند_حذف) still says 7 | Use 10. |
| Hamza in مسئله | The vowel rule (fatha → أ) implies مسأله [LOW] | دستور خط lists مسئله / مسئول under ئ [LOW]; AA rewrites مساله / مسأله → مسئله [C] | Use a whitelist, not the rule. |
| Centuries | Spell out (سدهٔ هفتم) [V] | The same page gives «سدهٔ ۱۹ میلادی» [V] | Treat digit centuries as a warning only. |
| BC / solar abbreviations | کوته‌نوشت: «ق.م» (not «ق.م.»); prefers ه‍.ش / ه‍.خ [LOW] | Article پیش از میلاد uses «پ.م.» / «ق.م.»; the solar-abbreviation RfC found no consensus [V] | Don't auto-fix between forms. |
| {{پانویس\|اندازه=}} | FCC still emits `اندازه=کوچک` [C] | The doc says it has no effect [V] | Don't emit it. |
| Access-date parameter | citer: `تاریخ بازبینی` [C] | The doc also shows `تاریخ بازدید` [LOW] | Emit `تاریخ بازبینی`. |
| Birth parameters | زندگی‌نامه: `زادروز` / `زادگاه` [V] | بازیگر: `تاریخ تولد` / `محل تولد` [V] | Keep one parameter map per template. |
| Digits in prose | PT converts unconditionally [C] | FCC never converts in prose [C]; the MOS requires Persian digits [V] | Convert only prose tokens with no Latin letters, outside protected zones. |
| ZWNJ after `]]` | FCC keeps `]]‌ها` [C] | PT/AA delete it [C] | Keep it (follow FCC). |
| Dictionary vs epithets | FCC fixes پرفسور→پروفسور and آیت الله→آیت‌الله, and keeps فوق‌الذکر [C] | WWD lists پروفسور and آیت‌الله as forbidden epithets, and says فوق‌الذکر → یادشده [C] | Warn only. |
| End-section order | پانویس / منابع may be one section [V] | An alternate revision puts پانویس before منابع [V] | Either form is fine; don't reorder. |

## 6. How to re-verify when wikipedia.org is reachable

Steps 3 to 5 are automated: `bench/live_check.py templates` (monthly in `.github/workflows/live.yml`).

Record each page's `revid` so that rows can cite pinned revisions. Then replace every [LOW] / [UNVERIFIED] tag and re-check every [V] quote against the live wikitext.

```bash
API=https://fa.wikipedia.org/w/api.php
q(){ curl -sG "$API" --data-urlencode format=json --data-urlencode formatversion=2 "$@"; }
# 1) Section index + revid, then one section's wikitext
q --data-urlencode action=parse --data-urlencode page='ویکی‌پدیا:شیوه‌نامه' --data-urlencode prop='sections|revid'
q --data-urlencode action=parse --data-urlencode page='ویکی‌پدیا:شیوه‌نامه' --data-urlencode section=N --data-urlencode prop='wikitext|revid'
# 2) Status banner: which templates the page transcludes (policy / guideline / essay)
q --data-urlencode action=parse --data-urlencode page='ویکی‌پدیا:مدل‌های_زبانی_بزرگ' --data-urlencode prop=templates
# 3) TemplateData: parameter names, aliases, required flags
q --data-urlencode action=templatedata --data-urlencode lang=fa --data-urlencode titles='الگو:یادکرد وب|الگو:یادکرد کتاب|الگو:یادکرد ژورنال|الگو:یادکرد خبر|الگو:پانویس|الگو:پک|الگو:مدرک|الگو:صفحه ترجمه‌شده'
q --data-urlencode action=templatedata --data-urlencode lang=fa --data-urlencode titles='الگو:جعبه اطلاعات زندگی‌نامه|الگو:جعبه اطلاعات منطقه مسکونی|الگو:جعبه اطلاعات روستای ایران|الگو:جعبه اطلاعات شرکت|الگو:جعبه اطلاعات فیلم|الگو:جعبه اطلاعات کتاب|الگو:جعبه اطلاعات دانشگاه|الگو:جعبه اطلاعات کشور'
# 4) CS1 alias table (authoritative for Persian/English parameter names)
q --data-urlencode action=query --data-urlencode prop=revisions --data-urlencode rvprop='content|ids' --data-urlencode rvslots=main --data-urlencode titles='پودمان:Citation/CS1/fa/Configuration'
# 5) Existence and redirects
q --data-urlencode action=query --data-urlencode redirects=1 --data-urlencode titles='الگو:جعبه اطلاعات شخص|ویکی‌پدیا:ترجمه|الگو:جعبه زندگینامه|الگو:جعبه اطلاعات هنرپیشه|الگو:منبع'
# 6) Most-transcluded templates (infobox ranking)
q --data-urlencode action=query --data-urlencode list=querypage --data-urlencode qppage=Mostlinkedtemplates --data-urlencode qplimit=500
# 7) History, to date ع۱۵ (repeat for ویکی‌پدیا:حذف_زمان‌دار to date the 7→10 change)
q --data-urlencode action=query --data-urlencode prop=revisions --data-urlencode rvlimit=50 --data-urlencode rvprop='ids|timestamp|comment' --data-urlencode titles='ویکی‌پدیا:معیارهای_حذف_سریع'
# 8) Raw pages: linter word list, and the live gadget to compare with the AA port
curl -s 'https://fa.wikipedia.org/w/index.php?title=ویکی‌پدیا:اشتباه‌یاب/فهرست&action=raw'
curl -s 'https://fa.wikipedia.org/w/index.php?title=MediaWiki:Gadget-Extra-Editbuttons-persianwikitools.js&action=raw'
```

**Priority pages for step 1:** شیوه‌نامه (§ عنوان, اعداد, نشانه‌گذاری, همزه); دستور خط; نیم‌فاصله; تاریخ‌ها و اعداد; کوته‌نوشت; صفحه‌آرایی; بخش آغازین; قواعد نام‌گذاری; سرشناسی (+ subpages); تأییدپذیری; زندگی‌نامه زندگان; دیدگاه بی‌طرف; معیارهای حذف سریع; حذف زمان‌دار; راهنما:ترجمه; الگو:صفحه ترجمه‌شده; مدل‌های زبانی بزرگ; هوش مصنوعی; شیوه ارجاع به منابع; راهنما:جعبه اطلاعات.
