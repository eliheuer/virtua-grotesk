# Arabic Full Queue AI Sweep

This generated report records AI-safe observations for the full pending
Arabic visual-review queue. It is not a human Arabic review, does not
approve drawings, and does not update `documentation/arabic-visual-review-log.md`.

## Evidence Basis

- Snapshot coverage source: `documentation/arabic-next-review-snapshots.md`
- Focused zoom snapshot source: `documentation/arabic-first-review-zoom-snapshots.md`
- Snapshot integrity source: `documentation/arabic-snapshot-integrity.md`
- Official review log: `documentation/arabic-visual-review-log.md`
- Pending/fix-needed rows covered: 32

## Coverage Audit

- Pending/fix-needed rows: 32
- Rows with AI observation: 32 / 32
- Rows with human follow-up: 32 / 32
- Rows with snapshot evidence: 32 / 32
- Missing AI observations: 0
- Missing human follow-ups: 0
- Missing snapshot evidence: 0
- Coverage ready for human review: yes

Representative images inspected in this sweep:

- `documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png`
- `documentation/arabic-review-snapshots/mark-shadda+sukun.png`
- `documentation/arabic-review-snapshots/proof-bold-text.png`
- `documentation/arabic-review-snapshots/proof-regular-proofer.png`
- `documentation/arabic-review-snapshots/class-dot-stack-helpers.png`

## Queue Groups

| Group | Rows |
| --- | ---: |
| dot helpers | 1 |
| marks | 8 |
| numerals | 1 |
| proofer | 4 |
| punctuation | 1 |
| smoke | 4 |
| structure | 5 |
| text | 4 |
| waterfall | 4 |

## Row Observations

| Review key | Group | AI observation | Human follow-up | Snapshot evidence |
| --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | structure | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. | `documentation/arabic-review-snapshots/proof-regular-glyphs.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-regular-glyphs.png` |
| `proof-medium-glyphs` | structure | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. | `documentation/arabic-review-snapshots/proof-medium-glyphs.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-medium-glyphs.png` |
| `proof-semibold-glyphs` | structure | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. | `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` |
| `proof-bold-glyphs` | structure | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. | `documentation/arabic-review-snapshots/proof-bold-glyphs.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`<br>`documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-bold-glyphs.png` |
| `class-letter-structures` | structure | Structure/risk snapshots show the expected high-risk overhang families. The overhangs need shaped-context judgment, not automatic sidebearing edits. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`<br>`documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html` |
| `mark-base+fatha` | marks | Section-targeted mark snapshot shows fatha samples across all five generated fonts. Human review still needs top-mark clearance, centering, and angle checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-base+fatha.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-base+damma` | marks | Section-targeted mark snapshot shows damma samples across all five generated fonts. Human review still needs damma scale and Bold readability checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-base+damma.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-base+kasra` | marks | Section-targeted mark snapshot shows kasra samples across all five generated fonts. Human review still needs bottom-mark clearance and sidebearing checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-base+kasra.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-shadda+sukun` | marks | Section-targeted mark snapshot shows shadda, sukun, and stacked composites across all five generated fonts. Prioritize the no-offset prompts for `بُّ` and `بَّ`. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-shadda+sukun.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-tanween` | marks | Section-targeted mark snapshot shows tanween samples across all five generated fonts. Human review still needs twin-mark clarity and alignment checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-tanween.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-hamza-above-below` | marks | Section-targeted mark snapshot shows hamza-above and hamza-below samples across all five generated fonts. Human review still needs above/below clearance checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-hamza-above-below.png` from `documentation/arabic-mark-review-proof.html` |
| `mark-dotted-circle` | marks | Section-targeted mark snapshot shows dotted circle with top, bottom, and tanween marks across all five generated fonts. Human review still needs dotted-circle readability checks. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/mark-dotted-circle.png` from `documentation/arabic-mark-review-proof.html` |
| `class-mark-combinations` | marks | Use the shared mark proof to compare composite mark scale and stacking; mechanical mark setup is present, but visual approval is still pending. | Open `documentation/arabic-mark-review-proof.html`. | `documentation/arabic-review-snapshots/class-mark-combinations.png` from `documentation/arabic-mark-review-proof.html` |
| `class-dot-stack-helpers` | dot helpers | Section-targeted dashboard snapshot shows Persian/Urdu dotted letters across all generated fonts. Use it to inspect dot separation, especially in Bold and in the variable font. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/class-dot-stack-helpers.png` from `documentation/arabic-manual-review-dashboard.html` |
| `proof-regular-text` | text | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-regular-text.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html` |
| `proof-regular-proofer` | proofer | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-regular-proofer.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html` |
| `proof-regular-waterfall` | waterfall | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-regular-waterfall.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html` |
| `proof-medium-text` | text | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-medium-text.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html` |
| `proof-medium-proofer` | proofer | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-medium-proofer.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html` |
| `proof-medium-waterfall` | waterfall | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-medium-waterfall.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html` |
| `proof-semibold-text` | text | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-semibold-text.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html` |
| `proof-semibold-proofer` | proofer | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-semibold-proofer.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html` |
| `proof-semibold-waterfall` | waterfall | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-semibold-waterfall.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html` |
| `proof-bold-text` | text | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-bold-text.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html` |
| `proof-bold-proofer` | proofer | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-bold-proofer.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html` |
| `proof-bold-waterfall` | waterfall | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. | `documentation/arabic-review-snapshots/proof-bold-waterfall.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html` |
| `smoke-salaam` | smoke | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/smoke-salaam.png` from `documentation/arabic-manual-review-dashboard.html` |
| `smoke-arabic` | smoke | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/smoke-arabic.png` from `documentation/arabic-manual-review-dashboard.html` |
| `smoke-bismillah` | smoke | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/smoke-bismillah.png` from `documentation/arabic-manual-review-dashboard.html` |
| `smoke-lam-alef` | smoke | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/smoke-lam-alef.png` from `documentation/arabic-manual-review-dashboard.html` |
| `class-arabic-farsi-numerals` | numerals | Section-targeted dashboard snapshot shows Arabic-Indic digit rhythm across all generated fonts. Open the dashboard and glyph sources before judging digit widths and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/class-arabic-farsi-numerals.png` from `documentation/arabic-manual-review-dashboard.html` |
| `class-arabic-punctuation` | punctuation | Section-targeted dashboard snapshot shows Arabic punctuation across all generated fonts. Review comma, semicolon, question mark, per mille, date separator, full stop, and parentheses in RTL context. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. | `documentation/arabic-review-snapshots/class-arabic-punctuation.png` from `documentation/arabic-manual-review-dashboard.html` |

## Non-Decisions

- No row was marked `pass`.
- No source glyph was marked `fix-needed`.
- No row was deferred.
- Proofer tofu in GF_Latin_Core proof snapshots is treated as a separate
  Latin Core coverage blocker, not as proof of Arabic drawing failure.
- Sidebearing and mark-offset prompts remain human visual-review prompts.
