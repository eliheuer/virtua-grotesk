#!/bin/bash

set -euo pipefail

FONT_PATHS=(
    'fonts/variable/VirtuaGrotesk[wght].ttf'
    'fonts/ttf/VirtuaGrotesk-Regular.ttf'
    'fonts/ttf/VirtuaGrotesk-Medium.ttf'
    'fonts/ttf/VirtuaGrotesk-SemiBold.ttf'
    'fonts/ttf/VirtuaGrotesk-Bold.ttf'
)

# Checks excluded from the gate, each with a reason and a re-enable
# condition. The goal is a ZERO-noise gate: anything this script prints
# is a regression. Revisit this list whenever one of the conditions is
# met, and prefer deleting entries over adding them.
#
# googlefonts/repo/dirname_matches_nameid_1
#   Local repo directory naming; not meaningful before GF packaging.
#
# Deferred until the Arabic drawing cleanup pass (overlapping parts
# currently produce near-degenerate intersections when instance overlap
# removal runs; fixing is outline redrawing work, tracked in
# documentation/manual-cleanup-handoff.md):
#   outline_alignment_miss, outline_colinear_vectors,
#   outline_semi_vertical, contour_count
#
# Deferred until the Latin language-coverage pass (auxiliary characters
# like E/I/O/U + breve/macron composites, and mark anchors for combining
# accents over ogonek/dotaccent bases):
#   googlefonts/glyphsets/shape_languages
#
# Deferred until GF packaging (requires a real METADATA.pb with an
# arabic subset; the PUA icon block E000-E021 will always be outside GF
# subsets by design):
#   googlefonts/metadata/unreachable_subsetting
EXCLUDES=(
    googlefonts/repo/dirname_matches_nameid_1
    outline_alignment_miss
    outline_colinear_vectors
    outline_semi_vertical
    contour_count
    googlefonts/glyphsets/shape_languages
    googlefonts/metadata/unreachable_subsetting
)

if ! command -v fontspector >/dev/null 2>&1; then
    echo "Missing fontspector. Install it from https://github.com/fonttools/fontspector/releases or with cargo-binstall."
    exit 1
fi

for font_path in "${FONT_PATHS[@]}"; do
    if [ ! -f "$font_path" ]; then
        echo "Missing $font_path. Run 'make build' before running Google Fonts QA."
        exit 1
    fi
done

mkdir -p "$HOME/.fontspector"

EXCLUDE_ARGS=()
for check in "${EXCLUDES[@]}"; do
    EXCLUDE_ARGS+=(--exclude-checkid "$check")
done

fontspector \
    -p googlefonts \
    "${FONT_PATHS[@]}" \
    "${EXCLUDE_ARGS[@]}" \
    --succinct \
    --loglevel warn \
    --skip-network

echo "Note: $(( ${#EXCLUDES[@]} - 1 )) checks deferred with documented reasons (see scripts/check_gf_fonts.sh)."
echo "Anything WARN/FAIL printed above is a regression."
