#!/usr/bin/env python3
"""Generate a compact Arabic hand-review session checklist."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from report_arabic_visual_review_runbook import (
    ROOT,
    command,
    evidence_lines,
    machine_precheck_lines,
    row_priority,
    visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-hand-review-session.md"
EDIT_TARGETS = ROOT / "documentation/glyph-review/arabic-manual-edit-targets.md"
BOARD = ROOT / "documentation/glyph-review/arabic-next-review-board.html"
LOG = ROOT / "documentation/glyph-review/arabic-visual-review-log.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/glyph-review/arabic-print-proof-index.md"

SESSION_GROUPS = [
    (
        "Glyph Proof First Pass",
        (
            "proof-regular-glyphs",
            "proof-medium-glyphs",
            "proof-semibold-glyphs",
            "proof-bold-glyphs",
            "class-letter-structures",
        ),
    ),
    (
        "Marks And Dotted Circle",
        (
            "mark-base+fatha",
            "mark-base+damma",
            "mark-base+kasra",
            "mark-shadda+sukun",
            "mark-tanween",
            "mark-hamza-above-below",
            "mark-dotted-circle",
            "class-mark-combinations",
            "class-dot-stack-helpers",
        ),
    ),
    (
        "Proof Texture And Spacing",
        (
            "proof-regular-text",
            "proof-regular-proofer",
            "proof-regular-waterfall",
            "proof-medium-text",
            "proof-medium-proofer",
            "proof-medium-waterfall",
            "proof-semibold-text",
            "proof-semibold-proofer",
            "proof-semibold-waterfall",
            "proof-bold-text",
            "proof-bold-proofer",
            "proof-bold-waterfall",
        ),
    ),
    (
        "Smoke Strings And Classes",
        (
            "smoke-salaam",
            "smoke-arabic",
            "smoke-bismillah",
            "smoke-lam-alef",
            "class-arabic-farsi-numerals",
            "class-arabic-punctuation",
        ),
    ),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_edit_targets(text: str) -> dict[str, dict[str, object]]:
    targets: dict[str, dict[str, object]] = {}
    current_key = ""
    for line in text.splitlines():
        match = re.match(r"^### `([^`]+)`", line)
        if match:
            current_key = match.group(1)
            targets[current_key] = {"summary": "", "paths": []}
            continue
        if line.startswith("### "):
            current_key = ""
            continue
        if not current_key:
            continue
        if line.startswith("- Source targets:"):
            targets[current_key]["summary"] = line.removeprefix("- ").strip()
            continue
        path_match = re.search(r"`(sources/[^`]+\.glif)`", line)
        if path_match:
            paths = targets[current_key]["paths"]
            assert isinstance(paths, list)
            paths.append(path_match.group(1))
    return targets


def row_target_lines(key: str, edit_targets: dict[str, dict[str, object]]) -> list[str]:
    target = edit_targets.get(key, {})
    summary = str(target.get("summary", "Source targets: not generated for this row"))
    paths = target.get("paths", [])
    if not isinstance(paths, list):
        paths = []
    lines = [f"- Edit targets: {summary}"]
    for path in paths[:4]:
        lines.append(f"  - `{path}`")
    if len(paths) > 4:
        lines.append(f"  - Additional GLIF targets in `{display_path(EDIT_TARGETS)}`: {len(paths) - 4}")
    elif not paths:
        lines.append("  - Record exact glyph names in the review log if this row becomes `fix-needed`.")
    return lines


def row_block(row, edit_targets: dict[str, dict[str, object]]) -> list[str]:
    lines = [
        f"### `{row.key}`",
        "",
        f"- Area/item: {row.area} / {row.item}",
        f"- Status: `{row.status}`",
        f"- Review cue: {row.cue}",
    ]
    lines.extend(evidence_lines(row))
    lines.extend(machine_precheck_lines(row))
    lines.extend(row_target_lines(row.key, edit_targets))
    lines.extend(
        [
            "",
            "```bash",
            command(row, "pass", "reviewed current proof"),
            command(row, "fix-needed", "specific glyph or proof issue"),
            command(row, "deferred", "needs Arabic native-reader review"),
            "```",
            "",
        ]
    )
    return lines


def report() -> str:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    rows = sorted(rows, key=row_priority)
    edit_targets = parse_edit_targets(read_text(EDIT_TARGETS))
    pending = sum(1 for row in rows if row.status == "pending")
    fix_needed = sum(1 for row in rows if row.status == "fix-needed")
    deferred = sum(1 for row in rows if row.status == "deferred")
    lines = [
        "# Arabic Hand Review Session",
        "",
        "This generated sheet is the compact execution view for the remaining",
        "human Arabic visual review. Use it with the local review board and",
        "proof HTML; it is not a substitute for human proof/source inspection.",
        "",
        "## Summary",
        "",
        f"- Pending/fix-needed rows in this sheet: {len(rows)}",
        f"- Pending: {pending}",
        f"- Fix-needed: {fix_needed}",
        f"- Deferred in active queue: {deferred}",
        f"- Review log: `{display_path(LOG)}`",
        f"- Local review board: `{display_path(BOARD)}`",
        f"- Arabic PDF proof: `{display_path(ARABIC_PRINT_PROOF)}`",
        f"- Arabic PDF proof index: `{display_path(ARABIC_PRINT_PROOF_INDEX)}`",
        f"- Full edit-target report: `{display_path(EDIT_TARGETS)}`",
        "",
        "## Rules",
        "",
        "- Review the proof HTML or source glyphs before recording `pass`.",
        "- Record `fix-needed` only with exact glyph names, proof locations, or source files.",
        "- Edit Regular and Bold together, preserving compatible glyph structure.",
        "- After any edit batch, run `./build.sh`, `make reports-only`, and `make preflight-only`.",
        "",
    ]
    for group_name, keys in SESSION_GROUPS:
        group_rows = [row for row in rows if row.key in keys]
        if not group_rows:
            continue
        lines.extend([f"## {group_name}", ""])
        for row in group_rows:
            lines.extend(row_block(row, edit_targets))
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report(), encoding="utf-8")
    print(display_path(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
