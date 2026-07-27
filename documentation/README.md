# Specimen & social images

The specimen and social-media images for Virtua Grotesk are generated with
[**designbot**](https://github.com/eliheuer/designbot) — a small DrawBot-style
Rust tool. Each image is a **little `.rs` script that lives right next to the
`.png` it produces**. Nothing project-specific is copied around: all the
reusable machinery (color themes, the OKLCH palette, canonical image sizes,
sRGB tagging) lives in designbot; a script here only holds the *content* and a
handful of explicit layout numbers.

```
documentation/
  specimen-square.rs      →  specimen-square.png     (1:1,   X / LinkedIn / IG)
  specimen-portrait.rs    →  specimen-portrait.png   (4:5,   IG feed)
  specimen-landscape.rs   →  specimen-landscape.png  (1.91:1, X / LinkedIn card)
  specimen-vertical.rs    →  specimen-vertical.png   (9:16,  Reels / Stories)
```

The `.rs` scripts are committed; the `.png` outputs are gitignored (regenerate
any time — the scripts are the source of truth).

## Render an image

Run from the **repo root** (so the font paths resolve):

```sh
designbot documentation/specimen-square.rs
```

This writes `documentation/specimen-square.png` next to the script. PNG output
is **social-optimized by default**: an sRGB tag, saturation + grain
pre-compensation for platform JPEG recompression, and the X-lossless alpha
trick. Add `--raw` if you want a plain, pixel-exact master instead. The first
run for a given script compiles a cache (~80 s); every run after that is
~1 second, so editing and re-rendering is fast.

Rebuild every specimen:

```sh
for s in square portrait landscape vertical; do
  designbot documentation/specimen-$s.rs
done
```

## Edit an image by hand

Open the `.rs` file. It reads top to bottom like a DrawBot sketch — the things
you'll touch:

- **Theme** — `let t = Theme::dark();` → `Theme::light()` or `Theme::black()`.
  Re-skins the whole card (ground / ink / furniture / rules).
- **Layout numbers** — `let (size, lead) = (210.0, 214.0);` (glyph size in px,
  baseline-to-baseline), and `let mut y = …` (first row's baseline). All
  explicit; no hidden auto-fit. Nudge and re-render.
- **Content** — the `for row in [ … ]` list (the rows of letters) and the four
  corner `text(...)` strings (foundry / license / family / repo).

Coordinates are DrawBot's: origin bottom-left, **y-up**, and `text()` sets the
baseline of the line at `y`.

## Add a new image

Copy the closest existing script, rename it (e.g. `poster-a.rs`), edit the
content and numbers, and render it — the output `.png` lands beside it
automatically.

## What lives where

| Concern | Lives in |
| --- | --- |
| Color themes / design systems | designbot — `Theme::dark/light/black` |
| Perceptual palette (OKLCH → sRGB) | designbot — `Color::oklch` |
| Canonical image sizes + margins | designbot — `Format::{Square,Portrait,Landscape,Vertical}` |
| sRGB tagging, X-lossless PNG | designbot — the `--social` flag |
| **This font's content + layout** | **these `.rs` scripts** |

To change the *system* (a theme color, a canonical size), edit designbot and
push; to change *an image*, edit its script here.

## Requirements

- The **designbot CLI**:
  `cargo install --git https://github.com/eliheuer/designbot designbot-cli`
- Fonts, read at render time:
  - `fonts/ttf/VirtuaGrotesk-Regular.ttf` (built from `sources/`; run `make build`)
  - Geist Mono, for the mono furniture (path set at the top of each script).
