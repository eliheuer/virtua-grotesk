#!/usr/bin/env python3
"""Generate row-by-row instructions for Arabic visual review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/arabic-visual-review-runbook.md"
VISUAL_LOG = ROOT / "documentation/arabic-visual-review-log.md"
BATCHES = ROOT / "documentation/arabic-manual-review-batches.md"
SNAPSHOTS = ROOT / "documentation/arabic-next-review-snapshots.md"
ZOOM_SNAPSHOTS = ROOT / "documentation/arabic-first-review-zoom-snapshots.md"
SNAPSHOT_INTEGRITY = ROOT / "documentation/arabic-snapshot-integrity.md"
NEXT_BATCH = ROOT / "documentation/arabic-next-review-batch.html"
DASHBOARD = ROOT / "documentation/arabic-manual-review-dashboard.html"
ARABIC_PRINT_PROOF = ROOT / "documentation/arabic-print-proof.pdf"
ARABIC_PRINT_PROOF_INDEX = ROOT / "documentation/arabic-print-proof-index.md"
PROOF_DIR = ROOT / "documentation/gftools-qa/Proof"
STRUCTURE_TRIAGE = ROOT / "documentation/arabic-structure-triage.md"
MARK_TRIAGE = ROOT / "documentation/arabic-mark-triage.md"
SHAPING_SMOKE = ROOT / "documentation/arabic-shaping-smoke-test.md"
CONTOUR_DECISIONS = ROOT / "documentation/contour-cleanup-decision-log.md"
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]
PROOF_INSTANCE_NAMES = {
    "regular": "Regular",
    "medium": "Medium",
    "semibold": "SemiBold",
    "bold": "Bold",
}
PRINT_PROOF_PAGES = {
    "regular": {"samples": 1, "numerals": 2, "cmap": 3},
    "medium": {"samples": 4, "numerals": 5, "cmap": 6},
    "semibold": {"samples": 7, "numerals": 8, "cmap": 9},
    "bold": {"samples": 10, "numerals": 11, "cmap": 12},
}
BATCH_REVIEW_ORDER = [
    "proof-regular-glyphs",
    "proof-medium-glyphs",
    "proof-semibold-glyphs",
    "proof-bold-glyphs",
    "class-letter-structures",
    "mark-base+fatha",
    "mark-base+damma",
    "mark-base+kasra",
    "mark-shadda+sukun",
    "mark-tanween",
    "mark-hamza-above-below",
    "mark-dotted-circle",
    "class-mark-combinations",
    "class-dot-stack-helpers",
    "proof-regular-text",
    "proof-regular-proofer",
    "proof-regular-waterfall",
    "proof-medium-text",
    "proof-medium-proofer",
    "proof-medium-waterfall",
    "proof-semibold-text",
    "proof-semibold-proofer",
    "proof-semibold-waterfall",
    "proof-bold-text",
    "proof-bold-proofer",
    "proof-bold-waterfall",
    "smoke-salaam",
    "smoke-arabic",
    "smoke-bismillah",
    "smoke-lam-alef",
    "class-arabic-farsi-numerals",
    "class-arabic-punctuation",
]
BATCH_REVIEW_PRIORITY = {
    key: index for index, key in enumerate(BATCH_REVIEW_ORDER, start=1)
}
FOCUSED_EVIDENCE_BY_KEY = {
    "proof-regular-glyphs": [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-structure-triage.md",
    ],
    "proof-medium-glyphs": [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-structure-triage.md",
    ],
    "proof-semibold-glyphs": [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-structure-triage.md",
    ],
    "proof-bold-glyphs": [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-structure-triage.md",
    ],
    "class-letter-structures": [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-structure-triage.md",
    ],
    "mark-base+fatha": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-base+damma": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-base+kasra": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-shadda+sukun": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-tanween": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-hamza-above-below": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "mark-dotted-circle": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
    "class-mark-combinations": [
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
    ],
}


@dataclass(frozen=True)
class ReviewRow:
    key: str
    area: str
    item: str
    evidence: str
    machine_precheck: str
    cue: str
    status: str
    reviewer: str
    notes: str


@dataclass(frozen=True)
class StructurePrompt:
    codepoint: str
    glyphs: str
    prompt: str


@dataclass(frozen=True)
class SourceGlyphTarget:
    ufo: Path
    glyph_name: str
    glif_path: Path


def split_markdown_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in line.strip().strip("|"):
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\":
            current.append(character)
            escaped = True
            continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    cells.append("".join(current).strip())
    return cells


def clean_key(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|")


def clean_text(value: str) -> str:
    return value.strip().replace("\\|", "|")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def codepoint_int(value: str) -> int | None:
    match = re.search(r"U\+([0-9A-Fa-f]{4,6})", value)
    return int(match.group(1), 16) if match else None


def source_targets_for_codepoint(codepoint: int) -> list[SourceGlyphTarget]:
    targets: list[SourceGlyphTarget] = []
    for ufo in SOURCE_UFOS:
        glyph_dir = ufo / "glyphs"
        for glif_path in sorted(glyph_dir.glob("*.glif")):
            try:
                root = ET.parse(glif_path).getroot()
            except ET.ParseError:
                continue
            for unicode_element in root.findall("unicode"):
                hex_value = unicode_element.attrib.get("hex", "")
                if not hex_value:
                    continue
                if int(hex_value, 16) == codepoint:
                    targets.append(
                        SourceGlyphTarget(
                            ufo=ufo,
                            glyph_name=root.attrib.get("name", glif_path.stem),
                            glif_path=glif_path,
                        )
                    )
    return targets


def visual_rows() -> list[ReviewRow]:
    rows: list[ReviewRow] = []
    for line in read_text(VISUAL_LOG).splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 8:
            continue
        if len(cells) >= 9:
            machine_precheck = clean_text(cells[4])
            cue = clean_text(cells[5])
            status = clean_text(cells[6]) or "pending"
            reviewer = clean_text(cells[7])
            notes = clean_text(cells[8])
        else:
            machine_precheck = ""
            cue = clean_text(cells[4])
            status = clean_text(cells[5]) or "pending"
            reviewer = clean_text(cells[6])
            notes = clean_text(cells[7])
        rows.append(
            ReviewRow(
                key=clean_key(cells[0]),
                area=clean_text(cells[1]),
                item=clean_text(cells[2]),
                evidence=clean_text(cells[3]),
                machine_precheck=machine_precheck,
                cue=cue,
                status=status,
                reviewer=reviewer,
                notes=notes,
            )
        )
    return rows


def proof_matches(row: ReviewRow) -> list[Path]:
    if not PROOF_DIR.exists() or row.area != "GF proof":
        return []
    tokens = row.key.split("-")
    if len(tokens) < 3:
        return []
    instance = PROOF_INSTANCE_NAMES.get(tokens[1], tokens[1].title())
    proof_type = tokens[2]
    return sorted(PROOF_DIR.glob(f"{instance}-diffbrowsers_{proof_type}.html"))


def print_proof_page_lines(row: ReviewRow) -> list[str]:
    if not ARABIC_PRINT_PROOF.exists() or not ARABIC_PRINT_PROOF_INDEX.exists():
        return []

    pages: list[tuple[str, str]] = []
    tokens = row.key.split("-")
    if row.key.startswith("proof-") and len(tokens) >= 3:
        instance = tokens[1]
        proof_type = tokens[2]
        style_pages = PRINT_PROOF_PAGES.get(instance)
        if style_pages:
            if proof_type == "glyphs":
                pages.append((str(style_pages["cmap"]), f"{PROOF_INSTANCE_NAMES.get(instance, instance)} cmap grid"))
            elif proof_type in {"text", "waterfall"}:
                pages.append((str(style_pages["samples"]), f"{PROOF_INSTANCE_NAMES.get(instance, instance)} Arabic samples"))
            elif proof_type == "proofer":
                pages.append((str(style_pages["samples"]), f"{PROOF_INSTANCE_NAMES.get(instance, instance)} Arabic samples"))
                pages.append((str(style_pages["numerals"]), f"{PROOF_INSTANCE_NAMES.get(instance, instance)} numerals and punctuation"))
    elif row.key.startswith("mark-") or row.key in {
        "class-mark-combinations",
        "class-dot-stack-helpers",
    }:
        pages.extend((str(page_set["samples"]), f"{PROOF_INSTANCE_NAMES[key]} Arabic samples") for key, page_set in PRINT_PROOF_PAGES.items())
    elif row.key == "class-letter-structures":
        pages.extend((str(page_set["cmap"]), f"{PROOF_INSTANCE_NAMES[key]} cmap grid") for key, page_set in PRINT_PROOF_PAGES.items())
        pages.extend((str(page_set["samples"]), f"{PROOF_INSTANCE_NAMES[key]} Arabic samples") for key, page_set in PRINT_PROOF_PAGES.items())
    elif row.key.startswith("smoke-"):
        pages.extend((str(page_set["samples"]), f"{PROOF_INSTANCE_NAMES[key]} Arabic samples") for key, page_set in PRINT_PROOF_PAGES.items())
    elif row.key == "class-arabic-farsi-numerals":
        pages.extend((str(page_set["numerals"]), f"{PROOF_INSTANCE_NAMES[key]} numerals") for key, page_set in PRINT_PROOF_PAGES.items())
    elif row.key == "class-arabic-punctuation":
        pages.extend((str(page_set["numerals"]), f"{PROOF_INSTANCE_NAMES[key]} punctuation") for key, page_set in PRINT_PROOF_PAGES.items())

    if not pages:
        return []
    page_text = "; ".join(f"p. {page} {label}" for page, label in pages)
    return [
        f"- Arabic print proof pages: {page_text}",
        f"  - Page map: `{ARABIC_PRINT_PROOF_INDEX.relative_to(ROOT)}`",
    ]


def snapshot_rows_for_key(key: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for path, suffix in [(SNAPSHOTS, ""), (ZOOM_SNAPSHOTS, " focused 2x crop")]:
        for line in read_text(path).splitlines():
            if not line.startswith("| `"):
                continue
            cells = split_markdown_row(line)
            if len(cells) != 4 or clean_key(cells[0]) != key:
                continue
            source_html = clean_text(cells[2]).strip("`")
            png = clean_text(cells[3]).strip("`")
            rows.append((f"{clean_text(cells[1])}{suffix}", source_html, png))
    return rows


def snapshot_lines(row: ReviewRow) -> list[str]:
    rows = snapshot_rows_for_key(row.key)
    if not rows:
        return []
    lines = ["- Snapshot aids:"]
    for label, source_html, png in rows:
        lines.append(f"  - {label}: `{png}` from `{source_html}`")
    return lines


def command(row: ReviewRow, status: str, note: str) -> str:
    return (
        f'make arabic-visual-review-update REVIEW_KEY={row.key} REVIEW_STATUS={status} '
        f'REVIEWER="Name YYYY-MM-DD" NOTES="{note}"'
    )


def row_priority(row: ReviewRow) -> tuple[int, str]:
    return (BATCH_REVIEW_PRIORITY.get(row.key, len(BATCH_REVIEW_ORDER) + 1), row.key)


def evidence_lines(row: ReviewRow) -> list[str]:
    lines = [f"- Evidence: {row.evidence}"]
    lines.extend(print_proof_page_lines(row))
    lines.extend(snapshot_lines(row))
    focused = FOCUSED_EVIDENCE_BY_KEY.get(row.key, [])
    existing_focused = [path for path in focused if (ROOT / path).exists()]
    if existing_focused:
        lines.append("- Focused review pages:")
        for path in existing_focused:
            lines.append(f"  - `{path}`")
    matches = proof_matches(row)
    if matches:
        lines.append("- Matching proof files:")
        for path in matches:
            lines.append(f"  - `{path.relative_to(ROOT)}`")
    if row.key.startswith("class-"):
        lines.append(f"- Dashboard: `{DASHBOARD.relative_to(ROOT)}`")
    return lines


def summary_value(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}: ([^\n]+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def grouped_structure_prompt_rows() -> list[StructurePrompt]:
    rows: list[StructurePrompt] = []
    in_section = False
    for line in read_text(STRUCTURE_TRIAGE).splitlines():
        if line == "## Grouped Review Prompts":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 6:
            continue
        codepoint = clean_text(cells[0])
        glyphs = clean_text(cells[1])
        prompt = clean_text(cells[5])
        rows.append(StructurePrompt(codepoint, glyphs, prompt))
    return rows


def needs_structure_prompt_summary(row: ReviewRow) -> bool:
    return (
        row.key == "class-letter-structures"
        or (row.key.startswith("proof-") and row.key.endswith("-glyphs"))
    )


def mark_prompt_summary_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    in_section = False
    for line in read_text(MARK_TRIAGE).splitlines():
        if line == "## No-Offset Review Prompt Summary":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 3:
            continue
        review_key = clean_key(cells[0])
        font = clean_text(cells[1])
        samples = clean_text(cells[2])
        sample_texts = clean_text(cells[3]) if len(cells) >= 4 else ""
        rows.append((review_key, font, samples, sample_texts))
    return rows


def mark_prompt_detail_rows() -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    in_section = False
    for line in read_text(MARK_TRIAGE).splitlines():
        if line == "## No-Offset Review Prompt Rows":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 4:
            continue
        review_key = clean_key(cells[0])
        font = clean_text(cells[1])
        sample = clean_text(cells[2])
        glyph_sequence = clean_text(cells[3])
        source_targets = clean_text(cells[4]) if len(cells) >= 5 else "none"
        rows.append((review_key, font, sample, glyph_sequence, source_targets))
    return rows


def needs_mark_prompt_summary(row: ReviewRow) -> bool:
    return row.key.startswith("mark-") or row.key == "class-mark-combinations"


def machine_precheck_lines(row: ReviewRow) -> list[str]:
    structure_text = read_text(STRUCTURE_TRIAGE)
    mark_text = read_text(MARK_TRIAGE)
    shaping_text = read_text(SHAPING_SMOKE)
    contour_text = read_text(CONTOUR_DECISIONS)

    lines = ["- Machine precheck:"]
    if row.key.startswith("proof-") and row.key.endswith("-glyphs"):
        lines.append(
            "  - Structure triage mechanical blockers: "
            f"{summary_value(structure_text, 'Mechanical blocking risks')}"
        )
        lines.append(
            "  - Structure triage review prompts: "
            f"{summary_value(structure_text, 'Review-prompt risk rows')}"
        )
    elif row.key.startswith("mark-") or row.key == "class-mark-combinations":
        lines.append(
            "  - Mark triage mechanical blockers: "
            f"{summary_value(mark_text, 'Mechanical blocking risks')}"
        )
        lines.append(
            "  - Mark triage no-offset prompts: "
            f"{summary_value(mark_text, 'No-offset mark review prompts')}"
        )
    elif row.key.startswith("smoke-"):
        shaping_ok = (
            shaping_text.count("GSUB has `arab/dflt`: `true`") == 5
            and shaping_text.count("GPOS has `arab/dflt`: `true`") == 5
            and "| 0 |" in shaping_text
        )
        lines.append(f"  - Shaping smoke mechanical pass: {'yes' if shaping_ok else 'review report'}")
        lines.append("  - Visual rhythm and style still require hand review.")
    elif row.key.startswith("class-"):
        contour_open = summary_value(contour_text, "Pending")
        fix_now = summary_value(contour_text, "Fix-now")
        lines.append(f"  - Contour decisions pending: {contour_open}")
        lines.append(f"  - Contour decisions marked fix-now: {fix_now}")
    else:
        proof_files = len(proof_matches(row))
        lines.append(f"  - Matching proof files present: {proof_files}")
        lines.append("  - Visual proof comparison still requires hand review.")
    return lines


def structure_prompt_summary_lines(row: ReviewRow) -> list[str]:
    if not needs_structure_prompt_summary(row):
        return []
    rows = grouped_structure_prompt_rows()
    if not rows:
        return []
    lines = [
        "- Grouped structure prompts:",
        "  - Use these collapsed codepoint questions before recording an outcome; they are not automatic approval.",
    ]
    for prompt_row in rows:
        lines.append(f"  - {prompt_row.codepoint} / {prompt_row.glyphs}: {prompt_row.prompt}")
        codepoint = codepoint_int(prompt_row.codepoint)
        targets = source_targets_for_codepoint(codepoint) if codepoint is not None else []
        if targets:
            target_text = "; ".join(
                f"`{target.ufo.name}` `{target.glyph_name}` -> `{target.glif_path.relative_to(ROOT)}`"
                for target in targets
            )
            lines.append(f"    - Source edit targets: {target_text}")
    return lines


def mark_prompt_summary_lines(row: ReviewRow) -> list[str]:
    if not needs_mark_prompt_summary(row):
        return []
    rows = [item for item in mark_prompt_summary_rows() if item[0] == row.key]
    if not rows:
        return []
    lines = [
        "- Mark placement prompts:",
        "  - These zero-offset rows need visual inspection in the mark proof; they are not automatic failures.",
    ]
    for _review_key, font, samples, sample_texts in rows:
        sample_note = f" ({sample_texts})" if sample_texts else ""
        lines.append(f"  - {font}: {samples} shaped sample(s){sample_note}")
    detail_rows = [item for item in mark_prompt_detail_rows() if item[0] == row.key]
    for _review_key, font, sample, glyph_sequence, source_targets in detail_rows:
        lines.append(f"    - {font} {sample}: {glyph_sequence}")
        lines.append(f"      - Source edit targets: {source_targets}")
    return lines


def global_mark_prompt_summary_lines(pending_rows: list[ReviewRow]) -> list[str]:
    mark_keys = {row.key for row in pending_rows if needs_mark_prompt_summary(row)}
    rows = [row for row in mark_prompt_summary_rows() if row[0] in mark_keys]
    if not rows:
        return []
    lines = [
        "## Mark Review Prompt Summary",
        "",
        "The current mark triage has no mechanical blockers. Its remaining",
        "zero-offset prompts are visual proof checks, not automatic failures.",
        "",
        "| Review row | Font | Samples | Sample texts |",
        "| --- | --- | ---: | --- |",
    ]
    for review_key, font, samples, sample_texts in rows:
        lines.append(f"| `{review_key}` | {font} | {samples} | {sample_texts or 'none'} |")
    lines.append("")
    return lines


def global_mark_prompt_detail_lines(pending_rows: list[ReviewRow]) -> list[str]:
    mark_keys = {row.key for row in pending_rows if needs_mark_prompt_summary(row)}
    rows = [row for row in mark_prompt_detail_rows() if row[0] in mark_keys]
    if not rows:
        return []
    lines = [
        "## Mark Review Source Targets",
        "",
        "Use these rows when a no-offset mark sample needs editing. The target",
        "list includes both masters so compatibility can be preserved.",
        "",
        "| Review row | Font | Sample | Glyph sequence | Source edit targets |",
        "| --- | --- | --- | --- | --- |",
    ]
    for review_key, font, sample, glyph_sequence, source_targets in rows:
        lines.append(
            f"| `{review_key}` | {font} | {sample} | {glyph_sequence} | {source_targets} |"
        )
    lines.append("")
    return lines


def compact_machine_precheck(row: ReviewRow) -> str:
    details = [
        line.removeprefix("  - ")
        for line in machine_precheck_lines(row)[1:]
    ]
    return "<br>".join(details) if details else "none"


def review_prompt(row: ReviewRow) -> str:
    return (
        "Compare the current Virtua Grotesk Arabic rendering for "
        f"`{row.key}` against the listed evidence. Focus on: {row.cue}. "
        "Classify the row as pass, fix-needed, or deferred. If fix-needed, "
        "name the specific source glyphs or proof locations to inspect; do not "
        "suggest copying outlines from reference fonts."
    )


def markdown_report() -> str:
    rows = visual_rows()
    pending = [row for row in rows if row.status in {"pending", "fix-needed"}]
    deferred = [row for row in rows if row.status == "deferred"]
    passed = [row for row in rows if row.status == "pass"]
    pending_sorted = sorted(pending, key=row_priority)
    next_rows = pending_sorted[:5]

    lines = [
        "# Arabic Visual Review Runbook",
        "",
        "This generated runbook turns `documentation/arabic-visual-review-log.md`",
        "into row-by-row review cards. It does not approve drawings; it makes the",
        "remaining human review faster and easier to record.",
        "",
        "## Summary",
        "",
        f"- Review rows: {len(rows)}",
        f"- Pending or fix-needed: {len(pending)}",
        f"- Deferred: {len(deferred)}",
        f"- Pass: {len(passed)}",
        f"- Focused next-batch page: `{NEXT_BATCH.relative_to(ROOT)}`",
        f"- Dashboard: `{DASHBOARD.relative_to(ROOT)}`",
        f"- Snapshot report: `{SNAPSHOTS.relative_to(ROOT)}`",
        f"- Focused zoom snapshot report: `{ZOOM_SNAPSHOTS.relative_to(ROOT)}`",
        f"- Snapshot integrity: `{SNAPSHOT_INTEGRITY.relative_to(ROOT)}`",
        f"- Batch order: `{BATCHES.relative_to(ROOT)}`",
        "",
        "## Next Five Review Cards",
        "",
    ]
    if not next_rows:
        lines.append("No pending or fix-needed visual review rows remain.")
        lines.append("")
    for index, row in enumerate(next_rows, start=1):
        lines.extend(review_card(index, row))

    lines.extend(global_mark_prompt_summary_lines(pending_sorted))
    lines.extend(global_mark_prompt_detail_lines(pending_sorted))

    lines.extend(
        [
            "## Full Pending Queue",
            "",
            "| Key | Area | Item | Status | Machine precheck | Review cue |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in pending_sorted:
        lines.append(
            f"| `{row.key}` | {row.area} | {row.item} | {row.status} | {compact_machine_precheck(row)} | {row.cue} |"
        )
    lines.append("")
    return "\n".join(lines)


def review_card(index: int, row: ReviewRow) -> list[str]:
    lines = [
        f"### {index}. `{row.key}`",
        "",
        f"- Area: {row.area}",
        f"- Item: {row.item}",
        f"- Current status: {row.status}",
        f"- Review cue: {row.cue}",
        *evidence_lines(row),
        *machine_precheck_lines(row),
        *structure_prompt_summary_lines(row),
        *mark_prompt_summary_lines(row),
        "",
        "Record one outcome:",
        "",
        "```bash",
        command(row, "pass", "reviewed evidence"),
        command(row, "fix-needed", "specific issue to fix"),
        command(row, "deferred", "needs Arabic native-reader review"),
        "```",
        "",
        "AI comparison prompt:",
        "",
        f"> {review_prompt(row)}",
        "",
    ]
    return lines


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
