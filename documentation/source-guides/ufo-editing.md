---
paths:
  - "sources/**/*.ufo/**"
  - "sources/**/*.glif"
  - "sources/**/*.plist"
---

# UFO Editing Rules

## Font Metrics (both masters must match)

| Metric | Value |
|--------|-------|
| UPM | 1024 |
| Ascender | 832 |
| Cap Height | 768 |
| x-Height | 576 |
| Descender | -256 |
| Grid Size | 2 (prefer even coordinates) |

## UFO3 Format Basics

Each master is a `.ufo` directory:
- `fontinfo.plist` — font-level metrics, naming
- `lib.plist` — font-level metadata
- `glyphs/contents.plist` — maps glyph names → `.glif` filenames
- `glyphs/<name>.glif` — individual glyph source (XML)
- `kerning.plist` — flat kerning pairs (see kerning-editing.md)
- `groups.plist` — kerning group definitions

## Glyph Lookup Pattern

To find a glyph file:
1. Read `glyphs/contents.plist` for the relevant master
2. Find the `<key>` matching the glyph name
3. The `<string>` value is the filename inside `glyphs/`

Example: glyph "A" → `A_.glif`, glyph "period" → `period.glif`

Filename conventions: uppercase letters get trailing underscore (`A_.glif`), lowercase are direct (`a.glif`), special names use descriptive form (`period.glif`, `exclam.glif`).

## GLIF XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<glyph name="A" format="2">
  <unicode hex="0041"/>
  <advance width="700"/>
  <outline>
    <contour>
      <point x="40" y="0" type="line"/>
      <point x="96" y="0" type="line"/>
      <!-- ... more points ... -->
    </contour>
    <!-- Additional contours for counter shapes -->
  </outline>
</glyph>
```

Key elements:
- `<advance width="N"/>` — total glyph width (advance width)
- `<outline>` — contains one or more `<contour>` elements
- `<contour>` — a closed path of points
- `<point>` attributes:
  - `x`, `y` — integer coordinates
  - `type="line"` — on-curve straight segment
  - `type="curve"` — on-curve cubic bezier (preceded by 2 off-curve points)
  - No `type` attribute — off-curve control point (for curves)

## Master Compatibility (CRITICAL)

Both masters (Regular and Bold) MUST have identical glyph structure:
- Same number of contours per glyph
- Same number of points per contour
- Same point types in the same order (line/curve/off-curve)
- Only coordinates and advance width may differ between masters

**After editing ANY glyph, verify the other master has the same structure.** Incompatible masters will cause the variable font build to fail.

## Sidebearing Rules

- **Left sidebearing (LSB):** The x-coordinate of the leftmost point. To change LSB, shift ALL points in the glyph by the same delta.
- **Right sidebearing (RSB):** `advance_width - rightmost_x`. To change RSB, only change the `<advance width>` value.
- **Both sidebearings:** Shift all points for LSB change, then adjust advance width for RSB.

## Coordinate Conventions

- All coordinates MUST be integers
- Prefer multiples of 2 (the grid size)
- Key vertical alignment zones:
  - Baseline: y=0
  - x-height: y=576
  - Cap height: y=768
  - Ascender: y=832
  - Descender: y=-256
- Slight overshoots (2–8 units) above/below alignment zones are normal for round shapes

## Safety Rules

1. **Always read before write** — never edit a .glif file without reading it first
2. **Edit both masters** when changing structure (adding/removing points or contours)
3. **Only edit one master** when adjusting coordinates for weight differences
4. **Verify after edit** — suggest running `make reports` to refresh `documentation/source/master-compatibility.md`, or `make preflight` for a fresh build plus checks
5. **Preserve XML declaration** — keep `<?xml version="1.0" encoding="UTF-8"?>` and `format="2"`
6. **Don't reorder points** — point order matters for interpolation
7. **Back up before bulk edits** — for changes affecting many glyphs, suggest a git commit first
