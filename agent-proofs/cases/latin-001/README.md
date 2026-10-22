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

Eli approved pushing attachment/coverage commit1e8dd28e; it is now on origin/main.
The subsequent drawing checkpoints remain local.

## Next bounded work

1. Cedilla, then ogonek and alternate carons. Generic g+U0326 still collides inside its descender; preserve the green base while diagnosing attachment. Preserve the rotated ģ placement introduced in batch07. Check full reverse closure for green/Arabic dependencies and preserve the shared
   reversed-Nun calibration when changing any dot geometry or anchors.
2. Spacing constraint reaffirmed by Eli: use the powers-of-two system for
sidebearings, advances and kerning. New machine values on8; record decompositions
and preserve green/human optical exceptions. See DESIGN.md#spacing.

3. Existing precomposed widths differ from the base+mark fallback by up to
   tens of units. `verification.json` retains the measured sample differences.
   Inspect wrapper metrics/kerning and word spacing before applying changes.
4. Remaining Rubik Latin codepoints: ĸ ŉ Ŧ ŧ ſ ƒ ﬁ ﬂ. Review encoded ligatures
   separately from GSUB behavior. Four combining marks, punctuation, fractions,
   maths and currencies are also absent; use `coverage-after.json`.
5. Full Rubik language coverage includes182 Cyrillic codepoints absent here.
   This is a separate drawing/reader-review phase, not a metadata toggle.
   The102 missing Arabic codepoints are presentation forms; compare GSUB and
   legacy text behavior before adding redundant forms. Leave Arabic sources to Eli.
6. Diagnose the216 existing Hebrew regressions, serving-subset failures, fresh
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
