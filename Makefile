-include local.mk

PYTHON ?= ./.venv/bin/python
DRAWBOT_SKIA_REPO ?=
DRAWBOT_PYTHON ?= $(PYTHON)
DRAWBOT_PYTHONPATH = $(if $(DRAWBOT_SKIA_REPO),$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH},$${PYTHONPATH})
GF_REPO_PATH ?=
GFT_PACKAGER_SOURCE_MODE ?= latest-release

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf

.PHONY: help setup build proof specimen qa test reports preflight drawing-check release-check package-check clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make specimen       Build the landscape spacing specimen PDF' \
		'  make qa             Run Fontspector Google Fonts profile' \
		'  make reports        Regenerate generated readiness/review reports' \
		'  make preflight      Build, proof, specimen, reports, then check artifacts' \
		'  make drawing-check  Regenerate drawing-session reports' \
		'  make release-check  Regenerate release blocker reports' \
		'  make package-check  Regenerate package readiness reports' \
		'  make clean          Remove generated build outputs'

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

build:
	./build.sh

proof: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_general_proof.py "$(REGULAR_FONT)" documentation/proofs/proof.pdf

specimen: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_print_spacing_specimen.py

qa: build
	./scripts/check_gf_fonts.sh

test: qa

reports:
	GFT_PACKAGER_SOURCE_MODE="$(GFT_PACKAGER_SOURCE_MODE)" $(PYTHON) scripts/run_reports.py

preflight: build proof specimen reports
	$(PYTHON) scripts/preflight.py

drawing-check:
	$(PYTHON) scripts/report_ufo_editor_readiness.py documentation/source/ufo-editor-readiness.md
	$(PYTHON) scripts/report_arabic_drawing_session_checklist.py documentation/glyph-review/arabic-drawing-session-checklist.md
	$(PYTHON) scripts/report_arabic_source_edit_diff.py documentation/glyph-review/arabic-source-edit-diff.md --fail-on-gap
	$(PYTHON) scripts/report_arabic_review_progress.py documentation/glyph-review/arabic-review-progress.md

release-check:
	$(PYTHON) scripts/report_release_source_readiness.py documentation/google-fonts/release-source-readiness.md
	$(PYTHON) scripts/report_release_archive_manifest.py documentation/google-fonts/release-archive-manifest.md
	$(PYTHON) scripts/report_final_submission_blockers.py documentation/google-fonts/final-submission-blockers.md
	$(PYTHON) scripts/report_next_actions.py documentation/google-fonts/next-actions.md

package-check:
	GFT_PACKAGER_SOURCE_MODE="$(GFT_PACKAGER_SOURCE_MODE)" $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/google-fonts/package-dry-run-readiness.md
	GFT_PACKAGER_SOURCE_MODE="$(GFT_PACKAGER_SOURCE_MODE)" $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/google-fonts/downstream-metadata-diff.md
	$(PYTHON) scripts/report_downstream_metadata_readiness.py documentation/google-fonts/downstream-metadata-readiness.md
	$(PYTHON) scripts/report_packager_source_strategy.py documentation/google-fonts/packager-source-strategy.md

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/instance_ufos
