# Arabic Batch Recorder

This generated file keeps the status-recording commands for the current
unresolved Arabic hand-review batch in one place. It does not apply any
status changes by itself, and the commands should only be run after
proof/source inspection.

## Current Batch

- Batch: 2. Structure And Wrong-Glyph Sweep
- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows: 5 (pending: 5)
- Contour rows: 0 (none)

## Visual Review Commands

Use exactly one command per reviewed row. Replace the reviewer and notes
before running.

### `proof-regular-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-letter-structures`

- Review cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Contour Decision Commands

No contour-decision rows in this batch.

## After Recording Outcomes

```bash
make reports-only
make preflight-only
```

If any row becomes `fix-needed`, use
`documentation/arabic-manual-edit-targets.md` before editing so Regular
and Bold stay compatible.

## Full Batch Order

- 1. Open The Fast Dashboard: visual none; contour none
- 2. Structure And Wrong-Glyph Sweep: visual pending: 5; contour none
- 3. Marks, Dotted Circle, And Stacking: visual pending: 8; contour none
- 4. Dot-Stack Helpers And Urdu/Persian Texture: visual pending: 1; contour none
- 5. RTL Text, Punctuation, Numerals, And Spacing: visual pending: 18; contour none
