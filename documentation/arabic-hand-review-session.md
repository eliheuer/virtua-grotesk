# Arabic Hand Review Session

This generated sheet is the compact execution view for the remaining
human Arabic visual review. Use it with the local review board and
proof HTML; it is not a substitute for human proof/source inspection.

## Summary

- Pending/fix-needed rows in this sheet: 32
- Pending: 32
- Fix-needed: 0
- Deferred in active queue: 0
- Review log: `documentation/arabic-visual-review-log.md`
- Local review board: `documentation/arabic-next-review-board.html`
- Arabic PDF proof: `documentation/arabic-print-proof.pdf`
- Arabic PDF proof index: `documentation/arabic-print-proof-index.md`
- Full edit-target report: `documentation/arabic-manual-edit-targets.md`

## Rules

- Review the proof HTML or source glyphs before recording `pass`.
- Record `fix-needed` only with exact glyph names, proof locations, or source files.
- Edit Regular and Bold together, preserving compatible glyph structure.
- After any edit batch, run `./build.sh`, `make reports-only`, and `make preflight-only`.

## Glyph Proof First Pass

### `proof-regular-glyphs`

- Area/item: GF proof / Regular glyphs
- Status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 3 Regular cmap grid
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Regular glyphs: `documentation/arabic-review-snapshots/proof-regular-glyphs.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
  - Regular Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-regular-glyphs.png`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-glyphs`

- Area/item: GF proof / Medium glyphs
- Status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/gftools-qa/Proof/*Medium*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 6 Medium cmap grid
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Medium glyphs: `documentation/arabic-review-snapshots/proof-medium-glyphs.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
  - Medium Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-medium-glyphs.png`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-glyphs`

- Area/item: GF proof / SemiBold glyphs
- Status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/gftools-qa/Proof/*SemiBold*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 9 SemiBold cmap grid
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - SemiBold glyphs: `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
  - SemiBold Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-semibold-glyphs.png`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-glyphs`

- Area/item: GF proof / Bold glyphs
- Status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/gftools-qa/Proof/*Bold*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 12 Bold cmap grid
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Bold glyphs: `documentation/arabic-review-snapshots/proof-bold-glyphs.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
  - Bold Arabic glyph rows focused 2x crop: `documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png` from `documentation/arabic-review-snapshots/proof-bold-glyphs.png`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-letter-structures`

- Area/item: Glyph class / letter-structures
- Status: `pending`
- Review cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-visual-risk-proof.html`
- Arabic print proof pages: p. 3 Regular cmap grid; p. 6 Medium cmap grid; p. 9 SemiBold cmap grid; p. 12 Bold cmap grid; p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic structure sweep: `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`
  - Arabic visual risk proof: `documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 4
  - Contour decisions marked fix-now: 0
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Marks And Dotted Circle

### `mark-base+fatha`

- Area/item: Mark attachment / base+fatha
- Status: `pending`
- Review cue: top mark position clears the base and matches style
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+fatha.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 4 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/fatha-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/fatha-ar.glif`

```bash
make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-base+fatha REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-base+damma`

- Area/item: Mark attachment / base+damma
- Status: `pending`
- Review cue: damma position and scale are readable across weights
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+damma.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 4 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/damma-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/damma-ar.glif`

```bash
make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-base+damma REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-base+kasra`

- Area/item: Mark attachment / base+kasra
- Status: `pending`
- Review cue: bottom mark position clears descenders and sidebearings
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-base+kasra.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 4 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/kasra-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/kasra-ar.glif`

```bash
make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-base+kasra REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-shadda+sukun`

- Area/item: Mark attachment / shadda+sukun
- Status: `pending`
- Review cue: stacked top marks remain clear and centered
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-shadda+sukun.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 10 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/shadda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/shadda-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 6

```bash
make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-shadda+sukun REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-tanween`

- Area/item: Mark attachment / tanween
- Status: `pending`
- Review cue: tanween combinations remain clear and aligned
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-tanween.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 8 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/fathatan-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/fathatan-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 4

```bash
make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-tanween REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-hamza-above-below`

- Area/item: Mark attachment / hamza-above-below
- Status: `pending`
- Review cue: hamza combinations attach cleanly above and below
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-hamza-above-below.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 6 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 2

```bash
make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-hamza-above-below REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `mark-dotted-circle`

- Area/item: Mark attachment / dotted-circle
- Status: `pending`
- Review cue: dotted circle with top and bottom marks is readable
- Evidence: `documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/mark-dotted-circle.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 14 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/dottedCircle.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/dottedCircle.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/fatha-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/fatha-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 10

```bash
make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=mark-dotted-circle REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-mark-combinations`

- Area/item: Glyph class / mark-combinations
- Status: `pending`
- Review cue: shadda, hamza, tanween, sukun, and kasra composites
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic mark proof: `documentation/arabic-review-snapshots/class-mark-combinations.png` from `documentation/arabic-mark-review-proof.html`
- Focused review pages:
  - `documentation/arabic-mark-review-proof.html`
  - `documentation/arabic-mark-triage.md`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Mark triage mechanical blockers: 0
  - Mark triage no-offset prompts: 10
- Edit targets: Source targets: 28 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/dottedCircle.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/dottedCircle.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 24

```bash
make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-mark-combinations REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-dot-stack-helpers`

- Area/item: Glyph class / dot-stack-helpers
- Status: `pending`
- Review cue: three-dot and six-dot Persian/Urdu helpers
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/class-dot-stack-helpers.png` from `documentation/arabic-manual-review-dashboard.html`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 4
  - Contour decisions marked fix-now: 0
- Edit targets: Source targets: 26 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/dotcenter-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/dotcenter-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/twodotshorizontalbelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/twodotshorizontalbelow-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 22

```bash
make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-dot-stack-helpers REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Proof Texture And Spacing

### `proof-regular-text`

- Area/item: GF proof / Regular text
- Status: `pending`
- Review cue: Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence
- Evidence: `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_text.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Regular text: `documentation/arabic-review-snapshots/proof-regular-text.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Regular-diffbrowsers_text.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-regular-proofer`

- Area/item: GF proof / Regular proofer
- Status: `pending`
- Review cue: Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing
- Evidence: `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_proofer.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 2 Regular numerals and punctuation
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Regular proofer: `documentation/arabic-review-snapshots/proof-regular-proofer.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Regular-diffbrowsers_proofer.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-regular-waterfall`

- Area/item: GF proof / Regular waterfall
- Status: `pending`
- Review cue: Waterfall: small-size behavior, interpolation, and mark clarity
- Evidence: `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_waterfall.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Regular waterfall: `documentation/arabic-review-snapshots/proof-regular-waterfall.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Regular-diffbrowsers_waterfall.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-text`

- Area/item: GF proof / Medium text
- Status: `pending`
- Review cue: Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence
- Evidence: `documentation/gftools-qa/Proof/*Medium*-diffbrowsers_text.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 4 Medium Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Medium text: `documentation/arabic-review-snapshots/proof-medium-text.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Medium-diffbrowsers_text.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-proofer`

- Area/item: GF proof / Medium proofer
- Status: `pending`
- Review cue: Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing
- Evidence: `documentation/gftools-qa/Proof/*Medium*-diffbrowsers_proofer.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 4 Medium Arabic samples; p. 5 Medium numerals and punctuation
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Medium proofer: `documentation/arabic-review-snapshots/proof-medium-proofer.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Medium-diffbrowsers_proofer.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-waterfall`

- Area/item: GF proof / Medium waterfall
- Status: `pending`
- Review cue: Waterfall: small-size behavior, interpolation, and mark clarity
- Evidence: `documentation/gftools-qa/Proof/*Medium*-diffbrowsers_waterfall.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 4 Medium Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Medium waterfall: `documentation/arabic-review-snapshots/proof-medium-waterfall.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Medium-diffbrowsers_waterfall.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-text`

- Area/item: GF proof / SemiBold text
- Status: `pending`
- Review cue: Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence
- Evidence: `documentation/gftools-qa/Proof/*SemiBold*-diffbrowsers_text.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 7 SemiBold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - SemiBold text: `documentation/arabic-review-snapshots/proof-semibold-text.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_text.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-proofer`

- Area/item: GF proof / SemiBold proofer
- Status: `pending`
- Review cue: Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing
- Evidence: `documentation/gftools-qa/Proof/*SemiBold*-diffbrowsers_proofer.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 7 SemiBold Arabic samples; p. 8 SemiBold numerals and punctuation
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - SemiBold proofer: `documentation/arabic-review-snapshots/proof-semibold-proofer.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_proofer.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-waterfall`

- Area/item: GF proof / SemiBold waterfall
- Status: `pending`
- Review cue: Waterfall: small-size behavior, interpolation, and mark clarity
- Evidence: `documentation/gftools-qa/Proof/*SemiBold*-diffbrowsers_waterfall.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 7 SemiBold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - SemiBold waterfall: `documentation/arabic-review-snapshots/proof-semibold-waterfall.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_waterfall.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-text`

- Area/item: GF proof / Bold text
- Status: `pending`
- Review cue: Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence
- Evidence: `documentation/gftools-qa/Proof/*Bold*-diffbrowsers_text.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Bold text: `documentation/arabic-review-snapshots/proof-bold-text.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Bold-diffbrowsers_text.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-text REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-proofer`

- Area/item: GF proof / Bold proofer
- Status: `pending`
- Review cue: Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing
- Evidence: `documentation/gftools-qa/Proof/*Bold*-diffbrowsers_proofer.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 10 Bold Arabic samples; p. 11 Bold numerals and punctuation
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Bold proofer: `documentation/arabic-review-snapshots/proof-bold-proofer.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Bold-diffbrowsers_proofer.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-proofer REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-waterfall`

- Area/item: GF proof / Bold waterfall
- Status: `pending`
- Review cue: Waterfall: small-size behavior, interpolation, and mark clarity
- Evidence: `documentation/gftools-qa/Proof/*Bold*-diffbrowsers_waterfall.html`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Bold waterfall: `documentation/arabic-review-snapshots/proof-bold-waterfall.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html`
- Matching proof files:
  - `documentation/gftools-qa/Proof/Bold-diffbrowsers_waterfall.html`
- Machine precheck:
  - Matching proof files present: 1
  - Visual proof comparison still requires hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-waterfall REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## Smoke Strings And Classes

### `smoke-salaam`

- Area/item: Smoke string / salaam
- Status: `pending`
- Review cue: contextual forms and lam-alef behavior look intentional
- Evidence: `documentation/arabic-shaping-smoke-test.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-salaam.png` from `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Shaping smoke mechanical pass: yes
  - Visual rhythm and style still require hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=smoke-salaam REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `smoke-arabic`

- Area/item: Smoke string / arabic
- Status: `pending`
- Review cue: initial, medial, and final joins are shaped and spaced coherently
- Evidence: `documentation/arabic-shaping-smoke-test.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-arabic.png` from `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Shaping smoke mechanical pass: yes
  - Visual rhythm and style still require hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=smoke-arabic REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `smoke-bismillah`

- Area/item: Smoke string / bismillah
- Status: `pending`
- Review cue: word spacing, medial joins, heh, and meem forms hold together
- Evidence: `documentation/arabic-shaping-smoke-test.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-bismillah.png` from `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Shaping smoke mechanical pass: yes
  - Visual rhythm and style still require hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=smoke-bismillah REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `smoke-lam-alef`

- Area/item: Smoke string / lam-alef
- Status: `pending`
- Review cue: lam-alef ligature is present and weight-compatible
- Evidence: `documentation/arabic-shaping-smoke-test.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/smoke-lam-alef.png` from `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Shaping smoke mechanical pass: yes
  - Visual rhythm and style still require hand review.
- Edit targets: Source targets: 0 existing, 0 missing
  - Record exact glyph names in the review log if this row becomes `fix-needed`.

```bash
make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=smoke-lam-alef REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-arabic-farsi-numerals`

- Area/item: Glyph class / arabic-farsi-numerals
- Status: `pending`
- Review cue: U+0660-U+0669 and U+06F0-U+06F9 rhythm, width, and style fit
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 2 Regular numerals; p. 5 Medium numerals; p. 8 SemiBold numerals; p. 11 Bold numerals
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/class-arabic-farsi-numerals.png` from `documentation/arabic-manual-review-dashboard.html`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 4
  - Contour decisions marked fix-now: 0
- Edit targets: Source targets: 40 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/zero-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/zero-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/one-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/one-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 36

```bash
make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-arabic-farsi-numerals REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-arabic-punctuation`

- Area/item: Glyph class / arabic-punctuation
- Status: `pending`
- Review cue: Arabic comma, semicolon, question mark, per mille, date separator, full stop, and parentheses
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 2 Regular punctuation; p. 5 Medium punctuation; p. 8 SemiBold punctuation; p. 11 Bold punctuation
  - Page map: `documentation/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic manual dashboard: `documentation/arabic-review-snapshots/class-arabic-punctuation.png` from `documentation/arabic-manual-review-dashboard.html`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 4
  - Contour decisions marked fix-now: 0
- Edit targets: Source targets: 32 existing, 0 missing
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/comma-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/comma-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/semicolon-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/semicolon-ar.glif`
  - Additional GLIF targets in `documentation/arabic-manual-edit-targets.md`: 28

```bash
make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-arabic-punctuation REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```
