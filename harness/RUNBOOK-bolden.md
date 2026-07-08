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
   a. **Neural pre-fill** — the glyph model in `font-garden-lab` predicts
      per-point Bold deltas from the Regular (structure-compatible by
      construction). Batch drafts arrive via a prefill UFO; copy the glyph's
      outline from there.
   b. **Analogy from a bolded neighbor** — copy the deltas of the most
      similar already-bolded glyph (e.g. bolden `dal-ar` by analogy to
      `reh-ar`), then adjust.
   c. **Manual** — thicken stems per `DESIGN.md`'s Bold measurements.

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

## Batch mode

Process at most 10–20 glyphs per session, grouped by script/similarity
(all Arabic digits together, all marks together), then STOP for a human
grading pass. Model retraining consumes graded glyphs nightly — quality of
the grade is quality of tomorrow's model.
