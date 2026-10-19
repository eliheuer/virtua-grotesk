---
name: render-specimen
description: Render and inspect Virtua Grotesk proof or specimen output with designbot.
---

# Render specimen

For the main PDF, run `make proof` from the repository root and inspect
`documentation/proofs/proof.pdf`.

For browser spacing review, run `make review` and inspect the Diffenator3
report under `out/review/`.

`make specimen` is an unimplemented marketing-specimen target. Do not promise
or report a landscape spacing PDF from that command. If the user requests a
custom specimen, inspect the existing scripts under `documentation/` and
choose or adapt one for the requested format.

Render and inspect the actual result before describing layout, spacing,
missing glyphs, collisions, or drawing quality. Report the output path.

For before/after chat review, follow
[the chat proof workflow](../../../documentation/qa.md#chat-proof-workflow).
Use `scripts/proof_compare.py` with compiled before/after fonts and explicit
sample strings. Inspect its PNG; keep the accompanying JSON hashes and shaping
records. Do not auto-fit each glyph or infer aesthetic approval from pixel counts.
