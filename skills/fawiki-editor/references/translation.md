# Translating an article into fa.wiki (usually from en.wiki), and AI use

Load this file whenever the user wants to **translate**, **adapt**, or **port** an article from another Wikipedia, or asks whether they may use AI/LLM help.

**Tags:** `[V]` means a Persian excerpt tied to the URL was seen. `[LOW]` means only a summary or paraphrase was seen. `[UNVERIFIED]` means the point is inferred or no source was found.
**Sources:** web-search excerpts from 2026-10-21. No page was read live. All page URLs have the form `https://fa.wikipedia.org/wiki/<title>`.
**Main help pages:** [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) and [ویکی‌پدیا:خودآموز (ترجمه)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)).

## Contents
1. [Hard rules (summary)](#1-hard-rules-summary)
2. [Attribution: edit summary and talk-page template](#2-attribution-edit-summary-and-talk-page-template)
3. [Machine translation and the Content Translation tool](#3-machine-translation-and-the-content-translation-tool)
4. [What transfers and what doesn't](#4-what-transfers-and-what-doesnt)
5. [AI / LLM use on fa.wiki](#5-ai--llm-use-on-fawiki)
6. [Ready-to-use Persian text](#6-ready-to-use-persian-text)

---

## 1. Hard rules (summary)

1. **Attribute in the edit summary.** Name the source wiki and link the source article. This is how the licence is honoured. See §2 [V].
2. **Never publish raw machine or LLM output.** fa.wiki consensus: unedited machine translation is «بدتر از هیچ چیز» (worse than nothing) [V]. Abandoned machine translations usually get **حذف زمان‌دار**, which means deletion after 10 days [V]. Unreviewed LLM pages can be speedily deleted under **ع۱۵** (see references/notability-deletion.md §5).
3. **Translate everything.** Leaving foreign-language text that copies another Wikimedia project risks speedy deletion under **م۲** [V].
4. **Check notability on fa.wiki terms** (references/notability-deletion.md §1). An en.wiki article existing does not prove the topic is notable, and other-language Wikipedias are not reliable sources ([ویکی‌پدیا:منابع معتبر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_معتبر) [LOW]).
5. **Verify the sources yourself.** The translator, not en.wiki, carries the burden of proof for every claim they add ([ویکی‌پدیا:تأییدپذیری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری) [V]).
6. **Disclose AI help** in the edit summary. See §5 [V].

## 2. Attribution: edit summary and talk-page template

| Item | Rule | Source |
|---|---|---|
| Edit summary (required) | «رعایت مجوز با ذکر مبدأ ترجمه و پیوند به مقالهٔ اصلی در خلاصهٔ ویرایش انجام می‌شود» (following en:Wikipedia:Translation). | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) [V] |
| Exact wording / format | **No mandated format was found.** The examples in §6 are a recommendation. | [UNVERIFIED] |
| Revision ID / permanent link in the summary | Not in the notes as a requirement. It is still good practice because it pins down exactly which text was translated. Use `[[:en:Special:PermanentLink/<revid>]]` or write «نسخهٔ <revid>». | [UNVERIFIED] |
| Interlanguage link syntax in summaries and text | `[[:en:Title]]` (leading colon) creates an inline link to the other wiki and is not altered by Wikidata. | [راهنما:پیوند میان‌ویکی](https://fa.wikipedia.org/wiki/راهنما:پیوند_میان‌ویکی) [LOW] |
| `{{صفحه ترجمه‌شده}}` | Goes on the **TALK page** (بحث:…), **never in the article** (it is self-referential). | [الگو:صفحه ترجمه‌شده](https://fa.wikipedia.org/wiki/الگو:صفحه_ترجمه‌شده) [V] |
| Param 1 | Source language code (`en`, `fr`, …). | same [V] |
| Param 2 | The **exact** source title. Do not transliterate it or change any character. | same [V] |
| `بخش` | Source section (when translating one section). | same [V, name] |
| `بخشی` | Any non-empty value marks a **partial** translation. | same [V, name] |
| `بی‌رده` | Suppresses the category. | same [V, name] |
| Source / target revision IDs | Optional params exist, but their **names were not captured verbatim** («نسخه» is a guess). Don't emit them unless you have checked the template page. | [UNVERIFIED] |
| Placement | With several boxes: order by date, newest on top, just before the first talk thread. Don't place one inside an archivable thread. | same [V] |
| What it claims | «فقط مبدأ متن را ثبت می‌کند و ادعایی دربارهٔ همهٔ منابع مقاله ندارد». | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) [V] |
| Optional? | The talk template (and copying page history) are described as optional. The edit summary is the attribution mechanism. Claude should still offer the template. | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) [LOW] |

Talk-page examples (positional params are the verified form):
```
{{صفحه ترجمه‌شده|en|Lake Urmia}}
{{صفحه ترجمه‌شده|en|Lake Urmia|بخش=History|بخشی=بله}}
```
The second line's `بخش`/`بخشی` usage follows the param descriptions. The value «بله» is arbitrary, since any non-empty value works.

## 3. Machine translation and the Content Translation tool

| Point | Detail | Source |
|---|---|---|
| MT as a starting point | Allowed (DeepL, Google, …), but the translator must correct errors and check accuracy. | [راهنما:ترجمه](https://fa.wikipedia.org/wiki/راهنما:ترجمه) [V] |
| Unedited MT | «اجماع کاربران ویکی‌پدیا بر این است که یک ترجمهٔ ماشینی ویرایش‌نشده که در قالب یک مقالهٔ ویکی‌پدیایی رها شده است، بدتر از هیچ چیز است.» | same [V] |
| Abandoned MT → timed deletion | «مقالاتی که به صورت ترجمه ماشینی رها شده‌باشند، معمولاً برچسب حذف زمان‌دار می‌خورند.» (deleted after 10 days unless someone objects) | [ویکی‌پدیا:ابزار ترجمه محتوا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابزار_ترجمه_محتوا) [V]; [ویکی‌پدیا:حذف زمان‌دار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:حذف_زمان‌دار) [V] |
| Content Translation (ابزار ترجمه محتوا) access | Only «کاربران تأییدشدهٔ پایدار (… ۳۰ روز از زمان ایجاد حسابشان گذشته باشد و دست کم ۵۰۰ ویرایش انجام داده باشند)». Others draft in their **user space** and ask experienced editors to review. | [ویکی‌پدیا:ابزار ترجمه محتوا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابزار_ترجمه_محتوا) [V] |
| Sanctions | Publishing unreviewed MT with the tool can cost the user access to it, or lead to a block from creating articles. | same; [ویکی‌پدیا:سطوح دسترسی کاربری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سطوح_دسترسی_کاربری) [V] |
| Tool output | Usually not final. The **title is not translated**. | [ویکی‌پدیا:ابزار ترجمه محتوا](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابزار_ترجمه_محتوا) [V] |
| Readability | The text must be understandable to most fa readers. Prefer an existing Persian equivalent of a foreign source, such as an official Persian translation. | [ویکی‌پدیا:خودآموز (ترجمه)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)) [V] |
| Cleanup tags | {{اصلاح ترجمه}}, {{تمیزکاری ترجمه}}, {{ترجمه تقریبی}} (the last is for text that «ممکن است توسط مترجم‌های ماشینی تولید شده باشد»). | [ویکی‌پدیا:صفحه‌های نیازمند ترجمه به فارسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:صفحه‌های_نیازمند_ترجمه_به_فارسی) [LOW] |
| Untranslated foreign text | **م۲**: a foreign-language article that duplicates another Wikimedia project. Being non-Persian is not, on its own, grounds for deletion. | [ویکی‌پدیا:معیارهای حذف سریع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع) [V tag / LOW text] |
| Dedicated MT policy / % cap | None found. | [UNVERIFIED] |

## 4. What transfers and what doesn't

Script checks: `scripts/wikitext_check.py` flags **WC05** (no `[[رده:…]]`), **WC07** (template unknown to the skill), **WC08** (English template name), **WC09** (English section heading) and **WC10** (English namespace such as `Category:` or `File:`). Fix every WC07 and WC08 hit before handing the text over.

| Element | What to do | Source / tag |
|---|---|---|
| **Prose** | **Rewrite in natural, formal Persian. Do not calque English syntax.** Restructure sentences and use Persian idiom, fa MOS orthography and Persian punctuation (see the skill's style reference). No word-for-word or MT-shaped text. | readability: [خودآموز (ترجمه)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)) [V]; MT rule §3 [V] |
| **References** | **Keep** them, but someone must **check that each source exists and supports the claim**: «بهتر است برای منبع‌دهی، حتماً منابع ذکر شده در آن ویکی‌ها را خودتان بازبینی کنید». A blanket «(ویکی‌پدیا انگلیسی و…)» citation is wrong. The tutorial allows case-by-case {{یادکرد-ویکی}} for unchecked items, but Wikipedia is not a reliable source, so treat that as a stopgap. | [خودآموز (ترجمه)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:خودآموز_(ترجمه)) [V]; [منابع معتبر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:منابع_معتبر) [LOW] |
| ↳ citation templates | Convert to the Persian forms using the mapping in **references/citations.md §10**: `cite web` → `{{یادکرد وب}}`, `cite book` → `{{یادکرد کتاب}}`, `cite journal` → `{{یادکرد ژورنال}}`. For news, citer emits `{{یادکرد وب}}`; the `{{یادکرد خبر}}` params are weakly sourced. Persian names for core fields (`عنوان`, `نشانی`/`پیوند`, `تاریخ`, `تاریخ بازبینی`). Identifiers keep their English names (`doi`, `pmid`, `issn`, `jstor`, `oclc`). | C-templates notes: citer `generator_fa.py` [VERIFIED-CODE] |
| ↳ title & language | **Keep the original English title** (do not translate it). For `یادکرد وب`, set `کد زبان=en`, which switches to Latin punctuation and digits. citer emits `زبان=en` in `یادکرد کتاب`/`ژورنال`. | [الگو:یادکرد وب](https://fa.wikipedia.org/wiki/الگو:یادکرد_وب) [V]; citer [VERIFIED-CODE] |
| ↳ citation dates | Use the calendar printed in the source. citer writes ISO `YYYY-MM-DD`. | [راهنما:ارجاع](https://fa.wikipedia.org/wiki/راهنما:ارجاع) [V] |
| ↳ reflist | `{{Reflist}}` / `<references/>` → `{{پانویس}}` under `== منابع ==` (`{{پانویس\|۲}}` for long lists, `چپ‌چین=بله` for LTR refs). | fawikibot code [VERIFIED-CODE]; [الگو:پانویس](https://fa.wikipedia.org/wiki/الگو:پانویس) [V] |
| **Section headings** | References → منابع · Notes → یادداشت‌ها / پانویس · See also → جستارهای وابسته (no red links) · Further reading → برای مطالعهٔ بیشتر · External links → پیوند به بیرون (singular). | fawikibot [VERIFIED-CODE]; [شیوه‌نامه/صفحه‌آرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی) [V/LOW] |
| **Infobox** | Switch to the **fa template**. The params differ, so map them one by one. Examples: `{{جعبه اطلاعات زندگی‌نامه}}` (`زادروز`, `زادگاه`) vs `{{جعبه اطلاعات بازیگر}}` (`تاریخ تولد`, `محل تولد`); `{{جعبه اطلاعات منطقه مسکونی}}` (`{{جعبه اطلاعات شهر ایران}}` is deprecated); `{{جعبه اطلاعات شرکت}}` (`شمار کارکنان`). Some boxes use English params, e.g. `{{Infobox football biography}}` [LOW]. Infoboxes are optional and sit at the top. Don't copy flags into them. | [راهنما:جعبه اطلاعات](https://fa.wikipedia.org/wiki/راهنما:جعبه_اطلاعات) [V]; per-template pages in C-templates notes [V/LOW] |
| **Templates / navboxes** | Carry a template over **only if a fa equivalent exists**. Otherwise drop it, and don't create English template calls (WC07/WC08). Hatnotes and maintenance tags from en don't transfer automatically; re-evaluate them for the fa article. | WC07/WC08 in `scripts/wikitext_check.py`; dropping rule [UNVERIFIED: skill practice] |
| **Categories** | Map to **existing** fa categories with `[[رده:…]]`, never `Category:` (WC10). **Never invent a category.** Red categories should not be added to articles. At least one category is required (WC05). If unsure that a category exists, list candidates and **ask the user to verify**. | [ویکی‌پدیا:پیوند قرمز](https://fa.wikipedia.org/wiki/ویکی‌پدیا:پیوند_قرمز) [LOW]; WC05/WC10 |
| **Interlanguage links** | **Add none to the wikitext.** They have lived on **Wikidata** since 2013, and bots remove old local links. After publishing, connect the page through the sidebar «افزودن پیوند» / Wikidata. | [راهنما:پیوند میان‌ویکی](https://fa.wikipedia.org/wiki/راهنما:پیوند_میان‌ویکی); [ویکی‌پدیا:ویکی‌داده](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ویکی‌داده) [LOW] |
| **Images** | Files on **Wikimedia Commons** display as-is. **Local en.wiki-only files** (often non-free) will not exist on fa. Write `[[پرونده:…]]` instead of `File:`/`Image:`, and translate captions and alt text. | namespace: fawikibot [VERIFIED-CODE], WC10; Commons vs local [UNVERIFIED: MediaWiki behaviour, not a fa page] |
| **Wikilinks** | Link the **existing fa article title**, which is usually not a literal translation of the en title. **If you are not sure the fa article exists or what it is called, flag it for the user rather than guess.** Red links are acceptable **sparingly**, for topics that could plausibly get an article; avoid red links to topics that never will. No red links in جستارهای وابسته. A template `{{پیوند با میان‌ویکی}}` exists (usage not researched). | [ویکی‌پدیا:پیوند قرمز](https://fa.wikipedia.org/wiki/ویکی‌پدیا:پیوند_قرمز) [LOW]; جستارهای وابسته [V]; template name only [UNVERIFIED usage] |
| **Dates** | Gregorian month names in Iranian usage (French-derived): ژانویه، فوریه، مارس، آوریل، مه، ژوئن، ژوئیه، اوت، سپتامبر، اکتبر، نوامبر، دسامبر. Order is day–month–year, Persian digits, no leading zero, no slashes: «۷ آوریل ۲۰۱۱». Decades: «دههٔ ۱۹۸۰». | [شیوه‌نامه/تاریخ‌ها و اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) [V; 6 of the 12 month names quoted, rest LOW] |
| ↳ calendar choice | **Keep Gregorian for non-Iranian topics.** Don't convert to Solar Hijri. Contemporary articles that use Solar Hijri don't need a Gregorian equivalent. | first half [UNVERIFIED: no explicit rule found]; second half [ویکی‌پدیا:گاهشماری هجری خورشیدی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:گاهشماری_هجری_خورشیدی) [V] |
| **Names / titles** | Use the established Persian form found in Persian reference sources. Otherwise use the form closest to the native pronunciation (via IPA). **See references/titles.md.** The Content Translation tool does not translate titles. | [قواعد نام‌گذاری (فارسی‌سازی نام‌های خارجی)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_(فارسی‌سازی_نام‌های_خارجی)) [LOW] |
| **English-specific sections** ("In popular culture", trivia, US-centric detail) | Translate only what is **sourced** and relevant to a Persian reader. Unsourced trivia can be challenged and removed, so leave it out rather than import it. | [ویکی‌پدیا:تأییدپذیری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تأییدپذیری) [V]; trivia caution [UNVERIFIED: no fa page on trivia sections found] |
| **Units** | Keep the source's figures. Converting units is allowed, because it counts as a simple calculation and not original research. Persian digits, separators `٬` (thousands) and `٫` (decimal). Spacing and ordering of number and unit: no fa rule found. | [تحقیق دست‌اول ممنوع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:تحقیق_دست‌اول_ممنوع) [LOW]; separators [ویکی‌پدیا:شیوه‌نامه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) [V]; unit format [UNVERIFIED] |
| **BLP content** | Contentious material about living people that is unsourced or poorly sourced must not be carried over, even if en.wiki has it. | [ویکی‌پدیا:زندگی‌نامه زندگان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:زندگی‌نامه_زندگان) [V] |

## 5. AI / LLM use on fa.wiki

**Status:** fa.wiki has **no comprehensive AI policy**. What exists is an information page, an LLM page of **unconfirmed status** (one summary called it an essay, «انشا»), and the speedy criterion ع۱۵. No formal RfC adopting the LLM page was found.

| Page / item | What it says | Source |
|---|---|---|
| [ویکی‌پدیا:هوش مصنوعی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:هوش_مصنوعی) (information page) | Wikipedia has no comprehensive «سیاست استفاده از هوش مصنوعی». The closest guidance, «ساخت مقاله با مدل‌های زبانی بزرگ», has one principle: **LLMs must not be used to create new articles from scratch** (it mirrors en:WP:NEWLLM; whether a fa page by that name exists is unclear). AI output must not be cited as a source. | [LOW] |
| [ویکی‌پدیا:مدل‌های زبانی بزرگ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:مدل‌های_زبانی_بزرگ) (**status unconfirmed, possibly an essay**) | «تمامی متون تولیدشده توسط مدل‌های زبانی بزرگ باید پیش از استفاده در مقالات، توسط ویراستاران بررسی و تأیید شوند.» | [V] |
| | **Disclosure:** «هرگونه استفاده از این ابزارها برای تولید یا اصلاح متن باید به‌صراحت در خلاصه ویرایش ذکر شود، حتی اگر شرایط استفاده از این ابزارها چنین الزامی را نداشته باشد.» | [V] |
| | «در هر صورت، ویراستاران باید از انتشار محتوایی که صرفاً با استفاده از مدل‌های زبانی بزرگ ایجاد شده است، خودداری کنند.» | [V] |
| | «مدل‌های زبانی بزرگ نباید برای وظایفی به کار گرفته شوند که ویراستار تسلط کافی به آن‌ها ندارد.» Editors who don't understand the risks should not use these tools. | [V] |
| | Non-transparent LLM use in talk-page comments or edit summaries is «به‌شدت ممنوع». The page also warns about fabricated content and fake references. | [V] |
| **ع۱۵** | Speedy deletion: «صفحه‌های ایجاد شده با مدل‌های زبانی بزرگ بدون بازبینی انسانی». Signs include chatbot phrasing, cutoff disclaimers, placeholders, and dead links, invalid ISBNs or unresolvable DOIs (full list in references/notability-deletion.md §5). | [ویکی‌پدیا:معیارهای حذف سریع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:معیارهای_حذف_سریع) [V/LOW] |
| `{{ترجمه با کمک مدل‌های بزرگ زبانی}}` | **A proposal only.** It was suggested at the village pump (alongside the Perseus/«پرسیوس» LLM translation tool) as a header marking generated articles as needing human editing. **It is not adopted.** Do not add it to articles. The page «ویکی‌پدیا:ترجمه با کمک مدل‌های زبانی بزرگ» is unconfirmed. | [ویکی‌پدیا:قهوه‌خانه/اجرایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قهوه‌خانه/اجرایی) [LOW] |
| AI maintenance template | None found. `{{هوش مصنوعی}}` is only a navbox. | [UNVERIFIED] |

**What this means for Claude (operational):**
- Claude is an LLM. A draft or translation from Claude is LLM output, so the **user** must review it, verify it, and take responsibility before publishing.
- **Translating** an existing article with human review is different from **creating a new article from scratch**. The info page discourages the latter. For a new topic, have the user supply the sources, and build the text only from those sources.
- Always show the **یادآوری** notice (§6) when handing over article text.
- Always propose an edit summary that **discloses AI help** (§6).
- Never invent citations. Mark unverifiable claims `{{مدرک}}` or drop them.

## 6. Ready-to-use Persian text

**یادآوری to show the user** with every draft or translation. This is Claude's own wording, not policy text; the requirements behind it are cited in §5.
> **یادآوری:** این متن با کمک هوش مصنوعی تهیه شده است. پیش از انتشار، تک‌تک ادعاها و منابع را خودتان بررسی کنید و از وجود و درستی هر منبع مطمئن شوید؛ متن را به زبان و سبک خودتان بازنویسی کنید؛ و در خلاصهٔ ویرایش صراحتاً ذکر کنید که از هوش مصنوعی کمک گرفته‌اید. انتشار متنی که صرفاً با مدل زبانی تولید شده و بازبینی نشده، ممکن است به حذف سریع مقاله (معیار ع۱۵) بینجامد.

**Edit-summary templates.** fa.wiki mandates no exact format, so this wording is [UNVERIFIED]. What is required: name the source and link it [V], and disclose AI use [V].
```
ترجمه از [[:en:Lake Urmia]] (نسخهٔ <revid>)؛ با کمک ابزار هوش مصنوعی و بازبینی کامل انسانی
ترجمهٔ بخش «History» از [[:en:Lake Urmia]] (نسخهٔ <revid>)؛ با کمک هوش مصنوعی، بازبینی‌شده
ویرایش متن با کمک ابزار هوش مصنوعی (Claude) و بازبینی انسانی
```
- Replace `<revid>` with the source revision ID from the en.wiki history, or use `[[:en:Special:PermanentLink/<revid>]]`. Pinning the revision is good practice, not a sourced requirement [UNVERIFIED].
- Naming the specific tool (Claude) is optional. The source requires only that AI use be stated explicitly («به‌صراحت») [V].

**Talk-page box** (on بحث:<عنوان فارسی>):
```
{{صفحه ترجمه‌شده|en|Lake Urmia}}
```

**Translation workflow for Claude:**
1. Run the notability checklist (references/notability-deletion.md §1) on fa terms.
2. Get the en.wiki revision ID from the user, or ask them to note it.
3. Translate the prose idiomatically (§4). Convert citations via references/citations.md.
4. Map the infobox, categories and wikilinks. Ask the user to confirm any fa title or category you are unsure of.
5. Run `scripts/fa_lint.py` and `scripts/wikitext_check.py`. Fix the issues they report, especially WC05/WC07/WC08/WC09/WC10.
6. Hand over the wikitext + the یادآوری + the edit summary + the talk-page box.
