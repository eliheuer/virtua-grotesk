# Batch 03 — Bold Noon / ghunna bowls

Baseline `da883a7c`. Applied working trial; human review remains pending.

Refined Bold `noonghunna-ar` and `noonghunna-ar.fina`, retaining the shared
bowl construction. Axis-aligned handles replace slanted/twisted turns; exposed
chamfers are 16 units, joining cuts 8, sides 168 and bowl base 160. The final
left terminal is lower than the right, following the Regular skeleton. Final
descender is -256 instead of -300. `noon-ar` and `noon-ar.fina` advances now
follow their bases (752 / 784). The small `noonGhunna-ar` component inherits the
base correction without its source changing. All Regular bytes remain unchanged.

## Raster-driven correction

The first Bold six-font raster exposed a dot/stem collision. It is retained as
`rejected-dot-collision-700.png` with its original hash receipt. The final Noon
wrapper's unchanged circular dot moved from offset (248,-456) to (192,-288):
centered on the bowl at x=344, with 48 units of vertical clearance above the
320-unit terminal. This is a necessary collision repair, not a general marks
pass. Anchors remain unchanged. Regular's existing low final dot remains for
later placement review; no silent change to Regular was made.

Inspected corrected `detail-400.png` and `detail-700.png`: the Bold dot is clear
of the stem, its final bowl no longer has the crooked outer join, and counters
and terminal cuts remain visible. The endpoint sheets use `ننن ن` at 176 px/em
with all four references. Regular visibly matches its baseline. Human
script/design assessment is still required; the four references inform structure
without donating outlines.

Build/preflight passed. `verification.json` records 161 compiled shaping checks
at seven weights, unchanged glyph order/clusters/offsets, declared advance
changes, compatible masters and source/compiled component scope. Curve profiles
show no sampled curvature reversals or zero-speed warnings in the candidates;
intentional corners are retained. Grid exceptions are preserved x=340 anchor
positions in the isolated base; every new outline point and advance is on 8.
