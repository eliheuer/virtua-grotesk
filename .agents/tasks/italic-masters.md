# Task: add the italic

Start this task when the upright masters are approved and Eli has decided
the three questions below. The italic is a slanted roman with corrections,
as in Rubik (12 degrees) and Inter (9.4 degrees). It is not a new design.

## Decisions for Eli

- The angle.
- Hebrew and Arabic: slanted like the Latin (Rubik slants its Hebrew to the
  right), slanted to the left, or upright.
- The grid: a slanted stem is not on the 8-unit grid in x. Either x is
  rounded to the 2-unit grid, or the italic masters are not part of the
  training data.

## Goal

`VirtuaGrotesk-Italic[wght].ttf` is built from one italic master for each
upright master. Google Fonts takes the italic as a separate file, not as an
axis. Each italic glyph is calculated from its upright glyph and is ready
for Eli to review.

## Acceptance

- fontgarden-tools has the command `fgtools draft-italic`, with tests, and
  its settings are an `[italic]` table of `context.md`.
- Each italic master has the glyphs, points and components of its upright
  master, so that the two can be compared point by point.
- A vertical stem has the same thickness, measured at a right angle to the
  stem, as in the upright master. A round letter has its thinnest and its
  thickest places where the upright has them.
- Chamfers are 45 degrees to the baseline after the slant, with the sizes of
  `[chamfers]`.
- Anchors and the offsets of components are slanted, so that the marks are
  above their letters. `make check-accents` reports no new finding.
- `fontinfo.plist` has the italic angle, and the caret slope follows it.
- Every glyph of the italic masters is purple. The upright masters do not change.
- `make build` and `make qa` succeed for both files.

## Method

1. Write the command in fontgarden-tools: slant by the angle, correct the
   curves (a plain slant makes one side of a round thin and the other
   thick), build the chamfers again, round to the grid.
2. Test the command on fonts with a known answer: slant the upright of a
   reference font that has an italic, and measure the distance to its italic.
3. Draft all italic masters into `out/italic/`. Look at them at each weight
   and in each script before anything is copied into `sources/`.
4. List the glyphs that need another form in italic (for example a, f, the
   arrows and the mathematical signs, which do not slant), with Eli.

## Constraints

- Work on a new branch. Do not push, merge or tag.
- Do not change the upright masters.
- A general tool goes in fontgarden-tools, not in `scripts/`.

## Done

Report the angle and the settings, the result of the test on the reference
fonts, the glyphs that need Eli, and the commands run with their results.
