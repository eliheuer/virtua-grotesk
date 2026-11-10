---
name: render-specimen
description: Launch and inspect the live web proof that compares Virtua Grotesk with the reference fonts, or render fixed DesignBot proofs when requested.
---

# Render and inspect proofs

Read [AGENTS.md](../../../AGENTS.md) and the
[design rules](../../../design/README.md) for the glyphs in scope.

## Live comparison

`make proof-web` builds the fonts and serves the current build beside the fonts
in `reference-fonts/` at one em size and weight. The
[app guide](../../../agent-proofs/app/README.md) describes the modes and controls.

For a Before/Candidate comparison, prepare a snapshot from frozen font files with
`agent-proofs/app/prepare.py`, then run
`.venv/bin/python agent-proofs/serve.py --snapshot <prepared-directory>`. A
missing Before or Candidate font is a blocker. Do not substitute the current
build for it.

Inspect the browser rendering: font loading, controls, shaping, marks, bidi and
glyph coverage. Capture bounded screenshots. Missing reference coverage must be
visible; system fallback is not a reference glyph.

## Fixed proofs

- `make proof`: the main DesignBot PDF.
- `make review`: a separate Diffenator3 QA report.
- `agent-proofs/app/render-detail.py`: fixed 400 and 700 raster details for
  Arabic drawing, with Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex
  Pro when they are in `reference-fonts/`.

Report the output paths and the visible findings. Rendering success is not
approval. Eli gives the verdict.
