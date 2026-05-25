# Arabic Mark Readiness

This report tracks the non-drawing setup needed for Arabic combining marks in the Google Fonts submission. It complements the Arabic Core codepoint report and the shaping smoke test; it does not replace visual proofing or language review.

## Summary

- Minimum Arabic target: `GF_Arabic_Core`
- Required Arabic combining marks in `GF_Arabic_Core`: 16
- Present in current variable-font cmap: 13
- Missing from current variable-font cmap: 3
- U+25CC dotted circle present: no
- Source anchors present: no
- Built mark/mkmk GPOS features present: no

## Built Layout Tables

| Font | GDEF marks | GDEF mark count | GPOS present | GPOS features | mark/mkmk present |
| --- | --- | ---: | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | 14 | yes | `kern` | no |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | 14 | no | `none` | no |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | 14 | no | `none` | no |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | 14 | no | `none` | no |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | 14 | no | `none` | no |

## Source Anchors

| UFO | Glyphs with anchors | Required Arabic mark glyphs with anchors | Required mark glyph names |
| --- | ---: | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | 0 | 0 | `none` |
| `sources/VirtuaGrotesk-Bold.ufo` | 0 | 0 | `none` |

## Required Arabic Marks

| Codepoint | Character | Unicode name | Glyph | Present | Source anchors |
| --- | --- | --- | --- | --- | --- |
| U+0615 |  | ARABIC SMALL HIGH TAH | `.notdef` | no | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+064B |  | ARABIC FATHATAN | `uni064B` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+064C |  | ARABIC DAMMATAN | `uni064C` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+064D |  | ARABIC KASRATAN | `uni064D` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+064E |  | ARABIC FATHA | `uni064E` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+064F |  | ARABIC DAMMA | `uni064F` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0650 |  | ARABIC KASRA | `uni0650` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0651 |  | ARABIC SHADDA | `uni0651` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0652 |  | ARABIC SUKUN | `uni0652` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0653 |  | ARABIC MADDAH ABOVE | `uni0653` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0654 |  | ARABIC HAMZA ABOVE | `uni0654` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0655 |  | ARABIC HAMZA BELOW | `uni0655` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0656 |  | ARABIC SUBSCRIPT ALEF | `uni0656` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0658 |  | ARABIC MARK NOON GHUNNA | `.notdef` | no | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+0670 |  | ARABIC LETTER SUPERSCRIPT ALEF | `uni0670` | yes | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
| U+06DB |  | ARABIC SMALL HIGH THREE DOTS | `.notdef` | no | VirtuaGrotesk-Regular.ufo: none<br>VirtuaGrotesk-Bold.ufo: none |
