#!/usr/bin/env python3
"""Generate a fill-in worksheet for the current Arabic hand-review batch."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_manual_review_batches import (
    ROOT,
    batch_evidence_paths,
    batch_snapshot_rows,
    clean,
    next_unresolved_batch,
    status_summary,
    visual_rows,
    contour_rows,
    decision_rule,
    snapshot_rows,
    zoom_snapshot_rows,
)
from report_arabic_visual_review_runbook import split_markdown_row


DEFAULT_OUTPUT = ROOT / "documentation/arabic-current-review-worksheet.md"
FIRST_REVIEW_AI_SWEEP = ROOT / "documentation/arabic-first-review-ai-sweep.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/arabic-print-proof-index.md"


def visual_command(key: str, status: str, notes: str) -> str:
    return (
        f"make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS={status} "
        f'REVIEWER="Name YYYY-MM-DD" NOTES="{notes}"'
    )


def machine_precheck(row: list[str]) -> str:
    return row[4] if len(row) >= 9 else ""


def review_cue(row: list[str]) -> str:
    return row[5] if len(row) >= 9 else row[4]


def ai_triage_rows() -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    if not FIRST_REVIEW_AI_SWEEP.exists():
        return rows
    for line in FIRST_REVIEW_AI_SWEEP.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 3:
            continue
        key = clean(cells[0])
        rows[key] = (cells[1], cells[2])
    return rows


def markdown_report() -> str:
    visual = visual_rows()
    contours = contour_rows()
    next_batch = next_unresolved_batch(visual, contours)
    lines = [
        "# Arabic Current Review Worksheet",
        "",
        "This generated worksheet is the fill-in sheet for the current Arabic",
        "hand-review batch. It is not an approval artifact by itself: record",
        "outcomes only after opening the linked proof/source evidence.",
        "",
    ]
    if next_batch is None:
        lines.extend(["No unresolved Arabic review rows remain.", ""])
        return "\n".join(lines)

    batch, state = next_batch
    visual_items = state["visual_items"]
    contour_items = state["contour_items"]
    snapshots = batch_snapshot_rows(visual_items, snapshot_rows(), zoom_snapshot_rows())
    evidence = batch_evidence_paths(batch, visual_items, contour_items)
    ai_rows = ai_triage_rows()

    lines.extend(
        [
            "## Batch",
            "",
            f"- Name: {batch['name']}",
            f"- Why: {batch['why']}",
            f"- Visual rows: {len(visual_items)} ({status_summary(state['visual_statuses'])})",
            f"- Contour rows: {len(contour_items)} ({status_summary(state['contour_statuses'])})",
            f"- Decision rule: {decision_rule(batch, contour_items)}",
            "",
            "## Evidence To Open",
            "",
        ]
    )
    if ARABIC_PRINT_PROOF.exists():
        lines.append(f"- `{ARABIC_PRINT_PROOF.relative_to(ROOT)}`")
    if ARABIC_PRINT_PROOF_INDEX.exists():
        lines.append(f"- `{ARABIC_PRINT_PROOF_INDEX.relative_to(ROOT)}`")
    for path in evidence:
        lines.append(f"- `{path}`")
    if ai_rows:
        lines.append(f"- `{FIRST_REVIEW_AI_SWEEP.relative_to(ROOT)}`")
    lines.extend(["", "## Snapshot Aids", ""])
    for row in snapshots:
        key = clean(row[0])
        label = row[1]
        source = clean(row[2])
        png = clean(row[3])
        lines.append(f"- `{key}` {label}: `{png}` from `{source}`")

    if ai_rows:
        lines.extend(
            [
                "",
                "## AI Triage Notes",
                "",
                "These notes come from `documentation/arabic-first-review-ai-sweep.md`.",
                "They are not review decisions and do not justify recording `pass`",
                "without opening the linked proof/source evidence.",
                "",
                "| Key | AI observation | Human follow-up |",
                "| --- | --- | --- |",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            observation, follow_up = ai_rows.get(key, ("", ""))
            if observation or follow_up:
                lines.append(f"| `{key}` | {observation} | {follow_up} |")

    if ARABIC_PRINT_PROOF.exists():
        lines.extend(
            [
                "",
                "## Print-Proof Pass",
                "",
                "Use `documentation/arabic-print-proof.pdf` as the quick paper or PDF",
                "scan for this batch before opening the heavier HTML proof pages.",
                "Use `documentation/arabic-print-proof-index.md` to jump to the",
                "right style and section in the PDF.",
                "For each row, look for missing glyphs, wrong glyphs, clipping,",
                "blank cells, malformed joins, and weight-specific rhythm changes.",
                "The PDF is a review aid: record `pass`, `fix-needed`, or",
                "`deferred` only after checking the linked source/proof evidence.",
            ]
        )

    lines.extend(
        [
            "",
            "## Fill-In Review Table",
            "",
            "| Key | Current status | Machine precheck | Review cue | Observed issue or `none` | Source/proof location | Final status |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in visual_items:
        key = clean(row[0])
        status = row[6] if len(row) >= 9 else row[5]
        lines.append(
            f"| `{key}` | {status} | {machine_precheck(row)} | {review_cue(row)} |  |  | pass / fix-needed / deferred |"
        )

    lines.extend(
        [
            "",
            "## Recording Commands",
            "",
            "Use exactly one command per reviewed row after filling the table. Replace",
            "`Name YYYY-MM-DD` and the notes before running.",
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
            "## After Recording Outcomes",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "If any row becomes `fix-needed`, open",
            "`documentation/arabic-manual-edit-targets.md` before editing so",
            "Regular and Bold stay compatible.",
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
