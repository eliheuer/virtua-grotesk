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

1. Batch25 fixes breve contour direction without moving geometry; do not redo it. Batch26 adds U0312 and batch27 adds U0335 with a narrow variant. Next the two remaining overlay marks U0337/U0338 and independent common-symbol gaps. Current online package QA is10 FAIL/9 WARN; serving-set mappings need a separate coverage/policy decision, not false subset declarations. Fi/fl are complete in batch22; retain optical pair-spacing review. Long s/florin/kra/apostrophe-n are added in batches18–21; do not redo them. Tbar/tbar are added in batch17; retain their separate pair-spacing follow-up. Narrow I/l and off8 K/c/k/t spacing exceptions remain measured in batch14; batch16 fixes only the six safe Bold c/k/t wrappers. Preserve base geometry/overhangs and keep these exceptions open for review. Hcaron attachment is repaired in batch15; do not redo it. Preserve intentional alternate-caron side spacing. Then remaining Latin coverage. Generic g+U0326 still collides inside its descender; preserve the green base while diagnosing attachment. Preserve the rotated ģ placement introduced in batch07. Check full reverse closure for green/Arabic dependencies and preserve the shared
   reversed-Nun calibration when changing any dot geometry or anchors.
2. Spacing constraint reaffirmed by Eli: use the powers-of-two system for
sidebearings, advances and kerning. New machine values on8; record decompositions
and preserve green/human optical exceptions. See DESIGN.md#spacing.

3. Existing precomposed widths differ from the base+mark fallback by up to
   tens of units. `verification.json` retains the measured sample differences.
   Inspect wrapper metrics/kerning and word spacing before applying changes.
4. No missing Latin-script codepoints in the pinned Rubik cmap comparison after batch22. This is not full language coverage or visual approval. Review encoded ligatures
   separately from GSUB behavior. Four combining marks, punctuation, fractions,
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
