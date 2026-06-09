#!/usr/bin/env python3
"""Report Arabic mark and dotted-circle readiness for Google Fonts handoff."""

from __future__ import annotations

from pathlib import Path
import plistlib
import sys
import unicodedata
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont
import glyphsets


ROOT = Path(__file__).resolve().parents[1]
GLYPHSET_NAME = "GF_Arabic_Core"
VARIABLE_FONT = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"
FONT_PATHS = [
    VARIABLE_FONT,
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
UFO_PATHS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def required_arabic_marks() -> list[int]:
    return sorted(
        cp
        for cp in glyphsets.unicodes_per_glyphset(GLYPHSET_NAME)
        if unicodedata.category(chr(cp)).startswith("M")
        and (0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF)
    )


def font_cmap(font_path: Path) -> dict[int, str]:
    font = TTFont(font_path)
    cmap = font.getBestCmap() or {}
    font.close()
    return cmap


def font_layout_row(font_path: Path) -> str:
    font = TTFont(font_path)
    gdef_mark_count = 0
    if "GDEF" in font and font["GDEF"].table.GlyphClassDef:
        gdef_mark_count = sum(
            1 for value in font["GDEF"].table.GlyphClassDef.classDefs.values() if value == 3
        )
    gpos_features = []
    if "GPOS" in font and font["GPOS"].table.FeatureList:
        gpos_features = sorted(
            {record.FeatureTag for record in font["GPOS"].table.FeatureList.FeatureRecord}
        )
    font.close()
    has_mark_features = bool({"mark", "mkmk"} & set(gpos_features))
    return "| `{}` | {} | {} | {} | `{}` | {} |".format(
        relative(font_path),
        "yes" if gdef_mark_count else "no",
        gdef_mark_count,
        "yes" if gpos_features else "no",
        ", ".join(gpos_features) if gpos_features else "none",
        "yes" if has_mark_features else "no",
    )


def source_anchors(ufo_path: Path) -> dict[str, tuple[str, ...]]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    contents = plistlib.loads(contents_path.read_bytes())
    anchors: dict[str, tuple[str, ...]] = {}
    for glyph_name, filename in contents.items():
        glif_path = ufo_path / "glyphs" / filename
        if not glif_path.exists():
            continue
        root = ET.parse(glif_path).getroot()
        names = tuple(sorted(anchor.attrib.get("name", "") for anchor in root.findall("anchor")))
        if names:
            anchors[glyph_name] = names
    return anchors


def source_glyphs_by_unicode(ufo_path: Path) -> dict[int, str]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    contents = plistlib.loads(contents_path.read_bytes())
    glyphs: dict[int, str] = {}
    for glyph_name, filename in contents.items():
        glif_path = ufo_path / "glyphs" / filename
        if not glif_path.exists():
            continue
        root = ET.parse(glif_path).getroot()
        for unicode_node in root.findall("unicode"):
            hex_value = unicode_node.attrib.get("hex")
            if hex_value:
                glyphs[int(hex_value, 16)] = glyph_name
    return glyphs


def source_anchor_row(ufo_path: Path, required_mark_glyphs: set[str]) -> str:
    anchors = source_anchors(ufo_path)
    mark_glyphs_with_anchors = sorted(set(anchors) & required_mark_glyphs)
    return "| `{}` | {} | {} | `{}` |".format(
        relative(ufo_path),
        len(anchors),
        len(mark_glyphs_with_anchors),
        ", ".join(mark_glyphs_with_anchors) if mark_glyphs_with_anchors else "none",
    )


def mark_rows(
    cmap: dict[int, str],
    source_anchor_maps: dict[str, dict[str, tuple[str, ...]]],
    source_mark_maps: dict[str, dict[int, str]],
) -> list[str]:
    rows = [
        "| Codepoint | Character | Unicode name | Glyph | Present | Source anchors |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for cp in required_arabic_marks():
        glyph_name = cmap.get(cp, "")
        anchor_parts = []
        for source_name, anchors in source_anchor_maps.items():
            source_glyph_name = source_mark_maps[source_name].get(cp, glyph_name)
            names = anchors.get(source_glyph_name, ())
            anchor_parts.append(f"{source_name}: {', '.join(names) if names else 'none'}")
        rows.append(
            "| U+{} | {} | {} | `{}` | {} | {} |".format(
                f"{cp:04X}",
                "" if unicodedata.category(chr(cp)).startswith("M") else chr(cp),
                unicodedata.name(chr(cp), "UNKNOWN"),
                glyph_name or ".notdef",
                "yes" if glyph_name else "no",
                "<br>".join(anchor_parts),
            )
        )
    return rows


def markdown_report() -> str:
    cmap = font_cmap(VARIABLE_FONT)
    required_marks = required_arabic_marks()
    present_marks = [cp for cp in required_marks if cp in cmap]
    missing_marks = [cp for cp in required_marks if cp not in cmap]
    source_anchor_maps = {ufo_path.name: source_anchors(ufo_path) for ufo_path in UFO_PATHS}
    source_mark_maps = {ufo_path.name: source_glyphs_by_unicode(ufo_path) for ufo_path in UFO_PATHS}
    required_mark_glyphs = {
        source_glyph
        for source_map in source_mark_maps.values()
        for cp in present_marks
        if (source_glyph := source_map.get(cp))
    }
    dotted_circle_present = 0x25CC in cmap
    has_any_source_anchors = any(source_anchor_maps[ufo.name] for ufo in UFO_PATHS)
    has_mark_positioning = False
    for font_path in FONT_PATHS:
        font = TTFont(font_path)
        if "GPOS" in font and font["GPOS"].table.FeatureList:
            features = {record.FeatureTag for record in font["GPOS"].table.FeatureList.FeatureRecord}
            has_mark_positioning = has_mark_positioning or bool({"mark", "mkmk"} & features)
        font.close()

    lines = [
        "# Arabic Mark Readiness",
        "",
        (
            "This report tracks the non-drawing setup needed for Arabic combining "
            "marks in the Google Fonts submission. It complements the Arabic Core "
            "codepoint report and the shaping smoke test; it does not replace "
            "visual proofing or language review."
        ),
        "",
        "## Summary",
        "",
        f"- Minimum Arabic target: `{GLYPHSET_NAME}`",
        f"- Required Arabic combining marks in `{GLYPHSET_NAME}`: {len(required_marks)}",
        f"- Present in current variable-font cmap: {len(present_marks)}",
        f"- Missing from current variable-font cmap: {len(missing_marks)}",
        f"- U+25CC dotted circle present: {'yes' if dotted_circle_present else 'no'}",
        f"- Source anchors present: {'yes' if has_any_source_anchors else 'no'}",
        f"- Built mark/mkmk GPOS features present: {'yes' if has_mark_positioning else 'no'}",
        "",
        "## Built Layout Tables",
        "",
        "| Font | GDEF marks | GDEF mark count | GPOS present | GPOS features | mark/mkmk present |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    lines.extend(font_layout_row(path) for path in FONT_PATHS)
    lines.extend(
        [
            "",
            "## Source Anchors",
            "",
            "| UFO | Glyphs with anchors | Required Arabic mark glyphs with anchors | Required mark glyph names |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    lines.extend(source_anchor_row(path, required_mark_glyphs) for path in UFO_PATHS)
    lines.extend(
        [
            "",
            "## Required Arabic Marks",
            "",
            *mark_rows(cmap, source_anchor_maps, source_mark_maps),
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output_path = Path(argv[1]) if len(argv) > 1 else None
    try:
        report = markdown_report()
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
