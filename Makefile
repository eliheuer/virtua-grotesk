PYTHON ?= ./venv/bin/python
DRAWBOT_SKIA_REPO ?= /Users/eli/GH/repos/drawbot-skia
DRAWBOT_PYTHON ?= $(DRAWBOT_SKIA_REPO)/.venv/bin/python
GF_REPO_PATH ?= /Users/eli/GH/forks/fonts
GFT_PACKAGER_SOURCE_MODE ?= latest-release
DESIGNER_PROFILE_NAME ?= Eli Heuer
DESIGNER_PROFILE_AVATAR ?= eliheuer.png
GF_WEIGHT_AXIS_REGISTRY = $(GF_REPO_PATH)/axisregistry/Lib/axisregistry/data/weight.textproto
VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
STATIC_FONTS = fonts/ttf/VirtuaGrotesk-Regular.ttf fonts/ttf/VirtuaGrotesk-Medium.ttf fonts/ttf/VirtuaGrotesk-SemiBold.ttf fonts/ttf/VirtuaGrotesk-Bold.ttf

.PHONY: help decisions decision-readiness-check decision-application-check reference-index-check agent-reuse-check next-actions blockers issue-draft handoff-readiness-check release-check release-archive-check release-archive-build release-archive-verify release-archive-test release-draft-check source-strategy-check package-readiness-check recent-gf-check family-name-check authorship-check pr-readiness-check vendor-id-check kerning-check kerning-proof-check kerning-proof-review-check pua-scope-check avar-check warnings-check github-auth-check designer-profile-check designer-profile-prepare-check designer-profile-info-check designer-profile-image-check designer-profile-bio-check designer-profile-validator-test public-upstream-url-check downstream-metadata-check downstream-metadata-helper-test package-wrapper-test build test reports reports-only proof proof-only preflight preflight-only handoff package-dry-run clean

help:
	@printf '%s\n' \
		'Virtua Grotesk Google Fonts workflow:' \
		'  make decisions      Show priority-sorted Google Fonts decision answer sheet' \
		'  make decision-readiness-check  Show decision log, prompts, and apply-target readiness' \
		'  make decision-application-check  Show which decisions block metadata/package gates' \
		'  make reference-index-check  Show official GF references mapped to local evidence' \
		'  make agent-reuse-check  Show reusable .agents Google Fonts onboarding kit readiness' \
		'  make next-actions   Show owner-grouped Google Fonts next-action queue' \
			'  make blockers       Show final Google Fonts submission blocker summary' \
			'  make issue-draft    Show current Google Fonts Add Font issue draft' \
			'  make handoff-readiness-check  Show handoff freshness, blockers, and next actions' \
			'  make release-check  Show release version, tag, and source-state readiness' \
			'  make release-archive-check  Show release/archive manifest, hashes, and freshness checks' \
			'  make release-archive-build  Build local dist/VirtuaGrotesk-1.000.zip review archive' \
			'  make release-archive-verify  Verify local release/archive zip against source.files' \
			'  make release-archive-test  Test release/archive path-safety gates' \
			'  make release-draft-check  Show GitHub release command and asset draft' \
			'  make source-strategy-check  Show release/source strategy readiness' \
			'  make package-readiness-check  Show packaging, metadata, and downstream PR readiness' \
			'  make recent-gf-check  Compare recent GF packages/upstream repos with this repo' \
			'  make family-name-check  Show family name, namecheck, RFN, and CLA readiness' \
			'  make authorship-check  Show authorship, contact, and AI-disclosure readiness' \
			'  make pr-readiness-check  Show downstream PR identity and scope readiness' \
		'  make vendor-id-check  Show OS/2 vendor ID readiness' \
		'  make kerning-check    Show source, built, and GF visual QA kerning readiness' \
		'  make kerning-proof-check  Run gftools qa HTML proof after QA extras are installed' \
		'  make kerning-proof-review-check  Show gftools QA proof review packet' \
		'  make pua-scope-check  Show private-use glyph scope readiness' \
		'  make avar-check       Show variable-axis avar readiness' \
		'  make warnings-check   Show Fontspector warning triage report' \
		'  make github-auth-check  Check GitHub API credentials for Packager' \
		'  make designer-profile-check  Check Google Fonts designer profile readiness' \
		'  make designer-profile-prepare-check  Dry-run final designer profile install into google/fonts' \
		'  make designer-profile-info-check INFO=path/to/info.pb' \
		'  make designer-profile-image-check IMAGE=path/to/image.png' \
		'  make designer-profile-bio-check BIO=path/to/bio.html' \
		'  make designer-profile-validator-test  Test designer profile validators' \
		'  make public-upstream-url-check  Preview public upstream URL replacements' \
		'  make downstream-metadata-check  Check final METADATA.pb preview readiness' \
		'      accepts GFT_PACKAGER_SOURCE_MODE=latest-release or build-from-source' \
		'  make downstream-metadata-helper-test  Test guarded downstream METADATA.pb helper' \
		'  make package-wrapper-test  Test Packager wrapper metadata gates' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make test           Build, then run Fontspector googlefonts profile' \
		'  make reports        Build, then regenerate all readiness reports' \
		'  make reports-only   Regenerate reports from the current build' \
		'  make preflight      Build, proof, regenerate reports, run local handoff gate' \
		'  make preflight-only Run local handoff gate from current files' \
		'  make proof          Build, then regenerate proof.pdf' \
		'  make handoff        Build once, proof, regenerate reports, preflight' \
		'  make package-dry-run Run gftools packager into local google/fonts fork without -p' \
		'      defaults to GFT_PACKAGER_SOURCE_MODE=latest-release; override with default or build-from-source' \
		'  make clean          Remove generated build outputs'

decisions:
	@$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts-decision-answer-sheet.md
	@cat documentation/google-fonts-decision-answer-sheet.md

decision-readiness-check:
	@$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts-decision-answer-sheet.md
	@$(PYTHON) scripts/report_decision_readiness.py documentation/decision-readiness.md
	@$(PYTHON) scripts/report_decision_application_blockers.py documentation/decision-application-blockers.md
	@cat documentation/google-fonts-decision-answer-sheet.md
	@printf '\n'
	@cat documentation/decision-readiness.md
	@printf '\n'
	@cat documentation/decision-application-blockers.md

decision-application-check:
	@$(PYTHON) scripts/report_decision_application_blockers.py documentation/decision-application-blockers.md
	@cat documentation/decision-application-blockers.md

reference-index-check:
	@$(PYTHON) scripts/report_gf_reference_index.py documentation/google-fonts-reference-index.md
	@cat documentation/google-fonts-reference-index.md

agent-reuse-check:
	@$(PYTHON) scripts/report_agent_reuse_readiness.py documentation/google-fonts-agent-reuse-readiness.md
	@cat documentation/google-fonts-agent-reuse-readiness.md

next-actions:
	@$(PYTHON) scripts/report_next_actions.py documentation/next-actions.md
	@cat documentation/next-actions.md

blockers:
	@$(PYTHON) scripts/report_final_submission_blockers.py documentation/final-submission-blockers.md
	@cat documentation/final-submission-blockers.md

issue-draft:
	@$(PYTHON) scripts/report_gf_add_font_template.py documentation/google-fonts-add-font-template-audit.md
	@$(PYTHON) scripts/report_add_font_issue_draft.py documentation/google-fonts-add-font-issue-draft.md
	@cat documentation/google-fonts-add-font-issue-draft.md

handoff-readiness-check:
	@$(PYTHON) scripts/report_submission_handoff_readiness.py documentation/submission-handoff-readiness.md
	@$(PYTHON) scripts/report_final_submission_blockers.py documentation/final-submission-blockers.md
	@$(PYTHON) scripts/report_next_actions.py documentation/next-actions.md
	@cat documentation/submission-handoff-readiness.md
	@printf '\n'
	@cat documentation/final-submission-blockers.md
	@printf '\n'
	@cat documentation/next-actions.md

release-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/release-metadata.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/release-source-readiness.md
	@$(PYTHON) scripts/report_github_release_draft.py documentation/github-release-draft.md
	@cat documentation/release-metadata.md
	@printf '\n'
	@cat documentation/release-source-readiness.md
	@printf '\n'
	@cat documentation/github-release-draft.md

release-archive-check:
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/release-archive-manifest.md
	@cat documentation/release-archive-manifest.md

release-archive-build:
	@$(PYTHON) scripts/build_release_archive.py
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/release-archive-manifest.md
	@cat documentation/release-archive-manifest.md

release-archive-verify:
	@$(PYTHON) scripts/verify_release_archive.py

release-archive-test:
	./scripts/test_release_archive_gates.sh

release-draft-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/release-metadata.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/release-source-readiness.md
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/release-archive-manifest.md
	@$(PYTHON) scripts/report_github_release_draft.py documentation/github-release-draft.md
	@cat documentation/github-release-draft.md

source-strategy-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/release-metadata.md
	@$(PYTHON) scripts/report_package_source_files.py documentation/package-source-files-audit.md
	@$(PYTHON) scripts/report_packager_source_strategy.py documentation/packager-source-strategy.md
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/release-archive-manifest.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/release-source-readiness.md
	@cat documentation/release-source-readiness.md
	@printf '\n'
	@cat documentation/packager-source-strategy.md
	@printf '\n'
	@cat documentation/release-archive-manifest.md

package-readiness-check:
	@$(PYTHON) scripts/report_package_source_files.py documentation/package-source-files-audit.md
	@$(PYTHON) scripts/report_packager_source_strategy.py documentation/packager-source-strategy.md
	@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/package-dry-run-readiness.md
	@$(PYTHON) scripts/report_downstream_metadata_readiness.py documentation/downstream-metadata-readiness.md
	@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/downstream-metadata-diff.md
	@$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/downstream-pr-readiness.md
	@cat documentation/packager-source-strategy.md
	@printf '\n'
	@cat documentation/package-dry-run-readiness.md
	@printf '\n'
	@cat documentation/downstream-metadata-readiness.md
	@printf '\n'
	@cat documentation/downstream-metadata-diff.md
	@printf '\n'
	@cat documentation/downstream-pr-readiness.md

recent-gf-check:
	@$(PYTHON) scripts/report_recent_gf_packages.py documentation/recent-google-fonts-packages.md
	@cat documentation/recent-google-fonts-packages.md

family-name-check:
	@$(PYTHON) scripts/report_family_name_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/family-name-readiness.md
	@cat documentation/family-name-readiness.md

authorship-check:
	@$(PYTHON) scripts/report_authorship_disclosure_readiness.py documentation/authorship-disclosure-readiness.md
	@cat documentation/authorship-disclosure-readiness.md

pr-readiness-check:
	@$(PYTHON) scripts/report_pr_identity_readiness.py documentation/pr-identity-readiness.md
	@$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/downstream-pr-readiness.md
	@cat documentation/pr-identity-readiness.md
	@printf '\n'
	@cat documentation/downstream-pr-readiness.md

vendor-id-check:
	@$(PYTHON) scripts/report_vendor_id_readiness.py documentation/vendor-id-readiness.md
	@cat documentation/vendor-id-readiness.md

kerning-check:
	@$(PYTHON) scripts/report_kerning_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/kerning-readiness.md
	@$(PYTHON) scripts/report_kerning_proof_review.py documentation/kerning-proof-review.md
	@cat documentation/kerning-readiness.md
	@printf '\n'
	@cat documentation/kerning-proof-review.md

kerning-proof-check:
	@PATH="$(CURDIR)/venv/bin:$$PATH" venv/bin/gftools qa --proof -f '$(VARIABLE_FONT)' -o documentation/gftools-qa

kerning-proof-review-check:
	@$(PYTHON) scripts/report_kerning_proof_review.py documentation/kerning-proof-review.md
	@cat documentation/kerning-proof-review.md

pua-scope-check:
	@$(PYTHON) scripts/report_pua_scope.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/pua-scope.md
	@cat documentation/pua-scope.md

avar-check:
	@$(PYTHON) scripts/report_avar_readiness.py '$(VARIABLE_FONT)' documentation/avar-readiness.md
	@cat documentation/avar-readiness.md

warnings-check:
	@$(PYTHON) scripts/report_fontspector_warnings.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/fontspector-warnings.md
	@cat documentation/fontspector-warnings.md

github-auth-check:
	@$(PYTHON) scripts/check_github_api_auth.py

designer-profile-check:
	@$(PYTHON) scripts/report_designer_profile.py documentation/designer-profile-readiness.md
	@$(PYTHON) scripts/report_designer_profile_package.py documentation/designer-profile-package-draft.md
	@cat documentation/designer-profile-readiness.md
	@printf '\n'
	@cat documentation/designer-profile-package-draft.md

designer-profile-prepare-check:
	@$(PYTHON) scripts/prepare_designer_profile.py

designer-profile-info-check:
	@test -n "$(INFO)" || (echo "Set INFO=path/to/info.pb" && exit 2)
	@$(PYTHON) scripts/validate_designer_profile_info.py "$(INFO)" "$(DESIGNER_PROFILE_NAME)" "$(DESIGNER_PROFILE_AVATAR)"

designer-profile-image-check:
	@test -n "$(IMAGE)" || (echo "Set IMAGE=path/to/designer-profile-image.png" && exit 2)
	@$(PYTHON) scripts/validate_designer_profile_image.py "$(IMAGE)" "$(DESIGNER_PROFILE_AVATAR)"

designer-profile-bio-check:
	@test -n "$(BIO)" || (echo "Set BIO=path/to/bio.html" && exit 2)
	@$(PYTHON) scripts/validate_designer_profile_bio.py "$(BIO)"

designer-profile-validator-test:
	./scripts/test_designer_profile_validators.sh

public-upstream-url-check:
	@$(PYTHON) scripts/apply_public_upstream_url.py

downstream-metadata-check:
	@GF_REPO_PATH='$(GF_REPO_PATH)' GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/prepare_downstream_metadata.py --gf-repo '$(GF_REPO_PATH)' --source-mode '$(GFT_PACKAGER_SOURCE_MODE)'

downstream-metadata-helper-test:
	./scripts/test_downstream_metadata_helper.sh

package-wrapper-test:
	./scripts/test_package_gf_dry_run_gates.sh

build:
	./build.sh

test: build
	./scripts/check_gf_fonts.sh

reports: build
	$(MAKE) reports-only

reports-only:
	$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts-decision-answer-sheet.md
	$(PYTHON) scripts/report_decision_readiness.py documentation/decision-readiness.md
	$(PYTHON) scripts/report_gf_reference_index.py documentation/google-fonts-reference-index.md
	$(PYTHON) scripts/report_agent_reuse_readiness.py documentation/google-fonts-agent-reuse-readiness.md
	$(PYTHON) scripts/report_source_metadata.py sources/VirtuaGrotesk-Regular.ufo sources/VirtuaGrotesk-Bold.ufo documentation/source-ufo-metadata.md
	$(PYTHON) scripts/report_master_compatibility.py sources/VirtuaGrotesk-Regular.ufo sources/VirtuaGrotesk-Bold.ufo documentation/master-compatibility.md
	$(PYTHON) scripts/report_generated_font_metadata.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/generated-font-metadata.md
	$(PYTHON) scripts/report_vendor_id_readiness.py documentation/vendor-id-readiness.md
	$(PYTHON) scripts/report_release_metadata.py documentation/release-metadata.md
	$(PYTHON) scripts/report_release_source_readiness.py documentation/release-source-readiness.md
	$(PYTHON) scripts/report_release_archive_manifest.py documentation/release-archive-manifest.md
	$(PYTHON) scripts/report_github_release_draft.py documentation/github-release-draft.md
	$(PYTHON) scripts/report_upstream_structure_readiness.py documentation/upstream-structure-readiness.md
	$(PYTHON) scripts/report_family_name_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/family-name-readiness.md
	$(PYTHON) scripts/report_authorship_disclosure_readiness.py documentation/authorship-disclosure-readiness.md
	$(PYTHON) scripts/report_pr_identity_readiness.py documentation/pr-identity-readiness.md
	$(PYTHON) scripts/report_drawbot_runtime_readiness.py documentation/drawbot-runtime-readiness.md
	GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/package-dry-run-readiness.md
	$(PYTHON) scripts/report_local_workflow_readiness.py documentation/local-workflow-readiness.md
	$(PYTHON) scripts/report_designer_profile.py documentation/designer-profile-readiness.md
	$(PYTHON) scripts/report_designer_profile_package.py documentation/designer-profile-package-draft.md
	$(PYTHON) scripts/report_variable_metadata.py '$(VARIABLE_FONT)' documentation/variable-font-metadata.md
	$(PYTHON) scripts/report_avar_readiness.py '$(VARIABLE_FONT)' documentation/avar-readiness.md
	$(PYTHON) scripts/report_axis_registry.py '$(VARIABLE_FONT)' '$(GF_WEIGHT_AXIS_REGISTRY)' documentation/google-fonts-axis-registry-audit.md
	$(PYTHON) scripts/report_gf_glyphset_readiness.py '$(VARIABLE_FONT)' documentation/gf-glyphset-readiness.md
	$(PYTHON) scripts/report_gf_language_metadata.py documentation/google-fonts-language-metadata.md
	$(PYTHON) scripts/report_missing_gf_latin_core.py '$(VARIABLE_FONT)' documentation/missing-gf-latin-core.md
	$(PYTHON) scripts/report_missing_gf_arabic_core.py '$(VARIABLE_FONT)' documentation/missing-gf-arabic-core.md
	$(PYTHON) scripts/report_arabic_source_checklist.py '$(VARIABLE_FONT)' documentation/arabic-source-work-checklist.md
	$(PYTHON) scripts/report_pua_scope.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/pua-scope.md
	$(PYTHON) scripts/report_public_upstream_readiness.py documentation/public-upstream-readiness.md
	$(PYTHON) scripts/report_open_placeholders.py documentation/open-placeholder-audit.md
	$(PYTHON) scripts/report_package_source_files.py documentation/package-source-files-audit.md
	$(PYTHON) scripts/report_packager_source_strategy.py documentation/packager-source-strategy.md
	$(PYTHON) scripts/report_downstream_metadata_readiness.py documentation/downstream-metadata-readiness.md
	GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/downstream-metadata-diff.md
	$(PYTHON) scripts/report_decision_application_blockers.py documentation/decision-application-blockers.md
	$(PYTHON) scripts/report_article_readiness.py documentation/article-readiness.md
	$(PYTHON) scripts/report_kerning_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/kerning-readiness.md
	$(PYTHON) scripts/report_kerning_proof_review.py documentation/kerning-proof-review.md
	$(PYTHON) scripts/report_arabic_mark_readiness.py documentation/arabic-mark-readiness.md
	$(PYTHON) scripts/report_arabic_shaping.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/arabic-shaping-smoke-test.md
	$(PYTHON) scripts/report_arabic_review_packet.py documentation/arabic-review-packet.md
	$(PYTHON) scripts/report_glyph_reachability.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/glyph-reachability.md
	$(PYTHON) scripts/report_numeric_feature_readiness.py documentation/numeric-feature-readiness.md
	$(PYTHON) scripts/report_fontspector_contours.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/fontspector-contour-count.md
	$(PYTHON) scripts/report_fontspector_warnings.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/fontspector-warnings.md
	./scripts/report_fontspector_markdown.sh documentation/fontspector-googlefonts-report.md
	$(PYTHON) scripts/report_production_requirements.py documentation/google-fonts-production-requirements.md
	$(PYTHON) scripts/report_recent_gf_packages.py documentation/recent-google-fonts-packages.md
	$(PYTHON) scripts/report_gf_add_font_template.py documentation/google-fonts-add-font-template-audit.md
	$(PYTHON) scripts/report_add_font_issue_draft.py documentation/google-fonts-add-font-issue-draft.md
	$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/downstream-pr-readiness.md
	$(PYTHON) scripts/report_project_template_automation.py documentation/project-template-automation-readiness.md
	$(PYTHON) scripts/report_submission_handoff_readiness.py documentation/submission-handoff-readiness.md
	$(PYTHON) scripts/report_final_submission_blockers.py documentation/final-submission-blockers.md
	$(PYTHON) scripts/report_next_actions.py documentation/next-actions.md

proof: build
	$(MAKE) proof-only

proof-only:
	PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH}" $(DRAWBOT_PYTHON) proof.py fonts/ttf/VirtuaGrotesk-Regular.ttf proof.pdf

preflight: build
	$(MAKE) proof-only
	$(MAKE) reports-only
	$(MAKE) preflight-only

preflight-only:
	$(PYTHON) scripts/gf_preflight.py

handoff: build
	$(MAKE) proof-only
	$(MAKE) reports-only
	$(MAKE) preflight-only

package-dry-run:
	GF_REPO_PATH='$(GF_REPO_PATH)' GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' ./scripts/package_gf_dry_run.sh

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/instance_ufos
