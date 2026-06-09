# Arabic Batch Recorder

This generated file keeps the status-recording commands for the current
unresolved Arabic hand-review batch in one place. It does not apply any
status changes by itself, and the commands should only be run after
proof/source inspection.

## Current Batch

- Batch: 2. Structure And Wrong-Glyph Sweep
- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows: 5 (pending: 5)
- Contour rows: 4 (pending: 4)
- Focused Arabic PDF proof: `documentation/glyph-review/arabic-print-proof.pdf`
- Focused Arabic PDF index: `documentation/glyph-review/arabic-print-proof-index.md`
- First-batch source checkpoint: `documentation/glyph-review/arabic-first-batch-source-checkpoint.md`
- Pending source checkpoint: `documentation/glyph-review/arabic-pending-source-checkpoint.md`

## Visual Review Commands

Use exactly one command per reviewed row. Replace the reviewer and notes
before running.

### `proof-regular-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Arabic print proof pages: p. 3 Regular cmap grid

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Arabic print proof pages: p. 6 Medium cmap grid

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Arabic print proof pages: p. 9 SemiBold cmap grid

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-glyphs`

- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Arabic print proof pages: p. 12 Bold cmap grid

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-letter-structures`

- Review cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof
- Arabic print proof pages: p. 3 Regular cmap grid; p. 6 Medium cmap grid; p. 9 SemiBold cmap grid; p. 12 Bold cmap grid; p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Optional Batch TSV Form

The canonical record is `documentation/glyph-review/arabic-visual-review-log.md`.
The per-row commands above are the clearest path. If you prefer
to record several reviewed rows at once, save a tab-separated
file with these columns, then dry-run it before applying.

```tsv
key	status	reviewer	notes
proof-regular-glyphs	pass	Name YYYY-MM-DD	reviewed current proof/source evidence
proof-medium-glyphs	pass	Name YYYY-MM-DD	reviewed current proof/source evidence
proof-semibold-glyphs	pass	Name YYYY-MM-DD	reviewed current proof/source evidence
proof-bold-glyphs	pass	Name YYYY-MM-DD	reviewed current proof/source evidence
class-letter-structures	pass	Name YYYY-MM-DD	reviewed current proof/source evidence
```

```bash
make arabic-visual-review-batch-dry-run REVIEW_BATCH=review.tsv
make arabic-visual-review-batch-update REVIEW_BATCH=review.tsv
make arabic-visual-review-batch-apply-check REVIEW_BATCH=review.tsv
```

Use the dry run first. The update target writes only the
canonical review log; the apply-check target writes the log,
regenerates reports, and reruns preflight.

## Contour Decision Commands

### `dad-ar.init`

```bash
make contour-decision-update GLYPH=dad-ar.init STATUS=fix-now DECISION="source edit needed" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=dad-ar.init STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=dad-ar.init STATUS=deferred DECISION="needs later drawing review" REVIEWED="Name YYYY-MM-DD"
```

### `hah-ar.fina`

```bash
make contour-decision-update GLYPH=hah-ar.fina STATUS=fix-now DECISION="source edit needed" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=hah-ar.fina STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=hah-ar.fina STATUS=deferred DECISION="needs later drawing review" REVIEWED="Name YYYY-MM-DD"
```

### `jeem-ar.fina`

```bash
make contour-decision-update GLYPH=jeem-ar.fina STATUS=fix-now DECISION="source edit needed" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=jeem-ar.fina STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=jeem-ar.fina STATUS=deferred DECISION="needs later drawing review" REVIEWED="Name YYYY-MM-DD"
```

### `sad-ar.init`

```bash
make contour-decision-update GLYPH=sad-ar.init STATUS=fix-now DECISION="source edit needed" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=sad-ar.init STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=sad-ar.init STATUS=deferred DECISION="needs later drawing review" REVIEWED="Name YYYY-MM-DD"
```

## After Recording Outcomes

```bash
make reports-only
make preflight-only
```

If any row becomes `fix-needed`, use
`documentation/glyph-review/arabic-manual-edit-targets.md` and rerun
`make arabic-first-batch-source-checkpoint` plus
`make arabic-pending-source-checkpoint` before editing so Regular
and Bold stay compatible.

## Full Batch Order

- 1. Open The Fast Dashboard: visual none; contour none
- 2. Structure And Wrong-Glyph Sweep: visual pending: 5; contour pending: 4
- 3. Marks, Dotted Circle, And Stacking: visual pending: 8; contour none
- 4. Dot-Stack Helpers And Urdu/Persian Texture: visual pending: 1; contour none
- 5. RTL Text, Punctuation, Numerals, And Spacing: visual pending: 18; contour none
