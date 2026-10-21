# Batch 22 — isolated Keheh/Gaf in both masters

Applied working drafts under Eli's autonomous Arabic authorization; human review
is pending. Six source files: `keheh-ar`, `gaf-ar`, and advance-only updates to
`kehehThreedotsabove-ar`, in Regular and Bold. Recursive component inspection
finds no other descendants or green consumers. The full 18-file Beh reservation,
manual Bold hamza, shared dot donors and `gafsarkashabove-ar` are unchanged.
Exact snapshots, source hashes and closure are in `applied.json`.

## Construction

The old isolated forms were upright Kaf duplicates with an internal S-like sign;
Gaf added another S-like donor overhead. The angled head, deliberate elbow flat,
inner cut and Gaf bar follow batch 21's final construction. The incoming join is
replaced with an isolated bowl returning tangentially into the descending arm.
This preserves the bowl role while correcting the wrong upper structure; no
external font outlines are copied.

Keheh now has one 31-point contour in each master. Gaf retains its Keheh base
component and adds a local eight-point bar, avoiding changes to the shared donor
while its initial/medial consumers are unfinished. Advances are 960. Uprights
are 96/160 and base weights 104/176; exposed cuts remain 16 units and the small
inner landing cut 8. The right bowl has an explicit extremum and aligned
handles. Local handle adjustment reduced its cubic-to-cubic curvature mismatch
to about 4%, without forcing equal handles or moving the extremum off the grid.

The three-dot wrappers retain their exact components, placements, anchors and
human grades; only advances now match the inherited base. Their donor and dot
placement still need the later dot pass. Keheh/Gaf redraws are purple.

## Attachment scope

Gaf's old propagated anchors were captured before removing its S-like donor and
made explicit on the wrapper. This preserves compiled mark positions while the
letter silhouette changes. Those inherited anchors are visibly inappropriate
for the new bar (top y1142; bottom y854 Regular/y798 Bold) and are explicitly on
the attachment queue. They are not claimed correct. Keheh anchors and three-dot
placements remain unchanged. The grid report has 54 inherited findings across
anchors, component offsets and the unchanged dot donor; all new geometry,
handles, widths and sidebearings are on 8.

## Verification

- Exact six-file source scope and reserved-source hashes checked at application.
- Matching master structure; Gaf's component and local bar stay compatible.
- Signed profiles and sampled intersections checked using scratch decompositions
  (never saved over component sources), at 400/475/550/625/700. No sampled
  reversals, tangent kinks or crossings; remaining line/curve curvature jumps
  are retained in the reports.
- 777 compiled shaping comparisons across seven weights. Changes are restricted
  to these three isolated glyphs; substitutions, clusters and mark offsets are
  preserved. Only declared advances change.
- Inspected 400/550/700 isolated rasters, both endpoint four-form rows,
  `درک رگ` isolated-word contexts, marked forms and all six large source details.
  Four references remain configured; Readex lacks U+06A9/U+06AF and is explicitly
  unavailable. Plex 550 is labeled with its nearest supplied static weight,500.
- Large source details confirm the tangent bowl return and the separate bar.
  The inherited three-dot group sits high/left; the Bold lower dots have a
  measured 64-unit horizontal gap (the initial visual reading of touching dots
  was incorrect). The
  fixed source canvas clips the upper dot, so additional taller-canvas proofs
  retain the complete group. Preserve this as a known donor/
  placement problem for the later dot pass, not a completed composite review.
- `کاج گل` word proofs intentionally show the still-unfinished initial forms;
  the isolated-word proofs show this batch's actual change.
- Preflight and final source/font identity are recorded in `preflight.json`.
  These checks do not establish human approval or release readiness.

## Remaining work

Initial/medial Keheh/Gaf and their shared S-like Gaf donor remain wrong. Treat
that as the next bounded family after the isolated proof; inspect every consumer
before changing the donor. The separately drawn three-dot final is another
follow-up. Protected Regular Arabic Kaf initial/final remain frozen. Dot groups,
attachment and comprehensive script QA follow base-form completion.
