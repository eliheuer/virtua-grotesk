#!/usr/bin/env python3
"""Generate source edit targets for Arabic visual-review rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import plistlib
import re
import sys

import report_arabic_visual_review_runbook as runbook


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-manual-edit-targets.md"
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]

DOT_STACK_GLYPHS = [
    "dotcenter-ar",
    "twodotshorizontalbelow-ar",
    "twodotsverticalabove-ar",
    "twodotsverticalbelow-ar",
    "threedotsdownabove-ar",
    "threedotsdownbelow-ar",
    "threedotsdowncenter-ar",
    "threedotsupbelow-ar",
    "smallHighThreeDots-ar",
    "seenSixdots-ar",
    "seenSixdots-ar.fina",
    "seenSixdots-ar.init",
    "seenSixdots-ar.medi",
]

ARABIC_FARSI_NUMERALS = [
    "zero-ar",
    "one-ar",
    "two-ar",
    "three-ar",
    "four-ar",
    "five-ar",
    "six-ar",
    "seven-ar",
    "eight-ar",
    "nine-ar",
    "zeroFarsi-ar",
    "oneFarsi-ar",
    "twoFarsi-ar",
    "threeFarsi-ar",
    "fourFarsi-ar",
    "fiveFarsi-ar",
    "sixFarsi-ar",
    "sevenFarsi-ar",
    "eightFarsi-ar",
    "nineFarsi-ar",
]

ARABIC_PUNCTUATION = [
    "comma-ar",
    "semicolon-ar",
    "question-ar",
    "percent-ar",
    "perMille-ar",
    "decimalseparator-ar",
    "thousandseparator-ar",
    "dateSeparator-ar",
    "fullStop-ar",
    "asterisk-ar",
    "parenleft-ar",
    "parenright-ar",
    "arabicNumberSign",
    "arabicFootnoteMarker",
    "arabicSignSafha",
    "arabicSignSanah",
]

MARK_REVIEW_GLYPHS = {
    "mark-base+fatha": ["beh-ar", "fatha-ar"],
    "mark-base+damma": ["beh-ar", "damma-ar"],
    "mark-base+kasra": ["beh-ar", "kasra-ar"],
    "mark-shadda+sukun": ["beh-ar", "shadda-ar", "sukun-ar"],
    "mark-tanween": ["beh-ar", "fathatan-ar", "dammatan-ar", "kasratan-ar"],
    "mark-hamza-above-below": ["beh-ar", "hamzaabove-ar", "hamzabelow-ar"],
    "mark-dotted-circle": [
        "dottedCircle",
        "fatha-ar",
        "damma-ar",
        "kasra-ar",
        "fathatan-ar",
        "dammatan-ar",
        "kasratan-ar",
    ],
    "class-mark-combinations": [
        "beh-ar",
        "dottedCircle",
        "fatha-ar",
        "damma-ar",
        "kasra-ar",
        "fathatan-ar",
        "dammatan-ar",
        "kasratan-ar",
        "hamzaabove-ar",
        "hamzabelow-ar",
        "shadda-ar",
        "sukun-ar",
        "shaddaDamma-ar",
        "shaddaFatha-ar",
    ],
}


@dataclass(frozen=True)
class EditTarget:
    ufo: Path
    glyph_name: str
    path: Path | None
    source: str

    def markdown(self) -> str:
        if self.path is None:
            return f"`{self.ufo.name}` `{self.glyph_name}` -> missing"
        return (
            f"`{self.ufo.name}` `{self.glyph_name}` -> "
            f"`{self.path.relative_to(ROOT)}`"
        )


def glyph_maps() -> dict[Path, dict[str, Path]]:
    maps: dict[Path, dict[str, Path]] = {}
    for ufo in SOURCE_UFOS:
        contents_path = ufo / "glyphs/contents.plist"
        with contents_path.open("rb") as handle:
            contents = plistlib.load(handle)
        maps[ufo] = {
            glyph_name: ufo / "glyphs" / file_name
            for glyph_name, file_name in contents.items()
        }
    return maps


def targets_for_glyph_names(glyph_names: list[str], source: str) -> list[EditTarget]:
    maps = glyph_maps()
    targets: list[EditTarget] = []
    for glyph_name in glyph_names:
        for ufo in SOURCE_UFOS:
            targets.append(
                EditTarget(
                    ufo=ufo,
                    glyph_name=glyph_name,
                    path=maps[ufo].get(glyph_name),
                    source=source,
                )
            )
    return targets


def structure_prompt_targets() -> list[EditTarget]:
    targets: list[EditTarget] = []
    for prompt in runbook.grouped_structure_prompt_rows():
        codepoint = runbook.codepoint_int(prompt.codepoint)
        if codepoint is None:
            continue
        for target in runbook.source_targets_for_codepoint(codepoint):
            targets.append(
                EditTarget(
                    ufo=target.ufo,
                    glyph_name=target.glyph_name,
                    path=target.glif_path,
                    source=f"{prompt.codepoint} structure prompt",
                )
            )
    return targets


def visual_risk_targets() -> list[EditTarget]:
    text = runbook.read_text(runbook.ROOT / "documentation/glyph-review/arabic-visual-risk-audit.md")
    codepoints: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line == "## Grouped Visual Review Prompts":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("| `"):
            continue
        cells = runbook.split_markdown_row(line)
        if not cells:
            continue
        codepoints.append(runbook.clean_text(cells[0]))

    targets: list[EditTarget] = []
    for codepoint_text in codepoints:
        codepoint = runbook.codepoint_int(codepoint_text)
        if codepoint is None:
            continue
        for target in runbook.source_targets_for_codepoint(codepoint):
            targets.append(
                EditTarget(
                    ufo=target.ufo,
                    glyph_name=target.glyph_name,
                    path=target.glif_path,
                    source=f"{codepoint_text} visual-risk sidebearing prompt",
                )
            )
    return targets


def mark_targets_for_row(review_key: str) -> list[EditTarget]:
    lines: list[str] = []
    for row_key, _font, _sample, _glyph_sequence, source_targets in runbook.mark_prompt_detail_rows():
        if row_key == review_key or review_key == "class-mark-combinations":
            lines.extend(source_targets.split("<br>"))

    parsed: list[tuple[str, str, str]] = []
    pattern = re.compile(r"`([^`]+\.ufo)` `([^`]+)` -> `([^`]+)`")
    for line in lines:
        match = pattern.search(line)
        if match:
            parsed.append((match.group(1), match.group(2), match.group(3)))

    seen: set[tuple[str, str, str]] = set()
    targets: list[EditTarget] = []
    for ufo_name, glyph_name, rel_path in parsed:
        key = (ufo_name, glyph_name, rel_path)
        if key in seen:
            continue
        seen.add(key)
        targets.append(
            EditTarget(
                ufo=ROOT / "sources" / ufo_name,
                glyph_name=glyph_name,
                path=ROOT / rel_path,
                source=f"{review_key} mark prompt",
            )
        )
    return targets


def row_targets(review_key: str) -> list[EditTarget]:
    if review_key.startswith("proof-") and review_key.endswith("-glyphs"):
        return unique_targets(structure_prompt_targets())
    if review_key == "class-letter-structures":
        return unique_targets(structure_prompt_targets() + visual_risk_targets())
    if review_key.startswith("mark-") or review_key == "class-mark-combinations":
        return unique_targets(
            targets_for_glyph_names(MARK_REVIEW_GLYPHS.get(review_key, []), review_key)
            + mark_targets_for_row(review_key)
        )
    if review_key == "class-dot-stack-helpers":
        return unique_targets(targets_for_glyph_names(DOT_STACK_GLYPHS, review_key))
    if review_key == "class-arabic-farsi-numerals":
        return unique_targets(targets_for_glyph_names(ARABIC_FARSI_NUMERALS, review_key))
    if review_key == "class-arabic-punctuation":
        return unique_targets(targets_for_glyph_names(ARABIC_PUNCTUATION, review_key))
    return []


def unique_targets(targets: list[EditTarget]) -> list[EditTarget]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[EditTarget] = []
    for target in targets:
        path_key = str(target.path.relative_to(ROOT)) if target.path else "missing"
        key = (target.ufo.name, target.glyph_name, path_key)
        if key in seen:
            continue
        seen.add(key)
        unique.append(target)
    return unique


def target_summary(targets: list[EditTarget]) -> tuple[int, int]:
    existing = sum(1 for target in targets if target.path and target.path.exists())
    missing = len(targets) - existing
    return existing, missing


def markdown_report() -> str:
    rows = sorted(
        [row for row in runbook.visual_rows() if row.status in {"pending", "fix-needed"}],
        key=runbook.row_priority,
    )
    rows_with_targets = [(row, row_targets(row.key)) for row in rows]
    all_targets = [target for _row, targets in rows_with_targets for target in targets]
    existing, missing = target_summary(all_targets)

    lines = [
        "# Arabic Manual Edit Targets",
        "",
        "This generated report maps unresolved Arabic visual-review rows to",
        "likely source glyph files in both masters. Use it only after a row is",
        "marked `fix-needed`; it is not approval to edit drawings automatically",
        "and it does not replace the visual proof review.",
        "",
        "## Summary",
        "",
        f"- Pending/fix-needed review rows: {len(rows)}",
        f"- Source target references: {len(all_targets)}",
        f"- Existing source target files: {existing}",
        f"- Missing source target files: {missing}",
        "- Compatibility rule: edit Regular and Bold together, preserving contour structure.",
        "",
        "## Row Targets",
        "",
    ]

    for row, targets in rows_with_targets:
        existing_count, missing_count = target_summary(targets)
        lines.extend(
            [
                f"### `{row.key}`",
                "",
                f"- Area: {row.area}",
                f"- Review cue: {row.cue}",
                f"- Source targets: {existing_count} existing, {missing_count} missing",
            ]
        )
        if not targets:
            lines.append("- Edit target guidance: proof/smoke review row; record the exact glyphs in the visual review log if it becomes `fix-needed`.")
        else:
            by_source: dict[str, list[EditTarget]] = {}
            for target in targets:
                by_source.setdefault(target.source, []).append(target)
            for source, source_targets in by_source.items():
                lines.append(f"- {source}:")
                for target in source_targets:
                    lines.append(f"  - {target.markdown()}")
        lines.append("")

    lines.extend(
        [
            "## Regenerate",
            "",
            "```bash",
            "make arabic-manual-edit-targets",
            "make reports-only",
            "make preflight-only",
            "```",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
