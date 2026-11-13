-include local.mk

PYTHON ?= ./.venv/bin/python
# The shared Font.Garden source tools: https://github.com/fontgarden/fontgarden-tools
FGTOOLS ?= ./.venv/bin/fgtools
# The revision that make diff and make check-changes compare with.
BASE ?= main

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help venv setup build diff proof proof-web review runebender qa test qa-full qa-package test-tools status queue check-design check-changes prepare-drafting score-drafting compare-drafting corrections lint-curves clean

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
		'  make diff           Compare builds of main and the working tree (diffenator3)' \
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
		'  make test-tools     Tests of the Python and JavaScript tools' \
		'  make clean          Remove the build output'

# gftools packager --their-venv runs `make venv`.
venv: setup

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools

build:
	./scripts/build.sh

# The built-in designbot print proof: introspects the variable font (axes,
# instances, charset, metrics, features) and emits a color-managed multi-page
# PDF.
# Build main and the working tree with fontc and compare them with diffenator3.
# BASE=<revision> compares with another revision. HTML reports go to out/diff/.
diff:
	$(FGTOOLS) diff --base "$(BASE)"

proof: build
	designbot proof "$(VARIABLE_FONT)" --output out/proof.pdf

# Live comparison of the current build with reference-fonts/ in a browser.
# See `fgtools proof-web --help` for a Before and Candidate snapshot.
proof-web: build
	$(FGTOOLS) proof-web --current

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
	$(FGTOOLS) qa

qa-full: build
	$(FGTOOLS) qa --full

qa-package:
	@test -n "$(PACKAGE)" || { echo "Set PACKAGE=/path/to/ofl/virtuagrotesk" >&2; exit 2; }
	$(FGTOOLS) qa --package "$(PACKAGE)"

test: qa


status:
	$(FGTOOLS) status

# Check glyphs against the design targets. Usage: make check-design GLYPHS="n seen-ar"
# Without GLYPHS it reports on every glyph that is not green.
check-design:
	$(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

queue:
	$(FGTOOLS) queue

# Check source changes since BASE (default main). Usage: make check-changes BASE=main GLYPHS="a e"
check-changes:
	$(FGTOOLS) check-changes --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

# Drafting evaluation. TASK is redraw, bold, repair or relatives.
# See `fgtools evaluate-drafting --help`.
prepare-drafting:
	$(FGTOOLS) evaluate-drafting prepare "$(TASK)" "$(RUN)"

score-drafting:
	$(FGTOOLS) evaluate-drafting score "$(RUN)"

compare-drafting:
	$(FGTOOLS) evaluate-drafting compare "$(A)" "$(B)"

# Eli's reviews of purple drafts. ALL=1 lists every review, not only the open
# corrections. See `fgtools corrections --help`.
corrections:
	$(FGTOOLS) corrections $(if $(ALL),--all,)

lint-curves:
	$(FGTOOLS) lint-curves Regular --all
	$(FGTOOLS) lint-curves Bold --all

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos


test-tools:
	$(PYTHON) -m unittest discover -s tests
