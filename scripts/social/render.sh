#!/usr/bin/env bash
# Render the Virtua Grotesk social assets.
#
# The Rust binaries are the source of truth; they emit color-managed PNG frame
# sequences into out/frames/ and carousel slides into out/carousel/. This script
# builds them, runs them, then encodes the frame sequences to mp4 + gif with
# ffmpeg. All of out/ is gitignored (the repo .gitignore ignores `out/`).
#
#   scripts/social/render.sh            # everything
#   scripts/social/render.sh carousel   # just the carousel PNGs
#   scripts/social/render.sh square     # just the square animation
#   scripts/social/render.sh reel       # just the vertical reel
#
# Deps: cargo (offline once designbot is cached), ffmpeg (for mp4/gif).
set -euo pipefail
cd "$(dirname "$0")"

OUT=out
VID=$OUT/video
mkdir -p "$VID"

have_ffmpeg=1
command -v ffmpeg >/dev/null 2>&1 || have_ffmpeg=0

# High-quality x264 source; platforms recompress, so hand them the best master.
# yuv420p for universal playback; BT.709 tagged so no player guesses colors.
X264="-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -an"

encode_mp4() { # <frames_dir> <fps> <out.mp4>
  local dir=$1 fps=$2 out=$3
  if [ "$have_ffmpeg" = 1 ]; then
    ffmpeg -y -loglevel error -framerate "$fps" -i "$dir/%04d.png" $X264 "$out"
    echo "  mp4 -> $out"
  else
    echo "  ffmpeg not found; skipping $out (frames are in $dir)"
  fi
}

encode_gif() { # <frames_dir> <fps> <scale_w> <out.gif>
  local dir=$1 fps=$2 sw=$3 out=$4
  if [ "$have_ffmpeg" = 1 ]; then
    local pal; pal=$(mktemp -t vgpal).png
    local vf="fps=$fps,scale=$sw:-1:flags=lanczos"
    ffmpeg -y -loglevel error -i "$dir/%04d.png" -vf "$vf,palettegen=stats_mode=diff" "$pal"
    ffmpeg -y -loglevel error -i "$dir/%04d.png" -i "$pal" \
      -lavfi "$vf,paletteuse=dither=bayer:bayer_scale=3" -loop 0 "$out"
    rm -f "$pal"
    echo "  gif -> $out"
  else
    echo "  ffmpeg not found; skipping $out"
  fi
}

target=${1:-all}

if [ "$target" = all ] || [ "$target" = carousel ]; then
  echo "carousel (§03 dyadic grid, 1080x1350 PNGs)"
  cargo run --release --quiet --bin carousel
fi

if [ "$target" = all ] || [ "$target" = square ]; then
  echo "square animation (2048x2048 weight morph)"
  cargo run --release --quiet --bin sq_morph
  encode_mp4 "$OUT/frames/sq_morph" 30 "$VID/sq-morph.mp4"
  encode_gif "$OUT/frames/sq_morph" 20 900 "$VID/sq-morph.gif"
fi

if [ "$target" = all ] || [ "$target" = reel ]; then
  echo "vertical reel (1080x1920 grid-as-dataset loop)"
  cargo run --release --quiet --bin reel_grid
  encode_mp4 "$OUT/frames/reel_grid" 30 "$VID/reel-grid.mp4"
  encode_gif "$OUT/frames/reel_grid" 20 540 "$VID/reel-grid.gif"
fi

echo "done -> $OUT/"
