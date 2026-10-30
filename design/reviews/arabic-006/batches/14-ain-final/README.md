# Batch 14 — Bold final Ain/Ghain

Applied working drafts under Eli's autonomous authorization; human review is
pending. Baseline `ea4e3208`. Only Bold `ain-ar.fina` and `ghain-ar.fina` change.
Both remain purple. All Regular source bytes, the manual hamza and the complete
18-file recursive Beh reservation are unchanged. Green Regular final Ain is
preserved. Exact before/candidate bytes and all source hashes are retained.

## Drawing decisions

The old Bold shelf doubled back into a spike. Its head and bowl also contained
multiple tangent kinks, duplicate junctions, and nearly Regular-weight sections.
The replacement uses the same head construction as batch 13, shifted +208 on x:
head center 560, crown y512, counter crown y352, 176-unit joining bar. The counter
has a 16-unit bottom flat at y192. Point types/counts remain compatible with
Regular: 48 outer and 16 counter points. Two cubic slots under the head now lie
on a straight baseline; they retain structure without retaining the old bump.
The profile calls two unmarked joins G0 although their geometry is collinear;
there is no kink there. Regular's duplicate nodes are not silently changed.

The descending bowl keeps the existing open, horizontal-terminal skeleton.
Outer left x64 / inner left x224 and bottom y-432 / inner bottom y-272 provide
160-unit extremum weights; the joining shelf is 176. Its axis-tangent turns have
separate extents and handles, following the measured hamza lesson rather than
forcing identical radii. This is not a claim of constant normal thickness
through every turn. The 16-unit exposed terminal cuts and 8-unit head shelf cuts
follow the live Bold H/E construction (H's (80,16)→(96,0) and internal
(272,304)→(280,312); E's terminal (656,0)→(672,16)). Donors are unchanged.

Both advances are 912 and the incoming edge reaches 912. Ghain's existing dot
moves locally from (398,-46) to (408,-64), centering at 560 with 80-unit head
clearance. Shared dot geometry and stored anchors remain unchanged. New outline
coordinates, advances and offsets are on 8. Eleven grid findings are inherited
anchors, including component-donor anchors; attachment remains a later pass.

## Evidence and checks

- Inspected all six Ain/Ghain reference rasters at 400, 550 and 700, plus
  `final-large.png` and marked `joins-700.png`. The head/bowl and joins are more
  coherent in Bold; the shelf spike is gone. The intermediate counter remains
  open, and these marked samples show no new visible collision. All four
  references are actual fonts; Plex 550 explicitly uses nearest static 500.
- Signed curvature has no sampled reversals or undefined derivatives; tangent
  kinks are removed. Remaining G1 curvature jumps are recorded: approximately
  43% at head outer turns, 50% at the small counter turns, 26% at the bowl outer
  left and 28% at the bowl inner left. Not an all-G2 claim. Chamfers/cuts remain
  deliberate corners. Curve profile, comb and lint output are saved.
- `quality-check.py` / `interpolation-check.py`: no sampled within- or
  between-contour crossings at 400, 475, 550, 625 and 700. Sampling is not an
  exact geometry certificate; raster review remains required.
- `verify.py`: 434 shaping comparisons across seven weights, stable clusters
  and substitutions, no missing glyphs. Only declared final-form advances and
  Ghain component-placement deltas occur. Compiled changes are confined to the
  two final glyphs. All unrelated source hashes and Beh reservations match.
- Preflight completed build, print proof, reports and artifact-presence checks.
  Zero blocking master mismatches; 511 width-only differences. Its rebuilt font
  differs from the raster snapshot only in head timestamp/checksum. Both hashes
  are in `preflight.json`; no release-readiness or human approval is implied.

## Next

Bold isolated Ain/Ghain still have the old lumpy, inflated head. Repair that
next, then continue the independent base families. Regular Ghain initial has
its previously recorded advance mismatch; green Regular Ain medial/final,
Regular medial Meem and Lam–Alef remain protected. Preserve Eli's Beh work.
Never rerun the saved preparation script over subsequent human saves.
