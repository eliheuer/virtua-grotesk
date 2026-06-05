#!/usr/bin/env python3
"""Report Google Fonts numeric feature readiness."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/numeric-feature-readiness.md")
VARIABLE_FONT = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
STATIC_FONTS = [
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
ALL_FONTS = [VARIABLE_FONT, *STATIC_FONTS]
DIGIT_CODEPOINTS = list(range(0x30, 0x3A))


@dataclass(frozen=True)
class FontNumericReport:
    path: Path
    exists: bool
    default_digits_present: int
    default_widths: tuple[int, ...]
    default_proportional: bool
    tnum_feature_present: bool
    tnum_supported: bool
    tnum_substitutions: tuple[tuple[str, str, int], ...]
    tnum_coverage: int
    tnum_widths: tuple[int, ...]
    tnum_tabular: bool
    unsupported_lookup_types: tuple[int, ...]


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def single_substitutions_for_feature(font: TTFont, feature_tag: str) -> tuple[dict[str, str], set[int]]:
    if "GSUB" not in font:
        return {}, set()
    gsub = font["GSUB"].table
    if gsub.FeatureList is None or gsub.LookupList is None:
        return {}, set()

    mappings: dict[str, str] = {}
    unsupported_lookup_types: set[int] = set()
    for feature_record in gsub.FeatureList.FeatureRecord:
        if feature_record.FeatureTag != feature_tag:
            continue
        for lookup_index in feature_record.Feature.LookupListIndex:
            lookup = gsub.LookupList.Lookup[lookup_index]
            lookup_type = lookup.LookupType
            for subtable in lookup.SubTable:
                resolved_lookup_type = lookup_type
                resolved_subtable = subtable
                if lookup_type == 7:
                    resolved_lookup_type = subtable.ExtensionLookupType
                    resolved_subtable = subtable.ExtSubTable
                if resolved_lookup_type == 1 and hasattr(resolved_subtable, "mapping"):
                    mappings.update(resolved_subtable.mapping)
                else:
                    unsupported_lookup_types.add(resolved_lookup_type)
    return mappings, unsupported_lookup_types


def numeric_report_for_font(relative_path: Path) -> FontNumericReport:
    path = ROOT / relative_path
    if not path.exists():
        return FontNumericReport(
            path=relative_path,
            exists=False,
            default_digits_present=0,
            default_widths=(),
            default_proportional=False,
            tnum_feature_present=False,
            tnum_supported=False,
            tnum_substitutions=(),
            tnum_coverage=0,
            tnum_widths=(),
            tnum_tabular=False,
            unsupported_lookup_types=(),
        )

    font = TTFont(path)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"].metrics
    default_glyphs = [cmap.get(codepoint) for codepoint in DIGIT_CODEPOINTS]
    default_widths = tuple(hmtx[glyph_name][0] for glyph_name in default_glyphs if glyph_name in hmtx)
    feature_tags = set()
    if "GSUB" in font and font["GSUB"].table.FeatureList:
        feature_tags = {record.FeatureTag for record in font["GSUB"].table.FeatureList.FeatureRecord}
    tnum_mapping, unsupported_lookup_types = single_substitutions_for_feature(font, "tnum")

    substitutions: list[tuple[str, str, int]] = []
    for glyph_name in default_glyphs:
        if not glyph_name:
            continue
        substitute = tnum_mapping.get(glyph_name)
        if substitute and substitute in hmtx:
            substitutions.append((glyph_name, substitute, hmtx[substitute][0]))

    tnum_widths = tuple(width for _, _, width in substitutions)
    font.close()
    return FontNumericReport(
        path=relative_path,
        exists=True,
        default_digits_present=len(default_widths),
        default_widths=default_widths,
        default_proportional=len(default_widths) == 10 and len(set(default_widths)) > 1,
        tnum_feature_present="tnum" in feature_tags,
        tnum_supported="tnum" in feature_tags and not unsupported_lookup_types,
        tnum_substitutions=tuple(substitutions),
        tnum_coverage=len(substitutions),
        tnum_widths=tnum_widths,
        tnum_tabular=len(tnum_widths) == 10 and len(set(tnum_widths)) == 1,
        unsupported_lookup_types=tuple(sorted(unsupported_lookup_types)),
    )


def width_set(widths: tuple[int, ...]) -> str:
    if not widths:
        return "missing"
    return ", ".join(str(width) for width in sorted(set(widths)))


def substitution_summary(report: FontNumericReport) -> str:
    if not report.tnum_substitutions:
        return "missing"
    return ", ".join(f"{source}->{target}({width})" for source, target, width in report.tnum_substitutions)


def markdown_report() -> str:
    reports = [numeric_report_for_font(path) for path in ALL_FONTS]
    all_present = all(report.exists for report in reports)
    all_default_digits_present = all(report.default_digits_present == 10 for report in reports)
    all_default_proportional = all(report.default_proportional for report in reports)
    all_tnum_feature_present = all(report.tnum_feature_present for report in reports)
    all_tnum_coverage = all(report.tnum_coverage == 10 for report in reports)
    all_tnum_tabular = all(report.tnum_tabular for report in reports)
    all_tnum_ready = (
        all_present
        and all_default_digits_present
        and all_default_proportional
        and all_tnum_feature_present
        and all_tnum_coverage
        and all_tnum_tabular
    )

    lines = [
        "# Numeric Feature Readiness",
        "",
        "This generated report checks the Google Fonts requirement that default",
        "ASCII numerals are proportional and complemented by a Tabular Numbers",
        "(`tnum`) feature.",
        "",
        "## Summary",
        "",
        f"- Built font files present: {yes_no(all_present)}",
        f"- Default ASCII digits present in every built font: {yes_no(all_default_digits_present)}",
        f"- Default ASCII digits are proportional in every built font: {yes_no(all_default_proportional)}",
        f"- `tnum` feature present in every built font: {yes_no(all_tnum_feature_present)}",
        f"- `tnum` substitutes all ten ASCII digits in every built font: {yes_no(all_tnum_coverage)}",
        f"- `tnum` substitutes to equal-width digits in every built font: {yes_no(all_tnum_tabular)}",
        f"- Numeric feature requirement ready: {yes_no(all_tnum_ready)}",
        "",
        "## Font Checks",
        "",
        "| Font | Exists | Default digits | Default widths | Proportional defaults | `tnum` | `tnum` coverage | `tnum` widths | Tabular alternates |",
        "| --- | --- | ---: | --- | --- | --- | ---: | --- | --- |",
    ]
    for report in reports:
        lines.append(
            "| `{path}` | {exists} | {digits}/10 | {default_widths} | {default_prop} | {tnum} | {coverage}/10 | {tnum_widths} | {tabular} |".format(
                path=report.path,
                exists=yes_no(report.exists),
                digits=report.default_digits_present,
                default_widths=width_set(report.default_widths),
                default_prop=yes_no(report.default_proportional),
                tnum=yes_no(report.tnum_feature_present),
                coverage=report.tnum_coverage,
                tnum_widths=width_set(report.tnum_widths),
                tabular=yes_no(report.tnum_tabular),
            )
        )

    lines.extend(
        [
            "",
            "## `tnum` Substitutions",
            "",
        ]
    )
    for report in reports:
        lines.append(f"- `{report.path}`: {substitution_summary(report)}")
        if report.unsupported_lookup_types:
            lines.append(
                f"  - Unsupported `tnum` lookup types seen: {', '.join(str(value) for value in report.unsupported_lookup_types)}"
            )

    lines.extend(
        [
            "",
            "## Required Follow-Up",
            "",
        ]
    )
    if all_tnum_ready:
        lines.append("- None for the current built fonts.")
    else:
        lines.extend(
            [
                "- Fix source feature or digit spacing work so every built font has",
                "  proportional default ASCII digits and full-width tabular alternates",
                "  reachable through `tnum`.",
            ]
        )

    lines.extend(
        [
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/requirements.html",
            "- https://googlefonts.github.io/gf-guide/production.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_numeric_feature_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
