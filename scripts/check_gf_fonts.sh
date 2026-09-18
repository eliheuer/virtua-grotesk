#!/usr/bin/env bash
# Development, full-font, and downstream-package Google Fonts QA.
set -euo pipefail
cd "$(dirname "$0")/.."

MODE=${1:-development}
FONTSPECTOR=${FONTSPECTOR:-fontspector}
QA_NETWORK=${QA_NETWORK:-online}
QA_REPORT_DIR=${QA_REPORT_DIR:-out/qa/$MODE}

case "$MODE" in
    development|full)
        if [ "$#" -gt 1 ]; then
            echo "usage: $0 [development|full|package DIRECTORY]" >&2; exit 2
        fi
        FONT_PATHS=(
            'fonts/variable/VirtuaGrotesk[wght].ttf'
            'fonts/ttf/VirtuaGrotesk-Regular.ttf'
            'fonts/ttf/VirtuaGrotesk-Medium.ttf'
            'fonts/ttf/VirtuaGrotesk-SemiBold.ttf'
            'fonts/ttf/VirtuaGrotesk-Bold.ttf'
        )
        ;;
    package)
        if [ "$#" -ne 2 ] || [ ! -f "$2/METADATA.pb" ] || [ ! -f "$2/OFL.txt" ] || [ ! -f "$2/article/ARTICLE.en_us.html" ]; then
            echo "package QA needs DIRECTORY with METADATA.pb, OFL.txt, and article/ARTICLE.en_us.html" >&2; exit 2
        fi
        shopt -s nullglob
        FONT_PATHS=("$2"/*.ttf)
        if [ "${#FONT_PATHS[@]}" -eq 0 ]; then echo 'Package has no TTFs' >&2; exit 2; fi
        ;;
    *) echo "usage: $0 [development|full|package DIRECTORY]" >&2; exit 2 ;;
esac

command -v "$FONTSPECTOR" >/dev/null 2>&1 || { echo "Missing Fontspector; see documentation/qa.md" >&2; exit 1; }
for font_path in "${FONT_PATHS[@]}"; do
    [ -f "$font_path" ] || { echo "Missing $font_path. Run make build." >&2; exit 1; }
done

INPUT_PATHS=("${FONT_PATHS[@]}")
if [ "$MODE" = package ]; then
    INPUT_PATHS+=("$2/METADATA.pb" "$2/OFL.txt" "$2/article/ARTICLE.en_us.html")
fi

ARGS=(-p googlefonts --error-code-on fail --loglevel warn --succinct)
if [ "$MODE" = development ]; then
    # Existing development debt. These are not release exceptions.
    # Directory naming needs downstream context; the other checks need
    # outline, language/mark, and subset work. Never add exclusions to hide debt.
    EXCLUDES=(
        googlefonts/repo/dirname_matches_nameid_1
        outline_alignment_miss
        googlefonts/glyphsets/shape_languages
        googlefonts/metadata/unreachable_subsetting
    )
    for check in "${EXCLUDES[@]}"; do ARGS+=(--exclude-checkid "$check"); done
    QA_NETWORK=offline
fi
case "$QA_NETWORK" in
    offline) ARGS+=(--skip-network) ;;
    online) ;;
    *) echo 'QA_NETWORK must be online or offline' >&2; exit 2 ;;
esac

mkdir -p "$QA_REPORT_DIR"
"$FONTSPECTOR" --version > "$QA_REPORT_DIR/tool-version.txt"
shasum -a 256 "${INPUT_PATHS[@]}" > "$QA_REPORT_DIR/input-sha256.txt"
git rev-parse HEAD > "$QA_REPORT_DIR/repository-revision.txt"
printf 'Mode: %s\nNetwork: %s\n' "$MODE" "$QA_NETWORK" > "$QA_REPORT_DIR/run.txt"
printf '%s\n' "${ARGS[@]}" "${INPUT_PATHS[@]}" >> "$QA_REPORT_DIR/run.txt"
# Clear only this run's generated reports so a failed invocation cannot leave
# an earlier result looking current.
rm -f "$QA_REPORT_DIR/fontspector.json" "$QA_REPORT_DIR/fontspector.md"
printf 'QA mode: %s; network: %s; reports: %s\n' "$MODE" "$QA_NETWORK" "$QA_REPORT_DIR"
"$FONTSPECTOR" "${ARGS[@]}" --json "$QA_REPORT_DIR/fontspector.json" \
    --ghmarkdown "$QA_REPORT_DIR/fontspector.md" "${INPUT_PATHS[@]}"
