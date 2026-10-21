---
name: draw-outline
description: Draw or redraw a glyph outline from scratch in both UFO masters, following Virtua Grotesk vector conventions (16-unit chamfers, master compatibility). Use when adding a new glyph or redrawing an existing one.
---

# /draw-outline

Draw or redraw a glyph outline from scratch, following vector best practices and Virtua Grotesk conventions.

## Usage
`/draw-outline <glyph-name> [--master regular|bold|both] [--from-sketch <image-path>]`

Default master: `both` (a new glyph needs both masters for interpolation)

## Instructions

### Step 0: Gather Context
Read `DESIGN.md` and the applicable `agent-proofs/cases/` feedback before drawing. Green Virtua geometry governs construction across scripts; external fonts are script references. Record donor geometry and any adaptation.

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
For curves, read [Curve quality](references/curve-quality.md) and follow its
comb/continuity workflow before accepting a candidate.

Write the `.glif` XML following all rules below. Then do the same for the second master.

### Step 3: Register & Validate
1. Add the glyph to `glyphs/contents.plist` in both masters if it's new
2. Verify both masters have identical structure (contour count, point count, point types)
3. Suggest `/build-font` to test and `/proof` or `make review` to preview

---

## Vector Drawing Rules

These rules apply to every outline in this project. Violating them will cause rendering artifacts, hinting failures, or interpolation kinks.

### Point Placement

**Extrema are mandatory.** Place on-curve points at every horizontal and vertical extreme of every curve — the topmost, bottommost, leftmost, and rightmost positions. This means handles at extrema shoot off at exactly 90 degrees (pure horizontal or pure vertical). Extrema are required for PostScript hinting and prevent rasterization artifacts.

**Minimum points necessary.** Use the fewest points that accurately describe the shape. Extra points make editing harder and can cause interpolation problems. A typical circle-like curve needs just 4 on-curve points (at the extremes) and 8 off-curve handles.

**Inflections.** Inspect signed curvature for reversals. Keep intended S-curves; remove unintended reversals in a convex turn. A cubic can contain an inflection without a node there. Split only when it improves control or is required downstream, and keep master structure compatible; splitting alone does not prevent interpolation defects.

### Curve Construction

**Handle-ray triangle.** For an ordinary convex turn with intersecting handle rays, inspect handle positions relative to their intersection. This is not a universal validity test: parallel tangents and intended inflections need separate analysis. Check actual curvature and intersections instead of inferring a cusp from handle layout alone.

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

**Curve tension.** Handle length controls curve tension. Longer handles = fuller curve, shorter handles = flatter curve. For a circular 90-degree arc, the standard cubic approximation uses handles of about 0.552285 times the radius (not the endpoint chord). This is a circular construction, not a default tension for Virtua turns. Inspect curvature and mass instead of forcing equal handles.

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
- New machine drafts: every on/off-curve point, anchor, advance and sidebearing on 8. Read DESIGN.md for recorded optical exceptions; never snap green donors.
- Measure popcount separately; high popcount alone is not a failure.
- Run `scripts/draft_grid_check.py --ufo <scratch-Regular.ufo> --ufo <scratch-Bold.ufo> --glyphs <names> --json <report>` before building. Then check curves, compatibility, shaping and rendered proofs. Retain source hashes and draft evidence for later human corrections.
- Keep 16-unit exposed chamfers and 8-unit small joins in both masters
- Regular stems ~96 units wide, Bold stems ~160+ units

### Weight Axis Strategy
- Keep outer contours identical between masters when possible (especially round forms)
- Add weight by shrinking counters inward
- Crossbars may shift vertically in Bold for optical balance
- Both masters must have identical structure (contour count, point count per contour, point types)

### Stroke Character
- Monolinear — no thick/thin contrast
- Generous, open counters and apertures
- Deliberately constructed, machined curves inside the geometric chamfered framework; follow measured manual corrections in DESIGN.md

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

### Learn from saved manual corrections

Before revising a related form, search the
[manual correction index](../../../agent-proofs/FEEDBACK.md#manual-correction-library)
by glyph and construction (for example, tangent, chamfer, neck, bowl).
Read the relevant source pair and its case notes, not just the lesson summary.
Separate geometry changes from editor serialization or metadata changes.
Treat the human-edited source as fixed when adapting another master; transfer
construction relationships, not a blanket coordinate scale. Check point order,
metrics, anchors and interpolated forms in scratch before presenting a candidate.

For Zayin’s head/stem junction, HEB-006 correction 01 demonstrates a horizontal
tangent on one side and an intentional small cut on the other. Do not interpret
“chamfer corners” as adding bevels to smooth tangent joins. This is a local
example, not a requirement to make all Hebrew junctions asymmetric.
Record reuse and Eli’s verdict in the same case; promote repeated, confirmed
patterns into DESIGN.md while retaining exceptions and rejected examples.

HEB-006 correction 02 revises that transfer: the Bold candidate had the correct
tangent/cut types but kept Regular’s tall transition, which Eli rejected as
humanist. His Bold turns within a square extent with equal tangent handles,
keeping the curve start at Regular’s y=376 as the head thickens. Before adapting
weight, compare curve extents, straight-run lengths and handle relationships;
choose fixed alignments explicitly. Neither lattice compliance nor matching
point types establishes the intended machined character. Retrieve the exact
[source pair and measurements](../../../agent-proofs/cases/hebrew-006/README.md#manual-correction-02--bold-geometric-turn-2026-10-20).
Treat 56-unit extent and 40-unit handles as this example’s dimensions, not a
generic corner recipe. Retain rejected candidates alongside human corrections.

### Active Virtua drawing workflow

Follow the standing authorization in `agent-proofs/README.md`: as of 2026-10-20,
new Hebrew drawing batches go directly into active masters after preserving a
baseline; no repeated application question is needed. Retain technical checks,
proofs, exact manual corrections, source-color protections and human grading.

### Audit joins by intended construction

For curve/terminal work, run `scripts/curve_lint.py <Master> <glyphs> --joins`.
The default CLI checks crest/tension only. The join audit exposes unmarked
line/curve corners as well as marked-smooth kinks; inspect the former instead
of assuming a missing smooth flag is deliberate. Do not round intentional
corners automatically. Distinguish tangent continuation, a short straight
landing before a chamfer, and an intentional shelf. See
[HEB-007 correction 01](../../../agent-proofs/cases/hebrew-007/README.md#manual-correction-01--regular-gimel-2026-10-20)
for the exact Regular example and pending Bold transfer test. Align cyclic
contour order before comparing point indices; preserve manual optical edits.

### Transfer bounded turns, not stretched handles

For branch/diagonal joins, read [HEB-008 Final Tsadi correction 01](../../../agent-proofs/cases/hebrew-008/README.md#manual-correction-01--regular-final-tsadi).
The human edit separates axis-tangent turns from straight shelves, junction cuts
and terminal landings; equal handle pairs replace a sweep stretched directly
to the diagonal. Before transferring, record each turn's endpoints, extents,
handle directions/lengths and adjoining flats. Choose which alignments stay
fixed as weight changes. Do not assume an unmarked curve/line join is an
intentional corner: inspect its geometry. Preserve human smooth flags/source
bytes even when geometry is tangent. Exact 64/128 handles are local evidence,
not universal radii; distinguish the requested transfer trial from approval.

### Do not equate machined with equal handles

Before reusing the square-turn examples, consult
[ARB-003 correction 01](../../../agent-proofs/cases/arabic-003/README.md#manual-correction-01--bold-hamza-above).
Eli narrowed/lightened the hamza base and changed square inner turns to unequal
handle lengths while preserving axis tangency and the 16/8-unit cuts. Compare
bar mass, terminal projection, curve extent and each handle independently.
Equal handles are a construction choice, not a quality gate; a source passing
grid and tangent checks can still have poor proportions. Keep these local
human ratios as evidence rather than applying them wholesale to new marks.

### Required raster proof gate — 2026-10-21

Eli made fixed raster inspection a core part of Arabic drawing work. After each
bounded batch, render 400 and 700 with `agent-proofs/app/render-detail.py`, using
Before, Working, Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro.
Inspect the actual PNGs, record visible findings, and fix observed faults before
advancing. Use shorter/larger details or reading-size context as needed. Keep
PNGs and hash receipts beside source snapshots. Browser proofs, curve diagnostics
and compiled shaping remain complementary; command success is not visual review
or a human grade. See `agent-proofs/FEEDBACK.md#raster-proof-gate--2026-10-21`.
