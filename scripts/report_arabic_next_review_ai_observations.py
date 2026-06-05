#!/usr/bin/env python3
"""Generate AI-safe observation notes for Arabic review snapshots."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from report_arabic_visual_review_runbook import (
    ROOT,
    row_priority,
    split_markdown_row,
    visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-next-review-ai-observations.md"
SNAPSHOTS = ROOT / "documentation/glyph-review/arabic-next-review-snapshots.md"
ZOOM_SNAPSHOTS = ROOT / "documentation/glyph-review/arabic-first-review-zoom-snapshots.md"
SNAPSHOT_INTEGRITY = ROOT / "documentation/glyph-review/arabic-snapshot-integrity.md"
VISUAL_LOG = ROOT / "documentation/glyph-review/arabic-visual-review-log.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def summary_value(text: str, label: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def snapshot_rows() -> dict[str, list[tuple[str, str, str]]]:
    rows: dict[str, list[tuple[str, str, str]]] = {}
    for path, heading in [
        (SNAPSHOTS, "## Snapshots"),
        (ZOOM_SNAPSHOTS, "## Zoom Snapshots"),
    ]:
        in_table = False
        for line in read(path).splitlines():
            if line == heading:
                in_table = True
                continue
            if in_table and line.startswith("## "):
                break
            if not in_table or not line.startswith("| `"):
                continue
            cells = split_markdown_row(line)
            if len(cells) != 4:
                continue
            key = cells[0].strip("`")
            label = cells[1]
            source = cells[2].strip("`")
            png = cells[3].strip("`")
            rows.setdefault(key, []).append((label, source, png))
    return rows


def pending_rows() -> list[object]:
    return sorted(
        [row for row in visual_rows() if row.status in {"pending", "fix-needed"}],
        key=row_priority,
    )


def snapshot_evidence(key: str, snapshots: dict[str, list[tuple[str, str, str]]]) -> str:
    rows = snapshots.get(key, [])
    if not rows:
        return "missing snapshot row"
    return "<br>".join(f"`{png}` from `{source}`" for _label, source, png in rows)


def observation(row) -> str:
    if row.key.startswith("proof-") and row.key.endswith("-glyphs"):
        weight = row.item.split()[0]
        return (
            f"{weight} glyph-proof snapshot evidence and a focused 2x Arabic-row "
            "crop are present and nonblank. Use the crop for faster structure "
            "screening of missing, blank, clipped, duplicated, malformed, or "
            "wrong-codepoint Arabic glyphs before opening the full proof HTML."
        )
    if row.key == "class-letter-structures":
        return (
            "Structure and visual-risk snapshots are present. Treat sidebearing "
            "and overhang prompts as style-review questions in shaped RTL context, "
            "not automatic spacing failures."
        )
    if row.key.startswith("mark-"):
        return (
            "Mark-proof snapshot evidence is present. The mechanical reports are "
            "clean enough for visual attachment review, with attention to "
            "collisions, stacked marks, dotted-circle clarity, and weight changes."
        )
    if row.key == "class-mark-combinations":
        return (
            "Mark-combination snapshot evidence is present. Review composite mark "
            "scale and stacking in the shared mark proof before deciding whether "
            "source edits are needed."
        )
    if row.key == "class-dot-stack-helpers":
        return (
            "Dashboard snapshot evidence is present for dot-stack helper review. "
            "Check whether three-dot and six-dot helpers keep separation in Bold "
            "and interpolate cleanly."
        )
    if row.key.startswith("proof-") and "-text" in row.key:
        return (
            "Text-proof snapshot evidence is present. Use it to triage RTL texture, "
            "fallback, mark collisions, and unexpected spacing influence before "
            "opening the full text proof."
        )
    if row.key.startswith("proof-") and "-proofer" in row.key:
        return (
            "Proofer snapshot evidence is present. Inspect sidebearing rhythm, "
            "Arabic punctuation spacing, numeral rhythm, and weight-specific "
            "spacing in the linked proof HTML."
        )
    if row.key.startswith("proof-") and "-waterfall" in row.key:
        return (
            "Waterfall snapshot evidence is present. Use it to check small-size "
            "behavior, interpolation, and mark clarity across sizes."
        )
    if row.key.startswith("smoke-"):
        return (
            "Dashboard snapshot evidence is present and the shaping smoke report "
            "mechanically passes. Human review still needs to judge rhythm, joins, "
            "and style fit in the rendered string."
        )
    if row.key == "class-arabic-farsi-numerals":
        return (
            "Dashboard snapshot evidence is present for Arabic and Farsi numerals. "
            "Review width rhythm and style fit against Latin numerals and Arabic "
            "text before passing."
        )
    if row.key == "class-arabic-punctuation":
        return (
            "Dashboard snapshot evidence is present for Arabic punctuation. Review "
            "comma, semicolon, question mark, per mille, date separator, full stop, "
            "and parentheses spacing in RTL context."
        )
    return (
        "Snapshot evidence is present. Open the linked proof or source evidence "
        "before recording a final review status."
    )


def suggested_action(row) -> str:
    if row.key.startswith("proof-") and row.key.endswith("-glyphs"):
        return (
            "Open the matching gftools glyph proof at zoom; record `fix-needed` "
            "only with exact glyph names or proof locations."
        )
    if row.key.startswith("mark-") or row.key == "class-mark-combinations":
        return (
            "Open `documentation/glyph-review/arabic-mark-review-proof.html`; compare mark "
            "placement across weights before recording pass/fix/defer."
        )
    if row.key.startswith("smoke-"):
        return (
            "Open `documentation/glyph-review/arabic-shaping-smoke-test.md` and the dashboard; "
            "confirm joins and spacing visually before passing."
        )
    if row.key.startswith("proof-"):
        return (
            "Open the matching gftools proof HTML; inspect the row cue directly "
            "before recording an outcome."
        )
    if row.key.startswith("class-"):
        return (
            "Open the dashboard plus linked proof/source reports; record `pass` "
            "only after the whole class cue is reviewed."
        )
    return "Open the linked evidence and record pass, fix-needed, or deferred."


def markdown_report() -> str:
    snapshots = snapshot_rows()
    rows = pending_rows()
    integrity = read(SNAPSHOT_INTEGRITY)
    rendered = summary_value(read(SNAPSHOTS), "Rendered snapshots")
    errors = summary_value(read(SNAPSHOTS), "Errors")
    no_snapshot = summary_value(integrity, "Pending/fix-needed rows without snapshot")
    ready = summary_value(integrity, "Snapshot evidence ready for hand review")

    lines = [
        "# Arabic Next Review AI Observations",
        "",
        "This generated note records AI-safe first-pass observations over the",
        "current Arabic review snapshot set. It is not a human Arabic review and",
        "does not mark any row in `documentation/glyph-review/arabic-visual-review-log.md` as",
        "passed.",
        "",
        "## Snapshot Inputs",
        "",
        "- Full pending-queue snapshot report:",
        f"  - `{SNAPSHOTS.relative_to(ROOT)}`",
        f"  - Rendered snapshots: {rendered}",
        f"  - Rows without snapshot source: {summary_value(read(SNAPSHOTS), 'Rows without snapshot source')}",
        f"  - Snapshot errors: {errors}",
        "- Focused zoom snapshot report:",
        f"  - `{ZOOM_SNAPSHOTS.relative_to(ROOT)}`",
        f"  - Rendered zoom snapshots: {summary_value(read(ZOOM_SNAPSHOTS), 'Rendered zoom snapshots')}",
        f"  - Zoom snapshot errors: {summary_value(read(ZOOM_SNAPSHOTS), 'Errors')}",
        "- Snapshot integrity:",
        f"  - `{SNAPSHOT_INTEGRITY.relative_to(ROOT)}`",
        f"  - Pending/fix-needed rows without snapshot: {no_snapshot}",
        f"  - Snapshot evidence ready for hand review: {ready}",
        "",
        "## Observations",
        "",
        "| Review key | AI first-pass observation | Suggested human action |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| `{row.key}` | {observation(row)} | {suggested_action(row)} |")

    lines.extend(
        [
            "",
            "## Full Queue Snapshot Evidence",
            "",
            "| Order | Review key | Snapshot evidence |",
            "| ---: | --- | --- |",
        ]
    )
    for index, row in enumerate(rows, start=1):
        lines.append(f"| {index} | `{row.key}` | {snapshot_evidence(row.key, snapshots)} |")

    lines.extend(
        [
            "",
            "## Non-Decisions",
            "",
            "- Do not mark any row as `pass` from this file alone.",
            "- Do not edit sidebearings only because the mechanical audit flags negative",
            "  sidebearings; joining-script rhythm must be checked in shaped context.",
            "- Do not copy reference-font outlines. Use references only to compare joining",
            "  logic, dot placement, and mark placement.",
            "",
            "## Next Commands",
            "",
            "After human inspection, record one outcome per row:",
            "",
            "```bash",
        ]
    )
    for row in rows[:5]:
        lines.append(
            f'make arabic-visual-review-update REVIEW_KEY={row.key} REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"'
        )
    lines.extend(
        [
            "```",
            "",
            "Use `fix-needed` or `deferred` instead of `pass` wherever the proof or",
            "source inspection is inconclusive.",
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
