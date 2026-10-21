# Article titles and naming on fa.wiki

Purpose: how to choose and spell a fa.wiki article title. Covers common name, singular, characters, هٔ, diacritics and ZWNJ, parenthetical disambiguation, people, works, foreign-name transliteration, and redirects.

Tags:
- **[V]**: a quote or close paraphrase from the fa.wiki page.
- **[C]**: read in the source of fa.wiki's tools.
- **[LOW]**: from a search summary only.
- **[UNVERIFIED]**: no source found.

Researched 2026-10-21. `scripts/fa_lint.py` lints article text, **not titles**, so every rule here is manual (Claude). Main page: NAMING = [ویکی‌پدیا:قواعد نام‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری). Title rules in the MOS: [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه).

## Contents
1. [Choosing the name](#1-choosing-the-name)
2. [Spelling the title](#2-spelling-the-title)
3. [هٔ in titles: current status](#3-هٔ-in-titles-current-status)
4. [Disambiguation](#4-disambiguation)
5. [People](#5-people)
6. [Works: title vs running text](#6-works-title-vs-running-text)
7. [Foreign names and transliteration](#7-foreign-names-and-transliteration)
8. [Redirects](#8-redirects)
9. [Known gaps / UNVERIFIED](#9-known-gaps--unverified)

## 1. Choosing the name

| Rule | ✅ | ❌ | Source | Tag |
|---|---|---|---|---|
| Use the **common name** in reliable Persian sources. The ideal title is «کوتاه، معمولی، قابل تمایز و قابل شناختن» and consistent with similar articles. | — | — | [NAMING § عنوان ایدئال](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری) | [V] |
| **Singular**, unless the name is always plural in Persian: «نام مقاله‌های خود را به شکل مفرد انتخاب کرده و از شکل جمع آن بپرهیزید، مگر اینکه آن نام همیشه در زبان فارسی به شکل جمع استفاده شود». | گربه | گربه‌ها | [NAMING § مفرد و جمع](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری) | [V] |
| Persian characters. No #, $, &, * and similar symbols. | — | — | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [NAMING](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری) | [LOW] |
| Persian ی/ک, never Arabic ي/ك (as in body text). | — | — | [شیوه‌نامه § کد صحیح نویسه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |

## 2. Spelling the title

| Rule | ✅ | ❌ | Source | Tag |
|---|---|---|---|---|
| **No اعراب** (fatha, kasra, damma, tashdid): «در عنوان اصلی مقاله نباید از اعراب (زبر و زیر و پیش و تشدید) استفاده شود». An RfC proposed minimal diacritics for ambiguous titles that also have a diacritic-free redirect. Its outcome is unclear, so do not rely on it. | محمد | مُحَمَّد | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [نظرخواهی اعراب](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_اعراب_در_عنوان_مقالات_ابهام‌دار_به_شرط_موجود_بودن_تغییرمسیر_بدون_اعراب) | [V] / [LOW] |
| **ZWNJ follows دستور خط** in titles too: «سرهم‌نویسی و جدانویسی و استفاده از فاصلهٔ مجازی بر طبق دستور خط … باید رعایت شود». | اسکی‌محله؛ عادل‌ها | اسکی محله؛ عادلها، عادل ها | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| **Tanvin is allowed** where pronounced: «استفاده از تنوین در عنوان مقاله مجاز باشد». | — | — | [نظرخواهی تنوین در عنوان § جمع‌بندی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_تنوین_در_عنوان_مقاله); [دستور خط § تنوین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] |
| **No ezafe hamza (هٔ)**. See §3. | (title) خانه … | (title) خانهٔ … | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| All other body-text orthography (ی/ک, ZWNJ, hamza seats) applies. See `orthography.md`. | — | — | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |

## 3. هٔ in titles: current status

- **The current MOS text bans it:** «به طور سنتی برای آسان‌تر شدن فرایند جستجو، «ی روی ه‍» (مثال: خانهٔ) در عنوان مقاله‌ها نمی‌آید». دستور خط says the same: «به جز در عنوان مقاله ها، پس از «ه» ناملفوظ باید با «-ٔ» نوشت». Sources: [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [دستور خط § کسرهٔ اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط). [V]
- 2014 RfC «تغییر شیوه‌نامه برای بکارگیری «هٔ» در عنوان مقاله‌ها»: summarised as **no consensus to allow هٔ** ([RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/تغییر_شیوه‌نامه_برای_بکارگیری_«هٔ»_در_عنوان_مقاله‌ها)). [LOW]
- A later RfC, «تغییر بند سیاست عنوان صفحه‌ها», proposed allowing هٔ and اعراب. **Its outcome was not found** ([RfC](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/تغییر_بند_سیاست_عنوان_صفحه‌ها)). [LOW]
- ⚠️ **Uncertain.** Default to **no هٔ in the title, with هٔ in the body.** Example: title «… خانه …», body «خانهٔ …». Before a page move or a title dispute, re-check the live MOS § عنوان. Never mass-move existing titles in either direction.
- The body of the article still uses هٔ (FA14/FA15 enforce this in text). The bold title-word in the lead follows body orthography. This is inferred from the body rule; no explicit source was found [UNVERIFIED].

## 4. Disambiguation
Sources: [ویکی‌پدیا:ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی); [شیوه‌نامه/صفحه‌های ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌های_ابهام‌زدایی).

| Rule | ✅ | ❌ | Source | Tag |
|---|---|---|---|---|
| Add a parenthetical qualifier only when natural disambiguation is impossible: «افزودن عبارت ابهام‌زدا داخل پرانتز به انتهای عنوان دارای ابهام روش استاندارد است». Parentheses disambiguate; they do not add information. | — | — | [ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی) | [V] |
| **Exactly one space** before the parenthesis. | کازابلانکا (فیلم) | کازابلانکا(فیلم) | [ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی); [شیوه‌نامه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] |
| Use the simplest qualifier. | موز (اسطوره) | موز (شخصیت اسطوره‌ای) | [ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی) | [V] |
| Primary topic: the main sense gets the bare title, the others get parentheses. If the name has only one use on fa.wiki, add no parentheses. | — | — | [ابهام‌زدایی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ابهام‌زدایی) | [V] |
| **Films:** other films with the same title are qualified with «فیلم» plus the release year. The exact pattern (e.g. «(فیلم ۱۹۴۲)») is not confirmed. | «X (فیلم ۱۹۴۲)» (pattern [UNVERIFIED]) | — | [قواعد نام‌گذاری (فیلم‌ها)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28فیلم‌ها%29) | [LOW] |
| **Places:** use parentheses, not a comma. For Iranian villages or cities with the same name, put the شهرستان in parentheses. | X (شهرستان Y) | X، Y | [قواعد نام‌گذاری (اسامی جغرافیایی)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28اسامی_جغرافیایی%29) | [LOW] |

## 5. People
Source: [قواعد نام‌گذاری (اشخاص)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28اشخاص%29) (all [LOW] unless marked).
- Usually **given name + family name**, with redirects from the other forms.
- For **pseudonyms and pen names**, use the name most reliable sources use.
- **Honorifics** (e.g. اعلی‌حضرت) are not used unless the titled form is unambiguous and better known. In body text, the اشتباه‌یاب list of القاب غیرمجاز (حضرت، (ع)، (ره)، شادروان، مرحوم، زنده‌یاد، دکتر، پروفسور، آیت‌الله…) is flagged by the linter as **FW06** ([WWD L769](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L769)) [C].
- **«سید»:** include it in the title unless the person is widely known without it. A separate RfC exists («سید در عنوان مقالات»); its outcome was not retrieved [LOW].
- Spelling of personal names: follow reliable sources. Never auto-join or auto-split compound names (حمیدرضا, محمدزاده). The tools' name rules are flagged as risky ([AA L118-L124](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L118-L124)) [C].
- The biography lead gives name, birth/death dates, nationality and main roles ([شیوه‌نامه/زندگی‌نامه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/زندگی‌نامه‌ها)) [LOW].

## 6. Works: title vs running text
Source: [شیوه‌نامه/قالب‌بندی متون § عنوان آثار](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/قالب‌بندی_متون) [V]: «عنوان آثار کوتاه‌تر، از جمله موارد زیر، در داخل گیومه می‌آید».

| Kind of work | In running text | Example |
|---|---|---|
| Books, films, albums, plays, TV series, newspapers and magazines | *italic* (`''…''`) | ''شازده کوچولو'' |
| Songs, short poems, short stories, articles, episodes and chapters | «…» | «مرغ سحر» |
| Scriptures and legal documents | neither | قرآن، قانون اساسی |

- The **article title itself** is plain text: no italics or «» in the page name. The subject is bolded at its first mention in the lead and not linked ([بخش آغازین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/بخش_آغازین), [راهنمایی برای نوشتن مقاله‌های بهتر](https://fa.wikipedia.org/wiki/ویکی‌پدیا:راهنمایی_برای_نوشتن_مقاله‌های_بهتر)) [LOW].
- Use «» for names and technical terms **only on first use** ([نشانه‌های نگارشی § گیومه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی)) [V].

## 7. Foreign names and transliteration

| Step | Rule | Source | Tag |
|---|---|---|---|
| 1 | **An established Persian form wins**, even if it is "incorrect". The criterion is wide use in Persian reference sources. | [قواعد نام‌گذاری (فارسی‌سازی نام‌های خارجی)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28فارسی‌سازی_نام‌های_خارجی%29) | [LOW] |
| 2 | If several forms are common, decide by consensus and mention the alternate form in the lead (e.g. واشِنگتن / واشینگتن). | same | [LOW] |
| 3 | With no Persian written record, use sources such as the Academy's 1381 «شیوه‌نامه ضبط اعلام». | [ویکی‌پدیا:نگارش نام‌های خارجی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نگارش_نام‌های_خارجی) | [LOW] |
| 4 | Otherwise, use the form closest to the **native pronunciation**: transcribe to IPA first, then apply the IPA → Persian guide. The page includes a Pinyin → Persian table. | [ویکی‌پدیا:نویسه‌گردانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نویسه‌گردانی); [راهنما:الفبای آوانگاری بین‌المللی فارسی](https://fa.wikipedia.org/wiki/راهنما:الفبای_آوانگاری_بین‌المللی_فارسی) | [LOW] |
| 5 | Per-language pages exist, e.g. German (with an Italian section). A consensus about a specific word overrides the rule-of-thumb tables. | [نویسه‌گردانی آلمانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:زبان_و_زبان‌شناسی/نویسه‌گردانی_آلمانی) | [LOW] |
| — | Romanising Persian (Persian → Latin): see [ویکی‌پدیا:آوانویسی فارسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:آوانویسی_فارسی). Its content was not researched. | [آوانویسی فارسی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:آوانویسی_فارسی) | [UNVERIFIED] |

Practical rules for Claude:
- When translating from English, **do not transliterate an English spelling letter by letter**. First search fa.wiki and Persian reliable sources for an existing form.
- If none exists, follow the native-language pronunciation (step 4), not the English pronunciation, and put the original-script name in the lead, e.g. with `{{به انگلیسی|…}}`. fa.wiki's bot renames `{{انگلیسی|…}}` to this name ([FCC L441-L448](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L441-L448)) [C].
- No English-letter → Persian table (for th, w, etc.) was found [UNVERIFIED]. Flag uncertain renderings on the talk page or in the edit summary rather than guessing silently.

## 8. Redirects
- **People:** create redirects from other name forms (e.g. full name, name without سید) ([قواعد نام‌گذاری (اشخاص)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28اشخاص%29)) [LOW].
- **Diacritics:** the RfC on minimal diacritics assumes a diacritic-free redirect exists ([نظرخواهی اعراب](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_اعراب_در_عنوان_مقالات_ابهام‌دار_به_شرط_موجود_بودن_تغییرمسیر_بدون_اعراب)) [LOW]. Since titles have no diacritics, a redirect *from* a diacritic form is optional [UNVERIFIED].
- **هٔ:** create a redirect from the هٔ spelling to the plain-ه title, so both spellings work in search. This is a research recommendation, not quoted policy [UNVERIFIED].
- **Transliteration variants:** redirect common alternate spellings (e.g. the واشِنگتن / واشینگتن pair from the naming page), and mention the main alternate in the lead (§7) [LOW].
- **ZWNJ / no-ZWNJ and joined ها variants:** a redirect from the space-separated form helps search [UNVERIFIED].
- Disambiguation pages list the uses. Do not link to a disambiguation page from «جستارهای وابسته» («به هیچ وجه») ([صفحه‌آرایی § جستارهای وابسته](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/صفحه‌آرایی)) [V].

## 9. Known gaps / [UNVERIFIED]
- The outcome of «تغییر بند سیاست عنوان صفحه‌ها» (هٔ and اعراب in titles). The status of the minimal-diacritics RfC.
- The exact film qualifier pattern («فیلم ۱۹۴۲» vs other forms). Rules for other media (albums, TV series, books).
- The outcome of the «سید در عنوان مقالات» RfC.
- An English-letter → Persian transliteration table. The content of آوانویسی فارسی.
- Whether redirects from هٔ, diacritic and ZWNJ variants are recommended by policy (only inferred here).
- Whether the bolded lead title uses هٔ (inferred yes).
