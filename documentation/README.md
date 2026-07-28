# Documentation images

The specimen and promotional images for Virtua Grotesk are generated with
[**designbot**](https://github.com/eliheuer/designbot), a small DrawBot-style
Rust tool. Each image is a little `.rs` script that lives **right next to the
`.png` it produces**. Nothing project-specific is copied around: the reusable
machinery (color themes, the OKLCH palette, canonical image sizes, social/sRGB
optimization) lives in designbot; a script here holds only the *content* and a
few explicit layout numbers.

Images are organized into the Google-Fonts documentation folders:

```
documentation/
  readme-images/   README + specimen figures   ← we start here
  article/         About-section (ARTICLE) images
  social-assets/   social promo renders / animations   (added later)
```

## Current image

```
readme-images/specimen-regular.rs  →  readme-images/specimen-regular.png
```

A wide **1.91:1** card (the X / LinkedIn ratio): the Regular character set on a
single background color, in a single foreground color — no furniture, so a
theme swap re-skins the whole thing.

## Render

Run from the **repo root** (so the font path resolves):

```sh
designbot documentation/readme-images/specimen-regular.rs
```

The `.png` is written next to the script. PNG output is **social-optimized by
default** (sRGB tag + JPEG-recompression pre-compensation + the X-lossless
alpha trick); add `--raw` for a plain, pixel-exact master. The first run for a
script compiles a cache (~80 s); every run after is ~1 second.

## Edit by hand

Open the `.rs`. It reads top to bottom like a DrawBot sketch:

- **Theme** — `let t = Theme::dark();` → `Theme::light()`. Two colors,
  `t.ground` (background) and `t.ink` (type); the swap re-skins everything.
- **Content** — the `rows` array (the lines of glyphs).
- **Layout numbers** — `m` (margin; smaller = bigger type) and the vertical
  spacing. All explicit; no hidden auto-fit beyond the one-line "fit the
  uppercase row to the margins."

Coordinates are DrawBot's: origin bottom-left, **y-up**, and `text()` sets the
baseline of the line at `y`.

## What lives where

| Concern | Lives in |
| --- | --- |
| Color themes / design systems | designbot — `Theme::dark/light/black` |
| Perceptual palette (OKLCH → sRGB) | designbot — `Color::oklch` |
| Canonical sizes + margins | designbot — `Format::{Square,Portrait,Landscape,Vertical}` |
| Social/sRGB optimization | designbot — default (`--raw` opts out) |
| **This font's content + layout** | **these `.rs` scripts** |

## Requirements

- The **designbot CLI**:
  `cargo install --git https://github.com/eliheuer/designbot designbot-cli`
- `fonts/ttf/VirtuaGrotesk-Regular.ttf` (built from `sources/` via `make build`).

## Next

Once this specimen is dialed in: add the About-article images under `article/`,
then social posts + animations under `social-assets/`.
