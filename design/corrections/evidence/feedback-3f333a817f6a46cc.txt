# HEB-005 — Mem, Final Mem and Samekh

2026-10-19. **V5 approved and applied to both masters. V4 rejected.**
Eli requested: “lets keep working through hebrew until we have hebrew parity
with rubik.” This continues the existing small-group proof/review/application
loop. Open `make proof-web` (localhost:60272) for Before/Applied/Rubik/Noto.
Before is the active HEB-004 baseline; Applied is the rebuilt approved v5.
The previous/refined design comparison remains in `candidate-v5/`.

Scope: מ Mem U+05DE (`mem-hb`), ם Final Mem U+05DD (`finalmem-hb`),
ס Samekh U+05E1 (`samekh-hb`), both masters. The active drawings have identical
Regular/Bold outlines and advances of 628, 606 and 602. Regular is orange;
Bold blue. Candidate colors remain unchanged. Existing structure and the
open/closed and square/rounded distinctions are preserved.

## Original v3 construction

Live green n/o/H/E outlines and reviewed Kaf/Resh were read, with exact donor
hashes in `reference-sources.json`. No external reference outlines were copied.
The original drawings and hashes are in `source-inspection.json`; complete
before/candidate GLIFs are retained in `candidate-v3-sources/`.

- Mem retains its diagonal entry, open base and shoulder. The outer right
  shoulder is a translation of green n (+40 Regular, +8 Bold), including its
  592 top. Inner geometry adapts n to the diagonal leg with collinear entry
  handles on the 8-grid. There is one contour with 31 points per master.
- Final Mem keeps a square enclosure, using n's outer shoulder translated to
  top 576 and the reviewed Resh inner shoulder. Exposed cuts remain 16 units;
  counter joins are 8. Two contours have 10 points each in both masters.
- Samekh preserves the upper-left projection and rounded base. Its lower outer
  quadrants reuse green o exactly, including the −16 overshoot. The top is
  flattened to 576 for Hebrew structure. Optical o counter coordinates are
  deliberately adapted to 8: Regular sides 144/496 and base 80; Bold sides
  240/464 and base 128. It has two contours, 18 and 14 points in both masters.

| Measurement | Regular | Bold |
| --- | --- | --- |
| Mem advance | 608 | 704 |
| Final Mem advance | 600 | 696 |
| Samekh advance | 640 | 704 |
| Mem / Final Mem main vertical | 96 | 192 |
| Mem crown / base | 96 / 96 | 160 / 168 |
| Final Mem roof / base | 96 | 168 |
| Samekh sides | 96 | 200 |
| Samekh roof / base | 96 | 144 |

Review question: do the denser Bold counters and Mem's diagonal join give the
right texture beside the already applied letters and Latin? Script-wide weight
remains provisional. The reference families guide distinctions and texture,
not compulsory equality of widths or contour shapes.

## Verification and evidence

Scratch v1 exposed curve tension breaks in Mem and Samekh. An intermediate v2
preparation stopped on an off-grid handle and is not a candidate. The retained
v3 adjusts the transitions with tangent-aligned 8-grid handles. `prepare_candidate_v3.py`
reproduces v3 in a fresh `out/qa/` directory; earlier scratch builds are not the
reviewed sources.

- Six glyph-masters pass the full 8-grid gate; both masters pass curve lint.
- Full master compatibility has zero blocking mismatches. Canonical preflight
  built the variable font, four static fonts, PDF and reports; artifact presence
  alone is not release readiness.
- Hebrew checks: zero failures. At seven weights, 6,048 compiled comparisons
  show only these three glyphs' outlines/advances changing.
- 294 before/candidate mark-pair checks found no ink intersections. This is a
  bounded synthetic mark check, not complete niqqud/cantillation review.
- The validator guards all 1,759 active source files; none changed. Only the six
  selected scratch GLIFs changed, with colors and Unicode preserved.
- Browser Regular, midpoint and Bold comparisons, individual large Bold forms,
  marks and running text were visually inspected and saved in `candidate-v3/`.
  The surrounding unfinished Hebrew still has mixed weights at Bold.

No component glyph directly references these three base names in the active
UFOs. Standalone presentation forms, including Mem/Samekh dagesh, remain a
separate consistency pass. No protected marked form has been overwritten.

## Rubik parity baseline

`rubik-coverage.json` binds this inspection to the exact local fonts. In the
Hebrew block and Hebrew presentation forms, frozen Rubik contains 76 encoded
codepoints; active Virtua contains 134 and covers all 76 with nonempty outlines.
This is **coverage parity only**. It does not establish drawing, spacing,
shaping, mark placement or reader approval. Rubik's axis spans 300–900; the
current project scope remains Virtua's 400–700, so compare within that shared
range. An axis expansion would be a separate design decision.

The central handoff tracks remaining base groups and the later marked-form,
spacing and native-reader passes. Do not turn this coverage count or passing
checks into a claim that Hebrew is finished or ready for Google Fonts.

## Samekh feedback — 2026-10-19

Eli: “the Samekh looks too organic and humanist it needs to look more geometric
and like it is in a neo grotesk style”. Candidate v3 is retained as the previous
trial. Revise Samekh only: straight sides, a broad flat base, rounded rectangular
counter and controlled corner curves. Preserve Mem and Final Mem exactly.
This is a Samekh correction, not approval to square every round Hebrew form.

## Rejected candidate v4 — geometric Samekh

`prepare_candidate_v4.py` preserves the rejected v4 recipe. Samekh keeps two compatible contours,
with 18 outer and 16 counter points per master. Its outer sides are straight,
the lower corners use a 160-unit radius with 88-unit tangent handles, and the
base is flat at 0 (no round overshoot). The upper-right corner uses the same
radius; the upper-left projection and 16-unit exposed chamfers remain.
The counter is a rounded rectangle: 64-unit corners in Regular, 48 in Bold.
These are deliberate geometric adaptations of the family construction, not
copies of Rubik or Noto. The widths remain 640/704, side strokes 96/192 and
roof/base 96/144. Mem and Final Mem are byte-identical to v3.

`candidate-v4-revision-scope.json` verifies only the two Samekh GLIFs differ
from v3. All active source files remain unchanged. Grid and curve checks,
master compatibility, canonical preflight, Hebrew QA, 6,048 compiled comparisons
against the active baseline and 294 mark-pair checks pass. Large Regular/Bold
and Bold running text were inspected in the browser. The proof deliberately
compares v3 with v4 to isolate this correction; both remain unapplied trials.
Sources and evidence are retained under `candidate-v4-sources/`,
`candidate-v4-*.json` and `candidate-v4/`.

## Correction to the correction — 2026-10-19

Eli rejected v4: “This looks worse than the version before ... I wanted a slight
cleanup of the outline and you did a completly different design. the previous
version here is much better ... rubik is a good example”. V4's rounded rectangle
is rejected, not a new design direction. Return to v3's skeleton, oval bowl,
projection and counter. Limit v5 to small curve-handle adjustments; preserve
all on-curve positions, widths, anchors, chamfers and contour structure. Mem and
Final Mem stay unchanged. This feedback supersedes the earlier interpretation
that geometric meant a flat base and rectangular counter.

## Candidate v5 — restrained cleanup of v3

`prepare_candidate.py` reproduces this trial. It restores v3, then changes only
12 off-curve handle positions per master, by 8 or 16 units on a single axis.
Slightly longer tangent handles make the lower bowl and counter fuller and the
upper-right transition more even. Every on-curve point, contour structure,
advance, anchor, chamfer, extremum and color is identical to v3. Mem and Final
Mem remain byte-identical. The rounded base and oval counter are preserved.
`candidate-v5-revision-scope.json` records and checks those constraints.

Grid and curve checks, full master compatibility, canonical preflight, Hebrew
QA, 6,048 compiled comparisons against the active baseline and 294 mark-pair
checks pass. The Regular and Bold browser comparisons were visually inspected;
this is a small refinement awaiting Eli's review, not an approved improvement.
The live proof compares v3 (Previous) with v5 (Refined), alongside Rubik and
Noto. Active sources are unchanged. V3 remains available if this refinement
is not preferred. Evidence and source copies use the `candidate-v5` prefix.

## Application — 2026-10-19

Eli approved: “apply the Mem, Final Mem and refined Samekh changes to both
masters”. The exact six v5 GLIFs were copied into active sources with hash
guards; all 1,753 other active source files were preserved. No glyph colors
were changed. `application-v5.json` records authorization and before/after
hashes. Canonical preflight, grid and curve checks, zero blocking master
mismatches and zero Hebrew check failures passed. All tables in the rebuilt
variable and four static fonts match the approved candidate except the build
timestamp/checksum fields. The applied browser proof is in `applied-v5/`.

Next group: י ו ז נ ן — Yod, Vav, Zayin, Nun and Final Nun. Review narrow-stem
proportions, head/foot treatment, length distinctions and spacing together.
Protected marked presentation forms and script-wide weight remain later work.
