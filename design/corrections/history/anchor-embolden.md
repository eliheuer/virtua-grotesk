# 2026-08-04 — emboldening a script by outline offset

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


**Validate the weight model against known-good output first.** Before
pointing the emboldener at the Arabic, it was run on the Latin Regular and
compared to the real, hand-drawn Latin Bold. It reproduced every stroke
class to within 4 units, which is what made it trustworthy. If a transform
can be checked against something already correct in the same repo, check it
there before using it where you cannot tell.

**Measure the font's own weight rule, don't import the reference's.** Rubik
was the reference for *behaviour* (does the silhouette grow or does the
counter shrink? do zones rise with weight?), but every number came from
Virtua's own Latin Regular → Bold. Rubik's Light→Black is a far wider range
than 400→700, so its ratios were never transferable.

**Absolute offsets don't transfer between scripts of different size.** The
Latin's dx 48 / dy 36 made a Black out of the Arabic, because these Arabic
forms are ~25% shorter than the Latin (tooth 432 vs x-height 576). Scaling
the offset by the height ratio was the fix. Render 3–4 variants and look;
the right weight is a five-minute comparison, not an argument.

**Use the build's own filter as the oracle.** ufo2ft runs
`EraseOpenCornersFilter`, which DELETES points where an outline doubles
back. A generated Bold with open corners therefore stops matching the
Regular's point count and the build dies with "different number of
segments" and no useful location. Rather than guess which corners are
unsafe, import `glyphsLib.filters.eraseOpenCorners.EraseOpenCornersPen`,
run it on the candidate, and back the offset off for that glyph until it
reports nothing. Same trick applies to any generated-geometry pass: if a
build-time filter can silently change your output, run it yourself first.

**Coincident points are landmines for any offset.** Several green glyphs
repeat a point at a notch vertex. Offset the copies independently and the
zero-length segment between them reverses — an open corner. Give coincident
points a shared displacement. This one fix took `ain-ar.medi` from ×0.10
(effectively unbolded) back to full weight.

**Winding cannot be assumed, even inside one script.** The green Arabic
mixes CW and CCW outer contours, so a fixed normal direction emboldened
half the set and *thinned* the other half. Decide per contour from its own
signed area plus nesting depth.

**Component offsets may differ between masters — use that.** Bold marks are
bigger, so composites built with the Regular's offsets dropped below the
descent limit. Nudging the mark component in Bold only is legal and is the
right fix; it does not touch the skeleton.
