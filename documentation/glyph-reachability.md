# Glyph Reachability

This generated report checks which built glyphs are not reachable from
Unicode cmap entries or direct GSUB substitution outputs. It complements
Fontspector's `unreachable_glyphs` and
`googlefonts/metadata/unreachable_subsetting` warnings so Arabic helper
glyphs, private-use glyphs, and final feature coverage can be reviewed
deliberately before downstream packaging.

## Summary

- Fonts checked: 5
- Unique unreachable glyphs: 19
- Unique Arabic helper/form glyphs: 5
- Unique Arabic mark helper glyphs: 13
- Unique source cleanup glyphs: 1
- Fontspector warning linkage: `unreachable_glyphs`,
  `googlefonts/metadata/unreachable_subsetting`

## Per-Font Counts

| Font | cmap glyphs | GSUB output glyphs | Unreachable glyphs |
| --- | ---: | ---: | ---: |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | 201 | 127 | 19 |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | 201 | 127 | 19 |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | 201 | 127 | 19 |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | 201 | 127 | 19 |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | 201 | 127 | 19 |

## Unique Category Counts

| Category | Unique glyphs |
| --- | ---: |
| Arabic helper/form | 5 |
| Arabic mark helper | 13 |
| source cleanup | 1 |

## Category Occurrence Counts

| Category | Count |
| --- | ---: |
| Arabic helper/form | 25 |
| Arabic mark helper | 65 |
| source cleanup | 5 |

## Unique Unreachable Glyphs

| Glyph | Category | Fonts |
| --- | --- | --- |
| `dotabovear` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `dotbelowar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `dotcenterar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `doublestrokear` | Arabic helper/form | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `gafsarkashabovear` | Arabic helper/form | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `gafsarkashcenterar` | Arabic helper/form | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `miniKehehar` | Arabic helper/form | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `threedotsdownabovear` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `threedotsdownbelowar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `threedotsdowncenterar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `threedotsupabovear` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `threedotsupbelowar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `twodotshorizontalabovear` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `twodotshorizontalbelowar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `twodotsverticalabovear` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `twodotsverticalbelowar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `uni0647.medi.001` | Arabic helper/form | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `waslaar` | Arabic mark helper | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |
| `yabaha` | source cleanup | `fonts/ttf/VirtuaGrotesk-Bold.ttf`<br>`fonts/ttf/VirtuaGrotesk-Medium.ttf`<br>`fonts/ttf/VirtuaGrotesk-Regular.ttf`<br>`fonts/ttf/VirtuaGrotesk-SemiBold.ttf`<br>`fonts/variable/VirtuaGrotesk[wght].ttf` |

## Apply Before Final Submission

- Decide whether each unreachable Arabic helper glyph should be reached
  through GSUB, encoded, decomposed into reachable outlines, or removed.
- Revisit this report after final Arabic features, PUA scope, and mark
  handling decisions are applied.
- Regenerate `documentation/fontspector-warnings.md` and this report
  after source or feature changes.
