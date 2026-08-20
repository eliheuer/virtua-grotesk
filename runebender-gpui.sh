#!/usr/bin/env bash
# Open this font in runebender-gpui (the native editor).
#
# The binary comes from `cargo install --path ~/GH/repos/runebender-gpui`;
# fall back to that checkout's release build when it is not on PATH.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_PATH="${RUNEBENDER_SOURCE:-sources/VirtuaGrotesk.designspace}"

BIN="$(command -v runebender-gpui || true)"
if [[ -z "$BIN" ]]; then
  BIN="$HOME/GH/repos/runebender-gpui/target/release/runebender-gpui"
fi
if [[ ! -x "$BIN" ]]; then
  echo "runebender-gpui was not found." >&2
  echo "Install it: cargo install --path ~/GH/repos/runebender-gpui" >&2
  exit 1
fi

exec "$BIN" "$ROOT_DIR/$SOURCE_PATH"
