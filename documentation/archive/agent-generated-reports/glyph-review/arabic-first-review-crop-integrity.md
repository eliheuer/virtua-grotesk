# Arabic First Review Crop Integrity

This generated report mechanically checks the focused Arabic-row PNG
crops for the first hand-review batch. It proves only that the crop files
are readable, correctly sized, and nonblank; it is not a human Arabic
drawing review.

- Expected dimensions: 2880x1040
- Requested crops: 4
- Readable crops: 4
- Dimension matches: 4
- Nonblank crops: 4
- Crop errors: 0
- Evidence ready for hand review: yes

## Crop Checks

| Review key | Weight | Crop path | Dimensions | File status | Nonwhite sample | Content bbox | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | Regular | `documentation/glyph-review/review-snapshots/proof-regular-glyphs-arabic-zoom.png` | 2880x1040 | readable | 3.5734% | 30,0,2834,1040 | ok |
| `proof-medium-glyphs` | Medium | `documentation/glyph-review/review-snapshots/proof-medium-glyphs-arabic-zoom.png` | 2880x1040 | readable | 3.7030% | 30,0,2834,1040 | ok |
| `proof-semibold-glyphs` | SemiBold | `documentation/glyph-review/review-snapshots/proof-semibold-glyphs-arabic-zoom.png` | 2880x1040 | readable | 3.8091% | 30,0,2834,1040 | ok |
| `proof-bold-glyphs` | Bold | `documentation/glyph-review/review-snapshots/proof-bold-glyphs-arabic-zoom.png` | 2880x1040 | readable | 3.9219% | 30,0,2834,1040 | ok |

## Non-Decisions

- No row was marked `pass`.
- No row was marked `fix-needed`.
- No row was deferred.
- Do not edit Arabic outlines, marks, or sidebearings from this report alone.
