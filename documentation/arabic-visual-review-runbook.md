# Arabic Visual Review Runbook

This generated runbook turns `documentation/arabic-visual-review-log.md`
into row-by-row review cards. It does not approve drawings; it makes the
remaining human review faster and easier to record.

## Summary

- Review rows: 32
- Pending or fix-needed: 32
- Deferred: 0
- Pass: 0
- Focused next-batch page: `documentation/arabic-next-review-batch.html`
- Dashboard: `documentation/arabic-manual-review-dashboard.html`
- Snapshot report: `documentation/arabic-next-review-snapshots.md`
- Focused zoom snapshot report: `documentation/arabic-first-review-zoom-snapshots.md`
- Snapshot integrity: `documentation/arabic-snapshot-integrity.md`
- Batch order: `documentation/arabic-manual-review-batches.md`

## Next Five Review Cards

### 1. `proof-regular-glyphs`

- Area: GF proof
- Item: Regular glyphs
- Current status: pending
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

Record one outcome:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed evidence"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific issue to fix"
make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-regular-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

### 2. `proof-medium-glyphs`

- Area: GF proof
- Item: Medium glyphs
- Current status: pending
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

Record one outcome:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed evidence"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific issue to fix"
make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-medium-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

### 3. `proof-semibold-glyphs`

- Area: GF proof
- Item: SemiBold glyphs
- Current status: pending
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

Record one outcome:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed evidence"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific issue to fix"
make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-semibold-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

### 4. `proof-bold-glyphs`

- Area: GF proof
- Item: Bold glyphs
- Current status: pending
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

Record one outcome:

```bash
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed evidence"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific issue to fix"
make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `proof-bold-glyphs` against the listed evidence. Focus on: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

### 5. `class-letter-structures`

- Area: Glyph class
- Item: letter-structures
- Current status: pending
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

Record one outcome:

```bash
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed evidence"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific issue to fix"
make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"
```

AI comparison prompt:

> Compare the current Virtua Grotesk Arabic rendering for `class-letter-structures` against the listed evidence. Focus on: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof. Classify the row as pass, fix-needed, or deferred. If fix-needed, name the specific source glyphs or proof locations to inspect; do not suggest copying outlines from reference fonts.

## Mark Review Prompt Summary

The current mark triage has no mechanical blockers. Its remaining
zero-offset prompts are visual proof checks, not automatic failures.

| Review row | Font | Samples | Sample texts |
| --- | --- | ---: | --- |
| `mark-shadda+sukun` | Bold | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Medium | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Regular | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | SemiBold | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Variable | 2 | `بُّ`, `بَّ` |

## Mark Review Source Targets

Use these rows when a no-offset mark sample needs editing. The target
list includes both masters so compatibility can be preserved.

| Review row | Font | Sample | Glyph sequence | Source edit targets |
| --- | --- | --- | --- | --- |
| `mark-shadda+sukun` | Bold | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Bold | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Medium | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Medium | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Regular | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Regular | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | SemiBold | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | SemiBold | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Variable | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Variable | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |

## Full Pending Queue

| Key | Area | Item | Status | Machine precheck | Review cue |
| --- | --- | --- | --- | --- | --- |
| `proof-regular-glyphs` | GF proof | Regular glyphs | pending | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-medium-glyphs` | GF proof | Medium glyphs | pending | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-semibold-glyphs` | GF proof | SemiBold glyphs | pending | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `proof-bold-glyphs` | GF proof | Bold glyphs | pending | Structure triage mechanical blockers: 0<br>Structure triage review prompts: 66 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| `class-letter-structures` | Glyph class | letter-structures | pending | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof |
| `mark-base+fatha` | Mark attachment | base+fatha | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | top mark position clears the base and matches style |
| `mark-base+damma` | Mark attachment | base+damma | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | damma position and scale are readable across weights |
| `mark-base+kasra` | Mark attachment | base+kasra | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | bottom mark position clears descenders and sidebearings |
| `mark-shadda+sukun` | Mark attachment | shadda+sukun | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | stacked top marks remain clear and centered |
| `mark-tanween` | Mark attachment | tanween | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | tanween combinations remain clear and aligned |
| `mark-hamza-above-below` | Mark attachment | hamza-above-below | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | hamza combinations attach cleanly above and below |
| `mark-dotted-circle` | Mark attachment | dotted-circle | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | dotted circle with top and bottom marks is readable |
| `class-mark-combinations` | Glyph class | mark-combinations | pending | Mark triage mechanical blockers: 0<br>Mark triage no-offset prompts: 10 | shadda, hamza, tanween, sukun, and kasra composites |
| `class-dot-stack-helpers` | Glyph class | dot-stack-helpers | pending | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | three-dot and six-dot Persian/Urdu helpers |
| `proof-regular-text` | GF proof | Regular text | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence |
| `proof-regular-proofer` | GF proof | Regular proofer | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing |
| `proof-regular-waterfall` | GF proof | Regular waterfall | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Waterfall: small-size behavior, interpolation, and mark clarity |
| `proof-medium-text` | GF proof | Medium text | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence |
| `proof-medium-proofer` | GF proof | Medium proofer | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing |
| `proof-medium-waterfall` | GF proof | Medium waterfall | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Waterfall: small-size behavior, interpolation, and mark clarity |
| `proof-semibold-text` | GF proof | SemiBold text | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence |
| `proof-semibold-proofer` | GF proof | SemiBold proofer | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing |
| `proof-semibold-waterfall` | GF proof | SemiBold waterfall | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Waterfall: small-size behavior, interpolation, and mark clarity |
| `proof-bold-text` | GF proof | Bold text | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence |
| `proof-bold-proofer` | GF proof | Bold proofer | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing |
| `proof-bold-waterfall` | GF proof | Bold waterfall | pending | Matching proof files present: 1<br>Visual proof comparison still requires hand review. | Waterfall: small-size behavior, interpolation, and mark clarity |
| `smoke-salaam` | Smoke string | salaam | pending | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | contextual forms and lam-alef behavior look intentional |
| `smoke-arabic` | Smoke string | arabic | pending | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | initial, medial, and final joins are shaped and spaced coherently |
| `smoke-bismillah` | Smoke string | bismillah | pending | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | word spacing, medial joins, heh, and meem forms hold together |
| `smoke-lam-alef` | Smoke string | lam-alef | pending | Shaping smoke mechanical pass: yes<br>Visual rhythm and style still require hand review. | lam-alef ligature is present and weight-compatible |
| `class-arabic-farsi-numerals` | Glyph class | arabic-farsi-numerals | pending | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | U+0660-U+0669 and U+06F0-U+06F9 rhythm, width, and style fit |
| `class-arabic-punctuation` | Glyph class | arabic-punctuation | pending | Contour decisions pending: 4<br>Contour decisions marked fix-now: 0 | Arabic comma, semicolon, question mark, per mille, date separator, full stop, and parentheses |
