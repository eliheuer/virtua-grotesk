#!/usr/bin/env bash
# Render the social animations: native master + platform fits.
# Scripts are the source of truth; video outputs are gitignored.
set -euo pipefail
cd "$(dirname "$0")/../../.."
OUT=documentation/assets/social/video
mkdir -p "$OUT"

# OG dimension sheet: native 2400x1260 master, then ffmpeg fits.
# (Composition is horizontal by design; vertical formats letterbox on
# the sheet background color.)
designbot --render scripts/designbot/social/og_dimension_sheet.rs \
    --output "$OUT/og-sheet-native.mp4"
BG=101010
ffmpeg -y -loglevel error -i "$OUT/og-sheet-native.mp4" \
  -vf "scale=1920:-2,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:0x$BG" -an "$OUT/og-sheet-wide.mp4"
ffmpeg -y -loglevel error -i "$OUT/og-sheet-native.mp4" \
  -vf "scale=1080:-2,pad=1080:1350:(ow-iw)/2:(oh-ih)/2:0x$BG" -an "$OUT/og-sheet-feed.mp4"
ffmpeg -y -loglevel error -i "$OUT/og-sheet-native.mp4" \
  -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:0x$BG" -an "$OUT/og-sheet-reel.mp4"

# LAB stacked reel (native per-format compositions)
for f in reel feed wide; do
  designbot --render scripts/designbot/social/reel_grid_as_dataset.rs \
      --output "$OUT/grid-as-dataset-$f.mp4" -- "$f"
done
echo "done -> $OUT"
