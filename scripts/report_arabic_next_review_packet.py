#!/usr/bin/env python3
"""Generate a compact packet for the next Arabic visual review batch."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_visual_review_runbook import (
    ROOT,
    command,
    evidence_lines,
    machine_precheck_lines,
    mark_prompt_summary_lines,
    needs_mark_prompt_summary,
    needs_structure_prompt_summary,
    review_prompt,
    row_priority,
    structure_prompt_summary_lines,
    visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-next-review-packet.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/glyph-review/arabic-print-proof-index.md"


def compact_bullets(lines: list[str]) -> list[str]:
    return [line for line in lines if line.strip()]


def review_card(index: int, row) -> list[str]:
    lines = [
        f"## {index}. `{row.key}`",
        "",
        f"- Area: {row.area}",
        f"- Item: {row.item}",
        f"- Cue: {row.cue}",
        *compact_bullets(evidence_lines(row)),
        *compact_bullets(machine_precheck_lines(row)),
        "",
        "Record the review result:",
        "",
        "```bash",
        command(row, "pass", "reviewed current proof"),
        command(row, "fix-needed", "specific glyph or proof issue"),
        command(row, "deferred", "needs Arabic native-reader review"),
        "```",
        "",
        "AI comparison prompt:",
        "",
        f"> {review_prompt(row)}",
        "",
    ]
    return lines


def shared_prompt_details(rows: list[object]) -> list[str]:
    lines: list[str] = []
    structure_row = next((row for row in rows if needs_structure_prompt_summary(row)), None)
    if structure_row is not None:
        lines.extend(["## Shared Structure Prompt Details", ""])
        lines.extend(compact_bullets(structure_prompt_summary_lines(structure_row)))
        lines.append("")

    mark_rows = [row for row in rows if needs_mark_prompt_summary(row)]
    if mark_rows:
        lines.extend(["## Shared Mark Prompt Details", ""])
        seen: set[str] = set()
        for row in mark_rows:
            if row.key in seen:
                continue
            seen.add(row.key)
            lines.extend(compact_bullets(mark_prompt_summary_lines(row)))
        lines.append("")
    return lines


def packet() -> str:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    rows = sorted(rows, key=row_priority)
    next_rows = rows[:5]

    lines = [
        "# Arabic Next Review Packet",
        "",
        "This generated packet is the smallest current hand-review batch. It is",
        "derived from `documentation/glyph-review/arabic-visual-review-log.md` and should be",
        "regenerated after recording outcomes.",
        "",
        f"- Pending or fix-needed rows: {len(rows)}",
        "- Full runbook: `documentation/glyph-review/arabic-visual-review-runbook.md`",
        "- Dashboard: `documentation/glyph-review/arabic-manual-review-dashboard.html`",
        "- Focused Arabic PDF proof: `documentation/glyph-review/arabic-print-proof.pdf`",
        "- Focused Arabic PDF index: `documentation/glyph-review/arabic-print-proof-index.md`",
        "- Focused HTML: `documentation/glyph-review/arabic-next-review-batch.html`",
        "- AI-safe triage: run `make arabic-next-review-ai-triage`",
        "- AI visual observations: run `make arabic-next-review-ai-observations`",
        "- Local review board: run `make arabic-next-review-board`",
        "- Optional PNG snapshots: run `make arabic-next-review-snapshots`",
        '- Optional full-queue PNG snapshot probe: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --timeout 20"`',
        '- Optional full-queue snapshot coverage check without Chrome: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --list-only --timeout 20"`',
        '- Optional rebuild from existing PNGs: `make arabic-next-review-snapshots ARABIC_SNAPSHOT_ARGS="--all-pending --limit 32 --reuse-existing"`',
        "",
    ]
    if not next_rows:
        lines.append("No pending or fix-needed review rows remain.")
        lines.append("")
        return "\n".join(lines)

    if ARABIC_PRINT_PROOF.exists():
        lines.extend(
            [
                "## Fast Review Order",
                "",
                "1. Open `documentation/glyph-review/arabic-print-proof.pdf` and scan the current",
                "   five-row batch across Regular, Medium, SemiBold, and Bold.",
                "2. Use `documentation/glyph-review/arabic-print-proof-index.md` to jump directly",
                "   to the style and section you are reviewing.",
                "3. Use the linked HTML/source evidence below for any row that looks",
                "   missing, clipped, malformed, duplicated, wrong-codepoint, or",
                "   stylistically inconsistent.",
                "4. Record one guarded status command per row only after checking the",
                "   evidence. The PDF speeds review; it does not replace source/proof",
                "   inspection for final approval.",
                "",
            ]
        )

    lines.extend(
        [
            "## Next Rows",
            "",
            "| Order | Key | Item | Status |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for index, row in enumerate(next_rows, start=1):
        lines.append(f"| {index} | `{row.key}` | {row.item} | {row.status} |")
    lines.append("")

    lines.extend(shared_prompt_details(next_rows))

    for index, row in enumerate(next_rows, start=1):
        lines.extend(review_card(index, row))

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(packet(), encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
