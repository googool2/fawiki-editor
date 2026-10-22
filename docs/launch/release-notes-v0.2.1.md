# fawiki-editor v0.2.1

A patch release from the first checks against the live Persian Wikipedia. It fixes one serious
bug: v0.2.0 could corrupt Uyghur text. It also corrects six infobox parameter names. No command,
option or output format changed, and safety only got stricter.

## Upgrade

```bash
claude plugin marketplace update fawiki-tools
claude plugin update fawiki-editor@fawiki-tools
```
If you copied the skill by hand, replace `~/.claude/skills/fawiki-editor` with the new
`skills/fawiki-editor`.

## Fixed
- **Other Arabic-script languages are left alone.** v0.2.0 changed ي/ك/ى inside Uyghur place
  names (109 wrong changes in one article). Words that contain letters Persian never uses
  (Uyghur, Kurdish, Urdu, Pashto, Sindhi), and their neighbours, are now protected like
  templates and links.
- **FA42** no longer splits chains of initials or acronyms («آ.ای.اچ.», «دی.آی.سی.ای») and no
  longer puts a space after a namespace colon («ویکی‌پدیا:شیوه‌نامه»).
- **FA40** no longer removes the space in list items such as `* .us`.
- **Infobox parameters checked against the live templates:** 117 of 123 were right. Fixed:
  film `مدت` (was `مدت زمان`); country `نام عادی`, `تصویر نشان ملی`, `زبان(های) رسمی`; musical
  artist `پس‌زمینه` (was `پیش‌زمینه`); `سازهای برجسته` removed.
- `{{کنترل مرجعیت}}` does not exist on fa.wiki. English Authority control now maps to
  `{{داده‌های کتابخانه‌ای}}`, and Short description to `{{توصیف کوتاه}}`.

## Measured
- **240 random current fa.wiki articles**, every automatic change read by hand. With the v0.2.0
  rules, 109 of 668 changes were wrong, all in one article. With v0.2.1, **0 of 475** were wrong.
- The 88-article corpus is unchanged: **0 wrong of 742**.
- 300 tests pass, and the synthetic benchmark is green on Linux, macOS and Windows with Python
  3.10 and 3.13. It now includes a Uyghur trap that fails on v0.2.0.

## New for maintainers and reviewers
- A monthly CI job (`live fa.wiki check`) re-checks template names and rehearses on 60 new
  random articles.
- **Review wanted:** [docs/review/REVIEWING.md](https://github.com/googool2/fawiki-editor/blob/main/docs/review/REVIEWING.md)
  lists every rule in Persian. A [review form](https://github.com/googool2/fawiki-editor/issues/new?template=rule-review.yml)
  takes one line per rule.

## Known issues
- Five citation parameter names are unresolved: `{{یادکرد کتاب}}` `نویسنده`, `ترجمه` and
  `{{یادکرد ژورنال}}` `نویسنده`, `جلد`, `ناشر`. They are missing from TemplateData, but fa.wiki's own
  citer tool emits them, so they were kept. If preview shows an unknown-parameter error, see
  `references/citations.md`.
- The rules and all labels were written by Claude, and no fa.wiki editor has reviewed them yet.

## خلاصه به فارسی
نسخهٔ ۰٫۲٫۱ باگی را اصلاح می‌کند که حرف‌های ی و ک را در متن اویغوری عوض می‌کرد. حالا متن اویغوری، کردی، اردو، پشتو و سندی دست نمی‌خورد. نام شش پارامتر جعبهٔ اطلاعات هم با الگوهای خود ویکی‌فا تطبیق داده و اصلاح شد. روی ۲۴۰ مقالهٔ تصادفی امروز، این نسخه از ۴۷۵ اصلاح خودکار هیچ‌کدام را غلط انجام نداد. اگر در ویکی‌پدیای فارسی ویرایش می‌کنید، از بازبینی قواعد استقبال می‌کنیم.

Full list: [CHANGELOG](https://github.com/googool2/fawiki-editor/blob/main/CHANGELOG.md#021---2026-10-22)
