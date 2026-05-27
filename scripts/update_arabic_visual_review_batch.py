#!/usr/bin/env python3
"""Safely update Arabic visual review rows from a TSV file."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import sys

from update_arabic_visual_review import (
    ALLOWED_STATUSES,
    DEFAULT_LOG,
    ROOT,
    ReviewRow,
    display_path,
    update_log,
)


REQUIRED_COLUMNS = ("key", "status", "reviewer", "notes")


@dataclass(frozen=True)
class BatchRow:
    line_number: int
    key: str
    status: str
    reviewer: str
    notes: str


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "tsv",
        type=Path,
        help="TSV with columns: key, status, reviewer, notes",
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--apply", action="store_true", help="Write the update; otherwise dry-run only")
    return parser


def read_batch(path: Path) -> list[BatchRow]:
    if not path.exists():
        raise ValueError(f"batch TSV not found: {path}")

    rows: list[BatchRow] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError("batch TSV is empty")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"batch TSV missing columns: {', '.join(missing)}")

        for line_number, row in enumerate(reader, start=2):
            key = (row.get("key") or "").strip()
            status = (row.get("status") or "").strip()
            reviewer = (row.get("reviewer") or "").strip()
            notes = (row.get("notes") or "").strip()
            if not any([key, status, reviewer, notes]):
                continue
            if not key:
                raise ValueError(f"line {line_number}: key is required")
            if status not in ALLOWED_STATUSES:
                raise ValueError(
                    f"line {line_number}: status must be one of {', '.join(ALLOWED_STATUSES)}"
                )
            rows.append(
                BatchRow(
                    line_number=line_number,
                    key=key,
                    status=status,
                    reviewer=reviewer,
                    notes=notes,
                )
            )

    if not rows:
        raise ValueError("batch TSV has no review rows")
    return rows


def apply_batch(text: str, rows: list[BatchRow]) -> tuple[str, list[tuple[ReviewRow, ReviewRow]]]:
    updates: list[tuple[ReviewRow, ReviewRow]] = []
    updated = text
    seen: set[str] = set()
    for row in rows:
        if row.key in seen:
            raise ValueError(f"line {row.line_number}: duplicate key `{row.key}`")
        seen.add(row.key)
        updated, before, after = update_log(
            updated,
            row.key,
            row.status,
            row.reviewer,
            row.notes,
        )
        updates.append((before, after))
    return updated, updates


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    log_path = args.log
    if not log_path.exists():
        print(f"ERR Arabic visual review log not found: {log_path}", file=sys.stderr)
        return 1

    try:
        rows = read_batch(args.tsv)
        updated, updates = apply_batch(log_path.read_text(encoding="utf-8"), rows)
    except ValueError as error:
        print(f"ERR {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(updates)} visual review update(s).")
    for before, after in updates:
        print(f"{before.key}: {before.status} -> {after.status}")
        if before.reviewer != after.reviewer:
            print(f"  Reviewer: {before.reviewer!r} -> {after.reviewer!r}")
        if before.notes != after.notes:
            print(f"  Notes: {before.notes!r} -> {after.notes!r}")

    if args.apply:
        log_path.write_text(updated, encoding="utf-8")
        print(f"Wrote {display_path(log_path)}")
    else:
        print("Dry run only. Re-run with --apply to write the visual review log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
