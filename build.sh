#!/bin/bash

# Build Virtua Grotesk through the Google Fonts builder.

set -euo pipefail

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if ! command -v gftools >/dev/null 2>&1; then
    echo "error: gftools is not installed or not on PATH." >&2
    echo "Install the project toolchain with:" >&2
    echo "  python3 -m venv .venv" >&2
    echo "  source .venv/bin/activate" >&2
    echo "  pip install -r requirements.txt" >&2
    exit 1
fi

echo "Building Virtua Grotesk fonts with gftools builder..."

rm -rf build build.ninja .ninja_log fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
mkdir -p fonts/variable fonts/ttf

gftools builder sources/config.yaml

built_fonts=()
while IFS= read -r font_path; do
    built_fonts+=("$font_path")
done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)

if [ "${#built_fonts[@]}" -eq 0 ]; then
    echo "error: gftools builder completed but produced no TTF files." >&2
    exit 1
fi

python scripts/fix_gf_metadata.py "${built_fonts[@]}"
rm -rf sources/build.ninja sources/.ninja_log sources/instance_ufos

echo ""
echo "Build complete! Fonts are in the fonts/ directory:"
find fonts/variable fonts/ttf -maxdepth 1 -type f -name "*.ttf" -print
