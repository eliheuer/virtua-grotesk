---
name: anchor-sheet-glyphs
description: Add or rebuild glyphs from anchor-calibrated reference sheets — one image containing a known green glyph plus targets. Covers calibration (anchor_sheet.py), parametric generation for line-grammar glyphs (symbol_gen.py), img2bez for organic glyphs, and the running LESSONS.md log. Use whenever building glyphs from a reference image, and APPEND to LESSONS.md whenever Eli corrects an output.
---

# /anchor-sheet-glyphs

Build missing or red glyphs from **anchor sheets**: a single image of glyphs
on one baseline that includes at least one glyph that already exists green
in the sources (the *anchor*, usually `n`). The anchor makes the sheet
self-calibrating — its known ink height gives px→unit scale and baseline,
eliminating scale guessing (historically the #1 cause of bad traces).

**Read `LESSONS.md` in this directory before generating anything** — it is
the running log of optical corrections Eli has made to generated output.
Every rule there outranks the formulas. **When Eli corrects a generated
glyph, append the rule to LESSONS.md in the same session**, with the date,
the glyph, exact numbers, and (when captured) the generator change.

## The pipeline

1. **Calibrate + measure** the sheet:
   ```sh
   ./.venv/bin/python scripts/anchor_sheet.py SHEET.png n less equal greater \
       --json /Users/eli/Temp/sheet.json
   ```
   Names are left-to-right; `--anchor N` if the anchor isn't first.
   Output: per-glyph width / vertical extent / center / stroke cuts, all in
   font units relative to the real baseline.

2. **Sanity-check the calibration** — always cross-validate one measured
   stroke against a system-derived expectation (e.g. symbol stroke ≈
   hyphen × HN's 64/80 math ratio). Within a few units = trust the sheet.
   THE SHEET IS AUTHORITATIVE over reference fonts: if its axis or
   proportions disagree with Helvetica/Inter, the sheet wins (Eli chose it).

3. **Reconstruct**, by glyph class:
   - **Line-grammar glyphs** (math, punctuation, arrows, dashes, PUA
     icons): do NOT trace. Extract parameters (axis, box, stroke, gaps,
     angles) and generate with `scripts/symbol_gen.py` — grammar constants
     and glyph generators live there; add a `gen_<name>()` per new glyph.
     Bold is derived (same box/axis, stroke from the class weight ratio),
     so master compatibility holds by construction.
   - **Organic glyphs** (Arabic, drawn Latin): crop per glyph and run
     `img2bez masters` with EXACT `--fit` derived from the calibration,
     then apply the system snap pass (weights → palette, corners → 16u
     bevels, 2-grid, sb classes). Verify per harness/RUNBOOK-codex.md.

4. **Verify** before showing: bbox/advance/axis assertions, stroke scans at
   two heights, `make build` (master compat), shaped-text render at both
   weights (uharfbuzz), curve_lint for anything curved, and
   **`scripts/curve_continuity.py <Master> <glyphs>`** — the Runebender
   G0–G3 overlay as a CLI gate. It must exit 0: no KINKs, line↔curve
   joints tangent, every smooth curve-curve joint G2. Mark results
   **blue** and stop — Eli grades.

## Grammar constants (Regular / Bold)

- Grid 2 (all values even) · bevels 16u at 45° · notch flats 8u total
- Math axis **352** · math stroke **72 / 132** · math advance **600**
- Symbol widths follow the sheet (Helvetica-proportioned per the width
  pass); sidebearings symmetric inside the class advance
- Weight palette elsewhere: cap stems 100/192, lc stems 96/192, cap
  horizontals 96, rounds 102/204, lc rounds 98/196, hyphen 88/TBD

## Model integration (virtua-12m)

The model's job is to SUPPLY sheets for glyphs with no reference: generate
on anchor-sheet canvases (green context glyphs + target slot) so outputs
enter this same pipeline. The verify gates in step 4 are the accept/reject
filter for model output. Human sheets and model sheets go through one door.
