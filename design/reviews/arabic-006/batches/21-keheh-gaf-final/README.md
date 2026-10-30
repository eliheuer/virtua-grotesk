# Batch 21 — Keheh/Gaf final forms, both masters

Working drawings applied under Eli's autonomous Arabic authorization; human
review is pending. Four files only: `keheh-ar.fina` and `gaf-ar.fina` in Regular
and Bold. Regular targets were orange and Bold red; these new drafts are purple.
No green source or descendant is involved. Neither final glyph has component
descendants. All other sources, manual Bold hamza and the recomputed recursive
18-file Beh reservation are unchanged. Exact baseline/candidate bytes and hashes
are retained in `applied.json` and the source snapshot folders.

## Diagnosis and repair

Both final forms duplicated an upright Arabic Kaf with an inner S-like sign;
final Gaf lacked its distinguishing bar. Rubik, Noto Sans Arabic and IBM Plex
Sans Arabic show the angled Keheh structure and separate Gaf bar. The existing
bowl and incoming-join role are retained, while the wrong upper construction is
replaced with a straight angled head and descending arm. No reference outlines
were copied. Readex Pro lacks U+06A9 and U+06AF; its panel is explicitly unavailable,
not replaced by a fallback or a mislabeled font.

The shared final construction has 29 points, with 96/160-unit left uprights,
104/176-unit base and joining bars, 16-unit terminal cuts and an 8-unit inner
landing cut. The outer elbow is blunted by a 32-unit vertical cut. The first
raster exposed a rounded protrusion at the inner junction; a straight landing
replaced it. Large inspection then exposed a pointed outer elbow, removed in
both masters. `gaf-first-trial.png` records the earlier trial, not final evidence.

Both advances are 960. Gaf adds a separate eight-point upper bar, with a 48/80-unit
vertical thickness and top at 880/912. This is an integral letter distinction,
not a change to the shared `gafsarkashabove-ar` donor. Upper-arm and bar proportions
remain drafts for human review. Existing anchors remain unchanged; four grid
findings are the two Bold bottom/bottomDots anchors at y=-12 in each glyph.
All new outline points, handles, cuts and advances are on the 8-unit lattice.

## Verification and raster evidence

- Matching master structure: Keheh one 29-point contour; Gaf 29+8 points.
- Signed profiles show no sampled reversals or undefined/kinked curve joins.
  Curves meet the adjoining runs tangentially; line/curve curvature jumps remain
  explicitly recorded. Intentional angled corners are not smoothed away.
- No sampled contour crossings at 400/475/550/625/700, including Gaf's upper bar.
- 728 compiled shaping comparisons and outline verification at seven weights scopes every change to
  the two final glyphs. Substitutions, clusters and offsets remain stable; only
  the declared advances change. Beh and manual corrections remain byte-identical.
- Inspected final joins at 400/550/700, both endpoint full-form rows, `نمک سنگ`
  contexts, marked finals, and large Regular/Bold source details. Plex at 550
  explicitly uses its nearest supplied static weight, 500. All four references
  remain configured; Readex's missing coverage is clearly labeled.
- Required preflight and post-build identity checks are recorded in
  `preflight.json` and `verification.json`. These are technical checks, not
  human approval, complete script QA or release readiness.

Final joins are continuous and Gaf's upper bar remains separated through the
sampled weights. The full-form proofs deliberately expose the remaining old
isolated/initial/medial drawings. Marked final samples do not show collisions,
but attachment/stacking has not been comprehensively reviewed.

## Next bounded work

Adapt isolated Keheh and its Gaf/three-dot wrappers, checking recursive
protection and their grades before any shared-root change. Then initial/medial
forms and the inappropriate hamza-like Gaf donor. Do not repair that donor
without accounting for its other inherited forms. The separately drawn
`kehehThreedotsabove-ar.fina` remains old construction and needs its own follow-up.
Protected Regular initial/final Arabic Kaf are distinct sources and stay frozen.
Keep Beh and all reserved donors untouched.
