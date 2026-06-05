#!/usr/bin/env python3
"""Report shaping triage for Arabic mark review samples."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import plistlib
import sys
import unicodedata
import xml.etree.ElementTree as ET

import uharfbuzz as hb
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-mark-triage.md"
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]
FONTS = [
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf"),
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
SECTIONS = [
    ("mark-base+fatha", "Base plus fatha", ["بَ", "تَ", "جَ", "سَ", "صَ", "طَ", "مَ", "هَ"]),
    ("mark-base+damma", "Base plus damma", ["بُ", "تُ", "جُ", "سُ", "صُ", "طُ", "مُ", "هُ"]),
    ("mark-base+kasra", "Base plus kasra", ["بِ", "تِ", "جِ", "سِ", "صِ", "طِ", "مِ", "هِ"]),
    ("mark-shadda+sukun", "Shadda and sukun stacking", ["بّ", "بْ", "بُّ", "بَّ", "بّْ", "مّ", "هّ", "سْ"]),
    ("mark-tanween", "Tanween", ["بً", "بٌ", "بٍ", "مً", "مٌ", "مٍ", "هً", "هٍ"]),
    ("mark-hamza-above-below", "Hamza above and below", ["بٔ", "بٕ", "أ", "إ", "ؤ", "ئ", "مٔ", "هٔ"]),
    ("mark-dotted-circle", "Dotted circle", ["◌َ", "◌ُ", "◌ِ", "◌ّ", "◌ْ", "◌ٔ", "◌ٕ", "◌ً", "◌ٌ", "◌ٍ"]),
    (
        "class-mark-combinations",
        "Required mark inventory",
        ["◌ؕ", "◌ً", "◌ٌ", "◌ٍ", "◌َ", "◌ُ", "◌ِ", "◌ّ", "◌ْ", "◌ٓ", "◌ٔ", "◌ٕ", "◌ٖ", "◌٘", "◌ٰ", "◌ۛ"],
    ),
]
MARK_GLYPH_NAMES = {
    "smallHighTahar",
    "uni064B",
    "uni064C",
    "uni064D",
    "uni064E",
    "uni064F",
    "uni0650",
    "uni0651",
    "uni0652",
    "uni0653",
    "uni0654",
    "uni0655",
    "uni0656",
    "noonGhunnaar",
    "uni0670",
    "smallHighThreeDotsar",
    "uni0654064F",
    "uni0654064C",
    "uni0654064E",
    "uni0654064B",
    "uni06540652",
    "uni06550650",
    "uni0655064D",
    "uni06510670",
    "uni0651064F",
    "uni0651064C",
    "uni0651064E",
    "uni0651064B",
    "uni06510650",
    "uni0651064D",
}


@dataclass(frozen=True)
class ShapedGlyph:
    name: str
    advance: tuple[int, int]
    offset: tuple[int, int]


@dataclass(frozen=True)
class SampleRecord:
    review_key: str
    section: str
    font_label: str
    font_path: str
    sample: str
    glyphs: tuple[ShapedGlyph, ...]
    risks: tuple[str, ...]


def has_mark(text: str) -> bool:
    return any(unicodedata.category(character).startswith("M") for character in text)


def shape_sample(font_path: Path, sample: str) -> tuple[ShapedGlyph, ...]:
    font_data = font_path.read_bytes()
    face = hb.Face(font_data)
    hb_font = hb.Font(face)
    hb_font.scale = (face.upem, face.upem)
    buffer = hb.Buffer()
    buffer.add_str(sample)
    buffer.guess_segment_properties()
    hb.shape(hb_font, buffer, {"mark": True, "mkmk": True})

    glyph_order = TTFont(font_path).getGlyphOrder()
    shaped: list[ShapedGlyph] = []
    for info, position in zip(buffer.glyph_infos, buffer.glyph_positions):
        glyph_id = info.codepoint
        glyph_name = glyph_order[glyph_id] if glyph_id < len(glyph_order) else f"gid{glyph_id}"
        shaped.append(
            ShapedGlyph(
                name=glyph_name,
                advance=(position.x_advance, position.y_advance),
                offset=(position.x_offset, position.y_offset),
            )
        )
    return tuple(shaped)


def risks_for(sample: str, glyphs: tuple[ShapedGlyph, ...]) -> tuple[str, ...]:
    risks: list[str] = []
    if any(glyph.name == ".notdef" for glyph in glyphs):
        risks.append("maps-to-notdef")
    if has_mark(sample):
        mark_like = [
            glyph
            for glyph in glyphs
            if glyph.advance == (0, 0) or glyph.name in MARK_GLYPH_NAMES
        ]
        if not mark_like and len(glyphs) != 1:
            risks.append("no-mark-glyph-detected")
        if any(glyph.advance != (0, 0) for glyph in mark_like):
            risks.append("mark-like-nonzero-advance")
        if mark_like and all(glyph.offset == (0, 0) for glyph in mark_like):
            risks.append("no-mark-position-offset-observed")
    return tuple(risks)


def sample_records() -> list[SampleRecord]:
    records: list[SampleRecord] = []
    for font_label, font_path in FONTS:
        path = ROOT / font_path
        for review_key, section, samples in SECTIONS:
            for sample in samples:
                glyphs = shape_sample(path, sample)
                records.append(
                    SampleRecord(
                        review_key=review_key,
                        section=section,
                        font_label=font_label,
                        font_path=font_path,
                        sample=sample,
                        glyphs=glyphs,
                        risks=risks_for(sample, glyphs),
                    )
                )
    return records


def glyph_summary(glyphs: tuple[ShapedGlyph, ...]) -> str:
    parts = []
    for glyph in glyphs:
        advance = f"{glyph.advance[0]},{glyph.advance[1]}"
        offset = f"{glyph.offset[0]},{glyph.offset[1]}"
        parts.append(f"{glyph.name} adv={advance} off={offset}")
    return "<br>".join(f"`{part}`" for part in parts)


def unicode_from_uni_name(glyph_name: str) -> int | None:
    if not glyph_name.startswith("uni") or len(glyph_name) < 7:
        return None
    try:
        return int(glyph_name[3:7], 16)
    except ValueError:
        return None


def glyph_has_unicode(glif_path: Path, codepoint: int) -> bool:
    try:
        root = ET.parse(glif_path).getroot()
    except ET.ParseError:
        return False
    for unicode_element in root.findall("unicode"):
        hex_value = unicode_element.attrib.get("hex", "")
        if hex_value and int(hex_value, 16) == codepoint:
            return True
    return False


def source_targets_for_built_glyph(glyph_name: str) -> list[str]:
    if glyph_name == ".notdef":
        return []
    targets: list[str] = []
    codepoint = unicode_from_uni_name(glyph_name)
    for ufo in SOURCE_UFOS:
        contents_path = ufo / "glyphs/contents.plist"
        lib_path = ufo / "lib.plist"
        with contents_path.open("rb") as file:
            contents = plistlib.load(file)
        with lib_path.open("rb") as file:
            lib = plistlib.load(file)
        postscript_names = lib.get("public.postscriptNames", {})

        source_names = [
            source_name
            for source_name, production_name in postscript_names.items()
            if production_name == glyph_name
        ]
        if not source_names and glyph_name in contents:
            source_names = [glyph_name]
        if not source_names and codepoint is not None:
            for source_name, filename in contents.items():
                glif_path = ufo / "glyphs" / filename
                if glyph_has_unicode(glif_path, codepoint):
                    source_names.append(source_name)

        for source_name in sorted(set(source_names)):
            filename = contents.get(source_name)
            if not filename:
                continue
            glif_path = ufo / "glyphs" / filename
            targets.append(
                f"`{ufo.name}` `{source_name}` -> `{glif_path.relative_to(ROOT)}`"
            )
    return targets


def source_target_summary(glyphs: tuple[ShapedGlyph, ...]) -> str:
    targets: list[str] = []
    for glyph in glyphs:
        for target in source_targets_for_built_glyph(glyph.name):
            if target not in targets:
                targets.append(target)
    return "<br>".join(targets) if targets else "none"


def markdown_report() -> str:
    records = sample_records()
    risk_records = [record for record in records if record.risks]
    risk_counts = Counter(risk for record in risk_records for risk in record.risks)
    blocking = {"maps-to-notdef", "no-mark-glyph-detected", "mark-like-nonzero-advance"}
    blocking_records = [
        record for record in risk_records if any(risk in blocking for risk in record.risks)
    ]
    blocking_count = len(blocking_records)
    no_offset_summary = Counter(
        (record.review_key, record.font_label)
        for record in risk_records
        if "no-mark-position-offset-observed" in record.risks
    )
    no_offset_samples: dict[tuple[str, str], list[str]] = {}
    for record in risk_records:
        if "no-mark-position-offset-observed" not in record.risks:
            continue
        no_offset_samples.setdefault((record.review_key, record.font_label), []).append(
            record.sample
        )
    no_offset_count = risk_counts.get("no-mark-position-offset-observed", 0)

    lines = [
        "# Arabic Mark Triage",
        "",
        "This generated report supports visual-review batch 3:",
        "`Marks, Dotted Circle, And Stacking`. It shapes the same samples used",
        "by `documentation/glyph-review/arabic-mark-review-proof.html` and records mechanical",
        "risks that AI can pre-triage before hand review.",
        "",
        "It does not approve mark placement. Zero-position offsets can be valid",
        "for this source if marks are drawn at their intended origin, so those",
        "rows remain hand-review prompts, not automatic failures.",
        "",
        "## Summary",
        "",
        f"- Fonts checked: {len(FONTS)}",
        f"- Review sections checked: {len(SECTIONS)}",
        f"- Shaped sample rows: {len(records)}",
        f"- Mechanical blocking risks: {blocking_count}",
        f"- No-offset mark review prompts: {no_offset_count}",
        "",
        "## Review Sections",
        "",
        "| Review row | Section | Samples |",
        "| --- | --- | ---: |",
    ]
    for review_key, section, samples in SECTIONS:
        lines.append(f"| `{review_key}` | {section} | {len(samples)} |")

    lines.extend(
        [
            "",
            "## Risk Counts",
            "",
            "| Risk | Rows |",
            "| --- | ---: |",
        ]
    )
    if risk_counts:
        for risk, count in sorted(risk_counts.items()):
            lines.append(f"| `{risk}` | {count} |")
    else:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Mechanical Blocking Rows",
            "",
            "| Review row | Font | Sample | Glyph sequence | Risks |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    if blocking_records:
        for record in blocking_records:
            lines.append(
                "| `{}` | `{}` | `{}` | {} | {} |".format(
                    record.review_key,
                    record.font_path,
                    record.sample,
                    glyph_summary(record.glyphs),
                    ", ".join(f"`{risk}`" for risk in record.risks),
                )
            )
    else:
        lines.append("| none | none | none | none | none |")

    lines.extend(
        [
            "",
            "## No-Offset Review Prompt Summary",
            "",
            "These rows need visual inspection in the proof. They are not automatic",
            "failures because this source can place marks at their intended origin.",
            "",
            "| Review row | Font | Samples | Sample texts |",
            "| --- | --- | ---: | --- |",
        ]
    )
    if no_offset_summary:
        for (review_key, font_label), count in sorted(no_offset_summary.items()):
            samples = ", ".join(f"`{sample}`" for sample in no_offset_samples[(review_key, font_label)])
            lines.append(f"| `{review_key}` | {font_label} | {count} | {samples} |")
    else:
        lines.append("| none | none | 0 | none |")

    lines.extend(
        [
            "",
            "## No-Offset Review Prompt Rows",
            "",
            "| Review row | Font | Sample | Glyph sequence | Source edit targets |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    no_offset_records = [
        record
        for record in risk_records
        if "no-mark-position-offset-observed" in record.risks
    ]
    if no_offset_records:
        for record in sorted(
            no_offset_records,
            key=lambda item: (item.review_key, item.font_label, item.sample),
        ):
            lines.append(
                f"| `{record.review_key}` | {record.font_label} | `{record.sample}` | {glyph_summary(record.glyphs)} | {source_target_summary(record.glyphs)} |"
            )
    else:
        lines.append("| none | none | none | none | none |")

    lines.extend(
        [
            "",
            "## Next Manual Action",
            "",
            "Open these together for the mark review batch:",
            "",
            "- `documentation/glyph-review/arabic-mark-review-proof.html`",
            "- `documentation/glyph-review/arabic-mark-readiness.md`",
            "- `documentation/glyph-review/arabic-manual-review-dashboard.html`",
            "",
            "Record the eight batch-3 rows in",
            "`documentation/glyph-review/arabic-visual-review-log.md` after hand inspection.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
