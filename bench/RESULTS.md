# Synthetic benchmark results

fawiki-editor 0.2.0 · Python 3.13.16 · Linux · mwparserfromhell: yes

**PASS: 28/28 checks**

| Metric | Value |
|---|---|
| Planted errors fixed | 16/16 |
| Traps left untouched | 36/36 |
| Lint time, ~0.5 MB | 0.65 s |

| Check | Result | Detail |
|---|---|---|
| biography: apply exit 0 | pass | exit 0 |
| biography: protected regions byte-identical | pass |  |
| biography: template/link inventory unchanged | pass |  |
| biography: idempotent | pass |  |
| biography: no structural errors after fix | pass |  |
| biography: undo byte-identical | pass |  |
| biography: no leftovers after undo | pass |  |
| city: apply exit 0 | pass | exit 0 |
| city: protected regions byte-identical | pass |  |
| city: template/link inventory unchanged | pass |  |
| city: idempotent | pass |  |
| city: no structural errors after fix | pass |  |
| city: undo byte-identical | pass |  |
| city: no leftovers after undo | pass |  |
| tech: apply exit 0 | pass | exit 0 |
| tech: protected regions byte-identical | pass |  |
| tech: template/link inventory unchanged | pass |  |
| tech: idempotent | pass |  |
| tech: warnings reported, not applied | pass | got ['FW01', 'FW02', 'FW03', 'FW06'] |
| tech: undo byte-identical | pass |  |
| tech: no leftovers after undo | pass |  |
| crlf: line endings kept | pass |  |
| crlf: undo byte-identical | pass |  |
| 3 articles: all planted fixes applied | pass | 16/16 |
| 3 articles: all traps untouched | pass | 36/36 |
| broken draft: planted structural errors found | pass | want ['WC01', 'WC03', 'WC05', 'WC06'] got ['WC01', 'WC03', 'WC05', 'WC06'] |
| cite --offline: no network | pass |  |
| speed: ~0.5 MB lints in under 20 s | pass | 0.13 MB in 0.65 s |
