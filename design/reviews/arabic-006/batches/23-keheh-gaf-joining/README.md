# Batch 23 — initial and medial Keheh/Gaf in both masters

Applied working drafts under Eli's autonomous Arabic authorization; human review
is pending. Fourteen source files: `keheh-ar.init`, `keheh-ar.medi`,
`gaf-ar.init`, `gaf-ar.medi`, `gafsarkashabove-ar`, and advance-only updates to
`kehehThreedotsabove-ar.init` / `.medi`, in Regular and Bold. Exact before and
candidate bytes, hashes and the complete consumer closure are in `applied.json`.
No green consumers exist in that closure. Beh's 18 reserved files, manual Bold
hamza, isolated/final Keheh/Gaf and every other active source are unchanged.

## Construction

The old initial/medial forms used an upright Arabic Kaf structure with an
internal S-like sign; Gaf added another S-like shape overhead. These now follow
the angled Keheh head and separate Gaf bar established in batches 21–22.
The initial form retains the tangent bowl return; the medial form has an
incoming shoulder and a continuous baseline. Both retain the outgoing join.
Initial advances are 704, medial advances 832, in both masters. Bases have
23/21 points; the shared bar has eight points and advance 448. No external
outlines are copied. The deliberate 32-unit elbow flat, 8-unit inner landing
cut, 16-unit exposed cuts and 104/176-unit joining strokes remain explicit.

The donor has only two consumers per master: Gaf initial and medial. Their
placements are 192,0 and 320,0. Existing isolated local bars and final direct
outlines remain unchanged. Three-dot wrappers receive advance-only fixes;
their donor drawings, placements, anchors and human grades are preserved.
Other changed drawings/constructions are purple, awaiting human review.

## Verification and remaining findings

- Exact source scope and recomputed Beh dependency hashes guarded application.
- Matching contour/point types between masters and compatible component order.
- Signed curvature, continuity and sampled within/between-contour intersections
  checked on scratch decompositions. No unintended sampled reversals, tangent
  kinks or crossings at 400/475/550/625/700. The initial bowl's cubic join has
  about 4% curvature mismatch; line/curve transitions remain documented.
  The medial incoming edge is an intentional join boundary, not a smooth node.
- 805 compiled shaping comparisons at seven weights preserve substitutions,
  clusters and mark offsets; only the declared family outlines/advances change.
- Inspected joined-plus-isolated rasters at 400/550/700; endpoint word,
  medial-context and marked proofs; and large Gaf initial/medial renders in
  both masters, which expose the full Keheh base and separate shared bar.
  All four references remain configured. Readex lacks U+06A9/U+06AF and is
  explicitly unavailable; Plex 550 is labeled nearest supplied weight 500.
- Full rows show continuous joins without the old internal sign, medial
  underside notch or S-like overhead donor. The live proof is updated to this
  batch and saved at weight 700.
- Gaf's old propagated anchors were captured and made explicit before moving
  the donor, preserving existing compiled mark positions. Their top y1142
  and high bottom anchors are inappropriate for the new construction and
  remain attachment work; marked proofs visibly retain excessive separation.
- The grid gate reports 143 inherited findings, not a clean pass: preserved
  anchors, untouched three-dot donor points/offsets and inherited dot bounds.
  All new geometry and advances are on 8. `grid-exceptions.json` scopes this
  precisely; source curve lint has no crest/tension/kink flags.
- Preflight and post-build source/font identity are recorded in `preflight.json`.
  None of these checks establishes human approval or release readiness.

## Next

Heh/Goal/Doachashmee base forms are next, after checking colors and component
consumers. The separately drawn three-dot final Keheh remains a base follow-up;
three-dot donor/placement repairs and Gaf attachment remain later work.
Protected Arabic Kaf initial/final Regular and all Beh reservations stay frozen.
