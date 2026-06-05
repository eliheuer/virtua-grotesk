# Curve Quality Workplan: Levien-Based Fitting for img2bez

Following Raph Levien's work on curve fitting (blog posts, PhD thesis "From Spiral to Spline", kurbo crate, and Potrace's opticurve algorithm) to replace img2bez's brute-force grid search with mathematically optimal fitting.

## The Problem

Comparing traced output to the hand-drawn reference in a font editor reveals:
- Curves are wobbly/egg-shaped where they should be smooth, regular arcs
- Visible curvature changes at on-curve points (no G2 continuity)
- Too many tiny line segments in complex areas (tail, notch)
- Asymmetric handles producing unbalanced arcs
- Overall shape "follows the pixel noise" instead of producing the smoothest possible approximation

**Root cause:** `fit_single_cubic()` in `src/vectorize/curve.rs` uses a brute-force grid search over handle lengths (7×7 coarse + refinement), optimizing for geometric accuracy to noisy polygon vertices. Each section is fit independently with no cross-section coordination.

## Reference Material (Raph Levien)

| Source | Key Concept |
|--------|-------------|
| [Fitting cubic Bezier curves](https://raphlinus.github.io/curves/2021/03/11/bezier-fitting.html) | Area/moment method: solve quartic polynomial for optimal handle lengths |
| [Simplifying Bezier paths](https://raphlinus.github.io/curves/2023/04/18/bezpath-simplify.html) | `fit_to_bezpath_opt`: optimal segment count via ITP root-finding |
| [Euler spiral blog](https://raphlinus.github.io/curves/2018/12/08/euler-spiral.html) | Minimum Curvature Variation — mathematical definition of "smoothest curve" |
| [PhD thesis](https://levien.com/phd/thesis.pdf) | Full theory of spiral-to-spline conversion, Section 9.6.4 for optimal subdivision |
| [Potrace paper](https://potrace.sourceforge.net/potrace.pdf) | Opticurve: DP-based segment merging |
| kurbo crate (0.13, already in Cargo.toml) | `fit_to_cubic`, `fit_to_bezpath_opt`, `SimplifyBezPath` |

### Levien's Key Insight

The goal is NOT "trace the polygon as accurately as possible." The goal is **"find the smoothest curve that approximates the polygon within tolerance."** Levien's area/moment method finds the mathematically optimal cubic Bezier for given endpoint tangents — it solves a quartic polynomial instead of searching a grid.

---

## Workplan

### Phase 1: Replace Grid Search with Levien's Algebraic Fitter

**Goal:** Replace `fit_single_cubic()` grid search with kurbo's `fit_to_cubic` (Levien's area/moment quartic solver).

**Why this first:** It's the most targeted change. kurbo 0.13 is already a dependency. The current grid search is the direct cause of suboptimal handle lengths and asymmetric curves.

**How Levien's method works:**
1. Normalize the section into a coordinate system where the chord runs (0,0)→(1,0)
2. Compute tangent angles th0, th1 relative to the chord
3. Compute signed area and x-moment of the polygon section via Green's theorem (16-point Gauss-Legendre quadrature)
4. The area constraint expresses d1 as a function of d0
5. The moment constraint gives a quartic polynomial in d0
6. Solve the quartic (Orellana-De Michele factorization) for up to 4 candidates
7. Pick the candidate with lowest error (approximate Frechet distance with bump penalty)

**Files to modify:** `src/vectorize/curve.rs`

- [x] **1a. Create a `ParamCurveFit` adapter for polygon sections.** DONE — `SmoothPolyline` struct with chord-length parametrization, smooth tangent interpolation, and exact analytical moment integrals (Green's theorem). Code exists in `curve.rs` but is currently unused.

- [x] **1b-d. Replace `fit_single_cubic()` with Levien fitter.** ATTEMPTED AND REVERTED. Key findings:
  - **Critical bug:** `accuracy` parameter controls the "short chord" threshold in `fit_to_cubic` (line 397: `if chord2 <= acc2 → try_fit_line`). Using `accuracy=1e6` made ALL chords appear "short", producing degenerate straight lines. Must use accuracy < chord length.
  - **Best result:** 0.907 overall (vs 0.920 baseline) at accuracy=8.0 with H/V-snapped tangent input. Degenerate zero-length handles in some cubics.
  - **Root cause of underperformance:** H/V-snapped tangent directions can end up on the wrong side of the chord for Levien's quartic solver, producing area/moment mismatches. The grid search fitter is more robust because it directly optimizes Hausdorff distance to the polyline.
  - **Decision:** Reverted to grid search fitter. The Levien approach needs a different tangent estimation strategy (possibly iterative refinement of tangent angles rather than upfront H/V snap) to outperform grid search for noisy polyline data.

- [ ] **1e. Test and compare.** Phase 1 did not improve on baseline. Grid search remains primary fitter.

### Phase 2: Use `fit_to_bezpath_opt` for Curved Sections

**Goal:** Instead of forcing exactly one cubic per section, let kurbo's optimal fitter decide how many cubics each section needs.

**Why:** Some sections (long arcs, S-curves) genuinely need 2+ cubics for a good fit. The current approach forces one cubic, which can produce egg-shaped or wobbly curves. Levien's `fit_to_bezpath_opt` finds the minimum number of segments needed with error equalized across segments.

**How it works (Levien thesis Section 9.6.4):**
1. Phase 1: Greedily count the minimum segments needed (binary search for furthest parameter where a single cubic fits)
2. Phase 2: Equalize error across segments using ITP root-finding

**Files to modify:** `src/vectorize/curve.rs`

- [ ] **2a. Replace the `fit_single_cubic` call in `polygon_to_bezpath`.** For curved sections, build a `SimplifyBezPath` from the smoothed polyline segment and call `fit_to_bezpath_opt(&simplified, accuracy)`. This may produce 1 or 2 cubics per section, automatically choosing the optimal subdivision.

- [ ] **2b. Apply H/V handle post-correction to multi-cubic output.** For each cubic in the result, snap handles to H/V where appropriate. The correction needs to handle interior joins (between cubics within a section) where handles should maintain G1 continuity.

- [ ] **2c. Tune the accuracy parameter.** Levien's `accuracy` controls the Frechet distance tolerance. Lower values = more cubics but better shape. Find the sweet spot for Virtua Grotesk (probably 1.0–4.0 in polygon-coordinate pixels).

- [ ] **2d. Test and compare.** Eval loop. Should see better shape fidelity, especially in the bowl and arch areas. Point count may increase slightly if some sections need 2 cubics.

### Phase 3: Opticurve Segment Merging (Potrace-style)

**Goal:** Add a post-fit optimization pass that merges adjacent cubic segments when the combined curve stays within tolerance. This is Potrace's "Stage 5" algorithm.

**Why:** After Phase 1-2 produce per-section cubics, adjacent sections that curve the same direction can often be combined into a single, smoother cubic. This reduces point count and eliminates choppy transitions (especially in the tail/notch area).

**How Potrace's opticurve works:**
1. Pre-compute convexity array (left/right turn at each vertex) and cumulative area
2. For each pair of vertices (i, j), evaluate `opti_penalty`:
   - All intermediate segments must have same convexity (can't merge across inflections)
   - Total direction change < 179°
   - Find intersection of entry/exit tangent lines
   - Compute alpha from area, place control points
   - Measure perpendicular distance at each intermediate vertex
   - If any distance > opttolerance (default 0.2), reject
   - Otherwise return sum of squared distances as penalty
3. Dynamic programming to find lexicographically optimal (min segments, then min penalty) path

**Files to modify:** `src/vectorize/curve.rs` (new function), `src/cleanup/mod.rs` (add step)

- [ ] **3a. Implement `opticurve_merge()` function.** Input: a `BezPath` of cubics and lines. Output: a simplified `BezPath` where adjacent cubics have been merged where possible. Operate on the fitted BezPath BEFORE grid/H/V snapping.

- [ ] **3b. Convexity and area pre-computation.** For each segment, compute the turning direction (cross product of consecutive tangents) and cumulative signed area.

- [ ] **3c. Implement `merge_penalty()`.** Given a candidate merge range [i, j], compute the combined cubic and evaluate fit quality:
   - Check convexity consistency
   - Check total bend < 179°
   - Use `fit_to_cubic` (from Phase 1) to fit the combined range
   - Measure distance at intermediate on-curve points
   - Return penalty or reject

- [ ] **3d. Dynamic programming pass.** Walk through segments, building the optimal merge solution. Prefer fewer segments (like Potrace), break ties by lower penalty.

- [ ] **3e. Wire into the pipeline.** Call `opticurve_merge()` on each contour's BezPath after `polygon_to_bezpath` returns, before passing to cleanup.

- [ ] **3f. Add `opttolerance` parameter.** Expose as a CLI flag (default 0.2 pixels, per Potrace). Larger values = more aggressive merging = smoother but less accurate curves.

- [ ] **3g. Test and compare.** Eval loop. Should see reduced point count, smoother transitions in complex areas (tail, notch), and flowing curves that look more like the reference.

### Phase 4: G2 Curvature Continuity Harmonization

**Goal:** Add a post-fit pass that adjusts handle lengths so curvature matches on both sides of smooth on-curve points. This is the "Harmonize Node" operation from FontLab.

**Why:** After fitting, each cubic is optimized independently. At joins between adjacent cubics, the tangent direction is continuous (G1) but the curvature magnitude may jump. This creates visible "kinks" where the curve seems to change direction slightly. G2 harmonization eliminates these.

**The math (curvature at cubic endpoint):**
For a cubic with control points P0, P1, P2, P3:
- Curvature at P0 = `(2/3) * |cross(P1-P0, P2-P0)| / |P1-P0|^3`
- Curvature at P3 = `(2/3) * |cross(P2-P3, P1-P3)| / |P2-P3|^3`

For G2 at a join between cubic A (ending) and cubic B (starting):
- `kappa_A(t=1) = kappa_B(t=0)`
- This constrains the ratio of handle lengths on each side of the join

**Files to modify:** `src/cleanup/mod.rs` (new module `harmonize.rs`)

- [x] **4a. Implement curvature computation at cubic endpoints.** DONE — `κ = (2/3) * |cross(unit_handle, next_control - on_curve)| / handle_len²`

- [x] **4b. Implement `harmonize_path()`.** DONE — `src/cleanup/harmonize.rs`. Algorithm:
  - At each smooth join (handles ~opposite, within 30° threshold), computes curvature on both sides
  - Targets geometric mean curvature: `κ_target = sqrt(κ_in * κ_out)`
  - Blends 30% toward harmonized handle length (`BLEND_FACTOR = 0.3`)
  - Grid-snaps adjusted positions
  - Tuned via sweep: blend=0.0→0.920, 0.3→0.919, 0.5→0.917, 1.0→0.918

- [x] **4c. Add as cleanup step.** DONE — Pipeline order: fix_direction → grid snap → H/V lines → **harmonize** → H/V handles → chamfer

- [x] **4d. Only harmonize smooth points.** DONE — Detects corners via handle angle (dot product threshold with SMOOTH_ANGLE_THRESHOLD = 30°). Skips degenerate handles (< 2 units) and nearly-straight segments.

- [x] **4e. Test and compare.** Score 0.919 (vs 0.920 baseline). Harmonization is subtle — preserves shape while reducing curvature discontinuities at smooth joins. Visual improvement mainly visible in font editor overlay.

### Phase 5: Circular Arc Detection for Geometric Fonts

**Goal:** For Virtua Grotesk's geometric style, detect near-circular arc sections and use the mathematically optimal handle length (kappa = 0.5522847498 of chord length for a quarter circle).

**Why:** Many curves in a geometric grotesk are intentionally circular or near-circular. When the polygon data approximates a circle, using the theoretical optimal kappa produces perfectly regular, symmetric curves — matching designer intent better than fitting to noisy polygon data.

**Reference:** [Approximate a circle with cubic Beziers](https://spencermortensen.com/articles/bezier-circle/) — Spencer Mortensen's derivation of the optimal kappa = 0.5522847498.

**Files to modify:** `src/vectorize/curve.rs`

- [x] **5a-d. Implement and test circular arc detection.** ATTEMPTED AND REVERTED. Key findings:
  - Kåsa algebraic circle fit implemented: several sections pass circularity test (0.3-1.9% radial deviation)
  - **With H/V-snapped tangents:** Arc error always 1.5-4.5x worse than grid search. H/V snapping distorts the tangent direction away from the true circle perpendicular, making the cubic deviate significantly from the polyline.
  - **With raw tangents:** Some sections (2/12) use arcs with better Hausdorff than grid search, BUT H/V handles drop from 100% to 96% because cleanup's 25° snap can't fix all diagonal handles. Overall score drops from 0.919 to 0.913.
  - **Root cause:** The grid search directly minimizes Hausdorff distance WITH H/V handle constraints. It's solving the exact optimization problem we care about. The circular arc formula optimizes for a different objective (exact circle shape) and produces worse results on the metric we measure.
  - **Conclusion:** Circular arc detection is not beneficial when the fitter already optimizes Hausdorff distance. The approach might help in a Levien fitter pipeline (Phase 1) where the fitter doesn't have H/V handle awareness, but is redundant with the grid search.

- [ ] **5e. Test and compare.** Phase 5 did not improve on baseline. Grid search with H/V snap remains optimal.

### Phase 6: Cleanup — Remove Dead Code

**Goal:** Clean up unused code paths left from the old fitting approach.

- [ ] **6a. Remove `max_polyline_deviation()`.** NOT DONE — still needed by the active grid search fitter.
- [ ] **6b. Remove old grid search constants.** NOT DONE — grid search is still the primary fitter.
- [x] **6c. Clean up unused code.** DONE:
  - Removed `SmoothPolyline` struct and `ParamCurveFit` impl from `curve.rs` (was unused after Phase 1 revert)
  - Removed `snap_vec2_hv()` from `curve.rs` (was only used by SmoothPolyline)
  - Removed `mod extrema` and `mod simplify` from `cleanup/mod.rs` (never called)
  - Removed `force_hv_handles()`, `is_already_hv()`, `pick_best_snap()`, `curve_deviation()`, unused constants from `snap.rs`
  - Removed unused imports (`fit_to_cubic`, `CurveFitSample`, `ParamCurveFit`, `Vec2`, `Range`, `CubicBez`, `ParamCurve`)
  - Warnings reduced from 30 to 2 (harmless cursor assignment warnings)
- [ ] **6d. Update documentation.** Partially done — workplan updated with status. Memory files pending.

---

## Architecture After All Phases

```
polygon vertices
    │
    ▼
split points (corners + transitions + extrema)
    │
    ▼
for each section:
    ├─ straight? → LineTo
    ├─ near-circular? → analytic arc cubic (Phase 5)
    └─ curved → fit_to_bezpath_opt (Levien, Phase 1-2)
    │
    ▼
opticurve merge pass (Phase 3)
    │
    ▼
G2 harmonize (Phase 4)
    │
    ▼
cleanup: direction → grid snap → H/V lines → H/V handles → chamfer
    │
    ▼
UFO output
```

## Key Parameters

| Parameter | Default | Source | Controls |
|-----------|---------|--------|----------|
| `accuracy` | 4.0 | Levien / kurbo | Frechet distance tolerance for curve fitting |
| `opttolerance` | 0.2 | Potrace | Maximum vertex deviation for segment merging |
| `alphamax` | 0.8 | Potrace | Corner detection threshold (alpha ≥ this → corner) |
| `smooth_iterations` | 1 | img2bez | Laplacian smoothing passes on polygon |
| `kappa_quarter` | 0.5522847498 | Mortensen | Optimal handle ratio for quarter-circle |
| `D_PENALTY_ELBOW` | 0.65 | Levien / kurbo | Arm length bump penalty threshold |
| `grid` | 2 | VG | Coordinate grid (snaps to multiples of 2) |

## Testing Protocol

After each phase, run:
```bash
cd ~/GH/repos/img2bez
cargo run --release -- \
  -i ~/Desktop/a-U+0061.png \
  -o ~/Temp/test_output.ufo \
  -n a -u 0061 \
  --target-height 735 --y-offset=-172 \
  --grid 2 --alphamax 0.8 --smooth 1 \
  --reference ~/GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo/glyphs/a.glif
```

Check:
1. **Eval score** — overall should improve, shape especially
2. **Font editor view** — open in Glyphs/FontForge, compare curves to reference
3. **H/V handles** — must stay at 100%
4. **Grid compliance** — must stay at 100%
5. **Comparison PNG** — overlay should show tighter alignment

## Status Summary

| Phase | Status | Impact |
|-------|--------|--------|
| 1. Levien algebraic fitter | Attempted, reverted | Best 0.907, baseline 0.920 |
| 2. fit_to_bezpath_opt | Blocked by Phase 1 | — |
| 3. Opticurve segment merging | Not started | — |
| 4. G2 harmonization | **DONE, active** | 0.919 (neutral) |
| 5. Circular arc detection | Attempted, reverted | Score dropped to 0.913 |
| 6. Remove dead code | **Partially done** | 30→2 warnings |

## Current Baseline (2026-03-01, updated)

| Metric | Score | Detail |
|--------|-------|--------|
| Overall | **0.925** | Tuned transition threshold + min section length |
| Shape | 0.767 | Hausdorff 9.3, mean 3.4 |
| Points | 0.966 | 30 vs 29 on-curve |
| Segments | 0.984 | 12c+16l vs 12c+15l |
| H/V handles | 1.000 | 24/24 (100%) |
| Grid (2) | 1.000 | 30/30 (100%) |

### Score Progression
| Change | Score |
|--------|-------|
| Original baseline | 0.920 |
| + G2 harmonization (Phase 4) | 0.919 |
| + transition threshold 0.3→0.37 | 0.921 |
| + min_section_len 40→50 | **0.925** |
