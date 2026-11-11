# Build and QA

Run the commands from the repository root. Use `.venv/bin/python` for scripts.

## Setup

`make setup` creates `.venv`, installs the pinned `requirements.txt` and
installs Fontspector into `.venv/bin`. `requirements.in` lists the direct
dependencies; keep the two files in sync when you update the tools. On a
platform that the installer does not support, install the same Fontspector
version and set `FONTSPECTOR=/path/to/fontspector`.

`make proof` needs [DesignBot](https://github.com/eliheuer/designbot). The
design checks need the Runebender binary; set `RUNEBENDER` if it is not at
`~/GH/repos/runebender/target/release/runebender` or on `PATH`.

## Build

`make build` copies the sources to a temporary directory, builds one variable
TTF and four static TTFs with gftools, and applies the metadata fixes in
`scripts/fix_gf_metadata.py`. The static fonts are instances of the variable
font. `make build-fontc` is an alternative compiler, not the release build.

## Commands

| Command | Purpose |
| --- | --- |
| `make build` | Build the fonts into `fonts/`. |
| `make test` | Development Fontspector checks, offline, with documented exclusions. |
| `make qa-full` | Full Google Fonts profile with network checks and no exclusions. |
| `make qa-package PACKAGE=<directory>` | Full profile on an assembled google/fonts package. |
| `make qa-hebrew` | Hebrew coverage and mark attachment, with proofs in `out/hebrew/`. |
| `make test-tools` | Tests of the Python and JavaScript tools. |
| `make status` | Rewrite `STATUS.md` from the mark colors. |
| `make check-design GLYPHS="..."` | Compare glyphs with the targets in `sources/design.toml`. |
| `make check-changes` | Check source changes since `main`: green glyphs unchanged, drafts purple. |
| `make lint-curves` | Curve fairness checks of the sources. Grid checks are in `make check-design`. |
| `make proof-web` | Compare the current build with `reference-fonts/` in a browser. |
| `make review` | Diffenator3 HTML proof in `out/review/`. |
| `make proof` | DesignBot PDF proof in `out/proof.pdf`. |
| `make reports` | Source, compatibility and binary metadata reports in `out/reports/`. |

QA writes JSON, Markdown and tool versions under `out/qa/`. Set
`QA_REPORT_DIR` for a separate run. A FAIL returns a failing exit status. A
WARN needs review. No warning is waived automatically. The
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
4. For a regression comparison between two builds:

   ```sh
   .venv/bin/diffenator3 OLD.ttf NEW.ttf --html --instance '*' --output out/diff
   ```

Command success is not visual review. Numeric coverage does not show that a
script is correct. Eli gives the verdict on drawings.

## Proof rules

- Use the same em size, origin and baseline for every font in a comparison.
  Do not fit each glyph or font to its own size.
- A proof is valid only for the sources it was built from. Do not reuse an
  older proof after an edit, and do not rebuild a "before" state from the
  current sources. Build a known revision in a separate checkout.
- `out/` is ignored by Git. Its files do not exist in a new clone.

`scripts/proof_compare.py` (before and after, with a difference panel) and
`scripts/proof_reference.py` (Virtua beside reference fonts) render shaped
PNG comparisons for a diagnostic that the browser proof does not give. Each
needs a `--samples` file: a JSON list of objects with `label`, `text` and an
optional `size`. Write it under `out/`.
