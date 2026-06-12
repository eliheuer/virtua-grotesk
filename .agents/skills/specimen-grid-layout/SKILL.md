---
name: specimen-grid-layout
description: Modular grid discipline for all DrawBot-skia specimen output in this repo — PNG social images and PDF proofs. Use whenever creating or editing a script in scripts/ that draws pages or images, or when reviewing/fixing layout. Encodes the house unit-grid idiom, the shared scripts/grid_system.py module, the GRID_VIEW overlay toggle, and the render-and-look verification loop.
---

# /specimen-grid-layout

Layout discipline for every image and PDF this repo generates. Based on
Müller-Brockmann's modular grid ethic (*Grid Systems in Graphic Design*,
1981) and the house drawbot idiom used across eliheuer font repos
(wallingford, fg-grotesk, micro-grotesk): **the grid is the coordinate
system, not decoration.**

## The system

- **One source of truth:** `scripts/grid_system.py`. Every drawing script
  imports `Grid` and `grid_view` from it. Never re-implement a local
  `grid()` function or hardcode margins per script.
- **Margin** = `min(width, height) / 16` unless a format dictates
  otherwise. **Unit** = `margin / 2`.
- **Every coordinate is a whole multiple of the unit**, measured from the
  margin lines: `g.x(0)` is the left margin line, `g.y_top(2)` is two
  units below the top margin line. If you find yourself typing a raw
  pixel number for a position, snap it: `g.snap(value)`.
- **Leading in stacked text should be unit-friendly** — when rows of type
  repeat down the page, prefer leadings that put successive baselines on
  or near unit lines. Cap heights are what the eye reads; align cap-tops
  or baselines, never bounding boxes.
- **Flush left, ragged right.** Headlines and repetition blocks start at
  `g.x(0)`. Centering is the exception (single hero glyphs), not the rule.
- **Restrained palette, one accent.** Near-black paper, gray-white ink,
  and the source markColor red `(1.0, 0.29, 0.24)` as the only accent.
  Captions live in the four corners (Font.Garden idiom), set in the font
  itself, on the margin lines.

## The overlay toggle

`GRID_VIEW=1` in the environment turns on the live grid overlay in every
script that uses `grid_system`:

```bash
GRID_VIEW=1 make social-images
GRID_VIEW=1 make proof
GRID_VIEW=1 ./.venv/bin/python scripts/build_social_images.py
```

The overlay is drawn by `Grid.draw(db)` in the **same coordinate space
the layout uses** — minor lines every unit, major lines every 4 units,
the margin frame, and center crosshairs. If the overlay doesn't match
where elements sit, the layout is off the grid, not the overlay.

## Optical alignment — ink, not box

A display-size headline whose text-box origin is on a grid line still
looks misaligned: the letterform's ink is inset by its left side-bearing.
For large type at the left margin, shift by the measured side-bearing so
the **ink** lands on the line:

```python
x = g.x(0) - g.ink_left(font_path, txt, size)
db.text(txt, (x, baseline))
```

Side-bearings are font- and glyph-specific — measure with the actual
font being drawn, never assume. Small text (captions) does not need
this; apply it from roughly 100pt up.

## Verify — render and look, don't trust the math

After any layout change:

1. Render with `GRID_VIEW=1`.
2. Downscale for review: `sips -Z 640 out.png --out preview.png`.
3. Read the preview and check: left edges of ink on unit lines, repeated
   baselines evenly stepped, captions on the margin lines, nothing
   colliding with the caption band.
4. Render once more with the overlay off before committing — overlay
   pixels must never ship.

PNG output is quantized and deterministic (see `build_social_images.py`
`save()`); re-rendering unchanged sources must produce byte-identical
files. If git reports modified images after a no-op render, something
nondeterministic crept in (timestamps, hashes, dict ordering) — fix that
before committing.

## Applying to scripts

- `scripts/build_social_images.py` — fully on the system; use it as the
  reference implementation (per-format `Grid`, caption band derived from
  unit lines, fit-to-width sizes, stack() leading clamps).
- `scripts/build_general_proof.py` and
  `scripts/build_print_spacing_specimen.py` — US Letter pages with
  `Grid(612, 792, margin=36)` (unit 18). The overlay toggle is wired into
  page creation; when editing these layouts, move positions onto unit
  coordinates rather than adding new magic numbers.
- New scripts: start from the constants block (`WIDTH`, `HEIGHT`,
  `Grid`), place everything through `g.x()/g.y()/g.y_top()/g.columns()`,
  and add a `GRID_VIEW=1` screenshot to your review loop before the
  first human look.
