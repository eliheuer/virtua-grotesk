#!/usr/bin/env python3
"""Report missing GF Arabic Core codepoints for a built font."""

from pathlib import Path
import sys
import unicodedata

from fontTools.ttLib import TTFont
import glyphsets


GLYPHSET_NAME = "GF_Arabic_Core"
COVERAGE_NOTE = (
    "Google Fonts uses the `glyphsets` package for authoring glyphset "
    "definitions. For this family, Arabic support means the first submission "
    "must cover `GF_Arabic_Core` at minimum, in addition to the Latin coverage "
    "target already tracked separately. This report checks Unicode cmap "
    "coverage only; contextual forms, mark behavior, and OpenType layout are "
    "tracked in the Arabic shaping smoke test and still need visual proofing."
)
CATEGORY_ORDER = [
    "Arabic letters",
    "Arabic marks",
    "Arabic numbers",
    "Arabic punctuation and symbols",
    "Shared punctuation and symbols",
]


def font_codepoints(font_path: Path) -> set[int]:
    font = TTFont(font_path)
    codepoints = set()
    for table in font["cmap"].tables:
        codepoints.update(table.cmap.keys())
    font.close()
    return codepoints


def display_character(codepoint: int) -> str:
    char = chr(codepoint)
    if char.isspace() or unicodedata.category(char).startswith("M"):
        return ""
    return char.replace("|", "\\|")


def codepoint_category(codepoint: int) -> str:
    unicode_category = unicodedata.category(chr(codepoint))
    if 0x0600 <= codepoint <= 0x06FF or 0x0750 <= codepoint <= 0x077F:
        if unicode_category.startswith("L"):
            return "Arabic letters"
        if unicode_category.startswith("M"):
            return "Arabic marks"
        if unicode_category.startswith("N"):
            return "Arabic numbers"
        return "Arabic punctuation and symbols"
    return "Shared punctuation and symbols"


def table_rows(codepoints: list[int]) -> list[str]:
    rows = [
        "| Codepoint | Character | Unicode name |",
        "| --- | --- | --- |",
    ]
    for codepoint in codepoints:
        rows.append(
            "| U+{} | {} | {} |".format(
                f"{codepoint:04X}",
                display_character(codepoint),
                unicodedata.name(chr(codepoint), "UNKNOWN"),
            )
        )
    return rows


def markdown_report(font_path: Path) -> str:
    required = set(glyphsets.unicodes_per_glyphset(GLYPHSET_NAME))
    present = font_codepoints(font_path)
    missing = sorted(required - present)
    categorized_missing = {
        category: [cp for cp in missing if codepoint_category(cp) == category]
        for category in CATEGORY_ORDER
    }

    lines = [
        "# Missing GF Arabic Core Codepoints",
        "",
        f"Font: `{font_path}`",
        f"GF Arabic Core required codepoints: {len(required)}",
        f"Missing codepoints: {len(missing)}",
        "",
        COVERAGE_NOTE,
        "",
        "## Submission target",
        "",
        "- Minimum Arabic authoring glyphset: `GF_Arabic_Core`",
        "- Installed `glyphsets` required codepoints: {}".format(len(required)),
        "- Current built-font gap: {}".format(len(missing)),
        "- Coverage source: `glyphsets.unicodes_per_glyphset(\"GF_Arabic_Core\")`",
        "",
    ]

    for category in CATEGORY_ORDER:
        codepoints = categorized_missing[category]
        lines.extend(
            [
                f"## {category}",
                "",
                f"Missing: {len(codepoints)}",
                "",
            ]
        )
        if codepoints:
            lines.extend(table_rows(codepoints))
            lines.append("")

    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    font_path = Path(argv[1]) if len(argv) > 1 else Path("fonts/variable/VirtuaGrotesk[wght].ttf")
    output_path = Path(argv[2]) if len(argv) > 2 else None
    try:
        report = markdown_report(font_path)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
