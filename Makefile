# The daily commands of this project. Run `make` or `make help` for the list.
#
# Each target runs one command of fgtools (https://github.com/fontgarden/fgtools),
# the shared tools of Font.Garden projects. `.venv/bin/fgtools --help` lists
# every command, and `.venv/bin/fgtools <command> --help` lists its options.
# A target has no logic of its own: to change what a target does, change fgtools.
#
# A line `##@ Title` starts a section of `make help`, and the text after `##`
# on the line of a target is its description there.

PYTHON = .venv/bin/python
FGTOOLS = .venv/bin/fgtools
# The revision that diff and check-changes compare with: make diff BASE=<revision>
BASE = main

help:
	@awk -F ':.*## ' '/^##@ / {printf "\n%s\n", substr($$0, 5)} /^[a-z-]+:.*## / {printf "  make %-16s %s\n", $$1, $$2}' Makefile

##@ Setup

# Installs the pinned versions: fgtools from requirements.txt, and the fontc
# and Fontspector binaries. Run it again after a change of requirements.txt.
setup: ## Create .venv and install the requirements and the pinned tools
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools

# gftools packager --their-venv runs `make venv`.
venv: setup

##@ Build and test

# The recipe of the build is sources/config.yaml.
# sources/fix_gf_metadata.py applies three metadata fixes that only this font needs.
build: ## Build the variable and static TTFs into fonts/
	$(FGTOOLS) build
	$(PYTHON) sources/fix_gf_metadata.py fonts/variable/*.ttf fonts/ttf/*.ttf

test: build ## Build, then check the repository and run the Fontspector checks
	$(FGTOOLS) check-repository
	$(FGTOOLS) qa

qa: build ## Build, then run the Fontspector checks only
	$(FGTOOLS) qa

# Every check of the Google Fonts profile, with the checks that need the
# network. CI runs it and reports the result, but it does not fail the run.
qa-full: build ## Build, then run every Fontspector check, with network checks
	$(FGTOOLS) qa --full

##@ Design work

# The mark color of a glyph is its state. STATUS.md counts the colors.
status: ## Rewrite STATUS.md from the mark colors
	$(FGTOOLS) status

queue: ## Rank the glyphs that most composites wait on
	$(FGTOOLS) queue

# The rules and the values are in CONTEXT.md. Without GLYPHS, every glyph that
# is not green is checked.
check-design: ## Check glyphs against CONTEXT.md: make check-design GLYPHS="n a"
	$(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

# Run it after an agent edits glyphs. It fails when a green glyph changed, or
# when the contours of a glyph changed and it is not purple.
check-changes: ## Check source changes since BASE: green unchanged, drafts purple
	$(FGTOOLS) check-changes --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

# A large picture of glyphs for review: the change since BASE, the filled
# glyph, its points, the reference fonts and the glyph in a block of text.
render: ## Draw glyphs large for review: make render GLYPHS="a n"
	@test -n "$(GLYPHS)" || { echo 'Name the glyphs: make render GLYPHS="a n"' >&2; exit 2; }
	$(FGTOOLS) render "$(GLYPHS)" --base "$(BASE)"

diff: ## Compare builds of BASE and the working tree, reports in output/diff/
	$(FGTOOLS) diff --base "$(BASE)"

reference-fonts: ## Get the reference fonts that CONTEXT.md lists
	$(FGTOOLS) fetch-reference-fonts --project

runebender: ## Open the designspace in Runebender
	runebender sources/VirtuaGrotesk.designspace &

##@ Proofs, specimen and media

# These three targets use one layout system: the lattice of the typeface,
# rules R61 to R67 of CONTEXT.md. A checker verifies each layout, and DesignBot
# draws it. They need the `designbot` command on PATH, and a video needs
# `ffmpeg`:
#   cargo install --git https://github.com/eliheuer/designbot designbot-cli
# The output is in output/, which Git ignores. CI runs the three targets on
# each push to main and publishes the result on GitHub Pages.

# Each of the three targets can make a part only:
#   make proof PAGE="spacing kerning"       some pages of the proof
#   make specimen PAGE=words                some pages of the specimen
#   make media FORMAT=videos                one kind: images, carousels or videos
#   make media FORMAT="words glyph"         some formats
#   make media FORMAT=weight-axis CANVAS=landscape    one format on one canvas
#   make media LATTICE=1                    draw the lattice on each picture
# `make formats` lists the names. The format `glyph` is the technical image.
# The last line of each target is `Open:` and the file to look at.

formats: ## List the formats, the canvases and the pages of the proof
	$(FGTOOLS) media --list

# For the designer, to find faults: the character set, the sizes, reading
# text, spacing, kerning, diacritics, the weight axis, and the tables of the
# Arabic script. The short lines of sources/proof-samples.toml are in it.
proof: build ## Build, then write the print proof to output/proof/proof.pdf, or its pages PAGE=...
	$(FGTOOLS) media --proof $(PAGE)

# For a reader: the formats of the marketing media on A4 pages.
specimen: build ## Build, then write the print specimen to output/specimen/, or its pages PAGE=...
	$(FGTOOLS) media --specimen $(PAGE)

# The images, carousels and videos for the social platforms. The brand of this
# font is documentation/media/brand.toml. One format: .venv/bin/fgtools media words
# The review page is output/media/index.html. With LATTICE=1, each picture is
# also written with the lattice and the text area drawn on it, with the
# suffix _lattice in its name.
media: build ## Build, then render the media into output/media/, or only FORMAT=... CANVAS=...
	$(FGTOOLS) media $(FORMAT) $(if $(CANVAS),--canvas $(CANVAS),) $(if $(LATTICE),--lattice,)

# A default format of fgtools reaches every font. To change a format for this
# font only, copy it into documentation/media/ and edit the copy there.
copy-format: ## Copy a default format into this project to change it: make copy-format FORMAT=words
	@test -n "$(FORMAT)" || { echo 'Name the format: make copy-format FORMAT=words' >&2; exit 2; }
	$(FGTOOLS) media --copy $(FORMAT)

# Everything that CI publishes: the proof, the specimen and the media,
# collected into output/site/ with an index page. CI runs this target.
site: proof specimen media ## Build and render everything, then collect it into output/site/
	$(FGTOOLS) site

# The interactive proof: this font beside the fonts of reference-fonts/.
proof-web: build ## Build, then compare with reference-fonts/ in a browser
	$(FGTOOLS) proof-web --current

##@ Housekeeping

clean: ## Remove fonts/ and output/
	rm -rf fonts output

.PHONY: help setup venv build test qa qa-full status queue check-design check-changes render diff reference-fonts runebender formats proof specimen media copy-format site proof-web clean
