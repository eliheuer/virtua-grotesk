#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/venv/bin/python}"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-metadata-helper.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

GF_REPO="$TMPDIR/fonts"
PACKAGE_DIR="$GF_REPO/ofl/virtuagrotesk"
PREVIEW="$TMPDIR/preview.md"

git init -q -b main "$GF_REPO"
git -C "$GF_REPO" remote add origin git@github.com:eliheuer/fonts.git
git -C "$GF_REPO" remote add upstream https://github.com/google/fonts.git
mkdir -p "$PACKAGE_DIR"
git -C "$GF_REPO" -c user.name="Virtua Test" -c user.email="virtua-test@example.com" commit --allow-empty -q -m "initial"
git -C "$GF_REPO" update-ref refs/remotes/origin/main HEAD
git -C "$GF_REPO" update-ref refs/remotes/upstream/main HEAD

write_preview() {
    local date_added="${1:-2026-05-23}"
    local commit_value="${2:-0123456789abcdef0123456789abcdef01234567}"
    local archive_url="${3:-https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip}"

    cat >"$PREVIEW" <<EOF
# Test Preview

## Expected METADATA.pb shape

\`\`\`text
name: "Virtua Grotesk"
designer: "Eli Heuer"
license: "OFL"
category: "SANS_SERIF"
date_added: "$date_added"
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
  repository_url: "https://github.com/eliheuer/virtua-grotesk"
  commit: "$commit_value"
  archive_url: "$archive_url"
  files {
    source_file: "OFL.txt"
    dest_file: "OFL.txt"
  }
  files {
    source_file: "fonts/variable/VirtuaGrotesk[wght].ttf"
    dest_file: "VirtuaGrotesk[wght].ttf"
  }
  files {
    source_file: "documentation/ARTICLE.en_us.html"
    dest_file: "article/ARTICLE.en_us.html"
  }
  files {
    source_file: "documentation/readme-specimen.png"
    dest_file: "article/readme-specimen.png"
  }
  branch: "main"
}
primary_script: "Arab"
stroke: "SANS_SERIF"
\`\`\`
EOF
}

expect_ready() {
    local output
    write_preview
    output="$("$PYTHON_BIN" "$ROOT/scripts/prepare_downstream_metadata.py" --preview "$PREVIEW" --gf-repo "$GF_REPO" --source-mode latest-release)"
    if [[ "$output" != *"Ready to apply: yes"* ]]; then
        echo "Expected downstream metadata helper to be ready"
        echo "$output"
        exit 1
    fi
}

expect_blocked() {
    local label="$1"
    local expected="$2"
    local output

    output="$("$PYTHON_BIN" "$ROOT/scripts/prepare_downstream_metadata.py" --preview "$PREVIEW" --gf-repo "$GF_REPO" --source-mode latest-release)"
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected blocker not found for: $label"
        echo "Expected: $expected"
        echo "$output"
        exit 1
    fi
}

expect_ready

write_preview "2026-02-31"
expect_blocked "invalid date_added" 'date_added with final valid "YYYY-MM-DD" Google Fonts date'

write_preview "2026-05-23" "0123456789abcdef"
expect_blocked "short source commit" "source.commit with final 40-character lowercase git hash"

write_preview "2026-05-23" "0123456789ABCDEF0123456789ABCDEF01234567"
expect_blocked "uppercase source commit" "source.commit with final 40-character lowercase git hash"

write_preview "2026-05-23" "0123456789abcdef0123456789abcdef01234567" "https://github.com/eliheuer/virtua-grotesk"
expect_blocked "non-release archive_url" "source.archive_url for latest-release mode must be a GitHub release download URL ending in .zip"

write_preview "2026-05-23" "0123456789abcdef0123456789abcdef01234567" "https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.txt"
expect_blocked "non-zip archive_url" "source.archive_url for latest-release mode must be a GitHub release download URL ending in .zip"

echo "Downstream metadata helper tests passed."
