#!/usr/bin/env python3
"""Copy AI-safe Arabic review observations into blank visual-review notes."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from update_arabic_visual_review import (
    DEFAULT_LOG,
    ROOT,
    row_from_line,
    split_markdown_row,
    update_log,
)


DEFAULT_AI_SWEEP = ROOT / "documentation/glyph-review/arabic-full-queue-ai-sweep.md"


def clean_cell(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|").replace("<br>", " ")


def ai_observations(path: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "## Row Observations":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 4:
            continue
        key = clean_cell(cells[0])
        observation = clean_cell(cells[2])
        follow_up = clean_cell(cells[3])
        rows[key] = (observation, follow_up)
    return rows


def existing_status_and_notes(path: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = row_from_line(line)
        if row is None:
            continue
        rows[row.key] = (row.status, row.notes)
    return rows


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--ai-sweep", type=Path, default=DEFAULT_AI_SWEEP)
    parser.add_argument("--reviewer", default=f"AI screen {date.today().isoformat()}")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing notes instead of filling blanks only")
    parser.add_argument("--apply", action="store_true", help="Write updates; otherwise dry-run only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not args.log.exists():
        print(f"ERR review log not found: {args.log}", file=sys.stderr)
        return 1
    if not args.ai_sweep.exists():
        print(f"ERR AI sweep report not found: {args.ai_sweep}", file=sys.stderr)
        return 1

    observations = ai_observations(args.ai_sweep)
    status_and_notes_by_key = existing_status_and_notes(args.log)
    updated_text = args.log.read_text(encoding="utf-8")
    updated_keys: list[str] = []

    for key, (observation, follow_up) in observations.items():
        current_status, current_note = status_and_notes_by_key.get(key, ("pending", ""))
        if current_note and not args.overwrite:
            continue
        note = f"AI screen: {observation} Human follow-up: {follow_up}"
        updated_text, before, after = update_log(
            updated_text,
            key,
            current_status,
            args.reviewer,
            note,
        )
        updated_keys.append(after.key)

    print(f"AI observations available: {len(observations)}")
    print(f"Rows updated: {len(updated_keys)}")
    if updated_keys:
        print("Updated keys: " + ", ".join(updated_keys))

    if args.apply:
        args.log.write_text(updated_text, encoding="utf-8")
        print(f"Wrote {args.log.relative_to(ROOT)}")
    else:
        print("Dry run only. Re-run with --apply to write the visual review log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
