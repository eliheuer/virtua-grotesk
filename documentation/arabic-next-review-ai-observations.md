# Arabic Next Review AI Observations

This generated note records AI-safe first-pass observations over the
current Arabic review snapshot set. It is not a human Arabic review and
does not mark any row in `documentation/arabic-visual-review-log.md` as
passed.

## Snapshot Inputs

- Full pending-queue snapshot report:
  - `documentation/arabic-next-review-snapshots.md`
  - Rendered snapshots: 33
  - Rows without snapshot source: 0
  - Snapshot errors: 0
- Focused zoom snapshot report:
  - `documentation/arabic-first-review-zoom-snapshots.md`
  - Rendered zoom snapshots: 4
  - Zoom snapshot errors: 0
- Snapshot integrity:
  - `documentation/arabic-snapshot-integrity.md`
  - Pending/fix-needed rows without snapshot: 0
  - Snapshot evidence ready for hand review: yes

## Observations

| Review key | AI first-pass observation | Suggested human action |
| --- | --- | --- |
| `proof-regular-glyphs` | Regular glyph-proof snapshot evidence and a focused 2x Arabic-row crop are present and nonblank. Use the crop for faster structure screening of missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs before opening the full proof HTML. | Open the matching gftools glyph proof at zoom; record `fix-needed` only with exact glyph names or proof locations. |
| `proof-medium-glyphs` | Medium glyph-proof snapshot evidence and a focused 2x Arabic-row crop are present and nonblank. Use the crop for faster structure screening of missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs before opening the full proof HTML. | Open the matching gftools glyph proof at zoom; record `fix-needed` only with exact glyph names or proof locations. |
| `proof-semibold-glyphs` | SemiBold glyph-proof snapshot evidence and a focused 2x Arabic-row crop are present and nonblank. Use the crop for faster structure screening of missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs before opening the full proof HTML. | Open the matching gftools glyph proof at zoom; record `fix-needed` only with exact glyph names or proof locations. |
| `proof-bold-glyphs` | Bold glyph-proof snapshot evidence and a focused 2x Arabic-row crop are present and nonblank. Use the crop for faster structure screening of missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs before opening the full proof HTML. | Open the matching gftools glyph proof at zoom; record `fix-needed` only with exact glyph names or proof locations. |
| `class-letter-structures` | Structure and visual-risk snapshots are present. Treat sidebearing and overhang prompts as style-review questions in shaped RTL context, not automatic spacing failures. | Open the dashboard plus linked proof/source reports; record `pass` only after the whole class cue is reviewed. |
| `mark-base+fatha` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-base+damma` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-base+kasra` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-shadda+sukun` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-tanween` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-hamza-above-below` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `mark-dotted-circle` | Mark-proof snapshot evidence is present. The mechanical reports are clean enough for visual attachment review, with attention to collisions, stacked marks, dotted-circle clarity, and weight changes. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `class-mark-combinations` | Mark-combination snapshot evidence is present. Review composite mark scale and stacking in the shared mark proof before deciding whether source edits are needed. | Open `documentation/arabic-mark-review-proof.html`; compare mark placement across weights before recording pass/fix/defer. |
| `class-dot-stack-helpers` | Dashboard snapshot evidence is present for dot-stack helper review. Check whether three-dot and six-dot helpers keep separation in Bold and interpolate cleanly. | Open the dashboard plus linked proof/source reports; record `pass` only after the whole class cue is reviewed. |
| `proof-regular-text` | Text-proof snapshot evidence is present. Use it to triage RTL texture, fallback, mark collisions, and unexpected spacing influence before opening the full text proof. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-regular-proofer` | Proofer snapshot evidence is present. Inspect sidebearing rhythm, Arabic punctuation spacing, numeral rhythm, and weight-specific spacing in the linked proof HTML. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-regular-waterfall` | Waterfall snapshot evidence is present. Use it to check small-size behavior, interpolation, and mark clarity across sizes. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-medium-text` | Text-proof snapshot evidence is present. Use it to triage RTL texture, fallback, mark collisions, and unexpected spacing influence before opening the full text proof. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-medium-proofer` | Proofer snapshot evidence is present. Inspect sidebearing rhythm, Arabic punctuation spacing, numeral rhythm, and weight-specific spacing in the linked proof HTML. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-medium-waterfall` | Waterfall snapshot evidence is present. Use it to check small-size behavior, interpolation, and mark clarity across sizes. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-semibold-text` | Text-proof snapshot evidence is present. Use it to triage RTL texture, fallback, mark collisions, and unexpected spacing influence before opening the full text proof. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-semibold-proofer` | Proofer snapshot evidence is present. Inspect sidebearing rhythm, Arabic punctuation spacing, numeral rhythm, and weight-specific spacing in the linked proof HTML. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-semibold-waterfall` | Waterfall snapshot evidence is present. Use it to check small-size behavior, interpolation, and mark clarity across sizes. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-bold-text` | Text-proof snapshot evidence is present. Use it to triage RTL texture, fallback, mark collisions, and unexpected spacing influence before opening the full text proof. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-bold-proofer` | Proofer snapshot evidence is present. Inspect sidebearing rhythm, Arabic punctuation spacing, numeral rhythm, and weight-specific spacing in the linked proof HTML. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `proof-bold-waterfall` | Waterfall snapshot evidence is present. Use it to check small-size behavior, interpolation, and mark clarity across sizes. | Open the matching gftools proof HTML; inspect the row cue directly before recording an outcome. |
| `smoke-salaam` | Dashboard snapshot evidence is present and the shaping smoke report mechanically passes. Human review still needs to judge rhythm, joins, and style fit in the rendered string. | Open `documentation/arabic-shaping-smoke-test.md` and the dashboard; confirm joins and spacing visually before passing. |
| `smoke-arabic` | Dashboard snapshot evidence is present and the shaping smoke report mechanically passes. Human review still needs to judge rhythm, joins, and style fit in the rendered string. | Open `documentation/arabic-shaping-smoke-test.md` and the dashboard; confirm joins and spacing visually before passing. |
| `smoke-bismillah` | Dashboard snapshot evidence is present and the shaping smoke report mechanically passes. Human review still needs to judge rhythm, joins, and style fit in the rendered string. | Open `documentation/arabic-shaping-smoke-test.md` and the dashboard; confirm joins and spacing visually before passing. |
| `smoke-lam-alef` | Dashboard snapshot evidence is present and the shaping smoke report mechanically passes. Human review still needs to judge rhythm, joins, and style fit in the rendered string. | Open `documentation/arabic-shaping-smoke-test.md` and the dashboard; confirm joins and spacing visually before passing. |
| `class-arabic-farsi-numerals` | Dashboard snapshot evidence is present for Arabic and Farsi numerals. Review width rhythm and style fit against Latin numerals and Arabic text before passing. | Open the dashboard plus linked proof/source reports; record `pass` only after the whole class cue is reviewed. |
| `class-arabic-punctuation` | Dashboard snapshot evidence is present for Arabic punctuation. Review comma, semicolon, question mark, per mille, date separator, full stop, and parentheses spacing in RTL context. | Open the dashboard plus linked proof/source reports; record `pass` only after the whole class cue is reviewed. |

## Full Queue Snapshot Evidence

| Order | Review key | Snapshot evidence |
| ---: | --- | --- |
| 1 | `proof-regular-glyphs` | `documentation/arabic-review-snapshots/proof-regular-glyphs.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-regular-glyphs.png` |
| 2 | `proof-medium-glyphs` | `documentation/arabic-review-snapshots/proof-medium-glyphs.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-medium-glyphs.png` |
| 3 | `proof-semibold-glyphs` | `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` |
| 4 | `proof-bold-glyphs` | `documentation/arabic-review-snapshots/proof-bold-glyphs.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-bold-glyphs.png` |
| 5 | `class-letter-structures` | `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`<br>`documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html` |
| 6 | `mark-base+fatha` | `documentation/arabic-review-snapshots/mark-base+fatha.png` from `documentation/arabic-mark-review-proof.html` |
| 7 | `mark-base+damma` | `documentation/arabic-review-snapshots/mark-base+damma.png` from `documentation/arabic-mark-review-proof.html` |
| 8 | `mark-base+kasra` | `documentation/arabic-review-snapshots/mark-base+kasra.png` from `documentation/arabic-mark-review-proof.html` |
| 9 | `mark-shadda+sukun` | `documentation/arabic-review-snapshots/mark-shadda+sukun.png` from `documentation/arabic-mark-review-proof.html` |
| 10 | `mark-tanween` | `documentation/arabic-review-snapshots/mark-tanween.png` from `documentation/arabic-mark-review-proof.html` |
| 11 | `mark-hamza-above-below` | `documentation/arabic-review-snapshots/mark-hamza-above-below.png` from `documentation/arabic-mark-review-proof.html` |
| 12 | `mark-dotted-circle` | `documentation/arabic-review-snapshots/mark-dotted-circle.png` from `documentation/arabic-mark-review-proof.html` |
| 13 | `class-mark-combinations` | `documentation/arabic-review-snapshots/class-mark-combinations.png` from `documentation/arabic-mark-review-proof.html` |
| 14 | `class-dot-stack-helpers` | `documentation/arabic-review-snapshots/class-dot-stack-helpers.png` from `documentation/arabic-manual-review-dashboard.html` |
| 15 | `proof-regular-text` | `documentation/arabic-review-snapshots/proof-regular-text.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html` |
| 16 | `proof-regular-proofer` | `documentation/arabic-review-snapshots/proof-regular-proofer.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html` |
| 17 | `proof-regular-waterfall` | `documentation/arabic-review-snapshots/proof-regular-waterfall.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html` |
| 18 | `proof-medium-text` | `documentation/arabic-review-snapshots/proof-medium-text.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html` |
| 19 | `proof-medium-proofer` | `documentation/arabic-review-snapshots/proof-medium-proofer.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html` |
| 20 | `proof-medium-waterfall` | `documentation/arabic-review-snapshots/proof-medium-waterfall.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html` |
| 21 | `proof-semibold-text` | `documentation/arabic-review-snapshots/proof-semibold-text.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html` |
| 22 | `proof-semibold-proofer` | `documentation/arabic-review-snapshots/proof-semibold-proofer.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html` |
| 23 | `proof-semibold-waterfall` | `documentation/arabic-review-snapshots/proof-semibold-waterfall.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html` |
| 24 | `proof-bold-text` | `documentation/arabic-review-snapshots/proof-bold-text.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html` |
| 25 | `proof-bold-proofer` | `documentation/arabic-review-snapshots/proof-bold-proofer.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html` |
| 26 | `proof-bold-waterfall` | `documentation/arabic-review-snapshots/proof-bold-waterfall.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html` |
| 27 | `smoke-salaam` | `documentation/arabic-review-snapshots/smoke-salaam.png` from `documentation/arabic-manual-review-dashboard.html` |
| 28 | `smoke-arabic` | `documentation/arabic-review-snapshots/smoke-arabic.png` from `documentation/arabic-manual-review-dashboard.html` |
| 29 | `smoke-bismillah` | `documentation/arabic-review-snapshots/smoke-bismillah.png` from `documentation/arabic-manual-review-dashboard.html` |
| 30 | `smoke-lam-alef` | `documentation/arabic-review-snapshots/smoke-lam-alef.png` from `documentation/arabic-manual-review-dashboard.html` |
| 31 | `class-arabic-farsi-numerals` | `documentation/arabic-review-snapshots/class-arabic-farsi-numerals.png` from `documentation/arabic-manual-review-dashboard.html` |
| 32 | `class-arabic-punctuation` | `documentation/arabic-review-snapshots/class-arabic-punctuation.png` from `documentation/arabic-manual-review-dashboard.html` |

## Non-Decisions

- Do not mark any row as `pass` from this file alone.
- Do not edit sidebearings only because the mechanical audit flags negative
  sidebearings; joining-script rhythm must be checked in shaped context.
- Do not copy reference-font outlines. Use references only to compare joining
  logic, dot placement, and mark placement.

## Next Commands

After human inspection, record one outcome per row:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
```

Use `fix-needed` or `deferred` instead of `pass` wherever the proof or
source inspection is inconclusive.
