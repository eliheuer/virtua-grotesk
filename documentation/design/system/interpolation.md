## Master compatibility (build constraint)

Both masters must have **identical contour count, point count, point types,
and point order** for every glyph — only coordinates and advance widths may
differ. This is a hard requirement of the variable build, checked by
`out/reports/master-compatibility.md` (`make reports`).


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

## Rule entries

### No overlapping contours in sources

Union overlapping parts into one contour. Sources never contain overlaps.
Seen in: dollar (7f8be952), one.tf (dbe60148).

### A weight transfer keeps edge directions

A Bold edge has the same direction as the Regular edge it comes from.
Seen in: Bold seven nine (70c6a082).

### Contour start point

The start point is on the side where the writing direction starts: the
leftmost point for Latin, the rightmost point for Arabic and Hebrew. If two
points tie, the lowest one is the start point. This replaces the
leftmost-then-lowest rule of 56f4b437 for right-to-left scripts.
Seen in: asciitilde (56f4b437), Eli's instruction (2026-11-10).
