#!/usr/bin/env python3
"""Report mechanical visual risks in built Arabic glyphs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
import unicodedata

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import glyphsets


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/arabic-visual-risk-audit.md")
GLYPHSET_NAME = "GF_Arabic_Core"
FONT_PATHS = [
    ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
CONTROL_CODEPOINTS = {0x200C, 0x200D, 0x200F}
EXTRA_REVIEW_CODEPOINTS = {0x25CC}


@dataclass(frozen=True)
class GlyphRisk:
    font_path: Path
    codepoint: int
    glyph_name: str
    advance: int
    bounds: tuple[float, float, float, float] | None
    risks: tuple[str, ...]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def display_char(codepoint: int) -> str:
    character = chr(codepoint)
    if character.isspace() or unicodedata.category(character).startswith(("C", "M")):
        return ""
    return character


def is_mark(codepoint: int) -> bool:
    return unicodedata.category(chr(codepoint)).startswith("M")


def is_visible_outline_expected(codepoint: int) -> bool:
    category = unicodedata.category(chr(codepoint))
    if codepoint in CONTROL_CODEPOINTS:
        return False
    if category.startswith("Z"):
        return False
    return True


def bounds_for_glyph(font: TTFont, glyph_name: str) -> tuple[float, float, float, float] | None:
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return pen.bounds


def risk_labels(
    codepoint: int,
    glyph_name: str,
    advance: int,
    bounds: tuple[float, float, float, float] | None,
    ascender: int,
    descender: int,
) -> tuple[str, ...]:
    risks: list[str] = []
    if bounds is None and is_visible_outline_expected(codepoint):
        risks.append("blank-visible-glyph")
    if not is_mark(codepoint) and codepoint not in CONTROL_CODEPOINTS and advance <= 0:
        risks.append("nonmark-zero-advance")
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
        left_sb = xmin
        right_sb = advance - xmax
        if ymin < descender - 64:
            risks.append("below-descender-margin")
        if ymax > ascender + 64:
            risks.append("above-ascender-margin")
        if not is_mark(codepoint) and left_sb < -96:
            risks.append("large-negative-left-sidebearing")
        if not is_mark(codepoint) and right_sb < -96:
            risks.append("large-negative-right-sidebearing")
        if xmax <= xmin or ymax <= ymin:
            risks.append("degenerate-bounds")
    if glyph_name == ".notdef":
        risks.append("maps-to-notdef")
    return tuple(risks)


def audit_font(font_path: Path, codepoints: set[int]) -> list[GlyphRisk]:
    font = TTFont(font_path)
    cmap = font.getBestCmap() or {}
    hmtx = font["hmtx"].metrics
    os2 = font["OS/2"]
    ascender = int(getattr(os2, "sTypoAscender", 832))
    descender = int(getattr(os2, "sTypoDescender", -256))
    rows: list[GlyphRisk] = []
    for codepoint in sorted(codepoints):
        glyph_name = cmap.get(codepoint, ".notdef")
        advance = int(hmtx.get(glyph_name, (0, 0))[0])
        bounds = bounds_for_glyph(font, glyph_name) if glyph_name != ".notdef" else None
        risks = risk_labels(codepoint, glyph_name, advance, bounds, ascender, descender)
        if risks:
            rows.append(
                GlyphRisk(
                    font_path=font_path,
                    codepoint=codepoint,
                    glyph_name=glyph_name,
                    advance=advance,
                    bounds=bounds,
                    risks=risks,
                )
            )
    font.close()
    return rows


def bounds_label(bounds: tuple[float, float, float, float] | None) -> str:
    if bounds is None:
        return "none"
    return ", ".join(str(int(value)) for value in bounds)


def markdown_report(font_paths: list[Path]) -> str:
    codepoints = set(glyphsets.unicodes_per_glyphset(GLYPHSET_NAME)) | EXTRA_REVIEW_CODEPOINTS
    risks = [risk for font_path in font_paths for risk in audit_font(font_path, codepoints)]
    risk_counts: dict[str, int] = {}
    for risk in risks:
        for label in risk.risks:
            risk_counts[label] = risk_counts.get(label, 0) + 1

    lines = [
        "# Arabic Visual Risk Audit",
        "",
        "This generated report catches mechanical visual risks before human",
        "Arabic proof review. It is not a substitute for native-reader review",
        "or hand inspection in Runebender; it only flags cases such as blank",
        "visible glyphs, `.notdef` mappings, suspicious advances, extreme",
        "bounds, and large negative sidebearings.",
        "",
        f"- Target glyphset: `{GLYPHSET_NAME}` plus U+25CC dotted circle",
        f"- Fonts checked: {len(font_paths)}",
        f"- Codepoints checked per font: {len(codepoints)}",
        f"- Risk rows: {len(risks)}",
        "",
        "## Risk Counts",
        "",
        "| Risk | Rows |",
        "| --- | ---: |",
    ]
    if risk_counts:
        for label, count in sorted(risk_counts.items()):
            lines.append(f"| `{label}` | {count} |")
    else:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Risk Rows",
            "",
            "| Font | Codepoint | Character | Name | Glyph | Advance | Bounds | Risks |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for risk in risks:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{display_path(risk.font_path)}`",
                    f"U+{risk.codepoint:04X}",
                    display_char(risk.codepoint),
                    unicodedata.name(chr(risk.codepoint), "UNKNOWN"),
                    f"`{risk.glyph_name}`",
                    str(risk.advance),
                    bounds_label(risk.bounds),
                    ", ".join(f"`{label}`" for label in risk.risks),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- `blank-visible-glyph` and `maps-to-notdef` are likely source/build bugs.",
            "- `nonmark-zero-advance` is a spacing risk for letters, numbers, or punctuation.",
            "- Vertical-bound and sidebearing rows are review prompts, not automatic failures.",
            "- If this report is clean, continue with `documentation/arabic-visual-review-log.md`",
            "  and the GF proof HTML; it does not prove the drawings are culturally or",
            "  stylistically correct.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_arabic_visual_risk.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(FONT_PATHS), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
