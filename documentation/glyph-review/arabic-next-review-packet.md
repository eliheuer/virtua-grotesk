# Arabic Next Review Packet

This generated packet is the smallest current hand-review batch. It is
derived from `documentation/glyph-review/arabic-visual-review-log.md` and should be
regenerated after recording outcomes.

- Pending or fix-needed rows: 32
- Full runbook: `documentation/glyph-review/arabic-visual-review-runbook.md`
- Dashboard: `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Focused Arabic PDF proof: `documentation/glyph-review/arabic-print-proof.pdf`
- Focused Arabic PDF index: `documentation/glyph-review/arabic-print-proof-index.md`
- Focused HTML: `documentation/glyph-review/arabic-next-review-batch.html`
- AI-safe triage: run `make arabic-next-review-ai-triage`
- AI visual observations: run `make arabic-next-review-ai-observations`
- Local review board: run `make arabic-next-review-board`
- Optional PNG snapshots: run `make arabic-next-review-snapshots`
- Optional full-queue PNG snapshot probe: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --timeout 20"`
- Optional full-queue snapshot coverage check without Chrome: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --list-only --timeout 20"`
- Optional rebuild from existing PNGs: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --reuse-existing"`

## Fast Review Order

1. Open `documentation/glyph-review/arabic-print-proof.pdf` and scan the current
   five-row batch across Regular, Medium, SemiBold, and Bold.
2. Use `documentation/glyph-review/arabic-print-proof-index.md` to jump directly
   to the style and section you are reviewing.
3. Use the linked HTML/source evidence below for any row that looks
   missing, clipped, malformed, duplicated, wrong-codepoint, or
   stylistically inconsistent.
4. Record one guarded status command per row only after checking the
   evidence. The PDF speeds review; it does not replace source/proof
   inspection for final approval.

## Next Rows

| Order | Key | Item | Status |
| ---: | --- | --- | --- |
| 1 | `proof-regular-glyphs` | Regular glyphs | pending |
| 2 | `proof-medium-glyphs` | Medium glyphs | pending |
| 3 | `proof-semibold-glyphs` | SemiBold glyphs | pending |
| 4 | `proof-bold-glyphs` | Bold glyphs | pending |
| 5 | `class-letter-structures` | letter-structures | pending |

## Shared Structure Prompt Details

- Grouped structure prompts:
  - Use these collapsed codepoint questions before recording an outcome; they are not automatic approval.
  - `U+062B ARABIC LETTER THEH` / `uni062B`: Check dot stack height and left overhang in glyph proofs before spacing edits.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `theh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`; `VirtuaGrotesk-Bold.ufo` `theh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
  - `U+062C ARABIC LETTER JEEM` / `uni062C`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `jeem-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/jeem-ar.glif`; `VirtuaGrotesk-Bold.ufo` `jeem-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
  - `U+062D ARABIC LETTER HAH` / `uni062D`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `hah-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/hah-ar.glif`; `VirtuaGrotesk-Bold.ufo` `hah-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/hah-ar.glif`
  - `U+062E ARABIC LETTER KHAH` / `uni062E`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `khah-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/khah-ar.glif`; `VirtuaGrotesk-Bold.ufo` `khah-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/khah-ar.glif`
  - `U+0633 ARABIC LETTER SEEN` / `uni0633`: Check whether the left overhang is intentional joining-script rhythm across all weights.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`; `VirtuaGrotesk-Bold.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `U+0634 ARABIC LETTER SHEEN` / `uni0634`: Check whether the left overhang is intentional joining-script rhythm across all weights.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`; `VirtuaGrotesk-Bold.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `U+0639 ARABIC LETTER AIN` / `uni0639`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `ain-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/ain-ar.glif`; `VirtuaGrotesk-Bold.ufo` `ain-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/ain-ar.glif`
  - `U+063A ARABIC LETTER GHAIN` / `uni063A`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `ghain-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/ghain-ar.glif`; `VirtuaGrotesk-Bold.ufo` `ghain-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/ghain-ar.glif`
  - `U+0645 ARABIC LETTER MEEM` / `uni0645`: Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `meem-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/meem-ar.glif`; `VirtuaGrotesk-Bold.ufo` `meem-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/meem-ar.glif`
  - `U+0648 ARABIC LETTER WAW` / `uni0648`: Check descending bowl and left overhang against adjacent text samples.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`; `VirtuaGrotesk-Bold.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
  - `U+0651 ARABIC SHADDA` / `uni0651`: Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `shadda-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shadda-ar.glif`; `VirtuaGrotesk-Bold.ufo` `shadda-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shadda-ar.glif`
  - `U+0653 ARABIC MADDAH ABOVE` / `uni0653`: Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `madda-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`; `VirtuaGrotesk-Bold.ufo` `madda-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
  - `U+0654 ARABIC HAMZA ABOVE` / `uni0654`: Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `hamzaabove-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`; `VirtuaGrotesk-Bold.ufo` `hamzaabove-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
  - `U+0655 ARABIC HAMZA BELOW` / `uni0655`: Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `hamzabelow-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`; `VirtuaGrotesk-Bold.ufo` `hamzabelow-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`

## 1. `proof-regular-glyphs`

- Area: GF proof
- Item: Regular glyphs
- Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 3 Regular cmap grid
  - Page map: `documentation/glyph-review/arabic-print-proof-index.md`
- Snapshot aids:
  - Regular glyphs: `documentation/glyph-review/review-snapshots/proof-regular-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
  - Regular Arabic glyph rows focused 2x crop: `documentation/glyph-review/review-snapshots/proof-regular-glyphs-arabic-zoom.png` from `documentation/glyph-review/review-snapshots/proof-regular-glyphs.png`
- Focused review pages:
  - `documentation/glyph-review/arabic-structure-sweep.html`
  - `documentation/glyph-review/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/google-fonts/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-regular-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

## 2. `proof-medium-glyphs`

- Area: GF proof
- Item: Medium glyphs
- Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 6 Medium cmap grid
  - Page map: `documentation/glyph-review/arabic-print-proof-index.md`
- Snapshot aids:
  - Medium glyphs: `documentation/glyph-review/review-snapshots/proof-medium-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
  - Medium Arabic glyph rows focused 2x crop: `documentation/glyph-review/review-snapshots/proof-medium-glyphs-arabic-zoom.png` from `documentation/glyph-review/review-snapshots/proof-medium-glyphs.png`
- Focused review pages:
  - `documentation/glyph-review/arabic-structure-sweep.html`
  - `documentation/glyph-review/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/google-fonts/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-medium-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

## 3. `proof-semibold-glyphs`

- Area: GF proof
- Item: SemiBold glyphs
- Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/google-fonts/gftools-qa/Proof/*SemiBold*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 9 SemiBold cmap grid
  - Page map: `documentation/glyph-review/arabic-print-proof-index.md`
- Snapshot aids:
  - SemiBold glyphs: `documentation/glyph-review/review-snapshots/proof-semibold-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
  - SemiBold Arabic glyph rows focused 2x crop: `documentation/glyph-review/review-snapshots/proof-semibold-glyphs-arabic-zoom.png` from `documentation/glyph-review/review-snapshots/proof-semibold-glyphs.png`
- Focused review pages:
  - `documentation/glyph-review/arabic-structure-sweep.html`
  - `documentation/glyph-review/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/google-fonts/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-semibold-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

## 4. `proof-bold-glyphs`

- Area: GF proof
- Item: Bold glyphs
- Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
- Evidence: `documentation/google-fonts/gftools-qa/Proof/*Bold*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Arabic print proof pages: p. 12 Bold cmap grid
  - Page map: `documentation/glyph-review/arabic-print-proof-index.md`
- Snapshot aids:
  - Bold glyphs: `documentation/glyph-review/review-snapshots/proof-bold-glyphs.png` from `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
  - Bold Arabic glyph rows focused 2x crop: `documentation/glyph-review/review-snapshots/proof-bold-glyphs-arabic-zoom.png` from `documentation/glyph-review/review-snapshots/proof-bold-glyphs.png`
- Focused review pages:
  - `documentation/glyph-review/arabic-structure-sweep.html`
  - `documentation/glyph-review/arabic-structure-triage.md`
- Matching proof files:
  - `documentation/google-fonts/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`
- Machine precheck:
  - Structure triage mechanical blockers: 0
  - Structure triage review prompts: 66

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-bold-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

## 5. `class-letter-structures`

- Area: Glyph class
- Item: letter-structures
- Cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof
- Evidence: `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`; `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`; `documentation/glyph-review/arabic-manual-review-dashboard.html`; `documentation/glyph-review/arabic-visual-risk-proof.html`
- Arabic print proof pages: p. 3 Regular cmap grid; p. 6 Medium cmap grid; p. 9 SemiBold cmap grid; p. 12 Bold cmap grid; p. 1 Regular Arabic samples; p. 4 Medium Arabic samples; p. 7 SemiBold Arabic samples; p. 10 Bold Arabic samples
  - Page map: `documentation/glyph-review/arabic-print-proof-index.md`
- Snapshot aids:
  - Arabic structure sweep: `documentation/glyph-review/review-snapshots/class-letter-structures.png` from `documentation/glyph-review/arabic-structure-sweep.html`
  - Arabic visual risk proof: `documentation/glyph-review/review-snapshots/class-letter-structures-2.png` from `documentation/glyph-review/arabic-visual-risk-proof.html`
- Focused review pages:
  - `documentation/glyph-review/arabic-structure-sweep.html`
  - `documentation/glyph-review/arabic-structure-triage.md`
- Dashboard: `documentation/glyph-review/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 4
  - Contour decisions marked fix-now: 0

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `class-letter-structures` against the listed evidence. Focus on: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.
