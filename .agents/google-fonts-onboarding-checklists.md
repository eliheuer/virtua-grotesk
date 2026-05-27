# Google Fonts Onboarding Checklists

These checklists collect the reusable parts of the Virtua Grotesk onboarding
work so another font project can start from a stronger baseline. Copy this file
and the related `.agents/skills/google-fonts-*` skills into the next repo, then
replace family-specific paths, names, scripts, and source strategy values.

## 1. Repo Baseline

- Public upstream URL chosen and recorded.
- OFL or other accepted license present.
- `AUTHORS.txt` and `CONTRIBUTORS.txt` present when applicable.
- Reserved Font Name status explicit.
- Active sources live in a clear source directory.
- Generated build outputs are ignored unless the packaging strategy requires
  committing them.
- Build command documented and reproducible.
- Source archive or release strategy documented.
- README explains build, QA, proof, and handoff commands.
- Agent entrypoint points to the Google Fonts skills/checklists.

## 2. Decision Log

Create one canonical decision log with status, answer, rationale, and apply-to
surfaces. Track at least:

- public upstream URL,
- source packaging strategy,
- version and tag,
- family name, trademarks, namecheck, and RFN status,
- copyright holder and CLA identity,
- AI-use disclosure,
- designer profile identity,
- first-submission script scope,
- custom sample text,
- Article versus legacy description,
- variable-axis and `avar` decisions,
- vendor ID,
- kerning scope,
- private-use glyph scope,
- project-template automation.

## 3. Build And Binary QA

- Build variable fonts and expected static instances.
- Confirm generated file names and locations.
- Inspect name table, version, license, `OS/2.fsType`, vendor ID, `fvar`,
  `STAT`, and script metadata.
- Run Fontspector `googlefonts` profile.
- Save the report in `documentation/`.
- Classify every FAIL and WARN.
- Run a package-context warning probe with the intended `METADATA.pb` before
  treating loose-font subset or reachability warnings as final.
- When loose-font QA repeats one subset/reachability warning across variable
  and static fonts, keep the loose count in the report but base downstream
  triage on the package-context warning floor.
- For any lower-warning subset variant, confirm it still serves the intended
  script scope; do not remove a target subset just to make WARN count smaller.
- Keep a zero-warning queue that distinguishes mechanical metadata fixes,
  glyphset coverage, drawing/source cleanup, and reviewer-accepted exceptions.
- Add an explicit "honest zero possible" line to the queue. If the answer is
  no, record the current warning floor and the exact scope/coverage choices
  that would be required to reach zero.
- Split the zero-warning plan into a release-scope path and a true zero path.
  The release path should say what can ship with reviewer evidence; the true
  zero path should list the larger glyphset or metadata-scope work needed.
- For intended script subsets that fail subset-threshold warnings, decide
  whether to expand coverage, defer the script, or carry reviewer evidence; do
  not lower the warning count by hiding the intended serving scope.
- If zero requires a large new glyphset expansion, make that a scoped coverage
  project instead of mixing it into final cleanup.
- For support codepoints such as U+0237, U+200F, U+20B9, or U+25CC, prove any
  proposed cmap removal or metadata rescue in package context; these codepoints
  may be required for Google Fonts checks, shaping, or mark proofing even when
  Fontspector reports reachability noise.
- Keep a final blocker summary that distinguishes drawing/source blockers from
  onboarding mechanics.

## 4. Glyphset And Script QA

- Identify intended first-submission script scope.
- Check Latin Core coverage.
- Check each non-Latin core glyphset needed for the submission.
- Generate missing-codepoint reports.
- Convert codepoint gaps into source glyph work by master.
- For non-Latin scripts, build candidates with deterministic source reuse before
  considering AI-generated outlines or model training.
- Keep candidate generation dry-run-first and idempotent; after a write pass, a
  clean dry run should show no remaining candidate creation or compatibility
  risks.
- Use `.agents/skills/google-fonts-nonlatin-drawing/SKILL.md` as the portable
  rescue workflow when a future family has missing Arabic or other non-Latin
  drawings.
- Assign Unicode only to encoded default glyphs; keep positional forms and
  helper glyphs unencoded unless the project has a documented reason.
- Verify mark glyphs, anchors, and mark/mkmk support when needed.
- Run shaping smoke tests for joining scripts.
- Keep script review packets linked from the Add Font issue draft.
- Track source-only helper glyph reachability separately from script coverage:
  Unicode cmap, GSUB outputs, and component references are different evidence.
- Treat generated candidates as scaffolds that still need visual proofing,
  contour cleanup, spacing, and script-specialist review.
- Before hand cleanup, verify the active UFOs load in the editor being used.
  A strict source check with `fontTools.ufoLib` is useful, but editor-specific
  loaders such as Norad may catch different issues; keep a focused loader check
  available when the editor fails without a useful nested error.
- Add a built-font visual-risk audit for non-Latin scripts before broad human
  proof review. Check for blank visible glyphs, `.notdef` mappings,
  non-mark zero advances, extreme bounds, and sidebearing outliers.
- For any visual-risk rows, generate a focused proof that embeds the current
  built fonts and shows the risky glyphs in isolated plus shaped script
  contexts across weights.
- For Fontspector contour-count warnings, map production glyph names back to
  source glyphs and record both masters' contour, point, and component counts.
  Use that as an editor queue, not as permission to change contour structure
  without visual review.
- Preserve contour review decisions in a regeneratable log with statuses such
  as `pending`, `fix-now`, `fixed`, `accepted`, and `deferred`.
- When broad proof review still feels too wide, generate a compact manual
  review batch report that groups visual proof rows with related contour
  decisions and guarded update commands.
- Add a compact hand-review session sheet for the full remaining queue when the
  reviewer needs a single execution checklist. It should group the rows by
  proof glyph pass, marks, spacing/texture, smoke strings, and class reviews,
  while linking source GLIF targets for any `fix-needed` row.
- Add a print-friendly contact sheet when snapshot evidence exists for the
  full queue. It should show the row snapshot, cue, proof/source links, and
  guarded status commands without replacing proof/source inspection.
- Keep an even smaller "next review packet" for the current first batch. It
  should include the next pending proof rows, exact evidence links, source edit
  targets, AI comparison prompts, and guarded commands for recording `pass`,
  `fix-needed`, or `deferred`.
- For the first unresolved batch, also generate a one-session worksheet that
  removes broad runbook noise and keeps only the current row cues, proof links,
  snapshots, source GLIF targets, and guarded status commands.
- Add a batch recorder when the reviewer is ready to close rows. It should
  expand the current unresolved batch into one `pass`, `fix-needed`, and
  `deferred` command per row, plus the regeneration commands to run afterward.
- Add an optional TSV batch template and validating updater when several rows
  may close together. Treat TSV as a temporary input form, not the canonical
  record; the official review log stays the source of truth. Keep the generated
  template blank in the status/reviewer/notes fields, make the updater dry-run
  by default, reject bad statuses and duplicate keys, and require an explicit
  apply flag before writing the review log. Add a one-command apply-check target
  that applies the TSV, regenerates reports, and reruns preflight so the
  official review log and derived evidence stay in sync after a batch review
  pass.
- Add a compact drawing-session checklist before hand editing starts. It should
  begin with UFO/editor loader checks, then list the current batch, exact proof
  files to open, guarded pass/fix/defer commands, likely source GLIF files in
  every master, a glyph-level punchlist grouped by source glyph and review
  prompt, and the rebuild/report/preflight commands after edits.
- Add a fast source-edit diff report for variable or multi-master projects.
  It should read current worktree status, list changed non-Latin GLIF files,
  and flag one-sided edits where a Regular/Bold or otherwise paired master edit
  is missing before the full build/preflight loop runs.
- Add source-structure checkpoints for the active batch and, when the queue is
  broad, all unresolved review rows. Resolve GLIF paths through UFO
  `contents.plist`, not filename guesses; report missing source files,
  contours, components, points, and paired-master structure mismatches before
  hand drawing starts.
- When AI has actually looked at snapshots, keep that as a separate companion
  sweep note. The note should list viewed evidence, concrete observations,
  human follow-ups, and non-decisions; it must not silently update the official
  review log.
- For longer queues, add a full-queue sweep that groups pending rows by review
  kind, calls out representative images inspected, and separates unrelated
  coverage blockers from drawing quality prompts.
- Add an AI-safe triage report for the packet when useful. It may summarize
  current snapshots, mechanical blockers, and review prompts, but it must not
  mark rows as passed without human proof/source inspection.
- When reviewers need a faster hand pass, build a single local review board
  that embeds the packet snapshots next to proof/source links and guarded
  update commands. Treat it as a convenience layer over the same evidence.
- When proof HTML is too slow to scan row-by-row, generate local PNG snapshots
  for the current next-review packet. Treat snapshots as triage aids only:
  final status still comes from reviewing the proof HTML/source glyphs and
  recording `pass`, `fix-needed`, or `deferred`.

## 5. Visual QA

- Generate proof PDF or equivalent local proof.
- Generate `gftools qa --proof` HTML output.
- Confirm proof coverage for every expected instance and proof type.
- Review the focused visual-risk proof before broad proof sweeps so blank glyphs,
  sidebearing outliers, clipping risks, and spacing risks are resolved or
  explicitly queued.
- Review spacing, kerning, diacritics, and script-specific behavior.
- Record review status and accepted deferrals.
- For non-Latin additions, record visual proof status and contour decisions in
  separate logs, then summarize them in a batch queue for hand cleanup.
- Use a next-review packet when the full runbook is too large for a hand pass;
  regenerate it after each recorded outcome so the first page always shows the
  next actionable rows.
- Use a hand-review session sheet when the reviewer is ready to work through
  the full pending queue in several short passes without losing the update
  commands or edit-target links.
- Use a contact-sheet HTML view when the reviewer needs a snapshot-first pass
  over the whole queue before opening the detailed proof HTML.
- Include an optional snapshot command for the first pending rows when useful.
  Keep it out of default QA if it depends on a local browser, and make the
  renderer delete stale files before capture so old PNGs cannot look current.
- Rerun proofs after spacing, kerning, glyph, source, or scope changes.

## 6. Metadata

- Generate downstream `METADATA.pb` from built fonts and decisions.
- Check family and designer strings.
- Check `category`, `subsets`, and `primary_script`.
- Confirm `date_added` is final before applying downstream.
- Confirm `source.repository_url` is public and final.
- Confirm `source.commit` is a final 40-character lowercase commit.
- Include `source.archive_url` only when release/archive mode is selected.
- Include `source.config_yaml` only for build-from-source mode or reviewer
  request.
- Avoid custom `languages`, `sample_text`, or `tags` unless review asks.

## 7. Article And Images

- Decide Article versus legacy description.
- Keep `ARTICLE.en_us.html` valid and package-ready.
- Keep `DESCRIPTION.en_us.html` available if needed.
- Track image paths, size limits, and provenance/license.
- Use real font specimens or relevant visuals, not placeholder art.
- Confirm article assets appear in the selected package source strategy.

## 8. Designer Profile

- Compare final designer strings to existing `google/fonts` catalog profiles.
- Prepare `info.pb`, `bio.html`, and a square image when a profile is missing.
- Validate links, biography HTML, and image dimensions/format.
- Check for path collisions in the local `google/fonts` fork.
- Keep the designer-profile request plan linked from the Add Font issue draft.

## 9. Release And Package Strategy

- Choose default branch, latest-release/archive, or build-from-source.
- Verify every source file exists locally.
- Reject unsafe or duplicate source and destination paths.
- If using release/archive mode, build the archive from a manifest and verify
  contents plus hashes.
- Do not mark the archive URL final until the GitHub tag and release asset
  exist publicly.
- Keep fallback paths documented for Google Fonts reviewer requests.

## 10. Local google/fonts Fork

- Local fork exists.
- `origin` points to the maintainer fork.
- `upstream` points to `google/fonts`.
- Main branch is synced with both remotes.
- No dirty paths outside the target family directory.
- Current target family directory contents are listed explicitly.
- Starter `METADATA.pb` state is clearly marked when present.
- Git user name/email align with CLA and final downstream commit identity.
- GitHub API auth is ready before Packager calls that need GitHub.

## 11. Add Font Issue

- Refresh the current Add Font issue template from `google/fonts`.
- Use current template labels.
- Leave requirement checkboxes unchecked until opening the actual issue.
- Include the public repo URL.
- Include short description, namecheck status, maintenance commitment, license,
  source, TTF, glyphset, and QA status.
- Include AI-use disclosure when applicable.
- Include script-specific scope and known blockers.
- Link evidence reports instead of pasting long generated output.

## 12. Packager And PR

- Run Packager without PR mode first.
- Review generated downstream changes.
- Confirm changes are scoped to one family directory.
- Confirm metadata, fonts, article, image assets, license, and upstream linkage.
- Open or link the Add Font issue before PR mode.
- Use the expected PR title/body/provenance.
- Use `-p -i ISSUE_NUMBER` only after the no-PR package is reviewed.

## 13. Final Handoff

Before final issue/PR work, the repo should have current reports for:

- reference index,
- production requirements,
- decision readiness,
- final blockers,
- next actions,
- generated font metadata,
- glyphset coverage,
- language metadata,
- Fontspector results,
- proof review,
- package source files,
- source strategy,
- release archive manifest,
- downstream metadata,
- package dry-run readiness,
- Add Font issue draft,
- PR identity/auth,
- downstream PR readiness,
- designer profile readiness.

## 14. Copy-To-Next-Font Notes

When copying to another font repo:

- replace family name, style names, axes, source paths, and downstream directory,
- remove Virtua-specific Arabic, PUA, and release decisions unless they apply,
- refresh official Google Fonts docs and templates before relying on copied
  wording,
- rebuild report scripts around that repo's actual source structure,
- keep final gates strict enough to fail on stale generated evidence.
