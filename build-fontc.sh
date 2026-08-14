#!/usr/bin/env bash
# Build Virtua Grotesk with fontc (the Rust compiler) instead of fontmake.
#
# fontc compiles a source to a font and has no instance flag, so the statics
# are cut out of the variable font with varLib.instancer rather than compiled
# one at a time. That is also the direction Google Fonts has been moving:
# instances cut from the variable are guaranteed to agree with it.
#
# gftools' own fontc path refuses to build statics alongside a variable font
# (gftools/builder/fontc.py sets buildStatic=False), and forcing it produces
# four copies of the default instance, so we do that step ourselves.

set -euo pipefail

if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

for tool in gftools fontc fonttools; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "error: $tool is not installed or not on PATH." >&2
        exit 1
    fi
done

VF="fonts/variable/VirtuaGrotesk[wght].ttf"
INSTANCES=(400:Regular 500:Medium 600:SemiBold 700:Bold)

echo "Building Virtua Grotesk with fontc ($(fontc --version))..."
rm -rf build build.ninja .ninja_log fonts \
       sources/build.ninja sources/build-*.ninja sources/.ninja_log \
       sources/instance_ufos
mkdir -p fonts/variable fonts/ttf

# 1. Variable font: fontc, then gftools' own fix + STAT generation.
gftools builder sources/config.yaml --experimental-fontc "$(command -v fontc)"

if [ ! -f "$VF" ]; then
    echo "error: fontc build produced no variable font at $VF" >&2
    exit 1
fi

# 2. Statics, cut from the variable at each instance location.
for spec in "${INSTANCES[@]}"; do
    wght="${spec%%:*}"
    name="${spec##*:}"
    out="fonts/ttf/VirtuaGrotesk-${name}.ttf"
    fonttools varLib.instancer -q --update-name-table -o "$out" "$VF" "wght=${wght}"
    gftools-fix-font -o "$out" "$out" >/dev/null
done

# 3. Repo metadata patches that the generic tools do not cover.
built_fonts=()
while IFS= read -r font_path; do
    built_fonts+=("$font_path")
done < <(find fonts/variable fonts/ttf -type f -name "*.ttf" 2>/dev/null)

if [ "${#built_fonts[@]}" -eq 0 ]; then
    echo "error: build completed but produced no TTF files." >&2
    exit 1
fi

python scripts/fix_gf_metadata.py "${built_fonts[@]}"
rm -rf sources/build.ninja sources/build-*.ninja sources/.ninja_log \
       sources/instance_ufos

echo ""
echo "Build complete! Fonts are in the fonts/ directory:"
find fonts/variable fonts/ttf -maxdepth 1 -type f -name "*.ttf" -print
