# Arabic First Review Batch

This generated worksheet flattens the next Arabic hand-review batch into
one short session. It is a review aid only: open the proof/source evidence
before recording any `pass`, and use `fix-needed` only with exact glyphs,
proof locations, or source files.

## Batch Goal

Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint
Arabic glyphs before judging spacing, rhythm, marks, or kerning.

## Batch State

- Review rows: 5
- Status counts: `pending`: 5
- Main proof directory: `documentation/gftools-qa/Proof/`
- Structure triage: `documentation/arabic-structure-triage.md`
- Visual-risk proof: `documentation/arabic-visual-risk-proof.html`
- Edit-target source: `documentation/arabic-manual-edit-targets.md`
- AI visual sweep notes: `documentation/arabic-first-review-ai-sweep.md`
- Focused zoom crops: `documentation/arabic-first-review-zoom-snapshots.md`
- Focused crop integrity: `documentation/arabic-first-review-crop-integrity.md`
- AI-visible risk shortlist: `documentation/arabic-first-review-risk-shortlist.md`

## Shared High-Risk Prompts

- `U+062B THEH`: dot stack height and left overhang.
- `U+0633 SEEN` / `U+0634 SHEEN`: left overhang in shaped RTL context.
- `U+0648 WAW`: descending bowl and left overhang in adjacent text.
- `U+0653`, `U+0654`, `U+0655`: expected zero-advance mark overhang; inspect attachment and dotted-circle clarity.

Additional structure-triage prompts:

- `U+062B ARABIC LETTER THEH`: Check dot stack height and left overhang in glyph proofs before spacing edits.
- `U+0633 ARABIC LETTER SEEN`: Check whether the left overhang is intentional joining-script rhythm across all weights.
- `U+0634 ARABIC LETTER SHEEN`: Check whether the left overhang is intentional joining-script rhythm across all weights.
- `U+0648 ARABIC LETTER WAW`: Check descending bowl and left overhang against adjacent text samples.

## Row Worksheet

### `proof-regular-glyphs`

- Area/item: GF proof / Regular glyphs
- Current status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Machine precheck: Structure triage mechanical blockers: 0; structure review prompts: 35
- Source targets: 14 existing, 0 missing
- Snapshot aids:
  - Regular glyphs: `documentation/arabic-review-snapshots/proof-regular-glyphs.png` from `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- Focused Arabic-row crop: `documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png`
- First source files to inspect if `fix-needed`:
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`

Record after proof/source review:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-medium-glyphs`

- Area/item: GF proof / Medium glyphs
- Current status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Machine precheck: Structure triage mechanical blockers: 0; structure review prompts: 35
- Source targets: 14 existing, 0 missing
- Snapshot aids:
  - Medium glyphs: `documentation/arabic-review-snapshots/proof-medium-glyphs.png` from `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- Focused Arabic-row crop: `documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png`
- First source files to inspect if `fix-needed`:
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`

Record after proof/source review:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-semibold-glyphs`

- Area/item: GF proof / SemiBold glyphs
- Current status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Machine precheck: Structure triage mechanical blockers: 0; structure review prompts: 35
- Source targets: 14 existing, 0 missing
- Snapshot aids:
  - SemiBold glyphs: `documentation/arabic-review-snapshots/proof-semibold-glyphs.png` from `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- Focused Arabic-row crop: `documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png`
- First source files to inspect if `fix-needed`:
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`

Record after proof/source review:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `proof-bold-glyphs`

- Area/item: GF proof / Bold glyphs
- Current status: `pending`
- Review cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Machine precheck: Structure triage mechanical blockers: 0; structure review prompts: 35
- Source targets: 14 existing, 0 missing
- Snapshot aids:
  - Bold glyphs: `documentation/arabic-review-snapshots/proof-bold-glyphs.png` from `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
- Focused Arabic-row crop: `documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png`
- First source files to inspect if `fix-needed`:
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`

Record after proof/source review:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

### `class-letter-structures`

- Area/item: Glyph class / letter-structures
- Current status: `pending`
- Review cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof
- Machine precheck: Contour decisions pending: 0; fix-now: 0
- Source targets: 14 existing, 0 missing
- Snapshot aids:
  - Arabic structure sweep: `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`
  - Arabic visual risk proof: `documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html`
- First source files to inspect if `fix-needed`:
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
  - `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`

Record after proof/source review:

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

## After This Batch

If any row becomes `fix-needed`, edit Regular and Bold together, then run:

```bash
./build.sh
make reports-only
make preflight-only
```

If all five rows are passed or explicitly deferred, regenerate the
review reports and continue with the marks/dotted-circle batch.
