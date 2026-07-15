-include local.mk

PYTHON ?= ./.venv/bin/python

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace
PNGQUANT ?= ./.venv/bin/pngquant

.PHONY: help setup build proof specimen social-images runebender glyph-ai-inventory glyph-ai-prepare qa test reports lint-grid preflight scoreboard skeleton clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make specimen       Build the landscape spacing specimen PDF' \
		'  make social-images  Build square social media specimen PNGs' \
		'  make runebender     Open sources/VirtuaGrotesk.designspace in chromeless Runebender web' \
		'  make glyph-ai-inventory  Scan Runebender color labels for AI glyph work' \
		'  make glyph-ai-prepare TARGET=glyph REFERENCES="a,e"  Build AI glyph run packet' \
		'  make qa             Run Fontspector Google Fonts profile' \
		'  make reports        Regenerate source/build metadata reports' \
		'  make grid-qa        Per-glyph design-system conformance report (grades + popcounts)' \
		'  make lint-grid      Check source outlines against the power-of-two grid' \
		'  make scoreboard     Update documentation/scoreboard.md (GF-gate burn-down)' \
		'  make skeleton       End-to-end loop: build + qa + reports + scoreboard (qa may fail while debt exists)' \
		'  make preflight      Build, proof, specimen, reports, then check artifacts' \
		'  make clean          Remove generated build outputs'

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

build:
	./build.sh

proof: build
	designbot --render scripts/designbot/general_proof.rs --output documentation/proofs/proof.pdf -- "$(REGULAR_FONT)"

specimen: build
	designbot --render scripts/designbot/print_spacing_specimen.rs --output documentation/proofs/print-spacing-specimen.pdf

SOCIAL_IMAGES = 01-hero:hero 02-weights:weights 03-alphabet-regular:alphabet-regular \
	03-alphabet-medium:alphabet-medium 03-alphabet-semibold:alphabet-semibold \
	03-alphabet-bold:alphabet-bold 04-tabular:tabular 05-chamfer:chamfer \
	06-waterfall:waterfall 07-symbols:symbols 08-lowercase:lowercase

social-images: build
	@for f in square portrait landscape; do \
	  for spec in $(SOCIAL_IMAGES); do \
	    name=$${spec%%:*}; mode=$${spec##*:}; \
	    designbot --render scripts/designbot/social_images.rs \
	      --output "documentation/assets/social/$$f/social-$$name.png" -- "$$f:$$mode" || exit 1; \
	  done; \
	done
	-$(PNGQUANT) --force --ext .png --skip-if-larger documentation/assets/social/*/*.png

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

lint-grid:
	$(PYTHON) scripts/grid_lint.py

lint-curves:
	$(PYTHON) scripts/curve_lint.py Regular --all
	$(PYTHON) scripts/curve_lint.py Bold --all

# The end-to-end skeleton: prove the whole pipeline runs TODAY, debt and
# all. qa failures are expected while debt exists (the leading "-" keeps
# make going); the scoreboard headline is the progress metric.
skeleton: build
	-./scripts/check_gf_fonts.sh
	-$(PYTHON) scripts/grid_lint.py --quiet
	$(PYTHON) scripts/run_reports.py
	$(PYTHON) scripts/scoreboard.py

preflight: build proof specimen reports
	$(PYTHON) scripts/preflight.py

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
