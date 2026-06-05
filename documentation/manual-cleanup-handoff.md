# Manual Cleanup Handoff

This is the pause point for finishing drawing/source work and hand cleanup
before the final Google Fonts package pass.

## Current State

- Full `make preflight` passes with only documented drawing/source blockers
  remaining after a fresh build, proof PDF generation, report regeneration, and
  `make preflight-only`.
- GF Arabic Core coverage is complete: 224 / 224 required codepoints present,
  with zero missing Arabic source glyphs in the generated worklist.
- Arabic shaping smoke tests pass in all 5 built fonts, required Arabic marks
  are present, dotted circle is present, source anchors are present, and built
  `mark`/`mkmk` GPOS features are present.
- The active UFOs are ready for hand cleanup: `make ufo-editor-check` reports
  both masters loadable with 489 glyphs, zero GLIF read errors, zero missing
  GLIF files, and zero duplicate GLIF filenames; `make runebender-ufo-check`
  also validates both active UFOs through Runebender/Norad loader dependencies.
- `make kerning-proof-check` has regenerated the Google Fonts QA proof output
  under `documentation/google-fonts/gftools-qa/Proof`; `make kerning-proof-review-check`
  confirms all 16 expected HTML proof files are present.
- Arabic PNG snapshot evidence is complete enough for hand review navigation:
  `documentation/glyph-review/arabic-snapshot-integrity.md` reports 32 pending/fix-needed
  review keys, 33 readable PNG files, 33 nonblank PNG files, zero missing
  snapshot rows, and zero integrity errors.
- Arabic source-structure checkpoints are ready for hand drawing:
  `documentation/glyph-review/arabic-first-batch-source-checkpoint.md` covers the current
  structure/wrong-glyph batch, and
  `documentation/glyph-review/arabic-pending-source-checkpoint.md` covers all unresolved
  review-row source targets with 68 unique glyph names, 136 paired source
  files, zero missing files, and zero Regular/Bold structure mismatches.
- Reusable Google Fonts onboarding knowledge has been captured in `.agents/`.
- The generated Add Font issue draft, downstream package preview, release
  archive plan, Packager dry-run gates, and downstream PR readiness reports are
  in place.
- The local `google/fonts` fork is synced and dirty only inside
  `ofl/virtuagrotesk`, where the current starter-only `METADATA.pb` remains
  quarantined until final metadata can be applied.

## Finish By Hand

Use `documentation/google-fonts/next-actions.md` as the main queue. The drawing/source
cleanup pass should focus on:

1. GF Latin Core coverage.
2. Human visual review of Arabic drawing quality, spacing, mark placement, and
   shaping behavior. Start with
   `documentation/glyph-review/arabic-manual-review-dashboard.html`, then use
   `documentation/google-fonts/gftools-qa/Proof`; use
   `documentation/glyph-review/arabic-current-review-worksheet.md` as the current fill-in
   sheet for observations and final status decisions, use
   `documentation/glyph-review/arabic-first-review-batch.md` as the shortest one-session
   structure/wrong-glyph worksheet, pair it with
   `documentation/glyph-review/arabic-first-review-ai-sweep.md` for AI snapshot observations
   that are not review decisions, use
   `documentation/glyph-review/arabic-full-queue-ai-sweep.md` when you want the same
   non-decision framing across all pending rows, use
   `documentation/glyph-review/arabic-hand-review-session.md` as the compact current
   session checklist, use
   `documentation/glyph-review/arabic-hand-review-contact-sheet.html` for a snapshot-first
   scan of the full queue, then use
   `documentation/glyph-review/arabic-visual-review-checklist.md` as the targeted Arabic
   review packet. Use `documentation/glyph-review/arabic-next-review-board.html` and
   `documentation/glyph-review/arabic-snapshot-integrity.md` for fast navigation, but open
   the linked proof/source HTML before recording a row outcome. Start the
   sidebearing pass with
   `documentation/glyph-review/arabic-visual-risk-proof.html`, which isolates the current
   risk rows for U+062B, U+0633, U+0634, and U+0648 across weights.
   If a row becomes `fix-needed`, use
   `documentation/glyph-review/arabic-manual-edit-targets.md` to jump to the exact Regular
   and Bold GLIF files; use
   `documentation/glyph-review/arabic-pending-source-checkpoint.md` to confirm the broader
   unresolved queue still has paired source files, and keep both masters
   structurally compatible.
3. Keep source contour/no-contour cleanup closed by regenerating the contour
   proof after any drawing edits; there are currently zero unresolved contour
   review rows.
4. PUA/reachability cleanup or an explicit keep/defer decision.
5. Kerning completion or explicit first-submission deferral.
6. Human review of the `gftools qa --proof` output.

## Current Contour Cleanup Map

Use `documentation/google-fonts/fontspector-contour-count.md` as the generated source of
truth. The current contour queue is closed: there are zero source glyph
findings, zero all-font rows, zero pending decisions, and zero `fix-now`
decisions. Treat the contour proof as a regression check after new drawing
edits, not as the current Arabic cleanup queue.

Regenerate `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`,
`documentation/glyph-review/contour-cleanup/contour-cleanup-review-queue.md`, and
`documentation/glyph-review/contour-cleanup/contour-cleanup-edit-plan.md` plus
`documentation/glyph-review/arabic-cleanup-drawing-briefs.md` and
`documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md` plus
`documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md` with:

```bash
make contour-cleanup-proof
```

If a later build reintroduces findings, open that HTML proof when deciding
whether a finding is a real drawing issue, an expected style divergence, or a
source structure cleanup candidate. The proof starts with a deduplicated review
queue so the drawing pass can work through unique glyph decisions instead of
repeated built-font rows. Use the Markdown queue as the lightweight checklist
while editing, and use the edit plan for source glyph names plus
`/edit-glyph <name> --master both` commands. Use the drawing briefs as
AI/manual prompt cards: they restate the flagged contour mismatch, source
structure, Rubik reference availability, and acceptance criteria without
allowing reference-outline copying. Use
`documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md` when you want a shorter Runebender
session plan grouped by practical cleanup type. Use
`documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md` to preserve per-glyph
`pending`, `fix-now`, `fixed`, `accepted`, or `deferred` decisions between
regenerations.

For sidebearing and spacing outliers, regenerate the focused visual-risk proof:

```bash
make arabic-visual-risk-proof
make arabic-manual-review-dashboard
make arabic-manual-review-batches
make arabic-current-review-worksheet
make arabic-batch-recorder
make arabic-manual-edit-targets
make arabic-first-review-batch
make arabic-hand-review-session
make arabic-hand-review-contact-sheet
```

Review `documentation/glyph-review/arabic-visual-risk-proof.html` before editing Arabic
overhangs. The current rows are review prompts, not automatic failures, so
record whether they are intentional joining-script spacing, need a source edit,
or should be deferred for native-reader review.
Then use `documentation/glyph-review/arabic-manual-review-dashboard.html` for the compact
cross-weight smoke, mark, numeral, punctuation, risk-row, and contour-queue
pass before opening the full Google Fonts proof files.
Use `documentation/glyph-review/arabic-manual-review-batches.md` as the shortest hand-cleanup
queue; it groups visual proof rows with related contour decisions and gives
guarded update commands.
Use `documentation/glyph-review/arabic-current-review-worksheet.md` as the current fill-in
sheet for observed issues, source/proof locations, and final status before
running any guarded status command.
Use `documentation/glyph-review/arabic-batch-recorder.md` when you are ready to record the
current batch; it expands every unresolved row into `pass`, `fix-needed`, and
`deferred` commands without applying any status change.
Use `documentation/glyph-review/arabic-first-review-batch.md` when you want just the next
structure/wrong-glyph pass with proof links, snapshot links, source GLIF
targets, and guarded outcome commands in one short file.
Use `documentation/glyph-review/arabic-first-review-ai-sweep.md` as a companion snapshot
triage note only; it can speed the pass but it cannot approve rows or recommend
source edits by itself.
Use `documentation/glyph-review/arabic-full-queue-ai-sweep.md` for a queue-wide AI snapshot
summary that separates structure, mark, proof, smoke, numeral, and punctuation
prompts without updating the official review log.
Use `documentation/glyph-review/arabic-hand-review-session.md` when you are ready to work the
whole remaining queue in review passes; it groups the rows by glyph proofs,
marks, proof texture/spacing, smoke strings, and class reviews.
Use `documentation/glyph-review/arabic-hand-review-contact-sheet.html` when you want the
same queue as a print-friendly snapshot sheet with proof links and guarded
update commands.
Use `documentation/glyph-review/arabic-manual-edit-targets.md` only after review marks a row
`fix-needed`; it maps review rows to the current source GLIF paths in both
masters and is not automatic approval to change drawings.

Update one decision row with the guarded helper instead of hand-editing the
wide Markdown table:

```bash
make contour-decision-update GLYPH=dad-ar.fina STATUS=fix-now DECISION="redraw component-only form" NOTES="check dad positional proof" REVIEWED=2026-05-25
```

Already-cleaned mechanical source items:

- `degree`: changed from a solid placeholder into a ring with a counter.
- `ain-ar`: replaced a placeholder-grid outline with a real `ain` candidate.
- `one-ar` and `oneFarsi-ar`: merged overlapping digit pieces into compatible
  single contours.
- `eight-ar`: replaced the two-contour counter form with the one-contour
  Arabic/Persian numeral skeleton.
- `four-ar`: merged overlapping stroke pieces into a compatible single contour,
  removing the variable-only `uni0664` finding.

Former contour-review themes that still deserve visual review:

- Arabic letter structures: `sad`, `dad`, `tah`, `zah`, `meem`, `heh`, `waw`
  hamza, lam-alef composites, and related positional forms. Judge these in the
  Arabic visual review, not by contour-count heuristics alone.
- Arabic mark combinations: `uni0654`/`uni0655` plus tanween/sukun/shadda
  combinations. Review whether the current mark attachment and precomposed
  helper drawings look intentional across weights.
- Required marks: `smallHighTah-ar` and `noonGhunna-ar` are present, anchored,
  and built into `mark`/`mkmk`; their remaining work is visual mark-position
  review.
- Shared punctuation: `braceleft` and `braceright` are currently mechanically
  clean. If edited later, redraw both masters deliberately rather than
  flattening one master in isolation.
- Extended Arabic helpers with dot stacks, including `seenSixdots-ar` and
  three-dot Persian/Urdu forms, need a dot-collision and weight review before
  the Arabic drawing pass is final.

## Resume Commands

After drawing/source edits:

```bash
make arabic-candidate-plan
make ufo-editor-check
make runebender-ufo-check
make arabic-visual-risk-proof
make contour-cleanup-proof
make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --reuse-existing"
make arabic-snapshot-integrity
make arabic-manual-edit-targets
make arabic-first-batch-source-checkpoint
make arabic-pending-source-checkpoint
make preflight
make next-actions
make blockers
```

After proof-sensitive Arabic, spacing, or kerning edits:

```bash
make kerning-proof-check
make kerning-proof-review-check
make preflight
```

If `make kerning-proof-check` fails with a `fonts.google.com` DNS or connection
error, rerun that specific target with network access. `gftools qa --proof`
queries Google Fonts metadata before producing the local HTML proof.

After final values exist and the tree is ready for packaging:

```bash
make release-archive-build
make release-draft-check
make downstream-metadata-check
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Do not use Packager PR mode until the no-PR package has been reviewed and the
Google Fonts Add Font issue exists.

## Remaining Non-Drawing Inputs

- Decide PUA icon block scope.
- Decide kerning scope.
- Finalize release/source commit, tag, and `date_added`.
- Restore GitHub API auth.
- Provide the designer-profile square image or a profile-request plan.
- Apply checked downstream metadata only after final values are present.
