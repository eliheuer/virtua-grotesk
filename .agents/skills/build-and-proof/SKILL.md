---
name: build-and-proof
description: Build the Virtua Grotesk fonts and render proofs of them. Use when asked to build, compile or regenerate the fonts, or to make or look at a proof, specimen or comparison with the reference fonts.
---

# Build and proof

Run every command from the repository root.

## Build

`make build` builds the variable font and four static fonts into `fonts/`
with `gftools builder` and fontc (`fgtools build`), then applies
`scripts/fix_gf_metadata.py`. If the build fails, read the error
output. Common causes are incompatible masters, a missing glyph and invalid
GLIF XML.

## Proofs

| Command | Output |
| --- | --- |
| `make proof-web` | Serves the current build beside the fonts in `reference-fonts/` at one em size and weight (`fgtools proof-web`). |
| `make proof` | DesignBot PDF proof in `out/proof.pdf`, generated from the font. |
| `make diff` | diffenator3 comparison of main and the working tree in `out/diff/`. Run it after every source edit. |
| `make review` | diff3proof browser proof of the current build in `out/review/`. |
| `make check-changes GLYPHS="..."` with `--proof <dir>` | Runebender proof sheets of changed glyphs, before and after. |

For a Before and Candidate comparison in the web proof, prepare a snapshot
from fixed font files with `.venv/bin/fgtools proof-web prepare`, then run
`.venv/bin/fgtools proof-web --snapshot <directory>`. If the
Before or Candidate font is missing, stop. Do not use the current build in
its place.

Specimen and publicity images are DesignBot scripts (`.rs`) in
`documentation/`, next to their output. Run them with
`designbot <script>.rs --output <file>` after `make build`.

## Report

Look at the rendered output before you describe it: font loading, shaping,
marks, right-to-left text and coverage. A reference font without a glyph must
show as missing, not as a system fallback. Give the output paths and the
visible findings. A rendered proof is not approval. Eli gives the verdict.
