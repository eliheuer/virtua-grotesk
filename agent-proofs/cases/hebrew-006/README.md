# HEB-006 — Yod, Vav, Zayin, Nun and Final Nun

2026-10-20. **V2 installed in both active masters for Eli to correct by hand.**
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
