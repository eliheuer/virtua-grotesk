# Social assets

Promotional images, loops, and video for social media, generated with
[designbot](https://github.com/eliheuer/designbot). Each asset is a small `.rs`
script **co-located with the media it renders**; the rendered `.png` / `.gif` /
`.mp4` is gitignored (regenerable — force-add finals at v1.0).

Organized by the kind of thing you post:

| Folder | What | Typical output |
| --- | --- | --- |
| `reels/` | vertical video for Instagram Reels / TikTok | 9:16 `.mp4` |
| `loops/` | short seamless animated loops | 1:1 `.gif` + `.mp4` |
| `posts/` | single static feed images | 1:1 / 4:5 / 1.91:1 `.png` |
| `carousels/` | multi-slide swipeable image sets | numbered `.png` |

## Render

```sh
# from the repo root
designbot --render documentation/social-assets/reels/bounce.rs \
          --output documentation/social-assets/reels/bounce.mp4
```

PNG output is social-optimized by default (sRGB-tagged; `--raw` for a plain
master). Video (`.mp4`/`.gif`) needs ffmpeg and is tagged BT.709. Add music to a
reel with `~/Desktop/add-sound.sh` (designbot renders silent video).

## Current assets

| Script | Output |
| --- | --- |
| `reels/bounce.rs` | bouncing-glyphs physics reel (30s, 9:16) |
| `loops/weight-morph.rs` | `Aa` breathing the wght axis (Regular ⇄ Bold) |

See `../README.md` for the overall documentation-image system, the DrawBot-style
editing model, and the color / safe-zone conventions.
