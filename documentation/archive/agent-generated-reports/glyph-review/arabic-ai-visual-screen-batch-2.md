# Arabic AI Visual Screen: Batch 2

This note records an AI visual screen of the current batch-2 Arabic
structure and wrong-glyph evidence. It does not mark any review row as
passed. Use it to make the human proof pass faster, then record outcomes
in `documentation/glyph-review/arabic-visual-review-log.md`.

## Scope

- Review batch: `Structure And Wrong-Glyph Sweep`
- Visual rows screened: 5
- Source reports:
  - `documentation/glyph-review/arabic-structure-triage.md`
  - `documentation/glyph-review/arabic-visual-risk-audit.md`
  - `documentation/glyph-review/arabic-first-review-crop-integrity.md`
  - `documentation/glyph-review/review-snapshots/proof-regular-glyphs-arabic-zoom.png`
  - `documentation/glyph-review/review-snapshots/proof-medium-glyphs-arabic-zoom.png`
  - `documentation/glyph-review/review-snapshots/proof-semibold-glyphs-arabic-zoom.png`
  - `documentation/glyph-review/review-snapshots/proof-bold-glyphs-arabic-zoom.png`
  - `documentation/glyph-review/review-snapshots/class-letter-structures-2.png`

## Summary

- No blank-page, missing-image, or all-white snapshot failure was visible in
  the batch-2 PNG evidence.
- The four focused glyph-proof crops show Arabic glyph rows present across
  Regular, Medium, SemiBold, and Bold.
- The focused crops do not show an obvious weight-specific dropout, but they
  are broad page crops; the full proof HTML still needs hand inspection at
  zoom before recording `pass`.
- The mechanical structure triage has 0 blocking risks. Its remaining rows are
  sidebearing/overhang prompts for `U+062B`, `U+0633`, `U+0634`, `U+0648`,
  `U+0653`, `U+0654`, and `U+0655`.
- Mark sidebearing prompts for `U+0653`, `U+0654`, and `U+0655` are expected
  zero-advance mark overhang checks, not batch-2 drawing failures by
  themselves.

## Row Screen

| Review row | AI screen | Human follow-up before status |
| --- | --- | --- |
| `proof-regular-glyphs` | Focused crop is nonblank and includes Arabic glyph rows. No obvious missing Arabic row or wrong-font fallback is visible at this zoom. | Open `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html` and check individual Arabic cells for clipping, duplicates, wrong codepoints, and malformed joins. |
| `proof-medium-glyphs` | Focused crop is nonblank and broadly matches the Regular crop. No obvious Medium-only dropout is visible at this zoom. | Open `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`; compare `U+062B`, `U+0633`, `U+0634`, and `U+0648` against Regular/Bold. |
| `proof-semibold-glyphs` | Focused crop is nonblank and broadly matches neighboring weights. No obvious SemiBold-only missing glyph is visible at this zoom. | Open `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`; check whether interpolation-driven width changes make `U+0634` feel cramped. |
| `proof-bold-glyphs` | Focused crop is nonblank and Arabic rows are present. No obvious Bold-only missing glyph is visible at this zoom. | Open `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`; inspect Bold `U+0634` because it is the only structure row with both left and right sidebearing prompts. |
| `class-letter-structures` | The visual-risk proof renders comparison samples for the high-risk letters. `U+062B` dot stacks, `U+0633`/`U+0634` left overhang, and `U+0648` bowl overhang are visible in shaped contexts. | Open `documentation/glyph-review/arabic-visual-risk-proof.html`; decide whether each overhang is intentional RTL joining rhythm or needs source spacing/drawing edits. |

## Priority Checks For Human Review

1. `U+0634 ARABIC LETTER SHEEN` in Bold: this is the only current batch-2
   prompt with both large negative left and right sidebearing flags.
2. `U+0633` and `U+0634` across weights: verify the left overhang reads as
   joining-script rhythm rather than accidental overshoot.
3. `U+062B`: verify three-dot height and spacing in repeated and word rhythm
   samples, especially Regular to Medium.
4. `U+0648`: inspect the descending bowl and left overhang in adjacent text
   before changing sidebearings.
5. `U+0653`, `U+0654`, `U+0655`: keep these in the mark-review batch unless
   the glyph proof shows clipping or wrong-codepoint rendering.

## Non-Decisions

- No `pass`, `fix-needed`, or `deferred` status was recorded.
- No source GLIF was changed from this screen.
- No Rubik or other reference outlines were copied or recommended.
