# Arabic Current Review Worksheet

This generated worksheet is the fill-in sheet for the current Arabic
hand-review batch. It is not an approval artifact by itself: record
outcomes only after opening the linked proof/source evidence.

## Batch

- Name: 2. Structure And Wrong-Glyph Sweep
- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows: 5 (pending: 5)
- Contour rows: 0 (none)
- Decision rule: Confirm the contour queue is empty, then record the visual review rows only.

## Source Structure Guard

- First-batch checkpoint: `documentation/arabic-first-batch-source-checkpoint.md`
- Full unresolved-queue checkpoint: `documentation/arabic-pending-source-checkpoint.md`
- Use these before source edits to confirm every reviewed `fix-needed`
  row still maps to paired Regular and Bold GLIF files with no
  structure mismatches.

## Evidence To Open

- `documentation/arabic-print-proof.pdf`
- `documentation/arabic-print-proof-index.md`
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
- `documentation/arabic-first-batch-source-checkpoint.md`
- `documentation/arabic-pending-source-checkpoint.md`
- `documentation/arabic-first-review-ai-sweep.md`

## Snapshot Aids

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

## AI Triage Notes

These notes come from `documentation/arabic-first-review-ai-sweep.md`.
They are not review decisions and do not justify recording `pass`
without opening the linked proof/source evidence.

| Key | AI observation | Human follow-up |
| --- | --- | --- |
| `proof-regular-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop does not show obvious tofu, `.notdef`, empty cells, or gross clipping at structure-screening scale. | Open `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html` at zoom before recording a status. |
| `proof-medium-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop follows the same coverage pattern as Regular/Bold: no obvious tofu, `.notdef`, empty cells, or gross clipping visible at structure-screening scale. | Open `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html` at zoom and compare the same high-risk glyphs before recording a status. |
| `proof-semibold-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop follows the same coverage pattern as Regular/Bold: no obvious tofu, `.notdef`, empty cells, or gross clipping visible at structure-screening scale. | Open `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html` at zoom and compare the same high-risk glyphs before recording a status. |
| `proof-bold-glyphs` | The visible glyph proof is nonblank, and the focused 2x Arabic-row crop does not show obvious tofu, `.notdef`, empty cells, or gross clipping at structure-screening scale. | Open `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html` at zoom before recording a status. |
| `class-letter-structures` | The visual-risk proof shows `U+062B THEH` and part of `U+0633 SEEN` rendering in isolated, repeated, joining, and word contexts. The flagged negative left sidebearings look like review prompts in the shown shaped contexts, not automatic source errors. | Continue through the full HTML for `U+0634 SHEEN`, `U+0648 WAW`, and the mark-overhang rows before passing or deferring. |

## Print-Proof Pass

Use `documentation/arabic-print-proof.pdf` as the quick paper or PDF
scan for this batch before opening the heavier HTML proof pages.
Use `documentation/arabic-print-proof-index.md` to jump to the
right style and section in the PDF.
For each row, look for missing glyphs, wrong glyphs, clipping,
blank cells, malformed joins, and weight-specific rhythm changes.
The PDF is a review aid: record `pass`, `fix-needed`, or
`deferred` only after checking the linked source/proof evidence.

## Glyph-Level Drawing Punchlist

Use this as the first-pass inspection order for the current
batch. It is not an edit instruction by itself: edit only after
a row is marked `fix-needed`, and then keep Regular and Bold
source files structurally compatible.

| Glyph | Masters | Review prompt source |
| --- | --- | --- |
| `hamzaabove-ar` | Bold, Regular | `U+0654 ARABIC HAMZA ABOVE` structure prompt |
| `hamzabelow-ar` | Bold, Regular | `U+0655 ARABIC HAMZA BELOW` structure prompt |
| `madda-ar` | Bold, Regular | `U+0653 ARABIC MADDAH ABOVE` structure prompt |
| `seen-ar` | Bold, Regular | `U+0633 ARABIC LETTER SEEN` structure prompt |
| `sheen-ar` | Bold, Regular | `U+0634 ARABIC LETTER SHEEN` structure prompt |
| `theh-ar` | Bold, Regular | `U+062B ARABIC LETTER THEH` structure prompt |
| `waw-ar` | Bold, Regular | `U+0648 ARABIC LETTER WAW` structure prompt |

## Fill-In Review Table

| Key | Current status | Machine precheck | Review cue | Observed issue or `none` | Source/proof location | Final status |
| --- | --- | --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | pending | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |  |  | pass / fix-needed / deferred |
| `proof-medium-glyphs` | pending | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |  |  | pass / fix-needed / deferred |
| `proof-semibold-glyphs` | pending | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |  |  | pass / fix-needed / deferred |
| `proof-bold-glyphs` | pending | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |  |  | pass / fix-needed / deferred |
| `class-letter-structures` | pending | Contour decisions pending: 0; fix-now: 0 | sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof |  |  | pass / fix-needed / deferred |

## Recording Commands

Use exactly one command per reviewed row after filling the table. Replace
`Name YYYY-MM-DD` and the notes before running.

### `proof-regular-glyphs`

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-glyphs`

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-glyphs`

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-glyphs`

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-letter-structures`

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## After Recording Outcomes

```bash
make reports-only
make preflight-only
```

If any row becomes `fix-needed`, open
`documentation/arabic-manual-edit-targets.md` before editing so
Regular and Bold stay compatible.
