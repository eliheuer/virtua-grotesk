# ARB-006 batch 08 — Final Lam correction (candidate)

Eli reports that Lam still has issues in the 700 joined proof (2026-10-21).
The leftmost joined form is thin, has a joining-bar step, and lacks its descending
bowl. Batch 07 repaired three forms but left this visible structural problem.
Do not call a family checked/completed merely because its edited roots pass.

Scope: `lam-ar.fina` in Regular and Bold, 31 matching points instead of 14.
Separate scratch candidate only: Regular is green and needs an explicit named
exception before active application. No active font source has been changed.
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
The browser proof is labeled Candidate. No claim of human approval or release
readiness. Full active-source build/preflight follows application if authorized.

A specific request to apply `lam-ar.fina` in Regular and Bold, including the green
Regular exception, is pending. Do not apply by heartbeat unless Eli grants it.
Other independent work may continue while preserving this candidate and Beh.
