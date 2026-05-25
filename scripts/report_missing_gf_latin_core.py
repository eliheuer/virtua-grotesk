#!/usr/bin/env python3
"""Report missing GF Latin Core codepoints for a built font."""

from pathlib import Path
import sys
import unicodedata

from fontTools.ttLib import TTFont
import glyphsets


def font_codepoints(font_path: Path) -> set[int]:
    font = TTFont(font_path)
    codepoints = set()
    for table in font["cmap"].tables:
        codepoints.update(table.cmap.keys())
    font.close()
    return codepoints


def markdown_report(font_path: Path) -> str:
    required = set(glyphsets.unicodes_per_glyphset("GF_Latin_Core"))
    present = font_codepoints(font_path)
    missing = sorted(required - present)

    lines = [
        "# Missing GF Latin Core Codepoints",
        "",
        f"Font: `{font_path}`",
        f"GF Latin Core required codepoints: {len(required)}",
        f"Missing codepoints: {len(missing)}",
        "",
        "| Codepoint | Character | Unicode name |",
        "| --- | --- | --- |",
    ]
    for cp in missing:
        char = chr(cp)
        display = char
        if char.isspace() or unicodedata.category(char).startswith("M"):
            display = ""
        display = display.replace("|", "\\|")
        lines.append(
            f"| U+{cp:04X} | {display} | {unicodedata.name(char, 'UNKNOWN')} |"
        )
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
