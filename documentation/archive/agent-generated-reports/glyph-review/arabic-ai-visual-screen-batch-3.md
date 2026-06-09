# Arabic AI Visual Screen: Batch 3

Scope: `Marks, Dotted Circle, And Stacking`

Visual rows screened: 8

No `pass`, `fix-needed`, or `deferred` status was recorded.

This is an AI-assisted screen of the batch-3 proof artifacts. It is a
navigation and triage aid only. Human review in
`documentation/glyph-review/arabic-visual-review-log.md` remains the authority for
passing, fixing, or deferring a row.

## Evidence

- `documentation/glyph-review/arabic-mark-review-proof.html`
- `documentation/glyph-review/arabic-mark-triage.md`
- `documentation/glyph-review/arabic-mark-readiness.md`
- `documentation/glyph-review/arabic-next-review-snapshots.md`
- `documentation/glyph-review/arabic-snapshot-integrity.md`
- `documentation/glyph-review/review-snapshots/mark-base+fatha.png`
- `documentation/glyph-review/review-snapshots/mark-base+damma.png`
- `documentation/glyph-review/review-snapshots/mark-base+kasra.png`
- `documentation/glyph-review/review-snapshots/mark-shadda+sukun.png`
- `documentation/glyph-review/review-snapshots/mark-tanween.png`
- `documentation/glyph-review/review-snapshots/mark-hamza-above-below.png`
- `documentation/glyph-review/review-snapshots/mark-dotted-circle.png`
- `documentation/glyph-review/review-snapshots/class-mark-combinations.png`

## Mechanical State

- Required Arabic Core marks present: 16 / 16.
- U+25CC dotted circle present: yes.
- Source anchors present: yes.
- Built `mark`/`mkmk` GPOS present in all generated fonts: yes.
- GDEF marks present in all generated fonts: yes.
- Mark triage mechanical blocking risks: 0.
- Mark triage no-offset review prompts: 10.

The no-offset prompts are all in `mark-shadda+sukun`, for `بُّ` and
`بَّ` across Regular, Medium, SemiBold, Bold, and Variable. They are not
automatic failures because this source can draw composite marks at the
intended origin; they are the highest-priority human check in this batch.

## Snapshot Screen

| Review row | AI screen note | Human follow-up |
| --- | --- | --- |
| `mark-base+fatha` | Section-specific PNG is nonblank and shows fatha samples across all five generated fonts. | Inspect top-mark clearance, centering, and angle over wide and narrow bases. |
| `mark-base+damma` | Section-specific PNG is nonblank and shows damma samples across all five generated fonts. | Inspect damma scale/readability, especially in Bold. |
| `mark-base+kasra` | Section-specific PNG is nonblank and shows bottom-mark samples across all five generated fonts. | Inspect descender clearance and sidebearing interactions. |
| `mark-shadda+sukun` | Section-specific PNG is nonblank and shows shadda, sukun, and stacked composites across all five generated fonts. | Prioritize `بُّ` and `بَّ`; decide whether origin-drawn composites are acceptable. |
| `mark-tanween` | Section-specific PNG is nonblank and shows fathatan, dammatan, and kasratan samples across all five generated fonts. | Inspect twin-mark clarity and alignment. |
| `mark-hamza-above-below` | Section-specific PNG is nonblank and shows above/below hamza on several bases across all five generated fonts. | Inspect below-mark clearance on descenders and above-mark fit on narrow bases. |
| `mark-dotted-circle` | Section-specific PNG is nonblank and shows dotted circle with top, bottom, and tanween marks across all five generated fonts. | Inspect dotted-circle readability with each mark class. |
| `class-mark-combinations` | Section-specific PNG is nonblank and shows the required mark inventory on dotted circle across all five generated fonts. | Confirm all required marks remain identifiable at the proof size. |

## Priority Checks

1. Review `mark-shadda+sukun` no-offset prompts for `بُّ` and `بَّ`.
2. Check dotted-circle readability with top, bottom, and stacked marks.
3. Check kasra, kasratan, and hamzabelow clearance.
4. Check damma and tanween scale in Bold.
5. Check top-mark centering over wide bases such as seen and sad.

