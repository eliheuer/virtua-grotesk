#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNEBENDER_REPO="${RUNEBENDER_REPO:-/Users/eli/GH/repos/runebender-xilem}"
DEPS_DIR="$RUNEBENDER_REPO/target/release/deps"

if [[ ! -d "$DEPS_DIR" ]]; then
  echo "Runebender release deps not found: $DEPS_DIR" >&2
  echo "Build runebender-xilem first, or set RUNEBENDER_REPO=/path/to/runebender-xilem." >&2
  exit 1
fi

NORAD_RLIB="$(find "$DEPS_DIR" -name 'libnorad-*.rlib' | head -n 1)"
if [[ -z "$NORAD_RLIB" ]]; then
  echo "Norad rlib not found in: $DEPS_DIR" >&2
  echo "Build runebender-xilem first so this check can use the same loader crate." >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/norad_check.rs" <<'RS'
use std::path::Path;

fn main() {
    let path = std::env::args().nth(1).expect("usage: norad_check <ufo>");
    match norad::Font::load(Path::new(&path)) {
        Ok(font) => {
            println!("OK {} glyphs {}", font.default_layer().iter().count(), path);
        }
        Err(error) => {
            eprintln!("{error:?}");
            std::process::exit(1);
        }
    }
}
RS

rustc "$TMP_DIR/norad_check.rs" \
  --edition=2021 \
  -L "dependency=$DEPS_DIR" \
  --extern "norad=$NORAD_RLIB" \
  -o "$TMP_DIR/norad_check"

"$TMP_DIR/norad_check" "$ROOT/sources/VirtuaGrotesk-Regular.ufo"
"$TMP_DIR/norad_check" "$ROOT/sources/VirtuaGrotesk-Bold.ufo"
