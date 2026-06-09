#!/usr/bin/env python3
"""Map GF Arabic Core gaps to source glyph work across both masters."""

from __future__ import annotations

from pathlib import Path
import plistlib
import sys
import unicodedata

from fontTools.ttLib import TTFont
import glyphsets


ROOT = Path(__file__).resolve().parents[1]
GLYPHSET_NAME = "GF_Arabic_Core"
VARIABLE_FONT = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"
UFO_PATHS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]

ARABIC_NAME_OVERRIDES = {
    0x0609: ("perMille-ar",),
    0x060D: ("dateSeparator-ar",),
    0x0615: ("smallHighTah-ar",),
    0x0658: ("noonGhunna-ar",),
    0x0679: ("tteh-ar", "tteh-ar.fina", "tteh-ar.init", "tteh-ar.medi"),
    0x067E: ("peh-ar", "peh-ar.fina", "peh-ar.init", "peh-ar.medi"),
    0x0686: ("tcheh-ar", "tcheh-ar.fina", "tcheh-ar.init", "tcheh-ar.medi"),
    0x0688: ("ddal-ar", "ddal-ar.fina"),
    0x0691: ("rreh-ar", "rreh-ar.fina"),
    0x0698: ("jeh-ar", "jeh-ar.fina"),
    0x06A9: ("keheh-ar", "keheh-ar.fina", "keheh-ar.init", "keheh-ar.medi"),
    0x06AF: ("gaf-ar", "gaf-ar.fina", "gaf-ar.init", "gaf-ar.medi"),
    0x06BE: (
        "hehDoachashmee-ar",
        "hehDoachashmee-ar.fina",
        "hehDoachashmee-ar.init",
        "hehDoachashmee-ar.medi",
    ),
    0x06C1: ("hehGoal-ar", "hehGoal-ar.fina", "hehGoal-ar.init", "hehGoal-ar.medi"),
    0x06CC: ("farsiYeh-ar", "farsiYeh-ar.fina", "farsiYeh-ar.init", "farsiYeh-ar.medi"),
    0x06D2: ("yehBarree-ar", "yehBarree-ar.fina"),
    0x06D4: ("fullStop-ar",),
    0x06DB: ("smallHighThreeDots-ar",),
    0x06F0: ("zeroFarsi-ar",),
    0x06F1: ("oneFarsi-ar",),
    0x06F2: ("twoFarsi-ar",),
    0x06F3: ("threeFarsi-ar",),
    0x06F4: ("fourFarsi-ar",),
    0x06F5: ("fiveFarsi-ar",),
    0x06F6: ("sixFarsi-ar",),
    0x06F7: ("sevenFarsi-ar",),
    0x06F8: ("eightFarsi-ar",),
    0x06F9: ("nineFarsi-ar",),
    0x0763: (
        "kehehThreedotsabove-ar",
        "kehehThreedotsabove-ar.fina",
        "kehehThreedotsabove-ar.init",
        "kehehThreedotsabove-ar.medi",
    ),
    0x25CC: ("dottedCircle",),
}

SHARED_NAME_OVERRIDES = {
    0x002B: ("plus",),
    0x003C: ("less",),
    0x003D: ("equal",),
    0x003E: ("greater",),
    0x0040: ("at",),
    0x005B: ("bracketleft",),
    0x005D: ("bracketright",),
    0x005E: ("asciicircum",),
    0x0060: ("grave",),
    0x007B: ("braceleft",),
    0x007C: ("bar",),
    0x007D: ("braceright",),
    0x007E: ("asciitilde",),
    0x00A2: ("cent",),
    0x00A3: ("sterling",),
    0x00A5: ("yen",),
    0x00A9: ("copyright",),
    0x00AB: ("guillemotleft",),
    0x00AE: ("registered",),
    0x00B0: ("degree",),
    0x00BB: ("guillemotright",),
    0x00D7: ("multiply",),
    0x00F7: ("divide",),
    0x2039: ("guilsinglleft",),
    0x203A: ("guilsinglright",),
    0x20AC: ("Euro",),
    0x2122: ("trademark",),
}

COMPONENT_NOTES = {
    0x0679: "`teh-ar` plus `twodotsverticalabove-ar` pattern",
    0x067E: "`behDotless-ar` plus `threedotsdownbelow-ar`",
    0x0686: "`hah-ar` plus `threedotsdownbelow-ar`",
    0x0688: "`dal-ar` plus dot/mark pattern",
    0x0691: "`reh-ar` plus dot/mark pattern",
    0x0698: "`reh-ar` plus `threedotsupabove-ar`",
    0x06A9: "`kaf-ar` skeleton, Persian/Urdu proportions need review",
    0x06AF: "`kaf-ar` plus `gafsarkashabove-ar` pattern",
    0x06BE: "`heh-ar` skeleton, Urdu joining behavior needs review",
    0x06C1: "`heh-ar` skeleton, Urdu joining behavior needs review",
    0x06CC: "`yeh-ar` skeleton, Persian/Urdu dot behavior needs review",
    0x06D2: "`alefMaksura-ar` / `yeh-ar` skeleton, Urdu behavior needs review",
    0x0763: "`keheh-ar` plus three-dot-above pattern after `keheh-ar` exists",
    0x25CC: "needed for mark specimens and mark attachment proofing",
}

REUSE_PREREQUISITES = {
    0x0679: ("teh-ar", "teh-ar.fina", "teh-ar.init", "teh-ar.medi", "twodotsverticalabove-ar"),
    0x067E: (
        "behDotless-ar",
        "behDotless-ar.fina",
        "behDotless-ar.init",
        "behDotless-ar.medi",
        "threedotsdownbelow-ar",
    ),
    0x0686: ("hah-ar", "hah-ar.fina", "hah-ar.init", "hah-ar.medi", "threedotsdownbelow-ar"),
    0x0688: ("dal-ar", "dal-ar.fina"),
    0x0691: ("reh-ar", "reh-ar.fina"),
    0x0698: ("reh-ar", "reh-ar.fina", "threedotsupabove-ar"),
    0x06A9: ("kaf-ar", "kaf-ar.fina", "kaf-ar.init", "kaf-ar.medi"),
    0x06AF: ("kaf-ar", "kaf-ar.fina", "kaf-ar.init", "kaf-ar.medi", "gafsarkashabove-ar"),
    0x06BE: ("heh-ar", "heh-ar.fina", "heh-ar.init", "heh-ar.medi"),
    0x06C1: ("heh-ar", "heh-ar.fina", "heh-ar.init", "heh-ar.medi"),
    0x06CC: ("yeh-ar", "yeh-ar.fina", "yeh-ar.init", "yeh-ar.medi"),
    0x06D2: ("alefMaksura-ar", "alefMaksura-ar.fina", "yeh-ar", "yeh-ar.fina"),
    0x0763: ("kaf-ar", "kaf-ar.fina", "kaf-ar.init", "kaf-ar.medi", "threedotsupabove-ar"),
}


def relative(path: Path) -> str:
    resolved = path if path.is_absolute() else ROOT / path
    return resolved.relative_to(ROOT).as_posix()


def font_cmap(font_path: Path) -> dict[int, str]:
    font = TTFont(font_path if font_path.is_absolute() else ROOT / font_path)
    cmap = font.getBestCmap() or {}
    font.close()
    return cmap


def source_glyphs(ufo_path: Path) -> set[str]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    return set(plistlib.loads(contents_path.read_bytes()))


def category(codepoint: int) -> str:
    unicode_category = unicodedata.category(chr(codepoint))
    if 0x0600 <= codepoint <= 0x06FF or 0x0750 <= codepoint <= 0x077F:
        if unicode_category.startswith("L"):
            return "Arabic letter"
        if unicode_category.startswith("M"):
            return "Arabic mark"
        if unicode_category.startswith("N"):
            return "Arabic number"
        return "Arabic punctuation"
    return "Shared punctuation/symbol"


def fallback_name(codepoint: int) -> tuple[str, ...]:
    if codepoint in ARABIC_NAME_OVERRIDES:
        return ARABIC_NAME_OVERRIDES[codepoint]
    if codepoint in SHARED_NAME_OVERRIDES:
        return SHARED_NAME_OVERRIDES[codepoint]
    return (f"uni{codepoint:04X}",)


def format_codepoint(codepoint: int) -> str:
    char = chr(codepoint)
    display = "" if char.isspace() or unicodedata.category(char).startswith("M") else char
    return f"U+{codepoint:04X} {display}".rstrip()


def source_status(expected_names: tuple[str, ...], glyphs: set[str]) -> str:
    present = [name for name in expected_names if name in glyphs]
    if not present:
        return "missing"
    if len(present) == len(expected_names):
        return "present"
    return "partial: " + ", ".join(f"`{name}`" for name in present)


def source_inventory(missing: list[int], source_maps: dict[str, set[str]]) -> dict[str, int]:
    suggested_names = sorted({name for cp in missing for name in fallback_name(cp)})
    arabic_names = sorted(
        {
            name
            for cp in missing
            if category(cp).startswith("Arabic")
            for name in fallback_name(cp)
        }
    )
    shared_names = sorted(
        {
            name
            for cp in missing
            if category(cp) == "Shared punctuation/symbol"
            for name in fallback_name(cp)
        }
    )
    positional_names = [name for name in suggested_names if name.endswith((".fina", ".init", ".medi"))]
    default_arabic_names = [
        name
        for name in arabic_names
        if not name.endswith((".fina", ".init", ".medi"))
    ]
    present_both = [
        name
        for name in suggested_names
        if all(name in glyphs for glyphs in source_maps.values())
    ]
    missing_both = [
        name
        for name in suggested_names
        if all(name not in glyphs for glyphs in source_maps.values())
    ]
    partial = [
        name
        for name in suggested_names
        if name not in present_both and name not in missing_both
    ]
    return {
        "total": len(suggested_names),
        "arabic": len(arabic_names),
        "shared": len(shared_names),
        "default_arabic": len(default_arabic_names),
        "positional": len(positional_names),
        "present_both": len(present_both),
        "missing_both": len(missing_both),
        "partial": len(partial),
    }


def prerequisite_status(names: tuple[str, ...], glyphs: set[str]) -> str:
    missing = [name for name in names if name not in glyphs]
    if not missing:
        return "ready"
    return "missing: " + ", ".join(f"`{name}`" for name in missing)


def batch_name(codepoint: int) -> str:
    if codepoint in SHARED_NAME_OVERRIDES or codepoint == 0x25CC:
        return "Shared punctuation and symbols"
    if 0x06F0 <= codepoint <= 0x06F9:
        return "Extended Arabic-Indic digits"
    if codepoint in {0x0615, 0x0658, 0x06DB}:
        return "Arabic marks"
    if category(codepoint) == "Arabic letter":
        return "Urdu/Persian joining letters"
    return "Arabic punctuation and symbols"


def batch_order(codepoint: int) -> int:
    order = {
        "Shared punctuation and symbols": 1,
        "Extended Arabic-Indic digits": 2,
        "Urdu/Persian joining letters": 3,
        "Arabic punctuation and symbols": 4,
        "Arabic marks": 5,
    }
    return order[batch_name(codepoint)]


def batch_rows(missing: list[int]) -> list[tuple[str, list[int], list[str]]]:
    batches: dict[str, list[int]] = {}
    for cp in sorted(missing, key=lambda item: (batch_order(item), item)):
        batches.setdefault(batch_name(cp), []).append(cp)
    rows: list[tuple[str, list[int], list[str]]] = []
    for name, codepoints in sorted(
        batches.items(), key=lambda item: batch_order(item[1][0])
    ):
        glyph_names = sorted({glyph for cp in codepoints for glyph in fallback_name(cp)})
        rows.append((name, codepoints, glyph_names))
    return rows


def markdown_report(font_path: Path) -> str:
    required = set(glyphsets.unicodes_per_glyphset(GLYPHSET_NAME))
    cmap = font_cmap(font_path)
    missing = sorted(required - set(cmap))
    source_maps = {path.name: source_glyphs(path) for path in UFO_PATHS}
    arabic_missing = [
        cp
        for cp in missing
        if 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F
    ]
    shared_missing = [cp for cp in missing if cp not in arabic_missing]
    prerequisite_codepoints = [cp for cp in arabic_missing if cp in REUSE_PREREQUISITES]
    prerequisite_missing = [
        (cp, path.name, name)
        for cp in prerequisite_codepoints
        for path in UFO_PATHS
        for name in REUSE_PREREQUISITES[cp]
        if name not in source_maps[path.name]
    ]
    inventory = source_inventory(missing, source_maps)

    lines = [
        "# Arabic Source Work Checklist",
        "",
        (
            "This generated checklist translates the current `GF_Arabic_Core` "
            "cmap gaps into source-glyph work across both active UFO masters. "
            "It is a production aid for drawing and compatibility work; the "
            "authoritative coverage target remains the installed `glyphsets` "
            "definition, and visual Arabic review is still required."
        ),
        "",
        "## Summary",
        "",
        f"- Font checked: `{relative(font_path)}`",
        f"- Minimum Arabic target: `{GLYPHSET_NAME}`",
        f"- Missing required codepoints: {len(missing)}",
        f"- Arabic-range missing codepoints: {len(arabic_missing)}",
        f"- Shared punctuation/symbol missing codepoints: {len(shared_missing)}",
        f"- U+25CC dotted circle missing: {'yes' if 0x25CC in missing else 'no'}",
        f"- Suggested source glyph names: {inventory['total']}",
        f"- Suggested Arabic source glyph names: {inventory['arabic']}",
        f"- Suggested shared punctuation/symbol glyph names: {inventory['shared']}",
        f"- Suggested Arabic default glyph names: {inventory['default_arabic']}",
        f"- Suggested Arabic positional-form glyph names: {inventory['positional']}",
        f"- Suggested glyph names present in both masters: {inventory['present_both']}",
        f"- Suggested glyph names missing in both masters: {inventory['missing_both']}",
        f"- Suggested glyph names partial across masters: {inventory['partial']}",
        f"- Arabic reuse prerequisites checked: {len(prerequisite_codepoints)} codepoints",
        f"- Missing reuse prerequisites across masters: {len(prerequisite_missing)}",
        f"- Active source masters checked: {', '.join(f'`{relative(path)}`' for path in UFO_PATHS)}",
        "",
        "## Suggested Source Inventory",
        "",
        "| Bucket | Count |",
        "| --- | ---: |",
        f"| Total suggested source glyph names | {inventory['total']} |",
        f"| Arabic suggested source glyph names | {inventory['arabic']} |",
        f"| Shared punctuation/symbol suggested glyph names | {inventory['shared']} |",
        f"| Arabic default glyph names | {inventory['default_arabic']} |",
        f"| Arabic positional-form glyph names | {inventory['positional']} |",
        f"| Suggested glyph names already present in both masters | {inventory['present_both']} |",
        f"| Suggested glyph names missing in both masters | {inventory['missing_both']} |",
        f"| Suggested glyph names partial across masters | {inventory['partial']} |",
        "",
        "## Source Rules",
        "",
        "- Add every required encoded glyph to both active UFO masters.",
        "- For joining Arabic letters, keep the same default/final/initial/medial glyph structure in both masters.",
        "- Preserve master compatibility: same contour/component structure, point counts, and point types in Regular and Bold.",
        "- Add dotted circle and mark anchors before final Arabic mark proofing.",
        "- Rerun `make preflight` after each source batch.",
        "",
        "## Missing Codepoint Worklist",
        "",
        "| Codepoint | Unicode name | Type | Suggested source glyphs | Built cmap glyph | Regular source | Bold source | Reuse note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for cp in missing:
        names = fallback_name(cp)
        source_statuses = [
            source_status(names, source_maps[path.name])
            for path in UFO_PATHS
        ]
        lines.append(
            "| {} | {} | {} | {} | `{}` | {} | {} | {} |".format(
                format_codepoint(cp).replace("|", "\\|"),
                unicodedata.name(chr(cp), "UNKNOWN"),
                category(cp),
                ", ".join(f"`{name}`" for name in names),
                cmap.get(cp, ".notdef"),
                source_statuses[0],
                source_statuses[1],
                COMPONENT_NOTES.get(cp, "draw/review as standalone shared glyph"),
            )
        )

    lines.extend(
        [
            "",
            "## Reuse Prerequisite Audit",
            "",
            (
                "These rows check whether suggested Arabic source reuse bases "
                "already exist in both active masters. They do not replace "
                "drawing review; they only verify that the referenced skeleton "
                "or dot helper names are available before new glyphs are built."
            ),
            "",
            "| Codepoint | Target glyphs | Reuse prerequisites | Regular prerequisites | Bold prerequisites |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for cp in prerequisite_codepoints:
        prerequisites = REUSE_PREREQUISITES[cp]
        statuses = [
            prerequisite_status(prerequisites, source_maps[path.name])
            for path in UFO_PATHS
        ]
        lines.append(
            "| {} | {} | {} | {} | {} |".format(
                format_codepoint(cp).replace("|", "\\|"),
                ", ".join(f"`{name}`" for name in fallback_name(cp)),
                ", ".join(f"`{name}`" for name in prerequisites),
                statuses[0],
                statuses[1],
            )
        )

    lines.extend(
        [
            "",
            "## Batch Work Plan",
            "",
            "These batches group the same `GF_Arabic_Core` gaps by production",
            "dependency so drawing work can move in source-compatible passes.",
            "The per-codepoint table above remains the source of truth for",
            "which encoded characters are still missing.",
            "",
            "| Order | Batch | Codepoints | Source glyph names | Notes |",
            "| ---: | --- | ---: | ---: | --- |",
        ]
    )
    for order, (name, codepoints, glyph_names) in enumerate(batch_rows(missing), start=1):
        notes = {
            "Shared punctuation and symbols": "Also reduces Latin Core shared punctuation gaps.",
            "Extended Arabic-Indic digits": "Draw encoded digit defaults before numeral proofing.",
            "Urdu/Persian joining letters": "Includes default, final, initial, and medial forms where required.",
            "Arabic punctuation and symbols": "Review directionality and Arabic text rhythm in proof strings.",
            "Arabic marks": "Pair with dotted circle, anchors, and mark/mkmk proofing.",
        }[name]
        lines.append(
            f"| {order} | {name} | {len(codepoints)} | {len(glyph_names)} | {notes} |"
        )

    lines.extend(
        [
            "",
            "## Batch Glyph Lists",
            "",
        ]
    )
    for name, codepoints, glyph_names in batch_rows(missing):
        lines.extend(
            [
                f"### {name}",
                "",
                f"- Codepoints: {', '.join(format_codepoint(cp).replace('|', '\\|') for cp in codepoints)}",
                f"- Source glyphs: {', '.join(f'`{glyph}`' for glyph in glyph_names)}",
                "",
            ]
        )

    lines.extend(
        [
            "## Batch Order Suggestion",
            "",
            "1. Shared punctuation and symbols that are also needed by Latin Core.",
            "2. Extended Arabic-Indic digits U+06F0-U+06F9.",
            "3. Urdu/Persian joining letters and their positional forms.",
            "4. Missing Arabic marks plus U+25CC dotted circle.",
            "5. Source anchors and built `mark`/`mkmk` features.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    font_path = Path(argv[1]) if len(argv) > 1 else VARIABLE_FONT
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
