#!/usr/bin/env python3
"""Generate fill-in worksheets for every unresolved Arabic review batch."""

from __future__ import annotations

from pathlib import Path
import sys

import report_arabic_manual_edit_targets as edit_targets
from report_arabic_manual_review_batches import (
    BATCHES,
    ROOT,
    ai_observation_rows,
    batch_evidence_paths,
    batch_snapshot_rows,
    batch_status,
    clean,
    decision_rule,
    snapshot_rows,
    status_summary,
    visual_cue,
    visual_rows,
    visual_status,
    zoom_snapshot_rows,
)
from report_arabic_visual_review_runbook import (
    print_proof_page_lines,
    visual_rows as runbook_visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-review-worksheet-bundle.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/glyph-review/arabic-print-proof-index.md"


def visual_command(key: str, status: str, notes: str) -> str:
    return (
        f"make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS={status} "
        f'REVIEWER="Name YYYY-MM-DD" NOTES="{notes}"'
    )


def command_set(key: str) -> str:
    return "<br>".join(
        f"`{command}`"
        for command in [
            visual_command(key, "pass", "reviewed current proof/source evidence"),
            visual_command(key, "fix-needed", "specific glyph or proof issue"),
            visual_command(key, "deferred", "needs Arabic native-reader review"),
        ]
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


def batch_edit_targets(visual_items: list[list[str]]) -> list[edit_targets.EditTarget]:
    targets: list[edit_targets.EditTarget] = []
    seen: set[tuple[str, str, str]] = set()
    for row in visual_items:
        key = clean(row[0])
        for target in edit_targets.row_targets(key):
            path_key = str(target.path.relative_to(ROOT)) if target.path else "missing"
            target_key = (target.ufo.name, target.glyph_name, path_key)
            if target_key in seen:
                continue
            seen.add(target_key)
            targets.append(target)
    return targets


def glyph_focus_rows(
    targets: list[edit_targets.EditTarget],
) -> list[tuple[str, list[edit_targets.EditTarget], list[str]]]:
    by_glyph: dict[str, list[edit_targets.EditTarget]] = {}
    for target in targets:
        by_glyph.setdefault(target.glyph_name, []).append(target)

    rows: list[tuple[str, list[edit_targets.EditTarget], list[str]]] = []
    for glyph_name, glyph_targets in sorted(by_glyph.items()):
        sources = sorted({target.source for target in glyph_targets})
        rows.append((glyph_name, glyph_targets, sources))
    return rows


def master_names(targets: list[edit_targets.EditTarget]) -> str:
    return ", ".join(
        sorted(
            {
                target.ufo.name.replace("VirtuaGrotesk-", "").replace(".ufo", "")
                for target in targets
            }
        )
    )


def markdown_report() -> str:
    visual = visual_rows()
    runbook_rows = {row.key: row for row in runbook_visual_rows()}
    snapshots_by_key = snapshot_rows()
    zoom_snapshots_by_key = zoom_snapshot_rows()
    ai_rows = ai_observation_rows()

    pending_visual = [row for row in visual.values() if visual_status(row) in {"pending", "fix-needed"}]
    worksheet_rows = 0
    lines = [
        "# Arabic Review Worksheet Bundle",
        "",
        "This generated bundle turns the remaining Arabic visual-review queue into",
        "batch fill-in worksheets. It does not approve drawings: record outcomes",
        "only after opening the linked proof/source evidence.",
        "",
        "## Coverage",
        "",
        f"- Pending/fix-needed visual rows: {len(pending_visual)}",
        "- Source for AI-safe notes: `documentation/glyph-review/arabic-full-queue-ai-sweep.md`",
        "- Source for snapshots: `documentation/glyph-review/arabic-next-review-snapshots.md`",
        "- Source for official statuses: `documentation/glyph-review/arabic-visual-review-log.md`",
        f"- Focused Arabic PDF proof: `{ARABIC_PRINT_PROOF.relative_to(ROOT)}`",
        f"- Focused Arabic PDF index: `{ARABIC_PRINT_PROOF_INDEX.relative_to(ROOT)}`",
        "",
        "## Review Batches",
        "",
    ]

    for batch in BATCHES:
        if not batch["visual_keys"]:
            continue
        status = batch_status(batch, visual, [])
        visual_items = [
            row for row in status["visual_items"] if visual_status(row) in {"pending", "fix-needed"}
        ]
        if not visual_items:
            continue
        worksheet_rows += len(visual_items)
        batch_snapshots = batch_snapshot_rows(visual_items, snapshots_by_key, zoom_snapshots_by_key)
        evidence = batch_evidence_paths(batch, visual_items, [])
        lines.extend(
            [
                f"### {batch['name']}",
                "",
                f"- Why: {batch['why']}",
                f"- Visual rows in worksheet: {len(visual_items)} ({status_summary([visual_status(row) for row in visual_items])})",
                f"- Decision rule: {decision_rule(batch, [])}",
                "",
                "Evidence to open:",
                "",
            ]
        )
        lines.extend(f"- `{path}`" for path in evidence)
        if batch_snapshots:
            lines.extend(["", "Snapshot aids:", ""])
            lines.extend(
                f"- `{clean(row[0])}` {row[1]}: `{row[3].strip('`')}` from `{row[2].strip('`')}`"
                for row in batch_snapshots
            )
        focus_rows = glyph_focus_rows(batch_edit_targets(visual_items))
        if focus_rows:
            lines.extend(
                [
                    "",
                    "Glyph-level drawing punchlist:",
                    "",
                    "| Glyph | Masters | Review prompt source |",
                    "| --- | --- | --- |",
                ]
            )
            for glyph_name, glyph_targets, sources in focus_rows:
                lines.append(
                    f"| `{glyph_name}` | {master_names(glyph_targets)} | {'; '.join(sources)} |"
                )
        lines.extend(
            [
                "",
                "| Print proof pages | Key | Status | Review cue | AI observation | Human follow-up | Observed issue or `none` | Source/proof location | Final status | Guarded commands |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            ai_observation, human_follow_up = ai_rows.get(key, ("", ""))
            lines.append(
                f"| {print_proof_pages_for_key(key, runbook_rows)} | `{key}` | {visual_status(row)} | {visual_cue(row)} | {ai_observation} | "
                f"{human_follow_up} |  |  | pass / fix-needed / deferred | {command_set(key)} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Bundle Audit",
            "",
            f"- Worksheet rows: {worksheet_rows}",
            f"- Matches pending/fix-needed visual rows: {'yes' if worksheet_rows == len(pending_visual) else 'no'}",
            "",
            "## After Recording Outcomes",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "If any row becomes `fix-needed`, open",
            "`documentation/glyph-review/arabic-manual-edit-targets.md` before editing so",
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
