# Fontspector Contour Count Findings

Fonts:

- `fonts/variable/VirtuaGrotesk[wght].ttf`
- `fonts/ttf/VirtuaGrotesk-Regular.ttf`
- `fonts/ttf/VirtuaGrotesk-Medium.ttf`
- `fonts/ttf/VirtuaGrotesk-SemiBold.ttf`
- `fonts/ttf/VirtuaGrotesk-Bold.ttf`

These are source/drawing issues reported by Fontspector's `contour_count` check.

## `fonts/ttf/VirtuaGrotesk-Medium.ttf`

### WARN: `contour-count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0628` | U+0628 | 1 | 0, 2, 68 |
| `uni0628.fina` | unencoded | 1 | 2, 3, 5 |
| `uni062E.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0632` | U+0632 | 1 | 2, 32 |
| `uni0636.fina` | unencoded | 1 | 3, 4, 5 |
| `uni0636.medi` | unencoded | 1 | 3, 4, 6 |
| `uni0636.init` | unencoded | 1 | 3, 5 |
| `uni0638.init` | unencoded | 1 | 3, 4, 5 |
| `uni0639` | U+0639 | 17 | 1, 2 |
| `uni063A.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0641.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0642.fina` | unencoded | 2 | 3, 4 |
| `uni0646.fina` | unencoded | 1 | 2, 3 |

### FAIL: `no-contour`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0621` | U+0621 | 0 | at least 1 |
| `uni0625.fina` | unencoded | 0 | at least 1 |
| `uni0622.fina` | unencoded | 0 | at least 1 |
| `uni0671` | U+0671 | 0 | at least 1 |
| `uni0671.fina` | unencoded | 0 | at least 1 |
| `uni066E` | U+066E | 0 | at least 1 |
| `uni066E.fina` | unencoded | 0 | at least 1 |
| `uni062C` | U+062C | 0 | at least 1 |
| `uni062C.fina` | unencoded | 0 | at least 1 |
| `uni062D` | U+062D | 0 | at least 1 |
| `uni062D.fina` | unencoded | 0 | at least 1 |
| `uni062D.medi` | unencoded | 0 | at least 1 |
| `uni0631` | U+0631 | 0 | at least 1 |
| `uni0633.medi` | unencoded | 0 | at least 1 |
| `uni0635` | U+0635 | 0 | at least 1 |
| `uni0635.fina` | unencoded | 0 | at least 1 |
| `uni0635.medi` | unencoded | 0 | at least 1 |
| `uni0635.init` | unencoded | 0 | at least 1 |
| `uni0637` | U+0637 | 0 | at least 1 |
| `uni0637.init` | unencoded | 0 | at least 1 |
| `uni0639.fina` | unencoded | 0 | at least 1 |
| `uni066F` | U+066F | 0 | at least 1 |
| `uni0643.medi` | unencoded | 0 | at least 1 |
| `uni0643.init` | unencoded | 0 | at least 1 |
| `uni0644` | U+0644 | 0 | at least 1 |
| `uni0645` | U+0645 | 0 | at least 1 |
| `uni0645.fina` | unencoded | 0 | at least 1 |
| `uni0645.medi` | unencoded | 0 | at least 1 |
| `uni0645.init` | unencoded | 0 | at least 1 |
| `uni06BA` | U+06BA | 0 | at least 1 |
| `uni06BA.fina` | unencoded | 0 | at least 1 |
| `uni0647` | U+0647 | 0 | at least 1 |
| `uni0647.init` | unencoded | 0 | at least 1 |
| `uni0648.fina` | unencoded | 0 | at least 1 |
| `uni0624.fina` | unencoded | 0 | at least 1 |
| `uni0649` | U+0649 | 0 | at least 1 |
| `uni0649.fina` | unencoded | 0 | at least 1 |
| `uni0626.fina` | unencoded | 0 | at least 1 |
| `uni0626.medi` | unencoded | 0 | at least 1 |
| `uni0626.init` | unencoded | 0 | at least 1 |
| `uni06440627` | unencoded | 0 | at least 1 |
| `uni06440623` | unencoded | 0 | at least 1 |
| `uni06440625` | unencoded | 0 | at least 1 |
| `uni06440622` | unencoded | 0 | at least 1 |
| `uni06440622.fina` | unencoded | 0 | at least 1 |
| `uni06440671` | unencoded | 0 | at least 1 |
| `uni06440671.fina` | unencoded | 0 | at least 1 |
| `uni066B` | U+066B | 0 | at least 1 |
| `uni066C` | U+066C | 0 | at least 1 |
| `uni0660` | U+0660 | 0 | at least 1 |
| `uni0661` | U+0661 | 0 | at least 1 |
| `uni0662` | U+0662 | 0 | at least 1 |
| `uni0663` | U+0663 | 0 | at least 1 |
| `uni0664` | U+0664 | 0 | at least 1 |
| `uni0665` | U+0665 | 0 | at least 1 |
| `uni0666` | U+0666 | 0 | at least 1 |
| `uni0667` | U+0667 | 0 | at least 1 |
| `uni0668` | U+0668 | 0 | at least 1 |
| `uni0669` | U+0669 | 0 | at least 1 |
| `uni060C` | U+060C | 0 | at least 1 |
| `uni061B` | U+061B | 0 | at least 1 |
| `uni061F` | U+061F | 0 | at least 1 |
| `ellipsis` | U+2026 | 0 | at least 1 |
| `exclamdown` | U+00A1 | 0 | at least 1 |
| `questiondown` | U+00BF | 0 | at least 1 |
| `periodcentered` | U+00B7 | 0 | at least 1 |
| `bullet` | U+2022 | 0 | at least 1 |
| `numbersign` | U+0023 | 0 | at least 1 |
| `backslash` | U+005C | 0 | at least 1 |
| `endash` | U+2013 | 0 | at least 1 |
| `underscore` | U+005F | 0 | at least 1 |
| `quotesinglbase` | U+201A | 0 | at least 1 |
| `quoteleft` | U+2018 | 0 | at least 1 |
| `quotedbl` | U+0022 | 0 | at least 1 |
| `twodotsverticalabovear` | unencoded | 0 | at least 1 |
| `twodotsverticalbelowar` | unencoded | 0 | at least 1 |
| `threedotsdownabovear` | unencoded | 0 | at least 1 |
| `threedotsdownbelowar` | unencoded | 0 | at least 1 |
| `threedotsdowncenterar` | unencoded | 0 | at least 1 |
| `threedotsupbelowar` | unencoded | 0 | at least 1 |
| `waslaar` | unencoded | 0 | at least 1 |
| `uni0670` | U+0670 | 0 | at least 1 |
| `uni0656` | U+0656 | 0 | at least 1 |
| `uni0654064F` | unencoded | 0 | at least 1 |
| `uni0654064C` | unencoded | 0 | at least 1 |
| `uni0654064E` | unencoded | 0 | at least 1 |
| `uni0654064B` | unencoded | 0 | at least 1 |
| `uni06540652` | unencoded | 0 | at least 1 |
| `uni06550650` | unencoded | 0 | at least 1 |
| `uni0655064D` | unencoded | 0 | at least 1 |
| `uni064B` | U+064B | 0 | at least 1 |
| `uni064D` | U+064D | 0 | at least 1 |
| `uni064E` | U+064E | 0 | at least 1 |
| `uni064F` | U+064F | 0 | at least 1 |
| `uni0650` | U+0650 | 0 | at least 1 |
| `uni0651` | U+0651 | 0 | at least 1 |
| `uni0651064B` | unencoded | 0 | at least 1 |
| `uni0651064D` | unencoded | 0 | at least 1 |
| `uni0651064E` | unencoded | 0 | at least 1 |
| `uni0651064F` | unencoded | 0 | at least 1 |
| `uni06510650` | unencoded | 0 | at least 1 |
| `uni06510670` | unencoded | 0 | at least 1 |
| `uni0652` | U+0652 | 0 | at least 1 |
| `uni0653` | U+0653 | 0 | at least 1 |

## `fonts/ttf/VirtuaGrotesk-Regular.ttf`

### WARN: `contour-count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0628` | U+0628 | 1 | 0, 2, 68 |
| `uni0628.fina` | unencoded | 1 | 2, 3, 5 |
| `uni062E.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0632` | U+0632 | 1 | 2, 32 |
| `uni0636.fina` | unencoded | 1 | 3, 4, 5 |
| `uni0636.medi` | unencoded | 1 | 3, 4, 6 |
| `uni0636.init` | unencoded | 1 | 3, 5 |
| `uni0638.init` | unencoded | 1 | 3, 4, 5 |
| `uni0639` | U+0639 | 17 | 1, 2 |
| `uni063A.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0641.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0642.fina` | unencoded | 2 | 3, 4 |
| `uni0646.fina` | unencoded | 1 | 2, 3 |

### FAIL: `no-contour`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0621` | U+0621 | 0 | at least 1 |
| `uni0625.fina` | unencoded | 0 | at least 1 |
| `uni0622.fina` | unencoded | 0 | at least 1 |
| `uni0671` | U+0671 | 0 | at least 1 |
| `uni0671.fina` | unencoded | 0 | at least 1 |
| `uni066E` | U+066E | 0 | at least 1 |
| `uni066E.fina` | unencoded | 0 | at least 1 |
| `uni062C` | U+062C | 0 | at least 1 |
| `uni062C.fina` | unencoded | 0 | at least 1 |
| `uni062D` | U+062D | 0 | at least 1 |
| `uni062D.fina` | unencoded | 0 | at least 1 |
| `uni062D.medi` | unencoded | 0 | at least 1 |
| `uni0631` | U+0631 | 0 | at least 1 |
| `uni0633.medi` | unencoded | 0 | at least 1 |
| `uni0635` | U+0635 | 0 | at least 1 |
| `uni0635.fina` | unencoded | 0 | at least 1 |
| `uni0635.medi` | unencoded | 0 | at least 1 |
| `uni0635.init` | unencoded | 0 | at least 1 |
| `uni0637` | U+0637 | 0 | at least 1 |
| `uni0637.init` | unencoded | 0 | at least 1 |
| `uni0639.fina` | unencoded | 0 | at least 1 |
| `uni066F` | U+066F | 0 | at least 1 |
| `uni0643.medi` | unencoded | 0 | at least 1 |
| `uni0643.init` | unencoded | 0 | at least 1 |
| `uni0644` | U+0644 | 0 | at least 1 |
| `uni0645` | U+0645 | 0 | at least 1 |
| `uni0645.fina` | unencoded | 0 | at least 1 |
| `uni0645.medi` | unencoded | 0 | at least 1 |
| `uni0645.init` | unencoded | 0 | at least 1 |
| `uni06BA` | U+06BA | 0 | at least 1 |
| `uni06BA.fina` | unencoded | 0 | at least 1 |
| `uni0647` | U+0647 | 0 | at least 1 |
| `uni0647.init` | unencoded | 0 | at least 1 |
| `uni0648.fina` | unencoded | 0 | at least 1 |
| `uni0624.fina` | unencoded | 0 | at least 1 |
| `uni0649` | U+0649 | 0 | at least 1 |
| `uni0649.fina` | unencoded | 0 | at least 1 |
| `uni0626.fina` | unencoded | 0 | at least 1 |
| `uni0626.medi` | unencoded | 0 | at least 1 |
| `uni0626.init` | unencoded | 0 | at least 1 |
| `uni06440627` | unencoded | 0 | at least 1 |
| `uni06440623` | unencoded | 0 | at least 1 |
| `uni06440625` | unencoded | 0 | at least 1 |
| `uni06440622` | unencoded | 0 | at least 1 |
| `uni06440622.fina` | unencoded | 0 | at least 1 |
| `uni06440671` | unencoded | 0 | at least 1 |
| `uni06440671.fina` | unencoded | 0 | at least 1 |
| `uni066B` | U+066B | 0 | at least 1 |
| `uni066C` | U+066C | 0 | at least 1 |
| `uni0660` | U+0660 | 0 | at least 1 |
| `uni0661` | U+0661 | 0 | at least 1 |
| `uni0662` | U+0662 | 0 | at least 1 |
| `uni0663` | U+0663 | 0 | at least 1 |
| `uni0664` | U+0664 | 0 | at least 1 |
| `uni0665` | U+0665 | 0 | at least 1 |
| `uni0666` | U+0666 | 0 | at least 1 |
| `uni0667` | U+0667 | 0 | at least 1 |
| `uni0668` | U+0668 | 0 | at least 1 |
| `uni0669` | U+0669 | 0 | at least 1 |
| `uni060C` | U+060C | 0 | at least 1 |
| `uni061B` | U+061B | 0 | at least 1 |
| `uni061F` | U+061F | 0 | at least 1 |
| `ellipsis` | U+2026 | 0 | at least 1 |
| `exclamdown` | U+00A1 | 0 | at least 1 |
| `questiondown` | U+00BF | 0 | at least 1 |
| `periodcentered` | U+00B7 | 0 | at least 1 |
| `bullet` | U+2022 | 0 | at least 1 |
| `numbersign` | U+0023 | 0 | at least 1 |
| `backslash` | U+005C | 0 | at least 1 |
| `endash` | U+2013 | 0 | at least 1 |
| `underscore` | U+005F | 0 | at least 1 |
| `quotesinglbase` | U+201A | 0 | at least 1 |
| `quoteleft` | U+2018 | 0 | at least 1 |
| `quotedbl` | U+0022 | 0 | at least 1 |
| `twodotsverticalabovear` | unencoded | 0 | at least 1 |
| `twodotsverticalbelowar` | unencoded | 0 | at least 1 |
| `threedotsdownabovear` | unencoded | 0 | at least 1 |
| `threedotsdownbelowar` | unencoded | 0 | at least 1 |
| `threedotsdowncenterar` | unencoded | 0 | at least 1 |
| `threedotsupbelowar` | unencoded | 0 | at least 1 |
| `waslaar` | unencoded | 0 | at least 1 |
| `uni0670` | U+0670 | 0 | at least 1 |
| `uni0656` | U+0656 | 0 | at least 1 |
| `uni0654064F` | unencoded | 0 | at least 1 |
| `uni0654064C` | unencoded | 0 | at least 1 |
| `uni0654064E` | unencoded | 0 | at least 1 |
| `uni0654064B` | unencoded | 0 | at least 1 |
| `uni06540652` | unencoded | 0 | at least 1 |
| `uni06550650` | unencoded | 0 | at least 1 |
| `uni0655064D` | unencoded | 0 | at least 1 |
| `uni064B` | U+064B | 0 | at least 1 |
| `uni064D` | U+064D | 0 | at least 1 |
| `uni064E` | U+064E | 0 | at least 1 |
| `uni064F` | U+064F | 0 | at least 1 |
| `uni0650` | U+0650 | 0 | at least 1 |
| `uni0651` | U+0651 | 0 | at least 1 |
| `uni0651064B` | unencoded | 0 | at least 1 |
| `uni0651064D` | unencoded | 0 | at least 1 |
| `uni0651064E` | unencoded | 0 | at least 1 |
| `uni0651064F` | unencoded | 0 | at least 1 |
| `uni06510650` | unencoded | 0 | at least 1 |
| `uni06510670` | unencoded | 0 | at least 1 |
| `uni0652` | U+0652 | 0 | at least 1 |
| `uni0653` | U+0653 | 0 | at least 1 |

## `fonts/ttf/VirtuaGrotesk-SemiBold.ttf`

### WARN: `contour-count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0628` | U+0628 | 1 | 0, 2, 68 |
| `uni0628.fina` | unencoded | 1 | 2, 3, 5 |
| `uni062E.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0632` | U+0632 | 1 | 2, 32 |
| `uni0636.fina` | unencoded | 1 | 3, 4, 5 |
| `uni0636.medi` | unencoded | 1 | 3, 4, 6 |
| `uni0636.init` | unencoded | 1 | 3, 5 |
| `uni0638.init` | unencoded | 1 | 3, 4, 5 |
| `uni0639` | U+0639 | 17 | 1, 2 |
| `uni063A.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0641.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0642.fina` | unencoded | 2 | 3, 4 |
| `uni0646.fina` | unencoded | 1 | 2, 3 |

### FAIL: `no-contour`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0621` | U+0621 | 0 | at least 1 |
| `uni0625.fina` | unencoded | 0 | at least 1 |
| `uni0622.fina` | unencoded | 0 | at least 1 |
| `uni0671` | U+0671 | 0 | at least 1 |
| `uni0671.fina` | unencoded | 0 | at least 1 |
| `uni066E` | U+066E | 0 | at least 1 |
| `uni066E.fina` | unencoded | 0 | at least 1 |
| `uni062C` | U+062C | 0 | at least 1 |
| `uni062C.fina` | unencoded | 0 | at least 1 |
| `uni062D` | U+062D | 0 | at least 1 |
| `uni062D.fina` | unencoded | 0 | at least 1 |
| `uni062D.medi` | unencoded | 0 | at least 1 |
| `uni0631` | U+0631 | 0 | at least 1 |
| `uni0633.medi` | unencoded | 0 | at least 1 |
| `uni0635` | U+0635 | 0 | at least 1 |
| `uni0635.fina` | unencoded | 0 | at least 1 |
| `uni0635.medi` | unencoded | 0 | at least 1 |
| `uni0635.init` | unencoded | 0 | at least 1 |
| `uni0637` | U+0637 | 0 | at least 1 |
| `uni0637.init` | unencoded | 0 | at least 1 |
| `uni0639.fina` | unencoded | 0 | at least 1 |
| `uni066F` | U+066F | 0 | at least 1 |
| `uni0643.medi` | unencoded | 0 | at least 1 |
| `uni0643.init` | unencoded | 0 | at least 1 |
| `uni0644` | U+0644 | 0 | at least 1 |
| `uni0645` | U+0645 | 0 | at least 1 |
| `uni0645.fina` | unencoded | 0 | at least 1 |
| `uni0645.medi` | unencoded | 0 | at least 1 |
| `uni0645.init` | unencoded | 0 | at least 1 |
| `uni06BA` | U+06BA | 0 | at least 1 |
| `uni06BA.fina` | unencoded | 0 | at least 1 |
| `uni0647` | U+0647 | 0 | at least 1 |
| `uni0647.init` | unencoded | 0 | at least 1 |
| `uni0648.fina` | unencoded | 0 | at least 1 |
| `uni0624.fina` | unencoded | 0 | at least 1 |
| `uni0649` | U+0649 | 0 | at least 1 |
| `uni0649.fina` | unencoded | 0 | at least 1 |
| `uni0626.fina` | unencoded | 0 | at least 1 |
| `uni0626.medi` | unencoded | 0 | at least 1 |
| `uni0626.init` | unencoded | 0 | at least 1 |
| `uni06440627` | unencoded | 0 | at least 1 |
| `uni06440623` | unencoded | 0 | at least 1 |
| `uni06440625` | unencoded | 0 | at least 1 |
| `uni06440622` | unencoded | 0 | at least 1 |
| `uni06440622.fina` | unencoded | 0 | at least 1 |
| `uni06440671` | unencoded | 0 | at least 1 |
| `uni06440671.fina` | unencoded | 0 | at least 1 |
| `uni066B` | U+066B | 0 | at least 1 |
| `uni066C` | U+066C | 0 | at least 1 |
| `uni0660` | U+0660 | 0 | at least 1 |
| `uni0661` | U+0661 | 0 | at least 1 |
| `uni0662` | U+0662 | 0 | at least 1 |
| `uni0663` | U+0663 | 0 | at least 1 |
| `uni0664` | U+0664 | 0 | at least 1 |
| `uni0665` | U+0665 | 0 | at least 1 |
| `uni0666` | U+0666 | 0 | at least 1 |
| `uni0667` | U+0667 | 0 | at least 1 |
| `uni0668` | U+0668 | 0 | at least 1 |
| `uni0669` | U+0669 | 0 | at least 1 |
| `uni060C` | U+060C | 0 | at least 1 |
| `uni061B` | U+061B | 0 | at least 1 |
| `uni061F` | U+061F | 0 | at least 1 |
| `ellipsis` | U+2026 | 0 | at least 1 |
| `exclamdown` | U+00A1 | 0 | at least 1 |
| `questiondown` | U+00BF | 0 | at least 1 |
| `periodcentered` | U+00B7 | 0 | at least 1 |
| `bullet` | U+2022 | 0 | at least 1 |
| `numbersign` | U+0023 | 0 | at least 1 |
| `backslash` | U+005C | 0 | at least 1 |
| `endash` | U+2013 | 0 | at least 1 |
| `underscore` | U+005F | 0 | at least 1 |
| `quotesinglbase` | U+201A | 0 | at least 1 |
| `quoteleft` | U+2018 | 0 | at least 1 |
| `quotedbl` | U+0022 | 0 | at least 1 |
| `twodotsverticalabovear` | unencoded | 0 | at least 1 |
| `twodotsverticalbelowar` | unencoded | 0 | at least 1 |
| `threedotsdownabovear` | unencoded | 0 | at least 1 |
| `threedotsdownbelowar` | unencoded | 0 | at least 1 |
| `threedotsdowncenterar` | unencoded | 0 | at least 1 |
| `threedotsupbelowar` | unencoded | 0 | at least 1 |
| `waslaar` | unencoded | 0 | at least 1 |
| `uni0670` | U+0670 | 0 | at least 1 |
| `uni0656` | U+0656 | 0 | at least 1 |
| `uni0654064F` | unencoded | 0 | at least 1 |
| `uni0654064C` | unencoded | 0 | at least 1 |
| `uni0654064E` | unencoded | 0 | at least 1 |
| `uni0654064B` | unencoded | 0 | at least 1 |
| `uni06540652` | unencoded | 0 | at least 1 |
| `uni06550650` | unencoded | 0 | at least 1 |
| `uni0655064D` | unencoded | 0 | at least 1 |
| `uni064B` | U+064B | 0 | at least 1 |
| `uni064D` | U+064D | 0 | at least 1 |
| `uni064E` | U+064E | 0 | at least 1 |
| `uni064F` | U+064F | 0 | at least 1 |
| `uni0650` | U+0650 | 0 | at least 1 |
| `uni0651` | U+0651 | 0 | at least 1 |
| `uni0651064B` | unencoded | 0 | at least 1 |
| `uni0651064D` | unencoded | 0 | at least 1 |
| `uni0651064E` | unencoded | 0 | at least 1 |
| `uni0651064F` | unencoded | 0 | at least 1 |
| `uni06510650` | unencoded | 0 | at least 1 |
| `uni06510670` | unencoded | 0 | at least 1 |
| `uni0652` | U+0652 | 0 | at least 1 |
| `uni0653` | U+0653 | 0 | at least 1 |

## `fonts/variable/VirtuaGrotesk[wght].ttf`

### WARN: `contour-count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0628` | U+0628 | 1 | 0, 2, 68 |
| `uni0628.fina` | unencoded | 1 | 2, 3, 5 |
| `uni062E.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0632` | U+0632 | 1 | 2, 32 |
| `uni0636.fina` | unencoded | 1 | 3, 4, 5 |
| `uni0636.medi` | unencoded | 1 | 3, 4, 6 |
| `uni0636.init` | unencoded | 1 | 3, 5 |
| `uni0638.init` | unencoded | 1 | 3, 4, 5 |
| `uni0639` | U+0639 | 17 | 1, 2 |
| `uni063A.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0641.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0642.fina` | unencoded | 2 | 3, 4 |
| `uni0646.fina` | unencoded | 1 | 2, 3 |

### FAIL: `no-contour`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0621` | U+0621 | 0 | at least 1 |
| `uni0625.fina` | unencoded | 0 | at least 1 |
| `uni0622.fina` | unencoded | 0 | at least 1 |
| `uni0671` | U+0671 | 0 | at least 1 |
| `uni0671.fina` | unencoded | 0 | at least 1 |
| `uni066E` | U+066E | 0 | at least 1 |
| `uni066E.fina` | unencoded | 0 | at least 1 |
| `uni062C` | U+062C | 0 | at least 1 |
| `uni062C.fina` | unencoded | 0 | at least 1 |
| `uni062D` | U+062D | 0 | at least 1 |
| `uni062D.fina` | unencoded | 0 | at least 1 |
| `uni062D.medi` | unencoded | 0 | at least 1 |
| `uni0631` | U+0631 | 0 | at least 1 |
| `uni0633.medi` | unencoded | 0 | at least 1 |
| `uni0635` | U+0635 | 0 | at least 1 |
| `uni0635.fina` | unencoded | 0 | at least 1 |
| `uni0635.medi` | unencoded | 0 | at least 1 |
| `uni0635.init` | unencoded | 0 | at least 1 |
| `uni0637` | U+0637 | 0 | at least 1 |
| `uni0637.init` | unencoded | 0 | at least 1 |
| `uni0639.fina` | unencoded | 0 | at least 1 |
| `uni066F` | U+066F | 0 | at least 1 |
| `uni0643.medi` | unencoded | 0 | at least 1 |
| `uni0643.init` | unencoded | 0 | at least 1 |
| `uni0644` | U+0644 | 0 | at least 1 |
| `uni0645` | U+0645 | 0 | at least 1 |
| `uni0645.fina` | unencoded | 0 | at least 1 |
| `uni0645.medi` | unencoded | 0 | at least 1 |
| `uni0645.init` | unencoded | 0 | at least 1 |
| `uni06BA` | U+06BA | 0 | at least 1 |
| `uni06BA.fina` | unencoded | 0 | at least 1 |
| `uni0647` | U+0647 | 0 | at least 1 |
| `uni0647.init` | unencoded | 0 | at least 1 |
| `uni0648.fina` | unencoded | 0 | at least 1 |
| `uni0624.fina` | unencoded | 0 | at least 1 |
| `uni0649` | U+0649 | 0 | at least 1 |
| `uni0649.fina` | unencoded | 0 | at least 1 |
| `uni0626.fina` | unencoded | 0 | at least 1 |
| `uni0626.medi` | unencoded | 0 | at least 1 |
| `uni0626.init` | unencoded | 0 | at least 1 |
| `uni06440627` | unencoded | 0 | at least 1 |
| `uni06440623` | unencoded | 0 | at least 1 |
| `uni06440625` | unencoded | 0 | at least 1 |
| `uni06440622` | unencoded | 0 | at least 1 |
| `uni06440622.fina` | unencoded | 0 | at least 1 |
| `uni06440671` | unencoded | 0 | at least 1 |
| `uni06440671.fina` | unencoded | 0 | at least 1 |
| `uni066B` | U+066B | 0 | at least 1 |
| `uni066C` | U+066C | 0 | at least 1 |
| `uni0660` | U+0660 | 0 | at least 1 |
| `uni0661` | U+0661 | 0 | at least 1 |
| `uni0662` | U+0662 | 0 | at least 1 |
| `uni0663` | U+0663 | 0 | at least 1 |
| `uni0664` | U+0664 | 0 | at least 1 |
| `uni0665` | U+0665 | 0 | at least 1 |
| `uni0666` | U+0666 | 0 | at least 1 |
| `uni0667` | U+0667 | 0 | at least 1 |
| `uni0668` | U+0668 | 0 | at least 1 |
| `uni0669` | U+0669 | 0 | at least 1 |
| `uni060C` | U+060C | 0 | at least 1 |
| `uni061B` | U+061B | 0 | at least 1 |
| `uni061F` | U+061F | 0 | at least 1 |
| `ellipsis` | U+2026 | 0 | at least 1 |
| `exclamdown` | U+00A1 | 0 | at least 1 |
| `questiondown` | U+00BF | 0 | at least 1 |
| `periodcentered` | U+00B7 | 0 | at least 1 |
| `bullet` | U+2022 | 0 | at least 1 |
| `numbersign` | U+0023 | 0 | at least 1 |
| `backslash` | U+005C | 0 | at least 1 |
| `endash` | U+2013 | 0 | at least 1 |
| `underscore` | U+005F | 0 | at least 1 |
| `quotesinglbase` | U+201A | 0 | at least 1 |
| `quoteleft` | U+2018 | 0 | at least 1 |
| `quotedbl` | U+0022 | 0 | at least 1 |
| `twodotsverticalabovear` | unencoded | 0 | at least 1 |
| `twodotsverticalbelowar` | unencoded | 0 | at least 1 |
| `threedotsdownabovear` | unencoded | 0 | at least 1 |
| `threedotsdownbelowar` | unencoded | 0 | at least 1 |
| `threedotsdowncenterar` | unencoded | 0 | at least 1 |
| `threedotsupbelowar` | unencoded | 0 | at least 1 |
| `waslaar` | unencoded | 0 | at least 1 |
| `uni0670` | U+0670 | 0 | at least 1 |
| `uni0656` | U+0656 | 0 | at least 1 |
| `uni0654064F` | unencoded | 0 | at least 1 |
| `uni0654064C` | unencoded | 0 | at least 1 |
| `uni0654064E` | unencoded | 0 | at least 1 |
| `uni0654064B` | unencoded | 0 | at least 1 |
| `uni06540652` | unencoded | 0 | at least 1 |
| `uni06550650` | unencoded | 0 | at least 1 |
| `uni0655064D` | unencoded | 0 | at least 1 |
| `uni064B` | U+064B | 0 | at least 1 |
| `uni064D` | U+064D | 0 | at least 1 |
| `uni064E` | U+064E | 0 | at least 1 |
| `uni064F` | U+064F | 0 | at least 1 |
| `uni0650` | U+0650 | 0 | at least 1 |
| `uni0651` | U+0651 | 0 | at least 1 |
| `uni0651064B` | unencoded | 0 | at least 1 |
| `uni0651064D` | unencoded | 0 | at least 1 |
| `uni0651064E` | unencoded | 0 | at least 1 |
| `uni0651064F` | unencoded | 0 | at least 1 |
| `uni06510650` | unencoded | 0 | at least 1 |
| `uni06510670` | unencoded | 0 | at least 1 |
| `uni0652` | U+0652 | 0 | at least 1 |
| `uni0653` | U+0653 | 0 | at least 1 |

## `fonts/ttf/VirtuaGrotesk-Bold.ttf`

### WARN: `contour-count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0628` | U+0628 | 1 | 0, 2, 68 |
| `uni0628.fina` | unencoded | 1 | 2, 3, 5 |
| `uni062E.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0632` | U+0632 | 1 | 2, 32 |
| `uni0636.fina` | unencoded | 1 | 3, 4, 5 |
| `uni0636.medi` | unencoded | 1 | 3, 4, 6 |
| `uni0636.init` | unencoded | 1 | 3, 5 |
| `uni0638.init` | unencoded | 1 | 3, 4, 5 |
| `uni0639` | U+0639 | 17 | 1, 2 |
| `uni063A.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0641.fina` | unencoded | 1 | 2, 3, 4 |
| `uni0642.fina` | unencoded | 2 | 3, 4 |
| `uni0646.fina` | unencoded | 1 | 2, 3 |

### FAIL: `no-contour`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0621` | U+0621 | 0 | at least 1 |
| `uni0625.fina` | unencoded | 0 | at least 1 |
| `uni0622.fina` | unencoded | 0 | at least 1 |
| `uni0671` | U+0671 | 0 | at least 1 |
| `uni0671.fina` | unencoded | 0 | at least 1 |
| `uni066E` | U+066E | 0 | at least 1 |
| `uni066E.fina` | unencoded | 0 | at least 1 |
| `uni062C` | U+062C | 0 | at least 1 |
| `uni062C.fina` | unencoded | 0 | at least 1 |
| `uni062D` | U+062D | 0 | at least 1 |
| `uni062D.fina` | unencoded | 0 | at least 1 |
| `uni062D.medi` | unencoded | 0 | at least 1 |
| `uni0631` | U+0631 | 0 | at least 1 |
| `uni0633.medi` | unencoded | 0 | at least 1 |
| `uni0635` | U+0635 | 0 | at least 1 |
| `uni0635.fina` | unencoded | 0 | at least 1 |
| `uni0635.medi` | unencoded | 0 | at least 1 |
| `uni0635.init` | unencoded | 0 | at least 1 |
| `uni0637` | U+0637 | 0 | at least 1 |
| `uni0637.init` | unencoded | 0 | at least 1 |
| `uni0639.fina` | unencoded | 0 | at least 1 |
| `uni066F` | U+066F | 0 | at least 1 |
| `uni0643.medi` | unencoded | 0 | at least 1 |
| `uni0643.init` | unencoded | 0 | at least 1 |
| `uni0644` | U+0644 | 0 | at least 1 |
| `uni0645` | U+0645 | 0 | at least 1 |
| `uni0645.fina` | unencoded | 0 | at least 1 |
| `uni0645.medi` | unencoded | 0 | at least 1 |
| `uni0645.init` | unencoded | 0 | at least 1 |
| `uni06BA` | U+06BA | 0 | at least 1 |
| `uni06BA.fina` | unencoded | 0 | at least 1 |
| `uni0647` | U+0647 | 0 | at least 1 |
| `uni0647.init` | unencoded | 0 | at least 1 |
| `uni0648.fina` | unencoded | 0 | at least 1 |
| `uni0624.fina` | unencoded | 0 | at least 1 |
| `uni0649` | U+0649 | 0 | at least 1 |
| `uni0649.fina` | unencoded | 0 | at least 1 |
| `uni0626.fina` | unencoded | 0 | at least 1 |
| `uni0626.medi` | unencoded | 0 | at least 1 |
| `uni0626.init` | unencoded | 0 | at least 1 |
| `uni06440627` | unencoded | 0 | at least 1 |
| `uni06440623` | unencoded | 0 | at least 1 |
| `uni06440625` | unencoded | 0 | at least 1 |
| `uni06440622` | unencoded | 0 | at least 1 |
| `uni06440622.fina` | unencoded | 0 | at least 1 |
| `uni06440671` | unencoded | 0 | at least 1 |
| `uni06440671.fina` | unencoded | 0 | at least 1 |
| `uni066B` | U+066B | 0 | at least 1 |
| `uni066C` | U+066C | 0 | at least 1 |
| `uni0660` | U+0660 | 0 | at least 1 |
| `uni0661` | U+0661 | 0 | at least 1 |
| `uni0662` | U+0662 | 0 | at least 1 |
| `uni0663` | U+0663 | 0 | at least 1 |
| `uni0664` | U+0664 | 0 | at least 1 |
| `uni0665` | U+0665 | 0 | at least 1 |
| `uni0666` | U+0666 | 0 | at least 1 |
| `uni0667` | U+0667 | 0 | at least 1 |
| `uni0668` | U+0668 | 0 | at least 1 |
| `uni0669` | U+0669 | 0 | at least 1 |
| `uni060C` | U+060C | 0 | at least 1 |
| `uni061B` | U+061B | 0 | at least 1 |
| `uni061F` | U+061F | 0 | at least 1 |
| `ellipsis` | U+2026 | 0 | at least 1 |
| `exclamdown` | U+00A1 | 0 | at least 1 |
| `questiondown` | U+00BF | 0 | at least 1 |
| `periodcentered` | U+00B7 | 0 | at least 1 |
| `bullet` | U+2022 | 0 | at least 1 |
| `numbersign` | U+0023 | 0 | at least 1 |
| `backslash` | U+005C | 0 | at least 1 |
| `endash` | U+2013 | 0 | at least 1 |
| `underscore` | U+005F | 0 | at least 1 |
| `quotesinglbase` | U+201A | 0 | at least 1 |
| `quoteleft` | U+2018 | 0 | at least 1 |
| `quotedbl` | U+0022 | 0 | at least 1 |
| `twodotsverticalabovear` | unencoded | 0 | at least 1 |
| `twodotsverticalbelowar` | unencoded | 0 | at least 1 |
| `threedotsdownabovear` | unencoded | 0 | at least 1 |
| `threedotsdownbelowar` | unencoded | 0 | at least 1 |
| `threedotsdowncenterar` | unencoded | 0 | at least 1 |
| `threedotsupbelowar` | unencoded | 0 | at least 1 |
| `waslaar` | unencoded | 0 | at least 1 |
| `uni0670` | U+0670 | 0 | at least 1 |
| `uni0656` | U+0656 | 0 | at least 1 |
| `uni0654064F` | unencoded | 0 | at least 1 |
| `uni0654064C` | unencoded | 0 | at least 1 |
| `uni0654064E` | unencoded | 0 | at least 1 |
| `uni0654064B` | unencoded | 0 | at least 1 |
| `uni06540652` | unencoded | 0 | at least 1 |
| `uni06550650` | unencoded | 0 | at least 1 |
| `uni0655064D` | unencoded | 0 | at least 1 |
| `uni064B` | U+064B | 0 | at least 1 |
| `uni064D` | U+064D | 0 | at least 1 |
| `uni064E` | U+064E | 0 | at least 1 |
| `uni064F` | U+064F | 0 | at least 1 |
| `uni0650` | U+0650 | 0 | at least 1 |
| `uni0651` | U+0651 | 0 | at least 1 |
| `uni0651064B` | unencoded | 0 | at least 1 |
| `uni0651064D` | unencoded | 0 | at least 1 |
| `uni0651064E` | unencoded | 0 | at least 1 |
| `uni0651064F` | unencoded | 0 | at least 1 |
| `uni06510650` | unencoded | 0 | at least 1 |
| `uni06510670` | unencoded | 0 | at least 1 |
| `uni0652` | U+0652 | 0 | at least 1 |
| `uni0653` | U+0653 | 0 | at least 1 |
