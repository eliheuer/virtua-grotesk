# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `d80aff9da07e4f97ffdd28dd115abffdbfd91126`
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
| commit | `d80aff9da07e4f97ffdd28dd115abffdbfd91126` |
| short commit | `d80aff9` |
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

- `M .agents/README.md`
- ` M .agents/google-fonts-onboarding-checklists.md`
- ` M .agents/skills/google-fonts-qa/SKILL.md`
- ` M AGENTS.md`
- ` M GF_READINESS.md`
- ` M Makefile`
- ` M README.md`
- ` M documentation/arabic-mark-readiness.md`
- ` M documentation/arabic-missing-drawings-ai-execution-goal.md`
- ` M documentation/arabic-review-packet.md`
- ` M documentation/arabic-shaping-smoke-test.md`
- ` M documentation/arabic-source-work-checklist.md`
- ` M documentation/authorship-disclosure-readiness.md`
- ` M documentation/avar-readiness.md`
- ` M documentation/core-qa-process.md`
- ` M documentation/decision-application-blockers.md`
- ` M documentation/decision-readiness.md`
- ` M documentation/downstream-metadata-diff.md`
- ` M documentation/downstream-metadata-readiness.md`
- ` M documentation/final-submission-blockers.md`
- ` M documentation/fontspector-contour-count.md`
- ` M documentation/fontspector-googlefonts-report.md`
- ` M documentation/fontspector-warnings.md`
- ` M documentation/gf-glyphset-readiness.md`
- ` M documentation/github-release-draft.md`
- ` M documentation/github-release-notes.md`
- ` M documentation/glyph-reachability.md`
- ` M documentation/google-fonts-add-font-issue-draft.md`
- ` M documentation/google-fonts-agent-reuse-readiness.md`
- ` M documentation/google-fonts-decision-answer-sheet.md`
- ` M documentation/google-fonts-decision-questions.md`
- ` M documentation/google-fonts-decisions.md`
- ` M documentation/google-fonts-downstream-package-preview.md`
- ` M documentation/google-fonts-language-metadata.md`
- ` M documentation/google-fonts-metadata-review.md`
- ` M documentation/google-fonts-package-checklist.md`
- ` M documentation/google-fonts-production-requirements.md`
- ` M documentation/google-fonts-submission-handoff.md`
- ` M documentation/google-fonts-template-and-pr-audit.md`
- ` M documentation/kerning-proof-review.md`
- ` M documentation/kerning-readiness.md`
- ` M documentation/local-workflow-readiness.md`
- ` M documentation/manual-cleanup-handoff.md`
- ` M documentation/master-compatibility.md`
- ` M documentation/missing-gf-arabic-core.md`
- ` M documentation/missing-gf-latin-core.md`
- ` M documentation/next-actions.md`
- ` M documentation/package-dry-run-readiness.md`
- ` M documentation/package-source-files-audit.md`
- ` M documentation/packager-source-strategy.md`
- ` M documentation/release-archive-manifest.md`
- ` M documentation/release-source-readiness.md`
- ` M documentation/source-ufo-metadata.md`
- ` M documentation/submission-handoff-readiness.md`
- ` M documentation/upstream-structure-readiness.md`
- ` M documentation/variable-font-metadata.md`
- ` M proof.pdf`
- ` M scripts/fix_gf_metadata.py`
- ` M scripts/gf_preflight.py`
- ` M scripts/prepare_downstream_metadata.py`
- ` M scripts/report_add_font_issue_draft.py`
- ` M scripts/report_agent_reuse_readiness.py`
- ` M scripts/report_arabic_mark_readiness.py`
- ` M scripts/report_avar_readiness.py`
- ` M scripts/report_decision_answer_sheet.py`
- ` M scripts/report_decision_readiness.py`
- ` M scripts/report_downstream_metadata_diff.py`
- ` M scripts/report_downstream_metadata_readiness.py`
- ` M scripts/report_final_submission_blockers.py`
- ` M scripts/report_fontspector_contours.py`
- ` M scripts/report_fontspector_markdown.sh`
- ` M scripts/report_fontspector_warnings.py`
- ` M scripts/report_gf_glyphset_readiness.py`
- ` M scripts/report_gf_language_metadata.py`
- ` M scripts/report_glyph_reachability.py`
- ` M scripts/report_kerning_readiness.py`
- ` M scripts/report_next_actions.py`
- ` M scripts/report_production_requirements.py`
- ` M scripts/report_submission_handoff_readiness.py`
- ` M scripts/report_variable_metadata.py`
- ... 1116 more entries omitted

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
