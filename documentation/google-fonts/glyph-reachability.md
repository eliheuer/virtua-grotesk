# Glyph Reachability

This generated report checks which built glyphs are not reachable from
Unicode cmap entries, direct GSUB substitution outputs, or component
references from those glyphs. It complements Fontspector's
`unreachable_glyphs` and
`googlefonts/metadata/unreachable_subsetting` warnings so Arabic helper
glyphs, private-use glyphs, and final feature coverage can be reviewed
deliberately before downstream packaging.

## Summary

- Fonts checked: 5
- Unique unreachable glyphs: 0
- Unique Arabic helper/form glyphs: 0
- Unique Arabic mark helper glyphs: 0
- Unique source cleanup glyphs: 0
- Unique component-reachable glyphs: 100
- Fontspector warning linkage: `unreachable_glyphs`,
  `googlefonts/metadata/unreachable_subsetting`

## Per-Font Counts

| Font | cmap glyphs | GSUB output glyphs | Unreachable glyphs |
| --- | ---: | ---: | ---: |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | 474 | 194 | 0 |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | 474 | 194 | 0 |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | 474 | 194 | 0 |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | 474 | 194 | 0 |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | 474 | 194 | 0 |

## Unique Category Counts

| Category | Unique glyphs |
| --- | ---: |

## Category Occurrence Counts

| Category | Count |
| --- | ---: |

## Unique Unreachable Glyphs

| Glyph | Category | Fonts |
| --- | --- | --- |

## Apply Before Final Submission

- Decide whether each unreachable Arabic helper glyph should be reached
  through GSUB, encoded, decomposed into reachable outlines, or removed.
- Revisit this report after final Arabic features, PUA scope, and mark
  handling decisions are applied.
- Regenerate `documentation/google-fonts/fontspector-warnings.md` and this report
  after source or feature changes.
