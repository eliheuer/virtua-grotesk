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

Write or use a candidate script so it is safe to run repeatedly. It should
accept a target source, a donor/reference source, a glyph selection, and an
output path. Do not hard-code one donor family; Rubik, Noto, or another OFL
source may be useful depending on the target design.

```bash
python scripts/build_nonlatin_candidate_glyphs.py --donor path/to/Donor.designspace --dry-run
python scripts/build_nonlatin_candidate_glyphs.py --donor path/to/Donor.designspace --write
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

### Review-Then-Apply Workflow

For replacement batches, prefer this split:

1. Human marks glyphs needing replacement in the editor, usually with red
   `public.markColor`.
2. Agent builds a scratch candidate from those marks and an explicit donor
   source. This can be previewed in ComfyUI/Runebender or with generated proofs.
3. Human reviews the scratch result.
4. Agent applies only the approved candidate glyphs back to production sources
   with a surgical `.glif` copy. Do not save/rewrite whole UFOs just to copy
   outlines.

For this repo the concrete commands are:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --donor /path/to/Donor.designspace \
  --glyphs mark:red \
  --arabic-only \
  --output build/arabic-donor-candidates/red-marked-arabic \
  --write --force

./venv/bin/python scripts/apply_donor_glyph_candidates.py \
  --report build/arabic-donor-candidates/red-marked-arabic/glyph-candidate-report.json \
  --glyphs report \
  --arabic-only

./venv/bin/python scripts/apply_donor_glyph_candidates.py \
  --report build/arabic-donor-candidates/red-marked-arabic/glyph-candidate-report.json \
  --glyphs report \
  --arabic-only \
  --write
```

Guardrails for the apply step:

- dry-run first; require `would-apply` for every selected master/glyph pair;
- preserve existing mark colors by default so the human can approve/clear them;
- select `status == candidate` from the candidate report, not every red glyph;
- keep hand-drawn or approved glyphs unmarked or listed in an exclude file;
- after write, check `git diff --name-only sources` and confirm only intended
  `.glif` files changed and no untracked glyph files appeared;
- open both source UFOs with the repo venv, rebuild, and rerun reports.

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
make reports
make preflight
```

After shaping-sensitive work:

```bash
make preflight
make specimen
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
- if multiple rows are likely to close in one pass, optionally add a TSV batch
  template plus a validating updater as a temporary entry form. The canonical
  record should remain the Markdown or structured review log. The template
  should be blank by default so applying it unedited fails, and the updater
  should dry-run by default, reject unknown statuses, reject duplicate keys, and
  only write on an explicit apply flag. Provide a paired apply-check command
  that writes the canonical log, regenerates reports, and reruns preflight after
  the dry run has been reviewed.
- a compact hand-review session sheet exists for the whole remaining queue,
  grouped into realistic review passes with proof links, GLIF targets, and
  guarded status-update commands.
- a compact drawing-session checklist exists for the active cleanup session. It
  should start with source-editor readiness checks, then list the current batch,
  exact proof files to open, guarded pass/fix/defer commands, likely Regular and
  Bold GLIF targets, a glyph-level punchlist grouped by source glyph and prompt
  source, and the rebuild/report/preflight loop.
- a fast source-edit diff report exists for hand drawing. It should read
  worktree status, list changed non-Latin GLIF files, and flag one-sided
  Regular/Bold or otherwise paired-master edits before the full build/preflight
  loop runs.
- a source-structure checkpoint exists for unresolved review rows. It should
  resolve row-to-GLIF targets through the UFO `contents.plist` mapping, inspect
  every active master, report missing source files, contour/component/point
  counts, and flag Regular/Bold or otherwise paired-master structure mismatches
  before hand edits start.
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
- compact drawing-session checklists for the current hand-edit pass, especially
  when the reviewer is moving from proof review into source editing;
- glyph-level punchlists for the active batch so reviewers can inspect a short
  source-glyph order before opening outlines, while still requiring a row to be
  marked `fix-needed` before editing;
- source-edit diff guards that catch one-sided non-Latin GLIF edits during a
  drawing session before master compatibility or interpolation failures appear;
- source-structure checkpoints for the current batch and the full unresolved
  queue, so reviewers know every `fix-needed` row maps to paired source files
  before opening the UFOs;
- optional TSV batch recorder templates and validators for recording multiple
  human `pass`, `fix-needed`, or `deferred` decisions without hand-editing wide
  Markdown tables. Treat TSV as a temporary input form only; the canonical
  review log remains the durable source of truth. Pair the optional form with
  apply-check targets that immediately refresh generated reports and preflight
  after those decisions are written;
- optional screenshot/snapshot generation for those rows, with stale-output
  protection, full-queue mode when useful, and browser failures reported in a
  review report;
- finding likely glyph names or proof locations for fix-needed rows;
- summarizing blockers into hand-cleanup lists.

Do not ask AI to approve final Arabic or other script drawings without human
visual review. When a row is uncertain, record `deferred` with the needed
native-reader or script-specialist follow-up.
