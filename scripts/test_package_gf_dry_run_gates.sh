#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/venv/bin/python}"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-packager-gates.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

GF_REPO="$TMPDIR/fonts"
PACKAGE_DIR="$GF_REPO/ofl/virtuagrotesk"

git init -q -b main "$GF_REPO"
git -C "$GF_REPO" remote add origin git@github.com:eliheuer/fonts.git
git -C "$GF_REPO" remote add upstream https://github.com/google/fonts.git
mkdir -p "$PACKAGE_DIR"
printf 'name: "Virtua Grotesk"\n' >"$PACKAGE_DIR/METADATA.pb"
git -C "$GF_REPO" add ofl/virtuagrotesk/METADATA.pb
git -C "$GF_REPO" -c user.name="Virtua Test" -c user.email="virtua-test@example.com" commit --allow-empty -q -m "initial"
git -C "$GF_REPO" update-ref refs/remotes/origin/main HEAD
git -C "$GF_REPO" update-ref refs/remotes/upstream/main HEAD

write_metadata() {
    local mode="$1"
    local optional_line="${2:-}"
    local repository_url="${3:-https://github.com/eliheuer/virtua-grotesk}"
    local commit_value="${4:-0123456789abcdef0123456789abcdef01234567}"
    local designer_value="${5:-Eli Heuer}"
    local source_file_value="${6:-fonts/variable/VirtuaGrotesk[wght].ttf}"
    local primary_script_value="${7:-Arab}"
    local archive_url_value="${8:-https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/virtua-grotesk.zip}"
    local config_line=""
    local archive_line=""

    case "$mode" in
        with-config)
            config_line='  config_yaml: "sources/config.yaml"'
            ;;
        with-archive)
            archive_line="  archive_url: \"$archive_url_value\""
            ;;
    esac

    cat >"$PACKAGE_DIR/METADATA.pb" <<EOF
name: "Virtua Grotesk"
designer: "${designer_value}"
license: "OFL"
category: "SANS_SERIF"
date_added: "2026-05-23"
fonts {
  name: "Virtua Grotesk"
  style: "normal"
  weight: 400
  filename: "VirtuaGrotesk[wght].ttf"
  post_script_name: "VirtuaGrotesk-Regular"
  full_name: "Virtua Grotesk Regular"
  copyright: "Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)"
}
subsets: "arabic"
subsets: "latin"
subsets: "latin-ext"
subsets: "menu"
axes {
  tag: "wght"
  min_value: 400.0
  max_value: 700.0
}
source {
  repository_url: "${repository_url}"
  commit: "${commit_value}"
${archive_line}
  files {
    source_file: "OFL.txt"
    dest_file: "OFL.txt"
  }
  files {
    source_file: "${source_file_value}"
    dest_file: "VirtuaGrotesk[wght].ttf"
  }
  branch: "main"
${config_line}
}
primary_script: "${primary_script_value}"
stroke: "SANS_SERIF"
${optional_line}
EOF
}

expect_blocked() {
    local label="$1"
    local source_mode="$2"
    local metadata_variant="$3"
    local expected="$4"
    local optional_line="${5:-}"
    local output

    write_metadata "$metadata_variant" "$optional_line"
    if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" GFT_PACKAGER_SOURCE_MODE="$source_mode" ./scripts/package_gf_dry_run.sh 2>&1)"; then
        echo "Expected wrapper to block: $label"
        echo "$output"
        exit 1
    fi
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected message not found for: $label"
        echo "Expected: $expected"
        echo "$output"
        exit 1
    fi
}

expect_blocked "default rejects config_yaml" "default" "with-config" "source.config_yaml"
expect_blocked "latest-release requires archive_url" "latest-release" "without-config" "source.archive_url"
expect_blocked "build-from-source requires config_yaml" "build-from-source" "without-config" "missing source.config_yaml"
expect_blocked "review-gated optional fields blocked" "default" "without-config" "review-gated optional field" 'sample_text: "Custom sample"'

write_metadata "with-archive" "" "https://github.com/eliheuer/virtua-grotesk" "0123456789abcdef0123456789abcdef01234567" "Eli Heuer" "fonts/variable/VirtuaGrotesk[wght].ttf" "Arab" "https://github.com/eliheuer/virtua-grotesk"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" GFT_PACKAGER_SOURCE_MODE="latest-release" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block non-release archive_url"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"release download URL ending in .zip"* ]]; then
    echo "Expected release download archive_url message not found"
    echo "$output"
    exit 1
fi

write_metadata "with-archive" "" "https://github.com/eliheuer/virtua-grotesk" "0123456789abcdef0123456789abcdef01234567" "Eli Heuer" "fonts/variable/VirtuaGrotesk[wght].ttf" "Arab" "https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/virtua-grotesk.txt"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" GFT_PACKAGER_SOURCE_MODE="latest-release" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block non-zip archive_url"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"release download URL ending in .zip"* ]]; then
    echo "Expected zip archive_url message not found"
    echo "$output"
    exit 1
fi

write_metadata "without-config" "" "https://github.com/fontgarden/virtua-grotesk"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block stale placeholder upstream URL"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"stale placeholder upstream URL"* ]]; then
    echo "Expected stale placeholder message not found"
    echo "$output"
    exit 1
fi

write_metadata "without-config" "" "https://github.com/eliheuer/virtua-grotesk" "Pending final release/source commit"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block unresolved metadata"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"unresolved metadata"* ]]; then
    echo "Expected unresolved metadata message not found"
    echo "$output"
    exit 1
fi

write_metadata "without-config"
"$PYTHON_BIN" - "$PACKAGE_DIR/METADATA.pb" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
path.write_text(text.replace('date_added: "2026-05-23"', 'date_added: "2026-02-31"'))
PY
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block invalid date_added"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"final valid date_added"* ]]; then
    echo "Expected final date_added message not found"
    echo "$output"
    exit 1
fi

write_metadata "without-config" "" "https://github.com/eliheuer/virtua-grotesk" "0123456789ABCDEF0123456789ABCDEF01234567"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block uppercase source.commit"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"lowercase 40-character source.commit hash"* ]]; then
    echo "Expected lowercase source.commit message not found"
    echo "$output"
    exit 1
fi

write_metadata "without-config" "" "https://github.com/user/repo"
if output="$(cd "$ROOT" && env -u GH_TOKEN GF_REPO_PATH="$GF_REPO" ./scripts/package_gf_dry_run.sh 2>&1)"; then
    echo "Expected wrapper to block starter repository_url"
    echo "$output"
    exit 1
fi
if [[ "$output" != *"Packager starter template"* ]]; then
    echo "Expected starter template message not found"
    echo "$output"
    exit 1
fi

echo "Package dry-run metadata gate tests passed."
