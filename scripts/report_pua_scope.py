#!/usr/bin/env python3
"""Report Private Use Area codepoints in built fonts and UFO sources."""

from __future__ import annotations

from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont


DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
SOURCE_UFOS = [
    Path("sources/VirtuaGrotesk-Regular.ufo"),
    Path("sources/VirtuaGrotesk-Bold.ufo"),
]
PUA_START = 0xE000
PUA_END = 0xF8FF
GF_PRECEDENT_FONTS = [
    Path("ofl/scheherazadenew/ScheherazadeNew-Regular.ttf"),
    Path("ofl/kedebideri/Kedebideri-Regular.ttf"),
    Path("ofl/inika/Inika-Regular.ttf"),
    Path("ofl/signikanegative/SignikaNegative[wght].ttf"),
]


def font_pua_map(font_path: Path) -> dict[int, str]:
    font = TTFont(font_path)
    cmap = font.getBestCmap() or {}
    font.close()
    return {cp: name for cp, name in sorted(cmap.items()) if PUA_START <= cp <= PUA_END}


def source_pua_map(ufo_path: Path) -> dict[int, str]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    with contents_path.open("rb") as file:
        contents = plistlib.load(file)

    result: dict[int, str] = {}
    for glyph_name, file_name in contents.items():
        glif_path = ufo_path / "glyphs" / file_name
        try:
            root = ET.parse(glif_path).getroot()
        except ET.ParseError:
            continue
        for unicode_el in root.findall("unicode"):
            value = unicode_el.attrib.get("hex")
            if not value:
                continue
            codepoint = int(value, 16)
            if PUA_START <= codepoint <= PUA_END:
                result[codepoint] = glyph_name
    return dict(sorted(result.items()))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def google_fonts_precedents(gf_repo: Path = DEFAULT_GF_REPO) -> list[tuple[Path, int, int | None, int | None]]:
    rows: list[tuple[Path, int, int | None, int | None]] = []
    for relative_path in GF_PRECEDENT_FONTS:
        font_path = gf_repo / relative_path
        if not font_path.exists():
            rows.append((relative_path, 0, None, None))
            continue
        mapping = font_pua_map(font_path)
        codepoints = sorted(mapping)
        rows.append(
            (
                relative_path,
                len(codepoints),
                codepoints[0] if codepoints else None,
                codepoints[-1] if codepoints else None,
            )
        )
    return rows


def codepoint_label(codepoint: int | None) -> str:
    return "missing" if codepoint is None else f"U+{codepoint:04X}"


def markdown_report(font_paths: list[Path]) -> str:
    font_maps = {path: font_pua_map(path) for path in font_paths}
    source_maps = {path: source_pua_map(path) for path in SOURCE_UFOS}
    variable_path = font_paths[0]
    variable_pua = font_maps[variable_path]
    all_codepoints = sorted(
        {
            *variable_pua.keys(),
            *(cp for mapping in font_maps.values() for cp in mapping),
            *(cp for mapping in source_maps.values() for cp in mapping),
        }
    )

    lines = [
        "# Private-Use Glyph Scope",
        "",
        f"Primary font: `{variable_path}`",
        f"Variable font PUA codepoints: {len(variable_pua)}",
        "",
        (
            "This report inventories encoded Unicode Private Use Area glyphs "
            "from U+E000 through U+F8FF. PUA scope is a maintainer decision for "
            "Google Fonts review because these glyphs are not covered by public "
            "Unicode semantics."
        ),
        "",
        "## Google Fonts Review Impact",
        "",
        "- PUA glyphs can affect Fontspector `unreachable_glyphs` warnings.",
        "- PUA glyphs can affect `googlefonts/metadata/unreachable_subsetting` warnings.",
        "- If these glyphs stay in the first submission, document why they should remain encoded and reachable.",
        "- If these glyphs are removed or deferred, regenerate this report and the downstream package preview.",
        "- Local Google Fonts package precedent shows PUA can ship, but usually with a small, family-specific rationale.",
        "",
        "## Local Google Fonts PUA Precedent",
        "",
        "This is a limited local checkout sample, not a policy exemption. Use it",
        "only to frame the maintainer decision and any issue/PR rationale.",
        "",
        "| Google Fonts package font | PUA codepoints | Min | Max |",
        "| --- | ---: | --- | --- |",
    ]

    for font_path, count, min_cp, max_cp in google_fonts_precedents():
        lines.append(
            f"| `{font_path}` | {count} | {codepoint_label(min_cp)} | {codepoint_label(max_cp)} |"
        )

    lines.extend(
        [
        "",
        "## Source Coverage Summary",
        "",
        "| Source | PUA codepoints | Matches variable cmap |",
        "| --- | ---: | --- |",
        ]
    )

    variable_set = set(variable_pua)
    for ufo_path, mapping in source_maps.items():
        lines.append(
            f"| `{ufo_path}` | {len(mapping)} | {yes_no(set(mapping) == variable_set)} |"
        )

    lines.extend(
        [
            "",
            "## Built Font Summary",
            "",
            "| Font | PUA codepoints | Matches variable cmap |",
            "| --- | ---: | --- |",
        ]
    )
    for font_path, mapping in font_maps.items():
        lines.append(
            f"| `{font_path}` | {len(mapping)} | {yes_no(set(mapping) == variable_set)} |"
        )

    lines.extend(
        [
            "",
            "## PUA Codepoint Inventory",
            "",
            "| Codepoint | Variable glyph | Regular source glyph | Bold source glyph | Present in all built fonts |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    regular_source = source_maps[SOURCE_UFOS[0]]
    bold_source = source_maps[SOURCE_UFOS[1]]
    for codepoint in all_codepoints:
        present_all = all(codepoint in mapping for mapping in font_maps.values())
        lines.append(
            "| U+{codepoint:04X} | `{variable}` | `{regular}` | `{bold}` | {present_all} |".format(
                codepoint=codepoint,
                variable=variable_pua.get(codepoint, "missing"),
                regular=regular_source.get(codepoint, "missing"),
                bold=bold_source.get(codepoint, "missing"),
                present_all=yes_no(present_all),
            )
        )

    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[list[Path], Path | None]:
    if len(argv) == 1:
        return DEFAULT_FONT_PATHS, None
    paths = [Path(arg) for arg in argv[1:]]
    output_path = paths[-1] if paths[-1].suffix.lower() == ".md" else None
    font_paths = paths[:-1] if output_path else paths
    return font_paths, output_path


def main(argv: list[str]) -> int:
    font_paths, output_path = parse_args(argv)
    try:
        report = markdown_report(font_paths)
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
