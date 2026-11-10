-include local.mk

PYTHON ?= ./.venv/bin/python

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help setup build build-fontc proof proof-web review review-rubik qa-diacritics specimen runebender runebender-web runebender-tab qa qa-full qa-package test reports lint-grid preflight status skeleton clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make status        Rewrite STATUS.md from mark colors (release target: all green)' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make proof-web      Build, then compare the fonts with reference-fonts/ in a browser' \
		'  make review         Build a Diffenator3 QA browser proof' \
		'  make specimen       (not implemented yet — marketing specimen is future work)' \
		'  make runebender     Open the designspace in Runebender gpui (native)' \
		'  make runebender-web Same source in Runebender web, chromeless app window' \
		'  make runebender-tab Runebender web as a tab in your default browser' \
		'  make test-tools     Run the Python and JavaScript tool tests' \
		'  make qa             Development Fontspector checks (documented exclusions)' \
		'  make qa-hebrew      Check Hebrew coverage/attachment and render three weights' \
		'  make qa-full        Full Fontspector profile; no exclusions' \
		'  make qa-package PACKAGE=path  Full downstream-package QA' \
		'  make reports        Regenerate source/build metadata reports' \
		'  make grid-qa        Per-glyph design-system conformance report (grades + popcounts)' \
		'  make dashboard GLYPH=a  Live one-glyph design dashboard (re-renders on save)' \
		'  make lint-grid      Check source outlines against the power-of-two grid' \
		'  make metrics        Normalized metric comparison vs Inter/Geist (weight, spacing, proportion)' \
		'  make skeleton       End-to-end loop: build + qa + reports + status (qa may fail while debt exists)' \
		'  make preflight      Build, proof, reports, then check artifacts' \
		'  make clean          Remove generated build outputs'

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) scripts/install_fontspector.py

build:
	./build.sh

build-fontc:  ## Build with fontc (Rust) instead of fontmake
	./build-fontc.sh

# The built-in designbot print proof: introspects the variable font (axes,
# instances, charset, metrics, features) and emits a color-managed multi-page
# PDF. No per-repo script to maintain — see documentation/proofs/PROOF_SPEC.md.
proof: build
	designbot proof "$(VARIABLE_FONT)" --output documentation/proofs/proof.pdf

# Live comparison of the current build with reference-fonts/. To serve a
# prepared Before/Working snapshot instead, run
# $(PYTHON) agent-proofs/serve.py --snapshot <prepared-directory>.
proof-web: build
	$(PYTHON) agent-proofs/serve.py --current

# Current Google Fonts browser proof renderer, distributed with Diffenator3.
DIFFPROOF = ./.venv/bin/diff3proof
RUBIK_FONT ?= $(HOME)/GH/repos/google-fonts/ofl/rubik/Rubik[wght].ttf

review: build
	@mkdir -p out
	$(DIFFPROOF) "$(VARIABLE_FONT)" --output out/review
	@echo ">>> open out/review/diff3proof.html"

review-rubik:
	@mkdir -p out
	$(DIFFPROOF) "$(RUBIK_FONT)" --output out/review-rubik
	@echo ">>> open out/review-rubik/diff3proof.html"

# Diacritic/spacing QA loop harness: audit + Rubik render + review checklist.
# The agent (person, or Gemma once wired) drives this; fix with build_anchors.py.
qa-diacritics: build
	$(PYTHON) scripts/qa_loop.py

# The marketing specimen (on-brand showcase) is not built yet — it will be a
# `designbot specimen` built-in or a per-repo on-brand script. Until then this
# target is a no-op stub so `make specimen` fails loudly instead of silently.
specimen:
	@echo "specimen: not implemented yet — see documentation/proofs/PROOF_SPEC.md (marketing specimen is future work)"; exit 1

# Social media assets now live as co-located designbot scripts under
# documentation/social-assets/ (render each with `designbot <script.rs>`);
# the old batch target rendered a since-deleted script.

# The native editor. Faster and the one being developed against, but it
# is younger than the web build: no sketch layer (the raster brush), and
# no font info editing. If it gets in the way, `make runebender-web` is
# the same source in the editor that has more mileage on it.
runebender:
	RUNEBENDER_SOURCE="$(RUNEBENDER_SOURCE)" ./runebender-gpui.sh

# The fallback: a chromeless app window on its own Chrome profile, the
# editor and nothing else.
runebender-web:
	RUNEBENDER_SOURCE="$(RUNEBENDER_SOURCE)" ./runebender-web.sh

# The same server, opened as an ordinary tab in the default browser —
# devtools, the address bar and your logged-in profile all to hand.
runebender-tab:
	RUNEBENDER_SOURCE="$(RUNEBENDER_SOURCE)" RUNEBENDER_OPEN_MODE=tab ./runebender-web.sh

qa: build
	./scripts/check_gf_fonts.sh development

qa-full: build
	./scripts/check_gf_fonts.sh full

qa-package:
	@test -n "$(PACKAGE)" || { echo "Set PACKAGE=/path/to/ofl/virtuagrotesk" >&2; exit 2; }
	./scripts/check_gf_fonts.sh package "$(PACKAGE)"

test: qa

reports:
	$(PYTHON) scripts/run_reports.py

status:
	$(PYTHON) scripts/status.py

grid-qa:
	$(PYTHON) scripts/grid_qa.py

# Live design dashboard for one glyph, for a second monitor while editing:
# re-renders on every save. GLYPH accepts a glyph name, character, or U+XXXX.
# Usage: make dashboard GLYPH=a
GLYPH ?= $(G)
dashboard:
	@test -n "$(GLYPH)" || { echo "usage: make dashboard GLYPH=<name|char|U+XXXX>"; exit 1; }
	$(PYTHON) scripts/grid_qa.py --focus "$(GLYPH)" --watch

lint-grid:
	$(PYTHON) scripts/grid_lint.py

lint-curves:
	$(PYTHON) scripts/curve_lint.py Regular --all
	$(PYTHON) scripts/curve_lint.py Bold --all

# Normalized metric comparison of Virtua glyphs against reference fonts
# (Inter, Geist). See documentation/normalized-metrics-workflow.md.
metrics:
	$(PYTHON) scripts/normalize_metrics.py

# The end-to-end skeleton: prove the whole pipeline runs TODAY, debt and
# all. qa failures are expected while debt exists (the leading "-" keeps
# make going); STATUS.md is the progress metric.
skeleton: build
	-./scripts/check_gf_fonts.sh
	-$(PYTHON) scripts/grid_lint.py --quiet
	$(PYTHON) scripts/run_reports.py
	$(PYTHON) scripts/status.py

preflight: build proof reports
	$(PYTHON) scripts/preflight.py

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos

.PHONY: arabic-sync
arabic-sync:  ## Re-snap Arabic dots to their anchors, then re-sync Bold
	./.venv/bin/python scripts/arabic_anchors.py
	./.venv/bin/python scripts/embolden.py --dx 36 --dy 27
	./.venv/bin/python scripts/arabic_anchors.py
	./.venv/bin/python scripts/glif_lint.py

.PHONY: qa-hebrew
qa-hebrew: build
	$(PYTHON) scripts/check_hebrew.py "$(VARIABLE_FONT)" --json out/hebrew/qa.json --proof-dir out/hebrew/proofs

.PHONY: test-tools
test-tools:
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) -m unittest discover -s agent-proofs/app -p 'test_*.py'
	node --test agent-proofs/app/test-reference-selection.cjs
