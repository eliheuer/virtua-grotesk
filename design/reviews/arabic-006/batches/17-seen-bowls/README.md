# Batch 17 — Bold Seen/Sheen final and isolated forms

Baseline `35cd5bb2`. Authorized working drafts, pending human review.
Six Bold files change: `seen-ar`, `seen-ar.fina`, and their `sheen-ar` and
`seenSixdots-ar` wrappers. These remain purple. Two orange Regular final
wrappers (`sheen-ar.fina`, `seenSixdots-ar.fina`) change **advance only**;
their human grades, components, outlines and anchors are preserved.
All other sources, manual hamza and all 18 reserved Beh files are byte-identical.
Exact before/candidate GLIFs and full source hashes are in this batch.

## Construction and scope

Final Seen was identical in Regular and Bold. Its joining stroke and teeth
therefore stayed thin at 700. The old isolated Bold also had reversing inner
turns, tangent kinks and enlarged terminal cuts. Both now use the batch 16
160-unit teeth, 128-unit counter openings, crowns at y384 and 16-unit exposed
chamfers. Tooth spans are x640–800,928–1088,1216–1376. The final incoming
join spans y0–176 and ends on the advance, matching the medial form.

The bowl has outer left x64, inner left x224; bottom y-256, inner bottom y-96.
The inner right at x640 and outer right at x800 carry the same 160-unit weight.
An 8-unit cut separates the bowl's outer landing from the tooth floor.
The isolated bowl retains a continuous curved bottom; the final retains its
short horizontal bottom runs. Neither is forced onto an equal-radius recipe.
The 58/70-point topology remains compatible with the unchanged Regular drawings.

Bold isolated advance is 1440 and final is 1472; all corresponding wrappers
match. Local dot offsets (776,-160) center the existing groups at x1008 above
the teeth, with 80-unit clearance for Sheen's circular donor. Shared donor
geometry is untouched. The existing U+069C missing-below-group issue is not
resolved by aligning its wrapper.

Regular final wrapper advances were 1632 while the base advance was 1348,
creating a visible gap even at 400. Both are now exactly 1348, closing the
inherited gap throughout interpolation. This is a metrics-only correction,
not a redraw or grade change. The inherited base width is off the 8-unit draft
lattice; matching it is a recorded exception to preserve its drawing and join,
not an excuse to resnap the Regular source. `regular-wrapper-metrics.py` records
the separate hash-guarded correction after the Bold preparation.

## Checks and inspected evidence

- `verify.py`: 525 shaped comparisons at seven weights. Stable substitutions
  and clusters; only declared width/component-placement deltas. The two Regular
  changes are checked against exact advance-only text replacements. Compiled
  changes stay within the six named glyphs and their two Regular metrics.
- Inspected 400/550/700 Seen and Sheen rasters with all four references;
  Plex's 550 panel explicitly labels the nearest supplied static face (500).
  The new 700 string is continuous and consistent across all four forms;
  the Regular and intermediate Sheen gaps are also closed. Intermediate curves
  still inherit Regular's scalloped underside; no human approval is inferred.
- Inspected `isolated-large.png`, `final-large.png`, 144px final joins `بس بش`,
  words `سمسم شمس` and marked isolated `سَ شُ`. The counter openings, bowl
  weight and terminal cuts are visible; no missing final bowl or broken join
  remains in those samples. Near-circular dot drawings remain unchanged.
- Signed curve profiles: no sampled sign reversals, tangent kinks or contour
  crossings. Isolated inner bottom has an 11.4% G1 curvature jump; outer bottom
  7.1%; straight underside to outer tooth turn 100%. Line/curve transitions
  are reported too. These are not claimed to be an all-G2 design.
- No sampled contour crossings at source weights 400/475/550/625/700.
  Sampling and passing numerical scores are not substitutes for visual review.
- Six grid findings are inherited stored anchors. All new Bold outline points,
  widths and local placements lie on 8. Regular metrics exception noted above.
- Preflight completed build, print proof, reports and artifact checks: zero
  blocking master mismatches, 520 width-only differences. `preflight.json`
  records snapshot/rebuild hashes and timestamp-only differences.

## Remaining findings and next step

The isolated marked proof has clearance at 700 after lowering the crown from
the old y460 to y384. This does **not** resolve the low initial/medial Seen
fatha position recorded in batch 16, nor certify stacking generally. Attachment
and diacritic design remain later work. U+069C still lacks its lower dots and
uses an old upper donor; it remains on the dependent-dot queue. Existing Regular
initial wrapper metrics and isolated/final height differences still need review.

All four Bold Seen/Sheen base forms now have first-pass repairs in batches 16–17.
Next: Sad/Dad base forms, then Tah/Zah. Preserve Beh and every recursive donor,
all green drawings and manual corrections. Do not rerun old application scripts
over later human saves. This checkpoint is not release readiness or green grading.
