---
name: render-specimen
description: Launch and inspect the default live web proof for Virtua design review, or render fixed DesignBot proofs when requested.
---

# Render and inspect proofs

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation inspect`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Use `make proof-web` and [the app guide](../../../agent-proofs/app/README.md) for
interactive Before/Working/reference comparison. Preserve the accepted interface,
two grays, aligned labels, scale/weight controls and actual browser font rendering.
Choose exact verified snapshots; label Candidate/Applied/Rejected accurately.
Current state comes from design/reviews/current.json, not an old phase queue.

For new snapshots use app/prepare.py with the current schema/example and frozen
font files. A missing before/candidate file is a blocker; never silently substitute
current builds. Live references come from reference-fonts with coverage/hash checks.
Inspect browser loading, controls, shaping and glyph coverage; capture screenshots.

`make proof` produces the main DesignBot PDF. `make review` produces a separate
Diffenator3 QA report. `make specimen` remains unimplemented. For fixed comparative
exports follow documentation/qa.md and documentation/proofs/hebrew_review.rs; use
Virtua labels, fixed em scale/origin/baseline, title case, light/dark two-gray output,
zero text tracking and --raw. Inspect output plus the grid version.

Arabic drawing also requires fixed raster inspection at 400/700 via
agent-proofs/app/render-detail.py with Before, Working, Rubik, Noto Sans Arabic,
IBM Plex Sans Arabic and Readex Pro. Record visible findings alongside snapshots;
missing fonts/coverage must be explicit. Do not delay a focused candidate review
for broad QA. Reusable feedback belongs in design/corrections.
