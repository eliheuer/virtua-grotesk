#!/usr/bin/env python3
"""Safely update one row in the Arabic visual review log."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "documentation/arabic-visual-review-log.md"
ALLOWED_STATUSES = ("pending", "pass", "fix-needed", "deferred")
SUMMARY_LABELS = {
    "pending": "Pending",
    "pass": "Pass",
    "fix-needed": "Fix-needed",
    "deferred": "Deferred",
}


@dataclass(frozen=True)
class ReviewRow:
    key: str
    area: str
    item: str
    evidence: str
    machine_precheck: str
    cue: str
    status: str
    reviewer: str
    notes: str


def clean_table_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        value = value[1:-1]
    return value.replace("\\|", "|")


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


def row_from_line(line: str) -> ReviewRow | None:
    if not line.startswith("| `"):
        return None
    cells = split_markdown_row(line)
    if len(cells) < 8:
        return None
    if len(cells) >= 9:
        machine_precheck = clean_table_cell(cells[4])
        cue = clean_table_cell(cells[5])
        status = clean_table_cell(cells[6]) or "pending"
        reviewer = clean_table_cell(cells[7])
        notes = clean_table_cell(cells[8])
    else:
        machine_precheck = ""
        cue = clean_table_cell(cells[4])
        status = clean_table_cell(cells[5]) or "pending"
        reviewer = clean_table_cell(cells[6])
        notes = clean_table_cell(cells[7])
    return ReviewRow(
        key=clean_table_cell(cells[0]),
        area=clean_table_cell(cells[1]),
        item=clean_table_cell(cells[2]),
        evidence=clean_table_cell(cells[3]),
        machine_precheck=machine_precheck,
        cue=cue,
        status=status,
        reviewer=reviewer,
        notes=notes,
    )


def line_from_row(row: ReviewRow) -> str:
    return (
        "| "
        + " | ".join(
            [
                f"`{row.key}`",
                escape_table_cell(row.area),
                escape_table_cell(row.item),
                escape_table_cell(row.evidence),
                escape_table_cell(row.machine_precheck),
                escape_table_cell(row.cue),
                escape_table_cell(row.status),
                escape_table_cell(row.reviewer),
                escape_table_cell(row.notes),
            ]
        )
        + " |"
    )


def update_summary_counts(text: str, rows: list[ReviewRow]) -> str:
    counts = {status: 0 for status in ALLOWED_STATUSES}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    ready = counts["pending"] == 0 and counts["fix-needed"] == 0

    updated = re.sub(
        r"^- Visual review ready: (yes|no)$",
        f"- Visual review ready: {'yes' if ready else 'no'}",
        text,
        flags=re.MULTILINE,
    )
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
    key: str,
    status: str,
    reviewer: str | None,
    notes: str | None,
) -> tuple[str, ReviewRow, ReviewRow]:
    rows: list[ReviewRow] = []
    before: ReviewRow | None = None
    after: ReviewRow | None = None
    output_lines: list[str] = []

    for line in text.splitlines():
        row = row_from_line(line)
        if row is None:
            output_lines.append(line)
            continue
        if row.key == key:
            before = row
            row = ReviewRow(
                key=row.key,
                area=row.area,
                item=row.item,
                evidence=row.evidence,
                machine_precheck=row.machine_precheck,
                cue=row.cue,
                status=status,
                reviewer=reviewer if reviewer is not None else row.reviewer,
                notes=notes if notes is not None else row.notes,
            )
            after = row
            output_lines.append(line_from_row(row))
        else:
            output_lines.append(line)
        rows.append(row)

    if before is None or after is None:
        known_keys = ", ".join(row.key for row in rows[:8])
        raise ValueError(
            f"review key `{key}` was not found in the Arabic visual review log"
            + (f"; first known keys: {known_keys}" if known_keys else "")
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
    parser.add_argument("review_key", help="Review row key, for example proof-regular-glyphs")
    parser.add_argument("--status", required=True, choices=ALLOWED_STATUSES)
    parser.add_argument("--reviewer", help="Reviewer/date marker for the Reviewer cell")
    parser.add_argument("--notes", help="Optional review notes")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--apply", action="store_true", help="Write the update; otherwise dry-run only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    log_path = args.log
    if not log_path.exists():
        print(f"ERR Arabic visual review log not found: {log_path}", file=sys.stderr)
        return 1

    try:
        updated, before, after = update_log(
            log_path.read_text(encoding="utf-8"),
            args.review_key,
            args.status,
            args.reviewer,
            args.notes,
        )
    except ValueError as error:
        print(f"ERR {error}", file=sys.stderr)
        return 1

    print(f"{before.key}: {before.status} -> {after.status}")
    if before.reviewer != after.reviewer:
        print(f"Reviewer: {before.reviewer!r} -> {after.reviewer!r}")
    if before.notes != after.notes:
        print(f"Notes: {before.notes!r} -> {after.notes!r}")

    if args.apply:
        log_path.write_text(updated, encoding="utf-8")
        print(f"Wrote {display_path(log_path)}")
    else:
        print("Dry run only. Re-run with --apply to write the visual review log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
