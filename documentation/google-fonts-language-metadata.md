# Google Fonts Language Metadata

This generated report records the local Google Fonts language metadata
evidence behind the current Virtua Grotesk downstream metadata target:
`subsets: "arabic"` and `primary_script: "Arab"`.

## Local Google Fonts Lang Data

- Checkout: `/Users/eli/GH/forks/fonts`
- Script record: `lang/Lib/gflanguages/data/scripts/Arab.textproto`
- Script record exists: yes
- Script id: `Arab`
- Script name: `Arabic`

## Arabic Core Language Records

| Language code | Exists | Script | Name |
| --- | --- | --- | --- |
| `ar_Arab` | yes | `Arab` | `Arabic` |
| `fa_Arab` | yes | `Arab` | `Persian` |
| `ur_Arab` | yes | `Arab` | `Urdu` |

## Current Virtua Grotesk Target

- `primary_script`: `Arab`
- Expected downstream subsets after drawing: `arabic`, `latin`, `latin-ext`, `menu`
- Preview `subsets` match target: yes
- Preview `primary_script` matches target: yes
- Preview non-Noto `languages` entries absent: yes
- Preview custom `sample_text` absent: yes
- Compared Arabic package examples present: 9 / 9
- Compared examples with `arabic` subset: 9 / 9
- Compared examples with `primary_script: "Arab"`: 9 / 9
- Compared non-Noto Arabic examples omit `languages`: yes
- Compared non-Noto Arabic examples omit `sample_text`: yes
- Do not add `languages` entries for this non-Noto family unless Google
  Fonts review asks for a narrower language scope.
- Do not add custom `sample_text` unless Google Fonts review asks for it
  or the default Arabic specimen text is unsuitable.

## Downstream Preview Alignment

| Field | Preview value | Target | Aligned |
| --- | --- | --- | --- |
| `subsets` | `arabic`, `latin`, `latin-ext`, `menu` | `arabic`, `latin`, `latin-ext`, `menu` | yes |
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
| `ofl/estedad/METADATA.pb` | `Estedad` | yes | 1 | yes | `Arab` | yes | 0 | 0 | `sources/config.yaml` | `arabic`, `latin`, `latin-ext`, `menu`, `vietnamese` |
| `ofl/scheherazadenew/METADATA.pb` | `Scheherazade New` | yes | 4 | no | `Arab` | yes | 0 | 0 | `none` | `arabic`, `latin`, `latin-ext`, `menu` |
| `ofl/playpensansarabic/METADATA.pb` | `Playpen Sans Arabic` | yes | 1 | yes | `Arab` | yes | 0 | 0 | `sources/config-Arabic.yaml` | `arabic`, `emoji`, `latin`, `latin-ext`, `math`, `menu` |
| `ofl/readexpro/METADATA.pb` | `Readex Pro` | yes | 1 | yes | `Arab` | yes | 0 | 0 | `sources/config.yaml` | `arabic`, `latin`, `latin-ext`, `menu`, `vietnamese` |
| `ofl/cairo/METADATA.pb` | `Cairo` | yes | 1 | yes | `Arab` | yes | 0 | 0 | `sources/cairo.yaml` | `arabic`, `latin`, `latin-ext`, `menu` |
| `ofl/amiri/METADATA.pb` | `Amiri` | yes | 4 | no | `Arab` | yes | 0 | 0 | `none` | `arabic`, `latin`, `latin-ext`, `menu` |
| `ofl/notosansarabic/METADATA.pb` | `Noto Sans Arabic` | yes | 1 | yes | `Arab` | yes | 81 | 0 | `sources/config-sans-arabic.yaml` | `arabic`, `latin`, `latin-ext`, `math`, `menu`, `symbols` |
| `ofl/notonaskharabic/METADATA.pb` | `Noto Naskh Arabic` | yes | 1 | yes | `Arab` | yes | 80 | 0 | `sources/config-naskh-arabic.yaml` | `arabic`, `latin`, `latin-ext`, `math`, `menu`, `symbols` |
| `ofl/notokufiarabic/METADATA.pb` | `Noto Kufi Arabic` | yes | 1 | yes | `Arab` | yes | 81 | 0 | `none` | `arabic`, `latin`, `latin-ext`, `math`, `menu`, `symbols` |

References:

- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/lang.html
- https://googlefonts.github.io/gf-guide/googlefonts.html
