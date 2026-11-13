#!/usr/bin/env bash
# Run Fontspector with the Font.Garden profile, which includes the Google
# Fonts profile. The profile is in scripts/fontspector_fontgarden.py.
#
#   check_gf_fonts.sh development        the built fonts, offline, with the
#                                        exclusions below
#   check_gf_fonts.sh full               the built fonts, all checks
#   check_gf_fonts.sh package DIRECTORY  an assembled google/fonts package
#
# Reports go to out/qa/<mode>/. A FAIL gives a failing exit status.
set -euo pipefail
cd "$(dirname "$0")/.."

MODE=${1:-development}
FONTSPECTOR=${FONTSPECTOR:-$(command -v .venv/bin/fontspector || command -v fontspector || true)}
[ -n "$FONTSPECTOR" ] || { echo 'Fontspector is missing. Run make setup.' >&2; exit 1; }
# The plugin runs with the Python of .venv, which has fontspectorapi.
export PATH="$PWD/.venv/bin:$PATH"
ARGS=(--plugin scripts/fontspector_fontgarden.py -p fontgarden
      --error-code-on fail --loglevel warn --succinct)

case "$MODE" in
    development|full)
        INPUTS=('fonts/variable/VirtuaGrotesk[wght].ttf' fonts/ttf/VirtuaGrotesk-*.ttf)
        ;;
    package)
        PACKAGE=${2:?usage: $0 package DIRECTORY}
        # Fontspector checks the article references only in its input set.
        INPUTS=("$PACKAGE"/*.ttf "$PACKAGE/METADATA.pb" "$PACKAGE/OFL.txt")
        while IFS= read -r file; do INPUTS+=("$file"); done < <(find "$PACKAGE/article" -type f | sort)
        ;;
    *) echo "usage: $0 [development|full|package DIRECTORY]" >&2; exit 2 ;;
esac

if [ "$MODE" = development ]; then
    # Known development debt, not release exceptions. The directory name
    # check needs the google/fonts package; the two after it need language
    # and subset work; the grid check waits for Eli to put section, uniE000,
    # germandbls and three Arabic advances on the grid. Do not add an
    # exclusion to hide a new failure.
    for check in googlefonts/repo/dirname_matches_nameid_1 \
                 googlefonts/glyphsets/shape_languages \
                 googlefonts/metadata/unreachable_subsetting \
                 fontgarden/grid; do
        ARGS+=(--exclude-checkid "$check")
    done
    ARGS+=(--skip-network)
fi

for input in "${INPUTS[@]}"; do
    [ -f "$input" ] || { echo "Missing $input. Run make build." >&2; exit 1; }
done
REPORTS=out/qa/$MODE
mkdir -p "$REPORTS"
"$FONTSPECTOR" "${ARGS[@]}" --json "$REPORTS/fontspector.json" \
    --ghmarkdown "$REPORTS/fontspector.md" "${INPUTS[@]}"
