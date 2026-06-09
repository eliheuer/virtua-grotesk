# Arabic AI Visual Screen: Batch 5

Scope: `RTL Text, Punctuation, Numerals, And Spacing`

Visual rows screened: 18

No `pass`, `fix-needed`, or `deferred` status was recorded.

This is an AI-assisted screen of the batch-5 proof artifacts. It is a
navigation and triage aid only. Human review in
`documentation/glyph-review/arabic-visual-review-log.md` remains the authority for
passing, fixing, or deferring a row.

## Evidence

- `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_text.html`
- `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_proofer.html`
- `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html`
- `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_text.html`
- `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_proofer.html`
- `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html`
- `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_text.html`
- `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html`
- `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html`
- `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_text.html`
- `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_proofer.html`
- `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html`
- `documentation/glyph-review/arabic-manual-review-dashboard.html`
- `documentation/glyph-review/arabic-shaping-smoke-test.md`
- `documentation/glyph-review/arabic-next-review-snapshots.md`
- `documentation/glyph-review/arabic-snapshot-integrity.md`

## Mechanical State

- Arabic shaping smoke fonts checked: 5.
- GSUB `arab/dflt`: 5 / 5.
- GPOS `arab/dflt`: 5 / 5.
- No `.notdef` in shaping smoke: yes.
- Snapshot integrity errors: 0.
- Batch row statuses: all pending human visual review.

## Snapshot Screen

| Review rows | AI screen note | Human follow-up |
| --- | --- | --- |
| `proof-regular-text`, `proof-medium-text`, `proof-semibold-text`, `proof-bold-text` | Text-proof PNGs are nonblank and show proof text across all static weights. | Inspect RTL texture, fallback, mark collisions, and unexpected spacing influence in the HTML proofs. |
| `proof-regular-proofer`, `proof-medium-proofer`, `proof-semibold-proofer`, `proof-bold-proofer` | Proofer PNGs are nonblank. Existing tofu/box cells are expected from remaining Latin Core coverage and should not be mistaken for Arabic drawing failure. | Inspect Arabic spacing, punctuation, and numeral rhythm in the HTML proofs; keep Latin Core coverage separate. |
| `proof-regular-waterfall`, `proof-medium-waterfall`, `proof-semibold-waterfall`, `proof-bold-waterfall` | Waterfall PNGs are nonblank and ready for size/interpolation review. | Inspect small-size Arabic mark clarity and weight progression in the HTML proofs. |
| `smoke-salaam`, `smoke-arabic`, `smoke-bismillah`, `smoke-lam-alef` | Section-targeted dashboard PNGs are nonblank and show smoke strings across Variable, Regular, Medium, SemiBold, and Bold. | Inspect contextual forms, word spacing, lam-alef behavior, and overall join rhythm. |
| `class-arabic-farsi-numerals` | Section-targeted dashboard PNG is nonblank and shows Arabic-Indic digit rhythm across generated fonts. | Inspect U+0660-U+0669 and U+06F0-U+06F9 widths, rhythm, and style fit. |
| `class-arabic-punctuation` | Section-targeted dashboard PNG is nonblank and shows Arabic punctuation across generated fonts. | Inspect comma, semicolon, question mark, per mille, date separator, full stop, and parentheses in RTL context. |

## Priority Checks

1. Review the four text proofs for RTL texture and mark collisions.
2. Review the four waterfalls for small-size mark clarity.
3. Review smoke strings for joining rhythm and lam-alef behavior.
4. Review Arabic/Farsi numerals for width and rhythm.
5. Review Arabic punctuation in RTL text context.
6. Keep proofer tofu tied to Latin Core coverage; do not record it as Arabic drawing failure.

