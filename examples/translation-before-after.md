# Translation example: en.wiki → fa.wiki

A short, illustrative en.wiki-style excerpt (not a copy of the live article) and the
Persian wikitext the skill should produce from it. It shows what changes, what is kept,
and what the user still has to check by hand. Rules: `references/translation.md`,
`references/citations.md`, `references/article-structure.md`.

<!-- BEFORE -->
## Before (English wikitext)

```wikitext
'''Lake Urmia''' is an [[endorheic lake|endorheic]] [[salt lake]] in [[Iran]].<ref>{{cite web |url=https://www.britannica.com/place/Lake-Urmia |title=Lake Urmia |website=Encyclopaedia Britannica |access-date=12 March 2024}}</ref> The lake is located between the provinces of [[West Azerbaijan Province|West Azerbaijan]] and [[East Azerbaijan Province|East Azerbaijan]].

== References ==
{{Reflist}}

[[Category:Lakes of Iran]]
```

<!-- AFTER -->
## After (Persian wikitext)

```wikitext
'''دریاچهٔ ارومیه''' یک [[دریاچهٔ بسته|دریاچهٔ بستهٔ]] شور در [[ایران]] است.<ref>{{یادکرد وب
| عنوان = Lake Urmia
| نشانی = https://www.britannica.com/place/Lake-Urmia
| وبگاه = Encyclopaedia Britannica
| کد زبان = en
| تاریخ بازبینی = 2024-03-12
}}</ref> این دریاچه میان استان‌های [[استان آذربایجان غربی|آذربایجان غربی]] و [[استان آذربایجان شرقی|آذربایجان شرقی]] قرار دارد.

== منابع ==
{{پانویس}}

[[رده:دریاچه‌های ایران]]
```

## What changed and why

| Element | en.wiki | fa.wiki | Why |
|---|---|---|---|
| Citation template | `{{cite web}}` | `{{یادکرد وب}}` | Persian template and parameter names (`url`→`نشانی`, `title`→`عنوان`, `website`→`وبگاه`, `access-date`→`تاریخ بازبینی`). |
| Source language | implicit | `کد زبان = en` | The source stays English; its title is **not** translated. |
| Access date | `12 March 2024` | `2024-03-12` | Same date, ISO format as fa.wiki's citation generator writes it. Nothing new is added. |
| Reference list | `== References ==` + `{{Reflist}}` | `== منابع ==` + `{{پانویس}}` | Standard fa.wiki heading and template. |
| Category | `[[Category:Lakes of Iran]]` | `[[رده:دریاچه‌های ایران]]` | Persian namespace; the user must confirm the category exists. |
| Links | en titles | fa titles | Each target must be an existing fa.wiki article; see the checklist below. |
| Prose | English | Persian, rewritten | Natural Persian, not a word-for-word calque; orthography via `fa_lint.py`. |

## What the user still has to do

1. **Check every link target** on fa.wiki. Here: `دریاچهٔ بسته`, `استان آذربایجان غربی`,
   `استان آذربایجان شرقی`, and the category `رده:دریاچه‌های ایران`. Titles that do not
   exist must be fixed or unlinked (fa.wiki titles avoid «هٔ», so the real title may be
   «دریاچه بسته»).
2. **Open the source** and confirm it supports each sentence.
3. **Attribute the translation in the edit summary**, for example:
   `ترجمه از [[:en:Lake Urmia]] در ویکی‌پدیای انگلیسی؛ متن با کمک هوش مصنوعی پیش‌نویس و به‌طور کامل بازبینی شد.`
4. **Add the talk-page template** on «بحث:دریاچه ارومیه»: `{{صفحه ترجمه‌شده|en|Lake Urmia}}`.
5. Run the checks before publishing:

```bash
python3 scripts/fa_lint.py draft.wikitext --check
python3 scripts/wikitext_check.py draft.wikitext
```
