# Verify a change

Do these checks after a glyph edit and before you show the result to Eli.

1. Look at the filled glyph next to the green Virtua glyphs of the same
   construction.
2. Make sure that new points are on the grid of 8, and that both masters
   have the same contours, points and components.
3. Run `fontgarden lint-curves <Master> <glyphs> --joins` and look at each
   reported curve.
4. Build with `make build`. Look at the glyph at 400, 700 and an
   intermediate weight, and in each composite that uses it.
5. Compare the build with `reference-fonts/` in `make proof-web`.

To compare a before and an after build, prepare a snapshot with
`scripts/proof-web/app/prepare.py` and serve it with
`scripts/proof-web/serve.py --snapshot`. For a close view of Arabic details at
400 and 700, use `scripts/proof-web/app/render-detail.py`.

A passing check does not make a glyph correct. Report each visible fault, for
example a swollen join, a notch or a pinched counter, even when the checks
pass. Eli decides the grade.

The build and release checks are in [qa.md](../../qa.md).
