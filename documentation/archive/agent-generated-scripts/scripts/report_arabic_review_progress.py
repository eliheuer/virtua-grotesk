#!/usr/bin/env python3
"""Generate a concise progress report for Arabic human review."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

from report_arabic_manual_review_batches import (
    BATCHES,
    ROOT,
    clean,
    next_unresolved_batch,
    status_summary,
    visual_rows,
    contour_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-review-progress.md"
VISUAL_LOG = ROOT / "documentation/glyph-review/arabic-visual-review-log.md"
CURRENT_WORKSHEET = ROOT / "documentation/glyph-review/arabic-current-review-worksheet.md"
BATCH_RECORDER = ROOT / "documentation/glyph-review/arabic-batch-recorder.md"
FIRST_REVIEW_BATCH = ROOT / "documentation/glyph-review/arabic-first-review-batch.md"
FIRST_BATCH_SOURCE_CHECKPOINT = ROOT / "documentation/glyph-review/arabic-first-batch-source-checkpoint.md"
PENDING_SOURCE_CHECKPOINT = ROOT / "documentation/glyph-review/arabic-pending-source-checkpoint.md"
GOAL_AUDIT = ROOT / "documentation/glyph-review/arabic-goal-completion-audit.md"


def visual_status(row: list[str]) -> str:
    return row[6] if len(row) >= 9 else row[5]


def visual_cue(row: list[str]) -> str:
    return row[5] if len(row) >= 9 else row[4]


def visual_area_item(row: list[str]) -> str:
    area = row[1] if len(row) >= 3 else ""
    item = row[2] if len(row) >= 3 else ""
    return f"{area} / {item}".strip(" /")


def summary_value(label: str, path: Path, default: str = "unknown") -> str:
    if not path.exists():
        return default
    prefix = f"- {label}: "
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return default


def visual_command(key: str, status: str, notes: str) -> str:
    return (
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS={status} '
        f'REVIEWER="Name YYYY-MM-DD" NOTES="{notes}"'
    )


def batch_rows(batch: dict[str, object], visual: dict[str, list[str]]) -> list[list[str]]:
    keys = batch.get("visual_keys", [])
    return [visual[key] for key in keys if isinstance(key, str) and key in visual]


def markdown_report() -> str:
    visual = visual_rows()
    contours = contour_rows()
    visual_counts = Counter(visual_status(row) for row in visual.values())
    unresolved = [
        row for row in visual.values() if visual_status(row) in {"pending", "fix-needed"}
    ]
    next_batch = next_unresolved_batch(visual, contours)
    first_ready = summary_value("Ready for paired-master hand review", FIRST_BATCH_SOURCE_CHECKPOINT)
    pending_ready = summary_value("Ready for paired-master hand review", PENDING_SOURCE_CHECKPOINT)
    pending_glyphs = summary_value("Unique source glyph names checked", PENDING_SOURCE_CHECKPOINT)
    pending_files = summary_value("Unique source target files referenced", PENDING_SOURCE_CHECKPOINT)
    pending_missing = summary_value("Missing source files", PENDING_SOURCE_CHECKPOINT)
    pending_mismatches = summary_value("Regular/Bold structure mismatches", PENDING_SOURCE_CHECKPOINT)

    lines = [
        "# Arabic Review Progress",
        "",
        "This generated report is the short status surface for closing the",
        "remaining human Arabic visual-review rows. It does not replace the",
        "review log; it points to the next rows and commands.",
        "",
        "## Summary",
        "",
        f"- Visual review ready: {'yes' if not unresolved else 'no'}",
        f"- Review rows: {len(visual)}",
        f"- Pending: {visual_counts.get('pending', 0)}",
        f"- Fix-needed: {visual_counts.get('fix-needed', 0)}",
        f"- Deferred: {visual_counts.get('deferred', 0)}",
        f"- Pass: {visual_counts.get('pass', 0)}",
        f"- Unresolved rows: {len(unresolved)}",
        f"- First-batch source checkpoint ready: {first_ready}",
        f"- Pending source checkpoint ready: {pending_ready}",
        f"- Pending source glyphs/files: {pending_glyphs} glyphs / {pending_files} files",
        f"- Pending source missing files: {pending_missing}",
        f"- Pending source Regular/Bold mismatches: {pending_mismatches}",
        "",
        "## Open First",
        "",
        f"- `{CURRENT_WORKSHEET.relative_to(ROOT)}`",
        f"- `{FIRST_REVIEW_BATCH.relative_to(ROOT)}`",
        f"- `{BATCH_RECORDER.relative_to(ROOT)}`",
        f"- `{FIRST_BATCH_SOURCE_CHECKPOINT.relative_to(ROOT)}`",
        f"- `{PENDING_SOURCE_CHECKPOINT.relative_to(ROOT)}`",
        f"- `{VISUAL_LOG.relative_to(ROOT)}`",
        "",
    ]

    if next_batch is None:
        lines.extend(
            [
                "## Current Batch",
                "",
                "No unresolved Arabic review rows remain.",
                "",
            ]
        )
    else:
        batch, state = next_batch
        visual_items = state["visual_items"]
        lines.extend(
            [
                "## Current Batch",
                "",
                f"- Name: {batch['name']}",
                f"- Why: {batch['why']}",
                f"- Visual rows: {len(visual_items)} ({status_summary(state['visual_statuses'])})",
                f"- Contour rows: {len(state['contour_items'])} ({status_summary(state['contour_statuses'])})",
                "",
                "| Key | Area / item | Status | Review cue |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            lines.append(
                f"| `{key}` | {visual_area_item(row)} | {visual_status(row)} | {visual_cue(row)} |"
            )
        lines.extend(
            [
                "",
                "## Recording Commands",
                "",
                "After opening the proof/source evidence, run exactly one command per",
                "reviewed row. Replace reviewer and notes before running.",
                "",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            lines.extend(
                [
                    f"### `{key}`",
                    "",
                    "```bash",
                    visual_command(key, "pass", "reviewed current proof/source evidence"),
                    visual_command(key, "fix-needed", "specific glyph or proof issue"),
                    visual_command(key, "deferred", "needs Arabic native-reader review"),
                    "```",
                    "",
                ]
            )

    lines.extend(
        [
            "## Batch Order",
            "",
            "| Batch | Remaining visual rows |",
            "| --- | ---: |",
        ]
    )
    for batch in BATCHES:
        rows = batch_rows(batch, visual)
        remaining = sum(1 for row in rows if visual_status(row) in {"pending", "fix-needed"})
        lines.append(f"| {batch['name']} | {remaining} |")

    lines.extend(
        [
            "",
            "## After Any Status Updates",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "Before closing the Arabic goal, verify:",
            "",
            f"- `{GOAL_AUDIT.relative_to(ROOT)}`",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
