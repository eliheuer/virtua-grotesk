#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/.venv/bin/python}"
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
expect_contains "applied row" '| `proof-regular-glyphs` | GF proof | Regular glyphs | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html` | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | pass | Test 2026-05-25 | reviewed glyph proof |' "$LOG"

"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review.py" proof-regular-glyphs --status pending --reviewer "" --notes "" --log "$LOG" --apply >/dev/null
expect_contains "restored pending count" "- Pending: 32" "$LOG"
expect_contains "restored pass count" "- Pass: 0" "$LOG"

BATCH="$TMPDIR/review-batch.tsv"
cat >"$BATCH" <<'TSV'
key	status	reviewer	notes
proof-regular-glyphs	pass	Test 2026-05-25	reviewed regular glyph proof
proof-medium-glyphs	deferred	Test 2026-05-25	needs Arabic reader
TSV

before="$(cat "$LOG")"
"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review_batch.py" "$BATCH" --log "$LOG" >/dev/null
after="$(cat "$LOG")"
if [[ "$before" != "$after" ]]; then
    echo "Batch dry run unexpectedly changed the visual review log"
    exit 1
fi

"$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review_batch.py" "$BATCH" --log "$LOG" --apply >/dev/null
expect_contains "batch pending count" "- Pending: 30" "$LOG"
expect_contains "batch pass count" "- Pass: 1" "$LOG"
expect_contains "batch deferred count" "- Deferred: 1" "$LOG"
expect_contains "batch applied pass row" '| `proof-regular-glyphs` | GF proof | Regular glyphs | `documentation/google-fonts/gftools-qa/Proof/*Regular*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html` | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | pass | Test 2026-05-25 | reviewed regular glyph proof |' "$LOG"
expect_contains "batch applied deferred row" '| `proof-medium-glyphs` | GF proof | Medium glyphs | `documentation/google-fonts/gftools-qa/Proof/*Medium*-diffbrowsers_glyphs.html`; `documentation/glyph-review/arabic-manual-review-dashboard.html` | Structure triage mechanical blockers: 0; structure review prompts: 35 | Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs | deferred | Test 2026-05-25 | needs Arabic reader |' "$LOG"

BAD_BATCH="$TMPDIR/bad-review-batch.tsv"
cat >"$BAD_BATCH" <<'TSV'
key	status	reviewer	notes
proof-bold-glyphs	done	Test 2026-05-25	bad status
TSV
if "$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review_batch.py" "$BAD_BATCH" --log "$LOG" >/tmp/virtua-arabic-visual-review-batch-test.out 2>&1; then
    echo "Expected bad batch visual review status to fail"
    cat /tmp/virtua-arabic-visual-review-batch-test.out
    exit 1
fi
if ! grep -Fq "status must be one of" /tmp/virtua-arabic-visual-review-batch-test.out; then
    echo "Expected bad batch status error message not found"
    cat /tmp/virtua-arabic-visual-review-batch-test.out
    exit 1
fi

DUPLICATE_BATCH="$TMPDIR/duplicate-review-batch.tsv"
cat >"$DUPLICATE_BATCH" <<'TSV'
key	status	reviewer	notes
proof-bold-glyphs	pass	Test 2026-05-25	first review
proof-bold-glyphs	deferred	Test 2026-05-25	duplicate review
TSV
if "$PYTHON_BIN" "$ROOT/scripts/update_arabic_visual_review_batch.py" "$DUPLICATE_BATCH" --log "$LOG" >/tmp/virtua-arabic-visual-review-batch-test.out 2>&1; then
    echo "Expected duplicate batch visual review key to fail"
    cat /tmp/virtua-arabic-visual-review-batch-test.out
    exit 1
fi
if ! grep -Fq 'duplicate key `proof-bold-glyphs`' /tmp/virtua-arabic-visual-review-batch-test.out; then
    echo "Expected duplicate-key error message not found"
    cat /tmp/virtua-arabic-visual-review-batch-test.out
    exit 1
fi

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
