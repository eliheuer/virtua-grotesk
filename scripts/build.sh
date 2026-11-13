#!/bin/bash
# Build Virtua Grotesk: the shared Font.Garden build (`fgtools build`),
# then the metadata fixes of this font (scripts/fix_gf_metadata.py).
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf build build.ninja .ninja_log
.venv/bin/fgtools build
.venv/bin/python scripts/fix_gf_metadata.py fonts/variable/*.ttf fonts/ttf/*.ttf
