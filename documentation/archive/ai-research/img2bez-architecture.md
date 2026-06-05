# img2bez: Bitmap-to-Bezier Autotracer

**Repo:** `~/GH/repos/img2bez`
**Purpose:** Traces bitmap glyph images into font-ready cubic Bezier contours.

## File Structure

```
img2bez/
├── Cargo.toml
└── src/
    ├── lib.rs              # Public API: trace(), trace_into_ufo(), TraceResult
    ├── main.rs             # CLI binary (clap)
    ├── config.rs           # TracingConfig struct
    ├── bitmap.rs           # Image loading + thresholding
    ├── error.rs            # TraceError enum
    ├── geom.rs             # Geometry helpers (signed_area)
    ├── metrics.rs          # Reposition + advance width computation
    ├── render.rs           # 3-panel comparison PNG (source | traced | overlay)
    ├── ufo.rs              # BezPath → norad Glyph (behind "ufo" feature)
    ├── eval.rs             # Quality evaluation vs reference .glif (behind "ufo" feature)
    ├── vectorize/
    │   ├── mod.rs          # vectorize::trace() — orchestrates the pipeline
    │   ├── decompose.rs    # Pixel-edge contour extraction (dual grid, XOR fill)
    │   ├── polygon.rs      # DP optimal polygon approximation + vertex refinement
    │   └── curve.rs        # Corner/extrema detection + single-cubic Bezier fitting
    └── cleanup/
        ├── mod.rs          # Post-processing pipeline (4 steps)
        ├── direction.rs    # Fix contour winding direction
        ├── chamfer.rs      # Insert 45° bevels at line-line corners
        ├── snap.rs         # Grid snap, H/V line snap, H/V handle snap
        ├── extrema.rs      # (currently unused — extrema handled in curve.rs)
        └── simplify.rs     # (currently unused — simplification handled in curve.rs)
```

## Pipeline

```
PNG/JPEG
  │
  ▼ bitmap.rs: load + Otsu threshold → binary GrayImage
  │
  ▼ vectorize/decompose.rs: pixel-edge contour extraction on dual grid
  │  (Y-up coordinates, XOR fill for nesting detection)
  │  → Vec<PixelPath>
  │
  ▼ vectorize/polygon.rs: DP optimal polygon + sub-pixel vertex refinement
  │  → Vec<Polygon> (20-100 vertices per contour)
  │
  ▼ vectorize/curve.rs: polygon_to_bezpath()
  │  1. Compute alpha (smoothness) for each vertex
  │  2. Find corners (alpha >= alphamax)
  │  3. Find curvature transitions (straight↔curved boundaries)
  │  4. Merge corners + transitions into split points
  │  5. Find per-segment extrema (X/Y bounding box protrusions)
  │  6. For each section between split points:
  │     - Laplacian smooth the vertices
  │     - If collinear deviation < tolerance → LineTo (straight)
  │     - Otherwise → fit_single_cubic() (one cubic with H/V handles)
  │  7. Snap nearly-H/V lines and merge collinear segments
  │  → Vec<BezPath> (in pixel-corner coordinates)
  │
  ▼ vectorize/mod.rs: apply scale + Y-offset transform
  │  transform = scale(target_height / image_height) * translate(0, y_offset/scale)
  │  → Vec<BezPath> (in font units)
  │
  ▼ lib.rs: cleanup::process()
  │  1. Fix contour direction (CCW outer, CW counter)
  │  2. Grid snap (coordinates to multiples of grid)
  │  3. Snap nearly-H/V line endpoints to exact H/V
  │  4. Snap nearly-H/V handles to exact H/V
  │  5. Chamfer corners (optional, for Virtua Grotesk style)
  │  → Vec<BezPath> (font-ready)
  │
  ▼ metrics.rs: reposition (shift left edge to LSB, bottom to baseline)
  │  → Vec<BezPath> + advance_width + reposition_shift
  │
  ▼ TraceResult { paths, contour_types, advance_width, reposition_shift }
```

## Key Design Decisions

### Potrace-style decompose → polygon → curve
The vectorize pipeline follows Potrace's algorithm (not imageproc's find_contours). Decompose extracts pixel-edge contours on the dual grid with correct nesting via XOR fill. Polygon uses dynamic programming for optimal approximation. This gives much cleaner polygons than pixel-center contour detection.

### Extrema-based splitting BEFORE curve fitting
Split points include corners, curvature transitions, AND per-segment extrema. This means each curve section starts/ends at an extremum or corner, so handles naturally point H/V — matching type design convention. No post-hoc extrema insertion needed.

### Single cubic per section (fit_single_cubic)
Each section between split points gets exactly ONE cubic Bezier. Handle directions use a wider tangent window (1/3 of section) and snap to H/V within 40°. Handle lengths are optimized via 5×5 asymmetric grid search. This produces minimal point counts with proper type-design structure.

### Straight line detection
After smoothing, each section's collinear deviation is checked. If below `max(seg_len * 0.02, 3.0)` pixels, it becomes a LineTo. Stems and crossbars are correctly detected as straight segments.

## TracingConfig (key parameters)

| Parameter | Default | CLI flag | Description |
|-----------|---------|----------|-------------|
| `threshold` | Otsu | `--threshold N` | Brightness threshold (auto if omitted) |
| `alphamax` | 1.0 | `--alphamax` | Corner detection (0=all corners, >1.34=all smooth) |
| `fit_accuracy` | 4.0 | `--accuracy` | Curve fit tolerance in font units |
| `smooth_iterations` | 3 | `--smooth` | Laplacian smoothing passes before fitting |
| `grid` | 0 | `--grid` | Coordinate snapping (2 for Virtua Grotesk) |
| `target_height` | 1000 | `--target-height` | Scale: image height → this many font units |
| `y_offset` | 0 | `--y-offset` | Baseline offset (typically negative descender) |
| `chamfer_size` | 0 | `--chamfer` | Chamfer size (0=off) |
| `lsb` / `rsb` | 50 | — | Left/right sidebearing |

## CLI Usage

```bash
cargo run --release -- \
  -i ~/Desktop/a-U+0061.png \
  -o /path/to/font.ufo \
  -n a -u 0061 \
  --target-height 1088 --y-offset=-256 \
  --grid 2 --accuracy 2.0 --alphamax 0.8
```

## Debug Environment Variables

| Variable | Effect |
|----------|--------|
| `IMG2BEZ_DEBUG_SPLITS` | Print split point analysis (corners, transitions, extrema, line/curve decisions) |
| `IMG2BEZ_DEBUG_PIXELDIFF` | Generate pixel-level diff image (green=overlap, red=traced-only, blue=source-only) |
| `IMG2BEZ_DEBUG_NO_CLEANUP` | Skip cleanup pipeline (raw curve output) |

## Evaluation (--reference)

```bash
cargo run --release -- -i glyph.png -o font.ufo -n a -u 0061 \
  --reference /path/to/hand-drawn-a.glif \
  --target-height 1088 --y-offset=-256 --grid 2
```

Compares traced output against a reference .glif on 7 metrics:
- **Shape** (30%): Hausdorff + mean distance from 256 sampled points
- **Scale** (15%): Bounding box diagonal ratio
- **H/V handles** (15%): % of handles aligned H/V
- **Points** (10%): On-curve point count ratio
- **Segments** (10%): Line vs curve fraction match
- **Grid** (10%): % of points on grid
- **Contours** (10%): Contour count match

## Render Comparison

The tracer automatically generates a 3-panel comparison PNG:
1. **Left**: Thresholded source bitmap
2. **Middle**: Traced contours re-rasterized
3. **Right**: Overlay (traced in red on source)

Saved as `{glyph_name}_comparison.png` next to the output UFO.
