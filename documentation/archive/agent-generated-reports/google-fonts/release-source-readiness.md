# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `fe21c5349deff07ac6eac638281a54b4c09ec7d6`
- Origin URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`
- Normalized origin differs from placeholder: yes
- Source version from release metadata: `1.000`
- Suggested tag from release metadata: `v1.000`
- Suggested tag matches source version: yes
- Suggested tag exists locally: no
- Working tree clean: no
- Branch upstream: `origin/main`
- Ahead/behind branch upstream: `1	0`
- Ahead/behind origin branch: `1	0`
- Placeholder upstream URL still present: no
- Pending source fields in downstream preview: 1
- Downstream `source.files` entries: 4
- Downstream source destination mapping ready: yes
- Downstream source mapping is variable-font-first: yes
- Missing local `source.files`: 0
- Ignored/generated `source.files`: 2
- Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`
- Local google/fonts fork exists: no
- Local google/fonts branch: `missing`
- Local google/fonts main vs upstream/main: `missing`
- Local google/fonts worktree clean: yes
- Local google/fonts dirty paths inside `ofl/virtuagrotesk`: 0
- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0
- Local google/fonts dirty state isolated to `ofl/virtuagrotesk`: no

## Current Repo Git State

| Field | Value |
| --- | --- |
| branch | `main` |
| commit | `fe21c5349deff07ac6eac638281a54b4c09ec7d6` |
| short commit | `fe21c53` |
| origin | `git@github.com:eliheuer/virtua-grotesk.git` |
| normalized GitHub origin candidate | `https://github.com/eliheuer/virtua-grotesk` |
| upstream | `origin/main` |
| upstream ahead/behind | `1	0` |
| origin ahead/behind | `1	0` |
| source version | `1.000` |
| suggested tag | `v1.000` |
| suggested tag matches source version | yes |
| suggested tag exists | no |

## Current Dirty State

- `M .agents/skills/build-font/SKILL.md`
- ` M .agents/skills/compare-reference/SKILL.md`
- ` M .agents/skills/draw-outline/SKILL.md`
- ` M .agents/skills/edit-glyph/SKILL.md`
- ` M .agents/skills/google-fonts-nonlatin-drawing/SKILL.md`
- ` M .agents/skills/kerning/SKILL.md`
- ` M .agents/skills/proof/SKILL.md`
- ` M .agents/skills/render-specimen/SKILL.md`
- ` M .gitignore`
- ` M .ignore`
- ` M AGENTS.md`
- ` M Makefile`
- ` M README.md`
- ` M build.sh`
- ` D designbot/001.rs`
- ` D designbot/002.rs`
- ` D designbot/card.rs`
- ` M documentation/assets/image-license.txt`
- ` M documentation/glyph-review/arabic-cleanup-drawing-briefs.md`
- ` M documentation/glyph-review/arabic-donor-preserve-glyphs.txt`
- ` M documentation/glyph-review/arabic-expansion-from-latin-style.md`
- ` M documentation/glyph-review/arabic-manual-review-dashboard.html`
- ` M documentation/glyph-review/arabic-missing-drawings-ai-execution-goal.md`
- ` M documentation/glyph-review/arabic-next-review-batch.html`
- ` M documentation/glyph-review/arabic-review-packet.md`
- ` M documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`
- ` M documentation/glyph-review/contour-cleanup/contour-cleanup-review-queue.md`
- ` M documentation/google-fonts/article-readiness.md`
- ` M documentation/google-fonts/authorship-disclosure-readiness.md`
- ` M documentation/google-fonts/decision-application-blockers.md`
- ` M documentation/google-fonts/designer-profile-package-draft.md`
- ` M documentation/google-fonts/designer-profile-readiness.md`
- ` M documentation/google-fonts/downstream-metadata-diff.md`
- ` M documentation/google-fonts/downstream-pr-readiness.md`
- ` M documentation/google-fonts/drawbot-runtime-readiness.md`
- ` M documentation/google-fonts/family-name-readiness.md`
- ` M documentation/google-fonts/final-submission-blockers.md`
- ` M documentation/google-fonts/fontspector-contour-count.md`
- ` M documentation/google-fonts/fontspector-googlefonts-report.md`
- ` M documentation/google-fonts/fontspector-metadata-warning-probe.md`
- ` M documentation/google-fonts/fontspector-warnings.md`
- ` M documentation/google-fonts/github-release-draft.md`
- ` M documentation/google-fonts/github-release-notes.md`
- ` M documentation/google-fonts/google-fonts-add-font-issue-draft.md`
- ` M documentation/google-fonts/google-fonts-add-font-template-audit.md`
- ` M documentation/google-fonts/google-fonts-axis-registry-audit.md`
- ` M documentation/google-fonts/google-fonts-decisions.md`
- ` M documentation/google-fonts/google-fonts-downstream-package-preview.md`
- ` M documentation/google-fonts/google-fonts-language-metadata.md`
- ` M documentation/google-fonts/google-fonts-package-checklist.md`
- ` M documentation/google-fonts/google-fonts-readiness.md`
- ` M documentation/google-fonts/google-fonts-reference-index.md`
- ` M documentation/google-fonts/google-fonts-submission-handoff.md`
- ` M documentation/google-fonts/google-fonts-template-and-pr-audit.md`
- ` M documentation/google-fonts/google-fonts-upstream-audit.md`
- ` M documentation/google-fonts/kerning-readiness.md`
- ` M documentation/google-fonts/local-workflow-readiness.md`
- ` M documentation/google-fonts/next-actions.md`
- ` M documentation/google-fonts/open-placeholder-audit.md`
- ` M documentation/google-fonts/package-dry-run-readiness.md`
- ` M documentation/google-fonts/package-source-files-audit.md`
- ` M documentation/google-fonts/packager-source-strategy.md`
- ` M documentation/google-fonts/pr-identity-readiness.md`
- ` M documentation/google-fonts/project-template-automation-readiness.md`
- ` M documentation/google-fonts/pua-scope.md`
- ` M documentation/google-fonts/public-upstream-readiness.md`
- ` M documentation/google-fonts/recent-google-fonts-packages.md`
- ` M documentation/google-fonts/release-archive-manifest.md`
- ` M documentation/google-fonts/release-source-readiness.md`
- ` M documentation/google-fonts/submission-handoff-readiness.md`
- ` M documentation/google-fonts/upstream-structure-readiness.md`
- ` M documentation/proofs/print-spacing-specimen.pdf`
- ` M documentation/proofs/print-specimen-setup.md`
- ` M documentation/proofs/proof.pdf`
- ` M documentation/python-tooling-notes.md`
- ` M documentation/source-guides/ufo-editing.md`
- ` M documentation/source/ufo-editor-readiness.md`
- ` M requirements.in`
- ` M scripts/build_arabic_manual_review_dashboard.py`
- ` M scripts/build_arabic_print_proof.py`
- ... 40 more entries omitted

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
| path | `GF_REPO_PATH_NOT_CONFIGURED` |
| exists | no |
| branch | `missing` |
| origin | `missing` |
| upstream | `missing` |
| main vs upstream/main | `missing` |
| dirty entries | 0 |
| dirty inside `ofl/virtuagrotesk` | 0 |
| dirty outside `ofl/virtuagrotesk` | 0 |
| dirty isolated to `ofl/virtuagrotesk` | no |

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
