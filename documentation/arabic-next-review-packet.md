# Arabic Next Review Packet

This generated packet is the smallest current hand-review batch. It is
derived from `documentation/arabic-visual-review-log.md` and should be
regenerated after recording outcomes.

- Pending or fix-needed rows: 32
- Full runbook: `documentation/arabic-visual-review-runbook.md`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Focused Arabic PDF proof: `documentation/arabic-print-proof.pdf`
- Focused HTML: `documentation/arabic-next-review-batch.html`
- AI-safe triage: run `make arabic-next-review-ai-triage`
- AI visual observations: run `make arabic-next-review-ai-observations`
- Local review board: run `make arabic-next-review-board`
- Optional PNG snapshots: run `make arabic-next-review-snapshots`
- Optional full-queue PNG snapshot probe: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --timeout 20"`
- Optional full-queue snapshot coverage check without Chrome: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --list-only --timeout 20"`
- Optional rebuild from existing PNGs: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --reuse-existing"`

## Fast Review Order

1. Open `documentation/arabic-print-proof.pdf` and scan the current
   five-row batch across Regular, Medium, SemiBold, and Bold.
2. Use the linked HTML/source evidence below for any row that looks
   missing, clipped, malformed, duplicated, wrong-codepoint, or
   stylistically inconsistent.
3. Record one guarded status command per row only after checking the
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
  - `U+0633 ARABIC LETTER SEEN` / `uni0633`: Check whether the left overhang is intentional joining-script rhythm across all weights.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`; `VirtuaGrotesk-Bold.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
  - `U+0634 ARABIC LETTER SHEEN` / `uni0634`: Check whether the left overhang is intentional joining-script rhythm across all weights.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`; `VirtuaGrotesk-Bold.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
  - `U+0648 ARABIC LETTER WAW` / `uni0648`: Check descending bowl and left overhang against adjacent text samples.
    - Source edit targets: `VirtuaGrotesk-Regular.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`; `VirtuaGrotesk-Bold.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
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
- Evidence: `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
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
  - Structure triage review prompts: 35

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
- Evidence: `documentation/gftools-qa/Proof/*Medium*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
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
  - Structure triage review prompts: 35

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
- Evidence: `documentation/gftools-qa/Proof/*SemiBold*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
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
  - Structure triage review prompts: 35

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
- Evidence: `documentation/gftools-qa/Proof/*Bold*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`
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
  - Structure triage review prompts: 35

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
- Evidence: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-visual-risk-proof.html`
- Snapshot aids:
  - Arabic structure sweep: `documentation/arabic-review-snapshots/class-letter-structures.png` from `documentation/arabic-structure-sweep.html`
  - Arabic visual risk proof: `documentation/arabic-review-snapshots/class-letter-structures-2.png` from `documentation/arabic-visual-risk-proof.html`
- Focused review pages:
  - `documentation/arabic-structure-sweep.html`
  - `documentation/arabic-structure-triage.md`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Machine precheck:
  - Contour decisions pending: 0
  - Contour decisions marked fix-now: 0

Record the review result:

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `class-letter-structures` against the listed evidence. Focus on: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.
