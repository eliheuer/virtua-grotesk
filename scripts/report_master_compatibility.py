#!/usr/bin/env python3
"""Report interpolation compatibility between the Regular and Bold UFO masters."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET


DEFAULT_REGULAR_UFO = Path("sources/VirtuaGrotesk-Regular.ufo")
DEFAULT_BOLD_UFO = Path("sources/VirtuaGrotesk-Bold.ufo")


@dataclass(frozen=True)
class GlyphStructure:
    unicodes: tuple[str, ...]
    width: str
    contours: tuple[tuple[str, ...], ...]
    components: tuple[str, ...]
    anchors: tuple[str, ...]


def glyph_paths(ufo_path: Path) -> dict[str, Path]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    contents = plistlib.loads(contents_path.read_bytes())
    return {
        glyph_name: ufo_path / "glyphs" / filename
        for glyph_name, filename in contents.items()
    }


def point_type(point: ET.Element) -> str:
    return point.attrib.get("type", "offcurve")


def glyph_structure(path: Path) -> GlyphStructure:
    root = ET.parse(path).getroot()
    unicodes = tuple(sorted(element.attrib["hex"] for element in root.findall("unicode")))
    advance = root.find("advance")
    width = advance.attrib.get("width", "") if advance is not None else ""
    outline = root.find("outline")
    contours: list[tuple[str, ...]] = []
    components: list[str] = []
    if outline is not None:
        for contour in outline.findall("contour"):
            contours.append(tuple(point_type(point) for point in contour.findall("point")))
        for component in outline.findall("component"):
            components.append(component.attrib.get("base", ""))
    anchors = tuple(sorted(anchor.attrib.get("name", "") for anchor in root.findall("anchor")))
    return GlyphStructure(
        unicodes=unicodes,
        width=width,
        contours=tuple(contours),
        components=tuple(components),
        anchors=anchors,
    )


def contour_summary(structure: GlyphStructure) -> str:
    if not structure.contours:
        return "0"
    return ", ".join(str(len(contour)) for contour in structure.contours)


def component_summary(structure: GlyphStructure) -> str:
    return ", ".join(structure.components) if structure.components else "none"


def compatibility_rows(regular_ufo: Path, bold_ufo: Path) -> tuple[list[str], dict[str, int]]:
    regular_paths = glyph_paths(regular_ufo)
    bold_paths = glyph_paths(bold_ufo)
    all_glyphs = sorted(set(regular_paths) | set(bold_paths))
    rows: list[str] = []
    counts = {
        "missing_in_regular": 0,
        "missing_in_bold": 0,
        "unicode_mismatch": 0,
        "contour_mismatch": 0,
        "component_mismatch": 0,
        "anchor_mismatch": 0,
        "width_only": 0,
    }

    for glyph_name in all_glyphs:
        regular_path = regular_paths.get(glyph_name)
        bold_path = bold_paths.get(glyph_name)
        if regular_path is None:
            counts["missing_in_regular"] += 1
            rows.append(f"| `{glyph_name}` | Missing in Regular |  |  |")
            continue
        if bold_path is None:
            counts["missing_in_bold"] += 1
            rows.append(f"| `{glyph_name}` | Missing in Bold |  |  |")
            continue

        regular = glyph_structure(regular_path)
        bold = glyph_structure(bold_path)
        issues = []
        details = []
        if regular.unicodes != bold.unicodes:
            counts["unicode_mismatch"] += 1
            issues.append("Unicode mismatch")
            details.append(f"Regular {regular.unicodes or 'none'} / Bold {bold.unicodes or 'none'}")
        if regular.contours != bold.contours:
            counts["contour_mismatch"] += 1
            issues.append("Contour structure mismatch")
            details.append(f"Regular points [{contour_summary(regular)}] / Bold points [{contour_summary(bold)}]")
        if regular.components != bold.components:
            counts["component_mismatch"] += 1
            issues.append("Component mismatch")
            details.append(f"Regular {component_summary(regular)} / Bold {component_summary(bold)}")
        if regular.anchors != bold.anchors:
            counts["anchor_mismatch"] += 1
            issues.append("Anchor mismatch")
            details.append(f"Regular {regular.anchors or 'none'} / Bold {bold.anchors or 'none'}")
        if regular.width != bold.width and not issues:
            counts["width_only"] += 1

        if issues:
            rows.append(
                "| `{}` | {} | {} | {} |".format(
                    glyph_name,
                    "<br>".join(issues),
                    "<br>".join(details),
                    "Must match for variable interpolation.",
                )
            )

    return rows, counts


def markdown_report(regular_ufo: Path, bold_ufo: Path) -> str:
    rows, counts = compatibility_rows(regular_ufo, bold_ufo)
    blocking = sum(counts[key] for key in counts if key != "width_only")
    lines = [
        "# Master Compatibility Report",
        "",
        f"Regular master: `{regular_ufo}`",
        f"Bold master: `{bold_ufo}`",
        "",
        f"Blocking structure mismatches: {blocking}",
        f"Width-only differences: {counts['width_only']}",
        "",
        "This report checks glyph-set presence, Unicode assignments, contour point "
        "types/counts, component bases, and anchors. Width differences are expected "
        "across the Weight axis and are reported separately.",
        "",
        "## Summary",
        "",
        "| Category | Count |",
        "| --- | ---: |",
        f"| Missing in Regular | {counts['missing_in_regular']} |",
        f"| Missing in Bold | {counts['missing_in_bold']} |",
        f"| Unicode mismatches | {counts['unicode_mismatch']} |",
        f"| Contour structure mismatches | {counts['contour_mismatch']} |",
        f"| Component mismatches | {counts['component_mismatch']} |",
        f"| Anchor mismatches | {counts['anchor_mismatch']} |",
        f"| Width-only differences | {counts['width_only']} |",
        "",
        "## Blocking Mismatches",
        "",
    ]
    if rows:
        lines.extend(
            [
                "| Glyph | Issue | Detail | Action |",
                "| --- | --- | --- | --- |",
                *rows,
                "",
            ]
        )
    else:
        lines.extend(["No blocking master-compatibility mismatches found.", ""])
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    regular_ufo = Path(argv[1]) if len(argv) > 1 else DEFAULT_REGULAR_UFO
    bold_ufo = Path(argv[2]) if len(argv) > 2 else DEFAULT_BOLD_UFO
    output_path = Path(argv[3]) if len(argv) > 3 else None
    try:
        report = markdown_report(regular_ufo, bold_ufo)
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
