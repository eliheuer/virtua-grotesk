-include local.mk

PYTHON ?= ./.venv/bin/python
DRAWBOT_SKIA_REPO ?=
DRAWBOT_PYTHON ?= $(PYTHON)
DRAWBOT_PYTHONPATH = $(if $(DRAWBOT_SKIA_REPO),$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH},$${PYTHONPATH})

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf
RUNEBENDER_SOURCE = sources/VirtuaGrotesk.designspace

.PHONY: help setup build proof specimen proof-py specimen-py readme-images social-images runebender glyph-ai-inventory glyph-ai-prepare qa test reports preflight scoreboard skeleton clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make specimen       Build the landscape spacing specimen PDF' \
		'  make readme-images  Build README PNG specimen images' \
		'  make social-images  Build square social media specimen PNGs' \
		'  make runebender     Open sources/VirtuaGrotesk.designspace in chromeless Runebender web' \
		'  make glyph-ai-inventory  Scan Runebender color labels for AI glyph work' \
		'  make glyph-ai-prepare TARGET=glyph REFERENCES="a,e"  Build AI glyph run packet' \
		'  make qa             Run Fontspector Google Fonts profile' \
		'  make reports        Regenerate source/build metadata reports' \
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

# Legacy drawbot-skia (Python) fallbacks, kept until the designbot ports have
# survived a few review cycles. Remove together with the Python scripts.
proof-py: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_general_proof.py "$(REGULAR_FONT)" documentation/proofs/proof.pdf

specimen-py: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_print_spacing_specimen.py

readme-images: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_readme_images.py

social-images: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_social_images.py

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

# The end-to-end skeleton: prove the whole pipeline runs TODAY, debt and
# all. qa failures are expected while debt exists (the leading "-" keeps
# make going); the scoreboard headline is the progress metric.
skeleton: build
	-./scripts/check_gf_fonts.sh
	$(PYTHON) scripts/run_reports.py
	$(PYTHON) scripts/scoreboard.py

preflight: build proof specimen reports
	$(PYTHON) scripts/preflight.py

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
