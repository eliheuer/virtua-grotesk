# Google Fonts onboarding

Official guidance checked on **2026-10-18**. This is the single active release
checklist. The [September 7 review](../archive/release-review-2026-09-07.md)
and its artifacts are historical evidence.

## Release scope

Eli confirmed **Latin, Arabic, and Hebrew** on September 9. On October 21 he
requested Rubik-level quality and language coverage, which also requires
**Cyrillic and extended Cyrillic**. The current build still covers only the
original three scripts; do not declare Cyrillic in package metadata yet.
The family is upright, wght 400–700, with Regular, Medium, SemiBold, and Bold
instances. Italic remains a [separate proposal](../goal-google-fonts-launch.md).
Do not drop Hebrew or Arabic from the export or metadata to reduce QA findings.

The upstream is `https://github.com/eliheuer/virtua-grotesk`. Source and build
instructions are in the [README](../../README.md); the font license is
[OFL.txt](../../OFL.txt). AI assistance is disclosed in the README and article.
The public name remains **Virtua Grotesk**.

The reusable [chat proof workflow](../qa.md#chat-proof-workflow) and
`scripts/proof_compare.py` let subsequent sessions generate comparable shaped
before/after proofs. Historical `out/qa/` evidence remains local and ignored.

## Current preparation — 2026-10-21

Arabic handoff `889ffa58` is committed and pushed for Eli's manual drawing.
The recurring Arabic pass is paused; source changes now focus on independent
Latin and release work. [LAT-001](../../agent-proofs/cases/latin-001/README.md)
records exact snapshots, source changes, raster review, tests and the next queue.
The attachment/coverage checkpoint1e8dd28e is also pushed with Eli’s approval.
Subsequent accent drawing batches remain local.
The previous dated sections below are historical evidence.

Applied thirteen Regular combining-offset fixes, stack-anchor propagation,
ten missing Latin composites in both masters, and a measured Windows clipping
ascent of1488. Typographic line spacing and all Arabic GLIFs remain unchanged.
Three new Latin regression tests and240 scoped comparisons pass; build and
preflight complete. Subsequent LAT-001 batch02 strengthens acute/grave and
macron ink in four donor GLIFs, with endpoint/intermediate whole-word rasters and
80 scoped shaping checks. Its full-suite delta is zero; the existing online QA
counts below precede these drawing batches and are not a fresh certification.
Batch03 adds two Bold chevron donor repairs with90 scoped shaping checks, whole
word/stack rasters and a224px/em detail; all Regular/Arabic sources are unchanged.
Batch04 repairs both ring donors and their outgoing stack anchors in four GLIFs,
with90 shaping checks and full endpoint/intermediate image review. All other
source bytes remain unchanged. Batch05 rounds both breve bowls and adds Bold
weight in four GLIFs, with90 shaping checks and whole-image review at three
weights; all other source bytes unchanged. Batch06 repairs both tilde waves and
stack anchors in four GLIFs, with90 shaping checks, whole-image review and zero
grid findings; all other source bytes unchanged. Batch07 corrects twenty Latvian
composite constructions and adds canonical fallback in both feature files.205
scoped comparisons and four Latin tests pass, with whole images at three weights;
batch08 then repairs both comma-accent donor weights/terminals in two GLIFs.
Its220 scoped comparisons, four Latin tests and complete images pass the local
checks. Generic g+U0326 descender attachment remains unresolved. Batch09 rounds
cedilla hooks and updates bottom anchors, with90 scoped checks, five Latin tests
and complete images. Its deeper stacks exposed clipping, fixed by Windows
descent512→576 in both masters; typographic metrics stay unchanged. Legacy
Windows-metric line spacing still needs platform testing. Batch10 rounds ogonek hooks, fixes fourteen local placements (including detached Ą),
and adds canonical ogonek composition.100 scoped comparisons, six Latin tests and
whole400/550/700 images completed; no base/Arabic/green source changes. Independent
RAQM proofs resolve a DesignBot decomposed-row discrepancy. Missing ogonek cmap
plus acute still fails40 VF samples before/after and remains a serving-subset
follow-up. Batch11 repairs alternate-caron donors/placements and the wrong
uppercase Ť construction in12 GLIFs, with grid spacing and five canonical
compositions/master.135 scoped checks, seven Latin tests and full images at three
weights completed; optical spacing and reader review remain pending.
All216 pre-existing Hebrew regression subcases still fail
(105 cantillation clearance,111 meteg/composition). Frozen-baseline comparison
shows no new failures; this does not waive the existing failures.

| Current unexcluded online run | FAIL | WARN | PASS | INFO | SKIP |
| --- | ---: | ---: | ---: | ---: | ---: |
| Five active binaries | 1 | 29 | 529 | 39 | 294 |
| Local VF package | 10 | 8 | 160 | 10 | 41 |

The loose-font failure is the `ttf` directory name. Package failures are serving-
subset reachability for U+0302, U+0331 and U+1EBC/U+1EBD, including newly exposed
Aleut support. No exclusions or misleading subset declarations were added.
Current local evidence: `out/qa/2026-10-21-latin-applied/` and
`out/qa/2026-10-21-latin-package/`; compact findings and hashes are retained in
LAT-001. Source revision before this batch is889ffa58; its final identities are
in `final-identity.json`. The package is unpublished and carries provisional
date/primary-script/source-delivery choices, with existing artwork pending approval.

The pinned official Rubik comparison now finds8 missing Latin codepoints,
182 Cyrillic,4 inherited/common combining marks,62 common symbols and102 Arabic
presentation forms. Those are encoded-character differences, not language counts.
Cyrillic requires actual drawing and reader review. Arabic presentation forms
need a GSUB/legacy-text assessment; they are not an automatic new-glyph queue.
Latin accent review, bottom-mark shapes, wrapper spacing on the dyadic grid,
Hebrew regression repair, Arabic manual review, CI and package provenance remain
open. **The family is not ready for submission or publication.**

## Historical evidence — 2026-10-18

**Not ready for Google Fonts release.** Engineering repairs and all 54 formerly
blank Hebrew glyph drafts are applied under Eli's authorization. Every encoded
visible character now has ink. This establishes draft coverage, not finished
drawings or native-reader approval; no cmap entries or QA checks were removed. The
[September 9 audit](audit-2026-09-09.md) is historical evidence.

Built the variable font and four statics using the latest stable build/QA
packages rechecked against PyPI and the official Fontspector release on October 18.
Pinned the updated environment in `requirements.txt`; see the
[tool versions](../qa.md#tools). `make setup` now installs checksum-verified
Fontspector into `.venv/bin`, used by both local QA and CI. The older global
Fontspector 1.6.0 is no longer selected by the project wrapper.
Ran the full Google Fonts profile with **Fontspector 1.9.0**, no exclusions,
and network checks enabled. The macOS executable was downloaded from the
[official release](https://github.com/fonttools/fontspector/releases/tag/fontspector-v1.9.0)
and checked against its published SHA-256. CI now pins the same version and
its Linux checksum; that updated workflow has not been run on GitHub.

| Run | FAIL | WARN | PASS | INFO | SKIP |
| --- | ---: | ---: | ---: | ---: | ---: |
| Five binaries before repairs | 6 | 59 | 506 | 39 | 306 |
| Five binaries after approved Hebrew repairs | 6 | 47 | 526 | 39 | 294 |
| Five binaries after latest-tools pass | 6 | 36 | 527 | 39 | 294 |
| One-VF package before repairs | 7 | 28 | 155 | 10 | 41 |
| One-VF package after approved Hebrew repairs | 7 | 26 | 157 | 10 | 41 |
| One-VF package after latest-tools pass | 7 | 14 | 159 | 10 | 41 |
| Five binaries after approved macron-below application | **6** | **36** | **527** | **39** | **294** |
| One-VF package after approved macron-below application | 11 | 14 | 159 | 10 | 41 |
| Five binaries after approved hyphen application | **6** | **36** | **527** | **39** | **294** |
| One-VF package after approved hyphen application | 11 | 14 | 159 | 10 | 41 |
| Five binaries after approved double-vav application | **6** | **36** | **527** | **39** | **294** |
| One-VF package after approved double-vav application | 11 | 14 | 159 | 10 | 41 |
| Five binaries after VAV-YOD and seen cleanup | **6** | **35** | **528** | **39** | **294** |
| One-VF package after VAV-YOD and seen cleanup | **11** | **13** | **160** | **10** | **41** |
| Five binaries after approved accent winding repair | **6** | **35** | **528** | **39** | **294** |
| One-VF package after approved accent winding repair | **11** | **13** | **160** | **10** | **41** |
| Five binaries after approved final-alef/lam repair | **6** | **35** | **528** | **39** | **294** |
| One-VF package after approved final-alef/lam repair | **11** | **13** | **160** | **10** | **41** |
| Five binaries after approved medial-ain repair | **6** | **35** | **528** | **39** | **294** |
| One-VF package after approved medial-ain repair | **11** | **13** | **160** | **10** | **41** |
| Five binaries after approved medial-meem repair | **6** | **35** | **528** | **39** | **294** |
| One-VF package after approved medial-meem repair | **11** | **13** | **160** | **10** | **41** |
| Five binaries after approved initial-heh repair | **6** | **35** | **528** | **39** | **294** |
| One-VF package after approved initial-heh repair | **11** | **13** | **160** | **10** | **41** |
| Five binaries after autonomous QA repairs and Eng/eng | **6** | **28** | **530** | **39** | **294** |
| One-VF package after autonomous QA repairs and Eng/eng | **10** | **6** | **162** | **10** | **41** |
| Five binaries after tilde/anchor/recomposition source repairs | **6** | **28** | **530** | **39** | **294** |
| One-VF package after tilde/anchor/recomposition source repairs | **10** | **6** | **162** | **10** | **41** |
| Five binaries after eleven Hebrew drawing drafts | **1** | **28** | **530** | **39** | **294** |
| One-VF package after eleven Hebrew drawing drafts | **9** | **6** | **162** | **10** | **41** |
| Five binaries after the remaining 43 Hebrew drafts | **1** | **28** | **530** | **39** | **294** |
| One-VF package after the remaining 43 Hebrew drafts | **9** | **6** | **162** | **10** | **41** |

Commit handoff: the proof renderer, sample recipe, and workflow documentation are
tracked; raw batch evidence remains under ignored `out/qa/`. The local tested
source state includes a pre-existing Regular `.notdef` color-only change that is
left outside this QA commit, along with unrelated graph/social/scoreboard work.
Its outline and metrics match HEAD. Source hashes above therefore describe the
local tested snapshot, not a claim of a clean-checkout CI run.

These are result-severity counts, not unique defects. No ERROR or FATAL results.
The only loose-font FAIL is an upstream `ttf/` directory-name mismatch; the
correctly named local package passes that check. The current package has nine
subset-reachability results. The eleven-glyph blank-outline failure is resolved.
Neither gate passes; absence of a blank-outline failure does not establish
complete coverage or drawing quality.

### Repairs applied

- U+200B ZERO WIDTH SPACE now has zero advance in both masters and all outputs.
- Classified 280 previously uncategorized letter/base glyphs and 36 Hebrew
  combining marks in each master's GDEF source metadata. Added the missing
  Bold anchor-propagation filter and registered the Hebrew language system.
  Lithuanian composite-accent attachment warnings are resolved in all five
  outputs. This does not establish optical or native-reader approval.
- Applied Eli-approved Hebrew anchor and zero-width mark repairs: 72 Hebrew
  glyphs plus the dotted-circle placeholder receive anchors in each master;
  36 combining marks per master receive zero advance. Original outlines and
  colors are unchanged, including protected glyphs. All five outputs pass the
  Hebrew attachment audit and the GDEF/dotted-circle checks. Reviewed Hebrew
  renders at 400/550/700 and the isolated-mark dotted-circle proof.
- Added weight/italic STAT metadata to the static fonts. Removed the unused
  `a.bold` from the Regular export while retaining the VF rule and heavier
  instances. HarfBuzz verifies the alternate switches at weight 500.
- Converted six malformed Regular kerning group pairs into ten explicit
  pairs using their existing group memberships and values. Preserved the
  existing `r/o = -64` override. HarfBuzz verifies all ten repaired pairs.
- Removed the obsolete `outline_alignment_miss` development exclusion after
  it passed on all five fonts. The remaining three exclusions are still
  development debt, not release exceptions. Full QA remains unexcluded.

- Corrected Bold `qafDotless-ar.fina` advance from 1072 to its right joining
  edge at 512. The existing outline, anchors, and color are unchanged. This
  restores the join in `بٯ` and resolves both suspicious-sidebearing warnings.
- Aligned contour start points in editable Bold `w`, Regular comma, and
  Regular quotesingle. These are cyclic permutations of unchanged point
  records; the protected opposite masters were untouched. This removes nine
  interpolation warnings, including inherited w/quote forms and the straight
  quote's intermediate underweight warning. See the
  [worklog](../design-pass-worklog.md) for measurements.
- Added an outlined, 1600×900 SVG article specimen generated from the built
  font with `scripts/article_specimen.py`. Package QA now includes and hashes
  article assets, and validates the image reference. Final artwork selection
  and the required image-license approval remain maintainer decisions.
- Replaced the Diffenator2 browser-proof command with Diffenator3's
  `diff3proof`. Diffenator2 0.5.0 requires protobuf ≤3.20.3 and cannot share
  the current gftools environment, which requires protobuf ≥6.33.0.

Thirteen regression tests pass, including compiled-font mark attachment,
kerning, metadata, and dotless-qaf joining at all four instance weights.
Master structural compatibility reports zero blocking mismatches. Preflight
passes using the newly built binaries. No exclusions were added.

The four edited source GLIFs preserve every master point coordinate, component,
anchor, and color. The only advance change in this pass is Bold dotless-qaf.
Canonical contour comparison confirms identical Regular/Bold geometry and
unchanged cmap in all five fonts. Medium/SemiBold geometry changes only in the
11 forms inheriting the repaired w/comma/straight-quote correspondence. The
new compiler also changes generated GDEF/GPOS; attachment regressions pass.
Existing local edits, including Regular `.notdef`, were preserved.

Regenerated the 24-page designbot PDF and Diffenator3 browser proof. Inspected
the article specimen, dotless-qaf joining before/after, and point-order
candidate at 400/550/700 in the browser. Also inspected Arabic text at 400/700
in Diffenator3. Earlier Hebrew/Latin proof review is retained as historical
evidence. This is limited visual QA, not print or native-reader approval.
Bold `ū́` stack clearance and unfinished Arabic positioning still need review.

### Applied approved candidate — U+0331

Eli reviewed and approved applying `macronbelowcomb` and the `a.bold` base
classification to both active masters. The mark reuses the existing `macron`
component at yOffset -824, with zero advance and `_bottom` at (180, 0).
Only the new GLIFs and their contents/glyph-order/class registrations changed;
all existing GLIFs, anchors, colors, and unrelated staged work were preserved.

All five rebuilt fonts match the reviewed candidate's compiled tables except
head timestamps/checksums. Attachment passes at VF weights 400, 499, 500, 550,
and 700 and in all four statics. The active build's proof was visually inspected
at 400, 550, and 700. The three target language samples shape without missing
glyphs. Nine compiled engineering tests and four QA-entrypoint tests pass;
master compatibility has zero blocking mismatches and preflight artifacts exist.

Current package QA is **11 FAIL / 14 WARN**, with no tool errors and network
checks enabled. U+0331 now renders in the font but is absent from the declared
Google Fonts serving subsets. Adding it also exposes additional languages with
subset-data problems; the higher failure count does not indicate a regression
in the approved drawing or attachment. No exclusions or subset changes were made.
Evidence and reversible backups are in `out/qa/2026-10-17/applied-macron-below/`.
The original reviewed candidate remains in `macron-below-candidate/`.

### All nine remaining package failures

| Count | Check / cause | What resolves it |
| ---: | --- | --- |
| 6 | `tofu/missing-subsetted`: Amarakaeri, Chickasaw, Mezquital Otomi, Secoya, Siona, and Ticuna require U+0331 | The mark is now present and attaches. Correct the Google Fonts subset definitions or agree a serving strategy with onboarding reviewers. |
| 3 | `tofu/missing-subsetted`: Guarani and Yanomamö require U+1EBD; Ticuna requires U+1EBC/U+1EBD | These drawings exist but are outside the declared serving subsets. Resolve the subset-data issue; adding unrelated subsets solely to hide it would misrepresent coverage. |

### Applied approved hyphen and double vav

Eli approved applying U+2010 HYPHEN and subsequently U+05F0 DOUBLE VAV to both
active masters. Hyphen reuses the existing `hyphen` component at advance 440.
Double vav uses two unchanged `vav-hb` components: Regular offsets 0/240,
advance 480; Bold offsets 0/328, advance 656. Colors and unrelated source files
are unchanged. Reuse does not independently approve the original vav designs.

All five active binaries match the reviewed double-vav candidate's compiled
tables except timestamps/checksum. That candidate's comparison and Yiddish
proof was inspected at 400/550/700. The geometry matches two vavs at
400/500/550/600/700 and all four statics; Medium/SemiBold widths differ from
twice the independently rounded single-vav width by one unit. Nine compiled
regression tests pass, master compatibility has zero blocking mismatches, and
the main PDF, reports, and preflight were regenerated. Source-file hashes and
the staged patch confirm unrelated work was preserved.

At the double-vav stage, online package QA was **11 FAIL / 14 WARN**, with no tool errors.
The aggregate empty-outline list is down to 14 glyphs (16 before hyphen and
double vav). Evidence and backups are in `out/qa/2026-10-17/applied-double-vav/`;
`applied-hyphen/` and the original candidates retain the earlier evidence.

### Applied approved VAV-YOD and seen cleanup

Eli approved preparing and applying U+05F1 VAV-YOD if its checks passed, and
removing the five collapsed contours from `seen-ar.medi` in both masters only
if rendering remained identical, including a named exception for green Regular.
Both conditions passed before application. Only four GLIF files changed.

`vavyod-hb` now uses yod on the left and vav on the right, at advances 480
Regular / 656 Bold. Both original component drawings are untouched. Seen's
visible contour, advance, anchors, and colors are unchanged; only five contours
whose every point was (576, -16) were removed from each master.

The candidate matches the existing VAV-YOD sequence. Seen, sheen, and six-dot
seen medial glyphs have identical raster output in **144 comparisons**: four
pixel sizes, four statics, and eight VF weights from 400 to 700. Sixty shaping
comparisons also agree, and all other visible glyph geometry and metrics are
unchanged. The comparison proof was inspected at 400/550/700. All nine compiled
regression tests pass; both edited masters pass curve lint; structural
compatibility has zero blocking mismatches. Active font tables match the
verified candidate except timestamps/checksums. The main proof, reports, and
preflight were regenerated.

Current package QA is **11 FAIL / 13 WARN**, with no tool errors and no new
warning/failure categories. `overlapping_path_segments` now passes for the VF
package. The empty-outline failure lists 13 glyphs rather than 14. The five-font
run is **6 FAIL / 35 WARN**; existing static-font warnings remain separate.
Evidence and reversible backups: `out/qa/2026-10-17/applied-vavyod-seen/`.
The reviewed candidate and rendering checks remain in `vavyod-seen-candidate/`.

### Applied approved caron/circumflex winding repair

Reversed the single line contour in `caron` and `circumflex` in both masters,
retaining every coordinate, anchor, advance, and color. The change propagates
to 41 composites. Initial application was conditional on identical rendering;
that condition did not pass. In 2,064 comparisons, all 688 static-font cases
were identical, but 1,087 VF cases differed. Most were one-level antialiasing
changes; the meaningful change fills the white cutouts where the caron overlaps
the stems of `hcaron` and `kcaron`. Eli reviewed the 400/550/700 proof and explicitly
approved applying that visible effect. No other source geometry was edited.

The full-list direction check drops from 137 reported contour items in 130
glyphs to 94 items in 87 glyphs: **43 glyphs repaired**. The aggregate warning
remains because Arabic findings persist. Active online QA is **11 FAIL / 13 WARN**
for the package and **6 FAIL / 35 WARN** for five binaries, with no tool errors.
All nine engineering regressions pass, compatibility has zero blocking
mismatches, and all metrics/layout tables are unchanged. Active compiled tables
match the reviewed candidate except timestamps/checksums. Reports, main PDF,
and preflight were refreshed. Official release metadata again confirmed the
installed Fontspector 1.9.0 and ten Python build/QA packages are latest stable.
Evidence/backups: `out/qa/2026-10-17/applied-accent-winding/`;
full rendering comparisons: `accent-winding-candidate/verification.json`.

### Applied approved final-alef/lam repair

Eli reviewed the combined proof and approved applying Regular `alef-ar.fina`
and `lam-ar.medi` in both masters. Only those three GLIFs changed. Traversal
was reversed and the Regular alef start point aligned with Bold; every source
coordinate, anchor, advance, and color is preserved. At weight 500, the alef
stem at y=500 is now 114.67 units instead of 2.67; at weight 550, 128 instead
of 40. The lam winding repair removes the lam–alef overlap cutouts exposed
by the alef-only candidate and already present in the original Bold.

The 400/500/550/700 comparison proof, marked medial-lam contexts at 400/550/700,
and enlarged lam rendering were inspected before user approval. Exact source
segment geometry is preserved in both masters. Existing Bold lam shape details
remain; this does not establish new drawing or native-reader approval.

All five active binaries match the reviewed candidate's compiled tables except
head timestamps/checksums. Nine regression tests pass, compatibility has zero
blocking mismatches, and curve lint passes in both masters. The candidate's
180 shaping comparisons agree with the original build. Unrelated compiled
geometry, all advances, and layout tables are unchanged. Source hashes confirm
only the three approved GLIFs changed; the staged index is untouched. Main PDF,
reports, and preflight were refreshed after rebuilding.

Active online package QA is **11 FAIL / 13 WARN**; five-font QA is
**6 FAIL / 35 WARN**, with no tool errors. Direction findings drop from 94 to
78 individual contour items, clearing all eleven affected glyphs from that
check. Other Arabic defects keep the aggregate warning open. The remaining
failure categories are unchanged; no exclusions or metadata scope changes were
introduced.

Evidence and reversible backups: `out/qa/2026-10-17/applied-final-alef-lam/`.
The reviewed candidate remains in `final-alef-lam-candidate/`; the initial
alef-only experiment remains in `final-alef-candidate/`.

### Applied approved medial-beh repair

Eli reviewed and approved applying `behDotless-ar.medi` in both masters. Only
those two GLIFs changed. Reversing the single 26-point contour preserves exact
source segment geometry, anchors, advances, and colors. All thirteen affected
medial forms were inspected before/after at 400/550/700, along with joined
contexts and an enlarged glyph. Existing drawing details remain unchanged.

All five active font binaries match the reviewed candidate's compiled tables
except head timestamps/checksums. Nine regression tests pass; master compatibility
has zero blocking mismatches. Both masters pass curve lint. Candidate verification
includes 192 identical shaping comparisons and unchanged unrelated compiled
geometry, advances, and layout tables. All 208 static bitmap comparisons are
identical; the 416 VF comparisons differ only in pixel shading (414 by at most
1/255; two 12px noon cases at weights 499/500 by at most 3/255). All bitmap bounds
and advances match. No visible contour or overlap change was observed in the
inspected proof. This is not native-reader or new drawing approval.

Active online package QA is **11 FAIL / 13 WARN**; five-font QA is
**6 FAIL / 35 WARN**, without tool errors. Direction findings drop from 78 to
65 individual items, clearing all thirteen affected glyphs. Other Arabic forms
keep the aggregate warning open. The failure categories remain unchanged.
Main PDF, reports, and preflight were refreshed; final hashes confirm exactly
the approved source scope and untouched staged work. No exclusions were added.

Evidence/backups: `out/qa/2026-10-17/applied-medial-beh/`.
The reviewed proof and candidate remain in `medial-beh-candidate/`.

### Applied approved hah-family repair

Eli approved applying `hah-ar`, `hah-ar.init`, `hah-ar.medi`, and
`hah-ar.fina` in both masters, including the reviewed jeem dot/bowl overlap
fill change. Exactly those eight GLIFs changed from the application baseline.
Their reversed contours preserve exact source segment geometry, anchors,
advances, colors, and unfinished Bold drawing details. All fifteen affected
forms were inspected at 400/550/700, in joined contexts and enlarged roots.

All five rebuilt fonts match the reviewed candidate tables, excluding only
build timestamps and checksum adjustment. Nine regression tests pass, and
there are zero blocking master-compatibility mismatches. The candidate's 228
shaping comparisons pass; unrelated compiled geometry, advances, and layout
tables remain unchanged. Regular curve lint is clean. Bold initial hah retains
the existing tension warning at (176,312), ratio 2.7, verified unchanged.

All 240 static bitmap comparisons were identical. Of 480 VF comparisons, 440
differed by at most one pixel-intensity level; 40 jeem cases had larger changes
from filling the existing dot/bowl overlap. Eli explicitly approved that visible
effect after reviewing `jeem-overlap.png`. No dot or bowl coordinates moved.

Online package QA is **11 FAIL / 13 WARN**; the full five-font run is
**6 FAIL / 35 WARN**, with no tool errors or new severity/code categories.
Direction findings fall from 65 to 50 items (48 distinct glyphs), clearing all
fifteen affected glyphs. Other Arabic forms keep the aggregate warning open.
Reports, the main designbot PDF proof, and artifact-presence preflight were
refreshed. These results do not establish release or native-reader approval.

Evidence and reversible backups: `out/qa/2026-10-17/applied-hah-family/`.
`proof.png` and the affected-form atlases are the reviewed candidate images;
active font table equivalence connects those proofs to this application.
`manifest.json` records source and binary hashes, scope, and verification.
The staged index and unrelated sources were verified unchanged.

### Applied approved feh-family repair (2026-10-18)

Eli approved applying `fehDotless-ar`, `fehDotless-ar.init`, and
`fehDotless-ar.medi` in both masters, including the reviewed dot/bowl overlap
fill effect. Exactly six GLIFs changed from the application baseline. Both
contours were reversed independently; exact source segments, anchors, advances,
colors, and existing drawing details are preserved. All five rebuilt fonts match
the reviewed candidate tables apart from build timestamps and checksum adjustment.

Nine regression tests pass; structural compatibility has zero blocking issues.
The candidate's 252 shaping comparisons pass, and all nineteen inherited forms
were inspected at 400/550/700 with joined contexts and enlarged roots. Layout
tables, advances, and unrelated compiled geometry are unchanged. All 304 static
bitmap comparisons were identical. Of 608 VF comparisons, 519 differed by at
most one pixel-intensity level; 89 had larger changes around dot/bowl overlaps.
Bounds were identical. The approved visible fill change is shown in `overlap.png`.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **50 to 31 items**, leaving 29 distinct glyphs. All nineteen affected
forms clear that check; other roots keep the aggregate warning open. Reports,
the main designbot PDF, and artifact-presence preflight were refreshed.
Fontspector 1.9.0 and all ten tracked Python build/QA packages were rechecked
against official releases/PyPI on 2026-10-18 and are current stable versions.

Eli raised the visible lumpiness in the proof. Read-only diagnosis confirms
pre-existing misaligned handles in Bold `fehDotless-ar.medi` and `dotabove-ar`,
with identical point coordinates already present at checkout HEAD. The medial
counter's bottom join changes tangent direction by about 48.6 degrees despite
its smooth flag; other counter joins differ by about 15 degrees. The dot also
has misaligned handles. Existing curve lint reports these glyphs clean: it does
not establish tangent continuity or visual quality. These defects, the Bold
outer shapes, and joining gaps remain unchanged by the winding repair.

Eli deferred smoothing until after the QA failures and warnings are addressed.
The Bold medial-feh counter and dot handle defects remain recorded above; no
smoothing is authorized or prepared.

Evidence/backups: `out/qa/2026-10-18/applied-feh-family/`, including the reviewed
proofs, `verification.json`, `manifest.json`, `lumpiness-diagnosis.json`, and
current QA logs. The scratch candidate remains in `feh-family-candidate/`.
Unrelated sources and the staged index were verified unchanged.

### Applied approved qaf-family repair (2026-10-18)

Eli approved applying `qafDotless-ar` and `qafDotless-ar.fina` in both masters,
including the reviewed below-dot overlap fill changes. Exactly four GLIFs
changed from the application baseline. Both contours were reversed independently;
exact source segments, anchors, advances, colors, and unfinished details remain.
All five rebuilt fonts match the reviewed candidate tables apart from build
timestamps and checksum adjustment. Unrelated sources and the staged index
were verified unchanged.

Nine regression tests pass, and structural compatibility has zero blocking
issues. The candidate's 192 shaping comparisons pass; all twelve affected
forms were inspected at 400/550/700 with joined contexts, enlarged roots, and
a below-dot overlap proof. Advances, layout tables, and unrelated compiled
geometry remain unchanged. Curve lint reports clean before and after; this
does not establish visual design quality. All 192 static bitmap comparisons
were identical. Of 384 VF comparisons, 256 were identical or differed by at
most one pixel-intensity level; 128 had larger changes in the four below-dot
feh forms. Raster bounds were unchanged.

The approved fill change affects existing dot/body intersections in
`fehDotmovedbelow-ar` and `fehThreedotsbelow-ar`, isolated and final, as shown
in `overlap.png`. Dot placement, Bold shape defects, and existing joining gaps
are retained. Smoothing remains deferred until after the QA pass.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **31 to 19 items**, leaving 17 distinct glyphs. All twelve targeted
forms clear the check; other roots keep the aggregate warning open. Reports,
the main designbot PDF, and artifact-presence preflight were refreshed. The
toolchain remains the current stable baseline checked earlier on 2026-10-18.

Evidence/backups: `out/qa/2026-10-18/applied-qaf-family/`, including reviewed
proofs, `verification.json`, `manifest.json`, tool versions, and current QA logs.
The reviewed scratch candidate remains in `qaf-family-candidate/`.

### Applied approved dal-family repair (2026-10-18)

Eli approved applying `dal-ar` and `dal-ar.fina` in both masters, including
exceptions for all four green glyphs. Exactly four GLIFs changed from the
application baseline. Reversal preserves exact source segments, anchors,
advances, colors, and existing drawing details. All five rebuilt fonts match
the reviewed candidate tables apart from build timestamps and checksum
adjustment. Unrelated sources and the staged index were verified unchanged.

Nine regression tests pass, with zero blocking structural compatibility issues.
The candidate's 132 shaping comparisons pass. All four dal/thal forms were
inspected at 400/550/700 in isolated and joined contexts, with enlarged roots.
All 64 static bitmap comparisons were identical; all 128 VF comparisons differed
by at most one pixel-intensity level. Raster bounds, advances, layout tables,
and unrelated compiled geometry are unchanged. No visible fill change was
observed. Curve lint retains the existing final-dal tension warning at (408,184),
ratio 3.2, in both masters, with identical before/after logs. Smoothing and
existing unfinished drawing details remain deferred.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **19 to 15 items**, leaving 13 distinct glyphs; all four targeted
forms clear the check. Reports, the main designbot PDF, and artifact-presence
preflight were refreshed. The same current stable toolchain checked on
2026-10-18 was used.

Evidence/backups: `out/qa/2026-10-18/applied-dal-family/`, including reviewed
proofs, `verification.json`, `manifest.json`, tool versions, and current QA logs.
The reviewed scratch candidate remains in `dal-family-candidate/`.

### Applied approved waw-family repair (2026-10-18)

Eli approved applying `waw-ar` and `waw-ar.fina` in both masters, including
exceptions for the two green Bold glyphs. Exactly four GLIFs changed from the
application baseline. Both contours were reversed independently, preserving
exact source segments, anchors, advances, colors, and existing drawing details.
All five rebuilt fonts match the reviewed candidate tables apart from build
timestamps and checksum adjustment. Unrelated sources and the staged index
were verified unchanged.

Nine regression tests pass, with zero blocking structural compatibility issues.
The candidate's 132 shaping comparisons pass. All four affected forms were
inspected at 400/550/700 in isolated and joined contexts, with enlarged roots.
All 64 static bitmap comparisons were identical. Of 128 VF comparisons, 112
were identical or differed by at most one pixel-intensity level; 16 final-form
comparisons differed by 2–6 levels out of 255. No visible fill change was observed.
Raster bounds, advances, layout tables, and unrelated compiled geometry are
unchanged. Curve lint reports clean in both masters before and after; this
does not establish visual design quality. Drawing and joining defects remain
untouched, and smoothing is deferred.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **15 to 11 items**, leaving nine distinct glyphs; all four targeted
forms clear the check. Reports, the main designbot PDF, and artifact-presence
preflight were refreshed. The same current stable toolchain checked on
2026-10-18 was used.

Evidence/backups: `out/qa/2026-10-18/applied-waw-family/`, including reviewed
proofs, `verification.json`, `manifest.json`, tool versions, and current QA logs.
The reviewed scratch candidate remains in `waw-family-candidate/`.

### Applied approved initial-seen repair (2026-10-18)

Eli approved applying `seen-ar.init` in both masters, including exceptions for
both green glyphs. Exactly two GLIFs changed from the application baseline.
Contour reversal preserves exact source segments, anchors, advances, colors,
and existing drawing details. All five rebuilt fonts match the reviewed
candidate tables apart from build timestamps and checksum adjustment. Unrelated
sources and the staged index were verified unchanged.

Nine regression tests pass, with zero blocking structural compatibility issues.
The candidate's 108 shaping comparisons pass. All three affected initial
seen/sheen/six-dot-seen forms were inspected at 400/550/700, in joined and mark
contexts, with enlarged roots. All 48 static bitmap comparisons were identical;
all 96 VF comparisons differed by at most one pixel-intensity level. No visible
fill change was observed. Raster bounds, advances, layout tables, and unrelated
compiled geometry are unchanged. Curve lint reports clean before and after;
visual design quality remains separate. The existing weight mismatch, unfinished
six-dot form, and other drawing/joining details remain intact. Smoothing is deferred.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **11 to 8 items**, leaving six distinct glyphs; all three targeted
forms clear the check. Reports, the main designbot PDF, and artifact-presence
preflight were refreshed. The same current stable toolchain checked on
2026-10-18 was used.

Evidence/backups: `out/qa/2026-10-18/applied-initial-seen/`, including reviewed
proofs, `verification.json`, `manifest.json`, tool versions, and current QA logs.
The reviewed scratch candidate remains in `initial-seen-candidate/`.

### Applied approved medial-ain repair (2026-10-18)

Eli approved applying `ain-ar.medi` in both masters, including exceptions for
both green glyphs. Exactly two GLIFs changed from the application baseline.
Both contours were reversed independently, preserving exact source segments,
anchors, advances, colors, and existing drawing details. All five rebuilt fonts
match the reviewed candidate tables apart from build timestamps and checksum
adjustment. Unrelated sources and the staged index were verified unchanged.

Nine regression tests pass, with zero blocking structural compatibility issues.
The candidate's 96 shaping comparisons pass. Medial ain and ghain were inspected
at 400/550/700 in joined and mark contexts, with enlarged roots. All 32 static
bitmap comparisons were identical; all 64 VF comparisons differed by at most
one pixel-intensity level. No visible fill change was observed. Raster bounds,
advances, layout tables, and unrelated compiled geometry are unchanged. Curve
lint reports clean before and after; visual design quality remains separate.
Existing drawing and joining defects remain intact. Smoothing is deferred.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no tool errors or new severity/code categories. Direction findings
fall from **8 to 6 items**, leaving four distinct glyphs; both targeted forms
clear the check. Reports, the main designbot PDF, and artifact-presence preflight
were refreshed. The same current stable toolchain checked on 2026-10-18 was used.

Evidence/backups: `out/qa/2026-10-18/applied-medial-ain/`, including reviewed
proofs, `verification.json`, `manifest.json`, tool versions, and current QA logs.
The reviewed scratch candidate remains in `medial-ain-candidate/`.

Read-only diagnosis of all four remaining direction roots is recorded in
`remaining-direction-diagnosis.json`: medial meem (three outer-contour findings),
initial/medial heh, and final yeh. Heh and yeh edits have not been prepared.

### Applied approved medial-meem repair (2026-10-18)

Eli approved preparing and then applying `meem-ar.medi` in both masters,
including green Regular and the reviewed static edge differences. All four
contours were reversed independently. Exact source segments, contour separation,
anchors, advances, and colors are preserved. Only the two named GLIFs changed
from the application baseline; unrelated sources and the staged index remain
unchanged. No smoothing or contour merging is included. All five active rebuilt
fonts match the candidate tables apart from timestamps and checksum adjustment.

The active build passes nine regression tests and structural compatibility.
The reviewed candidate passes 96 shaping comparisons. Curve lint is clean before and after. Reviewed
joined and mark contexts at 400/550/700 and enlarged isolated forms. Existing
joining gaps and weight differences remain. All 32 VF raster comparisons differ
by at most one intensity level. Of 16 static comparisons, Bold is identical;
Regular, Medium, and SemiBold show small upper-right bowl/join edge differences
from the compiled curve approximation (up to 52 intensity levels at 256 px/em).
The enlarged `static-difference.png` shows these explicitly; static raster
identity is not claimed. Raster bounds, advances, layout tables, and unrelated
compiled geometry are unchanged.

Online package QA remains **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no new severity/code categories or tool errors. Direction findings fall
from **6 to 3**, leaving initial heh, medial heh, and final yeh. The aggregate
direction warning remains until its other glyphs are resolved. The separate
contour-count heuristic remains unchanged. Used the stable toolchain verified
on October 18, including Fontspector 1.9.0.

Evidence/backups: `out/qa/2026-10-18/applied-medial-meem/`, including `proof.png`,
`static-difference.png`, `verification.json`, `manifest.json`, and full/package
QA. Reports, the main designbot PDF, and artifact-presence preflight were refreshed.
The reviewed scratch evidence remains in `medial-meem-candidate/`.

Read-only diagnosis of initial heh is in `next-initial-heh-diagnosis.json`.

### Applied approved initial-heh repair (2026-10-18)

Eli approved preparing and then applying `heh-ar.init` in both masters,
including the reviewed heavier-static edge differences. Its outer contour and
counter were reversed independently. Exact source segments, anchors, advances,
and colors (yellow Regular, blue Bold) are preserved. Only the two named GLIFs
changed from the application baseline; unrelated sources and the staged index
remain unchanged. All five rebuilt fonts match the reviewed candidate tables
apart from timestamps and checksum adjustment.

The active build passes nine regression tests and structural compatibility.
The reviewed candidate passes 96 shaping comparisons. Reviewed joining and mark contexts at 400/550/700,
enlarged masters, and static before/after/difference renders. All eight Regular
and Medium static bitmap comparisons are identical. SemiBold and Bold have
small edge differences, up to 19 intensity levels at 256 px/em; all 32 VF
comparisons differ by at most one intensity level. Bounds, advances, layout
tables, and unrelated compiled geometry are unchanged. Existing Bold counter
irregularities and joining details remain; smoothing is deferred.

Curve lint retains the same six crest and two tension findings in Bold.
Regular's four crest findings disappear after reversal despite exact segment
identity: the heuristic is sensitive to traversal order, so this is not evidence
of a drawing repair. The before/after lint logs are retained.

Online package QA is **11 FAIL / 13 WARN / 160 PASS / 10 INFO / 41 SKIP**;
full five-font QA is **6 FAIL / 35 WARN / 528 PASS / 39 INFO / 294 SKIP**.
There are no new severity/code categories or tool errors. Direction findings fall
from **3 to 2**, leaving medial heh and final yeh. Used the same stable toolchain
verified on October 18, including Fontspector 1.9.0.

Evidence/backups: `out/qa/2026-10-18/applied-initial-heh/`, including `proof.png`,
`large-heh.png`, `static-difference.png`, `verification.json`, `manifest.json`,
and full/package QA. Reports, the main designbot PDF, and artifact-presence
preflight were refreshed. Reviewed scratch evidence remains in
`initial-heh-candidate/`.

Read-only diagnosis of the next proposed target is in
`next-medial-heh-diagnosis.json`: reverse the outer contour and both counters
of `heh-ar.medi` in both masters, retaining exact geometry and metadata. Both
masters are green and require a named exception. No dependent forms were found.
The later autonomous QA pass below prepared, verified, and applied medial heh.
Eli superseded the per-edit approval requirement for targeted repairs in this task.

### Autonomous QA repair pass (2026-10-18)

Eli explicitly authorized targeted QA repairs without asking for each glyph.
Scratch builds, backups, compiled checks, and visual review were retained.
This authorization does not imply human color grading or publication approval.

- Reversed all three `heh-ar.medi` contours and the outer `yeh-ar.fina` contour
  in both masters. The final-yeh dots were already correct. Exact source geometry
  was preserved. The direction check now passes; reviewed joined/marked forms
  at 400/550/700 and checked 96 shaping and 96 raster comparisons.
- Repaired `hamzabelowKasratan-ar`, `shaddaFathatan-ar`, and `shaddaDammatan-ar`
  in both masters. Their old Bold offsets misplaced components by hundreds of
  units; the Regular pairs also overlapped. Both copies now use half-scale
  existing mark components, with separate fatha/kasra strokes or side-by-side
  dammas. The base shadda/hamza drawings remain intact. All six interpolation
  findings are resolved. These are visible design changes, not contour-only fixes.
- Reduced `noonGhunna-ar` to a quarter-scale instance of the existing noon-ghunna
  shape, positioned it in the above-mark band, and added `_top` attachment plus
  stacking anchors. The Urdu attachment finding is resolved. Proofs show its
  previous full-size, unattached form and the corrected mark on a base.
- Filled U+FB1D and U+FB1F using the existing Hebrew yod/double-yod and vowel
  components. Added IJ, ij, and U+02BB using existing Latin letter/quote components.
  English and Dutch auxiliary-character findings are resolved. Original component
  drawings and existing review colors are unchanged; new glyphs are ungraded.
- Added the complete U+014A/U+014B Eng/eng case pair, using green N/n and j
  geometry. Donor glyphs are unchanged. Lowercase eng has 35 points and capitals
  have 30 points in each master; curve lint and compatibility pass. See the
  [construction measurements](../design-pass-worklog.md). The Purepecha missing-letter
  failure is resolved. These new drawings remain ungraded.

All five active fonts match the final candidate tables except timestamps and
checksum adjustment. Eleven compiled regression tests pass, including mark
attachment and nonempty new/composite characters. The composite and case-pair
batches each passed 216 shaping checks; unrelated compiled outlines were verified
unchanged. Structural compatibility has zero blockers. The targeted raw/context
proofs and enlarged Eng/eng were inspected at 400/550/700. Existing unrelated
unfinished drawings and lumpiness remain. Reports, the main designbot PDF, and
artifact-presence preflight were refreshed; native-reader review remains pending.

Final online QA, with no exclusions: **10 FAIL / 6 WARN / 162 PASS / 10 INFO /
41 SKIP** for the package; **6 FAIL / 28 WARN / 530 PASS / 39 INFO / 294 SKIP**
for the five loose binaries. No ERROR/FATAL results. A scratch name-availability
request had a transient network error; its retry and final runs passed. Used
Fontspector 1.9.0 and the stable build/QA versions verified on October 18.

Evidence/backups are in `applied-final-directions/`, `applied-qa-composites/`,
and `applied-eng/` under `out/qa/2026-10-18/`; corresponding `*-candidate/`
directories retain scratch proofs and checks. The latest manifest verifies the
32 changed source files in this turn, with unrelated sources and the staged
index preserved. No exclusions, subset declarations, cmap removals, or tool-data
patches were used to reduce the counts.

### Investigation of the nine subset-data failures

No valid local metadata fix was found that preserves the current drawings,
cmap, and intended subsets. The October 17 probes left active subset declarations
unchanged. The exact
`google-fonts-subsets` 0.202602.1 crate used by Fontspector 1.9.0 was fetched
and checksum-verified against its Cargo.lock. It is still the latest released
Rust subset data. Current NAM main (`2a68014b16056e965c18fd47de1f3fde9a5b0095`)
also lacks the three affected characters in the declared subsets.

- **Six results concern U+0331:** Amarakaeri, Chickasaw, Mezquital Otomi,
  Secoya, Siona, and Ticuna. The mark exists and works in the full font, but
  is absent from the declared Latin/Latin-ext/Arabic/Hebrew subsets. This
  overlaps the open [Fontspector issue #946](https://github.com/fonttools/fontspector/issues/946).
  The proposed [NAM correction #31](https://github.com/googlefonts/nam-files/pull/31)
  was closed without merging on October 13. A
  [maintainer response](https://github.com/googlefonts/nam-files/pull/31#issuecomment-6137469597)
  identifies base/mark separation as a known browser-dependent serving
  limitation that font authors are not expected to solve during onboarding.
  This is evidence for review, not a project-specific accepted exception.
- **Three results concern U+1EBC/U+1EBD:** Guarani, Yanomamö, and Ticuna.
  These existing letters occur only in the Vietnamese subset. Virtua has
  19 of its 115 codepoints. An isolated metadata-only experiment adding
  Vietnamese changed QA to **8 FAIL / 15 WARN**: three failures disappeared,
  but an unsupported-Vietnamese warning appeared. This experiment was not
  adopted; it does not establish Vietnamese coverage.
- **Shaping nuance:** all nine affected full-font samples shape without
  missing glyphs at 400/550/700. A local font subset using the union of the
  declared NAM sets loses U+0331 in all six affected cases. HarfBuzz can
  reconstruct `Ẽ/ẽ` from base letters and a combining tilde in the other
  three cases. The October 18 investigation below found and repaired an actual
  Regular combining-tilde offset and preserved the existing accented kerning
  through recomposition. The earlier raster comparison was not evidence of a
  Bold placement error: the measured vertical difference was 250 units at 400,
  125 at 550, and zero at 700. This union simulation is not Google's private
  CSS/WOFF2 serving system.

Read-only reproduction, fetched source/data and issue status, JSON findings,
the isolated Vietnamese experiment, and the decomposition comparison are under
`out/qa/2026-10-17/subset-investigation/`. Run its `reproduce.py` from the repo
root against the saved data to repeat the membership/shaping diagnosis. No
QA exclusions, severity overrides, installed-data edits, cmap removals, or
upstream messages were made. Coordinate these nine results with onboarding
reviewers; the remaining package failure concerns the 11 blank Hebrew glyphs.

### Source-first reinvestigation and repairs (2026-10-18)

Eli requested source fixes before considering any upstream PR. The released
Fontspector 1.9.0 `tofu.rs` was fetched again and is byte-identical to the
previously inspected implementation. Its `missing-subsetted` branch checks
whether normalized sample codepoints occur in the intersection of the font cmap
and declared NAM sets. It does not shape text or examine outlines, anchors,
GSUB, GPOS, glyph names, or OS/2 range flags. This establishes what the check
measures; it does not establish that changing NAM is the correct serving policy.

The source investigation nevertheless found real defects and applied repairs:

- Removed an extra **250-unit y offset** from Regular `tildecomb`'s component.
  Its `_top` anchor was already at 576, and Bold had no component offset.
  The mark now agrees with the precomposed `Ẽ/ẽ` geometry across interpolation.
- Raised only the `top` anchor on **b, d, f, h, k, l** from 576 to 768 in both
  masters. For **t**, it now follows the actual top: 696 Regular / 736 Bold.
  For **dottedCircle**, it is 680 / 688. This avoids collisions exposed by
  correcting the combining mark. Drawings, advances, other anchors, and colors
  remain unchanged. The tilde component translation is the only outline change.
- Added a Latin/DFLT **ccmp recomposition** lookup in both feature sources:
  `E tildecomb -> Etilde` and `e tildecomb -> etilde`. A fontTools subset retains
  these output glyphs through layout closure even when their cmap entries are
  omitted. HarfBuzz now preserves the existing accented-glyph outlines and
  kerning. The full font's existing spacing is unchanged.

A scratch proposal to copy plain e's kerning groups and exceptions was **rejected**
after the proof showed Regular T-tilde contact. No kerning/group edits were applied.
The replacement recomposition approach passed rendered checks at 400/550/700,
27 language-sample runs, and 27,225 unchanged ordinary-Latin pair comparisons.
All three E-tilde sample cases now have identical full-font/subset advances at
400/550/700. The direct decomposed accent also matches full-font bounds within
one unit with ccmp disabled. These checks do not validate Google's live CSS routing.

All six U+0331 cases still lose the mark in the declared-union subset. Their
sample sequences include a/e/i/o/u plus macron below and have no single-character
Unicode NFC alternative. Adding a precomposed drawing cannot supply a missing
U+0331 input mapping in those subset fonts.

An isolated metadata control used the **same binary bytes** in all three runs:

| Diagnostic declarations | `tofu` failures | `subsets_correct` warnings |
| --- | ---: | ---: |
| Existing declarations | 9 | 2 |
| Existing + Vietnamese | 6 | 3 |
| Existing + Vietnamese + Thai | 0 | 4 |

The extra labels lack the required coverage and were never adopted. This is an
input-isolation experiment, not a release fix. No check exclusions, installed-data
patches, cmap deletions, upstream PRs, or public messages were used.

Final active QA remains **10 FAIL / 6 WARN** for the package and **6 FAIL / 28 WARN**
for all five loose fonts, with no ERROR/FATAL. All **13 regression tests** pass;
master compatibility has zero blockers. The two new regression tests cover
fallback placement/spacing and clearance over ascenders. Reports, main proof,
and artifact-presence preflight were refreshed. Nineteen source files changed
in this pass: seventeen GLIFs and two feature files. The staged index and all
unrelated sources were preserved.

Current evidence/backups: `out/qa/2026-10-18/applied-subset-source-fixes/` and
`applied-tilde-anchors/`. Reproduction scripts, controlled experiments, original
source hashes, and normalization evidence are in `subset-source-investigation/`;
`tilde-recomposition-candidate/` retains the successful scratch build. The rejected
kerning experiment is marked explicitly in `etilde-kerning-candidate/rejected.json`.

### All six remaining package warnings

| Count | Check | Why it remains |
| ---: | --- | --- |
| 1 | `contour_count` | Five Arabic forms have unusual counts: medial meem, initial heh, hamza-above/dammatan, per-mille, and six-dot seen. Review their actual drawing/topology; deleting or adding contours solely for this heuristic is not a repair. |
| 1 | `glyphsets/shape_languages` | Missing auxiliary characters: ſ, Ŧ/ŧ, Ǥ/ǥ, Ʒ/ʒ, and Ǯ/ǯ. English, Dutch, Urdu attachment, and Eng/eng gaps are resolved. |
| 2 | `metadata/subsets_correct` | Arabic coverage is below 50% and Latin-ext below 20% of the check's subset definitions. Preserve intended scripts while completing coverage. |
| 1 | `metadata/unreachable_subsetting` | Thirteen existing codepoints are outside the declared serving ranges: U+02D8, U+02D9, U+02DB, U+0302, U+0306, U+030A, U+030B, U+030C, U+0326, U+0327, U+0331, U+1EBC, U+1EBD. Requires Google Fonts subset-data review. |
| 1 | `metadata/designer_profiles` | `eliheuer` has no Google Fonts designer-catalog entry. Requires profile/photo material and an upstream submission; author identity was not replaced. |

### Remaining engineering and review blockers

- **Unresolved Arabic kerning:** four Regular entries reference nonexistent
  groups (`public.kern1.beh-ar`, `public.kern1.kaf-ar`,
  `public.kern1.yeh-ar`, `public.kern2.reh-ar`). Their intended membership
  cannot be recovered from the available group history. Preserve the values
  until the intended isolated/contextual forms are confirmed.
- **Deferred drawing quality:** the former 54 blank Hebrew codepoints now have
  drafts, with no remaining encoded visible blanks. New marks need optical and
  Hebrew-reader review; wide letters inherit unfinished base weight and curve
  quality. Unfinished Arabic/Hebrew
  shapes, unusual contour topology, and curve/joining quality still require
  drawing review. The direction, interpolation, and Urdu attachment findings
  described above are now resolved; this does not approve overall script quality.
- **Package data:** U+0331 and U+1EBC/U+1EBD exist but are unreachable through
  intended subsets. Arabic/Latin-ext thresholds and other unreachable-codepoint
  warnings remain. Do not add unrelated subsets or remove intended coverage
  to silence these findings; resolve the data/serving issue with onboarding reviewers.
- **Human/submission work:** Arabic and Hebrew reader review, final article
  artwork/licensing, designer profile, name/identity attestations, public
  binary delivery, clean CI reproduction, and final package approval remain.

### Applied first Hebrew drawing batch

Filled U+05BD, U+05BF, U+05C0, U+05C3, U+05C6, U+FB20, U+FB29,
and U+FB4C–FB4F in both masters. Nun hafukha and alef–lamed reuse exact
shoulder curves from green `n`; punctuation and terminals follow green `I`/`L`
stroke and chamfer construction. Alternative ayin and bet/kaf/pe with rafe
reuse the existing Hebrew bases. Those bases currently have identical Regular
and Bold outlines, so their inherited weight design remains unfinished.

Added rafe, vowel/meteg, and nun-dot attachment anchors, plus nun hafukha's
GDEF base classification. The source batch changes 22 target drawing GLIFs,
148 anchor-only GLIFs, and two category plists. Existing outlines outside those
eleven targets, advances, and review-color metadata are preserved. Preserved
colors do not constitute human approval of the new drafts.

All 18 tests pass (14 compiled-font regressions and four QA-entrypoint tests).
The two masters have zero blocking structural mismatches. Curve lint reports
no findings for the newly constructed curved forms. Scratch checks cover 792
vowel/meteg clearance cases and 36 precomposed/decomposed rafe equivalence cases;
5,970 unrelated glyph geometry/advance comparisons remain identical. The active
five-font build matches the verified candidate tables, except build timestamps
and checksums. Agent-inspected proofs show 400/550/700 letters, marks, and shaped
text. Human drawing quality and Hebrew reader review remain pending.

Final online QA with Fontspector 1.9.0 and no exclusions: package **9 FAIL /
6 WARN**; five loose binaries **1 FAIL / 28 WARN**. No ERROR/FATAL results.
The eleven blanks are cleared without suppressing checks. Forty-three further
encoded Hebrew blanks remain; see `remaining-visible-blanks.json` in the evidence.

### Applied remaining 43 Hebrew drafts

Under Eli's explicit instruction to fill the remaining blanks and leave them
unapproved, added U+0591–U+05AF, U+05C4/U+05C5, U+05EF, U+FB1E, and
U+FB21–U+FB28 to both masters. The 34 combining signs use shared chamfered
strokes/dots and tangent circular hooks, cups, and rings. Yod triangle uses three
unchanged Virtua yods. Eight wide letters extend Virtua's existing bases;
wide alef uses proportional horizontal expansion to avoid an overthick central
junction. The others extend their central interval, preserving stem widths.
New target grades are **42 orange outlines and one blue composite per master**.
None is green or purple. Existing reference outlines and labels are unchanged.

Inspected [Rubik's sources](https://github.com/googlefonts/rubik) and
[Noto Sans Hebrew's sources](https://github.com/notofonts/hebrew). Rubik does not
contain the Biblical cantillation repertoire; Noto and Unicode supplied form
and positioning references. No donor outline coordinates were copied. Exact
reference revisions, downloaded source hashes, and licenses are retained in
`hebrew-remaining-candidate/references/manifest.json` and adjacent files.

Added above/below, prepositive/postpositive, vowel-side, and holam-side attachment
anchors. The source batch is 254 GLIFs: 86 target drawings/labels and 168
anchor-only edits. No feature, category, glyph-registration, or existing advance
changes were needed. All 20 tests pass, including new all-Hebrew ink and accent
placement regressions. Structural compatibility has zero blockers. Scratch
verification passes 516 target-outline checks, 12,012 below-accent/vowel and
1,512 upper-accent/holam clearance cases, 9,851 unrelated geometry/advance
comparisons, and 96 unchanged shaping comparisons. Active tables match the
verified candidate except build timestamps/checksums.

Inspected 400/550/700 glyph sheets and shaped text, including vowel/meteg/accent
stacks, shin/sin dots, tall/descending bases, wide forms, and Genesis 1:1. Fixed
Bold yod-triangle contact, tevir dot crowding, wide-alef thickening, zarqa/zinor
curve tension, and duplicate cup seams before final application. The new marks
have no smooth-tag tangent kinks or tension-break findings. Curve lint still
flags deliberate separated crest centers in the two-lobed zarqa/zinor forms.
Wide alef, he, lamed, and tav retain smooth-tag tangent issues from their base
construction; widening can magnify these. Most wide bases also retain unfinished
Bold weight. These are explicit orange-draft follow-ups, not approved geometry.
The proof set is not an exhaustive Biblical typography or cross-cluster collision
review; specialist placement and optical correction remain for human review.

Final online package QA remains **9 FAIL / 6 WARN**, and five-font QA remains
**1 FAIL / 28 WARN**, with no ERROR/FATAL results. Warning details are unchanged
apart from report ordering and paths. No exclusions were added. All encoded
visible codepoints have ink; coverage is no longer being claimed for blanks.

### Reproduction and artifact identity

Current evidence is `out/qa/2026-10-18/applied-hebrew-remaining/`.
`full-qa/` and `package-qa/` contain the online reports and input hashes.
`manifest.json` records source/binary identity, exact source scope, verification,
review limits, reference provenance, and QA status. `tests.log` and
`preflight-review.log` record tests, build, reports, PDF, artifact preflight, and
the generated Diffenator3 browser proof (`out/review/diff3proof.html`).
`marks-1.png`, `marks-2.png`, `letters.png`, and `shaping-400/550/700.png`
are the inspected focused proofs. Human drawing grades remain pending.

Complete source/font backups and repeatable scratch scripts (`prepare.py`,
`verify.py`, `proof.py`, `apply.py`) remain in `hebrew-remaining-candidate/`.
`prepare.py` is dry-run by default and only writes scratch sources with
`--write`; `apply.py` checks the frozen source hashes before applying.
That applied candidate's guard intentionally refuses reapplication against
changed active sources. Earlier applied/candidate folders are historical evidence.

Checkout HEAD: `d3184df9abfb4fedce16dd9f5b075324132847c7`, plus uncommitted repairs
and pre-existing work. This is not a released revision. Active source SHA-256
(sorted path + NUL + file bytes + NUL; excluding archive/generated files):
`be80a921024da456a16a0880a4f8012a09d1ad62e1cfb4d9586fcd4cf9dec769`. VF SHA-256:
`4479a843be9c6d747826909cc05e59d93e0677ce82a93bcebc6e89f17339d418`.
All five binary hashes and source-file hashes are in the current manifest.

The local `applied-hebrew-remaining/ofl/virtuagrotesk/` package contains the current
VF with the prior OFL, article/assets, and metadata for arabic/hebrew/latin/
latin-ext/menu. `Latn` primary script and generated date remain provisional;
release source/archive mapping is unfinished. No publication was performed.

## Latest applied design review — 2026-10-19

[HEB-001](../../agent-proofs/cases/hebrew-001/README.md) applies the approved `dalet-hb`
and `resh-hb` outlines in both masters. Weight is explicitly provisional; no
Latin, Arabic, related-form, anchor, advance or grade change was authorized.
Source hashing verified exactly four changes against the frozen candidate
baseline. Active preflight, both curve-lint runs and 20 regression tests pass.
All five active binaries match the reviewed candidate’s tables except head
build timestamps/checksum adjustment.

New VF SHA-256: `3b3d76a92eb124774f7ae56b2ffcf1352cc73d0da738af7924dea777c310736e`.
[Retained identities](../../agent-proofs/cases/hebrew-001/applied-v1-evidence.json) record
the four source hashes and all five binaries. Previous sections' font hashes
and local packages are historical snapshots, not this applied build.

The refreshed online package run remains **9 FAIL / 6 WARN**, and the five-font
run remains **1 FAIL / 28 WARN**, with no ERROR/FATAL results. Finding IDs/codes
are unchanged and no exclusions were added. Reports, tool version, input hashes,
backups and the current local package are under
`out/qa/2026-10-19/applied-dalet-resh/`; use `full-qa-online/` and
`package-qa-online/` (the initial network-restricted attempts are superseded).

The three comparison sheets now use the approved DesignBot Rust workflow,
Virtua labels, title case and both gray polarities. See HEB-001 for the inspected
six PNGs, recipe and tighter-headline setting. This presentation-only port leaves
font sources/binaries unchanged. Final cross-script weight remains open.
No release approval or publication is implied.

## Before submitting the font

- [x] Consolidate build/QA instructions and remove placeholder metadata and
  retired descriptions from the upstream root.
- [x] Use one [article draft](../article/ARTICLE.en_us.html), with no missing image
  references or unsupported model-capability claims.
- [x] Make full QA available without exclusions; make CI fail on QA failures
  and preserve diagnostic artifacts. Remove automatic tag publication.
- [x] Build and run the current Fontspector release locally.
- [ ] Resolve the drawing and engineering findings in the audit. Keep both
  masters compatible and respect protected glyph colors.
- [ ] Complete Latin, Arabic, and Hebrew shaping, mark, spacing, and weight
  review. Obtain Arabic and Hebrew reader review and Eli's drawing approval.
- [ ] Review fresh compiled-font proofs in browsers and in print. Record the
  exact binaries and source revision reviewed.
- [ ] Reproduce setup/build/QA in CI from a clean checkout. The workflow has
  been updated locally but has not yet run on GitHub.
- [ ] Confirm family-name availability, copyright/CLA identity, and that no
  restricted extended version exists. These are maintainer attestations.
- [ ] Approve final article text, specimen selection, and image licensing.
- [ ] Select a public binary delivery strategy: a reviewed release archive or
  committed release binaries. Current CI artifacts alone are not a stable
  public Packager source. Do not invent an archive URL.
- [ ] Assemble the downstream package, review metadata/subsets against actual
  support, and run full package QA with network checks enabled.
- [ ] Resolve all real FAILs and document reviewer disposition for warnings or
  exceptions. Do not silently add exclusions or suppress intended script scope.

## Starting the onboarding conversation

Google Fonts asks for an Add Font issue before a PR and asks contributors to
search for existing issues first. Its current template permits opening an issue
with requirements still unchecked and updating them later. Acceptance and
publication still require review. See the [onboarding guide](https://googlefonts.github.io/gf-guide/onboarding.html)
and [Add Font template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md).

Before posting, prepare an honest summary of scope and remaining work, one
specimen image, and the AI-use disclosure. Keep identity and license attestations
unchecked until Eli confirms them. No issue, PR, release, or public message has
been created by this cleanup.

## Downstream package

Keep downstream files separate from the upstream sources:

```text
ofl/virtuagrotesk/
  VirtuaGrotesk[wght].ttf
  METADATA.pb
  OFL.txt
  article/
    ARTICLE.en_us.html
    weight-specimen.svg
```

The four static TTFs remain useful upstream outputs; the proposed downstream
package uses the variable font. Generate metadata from the reviewed binary with
`gftools add-font`, then review designer, category/stroke, dates, axes, subsets,
primary script, and source linkage. Keep Arabic and Hebrew in the intended
subset scope even when coverage needs work. The current local probe uses `Latn`
as a provisional primary script; confirm which script should lead the specimen.

Use [the packaging skill](../../.agents/skills/google-fonts-packaging/SKILL.md)
for a local preview. `METADATA.pb` is a downstream artifact, not a hand-written
upstream placeholder. The local probe under `out/onboarding/` is incomplete
and unpublished; its date and source metadata are not final release values.

## References

- [Upstream structure](https://googlefonts.github.io/gf-guide/upstream.html):
  source layout, public repository, build recipe, and project documentation.
- [Font requirements](https://googlefonts.github.io/gf-guide/requirements.html):
  naming, embedding, license metadata, glyphsets, and features.
- [QA](https://googlefonts.github.io/gf-guide/qa.html): Fontspector and proof review.
- [Article](https://googlefonts.github.io/gf-guide/article.html): current About
  format, replacing the retired DESCRIPTION file.
- [Metadata](https://googlefonts.github.io/gf-guide/metadata.html) and
  [packaging](https://googlefonts.github.io/gf-guide/package.html): downstream
  fields, source mappings, and package review.

Some guide pages still refer to FontBakery. Use the current QA page and the
installed Fontspector CLI for commands. Recheck the official pages at submission;
this document is not a replacement for Google Fonts review.
