---
name: compare-reference
description: Compare a reference image against the current font rendering and propose specific glyph edits. Use when given a reference or target image for a glyph.
---

# Compare a reference

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation inspect`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Inspect the supplied image, identify text/glyphs, intended form and reference role.
Separate a human target drawing from an external font comparison and a current green
Virtua construction donor. Preserve supplied references and provenance in the case.

Build when sources changed, then use the live browser proof (render-specimen) for
matching text at equal em scale. Inspect coverage, shaping, baseline and weight
before comparing proportions, opposing-edge weight, counters, terminals and spacing.
For calibrated sheets use anchor-sheet-glyphs. List concrete bounded changes with
named glyphs/masters and evidence; comparison alone does not authorize application.
