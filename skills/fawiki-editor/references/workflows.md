# Workflows by task

Loaded from SKILL.md when the task is known. `F` below means
`python3 SKILL_DIR/scripts/fawiki.py`.

## Write a new article
1. **Notability gate first.** Walk `notability-deletion.md` §1 with the user: at least two
   independent, reliable, secondary sources with significant coverage? Own website, press
   releases and paid advertorials (رپورتاژ آگهی) do not count. If sources are not enough,
   say plainly that the article will probably be deleted and what coverage would change
   that. Do not draft a promotional or unsourced page. Also ask whether fa.wiki already has
   an article on the subject; improving it beats creating a duplicate.
2. **Collect sources** from the user or from tools you actually have. Build each citation
   with `F cite …`; never type citation fields from memory. A `<ref>` says "this source
   supports this sentence", so attach one only when you or the user have seen it say so.
   Well-known works you believe cover the topic but have not opened go in the reply as
   **leads to check** (author + title), and the claim keeps `{{مدرک}}` until verified.
3. **Draft** with the skeleton in `article-structure.md`: bold title in the first
   sentence, short lead, sections, `== منابع ==` + `{{پانویس}}`, categories.
4. **Tone:** encyclopedic and neutral. No value words without attribution («بزرگ‌ترین»،
   «برجسته»، «بی‌نظیر» only if a cited source says it and the text says who). No honorifics
   (حضرت، مرحوم، شادروان…). For living people, contentious claims need strong sources or go.
5. Save as `draft.wikitext`, then run the check loop in SKILL.md.

## Translate from en.wiki
1. Notability still applies; an en.wiki article is not proof for fa.wiki.
2. Rewrite in natural Persian; do not calque English syntax.
3. Convert templates and parameters (`{{cite web}}`→`{{یادکرد وب}}`, `{{Reflist}}`→
   `{{پانویس}}`, `[[Category:]]`→`[[رده:]]`, infobox → its fa template; table in
   `citations.md` §English→Persian). Keep source titles in their language with
   `کد زبان`/`زبان`.
4. Link only to fa.wiki titles you are sure exist; list the rest for the user. Never
   invent category names; propose and flag them. No `[[en:…]]` links (Wikidata does that).
5. Deliver the edit summary and the talk-page template from `translation.md` §6. Worked
   example: `examples/translation-before-after.md`.

## Review a draft
1. Save the text to a file; run `F scan FILE` (plan only, writes nothing).
2. Report three groups: **orthography** (fa_lint ids), **structure** (WCxx codes),
   **content** (your reading: unsourced claims, peacock or weasel words, NPOV, BLP,
   notability, missing lead or categories), citing the reference file for each content point.
3. `F apply FILE` (or `--only 1-5` if the user wants a subset), fix structure and content
   by hand, then `F report FILE` until it shows 0 changes and 0 errors.

## Build a citation
```bash
F cite "https://example.com/article"            # fetches page metadata
F cite "10.1000/xyz" --ref --name smith2020     # Crossref
F cite "978-964-..." --offline                  # no network: skeleton
F cite URL --offline --set title="…" --set date=2024-05-01
```
Use `--offline` when there is no internet. TODO fields must come from the source itself
(ask the user or open the page). An ISBN that fails the checksum is rejected; never repair it.

## Build an infobox
```bash
F infobox --list
F infobox --template film --skeleton
F infobox data.yaml            # keys: Persian names or English aliases
```
Most parameter names are [LOW] confidence (the script prints a NOTE): tell the user to
compare them with the template's documentation page.

## Explain a deletion
Use `notability-deletion.md` §8: map the symptoms (own sources only, advertising tone,
copied text, untranslated text, AI text, no claim of importance…) to the likely criterion
(ع۱۱، ع۱۲، ع۱۵، م۲، م۷…), link the fa.wiki page, and give the honest next steps from §9
(ask the deleting admin, find independent coverage, disclose conflicts of interest per
«ویکی‌پدیا:تعارض منافع»). Never promise restoration.
