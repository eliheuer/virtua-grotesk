#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-release-archive-gates.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

PYTHON="$ROOT/venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="python3"
fi

write_preview() {
    local path="$1"
    shift
    {
        printf '# Test package preview\n\n'
        for source_file in "$@"; do
            printf '  files {\n'
            printf '    source_file: "%s"\n' "$source_file"
            printf '    dest_file: "%s"\n' "$(basename "$source_file")"
            printf '  }\n'
        done
    } >"$path"
}

write_preview_pair() {
    local path="$1"
    local source_file="$2"
    local dest_file="$3"
    {
        printf '# Test package preview\n\n'
        printf '  files {\n'
        printf '    source_file: "%s"\n' "$source_file"
        printf '    dest_file: "%s"\n' "$dest_file"
        printf '  }\n'
    } >"$path"
}

expect_blocked() {
    local label="$1"
    local expected="$2"
    shift 2
    local output

    if output="$("$@" 2>&1)"; then
        echo "Expected release archive gate to block: $label"
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

SAFE_PREVIEW="$TMPDIR/safe.md"
EMPTY_PREVIEW="$TMPDIR/empty.md"
UNSAFE_PREVIEW="$TMPDIR/unsafe.md"
DUPLICATE_PREVIEW="$TMPDIR/duplicate.md"
UNSAFE_DEST_PREVIEW="$TMPDIR/unsafe-dest.md"
DUPLICATE_DEST_PREVIEW="$TMPDIR/duplicate-dest.md"
SAFE_ARCHIVE="$TMPDIR/safe.zip"
UNSAFE_ARCHIVE="$TMPDIR/unsafe.zip"
NONDETERMINISTIC_ARCHIVE="$TMPDIR/nondeterministic.zip"

write_preview "$SAFE_PREVIEW" "OFL.txt" "documentation/ARTICLE.en_us.html"
printf '# Empty package preview\n' >"$EMPTY_PREVIEW"
write_preview "$UNSAFE_PREVIEW" "../evil.txt"
write_preview "$DUPLICATE_PREVIEW" "OFL.txt" "OFL.txt"
write_preview_pair "$UNSAFE_DEST_PREVIEW" "OFL.txt" "../evil.txt"
{
    printf '# Test package preview\n\n'
    printf '  files {\n'
    printf '    source_file: "OFL.txt"\n'
    printf '    dest_file: "duplicate.txt"\n'
    printf '  }\n'
    printf '  files {\n'
    printf '    source_file: "documentation/ARTICLE.en_us.html"\n'
    printf '    dest_file: "duplicate.txt"\n'
    printf '  }\n'
} >"$DUPLICATE_DEST_PREVIEW"

(cd "$ROOT" && "$PYTHON" scripts/build_release_archive.py --preview "$SAFE_PREVIEW" --output "$SAFE_ARCHIVE") >/dev/null
(cd "$ROOT" && "$PYTHON" scripts/verify_release_archive.py --preview "$SAFE_PREVIEW" --archive "$SAFE_ARCHIVE" --quiet)
(cd "$ROOT" && "$PYTHON" scripts/verify_release_archive.py --preview "$SAFE_PREVIEW" --archive "$SAFE_ARCHIVE" --expected-sha256 "$("$PYTHON" - "$SAFE_ARCHIVE" <<'PY'
import hashlib
import sys

print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())
PY
)" --quiet)

expect_blocked \
    "builder rejects missing source_file entries" \
    "no source.files entries found" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --preview "$EMPTY_PREVIEW" --output "$TMPDIR/out.zip"

expect_blocked \
    "builder rejects unsafe source_file paths" \
    "unsafe paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --preview "$UNSAFE_PREVIEW" --output "$TMPDIR/out.zip"

expect_blocked \
    "builder rejects duplicate source_file paths" \
    "duplicate source_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --preview "$DUPLICATE_PREVIEW" --output "$TMPDIR/out.zip"

expect_blocked \
    "builder rejects unsafe dest_file paths" \
    "unsafe dest_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --preview "$UNSAFE_DEST_PREVIEW" --output "$TMPDIR/out.zip"

expect_blocked \
    "builder rejects duplicate dest_file paths" \
    "duplicate dest_file paths" \
    "$PYTHON" "$ROOT/scripts/build_release_archive.py" --preview "$DUPLICATE_DEST_PREVIEW" --output "$TMPDIR/out.zip"

expect_blocked \
    "verifier rejects missing source_file entries" \
    "no source.files entries found" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$EMPTY_PREVIEW" --archive "$SAFE_ARCHIVE"

expect_blocked \
    "verifier rejects unsafe source_file paths" \
    "unsafe source.files path" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$UNSAFE_PREVIEW" --archive "$SAFE_ARCHIVE"

expect_blocked \
    "verifier rejects duplicate source_file paths" \
    "duplicate source.files path" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$DUPLICATE_PREVIEW" --archive "$SAFE_ARCHIVE"

expect_blocked \
    "verifier rejects unsafe dest_file paths" \
    "unsafe source.files dest_file path" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$UNSAFE_DEST_PREVIEW" --archive "$SAFE_ARCHIVE"

expect_blocked \
    "verifier rejects duplicate dest_file paths" \
    "duplicate source.files dest_file path" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$DUPLICATE_DEST_PREVIEW" --archive "$SAFE_ARCHIVE"

"$PYTHON" -c 'import sys, zipfile; z = zipfile.ZipFile(sys.argv[1], "w"); z.writestr("../evil.txt", "bad"); z.close()' "$UNSAFE_ARCHIVE"

expect_blocked \
    "verifier rejects unsafe archive entries" \
    "archive contains unsafe path" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$SAFE_PREVIEW" --archive "$UNSAFE_ARCHIVE"

"$PYTHON" -c 'import sys, zipfile; z = zipfile.ZipFile(sys.argv[1], "w"); z.write(sys.argv[2], arcname="OFL.txt"); z.write(sys.argv[3], arcname="documentation/ARTICLE.en_us.html"); z.close()' "$NONDETERMINISTIC_ARCHIVE" "$ROOT/OFL.txt" "$ROOT/documentation/ARTICLE.en_us.html"

expect_blocked \
    "verifier rejects nondeterministic archive metadata" \
    "nondeterministic timestamp" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$SAFE_PREVIEW" --archive "$NONDETERMINISTIC_ARCHIVE"

expect_blocked \
    "verifier rejects whole-archive SHA mismatch" \
    "archive SHA-256 mismatch" \
    "$PYTHON" "$ROOT/scripts/verify_release_archive.py" --preview "$SAFE_PREVIEW" --archive "$SAFE_ARCHIVE" --expected-sha256 "0000000000000000000000000000000000000000000000000000000000000000"

echo "Release archive path-safety gate tests passed."
