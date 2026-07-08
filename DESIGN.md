# DESIGN.md — The Virtua Grotesk Design System

This is the canonical description of how Virtua Grotesk glyphs are drawn. It
sits at the repo root because every part of the AI production pipeline
consumes it: image-generation prompts quote it, tracing and placement snap to
its grid, review gates check against it, and humans grade glyphs (mark colors
in Runebender) by it. If a glyph contradicts this document, the glyph is
wrong — or this document needs a deliberate edit.

A longer prose companion lives at
`documentation/source-guides/design-philosophy.md`; this file is the
normative summary.

## Identity

Virtua Grotesk is a **geometric grotesk drawn on a power-of-two grid**, with
**chamfered (beveled) corners** as its signature detail. It draws inspiration
from the grid discipline of **Replica** (Norm, Lineto, 2008) — a font famous
for committing to a coarse drawing grid and cut corners — reinterpreted here
as a retro-futuristic, technical sans: 1980s computer-interface signage redrawn
with modern precision. Strokes are monolinear; there is no thick/thin contrast.

## The power-of-two grid

Everything in this font is drawn against powers of two.

- **UPM 1024** (= 2^10). All vertical metrics are power-of-two sums:
  ascender 768, cap height 768, x-height 576, descender −256. Ascenders and
  caps share one height — a single 768 (512+256) ceiling.
- **Grid size 2**: every coordinate is an integer, and even numbers are
  strongly preferred. img2bez runs with `--grid 2`.
- **Favored measurements: 2, 4, 8, 16, 32, 64, 128, 256…** Stem widths,
  sidebearings, counters, overshoots, chamfers, and advance widths should land
  on powers of two — or short sums of them (e.g. 96 = 64+32, 160 = 128+32) —
  wherever the drawing allows.
- **Optical corrections are allowed and expected** — the grid is the starting
  point, not a cage. When a curve needs a 1–2 unit nudge to look right, the
  eye wins. But corrections are deviations *from* a power-of-two intent, so
  they should be small, even-numbered when possible, and never turn a
  deliberate measurement (a 16-unit chamfer, a 96-unit stem) into an arbitrary
  one.

## Vertical metrics

| zone | y | notes |
|---|---|---|
| ascender | 768 | shared with cap height |
| cap height | 768 | round caps overshoot to 784 (+16) |
| x-height | 576 | round lowercase overshoots to 592 (+16) |
| baseline | 0 | round forms overshoot to −16 |
| descender | −256 | |

Overshoot is **16 units** — one grid quantum of the design, same as the
chamfer. Flat forms (E, H, stems) sit exactly on the lines; only curves
overshoot.

## The 16-unit chamfer (non-negotiable)

Every sharp corner where two straight segments meet gets a **45° bevel,
16 units per side** in the Regular master. Coordinate pattern where a stem
meets the baseline at x: `(x−16−stem, 0) → (x−16, 0) → (x, 16)`.

Applies at stem–baseline and stem–cap junctions, crossbar ends (A H E),
apexes (A), and open terminals. The chamfer is always a straight line
segment, never a curve. **The chamfer stays the same absolute size in both
masters** (measured from the drawings: 16-unit cuts in Regular and Bold
alike, with 8-unit cuts at small junctions) — it reads relatively smaller
as the weight increases, which is the intended optical effect.

## Stroke and weight model

- **Monolinear**: stems, bars, and curves share one visual thickness.
  The exact per-master values live in the Dimensions table below.
- **Weight through counter reduction**: from Regular to Bold, round forms
  keep an (often identical) outer contour and gain weight by shrinking the
  counter inward. Straight forms thicken symmetrically inward. The silhouette
  stays stable across the weight axis.
- Bold optical shifts are allowed (e.g. Bold A's crossbar sits lower), but
  structure never changes between masters.

## Dimensions

The canonical measured dimensions of each master — the equivalent of the
Glyphs "Dimensions" widget, recorded here so agents and scripts have them as
context. **These values are the targets when boldening, tracing, or fitting
a glyph**: measure the work, then move points until its measurements match
this table (reference images calibrate everything the table doesn't cover —
optical weight distribution, never raw outlines).

| measure | where measured | Regular | Bold |
| --- | --- | --- | --- |
| cap stem (H, I) | vertical stem @ y=600 | 104 | 200 |
| cap bar (H) | crossbar @ x=center | 96 | 160 |
| cap round (O) | bowl side @ y=500 | 110 | 192 |
| x-height stem (n, t) | vertical stem @ y=288 | 96 | 192 |
| x-height round (o) | bowl side @ y=288 | 100 | 196 |
| chamfer, primary | corner cut | 16 | 16 (same absolute size; reads smaller in Bold) |
| chamfer, small | junction cut | 8 | 8 |

Reading the table: the ladder values (96, 192, 160) are the *intent*; the
off-ladder values (104, 110, 100, 196) are recorded **optical corrections**
— rounds run slightly wider than flats, caps slightly heavier than
lowercase. Both are canonical: when boldening a lowercase stem the delta
budget is 96 units (48 per side, symmetric inward per the counter-reduction
rule); when drawing a new round, start from the ladder and let the eye add
its correction, then record it here if it becomes a pattern.

Values were measured by inside/outside scans on the sources at the stated
heights (grid-2 exact). If a master's proportions are deliberately changed,
re-measure and update this table in the same commit.

## Curves

- Round outer contours are built from **4 cubic segments** — on-curve points
  at the exact N/S/E/W extrema, two off-curve handles per quadrant, handles
  on-axis (horizontal or vertical) at the extrema.
- Outer forms are precisely geometric (the O is a near-superellipse);
  counters may be slightly organic for warmth.
- Winding: outer contour clockwise, counters counter-clockwise.
- Generous counters and open apertures (c e s a) — this is not a closed
  grotesk, even in Bold.

## Spacing

- Sidebearings balanced for symmetric letters; round forms fit tighter than
  flat-sided forms (standard optical spacing).
- Sidebearings and advance widths on the power-of-two ladder (multiples of
  8 or 16 typical).

## Master compatibility (build constraint)

Both masters must have **identical contour count, point count, point types,
and point order** for every glyph — only coordinates and advance widths may
differ. This is a hard requirement of the variable build, checked by
`documentation/source/master-compatibility.md` (`make reports`).

## What the AI pipeline takes from this document

- **Image-generation prompts**: describe a monolinear geometric grotesk with
  45° cut corners on every sharp junction, open apertures, generous counters,
  no stroke contrast; one black glyph on white, drawn as if on a coarse grid.
- **Trace + placement**: `--grid 2`; snap near-horizontal/vertical/45° lines
  exactly; snap near-baseline/x-height/cap points to the metric lines;
  chamfer segments must survive tracing as straight lines.
- **Review gates**: check the 16-unit chamfers exist and are straight, curves
  have on-axis extrema, coordinates are even, key measurements sit on or near
  the power-of-two ladder, and the glyph's weight matches its master's stem
  ladder (≈96 Regular / ≈160+ Bold) — *measured*, not eyeballed. Spacing is
  deliberate: sidebearings referenced to structurally similar glyphs, never
  zero, never an outline touching the advance-box edges.
- **Human grading**: green means "this glyph obeys this document."
