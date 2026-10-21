# Persian orthography (رسم‌الخط) on fa.wiki

Purpose: the spelling, character, ZWNJ, digit and punctuation rules fa.wiki expects in article prose. Each rule gives its source and says whether `scripts/fa_lint.py` fixes it, only warns, or leaves it to Claude.

**Workflow. Do not hand-fix any row whose "Automated by" cell names an FA rule.**
1. Write or translate normally, then run `python3 scripts/fa_lint.py ARTICLE.wikitext`. This prints a report and a diff and leaves the file alone. Run it again with `--fix` to apply the changes. `--list-rules` prints the live rule set, and `--disable FA01,…` skips rules.
2. The linter edits prose only. `[[…]]`, `{{…}}`, `<ref>`, URLs, comments, `<math>`, `<poem>` and table attributes stay byte-identical. Problems inside those zones come back as **FW** warnings.
3. Next, apply the rows marked **manual (Claude)** and decide each FW warning one at a time. Never bulk-accept them.
4. Do not submit an edit that changes only whitespace. fa.wiki's own cosmetic bot discards such diffs ([FCC L820-L822](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L820-L822)).

Tags:
- **[V]**: a quote or close paraphrase from the fa.wiki page.
- **[C]**: read in the source of fa.wiki's tools (fawikibot, persiantools/ابرابزار).
- **[LOW]**: from a search summary only.
- **[UNVERIFIED]**: no source found.

Researched 2026-10-21. These pages change, so re-check anything that will be contested.

## Contents
1. [Letters and invisible characters](#1-letters-and-invisible-characters)
2. [Ezafe after silent ه (هٔ)](#2-ezafe-after-silent-ه-هٔ)
3. [ZWNJ clean-up](#3-zwnj-clean-up)
4. [ZWNJ: where it is required](#4-zwnj-where-it-is-required)
5. [Hamza, tanvin, ة](#5-hamza-tanvin-ة)
6. [Digits and separators](#6-digits-and-separators)
7. [Punctuation and spacing](#7-punctuation-and-spacing)
8. [Common misspellings](#8-common-misspellings)
9. [Warning codes (never auto-fixed)](#9-warning-codes-never-auto-fixed)
10. [Known gaps / UNVERIFIED](#10-known-gaps--unverified)

Basis: «ویکی‌پدیا:دستور خط» is «برگرفته از کتاب دستور خط فرهنگستان زبان و ادب فارسی» ([دستور خط § intro](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط)) [V]. The Manual of Style is a guideline (رهنمود), not a policy ([سیاست‌ها و رهنمودها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:سیاست‌ها_و_رهنمودها)) [V].

## 1. Letters and invisible characters

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Use Persian ی (U+06CC, dec 1740), never Arabic ي (U+064A, dec 1610) or ى. The page says «این دو نویسه از اساس متفاوت بوده و به‌هیچ‌وجه نباید به جای یکدیگر به کار روند». | فارسی | فارسي، فارسى | [شیوه‌نامه § کد صحیح نویسه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [FCC L129-L140](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L129-L140) | [V] [C] | FA01 |
| Use Persian ک (U+06A9), never Arabic ك (U+0643). Final ک is written «با سرکش». | کتاب، کودک | كتاب، كودك | [شیوه‌نامه § کد صحیح نویسه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [PT L130-L145](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L130-L145) | [V] [C] | FA02 |
| Fold Arabic presentation forms (ﻙ ﻴ ﻻ …) and Sindhi ڪ to the standard letters. | لا، ک | ﻻ، ڪ | [PT L82-L128](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L82-L128); [AA L1032-L1048](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1032-L1048) | [C] | FA00 |
| Do **not** fold ہ ە ھ. They are real letters in Kurdish and Urdu names; only ي ى ك and the presentation forms are safe to fold. | (keep as in source) | — | [CD L353-L354](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L353-L354) (strips Arabic/Urdu templates before checking); research recommendation | [LOW] | manual (Claude) |
| Text that is actually in Arabic keeps its Arabic letters. Wrap it in `{{عبارت عربی\|…}}` (short) or `{{آغاز عربی}}…{{پایان عربی}}` (long) so the tools skip it. | `{{عبارت عربی\|…}}` | bare Arabic quotation in prose (it will be folded) | [شیوه‌نامه § Arabic text](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [CD L353-L354](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L353-L354) | [LOW] [C] | manual (Claude) |
| Arabic letters inside `[[links]]` or `{{templates}}` are reported, not changed. | `[[کتاب]]` | `[[كتاب]]` | [FCC L130](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L130) (protected zones) | [C] | FW01 |
| No kashida/tatweel ـ (U+0640) between letters. None of fa.wiki's tools removes it from prose, so the rule itself has no fa.wiki source. | ایران | ایـــران | none on fa.wiki; [CD L364](https://github.com/PersianWikipedia/fawikibot/blob/master/CheckDictation.py#L364) strips ـ before spell-checking | [UNVERIFIED] | FA05 |
| Remove control characters and the BOM. | — | U+FEFF, U+0000–U+001F | [AA L1056](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1056) | [C] | FA09 |
| Type ZWNJ as the real character U+200C (Shift+Space on the standard Persian keyboard). `&zwnj;` and `{{فم}}` both mean ZWNJ. | می‌رود | می&zwnj;رود (in new text) | [نیم‌فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله); [FCC L436](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L436) | [V] [C] | manual (Claude) |

## 2. Ezafe after silent ه (هٔ)

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| In body text, ezafe after silent ه is ه + U+0654 «ٔ»: «از نویسهٔ «ء روی ه‍» استفاده می‌شود». | خانهٔ بزرگ | خانه بزرگ، خانه ی بزرگ، خانه‌ی بزرگ | [شیوه‌نامه § اضافه پس از «ه» ناملفوظ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [دستور خط § کسرهٔ اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | FA14/FA15 for the malformed variants; a missing marker («خانه بزرگ») is manual (Claude) |
| The precomposed ۀ (U+06C0) is banned: «درست: خانهٔ = خانه + ٔ . غلط: خانۀ = خان + ۀ». | خانهٔ | خانۀ | [شیوه‌نامه § اضافه پس از «ه» ناملفوظ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | FA14 |
| هٓ, هء and «ه ء» become هٔ. | خانهٔ من | خانهء من، خانه ء من | [PT L157-L170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170); [PT tests L6-L24](https://github.com/ebraminio/persiantools/blob/master/test/persiantools_test.js#L6-L24) | [C] | FA14 |
| The ZWNJ form ه‌ی used as ezafe becomes هٔ. | خانهٔ من | خانه‌ی من | [شیوه‌نامه § اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) (lists «خانه‌ی بزرگ» as wrong); [PT L157-L170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170) | [V] [C] | FA15 |
| «ه ی» with a full space is ambiguous: it may be ezafe (→ هٔ) or the indefinite/relative ی (→ ه‌ای). Decide from the meaning. | خانهٔ من / خانه‌ای که | خانه ی من | [PT L157-L170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170) (⚠️ risky rule) | [C] | FW05 |
| The indefinite or relative ی after silent ه is written ه‌ای. | خانه‌ای | خانه‌ئی، خانه‌یی | [نیم‌فاصله § ی پایانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله); [PT L157-L170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170) | [V] [C] | FA16 |
| Never add هٔ after a consonantal ه (کوه، گره، شبیه، فرمانده). FCC keeps a list of these words (`sametH`) but never uses it. | کوه دماوند | کوهٔ دماوند | [FCC L41](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L41) | [LOW] | manual (Claude) |
| **Titles** take no هٔ (search convenience). See `titles.md`. | (title) خانه … | (title) خانهٔ … | [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [دستور خط § کسرهٔ اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) «به جز در عنوان مقاله ها» | [V] | manual (Claude) |

## 3. ZWNJ clean-up

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Collapse a run of ZWNJs into one. | می‌رود | می‌‌رود | [FCC L292](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L292); [PT L71](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L71) | [C] | FA10 |
| No ZWNJ next to a space. | کتاب‌ها و | کتاب‌ها‌ و | [PT L78-L79](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L78-L79); [AA L1022-L1028](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1022-L1028) | [C] | FA11 |
| No ZWNJ after a non-joining letter (ا آ د ذ ر ز ژ و ؤ …), where it does nothing. | کارها، روزها | کار‌ها، روز‌ها | [PT L73](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L73); [AA L1004-L1006](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1004-L1006), test «ر‌فاصله→رفاصله» [AA L1396](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1396) | [C] | FA12 |
| A ZWNJ belongs only between two letters. Keep it next to a wikilink: «[[کتاب]]‌ها» is legitimate. | `[[کتاب]]‌ها` | ZWNJ before a digit or punctuation mark | [FCC L816-L817](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L816-L817), [L293-L294](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L293-L294) | [C] | FA13 |

## 4. ZWNJ: where it is required

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| The verb prefixes می and همی are always separate, joined by ZWNJ: «می و همی همیشه جدا از فعلِ پس از خود است». | می‌رود، همی‌گوید | میرود، می رود | [دستور خط § می و همی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | FA20 (only for stems on the ابرابزار whitelist) |
| نمی‌ follows the same rule (ن + می). | نمی‌خواهد | نمیخواهد، نمی خواهد | inferred from [دستور خط § می و همی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط); [PT L195-L237](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L195-L237); [AA L1146-L1165](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1146-L1165) | [LOW] [C] | FA20 |
| Do not split nouns that begin with می. The tools use a verb-stem whitelist, not a noun blacklist, and they handle میگو, میستری and میدوی explicitly. | میوه، میز، میلیون، میدان، میگو | می‌وه، می‌گو | [AA L1203-L1209](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1203-L1209) | [C] | FA20 (stem whitelist protects these) |
| A verb whose stem is not on the whitelist, or a complex verb (باز/در/بر/فرو + می), still needs the ZWNJ after می. The tools' complex-verb rule is buggy («در گذشته», «بر گردن»). | (ن)می‌ + stem | — | [AA L1126-L1143](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1126-L1143) | [C] | manual (Claude) |
| Plural ها is never written after a full space: «در هیچ موردی ها با فاصلهٔ معمولی نوشته نمی‌شود». Otherwise joined and ZWNJ forms are both correct. | کتاب‌ها، کتابها | کتاب ها | [دستور خط § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | FA21 (space → ZWNJ; no ZWNJ after a non-joining letter) |
| ZWNJ before ها is **mandatory** after: foreign/unfamiliar words, words with many teeth, words ending in ط/ظ, words ending in silent ه, and pronounced ه after a joining letter. It is also required when the stem is emphasised. In titles, «عادل‌ها» is correct. **Safe default: always use ‌ها after a joining letter.** | فرمالیست‌ها، حساسیت‌ها، استنباط‌ها، خانه‌ها، فقیه‌ها | فرمالیستها، خانهها | [دستور خط § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط); [نیم‌فاصله § ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله); [شیوه‌نامه § عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | joined → ZWNJ is manual (Claude) |
| تر and ترین always take ZWNJ, with five exceptions: «جز در این کلمه‌ها: بهتر، مهتر، کهتر، بیشتر، کمتر». | بزرگ‌تر، بزرگ‌ترین، بیشتر، کمتر | بزرگتر، بزرگ تر، بیش‌تر | [نیم‌فاصله § تر و ترین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | FA22 for « ترین»; « تر» → FW02; a joined form is manual (Claude) |
| The superlatives of the exceptions are joined. | بیشترین، کمترین، بهترین | بیش‌ترین | extension of [نیم‌فاصله § تر و ترین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [LOW] | FA22 (بیش/کم → joined) |
| Pronoun suffixes ـم ـت ـش ـمان ـتان ـشان are joined: «این ضمیرها همیشه به صورت متصل نوشته می‌شوند». | کتابش، کتابمان | کتاب‌ش، کتاب ش | [نیم‌فاصله § ضمیرهای متصل](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | manual (Claude) |
| After silent ه, or after ی pronounced /i/, the suffix takes ZWNJ. | خانه‌ام، خانه‌اند، کشتی‌اش، کشتی‌مان | خانه ام، خانه اند | [دستور خط § میانجی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط); [نیم‌فاصله § ی پایانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | FA23 (ه + ام/ای/ایم/اید/اند); the کشتی‌… type is manual (Claude) |
| «است» after silent ه stays a separate word. The tools exclude it on purpose: «این یک خانه است». The copula section of نیم‌فاصله was not retrieved. | خانه است | خانه‌است | [PT L253-L256](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L253-L256) | [C] | FA23 leaves it alone |
| ⚠️ «ای» after ه can be a vocative or a separately written word. Check FA23 hits such as «که ای». | که ای | که‌ای | [AA L1201](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1201) | [C] | FA23 (review diff) |
| Indefinite ی after silent ه, a consonant ی, or the vowel ای is joined with ZWNJ. | خانه‌ای، تیزپی‌ای، کشتی‌ای | خانه ای | [نیم‌فاصله § ی پایانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | FA23 (ه + ای); others manual (Claude) |
| After long ا / و, write «یی» joined, with no ZWNJ. | آوایی، پرستویی، دانشجویی | دانشجوئی | [دستور خط § میانجی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | manual (Claude) |
| The prefixes بی and هم take ZWNJ, except in lexicalised (بسیط‌گونه) words. Decide word by word. | بی‌طرف؛ بیهوده، همسایه، همکار، همدرس | بی طرف | [نیم‌فاصله § بی / هم](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | manual (Claude) |
| Compounds take ZWNJ, including when the second part starts with ا. Per-word disputes go to «ویکی‌پدیا:نظرخواهی/استفاده از نیم‌فاصله در واژه‌های مرکب». | دست‌کم، سیب‌زمینی، دل‌انگیز | دستکم، سیب زمینی | [نیم‌فاصله § کلمات مرکب](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله) | [V] | manual (Claude) |
| The preposition به is a separate word, except in بدین، بدان، بدو، بدیشان. | به برادرت گفتم، به‌سختی | ببرادرت | [دستور خط § به](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | manual; FA50 fixes بعنوان/بطور/بدست/بوسیله |
| The names بهنام and بهروز take no ZWNJ. For other personal names (حمیدرضا, محمدزاده), follow the spelling reliable sources use. Never re-split or re-join them. | بهنام | به‌نام (as a name) | [نیم‌فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نیم‌فاصله); [AA L118-L124](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L118-L124) ⚠️ | [LOW] [C] | manual (Claude) |

## 5. Hamza, tanvin, ة

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| The hamza seat follows the preceding vowel: kasra/sukun → ئ, fatha → أ, damma → ؤ. | هیئت، تأثیر، مؤسسه | هیات، تاثیر، موسسه | [شیوه‌نامه § همزه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [LOW] | FA50 for listed words; others manual (Claude) |
| Conventional exceptions take ئ. Use the word, not the vowel rule. | مسئله، مسئول، مسئولیت | مساله، مسأله | [دستور خط § همزهٔ میانی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط); [AA L688-L689](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L688-L689) | [LOW] [C] | FA50 (مساله/مسأله) |
| Write ئ, not یی, in these words. | جزئی، جزئیات، رئیس | جزیی، جزییات، رییس | [WWD L219](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L219); [AA L687](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L687) | [C] | FA50 |
| Final hamza (استثنا vs استثناء): there is no consensus («اجماعی وجود ندارد»), so leave it as found. | (as found) | — | [AA L966](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L966) | [C] | manual (do not change) |
| Tanvin only on Arabic-origin words, and only where pronounced. Never on Persian or European words: «گاهاً، سفارشاً، ناچاراً … شکل درست: گاهی یا گهگاه، (به طور) سفارشی، به ناچار». | کاملاً، نسبتاً؛ گاهی، به ناچار | گاهاً، ناچاراً، تلفناً، زباناً | [دستور خط § تنوین](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | manual (Claude) |
| Arabic ة becomes ت before tanvin. Otherwise it becomes ت if pronounced /t/, or silent ه if pronounced /e/. | موقتاً، نسبتاً | موقةً | [دستور خط § ة](https://fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط) | [V] | manual (Claude) |
| Tanvin is allowed in titles (RfC). | — | — | [نظرخواهی تنوین در عنوان](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نظرخواهی/استفاده_از_تنوین_در_عنوان_مقاله) | [V] | manual (Claude) |

## 6. Digits and separators
More detail is in `dates-numbers.md`.

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Persian digits only: «ارقام به شکل فارسی نوشته می‌شوند: ۱۲۳۴۵۶۷۸۹۰ - نه به شکل عربی: ١٢٣٤٥٦٧٨٩٠ یا لاتین». | ۱۹۹۹، ۴۵۶ | 1999، ٤٥٦ | [تاریخ‌ها و اعداد § ارقام](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | FA03 (Arabic-Indic); FA04 (Latin, in prose tokens without Latin letters) |
| Keep Latin digits in URLs, ISBN/ISSN/DOI/PMID, template parameters, file names, `<math>`/`<code>`, and tokens mixed with Latin letters. FA04 also skips numbers on a stretch of line where Latin letters outnumber Persian ones (English bibliographies and titles; found in the real-world rehearsal). | F-16، MP3، Windows 10 | F-۱۶ | [FCC L58-L100](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L58-L100), [L520-L541](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L520-L541) (converts back to Latin there) | [C] | FA04 skips these |
| The thousands separator is ٬ (U+066C, dec 1644), not a comma or a dot. | ۲۴٬۷۰۰٬۰۰۰ | ۲۴,۷۰۰,۰۰۰، ۲۴.۷۰۰.۰۰۰ | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | FA08 (`,` between Persian digits); ، or . as a separator is manual (Claude) |
| The decimal separator is ٫ (U+066B, dec 1643), never «/». FA07 leaves «۷۰۰.۰۰۰»-style groups (exactly three digits after the dot: a thousands separator, reported as FW09) and version numbers after «نسخه/ویرایش» alone. | ۳٫۵، ۱۲٬۰۰۴٬۹۵۰٫۰۰۰۳ | ۳.۵، ۳/۵ | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [جداکننده هزارگان](https://fa.wikipedia.org/wiki/جداکننده_هزارگان) | [V] | FA07 (`.` between Persian digits); «/» is manual (Claude) |
| Never use a comma (، or ,) to group digits: the comma and the separator «نباید به جای یک‌دیگر به کار روند». | ۱٬۲۰۰ | ۱،۲۰۰ | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | FA08 / manual (Claude) |
| ٪ replaces % in scientific/technical text, tables and infoboxes, written to the left of the number. In non-technical prose write the word «درصد». | ۲۰ درصد (prose); ۲۰٪ (table) | ۲۰% | [تاریخ‌ها و اعداد § درصد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) (search excerpt, 2026-10-21) | [LOW] | FA06 fixes the glyph; choosing «درصد» is manual (Claude) |
| Spell out zero to nine in prose. Never spell out digits in formulas. Proper names keep their digits. | سه کتاب؛ خیابان ۱۷ شهریور | ۳ کتاب | [تاریخ‌ها و اعداد § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |
| Ordinals are spelled out, including regnal numbers. | پنجم، مهرداد دوم، لوئی نهم | ۵ام، مهرداد ۲ | [تاریخ‌ها و اعداد § اعداد ترتیبی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] | manual (Claude) |

## 7. Punctuation and spacing

| Rule | ✅ correct | ❌ wrong | Source | Tag | Automated by |
|---|---|---|---|---|---|
| Quotes use «» only, «نه از علامت نقل قول تکی یا دوتایی انگلیسی». Use them for direct quotes, and for names or technical terms **on first use only**. | «آزادی» | “آزادی”، "آزادی" | [نشانه‌های نگارشی § گیومه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی) | [V] | FA33 (curly “…”); straight "…" → FW03 |
| Use the Persian comma ، after Persian words. No explicit sentence requiring this was found, but it is implied and fa.wiki tools enforce it. | الف، ب | الف, ب | [AA L1228](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1228); [PT L275](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L275) | [C] ([UNVERIFIED] as a written rule) | FA30 |
| Semicolon ؛. Its uses are few: «کاربردهای آن اندک است». | …؛ … | …; … | [نشانه‌های نگارشی § نقطه‌ویرگول](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی); [AA L1224](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1224) | [V] [C] | FA31 |
| Question mark ؟. Not used in indirect questions. Repeated marks (؟؟) are not suitable for formal text. | آیا … ؟ | ? ، ؟؟ | [نشانه‌های نگارشی § علامت سؤال](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی); [AA L1220](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1220) | [V] [C] | FA32; ؟؟ and indirect questions are manual (Claude) |
| Single marks (. ، ؛ ؟ ! :) and closing marks () ») take no space before them. | کتاب، دفتر | کتاب ، دفتر | [شیوه‌نامه § نشانه‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) (منفرد/مزدوج); [AA L1342](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1342) | [LOW] [C] | FA40 |
| Opening « and ( take no space after them. | «متن» (متن) | « متن » ( متن ) | [شیوه‌نامه § نشانه‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [AA L1255-L1259](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1255-L1259) | [LOW] [C] | FA41 (FA40 handles the closing side) |
| One space after a single mark between Persian words. FA42 needs two letters on each side of «.» or «:», so abbreviations and initials («ه.ق»، «ی.س.باخ») stay joined; FA40 never glues «.» onto «...». | الف، ب. پ | الف،ب.پ | [شیوه‌نامه § نشانه‌گذاری](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [AA L1248](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1248) | [LOW] [C] | FA42 |
| A space before an opening « or ( that follows a word. | گفت «بله» | گفت«بله» | [AA L1263-L1269](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1263-L1269) | [C] | manual (Claude) |
| One space between words, and no trailing whitespace. Runs of spaces before `=` in templates are alignment and are left alone. | — | two spaces | [AA L1238](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1238), [L1057](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L1057) | [C] | FA43, FA44 |
| Avoid nested parentheses, except in formulas. | — | (… (…) …) | [نشانه‌های نگارشی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی) | [LOW] | manual (Claude) |
| No space inside an abbreviation: the abbreviation dot «جزو سجاوندی‌ها محسوب نمی‌شود». | ر.ک. | ر. ک. | [کوته‌نوشت § فاصله](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/کوته‌نوشت) | [V] | manual (Claude) |

## 8. Common misspellings
Source lists: «ویکی‌پدیا:اشتباه‌یاب/فهرست» ([page](https://fa.wikipedia.org/wiki/ویکی‌پدیا:اشتباه‌یاب/فهرست)), as used by the اشتباه‌یاب backend ([WWD](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt)), and the ابرابزار/FCC dictionaries. **Automated by FA50**, a curated list of unambiguous entries. If the linter does not flag one of these, fix it manually. Tag [C] throughout. Never "fix" text inside quotations or titles of works.

| ❌ → ✅ | Source | ❌ → ✅ | Source |
|---|---|---|---|
| اطاق → اتاق | [WWD L41](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L41); [شیوه عبارات عربی](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه_عبارات_عربی) | بعنوان → به‌عنوان | [WWD L116](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L116) |
| امپراطور → امپراتور | [WWD L52](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L52) | بطور → به‌طور | [WWD L111](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L111) |
| بلاخره → بالاخره | [WWD L121](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L121) | بدست / بوسیله → به‌دست / به‌وسیلهٔ | [WWD L85](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L85), [L134](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L134) |
| برخواست → برخاست | [WWD L93](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L93) | آنرا / آن‌را → آن را | [WWD L9](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L9) |
| خواستگاه → خاستگاه | [FCC L232](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L232) | درحالیکه → درحالی‌که | [WWD L288](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L288) |
| برگذار → برگزار | [WWD L100](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L100) | هیچکدام / هیچکس → هیچ‌کدام / هیچ‌کس | [AA L698-L701](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L698-L701) |
| خبرگذاری → خبرگزاری | [WWD L265](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L265) | همینطور / همانطور → همین‌طور / همان‌طور | [AA L692-L697](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L692-L697) |
| سپاسگذار → سپاسگزار | [AA L610](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L610) | گزارشات / پیشنهادات → گزارش‌ها / پیشنهادها | [WWD L700](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L700) |
| تلوزیون → تلویزیون | [WWD L187](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L187) | جزییات → جزئیات | [WWD L219](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L219) |
| پزشگی → پزشکی | [WWD L158](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L158) | هیات / هیأت → هیئت | [WWD L618](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L618) |
| لشگر → لشکر | [WWD L456](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L456) | مساله / مسأله → مسئله | [AA L688-L689](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L688-L689) |
| ملیون / ملیارد → میلیون / میلیارد | [WWD L565](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L565) | رییس → رئیس | [AA L687](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L687) |
| ضمینه → زمینه | [AA L603](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L603) | سوال / سئوال → سؤال | [WWD L339](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L339) |
| حاظر / حظور → حاضر / حضور | [AA L628-L631](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L628-L631) | علیرغم → علی‌رغم | [WWD L384](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L384) |
| متاسفانه → متأسفانه | [AA L588](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L588) | بر علیه / برعلیه → علیه | [WWD L98-L99](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L98-L99) |
| تاثیر / تالیف → تأثیر / تألیف | [AA L212-L215](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L212-L215) | فن‌آوری → فناوری | [WWD L417](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L417) |
| ژوییه → ژوئیه; دیسامبر → دسامبر | [FCC L255-L257](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L255-L257) | فرآیند → فرایند | [AA L577](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L577) |
| ویکی پدیا → ویکی‌پدیا; نرم افزار → نرم‌افزار | [AA L255-L257](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L255-L257) | دایره المعارف → دایرةالمعارف | [AA L563-L564](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L563-L564) |
| زنده‌گی / ویژه‌گی → زندگی / ویژگی | [AA L562](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L562), [L613](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L613) | | |

**The tools disagree on these. They are manual (Claude) and never bulk-replaced:** بنیانگذار vs بنیان‌گذار; اساتید → استادان and مربوطه → مربوط (style); فوق‌الذکر (FCC keeps it, WWD suggests یادشده); «گفت و گو» → گفتگو (FCC L210); پروفسور and آیت‌الله, which also appear on the honorific list.
**Register:** colloquial forms (میخونه، خونه، دیگه، بهش) are not encyclopedic. Rewrite them in formal Persian ([slang list](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_slang_word_dict.txt#L1-L16)) [C]: manual (Claude).

## 9. Warning codes (never auto-fixed)

| Code | Trigger | What Claude does | Source | Tag |
|---|---|---|---|---|
| FW01 | Arabic letters inside links or templates | Check that the Persian-letter target page exists before changing a link. Leave genuinely Arabic text (in Arabic templates) alone. | [شیوه‌نامه § کد صحیح نویسه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [FCC L130](https://github.com/PersianWikipedia/fawikibot/blob/master/fa_cosmetic_changes_core.py#L130) | [V] [C] |
| FW02 | « تر» after a word | Comparative → ‌تر. Leave it if it means "wet". | [AA L977-L989](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L977-L989) | [C] |
| FW03 | Straight "…" quotes | Persian quotation → «…». Leave English-language quotations as they are. Never treat `''` as a quote: it is wiki italics. | [نشانه‌های نگارشی § گیومه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:نشانه‌های_نگارشی); [AA L775-L862](https://github.com/PersianWikipedia/fawikibot/blob/master/AbarAbzar.py#L775-L862) | [V] [C] |
| FW04 | Slash or hyphen dates in prose (۲۹/۴/۱۳۶۸) | Rewrite as «۲۹ تیر ۱۳۶۸» (day, month name, year). | [تاریخ‌ها و اعداد § قالب تاریخ](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| FW05 | «ه ی» with a space | Ezafe → هٔ; indefinite/relative → ه‌ای. | [شیوه‌نامه § اضافه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه); [PT L157-L170](https://github.com/ebraminio/persiantools/blob/master/lib/persiantools.js#L157-L170) | [V] [C] |
| FW06 | Honorifics: حضرت، (ع)، (ره)، شادروان، مرحوم، زنده‌یاد، شهید شد، دکتر، پروفسور… | Remove from neutral narration. Keep them inside quotations and fixed proper names. | [WWD L769](https://github.com/PersianWikipedia/fawikibot/blob/master/checkdictation-fa/zz_Wrong_word_dict.txt#L769) (القاب غیرمجاز); [قواعد نام‌گذاری (اشخاص)](https://fa.wikipedia.org/wiki/ویکی‌پدیا:قواعد_نام‌گذاری_%28اشخاص%29) | [C] [LOW] |
| FW07 | «۱۹۷۰ها»-style decades | → «دههٔ ۱۹۷۰». | [تاریخ‌ها و اعداد § دهه](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] |
| FW08 | Non-French Gregorian month names (جولای، آگوست، آپریل، جون، مارچ) | Iranian usage → ژوئیه، اوت، آوریل، ژوئن، مارس. The page lists Afghan forms (جنوری، فبروری…) separately; whether to keep them in Afghan-topic articles is [UNVERIFIED]. | [تاریخ‌ها و اعداد § نام ماه‌ها](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه/تاریخ‌ها_و_اعداد) | [V] (partial) |
| FW09 | A dot between digit groups of three («۷۰۰.۰۰۰») | Probably a thousands separator: write «۷۰۰٬۰۰۰». A decimal uses «٫». Never auto-fixed because the meaning cannot be known. | [شیوه‌نامه § اعداد](https://fa.wikipedia.org/wiki/ویکی‌پدیا:شیوه‌نامه) | [V] | warning only |

## 10. Known gaps / [UNVERIFIED]
- Kashida: no fa.wiki page or tool bans it. FA05 follows general practice (virastar).
- No explicit fa.wiki sentence was found requiring ، ؛ ؟ over , ; ?. The rule is implied by the character sections and enforced by the tools.
- The exact spacing wording in «شیوه‌نامه § نشانه‌گذاری»: only the منفرد/مزدوج grouping was quoted.
- The copula forms (است/ام after words) in «نیم‌فاصله § صورت‌های متصل فعل بودن» were not retrieved.
- ها: نیم‌فاصله says «همیشه باید پیوسته نوشت», while دستور خط allows both forms. Read it as "never a full space" and prefer ZWNJ.
- Hamza: the vowel rule conflicts with مسئله/مسئول. Use the word lists.
- `{{عربی}}…{{پایان عربی}}` / `{{آغاز عربی}}…{{پایان عربی}}` blocks (and the same pattern for اردو، کردی، پشتو) are protected by `fa_lint.py`, as is any text inside a template such as `{{عبارت عربی|…}}` (tested in `tests/test_fa_lint_protection.py`). Bare Arabic text in prose is still folded: wrap it first.
- Unicode code points other than ی 1740 / ي 1610 / ٬ 1644 / ٫ 1643 are annotations, not quotes from fa.wiki.
