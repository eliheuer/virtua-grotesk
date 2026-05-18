# img2bez Eval Loop: Trace → Compare → Improve

This document describes the iterative workflow for improving img2bez's tracing output. Use this when starting a new session to work on the tracer.

## Prerequisites

- img2bez repo at `~/GH/repos/img2bez`
- Virtua Grotesk repo at `~/GH/repos/virtua-grotesk`
- Source glyph images on Desktop (e.g. `~/Desktop/a-U+0061.png`)
- Hand-drawn reference glifs in the VG UFO sources

## The Loop

### 1. Trace a glyph

```bash
cd ~/GH/repos/img2bez
cargo run --release -- \
  -i ~/Desktop/a-U+0061.png \
  -o ~/Temp/test_output.ufo \
  -n a -u 0061 \
  --target-height 735 --y-offset=-172 \
  --grid 2 --alphamax 0.8 --smooth 1
```

**Important:** Copy a VG UFO to the output path first (the tool inserts into an existing UFO):
```bash
cp -r ~/GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo ~/Temp/test_output.ufo
```

**Parameters for Virtua Grotesk:**
| Parameter | Value | Why |
|-----------|-------|-----|
| `--target-height 735` | Calibrated to source image scale | Maps image pixel height to font unit range |
| `--y-offset -172` | Calibrated vertical offset | Aligns baseline correctly for these source images |
| `--grid 2` | VG uses even coordinates | Snaps all points to multiples of 2 |
| `--alphamax 0.8` | Slightly aggressive corners | Catches geometric corners in VG's style (step at 0.85) |
| `--smooth 1` | Minimal smoothing | Preserves polygon detail better than default 3 |

**Note:** `--accuracy` has no effect (only used by unused kurbo fitter). `--target-height` and `--y-offset` are calibrated for the current source images — if you re-render sources at a different size, these must be recalibrated.

### 2. Inspect the output

The tracer automatically generates:
- **`~/Temp/a_comparison.png`** — 3-panel visual comparison (source | traced | overlay)
- **`~/Temp/test_output.ufo/glyphs/a.glif`** — the traced outline in UFO format

Read the comparison PNG and the glif to assess quality.

### 3. Compare against hand-drawn reference

Open both the traced output and the hand-drawn reference in a font editor (or screenshot them) and compare:

**What to look for:**
- **Handle directions**: All off-curve handles should share an x OR y coordinate with their adjacent on-curve point (H/V alignment). Non-H/V handles indicate a problem in tangent computation or snap threshold.
- **Point placement**: On-curve points should be at extrema (topmost, bottommost, leftmost, rightmost of each curve). Points at arbitrary positions indicate bad split-point detection.
- **Straight vs curved**: Stems and crossbars should be LineTo segments, not curves. If a stem is rendered as a curve, the transition detection or line tolerance is wrong.
- **Point economy**: Too many points = too many split points or poor line merging. Too few = missing structural features.
- **Shape fidelity**: The overlay panel should show close alignment. Systematic expansion/contraction indicates a threshold or smoothing issue.

### 4. Run eval metrics (optional)

```bash
cargo run --release -- \
  -i ~/Desktop/a-U+0061.png \
  -o ~/Temp/test_output.ufo -n a -u 0061 \
  --target-height 735 --y-offset=-172 --grid 2 --alphamax 0.8 --smooth 1 \
  --reference ~/GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo/glyphs/a.glif
```

This prints a scored evaluation report comparing against the reference on 7 metrics.

### 5. Diagnose and fix

Based on the comparison, identify the root cause and modify the appropriate file:

| Symptom | Root cause | File to modify |
|---------|-----------|---------------|
| Handles not H/V | Tangent computation or snap threshold | `src/vectorize/curve.rs` → `fit_single_cubic()`, `snap_tangent_hv()` |
| Curves where there should be lines | Line tolerance too tight or transitions filtered | `src/vectorize/curve.rs` → `collinear_deviation` check, transition filtering |
| Too many points | Too many split points | `src/vectorize/curve.rs` → `merge_nearby_preserve_corners()`, transition detection |
| Shape doesn't match source | Smoothing, curve fitting, or scale issue | `src/vectorize/curve.rs` → `laplacian_smooth()`, `fit_single_cubic()` |
| Points not at extrema | Extrema detection on polygon vertices | `src/vectorize/curve.rs` → `find_segment_extrema()` |
| Grid alignment issues | Grid snapping or rounding | `src/cleanup/snap.rs` |
| Wrong contour direction | Direction fixing logic | `src/cleanup/direction.rs` |
| Chamfer problems | Chamfer size/edge detection | `src/cleanup/chamfer.rs` |

### 6. Debug tools

**Split analysis** — see exactly how the polygon is split and why each section is line/curve:
```bash
IMG2BEZ_DEBUG_SPLITS=1 cargo run --release -- -i image.png -o ~/Temp/out.ufo ...
```

**Pixel diff** — generate a pixel-level accuracy map:
```bash
IMG2BEZ_DEBUG_PIXELDIFF=1 cargo run --release -- -i image.png -o ~/Temp/out.ufo ...
```

**Skip cleanup** — see raw curve output without post-processing:
```bash
IMG2BEZ_DEBUG_NO_CLEANUP=1 cargo run --release -- -i image.png -o ~/Temp/out.ufo ...
```

### 7. Rebuild and re-test

```bash
cargo run --release -- -i ~/Desktop/a-U+0061.png -o ~/Temp/test_output.ufo -n a -u 0061 \
  --target-height 735 --y-offset=-172 --grid 2 --alphamax 0.8 --smooth 1
```

Then re-inspect the comparison PNG and glif. Repeat until the output matches type design conventions.

## Type Design Conventions (from ohnotype.co/blog/drawing-vectors)

These are the standards we optimize for:

1. **Points at extrema** — on-curve points at the topmost, bottommost, leftmost, rightmost positions on each curve
2. **H/V handles** — all off-curve handles point exactly horizontally or vertically from their on-curve anchor
3. **Minimal point count** — use the fewest points necessary to define the shape
4. **Lines for straight sections** — stems, crossbars, and straight edges use LineTo, not curves
5. **Smooth vs corner** — smooth points where curves flow continuously, corner points at structural junctions
6. **Contour direction** — outer contours CCW, counter/hole contours CW

## Key Code Areas in curve.rs

The heart of the tracer. When making improvements, these are the critical functions:

### Split point detection
How the polygon is divided into sections. Controls WHERE on-curve points end up.
- `compute_alpha()` — smoothness metric per vertex
- `find_curvature_transitions()` — detect straight↔curved boundaries
- `find_segment_extrema()` — find bounding box extrema within sections
- `merge_nearby_preserve_corners()` — deduplicate nearby splits
- Short section removal — removes transitions creating sections <40px (protects corners+extrema)

### Line vs curve decision
After splitting, each section is classified as straight or curved.
- `laplacian_smooth()` — smooth polygon vertices before measuring
- `collinear_deviation()` — max perpendicular distance from straight line
- Tolerance: `max(seg_len * 0.02, 3.0)` pixels

### Curve fitting
How curves are drawn for non-straight sections.
- `fit_single_cubic()` — one cubic per section
- Tangent window: 1/3 of section length, capped at 5 (H/V snapping dominates regardless)
- H/V snap threshold: 40° (all handles naturally H/V for geometric fonts)
- Handle lengths: 7-scale coarse grid [0.15–0.57] → medium (step 0.01, ±0.05) → fine (step 0.003, ±0.01)
- Error metric: nearest-point Hausdorff (48-sample curve, min-distance to each polyline point)

### Post-fit cleanup (cleanup/mod.rs)
- `fix_direction()` — outer CCW, counter CW
- `to_grid()` — snap to grid=2
- `hv_lines()` — snap nearly-H/V line endpoints
- `hv_handles()` — snap handles within 25° to pure H/V

## History of Key Fixes

1. **Transition filter was too aggressive** — Transitions within 3 vertices of a corner were dropped, losing stem/curve boundary splits. Fixed by keeping ALL transitions and reducing merge gap to 1.
2. **kurbo fitter produced too many points** — Switched from `fit_to_bezpath_opt` (multiple cubics, arbitrary point placement) to `fit_single_cubic` (one cubic per section, preserves extrema structure).
3. **Handles not H/V** — Fixed by widening tangent window (nearest neighbor → 1/3 of section) and snap angle (30° → 40°).
4. **Symmetric handle constraint** — Changed from a=b to 5×5 (a,b) grid search for asymmetric handle lengths.
5. **Shape expansion in overlay** — Caused by anti-aliased source images; pre-thresholded binary sources produce better alignment.
6. **Parametric t-error in curve fitting** — `max_polyline_deviation` used `t=i/(n-1)` which is a poor approximation. Replaced with nearest-point Hausdorff (48 curve samples, find closest to each polyline point). Improved shape score by +0.07.
7. **UFO duplicate closing points** — BezPath ClosePath returns to MoveTo, duplicating the first on-curve. Fixed in `ufo.rs` by detecting and removing the duplicate.
