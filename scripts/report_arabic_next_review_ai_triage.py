#!/usr/bin/env python3
"""Generate AI-assisted triage notes for the next Arabic review packet."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from report_arabic_visual_review_runbook import (
    ROOT,
    command,
    compact_machine_precheck,
    evidence_lines,
    row_priority,
    visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-next-review-ai-triage.md"
PACKET = ROOT / "documentation/glyph-review/arabic-next-review-packet.md"
SNAPSHOTS = ROOT / "documentation/glyph-review/arabic-next-review-snapshots.md"
STRUCTURE_TRIAGE = ROOT / "documentation/glyph-review/arabic-structure-triage.md"
VISUAL_RISK = ROOT / "documentation/glyph-review/arabic-visual-risk-audit.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return int(match.group(1)) if match else default


def table_rows(text: str, section_heading: str) -> list[list[str]]:
    start = text.find(section_heading)
    if start == -1:
        return []
    section = text[start:]
    next_heading = re.search(r"\n## ", section[len(section_heading) :])
    if next_heading:
        section = section[: len(section_heading) + next_heading.start()]
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] not in {"Review key", "Codepoint", "Font"}:
            rows.append(cells)
    return rows


def snapshot_map(text: str) -> dict[str, list[tuple[str, str, str]]]:
    snapshots: dict[str, list[tuple[str, str, str]]] = {}
    for cells in table_rows(text, "## Snapshots"):
        if len(cells) < 4:
            continue
        key = cells[0].strip("`")
        label = cells[1]
        source = cells[2].strip("`")
        png = cells[3].strip("`")
        snapshots.setdefault(key, []).append((label, source, png))
    return snapshots


def grouped_prompt_rows(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for cells in table_rows(text, "## Grouped Review Prompts"):
        if len(cells) < 6:
            continue
        rows.append((cells[0].strip("`"), cells[1].replace("`", ""), cells[5]))
    return rows


def row_by_key(key: str):
    for row in visual_rows():
        if row.key == key:
            return row
    return None


def next_rows() -> list[object]:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    return sorted(rows, key=row_priority)[:5]


def pending_review_rows() -> list[object]:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    return sorted(rows, key=row_priority)


def review_commands(key: str) -> list[str]:
    row = row_by_key(key)
    if row is None:
        return []
    return [
        command(row, "pass", "reviewed current proof"),
        command(row, "fix-needed", "specific glyph or proof issue"),
        command(row, "deferred", "needs Arabic native-reader review"),
    ]


def classification_for_row(row, mechanical_blockers: int) -> tuple[int, str, str]:
    if row.key.startswith("proof-") and row.key.endswith("-glyphs"):
        return (
            mechanical_blockers,
            "ready for glyph-proof pass/fix/defer review",
            "Open matching gftools proof HTML; inspect missing, blank, clipped, duplicated, or wrong-codepoint Arabic glyphs.",
        )
    if row.key == "class-letter-structures":
        return (
            mechanical_blockers,
            "ready for focused structure review",
            "Inspect sidebearing prompt glyphs in structure sweep, visual-risk proof, and source if needed.",
        )
    if row.key.startswith("mark-") or row.key == "class-mark-combinations":
        return (
            0,
            "ready for mark-proof pass/fix/defer review",
            "Open mark proof and mark triage; inspect attachment, collisions, and dotted-circle clarity.",
        )
    if row.key.startswith("smoke-"):
        return (
            0,
            "mechanical shaping passes; needs visual rhythm review",
            "Open shaping smoke report and dashboard; inspect contextual forms and spacing rhythm.",
        )
    if row.key.startswith("proof-"):
        return (
            0,
            "ready for proof pass/fix/defer review",
            "Open matching gftools proof HTML; inspect RTL texture, spacing, marks, and waterfall behavior as appropriate.",
        )
    if row.key.startswith("class-"):
        return (
            0,
            "ready for class-level drawing review",
            "Open dashboard and linked source/proof evidence before recording status.",
        )
    return (0, "ready for human review", "Open listed evidence before recording status.")


def evidence_summary(row) -> str:
    paths: list[str] = []
    for line in evidence_lines(row):
        paths.extend(re.findall(r"`([^`]+)`", line))
    if not paths:
        return "open row evidence"
    return "<br>".join(f"`{path}`" for path in paths[:4])


def markdown_report() -> str:
    packet_text = read(PACKET)
    snapshot_text = read(SNAPSHOTS)
    structure_text = read(STRUCTURE_TRIAGE)
    visual_risk_text = read(VISUAL_RISK)
    snapshots = snapshot_map(snapshot_text)
    prompts = grouped_prompt_rows(structure_text)
    first_batch_rows = next_rows()
    all_pending_rows = pending_review_rows()

    mechanical_blockers = first_int(r"^- Mechanical blocking risks: (\d+)$", structure_text)
    structure_prompts = first_int(r"^- Review-prompt risk rows: (\d+)$", structure_text)
    visual_risk_rows = first_int(r"^- Risk rows: (\d+)$", visual_risk_text)
    rendered_snapshots = first_int(r"^- Rendered snapshots: (\d+)$", snapshot_text)
    snapshot_errors = first_int(r"^- Errors: (\d+)$", snapshot_text)
    pending_count = first_int(r"^- Pending or fix-needed rows: (\d+)$", packet_text)

    lines = [
        "# Arabic Next Review AI Triage",
        "",
        "This generated report summarizes what AI/mechanical review can safely",
        "pre-triage for the current Arabic next-review packet. It does not mark",
        "visual rows as passed; final status still requires human proof/source",
        "inspection and an explicit `arabic-visual-review-update` command.",
        "",
        "## Inputs",
        "",
        f"- Next-review packet: `{PACKET.relative_to(ROOT)}`",
        f"- Snapshot report: `{SNAPSHOTS.relative_to(ROOT)}`",
        f"- Structure triage: `{STRUCTURE_TRIAGE.relative_to(ROOT)}`",
        f"- Visual-risk audit: `{VISUAL_RISK.relative_to(ROOT)}`",
        "",
        "## Current Batch State",
        "",
        f"- Pending or fix-needed visual rows: {pending_count}",
        f"- Rendered PNG snapshots: {rendered_snapshots}",
        f"- Snapshot errors: {snapshot_errors}",
        f"- Structure triage mechanical blockers: {mechanical_blockers}",
        f"- Structure triage review-prompt rows: {structure_prompts}",
        f"- Visual-risk audit rows: {visual_risk_rows}",
        "",
        "## First-Batch AI Triage Summary",
        "",
        "| Review key | Snapshot evidence | Mechanical blockers | AI-safe classification | Human decision still needed |",
        "| --- | --- | ---: | --- | --- |",
    ]

    for row in first_batch_rows:
        row_snapshots = snapshots.get(row.key, [])
        evidence = "<br>".join(
            f"`{png}` from `{source}`" for _, source, png in row_snapshots
        ) or "missing snapshot report row"
        blockers, classification, human_need = classification_for_row(row, mechanical_blockers)
        lines.append(
            f"| `{row.key}` | {evidence} | {blockers} | {classification} | {human_need} |"
        )

    lines.extend(
        [
            "",
            "## Full Pending Queue AI Triage",
            "",
            "This table covers every pending or fix-needed visual review row. It is",
            "a navigation and risk summary only; it does not mark rows as passed.",
            "",
            "| Order | Review key | Area | Item | Mechanical precheck | AI-safe classification | Evidence to open | Human decision still needed |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for index, row in enumerate(all_pending_rows, start=1):
        _blockers, classification, human_need = classification_for_row(row, mechanical_blockers)
        lines.append(
            f"| {index} | `{row.key}` | {row.area} | {row.item} | {compact_machine_precheck(row)} | {classification} | {evidence_summary(row)} | {human_need} |"
        )

    lines.extend(
        [
            "",
            "## Structure Prompts To Inspect",
            "",
        ]
    )
    if prompts:
        lines.extend(
            [
                "| Codepoint | Glyphs | Prompt |",
                "| --- | --- | --- |",
            ]
        )
        for codepoint, glyphs, prompt in prompts:
            lines.append(f"| `{codepoint}` | `{glyphs}` | {prompt} |")
    else:
        lines.append("- none found")

    lines.extend(
        [
            "",
            "## Recommended Review Order",
            "",
            "1. Open the first-batch cards in `documentation/glyph-review/arabic-next-review-board.html`.",
            "2. If the glyph pages show no missing, blank, clipped, duplicated, or",
            "   wrong-codepoint Arabic glyphs, record those proof rows as `pass`.",
            "3. Open the structure sweep and visual-risk proof for the prompt glyphs.",
            "4. Continue through the full pending queue by area: mark attachment,",
            "   text/proofer/waterfall proofs, smoke strings, numerals, punctuation.",
            "5. Record each row as `pass`, `fix-needed`, or `deferred` only after",
            "   checking the linked proof/source evidence.",
            "",
            "## Guarded Update Commands",
            "",
            "Use one command per row after human inspection:",
            "",
            "```bash",
        ]
    )
    for row in first_batch_rows:
        lines.extend(review_commands(row.key))
    lines.extend(
        [
            "```",
            "",
            "## Notes",
            "",
            "- AI can confirm that current snapshot artifacts exist and that the",
            "  generated triage reports show no mechanical `.notdef`, blank-visible",
            "  glyph, nonmark-zero-advance, or shared visible cmap blockers.",
            "- AI cannot approve Arabic drawing quality, cultural/script correctness,",
            "  or final spacing rhythm without human review.",
            "- Do not copy reference-font outlines into production sources. Use",
            "  references only for comparison, then redraw or adjust in Virtua style.",
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
