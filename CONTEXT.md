# Virtua Grotesk

- Read this file before working on Virtua Grotesk.
- Use it to guide drawing and review.
- The TOML blocks contain the design settings.

## Design Intent

Link: https://elih.net/blog/virtua-grotesk/

- Virtua Grotesk is a typeface drawn on a dyadic self-labeling grid system
- A Dyadic self-labeling grid system is nested grids built on powers of two.
- Point placement defaults to an 8-unit grid, with small optical corrections dropping to a 2-unit subgrid.
- The grids record most of the drawing intent automatically, so the source files are labeled training data.
- This system makes the project a machine-learning and data-engineering project as much as a design project.

- Designing the system instead of the final object is an old modernist impulse.
- Karl Gerstner argued for it in his 1964 book Designing Programmes, a foundational text of systematic Swiss design.
- In practice, the idea ran into limits. Computers were procedural, and strict rules made type stiff.
- Neural networks might change that.
- A neural network is not a procedural program; it interpolates and tolerates nuance where a rule is brittle.
- It also answers a modernist ideal that the rigid version betrayed: technology people can live in harmony with, not technology that extinguishes human dignity. The old impulse is worth another look.

- Most fonts were never built for AI workflows. Their coordinates land wherever the designer put them. Their contours are as individual as handwriting. That is fine for a rasterizer, but it is a problem for data engineers working with font sources. Many font AI/ML projects train on exactly this accidental data: scraped fonts and Google Fonts, heterogeneous in every dimension that matters.

A typeface is not a collection of characters drawn in isolation. It is many drawings that work as one system. Font datasets need the same discipline. A collection assembled without it is not training data capable of delivering useful models in 2026.

Modernist design was born a little more than a century ago out of similar frustrations in a similar time of technological change. I think the way forward is not a return to the dogma and rigidity of modernist design (the culture of design that replaced modernism is equally if not more dogmatic and rigid, just in different ways), but a rediscovery, with fresh eyes and new technology, of the loftier goals of early modernism that were unachievable with the technology of the previous century.

The clearest precedent for Virtua Grotesk is LL Replica (Norm: Dimitri Bruni and Manuel Krebs; Lineto, 2008). Norm took the drawing grid in their font editor and made it ten times coarser. FontLab’s standard cap height is 700 units. Instead of 700 positions across it they had 70, a step of 10 units, and every node and Bézier control point had to land on one.

Two details make Replica more than a constraint exercise. First, the bevels: its corners are cut exactly one grid unit wide, so the grid is visible in the letterforms. Second, the cut diagonals: A, K, and R have no pointed apexes, so the letters can be set tight. The constraint produced the aesthetic, and the aesthetic advertises the constraint.

Virtua Grotesk uses two related hierarchies. The grid hierarchy classifies point positions. The measurement hierarchy labels distances between points by popcount. Both use powers of two, but they record different parts of the drawing.

The coordinate space of a font is called the em, and its size is given in units per em (UPM). Virtua Grotesk uses 1024 UPM, or 2¹⁰, rather than the industry’s usual 1000. This is less exotic than it sounds. TrueType commonly uses a power-of-two em: 2048 is standard, and Inter uses it.

The first hierarchy is positional. Every point must land on the 2-unit grid. The 8-unit grid is the default for structural points. A point on the 2-unit grid but off the 8-unit grid records a fine optical correction. Large corrections can still land on the 8-unit grid, so grid membership records most, but not all, drawing intent.

The second hierarchy describes measurements. Every integer has a unique binary decomposition: a sum of powers of two, each used once. The number of powers is its Hamming weight, or popcount. Virtua Grotesk uses popcount to label handle lengths and structural spans. A popcount of one is a pure power, such as 64, 128, or 256. Two is a short sum, such as 96 = 64 + 32. Three combines another increment, as in 104 = 64 + 32 + 8. Four or more uses a longer decomposition. The count is descriptive. A higher popcount often marks an optical adjustment or another fine detail. The value provides this label without additional annotation.

Popcount adds information that grid membership cannot. Both 96 and 112 are multiples of 8, but their decompositions record different design decisions. A 64-unit stem is too light and a 128-unit stem too heavy, so the Regular stem is 96 = 64 + 32. Where 96 is too light, the font uses 112 = 64 + 32 + 16. The additional term records a finer adjustment. Both measurements are valid.

## Drawing References

- Use Helvetica and Neue Haas Grotesk for neo-grotesk proportions.
- Use LL Replica as a reference for the mathematical grid-based drawing style.
- Use Inter, Geist, Rubik, Noto, IBM Plex, and Bricolage from reference-fonts.
- Use the referance fonts as examples for weight, spacing, and quality.
- Use `sources/drawing-references/` that shows the construction and outline quality we want.

## Grid and metrics

- Em 1024. Ascender and cap height 768, x-height 576, descender -256. Hebrew letter height 640.
- Keep points on-grid (2 units). Use 8 for new structure, handles, advances, sidebearings and kerning. Preserve Eli’s off-8 corrections.

```toml
[grid]
source = 2         # every point is on the 2-unit grid
machine_draft = 8  # new drafts use the 8-unit grid
```

- Snap intersections and cut ends to 8 within 3 units, otherwise to 2. Seen: v w x y V W X (9a2e884d).
- Preserve Eli’s optical stroke widths, including off-grid values. Seen: o side 98 and crown 84 (324e6a15), cap stems 100 (cbb174ea).
- Preserve measured values and curve construction. Grid constraints apply to source drawings only.

## Corners, tips and joins

- Bevel straight corners at 45°, 16 units per side (8 at tight junctions). Keep bevels straight and fixed across masters.

```toml
[chamfers]
exposed = 16
tight_junction = 8
```

- A tip ends on a flat after its bevel, never on an acute point.
  - The end of a diagonal gets a 16-unit flat.
  - Seen: less greater (cb7a5084), asciitilde (0faf5dbe), section (22ccd03a), v w x y V W X (9a2e884d), alef-hb (2026-11-15).
- No curve meets an edge in a point.
  - A curved stroke lands on a short flat, 8 units at a junction.
  - Seen: alef-hb (2026-11-15).
- In a weight transfer a cut can get larger, never smaller. Seen: Bold two three five six (c5042963).
- A tangent join is not a corner and gets no bevel. Keep the small cuts and straight landings of the donors.
- Before you fit handles, name each connection: tangent continuation, straight landing, deliberate cut, shelf or intended inflection.

## Strokes and curves

- Check apparent weight in Runebender’s thickness heatmap (Curves → Thickness).
  - Compare both edges at ¼, ½ and ¾ of a suspect turn.
  - Adjust paired handles and remeasure after rounding.
  - Heatmap colors track the glyph median.
  - Inspect visible faults even within target ranges.

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

- Diagonals are straight, with parallel edges, through every join.
- Place an on-curve point with an axis-aligned tangent at every crest, trough and side extreme. Seen: asciitilde (56f4b437), section (22ccd03a), b d (dec6b4b3).
- A turn in a bowl or a shoulder keeps one direction of curvature. Seen: hamzaabove-ar Bold (ce3a7669).
- G2 is not the target. A join can keep a curvature change when the shape needs it. Seen: hamzaabove-ar Bold (ce3a7669).
- A line that continues into a collinear handle is a smooth point. A corner is a deliberate kink only. Seen: 372bb48e.
- Handles within one segment have similar lengths, and the lengths follow the proportions of the glyph.
- Look at the whole filled shape before local curves. Change one node at a time and check its neighbors again.
- Review fill, curvature, joins and opposing edges. Repeat after rounding. Check every master, intermediate weights and words.
- Harmonize, Balance, Optimize and Simplify in Runebender can remove intended unequal handles.
  - Use them on a copy.
  - `fgtools lint-curves <Master> <glyph> --joins` reports are a reason to look, not a verdict.

## Bowls and rounds

- Copy o’s round half point-for-point for b d p q g.
  - Target 95% of o’s counter.
  - Derive b p q from approved d.
  - Seen: d (88b4aa2).
- Use o’s round sidebearing and 64 on Regular’s stem side.
  - Draw the junction.
  - Reverse mirrored contours.
  - Preserve bowl scale and wall curvature.
  - Seen: d (88b4aa2).
- Give g a shorter, higher bowl than o and a fuller upper left. Draw ear, spine and tail by eye. Tail depth −216.
- Geometric does not mean rectangular: keep oval bowls and counters. Seen: samekh v4, rejected (df38c4a2).
- Arabic letter dots are near-perfect circles: four symmetric cubic quarters.
  - A dot has no bevel.
  - This is for letter dots, not for every vowel mark.

## Weight and Bold

- Transfer construction relationships, not scaled coordinates. A Bold edge keeps the direction of the Regular edge. Seen: Bold seven nine (70c6a082).
- Open a Bold counter with width, not a thinner stem. Bold lowercase stems stay 192. Seen: Bold n b d (9fb03696).
- Before a weight transfer, decide which edges, alignments and counters are fixed.
  - Do not assume the Latin pattern for Arabic or Hebrew.
  - Seen: Bold zayin-hb, Bold hamzaabove-ar (ce3a7669).
- Masters: Thin 100, Regular 400, Bold 700, Black 900, each at 14 and 144 pt.
  - Thin and Black use Regular and Bold as donors:

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

- Derive 144 pt from the same weight at 14 pt.
  - Reduce each free sidebearing by `side`, including free sides in رب.
  - Shorten joining sides by the same amount.
  - Reach full adjustment at `complete`.
  - Preserve zero-advance marks and Eli’s display corrections.

```toml
[optical_size]
from = 14       # pt: the masters that are drawn
to = 144        # pt: the masters that are calculated
side = 24       # units that each side of a glyph loses
complete = 72   # pt: the size at which the change is complete
```

- The active axes are weight and optical size.

## Structure of the sources

- All masters have the same contours, points, point types, point order and components. Do not reorder points or contours.
- No overlapping contours. Seen: dollar (7f8be952), one.tf (dbe60148).
- Start contours leftmost in Latin, rightmost in Arabic and Hebrew. Break ties at the lowest point. Seen: asciitilde (56f4b437).
- Keep a compatible lowercase a.
  - Both waist edges land on horizontal shelves before 8-unit stem cuts.
  - Land the foot flat on the baseline.
  - Compare 9e009aad.
  - Regular triples give left x, right x and y.
  - Seen: 3c25f669.

```toml
[a_geometry]
regular_upper_waist = [328, 424, 352]
regular_lower_waist = [360, 424, 280]
regular_foot = [512, 560, 0]
```

- All masters have the same kerning groups and pairs. Kerning values are multiples of 8.

## Spacing

- Round forms fit tighter than flat-sided forms, and symmetric letters have balanced sidebearings.
  - Values use the 8-unit grid and recurring intervals (32, 48, 64, 96).
  - Judge spacing in words at 400, 550 and 700.
  - Keep approved widths that are off the grid.

## Latin

- h and m take their stems, shoulder and arch from the current n. Seen: m h (cbb174ea).
- Align mark heights over equal-height letters. Clear ascenders and capitals. Remove i and j dots under top marks.
- Optically center symmetric marks. Aim the lower end of acute and grave at center. Use consistent placement on asymmetric letters.
- A c edilla joins C and S at the center of the bowl.
  - An ogonek joins at the bottom right, or at the stem of I and i.
  - A comma accent is under the center with a gap.
  - The caron of d, t, l and L is an apostrophe form.
- A mark does not touch a part that it is not designed to join.
  - The masters have the same components and relative mark positions.

## Hebrew

- Match Regular Arabic contrast in Hebrew. Horizontals 104, uprights 88, descending right diagonals about 100, descending left tails 88–96.

```toml
[targets.Regular.Hebrew]
vertical_stem = [84, 92]
horizontal_stroke = [100, 108]
stroke_limit = 180
```

- The lamed ascender reaches 768. Final forms descend to -192.
- When a Hebrew letter looks wrong, compare its skeleton with Rubik, and follow that structure with Virtua's chamfers and grid.
  - Simplify, do not add.
  - Seen: zayin shin finaltsadi samekh (4e900dd0, df38c4a2), gimel (3814ca96).
- Vowel dots are 96 square with 24-unit bevels, and vowel bars are 104 thick. Bold: dots 128, bars 136, bevels 32.
- Check mark attachment in the compiled font at several weights.

## Arabic

```toml
[targets.Regular.Arabic]
vertical_stem = [80, 112]
horizontal_stroke = [88, 112]
stroke_limit = 180
```

- Draw and correct the base letters before their marks. The horizontal is usually a little heavier than the upright. Seen: 211c3b8d.
- The two terminals of an isolated boat or cup have the same thickness. Seen: behDotless-ar (67f4d301).
- Shape real neighbors at 400, 550 and 700.
  - Measure both join edges.
  - Take ligature stacking and proportions from the reference, curves and weight from Virtua.
  - In في preserve the middle shelf and initial feh’s counter and crown at native scale.
  - Proof في, فِي, فيه and لفي at every weight, with and without marks.

## Glyph decisions

- Thin medial heh (ـهـ) follows Regular’s vertical upper-counter wall and level joining stroke. Inspect the bowl-to-connector bend in the filled glyph.

- Arabic kaf is rounded with an old-style S shape. Keep its openings and rounded turns.
- The raised return of yeh-ar.fina is intentional in every master.
- Seen keeps upright teeth, separate rounded lobes and small junctions.
  - Start from seen-ar.init and seen-ar.medi.
  - Eli rejected version 4 although it passed the checks.
- The at sign keeps the small italic a and the continuous double spiral. Look at the whole filled spiral, not at local measurements.
- dollar uses the uppercase S as its body (7f8be952). section has bevelled terminals (22ccd03a).
- A symbol made of lines is constructed from green symbols.
  - An organic symbol is traced from an image with img2bez, with Virtua's construction, scale and weight.

## Proofs and media

- Follow the [proof workflow in AGENTS.md](AGENTS.md#proofs). Subagents return findings. The coordinator runs `make proofs` once per batch and shares the [review index](http://127.0.0.1:8770/) after checking the Print, Full and grid links.

- Every proof, specimen, picture and video is laid out on the powers of two of the typeface. No format has an exception.
- Align positions and lengths to 8 px within 64 px modules. In print, use 4 pt within 32 pt modules.
- Type sizes double: 32, 64, 128, 256, 512 and 1024 pixels, with 24 for labels.
  - A picture has at most three sizes and two weights.
- Align cap tops to modules and text starts to columns.
  - Set Latin flush left, Arabic and Hebrew flush right.
  - Use 16 px leading increments.
- Motion: 30 frames in a second, loops of 128 or 256 frames, durations in multiples of 8 frames.
  - One value moves in a picture.
- A text is chosen to fit its measure. The size never changes to make a text fit.
- A picture has one label size, one line weight, two inks and one accent.
  - Each setting has a label with its size and weight.

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
