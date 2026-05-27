# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `05706bd4442fe5c556495ad3f9c4dd7a5185b775`
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
- Ignored/generated `source.files`: 1
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
| commit | `05706bd4442fe5c556495ad3f9c4dd7a5185b775` |
| short commit | `05706bd` |
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

- `M .agents/google-fonts-onboarding-checklists.md`
- ` M .agents/skills/google-fonts-nonlatin-drawing/SKILL.md`
- ` M .agents/skills/google-fonts-qa/SKILL.md`
- ` M Makefile`
- ` M documentation/arabic-batch-recorder.md`
- ` M documentation/arabic-current-review-worksheet.md`
- ` M documentation/arabic-goal-completion-audit.md`
- ` M documentation/arabic-hand-review-contact-sheet.html`
- ` M documentation/arabic-hand-review-session.md`
- ` M documentation/arabic-manual-edit-targets.md`
- ` M documentation/arabic-next-review-ai-triage.md`
- ` M documentation/arabic-next-review-board.html`
- ` M documentation/arabic-next-review-packet.md`
- ` M documentation/arabic-print-proof.pdf`
- ` M documentation/arabic-review-worksheet-bundle.md`
- ` M documentation/arabic-visual-review-runbook.md`
- ` M documentation/final-submission-blockers.md`
- ` M documentation/fontspector-googlefonts-report.md`
- ` M documentation/fontspector-metadata-warning-probe.md`
- ` M documentation/fontspector-warnings.md`
- ` M documentation/github-release-draft.md`
- ` M documentation/github-release-notes.md`
- ` M documentation/next-actions.md`
- ` M documentation/release-archive-manifest.md`
- ` M documentation/release-source-readiness.md`
- ` M documentation/upstream-structure-readiness.md`
- ` M proof.pdf`
- ` M scripts/build_arabic_next_review_board.py`
- ` M scripts/build_arabic_print_proof.py`
- `MM scripts/gf_preflight.py`
- ` M scripts/report_arabic_batch_recorder.py`
- ` M scripts/report_arabic_current_review_worksheet.py`
- ` M scripts/report_arabic_goal_completion.py`
- ` M scripts/report_arabic_manual_edit_targets.py`
- ` M scripts/report_arabic_review_worksheet_bundle.py`
- ` M scripts/report_arabic_visual_review_runbook.py`
- ` M scripts/report_next_actions.py`
- ` M scripts/test_arabic_visual_review_update.sh`
- `?? documentation/arabic-drawing-session-checklist.md`
- `?? documentation/arabic-print-proof-index.md`
- `?? documentation/arabic-source-edit-diff.md`
- `?? documentation/arabic-visual-review-batch.tsv`
- `?? scripts/report_arabic_drawing_session_checklist.py`
- `?? scripts/report_arabic_source_edit_diff.py`
- `?? scripts/report_arabic_visual_review_batch_tsv.py`
- `?? scripts/update_arabic_visual_review_batch.py`

## Downstream Source Mapping

| Source file | Destination file | Local status |
| --- | --- | --- |
| `OFL.txt` | `OFL.txt` | present and not ignored |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | ignored/generated |
| `documentation/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | present and not ignored |
| `documentation/readme-specimen.png` | `article/readme-specimen.png` | present and not ignored |

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
  `documentation/google-fonts-downstream-package-preview.md`.
- Rerun `make preflight` so proof evidence and generated reports
  stay synchronized, then run
  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` from
  an aligned local `google/fonts` fork.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
