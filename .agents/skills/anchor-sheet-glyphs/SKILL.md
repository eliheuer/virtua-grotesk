---
name: anchor-sheet-glyphs
description: Build glyphs from anchor-calibrated reference sheets containing a known green glyph and targets. Use for sheet calibration, line-grammar generation or organic tracing; retrieve and record scoped corrections in design/corrections.
---

# Build from an anchor sheet

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation from-image`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Use [harness/RUNBOOK-anchor-sheets.md](../../../harness/RUNBOOK-anchor-sheets.md).
Calibrate against a known green glyph in the sheet, inspect crop bounds and a known
stroke, and retain the calibration evidence. Use symbol_gen for line-grammar
symbols; use img2bez masters on scratch for organic outlines with the calibrated
fit band. Preserve donor point order and master compatibility.

Applicable historical lessons are indexed by glyph/operation in the context packet.
When Eli corrects an output, capture exact feedback and pairs in the current review,
then add a record under design/corrections/records. Do not append to the retired
LESSONS.md or treat its historical blue/grid instructions as current.

Follow the shared grid, purple labeling and verification contract. Inspect signed
curvature and intended joins; do not force every curve to G2 or round away corners.
