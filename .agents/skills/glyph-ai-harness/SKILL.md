---
name: glyph-ai-harness
description: Use when expanding, repairing, or drafting Virtua Grotesk glyphs with Runebender green reference labels, designbot source renders, OpenAI image generation, and img2bez tracing.
---

# Glyph AI Harness

Use this workflow for AI-assisted glyph expansion in Virtua Grotesk. It packages green Runebender reference glyphs, OpenAI image-generation prompts, and img2bez trace commands while keeping generated outlines staged until they are reviewed.

For script expansion requests such as "add the missing Hebrew to this font",
follow `documentation/glyph-ai-harness-workflow.md` first. That document is the
end-to-end workflow contract for inventory, reference rendering, OpenAI raster
generation, img2bez tracing, compatibility, spacing, specimen review, and
promotion.

## Commands

```bash
make glyph-ai-inventory
make glyph-ai-prepare TARGET=<glyph-name> REFERENCES="a,e,exclam"
./.venv/bin/python scripts/glyph_ai_harness.py trace --run-dir .glyph-ai-runs/<glyph-name>
```

Generated run packets live under `.glyph-ai-runs/`, which is ignored but is not removed by `make build` or `make test`.

The current repo command surface is single-glyph oriented. For larger script
work, create a run packet under `.glyph-ai-runs/<script-or-batch>/`,
document the target glyphset there, and stage generated/traced output until the
promotion gate is clean.

## Workflow

1. Run `make glyph-ai-inventory` and inspect `.glyph-ai-runs/inventory.md`.
2. Choose green `good-reference` glyphs. Green is `public.markColor` `0.09,0.72,0.44,1`; other colors are queue labels, not automatic approval.
3. Prepare a target packet with `make glyph-ai-prepare TARGET=<glyph> REFERENCES="..."`.
4. Use the generated `prompts/<master>-<glyph>.md` with OpenAI image generation. Prefer reference-image workflows that include rendered green glyphs as input images. Save outputs as `generated/<master>/<glyph>.png` inside the run packet.
5. Run the packet's `trace-commands.sh` or the `trace` subcommand to call `img2bez` into scratch UFO copies under `trace/`.
6. Review the traced glyphs in Runebender, render mixed target/reference specimens, and run compatibility checks before copying outlines into `sources/`.

## Guardrails

- Treat img2bez output as a staged sketch unless the Regular and Bold structures match. Separate AI traces usually produce incompatible point counts.
- Detect the installed img2bez interface before tracing. Upstream img2bez documents a `masters` workflow for variable-font compatibility, but older local binaries expose only single-master tracing. Prefer `img2bez masters` when available; otherwise trace to scratch UFOs and reconcile structure before promotion.
- Preserve the 1024 UPM metrics: ascender `832`, descender `-256`, target image height `1088`, grid `2`.
- Use `--chamfer 0` for curved or mixed glyphs; only opt into `--chamfer 16` for line-based sharp forms after visual review, because automatic chamfering can flatten curves.
- Do not promote generated contours into active sources until `scripts/report_master_compatibility.py`, `make build`, and a proof/specimen review are clean for the target.
- Keep Runebender open with `make runebender` when doing hand cleanup so source edits live-reload and user saves remain ETag-guarded.

## Required Review Loop

For every generated glyph or batch:

1. Render green references and the new glyphs in the same specimen image.
2. Check weight, vertical placement, sidebearings, and rhythm.
3. Use AI/vision review only for bounded proposals such as scale, translate,
   sidebearing deltas, and issue labels; do not let it rewrite sources directly.
4. Apply deterministic edits in the UFOs or scratch UFOs.
5. Rerun compatibility, build, proof/specimen, and source reports.

## Follow-Up Editing

If the trace is useful but incompatible, use it as a visual guide and redraw with `/draw-outline` or `/edit-glyph`. Keep both masters structurally identical: same contour count, point count, point types, components, and anchors.
