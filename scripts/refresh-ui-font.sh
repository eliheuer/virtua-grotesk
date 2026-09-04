#!/usr/bin/env bash
# Copy the built Regular into the editors that use Virtua Grotesk as
# their interface font. Run ./build.sh first for a fresh build.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/fonts/ttf/VirtuaGrotesk-Regular.ttf"
[[ -f "$SRC" ]] || { echo "no built font at $SRC; run ./build.sh" >&2; exit 1; }
for repo in runebender-gpui runebender-xilem; do
  dest="$ROOT/../$repo/assets/fonts"
  [[ -d "$ROOT/../$repo" ]] || continue
  mkdir -p "$dest"
  cp "$SRC" "$dest/VirtuaGrotesk-Regular.ttf"
  cp "$ROOT/OFL.txt" "$dest/VirtuaGrotesk-OFL.txt"
  echo "$repo: refreshed"
done
