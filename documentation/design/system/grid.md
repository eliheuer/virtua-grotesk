# Grid and metrics

`sources/design.toml` holds the grid values and the mark colors that scripts read.
The em is 1024; ascender/caps 768, x-height 576, descender -256.
Source drawing metrics are distinct from font line-box and clipping metrics.
Read current fontinfo when changing engineering metrics.

New machine-drawn geometry, handles, advances and spacing use the 8-unit grid.
The source floor is 2; preserved human optical corrections may be off 8.
Never snap a protected or inherited human drawing to satisfy a new-draft check.
For bounded edits, report inherited exceptions separately from newly introduced
geometry. Record any explicitly authorized optical reuse or exception.

Run `make check-design GLYPHS="..."` on the named glyphs. Runebender's glyph
analysis reports the points on the 2, 4 and 8 grids and whether the advance is
on 8. Scaled or rotated components need decomposed inspection. A trace on
grid 2 alone is not a completed machine draft.

Grid membership describes positions. Popcount describes measurements; high
popcount is not a fault. Do not round a measurement to improve its count or
trade a curve's construction or continuity for tidier numbers.

Check the source masters on their intended lattice. Interpolated positions and
compiled quadratic approximations need not remain on that lattice. Never use
those derived values to justify resnapping the source.

## Rule entries

### Stroke weights are optical values

Stems, round sides and crowns can be off the 8-unit grid. The 8-unit grid is
for spacing and structure. Do not round Eli's stroke values to 8.
Seen in: o side 98 and crown 84 (324e6a15), cap stems 100 (cbb174ea).

### Derived points

An intersection or a cut endpoint snaps to the 8-unit grid if it is within 3
units of it. Otherwise it snaps to the 2-unit grid.
Seen in: v w x y V W X (9a2e884d).
