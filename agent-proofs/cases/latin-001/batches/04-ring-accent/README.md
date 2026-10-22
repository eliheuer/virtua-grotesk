# LAT-001 batch04 · Ring accent

Regular and Bold `ring` replace the inherited identical square outlines with
round outer and counter contours. `ringcomb` in each master receives only an
outgoing stack-anchor adjustment. Four source GLIFs change. The six-glyph reverse
closure per master is ring, ringcomb, Aring, aring, Uring and uring; none is green
or an Arabic dependency. All 1775 other source files are byte-identical, including
Arabic recursive donors, green drawings and the reversed-Nun calibration.

Regular outer/inner diameters are 176/112, centred at (152,728); Bold is 192/96,
centred at (152,736). Nominal extremum thickness is 32/48. Each master has two
compatible 12-point cubic contours. New outline coordinates are on8. These are
cubic circle approximations: sampled radial deviation is under1.1% in Regular,
and under2.8% in Bold, not a claim of mathematically exact circles. Five-weight
signed curvature profiles have no sampled reversals or tangent kinks and report
G2 joins. The nested radial bounds stay separated by at least31.11 units.

Incoming anchors and advances remain unchanged; legacy x150 anchors are retained
rather than snapped to the new x152 contour centre. The outgoing `top` anchors
in ring and ringcomb rise to848/864, 32 units above the new outer tops. Combining
wrapper grades stay unchanged; the redrawn spacing donors are purple. The20 grid
findings are retained anchors, advances and derived sidebearings; all new points
and new stack-anchor y values are on8. Eli's spacing reminder is recorded in
DESIGN.md and FEEDBACK.md for subsequent spacing work; no kerning changed here.

Whole-letter attachment/stack and Swedish/Czech reading rows were inspected at
400/550/700 against Before and Rubik, with224px/em details at both endpoints.
The square silhouette is gone; the counters remain open and the stacked marks
clear the larger rings. The ring walls are lighter than Rubik's in the enlarged
comparison. This is a pending human-review drawing decision, not visual approval.
Existing base-letter proportions, alternate carons, square diaereses and other
marks were not changed or approved by this batch.

Verification: complete master compatibility, changed compiled-ink closure,
90 shaped contexts at five weights, three Latin regression tests over VF/four
statics, endpoint curve lint and five-weight profiles. Frozen-baseline full-suite
comparison reproduces the same216 pre-existing Hebrew failing subcases, with
zero new or resolved failures. Build/preflight complete; preflight verifies
artifact presence, not release quality. Active and proof-candidate font tables
match except head timestamps. Online Fontspector was not rerun for this batch.

Exact before/candidate sources, source hashes, baseline fonts, signed profiles,
raster receipts and checks are retained. `apply.py` guards all frozen source
hashes before changing the four GLIFs. Next: breve and tilde, then bottom marks
and alternate carons, before the spacing/coverage and release-blocker queue.
