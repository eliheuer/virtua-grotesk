# LAT-001 · Attachment and coverage foundation

Eli requested committing/pushing the Arabic handoff, then autonomous work on
Latin diacritics and Google Fonts readiness toward Rubik quality/language coverage.
Arabic handoff `889ffa58` was pushed before this work. All Arabic GLIFs, their
manual donors, all green drawings and human grades are reserved. The Arabic live
proof stays on its whole-script handoff while Eli edits; do not replace its current
case merely to show Latin work. This request authorizes independent Latin repairs,
not green redesigns, public submission, or claims of reader approval.

## Applied scope

- Thirteen Regular combining marks lose accidental component translations from
  the earlier recoloring save. Existing outlines and human grades are unchanged.
- Fourteen spacing donors in each master gain outgoing stack anchors matching
  their combining forms. This fixes collisions in precomposed-plus-mark contexts
  such as `ū́` and `ǘ`; it does not redraw the marks.
- The shared Regular `dotaccentcomb` Hebrew-only `_hbNunDot` anchor changes y720
  to544, compensating its removed176-unit component translation. The reversed-Nun
  context `׆̇` retains exact shaped ink at400/475/550/625/700.
- Ten composites in each master: Ĉĉ Ĝĝ Ĥĥ Ĵĵ Ǽǽ. Existing Virtua components,
  purple pending-review grade, base categories and Latin-only ccmp closure.
  Ĵ and ĥ hats align to the ascender stems. AE/ae are expanded to their original
  two component references inside the new wrappers, avoiding nested components.
- Windows clipping ascent1152→1488 in both masters contains the current tallest
  encoded/source-mark geometry. Typographic ascender/descender, line gap and
  USE_TYPO_METRICS are unchanged. This is clipping protection, not approval of
  the tall Arabic mark construction.

`changes.json` names69 files (49 existing plus20 new). Exact backups and final
candidates are retained. `apply.py` refuses changed source hashes. All other
existing source files were byte-identical immediately after application.
`prepare.py` is a reproduction recipe against the frozen baseline, not a tool to
rerun blindly over newer editor saves.

## Proof and validation

Whole rasters inspected: attachment400/550/700, all marks400/700, new coverage
400/550/700, reading text400/700 and detail700. Before/Working/Rubik use identical
em scale and separate font contexts. Final raster receipts bind the images to
the current font. Whole marks remain visually unfinished, especially Bold weight;
this batch is not a drawing-quality signoff.

240 shaping/ink checks pass, including all existing compiled glyph outlines
unchanged apart from the13 translated combining marks, source compatibility,
all new composites, multi-mark clearance, missing-cmap fallback, and Arabic/Hebrew
preservation contexts. Three new regression tests pass across VF sample weights
and all four statics. Active build/preflight completed. Curves were not changed.
The grid report retains636 findings:630 inherited donor coordinates/anchors plus
six inherited advance/sidebearing findings in c/j; all new offsets/anchors are on8.
Do not snap the green Latin donors to remove these findings.

Full existing suite:28 test methods run,216 failing subcases remain. Rebuilding
the frozen pre-edit source reproduces exactly the same216 failures, with zero
new failures after the Hebrew-only compensation.105 are cantillation clearance;
111 are meteg clearance or Hebrew composed/decomposed mismatches. Their exact
records are in `existing-regressions.json`. They are unresolved release blockers.

Unexcluded online Fontspector1.9.0: full five-font run1 FAIL /29 WARN, improved
from6 FAIL /29 WARN. The remaining loose-font failure is directory naming (`ttf`).
The proper local package has10 FAIL /8 WARN: all10 failures concern serving-subset
reachability (U+0302, U+0331, U+1EBC/U+1EBD). Expanded Latin support exposes Aleut
in addition to the nine earlier results. No subset/exclusion was changed to hide
it. `qa-summary.json` and retained argument/hash receipts describe the checks.
The local package is `out/qa/2026-10-21-latin-package/ofl/virtuagrotesk`; metadata
primary script/date, source delivery and article licensing remain provisional.

## Subsequent drawing batches

[Batch02](batches/02-straight-accents/README.md) strengthens Bold acute/grave and
redraws both macrons with64/96-unit bars and clipped ends. Four source GLIFs only;
all green/Arabic/other source bytes and all anchors/advances preserved. Complete
word/attachment rasters at400/550/700 and large details inspected.80 shaping checks
and three Latin tests pass; the same216 baseline Hebrew failures remain. This
is a local pending-review draft, not a release approval.

[Batch03](batches/03-chevron-accents/README.md) strengthens only the Bold
circumflex/caron, with wider clipped apexes and thicker arms. Both Regular sources
and all other source bytes stay unchanged. Whole-word/stacking proofs at400/550/700
and224px/em detail inspected;90 shaping checks, Latin tests and preflight pass,
with zero new failures versus the216-failure engineering baseline.

[Batch04](batches/04-ring-accent/README.md) replaces the square ring accent in
both masters with round contours and raises outgoing stack anchors. Four GLIFs;
all other source bytes unchanged. Whole attachment/reading rasters at400/550/700
and enlarged endpoint proofs inspected;90 shaping checks, three Latin tests and
preflight complete. The same216 pre-existing Hebrew failures remain, with no new
failures. Ring proportions/weight await human review.

[Batch05](batches/05-breve/README.md) rounds the faceted breve bowl in both
masters, adds Bold weight and raises outgoing stack anchors. Four GLIFs only;
all other source bytes unchanged. Whole400/550/700 images and enlarged endpoint
letters inspected.90 shaping checks, three Latin tests, five-weight curve/outline
checks and preflight complete; no new failures against the216-failure baseline.
The round bowl and visible cap cuts await human review.

[Batch06](batches/06-tilde/README.md) replaces both angular tilde donors with
rounded waves, broad terminal landings and Bold weight. Four source GLIFs;
all other source bytes unchanged. A pinched-terminal trial was rejected by image
inspection before application. Whole400/550/700 word/stack proofs and enlarged
endpoint letters inspected;90 shaping checks, Latin tests and preflight complete,
with zero new failures. Zero grid findings; intentional S inflections documented.

[Batch07](batches/07-latvian-marks/README.md) corrects twenty Latvian wrappers
that used cedillas, including the mark incorrectly under ģ. Existing comma
components now supply detached below marks and the rotated above mark on ģ;
base/donor ink and advances are unchanged. Two Latin ccmp additions preserve
canonical web fallback.205 scoped checks, four Latin tests, endpoint/intermediate
whole images and preflight complete; zero new failures. The small, light comma
donor remains unfinished, especially at700. Independent FreeType/RAQM images
verify deep extra marks that were faint/missing in a DesignBot raster.

[Batch08](batches/08-comma-accent/README.md) repairs the two comma-accent donors:
parallel-sided64/96-unit marks replace notched identical-weight forms. All1777
other source files, anchors, advances and wrapper grades remain unchanged.
Whole400/550/700 and enlarged endpoint images inspected;220 scoped checks,
four Latin tests and preflight complete, with no new baseline failures.
The inherited generic g+U0326 descender collision remains; Latvian ģ is separate
and retains clear stacking. Eight inherited metric/anchor grid findings remain.

[Batch09](batches/09-cedilla/README.md) replaces the faceted cedilla donors with
rounded48/64-unit hooks and updates outgoing bottom anchors. Four GLIFs plus
two Windows clipping-descent fields (512→576) contain the newly deeper stacks;
typographic metrics stay unchanged. All1773 other source bytes are preserved.
Whole400/550/700 and enlarged endpoint images, five-weight signed profiles,
90 scoped checks, five Latin tests and preflight complete; no new baseline
failures. Hook depth/neck proportions remain for human review.

[Batch10](batches/10-ogonek/README.md) rounds and weights both ogonek hooks,
repairs fourteen local wrapper attachments (including detached Ą), and adds eight
canonical compositions per master. Eighteen GLIFs plus two feature files; all
base/Arabic/green source bytes unchanged. Whole400/550/700 and enlarged endpoint
images inspected;100 scoped checks, six Latin tests and preflight complete, with
no new failures against the216-failure engineering baseline. Independent RAQM
images confirm canonical output where DesignBot's decomposed row differs. A
separate existing missing-cmap plus acute failure remains (40 VF samples before
and after); retain it on the serving-subset queue. Hook proportions need review.

[Batch11](batches/11-alternate-carons/README.md) repairs both alternate-caron
donors and placements in Ľďľť, and replaces the wrong apostrophe on uppercase Ť
with the existing normal caron. New spacing/offsets are on8; base/Arabic/green
sources and wrapper grades are unchanged. Twelve GLIFs plus two feature files,
135 scoped checks, seven Latin tests, whole400/550/700 and enlarged endpoint
images, and preflight completed. The same216 baseline failures remain. Side-mark
proportions and conservative pair spacing await manual review.

[Batch12](batches/12-vowel-spacing/README.md) matches31 lowercase a/e/o/u accent
wrapper advances to their current bases in both masters (62 GLIFs). All ink,
placements, grades and kerning remain exact; all1717 other source files unchanged.
Whole400/550/700 form/word images and enlarged endpoints inspected.500 scoped
checks, eight Latin tests, unchanged216 baseline failures and preflight complete.
Basic missing-cmap advance differences fall133→0 across155 samples; separate
mark-placement/compound-accent subset findings remain. All new widths on8;
1185 inherited closure-grid findings retained. Bold e proportions remain a
protected base review issue, not approved by this spacing correction.

[Batch13](batches/13-uppercase-spacing/README.md) corrects21 Regular/45 Bold
uppercase accent advances (66 GLIFs;52 characters) to their current bases.
All ink/layout tables/placements/grades are unchanged; all1713 other sources
preserved. Whole400/550/700 and enlarged endpoint proofs inspected;815 scoped
checks, eight Latin tests, unchanged216 baseline failures and preflight complete.
Basic missing-cmap advance mismatches fall201→0 across260 samples.1080 inherited
grid findings remain, including Bold R's60-unit optical right bearing. Rubik's
missing U+0162 is explicit; supported T/U rows retain the comparison.

[Batch14](batches/14-consonant-spacing/README.md) matches20 Regular/25 Bold
lowercase consonant/iogonek advances (45 GLIFs,25 characters) to current bases.
All ink/layout/placements/grades and1734 other sources unchanged. Whole400/550/700
and enlarged endpoint images inspected;415 scoped checks, eight Latin methods,
unchanged216 baseline failures and preflight complete. Basic missing-cmap advance
differences fall105→0 across125 samples.1037 inherited grid findings remain;
new advances/target bearings on8. The hcaron width-only trial was withdrawn after
whole images exposed its existing ascender collision; both sources unchanged.
Narrow I/l and off8 K/c/k/t exceptions are measured and deferred. Local only.

[Batch15](batches/15-hcaron-attachment/README.md) clears hcaron's ascender
collision in both masters using local offsets, explicit stack anchors and a
base-matching Regular advance. Two GLIFs plus two feature files; all1775 other
sources/Arabic/green/base/donor bytes and grades unchanged. A narrow mark-filtered
composition handles intervening cedilla in missing-cmap fallback. Whole400/550/700
and enlarged endpoints inspected; Rubik lacks U+021F, explicitly unavailable,
with supported decomposed rows retained.135 scoped checks, nine Latin methods,
unchanged216 baseline failures and preflight complete.23 inherited donor-grid
findings remain. Mark proportions remain for human review. Local only.

[Batch16](batches/16-bold-ckt-spacing/README.md) matches six Bold c/k/t
accent advances to their on8 bases. All ink/layout/grades and1773 other source
files including every Regular source remain exact. Whole400/550/700 and enlarged
endpoint proofs inspected;130 scoped checks, nine Latin tests, unchanged216
baseline failures and preflight complete. Missing-cmap advance differences25→20
across30 samples: zero at700, retained below700 because Regular optical-width
exceptions are unchanged.91 inherited grid findings remain. Local only.

Eli approved pushing attachment/coverage commit1e8dd28e; it is now on origin/main.
The subsequent drawing checkpoints remain local.

[Batch17](batches/17-tbar/README.md) adds Ŧ/ŧ in both masters as unchanged green
T/t components plus eight-point clipped bars. Four new GLIFs and four registration
plists; all1775 other existing source files preserved, including326 Arabic
donors/master. New geometry/anchors/outer spacing on8. Whole400/550/700 and224px
endpoint proofs inspected against Rubik;130 scoped checks, ten Latin methods,
unchanged216 baseline failures and preflight complete.21 inherited component-grid
findings remain. New forms use default spacing: T/t kerning must not be copied
blindly because the added bars change collision clearance. Local only, purple
pending human review. Pinned Rubik Latin gap now six codepoints: ĸ ŉ ſ ƒ ﬁ ﬂ.

## Next bounded work

1. Batch25 fixes breve contour direction without moving geometry; do not redo it. Batch26 adds U0312 and batch27 adds U0335 with a narrow variant. Batch28 adds U0337 and batch29 adds U0338 with bounded math attachment. Batch30 adds encoded not-equal from the exact prior mathematical attachment. Batch31 adds less-equal/greater-equal with bounded long-slash negation. Batch32 adds plus-minus and not-sign. Batch33 adds broken bar U00A6. Batch34 assesses soft-hyphen shaping and actual browser line breaking without source edits. Batch35 adds the U+00AD exact-hyphen compatibility wrapper and verifies default/preserved ignorables, real subsets and unchanged browser line breaking. It introduces the explicit soft_hyphen policy WARN; release retain/omit choice remains unapproved. Batch36 completes the U+2011 assessment: browser behavior works, but text-only subsets can lose its U+2010 fallback. No alias added; optional direct-cmap/subset support remains separate. Batch37 adds generic currency U+00A4. Batch38 completes superior-digit donor/normalization/feature assessment: no existing superior donors or encoded coverage, all 1/2/3 donors green. Next prepare bounded onesuperior/twosuperior/threesuperior drawings in both masters from protected Virtua figure construction, preserving donor bytes; no ordinary-size aliases or automatic normalization. Encoded coverage is separate from a future coherent sups feature family. See batch38 for reference metrics, fallback and subset findings. Current online package QA is12 FAIL/10 WARN; serving-set mappings need a separate coverage/policy decision, not false subset declarations. Fi/fl are complete in batch22; retain optical pair-spacing review. Long s/florin/kra/apostrophe-n are added in batches18–21; do not redo them. Tbar/tbar are added in batch17; retain their separate pair-spacing follow-up. Narrow I/l and off8 K/c/k/t spacing exceptions remain measured in batch14; batch16 fixes only the six safe Bold c/k/t wrappers. Preserve base geometry/overhangs and keep these exceptions open for review. Hcaron attachment is repaired in batch15; do not redo it. Preserve intentional alternate-caron side spacing. Then remaining Latin coverage. Generic g+U0326 still collides inside its descender; preserve the green base while diagnosing attachment. Preserve the rotated ģ placement introduced in batch07. Check full reverse closure for green/Arabic dependencies and preserve the shared
   reversed-Nun calibration when changing any dot geometry or anchors.
2. Spacing constraint reaffirmed by Eli: use the powers-of-two system for
sidebearings, advances and kerning. New machine values on8; record decompositions
and preserve green/human optical exceptions. See DESIGN.md#spacing.

3. Existing precomposed widths differ from the base+mark fallback by up to
   tens of units. `verification.json` retains the measured sample differences.
   Inspect wrapper metrics/kerning and word spacing before applying changes.
4. No missing Latin-script codepoints in the pinned Rubik cmap comparison after batch22. This is not full language coverage or visual approval. Review encoded ligatures
   separately from GSUB behavior. The remaining punctuation, fractions,
   maths and currencies are also absent; use `coverage-after.json`.
5. Full Rubik language coverage includes182 Cyrillic codepoints absent here.
   This is a separate drawing/reader-review phase, not a metadata toggle.
   The102 missing Arabic codepoints are presentation forms; compare GSUB and
   legacy text behavior before adding redundant forms. Leave Arabic sources to Eli.
6. Diagnose the216 existing Hebrew regressions, serving-subset failures (batch23 fixes the recorded batch10 ogonek normalization failure; other subset failures remain), fresh
   interpolation/outline warnings, CI reproducibility and package provenance.
   Green exceptions require named approval; never suppress checks to pass.

Quality, readable language support and cmap counts are separate gates. Rubik
upright was downloaded from the official google/fonts source and frozen with
metadata in `assets/`; same coverage does not mean the same design or styles.

## Reproduce

Use `.venv/bin/python scripts/reference_coverage.py --font FONT --reference
REFERENCE --output REPORT` for the pinned cmap comparison. Run
`python -m unittest tests.test_latin_diacritics` after a fresh build.
`VIRTUA_FONT_QA_ROOT` can point those tests at a scratch build.

## Diffenator browser review — d2513094

At Eli's request, generated stock Diffenator3 1.1.4 context proofs for Virtua and
pinned Rubik, plus a two-font coverage-text comparison. Local interactive URL:
<http://127.0.0.1:60273/comparison/diff3proof.html> (Old=Virtua, New=Rubik).
Generated reports are in `out/review-latin-d2513094/`; exact commands, binary
hashes and captured browser images are in
[review.json](diffenator-d2513094/review.json). No source/font changes.

Inspected identical mixed coverage text at400/550/700 and Virtua Romanian and
Latvian context panels at400/700. Bold is visibly denser than Rubik; long-text
spacing still needs pair-level review. Tested marks are visible without line
clipping; this is not exhaustive language or native-reader approval. Literal
`[Missing]` occurs in the stock text in both views and is not itself a missing
cmap diagnosis. The instance dropdown stays Regular after manual slider changes;
actual recorded slider values set the weight. Use this actual Diffenator view
alongside enlarged drawing proofs on subsequent meaningful checkpoints.

## Batch18 · Long s coverage and Diffenator review

[Batch18](batches/18-longs/README.md) adds ſ in both masters with24-point contours
derived from unchanged green f, removing the right arm. Advances344/400 and all
new geometry/anchors/bearings are on8; zero grid findings. Six new/registration
files; all1779 other existing sources and all existing compiled ink/advances
unchanged.90 scoped checks,11 Latin methods, exact216 Hebrew baseline failures and
preflight complete. Whole400/550/700 rasters and224px endpoints inspected.
Actual Diffenator stock coverage and a labeled same-text long-s supplement were
inspected at400/550/700 against Rubik. The short f-derived head, dense Bold stem
and default pair spacing remain review items. Four tangent G1 joins/master retain
curvature jumps; no sampled reversals/proper crossings at five weights. No visual
approval or push. Rubik Latin gap is now five; next inspect florin.

## Batch19 · Florin coverage

[Batch19](batches/19-florin/README.md) adds ƒ in both masters:40-point contours
using green f head turns and a rotated descending hook at−256. Only the new glyph
extends off8 crossbar tips4 units; Bold inner hook shifts8 to the lower stem.
Advances408/456, points/anchors/bearings on8; zero grid findings. All1781 other
existing sources and all old compiled ink/advances unchanged.95 scoped checks,
12 Latin methods, unchanged216 baseline Hebrew failures and preflight complete.
Whole400/550/700,224px endpoints and actual Diffenator stock/supplement browser
text inspected against Rubik. Dense Bold, compact head/hook and default pairs
remain for human review. Eight G1 joins/master retain donor curvature jumps;
no sampled reversals/proper crossings at five weights. Local only. Rubik Latin
gap now four; next kra, then apostrophe-n and fi/fl. No release approval.

## Batch20 · Kra coverage

[Batch20](batches/20-kra/README.md) adds ĸ in both masters,23-point line contours
from the protected k structure with x-height tops. Only new glyph coordinates are
adapted to8; original k sources/optical widths remain exact. Advances600/664,
bearings72/24, zero grid findings. All1783 other existing sources and all old
compiled ink/advances unchanged.95 scoped checks,13 Latin methods, exact216
baseline Hebrew failures and preflight complete. Whole400/550/700 images,
224px details and actual Diffenator text against Rubik inspected. Dense Bold
branch/default pairs await optical review. No sampled proper polygon crossings;
no cubic contours. Rubik Latin gap now three: ŉ ﬁ ﬂ. Next apostrophe-n, then fi/fl.
Local only; no visual approval or push.

## Batch21 · Apostrophe-n coverage

[Batch21](batches/21-apostrophe-n/README.md) adds ŉ in both masters with unchanged
green n components and a local eight-point commaaccent-derived apostrophe. The
mark clears the crown40 units at five weights; advances672/816 and all new values
on8. Six inherited grid findings belong to protected n y508/452. All1785 other
sources and all old compiled ink/advances unchanged.95 scoped checks,14 Latin
methods, exact216 baseline Hebrew failures and preflight complete. Whole400/550/700,
224px endpoint and actual Diffenator images inspected against Rubik. Lighter,
farther-left apostrophe, dense Bold n and default pairs await human optical review.
Inherited n G1/G0 joins remain; no sampled proper crossings/profile warnings.
No forced substitution of ʼn/’n; compatibility decomposition is not canonical.
Rubik Latin gap now two: ﬁ ﬂ. Next fi/fl, then independent release blockers.
Local only; no visual approval or push.

## Batch22 · Fi/fl coverage and shaping

[Batch22](batches/22-fi-fl/README.md) adds ﬁ/ﬂ in both masters and standard liga
with numbered mark anchors. The first Bold fl trial was rejected for a closed
upper aperture; final openings40/48 remain visible. Advances fi528/656, fl560/672;
all new values on8, zero grid findings. Ten source files; all1785 other sources,
Arabic/green donors and old compiled glyph ink/advances unchanged.165 scoped checks,
15 Latin methods, exact216 baseline failures and preflight complete. Whole images
and actual Diffenator stock/supplement at400/550/700 inspected against Rubik.
Source overlap is intentional; diagnostic union has one contour at five weights.
Dense Bold, new pair spacing and f+fi/f+fl rhythm remain for review. Pinned Rubik
Latin cmap gap is zero;182 Cyrillic,4 combining,62 common and102 Arabic presentation
encodings remain. Next combining/subset normalization and independent release
blockers. Local only; no visual approval or push.

## Batch23 · Ogonek subset normalization

[Batch23](batches/23-ogonek-subset/README.md) repairs the recorded batch10
normalization failure using two feature files only. Contextual decomposition and
ogonek-only filtered recomposition preserve local hooks when accented vowel
normalization bypasses the absent ogonek cmap. All1793 other sources/GLIFs,
Arabic/green/manual donors and compiled drawing/metrics bytes unchanged. Forty
original acute failures fixed; expanded cmap failures435to0/600 samples and real
subset failures870to0/1200 encoded/NFD cases.3,995 preservation comparisons,
16 Latin methods, exact216 baseline Hebrew failures and preflight complete.
GPOS changes only in filter-set indices, verified by remapping. Whole400/550/700
and160px endpoint images and actual Diffenator NFD text inspected against Rubik.
Mark output order can differ without changing positioned ink. Existing Bold/hook
proportions remain for human review. This is not a clean package QA result or
full serving-subset approval. Next combining gaps and current package diagnostics.
Local only; no push.

## Batch24 · Ligature carets and refreshed package QA

[Batch24](batches/24-package-qa/README.md) adds only fi/fl caret_1 anchors in
both masters (288/288 Regular,344/360 Bold). Four GLIFs;1791 other source files,
Arabic326/master, green131/74, all ink/metrics/layout bytes unchanged.74 scoped
checks,17 Latin methods, exact216 baseline Hebrew failures and preflight complete.
Whole400/550/700 rasters,224px caret diagnostic and actual Diffenator comparison
with Rubik inspected; native editor cursor behavior not tested. Fresh online
unexcluded package QA improves10 FAIL/11 WARN to10 FAIL/10 WARN; caret warning
resolved. Remaining tofu failures concern serving-set reachability, separately
from batch23's fixed normalization cases. Full current reports retained. Breve
contour direction is the next concrete independent repair; other protected and
human findings remain open. Local only; no push or visual/release approval.

## Batch25 · Breve winding

[Batch25](batches/25-breve-winding/README.md) reverses only Regular/Bold breve
contour traversal, preserving exact geometry, placement and grades. Two GLIFs,
14 consumers/master,1793 other sources and all Arabic/green sources unchanged.
78 scoped checks plus4,410 exact compiled geometry comparisons at five weights;
17 Latin methods, unchanged216 baseline Hebrew failures and preflight complete.
Whole400/550/700 and224px endpoint proofs plus actual Diffenator target/stock
viewport images reviewed against Rubik. Raster pixels differ with changed
traversal despite exact geometry; no pixel identity claimed. Fresh full online
unexcluded package QA10 FAIL/9 WARN/160 PASS: outline_direction now passes.
Other serving-set/protected/human findings remain. Next four combining marks,
then common symbols. Local only; no visual approval or push.

## Batch26 · Turned comma above

[Batch26](batches/26-turned-comma/README.md) adds U+0312 in both masters as
compatible eight-point commaaccent-derived180° diagonals, with zero advance and
incoming/outgoing top anchors. Soft-dotted class handles i/j/iogonek and
intervening below marks. Eight source files; all1,789 other existing sources,
all existing GLIFs, Arabic and green sources unchanged.165 scoped checks,
4,410 old ink/advance comparisons,18 Latin methods, unchanged216 Hebrew baseline
failures and preflight complete. Six focused Fontspector checks pass; full
package10 FAIL/9 WARN evidence remains batch25 and predates this addition.
Whole400/550/700 forms/words,224px details and actual Diffenator target/stock
viewport comparisons inspected against Rubik. New marks remain lighter/smaller
than Rubik; dense Bold and longer-text spacing remain review items. No canonical
substitution of g+U0312 to ģ. Zero grid findings; compatible convex contours.
Rubik gap now349:182 Cyrillic,3 combining,62 Common,102 Arabic presentation forms.
Next U0335/U0337/U0338 overlays. Purple pending review; local only/no push.

## Batch27 · Short stroke overlay and build consistency

[Batch27](batches/27-short-stroke/README.md) adds U0335 plus a contextual narrow
variant, both masters, with Latin body-centered GPOS and preserved ordinary-mark
positions. Whole-image review rejected the wide-only narrow-letter trial. Eleven
source files;1790 other existing sources and every old GLIF unchanged, including
Arabic326/master and green131/74. All new points/anchors on8, zero grid findings.
765 scoped checks,4415 exact old VF ink/advance comparisons,20 Latin methods and
2 build-helper tests pass;216 baseline Hebrew failures persist with no numerical
regression. Full images400/550/700,224px endpoints, actual Diffenator supplement
and stock first view, plus four-weight static comparisons inspected.

Per-master feature positions exposed different master glyph orders and an old
static-build limitation. Build now normalizes order only in a temporary source
copy and derives statics from the VF. All static advances preserved; standard
overlap removal/serialization changes old static contour records, not source
outlines. Complete new static geometry matches serialized VF instances. This is
not a claim of old-static pixel equality. Full online final-package QA remains
10 FAIL/9 WARN/160 PASS/10 INFO/40 SKIP. No exclusions or subset changes. Rubik
gap348:182 Cyrillic,2 combining,62 Common,102 Arabic presentation forms. Pending
human review; local only. Next U0337/U0338 and independent symbols/blockers.

## Batch28 · Short slash overlay

[Batch28](batches/28-short-slash/README.md) adds U0337 and a contextual narrow
variant in both masters. Eight-point45-degree diagonals with clipped ends,
67.9/90.5 normal weights, default bounds±264/272, narrow±136/144. Initial short,
heavy trial rejected by whole-image review. Existing Latin body GPOS extended;
all existing anchors/GLIFs/metrics/kerning unchanged. Ten source files,1795 other
existing source bytes preserved including Arabic326/master and green131/74.
770 scoped checks,4425 exact old VF and3539 exact old static glyph comparisons,
21 Latin methods, unchanged216 baseline failures and preflight complete.
Whole400/550/700 forms/words,224px details and actual Diffenator supplement/stock
first view inspected. Zero grid findings; convex at five weights. Generic Bold
counter fragments, varying terminal projection and overall density remain human
review items. Full online package stays10 FAIL/9 WARN/160 PASS/10 INFO/40 SKIP.
Rubik gap347:182 Cyrillic,1 combining,62 Common,102 Arabic presentation forms.
Next U0338 with negation normalization/symbol attachment checks. Local only.

## Batch29 · Long solidus overlay and bounded math attachment

[Evidence](batches/29-long-slash/README.md): U0338 plus narrow variant, two masters,
new Latin/body and equal/less/greater/plus/minus attachment. Ten source files;
all1799 other sources/every old GLIF, Arabic326/master and green131/74 unchanged.
Eight-point convex clipped contours, default672/narrow448 heights, zero grid
findings. Steep first narrow trial and wider collision trial rejected; final
following-n checks pass. Narrow Bold tips remain subtle; generic counter fragments
and not-less triangular counter remain human-review findings. Whole400/550/700,
224px endpoint and actual Diffenator target/stock images inspected with Rubik.
775 scoped comparisons,4435 exact old VF and3547 old static ink/advance checks;
22 Latin methods plus2 build helper tests, unchanged216 baseline Hebrew failures,
active/scratch identity except head and preflight completed. Encoded ≠/≮/≯ match
NFD at five VF weights and all statics, but their cmap entries remain absent.
Online unexcluded package12 FAIL/9 WARN: two new exposed serving gaps (Central
Mazahua U0338, Ticuna U1EBC/U1EBD). No exclusions or false subset claims.
Rubik Latin/combining cmap gaps zero;346 encodings remain (182Cyrl,62Common,
102Arabic presentation forms). Not language/visual approval. Next common math
symbols, then independent release work. Local only; Arabic60272 unchanged.

## Batch30 · Encoded not-equal

[Evidence](batches/30-notequal/README.md): U2260 in both masters uses unchanged
equal/slashlongcomb components, exact old NFD placement304,352 and advance600.
Six source files;1805 other sources and all old GLIFs/Arabic/green sources unchanged.
90 scoped checks,4445 old VF and3555 old static ink/advance comparisons,23 Latin
methods and2 build-helper methods pass;216 baseline Hebrew failures persist.
Whole400/550/700 equations/forms,224px details and actual Diffenator target/stock
first viewport compared with Rubik. New composite reproduces existing geometry;
long slash proportions, heavy Bold bars and uneven text rhythm await human review.
Generic math accents retain their old right-side placement; not newly attached.
Real subsets and missing-cmap fallback tested. New values on8;16 inherited Bold
equal-point grid findings preserved. Active/scratch identity except head and
preflight complete. Full online package12 FAIL/9 WARN unchanged. Remaining345
encodings:182 Cyrillic,61 Common,102 Arabic presentation forms. Next ≤/≥/±/¬;
local only, no push. Arabic live proof60272 unchanged.

## Batch31 · Less-equal and greater-equal

[Evidence](batches/31-inequalities/README.md): adds ≤/≥ in both masters with16+8
line points,600 advances,72 bearings,72/112 lower bars and96/56 clear gaps.
Whole-image review rejected heavy Bold fill and dangling negation; final lighter
Bold and existing long-slash math lookup at304,368 address those observations.
Ten source files;1805 other source files and all old GLIFs/Arabic/green unchanged.
160 scoped checks,4450 old VF and3559 old static ink/advance checks,24 Latin
methods and2 helper methods pass;216 baseline Hebrew failures unchanged.
Whole400/550/700,224px details and actual Diffenator target/stock inspected.
All new values on8, zero grid findings; five-weight winding/crossing checks pass.
Negated wedge proportions, broader chevrons and pair spacing remain human review;
generic math accents still use fallback. Active/scratch identity except head and
preflight complete. Fresh online package12 FAIL/9 WARN unchanged semantically
(Ticuna bullet order only). Remaining343 encodings:182 Cyrillic,59 Common,
102 Arabic presentation forms. Next ±/¬; local only/no push, Arabic60272 preserved.

## Batch32 · Plus-minus and not sign

[Evidence](batches/32-plusminus-notsign/README.md): adds ±/¬ in both masters,
24+8-point cross/bar and12-point right-leg contours. Advance600,64-unit bearings,
new points/spacing on8, zero grid findings. Plus-minus lower clearance80/40 remains
visible. Eight source files; all1811 other sources and every old GLIF/Arabic/
green/human grade unchanged. No feature, kerning, anchor or metric changes.
160 scoped checks,4460 exact old VF and3567 old static ink/advance comparisons,
25 Latin methods plus2 helpers pass.216 baseline Hebrew failures unchanged;
active/scratch identity except head and preflight complete. Whole400/550/700,
224px endpoints and actual Diffenator target/stock first viewport inspected
against Rubik. Compact cross, default pairs, symbol/alphabet weight balance,
right-side generic math accents, dense Bold and uneven spacing remain review.
Online unexcluded Fontspector12FAIL9WARN160PASS10INFO40SKIP, exact failure
records unchanged. Initial network escalation was resolved through source-level
egress evidence; completed online report supersedes retained offline diagnostics.
Rubik gap341:182 Cyrillic,57 Common,102 Arabic presentation forms. Purple/local
only/no push. Next broken bar and soft-hyphen assessment; preserve Arabic60272.

## Batch33 · Broken bar

[Evidence](batches/33-brokenbar/README.md): adds U00A6 in Regular/Bold with two
8-point clipped vertical segments,96/160 strokes,320 advance and112/80 bearings.
The192-unit gap remains open; all new values on8, zero grid findings. Six source
files;1815 other sources and every previous GLIF/Arabic/green/human grade exact.
135 scoped checks,4470 old VF and3575 old static ink/advance comparisons,
26 Latin methods plus2 helpers pass;216 Hebrew baseline failures unchanged.
Active/scratch identity except head, whole400/550/700 and224px endpoint images,
actual Diffenator supplement/stock first viewport and preflight complete.
Taller/wider split than Rubik,16-unit thicker strokes than the unchanged Virtua
bar, default pair spacing and generic right-side accent fallback remain review.
Online unexcluded Fontspector12FAIL9WARN160PASS10INFO40SKIP, exact failure
records unchanged. Remaining340 Rubik encodings:182 Cyrillic,56 Common,
102 Arabic presentation forms. Purple/local only/no push; Arabic60272 unchanged.
Next soft-hyphen shaping/line-break assessment, then independent Common gaps.

## Batch34 · Soft-hyphen behavior assessment

[Evidence](batches/34-soft-hyphen-assessment/README.md) freezes revision9359e981;
all1821 sources and all five active font hashes unchanged.75 shaping cases and
actual English manual/disabled/no-wrap browser comparisons at400/550/700 show
U+00AD already behaves correctly in this browser despite the absent cmap entry.
Three diagnostic cmap-only probes isolate U+2010 as Virtua's displayed break
glyph; diagnostic binaries are not source/release candidates. Preserved-ignorable
HarfBuzz output still exposes missing U+00AD, unlike Rubik. Six actual Diffenator
Virtua/Rubik screenshots and six controlled browser screenshots inspected.
No new drawing, build, preflight or whole-suite claim. Current12 FAIL/9 WARN
package QA and216 Hebrew engineering failures remain; gap340 unchanged. Next
encoded U+00AD compatibility wrapper using the exact unchanged hyphen, then
independent Common gaps. Arabic60272 untouched; local evidence only.

## Batch35 · Encoded soft-hyphen compatibility

[Evidence](batches/35-soft-hyphen/README.md): two purple U+00AD wrappers reuse
unchanged hyphen components,440 advances; six source files,1817 others unchanged.
Arabic326/master and green131/74 bytes preserved.209 scoped checks,4475 old VF
and3579 old static exact ink/advance comparisons,27 Latin plus two helper methods,
unchanged216 baseline Hebrew failures and preflight complete. Grid0. Whole
400/550/700 and224px diagnostic ink, actual browser line breaks and Diffenator
supplement/stock first view inspected. Browser measurements match batch34 exactly.
No claim this changes already working normal browser behavior.

Full online unexcluded package12 FAIL/10 WARN/159 PASS/10 INFO/40 SKIP: FAILs
unchanged, one new soft_hyphen presence-policy warning. Fontspector recommends
omitting U+00AD; local compatibility addition remains pending release retain/omit
review. No exclusions or false passing claim. Rubik gap339 (182 Cyrillic,55 Common,
102 Arabic presentation forms). Next separate U+2011 behavior assessment, then
Common symbols; no automatic alias from cmap counts. Local only/no push.

## Batch36 · Nonbreaking-hyphen assessment

[Evidence](batches/36-nonbreaking-hyphen-assessment/README.md) freezes cd4e4fd7:
all1823 sources and five active font hashes unchanged.80 direct shaping samples
and30 real-subset samples show full Virtua falls back from U+2011 to U+2010;
text-only subsets can drop that fallback. Pinned Rubik lacks both cmap entries
and yields .notdef directly, although browser fallback visibly supplies a hyphen.
Twelve actual browser/Diffenator images at400/550/700 inspected: U+2011 stays
unbroken, ordinary hyphens wrap. Cmap-only H probes isolate Virtua's U+2010
routing without changing break semantics. Diagnostic fonts are never candidates.
No alias added; optional direct-cmap/subset coverage decision remains separate.
Current12 FAIL/10 WARN package,216 baseline failures and339 Rubik gap unchanged.
Next generic currency U+00A4 reference/donor assessment, then Common gaps.
Local read-only evidence; Arabic60272 unchanged; no push.

## Batch37 · Generic currency sign

[Evidence](batches/37-currency/README.md): two purple U+00A4 glyphs,608 advances,
56/48 bearings, ring plus four clipped arms; six compatible source contours.
Six source files;1819 other files/every old GLIF/Arabic/green source unchanged.
120 scoped checks,4480 old VF and3583 old static ink/advance comparisons,27 Latin
plus2 helper methods, exact216 baseline failures and preflight complete. Grid0.
Eight G2 cubic joins/master, no five-weight sampled reversals/proper crossings;
diagnostic union retains one counter. Whole400/550/700,224px detail, signed comb
and12 actual Diffenator stock/target screenshots inspected with Rubik. Compact
height, arm projection, weight balance/default pairs remain human review; generic
marks use right-side fallback. Online unexcluded package12FAIL10WARN159PASS10INFO40SKIP
unchanged, exact failures preserved. Rubik gap338 (182Cyrl/54Common/102Arab).
Next superior-digit donor/coverage inspection for U00B9/U00B2/U00B3. Local only.


## Batch38 · Superior-digit assessment

[Evidence](batches/38-superior-digit-assessment/README.md): read-only at4a940d06,
all1825 sources and five active font hashes unchanged. No existing superior
or numerator donors; green one/two/three source construction and three-member
reverse closures/master frozen, no Arabic intersection.60 direct shaping cases
with four feature modes and40 real-subset cases with two modes establish that
Virtua lacks encoded¹²³ and sups, while Rubik supports both. NFKD drops the
superior distinction; ordinary-digit aliases are not a fix. Default fontTools
subsetting drops Rubik sups for plain123; retaining features preserves it.
Five full rasters and15 actual browser/Diffenator images400/550/700 inspected.
Controlled Virtua text uses unidentified fallback ink; Diffenator shows boxes.
No source/build/preflight/new full-QA claim; batch37 package12FAIL10WARN and216
baseline Hebrew failures remain. Gap338 unchanged. Next bounded encoded1/2/3
superior drafts; preserve Virtua curved flag/rounded three and all green donors.
Local evidence only; Arabic60272 unchanged; no push.


## Batch39 · Encoded superior digits

[Evidence](batches/39-superior-digits/README.md): purple onesuperior/twosuperior/
threesuperior in both masters,16/35/50-point compatible contours derived from
unchanged protected figures. Ten source files;1821 others/every old GLIF/Arabic
and green bytes preserved. Advances232/264,328/352,352/376, all new values on8.
Initial two tangent kinks rejected; final G1 diagonal joins and open counters.
145 scoped checks,4485 old VF and3587 static exact ink/advance comparisons,54 real
subset/NFD cases,27 Latin plus2 helpers, exact216 baseline failures and preflight
complete. Whole400/550/700,224px details/comb and12 actual Diffenator target/stock
views inspected against Rubik. Regular2/3 lighter than Rubik; weight balance,
default pairs and right-side generic accents remain review. No sups feature or
ordinary-size alias. Online unexcluded package12FAIL10WARN159PASS10INFO40SKIP,
exact failures/no new semantic warnings. Gap335:182Cyrl/51Common/102Arab.
Next remaining superior0/4–9 construction/figure-family inspection, then bounded
extension and Common gaps. Human approval/release blockers remain; local/no push.


## Batch40 · Superior zero

[Evidence](batches/40-superior-zero/README.md): purple U2070 in both masters,
two12-point oval contours from protected zero construction. Advances368/416,
40 bearings, cardinal side weights56/88 and vertical48/80; all new values on8.
Six source files;1827 others/every old GLIF/Arabic/green bytes unchanged.125 scoped
checks,4500 old VF/3599 old static exact ink/advance comparisons,54 real subsets,
27 Latin plus2 helpers, unchanged216 baseline failures and preflight complete.
Eight G2 joins/master; no sampled reversals/proper crossings at five weights.
Whole400/550/700,224px details/comb and12 actual Diffenator images inspected.
Oval width/counter, partial-family weight and default spacing remain human review;
generic marks retain right fallback, no sups feature. Online package12FAIL10WARN
159PASS10INFO40SKIP; FAILs exact unchanged but unreachable-subsetting warning
expands by U2070 (installed gfsubsets: math only). No exclusions or unrelated
subset declaration. Gap334:182Cyrl/50Common/102Arab. Inventory0/4–9 frozen; next
bounded superior4/5, then6–9. Local only/no push; Arabic60272 unchanged.
