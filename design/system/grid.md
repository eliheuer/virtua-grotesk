# Grid and metrics

`contract.json` is the machine-readable owner of shared metrics, palette and
source-grid rules. The em is 1024; ascender/caps 768, x-height 576, descender -256.
Source drawing metrics are distinct from font line-box and clipping metrics.
Read current fontinfo when changing engineering metrics.

New machine-drawn geometry, handles, advances and spacing use the 8-unit grid.
The source floor is 2; preserved human optical corrections may be off 8.
Never snap a protected or inherited human drawing to satisfy a new-draft check.
For bounded edits, report inherited exceptions separately from newly introduced
geometry. Record any explicitly authorized optical reuse or exception.

Run `scripts/draft_grid_check.py` on the named scratch glyphs and inspect its
point, anchor, component, actual-ink-sidebearing and advance findings. Scaled or
rotated components need decomposed scratch inspection. A trace on grid 2 alone
is not a completed machine draft.

Grid membership describes positions. Popcount describes measurements; high
popcount is not a fault. Do not round a measurement to improve its count or
trade a curve's construction or continuity for tidier numbers.

Check the source masters on their intended lattice. Interpolated positions and
compiled quadratic approximations need not remain on that lattice. Never use
those derived values to justify resnapping the source.
