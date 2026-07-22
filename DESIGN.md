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

## The two lattices: division of labor

The grid is hierarchical, and the hierarchy assigns the work:

- **The 8-unit lattice is the machine's grid.** Advance widths,
  sidebearings, stem and bar widths, chamfer sizes, and every offset a
  tool fits or generates land on multiples of 8. Any tool that hands a
  human a draft containing 2-grid noise is broken: a human grading
  session must never include janitorial snapping. `make lint-grid`
  enforces this (machine drafts are the ERROR class; the *optical
  density* stat tracks it).
- **The 2-unit lattice is the human's grid.** Dropping from 8 to 2 is an
  optical correction — a decision only biological eyes can make, in
  Runebender, during grading. In a green glyph, every off-8 coordinate
  is deliberate design data.
- **Off the 2-grid is always an error**, for everyone.

This is also the data strategy: because machine drafts are 8-disciplined,
the diff between an orange draft and its human-approved green version
isolates pure optical knowledge — labeled training data for a future
optical-correction model. The machine proposes structure on 8; the human
teaches optics on 2; the dataset is the difference.

### The lattice split is a curriculum, not a wall

The end goal is automated type design: the systems should learn **how,
why, and where** the human makes optical corrections and eventually make
most of them automatically — balancing "stay on 8 by default" against
"deviate to 2 where the corpus shows eyes would". The division of labor
is therefore dynamic, governed by a trust ladder:

1. **Stage 0 (now):** machine emits 8-only drafts; the human makes every
   optical correction while grading. Each draft→green diff is captured
   (font-garden-lab `optics/extract_deltas.py`).
2. **Stage 1:** a model trained on those diffs *proposes* corrections in
   drafts. Acceptance rate is measured per geometric category (junction
   thinning, extreme overshoots, diagonal compensation, terminals…). The
   honest baseline it must beat: predict zero corrections everywhere.
3. **Stage 2:** categories with sustained high acceptance auto-apply in
   drafts. Categories graduate one at a time, with evidence — never by
   assumption (see the prefill post-mortem: models don't get deployed
   outside the distribution they were graded on).

Two things never automate: **green** (approval is a biological
signature), and corrections with no precedent in the corpus (novel
forms, whole-glyph proportion judgments). Nobody annotates "why" — the
local geometry around each corrected point is the label, and the model
learns the mapping the way sequence models always have.

## Curve smoothness comes before popcount

The power-of-two / low-popcount discipline exists for exactly one reason:
to make the sources compress into training data a small model can learn
efficiently. It is a **means, not the goal**, and it must never be pursued
at the expense of curve continuity. A kink costs the model far more than a
high-popcount coordinate ever saves.

- **A high-popcount coordinate is not a defect — it is signal.** It marks
  a place where an optical correction was needed. That tells the model
  "something happened here," which is useful information, not noise to
  scrub away. Do not blindly snap points toward round numbers to lower
  popcount.
- **If a "cleaner" number introduces a kink, a curvature jump, or a broken
  tangent, the clean number is wrong.** The eye and the curve win.
- **Priority order when they conflict:** (1) geometric continuity — G1
  tangent everywhere a point is smooth, and G2 curvature continuity
  wherever the design intends a smooth curve; then (2) correct optical
  weight and proportion; then (3) low popcount / power-of-two values where
  they cost nothing. **Popcount is the tiebreaker, never the master.**

Continuity vocabulary (used by the tools): **G0** positional only (a
corner — intended at sharp joins), **G1** tangent-continuous (handles
collinear through a smooth point), **G2** curvature-continuous (no visible
break in the curvature comb), **G3** curvature-derivative-continuous. Most
smooth points in Virtua should be at least G1, and the reference curves
(O H n o bowls and shoulders) should be G2.

We therefore analyze curves for continuity and curvature alongside the
grid metrics: `make grid-qa` / `make dashboard` report smoothness
(curvature discontinuities, kinks) per glyph, and Runebender draws a
curvature comb and continuity markers and offers harmonize / balance
tools. **A glyph is not signed off until its curves are smooth, not merely
until its numbers are round.**

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

## Reference glyphs: O H n o (the classical anchor)

Traditional type-design method, adopted here as process: **get O, H,
n, o right first — everything else derives from them.** H and O set
the uppercase (flat stem/bar vs round stroke, flat vs round
sidebearings, overshoot); n and o set the lowercase the same way.
Every other Latin glyph inherits its stems, curve weights, spacing
class, and overshoot from these four.

Practical consequences:

- These four glyphs get perfected on the grid system FIRST, in both
  masters, before mass-grading or training runs — an error here
  multiplies into the whole alphabet.
- When any of the four changes, the Dimensions table below must be
  re-measured in the same commit, and dependent glyphs re-checked
  against it.
- Agents evaluating or generating any Latin glyph should measure it
  against the current O H n o, not against stale table values or
  other unreviewed glyphs.

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
| cap bar (H) | crossbar @ x=center | 96 | 168 |
| cap round (O) | bowl side @ extremum | 108 | 204 |
| cap round horizontal (O) | crown/base @ extremum | 100 | 148 |
| x-height stem (n, t) | vertical stem @ y=288 | 96 | 192 |
| x-height round (o) | bowl side @ extremum | 100 | 196 |
| x-height round horizontal (o, n crown) | crown/base @ extremum | 92 | 140 |
| chamfer, primary | corner cut | 16 | 16 (same absolute size; reads smaller in Bold) |
| chamfer, small | junction cut | 8 | 8 |

Reading the table: the ladder values (96, 192, 168) are the *intent*; the
off-ladder values are recorded **optical corrections**, governed by three
rules: **curve = flat + 4 at the extremum, in both axes and both masters**
(vertical: 96→100, 104→108, 192→196, 200→204; horizontal: 88→92, 96→100);
**caps = lowercase + 8** (stems 96/104, corrections carried); and
**Regular→Bold growth comes in quanta of 24**: curve horizontals +48,
bars +72, verticals +96 — which is what keeps Medium and SemiBold on the
grid (delta/3 stays a multiple of 8). Both are canonical: when boldening a lowercase stem the delta
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

## Bracket alternates (structure switches along the weight axis)

Some glyphs change **structure** at the bold end, not just weight (the
double-story `a` is the canonical grotesk case). The designspace
mechanism (equivalent of Glyphs bracket layers): an unencoded `.bold`
alternate glyph plus a `<rules processing="last">` substitution in
`VirtuaGrotesk.designspace`, conditioned on the Weight axis. It compiles
to `rclt` FeatureVariations in the variable font; fontmake bakes the
swap into static instances at or above the switch point (600 unless a
glyph demands otherwise).

Workflow per bracket glyph: (1) Eli designs the alternate structure in
the REGULAR master (e.g. `a.bold` drawn at regular weight — it anchors
interpolation and is never shown below the switch); (2) the copy in the
Bold master starts red and gets lane-2 transferred from Eli's bold
reference image like any glyph; (3) one `<sub>` line in the designspace.
Both glyphs must each stay master-compatible with themselves — the
compat gate handles this with no special cases.
