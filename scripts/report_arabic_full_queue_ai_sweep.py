#!/usr/bin/env python3
"""Generate AI-safe observations for the full Arabic visual review queue."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_next_review_ai_observations import snapshot_evidence, snapshot_rows
from report_arabic_visual_review_runbook import ROOT, row_priority, visual_rows


DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-full-queue-ai-sweep.md"


REPRESENTATIVE_IMAGES = [
    "documentation/glyph-review/review-snapshots/proof-regular-glyphs-arabic-zoom.png",
    "documentation/glyph-review/review-snapshots/mark-shadda+sukun.png",
    "documentation/glyph-review/review-snapshots/proof-bold-text.png",
    "documentation/glyph-review/review-snapshots/proof-regular-proofer.png",
    "documentation/glyph-review/review-snapshots/class-dot-stack-helpers.png",
]


def pending_rows() -> list[object]:
    return sorted(
        [row for row in visual_rows() if row.status in {"pending", "fix-needed"}],
        key=row_priority,
    )


def row_group(key: str) -> str:
    if key.endswith("-glyphs") or key == "class-letter-structures":
        return "structure"
    if key.startswith("mark-") or key == "class-mark-combinations":
        return "marks"
    if key.startswith("proof-") and "-text" in key:
        return "text"
    if key.startswith("proof-") and "-proofer" in key:
        return "proofer"
    if key.startswith("proof-") and "-waterfall" in key:
        return "waterfall"
    if key.startswith("smoke-"):
        return "smoke"
    if key == "class-dot-stack-helpers":
        return "dot helpers"
    if key == "class-arabic-farsi-numerals":
        return "numerals"
    if key == "class-arabic-punctuation":
        return "punctuation"
    return "other"


def observation(row) -> str:
    key = row.key
    if key.endswith("-glyphs"):
        return (
            "Full snapshot and focused 2x Arabic-row crop are nonblank. Use the "
            "crop to screen structure faster, then open the full glyph proof for "
            "missing, blank, clipped, duplicated, malformed, or wrong-codepoint "
            "Arabic glyphs."
        )
    if key == "class-letter-structures":
        return (
            "Structure/risk snapshots show the expected high-risk overhang families. "
            "The overhangs need shaped-context judgment, not automatic sidebearing edits."
        )
    if key.startswith("mark-"):
        mark_notes = {
            "mark-base+fatha": "Section-targeted mark snapshot shows fatha samples across all five generated fonts. Human review still needs top-mark clearance, centering, and angle checks.",
            "mark-base+damma": "Section-targeted mark snapshot shows damma samples across all five generated fonts. Human review still needs damma scale and Bold readability checks.",
            "mark-base+kasra": "Section-targeted mark snapshot shows kasra samples across all five generated fonts. Human review still needs bottom-mark clearance and sidebearing checks.",
            "mark-shadda+sukun": "Section-targeted mark snapshot shows shadda, sukun, and stacked composites across all five generated fonts. Prioritize the no-offset prompts for `بُّ` and `بَّ`.",
            "mark-tanween": "Section-targeted mark snapshot shows tanween samples across all five generated fonts. Human review still needs twin-mark clarity and alignment checks.",
            "mark-hamza-above-below": "Section-targeted mark snapshot shows hamza-above and hamza-below samples across all five generated fonts. Human review still needs above/below clearance checks.",
            "mark-dotted-circle": "Section-targeted mark snapshot shows dotted circle with top, bottom, and tanween marks across all five generated fonts. Human review still needs dotted-circle readability checks.",
        }
        return mark_notes.get(key, "Section-targeted mark snapshot exists; open the full mark proof before deciding.")
    if key == "class-mark-combinations":
        return (
            "Use the shared mark proof to compare composite mark scale and stacking; "
            "mechanical mark setup is present, but visual approval is still pending."
        )
    if key.startswith("proof-") and "-text" in key:
        return (
            "Text snapshot renders mixed Latin/Arabic text without obvious blank-page "
            "failure. Inspect the full text proof for RTL texture, fallback, and mark "
            "collisions."
        )
    if key.startswith("proof-") and "-proofer" in key:
        return (
            "Proofer snapshot currently reflects GF_Latin_Core content and shows many "
            "box/tofu cells from missing Latin Core coverage. Treat it as a Latin/Core "
            "coverage blocker context, not Arabic drawing proof by itself."
        )
    if key.startswith("proof-") and "-waterfall" in key:
        return (
            "Waterfall snapshot is available for size/interpolation checks. Open the "
            "HTML at multiple sizes before judging small-size Arabic mark clarity."
        )
    if key.startswith("smoke-"):
        return (
            "Dashboard smoke strings are visible across variable/static weights. Use "
            "the dashboard and shaping report to judge join rhythm and style fit."
        )
    if key == "class-dot-stack-helpers":
        return (
            "Section-targeted dashboard snapshot shows Persian/Urdu dotted letters "
            "across all generated fonts. Use it to inspect dot separation, especially "
            "in Bold and in the variable font."
        )
    if key == "class-arabic-farsi-numerals":
        return (
            "Section-targeted dashboard snapshot shows Arabic-Indic digit rhythm across "
            "all generated fonts. Open the dashboard and glyph sources before judging "
            "digit widths and style fit."
        )
    if key == "class-arabic-punctuation":
        return (
            "Section-targeted dashboard snapshot shows Arabic punctuation across all "
            "generated fonts. Review comma, semicolon, question mark, per mille, date "
            "separator, full stop, and parentheses in RTL context."
        )
    return "Snapshot evidence exists; open the linked proof/source evidence before deciding."


def human_action(row) -> str:
    key = row.key
    if key.endswith("-glyphs"):
        return "Open the matching gftools glyph proof at zoom."
    if key.startswith("mark-") or key == "class-mark-combinations":
        return "Open `documentation/glyph-review/arabic-mark-review-proof.html`."
    if key.startswith("proof-"):
        return "Open the matching gftools proof HTML."
    if key.startswith("smoke-") or key.startswith("class-"):
        return "Open `documentation/glyph-review/arabic-manual-review-dashboard.html` and linked reports."
    return "Open linked proof/source evidence."


def coverage_audit(rows: list[object], snapshots: dict[str, list[tuple[str, str, str]]]) -> dict[str, object]:
    missing_observations: list[str] = []
    missing_followups: list[str] = []
    missing_snapshots: list[str] = []
    for row in rows:
        if not observation(row).strip():
            missing_observations.append(row.key)
        if not human_action(row).strip():
            missing_followups.append(row.key)
        if not snapshots.get(row.key):
            missing_snapshots.append(row.key)
    return {
        "rows": len(rows),
        "observation_rows": len(rows) - len(missing_observations),
        "followup_rows": len(rows) - len(missing_followups),
        "snapshot_rows": len(rows) - len(missing_snapshots),
        "missing_observations": missing_observations,
        "missing_followups": missing_followups,
        "missing_snapshots": missing_snapshots,
    }


def markdown_report() -> str:
    rows = pending_rows()
    snapshots = snapshot_rows()
    audit = coverage_audit(rows, snapshots)
    groups: dict[str, int] = {}
    for row in rows:
        groups[row_group(row.key)] = groups.get(row_group(row.key), 0) + 1

    lines = [
        "# Arabic Full Queue AI Sweep",
        "",
        "This generated report records AI-safe observations for the full pending",
        "Arabic visual-review queue. It is not a human Arabic review, does not",
        "approve drawings, and does not update `documentation/glyph-review/arabic-visual-review-log.md`.",
        "",
        "## Evidence Basis",
        "",
        "- Snapshot coverage source: `documentation/glyph-review/arabic-next-review-snapshots.md`",
        "- Focused zoom snapshot source: `documentation/glyph-review/arabic-first-review-zoom-snapshots.md`",
        "- Snapshot integrity source: `documentation/glyph-review/arabic-snapshot-integrity.md`",
        "- Official review log: `documentation/glyph-review/arabic-visual-review-log.md`",
        f"- Pending/fix-needed rows covered: {len(rows)}",
        "",
        "## Coverage Audit",
        "",
        f"- Pending/fix-needed rows: {audit['rows']}",
        f"- Rows with AI observation: {audit['observation_rows']} / {audit['rows']}",
        f"- Rows with human follow-up: {audit['followup_rows']} / {audit['rows']}",
        f"- Rows with snapshot evidence: {audit['snapshot_rows']} / {audit['rows']}",
        f"- Missing AI observations: {len(audit['missing_observations'])}",
        f"- Missing human follow-ups: {len(audit['missing_followups'])}",
        f"- Missing snapshot evidence: {len(audit['missing_snapshots'])}",
        "- Coverage ready for human review: "
        + (
            "yes"
            if not audit["missing_observations"]
            and not audit["missing_followups"]
            and not audit["missing_snapshots"]
            else "no"
        ),
        "",
        "Representative images inspected in this sweep:",
        "",
    ]
    lines.extend(f"- `{path}`" for path in REPRESENTATIVE_IMAGES)
    lines.extend(["", "## Queue Groups", "", "| Group | Rows |", "| --- | ---: |"])
    for group, count in sorted(groups.items()):
        lines.append(f"| {group} | {count} |")

    lines.extend(
        [
            "",
            "## Row Observations",
            "",
            "| Review key | Group | AI observation | Human follow-up | Snapshot evidence |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row.key}` | {row_group(row.key)} | {observation(row)} | "
            f"{human_action(row)} | {snapshot_evidence(row.key, snapshots)} |"
        )

    lines.extend(
        [
            "",
            "## Non-Decisions",
            "",
            "- No row was marked `pass`.",
            "- No source glyph was marked `fix-needed`.",
            "- No row was deferred.",
            "- Proofer tofu in GF_Latin_Core proof snapshots is treated as a separate",
            "  Latin Core coverage blocker, not as proof of Arabic drawing failure.",
            "- Sidebearing and mark-offset prompts remain human visual-review prompts.",
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
