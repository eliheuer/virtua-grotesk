# Arabic Visual Risk Audit

This generated report catches mechanical visual risks before human
Arabic proof review. It is not a substitute for native-reader review
or hand inspection in Runebender; it only flags cases such as blank
visible glyphs, `.notdef` mappings, suspicious advances, extreme
bounds, and large negative sidebearings.

- Target glyphset: `GF_Arabic_Core` plus U+25CC dotted circle
- Fonts checked: 5
- Codepoints checked per font: 224
- Risk rows: 46

## Risk Counts

| Risk | Rows |
| --- | ---: |
| `below-descender-margin` | 26 |
| `large-negative-left-sidebearing` | 20 |

## Risk Rows

| Font | Codepoint | Character | Name | Glyph | Advance | Bounds | Risks |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 0, 548, 1024 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+062C | ج | ARABIC LETTER JEEM | `uni062C` | 600 | 64, -376, 576, 448 | `below-descender-margin` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+062D | ح | ARABIC LETTER HAH | `uni062D` | 600 | 64, -376, 576, 448 | `below-descender-margin` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+062E | خ | ARABIC LETTER KHAH | `uni062E` | 600 | 64, -376, 576, 848 | `below-descender-margin` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0639 | ع | ARABIC LETTER AIN | `uni0639` | 600 | 22, -376, 554, 554 | `below-descender-margin` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+063A | غ | ARABIC LETTER GHAIN | `uni063A` | 600 | 22, -376, 554, 848 | `below-descender-margin` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, 0, 548, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+062C | ج | ARABIC LETTER JEEM | `uni062C` | 600 | 64, -376, 576, 448 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+062D | ح | ARABIC LETTER HAH | `uni062D` | 600 | 64, -376, 576, 448 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+062E | خ | ARABIC LETTER KHAH | `uni062E` | 600 | 64, -376, 576, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0639 | ع | ARABIC LETTER AIN | `uni0639` | 600 | 22, -376, 554, 554 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+063A | غ | ARABIC LETTER GHAIN | `uni063A` | 600 | 22, -376, 554, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, -4, 559, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+062C | ج | ARABIC LETTER JEEM | `uni062C` | 600 | 51, -392, 575, 494 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+062D | ح | ARABIC LETTER HAH | `uni062D` | 600 | 51, -392, 575, 494 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+062E | خ | ARABIC LETTER KHAH | `uni062E` | 600 | 51, -392, 575, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0639 | ع | ARABIC LETTER AIN | `uni0639` | 600 | 21, -397, 563, 587 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+063A | غ | ARABIC LETTER GHAIN | `uni063A` | 600 | 21, -397, 563, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, -8, 569, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+062C | ج | ARABIC LETTER JEEM | `uni062C` | 600 | 37, -408, 573, 540 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+062D | ح | ARABIC LETTER HAH | `uni062D` | 600 | 37, -408, 573, 540 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+062E | خ | ARABIC LETTER KHAH | `uni062E` | 600 | 37, -408, 573, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0639 | ع | ARABIC LETTER AIN | `uni0639` | 600 | 21, -417, 571, 619 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+063A | غ | ARABIC LETTER GHAIN | `uni063A` | 600 | 21, -417, 571, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+062B | ث | ARABIC LETTER THEH | `uni062B` | 600 | -224, -12, 580, 1024 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+062C | ج | ARABIC LETTER JEEM | `uni062C` | 600 | 24, -424, 572, 586 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+062D | ح | ARABIC LETTER HAH | `uni062D` | 600 | 24, -424, 572, 586 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+062E | خ | ARABIC LETTER KHAH | `uni062E` | 600 | 24, -424, 572, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0633 | س | ARABIC LETTER SEEN | `uni0633` | 864 | -368, -296, 768, 432 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0634 | ش | ARABIC LETTER SHEEN | `uni0634` | 864 | -368, -296, 768, 880 | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0639 | ع | ARABIC LETTER AIN | `uni0639` | 600 | 20, -438, 580, 652 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+063A | غ | ARABIC LETTER GHAIN | `uni063A` | 600 | 20, -438, 580, 848 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0645 | م | ARABIC LETTER MEEM | `uni0645` | 600 | 54, -376, 576, 548 | `below-descender-margin` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | U+0648 | و | ARABIC LETTER WAW | `uni0648` | 570 | -128, -256, 538, 408 | `large-negative-left-sidebearing` |

## Review Notes

- `blank-visible-glyph` and `maps-to-notdef` are likely source/build bugs.
- `nonmark-zero-advance` is a spacing risk for letters, numbers, or punctuation.
- Vertical-bound and sidebearing rows are review prompts, not automatic failures.
- If this report is clean, continue with `documentation/glyph-review/arabic-visual-review-log.md`
  and the GF proof HTML; it does not prove the drawings are culturally or
  stylistically correct.
