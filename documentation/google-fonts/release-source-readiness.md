# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `1af3f0594b03d9dfe534f8d4803016a27f5a7754`
- Origin URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`
- Normalized origin differs from placeholder: yes
- Source version from release metadata: `1.000`
- Suggested tag from release metadata: `v1.000`
- Suggested tag matches source version: yes
- Suggested tag exists locally: no
- Working tree clean: no
- Branch upstream: `origin/main`
- Ahead/behind branch upstream: `0	0`
- Ahead/behind origin branch: `0	0`
- Placeholder upstream URL still present: no
- Pending source fields in downstream preview: 1
- Downstream `source.files` entries: 4
- Downstream source destination mapping ready: yes
- Downstream source mapping is variable-font-first: yes
- Missing local `source.files`: 0
- Ignored/generated `source.files`: 2
- Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`
- Local google/fonts fork exists: yes
- Local google/fonts branch: `main`
- Local google/fonts main vs upstream/main: `0	0`
- Local google/fonts worktree clean: no
- Local google/fonts dirty paths inside `ofl/virtuagrotesk`: 1
- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0
- Local google/fonts dirty state isolated to `ofl/virtuagrotesk`: yes

## Current Repo Git State

| Field | Value |
| --- | --- |
| branch | `main` |
| commit | `1af3f0594b03d9dfe534f8d4803016a27f5a7754` |
| short commit | `1af3f05` |
| origin | `git@github.com:eliheuer/virtua-grotesk.git` |
| normalized GitHub origin candidate | `https://github.com/eliheuer/virtua-grotesk` |
| upstream | `origin/main` |
| upstream ahead/behind | `0	0` |
| origin ahead/behind | `0	0` |
| source version | `1.000` |
| suggested tag | `v1.000` |
| suggested tag matches source version | yes |
| suggested tag exists | no |

## Current Dirty State

- `M .agents/google-fonts-official-reference-map.md`
- ` M .agents/skills/build-font/SKILL.md`
- ` M .agents/skills/edit-glyph/SKILL.md`
- ` M .agents/skills/font-qa/SKILL.md`
- ` M .agents/skills/proof/SKILL.md`
- ` M .agents/skills/render-specimen/SKILL.md`
- ` D .claude/rules/design-philosophy.md`
- ` D .claude/rules/designspace-editing.md`
- ` D .claude/rules/kerning-editing.md`
- ` D .claude/rules/ufo-editing.md`
- ` D .claude/settings.json`
- ` D .claude/skills/build-font/SKILL.md`
- ` D .claude/skills/compare-reference/SKILL.md`
- ` D .claude/skills/draw-outline/SKILL.md`
- ` D .claude/skills/edit-glyph/SKILL.md`
- ` D .claude/skills/font-qa/SKILL.md`
- ` D .claude/skills/kerning/SKILL.md`
- ` D .claude/skills/proof/SKILL.md`
- ` D .claude/skills/render-specimen/SKILL.md`
- ` M .gitignore`
- ` M AGENTS.md`
- ` D CLAUDE.md`
- ` D GF_READINESS.md`
- ` M Makefile`
- ` M README.md`
- ` D arabic_expansion_autoresearch_goal.md`
- ` M build.sh`
- ` D context/curve-quality-workplan.md`
- ` D context/eval-loop.md`
- ` D context/img2bez-architecture.md`
- ` D context/img2bez-pipeline.md`
- ` D documentation/ARTICLE.en_us.html`
- ` D documentation/DESCRIPTION.en_us.html`
- ` D documentation/arabic-ai-visual-screen-batch-2.md`
- ` D documentation/arabic-ai-visual-screen-batch-3.md`
- ` D documentation/arabic-ai-visual-screen-batch-4.md`
- ` D documentation/arabic-ai-visual-screen-batch-5.md`
- ` D documentation/arabic-batch-recorder.md`
- ` D documentation/arabic-candidate-glyph-plan.md`
- ` D documentation/arabic-cleanup-drawing-briefs.md`
- ` D documentation/arabic-current-review-worksheet.md`
- ` D documentation/arabic-donor-preserve-glyphs.txt`
- ` D documentation/arabic-drawing-session-checklist.md`
- ` D documentation/arabic-expansion-from-latin-style.md`
- ` D documentation/arabic-first-batch-source-checkpoint.md`
- ` D documentation/arabic-first-review-ai-sweep.md`
- ` D documentation/arabic-first-review-batch.md`
- ` D documentation/arabic-first-review-crop-integrity.md`
- ` D documentation/arabic-first-review-risk-shortlist.md`
- ` D documentation/arabic-first-review-zoom-snapshots.md`
- ` D documentation/arabic-full-queue-ai-sweep.md`
- ` D documentation/arabic-goal-completion-audit.md`
- ` D documentation/arabic-hand-review-contact-sheet.html`
- ` D documentation/arabic-hand-review-session.md`
- ` D documentation/arabic-manual-edit-targets.md`
- ` D documentation/arabic-manual-review-batches.md`
- ` D documentation/arabic-manual-review-dashboard.html`
- ` D documentation/arabic-mark-readiness.md`
- ` D documentation/arabic-mark-review-proof.html`
- ` D documentation/arabic-mark-triage.md`
- ` D documentation/arabic-missing-drawings-ai-execution-goal.md`
- ` D documentation/arabic-next-review-ai-observations.md`
- ` D documentation/arabic-next-review-ai-triage.md`
- ` D documentation/arabic-next-review-batch.html`
- ` D documentation/arabic-next-review-board.html`
- ` D documentation/arabic-next-review-packet.md`
- ` D documentation/arabic-next-review-snapshots.md`
- ` D documentation/arabic-pending-source-checkpoint.md`
- ` D documentation/arabic-print-proof-index.md`
- ` D documentation/arabic-print-proof.pdf`
- ` D documentation/arabic-review-packet.md`
- ` D documentation/arabic-review-progress.md`
- ` D documentation/arabic-review-worksheet-bundle.md`
- ` D documentation/arabic-shaping-smoke-test.md`
- ` D documentation/arabic-snapshot-integrity.md`
- ` D documentation/arabic-source-edit-diff.md`
- ` D documentation/arabic-source-work-checklist.md`
- ` D documentation/arabic-structure-sweep.html`
- ` D documentation/arabic-structure-triage.md`
- ` D documentation/arabic-visual-review-batch.tsv`
- ... 198 more entries omitted

## Downstream Source Mapping

| Source file | Destination file | Local status |
| --- | --- | --- |
| `OFL.txt` | `OFL.txt` | present and not ignored |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | ignored/generated |
| `documentation/google-fonts/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | present and not ignored |
| `documentation/assets/readme-specimen.png` | `article/readme-specimen.png` | ignored/generated |

## Pending Downstream Source Fields

- `commit: "Pending final release/source commit"`

## Local google/fonts Fork

| Field | Value |
| --- | --- |
| path | `/Users/eli/GH/forks/fonts` |
| exists | yes |
| branch | `main` |
| origin | `git@github.com:eliheuer/fonts.git` |
| upstream | `https://github.com/google/fonts.git` |
| main vs upstream/main | `0	0` |
| dirty entries | 1 |
| dirty inside `ofl/virtuagrotesk` | 1 |
| dirty outside `ofl/virtuagrotesk` | 0 |
| dirty isolated to `ofl/virtuagrotesk` | yes |

## Apply Before Final Packager Run

- Keep the decided public upstream URL synchronized with OFL, source
  metadata, Article links, handoff text, and downstream metadata.
- Use the selected release/archive source strategy for the first
  Packager pass unless Google Fonts review asks for another mode.
- Ensure the final release archive contains every mapped
  `source.files` path before the latest-release Packager run.
- Create or update the final upstream tag only after drawing/source
  work and maintainer decisions are complete.
- Record the final repository URL, commit, branch, GitHub release download `.zip` URL, and source mode in
  `documentation/google-fonts/google-fonts-downstream-package-preview.md`.
- Rerun `make preflight` so proof evidence and generated reports
  stay synchronized, then run
  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` from
  an aligned local `google/fonts` fork.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
