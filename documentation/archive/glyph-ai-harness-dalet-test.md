# Glyph AI Harness Test: dalet-hb U+05D3

This records the first one-codepoint test of the glyph AI harness workflow after
the workflow contract was written.

## Target

- Glyph: `dalet-hb`
- Unicode: U+05D3
- Script: Hebrew
- Reference source: green Virtua glyphs plus Rubik Hebrew skeleton reference
- Result: promoted as an orange review glyph in both UFO masters

## What Worked

- The harness rendered current source references correctly.
- OpenAI image generation produced a usable dalet skeleton when given a rendered
  reference sheet.
- img2bez traced the generated images into clean line-based outlines.
- The first trace produced compatible contour structure across Regular and Bold:
  one contour, 12 line points in each master.
- A deterministic placement pass could fit both masters to the intended Hebrew
  0..576 vertical band.
- After outline cleanup, the source passed build, proof, reports, and the
  Fontspector Google Fonts gate.

## Bugs Found

1. Missing-target metadata
   - `glyph_ai_harness.py prepare` cannot yet infer Unicode or widths for a
     glyph that does not already exist in the UFO.
   - For this run, U+05D3 and per-master widths had to be handled manually.

2. Single width in manifest
   - The manifest has one `target.width`, but Regular and Bold can need
     different advance widths.
   - The next harness version should store per-master width proposals.

3. Bold green-reference coverage
   - Regular has many green Latin references, but Bold currently has very few
     green-marked glyphs.
   - The harness can render explicit Bold references, but it correctly warns
     that they are not marked green.

4. img2bez comparison overwrite
   - The local single-master img2bez CLI writes the comparison image to a
     non-master-specific filename, so the Bold comparison overwrote the Regular
     comparison.
   - The harness should move/rename comparison images after each trace.

5. Placement/scaling is mandatory
   - Raw generated images traced too tall and below baseline.
   - A placement pass scaled both masters to y=0..576 and snapped to the grid.

6. Raster trace cleanup is mandatory
   - The first promoted trace caused `outline_semi_vertical` warnings because
     generated-image edges were slightly off horizontal/vertical.
   - Cleaning the source to exact horizontal, vertical, and 45-degree chamfer
     geometry removed the warnings.

7. `build/` is not durable
   - The initial run packet was created under `build/glyph-ai-harness/`.
   - Normal build/test commands removed that packet.
   - The harness default was changed to `.glyph-ai-runs/`, which is ignored by
     git but not removed by `make build` or `make test`.

## Verification

- `make build`: passed
- `make proof`: passed
- `make reports`: passed
- `make test`: passed
- Final `make test` result: WARN 0, FAIL 0
- Master compatibility: 0 blocking structure mismatches
- Built Hebrew cmap after this test:
  - U+05D3 `dalethb`
  - U+05D5 `vavhb`
  - U+05D9 `yodhb`
  - U+05DF `finalnunhb`
  - U+05E8 `reshhb`

## Source Files Added

- `sources/VirtuaGrotesk-Regular.ufo/glyphs/dalet-hb.glif`
- `sources/VirtuaGrotesk-Bold.ufo/glyphs/dalet-hb.glif`

Both source glyphs are marked orange for review.
