-include local.mk

PYTHON ?= ./.venv/bin/python

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help setup build build-fontc proof proof-web review review-rubik qa-diacritics specimen runebender qa qa-full qa-package test reports lint-grid preflight status check-design queue check-changes benchmark skeleton clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make status        Rewrite STATUS.md from mark colors (release target: all green)' \
		'  make queue          Rank the glyphs that most composites wait on' \
		'  make check-changes  Check source changes since main (green unchanged, drafts purple)' \
		'  make check-design GLYPHS="n a"  Check glyphs against the design targets' \
		'  make benchmark RUN=dir  Score redrawn held-out glyphs against the green drawings' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make proof-web      Build, then compare the fonts with reference-fonts/ in a browser' \
		'  make review         Build a Diffenator3 QA browser proof' \
		'  make specimen       (not implemented yet — marketing specimen is future work)' \
		'  make runebender     Open the designspace in the Runebender web editor' \
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
	./scripts/build.sh

build-fontc:  ## Build with fontc (Rust) instead of fontmake
	./scripts/build-fontc.sh

# The built-in designbot print proof: introspects the variable font (axes,
# instances, charset, metrics, features) and emits a color-managed multi-page
# PDF. No per-repo script to maintain — see documentation/proofs/PROOF_SPEC.md.
proof: build
	designbot proof "$(VARIABLE_FONT)" --output documentation/proofs/proof.pdf

# Live comparison of the current build with reference-fonts/. To serve a
# prepared Before/Working snapshot instead, run
# $(PYTHON) scripts/proof-web/serve.py --snapshot <prepared-directory>.
proof-web: build
	$(PYTHON) scripts/proof-web/serve.py --current

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
# The agent (person, or Gemma once wired) drives this; fix the anchors in the source.
qa-diacritics: build
	$(PYTHON) scripts/qa_loop.py

# The marketing specimen (on-brand showcase) is not built yet — it will be a
# `designbot specimen` built-in or a per-repo on-brand script. Until then this
# target is a no-op stub so `make specimen` fails loudly instead of silently.
specimen:
	@echo "specimen: not implemented yet — see documentation/proofs/PROOF_SPEC.md (marketing specimen is future work)"; exit 1

# Serves the editor at localhost:8765 with the designspace open. Edits to
# the sources reload in the browser, and Cmd+S saves back to disk.
runebender:
	runebender-serve "$(RUNEBENDER_SOURCE)" --open

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

# Check glyphs against the design targets. Usage: make check-design GLYPHS="n seen-ar"
# Without GLYPHS it reports on every glyph that is not green.
check-design:
	$(PYTHON) scripts/check_design.py $(if $(GLYPHS),$(GLYPHS),--not-green)

queue:
	$(PYTHON) scripts/check_design.py --queue

# Check source changes since BASE (default main). Usage: make check-changes BASE=main GLYPHS="a e"
BASE ?= main
check-changes:
	$(PYTHON) scripts/check_changes.py --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

# Usage: make benchmark RUN=out/benchmark/run-1   (prepare it first; see scripts/benchmark.py)
benchmark:
	$(PYTHON) scripts/benchmark.py score "$(RUN)"

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

.PHONY: qa-hebrew
qa-hebrew: build
	$(PYTHON) scripts/check_hebrew.py "$(VARIABLE_FONT)" --json out/hebrew/qa.json --proof-dir out/hebrew/proofs

.PHONY: test-tools
test-tools:
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) -m unittest discover -s scripts/proof-web/app -p 'test_*.py'
	node --test scripts/proof-web/app/test-reference-selection.cjs
