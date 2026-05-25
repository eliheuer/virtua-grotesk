# Arabic Visual Risk Audit

This generated report catches mechanical visual risks before human
Arabic proof review. It is not a substitute for native-reader review
or hand inspection in Runebender; it only flags cases such as blank
visible glyphs, `.notdef` mappings, suspicious advances, extreme
bounds, and large negative sidebearings.

- Target glyphset: `GF_Arabic_Core` plus U+25CC dotted circle
- Fonts checked: 5
- Codepoints checked per font: 224
- Risk rows: 20

## Risk Counts

| Risk | Rows |
| --- | ---: |
| `large-negative-left-sidebearing` | 20 |

## Risk Rows

| Font | Codepoint | Character | Name | Glyph | Advance | Bounds | Risks |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 112, 536, 1024 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 112, 536, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 112, 536, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 112, 536, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 112, 536, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |

## Review Notes

- `blank-visible-glyph` and `maps-to-notdef` are likely source/build bugs.
- `nonmark-zero-advance` is a spacing risk for letters, numbers, or punctuation.
- Vertical-bound and sidebearing rows are review prompts, not automatic failures.
- If this report is clean, continue with `documentation/arabic-visual-review-log.md`
  and the GF proof HTML; it does not prove the drawings are culturally or
  stylistically correct.
