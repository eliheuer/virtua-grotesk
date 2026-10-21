# Batch 15 — Bold isolated Ain/Ghain

Working drafts applied under autonomous authorization. Baseline `177a6abc`.
Only Bold `ain-ar` and `ghain-ar` change; both are purple pending human review.
All Regular bytes, manual hamza, and the complete 18-file Beh dependency
reservation remain unchanged. Exact source snapshots and hashes are retained.

## Construction

The old isolated Bold contained a reversing inner bowl curve, multiple tangent
kinks, inflated terminal cuts and an inconsistent wrapper advance. The new
45-point contour preserves the open-head/two-bar skeleton and compatibility.

The head is centered at x416; outer x192–640, crown y608; inner x352–480,
crown y448. These give 160-unit crown/side weights at the measured extrema.
The terminal bottom y368 sits 112 units above the middle bar top y256. Exposed
cuts are 16 units, following live green Bold H/E, rather than the old 34/36-unit
cuts. The left head-to-bowl transition deliberately retains its small vertical
landing and horizontal shelf. Smooth joins are not beveled.

The lower bowl has outer x64, inner x224; bottom y-240 and inner bottom y-80.
The middle and lower terminals are 160 units thick. Separate inner/outer handle
lengths preserve open apertures and tangency, following the manual hamza lesson;
no copied reference outline or universal radius formula is used. Both advances
are now 784. Ghain's existing dot is centered at x416 with local offset (264,32),
80 units above the head. Shared donor outlines and stored anchors are unchanged.
All new outline points, advances and offsets are on the 8-unit lattice.

## Checks and visual findings

- Inspected Ain and Ghain at 400/550/700 with all four actual reference fonts,
  plus `isolated-large.png` and `marks-700.png`. Plex 550 is explicitly labeled
  nearest supplied static weight 500. The head and bowl are cleaner at 700 and
  remain open through the intermediate. Their overall compact, upright form
  remains a draft for human review; numerical passes do not establish design approval.
- Signed profiles remove the sampled reversal and tangent kinks. Crown joins
  are G2; remaining G1 jumps include about 69% at the inner head-left transition,
  16% at the outer head-left, 27% at the inner bowl-left and 35% at the outer
  bowl-left. These are reported, not hidden or treated as all-G2 geometry.
  Terminal cuts and the left landing remain deliberate corners.
- No sampled within-/between-contour crossings at 400/475/550/625/700.
  Sampling is not exact certification. The existing Regular curve is not altered.
- `verify.py`: 455 shaping comparisons at seven weights. Stable substitutions
  and clusters; only declared widths and Ghain placement offsets change.
  Compiled changes are confined to the two isolated glyphs.
- Three grid findings are preserved inherited anchor coordinates (including
  the dot donor). No new outline or offset is off the machine lattice.
- Preflight completed build, print proof, reports and artifact checks. Zero
  blocking master mismatches; 510 width-only differences. Raster snapshot and
  rebuilt font differ only in head timestamp/checksum; hashes in `preflight.json`.

## Explicit remaining findings

The marked proof shows the **existing Ain/fatha collision** in both Before and
Working. The stored Bold Ain top anchor is (400,392), well below the crown.
It remains unchanged because base drawings precede the attachment pass. Ghain's
dot/damma stack stays visibly separated in this sample. The first 112 px marked
render exceeded its panel's vertical ink bounds; the saved 80 px render fits.
This is proof sizing, not evidence of a resolved attachment problem.

All four Bold Ain/Ghain forms now have first-pass repairs (batches 12–15), but
human review, the Regular initial Ghain advance mismatch, protected Regular
forms and later attachment/spacing work remain. Next: Seen/Sheen base forms.
Preserve Beh and all its donors. Do not rerun historical apply scripts over
subsequent human saves. This checkpoint is not release readiness or green grading.
