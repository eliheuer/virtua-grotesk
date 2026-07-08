# RUNBOOK: Clearing Bold Debt

Procedure for turning a red-marked, structure-identical Bold copy into a
real Bold glyph. For any agent driving this repo (Codex GUI, Claude Code)
and for humans. Companion to `RUNBOOK-codex.md` (which covers adding *new*
glyphs from images; this runbook covers *boldening existing* glyphs).

## The one inviolable rule

**The Bold master must stay point-compatible with the Regular.** Same
contours, same point count, same point types, same order. You never add,
remove, or reorder points while boldening — you only *move* them. A raw
autotrace of a bold reference image is therefore NEVER pasted into the Bold
master: traces have their own point structure. References calibrate;
Regular's structure is the skeleton.

## Provenance rule

Reference images of existing typefaces (e.g. a Helvetica Bold screenshot)
are used to calibrate **weight, proportion, and optical behavior** — how
much stems thicken, how counters compress, where weight pools. Their
*outlines are never traced into the sources.* Every outline in this font
derives from Virtua's own Regular structure plus deltas, restyled by
`DESIGN.md` (grid 2, 16-unit chamfers, powers-of-two measurements). The
training-data manifest stays auditable: everything in the UFOs was drawn
here.

## Inputs

- `GLYPH`: the glyph name (must exist in both masters, marked red/debt).
- Optional `REF_IMAGE`: a bold reference at display size — a screenshot of
  a bold grotesk (Helvetica Bold, Replica Bold…) or an image-API render.
  High-res (≥1024px tall), black on white, single glyph.

## Procedure

1. **Confirm the debt.** The Bold glif's outline is geometrically identical
   to Regular's (or the mark color is red). If it already differs, stop —
   this glyph needs grading, not boldening.

2. **Get a draft Bold.** In order of preference:
   a. **Lane-2 form transfer** (line-only glyphs; the proven path) — a
      HUMAN picks a reference image whose form fits the glyph (this is a
      design decision, never automated), then the `glyph-transfer` tool in
      `font-garden-lab` fits the Regular outline to it in edge-offset
      space: edge orientations immutable (the style), corner cuts
      manufactured at spec, vertical metrics pinned, everything on grid 2.
      Structure-compatible by construction.
        cd ~/GH/repos/font-garden-lab
        .venv/bin/python transfer/bolden_one.py GLYPH --image REF.png
      Sidebearings inherit the Regular's by default (`--lsb/--rsb` to
      override); `--lambda` dials form-trust. Graded results: exclam,
      four. Reference choice is why comma failed — wrong reference form,
      not a tool bug.
   b. **Neural pre-fill** — the glyph model in `font-garden-lab` predicts
      per-point Bold deltas from the Regular. In-distribution glyphs only
      (see the prefill post-mortem: OOD deploys produce garbage).
   c. **Analogy from a bolded neighbor** — copy the deltas of the most
      similar already-bolded glyph (e.g. bolden `dal-ar` by analogy to
      `reh-ar`), then adjust.
   d. **Manual** — thicken stems per `DESIGN.md`'s Bold measurements.

3. **Fit to the Dimensions table.** `DESIGN.md`'s **Dimensions** section is
   the primary target: measure the draft (stems, bars, rounds at the stated
   heights) and move points until its measurements match the Bold column —
   e.g. a lowercase stem gains 96 units, 48 per side, symmetric inward per
   the counter-reduction rule. The reference image covers only what the
   table doesn't: optical weight distribution, how a specific form carries
   boldness. If you trace the reference (`img2bez --format json --grid 2`),
   use the trace as a ruler — measurements only, never outlines.

4. **Restyle to spec.** All coordinates on grid 2 (even integers), chamfers
   16 units, vertical metrics untouched (asc 768 / cap 768 / x 576 /
   desc −256; overshoots +16). Sidebearings: adjust per `DESIGN.md` spacing
   rules — Bold sidebearings typically tighten by a ladder step; advance
   widths stay power-of-two sums wherever the drawing allows.

5. **Verify.**
   - Structure check: point-structure signature identical to Regular
     (the build's compat gate must stay green).
   - `make build && make test` (Fontspector gate) — never re-add excludes.
   - `make proof` and eyeball the interpolation: instances at 500/600 must
     look like the same glyph gaining weight, no kinks.

6. **Mark and hand off.** Set the mark color to **orange** (machine/agent
   draft, needs human polish). Never self-assign green — green is the
   human's call, made in Runebender (`make runebender`).

## The grading contract (two lattices — see DESIGN.md)

A draft handed to the human must be **8-disciplined**: advance width,
sidebearing-derived spacing, stem widths, and all fitted offsets on the
8-unit lattice; cuts at spec; metrics pinned. The human's grading time is
reserved for **optical corrections** — the deliberate 8→2 deviations only
eyes can make. If a grading session involves snapping anything back to
the 8-grid, that is a tool bug: fix the tool, don't keep cleaning.
`make lint-grid` checks drafts; the orange optical-density stat is the
tool-noise alarm.

## Batch mode

Process at most 10–20 glyphs per session, grouped by script/similarity
(all Arabic digits together, all marks together), then STOP for a human
grading pass. Model retraining consumes graded glyphs nightly — quality of
the grade is quality of tomorrow's model.
