#!/usr/bin/env python3
"""Generate a TSV template for the current Arabic visual review batch."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_manual_review_batches import (
    ROOT,
    clean,
    contour_rows,
    next_unresolved_batch,
    visual_rows,
    visual_status,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-visual-review-batch.tsv"


def tsv_cell(value: str) -> str:
    return value.replace("\t", " ").replace("\n", " ").strip()


def tsv_report() -> str:
    visual = visual_rows()
    contours = contour_rows()
    next_batch = next_unresolved_batch(visual, contours)
    lines = ["key\tstatus\treviewer\tnotes"]
    if next_batch is None:
        return "\n".join(lines) + "\n"

    _batch, state = next_batch
    visual_items = [
        row for row in state["visual_items"] if visual_status(row) in {"pending", "fix-needed"}
    ]
    for row in visual_items:
        key = clean(row[0])
        lines.append(
            "\t".join(
                [
                    tsv_cell(key),
                    "",
                    "",
                    "",
                ]
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(tsv_report(), encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
