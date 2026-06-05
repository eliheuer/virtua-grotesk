#!/bin/bash

# Build script for Virtua Grotesk fonts.
# Prefer the Google Fonts builder when available; keep the older local build
# path as a fallback while the GF toolchain is being installed.

set -euo pipefail

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Building Virtua Grotesk fonts..."

rm -rf build build.ninja .ninja_log fonts sources/build.ninja sources/.ninja_log sources/instance_ufos
mkdir -p fonts/variable fonts/ttf

if command -v gftools >/dev/null 2>&1; then
    echo ""
    echo "Building with gftools builder..."
    gftools builder sources/config.yaml
    built_fonts=()
    while IFS= read -r font_path; do
        built_fonts+=("$font_path")
    done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)
    if [ "${#built_fonts[@]}" -gt 0 ]; then
        python scripts/fix_gf_metadata.py "${built_fonts[@]}"
    fi
    echo ""
    echo "Build complete! Fonts are in the fonts/ directory:"
    find fonts/variable fonts/ttf -maxdepth 1 -type f -name "*.ttf" -print
    exit 0
fi

echo ""
echo "gftools is not installed; using fallback fontc/fontmake build."

echo ""
echo "Building variable font with fontc..."
fontc sources/VirtuaGrotesk.designspace
if [ -f "build/font.ttf" ]; then
    mv build/font.ttf 'fonts/variable/VirtuaGrotesk[wght].ttf'
    echo "Variable font built: fonts/variable/VirtuaGrotesk[wght].ttf"
fi

echo ""
echo "Building static instances with fontmake..."
fontmake -m sources/VirtuaGrotesk.designspace -i -o ttf --output-dir fonts/ttf

echo ""
fallback_fonts=()
while IFS= read -r font_path; do
    fallback_fonts+=("$font_path")
done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)
if [ "${#fallback_fonts[@]}" -gt 0 ]; then
    python scripts/fix_gf_metadata.py "${fallback_fonts[@]}"
fi

echo ""
echo "Build complete! Fonts are in the fonts/ directory:"
find fonts/variable fonts/ttf -maxdepth 1 -type f -name "*.ttf" -print
