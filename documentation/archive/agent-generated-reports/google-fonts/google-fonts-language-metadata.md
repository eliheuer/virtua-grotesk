# Google Fonts Language Metadata

This generated report records the local Google Fonts language metadata
evidence behind the current Virtua Grotesk downstream metadata target:
`subsets: "arabic"` and `primary_script: "Arab"`.

## Local Google Fonts Lang Data

- Checkout: `GF_REPO_PATH_NOT_CONFIGURED`
- Script record: `lang/Lib/gflanguages/data/scripts/Arab.textproto`
- Script record exists: no
- Script id: `missing`
- Script name: `missing`

## Arabic Core Language Records

| Language code | Exists | Script | Name |
| --- | --- | --- | --- |
| `ar_Arab` | no | `missing` | `missing` |
| `fa_Arab` | no | `missing` | `missing` |
| `ur_Arab` | no | `missing` | `missing` |

## Current Virtua Grotesk Target

- `primary_script`: `Arab`
- Expected downstream subsets after drawing: `arabic`, `latin`, `menu`
- Preview `subsets` match target: yes
- Preview `primary_script` matches target: yes
- Preview non-Noto `languages` entries absent: yes
- Preview custom `sample_text` absent: yes
- Compared Arabic package examples present: 0 / 9
- Compared examples with `arabic` subset: 0 / 0
- Compared examples with `primary_script: "Arab"`: 0 / 0
- Compared non-Noto Arabic examples omit `languages`: yes
- Compared non-Noto Arabic examples omit `sample_text`: yes
- Do not add `languages` entries for this non-Noto family unless Google
  Fonts review asks for a narrower language scope.
- Do not add custom `sample_text` unless Google Fonts review asks for it
  or the default Arabic specimen text is unsuitable.

## Downstream Preview Alignment

| Field | Preview value | Target | Aligned |
| --- | --- | --- | --- |
| `subsets` | `arabic`, `latin`, `menu` | `arabic`, `latin`, `menu` | yes |
| `primary_script` | `Arab` | `Arab` | yes |
| `languages` | absent | absent for non-Noto package | yes |
| `sample_text` | absent | absent unless reviewer requests override | yes |

## Recent Arabic Package Evidence

This table reads current `METADATA.pb` files from the local synced
`google/fonts` checkout. Noto Arabic families are included to show the
`languages` exception; non-Noto Arabic examples generally omit
`languages` and rely on generated language support.

| Package | Family | Exists | Fonts | Variable | primary_script | Has arabic subset | Languages | sample_text | config_yaml | Subsets |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ofl/estedad/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/scheherazadenew/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/playpensansarabic/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/readexpro/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/cairo/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/amiri/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/notosansarabic/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/notonaskharabic/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |
| `ofl/notokufiarabic/METADATA.pb` | `missing` | no | 0 | no | `none` | no | 0 | 0 | `none` | missing |

References:

- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/lang.html
- https://googlefonts.github.io/gf-guide/googlefonts.html
