# Virtua Grotesk design rules

The rules of this font for every drawing, draft and review, and the values
that the tools check. This is the one design file of the project. Runebender
gives it to its agents (`design_context`), and the task contracts and the
review in `.agents/` require it.

A `toml` code block holds the values of the rule above it. `fgtools` reads
only these blocks, as one TOML document. Font metrics are in the
`fontinfo.plist` files and the weight axis is in the designspace; they are
not repeated here.

How to use it:

- Before you draw or change a glyph, read every rule here, not only the
  section of its script.
- When you review a glyph, check it against every rule that applies, by
  number: "R12: passes" or "R12: fails at (64,624), the tip has no flat".
  Then look at the whole glyph for faults that no rule names.
- When Eli corrects a glyph and the reason is a principle, add a rule here
  with "Seen in" and the commit, or add the commit to the rule that covers it.

## Character

R1. Virtua is a geometric grotesque on a dyadic grid: straight chamfered
corners, monolinear apparent weight, smooth deliberate cubic curves and open
counters. The character is clean, neo-modernist and machined.

R2. The reference fonts do not dictate the design. Compare visual weight,
spacing, outline consistency and the structure readers expect. A small
difference of form is not a fault; a glyph very different from all of them
needs a reason.

R3. Draw from green Virtua glyphs of the same construction (the donors): read
their points and their filled shape. A glyph that is not green is not a
donor.

R4. A local correction of one glyph (Zayin, Gimel, Final Tsadi, hamza) is an
example for that glyph and master, not a formula for others.

## Grid and metrics

R5. The em is 1024. Ascender and cap height 768, x-height 576, descender
-256. The Hebrew letter height is 640.

R6. Every point is on the 2-unit grid. New structural points, handles,
advances, sidebearings and kerning use the 8-unit grid. A point on 2 and off
8 is an optical correction by Eli: keep it, never snap it.

```toml
[grid]
source = 2         # every point is on the 2-unit grid
machine_draft = 8  # new drafts use the 8-unit grid
```

R7. An intersection or a cut end point snaps to the 8-unit grid when it is
within 3 units of it, else to the 2-unit grid.
Seen in: v w x y V W X (9a2e884d).

R8. Stroke weights are optical values. Stems, round sides and crowns can be
off the 8-unit grid; do not round Eli's stroke values.
Seen in: o side 98 and crown 84 (324e6a15), cap stems 100 (cbb174ea).

## Corners, tips and joins

R9. Every corner where two straight segments meet has a 45 degree bevel of
16 units per side in Regular. Tight junctions use 8. The bevel is a straight
segment, never a curve, and keeps its absolute size in both masters.

```toml
[chamfers]
exposed = 16
tight_junction = 8
```

R10. A tip or a terminal ends on a flat after its bevel; there is no acute
point. Where a bevel would leave an acute angle (the end of a diagonal),
the tip gets a short flat (16 units) before it turns into the stroke edge.
Seen in: less greater (cb7a5084), asciitilde (0faf5dbe), section (22ccd03a),
v w x y V W X (9a2e884d), alef-hb top terminal (Eli, 2026-11-15).

R11. No curve meets an edge in a point. Where a curved stroke joins a
straight edge, it lands on a short flat (8 units at a junction).
Seen in: alef-hb, the left leg on the diagonal (Eli, 2026-11-15).

R12. In a weight transfer, a cut can get larger, never smaller.
Seen in: Bold two three five six (c5042963).

R13. A tangent join is not a corner and gets no bevel. Keep the small
deliberate cuts and straight landings of the donors.

## Strokes and curves

R14. Apparent weight is monolinear. Measure across the stroke, on straight
strokes, diagonals and curves, and check the two opposing edges together: a
swelling or a pinch is a fault even when every check passes.

The stroke ranges that `make check-design` uses are set from the green glyphs
with `fgtools check-design --observe`. `vertical_stem` is the thickness of a
vertical stroke, measured horizontally. `horizontal_stroke` is the thickness
of a horizontal stroke, measured vertically. A measured span longer than
`stroke_limit` is not a stroke. A master and script without a table has no
green glyphs to set a range from yet (Bold Arabic, Bold Hebrew).

```toml
[targets.Regular.Latin]
vertical_stem = [92, 108]
horizontal_stroke = [78, 100]
stroke_limit = 180

[targets.Bold.Latin]
vertical_stem = [176, 208]
horizontal_stroke = [124, 170]
stroke_limit = 300
```

R15. Diagonals are straight, with parallel edges, through every join.

R16. Every crest, trough and side extreme of a curve has an on-curve point
with a horizontal or vertical tangent.
Seen in: asciitilde (56f4b437), section (22ccd03a), b d (dec6b4b3).

R17. A turn in a bowl or a shoulder keeps one direction of curvature; it
does not reverse.
Seen in: hamzaabove-ar Bold (ce3a7669).

R18. G2 is not the target. A join can keep a curvature change when the
shape needs it.
Seen in: hamzaabove-ar Bold (ce3a7669).

R19. A line that continues into a collinear handle is a smooth point. A
corner is a deliberate kink only.
Seen in: Eli's instruction (372bb48e).

R20. Handles within one segment have similar lengths, compensated pairs keep
the form, and the lengths follow the proportions of the glyph.

R21. Look at the whole filled shape before local curves: a smooth, even
stroke can still follow a poor path. Change one node at a time and check its
neighbors again.

## Bowls and rounds

R22. A lowercase Latin bowl (b d p q g) is the round half of the o, copied
point for point, joined to a stem. The advance follows the o; the counter is
about 0.95 of the o counter; the inner extreme passes the stem edge by about
4 units. b, p and q derive from an approved d by mirror or rotation.
Seen in: d (88b4aa2).

R23. Geometric does not mean rectangular: keep oval bowls and counters,
remove only organic irregularity.
Seen in: samekh v4, rejected (df38c4a2).

R24. Arabic letter dots are near-perfect circles: four symmetric cubic
quarters with equal radii. Hebrew marks are not copied into Arabic dots.

## Weight and Bold

R25. Transfer construction relationships, not scaled coordinates. A Bold
edge keeps the direction of the Regular edge it comes from.
Seen in: Bold seven nine (70c6a082).

R26. Open a Bold counter with width, not a thinner stem. Bold lowercase
stems stay 192.
Seen in: Bold n b d (9fb03696).

R44. More weights are drafted from two masters by `make draft-weights`, one
table for each weight. `wght` is the position on the weight axis, and
`between` names the two masters. `vertical_stem` and `horizontal_stroke`
give the stem and the bar of H in each master and the target of the weight.
The drafts go to `out/weights/`. They become masters of the designspace only
after Eli approves Regular and Bold.

```toml
[weights.Thin]
wght = 100
between = ["Regular", "Bold"]
vertical_stem = { Regular = 100, Bold = 192, target = 28 }
horizontal_stroke = { Regular = 88, Bold = 168, target = 26 }

[weights.Black]
wght = 900
between = ["Regular", "Bold"]
vertical_stem = { Regular = 100, Bold = 192, target = 256 }
horizontal_stroke = { Regular = 88, Bold = 168, target = 204 }
```

## Structure of the sources

R27. Both masters have the same contours, points, point types, point order
and components. A point added in one master is added in the other.

R28. No overlapping contours: union overlapping parts into one contour.
Seen in: dollar (7f8be952), one.tf (dbe60148).

R29. The start point of a contour is on the side where the writing starts:
the leftmost point for Latin, the rightmost for Arabic and Hebrew; the lowest
of two that tie.
Seen in: asciitilde (56f4b437), Eli's instruction (2026-11-10).

## Spacing

R30. Round forms fit tighter than flat-sided forms; symmetric letters have
balanced sidebearings. Spacing values use the 8-unit grid and recurring
intervals (32, 48, 64, 96). Judge spacing in words at 400, 550 and 700.

## Latin

R31. h and m take their stems, shoulder and arch from the current n.
Seen in: m h (cbb174ea).

## Hebrew

R32. Hebrew has the contrast of the Arabic, not of the Latin: horizontals
104 = 64 + 32 + 8 and verticals 88 = 64 + 16 + 8 in Regular, a ratio of 1.18,
and a curve goes evenly between them. Most Hebrew sans fonts have the Latin
direction (0.79 to 0.92); the designer chose the traditional one. A
diagonal that falls to the bottom right is thick (about 100: alef, tsadi);
a tail that falls to the bottom left is thin (88 to 96: qof, lamed).

```toml
[targets.Regular.Hebrew]
vertical_stem = [84, 92]
horizontal_stroke = [100, 108]
stroke_limit = 180
```

R33. The lamed ascender reaches 768, the height of Latin l. Final forms
descend to -192.

R34. When a Hebrew letter looks wrong, compare its skeleton with Rubik. If
the structure differs much, follow Rubik's structure drawn with Virtua's
chamfers, grid and forms. Simplify rather than add.
Seen in: zayin shin finaltsadi samekh (4e900dd0, df38c4a2), gimel (3814ca96).

R35. Hebrew vowel dots are 96 square with 24-unit bevels and the vowel bars
are 104 thick, as the letters' horizontals. Bold: dots 128, bars 136, bevels 32.

## Arabic

```toml
[targets.Regular.Arabic]
vertical_stem = [80, 112]
horizontal_stroke = [88, 112]
stroke_limit = 180
```

R36. Draw and correct the base letters before their marks.
Seen in: ARB-004 (211c3b8d).

R37. The two terminals of an isolated boat or cup have the same thickness.
Seen in: behDotless-ar (67f4d301).

R38. Check joining forms through shaping (three repetitions and an isolated
letter) at 400, 550 and 700, and measure both edges of a join against the
real neighbor forms.

## Glyph decisions

R39. Kaf (Arabic) is rounded with an old-style S shape; keep its openings
and rounded turns.

R40. The raised return of yeh-ar.fina is intentional.

R41. Seen keeps upright teeth, separate rounded lobes and small deliberate
junctions; do not flatten its underside into a wave.

R42. The at sign keeps the small italic a in the center and the continuous
double spiral.

R43. dollar uses the uppercase S as its body (7f8be952). section has bevelled
terminals (22ccd03a).

## Project settings

These tables are settings of the tools, not design rules.

### Mark colors

The mark color of a glyph is its review state. `rgba` lists every value that
the sources use for the color. The policy is what an agent can do with a
glyph that has the color.

```toml
[colors.green]
rgba = [[0, 1, 0, 1], [0.09, 0.72, 0.44, 1]]
policy = """Locked in as close to final. Eli approves contour glyphs. A composite is green when its \
parts are green and `fgtools check-design --ready` lists it."""

[colors.yellow]
rgba = [[1, 1, 0, 1], [1, 0.86, 0.2, 1], [0.91, 0.79, 0.27, 1]]
policy = "Close. Edit without replacing the drawing. Not a reference."

[colors.orange]
rgba = [[1, 0.5, 0, 1], [1, 0.6, 0.06, 1], [0.97, 0.58, 0, 1]]
policy = "Better, not good enough. Edit and keep useful construction. Replace only when Eli says so."

[colors.red]
rgba = [[1, 0, 0, 1], [1, 0.29, 0.24, 1], [1, 0.3, 0.3, 1]]
policy = "Broken. Can be replaced when Eli names the glyph. Not a reference."

[colors.purple]
rgba = [[0.54, 0.44, 0.88, 1], [0.5, 0, 1, 1]]
policy = "AI drawing that Eli has not reviewed. Not a reference."

[colors.blue]
rgba = [[0.27, 0.44, 1, 1]]
policy = "Composite that needs diagnosis. Not a reference."

[colors.pink]
rgba = []  # no glyph uses pink now
policy = "Composite that needs small edits. Not a reference."
```

`fgtools corrections` lists the reviews from this date. The earlier reviews
predate the grades.

```toml
[corrections]
start = "2026-11-13"
```

### Reference fonts

The fonts that the proofs and Runebender show beside this font. They are for
comparison of weight, spacing and structure. They are not a source of
outlines. Each key is a directory name of https://github.com/google/fonts
under `ofl/`, and each value is the reason that the family is a reference.
`make reference-fonts` copies the families into `reference-fonts/`, which Git
ignores.

```toml
[reference_fonts.families]
rubik = "The structural reference of the Hebrew. It also has Arabic and Latin."
notosanshebrew = "A Hebrew sans with full coverage of the marks."
heebo = "A Hebrew extension of Roboto: a plain sans for text."
ibmplexsanshebrew = "A Hebrew grotesque from a professional foundry."
assistant = "A Hebrew sans for text, drawn to work with Source Sans."
notosansarabic = "An Arabic sans with full coverage and even joining."
ibmplexsansarabic = "An Arabic grotesque from a professional foundry."
readexpro = "A geometric Arabic and Latin sans."
```

### Known QA debt

Known development debt, not release exceptions. `fgtools qa` leaves these
checks out, and `fgtools qa --full` runs them. Do not add a check to hide a
new failure.

```toml
[qa.exclude]
"googlefonts/repo/dirname_matches_nameid_1" = "Needs the google/fonts package directory."
"googlefonts/glyphsets/shape_languages" = "Needs language and shaping work."
"googlefonts/metadata/unreachable_subsetting" = "Needs subset work."
"fontgarden/grid" = "section, uniE000, germandbls and three Arabic advances are off the 2-unit grid; Eli corrects them."
```
