#!/usr/bin/env python3
"""Report mechanical triage for the Arabic structure review batch."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys
import unicodedata

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import glyphsets


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "documentation/arabic-structure-triage.md"
GLYPHSET_NAME = "GF_Arabic_Core"
EXTRA_CODEPOINTS = {0x25CC}
FONTS = [
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf"),
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]


@dataclass(frozen=True)
class GlyphRecord:
    font_label: str
    font_path: str
    codepoint: int
    glyph_name: str
    advance: int
    bounds: tuple[int, int, int, int] | None
    risks: tuple[str, ...]


def category_label(codepoint: int) -> str:
    category = unicodedata.category(chr(codepoint))
    if category.startswith("L"):
        return "letter"
    if category.startswith("M"):
        return "mark"
    if category.startswith("N"):
        return "number"
    if category.startswith("P"):
        return "punctuation"
    if category.startswith("S"):
        return "symbol"
    if category.startswith("Z"):
        return "space"
    if category == "Cf":
        return "format-control"
    if category.startswith("C"):
        return "control"
    return "other"


def codepoints() -> list[int]:
    return sorted(set(glyphsets.unicodes_per_glyphset(GLYPHSET_NAME)) | EXTRA_CODEPOINTS)


def codepoint_label(codepoint: int) -> str:
    name = unicodedata.name(chr(codepoint), "UNKNOWN")
    return f"U+{codepoint:04X} {name}"


def glyph_bounds(font: TTFont, glyph_name: str) -> tuple[int, int, int, int] | None:
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return pen.bounds


def glyph_advance(font: TTFont, glyph_name: str) -> int:
    if "hmtx" not in font or glyph_name not in font["hmtx"].metrics:
        return 0
    return int(font["hmtx"].metrics[glyph_name][0])


def record_risks(
    codepoint: int,
    glyph_name: str,
    advance: int,
    bounds: tuple[int, int, int, int] | None,
) -> tuple[str, ...]:
    category = category_label(codepoint)
    risks: list[str] = []
    if glyph_name == ".notdef":
        risks.append("maps-to-notdef")
        return tuple(risks)
    if bounds is None and category not in {"mark", "format-control", "control", "space"}:
        risks.append("blank-visible-glyph")
    if advance == 0 and category in {"letter", "number", "punctuation", "symbol"}:
        risks.append("nonmark-zero-advance")
    if bounds:
        x_min, y_min, x_max, y_max = bounds
        if x_min < -120:
            risks.append("large-negative-left-sidebearing")
        if x_max - advance > 120:
            risks.append("large-negative-right-sidebearing")
        if y_min < -360:
            risks.append("deep-vertical-bound")
        if y_max > 1100:
            risks.append("high-vertical-bound")
    return tuple(risks)


def font_records(label: str, path: str) -> list[GlyphRecord]:
    font = TTFont(ROOT / path)
    cmap = font.getBestCmap() or {}
    records: list[GlyphRecord] = []
    for codepoint in codepoints():
        glyph_name = cmap.get(codepoint, ".notdef")
        bounds = None if glyph_name == ".notdef" else glyph_bounds(font, glyph_name)
        advance = 0 if glyph_name == ".notdef" else glyph_advance(font, glyph_name)
        records.append(
            GlyphRecord(
                font_label=label,
                font_path=path,
                codepoint=codepoint,
                glyph_name=glyph_name,
                advance=advance,
                bounds=bounds,
                risks=record_risks(codepoint, glyph_name, advance, bounds),
            )
        )
    font.close()
    return records


def all_records() -> list[GlyphRecord]:
    records: list[GlyphRecord] = []
    for label, path in FONTS:
        records.extend(font_records(label, path))
    return records


def shared_mapping_rows(records: list[GlyphRecord]) -> list[tuple[str, str, list[str]]]:
    by_font_and_glyph: dict[tuple[str, str], list[int]] = defaultdict(list)
    for record in records:
        if record.glyph_name == ".notdef":
            continue
        by_font_and_glyph[(record.font_label, record.glyph_name)].append(record.codepoint)
    rows: list[tuple[str, str, list[str]]] = []
    for (font_label, glyph_name), mapped_codepoints in sorted(by_font_and_glyph.items()):
        visible = [
            codepoint
            for codepoint in mapped_codepoints
            if category_label(codepoint) not in {"mark", "format-control", "control"}
        ]
        if len(visible) > 1:
            rows.append(
                (
                    font_label,
                    glyph_name,
                    [codepoint_label(codepoint) for codepoint in visible],
                )
            )
    return rows


def bounds_text(bounds: tuple[int, int, int, int] | None) -> str:
    return "none" if bounds is None else ", ".join(str(value) for value in bounds)


def grouped_prompt_rows(records: list[GlyphRecord]) -> list[str]:
    by_codepoint: dict[int, list[GlyphRecord]] = defaultdict(list)
    for record in records:
        by_codepoint[record.codepoint].append(record)

    rows = [
        "| Codepoint | Glyphs | Category | Fonts | Risk summary | Review prompt |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if not by_codepoint:
        rows.append("| none | none | none | none | none | none |")
        return rows

    for codepoint, codepoint_records in sorted(by_codepoint.items()):
        glyphs = sorted({record.glyph_name for record in codepoint_records})
        fonts = sorted({record.font_label for record in codepoint_records})
        risks = Counter(risk for record in codepoint_records for risk in record.risks)
        x_min_values = [record.bounds[0] for record in codepoint_records if record.bounds]
        right_overhangs = [
            record.bounds[2] - record.advance
            for record in codepoint_records
            if record.bounds
        ]
        metric_parts = []
        if x_min_values:
            metric_parts.append(f"xMin {min(x_min_values)}..{max(x_min_values)}")
        if right_overhangs:
            metric_parts.append(f"right overhang {min(right_overhangs)}..{max(right_overhangs)}")
        risk_text = "<br>".join(f"`{risk}`: {count}" for risk, count in sorted(risks.items()))
        if metric_parts:
            risk_text = f"{risk_text}<br>{'; '.join(metric_parts)}"
        rows.append(
            "| `{}` | {} | {} | {} | {} | {} |".format(
                codepoint_label(codepoint),
                "<br>".join(f"`{glyph}`" for glyph in glyphs),
                category_label(codepoint),
                ", ".join(fonts),
                risk_text,
                review_prompt(codepoint, codepoint_records),
            )
        )
    return rows


def review_prompt(codepoint: int, records: list[GlyphRecord]) -> str:
    category = category_label(codepoint)
    name = unicodedata.name(chr(codepoint), "")
    if category == "mark":
        return "Expected zero-advance mark overhang; inspect attachment and dotted-circle clarity, not sidebearing alone."
    if "SEEN" in name or "SHEEN" in name:
        return "Check whether the left overhang is intentional joining-script rhythm across all weights."
    if "THEH" in name:
        return "Check dot stack height and left overhang in glyph proofs before spacing edits."
    if "WAW" in name:
        return "Check descending bowl and left overhang against adjacent text samples."
    return "Inspect in structure sweep and glyph proofs; edit only if the rendered drawing is wrong."


def markdown_report() -> str:
    records = all_records()
    risk_records = [record for record in records if record.risks]
    risk_counts = Counter(risk for record in risk_records for risk in record.risks)
    shared_mappings = shared_mapping_rows(records)
    blocking_risks = {
        "maps-to-notdef",
        "blank-visible-glyph",
        "nonmark-zero-advance",
    }
    blocking_count = sum(
        1 for record in risk_records if any(risk in blocking_risks for risk in record.risks)
    )

    lines = [
        "# Arabic Structure Triage",
        "",
        "This generated report supports the next manual review batch:",
        "`Structure And Wrong-Glyph Sweep`. It checks the built fonts for",
        "mechanical problems that AI can reliably pre-triage before hand review.",
        "It does not approve Arabic drawings or replace native-reader review.",
        "",
        "## Summary",
        "",
        f"- Target glyphset: `{GLYPHSET_NAME}` plus U+25CC dotted circle",
        f"- Fonts checked: {len(FONTS)}",
        f"- Codepoints checked per font: {len(codepoints())}",
        f"- Mechanical blocking risks: {blocking_count}",
        f"- Review-prompt risk rows: {len(risk_records) - blocking_count}",
        f"- Shared visible cmap mappings: {len(shared_mappings)}",
        "",
        "## Risk Counts",
        "",
        "| Risk | Rows |",
        "| --- | ---: |",
    ]
    if risk_counts:
        for risk, count in sorted(risk_counts.items()):
            lines.append(f"| `{risk}` | {count} |")
    else:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Grouped Review Prompts",
            "",
            "These rows collapse repeated per-font sidebearing prompts into the",
            "actual glyph/codepoint questions for the active structure review.",
            "They do not approve the drawings; they point the hand review at",
            "the shortest evidence set.",
            "",
            *grouped_prompt_rows(risk_records),
            "",
            "## Interpretation",
            "",
            "- `maps-to-notdef`, `blank-visible-glyph`, and `nonmark-zero-advance`",
            "  are likely source or build issues if present.",
            "- Sidebearing and vertical-bound rows are prompts for hand inspection,",
            "  especially in the focused structure sweep and glyph proof HTML.",
            "- Shared visible cmap mappings should be reviewed as possible",
            "  wrong-glyph mappings unless they are intentional aliases.",
            "",
            "## Risk Rows",
            "",
            "| Font | Codepoint | Glyph | Category | Advance | Bounds | Risks |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    if risk_records:
        for record in risk_records:
            lines.append(
                "| `{}` | `{}` | `{}` | {} | {} | `{}` | {} |".format(
                    record.font_path,
                    codepoint_label(record.codepoint),
                    record.glyph_name,
                    category_label(record.codepoint),
                    record.advance,
                    bounds_text(record.bounds),
                    ", ".join(f"`{risk}`" for risk in record.risks),
                )
            )
    else:
        lines.append("| none | none | none | none | 0 | none | none |")

    lines.extend(
        [
            "",
            "## Shared Visible Cmap Mappings",
            "",
            "| Font | Glyph | Codepoints |",
            "| --- | --- | --- |",
        ]
    )
    if shared_mappings:
        for font_label, glyph_name, mapped in shared_mappings:
            lines.append(
                f"| {font_label} | `{glyph_name}` | "
                + "<br>".join(f"`{codepoint}`" for codepoint in mapped)
                + " |"
            )
    else:
        lines.append("| none | none | none |")

    lines.extend(
        [
            "",
            "## Next Manual Action",
            "",
            "Open these together for the active structure review batch:",
            "",
            "- `documentation/arabic-structure-sweep.html`",
            "- `documentation/arabic-visual-risk-proof.html`",
            "- `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`",
            "- `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`",
            "- `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`",
            "- `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`",
            "",
            "Record the five batch-2 rows in",
            "`documentation/arabic-visual-review-log.md` after hand inspection.",
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
