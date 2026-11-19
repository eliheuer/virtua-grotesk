# Virtua Grotesk

Virtua Grotesk is a typeface designed by Eli Heuer. It is a grid-based
neo-grotesk drawn on a dyadic self-labeling grid system: nested grids built
on powers of two. The grid records drawing intent and limits the number of
possible points. A small local AI model, the Runebender font editor, large
cloud models and this file are then used together to draw and work on the
typeface.

The font supports Latin, Arabic and Hebrew all as one cohesive design
developed together by one designer. It is free and open source under the
SIL Open Font License 1.1.

This file is the description of the design. It has three readers:

- A person reads it to understand the typeface: the idea, the construction
  and the decisions.
- An agent reads all of it whenever it works on the sources of the font.
  Runebender gives it to its agents.
- `fgtools` and Runebender read the values in the `toml` code blocks. A
  block holds the values of the rule above it, and the tools read all blocks
  as one TOML document.

This file is a specification: it states the design and the system that the
project is built towards. Where a tool or a glyph does not yet do what this
file says, the file is correct and the tool or the glyph is not finished.

A design value or a design rule is stated here and in no other file. Font
metrics are in the `fontinfo.plist` files and the weight axis is in the
designspace. They are not repeated here.

## Contents

`make test` fails when this list and the chapters differ.

- [The idea](#the-idea): Why the font is drawn on a grid, and what came
  before it.
- [How to use the rules](#how-to-use-the-rules): How an agent draws and
  reviews with the numbered rules.
- [Character](#character): The look of the typeface, and the role of the
  reference fonts and the donors.
- [Grid and metrics](#grid-and-metrics): The em, the vertical metrics and
  the 8-unit and 2-unit grids.
- [Corners, tips and joins](#corners-tips-and-joins): Chamfers, stroke ends
  and the places where strokes meet.
- [Strokes and curves](#strokes-and-curves): Stroke weights, handles and the
  construction of curves.
- [Bowls and rounds](#bowls-and-rounds): Round letters and the bowls that
  join a stem.
- [Weight and Bold](#weight-and-bold): How a shape changes from Regular to
  Bold, and the planned weights.
- [Structure of the sources](#structure-of-the-sources): Contours,
  components and compatibility of the masters.
- [Spacing](#spacing): Sidebearings and kerning.
- [Latin](#latin): Rules for Latin, with the accented letters.
- [Hebrew](#hebrew): Rules for Hebrew.
- [Arabic](#arabic): Rules for Arabic.
- [Glyph decisions](#glyph-decisions): Decisions about single glyphs.
- [Proofs and media](#proofs-and-media): The layout of every proof, specimen
  and picture of the font, on the powers of two of the typeface.
- [Project settings](#project-settings): Settings of the tools: mark colors,
  reference fonts and known QA debt.

## The idea

### A system, not a set of drawings

A typeface is many drawings that work as one system. To design the system
and not the single object is an old modernist aim. Karl Gerstner argued for
it in *Designing Programmes* (1964). In practice it had limits: strict rules
made type stiff, because a rule cannot make the optical corrections that the
eye needs.

Virtua Grotesk keeps the system and keeps the corrections. Its grid records
which point is a default of the system and which point is a correction by
the designer.

### The precedent: LL Replica

The nearest precedent is LL Replica by Norm (Dimitri Bruni and Manuel Krebs),
released by Lineto in 2008. Three of its decisions matter here.

- **A coarse grid.** FontLab gives 700 units to the cap height. Norm used
  70, a step of 10 units, and every point and handle had to be on a step.
  Norm did not accept that a finer grid gives more freedom: fewer options
  made each decision larger and the design more its own.
- **A visible grid.** The corners are cut one grid step wide, with the same
  bevel on inside and outside joints. The constraint made the look, and the
  look shows the constraint.
- **Cut diagonals.** The ends of diagonal strokes are cut, so A, K and R
  have no pointed apex and the letters can be set tight.

From a distance Replica looks like a familiar grotesque. The differences
show at large sizes. Virtua has the same two scales: at 16 pixels its
16-unit chamfer is a quarter of a pixel, and at display sizes it is the
character of the face.

### What Virtua changes

Virtua uses powers of two where Replica uses tens, and two grids where
Replica uses one.

- The em is 1024 units, which is 2 to the power 10.
- Structural points are on the 8-unit grid. This is the default.
- An optical correction by the designer is on the 2-unit grid. Every point
  is on this grid.
- Corners are cut with a 16-unit chamfer, and a tip ends on a flat, never
  on an acute point.

A second system labels measurements. Every measurement is a sum of powers
of two, and the number of terms describes it. A 64-unit stem is too light
and a 128-unit stem is too heavy, so the Regular stem is 96 = 64 + 32.
Where 96 is too light, the font uses 112 = 64 + 32 + 16. More terms often
mark an optical adjustment. They are not a fault.

Spacing follows the same rule. Sidebearings and kerning use the 8-unit grid
by default, which gives the text a small set of recurring intervals.

### Sources as data

Most fonts were not made as training data: their points are where the
designer put them, and each font has its own habits. In Virtua the two
systems turn the drawing conventions into data, without extra labels.

- **Consistency.** The same stroke logic, chamfer sizes and start points
  recur in the whole glyph set. A model or an agent learns one design.
- **Measurable output.** A script can check the grids and the stroke
  values. The checks do not decide quality, but they give a draft an
  objective first test.
- **Clean interpolation.** The Regular stem is 96 and the Bold stem is 192.
  The weight between them has a 144-unit stem, also on the grid.

For this reason AI agents draft glyphs from the approved drawings, and a
small language model, Virtua-12M, is trained on the sources. A draft is not
a finished glyph. Eli Heuer draws, corrects and approves every glyph.

### Scripts and weights

Latin, Arabic and Hebrew use the same grid, the same chamfer and the same
stroke logic. The upright variable font has weight masters at Thin (100), Regular (400),
Bold (700) and Black (900). Each weight has masters at 14 and 144 pt.
The 144 pt masters start with the drawing and spacing of the 14 pt masters.
An italic is planned.

### Sources

The main source of this chapter is the article
[Virtua Grotesk: Grid Systems for Dataset Engineering](https://elih.net/blog/virtua-grotesk).
The facts about Replica are from that article, from
[Fonts In Use](https://www.fontsinuse.com/typefaces/7436/ll-replica) and
from the Eye article
[Buying into the Norm cosmos](https://eyemagazine.com/feature/article/buying-into-the-norm-cosmos).

## How to use the rules

The rules have numbers (R1, R2 and so on). A number never changes, so the
numbers are not in order in every chapter.

- Before you draw or change a glyph, read every rule, not only the chapter
  of its script.
- When you review a glyph, check it against every rule that applies, by
  number: "R12: passes" or "R12: fails at (64,624), the tip has no flat".
  Then look at the whole glyph for faults that no rule names.
- When Eli corrects a glyph and the reason is a principle, add a rule with
  "Seen in" and the commit, or add the commit to the rule that covers it.

## Character

R1. Virtua is a neo-grotesque with a machined finish. For Latin, use
Helvetica and Neue Haas Grotesk as guides to the silhouette, proportions
and distribution of black and white. LL Replica is a reference for how
the grid can show in the outline. At reading size the letter should feel
like a familiar neo-grotesque. At display size its flats, chamfers and
deliberate cubic curves should look precise enough to have been cut by a
CNC machine.

Keep the optical corrections that make the strokes look even and the
counters stay open. A bowl can be fuller on one side, and a stroke can
thin as it enters a join. Follow the approved donor for those decisions.
When refining a curve, preserve the flats it lands on. Avoid adding a
pen-like flare for smoothness or forcing a bowl into a perfect circle
for symmetry.

R2. The reference fonts do not dictate the design. Compare visual weight,
spacing, outline consistency and the structure readers expect. A small
difference of form is not a fault; a glyph very different from all of them
needs a reason. Rubik is the target for weight, spacing and outline quality.

R3. Draw from green Virtua glyphs of the same construction (the donors): read
their points and their filled shape. A glyph that is not green is not a
donor.

R45. The core donors are O, H, n and o, with green forms of the same script.
Before you use a donor, check its mark color in both masters and the
components it depends on. A sketch or image from Eli gives the intended shape:
calibrate its scale before you measure from it. A rejected candidate is a
counterexample.

R4. A local correction of one glyph (Zayin, Gimel, Final Tsadi, hamza) is an
example for that glyph and master, not a formula for others.

## Grid and metrics

R5. The em is 1024. Ascender and cap height 768, x-height 576, descender
-256. The Hebrew letter height is 640 = 512 + 128, which is 1.11 of the
x-height and 0.83 of the cap height: Hebrew has almost no ascenders and no
capitals, so at the x-height it looks smaller than the Latin beside it.

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

R46. The grid describes positions. The binary decomposition of a measurement
(32, 48 = 32 + 16, 96 = 64 + 32) describes it, and many terms are not a fault:
do not round a measurement, or give up the construction of a curve, to get a
tidier number. Interpolated positions and the quadratic curves of the compiled
font need not be on the grid. Never use them as a reason to snap a source.

## Corners, tips and joins

R9. Every corner where two straight segments meet has a 45 degree bevel of
16 units per side in Regular. Tight junctions use 8. The bevel is a straight
segment, never a curve, and keeps its absolute size in both masters, so it is relatively smaller in the
Bold. It applies where a stem meets the baseline or the cap height, at the
ends of crossbars, at apexes and at open terminals.

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

R47. Before you fit handles, name each connection: tangent continuation,
straight landing, deliberate cut, shelf or intended inflection. Choose where
the straight runs end and how far each turn extends.

## Strokes and curves

R14. Apparent weight is monolinear. Measure across the stroke, on straight
strokes, diagonals and curves, and check the two opposing edges together: a
swelling or a pinch is a fault even when every check passes.

Use the **thickness heatmap** (RuneBender → Curves → Thickness) to review strokes
in every script, including numerals, marks and punctuation. Establish the
intended weight at each end of a turn from the glyph’s construction.
Follow the transition on the heatmap. Its colors are relative to the
glyph’s own median. Use design units when comparing different glyphs.

Where a simple stroke appears to swell or pinch, measure from one edge
to the opposite edge along the normal at the quarter, half and
three-quarter points of the curve. Bisect again around an abrupt change.
Adjust the opposing handles together, preserve deliberate flats and
tangents, and repeat the measurements after grid rounding. At a branch,
the heatmap includes the ink where strokes meet. Inspect the incoming
strokes separately and judge the filled join in context at reading size.

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

R48. Check a curve in this order: the whole filled shape, the signed curvature
of each turn (the curvature comb of Runebender, at the same scale before and
after), the joins, the two opposing edges together, and then all of it again
after rounding. Rounding two edges separately can change the stroke weight
even when every point is on the grid. Then check both masters, the
intermediate weights and the glyph in words.

R49. Harmonize, Balance, Optimize and Simplify in Runebender change handles by
a formula and can remove intended unequal handles. Use them on a copy, then
check the neighbors and the grid again. `fgtools lint-curves <Master> <glyph>
--joins` reports off-center crests, tension breaks, inflections and the
continuity of every join. A report is a reason to look at the filled glyph,
and an S spine has an inflection by design.

## Bowls and rounds

R22. A lowercase Latin bowl (b d p q g) is the round half of the o, copied
point for point, joined to a stem. The advance follows the o; the counter is
about 0.95 of the o counter; the inner extreme passes the stem edge by about
4 units. b, p and q derive from an approved d by mirror or rotation.
Seen in: d (88b4aa2).

R50. The round side of a bowl letter keeps the sidebearing of the o, and the
stem side gets 64 in Regular. Draw the junction of bowl and stem: its handles
move in x and y for an even tangent. The top and the bottom of a bowl can
differ by a few units. A mirror reverses the contour direction, so reverse
each contour after a mirror. After a vertical mirror, put the bottom of the
descender terminal on the descender line. Do not shift or scale an older bowl
until its counter matches, and do not flatten its wall to one thickness.
Seen in: d (88b4aa2).

R51. The single-storey g is not a mirror of the d. Its bowl is shorter and
higher than the o, to make space for the ear and the tail, and its outer round
side is slightly flatter. The top left is fuller than the bottom left, where
the bowl meets the tail. The ear, the spine and the tail are drawn by eye. The
tail depth is -216.
Seen in: g, Eli's correction of an agent draft.

R23. Geometric does not mean rectangular: keep oval bowls and counters,
remove only organic irregularity.
Seen in: samekh v4, rejected (df38c4a2).

R24. Arabic letter dots are near-perfect circles: four symmetric cubic
quarters with equal radii. Hebrew marks are not copied into Arabic dots. A dot
has no corner to bevel. Measure the radial deviation, not only the bounding
box. This rule is for letter dots, not for every Arabic vowel mark.

## Weight and Bold

R25. Transfer construction relationships, not scaled coordinates. A Bold
edge keeps the direction of the Regular edge it comes from.
Seen in: Bold seven nine (70c6a082).

R26. Open a Bold counter with width, not a thinner stem. Bold lowercase
stems stay 192.
Seen in: Bold n b d (9fb03696).

R52. Before a weight transfer, decide which edges, alignments and counters of
the glyph are fixed. Counter reduction is the Latin pattern; do not assume
that the outer contour of every Arabic or Hebrew letter is fixed. No single
handle ratio serves every transfer.
Seen in: Bold zayin-hb, Bold hamzaabove-ar (ce3a7669).

R44. Thin and Black use Regular and Bold as donors. Each table records
the weight coordinate, the two donors and the target vertical stem and
horizontal bar of H. The target for Thin follows the supplied light
reference. Black is heavier than the supplied dark reference.

```toml
[weights.Thin]
wght = 100
between = ["Regular", "Bold"]
vertical_stem = { Regular = 100, Bold = 192, target = 62 }
horizontal_stroke = { Regular = 88, Bold = 168, target = 52 }

[weights.Black]
wght = 900
between = ["Regular", "Bold"]
vertical_stem = { Regular = 100, Bold = 192, target = 256 }
horizontal_stroke = { Regular = 88, Bold = 168, target = 204 }
```

## Structure of the sources

R27. All masters have the same contours, points, point types, point order
and components. A point added in one master is added in the other. Do not
reorder points or contours: the order controls interpolation.

R28. No overlapping contours: union overlapping parts into one contour.
Seen in: dollar (7f8be952), one.tf (dbe60148).

R29. The start point of a contour is on the side where the writing starts:
the leftmost point for Latin, the rightmost for Arabic and Hebrew; the lowest
of two that tie.
Seen in: asciitilde (56f4b437), Eli's instruction (2026-11-10).

R53. The lowercase a keeps the same contour structure across the weight
axis. Its foot turns outward in Regular and draws back toward the stem in
Bold. The two edges of the waist land on horizontal shelves before
the 8-unit cuts into the stem. The foot lands flat on the baseline before its
outer bevel. Compare the Regular outline at 14 pt to the green drawing in
9e009aad when changing the weight transition. Check the shelves and foot in
the exported font at the master weights and between them.
Seen in: the continuous a redraw (3c25f669).

Each triple gives the left end, right end and height of a Regular landing.

```toml
[a_geometry]
regular_upper_waist = [328, 424, 352]
regular_lower_waist = [360, 424, 280]
regular_foot = [512, 560, 0]
```

Accented forms use the same base. A glyph that needs a change in
contour structure can use an unencoded alternate and a designspace rule.

R54. All masters have the same kerning groups, and a glyph is in at most one
group of each side. A pair that is added to one master is added to the other;
its value can be 0. Kerning values are multiples of 8.

## Spacing

R30. Round forms fit tighter than flat-sided forms; symmetric letters have
balanced sidebearings. Spacing values use the 8-unit grid and recurring
intervals (32, 48, 64, 96). Judge spacing in words at 400, 550 and 700. Measure the
real ink sidebearings, with the components, and keep approved widths that
are off the 8-unit grid.

## Latin

R31. h and m take their stems, shoulder and arch from the current n.
Seen in: m h (cbb174ea).

### Accented letters

R57. A mark has one height over all letters of one height. Over an ascender
(h, k, l, b, d) and over a capital letter, the mark is above the letter: a
mark at the x-height that cuts into an ascender is a fault. The i and the j
have no dot under a top mark.

R58. A symmetric mark (dieresis, macron, circumflex, caron, breve, ring,
tilde, dot) is on the optical center of the letter. On a symmetric letter
that is the center of its width. An acute or a grave points at the center
with its lower end, so its bounding box is to the right (acute) or to the
left (grave) of the center. On a letter that is not symmetric (L, h, k, r, t,
f, J), the mark is over the stem or over the width: this is a decision of
the design, and all letters of the font follow one decision.

R59. A cedilla joins the bottom of the bowl of C and S at its center. An
ogonek joins the letter at the bottom right (A, a, E, e, U, u) or at the stem
(I, i), without a gap. A comma accent is under the center with a clear gap.
The caron of d, t, l and L is an apostrophe form at the right of the letter.
The comma accent of g is a turned comma over the letter.

R60. A mark does not touch a part of the letter that it is not designed to
join, and the letter does not cut it. The masters have the same components
and the same relative position of the mark.

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

R55. Check the attachment of a mark to a letter, and of a mark to a mark, in
the compiled font at several weights. Coverage does not show that the marks
are drawn or attached well.

## Arabic

```toml
[targets.Regular.Arabic]
vertical_stem = [80, 112]
horizontal_stroke = [88, 112]
stroke_limit = 180
```

R36. Draw and correct the base letters before their marks.
Seen in: ARB-004 (211c3b8d).

In Arabic the horizontal is usually a little heavier than the upright.
Use R14 to check the transition through the turn.

R37. The two terminals of an isolated boat or cup have the same thickness.
Seen in: behDotless-ar (67f4d301).

R38. Check joining forms through shaping (three repetitions and an isolated
letter) at 400, 550 and 700, and measure both edges of a join against the
real neighbor forms. A right-joining letter needs only the forms that its
joining has. The anchors of letter dots and the anchors of vowel marks have
separate roles.

## Glyph decisions

R39. Kaf (Arabic) is rounded with an old-style S shape; keep its openings
and rounded turns. The angular Kaf of some reference fonts does not override
this. The Regular initial Kaf is green and Eli approved the Bold initial Kaf;
that approval is for those two forms only.

R40. The raised return of yeh-ar.fina is intentional, in both masters. Do
not replace it with the descending form of the reference fonts. The decision
is for yeh-ar.fina only.

R41. Seen keeps upright teeth, separate rounded lobes and small deliberate
junctions; do not flatten its underside into a wave, and do not replace the bowl
junction with a diagonal sweep. This is for seen-ar and its forms, sheen-ar
and seenSixdots-ar. Start from the green Regular seen-ar.init and
seen-ar.medi. Eli rejected version 4 of the isolated Seen as a regression of
style, although it passed the checks.

R42. The at sign keeps the small italic a in the center and the continuous
double spiral. Eli rejected revisions with a lumpy stroke weight although
their local measurements were better: look at the whole filled spiral.

R43. dollar uses the uppercase S as its body (7f8be952). section has bevelled
terminals (22ccd03a).

R56. A symbol that is made of lines is constructed from green symbols. An
organic symbol is traced from an image with img2bez. The image gives the form,
and green Virtua glyphs give the construction, the scale and the weight.

## Proofs and media

R61. Every proof, specimen, technical image, marketing picture and video of
the font is laid out on the same powers of two as the typeface. The layout is
a part of the design: a picture of Virtua shows the grid of Virtua. This rule
has no exception for a format, a canvas or a platform.

R62. The module of a layout is 64 pixels, the 64-unit step of the design
grid, and the base unit is 8 pixels. Every position and every length of a
layout is a multiple of 8 pixels. A canvas has a live area of a whole number
of modules, and the margin is what remains. A glyph that is drawn at an em of
1024 pixels has 1 pixel for 1 font unit, so the grid lines of the picture are
the grid lines of the drawing. In print the module is 32 points and the base
unit is 4 points.

R63. Type sizes double: 32, 64, 128, 256, 512 and 1024 pixels, with 24 for
labels. The cap height is three quarters of the em and the x-height is nine
sixteenths, so only these sizes put the cap height and the x-height on whole
pixels and on the module lines. A size outside this list is a fault. A
picture has at most three sizes and two weights. A picture whose subject is
the weight axis can show more weights.

R64. The top of the capitals stands on a module line, and the start of a
text stands on a column line: the left edge for Latin, the right edge for
Arabic and Hebrew. Text is flush at its start and ragged at its end. It is
not centered and not justified. Leading is a multiple of 16 pixels. A large
line has its ink, not its origin, on the column line.

R65. Motion uses the same numbers: 30 frames in a second, loops of 128 or
256 frames, and durations that are multiples of 8 frames. An element that
moves, moves a whole number of units in each frame. One value moves in a
picture, and a line with a mark shows it.

R66. A text is chosen to fit its measure. The size never changes to make a
text fit. A large word fills its measure from the first column line to the
last, and a word that does not fill it is replaced by another word.

R67. A picture has one label size, one line weight, two inks and one accent.
Each setting has a label that states its size and its weight. The tools
check R62 to R64, and a layout with a fault is not written.

```toml
[layout]
unit = 8                                  # pixels: every position is a multiple
module = 64                               # pixels, and font units of the design grid
sizes = [32, 64, 128, 256, 512, 1024]     # type sizes in pixels
label_size = 24
print_unit = 4                            # points
print_module = 32                         # points
frames_per_second = 30
frame_unit = 8                            # frames: every duration is a multiple
loops = [128, 256]                        # frames
```

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
inter = "A neutral Latin sans for text and interfaces, with weights 100 to 900 and an italic."
bricolagegrotesque = "A Latin grotesque with weight, width and optical size axes."
geist = "A geometric Latin sans for interfaces, with weights 100 to 900 and an italic."
```

### Known QA debt

Known faults of the fonts, not release exceptions. `make test` leaves these
checks out, so that a FAIL there is a new fault. The fonts are ready for
release when this list is empty. Do not add a check to hide a new fault.

```toml
[qa.exclude]
"googlefonts/repo/dirname_matches_nameid_1" = "Needs the google/fonts package directory."
"googlefonts/glyphsets/shape_languages" = "Needs language and shaping work."
"googlefonts/metadata/unreachable_subsetting" = "Needs subset work."
"fontgarden/grid" = "uniE000 has off-grid points in both masters."
```
