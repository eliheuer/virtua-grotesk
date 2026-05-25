# Arabic Mark Readiness

This report tracks the non-drawing setup needed for Arabic combining marks in the Google Fonts submission. It complements the Arabic Core codepoint report and the shaping smoke test; it does not replace visual proofing or language review.

## Summary

- Minimum Arabic target: `GF_Arabic_Core`
- Required Arabic combining marks in `GF_Arabic_Core`: 16
- Present in current variable-font cmap: 16
- Missing from current variable-font cmap: 0
- U+25CC dotted circle present: yes
- Source anchors present: yes
- Built mark/mkmk GPOS features present: yes

## Built Layout Tables

| Font | GDEF marks | GDEF mark count | GPOS present | GPOS features | mark/mkmk present |
| --- | --- | ---: | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | 46 | yes | `kern, mark, mkmk` | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | 46 | yes | `kern, mark, mkmk` | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | 46 | yes | `kern, mark, mkmk` | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | 46 | yes | `kern, mark, mkmk` | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | 46 | yes | `kern, mark, mkmk` | yes |

## Source Anchors

| UFO | Glyphs with anchors | Required Arabic mark glyphs with anchors | Required mark glyph names |
| --- | ---: | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | 20 | 16 | `alefabove-ar, alefbelow-ar, damma-ar, dammatan-ar, fatha-ar, fathatan-ar, hamzaabove-ar, hamzabelow-ar, kasra-ar, kasratan-ar, madda-ar, noonGhunna-ar, shadda-ar, smallHighTah-ar, smallHighThreeDots-ar, sukun-ar` |
| `sources/VirtuaGrotesk-Bold.ufo` | 20 | 16 | `alefabove-ar, alefbelow-ar, damma-ar, dammatan-ar, fatha-ar, fathatan-ar, hamzaabove-ar, hamzabelow-ar, kasra-ar, kasratan-ar, madda-ar, noonGhunna-ar, shadda-ar, smallHighTah-ar, smallHighThreeDots-ar, sukun-ar` |

## Required Arabic Marks

| Codepoint | Character | Unicode name | Glyph | Present | Source anchors |
| --- | --- | --- | --- | --- | --- |
| U+0615 |  | ARABIC SMALL HIGH TAH | `smallHighTahar` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+064B |  | ARABIC FATHATAN | `uni064B` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+064C |  | ARABIC DAMMATAN | `uni064C` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+064D |  | ARABIC KASRATAN | `uni064D` | yes | VirtuaGrotesk-Regular.ufo: _bottom, bottom<br>VirtuaGrotesk-Bold.ufo: _bottom, bottom |
| U+064E |  | ARABIC FATHA | `uni064E` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+064F |  | ARABIC DAMMA | `uni064F` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0650 |  | ARABIC KASRA | `uni0650` | yes | VirtuaGrotesk-Regular.ufo: _bottom, bottom<br>VirtuaGrotesk-Bold.ufo: _bottom, bottom |
| U+0651 |  | ARABIC SHADDA | `uni0651` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0652 |  | ARABIC SUKUN | `uni0652` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0653 |  | ARABIC MADDAH ABOVE | `uni0653` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0654 |  | ARABIC HAMZA ABOVE | `uni0654` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0655 |  | ARABIC HAMZA BELOW | `uni0655` | yes | VirtuaGrotesk-Regular.ufo: _bottom, bottom<br>VirtuaGrotesk-Bold.ufo: _bottom, bottom |
| U+0656 |  | ARABIC SUBSCRIPT ALEF | `uni0656` | yes | VirtuaGrotesk-Regular.ufo: _bottom, bottom<br>VirtuaGrotesk-Bold.ufo: _bottom, bottom |
| U+0658 |  | ARABIC MARK NOON GHUNNA | `noonGhunnaar` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+0670 |  | ARABIC LETTER SUPERSCRIPT ALEF | `uni0670` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
| U+06DB |  | ARABIC SMALL HIGH THREE DOTS | `smallHighThreeDotsar` | yes | VirtuaGrotesk-Regular.ufo: _top, top<br>VirtuaGrotesk-Bold.ufo: _top, top |
