# Run `make` or `make help` for the list. Every other tool is a command of
# fgtools (https://github.com/fontgarden/fgtools): .venv/bin/fgtools --help

PYTHON = .venv/bin/python
FGTOOLS = .venv/bin/fgtools
# The revision that diff and check-changes compare with: make diff BASE=<revision>
BASE = main

help:
	@awk -F ':.*## ' '/^[a-z-]+:.*## / {printf "  make %-16s %s\n", $$1, $$2}' Makefile

setup: ## Create .venv and install the requirements and the pinned tools
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools

# gftools packager --their-venv runs `make venv`.
venv: setup

build: ## Build the variable and static TTFs into fonts/
	$(FGTOOLS) build
	$(PYTHON) scripts/fix_gf_metadata.py fonts/variable/*.ttf fonts/ttf/*.ttf

test: build ## Build, then check the repository and run the Fontspector checks
	$(FGTOOLS) check-repository
	$(FGTOOLS) qa

qa: build ## Build, then run the Fontspector checks only
	$(FGTOOLS) qa

status: ## Rewrite STATUS.md from the mark colors
	$(FGTOOLS) status

queue: ## Rank the glyphs that most composites wait on
	$(FGTOOLS) queue

check-design: ## Check glyphs against CONTEXT.md: make check-design GLYPHS="n a"
	$(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

check-changes: ## Check source changes since BASE: green unchanged, drafts purple
	$(FGTOOLS) check-changes --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

diff: ## Compare builds of BASE and the working tree, reports in output/diff/
	$(FGTOOLS) diff --base "$(BASE)"

proof-web: build ## Build, then compare with reference-fonts/ in a browser
	$(FGTOOLS) proof-web --current

reference-fonts: ## Get the reference fonts that CONTEXT.md lists
	$(FGTOOLS) fetch-reference-fonts --project

runebender: ## Open the designspace in Runebender
	runebender sources/VirtuaGrotesk.designspace &

clean: ## Remove fonts/ and output/
	rm -rf fonts output build

.PHONY: help setup venv build test qa status queue check-design check-changes diff proof-web reference-fonts runebender clean
