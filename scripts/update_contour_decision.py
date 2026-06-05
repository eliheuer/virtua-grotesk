#!/usr/bin/env python3
"""Safely update one row in the contour cleanup decision log."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md"
ALLOWED_STATUSES = ("pending", "fix-now", "fixed", "accepted", "deferred")
SUMMARY_LABELS = {
    "pending": "Pending",
    "fix-now": "Fix-now",
    "fixed": "Fixed",
    "accepted": "Accepted",
    "deferred": "Deferred",
}


@dataclass(frozen=True)
class DecisionRow:
    source: str
    fontspector_glyph: str
    batch: str
    category: str
    command: str
    status: str
    decision: str
    notes: str
    reviewed: str


def clean_table_cell(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|")


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def split_markdown_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in line.strip().strip("|"):
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\":
            current.append(character)
            escaped = True
            continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    cells.append("".join(current).strip())
    return cells


def row_from_line(line: str) -> DecisionRow | None:
    if not line.startswith("| `"):
        return None
    cells = split_markdown_row(line)
    if len(cells) < 9:
        return None
    return DecisionRow(
        source=clean_table_cell(cells[0]),
        fontspector_glyph=clean_table_cell(cells[1]),
        batch=clean_table_cell(cells[2]),
        category=clean_table_cell(cells[3]),
        command=clean_table_cell(cells[4]),
        status=clean_table_cell(cells[5]) or "pending",
        decision=clean_table_cell(cells[6]) or "pending",
        notes=clean_table_cell(cells[7]),
        reviewed=clean_table_cell(cells[8]),
    )


def line_from_row(row: DecisionRow) -> str:
    return (
        "| "
        + " | ".join(
            [
                f"`{row.source}`",
                f"`{row.fontspector_glyph}`",
                escape_table_cell(row.batch),
                escape_table_cell(row.category),
                f"`{row.command}`",
                escape_table_cell(row.status),
                escape_table_cell(row.decision),
                escape_table_cell(row.notes),
                escape_table_cell(row.reviewed),
            ]
        )
        + " |"
    )


def update_summary_counts(text: str, rows: list[DecisionRow]) -> str:
    counts = {status: 0 for status in ALLOWED_STATUSES}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    updated = text
    for status, label in SUMMARY_LABELS.items():
        updated = re.sub(
            rf"^- {re.escape(label)}: \d+$",
            f"- {label}: {counts[status]}",
            updated,
            flags=re.MULTILINE,
        )
    return updated


def update_log(
    text: str,
    source: str,
    status: str,
    decision: str | None,
    notes: str | None,
    reviewed: str | None,
) -> tuple[str, DecisionRow, DecisionRow]:
    rows: list[DecisionRow] = []
    before: DecisionRow | None = None
    after: DecisionRow | None = None
    output_lines: list[str] = []

    for line in text.splitlines():
        row = row_from_line(line)
        if row is None:
            output_lines.append(line)
            continue
        if row.source == source:
            before = row
            row = DecisionRow(
                source=row.source,
                fontspector_glyph=row.fontspector_glyph,
                batch=row.batch,
                category=row.category,
                command=row.command,
                status=status,
                decision=decision if decision is not None else row.decision,
                notes=notes if notes is not None else row.notes,
                reviewed=reviewed if reviewed is not None else row.reviewed,
            )
            after = row
            output_lines.append(line_from_row(row))
        else:
            output_lines.append(line)
        rows.append(row)

    if before is None or after is None:
        known_sources = ", ".join(row.source for row in rows[:8])
        raise ValueError(
            f"source glyph `{source}` was not found in the decision log"
            + (f"; first known sources: {known_sources}" if known_sources else "")
        )

    updated_text = update_summary_counts("\n".join(output_lines) + "\n", rows)
    return updated_text, before, after


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_glyph", help="Source glyph name, for example dad-ar.fina")
    parser.add_argument("--status", required=True, choices=ALLOWED_STATUSES)
    parser.add_argument("--decision", help="Short review decision to store in the Decision cell")
    parser.add_argument("--notes", help="Optional notes for the Notes cell")
    parser.add_argument("--reviewed", help="Reviewer/date marker for the Reviewed cell")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--apply", action="store_true", help="Write the update; otherwise dry-run only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    log_path = args.log
    if not log_path.exists():
        print(f"ERR decision log not found: {log_path}", file=sys.stderr)
        return 1

    try:
        updated, before, after = update_log(
            log_path.read_text(),
            args.source_glyph,
            args.status,
            args.decision,
            args.notes,
            args.reviewed,
        )
    except ValueError as error:
        print(f"ERR {error}", file=sys.stderr)
        return 1

    print(f"{before.source}: {before.status} -> {after.status}")
    print(f"Decision: {before.decision!r} -> {after.decision!r}")
    if before.notes != after.notes:
        print(f"Notes: {before.notes!r} -> {after.notes!r}")
    if before.reviewed != after.reviewed:
        print(f"Reviewed: {before.reviewed!r} -> {after.reviewed!r}")

    if args.apply:
        log_path.write_text(updated)
        print(f"Wrote {display_path(log_path)}")
    else:
        print("Dry run only. Re-run with --apply to write the decision log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
