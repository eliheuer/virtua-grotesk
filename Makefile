# The core commands for this project. Run `make` or `make help` for the list.
#
# Most targets run one command for fgtools (https://github.com/fontgarden/fgtools),
# the shared tools of Font.Garden projects. `.venv/bin/fgtools --help` lists
# every command, and `.venv/bin/fgtools <command> --help` lists its options.
# Make handles build dependencies and project entry points. Shared font
# operations live in fgtools.
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
# Targets with the BUILD prerequisite build the fonts first. Use NO_BUILD=1
# to reuse fonts/ for those targets, for example make test NO_BUILD=1.
BUILD = $(if $(NO_BUILD),,build)

##@ Help

# make help
# Prints each target that has a `## description`, under the `##@` section
# titles, then the note on NO_BUILD. It is the first target, so `make` alone
# runs it.
help: ## Print this list
	@awk -F ':.*## ' '/^##@ / {printf "\n%s\n", substr($$0, 5)} /^[a-z-]+:.*## / {printf "  make %-18s %s\n", $$1, $$2}' Makefile
	@echo
	@echo 'Use NO_BUILD=1 to reuse fonts/ for tests, proofs and media.'

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
# The Fontspector run uses the exclusions and reasons in [qa.exclude] of
# CONTEXT.md. Some Google Fonts checks need the internet.
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
# Run after edits to Regular or Bold at 14 pt. This runs the shared fgtools
# commands in dependency order: weight extremes, then optical size.
# Each drafting command handles preservation of hand corrections.
masters: ## Calculate Thin, Black and the 144 pt masters from Regular and Bold
	$(FGTOOLS) draft-weights --write
	$(FGTOOLS) draft-optical-size --write

# make reference-fonts
# Downloads the reference fonts that CONTEXT.md lists into reference-fonts/,
# which Git ignores. Runebender can show them beside this font.
reference-fonts: ## Download the reference fonts that CONTEXT.md lists into reference-fonts/
	$(FGTOOLS) fetch-reference-fonts --project

# make runebender
# Opens the designspace in the desktop editor via the runebender CLI.
runebender: ## Open the designspace in Runebender
	runebender sources/VirtuaGrotesk.designspace &

##@ Proofs and media

# DesignBot renders the proof PDFs and the marketing media.
# Video rendering also uses ffmpeg. Git ignores the generated output/ folder.

# make proofs
# Build the source PDF and plot, then render the Print Proof, Full Proof
# and their red-grid versions into output/proof/. PAGE selects the detail formats.
proofs: $(BUILD) ## Build Print and Full Proofs with and without the grid
	$(PYTHON) sources/proof_review.py --build-proof $(PAGE)

# make media
# Builds, then renders the images, carousels and videos for the social
# platforms into output/media/. The review page is output/media/index.html.
# The brand of this font is documentation/media/brand.toml.
# List formats and canvases with `.venv/bin/fgtools media --list`.
# Render a subset:
#   make media FORMAT=videos                one kind: images, carousels or videos
#   make media FORMAT="words glyph"         some formats; `glyph` is the technical image
#   make x-animation                clean, red-grid and CRT landscape animations
#   make media LATTICE=1                    also each picture with the lattice drawn on it
x-animation: $(BUILD) ## Render clean, red-grid and CRT X animations
	@set -e; for script in documentation/media/x/animations/*.rs; do .venv/bin/designbot "$$script"; done

media: $(if $(strip $(FORMAT)$(CANVAS)),,x-animation) $(BUILD) ## Render all marketing media
media-generic: $(BUILD) ## Render Font.Garden layouts with this font’s branding
media-custom: $(if $(strip $(FORMAT)$(CANVAS)),,x-animation) $(BUILD) ## Render marketing layouts defined by this project
media media-generic media-custom:
	$(FGTOOLS) media $(if $(filter media-%,$@),--layouts $(patsubst media-%,%,$@)) $(FORMAT) $(if $(CANVAS),--canvas $(CANVAS),) $(if $(LATTICE),--lattice,)

##@ Housekeeping

# make clean
# Removes built fonts and generated output. Run the corresponding target
# to regenerate each artifact.
clean: ## Remove built fonts and generated review files.
	rm -rf fonts output

.PHONY: help
.PHONY: setup venv
.PHONY: build test test-google-fonts test-fontgarden
.PHONY: status queue check-design check-changes render diff masters reference-fonts runebender
.PHONY: proofs x-animation media media-generic media-custom
.PHONY: clean
