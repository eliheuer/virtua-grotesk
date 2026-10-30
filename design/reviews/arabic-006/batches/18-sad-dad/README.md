# Batch 18 — Bold Sad/Dad base forms

Baseline `e03640fb`. Authorized first-pass drawings, pending human review.
All four Bold `sad-ar` bases and their four `dad-ar` wrappers are repaired and
purple. Four orange Regular Dad wrappers change advance only. Regular isolated
Sad gains two collinear points on an existing straight edge for compatible
Bold terminal chamfers; its exact geometry and human grade are preserved.
All other source bytes, manual hamza and the 18 recursively reserved Beh files
are unchanged. Exact snapshots, candidates and hashes are retained here.

## Construction

Bold initial, medial and final Sad had the same outlines as Regular. The old
isolated Bold had a nearly closed, reversing counter, distorted cuts and tangent
kinks. This batch establishes consistent 160-unit tooth, bowl and head weights,
with 176-unit joining bars. The horizontal head spans x320–960 at y0–448 in
initial/medial, translated 568 units in isolated/final. The counter spans
x480–800 at y160–288, retaining a 128-unit opening. Exposed cuts are 16 units;
small inside cuts are 8. Curves use on-axis extrema and handles on the 8-grid.
This preserves the existing horizontal-head interpretation; the four references
show differing slopes and proportions and are not outline donors.

Bowl outer/inner lefts are x64/224; bottoms -256/-96. The bowl's right stroke
uses x640/800. Isolated and final retain their respective bottom runs. Two
extra line points in Regular isolated Sad, (140,150) and (80,150), subdivide its
existing horizontal segment from (156,150) to (64,150) without changing any ink.
The corresponding Bold points allow proper chamfers at both terminal corners.
This is an explicit inherited y150 grid exception in Regular, not new drawing
noise or an optical adjustment. Regular metadata and grading are unchanged.
Point counts now match at 55/38/48/65 for isolated/initial/medial/final.

Bold advances are 1592/1024/1056/1624. Dad now matches its base in each form;
previous wrapper widths caused visible gaps. Regular Dad advances likewise
match their unchanged bases: 1520/864/848/1328. Bold local dot offsets are
(488,-128) for initial/medial and (1056,-128) for isolated/final. These center
the existing near-circular donor over each head with 80 units of clearance.
The shared donor and its protected Regular counterpart are untouched.

## Verification and inspected evidence

- `verify.py`: 581 shaped comparisons at seven weights, stable glyph selection
  and clusters, only declared advance and interpolated dot-placement changes.
  Compiled outline/width changes stay within the named family. Regular source
  changes are checked as exact width-only edits or the two collinear insertions.
- Source hash checks preserve all unrelated files and all 18 Beh reservations.
  `apply.py` checks the entire baseline immediately before application.
- Signed profiles and combs for all four Bold bases: no sampled reversals,
  tangent kinks or contour crossings. Curve-to-curve extrema are G2 under the
  profiler; line-to-curve transitions retain G1 curvature jumps. This is not an
  all-G2 claim or visual approval.
- No sampled within/between-contour crossings at 400/475/550/625/700.
- Inspected Sad and Dad rasters at 400/550/700 with all four references. Plex at
  550 explicitly labels its nearest supplied static weight, 500. The former Dad
  gaps are closed throughout interpolation; Regular ink is visually preserved.
  Intermediate underside scallops inherited from Regular remain visible.
- Inspected large source renders for isolated/final, compiled word contexts
  `صبر ضرب`, final joins `بص بض`, isolated marks and marked joined forms.
  Head counters stay open, bowls and joining strokes are consistent at 700.
  The first 128px marked render exceeded its panel's vertical ink guard; it was
  regenerated at a shared 96px size, without clipping or changing any font.
- Grid report: 18 findings, all inherited stored anchors (including recursively
  reported component anchors). New Bold points, widths and local offsets are
  on 8. These anchor exceptions are retained for the attachment pass.
- Preflight completed build, print proof, reports and required-artifact checks:
  zero blocking master mismatches, 526 width-only differences. Snapshot/rebuild
  differences are only the head timestamp and checksum, checked by `verify.py`.

## Unresolved / next

Existing mark placement remains uneven: Sad final's stored top anchor x1684
lies beyond the new advance1624 and shifts its fatha toward the following form;
initial top y424 also predates the new y448 crown. The marked-joins raster is
saved for the later attachment pass. Dad inherits its dot donor's top anchor.
Do not infer general attachment correctness from an isolated clearance proof.
Regular Sad still has different head heights, unchamfered isolated terminal and
scalloped joins; these drawings were deliberately preserved in this batch.

Next bounded family: Tah/Zah. Continue reserving Beh and all recursive donors,
all green sources and manual corrections. This is a local working checkpoint,
not human approval, final grading or release readiness. Do not replay the
application scripts over later editor saves.
