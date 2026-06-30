---
name: glyph-ai-harness
description: Use when expanding, repairing, or drafting Virtua Grotesk glyphs with Runebender green reference labels, drawbot-skia source renders, OpenAI image generation, and img2bez tracing.
---

# Glyph AI Harness

Use this workflow for AI-assisted glyph expansion in Virtua Grotesk. It packages green Runebender reference glyphs, OpenAI image-generation prompts, and img2bez trace commands while keeping generated outlines staged until they are reviewed.

## Commands

```bash
make glyph-ai-inventory
make glyph-ai-prepare TARGET=<glyph-name> REFERENCES="a,e,exclam"
./.venv/bin/python scripts/glyph_ai_harness.py trace --run-dir build/glyph-ai-harness/<glyph-name>
```

Generated run packets live under `build/glyph-ai-harness/`, which is ignored through `build/`.

## Workflow

1. Run `make glyph-ai-inventory` and inspect `build/glyph-ai-harness/inventory.md`.
2. Choose green `good-reference` glyphs. Green is `public.markColor` `0.09,0.72,0.44,1`; other colors are queue labels, not automatic approval.
3. Prepare a target packet with `make glyph-ai-prepare TARGET=<glyph> REFERENCES="..."`.
4. Use the generated `prompts/<master>-<glyph>.md` with OpenAI image generation. Save outputs as `generated/<master>/<glyph>.png` inside the run packet.
5. Run the packet's `trace-commands.sh` or the `trace` subcommand to call `img2bez` into scratch UFO copies under `trace/`.
6. Review the traced glyphs in Runebender, render proofs, and run compatibility checks before copying outlines into `sources/`.

## Guardrails

- Treat img2bez output as a staged sketch unless the Regular and Bold structures match. Separate AI traces usually produce incompatible point counts.
- Preserve the 1024 UPM metrics: ascender `832`, descender `-256`, target image height `1088`, grid `2`.
- Use `--chamfer 0` for curved or mixed glyphs; only opt into `--chamfer 16` for line-based sharp forms after visual review, because automatic chamfering can flatten curves.
- Do not promote generated contours into active sources until `scripts/report_master_compatibility.py`, `make build`, and a proof/specimen review are clean for the target.
- Keep Runebender open with `make runebender` when doing hand cleanup so source edits live-reload and user saves remain ETag-guarded.

## Follow-Up Editing

If the trace is useful but incompatible, use it as a visual guide and redraw with `/draw-outline` or `/edit-glyph`. Keep both masters structurally identical: same contour count, point count, point types, components, and anchors.
