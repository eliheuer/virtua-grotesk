# HEB-008 — remaining Hebrew base letters

Current proof: `working-v7/`, served by `make proof-web` at
<http://127.0.0.1:60272/>. Its portable input is `evidence-v7.json`.
These are active working drawings, not final human approval or release readiness.

## Scope and recovery

Regular and Bold: Tet, Ayin, Alef, Tsadi, Final Tsadi and Shin; double Yod,
geresh and gershayim; attachment-anchor adjustments including Samekh, Qof and
Final Kaf. Exact 24-file source scope is in `validation.json`; original sources
are in `before-sources/`, and v5 sources in `final-sources/`. V6 supersedes only Shin and Final Tsadi;
its exact current four files are in `revision-v6/after-sources/`.
The application-v1 through application-v5 receipts record each bounded change.
V5 flattens double Yod into exact copies of the existing Yod outlines to avoid
nested compiled composites. Historical proof snapshots remain unchanged.

Eli accepted HEB-007 Gimel v4 as good enough to continue. Both manual Zayin
corrections, Regular Gimel and accepted Bold Gimel are preserved byte-for-byte;
`preserved-manual-edits.json` records their hashes.

After the computer restart, the live proof was refreshed from the current
compiled font (SHA-256 e38a34944099b0c9fc5df2057e2254981ac18822ed3385978a13f0a48c8c3777).
All final source snapshots and preserved manual edits were rechecked.
The server was restarted on 60272. Browser automation was blocked by URL policy,
so this restart did not include a new visual inspection of working-v5.

## Verification and remaining work

- `validation.json`: current compiled font, 6,076 mark/base clearance trials,
  no detected working overlaps; source colors and Unicode preserved.
- `hebrew-qa-v5.json`: zero compiled Hebrew check failures.
- `preflight-final.log`: completed build, proof, reports and artifact checks.
- `fontspector-final-v5.log`: 1 failure, 28 warnings; directory/package naming
  failure remains. These results do not establish Google Fonts readiness.

All 27 base/final letters now have a weight-development pass. Review the six
new letters in Compare and Text against Rubik; source application is not a
human design verdict. Next are niqqud, presentation forms, spacing and script QA.
Existing purple forms/marks remain protected by AGENTS.md. The earlier request
for a named exception is unresolved; do not overwrite them without that answer.
Use `parity-inventory.json` to locate the existing forms and source permissions.
Arabic has not started.

## Revision v6 — Shin and Final Tsadi

Eli: “the Shin and Final Tsadi look wrong, can we use forms more like rubik”.
Scope: Shin and Final Tsadi, Regular and Bold only. Preserve the previous
working drawings as Before. Trial: upright left stem and rounded lower bowl
for Shin; uninterrupted diagonal descender for Final Tsadi. Retain Virtua's
16-unit terminal chamfers, 8-unit draft grid and master-compatible construction.
Rubik is the structural reference, not an outline donor. Live green Regular o
provides on-axis bowl tangency; Bold n provides the 192-unit stem and fixed
16-unit chamfer model. Adapt curve extents to each Hebrew form rather than
copying or scaling whole Latin glyphs. Drawing and approval state pending.

V6 is now applied to both active masters. Source colors/Unicode and all unrelated
source bytes were preserved; exact before/after hashes and source copies are in
`revision-v6/`. Shin uses one 33-point contour; Final Tsadi one 20-point contour
in each master. All coordinates/anchors are on 8. Exposed terminals use 16-unit
chamfers; branch/stem intersections remain intentional corners, while marked
smooth joins have zero tangent-angle error. Shin's bottom anchors moved to −32
to clear the new −16 overshoot; Final Tsadi's below anchors follow the diagonal
descender. Existing protected presentation forms remain untouched.

Verification: preflight completed, no master-compatibility blockers, zero Hebrew
check failures, zero overlaps across 6,076 compiled mark/base trials at seven
weights. Compiled outline changes are only shinhb/finaltsadihb; only Final Tsadi's
advance changes. See `revision-v6/validation.json`, `grid.json`, curve reports
and `preflight.log`. Inspected compiled comparisons at 400/550/700 and running
words at 400/700; PNGs are FreeType/RAQM diagnostics, not browser screenshots.
The live proof uses the actual compiled font, with v5 as Before. Browser refresh
remains a user action because the previous browser URL-policy block is unresolved.
This trial awaits Eli's visual verdict; no grading or release approval is implied.

## Manual correction 01 — Regular Final Tsadi

Eli saved a Regular Final Tsadi correction and explicitly requested extracting
style lessons, recording them in context, then transferring them to Bold Final
Tsadi and both Shins. Preserve Regular Final Tsadi byte-for-byte. Exact files
are `revision-v7/agent-Regular-finaltsadi.glif` and
`revision-v7/human-Regular-finaltsadi.glif`; measurements/hashes are in
`revision-v7/manual-correction.json`. The human drawing has 25 points versus
the candidate's 20. Width, anchors, Unicode and source color are unchanged.

Measured correction:
- Outer turn now runs (328,240) → (528,448), with horizontal/vertical
  128-unit handles. Previously it began directly on the diagonal at (304,240),
  with an oblique first handle to (464,256).
- Inner turn ends at (328,336), with 64-unit handles on both ends, followed
  by a 72-unit horizontal shelf to (256,336). Previously it swept directly
  to the diagonal at (256,336), with unequal 64/96 handles.
- Inner/outer turns share their left endpoint x=328 and right tangent y=448.
  Extents are 104×112 and 200×208: near-square, not mathematically circular.
- Lower junction adds (312,232) → (320,240) → (328,240): 8-unit cut and
  8-unit horizontal landing before the smooth outer turn.
- Diagonal terminals gain 16-unit vertical landings at x=40 and x=504.
  Terminal edges shift inward by 8; the main straight runs remain distinct
  from the 16-unit, 45-degree chamfers.

Interpretation for this transfer: construct the turn as its own bounded shape,
then join it with a straight landing and deliberate cut. Do not stretch a curve
to an arbitrary intersection and call its unmarked kink intentional. This
reinforces the prior Gimel landing and Zayin balanced-turn examples. Exact
64/128 handles, shelf lengths and endpoint alignments are local evidence, not
a rule to impose on all curves. A source correction demonstrates geometry;
it does not by itself confirm every inferred explanation.

V7 transfer plan: keep existing widths and source colors. Bold Final Tsadi
retains outer y=240 and vertical tangent y=448, uses paired 128-unit outer
handles and a compact 48×48 inner turn with paired 32-unit handles; the inner
shelf rises to y=400 with added weight. Both Shins reuse these branch-turn
relationships with horizontal landings and 8-unit junction cuts. Their lower
bowls use paired quarter-turn geometry separated by a short flat, rather than
unrelated left/right handle lengths. These adaptations await visual review.

V7 is applied as a working trial. Only three active source files were written:
Bold Final Tsadi and Regular/Bold Shin. Regular Final Tsadi matches the saved
human snapshot byte-for-byte. No advances, anchors, source colors or unrelated
source bytes changed during the transfer. Final Tsadi has 25 matching point
types in each master; Shin has 40. All draft coordinates are on 8; curve/join
checks find no marked-smooth kinks. Unmarked human tangent flags are preserved.

Build/preflight and global compatibility pass. Compiled Hebrew checks have
zero failures, and all 6,076 mark/base trials are clear. Compiled outline
changes versus v6 are only shinhb/finaltsadihb, with no advance changes.
Inspected actual compiled renders at 400/550/700 and word samples at 400/700;
see `revision-v7/compiled-comparison.png`, `compiled-text.png`, `validation.json`
and `preflight.log`. These are FreeType/RAQM renders, not browser screenshots.
The live proof is `working-v7/`, with v6 as Before. Its Working Regular Final
Tsadi is the human edit; the other three are agent transfers, not approved
drawings. Existing protected presentation forms remain untouched.

## Continuation verdict and next phase

Eli said v7 looks better and requested committing the drawings and lessons,
then continuing the remaining Hebrew. Retain v7 as the working baseline, with
no automatic color grading. After basic Hebrew, Eli wants a whole-font grading
pass, then to consider a bounded unattended Arabic run. That run has not been
scheduled or started; its scope should come from the grading results.
