# HEB-006 — Yod, Vav, Zayin, Nun and Final Nun

2026-10-20. **Eli’s Regular and Bold Zayin corrections are saved; correction 02 records Bold’s compact geometric turn.**
Baseline: approved HEB-005 v5 in active sources. Scope is ten GLIFs, both masters.
Preserve existing glyph colors. Regular is orange; Bold Yod/Vav/Final Nun are
red, Zayin/Nun blue. No protected glyph is a target.

V1 preserved the simple stem family, Zayin's angled crown and Nun's curved shoulder
and foot. In response to the HEB-005 lesson, do not interpret cleanup as license
for a different skeleton. One contour per glyph; matching topology in both
masters. Yod/Vav/Final Nun use green n's 96/192 stem measurements and the green
H/E 16-unit exposed cuts. Widths 240/336 with 72-unit sidebearings. Their lower
ends stay at 240/0/−128 respectively; Rubik also has a short Final Nun descender.
Zayin retains its angled head and curved neck, adapted to the 8-grid with a
96/192 stem, 16-unit exposed cuts and a heavier Bold crown. Widths 304/432.
Nun retains its existing skeleton; its shoulder translates green n to top 576
and uses the reviewed Resh inner construction, with a 96/168 foot and a 96/192
stem. Widths 336/432. All donor hashes and original outlines are retained here.

Mark anchors follow the new geometry. Dagesh positions for stem-only forms
stay to the left of the stem; Final Nun's existing centered anchor requires
correction to avoid ink overlap. No direct component references or standalone
marked glyphs will be altered without separate inspection. Marks and reading
texture remain part of review, not established by grid or compatibility alone.

## V1 review and verification

Open `make proof-web`, currently localhost:60272. The proof shows Before
(applied HEB-005 v5), Candidate, Rubik and Noto. The five-name heading wraps
on the existing grid without changing heading sizes; three-glyph studies retain
their previous layout. The Sample menu offers individual letters, the group,
words and marks; Text provides running Hebrew and mixed-language passages.

- All ten glyph-masters pass the 8-grid and curve gates. Preflight built the
  variable font, four static fonts, PDF and metadata reports. Full master
  compatibility has zero blockers; Hebrew checks have zero failures.
- At seven weights, 6,048 glyph comparisons confine outline changes to the five
  targets plus four dependent composites: vavvav-hb (U+05F0), vavyod-hb (U+05F1),
  yodtriangle-hb (U+05EF), and uniFB1D. Their source files and offsets are
  unchanged; the altered base outlines are inherited at compilation.
- 490 before/candidate base-mark pairs were checked. The seven baseline
  collisions are Final Nun plus dagesh at each weight; there are zero candidate
  collisions. This synthetic check does not establish linguistic validity or
  full combined-mark correctness.
- All 1,759 active source file hashes remain unchanged. Only ten GLIFs in the
  scratch sources changed. Colors and Unicode values are preserved.
- Browser Regular/Bold group comparisons, large Bold Zayin/Nun, marks, running
  text and inherited composites were inspected. Selected screenshots live in
  `candidate-v1/`. Unfinished surrounding letters still have uneven Bold weight.

For the composite review, paste `װ ױ ׯ יִ` into Your Text. The frozen Rubik
reference lacks these codepoints; the proof reports that instead of using a
fallback. Noto is available for this supplementary comparison. The inherited
composite offsets/mark alignment remain a separate follow-up, especially the
Yod-with-hiriq presentation form. No composite has been silently re-spaced.

Review focus: stem thickness and sidebearings across Yod/Vav/Final Nun, Nun's
shoulder and foot in Bold, and whether Zayin's retained angled crown sits well
with the reviewed family. Rubik has a flatter head; this candidate preserves
Virtua's existing angled construction rather than replacing the skeleton.
The existing Final Nun descender remains −128. Nothing is applied or auto-graded.

`prepare_candidate_v1.py` reproduces the original scratch trial in a new `out/qa/` folder.
`validate_candidate.py` verifies scope and mark evidence against the preserved
baseline. Original and candidate GLIFs are retained under
`candidate-v1-sources/`; source hashes, donor hashes and reports live alongside.

## Zayin feedback — 2026-10-20

Eli: “the zayin looks wrong, i think we over complicated it, should be more like
rubik”. Supersede the v1 choice to preserve the angled crown. V2 simplifies
Zayin only: level head, clean gently offset stem connection, existing 16-unit
Virtua chamfers. Preserve the other four candidate glyphs byte-for-byte and
retain v1. This is explicit feedback on Zayin, not a change to every glyph.

## V2 — simplified Zayin

The current `prepare_candidate.py` reproduces v2. Zayin now has a flat head
at 576, with a 96-unit Regular / 144-unit Bold bar. The stem remains 96/192
units, with a shallow 24-unit lateral transition over 128 vertical units into
the head. Exposed chamfers stay 16 units. Advances 304/432 and all anchors are
unchanged from v1. Rubik informs the simpler construction; its outlines were
not copied. Both masters retain one 20-point contour with matching point types.

The eight other glyph-master files are byte-identical to v1; only Zayin's two
outlines differ. `candidate-v2-revision-scope.json` records that check. All
active source hashes are unchanged. Grid, curves, full compatibility, preflight,
Hebrew QA, 6,048 compiled comparisons and 490 mark-pair checks pass with the same
seven baseline-only Final Nun/dagesh intersections recorded for v1. Large
Regular and Bold Zayin comparisons were visually inspected and saved.

The current live proof compares v1 (Previous) with v2 (Revised) to isolate
this feedback. The applied HEB-005 baseline remains in the v1 proof. V1 Zayin's
angled crown is superseded; the other four designs still await review as part
of this group. Nothing is applied. Source copies and evidence use the
`candidate-v2` prefix; `candidate-v2/snapshot.json` identifies the exact fonts.

## Hand-edit baseline — 2026-10-20

Eli requested committing and pushing these drawings so he can correct them
by hand on top. Exact v2 sources are now installed in both active masters;
this is a working baseline, not final visual approval. The frozen v2 proof
and source copies preserve the pre-correction geometry for later comparison.
See `application-v2.json`. Preserve Eli’s upcoming edits; do not regenerate over them.

## Eli’s saved Regular Zayin correction — 2026-10-20

Eli supplied the outline screenshot and confirmed “this was my edit i saved it.”
Compared the live GLIF against committed baseline `4e900dd`. Exact saved source:
[hand-edit-01-Regular-zayin.glif](hand-edit-01-Regular-zayin.glif).
SHA-256: `f1a1659624a317814e4ce80eb2b211d4a80e0ec2e12ada3b482bd0cdfc8f1171`.

Observed changes, not a new family-wide rule:

- Preserve the level head, 96-unit stem, advance 304, bounds, exterior 16-unit
  chamfers and all mark anchors. The correction is local to the neck.
- On the right, move the vertical-to-curve point from (184,352) to (184,376).
  The cubic now uses handles (184,440), (192,480), ending at (240,480).
  Its final handle is horizontal to the head’s underside, eliminating the
  previous angled arrival at (208,480).
- On the left, end the head underside at (104,480), then add an 8-by-8 chamfer
  to (112,472). Handles (88,440), (88,416) lead to the existing (88,352)
  stem point. This deliberately treats the two sides of the junction differently.

Drawing lesson for this glyph: plan each connection as either a tangent
transition or an intentional cut. A generic pair of offset curves does not
capture this construction. Preserve the established silhouette while refining
junctions; do not substitute a different skeleton. Other glyphs require their
own evidence before reusing these dimensions or asymmetry.

Regular now has 21 points; Bold retains the baseline 20-point outline. The
masters therefore need a corresponding Bold structural adaptation before a
variable build. No Bold drawing or source normalization was performed in this
inspection. The browser’s frozen v2 fonts do not yet show this hand correction.
The editor save also changed other source files; those changes were left intact
and are not attributed to this Zayin design lesson.

## V3 — Bold adaptation of manual correction 01

Authorization: adapt Bold to Eli’s saved Regular, leave Regular unchanged,
and show a candidate before applying. Prepared in
`out/qa/2026-10-20/hebrew-006-v3/`; only scratch Bold Zayin differs from the
current source snapshot. Both active masters remain untouched this turn.

Bold retains its 432 advance, 192-unit straight stem, 144-unit head,
16-unit exterior chamfers and all anchors. The right junction uses on-curve
(328,328), handles (328,392)/(336,432), and end (384,432): the same neck offsets
relative to the stem edge and head underside as Eli’s Regular. The left head
ends at (152,432), cuts to (160,424), then uses (136,392)/(136,368) into
(136,304). The 8-unit cut and 21-point topology correspond to Regular.
These Bold dimensions are a proposal, pending Eli’s visual review.

`candidate-v3-sources/` preserves the two exact GLIFs. The Regular copy is
byte-identical to Eli’s active source. `candidate-v3-scope.json` records source
hashes, the one-file edit boundary and checks. Grid and curve lint pass in both
masters; scratch build/preflight and Hebrew checks pass. Instances at 400–700
in steps of 50 compile; browser screenshots at 400, 550 and 700 were inspected.
No clipping or visible interpolation discontinuity was observed at those views.
This is not final drawing approval or Google Fonts release validation.

The live proof now serves `candidate-v3/` with Before, Candidate, Rubik and Noto.
Before is the frozen committed v2 font: at 400 the difference is Eli’s manual
Regular correction; at 700 it is the proposed Bold adaptation. It is not a
build of the currently incompatible live source pair. Candidate includes the
current saved sources plus only the proposed Bold change. The proof starts
with Zayin; the displayed handoff is at weight 700. Historical v2 remains intact.

Learning reuse: correction 01 directly informed the right horizontal tangent,
left 8-unit cut and preservation of head/stem dimensions. Await Eli’s verdict
before counting this adaptation as a successful reuse of the lesson.

## V3 installed for manual editing — 2026-10-20

Eli explicitly requested using the candidate as his starting point. Installed
only the exact v3 Bold Zayin GLIF after verifying both live Zayin sources still
matched the candidate baseline. Regular and every other source file are unchanged.
See `application-v3.json`. This is installation for manual correction, not final
visual approval. The frozen candidate proof remains the pre-correction comparison.
The available native UI connection exposed a separate empty Runebender window;
automatic refresh of the repository-launched editor was not visually verified.

## Manual correction 02 — Bold geometric turn, 2026-10-20

Eli reports saving the Bold correction and describes the candidate as too sloppy
and humanist. His stated direction is clean, designed, neo-modernist and machined,
with mathematical precision rather than a human-hand appearance.

Exact evidence: [saved Bold GLIF](hand-edit-02-Bold-zayin.glif),
[measured comparison](hand-edit-02-comparison.json), and the retained
[candidate v3 GLIF](candidate-v3-sources/sources/VirtuaGrotesk-Bold.ufo/glyphs/zayin-hb.glif).
Only three outline points differ:

| Role | Candidate v3 | Eli’s saved Bold |
| --- | --- | --- |
| Right stem/curve start | (328,328) | (328,376) |
| Vertical handle | (328,392) | (328,416) |
| Horizontal handle | (336,432) | (344,432) |

The endpoint remains (384,432). Thus the turn’s extent changes from 56 wide by
104 high to 56 by 56. Its vertical/horizontal tangent handles change from 64/48
to 40/40. The resulting cubic has balanced, reflection-symmetric local geometry.
It is not an exact circular arc: do not silently substitute a quarter-circle
formula or call 56 a measured radius. The straight stem extends 48 units higher.
The turn now starts at y=376 in both Regular and Bold, while Bold’s thicker head
has its underside at 432 instead of Regular’s 480.

All other outline points, the 432 advance, anchors and color are unchanged.
Regular is byte-identical to the preserved v3 Regular copy. Both live Zayins
retain one contour and matching 21-point type sequences. No active source was
edited during this comparison; no new build or rendering is claimed here.

### What the attempted transfer got wrong

V3 transferred the tangent-versus-cut distinction and preserved compatible point
order, but carried Regular’s 104-unit transition height into Bold by translating
it with the thicker head. Eli corrected that decision. Do not count v3 as a
successful stylistic transfer simply because its topology and QA passed.

For future related work, explicitly choose the straight-to-curve boundary and
the transition’s width/height, then derive its handles from those relationships.
Check which alignments should stay fixed as weight grows and which dimensions
should change; do not automatically translate the entire neck with the head.
Here the saved Bold demonstrates a square local turn with equal handles.
That exact 56/40 construction remains a Zayin Bold example, not a family-wide
radius or handle prescription. The broader machined, mathematically deliberate
style is explicit user direction and is recorded in DESIGN.md.

The current browser still shows frozen v3, before this Bold correction. Preserve
that rejected candidate as contrastive evidence; a later proof refresh must
identify the saved manual version distinctly.

## Continuation accepted — 2026-10-20

Eli requested committing the saved drawings and learning system and continuing
to the next Hebrew group. Both manual Zayin corrections remain unchanged.
Root `make preflight` passed after correction 02 (build, PDF proof, source/master
reports and artifact presence); this is not full Google Fonts release QA.
New batches may now be written directly to the active masters with a preserved
baseline and proofs, without another per-batch application question.
