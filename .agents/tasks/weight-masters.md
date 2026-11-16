# Task: add the Thin and Black masters

Start this task when Eli says that Regular and Bold are approved. Until
then, `make draft-weights` is a preview and a check of the two masters, and
nothing in `sources/` changes.

## Goal

The weight axis goes from 100 (Thin) to 900 (Black). Thin and Black are
masters of the designspace, calculated from Regular and Bold and then
corrected, with every glyph ready for Eli to review.

## Acceptance

- The UFOs of Thin and Black are in `sources/`, beside Regular and Bold, and
  the designspace has four sources and the axis 100 to 900.
- `sources/config.yaml` has the nine instances Thin, ExtraLight, Light,
  Regular, Medium, SemiBold, Bold, ExtraBold and Black.
- The stem and the bar of H in each new master are the targets of
  `[weights.<name>]` in `sources/design.toml`.
- `sources/design.toml` has `[targets.Thin.<script>]` and
  `[targets.Black.<script>]`, and `make check-design` reports no stroke
  finding that the report does not explain.
- Every glyph has the same contours, points and components in all four masters.
- No glyph of the report of `fgtools draft-weights` is "not compatible" or
  "inside out".
- Every glyph of the two new masters is purple. Regular and Bold do not change.
- `make build`, `make qa` and `make test-tools` succeed.

## Method

1. Run `make draft-weights`. Correct in Regular and Bold, with Eli, each
   glyph that the report lists as not compatible. Each one is a difference
   between the two masters that also harms the interpolation of today.
2. Look at `out/weights/` at each of the nine weights, in all three scripts.
   Set the targets in `sources/design.toml` again until H, O, n and o have
   the right weight. Change the targets, not the drafts.
3. Copy the two UFOs into `sources/`, and add the sources, the axis range and
   the instances. The designspace in `out/weights/` shows the form.
4. Correct what the calculation cannot do, glyph by glyph, in this order:
   contours that turned inside out; chamfers of the Thin, which are too
   large for a stroke of 28; counters of the Black that close (a, e, s, the
   Hebrew and Arabic bowls); advances of the Black that are too wide; marks
   and dots; kerning.
5. A correction that many glyphs need is a change to
   `fontgarden/draft_weights.py` in fontgarden-tools, with a test, not a
   change to each glyph.

## Constraints

- Work on a new branch. Do not push, merge or tag.
- Do not change a contour of Regular or Bold without Eli.
- Edit GLIF files surgically. Never call whole-UFO `font.save()`.

## Done

Report the targets used, the glyphs corrected by hand in each master with the
reason, the glyphs that still need Eli, and the commands run with their results.
