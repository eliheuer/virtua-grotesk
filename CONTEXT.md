# Virtua Grotesk

The design of the typeface, as rules and values. Agents read all of it before
they change a glyph. `fgtools` and Runebender read the `toml` blocks as one
TOML document. A design rule or a design value is in this file and in no
other file. Where a tool or a glyph differs from this file, this file is
correct. `README.md` has the idea of the design and its history.

## Contents

`make test` fails when this list and the chapters differ.

- [How to use the rules](#how-to-use-the-rules): How an agent draws and reviews with the numbered rules.
- [Character](#character): The look of the typeface, the reference fonts and the donors.
- [Grid and metrics](#grid-and-metrics): The em, the vertical metrics and the two grids.
- [Corners, tips and joins](#corners-tips-and-joins): Chamfers, stroke ends and the places where strokes meet.
- [Strokes and curves](#strokes-and-curves): Stroke weights, handles and the construction of curves.
- [Bowls and rounds](#bowls-and-rounds): Round letters and the bowls that join a stem.
- [Weight and Bold](#weight-and-bold): The weights, the optical size and the grade.
- [Structure of the sources](#structure-of-the-sources): Contours, components and compatibility of the masters.
- [Spacing](#spacing): Sidebearings and kerning.
- [Latin](#latin): Rules for Latin, with the accented letters.
- [Hebrew](#hebrew): Rules for Hebrew.
- [Arabic](#arabic): Rules for Arabic.
- [Glyph decisions](#glyph-decisions): Decisions about single glyphs.
- [Proofs and media](#proofs-and-media): The layout of every proof, specimen and picture.
- [Project settings](#project-settings): Mark colors, reference fonts and known QA debt.

## How to use the rules

- A rule number never changes, so the numbers are not in order.
- Read every rule before you draw, not only the chapter of the script.
- Review a glyph against each rule by number: "R12: passes" or "R12: fails at (64,624)". Then look at the whole glyph.
- When Eli corrects a glyph for a reason of principle, add a rule with "Seen" and the commit, or add the commit to the rule that covers it.

## Character

- R1. A neo-grotesque with a machined finish. Silhouette and proportions: Helvetica and Neue Haas Grotesk. The grid in the outline: LL Replica. At reading size it is a familiar neo-grotesque. At display size the flats, chamfers and curves look cut by a CNC machine. Keep the optical corrections of the donors: a bowl can be fuller on one side, a stroke can thin into a join. Keep the flats that a curve lands on. No pen-like flare, no perfect circle for symmetry.
- R2. The reference fonts do not dictate the design. Compare weight, spacing, outline consistency and expected structure. Rubik is the target for weight, spacing and outline quality.
- R3. Draw from green Virtua glyphs of the same construction (the donors): read their points and their filled shape. Where no green glyph has the construction, a yellow glyph is a donor. A glyph of another color is not a donor.
- R45. The core donors are O, H, n and o, with green or yellow forms of the same script. Check the mark color of a donor in every master. A sketch from Eli gives the shape: calibrate its scale first. A rejected candidate is a counterexample.
- R4. A local correction of one glyph (Zayin, Gimel, Final Tsadi, hamza) is for that glyph and master only.

## Grid and metrics

- R5. Em 1024. Ascender and cap height 768, x-height 576, descender -256. Hebrew letter height 640.
- R6. Every point is on the 2-unit grid. New structural points, handles, advances, sidebearings and kerning use the 8-unit grid. A point on 2 and off 8 is a correction by Eli: keep it, never snap it.

```toml
[grid]
source = 2         # every point is on the 2-unit grid
machine_draft = 8  # new drafts use the 8-unit grid
```

- R7. An intersection or a cut end point snaps to the 8-unit grid within 3 units of it, else to the 2-unit grid. Seen: v w x y V W X (9a2e884d).
- R8. Stroke weights are optical values and can be off the 8-unit grid. Do not round Eli's stroke values. Seen: o side 98 and crown 84 (324e6a15), cap stems 100 (cbb174ea).
- R46. Do not round a measurement, or give up the construction of a curve, for a tidier number. Interpolated positions and the compiled curves need not be on the grid.

## Corners, tips and joins

- R9. A corner of two straight segments has a 45 degree bevel of 16 units per side. Tight junctions use 8. The bevel is a straight segment and keeps its absolute size in every master.

```toml
[chamfers]
exposed = 16
tight_junction = 8
```

- R10. A tip ends on a flat after its bevel, never on an acute point. The end of a diagonal gets a 16-unit flat. Seen: less greater (cb7a5084), asciitilde (0faf5dbe), section (22ccd03a), v w x y V W X (9a2e884d), alef-hb (2026-11-15).
- R11. No curve meets an edge in a point. A curved stroke lands on a short flat, 8 units at a junction. Seen: alef-hb (2026-11-15).
- R12. In a weight transfer a cut can get larger, never smaller. Seen: Bold two three five six (c5042963).
- R13. A tangent join is not a corner and gets no bevel. Keep the small cuts and straight landings of the donors.
- R47. Before you fit handles, name each connection: tangent continuation, straight landing, deliberate cut, shelf or intended inflection.

## Strokes and curves

- R14. Apparent weight is monolinear. Measure across the stroke and check the two opposing edges together. A swelling or a pinch is a fault even when every check passes. Use the thickness heatmap of Runebender (Curves, Thickness); its colors are relative to the median of the glyph. Measure a suspect turn at the quarter, half and three-quarter points, adjust the opposing handles together, and measure again after rounding. `make check-design` uses these ranges, set from the green and yellow glyphs with `fgtools check-design --observe`:

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

- R15. Diagonals are straight, with parallel edges, through every join.
- R16. Every crest, trough and side extreme of a curve has an on-curve point with a horizontal or vertical tangent. Seen: asciitilde (56f4b437), section (22ccd03a), b d (dec6b4b3).
- R17. A turn in a bowl or a shoulder keeps one direction of curvature. Seen: hamzaabove-ar Bold (ce3a7669).
- R18. G2 is not the target. A join can keep a curvature change when the shape needs it. Seen: hamzaabove-ar Bold (ce3a7669).
- R19. A line that continues into a collinear handle is a smooth point. A corner is a deliberate kink only. Seen: 372bb48e.
- R20. Handles within one segment have similar lengths, and the lengths follow the proportions of the glyph.
- R21. Look at the whole filled shape before local curves. Change one node at a time and check its neighbors again.
- R48. Check a curve in this order: the filled shape, the curvature of each turn, the joins, the two opposing edges, then all of it again after rounding. Then every master, the intermediate weights and the glyph in words.
- R49. Harmonize, Balance, Optimize and Simplify in Runebender can remove intended unequal handles. Use them on a copy. `fgtools lint-curves <Master> <glyph> --joins` reports are a reason to look, not a verdict.

## Bowls and rounds

- R22. A lowercase Latin bowl (b d p q g) is the round half of the o, copied point for point, joined to a stem. The counter is about 0.95 of the o counter. b, p and q derive from an approved d. Seen: d (88b4aa2).
- R50. The round side of a bowl letter keeps the sidebearing of the o, and the stem side gets 64 in Regular. Draw the junction of bowl and stem. Reverse each contour after a mirror. Do not scale an older bowl, and do not flatten its wall. Seen: d (88b4aa2).
- R51. The single-storey g is not a mirror of the d. Its bowl is shorter and higher than the o, and the top left is fuller than the bottom left. The ear, the spine and the tail are drawn by eye. Tail depth -216.
- R23. Geometric does not mean rectangular: keep oval bowls and counters. Seen: samekh v4, rejected (df38c4a2).
- R24. Arabic letter dots are near-perfect circles: four symmetric cubic quarters. A dot has no bevel. This is for letter dots, not for every vowel mark.

## Weight and Bold

- R25. Transfer construction relationships, not scaled coordinates. A Bold edge keeps the direction of the Regular edge. Seen: Bold seven nine (70c6a082).
- R26. Open a Bold counter with width, not a thinner stem. Bold lowercase stems stay 192. Seen: Bold n b d (9fb03696).
- R52. Before a weight transfer, decide which edges, alignments and counters are fixed. Do not assume the Latin pattern for Arabic or Hebrew. Seen: Bold zayin-hb, Bold hamzaabove-ar (ce3a7669).
- R44. Masters: Thin 100, Regular 400, Bold 700, Black 900, each at 14 and 144 pt. Thin and Black use Regular and Bold as donors:

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

- R68. A 144 pt master starts as a calculation from the 14 pt master of the same weight. Each side of a glyph loses `side` units. A free side gets a smaller sidebearing. A joining side of an Arabic letter gets a shorter join. A free side inside an Arabic word, as in رب, changes as in Latin. A mark without an advance does not change. The change is complete at `complete` pt. A correction by Eli in a 144 pt master stays.

```toml
[optical_size]
from = 14       # pt: the masters that are drawn
to = 144        # pt: the masters that are calculated
side = 24       # units that each side of a glyph loses
complete = 72   # pt: the size at which the change is complete
```

- R69. The grade changes the weight and keeps every advance, in the units of the weight axis. A grade master has the outlines of `wght + grade` on the advances of `wght`. Past Thin and Black the grade has no effect. At 300 the letters of Regular collide.

```toml
[grade]
minimum = -200
maximum = 200
```

## Structure of the sources

- R27. All masters have the same contours, points, point types, point order and components. Do not reorder points or contours.
- R28. No overlapping contours. Seen: dollar (7f8be952), one.tf (dbe60148).
- R29. A contour starts on the side where the writing starts: leftmost for Latin, rightmost for Arabic and Hebrew, the lowest of two that tie. Seen: asciitilde (56f4b437).
- R53. The lowercase a keeps one contour structure across the weights. The two edges of the waist land on horizontal shelves before the 8-unit cuts into the stem, and the foot lands flat on the baseline. Compare with the drawing in 9e009aad. Seen: 3c25f669. Each triple is the left end, right end and height of a Regular landing:

```toml
[a_geometry]
regular_upper_waist = [328, 424, 352]
regular_lower_waist = [360, 424, 280]
regular_foot = [512, 560, 0]
```

- R54. All masters have the same kerning groups and pairs. Kerning values are multiples of 8.

## Spacing

- R30. Round forms fit tighter than flat-sided forms, and symmetric letters have balanced sidebearings. Values use the 8-unit grid and recurring intervals (32, 48, 64, 96). Judge spacing in words at 400, 550 and 700. Keep approved widths that are off the grid.

## Latin

- R31. h and m take their stems, shoulder and arch from the current n. Seen: m h (cbb174ea).
- R57. A mark has one height over all letters of one height. Over an ascender or a capital, the mark is above the letter. The i and the j have no dot under a top mark.
- R58. A symmetric mark is on the optical center of the letter. An acute or a grave points at the center with its lower end. On a letter that is not symmetric, all letters follow one decision.
- R59. A cedilla joins C and S at the center of the bowl. An ogonek joins at the bottom right, or at the stem of I and i. A comma accent is under the center with a gap. The caron of d, t, l and L is an apostrophe form.
- R60. A mark does not touch a part that it is not designed to join. The masters have the same components and relative mark positions.

## Hebrew

- R32. Hebrew has the contrast of the Arabic: horizontals 104 and verticals 88 in Regular. A diagonal that falls to the bottom right is thick (about 100), and a tail to the bottom left is thin (88 to 96).

```toml
[targets.Regular.Hebrew]
vertical_stem = [84, 92]
horizontal_stroke = [100, 108]
stroke_limit = 180
```

- R33. The lamed ascender reaches 768. Final forms descend to -192.
- R34. When a Hebrew letter looks wrong, compare its skeleton with Rubik, and follow that structure with Virtua's chamfers and grid. Simplify, do not add. Seen: zayin shin finaltsadi samekh (4e900dd0, df38c4a2), gimel (3814ca96).
- R35. Vowel dots are 96 square with 24-unit bevels, and vowel bars are 104 thick. Bold: dots 128, bars 136, bevels 32.
- R55. Check mark attachment in the compiled font at several weights.

## Arabic

```toml
[targets.Regular.Arabic]
vertical_stem = [80, 112]
horizontal_stroke = [88, 112]
stroke_limit = 180
```

- R36. Draw and correct the base letters before their marks. The horizontal is usually a little heavier than the upright. Seen: 211c3b8d.
- R37. The two terminals of an isolated boat or cup have the same thickness. Seen: behDotless-ar (67f4d301).
- R38. Check joining forms through shaping, at 400, 550 and 700, and measure both edges of a join against the real neighbors. For a ligature, take stacking and proportions from the reference and stroke weight and curves from Virtua. For في: keep the middle shelf visible, reuse the counter and crown of initial feh at their scale, and check في, فِي, فيه and لفي in every weight, with and without marks.

## Glyph decisions

- R39. Arabic kaf is rounded with an old-style S shape. Keep its openings and rounded turns.
- R40. The raised return of yeh-ar.fina is intentional in every master.
- R41. Seen keeps upright teeth, separate rounded lobes and small junctions. Start from seen-ar.init and seen-ar.medi. Eli rejected version 4 although it passed the checks.
- R42. The at sign keeps the small italic a and the continuous double spiral. Look at the whole filled spiral, not at local measurements.
- R43. dollar uses the uppercase S as its body (7f8be952). section has bevelled terminals (22ccd03a).
- R56. A symbol made of lines is constructed from green symbols. An organic symbol is traced from an image with img2bez, with Virtua's construction, scale and weight.

## Proofs and media

- R61. Every proof, specimen, picture and video is laid out on the powers of two of the typeface. No format has an exception.
- R62. The module is 64 pixels and the base unit is 8 pixels. Every position and length is a multiple of 8. In print the module is 32 points and the unit is 4 points.
- R63. Type sizes double: 32, 64, 128, 256, 512 and 1024 pixels, with 24 for labels. A picture has at most three sizes and two weights.
- R64. The top of the capitals stands on a module line, and the start of a text on a column line: left for Latin, right for Arabic and Hebrew. Text is flush at its start and ragged at its end. Leading is a multiple of 16 pixels.
- R65. Motion: 30 frames in a second, loops of 128 or 256 frames, durations in multiples of 8 frames. One value moves in a picture.
- R66. A text is chosen to fit its measure. The size never changes to make a text fit.
- R67. A picture has one label size, one line weight, two inks and one accent. Each setting has a label with its size and weight.

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

Settings of the tools, not design rules. The mark color of a glyph is its
review state, and the policy says what an agent can do with the glyph.

```toml
[colors.green]
rgba = [[0, 1, 0, 1], [0.09, 0.72, 0.44, 1]]
policy = """Locked in as close to final. Eli approves contour glyphs. A composite is green when its \
parts are green and `fgtools check-design --ready` lists it."""

[colors.yellow]
rgba = [[1, 1, 0, 1], [1, 0.86, 0.2, 1], [0.91, 0.79, 0.27, 1]]
policy = "Close to green. Small edits only, without replacing the drawing. A reference where no green glyph has the construction."

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

`fgtools corrections` lists the reviews from this date:

```toml
[corrections]
start = "2026-11-13"
```

`make reference-fonts` copies these families of https://github.com/google/fonts into `reference-fonts/`:

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

`make test` leaves these known faults out. The fonts are ready when the list is empty. Do not add a check to hide a new fault.

```toml
[qa.exclude]
"googlefonts/repo/dirname_matches_nameid_1" = "Needs the google/fonts package directory."
"googlefonts/glyphsets/shape_languages" = "Needs language and shaping work."
"googlefonts/metadata/unreachable_subsetting" = "Needs subset work."
"fontgarden/grid" = "uniE000 has off-grid points in both masters."
```
