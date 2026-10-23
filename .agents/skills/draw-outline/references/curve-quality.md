# Curve quality: inspect, diagnose, then alter

Use for curved outlines and weight transfers. The trigger is
[ARB-003 Bold hamza correction 01](../../../../agent-proofs/cases/arabic-003/README.md#manual-correction-01--bold-hamza-above).
Eli confirmed excess base mass/inflation and basic curve faults. Preserve his
source; diagnostics guide new candidates, not automatic cleanup of his edit.

## Working procedure

1. Preserve exact before/current GLIFs. Identify straight runs, extrema, turns,
   tangent continuations and intentional 16/8-unit cuts. Inspect unmarked joins
   too: a missing smooth flag does not prove a corner was intended.
2. Inspect **signed Curvature Comb** across whole turns: unintended reversals
   (an S-bend in a supposed convex turn), peaks, pinches and abrupt changes.
   Use the same outline scale and comb gain before/after. The comb measures
   curvature, not stroke thickness; measure opposing edges separately.
3. Inspect **Continuity** at joins. G1 means aligned tangents; G2 also matches
   signed endpoint curvature. No tangent kink does not imply G2. Preserve
   chamfer corners. A line can meet a cubic at G2 when the cubic's endpoint
   curvature is zero; this is not a reason to maximize every line/curve join.
4. Diagnose before choosing an operation below. Select one node/segment,
   try it on scratch, then recheck its neighbors. Retain silhouette, aperture,
   mass, anchors and cuts. Later join edits can disturb earlier adjustments.
5. After rounding, recheck tangency, curvature, intersections and grid. Editor
   integer/2-unit rounding is not Virtua's 8-unit draft grid. Never snap a
   human correction back to a formula. Record conflicting constraints.
6. Inspect both masters and intermediate weights, build, and review large
   glyphs plus reading-size carrier/context proofs. Metrics are not a grade.

## Choose the tool by the fault

| Tool | Purpose | Scope and limits in native RuneBender |
| --- | --- | --- |
| Curvature Comb | See turning behavior inside segments. | Sampling can miss narrow events; zero derivative means undefined curvature. Compare heights/sign rather than colors. |
| Continuity | Locate tangent kinks and curvature jumps at joins. | Check intended corners; do not make every join smooth. |
| Harmonize | Adjust neighboring handles at a tangent cubic/cubic join while retaining its on-curve node. | Select the smooth on-curve. Empty selection includes every eligible join. Recheck after rounding and neighboring edits. |
| Balance / Tunni | Adjust a cubic's handle proportions, retaining endpoints and handle directions. | Equal fractions toward the handle-ray intersection, NOT equal absolute lengths. Any selected point of a cubic includes it; empty selection includes all eligible segments. Can undo deliberate unequal handles. |
| Optimize | Explore broader handle adjustment on scratch. | Any selected point includes the whole contour. Actual code balances, searches low-popcount even coordinates and rounds to 2; not an 8-grid/G2/visual guarantee. |
| Simplify | Remove redundant structure within a selected run. | Preserve deliberate flats/cuts; topology changes need corresponding master changes and interpolation checks. |

## Headless tools for agents

From the Virtua repository root:

```sh
.venv/bin/python scripts/curve_lint.py Bold hamzaabove-ar --joins
.venv/bin/python scripts/curve_profile.py path/to/before.glif path/to/after.glif \
  --json path/to/curve-profile.json --svg path/to/curve-comb.svg
```

`curve_profile.py` is read-only: source hashes, signed sampled curvature,
endpoint jumps and one shared-scale SVG comb. It explicitly rejects components,
open paths and non-explicit-cubic contours. Decompose only on scratch as needed.
Interior sampling is not a proof of no inflections/cusps/intersections. Inspect
warnings and the SVG against intended shape; do not remove every sign change.

The older `curve_lint.py` crest heuristic may confuse different branches of
an open-shaped mark with a bowl. Its coarse tension ratio is not a comb.
`--joins` now prints classifications and signed curvatures previously hidden
behind tangent angles. `curve_continuity.py` is a legacy checker with unsigned
curvature and different tolerances (2 degrees/25%, versus native roughly
0.5 degrees/5%); its G2 labels are not equivalent evidence at sign reversals.

## Exact hamza evidence

- The AI lower-left turn reverses curvature; the human turn does not in the
  sampled profile. AI endpoint signs are opposite too. No-kink checks missed it.
- Inner join AI (88,952) has 11.1% relative curvature mismatch; human (88,944)
  matches signed curvature, G2, despite unequal handles.
- Human outer shoulder (16,960) retains 26.5% mismatch. Preserve it. Preferred
  shape is not an all-G2 score; do not optimize the human drawing away.

These are measured effects, not a claim Eli used particular commands. Handle
lengths and dimensions are local evidence, not defaults for all Arabic marks.

## Verified implementations and primary reading

Inspected native `/Users/eli/GH/repos/runebender` at commit
`5694c17647b91f69152c4bb16e74367c21a75088`, 2026-10-21. These files were clean:

- `src/analysis/curve.rs`: comb, continuity, harmonize, balance, optimize.
  G3 uses differences in Bézier parameter t, not arc length: a heuristic badge.
  G1Line is an implementation category, not a mathematical ceiling.
  `optimize_contour` does not call harmonize despite its stale doc comment.
- `src/font/babelfont/handle_cleanup.rs`: selection scope and canonical edits;
  closed ordinary cubic eligibility, preserved IDs, integer rounding for
  Harmonize/Balance and even-coordinate rounding for Optimize. Recheck if the
  implementation changes; do not rely on command names or comments alone.

Primary external references (read 2026-10-21; no plugin code copied):

- [SuperTool](https://github.com/simoncozens/SuperTool) and
  [user guide](https://www.simon-cozens.org/Supertool.pdf): curvature view,
  local harmonization, Tunni manipulation, balancing and stem thickness.
  Local work matters because changing a later join can disturb an earlier one.
- [Cozens' derivation](https://gist.github.com/simoncozens/3c5d304ae2c14894393c6284df91be5b):
  moving the joining node versus translating its adjacent handles.
- [Glyphs: Harmonization](https://glyphsapp.com/learn/harmonization): point
  placement, inner/outer curve relationships and joins are separate concerns.
  Speed Punk visualizes; Green Harmony moves nodes; Grey Harmony moves handles.
  Borrow geometric diagnostics, not the tutorial's calligraphic silhouette.
- [Curvatura](https://github.com/linusromer/curvatura): related harmonization,
  Tunni and inflection tools; consult its docs for operation details.

## Paired-edge weight: failed double-spiral at experiment, 2026-10-23

Eli rejected the second at candidate as lumpy despite its clean sampled tangent
checks. The local optimizer penalized individual-edge curvature and join jumps,
but not opposing-edge width; it fixed all traced spiral on-curves. The failure
is recorded in [feedback correction 02](../../../../agent-proofs/FEEDBACK.md).

For a nominally monoline curved stroke, diagnose three different things:

1. Each edge's flow over the full turn, using signed combs and plain silhouette.
2. Adjacent-segment transitions, using continuity checks.
3. The relationship between opposing edges: visible ink weight and white-space
   rhythm, supported by width measurements perpendicular to the stroke.

Do not infer item 3 from items 1 and 2. Pair the intended opposing branches
explicitly in spirals; arbitrary nearest-edge distances can cross a white gap
or hit another turn. Constant geometric width is a useful construction starting
point, not a replacement for optical correction or filled-text inspection.
Preserve the agreed form, not every accidental traced node. A visible swelling
is grounds to reject a candidate even if grid, compatibility and joins pass.
See the primary Glyphs harmonization and good-path guidance linked above.

## Broad flow is a separate review — AT-001, 2026-10-23

Eli rejected the paired-width revision too. [AT-001](../../../../agent-proofs/cases/at-001/README.md)
retains the rejected source pairs, his reference context and the r4 redraw.
Eli called r4 “better, but still bad” and authorized application for hand editing;
application does not make it a positive optical example. A locally fair, evenly thick stroke can still follow a visibly poor path.

Before optimizing joins, compare the full filled silhouette with the selected
reference. Identify flat sections, tight bends, swelling and white-space rhythm.
If fixed traced points preserve those defects, reconstruct the broad sweep on
scratch within the named scope. Preserve the agreed identity/topology, not every
traced node. Then check opposing edges together, adjacent joins, extrema and grid.
Reinspect the complete glyph and actual words after snapping: independently
rounding two edges can change stroke weight even when every point is on-grid.

Use `harness/paired_stroke_report.py` with explicit, hash-bound cubic pairing.
It retains ambiguous or missing normal intersections and supplies no optical
pass threshold. Local width ranges, continuity labels and curvature variance
cannot replace the filled proof. Directional weight, junction relief and terminal
taper are explicit design choices; do not minimize them away to get a score.
Record human verdicts with exact snapshots. Pending candidates are not accepted
training examples; updating these instructions does not train model weights.
