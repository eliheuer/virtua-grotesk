# Arabic Shaping Smoke Test

This report smoke-tests Arabic layout plumbing in every generated Google Fonts handoff font: the variable font and all static TTFs. It proves the built fonts emit Arabic GSUB tables and that HarfBuzz reaches contextual forms or required ligatures for representative strings. It does not replace visual proofing or language review.

## fonts/variable/VirtuaGrotesk[wght].ttf

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`
Has GSUB: `true`
GSUB features: `aalt, ccmp, fina, init, medi, rlig, tnum`
GSUB script records: `DFLT: dflt, arab: dflt, latn: dflt`
GSUB has `arab/dflt`: `true`
GPOS script records: `DFLT: dflt, arab: dflt, latn: dflt`
GPOS has `arab/dflt`: `true`
HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`

| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `salaam` | سلام | `uni0645 uni06440627.fina uni0633.init` | 0 | yes | yes | yes | yes |
| `arabic` | العربية | `uni0629.fina uni064A.medi uni0628.init uni0631.fina uni0639.medi uni0644.init uni0627` | 0 | yes | yes | no | no |
| `bismillah` | بسم الله | `uni0647.fina uni0644.medi uni0644.init uni0627 space uni0645.fina uni0633.medi uni0628.init` | 0 | yes | yes | no | no |
| `lam_alef` | لا | `uni06440627` | 0 | no | no | yes | yes |

## fonts/ttf/VirtuaGrotesk-Regular.ttf

Font: `fonts/ttf/VirtuaGrotesk-Regular.ttf`
Has GSUB: `true`
GSUB features: `aalt, ccmp, fina, init, medi, rlig, tnum`
GSUB script records: `DFLT: dflt, arab: dflt, latn: dflt`
GSUB has `arab/dflt`: `true`
GPOS script records: `DFLT: dflt, arab: dflt, latn: dflt`
GPOS has `arab/dflt`: `true`
HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`

| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `salaam` | سلام | `uni0645 uni06440627.fina uni0633.init` | 0 | yes | yes | yes | yes |
| `arabic` | العربية | `uni0629.fina uni064A.medi uni0628.init uni0631.fina uni0639.medi uni0644.init uni0627` | 0 | yes | yes | no | no |
| `bismillah` | بسم الله | `uni0647.fina uni0644.medi uni0644.init uni0627 space uni0645.fina uni0633.medi uni0628.init` | 0 | yes | yes | no | no |
| `lam_alef` | لا | `uni06440627` | 0 | no | no | yes | yes |

## fonts/ttf/VirtuaGrotesk-Medium.ttf

Font: `fonts/ttf/VirtuaGrotesk-Medium.ttf`
Has GSUB: `true`
GSUB features: `aalt, ccmp, fina, init, medi, rlig, tnum`
GSUB script records: `DFLT: dflt, arab: dflt, latn: dflt`
GSUB has `arab/dflt`: `true`
GPOS script records: `DFLT: dflt, arab: dflt, latn: dflt`
GPOS has `arab/dflt`: `true`
HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`

| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `salaam` | سلام | `uni0645 uni06440627.fina uni0633.init` | 0 | yes | yes | yes | yes |
| `arabic` | العربية | `uni0629.fina uni064A.medi uni0628.init uni0631.fina uni0639.medi uni0644.init uni0627` | 0 | yes | yes | no | no |
| `bismillah` | بسم الله | `uni0647.fina uni0644.medi uni0644.init uni0627 space uni0645.fina uni0633.medi uni0628.init` | 0 | yes | yes | no | no |
| `lam_alef` | لا | `uni06440627` | 0 | no | no | yes | yes |

## fonts/ttf/VirtuaGrotesk-SemiBold.ttf

Font: `fonts/ttf/VirtuaGrotesk-SemiBold.ttf`
Has GSUB: `true`
GSUB features: `aalt, ccmp, fina, init, medi, rlig, tnum`
GSUB script records: `DFLT: dflt, arab: dflt, latn: dflt`
GSUB has `arab/dflt`: `true`
GPOS script records: `DFLT: dflt, arab: dflt, latn: dflt`
GPOS has `arab/dflt`: `true`
HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`

| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `salaam` | سلام | `uni0645 uni06440627.fina uni0633.init` | 0 | yes | yes | yes | yes |
| `arabic` | العربية | `uni0629.fina uni064A.medi uni0628.init uni0631.fina uni0639.medi uni0644.init uni0627` | 0 | yes | yes | no | no |
| `bismillah` | بسم الله | `uni0647.fina uni0644.medi uni0644.init uni0627 space uni0645.fina uni0633.medi uni0628.init` | 0 | yes | yes | no | no |
| `lam_alef` | لا | `uni06440627` | 0 | no | no | yes | yes |

## fonts/ttf/VirtuaGrotesk-Bold.ttf

Font: `fonts/ttf/VirtuaGrotesk-Bold.ttf`
Has GSUB: `true`
GSUB features: `aalt, ccmp, fina, init, medi, rlig, tnum`
GSUB script records: `DFLT: dflt, arab: dflt, latn: dflt`
GSUB has `arab/dflt`: `true`
GPOS script records: `DFLT: dflt, arab: dflt, latn: dflt`
GPOS has `arab/dflt`: `true`
HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`

| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `salaam` | سلام | `uni0645 uni06440627.fina uni0633.init` | 0 | yes | yes | yes | yes |
| `arabic` | العربية | `uni0629.fina uni064A.medi uni0628.init uni0631.fina uni0639.medi uni0644.init uni0627` | 0 | yes | yes | no | no |
| `bismillah` | بسم الله | `uni0647.fina uni0644.medi uni0644.init uni0627 space uni0645.fina uni0633.medi uni0628.init` | 0 | yes | yes | no | no |
| `lam_alef` | لا | `uni06440627` | 0 | no | no | yes | yes |
