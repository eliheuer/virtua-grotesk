#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/venv/bin/python}"
TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-contour-decision.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

REPORT="$TMPDIR/fontspector-contour-count.md"
PROOF="$TMPDIR/contour-cleanup-proof.html"
LOG="$TMPDIR/contour-cleanup-proof-decision-log.md"
OUT="$TMPDIR/out.txt"

cat >"$REPORT" <<'REPORT'
# Fontspector Contour Count Findings

Synthetic fixture used by scripts/test_contour_decision_update.sh so this
helper remains tested even when the live contour-count report is empty.

## `fonts/ttf/VirtuaGrotesk-Regular.ttf`

### WARN: `contour_count`

| Glyph | Codepoint | Actual contours | Expected contours |
| --- | --- | --- | --- |
| `uni0647.init` | U+0647 | 3 | 2 |
REPORT
"$PYTHON_BIN" "$ROOT/scripts/build_contour_cleanup_proof.py" "$REPORT" "$PROOF" >/dev/null

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

expect_contains "initial pending count" "- Pending: 1" "$LOG"
expect_contains "initial fix-now count" "- Fix-now: 0" "$LOG"
expect_contains "initial accepted count" "- Accepted: 0" "$LOG"

before="$(cat "$LOG")"
"$PYTHON_BIN" "$ROOT/scripts/update_contour_decision.py" heh-ar.init --status fix-now --decision "dry run only" --notes "do not persist" --reviewed "Test 2026-05-25" --log "$LOG" >/dev/null
after="$(cat "$LOG")"
if [[ "$before" != "$after" ]]; then
    echo "Dry run unexpectedly changed the contour decision log"
    exit 1
fi

"$PYTHON_BIN" "$ROOT/scripts/update_contour_decision.py" heh-ar.init --status fix-now --decision "redraw with mirrored masters" --notes "test update" --reviewed "Test 2026-05-25" --log "$LOG" --apply >/dev/null
expect_contains "applied pending count" "- Pending: 0" "$LOG"
expect_contains "applied fix-now count" "- Fix-now: 1" "$LOG"
expect_contains "applied row" '| `heh-ar.init` | `uni0647.init` | 4. Arabic letterform review | Arabic letter or positional form | `/edit-glyph heh-ar.init --master both` | fix-now | redraw with mirrored masters | test update | Test 2026-05-25 |' "$LOG"

"$PYTHON_BIN" "$ROOT/scripts/update_contour_decision.py" heh-ar.init --status pending --decision "pending" --notes "" --reviewed "" --log "$LOG" --apply >/dev/null
expect_contains "restored pending count" "- Pending: 1" "$LOG"
expect_contains "restored fix-now count" "- Fix-now: 0" "$LOG"

if "$PYTHON_BIN" "$ROOT/scripts/update_contour_decision.py" missing-glyph --status accepted --log "$LOG" >"$OUT" 2>&1; then
    echo "Expected missing contour decision source glyph to fail"
    cat "$OUT"
    exit 1
fi
expect_contains "missing glyph error" "source glyph \`missing-glyph\` was not found" "$OUT"

echo "Contour decision update helper tests passed."
