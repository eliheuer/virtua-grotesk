# Arabic First Review AI Sweep

This note records an AI visual sweep over the first Arabic review batch
snapshots. It is not a human Arabic review and does not mark any row in
`documentation/arabic-visual-review-log.md` as passed.

## Evidence Viewed

- `documentation/arabic-review-snapshots/proof-regular-glyphs.png`
- `documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png`
- `documentation/arabic-review-snapshots/proof-medium-glyphs.png`
- `documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png`
- `documentation/arabic-review-snapshots/proof-semibold-glyphs.png`
- `documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png`
- `documentation/arabic-review-snapshots/proof-bold-glyphs.png`
- `documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png`
- `documentation/arabic-first-review-zoom-snapshots.md`
- `documentation/arabic-review-snapshots/class-letter-structures.png`
- `documentation/arabic-review-snapshots/class-letter-structures-2.png`

## First-Pass Observations

| Row | AI observation | Human follow-up |
| --- | --- | --- |
| `proof-regular-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop does not show obvious tofu, `.notdef`, empty cells, or gross clipping at structure-screening scale. | Open `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html` at zoom before recording a status. |
| `proof-medium-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop follows the same coverage pattern as Regular/Bold: no obvious tofu, `.notdef`, empty cells, or gross clipping visible at structure-screening scale. | Open `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html` at zoom and compare the same high-risk glyphs before recording a status. |
| `proof-semibold-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop follows the same coverage pattern as Regular/Bold: no obvious tofu, `.notdef`, empty cells, or gross clipping visible at structure-screening scale. | Open `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html` at zoom and compare the same high-risk glyphs before recording a status. |
| `proof-bold-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop does not show obvious tofu, `.notdef`, empty cells, or gross clipping at structure-screening scale. | Open `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html` at zoom before recording a status. |
| `class-letter-structures` | The visual-risk proof shows `U+062B THEH` and part of `U+0633 SEEN` rendering in isolated, repeated, joining, and word contexts. The flagged negative left sidebearings look like review prompts in the shown shaped contexts, not automatic source errors. | Continue through the full HTML for `U+0634 SHEEN`, `U+0648 WAW`, and the mark-overhang rows before passing or deferring. |

## Concrete Watch Points

- The original full glyph-proof snapshots are useful only for page-level screening. The focused 2x crops make Arabic-row structure screening easier, but still do not prove small mark placement, dot collisions, or wrong-codepoint details.
- `U+062B THEH`: dot stack is visible in the risk proof; inspect whether the top dots become too tall or too close in Bold before accepting.
- `U+0633 SEEN` and `U+0634 SHEEN`: the long leftward stroke is expected in shaped Arabic context; do not fix sidebearings from bounds alone.
- `U+0648 WAW`: still needs full-proof inspection for the descending bowl and left overhang in adjacent text.
- `U+0653`, `U+0654`, `U+0655`: expected zero-advance overhang; defer judgment to the mark/dotted-circle batch unless obvious clipping appears in the glyph proof.

## Non-Decisions

- No row was marked `pass`.
- No source glyph was marked `fix-needed`.
- No spacing edit is recommended from this sweep alone.
