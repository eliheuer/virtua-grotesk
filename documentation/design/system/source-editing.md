# Source editing

How to edit the UFO and designspace files directly. The source rules in
`AGENTS.md` apply in addition.

## Files

| File | Content |
| --- | --- |
| `sources/VirtuaGrotesk.designspace` | Format 5. Axis `wght` 400 to 700, default 400. Masters Regular (400) and Bold (700). Instances Regular, Medium, SemiBold, Bold. |
| `<master>.ufo/fontinfo.plist` | Names and metrics: units per em 1024, ascender and cap height 768, x-height 576, descender -256. |
| `<master>.ufo/glyphs/contents.plist` | Glyph name to GLIF file name. Read it to find a glyph file. |
| `<master>.ufo/glyphs/*.glif` | One glyph: advance, unicodes, contours, components, anchors, mark color. |
| `<master>.ufo/kerning.plist`, `groups.plist` | Kerning pairs and kerning groups. |
| `<master>.ufo/features.fea` | OpenType features. |
| `<master>.ufo/lib.plist` | `public.glyphOrder` and other font data. |

## Glyphs

- A point without a `type` attribute is an off-curve point. A `curve` point
  follows two off-curve points.
- Coordinates are integers on the 2-unit grid. New structural points use the
  8-unit grid (`sources/design.toml`).
- To change the left sidebearing, move every point and component by the same
  amount. To change the right sidebearing, change the advance only.
- Do not reorder points or contours. The order controls interpolation.

## Compatibility of the masters

A glyph has the same structure in both masters: the same contours, the same
number of points in each contour, the same point types in the same order, and
the same components. Only coordinates, advances and anchor positions differ.
If you add or remove a point or contour, do it in both masters.
`.venv/bin/fgtools lint-glifs` checks this.

## Kerning

- Both masters have kerning (Regular 128 pairs, Bold 77 pairs on 2026-11-10)
  and the same 89 groups. Keep the groups identical in both masters.
- `public.kern1.*` groups are the left side of a pair, `public.kern2.*` the
  right side. A glyph is in at most one group of each side.
- A specific pair overrides a group pair: glyph and glyph, then glyph and
  group, then group and glyph, then group and group.
- Use multiples of 8. Negative values tighten.
- When you add a pair to one master, add it to the other master too (the
  value can be 0).

## Designspace

- Source and instance paths are relative to the designspace file.
- To add an axis, add a dimension to every source and every instance.
- The default value of an axis must match the location of one source.
