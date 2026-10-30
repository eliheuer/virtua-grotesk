# HEB-004 — Pe and Final Pe

2026-10-19. **Candidate v1 approved and applied to both active masters.**
The following inspection records the starting state.
Eli approved HEB-003 and asked “next?” This pair follows naturally from the
new Kaf bowl and Final Kaf descender. Open `make proof-web` (localhost:60272).
Current includes the approved HEB-003 changes; Rubik/Noto hashes are unchanged.

Scope: פ Pe U+05E4 (`pe-hb`), ף Final Pe U+05E3 (`finalpe-hb`) in both masters.
Each has one contour. Pe has 24 points and advance 556; Final Pe has 16 points
and advance 548. Both outlines and advances are identical between Regular and
Bold. Tops are 576; Final Pe descends to −182. Source hashes and point listings
are retained in [source-inspection.json](source-inspection.json).

Regular drawings are orange; Bold blue. Preserve the existing structure and
colors. Proposed focus: develop actual Bold progression, coherent right-hand
curves and chamfered terminals, and preserve the inward stroke and its aperture
without filling in the upper counter. Dagesh needs room in the upper counter;
check it in both base-plus-mark shaping and standalone presentation forms.
Do not inherit prior provisional dimensions without reviewing the live donors
and this pair's distinctive internal structure.

The normal and final forms should be considered together; spacing and the
final descender are part of the comparison. Existing drawing data, anchor
placement and marked-form dependencies must be inspected before a scratch edit.
No candidate or application is authorized merely by this recommendation.

## Candidate v1 — 2026-10-19

Eli asked to make dark mode the default and continue to the next group. A
four-GLIF trial is now built in `out/qa/2026-10-19/hebrew-004-v1/`; **not applied**
to the active sources. `make proof-web` opens `candidate-v1/` at localhost:60272.
Before is the actual HEB-003 applied binary. Candidate and unchanged Rubik/Noto
bytes, licenses and hashes are retained alongside the page.

Both forms retain one continuous contour and the existing inward-stroke
structure. The right bowl uses the reviewed Kaf construction translated to
accommodate that stroke. Its outer handles retain the Kaf runs of 128/184 in
Regular and 168/168 in Bold; inner horizontal handles remain 88/64. Bold inner
vertical handles become 96 as the top/base bars reduce to 144 to preserve
counter space. The live green n/o/H/E donors and reviewed Kaf/Final Kaf are
hash-recorded in `reference-sources.json`; no donor was edited. The 16-unit
exposed chamfers and 8-unit concave joins follow H/E. Flat top stays 576 and
Final Pe's bottom is snapped from −182 to −184.

| Measurement | Regular | Bold |
| --- | --- | --- |
| Pe advance | 600 | 792 |
| Final Pe advance | 608 | 800 |
| Left bearing | 48 | 48 |
| Pe / Final Pe right bearing | 48 / 56 | 48 / 56 |
| Main side stroke | 96 | 192 |
| Roof / Pe base | 96 | 144 |
| Inward bar | 96 | 112 |
| Pe opening above base | 144 | 64 |
| Dagesh anchor | 264, 408 | 344, 376 |

The widened Bold and lighter inward bar are trial proportions, not a new
script-wide rule. Review them beside the Latin and the reference families.
Rendered Regular, midpoint and Bold comparisons, large single-glyph Bold
views, marks and running text were inspected and retained in `candidate-v1/`.
The new pair is visibly heavier at Bold; the surrounding unfinished Hebrew
still mixes weights in running text. This is not release approval.

Checks: four glyph-masters pass the full 8-grid gate; both masters pass curve
lint; the full source compatibility report has no blockers; build/preflight
produced the variable font, four statics and PDF. Hebrew checks have zero
failures. Across seven weights, 6,048 compiled glyph comparisons restrict
changes to Pe, Final Pe and the inherited Pe-rafe outline. Only the two base
advances change. 196 before/candidate mark-pair tests found no ink collisions.
The validator also confirms all active source bytes remain unchanged and
only the four intended scratch GLIFs differ. Exact evidence is in the
`candidate-v1-*.json`/logs and reproducible scripts here.

Protected follow-up: `uniFB4E` (Pe-rafe) inherits the changed base but retains
its old advance, rafe offset and anchors. Regular Pe-dagesh and Final-Pe-dagesh
are purple standalone outlines and remain untouched. These need explicit
review before this family is complete; ordinary base-plus-mark tests do not
validate those presentation forms. No color has been promoted.


## Applied — 2026-10-19

Eli approved: “ok this looks good, apply the Pe and Final Pe changes to both
masters.” Installed the exact four reviewed GLIFs; retained original colors.
`application-v1.json` records before/after hashes and verification. All other
active source bytes are unchanged. Active-source grid and curve checks pass,
full master compatibility reports zero blockers, Hebrew checks have zero
failures, and canonical preflight rebuilt five fonts, PDF and reports.
The applied variable binary equals the reviewed candidate in every table except
`head.modified` and `head.checkSumAdjustment`. The live page now says Applied
and uses the actual rebuilt binary; the reviewed candidate snapshot is retained.

Recommended next base group: מ Mem U+05DE, ם Final Mem U+05DD and ס Samekh U+05E1.
Live inspection found identical Regular/Bold outlines and widths in all three:
628, 606 and 602 units, respectively. Regular is orange and Bold blue. Their
open/closed counters and square/rounded distinction make a useful joint review.
This is a recommendation, not a new drawing or approval. Source hashes and
structure are retained in `next-group-inspection.json`. The protected marked
forms described above remain on the release follow-up list.
