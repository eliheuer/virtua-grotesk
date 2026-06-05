# Arabic Next Review AI Triage

This generated report summarizes what AI/mechanical review can safely
pre-triage for the current Arabic next-review packet. It does not mark
visual rows as passed; final status still requires human proof/source
inspection and an explicit `arabic-visual-review-update` command.

## Inputs

- Next-review packet: `documentation/glyph-review/arabic-next-review-packet.md`
- Snapshot report: `documentation/glyph-review/arabic-next-review-snapshots.md`
- Structure triage: `documentation/glyph-review/arabic-structure-triage.md`
- Visual-risk audit: `documentation/glyph-review/arabic-visual-risk-audit.md`

## Current Batch State

- Pending or fix-needed visual rows: 32
- Rendered PNG snapshots: 33
- Snapshot errors: 0
- Structure triage mechanical blockers: 0
- Structure triage review-prompt rows: 66
- Visual-risk audit rows: 46

## First-Batch AI Triage Summary

| Review key | Snapshot evidence | Mechanical blockers | AI-safe classification | Human decision still needed |
| --- | --- | ---: | --- | --- |
| `proof-regular-glyphs` | `documentation/glyph-review/review-snapshots/proof-regular-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html` | 0 | ready for glyph-proof pass/fix/defer review | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| `proof-medium-glyphs` | `documentation/glyph-review/review-snapshots/proof-medium-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html` | 0 | ready for glyph-proof pass/fix/defer review | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| `proof-semibold-glyphs` | `documentation/glyph-review/review-snapshots/proof-semibold-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html` | 0 | ready for glyph-proof pass/fix/defer review | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| `proof-bold-glyphs` | `documentation/glyph-review/review-snapshots/proof-bold-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html` | 0 | ready for glyph-proof pass/fix/defer review | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| `class-letter-structures` | `documentation/glyph-review/review-snapshots/class-letter-structures.png` from `documentation/glyph-review/arabic-structure-sweep.html`<br>`documentation/glyph-review/review-snapshots/class-letter-structures-2.png` from `documentation/glyph-review/arabic-visual-risk-proof.html` | 0 | ready for focused structure review | Inspect sidebearing prompt glyphs in structure sweep, visual-risk proof, and source if needed. |

## Full Pending Queue AI Triage

This table covers every pending or fix-needed visual review row. It is
a navigation and risk summary only; it does not mark rows as passed.

| Order | Review key | Area | Item | Mechanical precheck | AI-safe classification | Evidence to open | Human decision still needed |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `proof-regular-glyphs` | GF proof | Regular glyphs | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | ready for glyph-proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-regular-glyphs.png` | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| 2 | `proof-medium-glyphs` | GF proof | Medium glyphs | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | ready for glyph-proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_glyphs.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-medium-glyphs.png` | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| 3 | `proof-semibold-glyphs` | GF proof | SemiBold glyphs | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | ready for glyph-proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*SemiBold*-diffbrowsers_glyphs.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-semibold-glyphs.png` | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| 4 | `proof-bold-glyphs` | GF proof | Bold glyphs | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | ready for glyph-proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Bold*-diffbrowsers_glyphs.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-bold-glyphs.png` | Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs. |
| 5 | `class-letter-structures` | Glyph class | letter-structures | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | ready for focused structure review | `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`<br>`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-visual-risk-proof.html` | Inspect sidebearing prompt glyphs in structure sweep, visual-risk proof, and source if needed. |
| 6 | `mark-base+fatha` | Mark attachment | base+fatha | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 7 | `mark-base+damma` | Mark attachment | base+damma | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 8 | `mark-base+kasra` | Mark attachment | base+kasra | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 9 | `mark-shadda+sukun` | Mark attachment | shadda+sukun | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 10 | `mark-tanween` | Mark attachment | tanween | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 11 | `mark-hamza-above-below` | Mark attachment | hamza-above-below | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 12 | `mark-dotted-circle` | Mark attachment | dotted-circle | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/arabic-mark-readiness.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/google-fonts/gftools-qa/Proof`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 13 | `class-mark-combinations` | Glyph class | mark-combinations | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | ready for mark-proof pass/fix/defer review | `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`<br>`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity. |
| 14 | `class-dot-stack-helpers` | Glyph class | dot-stack-helpers | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | ready for class-level drawing review | `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`<br>`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open dashboard and linked source/proof evidence before recording status. |
| 15 | `proof-regular-text` | GF proof | Regular text | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_text.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-regular-text.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 16 | `proof-regular-proofer` | GF proof | Regular proofer | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_proofer.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-regular-proofer.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 17 | `proof-regular-waterfall` | GF proof | Regular waterfall | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_waterfall.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-regular-waterfall.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 18 | `proof-medium-text` | GF proof | Medium text | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_text.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-medium-text.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 19 | `proof-medium-proofer` | GF proof | Medium proofer | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_proofer.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-medium-proofer.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 20 | `proof-medium-waterfall` | GF proof | Medium waterfall | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_waterfall.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-medium-waterfall.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 21 | `proof-semibold-text` | GF proof | SemiBold text | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*SemiBold*-diffbrowsers_text.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-semibold-text.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 22 | `proof-semibold-proofer` | GF proof | SemiBold proofer | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*SemiBold*-diffbrowsers_proofer.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-semibold-proofer.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 23 | `proof-semibold-waterfall` | GF proof | SemiBold waterfall | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*SemiBold*-diffbrowsers_waterfall.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-semibold-waterfall.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 24 | `proof-bold-text` | GF proof | Bold text | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Bold*-diffbrowsers_text.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-bold-text.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 25 | `proof-bold-proofer` | GF proof | Bold proofer | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Bold*-diffbrowsers_proofer.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-bold-proofer.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 26 | `proof-bold-waterfall` | GF proof | Bold waterfall | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | ready for proof pass/fix/defer review | `documentation/google-fonts/gftools-qa/Proof/*Bold*-diffbrowsers_waterfall.html`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/proof-bold-waterfall.png` | Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate. |
| 27 | `smoke-salaam` | Smoke string | salaam | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | mechanical shaping passes; needs visual rhythm review | `documentation/glyph-review/arabic-shaping-smoke-test.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/smoke-salaam.png` | Open shaping smoke report and dashboard; inspect contextual forms and spacing rhythm. |
| 28 | `smoke-arabic` | Smoke string | arabic | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | mechanical shaping passes; needs visual rhythm review | `documentation/glyph-review/arabic-shaping-smoke-test.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/smoke-arabic.png` | Open shaping smoke report and dashboard; inspect contextual forms and spacing rhythm. |
| 29 | `smoke-bismillah` | Smoke string | bismillah | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | mechanical shaping passes; needs visual rhythm review | `documentation/glyph-review/arabic-shaping-smoke-test.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/smoke-bismillah.png` | Open shaping smoke report and dashboard; inspect contextual forms and spacing rhythm. |
| 30 | `smoke-lam-alef` | Smoke string | lam-alef | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | mechanical shaping passes; needs visual rhythm review | `documentation/glyph-review/arabic-shaping-smoke-test.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md`<br>`documentation/glyph-review/review-snapshots/smoke-lam-alef.png` | Open shaping smoke report and dashboard; inspect contextual forms and spacing rhythm. |
| 31 | `class-arabic-farsi-numerals` | Glyph class | arabic-farsi-numerals | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | ready for class-level drawing review | `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`<br>`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open dashboard and linked source/proof evidence before recording status. |
| 32 | `class-arabic-punctuation` | Glyph class | arabic-punctuation | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | ready for class-level drawing review | `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`<br>`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`<br>`documentation/glyph-review/arabic-manual-review-dashboard.html`<br>`documentation/glyph-review/arabic-print-proof-index.md` | Open dashboard and linked source/proof evidence before recording status. |

## Structure Prompts To Inspect

| Codepoint | Glyphs | Prompt |
| --- | --- | --- |
| `U+062B ARABIC LETTER THEH` | `uni062B` | Check dot stack height and left overhang in glyph proofs before spacing edits. |
| `U+062C ARABIC LETTER JEEM` | `uni062C` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+062D ARABIC LETTER HAH` | `uni062D` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+062E ARABIC LETTER KHAH` | `uni062E` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0633 ARABIC LETTER SEEN` | `uni0633` | Check whether the left overhang is intentional joining-script rhythm across all weights. |
| `U+0634 ARABIC LETTER SHEEN` | `uni0634` | Check whether the left overhang is intentional joining-script rhythm across all weights. |
| `U+0639 ARABIC LETTER AIN` | `uni0639` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+063A ARABIC LETTER GHAIN` | `uni063A` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0645 ARABIC LETTER MEEM` | `uni0645` | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0648 ARABIC LETTER WAW` | `uni0648` | Check descending bowl and left overhang against adjacent text samples. |
| `U+0651 ARABIC SHADDA` | `uni0651` | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0655 ARABIC HAMZA BELOW` | `uni0655` | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |

## Recommended Review Order

1. Open the first-batch cards in `documentation/glyph-review/arabic-next-review-board.html`.
2. If the glyph pages show no missing, blank, clipped, duplicated, or
   wrong-codepoint Arabic glyphs, record those proof rows as `pass`.
3. Open the structure sweep and visual-risk proof for the prompt glyphs.
4. Continue through the full pending queue by area: mark attachment,
   text/proofer/waterfall proofs, smoke strings, numerals, punctuation.
5. Record each row as `pass`, `fix-needed`, or `deferred` only after
   checking the linked proof/source evidence.

## Guarded Update Commands

Use one command per row after human inspection:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Notes

- AI can confirm that current snapshot artifacts exist and that the
  generated triage reports show no mechanical `.notdef`, blank-visible
  glyph, nonmark-zero-advance, or shared visible cmap blockers.
- AI cannot approve Arabic drawing quality, cultural/script correctness,
  or final spacing rhythm without human review.
- Do not copy reference-font outlines into production sources. Use
  references only for comparison, then redraw or adjust in Virtua style.
