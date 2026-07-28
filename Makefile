-include local.mk

PYTHON ?= ./.venv/bin/python

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help setup build proof review review-rubik qa-diacritics specimen runebender glyph-ai-inventory glyph-ai-prepare qa test reports lint-grid preflight scoreboard skeleton clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make specimen       (not implemented yet — marketing specimen is future work)' \
		'  make runebender     Open sources/VirtuaGrotesk.designspace in chromeless Runebender web' \
		'  make glyph-ai-inventory  Scan Runebender color labels for AI glyph work' \
		'  make glyph-ai-prepare TARGET=glyph REFERENCES="a,e"  Build AI glyph run packet' \
		'  make qa             Run Fontspector Google Fonts profile' \
		'  make reports        Regenerate source/build metadata reports' \
		'  make grid-qa        Per-glyph design-system conformance report (grades + popcounts)' \
		'  make dashboard GLYPH=a  Live one-glyph design dashboard (re-renders on save)' \
		'  make lint-grid      Check source outlines against the power-of-two grid' \
		'  make metrics        Normalized metric comparison vs Inter/Geist (weight, spacing, proportion)' \
		'  make scoreboard     Update documentation/scoreboard.md (GF-gate burn-down)' \
		'  make skeleton       End-to-end loop: build + qa + reports + scoreboard (qa may fail while debt exists)' \
		'  make preflight      Build, proof, specimen, reports, then check artifacts' \
		'  make clean          Remove generated build outputs'

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

build:
	./build.sh

# The built-in designbot print proof: introspects the variable font (axes,
# instances, charset, metrics, features) and emits a color-managed multi-page
# PDF. No per-repo script to maintain — see documentation/proofs/PROOF_SPEC.md.
proof: build
	designbot proof "$(VARIABLE_FONT)" --output documentation/proofs/proof.pdf

# diffenator2 -- the Google Fonts onboarding review view (glyph set, diacritic
# proofer, spacing, waterfall). Must run with the venv on PATH so diffenator2's
# _diffbrowsers helper resolves. `make review` = Virtua; `make review-rubik` =
# the shipped Rubik reference to match against. Open the printed index in a browser.
DIFFENATOR = PATH="$(CURDIR)/.venv/bin:$$PATH" ./.venv/bin/diffenator2
RUBIK_FONT ?= $(HOME)/GH/repos/google-fonts/ofl/rubik/Rubik[wght].ttf

review: build
	@mkdir -p out
	$(DIFFENATOR) proof "$(VARIABLE_FONT)" -o out/review
	@echo ">>> open out/review/diffenator2-report.html"

review-rubik:
	@mkdir -p out
	$(DIFFENATOR) proof "$(RUBIK_FONT)" -o out/review-rubik
	@echo ">>> open out/review-rubik/diffenator2-report.html"

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

runebender:
	RUNEBENDER_SOURCE="$(RUNEBENDER_SOURCE)" ./runebender-web.sh

glyph-ai-inventory:
	$(PYTHON) scripts/glyph_ai_harness.py inventory

glyph-ai-prepare:
	@test -n "$(TARGET)" || (printf '%s\n' 'Set TARGET=<glyph-name>' >&2; exit 2)
	$(PYTHON) scripts/glyph_ai_harness.py prepare --target "$(TARGET)" $(if $(REFERENCES),--references "$(REFERENCES)",)

qa: build
	./scripts/check_gf_fonts.sh

test: qa

reports:
	$(PYTHON) scripts/run_reports.py

scoreboard:
	$(PYTHON) scripts/scoreboard.py

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
# make going); the scoreboard headline is the progress metric.
skeleton: build
	-./scripts/check_gf_fonts.sh
	-$(PYTHON) scripts/grid_lint.py --quiet
	$(PYTHON) scripts/run_reports.py
	$(PYTHON) scripts/scoreboard.py

preflight: build proof reports
	$(PYTHON) scripts/preflight.py

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
