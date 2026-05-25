#!/bin/bash

set -euo pipefail

FONT_PATHS=(
    'fonts/variable/VirtuaGrotesk[wght].ttf'
    'fonts/ttf/VirtuaGrotesk-Regular.ttf'
    'fonts/ttf/VirtuaGrotesk-Medium.ttf'
    'fonts/ttf/VirtuaGrotesk-SemiBold.ttf'
    'fonts/ttf/VirtuaGrotesk-Bold.ttf'
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

fontspector \
    -p googlefonts \
    "${FONT_PATHS[@]}" \
    --exclude-checkid googlefonts/repo/dirname_matches_nameid_1 \
    --succinct \
    --loglevel warn \
    --skip-network
