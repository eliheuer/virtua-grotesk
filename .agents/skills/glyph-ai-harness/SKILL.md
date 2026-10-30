---
name: glyph-ai-harness
description: Use when expanding, repairing, or drafting Virtua Grotesk glyphs with Runebender green reference labels, designbot source renders, OpenAI image generation, and img2bez tracing.
---

# AI image and trace workflow

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation from-image`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Follow [the organic image runbook](../../../harness/RUNBOOK-codex.md). For sheets
use anchor-sheet-glyphs. The harness prepares context, current/green reference
renders, image prompts and one joint-master scratch trace; it never applies sources.

```sh
make glyph-ai-inventory
make glyph-ai-prepare TARGET=<glyph> REFERENCES="n,o" FIT=<calibrated-bottom:top>
.venv/bin/python scripts/glyph_ai_harness.py trace --run-dir .glyph-ai-runs/<glyph>
```

Preparation requires both masters, a fresh run directory and an explicit fit band.
Only verified green references qualify; the contract recognizes current color
variants and rejects conflicting grades. The packet includes hashes for target,
references and affected consumers. Trace refuses stale/legacy packets and existing
trace directories. Inspect `img2bez masters --help` for installed flags.

Joint tracing must report compatible=true and lowConfidence=false. A trace is still
a candidate: inspect calibrated bounds/metrics, refit on the draft grid, verify
curves and compiled shapes, and show proofs. Preserve the intended form; a flawed
trace calls for tuning/retracing, not an unrelated hand-drawn approximation.
