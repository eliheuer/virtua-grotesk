#!/usr/bin/env python3
"""Report basic Arabic shaping behavior for built fonts."""

from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont
import uharfbuzz as hb


DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
SAMPLES = [
    ("salaam", "سلام", True, True),
    ("arabic", "العربية", True, False),
    ("bismillah", "بسم الله", True, False),
    ("lam_alef", "لا", False, True),
]


def font_features(font: TTFont) -> list[str]:
    if "GSUB" not in font:
        return []
    feature_list = font["GSUB"].table.FeatureList
    if feature_list is None:
        return []
    return sorted({record.FeatureTag for record in feature_list.FeatureRecord})


def layout_scripts(font: TTFont, table_tag: str) -> dict[str, list[str]]:
    if table_tag not in font:
        return {}
    script_list = getattr(font[table_tag].table, "ScriptList", None)
    if script_list is None:
        return {}
    scripts: dict[str, list[str]] = {}
    for script_record in script_list.ScriptRecord:
        language_tags = []
        if script_record.Script.DefaultLangSys is not None:
            language_tags.append("dflt")
        language_tags.extend(record.LangSysTag for record in script_record.Script.LangSysRecord)
        scripts[script_record.ScriptTag] = sorted(language_tags)
    return scripts


def format_scripts(scripts: dict[str, list[str]]) -> str:
    if not scripts:
        return "none"
    return ", ".join(f"{script}: {'/'.join(languages)}" for script, languages in sorted(scripts.items()))


def shape(font_path: Path, text: str, glyph_order: list[str]) -> list[str]:
    data = font_path.read_bytes()
    face = hb.Face(data)
    font = hb.Font(face)
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.direction = "rtl"
    buffer.script = "Arab"
    buffer.language = "ar"
    hb.shape(font, buffer, {})

    glyphs = []
    for info in buffer.glyph_infos:
        if info.codepoint < len(glyph_order):
            glyphs.append(glyph_order[info.codepoint])
        else:
            glyphs.append(f"gid{info.codepoint}")
    return glyphs


def has_contextual_forms(glyphs: list[str]) -> bool:
    return any(glyph.endswith((".init", ".medi", ".fina")) for glyph in glyphs)


def has_lam_alef_ligature(glyphs: list[str]) -> bool:
    return any(glyph.startswith("uni06440627") for glyph in glyphs)


def font_report(font_path: Path) -> list[str]:
    font = TTFont(font_path)
    glyph_order = font.getGlyphOrder()
    features = font_features(font)
    gsub_scripts = layout_scripts(font, "GSUB")
    gpos_scripts = layout_scripts(font, "GPOS")
    has_gsub = "GSUB" in font
    has_arab_gsub = "arab" in gsub_scripts and "dflt" in gsub_scripts["arab"]
    has_arab_gpos = "arab" in gpos_scripts and "dflt" in gpos_scripts["arab"]
    font.close()

    lines = [
        f"## {font_path}",
        "",
        f"Font: `{font_path}`",
        f"Has GSUB: `{str(has_gsub).lower()}`",
        f"GSUB features: `{', '.join(features) if features else 'none'}`",
        f"GSUB script records: `{format_scripts(gsub_scripts)}`",
        f"GSUB has `arab/dflt`: `{'true' if has_arab_gsub else 'false'}`",
        f"GPOS script records: `{format_scripts(gpos_scripts)}`",
        f"GPOS has `arab/dflt`: `{'true' if has_arab_gpos else 'false'}`",
        "HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`",
        "",
        "| Sample | Text | Shaped glyph sequence | `.notdef` count | Contextual forms expected | Contextual forms present | Lam-alef expected | Lam-alef ligature present |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for label, text, expects_contextual, expects_lam_alef in SAMPLES:
        glyphs = shape(font_path, text, glyph_order)
        notdef_count = glyphs.count(".notdef")
        contextual_forms = has_contextual_forms(glyphs)
        lam_alef_ligature = has_lam_alef_ligature(glyphs)
        lines.append(
            "| `{}` | {} | `{}` | {} | {} | {} | {} | {} |".format(
                label,
                text,
                " ".join(glyphs),
                notdef_count,
                "yes" if expects_contextual else "no",
                "yes" if contextual_forms else "no",
                "yes" if expects_lam_alef else "no",
                "yes" if lam_alef_ligature else "no",
            )
        )

    lines.append("")
    return lines


def markdown_report(font_paths: list[Path]) -> str:
    lines = [
        "# Arabic Shaping Smoke Test",
        "",
        (
            "This report smoke-tests Arabic layout plumbing in every generated "
            "Google Fonts handoff font: the variable font and all static TTFs. "
            "It proves the built fonts emit Arabic GSUB tables and that HarfBuzz "
            "reaches contextual forms or required ligatures for representative "
            "strings. It does not replace visual proofing or language review."
        ),
        "",
    ]
    for font_path in font_paths:
        lines.extend(font_report(font_path))
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output_path = None
    font_paths = DEFAULT_FONT_PATHS
    if len(argv) == 2:
        font_paths = [Path(argv[1])]
    elif len(argv) > 2:
        font_paths = [Path(path) for path in argv[1:-1]]
        output_path = Path(argv[-1])
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
