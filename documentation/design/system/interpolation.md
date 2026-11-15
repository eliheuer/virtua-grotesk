## Master compatibility (build constraint)

Both masters must have **identical contour count, point count, point types,
and point order** for every glyph — only coordinates and advance widths may
differ. This is a hard requirement of the variable build, checked by
`.venv/bin/fgtools lint-glifs`.


## Bracket alternates (structure switches along the weight axis)

Some glyphs change **structure** at the bold end, not just weight (the
double-story `a` is the canonical grotesk case). The designspace
mechanism (equivalent of Glyphs bracket layers): an unencoded `.bold`
alternate glyph plus a `<rules processing="last">` substitution in
`VirtuaGrotesk.designspace`, conditioned on the Weight axis. It compiles
to `rclt` FeatureVariations in the variable font; fontmake bakes the
swap into static instances at or above the switch point (600 unless a
glyph demands otherwise).

Steps for each bracket glyph:

1. Eli draws the alternate structure in the Regular master, for example
   `a.bold` at Regular weight. It is the start of the interpolation and is
   not shown below the switch point.
2. The copy in the Bold master starts red and is drawn like any other glyph.
3. Add one `<sub>` line to the designspace.

Each of the two glyphs must be compatible between the masters, like every
other glyph.

## Rules

The rules of this subject are numbered in `context.md`.
