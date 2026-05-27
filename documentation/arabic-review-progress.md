# Arabic Review Progress

This generated report is the short status surface for closing the
remaining human Arabic visual-review rows. It does not replace the
review log; it points to the next rows and commands.

## Summary

- Visual review ready: no
- Review rows: 32
- Pending: 32
- Fix-needed: 0
- Deferred: 0
- Pass: 0
- Unresolved rows: 32
- First-batch source checkpoint ready: yes
- Pending source checkpoint ready: yes
- Pending source glyphs/files: 68 glyphs / 136 files
- Pending source missing files: 0
- Pending source Regular/Bold mismatches: 0

## Open First

- `documentation/arabic-current-review-worksheet.md`
- `documentation/arabic-first-review-batch.md`
- `documentation/arabic-batch-recorder.md`
- `documentation/arabic-first-batch-source-checkpoint.md`
- `documentation/arabic-pending-source-checkpoint.md`
- `documentation/arabic-visual-review-log.md`

## Current Batch

- Name: 2. Structure And Wrong-Glyph Sweep
- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows: 5 (pending: 5)
- Contour rows: 0 (none)

| Key | Area / item | Status | Review cue |
| --- | --- | --- | --- |
| `proof-regular-glyphs` | GF proof / Regular glyphs | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-medium-glyphs` | GF proof / Medium glyphs | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-semibold-glyphs` | GF proof / SemiBold glyphs | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-bold-glyphs` | GF proof / Bold glyphs | pending | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `class-letter-structures` | Glyph class / letter-structures | pending | sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof |

## Recording Commands

After opening the proof/source evidence, run exactly one command per
reviewed row. Replace reviewer and notes before running.

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

## Batch Order

| Batch | Remaining visual rows |
| --- | ---: |
| 1. Open The Fast Dashboard | 0 |
| 2. Structure And Wrong-Glyph Sweep | 5 |
| 3. Marks, Dotted Circle, And Stacking | 8 |
| 4. Dot-Stack Helpers And Urdu/Persian Texture | 1 |
| 5. RTL Text, Punctuation, Numerals, And Spacing | 18 |

## After Any Status Updates

```bash
make reports-only
make preflight-only
```

Before closing the Arabic goal, verify:

- `documentation/arabic-goal-completion-audit.md`
