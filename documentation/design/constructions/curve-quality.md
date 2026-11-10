# Curve quality

Use this procedure for curved outlines and for weight transfers. It comes
from Eli's corrections of Bold `hamzaabove-ar` and of the `at` sign in
October 2026. Their records are in the Git history before commit 1db2dfc7.

## Procedure

1. **Look at the whole filled shape first.** Compare it with the selected
   reference. Find flat sections, tight bends, swellings and the rhythm of
   the white space. A stroke that is smooth and even in thickness can still
   follow a poor path. If the existing points keep such a fault, redraw the
   broad curve, and keep the agreed form and topology.
2. **Read the signed curvature along each turn.** Use the curvature comb in
   Runebender at the same scale before and after. Look for reversals inside a
   turn that should be convex, peaks, pinches and abrupt changes. The comb
   shows curvature, not stroke thickness.
3. **Check the joins.** G1 means the tangents align. G2 means the curvature
   also matches. Keep the 16-unit and 8-unit chamfer corners. Do not make
   every join smooth, and do not make every smooth join G2.
4. **Check the opposing edges together.** For a stroke of even weight, the
   two edges must keep the visible weight even. Clean edges and clean joins
   do not show this. A visible swelling rejects a candidate even when every
   check passes.
5. **Change one node or segment at a time.** Then check its neighbors again,
   because a later edit can undo an earlier one.
6. **Check after rounding.** Rounding two edges separately can change the
   stroke weight even when all points are on the grid. Never snap Eli's
   corrections back to a formula.
7. **Check both masters and the intermediate weights,** then the glyph in
   words at reading and display sizes.

## Runebender tools

| Tool | Use | Limit |
| --- | --- | --- |
| Curvature comb | Curvature inside segments. | Sampling can miss narrow events. Compare height and sign, not color. |
| Continuity | Kinks and curvature jumps at joins. | Corners can be intended. |
| Harmonize | Adjust the handles at a smooth cubic join and keep the node. | Check again after rounding and after neighboring edits. |
| Balance (Tunni) | Adjust the handle proportions of a cubic. | Equal fractions, not equal lengths. It can remove intended unequal handles. |
| Optimize | Try broader handle changes on a scratch copy. | Rounds to 2 units. Not a guarantee of grid, G2 or visual quality. |
| Simplify | Remove redundant points. | A topology change must be made in both masters. |

## Headless checks

```sh
.venv/bin/python scripts/curve_lint.py Bold hamzaabove-ar --joins
.venv/bin/python scripts/curve_profile.py before.glif after.glif --svg out/comb.svg
.venv/bin/python scripts/paired_stroke_report.py glyph.glif pairs.json --output out/widths.json
```

`curve_profile.py` writes the signed curvature of two GLIFs on one scale.
`paired_stroke_report.py` measures the width between the edge pairs named in
its plan file. Neither gives a pass threshold. The filled proof decides.

## Evidence from the hamza correction

- The agent's lower-left turn reversed its curvature; Eli's did not. A check
  for kinks did not find it.
- Eli's outer shoulder keeps a curvature mismatch at one join. Keep it. The
  preferred shape is not the one with the most G2 joins.

## Rule entries

### On-curve points at extrema

Every crest, trough and side extreme of a curve has an on-curve point with a
horizontal or vertical tangent.
Seen in: asciitilde (56f4b437), section (22ccd03a), b d (dec6b4b3).

### Smooth flags

A line that continues into a collinear handle is a smooth point. A corner is
only a deliberate kink.
Seen in: Eli's instruction (372bb48e).

### Handle lengths

Compensated handle pairs keep the form. Handles within one segment stay of
similar length, and the lengths follow the proportions of the glyph.
Seen in: Eli's instruction in `design/reviews/latin-worklog.md`, in the Git
history before commit 1db2dfc7.

## Reading

- [SuperTool](https://github.com/simoncozens/SuperTool): curvature view,
  harmonization, Tunni and balance.
- [Glyphs: Harmonization](https://glyphsapp.com/learn/harmonization).
- [Curvatura](https://github.com/linusromer/curvatura).
