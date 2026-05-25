#!/usr/bin/env python3
"""Generate an AI-visible shortlist for the first Arabic review batch."""

from __future__ import annotations

from pathlib import Path
import sys

from report_arabic_visual_review_runbook import ROOT


DEFAULT_OUTPUT = ROOT / "documentation/arabic-first-review-risk-shortlist.md"

ZOOM_CROPS = [
    (
        "proof-regular-glyphs",
        "Regular",
        "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png",
    ),
    (
        "proof-medium-glyphs",
        "Medium",
        "documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png",
    ),
    (
        "proof-semibold-glyphs",
        "SemiBold",
        "documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png",
    ),
    (
        "proof-bold-glyphs",
        "Bold",
        "documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png",
    ),
]

WATCH_POINTS = [
    (
        "The focused crops show nonblank Arabic rows across all four weights.",
        "Use this only to speed up structure screening; it is not enough to pass a row.",
    ),
    (
        "No obvious tofu boxes, `.notdef` glyphs, fully blank Arabic cells, or gross clipping are visible at crop scale.",
        "Still open each full glyph proof to catch wrong-codepoint drawings and small mark issues.",
    ),
    (
        "`U+062B THEH`, `U+0633 SEEN`, `U+0634 SHEEN`, and `U+0648 WAW` remain the first shape-specific watch points.",
        "Compare the full proof with `documentation/arabic-structure-triage.md` before editing sidebearings or outlines.",
    ),
    (
        "`U+0653`, `U+0654`, and `U+0655` are visible only as small zero-advance marks in this crop.",
        "Judge their placement in the mark proof and dotted-circle context, not from the glyph crop alone.",
    ),
]


def status(path: str) -> str:
    full_path = ROOT / path
    return "present" if full_path.exists() else "missing"


def markdown_report() -> str:
    lines = [
        "# Arabic First Review Risk Shortlist",
        "",
        "This generated note records AI-visible structure risks from the focused",
        "Arabic-row glyph crops for the first review batch. It is not a human",
        "Arabic review and does not mark any row in",
        "`documentation/arabic-visual-review-log.md` as passed.",
        "",
        "## Evidence",
        "",
        "- Focused crop report: `documentation/arabic-first-review-zoom-snapshots.md`",
        "- Focused crop integrity: `documentation/arabic-first-review-crop-integrity.md`",
        "- First review worksheet: `documentation/arabic-first-review-batch.md`",
        "- AI sweep note: `documentation/arabic-first-review-ai-sweep.md`",
        "",
        "| Review key | Weight | Focused crop | File status | AI-visible structure screen |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, weight, crop in ZOOM_CROPS:
        lines.append(
            f"| `{key}` | {weight} | `{crop}` | {status(crop)} | "
            "Nonblank crop; no obvious tofu, `.notdef`, blank Arabic cell, or gross clipping visible at crop scale. |"
        )

    lines.extend(
        [
            "",
            "## First-Pass Risk Shortlist",
            "",
            "| AI-visible observation | Human review action |",
            "| --- | --- |",
        ]
    )
    for observation, action in WATCH_POINTS:
        lines.append(f"| {observation} | {action} |")

    lines.extend(
        [
            "",
            "## Non-Decisions",
            "",
            "- No row was marked `pass`.",
            "- No row was marked `fix-needed` from this crop review alone.",
            "- No row was deferred.",
            "- Do not edit Arabic sidebearings from the crop alone; verify shaped RTL context first.",
            "- Do not copy reference-font outlines. Use references only to compare structure, dot placement, and mark placement.",
            "",
            "## Next Human Step",
            "",
            "Open the five-row worksheet in `documentation/arabic-first-review-batch.md`",
            "and review the full proof HTML plus source targets for each row. Record",
            "a guarded status only after that proof/source pass.",
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
