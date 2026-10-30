# Batch 19 — Bold Tah/Zah base forms

Baseline `1a746f5f`. Authorized first-pass working drawings, pending human review.
All four Bold `tah-ar` bases and four `zah-ar` wrappers are repaired and purple.
Regular initial/medial/final Tah each receive one collinear point for compatible
Bold junction chamfers; isolated Regular Zah changes advance only. Regular ink,
components, anchors and human grades are preserved. All other sources, saved
manual hamza and the complete 18-file Beh reservation are byte-identical.

## Construction and scope

The old isolated Tah was still Regular weight. Its Bold joining forms had
reversing collapsed counters, tilted/oversized stem cuts and a deep trough
between the stem and bowl. All four references show a connected stem/bowl
construction. The repaired Bold joins the crown directly to the stem with an
8-unit inside cut, retaining Virtua's horizontal, machined head interpretation.
The former shoulder's extra cubic segments become collinear horizontal runs to
retain compatibility with Regular. No external outlines were used.

Stems, head extrema and bars use 160 units; incoming/outgoing joining bars are
176 units. Stem caps end at y768 with 16-unit straight cuts. Head crowns are
at y448, counters y160–288 (128 units open). Joined counter bounds x288–768;
outer right x928 gives 160-unit side weight. Isolated uses a 72-unit horizontal
translation and retains its chamfered counter corners. Joined counters retain
rounded corners. The intermediate still inherits some Regular stem/bowl notch;
that is visible and not called resolved across the whole axis.

Bold advances are 1064/992/1024/1024 for isolated/initial/medial/final, with
matching Zah wrappers. Isolated Regular Zah is corrected from 1200 to 984,
matching its unchanged Tah base. The three extra Regular line points at
(192,192) subdivide existing vertical runs; exact insertion checks establish
no geometry or grading change. Compatible point counts are 29/46/49/49.

Zah's existing near-circular dot is positioned locally at (448,-128) isolated
and (376,-128) joined, centered at x600/x528 over the counters. Clearance over
the y448 crown is 80 units. The shared dot donor is untouched. This lowers the
previous floating Bold dots from above the ascender into the bowl area seen in
the references; the high Regular dot positions remain unchanged.

## Verification and inspected proofs

- `verify.py`: 637 shaped comparisons at seven weights. Stable substitutions and
  clusters; only declared width and interpolated component-placement deltas.
  Full compiled outline/width changes are confined to this family.
- Full-source hashes, exact candidate hashes and the recomputed Beh dependency
  reservation verified before application and checkpoint. Regular modifications
  are checked as exact collinear insertions or an advance-only replacement.
- Signed profiles/combs for all four Bold bases: no sampled sign reversals,
  tangent kinks or contour crossings. Medial/final right turns retain a 100%
  curvature jump where the compatible straight cubic meets the curved crown;
  line/curve transitions are also reported. No all-G2 claim is made.
- Sampled source interpolation has no contour crossings at 400/475/550/625/700.
- Inspected Tah/Zah joined-plus-isolated rasters at 400/550/700 against all four
  references, large isolated/medial source renders, `طلب ظرف`, `بط بظ`, and
  marked isolated `طَ ظُ`. Counters remain open, joined strokes continuous and
  terminal cuts visible at 700. Plex 550 explicitly uses nearest supplied 500.
- 24 grid findings are inherited stored anchors, including recursively reported
  donor anchors. All new points, advances and local offsets are on 8.
- Preflight completed build, print proof, reports and artifact checks: zero
  blocking master mismatches, 531 width-only differences. `verify.py` confirms
  the frozen after font differs from the rebuilt binary only in head timestamp
  and checksum; identities are recorded in `preflight.json`.

## Remaining findings and next

The existing orange Regular joining forms retain their deep stem/bowl trough
and high Zah dots; intermediate 550 reflects that geometry. A Regular refinement
is still needed before declaring the family complete. Isolated and joined
counter corner treatments differ. Mark attachment/stacking remains a later
pass; the isolated marked proof alone is not general attachment approval.

Next bounded base family: Kaf/Keheh/Gaf. Preserve Beh and every recursive donor,
all green sources and saved human edits. Do not replay old application scripts
over newer editor saves. This checkpoint does not establish human approval,
green grading or release readiness.
