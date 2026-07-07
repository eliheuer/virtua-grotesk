# Hebrew Support Plan

This document tracks the Hebrew expansion plan for Virtua Grotesk. The goal is
to use Rubik as a practical open-source reference for Latin/Arabic/Hebrew source
organization, then use the img2bez/OpenAI raster workflow as a drafting tool for
new Virtua-style Hebrew outlines.

## Current State

- Virtua Grotesk currently has no encoded Hebrew glyphs in the built variable
  font or either UFO master.
- The active sources are `sources/VirtuaGrotesk-Regular.ufo`,
  `sources/VirtuaGrotesk-Bold.ufo`, and
  `sources/VirtuaGrotesk.designspace`.
- The repo worktree is already dirty from earlier Google Fonts/Arabic cleanup
  work. Hebrew work should avoid touching unrelated modified glyphs.
- Rubik is available locally at `/Users/eli/GH/repos/rubik` and already has UFO
  masters, so no Glyphs-to-UFO conversion is needed for reference inspection.

## Reference Scope

Rubik's shipped Google Fonts build covers 47 Hebrew codepoints:

- Marks: U+05B0..U+05BC, U+05C1, U+05C2, U+05C7
- Punctuation: U+05BE, U+05F2, U+05F3, U+05F4
- Letters: U+05D0..U+05EA, including the final forms

The Google Fonts `hebrew_unique-glyphs.nam` file is much larger. It includes
cantillation marks, support/control codepoints, U+25CC, shekel, and Hebrew
presentation forms. That larger set is not a good first drawing batch. The
pragmatic first target should match Rubik's 47-codepoint coverage, then decide
whether to expand to the full Google subset after the basic text setting works.

## Source Naming

Rubik uses readable source names such as `alef-hb`, `bet-hb`, `vav-hb`,
`finalnun-hb`, and `gershayim-hb`. The compiled TTF maps these to production
glyph names like `uni05D0`.

For Virtua, the same readable `*-hb` source-name convention is recommended. It
keeps feature code and Runebender review easier to read while still assigning
the correct Unicode values in each `.glif`.

## Metrics And Scaling

Virtua Grotesk uses:

- UPM 1024
- Ascender 832
- Descender -256
- x-height 576
- Cap height 832
- Preferred grid 2

Rubik uses:

- UPM 1000
- Ascender 750
- Descender -225
- x-height 520
- Cap height 700

The img2bez trace should therefore target Virtua's coordinate system directly,
not copy Rubik coordinates. For this repo the useful defaults are:

- `--target-height 1088`
- `--y-offset -256`
- `--grid 2`
- `--chamfer 0` for curved or mixed Hebrew forms

Advance widths should be chosen in Virtua space, then mirrored across masters
with the same glyph structure. Rubik widths are useful as proportions only.

## img2bez Constraint

The installed `img2bez` CLI currently supports a single-master trace:

```sh
img2bez --input glyph.png --output Master.ufo --name glyph --unicode 05D0
```

It does not currently expose a multi-master compatibility command. Separate
Regular and Bold traces can easily produce incompatible contour and point
structure. Until img2bez has a dedicated masters workflow, every generated
glyph must be treated as a sketch and reconciled before promotion.

## Recommended First Batch

Start with simple Hebrew letters that exercise different construction patterns
without immediately forcing mark positioning or presentation forms:

- `vav-hb` U+05D5
- `yod-hb` U+05D9
- `finalnun-hb` U+05DF
- `resh-hb` U+05E8

These are good first img2bez/OpenAI tests because they are simpler silhouettes,
they can be checked quickly in long Hebrew strings, and they make scaling,
baseline, and sidebearing problems obvious.

## Workflow

1. Render green Latin/Arabic Virtua references and selected Rubik Hebrew
   references as raster prompt material.
2. Generate clean black-on-white Hebrew glyph rasters with OpenAI image
   generation, one image per master.
3. Trace into scratch UFO copies with img2bez, never directly into the active
   sources first.
4. Compare Regular/Bold structure. If incompatible, either redraw one master
   from the other or use the trace only as a visual template.
5. Promote only compatible outlines into both Virtua masters.
6. Add each glyph to `contents.plist` and keep Unicode assignments identical.
7. Run `make reports`, `make build`, and proof strings that mix Latin, Arabic,
   and Hebrew.

## Later Work

After the first batch is stable:

- Add all 27 Hebrew letters and final forms.
- Add Hebrew punctuation and U+05F2/U+05F3/U+05F4.
- Add niqqud marks and anchors.
- Add `languagesystem hebr dflt;` and update GDEF/mark positioning.
- Decide whether Virtua should cover only Rubik's practical set or the full
  Google Fonts Hebrew subset.
