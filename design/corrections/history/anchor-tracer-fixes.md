# 2026-07-29 — img2bez upstream fixes #1 and #2 SHIPPED (b5cb87d)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


- img2bez now writes surgically (only the target .glif + contents entry
  for new glyphs) and normalizes winding on output (outer CCW/holes CW by
  nesting parity, with a type-shifting Contour::reverse). Verified on the
  section retrace: 2 files touched (was 638), correct winding unaided.
  Three regression tests in img2bez.
- Remaining upstream: sheet mode (anchor calibration + segmentation),
  synthetic-bold with counter guard, extrema/point-economy on traces
  (section's bottom missed an extremum and wastes points), continuity
  report in trace JSON, and normalize_start order (img2bez uses
  bottom-then-left; the font's START RULE is left-then-bottom).
- **section is marked ORANGE** (Eli's review): raw trace lacks Virtua's
  chamfer terminals and runs light — the STYLE-REFIT stage (harness rules
  / virtua-12m, possibly built on img2bez font/refit.rs which already
  does structure-preserving raster refits) is the missing piece and the
  next build.
