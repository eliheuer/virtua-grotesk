# Goal: AI-Assisted Arabic Drawing Finish

Finish Virtua Grotesk's Arabic drawings for Google Fonts submission with the fastest reliable workflow: generated candidates for coverage, AI-assisted review, and human cleanup for production quality.

## Current State

Repo: `/Users/eli/GH/repos/virtua-grotesk`

Candidate glyphs have been scaffolded in both masters and GF Arabic Core
coverage is now zero-missing by cmap. The candidate script is idempotent in
dry-run mode: all 256 worklist entries already exist in both masters, with
zero base-copy/geometric/hand-review candidates left to create and zero
compatibility-risk entries.

This does not mean the Arabic is production-finished. The remaining Arabic work
is human visual proofing, any source edits that review marks as `fix-needed`,
then a rebuild/report/preflight pass. Contour/no-contour cleanup is currently
closed in the generated decision log; do not reopen it unless new visual review
evidence identifies a real source drawing issue.

Track state in:

- `documentation/arabic-candidate-glyph-plan.md`
- `documentation/gf-glyphset-readiness.md`
- `documentation/arabic-review-packet.md`
- `documentation/arabic-mark-readiness.md`
- `documentation/arabic-visual-review-log.md`
- `documentation/arabic-next-review-packet.md`
- `documentation/arabic-visual-review-runbook.md`
- `documentation/arabic-manual-review-batches.md`
- `documentation/master-compatibility.md`
- `documentation/fontspector-zero-warning-worklist.md`
- `documentation/final-submission-blockers.md`

## Working Strategy

Use a hybrid process:

1. Keep candidate glyph generation deterministic with `scripts/build_arabic_candidate_glyphs.py`.
2. Use OFL Arabic fonts such as Rubik only as visual/reference overlays, not as final copied outlines.
3. Use AI for batching, reuse suggestions, proof comparison, and blocker summaries.
4. Manually clean final outlines, spacing, anchors, mark behavior, and shaping.

Training or finetuning a glyph model is likely slower than deterministic generation plus manual cleanup for this scope.

## Core Commands

```bash
make arabic-candidate-plan
./venv/bin/python scripts/build_arabic_candidate_glyphs.py --dry-run
./venv/bin/python scripts/build_arabic_candidate_glyphs.py --write
./build.sh
make reports-only
make preflight-only
```

For shaping-sensitive or final handoff work:

```bash
make preflight
make kerning-proof-check
make kerning-proof-review-check
make test
```

## Cleanup Order

Completed candidate-creation batches:

1. Shared punctuation/symbols.
2. Extended Arabic-Indic digits.
3. Urdu/Persian joining letters and their default/fina/init/medi forms.
4. Arabic punctuation: `perMille-ar`, `dateSeparator-ar`, `fullStop-ar`.
5. Arabic marks, dotted circle, anchors, `mark`, and `mkmk`.

Active cleanup order:

1. Open `documentation/arabic-manual-review-dashboard.html` and
   `documentation/arabic-next-review-batch.html` for the compact current proof
   queue.
2. Start with `documentation/arabic-next-review-packet.md`; it contains the
   smallest current hand-review batch, evidence links, source edit targets, and
   guarded update commands.
3. Work through `documentation/arabic-visual-review-runbook.md` in batch order
   when you need the full queue. Start with Regular/Medium/SemiBold/Bold glyph
   proofs and `class-letter-structures`.
4. For each reviewed row, record `pass`, `fix-needed`, or `deferred` in
   `documentation/arabic-visual-review-log.md` with
   `make arabic-visual-review-update`.
5. If a row is `fix-needed`, edit the source GLIFs named by the structure or
   mark source-target sections in the runbook, preserving Regular/Bold
   compatibility.
6. Rebuild and regenerate reports after each drawing batch:
   `./build.sh`, `make reports-only`, `make preflight-only`.

Current automated warning state:

- `make preflight-only` passes with only documented drawing/source blockers.
- Fontspector googlefonts profile still fails on `googlefonts/glyph_coverage`
  because GF Latin Core coverage is incomplete; the Arabic Core gap is closed.
- Package-context Fontspector warning floor is currently 2 after deferring
  `latin-ext` from the preview: one `googlefonts/metadata/subsets_correct`
  warning for the broad `arabic` subset threshold, plus one
  `googlefonts/metadata/unreachable_subsetting` warning for U+0237, U+200F,
  U+20B9, and U+25CC.
- Do not remove Arabic serving scope, U+200F, or U+25CC just to reduce warning
  count; `documentation/fontspector-metadata-warning-probe.md` documents why
  those shortcuts make the package less honest or introduce worse warnings.

## Done When

- GF Arabic Core gaps are zero or explicitly accepted.
- All required source glyphs exist in both masters.
- Regular and Bold structures stay compatible.
- Empty/placeholder candidate outlines are cleaned.
- Arabic shaping smoke tests pass.
- Dotted circle, marks, anchors, and `mark`/`mkmk` are ready or documented.
- `make preflight` has no undocumented drawing/source blockers.
- Human Arabic visual proof rows are all marked `pass` or explicitly
  `deferred` with reviewer notes.
- `make test` is ready for final Fontspector review, with any remaining Latin
  coverage or package-scope warnings intentionally documented.
