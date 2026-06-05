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
from report_arabic_visual_review_runbook import (
    print_proof_page_lines,
    visual_rows as runbook_visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-batch-recorder.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/glyph-review/arabic-print-proof-index.md"
FIRST_BATCH_SOURCE_CHECKPOINT = ROOT / "documentation/glyph-review/arabic-first-batch-source-checkpoint.md"
PENDING_SOURCE_CHECKPOINT = ROOT / "documentation/glyph-review/arabic-pending-source-checkpoint.md"


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


def print_proof_pages_for_key(key: str, rows_by_key: dict[str, object]) -> str:
    row = rows_by_key.get(key)
    if row is None:
        return ""
    for line in print_proof_page_lines(row):
        text = line.strip().removeprefix("- ").strip()
        if text.startswith("Arabic print proof pages: "):
            return text.removeprefix("Arabic print proof pages: ")
    return ""


def markdown_report() -> str:
    visual = visual_rows()
    runbook_rows = {row.key: row for row in runbook_visual_rows()}
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
            f"- Focused Arabic PDF proof: `{ARABIC_PRINT_PROOF.relative_to(ROOT)}`",
            f"- Focused Arabic PDF index: `{ARABIC_PRINT_PROOF_INDEX.relative_to(ROOT)}`",
            f"- First-batch source checkpoint: `{FIRST_BATCH_SOURCE_CHECKPOINT.relative_to(ROOT)}`",
            f"- Pending source checkpoint: `{PENDING_SOURCE_CHECKPOINT.relative_to(ROOT)}`",
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
            print_pages = print_proof_pages_for_key(key, runbook_rows)
            lines.extend(
                [
                    f"### `{key}`",
                    "",
                    f"- Review cue: {cue}",
                    f"- Arabic print proof pages: {print_pages or 'none mapped'}",
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
                "## Optional Batch TSV Form",
                "",
                "The canonical record is `documentation/glyph-review/arabic-visual-review-log.md`.",
                "The per-row commands above are the clearest path. If you prefer",
                "to record several reviewed rows at once, save a tab-separated",
                "file with these columns, then dry-run it before applying.",
                "",
                "```tsv",
                "key\tstatus\treviewer\tnotes",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            lines.append(f"{key}\tpass\tName YYYY-MM-DD\treviewed current proof/source evidence")
        lines.extend(
            [
                "```",
                "",
                "```bash",
                "make arabic-visual-review-batch-dry-run REVIEW_BATCH=review.tsv",
                "make arabic-visual-review-batch-update REVIEW_BATCH=review.tsv",
                "make arabic-visual-review-batch-apply-check REVIEW_BATCH=review.tsv",
                "```",
                "",
                "Use the dry run first. The update target writes only the",
                "canonical review log; the apply-check target writes the log,",
                "regenerates reports, and reruns preflight.",
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
            "`documentation/glyph-review/arabic-manual-edit-targets.md` and rerun",
            "`make arabic-first-batch-source-checkpoint` plus",
            "`make arabic-pending-source-checkpoint` before editing so Regular",
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
