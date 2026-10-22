# Final three-dot Keheh — focused working draft

Eli authorized `kehehThreedotsabove-ar.fina` in Regular and Bold on 2026-10-21,
requesting both weights, all four reference slots and whole-image inspection.
Only these two source files are in scope. They had the upright Arabic Kaf body
with an inner sign and no dots. The candidate instead composes `keheh-ar.fina`
and `threedotsupabove-ar`, with advance 960. No donor was modified.

The complete image was inspected at 400, 550 and 700, plus enlarged 400/700
final forms, the entire four-form row, and Beh/Lam/Meem joining contexts. This
caught an initially too-high final dot group; final offsets 216,72 (Regular)
and 216,40 (Bold) align it to the other forms within two units on the draft grid.
The angled head, open bowl and baseline join now belong to the same construction
as the other forms. The former reversing bowl curves and lower join notch are
absent. The existing donor retains tangent curves and exposed chamfers.

All four reference slots are retained. Noto Sans Arabic and IBM Plex Sans Arabic
cover U+0763; supplied Rubik and Readex do not and are explicitly unavailable.
No fallback is rendered. Plex 550 uses its nearest supplied 500, clearly labeled.

This is not human visual approval. The dots remain considerably larger and more
widely spaced than the references, consistent with the current Virtua family.
Their shared donor and the other forms were not redesigned. Existing final top
anchor y768 is below the new dot crown and needs the later attachment pass; no
mark-placement resolution is claimed. The base is inherited purple work, not a
green design reference. Its flat-bottomed bowl and angular silhouette remain
subject to Eli's judgment.

Verification checks exact source hashes, all 34 Beh/Heh reserved source files,
matching component order and donor point types, and compiled changes restricted
to the final U+0763 glyph. Thirty shaped comparisons at three weights preserve
substitutions, clusters and mark offsets, allowing only intended advance changes.
Curve lint of both donors records tangent line/curve joins and G2 dot joins;
these metrics do not establish drawing quality. All green sources, manual hamza,
Heh/Doachashmee and Beh remain untouched. See candidate.json, verification.json,
preflight.log and the PNG hash receipts for exact evidence.
