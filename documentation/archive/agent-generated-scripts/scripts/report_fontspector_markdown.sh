#!/bin/bash

set -euo pipefail

OUTPUT_PATH="${1:-documentation/google-fonts/fontspector-googlefonts-report.md}"
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
        echo "Missing $font_path. Run 'make build' before generating the Fontspector report."
        exit 1
    fi
done

mkdir -p "$(dirname "$OUTPUT_PATH")"

mkdir -p "$HOME/.fontspector"

set +e
fontspector \
    -p googlefonts \
    "${FONT_PATHS[@]}" \
    --exclude-checkid googlefonts/repo/dirname_matches_nameid_1 \
    --ghmarkdown "$OUTPUT_PATH" \
    --loglevel warn \
    --skip-network \
    --succinct
status=$?
set -e

python3 - "$OUTPUT_PATH" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(
    "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
    encoding="utf-8",
)
PY

if [ "$status" -ne 0 ] && [ "$status" -ne 1 ]; then
    exit "$status"
fi

exit 0
