#!/usr/bin/env python3
"""Generate the editable Arabic visual review log."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/arabic-visual-review-log.md"
PROOF_DIR = ROOT / "documentation/gftools-qa/Proof"
STRUCTURE_TRIAGE = ROOT / "documentation/arabic-structure-triage.md"
MARK_TRIAGE = ROOT / "documentation/arabic-mark-triage.md"
SHAPING_SMOKE = ROOT / "documentation/arabic-shaping-smoke-test.md"
CONTOUR_DECISIONS = ROOT / "documentation/contour-cleanup-decision-log.md"
ALLOWED_STATUSES = ("pending", "pass", "fix-needed", "deferred")
PROOF_INSTANCES = ("Regular", "Medium", "SemiBold", "Bold")
PROOF_TYPES = (
    ("glyphs", "Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs"),
    ("text", "Text proof: RTL texture, fallback, mark collisions, and unexpected spacing influence"),
    ("proofer", "Proofer: sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing"),
    ("waterfall", "Waterfall: small-size behavior, interpolation, and mark clarity"),
)
SMOKE_ROWS = (
    ("salaam", "contextual forms and lam-alef behavior look intentional"),
    ("arabic", "initial, medial, and final joins are shaped and spaced coherently"),
    ("bismillah", "word spacing, medial joins, heh, and meem forms hold together"),
    ("lam-alef", "lam-alef ligature is present and weight-compatible"),
)
MARK_ROWS = (
    ("base+fatha", "top mark position clears the base and matches style"),
    ("base+damma", "damma position and scale are readable across weights"),
    ("base+kasra", "bottom mark position clears descenders and sidebearings"),
    ("shadda+sukun", "stacked top marks remain clear and centered"),
    ("tanween", "tanween combinations remain clear and aligned"),
    ("hamza-above-below", "hamza combinations attach cleanly above and below"),
    ("dotted-circle", "dotted circle with top and bottom marks is readable"),
)
CLASS_ROWS = (
    ("letter-structures", "sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof"),
    ("mark-combinations", "shadda, hamza, tanween, sukun, and kasra composites"),
    ("dot-stack-helpers", "three-dot and six-dot Persian/Urdu helpers"),
    ("arabic-farsi-numerals", "U+0660-U+0669 and U+06F0-U+06F9 rhythm, width, and style fit"),
    ("arabic-punctuation", "Arabic comma, semicolon, question mark, per mille, date separator, full stop, and parentheses"),
)


@dataclass(frozen=True)
class ReviewRow:
    key: str
    area: str
    item: str
    evidence: str
    machine_precheck: str
    cue: str
    status: str = "pending"
    reviewer: str = ""
    notes: str = ""


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


def clean_cell(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|")


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def summary_value(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}: ([^\n]+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def proof_match_count(key: str) -> int:
    if not PROOF_DIR.exists() or not key.startswith("proof-"):
        return 0
    parts = key.split("-")
    if len(parts) < 3:
        return 0
    instance = {
        "regular": "Regular",
        "medium": "Medium",
        "semibold": "SemiBold",
        "bold": "Bold",
    }.get(parts[1], parts[1].title())
    proof_type = parts[2]
    return len(list(PROOF_DIR.glob(f"{instance}-diffbrowsers_{proof_type}.html")))


def machine_precheck(key: str) -> str:
    if key.startswith("proof-") and key.endswith("-glyphs"):
        text = read_text(STRUCTURE_TRIAGE)
        return (
            "Structure triage mechanical blockers: "
            f"{summary_value(text, 'Mechanical blocking risks')}; "
            "structure review prompts: "
            f"{summary_value(text, 'Review-prompt risk rows')}"
        )
    if key.startswith("mark-") or key == "class-mark-combinations":
        text = read_text(MARK_TRIAGE)
        return (
            "Mark triage mechanical blockers: "
            f"{summary_value(text, 'Mechanical blocking risks')}; "
            "mark no-offset prompts: "
            f"{summary_value(text, 'No-offset mark review prompts')}"
        )
    if key.startswith("smoke-"):
        text = read_text(SHAPING_SMOKE)
        shaping_ok = (
            text.count("GSUB has `arab/dflt`: `true`") == 5
            and text.count("GPOS has `arab/dflt`: `true`") == 5
            and "| 0 |" in text
        )
        return f"Shaping smoke mechanical pass: {'yes' if shaping_ok else 'review report'}"
    if key.startswith("class-"):
        text = read_text(CONTOUR_DECISIONS)
        return (
            "Contour decisions pending: "
            f"{summary_value(text, 'Pending')}; "
            "fix-now: "
            f"{summary_value(text, 'Fix-now')}"
        )
    if key.startswith("proof-"):
        return f"Matching proof files present: {proof_match_count(key)}"
    return "Review evidence manually"


def existing_decisions(path: Path) -> dict[str, tuple[str, str, str]]:
    if not path.exists():
        return {}
    decisions: dict[str, tuple[str, str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 8:
            continue
        key = clean_cell(cells[0])
        status_index = 6 if len(cells) >= 9 else 5
        status = clean_cell(cells[status_index]) or "pending"
        reviewer = clean_cell(cells[status_index + 1])
        notes = clean_cell(cells[status_index + 2])
        if status not in ALLOWED_STATUSES:
            status = "pending"
        decisions[key] = (status, reviewer, notes)
    return decisions


def proof_file_count() -> int:
    if not PROOF_DIR.exists():
        return 0
    return len(list(PROOF_DIR.glob("*-diffbrowsers_*.html")))


def rows() -> list[ReviewRow]:
    output: list[ReviewRow] = []
    for instance in PROOF_INSTANCES:
        for proof_type, cue in PROOF_TYPES:
            key = f"proof-{instance.lower()}-{proof_type}"
            pattern = (
                f"`documentation/gftools-qa/Proof/*{instance}*-diffbrowsers_{proof_type}.html`; "
                "`documentation/arabic-manual-review-dashboard.html`"
            )
            output.append(
                ReviewRow(
                    key,
                    "GF proof",
                    f"{instance} {proof_type}",
                    pattern,
                    machine_precheck(key),
                    cue,
                )
            )
    for label, cue in SMOKE_ROWS:
        output.append(
            ReviewRow(
                f"smoke-{label}",
                "Smoke string",
                label,
                "`documentation/arabic-shaping-smoke-test.md`; `documentation/arabic-manual-review-dashboard.html`",
                machine_precheck(f"smoke-{label}"),
                cue,
            )
        )
    for label, cue in MARK_ROWS:
        output.append(
            ReviewRow(
                f"mark-{label}",
                "Mark attachment",
                label,
                "`documentation/arabic-mark-readiness.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/gftools-qa/Proof`",
                machine_precheck(f"mark-{label}"),
                cue,
            )
        )
    for label, cue in CLASS_ROWS:
        evidence = (
            "`documentation/contour-cleanup-decision-log.md`; "
            "`documentation/arabic-cleanup-drawing-briefs.md`; "
            "`documentation/arabic-manual-review-dashboard.html`"
        )
        if label == "letter-structures":
            evidence += "; `documentation/arabic-visual-risk-proof.html`"
        output.append(
            ReviewRow(
                f"class-{label}",
                "Glyph class",
                label,
                evidence,
                machine_precheck(f"class-{label}"),
                cue,
            )
        )
    return output


def apply_existing(rows_: list[ReviewRow], decisions: dict[str, tuple[str, str, str]]) -> list[ReviewRow]:
    merged: list[ReviewRow] = []
    for row in rows_:
        status, reviewer, notes = decisions.get(row.key, (row.status, row.reviewer, row.notes))
        merged.append(
            ReviewRow(
                row.key,
                row.area,
                row.item,
                row.evidence,
                row.machine_precheck,
                row.cue,
                status,
                reviewer,
                notes,
            )
        )
    return merged


def markdown_report(output_path: Path) -> str:
    review_rows = apply_existing(rows(), existing_decisions(output_path))
    counts = {status: 0 for status in ALLOWED_STATUSES}
    for row in review_rows:
        counts[row.status] += 1
    ready = counts["pending"] == 0 and counts["fix-needed"] == 0
    proof_files = proof_file_count()

    lines = [
        "# Arabic Visual Review Log",
        "",
        "This generated log tracks the human Arabic drawing review required after",
        "candidate generation. Regenerating it preserves Status, Reviewer, and",
        "Notes for stable row keys.",
        "",
        f"- Visual review ready: {'yes' if ready else 'no'}",
        f"- Review rows: {len(review_rows)}",
        f"- Pending: {counts['pending']}",
        f"- Pass: {counts['pass']}",
        f"- Fix-needed: {counts['fix-needed']}",
        f"- Deferred: {counts['deferred']}",
        f"- Google Fonts QA proof files: {proof_files} / 16 present",
        "- Manual review dashboard: `documentation/arabic-manual-review-dashboard.html`",
        "",
        "Status values: `pending`, `pass`, `fix-needed`, or `deferred`.",
        "",
        "| Key | Area | Item | Evidence | Machine precheck | Review cue | Status | Reviewer | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in review_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.key}`",
                    escape_cell(row.area),
                    escape_cell(row.item),
                    row.evidence,
                    escape_cell(row.machine_precheck),
                    escape_cell(row.cue),
                    row.status,
                    escape_cell(row.reviewer),
                    escape_cell(row.notes),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Update Workflow",
            "",
            "Update one review row with the guarded helper:",
            "",
            "```bash",
            "make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER=\"Name YYYY-MM-DD\" NOTES=\"reviewed proof\"",
            "```",
            "",
            "You can also hand-edit the Status, Reviewer, and Notes cells while",
            "reviewing the proof HTML. Then regenerate reports with:",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(output), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
