-include local.mk

PYTHON ?= ./.venv/bin/python

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help setup build proof proof-web review runebender qa test qa-full qa-package qa-hebrew reports test-tools status queue check-design check-changes prepare-drafting score-drafting compare-drafting corrections lint-curves clean

help:
	@printf '%s\n' \
		'Design work:' \
		'  make status         Rewrite STATUS.md from the mark colors' \
		'  make queue          Rank the glyphs that most composites wait on' \
		'  make check-design GLYPHS="n a"  Check glyphs against sources/design.toml' \
		'  make check-changes  Check source changes since main (green unchanged, drafts purple)' \
		'  make prepare-drafting TASK=bold RUN=dir  Copy the sources for a drafting evaluation' \
		'  make score-drafting RUN=dir  Score the drafts against the green drawings' \
		'  make compare-drafting A=dir B=dir  Compare the scores of two runs' \
		'  make corrections    List the corrections of purple drafts that no rule cites' \
		'  make lint-curves    Curve fairness checks of both masters' \
		'' \
		'Build and proofs:' \
		'  make setup          Create .venv and install the requirements' \
		'  make build          Build the variable and static TTFs into fonts/' \
		'  make proof-web      Build, then compare with reference-fonts/ in a browser' \
		'  make proof          DesignBot PDF proof in out/proof.pdf' \
		'  make review         Diffenator3 browser proof in out/review/' \
		'  make runebender     Open the designspace in the Runebender web editor' \
		'' \
		'QA:' \
		'  make qa             Development Fontspector checks (make test is the same)' \
		'  make qa-full        Full Fontspector profile, no exclusions' \
		'  make qa-package PACKAGE=path  Full profile on a google/fonts package' \
		'  make qa-hebrew      Hebrew coverage and mark attachment' \
		'  make reports        Source and build metadata reports in out/reports/' \
		'  make test-tools     Tests of the Python and JavaScript tools' \
		'  make clean          Remove the build output'

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) scripts/install_fontspector.py

build:
	./scripts/build.sh

# The built-in designbot print proof: introspects the variable font (axes,
# instances, charset, metrics, features) and emits a color-managed multi-page
# PDF.
proof: build
	designbot proof "$(VARIABLE_FONT)" --output out/proof.pdf

# Live comparison of the current build with reference-fonts/. To serve a
# prepared Before/Working snapshot instead, run
# $(PYTHON) scripts/proof-web/serve.py --snapshot <prepared-directory>.
proof-web: build
	$(PYTHON) scripts/proof-web/serve.py --current

# Current Google Fonts browser proof renderer, distributed with Diffenator3.
DIFFPROOF = ./.venv/bin/diff3proof

review: build
	@mkdir -p out
	$(DIFFPROOF) "$(VARIABLE_FONT)" --output out/review
	@echo ">>> open out/review/diff3proof.html"

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

# Drafting evaluation. TASK is redraw, bold, repair or relatives.
# See scripts/evaluate_drafting.py.
prepare-drafting:
	$(PYTHON) scripts/evaluate_drafting.py prepare "$(TASK)" "$(RUN)"

score-drafting:
	$(PYTHON) scripts/evaluate_drafting.py score "$(RUN)"

compare-drafting:
	$(PYTHON) scripts/evaluate_drafting.py compare "$(A)" "$(B)"

# Eli's reviews of purple drafts. ALL=1 lists every review, not only the open
# corrections. See scripts/list_corrections.py.
corrections:
	$(PYTHON) scripts/list_corrections.py $(if $(ALL),--all,)

lint-curves:
	$(PYTHON) scripts/curve_lint.py Regular --all
	$(PYTHON) scripts/curve_lint.py Bold --all

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos

qa-hebrew: build
	$(PYTHON) scripts/check_hebrew.py "$(VARIABLE_FONT)" --json out/hebrew/qa.json --proof-dir out/hebrew/proofs

test-tools:
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) -m unittest discover -s scripts/proof-web/app -p 'test_*.py'
	node --test scripts/proof-web/app/test-reference-selection.cjs
