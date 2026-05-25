#!/usr/bin/env python3
"""Generate a one-session worksheet for the next Arabic visual review batch."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from report_arabic_visual_review_runbook import (
    ROOT,
    split_markdown_row,
    visual_rows,
)


DEFAULT_OUTPUT = ROOT / "documentation/arabic-first-review-batch.md"
SNAPSHOTS = ROOT / "documentation/arabic-next-review-snapshots.md"
EDIT_TARGETS = ROOT / "documentation/arabic-manual-edit-targets.md"
STRUCTURE_TRIAGE = ROOT / "documentation/arabic-structure-triage.md"
VISUAL_RISK = ROOT / "documentation/arabic-visual-risk-proof.html"
FIRST_BATCH_AI_SWEEP = ROOT / "documentation/arabic-first-review-ai-sweep.md"
ZOOM_SNAPSHOTS = ROOT / "documentation/arabic-first-review-zoom-snapshots.md"
CROP_INTEGRITY = ROOT / "documentation/arabic-first-review-crop-integrity.md"
RISK_SHORTLIST = ROOT / "documentation/arabic-first-review-risk-shortlist.md"

FIRST_BATCH_KEYS = [
    "proof-regular-glyphs",
    "proof-medium-glyphs",
    "proof-semibold-glyphs",
    "proof-bold-glyphs",
    "class-letter-structures",
]

ZOOM_SNAPSHOT_BY_KEY = {
    "proof-regular-glyphs": "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png",
    "proof-medium-glyphs": "documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png",
    "proof-semibold-glyphs": "documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png",
    "proof-bold-glyphs": "documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def snapshot_rows() -> dict[str, list[tuple[str, str, str]]]:
    rows: dict[str, list[tuple[str, str, str]]] = {}
    in_table = False
    for line in read(SNAPSHOTS).splitlines():
        if line == "## Snapshots":
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


def edit_target_section(key: str) -> str:
    text = read(EDIT_TARGETS)
    match = re.search(
        rf"^### `{re.escape(key)}`\n(?P<body>.*?)(?=^### `|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else ""


def source_target_summary(key: str) -> tuple[str, list[str]]:
    body = edit_target_section(key)
    if not body:
        return "Source targets: unavailable", []
    summary = re.search(r"^- Source targets: (.+)$", body, flags=re.MULTILINE)
    paths = sorted(set(re.findall(r"`(sources/[^`]+\.glif)`", body)))
    return f"Source targets: {summary.group(1)}" if summary else "Source targets: see edit-target report", paths


def structure_prompt_lines() -> list[str]:
    text = read(STRUCTURE_TRIAGE)
    prompts: list[str] = []
    for line in text.splitlines():
        if "review prompt" not in line.lower() and "Check " not in line:
            continue
        if line.startswith("| `"):
            cells = split_markdown_row(line)
            if len(cells) >= 4:
                prompts.append(f"- `{cells[0].strip('`')}`: {cells[-1]}")
    return prompts[:8]


def status_counts(rows_by_key: dict[str, object]) -> str:
    statuses = [rows_by_key[key].status for key in FIRST_BATCH_KEYS if key in rows_by_key]
    return ", ".join(f"`{status}`: {statuses.count(status)}" for status in sorted(set(statuses))) or "none"


def update_commands(key: str) -> list[str]:
    return [
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof"',
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"',
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"',
    ]


def zoom_snapshot_for_key(key: str) -> str | None:
    repo_path = ZOOM_SNAPSHOT_BY_KEY.get(key)
    if not repo_path:
        return None
    return repo_path if (ROOT / repo_path).exists() else None


def markdown_report() -> str:
    rows_by_key = {row.key: row for row in visual_rows()}
    snapshots = snapshot_rows()
    lines = [
        "# Arabic First Review Batch",
        "",
        "This generated worksheet flattens the next Arabic hand-review batch into",
        "one short session. It is a review aid only: open the proof/source evidence",
        "before recording any `pass`, and use `fix-needed` only with exact glyphs,",
        "proof locations, or source files.",
        "",
        "## Batch Goal",
        "",
        "Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint",
        "Arabic glyphs before judging spacing, rhythm, marks, or kerning.",
        "",
        "## Batch State",
        "",
        f"- Review rows: {len(FIRST_BATCH_KEYS)}",
        f"- Status counts: {status_counts(rows_by_key)}",
        f"- Main proof directory: `documentation/gftools-qa/Proof/`",
        f"- Structure triage: `{rel(STRUCTURE_TRIAGE)}`",
        f"- Visual-risk proof: `{rel(VISUAL_RISK)}`",
        f"- Edit-target source: `{rel(EDIT_TARGETS)}`",
        f"- AI visual sweep notes: `{rel(FIRST_BATCH_AI_SWEEP)}`",
        f"- Focused zoom crops: `{rel(ZOOM_SNAPSHOTS)}`",
        f"- Focused crop integrity: `{rel(CROP_INTEGRITY)}`",
        f"- AI-visible risk shortlist: `{rel(RISK_SHORTLIST)}`",
        "",
        "## Shared High-Risk Prompts",
        "",
        "- `U+062B THEH`: dot stack height and left overhang.",
        "- `U+0633 SEEN` / `U+0634 SHEEN`: left overhang in shaped RTL context.",
        "- `U+0648 WAW`: descending bowl and left overhang in adjacent text.",
        "- `U+0653`, `U+0654`, `U+0655`: expected zero-advance mark overhang; inspect attachment and dotted-circle clarity.",
        "",
    ]
    triage_lines = structure_prompt_lines()
    if triage_lines:
        lines.extend(["Additional structure-triage prompts:", "", *triage_lines, ""])

    lines.extend(["## Row Worksheet", ""])
    for key in FIRST_BATCH_KEYS:
        row = rows_by_key.get(key)
        if row is None:
            continue
        target_summary, target_paths = source_target_summary(key)
        lines.extend(
            [
                f"### `{key}`",
                "",
                f"- Area/item: {row.area} / {row.item}",
                f"- Current status: `{row.status}`",
                f"- Review cue: {row.cue}",
                f"- Machine precheck: {row.machine_precheck}",
                f"- {target_summary}",
            ]
        )
        if snapshots.get(key):
            lines.append("- Snapshot aids:")
            for label, source, png in snapshots[key]:
                lines.append(f"  - {label}: `{png}` from `{source}`")
        zoom_snapshot = zoom_snapshot_for_key(key)
        if zoom_snapshot:
            lines.append(f"- Focused Arabic-row crop: `{zoom_snapshot}`")
        if target_paths:
            lines.append("- First source files to inspect if `fix-needed`:")
            for path in target_paths:
                lines.append(f"  - `{path}`")
        lines.extend(["", "Record after proof/source review:", "", "```bash"])
        lines.extend(update_commands(key))
        lines.extend(["```", ""])

    lines.extend(
        [
            "## After This Batch",
            "",
            "If any row becomes `fix-needed`, edit Regular and Bold together, then run:",
            "",
            "```bash",
            "./build.sh",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "If all five rows are passed or explicitly deferred, regenerate the",
            "review reports and continue with the marks/dotted-circle batch.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
