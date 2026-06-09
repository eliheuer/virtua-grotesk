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

Prototype donor-copy scripts from an earlier Virtua Grotesk pass were archived
under `documentation/archive/agent-generated-scripts/scripts/`. Do not treat
those as active commands. If this workflow is needed again, first promote a
small generic candidate/apply script back into `scripts/`, document the exact
inputs, and keep the apply step dry-run-first.

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
- focused proof output is reviewed by a human;
- broad proof rows have human statuses: `pass`, `fix-needed`, or `deferred`;
- active source UFOs load in the editor intended for hand cleanup; if the
  editor uses a stricter UFO loader than the build tooling, add a focused
  loader check so syntax/editor issues do not block drawing sessions.

## AI Assistance

Use AI for triage and review acceleration:

- batch grouping and priority sorting;
- source reuse mapping suggestions;
- proof comparison prompts;
- finding likely glyph names or proof locations for fix-needed rows;
- summarizing blockers into hand-cleanup lists.

Keep temporary AI review files outside the active docs unless they are still
being used. Do not ask AI to approve final Arabic or other script drawings without human
visual review. When a row is uncertain, record `deferred` with the needed
native-reader or script-specialist follow-up.
