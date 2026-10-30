# Historical measured Latin construction

Moved intact from DESIGN.md on 2026-10-29. Verify against live green donors; these values do not silently override a subsequent human correction.

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
