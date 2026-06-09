# Arabic First Review Risk Shortlist

This generated note records AI-visible structure risks from the focused
Arabic-row glyph crops for the first review batch. It is not a human
Arabic review and does not mark any row in
`documentation/glyph-review/arabic-visual-review-log.md` as passed.

## Evidence

- Focused crop report: `documentation/glyph-review/arabic-first-review-zoom-snapshots.md`
- Focused crop integrity: `documentation/glyph-review/arabic-first-review-crop-integrity.md`
- First review worksheet: `documentation/glyph-review/arabic-first-review-batch.md`
- AI sweep note: `documentation/glyph-review/arabic-first-review-ai-sweep.md`

| Review key | Weight | Focused crop | File status | AI-visible structure screen |
| --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | Regular | `documentation/glyph-review/review-snapshots/proof-regular-glyphs-arabic-zoom.png` | present | Nonblank crop; no obvious tofu, `.notdef`, blank Arabic cell, or gross clipping visible at crop scale. |
| `proof-medium-glyphs` | Medium | `documentation/glyph-review/review-snapshots/proof-medium-glyphs-arabic-zoom.png` | present | Nonblank crop; no obvious tofu, `.notdef`, blank Arabic cell, or gross clipping visible at crop scale. |
| `proof-semibold-glyphs` | SemiBold | `documentation/glyph-review/review-snapshots/proof-semibold-glyphs-arabic-zoom.png` | present | Nonblank crop; no obvious tofu, `.notdef`, blank Arabic cell, or gross clipping visible at crop scale. |
| `proof-bold-glyphs` | Bold | `documentation/glyph-review/review-snapshots/proof-bold-glyphs-arabic-zoom.png` | present | Nonblank crop; no obvious tofu, `.notdef`, blank Arabic cell, or gross clipping visible at crop scale. |

## First-Pass Risk Shortlist

| AI-visible observation | Human review action |
| --- | --- |
| The focused crops show nonblank Arabic rows across all four weights. | Use this only to speed up structure screening; it is not enough to pass a row. |
| No obvious tofu boxes, `.notdef` glyphs, fully blank Arabic cells, or gross clipping are visible at crop scale. | Still open each full glyph proof to catch wrong-codepoint drawings and small mark issues. |
| `U+062B THEH`, `U+0633 SEEN`, `U+0634 SHEEN`, and `U+0648 WAW` remain the first shape-specific watch points. | Compare the full proof with `documentation/glyph-review/arabic-structure-triage.md` before editing sidebearings or outlines. |
| `U+0653`, `U+0654`, and `U+0655` are visible only as small zero-advance marks in this crop. | Judge their placement in the mark proof and dotted-circle context, not from the glyph crop alone. |

## Non-Decisions

- No row was marked `pass`.
- No row was marked `fix-needed` from this crop review alone.
- No row was deferred.
- Do not edit Arabic sidebearings from the crop alone; verify shaped RTL context first.
- Do not copy reference-font outlines. Use references only to compare structure, dot placement, and mark placement.

## Next Human Step

Open the five-row worksheet in `documentation/glyph-review/arabic-first-review-batch.md`
and review the full proof HTML plus source targets for each row. Record
a guarded status only after that proof/source pass.
