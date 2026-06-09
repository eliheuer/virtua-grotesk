# Contour Cleanup Review Queue

This generated queue deduplicates `documentation/google-fonts/fontspector-contour-count.md`
so manual drawing cleanup can work through unique glyph decisions before
checking repeated built-font rows in `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`.

- Unique glyph review items: 4
- All-font finding rows: 4
- Reference font: `none`

## Category Counts

| Category | Unique glyphs |
| --- | ---: |
| source outline review | 4 |

## Queue

| Glyph | Source glyph | Codepoint | Category | Fonts | Actual | Expected | Reference | Recommended action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `uni062C.fina` | `jeem-ar.fina` | unencoded | source outline review | `VirtuaGrotesk[wght].ttf` | 4 | 2, 3 | no | Inspect source outline structure and compare the rendered proof before editing. |
| `uni062D.fina` | `hah-ar.fina` | unencoded | source outline review | `VirtuaGrotesk[wght].ttf` | 3 | 1, 2 | no | Inspect source outline structure and compare the rendered proof before editing. |
| `uni0635.init` | `sad-ar.init` | unencoded | source outline review | `VirtuaGrotesk[wght].ttf` | 1 | 2 | no | Inspect source outline structure and compare the rendered proof before editing. |
| `uni0636.init` | `dad-ar.init` | unencoded | source outline review | `VirtuaGrotesk[wght].ttf` | 2 | 3, 5 | no | Inspect source outline structure and compare the rendered proof before editing. |
