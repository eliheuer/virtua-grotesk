# Arabic Structure Triage

This generated report supports the next manual review batch:
`Structure And Wrong-Glyph Sweep`. It checks the built fonts for
mechanical problems that AI can reliably pre-triage before hand review.
It does not approve Arabic drawings or replace native-reader review.

## Summary

- Target glyphset: `GF_Arabic_Core` plus U+25CC dotted circle
- Fonts checked: 5
- Codepoints checked per font: 224
- Mechanical blocking risks: 0
- Review-prompt risk rows: 66
- Shared visible cmap mappings: 0

## Risk Counts

| Risk | Rows |
| --- | ---: |
| `deep-vertical-bound` | 26 |
| `large-negative-left-sidebearing` | 25 |
| `large-negative-right-sidebearing` | 20 |

## Grouped Review Prompts

These rows collapse repeated per-font sidebearing prompts into the
actual glyph/codepoint questions for the active structure review.
They do not approve the drawings; they point the hand review at
the shortest evidence set.

| Codepoint | Glyphs | Category | Fonts | Risk summary | Review prompt |
| --- | --- | --- | --- | --- | --- |
| `U+062B ARABIC LETTER THEH` | `uni062B` | letter | Bold, Medium, Regular, SemiBold, Variable | `large-negative-left-sidebearing`: 5<br>xMin -224..-224; right overhang -52..-20 | Check dot stack height and left overhang in glyph proofs before spacing edits. |
| `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | Bold, Medium, Regular, SemiBold, Variable | `deep-vertical-bound`: 5<br>xMin 24..64; right overhang -28..-24 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+062D ARABIC LETTER HAH` | `uni062D` | letter | Bold, Medium, Regular, SemiBold, Variable | `deep-vertical-bound`: 5<br>xMin 24..64; right overhang -28..-24 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | Bold, Medium, Regular, SemiBold, Variable | `deep-vertical-bound`: 5<br>xMin 24..64; right overhang -28..-24 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | Bold, Medium, Regular, SemiBold, Variable | `large-negative-left-sidebearing`: 5<br>xMin -368..-368; right overhang -96..-96 | Check whether the left overhang is intentional joining-script rhythm across all weights. |
| `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | Bold, Medium, Regular, SemiBold, Variable | `large-negative-left-sidebearing`: 5<br>xMin -368..-368; right overhang -96..-96 | Check whether the left overhang is intentional joining-script rhythm across all weights. |
| `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | Bold, Medium, Regular, SemiBold, Variable | `deep-vertical-bound`: 5<br>xMin 20..22; right overhang -46..-20 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | Bold, Medium, Regular, SemiBold, Variable | `deep-vertical-bound`: 5<br>xMin 20..22; right overhang -46..-20 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0645 ARABIC LETTER MEEM` | `uni0645` | letter | Bold | `deep-vertical-bound`: 1<br>xMin 54..54; right overhang -24..-24 | Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong. |
| `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | Bold, Medium, Regular, SemiBold, Variable | `large-negative-left-sidebearing`: 5<br>xMin -128..-128; right overhang -32..-32 | Check descending bowl and left overhang against adjacent text samples. |
| `U+0651 ARABIC SHADDA` | `uni0651` | mark | Bold, Medium, Regular, SemiBold, Variable | `large-negative-right-sidebearing`: 5<br>xMin 82..84; right overhang 326..328 | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | Bold, Medium, Regular, SemiBold, Variable | `large-negative-left-sidebearing`: 5<br>`large-negative-right-sidebearing`: 5<br>xMin -144..-144; right overhang 144..144 | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | Bold, Medium, Regular, SemiBold, Variable | `large-negative-right-sidebearing`: 5<br>xMin 0..0; right overhang 224..224 | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |
| `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | Bold, Medium, Regular, SemiBold, Variable | `large-negative-right-sidebearing`: 5<br>xMin 0..0; right overhang 224..224 | Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone. |

## Interpretation

- `maps-to-notdef`, `blank-visible-glyph`, and `nonmark-zero-advance`
  are likely source or build issues if present.
- Sidebearing and vertical-bound rows are prompts for hand inspection,
  especially in the focused structure sweep and glyph proof HTML.
- Shared visible cmap mappings should be reviewed as possible
  wrong-glyph mappings unless they are intentional aliases.

## Risk Rows

| Font | Codepoint | Glyph | Category | Advance | Bounds | Risks |
| --- | --- | --- | --- | ---: | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+062B ARABIC LETTER THEH` | `uni062B` | letter | 600 | `-224, 0, 548, 1024` | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | 600 | `64, -376, 576, 448` | `deep-vertical-bound` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+062D ARABIC LETTER HAH` | `uni062D` | letter | 600 | `64, -376, 576, 448` | `deep-vertical-bound` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | 600 | `64, -376, 576, 848` | `deep-vertical-bound` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | 864 | `-368, -296, 768, 432` | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | 864 | `-368, -296, 768, 880` | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | 600 | `22, -376, 554, 554` | `deep-vertical-bound` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | 600 | `22, -376, 554, 848` | `deep-vertical-bound` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | 570 | `-128, -256, 538, 408` | `large-negative-left-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0651 ARABIC SHADDA` | `uni0651` | mark | 0 | `84, 678.530612244898, 326, 843.2857142857143` | `large-negative-right-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | 0 | `-144, 4, 144, 152` | `large-negative-left-sidebearing`, `large-negative-right-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | 0 | `0, 832, 224, 1024` | `large-negative-right-sidebearing` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | 0 | `0, -256, 224, -64` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+062B ARABIC LETTER THEH` | `uni062B` | letter | 600 | `-224, 0, 548, 1024` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | 600 | `64, -376, 576, 448` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+062D ARABIC LETTER HAH` | `uni062D` | letter | 600 | `64, -376, 576, 448` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | 600 | `64, -376, 576, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | 864 | `-368, -296, 768, 432` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | 864 | `-368, -296, 768, 880` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | 600 | `22, -376, 554, 554` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | 600 | `22, -376, 554, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | 570 | `-128, -256, 538, 408` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0651 ARABIC SHADDA` | `uni0651` | mark | 0 | `84, 678.530612244898, 326, 843.2857142857143` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | 0 | `-144, 4, 144, 152` | `large-negative-left-sidebearing`, `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | 0 | `0, 832, 224, 1024` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | 0 | `0, -256, 224, -64` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+062B ARABIC LETTER THEH` | `uni062B` | letter | 600 | `-224, -4, 559, 1024` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | 600 | `51, -392, 575, 494` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+062D ARABIC LETTER HAH` | `uni062D` | letter | 600 | `51, -392, 575, 494` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | 600 | `51, -392, 575, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | 864 | `-368, -296, 768, 432` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | 864 | `-368, -296, 768, 880` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | 600 | `21, -397, 563, 587` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | 600 | `21, -397, 563, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | 570 | `-128, -256, 538, 408` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0651 ARABIC SHADDA` | `uni0651` | mark | 0 | `83, 677.530612244898, 327, 853.2857142857143` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | 0 | `-144, 4, 144, 152` | `large-negative-left-sidebearing`, `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | 0 | `0, 832, 224, 1024` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | 0 | `0, -256, 224, -64` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+062B ARABIC LETTER THEH` | `uni062B` | letter | 600 | `-224, -8, 569, 1024` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | 600 | `37, -408, 573, 540` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+062D ARABIC LETTER HAH` | `uni062D` | letter | 600 | `37, -408, 573, 540` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | 600 | `37, -408, 573, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | 864 | `-368, -296, 768, 432` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | 864 | `-368, -296, 768, 880` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | 600 | `21, -417, 571, 619` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | 600 | `21, -417, 571, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | 570 | `-128, -256, 538, 408` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0651 ARABIC SHADDA` | `uni0651` | mark | 0 | `83, 677.530612244898, 327, 863.2857142857143` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | 0 | `-144, 4, 144, 152` | `large-negative-left-sidebearing`, `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | 0 | `0, 832, 224, 1024` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | 0 | `0, -256, 224, -64` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+062B ARABIC LETTER THEH` | `uni062B` | letter | 600 | `-224, -12, 580, 1024` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+062C ARABIC LETTER JEEM` | `uni062C` | letter | 600 | `24, -424, 572, 586` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+062D ARABIC LETTER HAH` | `uni062D` | letter | 600 | `24, -424, 572, 586` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+062E ARABIC LETTER KHAH` | `uni062E` | letter | 600 | `24, -424, 572, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0633 ARABIC LETTER SEEN` | `uni0633` | letter | 864 | `-368, -296, 768, 432` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0634 ARABIC LETTER SHEEN` | `uni0634` | letter | 864 | `-368, -296, 768, 880` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0639 ARABIC LETTER AIN` | `uni0639` | letter | 600 | `20, -438, 580, 652` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+063A ARABIC LETTER GHAIN` | `uni063A` | letter | 600 | `20, -438, 580, 848` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0645 ARABIC LETTER MEEM` | `uni0645` | letter | 600 | `54, -376, 576, 548` | `deep-vertical-bound` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0648 ARABIC LETTER WAW` | `uni0648` | letter | 570 | `-128, -256, 538, 408` | `large-negative-left-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0651 ARABIC SHADDA` | `uni0651` | mark | 0 | `82, 676.530612244898, 328, 873.2857142857143` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0653 ARABIC MADDAH ABOVE` | `uni0653` | mark | 0 | `-144, 4, 144, 152` | `large-negative-left-sidebearing`, `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0654 ARABIC HAMZA ABOVE` | `uni0654` | mark | 0 | `0, 832, 224, 1024` | `large-negative-right-sidebearing` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `U+0655 ARABIC HAMZA BELOW` | `uni0655` | mark | 0 | `0, -256, 224, -64` | `large-negative-right-sidebearing` |

## Shared Visible Cmap Mappings

| Font | Glyph | Codepoints |
| --- | --- | --- |
| none | none | none |

## Next Manual Action

Open these together for the active structure review batch:

- `documentation/glyph-review/arabic-structure-sweep.html`
- `documentation/glyph-review/arabic-visual-risk-proof.html`
- `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`

Record the five batch-2 rows in
`documentation/glyph-review/arabic-visual-review-log.md` after hand inspection.
