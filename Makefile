-include local.mk

PYTHON ?= ./.venv/bin/python
# The shared Font.Garden source tools: https://github.com/fontgarden/fontgarden-tools
# `fgtools --help` lists every command. The targets here are the daily ones.
FGTOOLS ?= ./.venv/bin/fgtools
# The revision that make diff and make check-changes compare with.
BASE ?= main

.PHONY: help venv setup build test qa status queue check-design check-changes diff proof-web reference-fonts runebender clean

help:
	@printf '%s\n' \
		'  make setup          Create .venv and install the requirements' \
		'  make build          Build the variable and static TTFs into fonts/' \
		'  make test           Build, then run the tests and the Fontspector checks' \
		'  make qa             Build, then run the Fontspector checks only' \
		'  make status         Rewrite STATUS.md from the mark colors' \
		'  make queue          Rank the glyphs that most composites wait on' \
		'  make check-design GLYPHS="n a"  Check glyphs against CONTEXT.md' \
		'  make check-changes  Check source changes since main (green unchanged, drafts purple)' \
		'  make diff           Compare builds of main and the working tree (diffenator3)' \
		'  make proof-web      Build, then compare with reference-fonts/ in a browser' \
		'  make reference-fonts  Get the reference fonts that CONTEXT.md lists' \
		'  make runebender     Open the designspace in Runebender' \
		'  make clean          Remove the build output' \
		'' \
		'Every other tool is a command of fgtools: .venv/bin/fgtools --help'

# gftools packager --their-venv runs `make venv`.
venv: setup

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools

# The shared build, then the three metadata fixes that only this font needs.
build:
	rm -rf build build.ninja .ninja_log
	$(FGTOOLS) build
	$(PYTHON) scripts/fix_gf_metadata.py fonts/variable/*.ttf fonts/ttf/*.ttf

test: build
	$(PYTHON) -m unittest discover -s tests
	$(FGTOOLS) qa

qa: build
	$(FGTOOLS) qa

status:
	$(FGTOOLS) status

queue:
	$(FGTOOLS) queue

# Without GLYPHS it reports on every glyph that is not green.
check-design:
	$(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

# Usage: make check-changes BASE=main GLYPHS="a e"
check-changes:
	$(FGTOOLS) check-changes --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

# Builds BASE and the working tree with fontc. HTML reports go to out/diff/.
diff:
	$(FGTOOLS) diff --base "$(BASE)"

proof-web: build
	$(FGTOOLS) proof-web --current

reference-fonts:
	$(FGTOOLS) fetch-reference-fonts --project

# Install: cargo install --locked --git https://github.com/fontgarden/runebender runebender
runebender:
	runebender sources/VirtuaGrotesk.designspace &

clean:
	rm -rf build build.ninja .ninja_log dist fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
