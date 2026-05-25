#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/venv/bin/python}"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-arabic-visual-review.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

LOG="$TMPDIR/arabic-visual-review-log.md"

"$PYTHON_BIN" "$ROOT/scripts/report_arabic_visual_review_log.py" "$LOG"

expect_contains() {
    local label="$1"
    local expected="$2"
    local file="$3"
    if ! grep -Fq -- "$expected" "$file"; then
        echo "Expected text not found for: $label"
        echo "Expected: $expected"
        cat "$file"
        exit 1
    fi
}

expect_contains "initial pending count" "- Pending: 32" "$LOG"
expect_contains "initial pass count" "- Pass: 0" "$LOG"
expect_contains "initial ready state" "- Visual review ready: no" "$LOG"
expect_contains "machine precheck header" "| Key | Area | Item | Evidence | Machine precheck | Review cue | Status | Reviewer | Notes |" "$LOG"
expect_contains "structure precheck" "Structure triage mechanical blockers: 0; structure review prompts: 35" "$LOG"

before="$(cat "$LOG")"
"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review.py" proof-regular-glyphs --status pass --reviewer "Test 2026-05-25" --notes "dry run only" --log "$LOG" >/dev/null
after="$(cat "$LOG")"
if [[ "$before" != "$after" ]]; then
    echo "Dry run unexpectedly changed the visual review log"
    exit 1
fi

"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review.py" proof-regular-glyphs --status pass --reviewer "Test 2026-05-25" --notes "reviewed glyph proof" --log "$LOG" --apply >/dev/null
expect_contains "applied pending count" "- Pending: 31" "$LOG"
expect_contains "applied pass count" "- Pass: 1" "$LOG"
expect_contains "applied row" '| `proof-regular-glyphs` | GF proof | Regular glyphs | `documentation/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html` | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | pass | Test 2026-05-25 | reviewed glyph proof |' "$LOG"

"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review.py" proof-regular-glyphs --status pending --reviewer "" --notes "" --log "$LOG" --apply >/dev/null
expect_contains "restored pending count" "- Pending: 32" "$LOG"
expect_contains "restored pass count" "- Pass: 0" "$LOG"

if "$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review.py" missing-key --status pass --log "$LOG" >/tmp/virtua-arabic-visual-review-test.out 2>&1; then
    echo "Expected missing visual review key to fail"
    cat /tmp/virtua-arabic-visual-review-test.out
    exit 1
fi
if ! grep -Fq "review key \`missing-key\` was not found" /tmp/virtua-arabic-visual-review-test.out; then
    echo "Expected missing-key error message not found"
    cat /tmp/virtua-arabic-visual-review-test.out
    exit 1
fi

echo "Arabic visual review update helper tests passed."
