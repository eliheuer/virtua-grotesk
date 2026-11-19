# The core commands for this project. Run `make` or `make help` for the list.
#
# Most targets run one command for fgtools (https://github.com/fontgarden/fgtools),
# the shared tools of Font.Garden projects. `.venv/bin/fgtools --help` lists
# every command, and `.venv/bin/fgtools <command> --help` lists its options.
# A target has no logic of its own: to change what a target does, change fgtools.
#
# Each target has a comment above it: the first line is the command, and the
# lines after it say what it does. A line `##@ Title` starts a section of
# `make help`, and the text after `##` on the line of a target is its
# description there.

PYTHON = .venv/bin/python
FGTOOLS = .venv/bin/fgtools
# The revision that diff, check-changes and render compare with:
# make diff BASE=<revision>
BASE = main
# A target that says "Build, then" builds the fonts first. NO_BUILD=1 skips
# the build and uses the fonts that are in fonts/: make test NO_BUILD=1
BUILD = $(if $(NO_BUILD),,build)

##@ Help

# make help
# Prints each target that has a `## description`, under the `##@` section
# titles, then the note on NO_BUILD. It is the first target, so `make` alone
# runs it.
help: ## Print this list
	@awk -F ':.*## ' '/^##@ / {printf "\n%s\n", substr($$0, 5)} /^[a-z-]+:.*## / {printf "  make %-18s %s\n", $$1, $$2}' Makefile
	@echo
	@echo 'A target that says "Build, then" skips the build with NO_BUILD=1, for example: make test NO_BUILD=1'

##@ Setup

# make setup
# Installs every tool of the project, Python and Rust, at its pinned version
# into .venv/. Nothing is installed outside the project, so each project can
# use other versions.
#   Python: fgtools and gftools, from requirements.txt
#   Rust:   fontc and Fontspector, downloaded release binaries in .venv/bin/
#           DesignBot, which Cargo compiles from the commit that fgtools pins
#           into .venv/bin/. The first compile takes about two minutes and
#           needs the `cargo` command (https://rustup.rs).
# Setup names ffmpeg and Runebender if they are missing; they are installed
# once for the computer. Run it again after a change of requirements.txt.
setup: ## Install the pinned Python and Rust tools of the project into .venv/
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools

# make venv
# Another name for `make setup`. The Google Fonts packager runs `make venv`
# when it builds the fonts with the environment of this project (--their-venv).
venv: setup

##@ Build and test

# make build
# Builds the fonts with the recipe and metadata preferences in sources/config.yaml.
build: ## Build the variable font and the static fonts into fonts/ with fontc
	$(FGTOOLS) build

# make test
# Builds, then runs every check. CI runs it on each push. Run it before a commit.
#   1. The repository: each file is in the folder where Font.Garden projects
#      keep it, and each file and `make` target that a document names exists.
#   2. The fonts, with Fontspector: the Google Fonts checks, the Font.Garden
#      checks and the checks of this font in sources/fontspector_checks.py.
# It skips only the known faults in [qa.exclude] of CONTEXT.md, each with
# its reason, so that a FAIL is a new fault. The font is ready for release
# when that list is empty. Some Google Fonts checks need the internet.
# The reports are in output/qa/.
test: $(BUILD) ## Build, then run every check, except the known faults in CONTEXT.md
	$(FGTOOLS) check-repository
	$(FGTOOLS) qa

# make test-google-fonts
# The Google Fonts checks of `make test` only.
test-google-fonts: $(BUILD) ## Build, then run only the Google Fonts checks
	$(FGTOOLS) qa --checks google-fonts

# make test-fontgarden
# The Font.Garden checks and the checks of this font, of `make test` only.
test-fontgarden: $(BUILD) ## Build, then run only the Font.Garden checks and the checks of this font
	$(FGTOOLS) qa --checks fontgarden

##@ Design work

# make status
# Counts the mark colors of the glyphs, which are their states, and writes
# the counts to STATUS.md.
status: ## Count the glyphs of each mark color into STATUS.md
	$(FGTOOLS) status

# make queue
# Lists the glyphs that are not green, with the glyphs that most composites
# wait on first.
queue: ## List the glyphs that are not green, the ones that most composites use first
	$(FGTOOLS) queue

# make check-design GLYPHS="n a"
# Checks glyphs against the rules and the values in CONTEXT.md. Without
# GLYPHS, it checks every glyph that is not green.
check-design: ## Check glyphs against the rules of CONTEXT.md: make check-design GLYPHS="n a"
	$(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

# make check-changes
# Compares the sources with BASE. Run it after an agent edits glyphs. It fails
# when a green glyph changed, or when the contours of a glyph changed and the
# glyph is not purple. GLYPHS="n a" limits it to some glyphs.
check-changes: ## Check the source changes since main, or BASE=...: green glyphs unchanged, changed glyphs purple
	$(FGTOOLS) check-changes --base "$(BASE)" $(if $(GLYPHS),--glyphs "$(GLYPHS)",)

# make render GLYPHS="a n"
# Draws glyphs large in one picture for review: the change since BASE, the
# filled glyph, its points, the reference fonts and the glyph in a block of text.
render: ## Draw glyphs large for review into output/render/: make render GLYPHS="a n"
	@test -n "$(GLYPHS)" || { echo 'Name the glyphs: make render GLYPHS="a n"' >&2; exit 2; }
	$(FGTOOLS) render "$(GLYPHS)" --base "$(BASE)"

# make diff
# Builds BASE and the working tree, and compares the fonts with diffenator3.
# The reports are in output/diff/.
diff: ## Build main, or BASE=..., and the working tree, and compare them with diffenator3 into output/diff/
	$(FGTOOLS) diff --base "$(BASE)"

# make masters
# Calculates every master that is not drawn, after a change of Regular or Bold:
# Thin and Black, then the grade masters, then the 144 pt masters. A glyph that
# was corrected by hand in one of these masters stays. The rules and the
# values are R44, R68 and R69 of CONTEXT.md.
masters: ## Calculate Thin, Black, the grade masters and the 144 pt masters from Regular and Bold
	$(FGTOOLS) draft-weights --write
	$(FGTOOLS) draft-grade
	$(FGTOOLS) draft-optical-size --write

# make reference-fonts
# Downloads the reference fonts that CONTEXT.md lists into reference-fonts/,
# which Git ignores. Runebender and `make proof-web` show them beside this font.
reference-fonts: ## Download the reference fonts that CONTEXT.md lists into reference-fonts/
	$(FGTOOLS) fetch-reference-fonts --project

# make runebender
# Opens the designspace in the Runebender font editor.
runebender: ## Open the designspace in Runebender
	runebender sources/VirtuaGrotesk.designspace &

##@ Proofs, specimen and media

# The proof, the specimen and the media use one layout system: the lattice of
# the typeface, rules R61 to R67 of CONTEXT.md. A checker verifies each
# layout, and DesignBot draws it. A video also needs `ffmpeg`. The output is
# in output/, which Git ignores. The last line of each target is `Open:` and
# the file to look at.

# make formats
# Lists the names that the targets below take: the formats of the media, the
# canvases, and the pages of the proof and of the specimen.
formats: ## List the names that FORMAT, CANVAS and PAGE take
	$(FGTOOLS) media --list

# make proof
# Builds, then writes the print proof to output/proof/proof.pdf. It is for the
# designer, to find faults: the character set, the sizes, reading text,
# spacing, kerning, diacritics, the weight axis and the tables of the Arabic
# script. The short lines of sources/proof-samples.toml are in it.
# Some pages only: make proof PAGE="spacing kerning"
proof: $(BUILD) ## Build, then write the print proof to output/proof/proof.pdf, or its pages PAGE=...
	$(PYTHON) sources/proof_review.py --build-proof $(PAGE)

# make specimen
# Builds, then writes the print specimen to output/specimen/. It is for a
# reader: the formats of the marketing media on A4 pages.
# Some pages only: make specimen PAGE=words
specimen: $(BUILD) ## Build, then write the print specimen to output/specimen/, or its pages PAGE=...
	$(FGTOOLS) media --specimen $(PAGE)

# make media
# Builds, then renders the images, carousels and videos for the social
# platforms into output/media/. The review page is output/media/index.html.
# The brand of this font is documentation/media/brand.toml.
# A part only:
#   make media FORMAT=videos                one kind: images, carousels or videos
#   make media FORMAT="words glyph"         some formats; `glyph` is the technical image
#   make media FORMAT=weight-axis CANVAS=landscape    one format on one canvas
#   make media LATTICE=1                    also each picture with the lattice drawn on it
media: $(BUILD) ## Build, then render the images, carousels and videos into output/media/, or FORMAT=... CANVAS=...
	$(FGTOOLS) media $(FORMAT) $(if $(CANVAS),--canvas $(CANVAS),) $(if $(LATTICE),--lattice,)

# make copy-format FORMAT=words
# Copies a default format of fgtools into documentation/media/, to change it
# for this font only. A default format that is not copied gets each
# improvement of fgtools.
copy-format: ## Copy a default format into documentation/media/ to change it: make copy-format FORMAT=words
	@test -n "$(FORMAT)" || { echo 'Name the format: make copy-format FORMAT=words' >&2; exit 2; }
	$(FGTOOLS) media --copy $(FORMAT)

# make site
# Builds, then makes the proof, the specimen and the media, and collects them
# into output/site/ with an index page. CI runs it on each push to main and
# publishes output/site/ on GitHub Pages.
site: proof specimen media ## Build, then make the proof, the specimen and the media, and collect them into output/site/
	$(FGTOOLS) site

# make proof-web
# Builds, then serves this font beside the fonts of reference-fonts/ in a
# browser, at one size and weight.
proof-web: $(BUILD) ## Build, then serve the font beside the fonts of reference-fonts/ in a browser
	$(FGTOOLS) proof-web --current

##@ Housekeeping

# make clean
# Removes fonts/ and output/. `make build` makes them again.
clean: ## Remove fonts/ and output/
	rm -rf fonts output

.PHONY: help setup venv build test masters test-google-fonts test-fontgarden status queue check-design check-changes render diff reference-fonts runebender formats proof specimen media copy-format site proof-web clean
