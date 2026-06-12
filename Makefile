-include local.mk

PYTHON ?= ./.venv/bin/python
DRAWBOT_SKIA_REPO ?=
DRAWBOT_PYTHON ?= $(PYTHON)
DRAWBOT_PYTHONPATH = $(if $(DRAWBOT_SKIA_REPO),$(DRAWBOT_SKIA_REPO)/src$${PYTHONPATH:+:$$PYTHONPATH},$${PYTHONPATH})

VARIABLE_FONT = fonts/variable/VirtuaGrotesk[wght].ttf
REGULAR_FONT = fonts/ttf/VirtuaGrotesk-Regular.ttf

.PHONY: help setup build proof specimen readme-images social-images qa test reports preflight clean

help:
	@printf '%s\n' \
		'Virtua Grotesk workflow:' \
		'  make setup          Create .venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make proof          Build the main PDF proof' \
		'  make specimen       Build the landscape spacing specimen PDF' \
		'  make readme-images  Build README PNG specimen images' \
		'  make social-images  Build square social media specimen PNGs' \
		'  make qa             Run Fontspector Google Fonts profile' \
		'  make reports        Regenerate source/build metadata reports' \
		'  make preflight      Build, proof, specimen, reports, then check artifacts' \
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

readme-images: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_readme_images.py

social-images: build
	PYTHONPATH="$(DRAWBOT_PYTHONPATH)" $(DRAWBOT_PYTHON) scripts/build_social_images.py

qa: build
	./scripts/check_gf_fonts.sh

test: qa

reports:
	$(PYTHON) scripts/run_reports.py

preflight: build proof specimen reports
	$(PYTHON) scripts/preflight.py

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
