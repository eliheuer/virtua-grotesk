# LAT-001 batch08 · Comma-accent weight and terminals

Only the Regular and Bold `commaaccent` donor outlines change. The previous
six-point notched polygon was identical in both weights. Both now use convex
eight-point contours with parallel diagonal sides, horizontal end landings and
16-unit corner cuts. Nominal horizontal stroke widths are64 Regular and96 Bold;
normal thicknesses are approximately62/93. Bounds are x96–192 Regular and80–208
Bold, y-200..-40 in both. The8-unit deeper bottom allows complete cuts without
shortening the main diagonal. Outlines and all cuts are on8. Donors are purple
pending human review; wrappers and their human grades remain unchanged.

The expanded consumer closure has16 glyphs per master, including the ten Latvian
wrappers repaired in batch07 and Romanian ȘșȚț. None is green or in the326-source
Arabic reservation. Every other source file (1777 total) remains byte-identical:
all advances, anchors, component transforms, green base drawings, Arabic/manual
donors, the reversed-Nun dot compensation and feature code are preserved.

The rotated mark on ģ retains24 units above the bowl, now reaches y776, and has
24 units below its outgoing top anchor800. The below donor has24 units before
its outgoing bottom anchor-224. Compiled stack checks verify that these margins
remain clear at five weights. The incoming x140 anchors and advance260 are
legacy exceptions; the new contour center is144. Grid QA records four findings
per master: advance260, both x140 anchors and resulting off8 right sidebearing.
No legacy metric was silently snapped to make the report pass.

Whole attachment, Latvian/Romanian reading and stacking rasters at400/550/700,
and224px/em endpoint letters, were inspected against actual Rubik. The notched
stubs are removed, and Bold marks now visibly gain weight with their letters.
Regular remains smaller/lighter than Rubik. Final size, spacing and optical
alignment remain human review judgments. No reader approval is claimed.

The complete attachment row also exposes an inherited **generic g + U+0326
collision** inside the descender, present in both Before and Working. This is
separate from Latvian ģ and its repaired stacking anchors. The green base g has
its bottom anchor at y0; its drawing/anchors were preserved. `geometry.json`
records the overlapping bounds at five weights. This batch does not fix or
approve generic below-mark attachment on descenders. Keep it on the attachment
queue and respect green protection when selecting a repair.

220 scoped comparisons cover canonical NFC/NFD/fallback, advances, unaffected
script/cedilla text, and above/below stack clearance. Changed compiled ink is
exactly the16-glyph donor closure. Complete master compatibility and convex,
non-intersecting contours pass at five weights. These polygons have no cubic
curves; curve lint is retained but does not certify their design quality.
Four Latin tests pass across VF/four statics. Frozen-baseline engineering tests
reproduce the same216 Hebrew failures with zero new or resolved failures.
Active build/preflight completed, and candidate/active VF tables match except
head timestamps. Online Fontspector was not rerun. Local checkpoint only.

Next: cedilla, then ogonek and alternate carons, plus the maintained attachment,
spacing/coverage and release queue. Preserve the rotated ģ construction and
review all consumers before touching a shared donor.
