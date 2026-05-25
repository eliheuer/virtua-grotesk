# /google-fonts-nonlatin-drawing

Finish missing non-Latin drawings for a Google Fonts submission while keeping
source masters compatible, script behavior intact, and final outline decisions
under human review. This skill is portable; replace family names, source paths,
script tags, glyphsets, and proof commands when copying it to another repo.

## Usage
`/google-fonts-nonlatin-drawing [audit|candidates|proof|review|all]`

Default: `all`

## Principles

- Treat generated outlines as scaffolds, not final production drawings.
- Prefer deterministic source reuse over model training for first-pass missing
  glyphs. Reuse family-native bases, dots, marks, punctuation, components, and
  spacing patterns before looking outside the family.
- Use OFL reference fonts only as visual references or overlays. Do not copy
  outlines into the submitted source unless the license, provenance, style fit,
  and maintainer decision explicitly allow it.
- Keep both masters structurally compatible. If one master gets a contour,
  component, anchor, width, or glyph entry change, verify the corresponding
  master immediately.
- Separate mechanical coverage from drawing quality. A cmap can be complete
  while shaping, marks, spacing, or script texture still need review.

## Audit

1. Identify the intended Google Fonts glyphset and first-submission script
   scope.
2. Generate or refresh reports for:
   - missing codepoints,
   - source glyph names needed in every master,
   - positional forms and unencoded helpers,
   - mark glyphs and dotted circle,
   - anchors and `mark`/`mkmk`,
   - shaping smoke strings,
   - master compatibility,
   - visual proof status.
3. Translate codepoint gaps into source glyph work. For joining scripts, track
   default, final, initial, medial, mark, ligature, and helper glyphs
   separately.
4. Record the stale baseline separately from current evidence so agents do not
   keep solving already-closed gaps.

## Candidate Generation

Write the candidate script so it is safe to run repeatedly:

```bash
python scripts/build_nonlatin_candidate_glyphs.py --dry-run
python scripts/build_nonlatin_candidate_glyphs.py --write
```

Requirements:

- dry-run by default;
- open every active UFO master;
- create the same glyph names in every master;
- assign Unicode only to encoded default glyphs;
- keep positional forms and source helpers unencoded unless explicitly decided;
- reuse existing family-native skeletons, marks, dots, anchors, and widths;
- report auto-created, review-needed, hand-draw-needed, and compatibility-risk
  buckets;
- after write, rerun dry-run and expect no remaining creation or compatibility
  risks.

## Reference Fonts

Use references such as Rubik, Noto, or another OFL family as comparison data:

- convert to UFO only when it helps inspect structure, anchors, glyph naming, or
  shaping behavior;
- normalize UPM mentally or in an overlay, then redraw in the target family's
  construction;
- compare proportions, joining logic, mark placement, and spacing rhythm;
- do not let reference contour count alone dictate the target drawing.

## Batch Order

Use small batches with a build/report/preflight loop after each one:

1. Shared punctuation and symbols with low shaping risk.
2. Digits and numerals, checking rhythm and widths.
3. Joining letters and their positional forms.
4. Script punctuation and symbols.
5. Marks, dotted circle, anchors, and mark-to-mark behavior.
6. Final spacing, sidebearing, contour cleanup, and native-reader review.

## Verification Loop

After each batch:

```bash
./build.sh
make reports-only
make preflight-only
```

After shaping-sensitive work:

```bash
make preflight
make kerning-proof-check
make kerning-proof-review-check
```

Verify evidence, not intent:

- no missing target codepoints unless explicitly accepted;
- source glyphs exist in all masters;
- master compatibility has no blocking mismatches;
- shaping smoke tests pass with no `.notdef`;
- dotted circle, marks, anchors, and `mark`/`mkmk` are ready or documented;
- visual-risk audit and focused proof are reviewed;
- broad proof rows have human statuses: `pass`, `fix-needed`, or `deferred`.
- active source UFOs load in the editor intended for hand cleanup; if the
  editor uses a stricter UFO loader than the build tooling, add a focused
  loader check so syntax/editor issues do not block drawing sessions.
- a compact next-review packet exists for the first pending proof rows so hand
  reviewers can make progress without reading the full generated runbook.
- a one-session first-batch worksheet exists when the first proof pass still
  feels too wide; it should include only the current row cues, proof links,
  snapshots, likely GLIF targets, and guarded status commands.
- a batch recorder exists when reviewers are ready to update statuses; it
  should print `pass`, `fix-needed`, and `deferred` commands for the current
  unresolved batch without applying changes.
- a compact hand-review session sheet exists for the whole remaining queue,
  grouped into realistic review passes with proof links, GLIF targets, and
  guarded status-update commands.
- a print-friendly contact sheet exists when snapshot evidence is ready, so
  reviewers can scan the full queue visually while keeping proof/source links
  and guarded status commands nearby.
- an AI-safe triage report exists for that packet when useful; it summarizes
  snapshots and machine checks, but does not record final visual status.
- a local review board exists when useful, embedding snapshots, proof links,
  prompts, and guarded update commands for the current hand-review batch.
- optional local PNG snapshots exist for the next-review packet when HTML proof
  navigation is slowing review; snapshots are triage aids and cannot replace
  human proof/source review.

## AI Assistance

Use AI for triage and review acceleration:

- batch grouping and priority sorting;
- source reuse mapping suggestions;
- proof comparison prompts;
- compact next-review packet generation for the first pending rows;
- compact hand-review session sheets that group the full pending queue into
  proof, mark, spacing, smoke-string, and class-review passes;
- AI-safe triage reports that separate mechanical prechecks from human
  pass/fix/defer decisions;
- AI visual-observation notes that record obvious snapshot findings and likely
  review prompts without changing the official review log;
- separate first-batch AI sweep notes when the model has inspected actual
  rendered images; include viewed evidence, concrete observations, human
  follow-ups, and explicit non-decisions;
- full-queue AI sweeps for larger review sets; group rows by review kind and
  separate unrelated coverage blockers from non-Latin drawing prompts;
- local review boards that put snapshot evidence and guarded update commands in
  one place for faster hand cleanup;
- optional screenshot/snapshot generation for those rows, with stale-output
  protection, full-queue mode when useful, and browser failures reported in a
  review report;
- finding likely glyph names or proof locations for fix-needed rows;
- summarizing blockers into hand-cleanup lists.

Do not ask AI to approve final Arabic or other script drawings without human
visual review. When a row is uncertain, record `deferred` with the needed
native-reader or script-specialist follow-up.
