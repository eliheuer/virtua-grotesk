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
# high-quality fits: platforms recompress whatever we upload, so give
# them the best possible source — CRF 16, lanczos downscale, BT.709
# tagged so no player guesses the colors
BG=101010
Q="-c:v libx264 -preset slow -crf 16 -x264-params aq-mode=3 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -an"
for spec in 1920:1080:wide 1080:1350:feed 1080:1920:reel; do
  IFS=: read -r FW FH NAME <<<"$spec"
  ffmpeg -y -loglevel error -i "$OUT/og-sheet-native.mp4" \
    -vf "scale=$FW:-2:flags=lanczos,pad=$FW:$FH:(ow-iw)/2:(oh-ih)/2:0x$BG" \
    $Q "$OUT/og-sheet-$NAME.mp4"
done

# LAB stacked reel (native per-format compositions)
for f in reel feed wide; do
  designbot --render scripts/designbot/social/reel_grid_as_dataset.rs \
      --output "$OUT/grid-as-dataset-$f.mp4" -- "$f"
done
echo "done -> $OUT"
