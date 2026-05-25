# Google Fonts Glyphset Readiness

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`

This report summarizes Google Fonts authoring glyphset coverage for the intended Latin plus Arabic submission scope. It is generated from the installed `glyphsets` package and should be reviewed with the downstream `METADATA.pb` subset and primary-script decisions.

## Tracked Glyphsets

| Glyphset | Script | Required codepoints | Present | Missing | Coverage | Language codes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `GF_Latin_Kernel` | Latin | 116 | 93 | 23 | 80.17% | none |
| `GF_Latin_Core` | Latin | 319 | 100 | 219 | 31.35% | `ca_Latn`, `cs_Latn`, `cy_Latn`, `da_Latn`, `de_Latn`, `en_Latn`, `es_Latn`, `fi_Latn`, `fr_Latn`, `hr_Latn`, `hu_Latn`, `is_Latn`, `it_Latn`, `lt_Latn`, `lv_Latn`, `mt_Latn`, `nb_Latn`, `nl_Latn`, `pl_Latn`, `pt_Latn`, `ro_Latn`, `sk_Latn`, `sq_Latn`, `sr_Latn`, `sv_Latn`, `tr_Latn` |
| `GF_Arabic_Core` | Arabic | 224 | 167 | 57 | 68.52% | `ar_Arab`, `fa_Arab`, `ur_Arab` |
| `GF_Arabic_Plus` | Arabic | 267 | 168 | 99 | 49.67% | `ckb_Arab`, `zlm_Arab`, `ps_Arab`, `sd_Arab`, `ug_Arab`, `ar_Arab`, `fa_Arab`, `ur_Arab` |

## Metadata Implications

- First-submission subsets should include `menu`, `latin`, `latin-ext`, and `arabic` after drawing work is complete.
- `primary_script: "Arab"` remains the current metadata review target because Arabic is in first-submission scope.
- `GF_Arabic_Core` is the current minimum Arabic target; `GF_Arabic_Plus` is tracked here only to show the cost of expanding scope.
- This report is coverage evidence only; shaping, mark behavior, and visual proofing are tracked separately.
