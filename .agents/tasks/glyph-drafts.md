# Task: draft glyphs from the green glyphs

Start this task with a list of glyphs and masters from Eli, for example
"acute caron circumflex, Regular" or "the first 5 contour glyphs from
`make queue`, both masters".

## Goal

Each named glyph is redrawn as a purple draft that follows the construction
of the green glyphs, and is ready for Eli to review.

## Acceptance

- Each named glyph is changed in the named masters and marked purple.
- A second agent, which has only the picture of `fgtools render`,
  `CONTEXT.md` and the glyph names, gives each glyph in each master the
  verdict `pass`. A `fault` that remains after three rounds is in the report,
  with the rule number and the place.
- `.venv/bin/fgtools check-changes --glyphs "<names>" --proof output/review/<branch>`
  prints PASS. Its proof sheets exist.
- For each glyph, the stroke findings of `make check-design GLYPHS="<names>"`
  are corrected, or the report gives the reason the glyph differs.
- A glyph drawn in both masters has the same contours, points and components
  in both.
- `make build` succeeds.
- `make diff` shows glyph and word image differences only in the named
  glyphs and the glyphs that use them as components. The report lists them.
- `.venv/bin/fgtools check-repository` passes.
- No green glyph changed, and no file outside the named glyph files changed.

## Method

1. Read `AGENTS.md` and all of `CONTEXT.md`.
2. For each glyph, find the green glyphs that share its construction: the same
   stroke, bowl, turn, terminal, mark or joining form. Use them as donors.
   Copy their geometry where the construction is the same. Do not invent a
   construction that no green glyph shows.
3. Put new structural points on the 8-unit grid. Keep the 2-unit corrections
   of a donor where the donor geometry is copied.
4. Commit each glyph separately, so that the Git history keeps each draft.

## Constraints

- Work on a new branch `omp/<short-description>` from `main`. Do not push,
  merge or tag.
- Change only the named glyphs. Do not edit scripts, documentation, features,
  kerning or fontinfo.
- Do not add files to the repository. Write output under `output/`.
- Edit GLIF files surgically. Never call whole-UFO `font.save()`.

## Autonomy

- Choose the donors and the construction. Continue through all glyphs.
- If no green glyph shows the construction that a glyph needs, do not draw
  it. List it in the report with the decision that Eli has to make.
- Use subagents only for glyphs that do not share donors.

## Done

Report, for each glyph: the donors used, what changed, the remaining
`check-design` findings, and the proof sheet path. Then list the skipped
glyphs and the commands run with their results.
