# Batch 16 — Bold Seen/Sheen initial and medial teeth

Working drafts under autonomous authorization; baseline `f19ad424`.
Six Bold sources change: `seen-ar.init`, `seen-ar.medi`, and the corresponding
`sheen-ar` and `seenSixdots-ar` wrappers. All six are purple pending human
review. Exact before/candidate sources and full source hashes are retained.
All Regular sources, manual hamza and all 18 reserved Beh files are unchanged.
The Regular Seen initial and medial drawings are green and remain fixed.

## Construction

Before this repair, Bold initial/medial Seen coordinates were identical to
Regular. Their 88–96-unit teeth and joins therefore remained visibly thin at
700. The Bold draft uses three 160-unit teeth at x96–256,384–544,672–832,
384-unit crowns, 16-unit terminal cuts, 128-unit open counters and a 160-unit
floor. Joining edges span y0–176. A flat lower joining band replaces the old
scalloped/pinched underside. Existing 51/62-point topology is retained, including
collinear cubic slots, for compatibility with the protected Regular sources.

Initial advance is 896 (64-unit right bearing); medial is 928 with its incoming
edge on the advance. All four inherited wrappers match their respective base
advance. Dot groups are centered over x464 using local offsets (232,-160).
Shared donors are unchanged; Sheen's existing circular donor has 80-unit
clearance from the new crowns. No external outlines were copied.

## Verification and visual findings

- Inspected Seen and Sheen at 400,550,700 with Rubik, Noto Sans Arabic,
  IBM Plex Sans Arabic and Readex Pro; Plex 550 explicitly uses its supplied
  500 face. Also inspected large initial/medial source renders, compiled
  `بسب بشب` and marked `سَس شُش`. Open counters and joining edges remain visible.
  This is an AI first pass, not human approval.
- Curve profiles show no sampled sign reversals, tangent kinks or crossings.
  The two counter-bottom cubic joins are G2. Initial bottom-to-outer-turn
  remains G1 with a 100% relative curvature jump from its straight section;
  line/curve shoulders also retain reported curvature transitions. No all-G2
  claim is made. Collinear old corner nodes are not new visible corners.
- Five interpolated source weights have no sampled contour crossings.
  525 shaping comparisons at seven compiled weights retain substitutions/clusters; declared advance and
  local dot-placement deltas are checked. U+069C contexts exercise both
  additional inherited wrappers, not only Seen and Sheen.
- Three grid findings are unchanged inherited anchors: initial top/bottom
  x420, medial topDots y426. New outline coordinates, widths and offsets lie
  on the 8-unit lattice. Stored anchors are unchanged.
- Build, print proof, source reports and preflight completed. Zero blocking master mismatches; 515 width-only differences. Exact results
  and font hashes are in `verification.json` and `preflight.json`.

## Remaining work made visible by the proof

**Final/isolated forms are not repaired in this batch.** Final Seen is still
thin; the new medial-to-old-final junction has a weight/height step. Final
Sheen's advance is 1632 while its base is 1348, leaving an existing visible
joining gap. The four-form sheets deliberately retain this evidence. Next
batch must reconcile final and isolated geometry, widths and local dots.
Regular wrapper advance differences are also still present.

The existing Seen top anchor places fatha too close to the taller Bold crown;
contact is visible in the marked Working proof. Sheen/damma stacking also needs
later attachment review. Do not describe base improvements as attachment QA.

The inherited `seenSixdots` construction (U+069C) contains only the existing
three-dot-above donor, without a below group. This batch aligns its inherited
base and local placement; it does not claim to complete that character or
repair the donor's old lumpy curves. Keep it on the dependent-dot queue.

The first long joining sample exceeded the raster panel width. The saved
shorter `بسب بشب` proof uses the same size for all six panels and fits.
Do not rerun application scripts over later human saves. This checkpoint does
not establish release readiness or change human grading.
