# ARB-006 batch 08 — Final Lam correction (applied)

Eli reports that Lam still has issues in the 700 joined proof (2026-10-21).
The leftmost joined form is thin, has a joining-bar step, and lacks its descending
bowl. Batch 07 repaired three forms but left this visible structural problem.
Do not call a family checked/completed merely because its edited roots pass.

Scope: `lam-ar.fina` in Regular and Bold, 31 matching points instead of 14.
Prepared in scratch because Regular was green. Eli subsequently approved both
masters, explicitly including that green exception; the exact candidate is now
applied to the two active GLIFs.
The descending bowl follows the family's isolated shape, with 96/160 stems,
104/176 bottom weight, 96/176 joining bars, 16-unit exposed chamfers and an
8-unit lower branch cut. The incoming arm has a separate 96-square tangent
turn. Regular geometry is deliberately constructed on 8 (including center312
and right edge592), rather than importing isolated Lam's off-grid coordinates.
Regular advance744; Bold824. Anchors unchanged. Both candidates are purple,
not a human grade. Lam–Alef is separate and still unresolved.

## Verification and application state

Both scratch masters built to variable and static TTFs using the normal gftools
configuration and metadata fixup. Zero master-structure mismatches; both final
glyphs pass the 8-grid gate. Signed profiles have no sampled reversals or smooth
kinks; sampled proper crossings are zero. Seventy shaped comparisons across
seven weights preserve glyph identities, clusters and offsets, with only the
declared final-Lam advance difference. Compiled outline changes are confined
to final Lam. Active source hashes, including 18 Beh files, are unchanged.

Actually inspected the 400, 550 and 700 six-panel raster sheets and the large
Bold detail. The final bowl now descends consistently with the isolated form,
stem weights match, and the incoming bar is continuous without the old step.
A bounded 8-unit branch cut and 16-unit external chamfers remain intentional.
The live proof now labels the applied font Working. Application was approved;
this does not assign green or establish release readiness.

Applied after the explicit 2026-10-21 approval. `application.json` records the
exact source hashes and recomputed 18-file Beh reservation. Active build and
preflight passed; rerun verification confirms only final Lam changes in compiled
fonts at seven weights, with 70 shaping checks. The applied 700 raster is saved
separately; Lam–Alef remains unresolved. Next independent family: Meem.
