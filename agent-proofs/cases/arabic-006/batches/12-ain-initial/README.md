# Batch 12 — Bold Ain/Ghain initial

Applied working drafts under the autonomous Arabic authorization. Human review
is pending. Baseline `af9e7f9b`. This is an **initial-only repair**, not a claim
that the four-form family is finished.

## Scope and construction

Two Bold GLIFs changed: `ain-ar.init` and its `ghain-ar.init` wrapper. All Regular
source bytes remain unchanged, including the green initial. The recomputed Beh
reservation has 18 files and all remain byte-identical, as do the manual hamza
correction and other sources. Both targets are purple pending human review.

The existing 31-point contour structure is retained for compatibility. The old
Bold has four smooth-node tangent kinks, an unintended reversal in its lower
inner turn, distorted cuts, and almost no gap between its head terminal and bar.
The new initial has a 160-unit crown and sides, a 176-unit outgoing joining bar,
16-unit exposed chamfers, and an 80-unit vertical mouth opening. Outer head
bounds are x32–512 and y272–496; the inner crown is y336. The lower shoulder
retains a deliberate 8-unit vertical landing before the joining shelf, keeping
that corner distinct from the curved turn. Advance is 560, with a 48-unit right
sidebearing. New outline points, handles, cuts and advance are all on 8.

Ghain follows the 560 advance and moves its existing dot locally by (120,-64),
centering it on x272 with 96 units of clearance above the new head. The shared
donor is unchanged. Anchors are preserved. Above-mark placement consequently
follows the existing donor anchor with its declared component offset; compiled
shaping checks record that change, rather than silently treating it as unchanged.

## Inspection and verification

- `ain-400/550/700.png` and `ghain-400/550/700.png` inspected with all four
  references: Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro.
  Plex at 550 explicitly uses the nearest supplied static weight, 500.
- `initial-large.png`: inspected the source silhouette, open aperture, chamfers,
  inner crown and shoulder. `joins-700.png`: initial forms joined to Beh with
  fatha/damma. No new visible collision or joining break in these samples.
  The longer 96 px sample was too wide and the short 128 px sample clipped the
  old high mark; the saved short 96 px proof passes the ink-bounds guard.
- `curve_profile.py` / `curve_lint.py --joins`: four old tangent kinks and the
  sampled unintended reversal removed. Remaining G1 curvature jumps are explicit
  (approximately 49% at inner left, 21% at outer crown and 56% at outer left).
  Chamfer corners and the shoulder landing are intentional. The coarse crest
  heuristic still flags this open form; it is not used as a visual verdict.
- `quality-check.py` and `interpolation-check.py`: no sampled crossings at five
  source weights. No claim of exact collision certification or all-G2 curves.
- `verify.py`: 385 shaping comparisons at seven weights, no missing glyphs or
  changed substitutions/clusters; only declared advances and Ghain component
  placement deltas. Compiled changes are restricted to the two initial forms.
- Nine draft-grid findings are retained existing anchors (including inherited
  donor anchors). No new outline or component offset is off the 8-unit grid.
- Before/candidate GLIFs, source hashes, font hashes, curve comb and raster
  receipts are retained. Do not rerun historical apply scripts over later edits.

`make preflight` passed build, print proof, reports and artifact checks. The
full report has zero blocking master mismatches and 508 width-only differences.
The rebuilt VF differs from the raster snapshot only in its head timestamp and
derived checksum; all other tables and head fields match. `preflight.json`
records both identities. This does not establish human approval or release readiness.

## Remaining family problems

The current medial and final loops visibly pinch at their lower counters and
use underweight joining bars; isolated Bold also retains its old lumpy head.
These are separate remaining repairs. Protected Regular medial/final sources
must not be changed without a named exception. Regular Ghain initial has an
existing advance of 468 around a 496-unit Ain base; its width and dot alignment
remain an explicit wrapper follow-up, not part of this Bold-only batch.

Next: Bold medial Ain/Ghain, then final and isolated forms. Preserve Beh and
all inherited donors reserved for Eli.
