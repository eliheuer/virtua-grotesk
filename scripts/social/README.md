# Virtua Grotesk — DesignBot social system

Native social-media compositions for the "Virtua Grotesk: Powers-of-Two Design
Grids for Neural Networks" post, drawn with [DesignBot]. This crate is the
**PHASE 4** promotion pass that the blog-figure crate at
`~/GH/repos/elih.net/scripts/virtua-grotesk` planned in its `export_social.py`
header and the placeholder at the bottom of its `src/lib.rs`: native **square
(2048×2048)** and **vertical (1080×1920)** compositions plus an Instagram
**carousel (1080×1350)**, instead of letterboxing the fixed 2520×1320 blog card.

It reuses the blog crate's renderer, its OKLCH color-management guardrail, and
its section-03 technical-drawing language — applied to social-native canvases and
motion. The look is Eli's established aesthetic; this crate does **not** invent a
new one.

[DesignBot]: https://github.com/eliheuer/designbot

## What it produces (the three proven formats)

| Format | Binary | Output | Notes |
| --- | --- | --- | --- |
| IG carousel, 1080×1350 | `carousel` | `out/carousel/03-dyadic-grid/slide-0N.png` | 6 slides teaching §03 |
| Square animation, 2048×2048 | `sq_morph` | `out/frames/sq_morph/*.png` → `out/video/sq-morph.{mp4,gif}` | Regular↔Bold weight interpolation on `n`, seamless loop |
| Vertical reel, 1080×1920 | `reel_grid` | `out/frames/reel_grid/*.png` → `out/video/reel-grid.{mp4,gif}` | grid-as-dataset scan, seamless loop |

All of `out/` is gitignored (regenerable); the Rust sources and scripts are the
source of truth.

## Regenerate

```sh
cd scripts/social
./render.sh          # or: make
# targeted:
./render.sh carousel # just the PNG slides
./render.sh square   # frames + mp4 + gif
./render.sh reel     # frames + mp4 + gif
```

`render.sh` builds the release binaries, runs them (each emits a color-managed
PNG frame sequence / slide set), then encodes the animation frame sequences to
mp4 + gif with ffmpeg (x264 CRF 16, yuv420p, BT.709-tagged; gif via
palettegen/paletteuse). Animations render a **frame sequence** varying one
parameter — no runtime video interpreter — so every frame is an inspectable,
sRGB-tagged PNG.

## Dependencies

- **cargo** (Rust). The `designbot`/`designbot-render` git deps are pinned to the
  exact commit the blog-figure crate uses (`f36dd25…`), so builds reuse the
  already-cached checkout and work offline.
- **ffmpeg** — mp4/gif encoding. If absent, `render.sh` still writes the PNG
  frames and prints a skip note; encode later on a machine that has it.
- Inputs read at render time (a slightly-stale font is fine for system art):
  - `<repo>/sources/VirtuaGrotesk-{Regular,Bold}.ufo` (glyph outlines)
  - `~/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf` (all labels)

  Pinned in `src/inputs.rs`; edit there to move to a new source deliberately.

## Reusing in another repo

The crate is a **copyable template with one config file**. The split is strict:

| Layer | Files | Per-repo? |
| --- | --- | --- |
| **Portable core** | `src/style.rs`, `src/technical.rs`, `src/lib.rs`, `render.sh`, `Makefile` | No — copy verbatim, never edit |
| **Project config** | `src/inputs.rs` | Yes — the only file to edit for a rebrand |
| **Content** | `src/bin/*.rs`, `Cargo.toml` `[package]`/`[[bin]]` | Yes — new compositions per repo |

The portable core carries **no** project logic (`grep -riE
'virtua|elih|geist' src/style.rs src/technical.rs src/lib.rs` returns only two
provenance comments citing the blog crate these were ported from — no code, no
paths that are read). Every project identity string — brand mark, footer
URL, human family name — lives in `src/inputs.rs` as `BRAND` / `BRAND_URL` /
`PROJECT`, and every font/UFO path resolves there too. The shared carousel
`chrome()` reads `inputs::BRAND`/`inputs::BRAND_URL`, so it copies without edits.

**Copy-and-edit steps for a new font repo `<newfont>`:**

1. `cp -r scripts/social <newfont>/scripts/social` (drop `out/`, `target/`).
2. In `Cargo.toml`, rename `[package] name` (e.g. `newfont-social`). Keep the
   pinned `designbot` rev unless you deliberately move it.
3. Edit **`src/inputs.rs` only**:
   - `regular_ufo()` / `bold_ufo()` (and `virtua_sources()`/`virtua_repo()` —
     rename freely; they resolve from `CARGO_MANIFEST_DIR`, so the enclosing
     checkout is found automatically) to point at the new UFO masters.
   - `geist_mono()` if the label face differs.
   - `BRAND`, `BRAND_URL`, `PROJECT`.
4. Write new content binaries under `src/bin/` (start by copying `carousel.rs` /
   `sq_morph.rs` / `reel_grid.rs`); change only the copy, glyphs, and layout.
   Add matching `[[bin]]` entries. Keep all drawing calls inside `role::` /
   `TechnicalStyle` — **no raw RGB or pixel literals in a binary**.
5. `cargo build && ./render.sh` — offline once the designbot checkout is cached.

**Core as a shared crate?** The three core files could be split into a git
dependency (`social-designbot-core`) so multiple repos share one source of
truth instead of copies drifting. It is deliberately **not** done yet: the core
still co-evolves with the compositions, and `style.rs`/`technical.rs` are the
"visual editing surface" a designer tweaks per family. The pragmatic target is
the copyable template above; promote to a crate only once the core stabilizes
across two or more real repos, at which point `inputs.rs` + `bin/*.rs` stay
local and the core arrives via `[dependencies]`.

## Harvested ideas / backlog

Concepts mined from the earlier prototype scripts at `scripts/designbot/social/`
(now retired) before deletion. Each is a future content binary; the portable
core already supports all of them. Motion uses `loop_pingpong` unless a **dwell
loop** is called out (hold at each weight extreme, then sine-ease across — worth
porting as a `loop_dwell(phase, dwell)` helper in `lib.rs` when the first of
these lands).

- **`reel_design_study`** (from `reel_design_study.rs`) — the gem; a `Format::
  Vertical` art reel, argument-driven on any glyph present in both masters
  (default `a`). Layers, back to front: (1) two oversized essay tickers scrolling
  as dark-on-dark texture ("A FONT IS A PROGRAM" top, "THE DATASET IS THE SOURCE
  CODE" bottom), each scrolling exactly one copy-width per loop so it's seamless;
  (2) a hero glyph scaled to ~1250px ink height, centered ~y=1090, bleeding the
  frame horizontally, drawn as translucent red fill + red contour + full handles
  and point markers (circle/square/small-circle), morphing Reg↔Bold on a dwell
  loop; (3) a **powers-of-two ladder** of small filled repeats at scales
  0.0625/0.125/0.25/0.5, each running the same morph offset in time (a staggered
  wave); (4) minimal green chrome rules with `BRAND` / `WGHT nnn` / section
  kicker / `BRAND_URL`. Brutalist, graphic-first. 4 s/loop, 4 loops.

- **`carousel_08`** (from `carousel_grid_as_dataset.rs`) — a **9-slide essay
  carousel** mapping to blog §08 "The Designspace Is a Data Factory", set in the
  project's own display face + Geist Mono captions on the shared dark grid. Slide
  spine: (01) cover "Aa" + "Grid as Dataset" headline; (02) "A font is a program"
  with a `MOVE/LINE/CURVE/CLOSE` mono block; (03) "Powers of two" with the metrics
  table (UPM 1024, cap 768, x-height 576, descender −256, chamfer 16, grid 2);
  (04) "Consistency is signal" body; (05) "Glyphs are sentences" with a
  `BOS…MOVE…CLOSE…EOS` token block; (06) "A small model learns to draw" (12M
  params / 1,722 tokens / 2 masters / 1 laptop overnight); (07) "Boldening is
  local prediction" — Regular contour over translucent Bold mass, point-compatible
  overlay; (08) "A designspace is a data factory" — the same glyph at five
  interpolated weights in a ramp; (09) CTA with `BRAND_URL`, repo URL, OFL 1.1.
  Reuses the current `heading`/`legend`/`chrome`; add a Virtua-display text
  helper (`virtua_text` at a `wght`) since this carousel typesets in the family
  itself, not only Geist Mono.

- **`reel_spec_sheet`** (from `glyph_sheet_vertical.rs`) — a `Format::Vertical`
  single-glyph **full spec sheet** morphing Reg↔Bold on a dwell loop. Default
  glyph `G` (advance 832 = 52×16, a clean multiple). One static cell sized to the
  Bold advance (so grid/tags/ticks never move; only the letter breathes),
  16-unit design grid, blue cell-boundary verticals, dashed overshoot + solid
  cap/x-height/baseline metric lines, translucent-red glyph with handles+points,
  blue **metric tags** (`CAP 768`, `X-HEIGHT 576`, `BASELINE 0`, `OVERSHOOT ±16`)
  docked to the cell edges, a **dimension row** with 45° **hatched side bearings**
  and live width/side-bearing numbers, boundary ticks with knockout nodes, green
  chrome. Reuses `metric_rules`/`dim_h`; needs ported `metric_tag`, `hatch`, and
  `node` helpers (add to `lib.rs`).

- **`sq_og_sheet`** (from `og_dimension_sheet.rs`) — the blog OG dimension sheet
  **animated** on a square/wide canvas: the word **grid** (`G` `r` `i` `d`) laid
  out in per-glyph cells sized to the Bold advances, all four glyphs morphing
  Reg↔Bold together on the dwell loop, with the metric tags, hatched side
  bearings, and **live per-glyph width / side-bearing numbers** all updating as
  the ink breathes. Everything static except the letters and the numbers that
  track them. Same `metric_tag`/`hatch`/`node` helpers as `reel_spec_sheet`;
  a natural `Format::Square` companion to `sq_morph`.

## Architecture (mirrors the blog crate's 7 layers)

```
scripts/social/
  Cargo.toml         designbot deps (pinned rev) + crc32fast/kurbo/norad
  render.sh          build → run → ffmpeg encode
  Makefile           make {all,carousel,square,reel,build,check,clean}
  src/
    inputs.rs        pinned fonts / UFO sources
    style.rs         THE visual editing surface — OKLCH color, line/type scales,
                     and role:: mappings. No RGB literals in binaries.
    technical.rs     TechnicalStyle::section_three() — the no/HO/optical drawing
                     language (grid, glyph pen, point language) as a preset.
    lib.rs           shared mechanics: Format (canvas sizes), color-managed
                     write_png, Sheet + labels (incl. auto-fit), UFO loading,
                     RawGlyph master interpolation, Frame, grids, dimensions,
                     easing/loop helpers.
    bin/
      carousel.rs    content + layout for the §03 carousel
      sq_morph.rs    the square weight-interpolation animation
      reel_grid.rs   the vertical grid-as-dataset reel
  out/               gitignored renders
```

Where to edit, same rules as the blog crate:
- Change a hue everywhere → its swatch in `style::color`.
- Change which swatch a job uses → the function in `style::role`.
- Change the shared drawing language → `TechnicalStyle` in `technical.rs`.
- Change one composition → its `src/bin/*.rs` (content + local layout constants;
  **no raw RGB** in binaries — use `role::`).

### Color management (carried over, not reinvented)

`style::oklch_srgb` and `lib::write_png`/`tag_png_as_srgb` (+ the `crc32fast`
dep) are copied from the blog crate per its README handoff rule. Every PNG is
written with explicit sRGB/gAMA/cHRM chunks so social ingestion pipelines don't
guess the color space and recompress unevenly. Keep this guardrail if these
sources are copied further.

### Coordinate convention

DesignBot's canvas is **y-up** (origin bottom-left), like the blog crate.
`Frame::fit` maps source-space glyph coordinates into a format's live area,
reserving optional top/bottom bands for a headline and caption. `draw_body`
and every point/grid/dimension helper go through `Frame`, so nothing is drawn
with a raw pixel literal for a glyph coordinate.

### Animations

A binary renders `N` numbered PNG frames while varying one parameter, then
`render.sh` encodes them. Loops use `loop_pingpong(phase)` (a 0→1→0 eased
ramp), so frame `0` and frame `N-1` are one step apart and the loop is seamless
with no duplicated frame. `sq_morph` varies the interpolation factor (Regular↔
Bold, a real master interpolation via `interp_raw`, so every on/off-curve point
and the advance width animate); `reel_grid` varies the source-space row of a
scan band sweeping the glyph.

## Extending to all 8 sections × 3 formats

The post has 8 sections and a fixed figure vocabulary
(`fig-system-no/ho`, `fig-optical-correction`, `fig-model-bolden-n`,
`fig-interp[-outlines]`, `fig-ladder`, `fig-midpoint`, `fig-bits`,
`fig-grid-labels`, `fig-scaling`). This first pass proves one carousel, one
square animation, and one vertical reel. To scale to the full 8 × 3 grid:

**1. Carousel per section (static).** Generalize `carousel.rs` into a
`carousel <section>` binary driven by a small per-section table (title, kicker,
and a `Vec` of slide closures reusing `TechnicalStyle`, `dim_h/dim_v`, `legend`,
`heading`, `chrome`). Each section's slides come straight from that section's
figures + alt text in `index.mdx`:

| § | Section | Carousel spine (from its figures) |
| --- | --- | --- |
| 01 | The Modernist Impulse | grid backdrop title + `fig-scaling` |
| 02 | Replica and the Coarse Grid | coarse-grid `n`, advance/stem dims |
| 03 | Dyadic Self-Labeling Grid | **built** — two grids, points-on-8, 2^k dims, correction |
| 04 | Aesthetic Discipline & Machine Legibility | `fig-optical-correction` neutral vs grid-level points |
| 05 | Glyphs as Sentences | point language as tokens; `fig-grid-labels` |
| 06 | A Small Model Learns to Draw | `fig-model-bolden-n` panels |
| 07 | Weight Transfer as Delta Prediction | Regular→Bold delta, `fig-interp[-outlines]` |
| 08 | The Designspace Is a Data Factory | `fig-ladder`/`fig-bits`/`fig-midpoint` as a factory line |

Output `out/carousel/<NN-slug>/slide-0N.png`.

**2. Square animation per section.** Add `bin/sq_<topic>.rs` reusing the
`sq_morph` skeleton (fresh `Sheet` per frame, `loop_pingpong`, `Frame::fit` with
`Format::Square`). Natural motions per section: §03 point-snap reveal, §07 the
Regular→Bold delta arrows, §08 the midpoint Bézier subdivision animating
`fig-midpoint`, §06 the model completing a partial outline.

**3. Vertical reel per section.** Add `bin/reel_<topic>.rs` reusing the
`reel_grid` skeleton with `Format::Vertical`. The scan-band, a slow orbit of a
single glyph, or a weight breathe all loop cleanly with `loop_pingpong`.

**4. Wire them into `render.sh` / `Makefile`** as new targets, and mirror the
blog crate's `export_social.py`: number the outputs in post order, subfolder per
format (`square/`, `vertical/`, `carousel/`), and extract each asset's alt text
from `index.mdx` into an `alt-texts.md`. The numbering and alt-text extraction
stay exactly as that script already does them; this crate only adds the native
square/vertical/carousel renders it emits.

Keep every new composition inside `TechnicalStyle` + `style::role`; if a new
format needs a shared primitive changed, change it in `technical.rs`/`style.rs`
and re-review the three reference examples, not in a one-off binary.

## What needs Eli's design eye

Engineering is done and correct; these are judgment calls left open on purpose:

- **Copy.** Slide headlines/subtitles and the animation captions are first-pass
  wording. Titles auto-fit to the margin; final phrasing is yours.
- **Section-03 slide count / order.** Six slides is a reasonable teach; you may
  want more/fewer or a different figure spine.
- **8-unit grid density** on the carousel technical slides reads as a fine mesh
  at phone size (slide 4 already uses 16). Decide per slide whether the coarse
  machine grid should be 8 or 16.
- **Animation timing/length.** 4 s square / 5 s reel at 30 fps are defaults; the
  ease (`loop_pingpong`) and durations are tunable in each binary.
- **Palette accents.** Fill colors (yellow Regular / blue Bold, purple/red/blue
  dimensions) follow the blog roles; any accent re-mapping belongs in
  `style::role`, then re-review at thumbnail size.
- **Reference glyphs.** `n`/`o` were chosen for structure; swapping in other
  glyphs is a design choice (never auto-picked).
```
