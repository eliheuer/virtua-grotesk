#!/usr/bin/env bash
# Social-image factory — theme-swappable, color-managed renders.
#
# The Rust bins are the source of truth: they emit sRGB-tagged PNGs (and, for
# animations, frame sequences that this script encodes to mp4 + gif). Committed
# output lands in ../../documentation/social-assets/; a --scratch run (passed
# straight through) writes throwaways under out/.
#
#   ./render.sh                        # every composition, every configured theme
#   ./render.sh specimen               # one composition, every configured theme
#   ./render.sh specimen light         # one composition, one theme
#   ./render.sh specimen light square  # one composition, one theme, one format
#
# Deps: cargo (offline once designbot is cached); ffmpeg (only for animations).
set -euo pipefail
cd "$(dirname "$0")"

# --- config -----------------------------------------------------------------
# Which themes to render when none is named. Edit freely.
THEMES=(dark light)
# Static-image compositions (each accepts --theme / --format / --scratch).
STATICS=(specimen)
# Animation compositions (emit out/frames/<name>/; encoded below). None yet.
ANIMATIONS=()

# --- ffmpeg encode helpers (kept ready for the animation phase) -------------
have_ffmpeg=1
command -v ffmpeg >/dev/null 2>&1 || have_ffmpeg=0
# yuv420p for universal playback; BT.709 tagged so no player guesses colors.
X264="-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -an"

encode_mp4() { # <frames_dir> <fps> <out.mp4>
  [ "$have_ffmpeg" = 1 ] || { echo "  (no ffmpeg; frames in $1)"; return; }
  ffmpeg -y -loglevel error -framerate "$2" -i "$1/%04d.png" $X264 "$3"
  echo "  mp4 -> $3"
}
encode_gif() { # <frames_dir> <fps> <scale_w> <out.gif>
  [ "$have_ffmpeg" = 1 ] || return
  local pal; pal=$(mktemp -t vgpal).png
  local vf="fps=$2,scale=$3:-1:flags=lanczos"
  ffmpeg -y -loglevel error -i "$1/%04d.png" -vf "$vf,palettegen=stats_mode=diff" "$pal"
  ffmpeg -y -loglevel error -i "$1/%04d.png" -i "$pal" \
    -lavfi "$vf,paletteuse=dither=bayer:bayer_scale=3" -loop 0 "$4"
  rm -f "$pal"; echo "  gif -> $4"
}

# --- driver -----------------------------------------------------------------
cargo build --release --bins --quiet

render_static() { # bin theme [format...]
  local bin=$1 theme=$2; shift 2
  local args=(); [ -n "$theme" ] && args+=(--theme "$theme")
  local f; for f in "$@"; do args+=(--format "$f"); done
  echo "· $bin${theme:+ [$theme]}"
  cargo run --release --quiet --bin "$bin" -- "${args[@]}"
}

comp=${1:-all}; theme=${2:-}
formats=()
[ $# -gt 2 ] && { shift 2; formats=("$@"); }

if [ "$comp" = all ]; then
  for c in "${STATICS[@]}"; do
    for t in "${THEMES[@]}"; do render_static "$c" "$t"; done
  done
elif printf '%s\n' "${STATICS[@]}" | grep -qx "$comp"; then
  if [ -n "$theme" ]; then
    render_static "$comp" "$theme" ${formats[@]+"${formats[@]}"}
  else
    for t in "${THEMES[@]}"; do render_static "$comp" "$t" ${formats[@]+"${formats[@]}"}; done
  fi
else
  echo "unknown composition: $comp"; echo "known: ${STATICS[*]}"; exit 1
fi

echo "done"
