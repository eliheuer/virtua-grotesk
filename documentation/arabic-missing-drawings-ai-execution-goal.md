# Virtua Grotesk Arabic Missing Drawings AI Execution Goal

Date: 2026-05-25

## Goal

Finish the missing Arabic drawings needed for the Google Fonts submission as quickly as possible without losing the Virtua Grotesk drawing style or breaking variable-font master compatibility.

The practical target is not to train a production font model. The target is to build an AI-assisted and script-assisted candidate workflow that gets every missing glyph into both UFO masters, then leaves a focused manual cleanup pass for drawing quality, spacing, anchors, and proof review.

## Current Baseline

Primary repo: `/Users/eli/GH/repos/virtua-grotesk`

Authoritative local reports:

- `documentation/arabic-source-work-checklist.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/arabic-review-packet.md`
- `documentation/arabic-mark-readiness.md`
- `documentation/master-compatibility.md`
- `documentation/manual-cleanup-handoff.md`

Current Arabic coverage state:

- Minimum Arabic target: `GF_Arabic_Core`
- Required Arabic Core codepoints: 224
- Present Arabic Core codepoints: 167
- Missing Arabic Core codepoints: 57
- Suggested source glyph names: 88
- Suggested Arabic source glyph names: 60
- Suggested shared punctuation/symbol glyph names: 28
- Positional-form glyph names: 31
- Suggested glyph names missing in both masters: 88
- Arabic reuse prerequisites checked: 13
- Missing reuse prerequisites across masters: 0
- U+25CC dotted circle missing: yes
- Required mark glyphs present: 13 / 16
- Source anchors present: no
- Built `mark`/`mkmk` GPOS features present: no
- Master compatibility report currently has no blocking structure mismatch.

## Strategy

Use a hybrid production workflow:

1. Script-generate candidate glyphs from existing Virtua Arabic sources.
2. Use OFL Arabic fonts such as Rubik only as visual/reference overlays, not as the first source of copied outlines.
3. Use AI where it helps accelerate comparison, naming, batching, and candidate review.
4. Keep all production outlines UFO-native and manually inspectable.
5. Preserve interpolation compatibility between Regular and Bold at every step.

This is likely faster and safer than post-training a font-generation model. The missing work is narrow enough that a deterministic candidate builder plus proof review should beat model training or finetuning.

## What Not To Do

- Do not directly copy Rubik or another OFL font into Virtua as the main approach unless provenance and design-fit notes are recorded per glyph.
- Do not rely on HuggingFace/font-generation output as final source outlines.
- Do not generate one master only and try to repair compatibility later.
- Do not add Arabic codepoints without checking positional forms, shaping, marks, anchors, and proof strings.
- Do not treat cmap coverage as completion.

## Candidate Builder Plan

Create a helper script:

`scripts/build_arabic_candidate_glyphs.py`

Expected behavior:

- Read `documentation/arabic-source-work-checklist.md` or an equivalent structured mapping.
- Open both active UFO masters:
  - `sources/VirtuaGrotesk-Regular.ufo`
  - `sources/VirtuaGrotesk-Bold.ufo`
- For every missing glyph, create the same glyph name in both masters.
- Assign Unicode values for encoded default glyphs.
- Copy compatible base skeletons where reuse prerequisites already exist.
- Compose dot/mark variants from existing Virtua dot helpers where possible.
- Create default, final, initial, and medial forms in matching master structure.
- Preserve glyph order where practical.
- Output a report listing:
  - auto-created glyphs,
  - glyphs using existing Virtua bases,
  - glyphs needing hand drawing,
  - glyphs needing Arabic shaping review,
  - glyphs needing anchor/mark review,
  - any master-compatibility risks.

Candidate script should start in dry-run mode by default.

Suggested CLI:

```bash
./venv/bin/python scripts/build_arabic_candidate_glyphs.py --dry-run
./venv/bin/python scripts/build_arabic_candidate_glyphs.py --write
make reports-only
make preflight-only
```

## Reference Font Workflow

Use reference fonts for overlays and shape checks.

Good candidates:

- Rubik Arabic sources from `googlefonts/rubik`
- Other Google Fonts Arabic families with OFL sources and current upstream history
- Existing Google Fonts downstream Arabic packages for metadata/proof expectations

Reference use:

- Convert reference font sources to UFO only in a separate scratch/reference folder.
- Never mix reference UFOs into production sources without a written decision.
- Generate overlay proofs against Virtua candidates.
- Use overlays to answer proportions and form questions:
  - Urdu/Persian joining behavior
  - positional form expectations
  - dot placement norms
  - Arabic/Farsi digit rhythm
  - punctuation directionality and spacing

Reference output folder suggestion:

`scratch/arabic-reference-overlays/`

Keep scratch/reference artifacts out of final packaging unless deliberately documented.

## AI-Assisted Workflow

Use AI for acceleration around the drawing process, not as the final source of truth.

Useful AI tasks:

- Turn the Arabic worklist into batch tickets.
- Suggest source-glyph reuse mappings from existing Virtua glyphs.
- Compare candidate proofs against reference overlays and flag likely issues.
- Generate review checklists for each batch.
- Summarize remaining blockers after each preflight.
- Help write anchor/mark test strings and proof strings.

Risky AI tasks:

- Generating final Arabic outlines directly.
- Guessing OpenType shaping behavior without HarfBuzz/gftools proof evidence.
- Finetuning a glyph-generation model for only this missing set.

Model/post-training research stance:

- Current public glyph-generation research is interesting but not mature enough for this immediate production deadline.
- Training data preparation, contour cleanup, compatibility repair, and QA would likely take longer than scripted candidate generation.
- Revisit post-training only after this submission, using Virtua as a controlled experiment.

## Batch Execution Plan

### Batch 1: Shared Punctuation And Symbols

Scope: 28 glyphs.

Why first:

- Helps both Latin Core and Arabic Core coverage.
- Mostly standalone drawings.
- Lower shaping risk.

Source glyphs:

`Euro`, `asciicircum`, `asciitilde`, `at`, `bar`, `braceleft`, `braceright`, `bracketleft`, `bracketright`, `cent`, `copyright`, `degree`, `divide`, `dottedCircle`, `equal`, `grave`, `greater`, `guillemotleft`, `guillemotright`, `guilsinglleft`, `guilsinglright`, `less`, `multiply`, `plus`, `registered`, `sterling`, `trademark`, `yen`

Done when:

- Glyphs exist in both masters.
- Widths are reviewed.
- Dotted circle is usable for mark proofing.
- `make preflight-only` shows reduced shared punctuation gaps.

### Batch 2: Extended Arabic-Indic Digits

Scope: 10 glyphs.

Source glyphs:

`zeroFarsi-ar`, `oneFarsi-ar`, `twoFarsi-ar`, `threeFarsi-ar`, `fourFarsi-ar`, `fiveFarsi-ar`, `sixFarsi-ar`, `sevenFarsi-ar`, `eightFarsi-ar`, `nineFarsi-ar`

Done when:

- Digits exist in both masters.
- Numeral rhythm is proofed against Arabic samples.
- Widths are intentionally proportional or intentionally matched to existing digit strategy.

### Batch 3: Urdu/Persian Joining Letters

Scope: 13 encoded letters, 44 source glyphs including positional forms.

Source glyph families:

`tteh-ar`, `peh-ar`, `tcheh-ar`, `ddal-ar`, `rreh-ar`, `jeh-ar`, `keheh-ar`, `gaf-ar`, `hehDoachashmee-ar`, `hehGoal-ar`, `farsiYeh-ar`, `yehBarree-ar`, `kehehThreedotsabove-ar`

Done when:

- Default and required positional forms exist in both masters.
- Existing Virtua Arabic bases are reused where the checklist says prerequisites are ready.
- Arabic shaping smoke test still passes.
- Proof strings show no `.notdef` for target words.
- Manual review confirms the forms fit Virtua’s geometric/chamfered style.

### Batch 4: Arabic Punctuation And Symbols

Scope: 3 glyphs.

Source glyphs:

`perMille-ar`, `dateSeparator-ar`, `fullStop-ar`

Done when:

- Glyphs exist in both masters.
- Directionality and spacing are proofed in Arabic text.
- Glyphs are not overfit to Latin punctuation rhythm.

### Batch 5: Arabic Marks, Anchors, And Mark Features

Scope:

- Missing marks: `smallHighTah-ar`, `noonGhunna-ar`, `smallHighThreeDots-ar`
- Dotted circle review
- Source anchors
- Built `mark`/`mkmk` GPOS features

Done when:

- Required marks exist in both masters.
- Dotted circle exists and attaches marks.
- Anchors exist on relevant bases and marks.
- Built fonts expose expected mark positioning behavior.
- Fontspector dotted-circle and mark-related warnings are resolved or explicitly documented.

## Verification Loop

Run after each batch:

```bash
./build.sh
make reports-only
make preflight-only
```

Run after Arabic shaping-sensitive batches:

```bash
make preflight
make kerning-proof-check
make kerning-proof-review-check
```

Final Arabic drawing gate:

```bash
make preflight
make test
make kerning-proof-check
make kerning-proof-review-check
```

Review these files after each pass:

- `documentation/gf-glyphset-readiness.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/arabic-source-work-checklist.md`
- `documentation/arabic-review-packet.md`
- `documentation/arabic-mark-readiness.md`
- `documentation/master-compatibility.md`
- `documentation/fontspector-googlefonts-report.md`
- `documentation/gftools-qa/`

## Manual Review Checklist

For every new Arabic glyph:

- Exists in Regular and Bold.
- Same contour/component structure in both masters.
- Unicode assigned only to encoded default glyphs.
- Positional forms are unencoded unless the current source convention requires otherwise.
- Advance width is intentional.
- Sidebearings are proofed in Arabic strings.
- Dot and mark placement follows existing Virtua Arabic rhythm.
- Chamfer logic matches the 16-unit, 45-degree design language where applicable.
- Curves are smooth and not imported-looking.
- No accidental reference-font style leaks.
- No generated helper glyph is unreachable unless deliberately kept.

## Success Criteria

The goal is complete when:

- GF Arabic Core missing codepoints: 0, or every remaining exception is explicitly reviewer-approved.
- Suggested Arabic source glyphs are present in both active masters or deliberately removed from scope.
- Arabic shaping smoke test passes.
- Dotted circle, required marks, anchors, and mark/mkmk status are ready or explicitly documented.
- `make preflight` passes with no undocumented drawing/source blockers.
- `make test` is ready for final Fontspector review.
- `gftools qa --proof` output has been regenerated and reviewed.
- The final state is recorded in `documentation/manual-cleanup-handoff.md`, `documentation/next-actions.md`, and the reusable `.agents/` Google Fonts onboarding material if the workflow teaches something portable.

## Immediate Next Actions

1. Create the candidate builder script in dry-run mode.
2. Generate a structured auto/review/manual split for the 88 source glyph names.
3. Start with Batch 1 because it is low-risk and improves both Latin and Arabic coverage.
4. Use one reference Arabic font as an overlay source before touching Batch 3.
5. After Batch 1 and Batch 2, pause for proof review before generating joining forms.

