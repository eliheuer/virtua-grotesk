PYTHON ?= ./venv/bin/python
DRAWBOT_SKIA_REPO ?= /Users/eli/GH/repos/drawbot-skia
DRAWBOT_PYTHON ?= $(PYTHON)
GF_REPO_PATH ?= /Users/eli/GH/forks/fonts
GFT_PACKAGER_SOURCE_MODE ?= latest-release
DESIGNER_PROFILE_NAME ?= Eli Heuer
DESIGNER_PROFILE_AVATAR ?= eliheuer.png
GF_WEIGHT_AXIS_REGISTRY = $(GF_REPO_PATH)/axisregistry/Lib/axisregistry/data/weight.textproto
VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
STATIC_FONTS = fonts/ttf/VirtuaGrotesk-Regular.ttf fonts/ttf/VirtuaGrotesk-Medium.ttf fonts/ttf/VirtuaGrotesk-SemiBold.ttf fonts/ttf/VirtuaGrotesk-Bold.ttf

.PHONY: help decisions decision-readiness-check decision-application-check reference-index-check agent-reuse-check next-actions blockers issue-draft handoff-readiness-check release-check release-archive-check release-archive-build release-archive-verify release-archive-test release-draft-check source-strategy-check package-readiness-check recent-gf-check family-name-check authorship-check pr-readiness-check vendor-id-check kerning-check kerning-proof-check kerning-proof-review-check contour-cleanup-proof contour-decision-update contour-decision-helper-test ufo-editor-check runebender-ufo-check pua-scope-check avar-check warnings-check metadata-warning-check zero-warning-check github-auth-check designer-profile-check designer-profile-prepare-check designer-profile-info-check designer-profile-image-check designer-profile-bio-check designer-profile-validator-test public-upstream-url-check downstream-metadata-check downstream-metadata-helper-test package-wrapper-test arabic-visual-review-helper-test arabic-candidate-plan arabic-goal-audit print-spacing-specimen print-spacing-specimen-only arabic-print-proof arabic-print-proof-only arabic-visual-risk-proof arabic-structure-sweep arabic-structure-triage arabic-mark-review-proof arabic-mark-triage arabic-manual-review-dashboard arabic-manual-review-batches arabic-review-progress arabic-current-review-worksheet arabic-review-worksheet-bundle arabic-drawing-session-checklist arabic-source-edit-diff-check arabic-first-batch-source-checkpoint arabic-pending-source-checkpoint arabic-before-drawing-check arabic-after-drawing-check arabic-visual-review-batch-tsv arabic-batch-recorder arabic-first-review-zoom-snapshots arabic-first-review-crop-integrity arabic-first-review-batch arabic-first-review-risk-shortlist arabic-manual-edit-targets arabic-hand-review-session arabic-hand-review-contact-sheet arabic-next-review-packet arabic-next-review-ai-triage arabic-next-review-ai-observations arabic-full-queue-ai-sweep arabic-next-review-board arabic-next-review-snapshots arabic-snapshot-integrity arabic-visual-review-runbook arabic-visual-review-check arabic-visual-review-log arabic-visual-review-update arabic-visual-review-batch-dry-run arabic-visual-review-batch-update arabic-visual-review-batch-apply-check build test reports reports-only proof proof-only preflight preflight-only handoff package-dry-run clean

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
		'  make contour-cleanup-proof  Render remaining contour-count findings to HTML' \
		'  make contour-decision-update GLYPH=dad-ar.fina STATUS=fix-now DECISION="redraw"  Update contour decision log' \
		'  make contour-decision-helper-test  Test guarded contour decision updater' \
		'  make ufo-editor-check  Check active UFOs are readable before hand cleanup' \
		'  make runebender-ufo-check  Check active UFOs with Runebender/Norad loader deps' \
		'  make pua-scope-check  Show private-use glyph scope readiness' \
		'  make avar-check       Show variable-axis avar readiness' \
		'  make warnings-check   Show Fontspector warning triage report' \
		'  make metadata-warning-check  Probe warning state with preview METADATA.pb' \
		'  make zero-warning-check  Show concrete worklist to reach zero Fontspector warnings' \
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
		'  make arabic-visual-review-helper-test  Test guarded Arabic visual review updater' \
		'  make arabic-candidate-plan  Dry-run candidate glyph creation plan for Arabic gaps' \
		'  make arabic-goal-audit  Show Arabic missing-drawings goal completion audit' \
		'  make print-spacing-specimen  Build landscape PDF specimen for print weight/spacing review' \
		'  make arabic-visual-risk-proof  Build focused proof for visual-risk sidebearing rows' \
		'  make arabic-structure-sweep  Build GF Arabic Core structure/wrong-glyph sweep' \
		'  make arabic-structure-triage  Show mechanical triage for structure review' \
		'  make arabic-mark-review-proof  Build focused Arabic mark attachment proof' \
		'  make arabic-mark-triage  Show mechanical triage for mark review' \
		'  make arabic-manual-review-dashboard  Build one-page Arabic manual review dashboard' \
		'  make arabic-manual-review-batches  Show compact Arabic hand-review batch queue' \
		'  make arabic-review-progress  Show concise Arabic visual review progress and next commands' \
		'  make arabic-current-review-worksheet  Show fill-in worksheet for current Arabic review batch' \
		'  make arabic-review-worksheet-bundle  Show fill-in worksheets for all pending Arabic batches' \
		'  make arabic-drawing-session-checklist  Show compact hand-drawing session checklist' \
		'  make arabic-source-edit-diff-check  Show changed Arabic GLIF pairing status' \
		'  make arabic-before-drawing-check  Run source-load checks before opening UFOs for drawing' \
		'  make arabic-after-drawing-check  Run source checks, build, reports, and preflight after Arabic edits' \
		'  make arabic-visual-review-batch-tsv  Generate TSV template for the current Arabic review batch' \
		'  make arabic-batch-recorder  Show guarded commands for the current Arabic review batch' \
		'  make arabic-first-review-zoom-snapshots  Crop Arabic-row zoom PNGs for the current batch' \
		'  make arabic-first-review-crop-integrity  Check focused Arabic-row crop PNG integrity' \
		'  make arabic-first-review-batch  Show one-session worksheet for the next Arabic review batch' \
		'  make arabic-first-review-risk-shortlist  Show AI-visible risk shortlist for the first review batch' \
		'  make arabic-manual-edit-targets  Show source GLIF targets for fix-needed Arabic rows' \
		'  make arabic-hand-review-session  Show compact session sheet for remaining Arabic review' \
		'  make arabic-hand-review-contact-sheet  Build print-friendly Arabic review snapshot sheet' \
		'  make arabic-next-review-packet  Show the smallest current Arabic hand-review packet' \
		'  make arabic-next-review-ai-triage  Show AI-safe triage for the current Arabic hand-review packet' \
		'  make arabic-next-review-ai-observations  Show AI visual observations for first-batch snapshots' \
		'  make arabic-full-queue-ai-sweep  Show AI-safe visual observations for all pending Arabic rows' \
		'  make arabic-next-review-board  Build local HTML board for current Arabic hand-review packet' \
		'  make arabic-next-review-snapshots  Render PNGs for the current Arabic hand-review packet' \
		'      accepts ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --timeout 20" for full queue' \
		'      use ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --list-only --timeout 20" to verify coverage without Chrome' \
		'      use ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --reuse-existing" to rebuild the contact sheet from existing PNGs' \
		'  make arabic-snapshot-integrity  Validate Arabic review PNG coverage and nonblank renders' \
		'  make arabic-visual-review-runbook  Show row-by-row Arabic visual review cards' \
		'  make arabic-visual-review-check  Show Arabic visual proof review checklist' \
		'  make arabic-visual-review-log  Show editable Arabic visual review log' \
		'  make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD"  Update visual review log' \
		'  make arabic-visual-review-batch-dry-run REVIEW_BATCH=review.tsv  Validate visual review TSV without writing' \
		'  make arabic-visual-review-batch-update REVIEW_BATCH=review.tsv  Update visual review log from TSV' \
		'  make arabic-visual-review-batch-apply-check REVIEW_BATCH=review.tsv  Apply TSV, regenerate reports, and preflight' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make test           Build, then run Fontspector googlefonts profile' \
		'  make reports        Build, then regenerate all readiness reports' \
		'  make reports-only   Regenerate reports from the current build' \
		'  make preflight      Build, proof, regenerate reports, run local handoff gate' \
		'  make preflight-only Run local handoff gate from current files' \
		'  make proof          Build, then regenerate documentation/proofs/proof.pdf' \
		'  make handoff        Build once, proof, regenerate reports, preflight' \
		'  make package-dry-run Run gftools packager into local google/fonts fork without -p' \
		'      defaults to GFT_PACKAGER_SOURCE_MODE=latest-release; override with default or build-from-source' \
		'  make clean          Remove generated build outputs'

decisions:
	@$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts/google-fonts-decision-answer-sheet.md
	@cat documentation/google-fonts/google-fonts-decision-answer-sheet.md

decision-readiness-check:
	@$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts/google-fonts-decision-answer-sheet.md
	@$(PYTHON) scripts/report_decision_readiness.py documentation/google-fonts/decision-readiness.md
	@$(PYTHON) scripts/report_decision_application_blockers.py documentation/google-fonts/decision-application-blockers.md
	@cat documentation/google-fonts/google-fonts-decision-answer-sheet.md
	@printf '\n'
	@cat documentation/google-fonts/decision-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/decision-application-blockers.md

decision-application-check:
	@$(PYTHON) scripts/report_decision_application_blockers.py documentation/google-fonts/decision-application-blockers.md
	@cat documentation/google-fonts/decision-application-blockers.md

reference-index-check:
	@$(PYTHON) scripts/report_gf_reference_index.py documentation/google-fonts/google-fonts-reference-index.md
	@cat documentation/google-fonts/google-fonts-reference-index.md

agent-reuse-check:
	@$(PYTHON) scripts/report_agent_reuse_readiness.py documentation/google-fonts/google-fonts-agent-reuse-readiness.md
	@cat documentation/google-fonts/google-fonts-agent-reuse-readiness.md

next-actions:
	@$(PYTHON) scripts/report_next_actions.py documentation/google-fonts/next-actions.md
	@cat documentation/google-fonts/next-actions.md

blockers:
	@$(PYTHON) scripts/report_final_submission_blockers.py documentation/google-fonts/final-submission-blockers.md
	@cat documentation/google-fonts/final-submission-blockers.md

issue-draft:
	@$(PYTHON) scripts/report_gf_add_font_template.py documentation/google-fonts/google-fonts-add-font-template-audit.md
	@$(PYTHON) scripts/report_add_font_issue_draft.py documentation/google-fonts/google-fonts-add-font-issue-draft.md
	@cat documentation/google-fonts/google-fonts-add-font-issue-draft.md

handoff-readiness-check:
	@$(PYTHON) scripts/report_submission_handoff_readiness.py documentation/google-fonts/submission-handoff-readiness.md
	@$(PYTHON) scripts/report_final_submission_blockers.py documentation/google-fonts/final-submission-blockers.md
	@$(PYTHON) scripts/report_next_actions.py documentation/google-fonts/next-actions.md
	@cat documentation/google-fonts/submission-handoff-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/final-submission-blockers.md
	@printf '\n'
	@cat documentation/google-fonts/next-actions.md

release-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/google-fonts/release-metadata.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/google-fonts/release-source-readiness.md
	@$(PYTHON) scripts/report_github_release_draft.py documentation/google-fonts/github-release-draft.md
	@cat documentation/google-fonts/release-metadata.md
	@printf '\n'
	@cat documentation/google-fonts/release-source-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/github-release-draft.md

release-archive-check:
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	@cat documentation/google-fonts/release-archive-manifest.md

release-archive-build:
	@$(PYTHON) scripts/build_release_archive.py
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	@cat documentation/google-fonts/release-archive-manifest.md

release-archive-verify:
	@$(PYTHON) scripts/verify_release_archive.py

release-archive-test:
	./scripts/test_release_archive_gates.sh

release-draft-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/google-fonts/release-metadata.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/google-fonts/release-source-readiness.md
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	@$(PYTHON) scripts/report_github_release_draft.py documentation/google-fonts/github-release-draft.md
	@cat documentation/google-fonts/github-release-draft.md

source-strategy-check:
	@$(PYTHON) scripts/report_release_metadata.py documentation/google-fonts/release-metadata.md
	@$(PYTHON) scripts/report_package_source_files.py documentation/google-fonts/package-source-files-audit.md
	@$(PYTHON) scripts/report_packager_source_strategy.py documentation/google-fonts/packager-source-strategy.md
	@$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	@$(PYTHON) scripts/report_release_source_readiness.py documentation/google-fonts/release-source-readiness.md
	@cat documentation/google-fonts/release-source-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/packager-source-strategy.md
	@printf '\n'
	@cat documentation/google-fonts/release-archive-manifest.md

package-readiness-check:
	@$(PYTHON) scripts/report_package_source_files.py documentation/google-fonts/package-source-files-audit.md
	@$(PYTHON) scripts/report_packager_source_strategy.py documentation/google-fonts/packager-source-strategy.md
	@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/google-fonts/package-dry-run-readiness.md
	@$(PYTHON) scripts/report_downstream_metadata_readiness.py documentation/google-fonts/downstream-metadata-readiness.md
	@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/google-fonts/downstream-metadata-diff.md
	@$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/google-fonts/downstream-pr-readiness.md
	@cat documentation/google-fonts/packager-source-strategy.md
	@printf '\n'
	@cat documentation/google-fonts/package-dry-run-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/downstream-metadata-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/downstream-metadata-diff.md
	@printf '\n'
	@cat documentation/google-fonts/downstream-pr-readiness.md

recent-gf-check:
	@$(PYTHON) scripts/report_recent_gf_packages.py documentation/google-fonts/recent-google-fonts-packages.md
	@cat documentation/google-fonts/recent-google-fonts-packages.md

family-name-check:
	@$(PYTHON) scripts/report_family_name_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/family-name-readiness.md
	@cat documentation/google-fonts/family-name-readiness.md

authorship-check:
	@$(PYTHON) scripts/report_authorship_disclosure_readiness.py documentation/google-fonts/authorship-disclosure-readiness.md
	@cat documentation/google-fonts/authorship-disclosure-readiness.md

pr-readiness-check:
	@$(PYTHON) scripts/report_pr_identity_readiness.py documentation/google-fonts/pr-identity-readiness.md
	@$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/google-fonts/downstream-pr-readiness.md
	@cat documentation/google-fonts/pr-identity-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/downstream-pr-readiness.md

vendor-id-check:
	@$(PYTHON) scripts/report_vendor_id_readiness.py documentation/google-fonts/vendor-id-readiness.md
	@cat documentation/google-fonts/vendor-id-readiness.md

kerning-check:
	@$(PYTHON) scripts/report_kerning_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/kerning-readiness.md
	@$(PYTHON) scripts/report_kerning_proof_review.py documentation/google-fonts/kerning-proof-review.md
	@cat documentation/google-fonts/kerning-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/kerning-proof-review.md

kerning-proof-check:
	@PATH="$(CURDIR)/venv/bin:$$PATH" venv/bin/gftools qa --proof -f '$(VARIABLE_FONT)' -o documentation/google-fonts/gftools-qa

kerning-proof-review-check:
	@$(PYTHON) scripts/report_kerning_proof_review.py documentation/google-fonts/kerning-proof-review.md
	@cat documentation/google-fonts/kerning-proof-review.md

contour-cleanup-proof:
	@$(PYTHON) scripts/build_contour_cleanup_proof.py

GLYPH ?= dad-ar.fina
STATUS ?= fix-now
DECISION ?= pending
NOTES ?=
REVIEWED ?=

contour-decision-update:
	@$(PYTHON) scripts/update_contour_decision.py '$(GLYPH)' --status '$(STATUS)' --decision '$(DECISION)' --notes '$(NOTES)' --reviewed '$(REVIEWED)' --apply

contour-decision-helper-test:
	./scripts/test_contour_decision_update.sh

ufo-editor-check:
	@$(PYTHON) scripts/report_ufo_editor_readiness.py documentation/source/ufo-editor-readiness.md
	@cat documentation/source/ufo-editor-readiness.md

runebender-ufo-check:
	./scripts/check_runebender_norad_load.sh

pua-scope-check:
	@$(PYTHON) scripts/report_pua_scope.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/pua-scope.md
	@cat documentation/google-fonts/pua-scope.md

avar-check:
	@$(PYTHON) scripts/report_avar_readiness.py '$(VARIABLE_FONT)' documentation/google-fonts/avar-readiness.md
	@cat documentation/google-fonts/avar-readiness.md

warnings-check:
	@$(PYTHON) scripts/report_metadata_warning_probe.py documentation/google-fonts/fontspector-metadata-warning-probe.md
	@$(PYTHON) scripts/report_zero_warning_worklist.py '$(VARIABLE_FONT)' documentation/google-fonts/fontspector-zero-warning-worklist.md
	@$(PYTHON) scripts/report_fontspector_warnings.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/fontspector-warnings.md
	@cat documentation/google-fonts/fontspector-warnings.md

metadata-warning-check:
	@$(PYTHON) scripts/report_metadata_warning_probe.py documentation/google-fonts/fontspector-metadata-warning-probe.md
	@cat documentation/google-fonts/fontspector-metadata-warning-probe.md

zero-warning-check:
	@$(PYTHON) scripts/report_zero_warning_worklist.py '$(VARIABLE_FONT)' documentation/google-fonts/fontspector-zero-warning-worklist.md
	@cat documentation/google-fonts/fontspector-zero-warning-worklist.md

github-auth-check:
	@$(PYTHON) scripts/check_github_api_auth.py

designer-profile-check:
	@$(PYTHON) scripts/report_designer_profile.py documentation/google-fonts/designer-profile-readiness.md
	@$(PYTHON) scripts/report_designer_profile_package.py documentation/google-fonts/designer-profile-package-draft.md
	@cat documentation/google-fonts/designer-profile-readiness.md
	@printf '\n'
	@cat documentation/google-fonts/designer-profile-package-draft.md

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

arabic-visual-review-helper-test:
	./scripts/test_arabic_visual_review_update.sh

arabic-candidate-plan:
	$(PYTHON) scripts/build_arabic_candidate_glyphs.py --output documentation/glyph-review/arabic-candidate-glyph-plan.md
	@cat documentation/glyph-review/arabic-candidate-glyph-plan.md

arabic-goal-audit:
	@$(PYTHON) scripts/report_arabic_goal_completion.py documentation/glyph-review/arabic-goal-completion-audit.md
	@cat documentation/glyph-review/arabic-goal-completion-audit.md

arabic-visual-risk-proof:
	@$(PYTHON) scripts/report_arabic_visual_risk.py documentation/glyph-review/arabic-visual-risk-audit.md
	@$(PYTHON) scripts/build_arabic_visual_risk_proof.py documentation/glyph-review/arabic-visual-risk-proof.html

arabic-structure-sweep:
	@$(PYTHON) scripts/build_arabic_structure_sweep.py documentation/glyph-review/arabic-structure-sweep.html

arabic-structure-triage:
	@$(PYTHON) scripts/report_arabic_structure_triage.py documentation/glyph-review/arabic-structure-triage.md
	@cat documentation/glyph-review/arabic-structure-triage.md

arabic-mark-review-proof:
	@$(PYTHON) scripts/build_arabic_mark_review_proof.py documentation/glyph-review/arabic-mark-review-proof.html

arabic-mark-triage:
	@$(PYTHON) scripts/report_arabic_mark_triage.py documentation/glyph-review/arabic-mark-triage.md
	@cat documentation/glyph-review/arabic-mark-triage.md

arabic-manual-review-dashboard:
	@$(PYTHON) scripts/build_arabic_manual_review_dashboard.py documentation/glyph-review/arabic-manual-review-dashboard.html

arabic-manual-review-batches:
	@$(PYTHON) scripts/report_arabic_manual_review_batches.py documentation/glyph-review/arabic-manual-review-batches.md
	@cat documentation/glyph-review/arabic-manual-review-batches.md

arabic-review-progress:
	@$(PYTHON) scripts/report_arabic_review_progress.py documentation/glyph-review/arabic-review-progress.md
	@cat documentation/glyph-review/arabic-review-progress.md

arabic-current-review-worksheet:
	@$(PYTHON) scripts/report_arabic_current_review_worksheet.py documentation/glyph-review/arabic-current-review-worksheet.md
	@cat documentation/glyph-review/arabic-current-review-worksheet.md

arabic-review-worksheet-bundle:
	@$(PYTHON) scripts/report_arabic_review_worksheet_bundle.py documentation/glyph-review/arabic-review-worksheet-bundle.md
	@cat documentation/glyph-review/arabic-review-worksheet-bundle.md

arabic-drawing-session-checklist:
	@$(PYTHON) scripts/report_arabic_drawing_session_checklist.py documentation/glyph-review/arabic-drawing-session-checklist.md
	@cat documentation/glyph-review/arabic-drawing-session-checklist.md

arabic-source-edit-diff-check:
	@$(PYTHON) scripts/report_arabic_source_edit_diff.py documentation/glyph-review/arabic-source-edit-diff.md --fail-on-gap
	@cat documentation/glyph-review/arabic-source-edit-diff.md

arabic-first-batch-source-checkpoint:
	@$(PYTHON) scripts/report_arabic_first_batch_source_checkpoint.py documentation/glyph-review/arabic-first-batch-source-checkpoint.md
	@cat documentation/glyph-review/arabic-first-batch-source-checkpoint.md

arabic-pending-source-checkpoint:
	@$(PYTHON) scripts/report_arabic_pending_source_checkpoint.py documentation/glyph-review/arabic-pending-source-checkpoint.md
	@cat documentation/glyph-review/arabic-pending-source-checkpoint.md

arabic-before-drawing-check: ufo-editor-check runebender-ufo-check

arabic-after-drawing-check: ufo-editor-check runebender-ufo-check build reports-only preflight-only

arabic-visual-review-batch-tsv:
	@$(PYTHON) scripts/report_arabic_visual_review_batch_tsv.py documentation/glyph-review/arabic-visual-review-batch.tsv
	@cat documentation/glyph-review/arabic-visual-review-batch.tsv

arabic-batch-recorder:
	@$(PYTHON) scripts/report_arabic_batch_recorder.py documentation/glyph-review/arabic-batch-recorder.md
	@cat documentation/glyph-review/arabic-batch-recorder.md

arabic-first-review-zoom-snapshots:
	@$(PYTHON) scripts/build_arabic_first_review_zoom_snapshots.py documentation/glyph-review/arabic-first-review-zoom-snapshots.md
	@cat documentation/glyph-review/arabic-first-review-zoom-snapshots.md

arabic-first-review-crop-integrity:
	@$(PYTHON) scripts/report_arabic_first_review_crop_integrity.py documentation/glyph-review/arabic-first-review-crop-integrity.md
	@cat documentation/glyph-review/arabic-first-review-crop-integrity.md

arabic-first-review-batch:
	@$(PYTHON) scripts/report_arabic_first_review_batch.py documentation/glyph-review/arabic-first-review-batch.md
	@cat documentation/glyph-review/arabic-first-review-batch.md

arabic-first-review-risk-shortlist:
	@$(PYTHON) scripts/report_arabic_first_review_risk_shortlist.py documentation/glyph-review/arabic-first-review-risk-shortlist.md
	@cat documentation/glyph-review/arabic-first-review-risk-shortlist.md

arabic-manual-edit-targets:
	@$(PYTHON) scripts/report_arabic_manual_edit_targets.py documentation/glyph-review/arabic-manual-edit-targets.md
	@cat documentation/glyph-review/arabic-manual-edit-targets.md

arabic-hand-review-session:
	@$(PYTHON) scripts/report_arabic_hand_review_session.py documentation/glyph-review/arabic-hand-review-session.md
	@cat documentation/glyph-review/arabic-hand-review-session.md

arabic-hand-review-contact-sheet:
	@$(PYTHON) scripts/build_arabic_hand_review_contact_sheet.py documentation/glyph-review/arabic-hand-review-contact-sheet.html

arabic-next-review-packet:
	@$(PYTHON) scripts/report_arabic_next_review_packet.py documentation/glyph-review/arabic-next-review-packet.md
	@cat documentation/glyph-review/arabic-next-review-packet.md

arabic-next-review-ai-triage:
	@$(PYTHON) scripts/report_arabic_next_review_ai_triage.py documentation/glyph-review/arabic-next-review-ai-triage.md
	@cat documentation/glyph-review/arabic-next-review-ai-triage.md

arabic-next-review-ai-observations:
	@$(PYTHON) scripts/report_arabic_next_review_ai_observations.py documentation/glyph-review/arabic-next-review-ai-observations.md
	@cat documentation/glyph-review/arabic-next-review-ai-observations.md

arabic-full-queue-ai-sweep:
	@$(PYTHON) scripts/report_arabic_full_queue_ai_sweep.py documentation/glyph-review/arabic-full-queue-ai-sweep.md
	@cat documentation/glyph-review/arabic-full-queue-ai-sweep.md

arabic-next-review-board:
	@$(PYTHON) scripts/build_arabic_next_review_board.py documentation/glyph-review/arabic-next-review-board.html

arabic-next-review-snapshots:
	@$(PYTHON) scripts/build_arabic_next_review_snapshots.py $(ARABIC_SNAPSHOT_ARGS)
	@cat documentation/glyph-review/arabic-next-review-snapshots.md

arabic-snapshot-integrity:
	@$(PYTHON) scripts/report_arabic_snapshot_integrity.py documentation/glyph-review/arabic-snapshot-integrity.md
	@cat documentation/glyph-review/arabic-snapshot-integrity.md

arabic-visual-review-runbook:
	@$(PYTHON) scripts/report_arabic_visual_review_runbook.py documentation/glyph-review/arabic-visual-review-runbook.md
	@cat documentation/glyph-review/arabic-visual-review-runbook.md

arabic-visual-review-check:
	@cat documentation/glyph-review/arabic-visual-review-checklist.md

arabic-visual-review-log:
	@$(PYTHON) scripts/report_arabic_visual_review_log.py documentation/glyph-review/arabic-visual-review-log.md
	@cat documentation/glyph-review/arabic-visual-review-log.md

REVIEW_KEY ?= proof-regular-glyphs
REVIEW_STATUS ?= pass
REVIEWER ?=
REVIEW_BATCH ?= documentation/glyph-review/arabic-visual-review-batch.tsv

arabic-visual-review-update:
	@$(PYTHON) scripts/update_arabic_visual_review.py '$(REVIEW_KEY)' --status '$(REVIEW_STATUS)' --reviewer '$(REVIEWER)' --notes '$(NOTES)' --apply

arabic-visual-review-batch-dry-run:
	@$(PYTHON) scripts/update_arabic_visual_review_batch.py '$(REVIEW_BATCH)'

arabic-visual-review-batch-update:
	@$(PYTHON) scripts/update_arabic_visual_review_batch.py '$(REVIEW_BATCH)' --apply

arabic-visual-review-batch-apply-check: arabic-visual-review-batch-update reports-only preflight-only

build:
	./build.sh

test: build
	./scripts/check_gf_fonts.sh

reports: build
	$(MAKE) reports-only

reports-only:
	$(PYTHON) scripts/report_decision_answer_sheet.py documentation/google-fonts/google-fonts-decision-answer-sheet.md
	$(PYTHON) scripts/report_decision_readiness.py documentation/google-fonts/decision-readiness.md
	$(PYTHON) scripts/report_gf_reference_index.py documentation/google-fonts/google-fonts-reference-index.md
	$(PYTHON) scripts/report_agent_reuse_readiness.py documentation/google-fonts/google-fonts-agent-reuse-readiness.md
	$(PYTHON) scripts/report_source_metadata.py sources/VirtuaGrotesk-Regular.ufo sources/VirtuaGrotesk-Bold.ufo documentation/source/source-ufo-metadata.md
	$(PYTHON) scripts/report_master_compatibility.py sources/VirtuaGrotesk-Regular.ufo sources/VirtuaGrotesk-Bold.ufo documentation/source/master-compatibility.md
	$(PYTHON) scripts/report_generated_font_metadata.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/generated-font-metadata.md
	$(PYTHON) scripts/report_vendor_id_readiness.py documentation/google-fonts/vendor-id-readiness.md
	$(PYTHON) scripts/report_release_metadata.py documentation/google-fonts/release-metadata.md
	$(PYTHON) scripts/report_release_source_readiness.py documentation/google-fonts/release-source-readiness.md
	$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	$(PYTHON) scripts/report_github_release_draft.py documentation/google-fonts/github-release-draft.md
	$(PYTHON) scripts/report_upstream_structure_readiness.py documentation/google-fonts/upstream-structure-readiness.md
	$(PYTHON) scripts/report_family_name_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/family-name-readiness.md
	$(PYTHON) scripts/report_authorship_disclosure_readiness.py documentation/google-fonts/authorship-disclosure-readiness.md
	$(PYTHON) scripts/report_pr_identity_readiness.py documentation/google-fonts/pr-identity-readiness.md
	$(PYTHON) scripts/report_drawbot_runtime_readiness.py documentation/google-fonts/drawbot-runtime-readiness.md
	GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/google-fonts/package-dry-run-readiness.md
	$(PYTHON) scripts/report_local_workflow_readiness.py documentation/google-fonts/local-workflow-readiness.md
	$(PYTHON) scripts/report_designer_profile.py documentation/google-fonts/designer-profile-readiness.md
	$(PYTHON) scripts/report_designer_profile_package.py documentation/google-fonts/designer-profile-package-draft.md
	$(PYTHON) scripts/report_variable_metadata.py '$(VARIABLE_FONT)' documentation/google-fonts/variable-font-metadata.md
	$(PYTHON) scripts/report_avar_readiness.py '$(VARIABLE_FONT)' documentation/google-fonts/avar-readiness.md
	$(PYTHON) scripts/report_axis_registry.py '$(VARIABLE_FONT)' '$(GF_WEIGHT_AXIS_REGISTRY)' documentation/google-fonts/google-fonts-axis-registry-audit.md
	$(PYTHON) scripts/report_gf_glyphset_readiness.py '$(VARIABLE_FONT)' documentation/google-fonts/gf-glyphset-readiness.md
	$(PYTHON) scripts/report_gf_language_metadata.py documentation/google-fonts/google-fonts-language-metadata.md
	$(PYTHON) scripts/report_ufo_editor_readiness.py documentation/source/ufo-editor-readiness.md
	$(PYTHON) scripts/report_missing_gf_latin_core.py '$(VARIABLE_FONT)' documentation/google-fonts/missing-gf-latin-core.md
	$(PYTHON) scripts/report_missing_gf_arabic_core.py '$(VARIABLE_FONT)' documentation/google-fonts/missing-gf-arabic-core.md
	$(PYTHON) scripts/report_arabic_source_checklist.py '$(VARIABLE_FONT)' documentation/glyph-review/arabic-source-work-checklist.md
	$(PYTHON) scripts/build_arabic_candidate_glyphs.py --output documentation/glyph-review/arabic-candidate-glyph-plan.md
	$(PYTHON) scripts/report_pua_scope.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/pua-scope.md
	$(PYTHON) scripts/report_public_upstream_readiness.py documentation/google-fonts/public-upstream-readiness.md
	$(PYTHON) scripts/report_open_placeholders.py documentation/google-fonts/open-placeholder-audit.md
	$(PYTHON) scripts/report_package_source_files.py documentation/google-fonts/package-source-files-audit.md
	$(PYTHON) scripts/report_packager_source_strategy.py documentation/google-fonts/packager-source-strategy.md
	$(PYTHON) scripts/report_downstream_metadata_readiness.py documentation/google-fonts/downstream-metadata-readiness.md
	GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/google-fonts/downstream-metadata-diff.md
	$(PYTHON) scripts/report_decision_application_blockers.py documentation/google-fonts/decision-application-blockers.md
	$(PYTHON) scripts/report_article_readiness.py documentation/google-fonts/article-readiness.md
	$(PYTHON) scripts/report_kerning_readiness.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/kerning-readiness.md
	$(PYTHON) scripts/report_kerning_proof_review.py documentation/google-fonts/kerning-proof-review.md
	$(PYTHON) scripts/report_arabic_mark_readiness.py documentation/glyph-review/arabic-mark-readiness.md
	$(PYTHON) scripts/report_arabic_shaping.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/glyph-review/arabic-shaping-smoke-test.md
	$(PYTHON) scripts/report_arabic_visual_risk.py documentation/glyph-review/arabic-visual-risk-audit.md
	$(PYTHON) scripts/build_arabic_visual_risk_proof.py documentation/glyph-review/arabic-visual-risk-proof.html
	$(PYTHON) scripts/build_arabic_structure_sweep.py documentation/glyph-review/arabic-structure-sweep.html
	$(PYTHON) scripts/report_arabic_structure_triage.py documentation/glyph-review/arabic-structure-triage.md
	$(PYTHON) scripts/build_arabic_mark_review_proof.py documentation/glyph-review/arabic-mark-review-proof.html
	$(PYTHON) scripts/report_arabic_mark_triage.py documentation/glyph-review/arabic-mark-triage.md
	$(PYTHON) scripts/report_arabic_visual_review_log.py documentation/glyph-review/arabic-visual-review-log.md
	$(PYTHON) scripts/report_glyph_reachability.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/glyph-reachability.md
	$(PYTHON) scripts/report_numeric_feature_readiness.py documentation/google-fonts/numeric-feature-readiness.md
	$(PYTHON) scripts/report_fontspector_contours.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/fontspector-contour-count.md
	$(PYTHON) scripts/build_contour_cleanup_proof.py
	$(PYTHON) scripts/build_arabic_manual_review_dashboard.py documentation/glyph-review/arabic-manual-review-dashboard.html
	$(PYTHON) scripts/report_arabic_manual_edit_targets.py documentation/glyph-review/arabic-manual-edit-targets.md
	$(PYTHON) scripts/build_arabic_first_review_zoom_snapshots.py documentation/glyph-review/arabic-first-review-zoom-snapshots.md
	$(PYTHON) scripts/report_arabic_first_review_crop_integrity.py documentation/glyph-review/arabic-first-review-crop-integrity.md
	$(PYTHON) scripts/report_arabic_first_review_batch.py documentation/glyph-review/arabic-first-review-batch.md
	$(PYTHON) scripts/report_arabic_first_review_risk_shortlist.py documentation/glyph-review/arabic-first-review-risk-shortlist.md
	$(PYTHON) scripts/report_arabic_hand_review_session.py documentation/glyph-review/arabic-hand-review-session.md
	$(PYTHON) scripts/build_arabic_hand_review_contact_sheet.py documentation/glyph-review/arabic-hand-review-contact-sheet.html
	$(PYTHON) scripts/report_arabic_next_review_packet.py documentation/glyph-review/arabic-next-review-packet.md
	$(PYTHON) scripts/report_arabic_next_review_ai_triage.py documentation/glyph-review/arabic-next-review-ai-triage.md
	$(PYTHON) scripts/report_arabic_next_review_ai_observations.py documentation/glyph-review/arabic-next-review-ai-observations.md
	$(PYTHON) scripts/report_arabic_full_queue_ai_sweep.py documentation/glyph-review/arabic-full-queue-ai-sweep.md
	$(PYTHON) scripts/report_arabic_manual_review_batches.py documentation/glyph-review/arabic-manual-review-batches.md
	$(PYTHON) scripts/report_arabic_review_progress.py documentation/glyph-review/arabic-review-progress.md
	$(PYTHON) scripts/report_arabic_current_review_worksheet.py documentation/glyph-review/arabic-current-review-worksheet.md
	$(PYTHON) scripts/report_arabic_review_worksheet_bundle.py documentation/glyph-review/arabic-review-worksheet-bundle.md
	$(PYTHON) scripts/report_arabic_drawing_session_checklist.py documentation/glyph-review/arabic-drawing-session-checklist.md
	$(PYTHON) scripts/report_arabic_source_edit_diff.py documentation/glyph-review/arabic-source-edit-diff.md --fail-on-gap
	$(PYTHON) scripts/report_arabic_first_batch_source_checkpoint.py documentation/glyph-review/arabic-first-batch-source-checkpoint.md
	$(PYTHON) scripts/report_arabic_pending_source_checkpoint.py documentation/glyph-review/arabic-pending-source-checkpoint.md
	$(PYTHON) scripts/report_arabic_visual_review_batch_tsv.py documentation/glyph-review/arabic-visual-review-batch.tsv
	$(PYTHON) scripts/report_arabic_batch_recorder.py documentation/glyph-review/arabic-batch-recorder.md
	$(PYTHON) scripts/build_arabic_next_review_board.py documentation/glyph-review/arabic-next-review-board.html
	$(PYTHON) scripts/report_arabic_snapshot_integrity.py documentation/glyph-review/arabic-snapshot-integrity.md
	$(PYTHON) scripts/report_arabic_visual_review_runbook.py documentation/glyph-review/arabic-visual-review-runbook.md
	$(PYTHON) scripts/report_arabic_goal_completion.py documentation/glyph-review/arabic-goal-completion-audit.md
	$(PYTHON) scripts/report_metadata_warning_probe.py documentation/google-fonts/fontspector-metadata-warning-probe.md
	$(PYTHON) scripts/report_zero_warning_worklist.py '$(VARIABLE_FONT)' documentation/google-fonts/fontspector-zero-warning-worklist.md
	$(PYTHON) scripts/report_fontspector_warnings.py '$(VARIABLE_FONT)' $(STATIC_FONTS) documentation/google-fonts/fontspector-warnings.md
	./scripts/report_fontspector_markdown.sh documentation/google-fonts/fontspector-googlefonts-report.md
	$(PYTHON) scripts/report_arabic_review_packet.py documentation/glyph-review/arabic-review-packet.md
	$(PYTHON) scripts/report_production_requirements.py documentation/google-fonts/google-fonts-production-requirements.md
	$(PYTHON) scripts/report_recent_gf_packages.py documentation/google-fonts/recent-google-fonts-packages.md
	$(PYTHON) scripts/report_gf_add_font_template.py documentation/google-fonts/google-fonts-add-font-template-audit.md
	$(PYTHON) scripts/report_add_font_issue_draft.py documentation/google-fonts/google-fonts-add-font-issue-draft.md
	$(PYTHON) scripts/report_downstream_pr_readiness.py documentation/google-fonts/downstream-pr-readiness.md
	$(PYTHON) scripts/report_project_template_automation.py documentation/google-fonts/project-template-automation-readiness.md
	$(PYTHON) scripts/report_submission_handoff_readiness.py documentation/google-fonts/submission-handoff-readiness.md
	$(PYTHON) scripts/report_final_submission_blockers.py documentation/google-fonts/final-submission-blockers.md
	$(PYTHON) scripts/report_next_actions.py documentation/google-fonts/next-actions.md

proof: build
	$(MAKE) proof-only

proof-only:
	PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH}" $(DRAWBOT_PYTHON) scripts/build_general_proof.py fonts/ttf/VirtuaGrotesk-Regular.ttf documentation/proofs/proof.pdf

print-spacing-specimen: build
	$(MAKE) print-spacing-specimen-only

print-spacing-specimen-only:
	PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH}" $(DRAWBOT_PYTHON) scripts/build_print_spacing_specimen.py

arabic-print-proof: build
	$(MAKE) arabic-print-proof-only

arabic-print-proof-only:
	PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH}" $(DRAWBOT_PYTHON) scripts/build_arabic_print_proof.py

preflight: build
	$(MAKE) proof-only
	$(MAKE) arabic-print-proof-only
	$(MAKE) reports-only
	$(MAKE) preflight-only

preflight-only:
	$(PYTHON) scripts/gf_preflight.py

handoff: build
	$(MAKE) proof-only
	$(MAKE) arabic-print-proof-only
	$(MAKE) reports-only
	$(MAKE) preflight-only

package-dry-run:
	GF_REPO_PATH='$(GF_REPO_PATH)' GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' ./scripts/package_gf_dry_run.sh

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/instance_ufos
