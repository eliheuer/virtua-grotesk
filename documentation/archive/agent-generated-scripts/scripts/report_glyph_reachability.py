#!/usr/bin/env python3
"""Report glyphs that are not reachable by cmap, GSUB output, or components."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import sys

from fontTools.ttLib import TTFont


DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
OUTPUT_DEFAULT = Path("documentation/google-fonts/glyph-reachability.md")


def gsub_output_glyphs(font: TTFont) -> set[str]:
    if "GSUB" not in font:
        return set()

    outputs: set[str] = set()
    lookup_list = font["GSUB"].table.LookupList
    if lookup_list is None:
        return outputs

    for lookup in lookup_list.Lookup:
        for subtable in lookup.SubTable:
            if hasattr(subtable, "mapping"):
                for value in subtable.mapping.values():
                    if isinstance(value, str):
                        outputs.add(value)
                    else:
                        outputs.update(glyph for glyph in value if isinstance(glyph, str))
            if hasattr(subtable, "alternates"):
                for alternates in subtable.alternates.values():
                    outputs.update(alternates)
            if hasattr(subtable, "ligatures"):
                for ligatures in subtable.ligatures.values():
                    outputs.update(ligature.LigGlyph for ligature in ligatures)
            if hasattr(subtable, "substitutes"):
                outputs.update(subtable.substitutes)
    return outputs


def glyph_category(glyph_name: str) -> str:
    if glyph_name.startswith("uniE") or glyph_name.startswith("uE"):
        return "PUA/private-use"
    if "dot" in glyph_name or "wasla" in glyph_name:
        return "Arabic mark helper"
    if glyph_name.endswith("ar") or "ar." in glyph_name or glyph_name.startswith("uni06"):
        return "Arabic helper/form"
    return "source cleanup"


def component_closure(font: TTFont, seed_glyphs: set[str]) -> set[str]:
    if "glyf" not in font:
        return set()
    glyph_order = set(font.getGlyphOrder())
    glyf = font["glyf"]
    reachable_components: set[str] = set()
    pending = [glyph for glyph in seed_glyphs if glyph in glyph_order]
    seen = set(pending)

    while pending:
        glyph_name = pending.pop()
        glyph = glyf[glyph_name]
        if not glyph.isComposite():
            continue
        for component in glyph.components:
            component_name = component.glyphName
            if component_name in reachable_components:
                continue
            reachable_components.add(component_name)
            if component_name not in seen and component_name in glyph_order:
                seen.add(component_name)
                pending.append(component_name)
    return reachable_components


def font_reachability(font_path: Path) -> tuple[set[str], set[str], set[str], list[str]]:
    font = TTFont(font_path)
    try:
        cmap_glyphs = set(font.getBestCmap().values())
        gsub_glyphs = gsub_output_glyphs(font)
        component_glyphs = component_closure(font, cmap_glyphs | gsub_glyphs | {".notdef"})
        reachable = cmap_glyphs | gsub_glyphs | component_glyphs | {".notdef"}
        unreachable = [glyph for glyph in font.getGlyphOrder() if glyph not in reachable]
        return cmap_glyphs, gsub_glyphs, component_glyphs, unreachable
    finally:
        font.close()


def markdown_report(font_paths: list[Path]) -> str:
    rows: list[str] = []
    all_unreachable: set[str] = set()
    all_component_glyphs: set[str] = set()
    category_counts: Counter[str] = Counter()
    unique_category_counts: Counter[str] = Counter()
    per_font_counts: dict[str, tuple[int, int, int]] = {}
    glyph_to_fonts: dict[str, list[str]] = defaultdict(list)

    for font_path in font_paths:
        cmap_glyphs, gsub_glyphs, component_glyphs, unreachable = font_reachability(font_path)
        all_component_glyphs.update(component_glyphs)
        per_font_counts[str(font_path)] = (len(cmap_glyphs), len(gsub_glyphs), len(unreachable))
        for glyph_name in unreachable:
            all_unreachable.add(glyph_name)
            category_counts[glyph_category(glyph_name)] += 1
            glyph_to_fonts[glyph_name].append(str(font_path))

    for glyph_name in all_unreachable:
        unique_category_counts[glyph_category(glyph_name)] += 1

    lines = [
        "# Glyph Reachability",
        "",
        "This generated report checks which built glyphs are not reachable from",
        "Unicode cmap entries, direct GSUB substitution outputs, or component",
        "references from those glyphs. It complements Fontspector's",
        "`unreachable_glyphs` and",
        "`googlefonts/metadata/unreachable_subsetting` warnings so Arabic helper",
        "glyphs, private-use glyphs, and final feature coverage can be reviewed",
        "deliberately before downstream packaging.",
        "",
        "## Summary",
        "",
        f"- Fonts checked: {len(font_paths)}",
        f"- Unique unreachable glyphs: {len(all_unreachable)}",
        f"- Unique Arabic helper/form glyphs: {unique_category_counts.get('Arabic helper/form', 0)}",
        f"- Unique Arabic mark helper glyphs: {unique_category_counts.get('Arabic mark helper', 0)}",
        f"- Unique source cleanup glyphs: {unique_category_counts.get('source cleanup', 0)}",
        f"- Unique component-reachable glyphs: {len(all_component_glyphs)}",
        "- Fontspector warning linkage: `unreachable_glyphs`,",
        "  `googlefonts/metadata/unreachable_subsetting`",
        "",
        "## Per-Font Counts",
        "",
        "| Font | cmap glyphs | GSUB output glyphs | Unreachable glyphs |",
        "| --- | ---: | ---: | ---: |",
    ]

    for font_path in font_paths:
        cmap_count, gsub_count, unreachable_count = per_font_counts[str(font_path)]
        lines.append(f"| `{font_path}` | {cmap_count} | {gsub_count} | {unreachable_count} |")

    lines.extend(
        [
            "",
            "## Unique Category Counts",
            "",
            "| Category | Unique glyphs |",
            "| --- | ---: |",
        ]
    )
    for category, count in sorted(unique_category_counts.items()):
        lines.append(f"| {category} | {count} |")

    lines.extend(
        [
            "",
            "## Category Occurrence Counts",
            "",
            "| Category | Count |",
            "| --- | ---: |",
        ]
    )
    for category, count in sorted(category_counts.items()):
        lines.append(f"| {category} | {count} |")

    lines.extend(
        [
            "",
            "## Unique Unreachable Glyphs",
            "",
            "| Glyph | Category | Fonts |",
            "| --- | --- | --- |",
        ]
    )
    for glyph_name in sorted(glyph_to_fonts):
        rows.append(
            "| `{}` | {} | {} |".format(
                glyph_name,
                glyph_category(glyph_name),
                "<br>".join(f"`{font}`" for font in sorted(glyph_to_fonts[glyph_name])),
            )
        )
    lines.extend(rows)

    lines.extend(
        [
            "",
            "## Apply Before Final Submission",
            "",
            "- Decide whether each unreachable Arabic helper glyph should be reached",
            "  through GSUB, encoded, decomposed into reachable outlines, or removed.",
            "- Revisit this report after final Arabic features, PUA scope, and mark",
            "  handling decisions are applied.",
            "- Regenerate `documentation/google-fonts/fontspector-warnings.md` and this report",
            "  after source or feature changes.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[list[Path], Path]:
    args = [Path(arg) for arg in argv[1:]]
    if not args:
        return DEFAULT_FONT_PATHS, OUTPUT_DEFAULT
    if len(args) == 1:
        return DEFAULT_FONT_PATHS, args[0]
    return args[:-1], args[-1]


def main(argv: list[str]) -> int:
    font_paths, output_path = parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(font_paths), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
