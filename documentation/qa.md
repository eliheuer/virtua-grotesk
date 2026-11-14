# Build and QA

Run the commands from the repository root. Use `.venv/bin/python` for scripts.

## Setup

`make setup` creates `.venv`, installs the pinned `requirements.txt`, and
runs `fgtools install-tools`, which installs the pinned fontc and Fontspector
binaries into `.venv/bin`. `requirements.in` lists the direct dependencies;
keep the two files in sync when you update the tools. On a platform that the
installer does not support, install the same versions into `.venv/bin`.

`make proof` needs [DesignBot](https://github.com/eliheuer/designbot). The
design checks need the Runebender binary; set `RUNEBENDER` if it is not at
`~/GH/repos/runebender/target/release/runebender` or on `PATH`.

## Build

`make build` runs `fgtools build`: it copies the sources to a temporary
directory and builds one variable TTF and four static TTFs with
`gftools builder` and fontc. Then it applies the three metadata fixes in
`scripts/fix_gf_metadata.py`. The static fonts are instances of the variable
font. A plain `gftools builder sources/config.yaml`, as the Google Fonts
packager runs it, builds the same fonts with fontmake, without those three
fixes. `fgtools diff --fontmake` checks that fontc and fontmake give the same
glyph and word images.

## Commands

| Command | Purpose |
| --- | --- |
| `make build` | Build the fonts into `fonts/`. |
| `make diff` | Build main and the working tree and compare them with diffenator3. `BASE=<revision>` compares with another revision. |
| `make test` | Development Fontspector checks, offline, with documented exclusions. |
| `make qa-full` | Full Font.Garden profile with network checks and no exclusions. |
| `make qa-package PACKAGE=<directory>` | Full profile on an assembled google/fonts package. |
| `make test-tools` | Tests of the Python and JavaScript tools. |
| `make status` | Rewrite `STATUS.md` from the mark colors. |
| `make check-design GLYPHS="..."` | Compare glyphs with the targets in `sources/design.toml`. |
| `make check-accents` | List the accented letters whose mark is not where the other accented letters predict, or not where the anchors of its parts are. |
| `make check-changes` | Check source changes since `main`: green glyphs unchanged, drafts purple. |
| `make lint-curves` | Curve fairness checks of the sources. Grid checks are in `make check-design`. |
| `make proof-web` | Compare the current build with `reference-fonts/` in a browser. |
| `make review` | Diffenator3 HTML proof in `out/review/`. |
| `make proof` | DesignBot PDF proof in `out/proof.pdf`. |

`fgtools qa` runs Fontspector with the Font.Garden profile of
fontgarden-tools. It includes the Google Fonts profile and adds the
Font.Garden requirements: a 1024-unit em, masters on the 2-unit grid, the
vendor ID FTGD and the OFL 1.1. `make qa` leaves out the checks listed with
their reasons in `[qa.exclude]` of `sources/design.toml`.

QA writes JSON and Markdown reports to `out/qa/<mode>/`. A FAIL returns a
failing exit status. A WARN needs review. No warning is waived automatically. The
[Google Fonts QA guide](https://googlefonts.github.io/gf-guide/qa.html)
explains the severities.

## After a source edit

1. Run `make check-changes` and `make check-design GLYPHS="..."` for the
   edited glyphs.
2. Run `make build`.
3. Look at the rendered glyphs in words, at reading and display sizes, at
   400, 550 and 700, beside the reference fonts (`make proof-web` or
   Runebender). Include the marks, joining forms and composites that use the
   edited glyphs.
4. Run `make diff`. It builds main and the working tree with fontc and
   compares them with diffenator3: glyph and word images at every instance,
   kerning, tables and language support. Every difference must be one that
   the edit explains. The HTML reports are in `out/diff/`.

Command success is not visual review. Numeric coverage does not show that a
script is correct. Eli gives the verdict on drawings.

## Proof rules

- Use the same em size, origin and baseline for every font in a comparison.
  Do not fit each glyph or font to its own size.
- A proof is valid only for the sources it was built from. Do not reuse an
  older proof after an edit, and do not rebuild a "before" state from the
  current sources. Build a known revision in a separate checkout.
- `out/` is ignored by Git. Its files do not exist in a new clone.

For a before and after comparison of glyphs, run
`make check-changes` with `--proof`, which draws Runebender proof sheets. Every
other rendered image is a DesignBot script (`.rs`) next to its output.
