# /draw-outline

Draw or redraw a glyph outline from scratch, following vector best practices and Virtua Grotesk conventions.

## Usage
`/draw-outline <glyph-name> [--master regular|bold|both] [--from-sketch <image-path>]`

Default master: `both` (a new glyph needs both masters for interpolation)

## Instructions

### Step 0: Gather Context
1. Check if the glyph already exists — read `sources/VirtuaGrotesk-Regular.ufo/glyphs/contents.plist`
2. If it exists, read the current `.glif` to understand what's there (this may be a redraw)
3. If `--from-sketch` is provided, read the image to understand the intended shape
4. Study related glyphs for consistency — e.g., if drawing `m`, read `n` first; if drawing `G`, read `C` and `O`

### Step 1: Plan the Outline
Before writing any XML, describe the plan:
- How many contours (outer shape + counters)
- Key dimensions: advance width, sidebearings, vertical alignment
- Where the Virtua Grotesk chamfers go
- Reference glyphs being used for consistency

### Step 2: Draw the Outline
Write the `.glif` XML following all rules below. Then do the same for the second master.

### Step 3: Register & Validate
1. Add the glyph to `glyphs/contents.plist` in both masters if it's new
2. Verify both masters have identical structure (contour count, point count, point types)
3. Suggest `/build-font` to test and `/proof` or `make specimen` to preview

---

## Vector Drawing Rules

These rules apply to every outline in this project. Violating them will cause rendering artifacts, hinting failures, or interpolation kinks.

### Point Placement

**Extrema are mandatory.** Place on-curve points at every horizontal and vertical extreme of every curve — the topmost, bottommost, leftmost, and rightmost positions. This means handles at extrema shoot off at exactly 90 degrees (pure horizontal or pure vertical). Extrema are required for PostScript hinting and prevent rasterization artifacts.

**Minimum points necessary.** Use the fewest points that accurately describe the shape. Extra points make editing harder and can cause interpolation problems. A typical circle-like curve needs just 4 on-curve points (at the extremes) and 8 off-curve handles.

**Inflection points.** Where a curve changes from clockwise to counter-clockwise curvature (like the spine of `s`), add an on-curve point at the inflection. At an inflection point, one handle points into the shape and the other points out. Missing inflection points cause kinks during interpolation.

### Curve Construction

**The magic triangle.** Every curve segment (two on-curve points + two off-curve handles) must fit inside the triangle formed by the on-curve points and the intersection of the extended handle lines. Handles must never cross each other or escape this triangle — doing so creates cusps or self-intersections.

```
        handle B₁
       /
  on-curve B ---- intersection point
       \            /
        curve      /
       /          /
  on-curve A ----
       \
        handle A₁
```

**Handle direction.** Handles at extrema must be perfectly horizontal or vertical. Interior handles should generally follow the curve's flow smoothly. Angled handles at extrema are a common mistake — they break hinting and create bumpy curves.

**Smooth connections.** Where two curve segments meet and should flow smoothly, the on-curve point between them must have its two handles exactly 180 degrees apart (collinear). This is a "smooth" node. If the handles are not collinear, it's a "corner" node and creates a visible angle.

**Curve tension.** Handle length controls curve tension. Longer handles = fuller curve, shorter handles = flatter curve. For a roughly circular arc, handles should be about 55% of the distance to the next on-curve point (the "four-thirds" rule for approximating circles).

### Path Direction & Structure

**Outer paths counter-clockwise, counters clockwise.** In UFO/PostScript convention, the outer contour winds counter-clockwise and inner counters wind clockwise. (This is the opposite of TrueType convention.) Wrong direction = the shape fills incorrectly.

How to verify: trace the contour in point order. For the outer path, the filled area should be to your left. For counters, the filled area should be to your right.

**All paths must be closed.** Every contour's last point connects back to its first. Open paths are ignored during compilation.

**No self-intersections in final output.** Overlapping contours are fine during editing (and Virtua Grotesk sources do use them), but the compiler resolves overlaps. If you create intentional overlaps, ensure they resolve cleanly — avoid "double overlaps" where tiny artifacts appear at junctions.

### What to Avoid

**No shallow curves.** If a curve segment is only a few units deep (nearly flat), remove it. Shallow curves distort because coordinates are integers — the rounding error is proportionally huge. Better to use a straight `line` segment.

**No zero-length handles.** A handle sitting exactly on its on-curve point is degenerate. Either extend it or remove the curve (convert to line).

**No coincident points.** Two points at the same coordinates serve no purpose and confuse interpolation. Remove the duplicate.

**No stray points outside the glyph.** Debris far from the glyph boundaries causes wrong sidebearing calculations. Always verify the bounding box makes sense.

---

## Virtua Grotesk Specifics

### The 16-Unit Chamfer
Every sharp corner gets a 45-degree bevel. The pattern:
```xml
<!-- Stem meeting baseline: stem at x=160 -->
<point x="80" y="0" type="line"/>   <!-- left of stem base -->
<point x="144" y="0" type="line"/>  <!-- 16 units before corner -->
<point x="160" y="16" type="line"/> <!-- 16 units up = the bevel -->
<point x="160" y="560" type="line"/><!-- stem continues up -->
```
Apply this at every junction: stem-baseline, stem-cap height, crossbar ends, apexes.

### Overshoots
Round forms overshoot alignment zones by ~16 units:
- Baseline overshoot: y = -16
- x-height overshoot: y = 592 (576 + 16)
- Cap height overshoot: y = 784 (768 + 16)

### Coordinates
- All integers, preferably multiples of 2
- Key measurements in multiples of 8 or 16
- Regular stems ~96 units wide, Bold stems ~160+ units

### Weight Axis Strategy
- Keep outer contours identical between masters when possible (especially round forms)
- Add weight by shrinking counters inward
- Crossbars may shift vertically in Bold for optical balance
- Both masters must have identical structure (contour count, point count per contour, point types)

### Stroke Character
- Monolinear — no thick/thin contrast
- Generous, open counters and apertures
- Smooth organic curves inside the geometric chamfered framework

---

## Template: Minimal Round Glyph (like O)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<glyph name="GLYPHNAME" format="2">
  <unicode hex="XXXX"/>
  <advance width="WIDTH"/>
  <outline>
    <!-- Outer contour (counter-clockwise) -->
    <contour>
      <point x="CENTER" y="-16" type="curve"/>     <!-- bottom extreme (overshoot) -->
      <point x="RIGHT_HANDLE" y="-16"/>              <!-- off-curve -->
      <point x="RIGHT" y="BOTTOM_HANDLE"/>           <!-- off-curve -->
      <point x="RIGHT" y="MID" type="curve"/>        <!-- right extreme -->
      <point x="RIGHT" y="TOP_HANDLE"/>              <!-- off-curve -->
      <point x="RIGHT_HANDLE" y="TOP"/>              <!-- off-curve -->
      <point x="CENTER" y="TOP" type="curve"/>       <!-- top extreme (overshoot) -->
      <point x="LEFT_HANDLE" y="TOP"/>               <!-- off-curve -->
      <point x="LEFT" y="TOP_HANDLE"/>               <!-- off-curve -->
      <point x="LEFT" y="MID" type="curve"/>         <!-- left extreme -->
      <point x="LEFT" y="BOTTOM_HANDLE"/>            <!-- off-curve -->
      <point x="LEFT_HANDLE" y="-16"/>               <!-- off-curve -->
    </contour>
    <!-- Inner counter (clockwise — reverse point order) -->
    <contour>
      <!-- Same structure, inset by stem width -->
    </contour>
  </outline>
</glyph>
```

## Template: Minimal Straight Glyph (like I or l)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<glyph name="GLYPHNAME" format="2">
  <unicode hex="XXXX"/>
  <advance width="WIDTH"/>
  <outline>
    <contour>
      <!-- Bottom-left, going counter-clockwise with chamfers -->
      <point x="LSB" y="0" type="line"/>
      <point x="STEM_LEFT_MINUS_16" y="0" type="line"/>
      <point x="STEM_LEFT" y="16" type="line"/>          <!-- chamfer -->
      <point x="STEM_LEFT" y="HEIGHT_MINUS_16" type="line"/>
      <point x="STEM_LEFT_PLUS_16" y="HEIGHT" type="line"/> <!-- chamfer -->
      <point x="STEM_RIGHT_MINUS_16" y="HEIGHT" type="line"/>
      <point x="STEM_RIGHT" y="HEIGHT_MINUS_16" type="line"/> <!-- chamfer -->
      <point x="STEM_RIGHT" y="16" type="line"/>
      <point x="STEM_RIGHT_PLUS_16" y="0" type="line"/>   <!-- chamfer -->
      <point x="RSB_EDGE" y="0" type="line"/>
      <!-- ... continues around the outer shape -->
    </contour>
  </outline>
</glyph>
```

## References
- [Drawing Vectors for Type — OHno Type Co](https://ohnotype.co/blog/drawing-vectors)
- [Drawing Good Paths — Glyphs App](https://glyphsapp.com/learn/drawing-good-paths)
- [Drawing Glyphs — RoboFont](https://robofont.com/documentation/tutorials/drawing-glyphs/)
