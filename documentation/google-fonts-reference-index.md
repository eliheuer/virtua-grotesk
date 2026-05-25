# Google Fonts Reference Index

This generated index maps official Google Fonts documentation and
Google Fonts GitHub references to the local reports and gates used for
Virtua Grotesk onboarding. Use it as the audit map before changing
handoff, metadata, package, QA, or designer-profile workflows.

## Summary

- References tracked: 17
- References with local evidence: 17 / 17
- Official-doc references only: yes
- Google Fonts GitHub references included: yes

## Reference Map

| Source | URL | Local evidence | Current local use |
| --- | --- | --- | --- |
| Adding & Upgrading Fonts to Google Fonts | https://googlefonts.github.io/gf-guide/onboarding.html | `documentation/google-fonts-add-font-issue-draft.md`<br>`documentation/google-fonts-production-requirements.md`<br>`documentation/final-submission-blockers.md` | tracks issue-first submission, OFL, public repo, source, TTF, glyphset, and QA requirements |
| Upstream repository structure | https://googlefonts.github.io/gf-guide/upstream.html | `documentation/upstream-structure-readiness.md`<br>`documentation/package-source-files-audit.md`<br>`documentation/project-template-automation-readiness.md` | checks mandatory upstream paths, source/build layout, public repo shape, and project-template deltas |
| Overall font files requirements | https://googlefonts.github.io/gf-guide/requirements.html | `documentation/google-fonts-production-requirements.md`<br>`documentation/missing-gf-latin-core.md`<br>`documentation/missing-gf-arabic-core.md`<br>`documentation/numeric-feature-readiness.md` | tracks family naming, embedding, glyphset coverage, OpenType feature expectations, and required shared glyphs |
| Production requirements | https://googlefonts.github.io/gf-guide/production.html | `documentation/google-fonts-production-requirements.md`<br>`documentation/core-qa-process.md`<br>`documentation/numeric-feature-readiness.md` | keeps scalable-font production, local QA, and web-serving assumptions visible before final submission |
| Variable fonts specifics | https://googlefonts.github.io/gf-guide/variable.html | `documentation/variable-font-metadata.md`<br>`documentation/avar-readiness.md`<br>`documentation/google-fonts-axis-registry-audit.md`<br>`documentation/google-fonts-production-requirements.md` | checks the wght axis, fvar/static instance expectations, avar warning state, and axis registry alignment |
| Build the fonts | https://googlefonts.github.io/gf-guide/build.html | `sources/config.yaml`<br>`documentation/upstream-structure-readiness.md`<br>`documentation/packager-source-strategy.md`<br>`documentation/google-fonts-production-requirements.md` | anchors the gftools builder config, build-from-source fallback, and public build-input review |
| Package the fonts | https://googlefonts.github.io/gf-guide/package.html | `documentation/package-dry-run-readiness.md`<br>`documentation/packager-source-strategy.md`<br>`documentation/downstream-metadata-diff.md`<br>`documentation/downstream-pr-readiness.md` | maps Packager source modes, no-PR dry-run flow, downstream branch naming, and source.files/archive strategy |
| METADATA file | https://googlefonts.github.io/gf-guide/metadata.html | `documentation/google-fonts-downstream-package-preview.md`<br>`documentation/downstream-metadata-readiness.md`<br>`documentation/downstream-metadata-diff.md`<br>`documentation/generated-font-metadata.md` | validates family metadata, variable font records, subsets, primary_script, source block, and final pending fields |
| Article file | https://googlefonts.github.io/gf-guide/article.html | `documentation/article-readiness.md`<br>`documentation/google-fonts-metadata-review.md`<br>`documentation/google-fonts-package-checklist.md`<br>`documentation/google-fonts-template-and-pr-audit.md` | checks ARTICLE.en_us.html, image/license assets, downstream article mapping, and package checklist wording |
| Lang Metadata System | https://googlefonts.github.io/gf-guide/lang.html | `documentation/google-fonts-language-metadata.md`<br>`documentation/arabic-review-packet.md`<br>`documentation/missing-gf-arabic-core.md` | ties Arabic script metadata, primary_script, subsets, and GF Arabic Core coverage evidence together |
| Making a PR to Google Fonts | https://googlefonts.github.io/gf-guide/making-pr.html | `documentation/pr-identity-readiness.md`<br>`documentation/downstream-pr-readiness.md`<br>`documentation/google-fonts-submission-handoff.md` | keeps issue-first rule, CLA/git identity, one-family-directory scope, PR title, and provenance body aligned |
| Tools and Dependencies | https://googlefonts.github.io/gf-guide/tools.html | `documentation/python-tooling-notes.md`<br>`documentation/local-workflow-readiness.md`<br>`documentation/core-qa-process.md` | documents the local venv, gftools, Fontspector, gftools QA, and reproducible command assumptions |
| Onboarder workflow guide | https://googlefonts.github.io/gf-guide/onboarder-workflow.html | `documentation/submission-handoff-readiness.md`<br>`documentation/kerning-proof-review.md`<br>`documentation/next-actions.md` | keeps generated QA/proof review, Traffic Jam/PR workflow notes, and handoff status visible |
| google/fonts repository explained | https://googlefonts.github.io/gf-guide/googlefonts.html | `documentation/google-fonts-language-metadata.md`<br>`documentation/designer-profile-readiness.md`<br>`documentation/packager-source-strategy.md`<br>`documentation/downstream-pr-readiness.md` | maps downstream family directories, designer catalog files, lang metadata, and upstream.yaml expectations |
| Designer profile guide | https://googlefonts.github.io/gf-guide/profile.html | `documentation/designer-profile-readiness.md`<br>`documentation/designer-profile-package-draft.md`<br>`documentation/designer-profile-candidate/info.pb`<br>`documentation/designer-profile-candidate/bio.html` | tracks designer profile slug, info.pb, bio.html, avatar filename, profile request route, and pending approvals |
| google/fonts Add Font issue template | https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md | `documentation/google-fonts-add-font-template-audit.md`<br>`documentation/google-fonts-add-font-issue-draft.md`<br>`documentation/submission-handoff-readiness.md` | keeps labels, requirement checkboxes, maintenance commitment, and issue text synced with the current template |
| googlefonts/gftools | https://github.com/googlefonts/gftools | `Makefile`<br>`scripts/package_gf_dry_run.sh`<br>`scripts/check_gf_fonts.sh`<br>`documentation/kerning-proof-review.md` | anchors local builder, packager, Fontspector, and gftools QA proof commands to the current toolchain |

## Local Evidence Files

| Local evidence | Exists | Referenced by |
| --- | --- | --- |
| `Makefile` | yes | googlefonts/gftools |
| `documentation/arabic-review-packet.md` | yes | Lang Metadata System |
| `documentation/article-readiness.md` | yes | Article file |
| `documentation/avar-readiness.md` | yes | Variable fonts specifics |
| `documentation/core-qa-process.md` | yes | Production requirements, Tools and Dependencies |
| `documentation/designer-profile-candidate/bio.html` | yes | Designer profile guide |
| `documentation/designer-profile-candidate/info.pb` | yes | Designer profile guide |
| `documentation/designer-profile-package-draft.md` | yes | Designer profile guide |
| `documentation/designer-profile-readiness.md` | yes | google/fonts repository explained, Designer profile guide |
| `documentation/downstream-metadata-diff.md` | yes | Package the fonts, METADATA file |
| `documentation/downstream-metadata-readiness.md` | yes | METADATA file |
| `documentation/downstream-pr-readiness.md` | yes | Package the fonts, Making a PR to Google Fonts, google/fonts repository explained |
| `documentation/final-submission-blockers.md` | yes | Adding & Upgrading Fonts to Google Fonts |
| `documentation/generated-font-metadata.md` | yes | METADATA file |
| `documentation/google-fonts-add-font-issue-draft.md` | yes | Adding & Upgrading Fonts to Google Fonts, google/fonts Add Font issue template |
| `documentation/google-fonts-add-font-template-audit.md` | yes | google/fonts Add Font issue template |
| `documentation/google-fonts-axis-registry-audit.md` | yes | Variable fonts specifics |
| `documentation/google-fonts-downstream-package-preview.md` | yes | METADATA file |
| `documentation/google-fonts-language-metadata.md` | yes | Lang Metadata System, google/fonts repository explained |
| `documentation/google-fonts-metadata-review.md` | yes | Article file |
| `documentation/google-fonts-package-checklist.md` | yes | Article file |
| `documentation/google-fonts-production-requirements.md` | yes | Adding & Upgrading Fonts to Google Fonts, Overall font files requirements, Production requirements, Variable fonts specifics, Build the fonts |
| `documentation/google-fonts-submission-handoff.md` | yes | Making a PR to Google Fonts |
| `documentation/google-fonts-template-and-pr-audit.md` | yes | Article file |
| `documentation/kerning-proof-review.md` | yes | Onboarder workflow guide, googlefonts/gftools |
| `documentation/local-workflow-readiness.md` | yes | Tools and Dependencies |
| `documentation/missing-gf-arabic-core.md` | yes | Overall font files requirements, Lang Metadata System |
| `documentation/missing-gf-latin-core.md` | yes | Overall font files requirements |
| `documentation/next-actions.md` | yes | Onboarder workflow guide |
| `documentation/numeric-feature-readiness.md` | yes | Overall font files requirements, Production requirements |
| `documentation/package-dry-run-readiness.md` | yes | Package the fonts |
| `documentation/package-source-files-audit.md` | yes | Upstream repository structure |
| `documentation/packager-source-strategy.md` | yes | Build the fonts, Package the fonts, google/fonts repository explained |
| `documentation/pr-identity-readiness.md` | yes | Making a PR to Google Fonts |
| `documentation/project-template-automation-readiness.md` | yes | Upstream repository structure |
| `documentation/python-tooling-notes.md` | yes | Tools and Dependencies |
| `documentation/submission-handoff-readiness.md` | yes | Onboarder workflow guide, google/fonts Add Font issue template |
| `documentation/upstream-structure-readiness.md` | yes | Upstream repository structure, Build the fonts |
| `documentation/variable-font-metadata.md` | yes | Variable fonts specifics |
| `scripts/check_gf_fonts.sh` | yes | googlefonts/gftools |
| `scripts/package_gf_dry_run.sh` | yes | googlefonts/gftools |
| `sources/config.yaml` | yes | Build the fonts |

## Maintenance Policy

- Update this index when a local gate starts relying on a new Google
  Fonts guide page, Google Fonts repository file, or gftools behavior.
- Keep generated readiness reports linked here instead of relying on
  memory of prior onboarding work.
- Rerun `make preflight` after changing this index so the reference map
  stays synchronized with the rest of the handoff evidence.
