#!/usr/bin/env python3
"""Report current Google Fonts production-requirements readiness."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts-production-requirements.md")
VARIABLE_FONT = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
STATIC_FONTS = [
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
ALL_FONTS = [VARIABLE_FONT, *STATIC_FONTS]
ALLOWED_FVAR_NAMES = {
    "Thin",
    "ExtraLight",
    "Light",
    "Regular",
    "Medium",
    "SemiBold",
    "Bold",
    "ExtraBold",
    "Black",
}


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def fontspector_counts(report_text: str) -> tuple[int, int, int]:
    match = re.search(
        r"### Summary\s*\n(?P<header>\|[^\n]*\|)\s*\n\|[^\n]*\|\s*\n(?P<values>\|[^\n]*\|)",
        report_text,
        flags=re.MULTILINE,
    )
    if not match:
        return (0, 0, 0)
    headers = [cell.strip() for cell in match.group("header").strip("|").split("|")]
    values = [cell.strip() for cell in match.group("values").strip("|").split("|")]
    counts = dict(zip(headers, values, strict=False))
    return (
        int(counts.get("🔥 FAIL", 0)),
        int(counts.get("⚠️ WARN", 0)),
        int(counts.get("✅ PASS", 0)),
    )


def decision_counts(decisions_text: str) -> tuple[int, int, list[str]]:
    open_decisions: list[str] = []
    decided = 0
    for match in re.finditer(
        r"^## (?P<name>[^\n]+)\n(?P<body>.*?)(?=^## |\Z)",
        decisions_text,
        flags=re.MULTILINE | re.DOTALL,
    ):
        status_match = re.search(r"^Status: ([a-z]+)$", match.group("body"), flags=re.MULTILINE)
        status = status_match.group(1) if status_match else "unknown"
        if status == "open":
            open_decisions.append(match.group("name"))
        elif status == "decided":
            decided += 1
    return len(open_decisions), decided, open_decisions


def feature_tags(font: TTFont) -> set[str]:
    tags: set[str] = set()
    for table_tag in ("GSUB", "GPOS"):
        if table_tag not in font:
            continue
        feature_list = font[table_tag].table.FeatureList
        if feature_list is None:
            continue
        tags.update(record.FeatureTag for record in feature_list.FeatureRecord)
    return tags


def name(font: TTFont, name_id: int) -> str:
    record = font["name"].getDebugName(name_id)
    return record or ""


def font_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative in ALL_FONTS:
        path = ROOT / relative
        if not path.exists():
            rows.append(
                {
                    "path": str(relative),
                    "exists": False,
                    "ttf": relative.suffix == ".ttf",
                    "fs_type": "missing",
                    "version": "missing",
                    "typo": "missing",
                    "hhea": "missing",
                    "tnum": False,
                }
            )
            continue
        font = TTFont(path)
        os2 = font["OS/2"]
        hhea = font["hhea"]
        rows.append(
            {
                "path": str(relative),
                "exists": True,
                "ttf": relative.suffix == ".ttf",
                "fs_type": os2.fsType,
                "version": name(font, 5),
                "typo": f"{os2.sTypoAscender}/{os2.sTypoDescender}/{os2.sTypoLineGap}",
                "hhea": f"{hhea.ascent}/{hhea.descent}/{hhea.lineGap}",
                "tnum": "tnum" in feature_tags(font),
            }
        )
        font.close()
    return rows


def variable_checks() -> dict[str, object]:
    font = TTFont(ROOT / VARIABLE_FONT)
    fvar = font["fvar"]
    axis_tags = [axis.axisTag for axis in fvar.axes]
    wght = next(axis for axis in fvar.axes if axis.axisTag == "wght")
    instance_names = [name(font, instance.subfamilyNameID) for instance in fvar.instances]
    instance_weights = [int(instance.coordinates["wght"]) for instance in fvar.instances]
    checks = {
        "filename": VARIABLE_FONT.name,
        "filename_ok": VARIABLE_FONT.name == "VirtuaGrotesk[wght].ttf",
        "has_fvar": "fvar" in font,
        "has_stat": "STAT" in font,
        "has_avar": "avar" in font,
        "axis_tags": axis_tags,
        "wght_min": int(wght.minValue),
        "wght_default": int(wght.defaultValue),
        "wght_max": int(wght.maxValue),
        "wght_includes_400": int(wght.minValue) <= 400 <= int(wght.maxValue),
        "instance_names": instance_names,
        "instance_weights": instance_weights,
        "instances_allowed": all(instance_name in ALLOWED_FVAR_NAMES for instance_name in instance_names),
    }
    font.close()
    return checks


def markdown_report() -> str:
    rows = font_rows()
    variable = variable_checks()
    latin_text = read_text("documentation/missing-gf-latin-core.md")
    arabic_text = read_text("documentation/missing-gf-arabic-core.md")
    fontspector_text = read_text("documentation/fontspector-googlefonts-report.md")
    numeric_text = read_text("documentation/numeric-feature-readiness.md")
    source_text = read_text("documentation/source-ufo-metadata.md")
    upstream_text = read_text("documentation/upstream-structure-readiness.md")
    decisions_text = read_text("documentation/google-fonts-decisions.md")

    latin_missing = first_int(r"Missing codepoints: (\d+)", latin_text)
    arabic_missing = first_int(r"Missing codepoints: (\d+)", arabic_text)
    fail_count, warn_count, pass_count = fontspector_counts(fontspector_text)
    open_decision_count, decided_decision_count, open_decisions = decision_counts(decisions_text)
    all_fonts_present = all(bool(row["exists"]) for row in rows)
    all_ttf = all(bool(row["ttf"]) for row in rows)
    all_fstype_zero = all(row["fs_type"] == 0 for row in rows)
    all_versions_1000 = all(str(row["version"]).startswith("Version 1.000") for row in rows)
    all_metrics_match = all(row["typo"] == "1024/-296/0" and row["hhea"] == "1024/-296/0" for row in rows)
    any_tnum = any(bool(row["tnum"]) for row in rows)
    numeric_ready = "Numeric feature requirement ready: yes" in numeric_text
    default_digits_proportional = "Default ASCII digits are proportional in every built font: yes" in numeric_text
    tnum_full_substitution = "`tnum` substitutes all ten ASCII digits in every built font: yes" in numeric_text
    tnum_tabular = "`tnum` substitutes to equal-width digits in every built font: yes" in numeric_text

    lines = [
        "# Google Fonts Production Requirements Audit",
        "",
        "This generated report maps current built fonts and source evidence to",
        "Google Fonts production and font-file requirements that can be checked",
        "locally. It separates satisfied engineering requirements from drawing,",
        "source-feature, and maintainer-decision blockers.",
        "",
        "## Summary",
        "",
        f"- Built TTF outputs present: {yes_no(all_fonts_present)}",
        f"- All handoff font binaries are `.ttf`: {yes_no(all_ttf)}",
        f"- One-command build path present: {yes_no('build.sh invokes gftools builder: yes' in upstream_text)}",
        f"- Open-source build toolchain documented: {yes_no('fontmake' in read_text('requirements.in') and 'gftools' in read_text('requirements.in'))}",
        f"- Source UFO/designspace inputs present: {yes_no('Active source inputs present: 4 / 4' in upstream_text)}",
        f"- Installable embedding fsType across built fonts: {yes_no(all_fstype_zero)}",
        f"- Version strings match first-submission version `1.000`: {yes_no(all_versions_1000)}",
        f"- Vertical metrics match GF source metrics: {yes_no(all_metrics_match)}",
        f"- Variable font has `fvar`: {yes_no(bool(variable['has_fvar']))}",
        f"- Variable font has `STAT`: {yes_no(bool(variable['has_stat']))}",
        f"- Variable `wght` axis includes 400: {yes_no(bool(variable['wght_includes_400']))}",
        f"- Variable `fvar` instance names are GF-allowed: {yes_no(bool(variable['instances_allowed']))}",
        f"- Tabular Numbers (`tnum`) feature present in any built font: {yes_no(any_tnum)}",
        f"- Default ASCII digits are proportional in every built font: {yes_no(default_digits_proportional)}",
        f"- `tnum` substitutes all ten ASCII digits in every built font: {yes_no(tnum_full_substitution)}",
        f"- `tnum` substitutes to equal-width digits in every built font: {yes_no(tnum_tabular)}",
        f"- Numeric feature requirement ready: {yes_no(numeric_ready)}",
        f"- GF Latin Core missing codepoints: {latin_missing}",
        f"- GF Arabic Core missing codepoints: {arabic_missing}",
        f"- Fontspector googlefonts profile: {fail_count} FAIL, {warn_count} WARN, {pass_count} PASS",
        f"- Open maintainer decisions: {open_decision_count}",
        f"- Decided maintainer decisions: {decided_decision_count}",
        f"- Open decision names: {', '.join(open_decisions) if open_decisions else 'none'}",
        "",
        "## Built Font Requirements",
        "",
        "| Font | Exists | TTF | fsType | Version | Typo metrics | hhea metrics | tnum |",
        "| --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| `{path}` | {exists} | {ttf} | {fs_type} | `{version}` | `{typo}` | `{hhea}` | {tnum} |".format(
                path=row["path"],
                exists=yes_no(bool(row["exists"])),
                ttf=yes_no(bool(row["ttf"])),
                fs_type=row["fs_type"],
                version=row["version"],
                typo=row["typo"],
                hhea=row["hhea"],
                tnum=yes_no(bool(row["tnum"])),
            )
        )

    lines.extend(
        [
            "",
            "## Variable Font Requirements",
            "",
            f"- Filename: `{variable['filename']}`",
            f"- Filename uses GF axis-bracket convention: {yes_no(bool(variable['filename_ok']))}",
            f"- Axis tags: {', '.join(f'`{tag}`' for tag in variable['axis_tags'])}",
            f"- `wght` min/default/max: {variable['wght_min']}/{variable['wght_default']}/{variable['wght_max']}",
            f"- `fvar` instances: {', '.join(f'{name} {weight}' for name, weight in zip(variable['instance_names'], variable['instance_weights']))}",
            f"- `avar` present: {yes_no(bool(variable['has_avar']))}",
            "",
            "## Outstanding Requirement Buckets",
            "",
            "- Drawing/source coverage: complete GF Latin Core and GF Arabic Core coverage.",
        ]
    )
    if numeric_ready:
        lines.extend(
            [
                "- Numeric feature status: default ASCII digits are proportional and the",
                "  current `tnum` feature substitutes all ten digits to equal-width",
                "  tabular alternates, so numeric feature readiness is no longer a",
                "  production blocker.",
            ]
        )
    else:
        lines.extend(
            [
                "- Numeric feature work: add or explicitly defer a Tabular Numbers (`tnum`)",
                "  feature. The GF requirements recommend proportional default numerals",
                "  complemented by `tnum`; the current built fonts do not expose it.",
            ]
        )
    lines.extend(
        [
            "- Fontspector: resolve current FAILs, or record explicit Google Fonts",
            "  reviewer acceptance for any remaining FAIL before submission.",
            "- Maintainer decisions: only the open decisions listed above remain",
            "  unresolved here; decided items stay covered by their dedicated",
            "  readiness reports and preflight checks.",
            "",
            "## Evidence Reports",
            "",
            "- `documentation/upstream-structure-readiness.md`",
            "- `documentation/source-ufo-metadata.md`",
            "- `documentation/generated-font-metadata.md`",
            "- `documentation/variable-font-metadata.md`",
            "- `documentation/numeric-feature-readiness.md`",
            "- `documentation/google-fonts-axis-registry-audit.md`",
            "- `documentation/missing-gf-latin-core.md`",
            "- `documentation/missing-gf-arabic-core.md`",
            "- `documentation/fontspector-googlefonts-report.md`",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/production.html",
            "- https://googlefonts.github.io/gf-guide/requirements.html",
            "- https://googlefonts.github.io/gf-guide/variable.html",
            "- https://googlefonts.github.io/gf-guide/statics.html",
            "- https://googlefonts.github.io/gf-guide/build.html",
            "",
        ]
    )
    assert "# Source UFO Metadata" in source_text
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_production_requirements.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
