---
name: specimen-grid-layout
description: Modular grid discipline for all designbot specimen output in this repo — PNG social images and PDF proofs. Use whenever creating or editing a script in scripts/designbot/ that draws pages or images, or when reviewing/fixing layout. Encodes the house unit-grid idiom, the inlined grid helpers, the GRID_VIEW overlay toggle, and the render-and-look verification loop.
---

# /specimen-grid-layout

Layout discipline for every image and PDF this repo generates. Based on
Müller-Brockmann's modular grid ethic (*Grid Systems in Graphic Design*,
1981) and the house idiom used across eliheuer font repos (wallingford,
fg-grotesk, micro-grotesk): **the grid is the coordinate system, not
decoration.**

All drawing scripts are **designbot** (Rust, single-file) under
`scripts/designbot/`, run via
`designbot --render scripts/designbot/<name>.rs --output <path> [-- <mode>]`.
The retired drawbot-skia originals (including the old shared
`grid_system.py`) live in `documentation/archive/agent-generated-scripts/`
— reference only, never wire them back in.

## The system

- **The grid helpers are inlined per script** (designbot scripts are
  single-file, so there is no shared module — the canonical Grid port to
  copy from is in `scripts/designbot/print_spacing_specimen.rs`). Keep the
  math identical across scripts; never invent a new grid idiom per script.
- **Margin** = `min(width, height) / 16` unless a format dictates
  otherwise. **Unit** = `margin / 2`.
- **Every coordinate is a whole multiple of the unit**, measured from the
  margin lines. If you find yourself typing a raw pixel number for a
  position, snap it to the unit grid.
- **designbot is y-down, top-left origin** (the archived drawbot scripts
  were y-up). The ports keep drawbot-style baseline math internally and
  flip at the draw call — follow that pattern, and remember
  `Canvas::text(s, x, y)` takes the TOP of the line, not the baseline
  (see `baseline_offset` in `scripts/designbot/general_proof.rs` for the
  exact parley first-baseline formula).
- **Leading in stacked text should be unit-friendly** — when rows of type
  repeat down the page, prefer leadings that put successive baselines on
  or near unit lines. Cap heights are what the eye reads; align cap-tops
  or baselines, never bounding boxes.
- **Flush left, ragged right.** Headlines and repetition blocks start at
  the left margin line. Centering is the exception (single hero glyphs),
  not the rule.
- **Restrained palette, one accent.** Near-black paper, gray-white ink,
  and the source markColor red `(255, 74, 61)` as the only accent.
  Captions live in the four corners (Font.Garden idiom), set in the font
  itself, on the margin lines. (Print proofs are the exception: black on
  white.)

## The overlay toggle

`GRID_VIEW=1` in the environment turns on the live grid overlay in every
ported script:

```bash
GRID_VIEW=1 make social-images
GRID_VIEW=1 make proof
GRID_VIEW=1 designbot --render scripts/designbot/social_images.rs \
  --output ~/Temp/check.png -- square:hero
```

The overlay is drawn in the **same coordinate space the layout uses** —
minor lines every unit, major lines every 4 units, the margin frame, and
center crosshairs. If the overlay doesn't match where elements sit, the
layout is off the grid, not the overlay.

## Optical alignment — ink, not box

A display-size headline whose text origin is on a grid line still looks
misaligned: the letterform's ink is inset by its left side-bearing. For
large type at the left margin, shift by the measured side-bearing so the
**ink** lands on the line. Side-bearings are font- and glyph-specific —
measure with the actual font being drawn (the ports parse `hmtx` for
this), never assume. Small text (captions) does not need this; apply it
from roughly 100pt up.

## Verify — render and look, don't trust the math

After any layout change:

1. Render with `GRID_VIEW=1`.
2. Downscale for review: `sips -Z 640 out.png --out preview.png`.
3. Read the preview and check: left edges of ink on unit lines, repeated
   baselines evenly stepped, captions on the margin lines, nothing
   colliding with the caption band.
4. Render once more with the overlay off before committing — overlay
   pixels must never ship.

Social/readme PNGs are quantized by the Makefile (`pngquant` post-step)
to keep tracked assets small; PDFs are vector with FlateDecode streams.
Re-rendering unchanged sources should produce visually identical files
(designbot renders are deterministic; quantization is too).

## Applying to scripts

- `scripts/designbot/social_images.rs` — fully on the system; the
  reference implementation (per-format grid, caption band from unit
  lines, fit-to-width sizes). One image per invocation via
  `<format>:<image>` modes.
- `scripts/designbot/general_proof.rs` and
  `scripts/designbot/print_spacing_specimen.rs` — US Letter pages,
  margin 36, unit 18. The overlay toggle is wired into page creation;
  when editing these layouts, move positions onto unit coordinates
  rather than adding new magic numbers.
- New scripts: copy the grid helpers from an existing port, place
  everything through the grid accessors, take a mode argument if the
  script emits more than one image (the CLI rewrites every `render_to_*`
  call to the single `--output`), and add a `GRID_VIEW=1` screenshot to
  your review loop before the first human look.
