#!/usr/bin/env python3
"""Generate guarded status-recording commands for the next Arabic review batch."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_manual_review_batches import (
    BATCHES,
    ROOT,
    batch_status,
    clean,
    next_unresolved_batch,
    status_summary,
    visual_rows,
    contour_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/arabic-batch-recorder.md"


def visual_command(key: str, status: str, notes: str) -> str:
    return (
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS={status} '
        f'REVIEWER="Name YYYY-MM-DD" NOTES="{notes}"'
    )


def contour_command(glyph: str, status: str, decision: str) -> str:
    return (
        f'make contour-decision-update GLYPH={glyph} STATUS={status} '
        f'DECISION="{decision}" REVIEWED="Name YYYY-MM-DD"'
    )


def markdown_report() -> str:
    visual = visual_rows()
    contours = contour_rows()
    next_batch = next_unresolved_batch(visual, contours)
    lines = [
        "# Arabic Batch Recorder",
        "",
        "This generated file keeps the status-recording commands for the current",
        "unresolved Arabic hand-review batch in one place. It does not apply any",
        "status changes by itself, and the commands should only be run after",
        "proof/source inspection.",
        "",
        "## Current Batch",
        "",
    ]

    if next_batch is None:
        lines.extend(["No unresolved Arabic visual-review or contour-decision rows remain.", ""])
        return "\n".join(lines)

    batch, state = next_batch
    visual_items = state["visual_items"]
    contour_items = state["contour_items"]
    lines.extend(
        [
            f"- Batch: {batch['name']}",
            f"- Why: {batch['why']}",
            f"- Visual rows: {len(visual_items)} ({status_summary(state['visual_statuses'])})",
            f"- Contour rows: {len(contour_items)} ({status_summary(state['contour_statuses'])})",
            "",
            "## Visual Review Commands",
            "",
            "Use exactly one command per reviewed row. Replace the reviewer and notes",
            "before running.",
            "",
        ]
    )

    if visual_items:
        for row in visual_items:
            key = clean(row[0])
            cue = row[5] if len(row) >= 9 else row[4]
            lines.extend(
                [
                    f"### `{key}`",
                    "",
                    f"- Review cue: {cue}",
                    "",
                    "```bash",
                    visual_command(key, "pass", "reviewed current proof/source evidence"),
                    visual_command(key, "fix-needed", "specific glyph or proof issue"),
                    visual_command(key, "deferred", "needs Arabic native-reader review"),
                    "```",
                    "",
                ]
            )
    else:
        lines.extend(["No visual-review rows in this batch.", ""])

    lines.extend(["## Contour Decision Commands", ""])
    if contour_items:
        for row in contour_items:
            glyph = clean(row[0])
            lines.extend(
                [
                    f"### `{glyph}`",
                    "",
                    "```bash",
                    contour_command(glyph, "fix-now", "source edit needed"),
                    contour_command(glyph, "accepted", "reviewed style divergence"),
                    contour_command(glyph, "deferred", "needs later drawing review"),
                    "```",
                    "",
                ]
            )
    else:
        lines.extend(["No contour-decision rows in this batch.", ""])

    lines.extend(
        [
            "## After Recording Outcomes",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "If any row becomes `fix-needed`, use",
            "`documentation/arabic-manual-edit-targets.md` before editing so Regular",
            "and Bold stay compatible.",
            "",
            "## Full Batch Order",
            "",
        ]
    )
    for batch in BATCHES:
        state = batch_status(batch, visual, contours)
        lines.append(
            f"- {batch['name']}: visual {status_summary(state['visual_statuses'])}; "
            f"contour {status_summary(state['contour_statuses'])}"
        )
    lines.append("")
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
