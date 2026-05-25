# Arabic Review Worksheet Bundle

This generated bundle turns the remaining Arabic visual-review queue into
batch fill-in worksheets. It does not approve drawings: record outcomes
only after opening the linked proof/source evidence.

## Coverage

- Pending/fix-needed visual rows: 32
- Source for AI-safe notes: `documentation/arabic-full-queue-ai-sweep.md`
- Source for snapshots: `documentation/arabic-next-review-snapshots.md`
- Source for official statuses: `documentation/arabic-visual-review-log.md`

## Review Batches

### 2. Structure And Wrong-Glyph Sweep

- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows in worksheet: 5 (pending: 5)
- Decision rule: Confirm the contour queue is empty, then record the visual review rows only.

Evidence to open:

- `documentation/arabic-structure-sweep.html`
- `documentation/arabic-structure-triage.md`
- `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- `documentation/arabic-manual-review-dashboard.html`
- `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
- `documentation/contour-cleanup-decision-log.md`
- `documentation/arabic-cleanup-drawing-briefs.md`
- `documentation/arabic-visual-risk-proof.html`

Snapshot aids:

- `proof-regular-glyphs` Regular glyphs: `documentation/arabic-review-snapshots/proof-regular-glyphs.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- `proof-regular-glyphs` Regular Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-regular-glyphs.png`
- `proof-medium-glyphs` Medium glyphs: `documentation/arabic-review-snapshots/proof-medium-glyphs.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- `proof-medium-glyphs` Medium Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-medium-glyphs.png`
- `proof-semibold-glyphs` SemiBold glyphs: `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- `proof-semibold-glyphs` SemiBold Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-semibold-glyphs.png`
- `proof-bold-glyphs` Bold glyphs: `documentation/arabic-review-snapshots/proof-bold-glyphs.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
- `proof-bold-glyphs` Bold Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-bold-glyphs.png`
- `class-letter-structures` Arabic structure sweep: `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`
- `class-letter-structures` Arabic visual risk proof: `documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html`

| Key | Status | Review cue | AI observation | Human follow-up | Observed issue or `none` | Source/proof location | Final status | Guarded commands |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-medium-glyphs` | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-semibold-glyphs` | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-bold-glyphs` | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | Full snapshot and focused 2x Arabic-row crop are nonblank. Use the crop to screen structure faster, then open the full glyph proof for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs. | Open the matching gftools glyph proof at zoom. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `class-letter-structures` | pending | sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof | Structure/risk snapshots show the expected high-risk overhang families. The overhangs need shaped-context judgment, not automatic sidebearing edits. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |

### 3. Marks, Dotted Circle, And Stacking

- Why: Arabic Core is mechanically present, but marks still need visual attachment and stacking review.
- Visual rows in worksheet: 8 (pending: 8)
- Decision rule: Review real-base attachment and dotted-circle behavior before accepting or editing mark composites.

Evidence to open:

- `documentation/arabic-mark-review-proof.html`
- `documentation/arabic-mark-triage.md`
- `documentation/arabic-mark-readiness.md`
- `documentation/arabic-manual-review-dashboard.html`
- `documentation/gftools-qa/Proof`
- `documentation/contour-cleanup-decision-log.md`
- `documentation/arabic-cleanup-drawing-briefs.md`

Snapshot aids:

- `mark-base+fatha` Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+fatha.png` from `documentation/arabic-mark-review-proof.html`
- `mark-base+damma` Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+damma.png` from `documentation/arabic-mark-review-proof.html`
- `mark-base+kasra` Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+kasra.png` from `documentation/arabic-mark-review-proof.html`
- `mark-shadda+sukun` Arabic mark proof: `documentation/arabic-review-snapshots/mark-shadda+sukun.png` from `documentation/arabic-mark-review-proof.html`
- `mark-tanween` Arabic mark proof: `documentation/arabic-review-snapshots/mark-tanween.png` from `documentation/arabic-mark-review-proof.html`
- `mark-hamza-above-below` Arabic mark proof: `documentation/arabic-review-snapshots/mark-hamza-above-below.png` from `documentation/arabic-mark-review-proof.html`
- `mark-dotted-circle` Arabic mark proof: `documentation/arabic-review-snapshots/mark-dotted-circle.png` from `documentation/arabic-mark-review-proof.html`
- `class-mark-combinations` Arabic mark proof: `documentation/arabic-review-snapshots/class-mark-combinations.png` from `documentation/arabic-mark-review-proof.html`

| Key | Status | Review cue | AI observation | Human follow-up | Observed issue or `none` | Source/proof location | Final status | Guarded commands |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mark-base+fatha` | pending | top mark position clears the base and matches style | Section-targeted mark snapshot shows fatha samples across all five generated fonts. Human review still needs top-mark clearance, centering, and angle checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-base+damma` | pending | damma position and scale are readable across weights | Section-targeted mark snapshot shows damma samples across all five generated fonts. Human review still needs damma scale and Bold readability checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-base+kasra` | pending | bottom mark position clears descenders and sidebearings | Section-targeted mark snapshot shows kasra samples across all five generated fonts. Human review still needs bottom-mark clearance and sidebearing checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-shadda+sukun` | pending | stacked top marks remain clear and centered | Section-targeted mark snapshot shows shadda, sukun, and stacked composites across all five generated fonts. Prioritize the no-offset prompts for `بُّ` and `بَّ`. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-tanween` | pending | tanween combinations remain clear and aligned | Section-targeted mark snapshot shows tanween samples across all five generated fonts. Human review still needs twin-mark clarity and alignment checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-hamza-above-below` | pending | hamza combinations attach cleanly above and below | Section-targeted mark snapshot shows hamza-above and hamza-below samples across all five generated fonts. Human review still needs above/below clearance checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `mark-dotted-circle` | pending | dotted circle with top and bottom marks is readable | Section-targeted mark snapshot shows dotted circle with top, bottom, and tanween marks across all five generated fonts. Human review still needs dotted-circle readability checks. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `class-mark-combinations` | pending | shadda, hamza, tanween, sukun, and kasra composites | Use the shared mark proof to compare composite mark scale and stacking; mechanical mark setup is present, but visual approval is still pending. | Open `documentation/arabic-mark-review-proof.html`. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |

### 4. Dot-Stack Helpers And Urdu/Persian Texture

- Why: Three-dot and six-dot helpers are likely to need Bold/variable separation checks.
- Visual rows in worksheet: 1 (pending: 1)
- Decision rule: Fix only if dots merge, collide, or break the intended geometric texture.

Evidence to open:

- `documentation/contour-cleanup-decision-log.md`
- `documentation/arabic-cleanup-drawing-briefs.md`
- `documentation/arabic-manual-review-dashboard.html`

Snapshot aids:

- `class-dot-stack-helpers` Arabic manual dashboard: `documentation/arabic-review-snapshots/class-dot-stack-helpers.png` from `documentation/arabic-manual-review-dashboard.html`

| Key | Status | Review cue | AI observation | Human follow-up | Observed issue or `none` | Source/proof location | Final status | Guarded commands |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `class-dot-stack-helpers` | pending | three-dot and six-dot Persian/Urdu helpers | Section-targeted dashboard snapshot shows Persian/Urdu dotted letters across all generated fonts. Use it to inspect dot separation, especially in Bold and in the variable font. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |

### 5. RTL Text, Punctuation, Numerals, And Spacing

- Why: Once glyph structures look sane, review the typography in proof text, proofer, and waterfall views.
- Visual rows in worksheet: 18 (pending: 18)
- Decision rule: Use `fix-needed` for visual log rows when spacing or rhythm needs drawing work; use `pass` only after checking all weights.

Evidence to open:

- `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html`
- `documentation/arabic-manual-review-dashboard.html`
- `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html`
- `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html`
- `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html`
- `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html`
- `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html`
- `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html`
- `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html`
- `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html`
- `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html`
- `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html`
- `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html`
- `documentation/arabic-shaping-smoke-test.md`
- `documentation/contour-cleanup-decision-log.md`
- `documentation/arabic-cleanup-drawing-briefs.md`

Snapshot aids:

- `proof-regular-text` Regular text: `documentation/arabic-review-snapshots/proof-regular-text.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html`
- `proof-regular-proofer` Regular proofer: `documentation/arabic-review-snapshots/proof-regular-proofer.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html`
- `proof-regular-waterfall` Regular waterfall: `documentation/arabic-review-snapshots/proof-regular-waterfall.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html`
- `proof-medium-text` Medium text: `documentation/arabic-review-snapshots/proof-medium-text.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html`
- `proof-medium-proofer` Medium proofer: `documentation/arabic-review-snapshots/proof-medium-proofer.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html`
- `proof-medium-waterfall` Medium waterfall: `documentation/arabic-review-snapshots/proof-medium-waterfall.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html`
- `proof-semibold-text` SemiBold text: `documentation/arabic-review-snapshots/proof-semibold-text.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html`
- `proof-semibold-proofer` SemiBold proofer: `documentation/arabic-review-snapshots/proof-semibold-proofer.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html`
- `proof-semibold-waterfall` SemiBold waterfall: `documentation/arabic-review-snapshots/proof-semibold-waterfall.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html`
- `proof-bold-text` Bold text: `documentation/arabic-review-snapshots/proof-bold-text.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html`
- `proof-bold-proofer` Bold proofer: `documentation/arabic-review-snapshots/proof-bold-proofer.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html`
- `proof-bold-waterfall` Bold waterfall: `documentation/arabic-review-snapshots/proof-bold-waterfall.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html`
- `smoke-salaam` Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-salaam.png` from `documentation/arabic-manual-review-dashboard.html`
- `smoke-arabic` Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-arabic.png` from `documentation/arabic-manual-review-dashboard.html`
- `smoke-bismillah` Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-bismillah.png` from `documentation/arabic-manual-review-dashboard.html`
- `smoke-lam-alef` Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-lam-alef.png` from `documentation/arabic-manual-review-dashboard.html`
- `class-arabic-farsi-numerals` Arabic manual dashboard: `documentation/arabic-review-snapshots/class-arabic-farsi-numerals.png` from `documentation/arabic-manual-review-dashboard.html`
- `class-arabic-punctuation` Arabic manual dashboard: `documentation/arabic-review-snapshots/class-arabic-punctuation.png` from `documentation/arabic-manual-review-dashboard.html`

| Key | Status | Review cue | AI observation | Human follow-up | Observed issue or `none` | Source/proof location | Final status | Guarded commands |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `proof-regular-text` | pending | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-regular-proofer` | pending | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-regular-waterfall` | pending | Waterfall: small-size behavior, interpolation, and mark clarity | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-medium-text` | pending | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-medium-proofer` | pending | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-medium-waterfall` | pending | Waterfall: small-size behavior, interpolation, and mark clarity | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-semibold-text` | pending | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-semibold-proofer` | pending | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-semibold-waterfall` | pending | Waterfall: small-size behavior, interpolation, and mark clarity | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-bold-text` | pending | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence | Text snapshot renders mixed Latin/Arabic text without obvious blank-page failure. Inspect the full text proof for RTL texture, fallback, and mark collisions. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-bold-proofer` | pending | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing | Proofer snapshot currently reflects GF_Latin_Core content and shows many box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core coverage blocker context, not Arabic drawing proof by itself. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `proof-bold-waterfall` | pending | Waterfall: small-size behavior, interpolation, and mark clarity | Waterfall snapshot is available for size/interpolation checks. Open the HTML at multiple sizes before judging small-size Arabic mark clarity. | Open the matching gftools proof HTML. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `smoke-salaam` | pending | contextual forms and lam-alef behavior look intentional | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `smoke-arabic` | pending | initial, medial, and final joins are shaped and spaced coherently | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `smoke-bismillah` | pending | word spacing, medial joins, heh, and meem forms hold together | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `smoke-lam-alef` | pending | lam-alef ligature is present and weight-compatible | Dashboard smoke strings are visible across variable/static weights. Use the dashboard and shaping report to judge join rhythm and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `class-arabic-farsi-numerals` | pending | U+0660-U+0669 and U+06F0-U+06F9 rhythm, width, and style fit | Section-targeted dashboard snapshot shows Arabic-Indic digit rhythm across all generated fonts. Open the dashboard and glyph sources before judging digit widths and style fit. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |
| `class-arabic-punctuation` | pending | Arabic comma, semicolon, question mark, per mille, date separator, full stop, and parentheses | Section-targeted dashboard snapshot shows Arabic punctuation across all generated fonts. Review comma, semicolon, question mark, per mille, date separator, full stop, and parentheses in RTL context. | Open `documentation/arabic-manual-review-dashboard.html` and linked reports. |  |  | pass / fix-needed / deferred | `make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`<br>`make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`<br>`make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"` |

## Bundle Audit

- Worksheet rows: 32
- Matches pending/fix-needed visual rows: yes

## After Recording Outcomes

```bash
make reports-only
make preflight-only
```

If any row becomes `fix-needed`, open
`documentation/arabic-manual-edit-targets.md` before editing so
Regular and Bold stay compatible.
