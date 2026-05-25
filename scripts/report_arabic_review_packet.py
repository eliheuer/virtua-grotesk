#!/usr/bin/env python3
"""Generate a consolidated Arabic review packet for GF onboarding."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
GOOGLE_FONTS_CHECKOUT = ROOT.parents[1] / "forks/fonts"
OUTPUT_DEFAULT = Path("documentation/arabic-review-packet.md")


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def text_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def yes_no_from_line(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else "unknown"


def line_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def missing_category_count(heading: str, text: str) -> int:
    pattern = rf"## {re.escape(heading)}\n\nMissing: (\d+)"
    return first_int(pattern, text)


def markdown_report() -> str:
    missing_text = read_text("documentation/missing-gf-arabic-core.md")
    checklist_text = read_text("documentation/arabic-source-work-checklist.md")
    mark_text = read_text("documentation/arabic-mark-readiness.md")
    shaping_text = read_text("documentation/arabic-shaping-smoke-test.md")
    language_text = read_text("documentation/google-fonts-language-metadata.md")
    warnings_text = read_text("documentation/fontspector-warnings.md")
    glyphset_text = read_text("documentation/gf-glyphset-readiness.md")
    reachability_text = read_text("documentation/glyph-reachability.md")
    recent_text = read_text("documentation/recent-google-fonts-packages.md")
    estedad_metadata_path = GOOGLE_FONTS_CHECKOUT / "ofl/estedad/METADATA.pb"
    estedad_metadata = (
        estedad_metadata_path.read_text(encoding="utf-8")
        if estedad_metadata_path.exists()
        else ""
    )

    required = first_int(r"GF Arabic Core required codepoints: (\d+)", missing_text)
    missing = first_int(r"Missing codepoints: (\d+)", missing_text)
    letters = missing_category_count("Arabic letters", missing_text)
    marks = missing_category_count("Arabic marks", missing_text)
    numbers = missing_category_count("Arabic numbers", missing_text)
    punctuation = missing_category_count("Arabic punctuation and symbols", missing_text)
    shared = missing_category_count("Shared punctuation and symbols", missing_text)
    suggested_source_names = first_int(r"Suggested source glyph names: (\d+)", checklist_text)
    suggested_arabic_names = first_int(r"Suggested Arabic source glyph names: (\d+)", checklist_text)
    suggested_shared_names = first_int(r"Suggested shared punctuation/symbol glyph names: (\d+)", checklist_text)
    suggested_positional_names = first_int(r"Suggested Arabic positional-form glyph names: (\d+)", checklist_text)
    suggested_missing_both = first_int(r"Suggested glyph names missing in both masters: (\d+)", checklist_text)
    dotted_circle = yes_no_from_line(r"U\+25CC dotted circle present: (yes|no)", mark_text)
    source_anchors = yes_no_from_line(r"Source anchors present: (yes|no)", mark_text)
    mark_features = yes_no_from_line(r"Built mark/mkmk GPOS features present: (yes|no)", mark_text)
    present_marks = first_int(r"Present in current variable-font cmap: (\d+)", mark_text)
    required_marks = first_int(r"Required Arabic combining marks in `GF_Arabic_Core`: (\d+)", mark_text)
    font_count = len(re.findall(r"^## fonts/", shaping_text, flags=re.MULTILINE))
    arab_gsub_count = shaping_text.count("GSUB has `arab/dflt`: `true`")
    arab_gpos_count = shaping_text.count("GPOS has `arab/dflt`: `true`")
    notdef_counts = [int(value) for value in re.findall(r"\|\s*(\d+)\s*\| yes \|", shaping_text)]
    no_notdef = all(value == 0 for value in notdef_counts) if notdef_counts else False
    lam_alef_rows = len(re.findall(r"\|\s*yes\s*\|\s*yes\s*\|$", shaping_text, flags=re.MULTILINE))
    script_record = yes_no_from_line(r"Script record exists: (yes|no)", language_text)
    primary_script = text_value(r"Script id: `([^`]+)`", language_text)
    preview_subsets = yes_no_from_line(r"Preview `subsets` match target: (yes|no)", language_text)
    preview_primary = yes_no_from_line(r"Preview `primary_script` matches target: (yes|no)", language_text)
    compared_arabic_packages = text_value(r"Compared Arabic package examples present: ([^\n]+)", language_text)
    compared_arabic_subset = text_value(r"Compared examples with `arabic` subset: ([^\n]+)", language_text)
    compared_arab_primary = text_value(r"Compared examples with `primary_script: \"Arab\"`: ([^\n]+)", language_text)
    compared_non_noto_languages_absent = yes_no_from_line(
        r"Compared non-Noto Arabic examples omit `languages`: (yes|no)",
        language_text,
    )
    compared_non_noto_sample_text_absent = yes_no_from_line(
        r"Compared non-Noto Arabic examples omit `sample_text`: (yes|no)",
        language_text,
    )
    arabic_core_match = re.search(
        r"^\| `GF_Arabic_Core` \| Arabic \| (?P<required>\d+) \| (?P<present>\d+) \| (?P<missing>\d+) \| (?P<coverage>[^|]+) \|",
        glyphset_text,
        flags=re.MULTILINE,
    )
    arabic_core_row = (
        (
            f"{arabic_core_match.group('present')} / {arabic_core_match.group('required')} present; "
            f"{arabic_core_match.group('missing')} missing; "
            f"{arabic_core_match.group('coverage').strip()} coverage"
        )
        if arabic_core_match
        else "unknown"
    )
    dotted_warning = "dotted_circle" in warnings_text
    soft_dotted_warning = "soft_dotted" in warnings_text
    unreachable_arabic_helpers = first_int(r"Unique Arabic helper/form glyphs: (\d+)", reachability_text)
    unreachable_mark_helpers = first_int(r"Unique Arabic mark helper glyphs: (\d+)", reachability_text)
    estedad_primary_script = line_value(r'^primary_script: "([^"]+)"', estedad_metadata)
    estedad_config_yaml = line_value(r'^\s*config_yaml: "([^"]+)"', estedad_metadata)
    estedad_branch = line_value(r'^\s*branch: "([^"]+)"', estedad_metadata)
    estedad_commit = line_value(r'^\s*commit: "([^"]+)"', estedad_metadata)
    estedad_source_repo = line_value(r'^\s*repository_url: "([^"]+)"', estedad_metadata)
    estedad_subsets = ", ".join(re.findall(r'^subsets: "([^"]+)"', estedad_metadata, flags=re.MULTILINE))
    estedad_variable_source = "fonts/variable/Estedad[wght].ttf" in estedad_metadata
    estedad_upstream_info = (
        "yes"
        if "`ofl/estedad` | yes | `Estedad[wght].ttf`" in recent_text
        and "upstream_info.md" in recent_text
        else "unknown"
    )

    lines = [
        "# Arabic Review Packet",
        "",
        "This generated packet collects the Arabic evidence needed for the Google",
        "Fonts handoff. It does not replace drawing, native-reader review, or",
        "final Fontspector cleanup; it keeps the minimum Arabic target and proofing",
        "tasks visible in one place.",
        "",
        "## Summary",
        "",
        f"- Minimum target: `GF_Arabic_Core`",
        f"- Required codepoints: {required}",
        f"- Missing codepoints: {missing}",
        f"- GF Arabic Core coverage row: `{arabic_core_row}`",
        f"- Missing Arabic letters: {letters}",
        f"- Missing Arabic marks: {marks}",
        f"- Missing Arabic numbers: {numbers}",
        f"- Missing Arabic punctuation/symbols: {punctuation}",
        f"- Missing shared punctuation/symbols: {shared}",
        f"- Suggested source glyph names: {suggested_source_names}",
        f"- Suggested Arabic source glyph names: {suggested_arabic_names}",
        f"- Suggested shared punctuation/symbol glyph names: {suggested_shared_names}",
        f"- Suggested Arabic positional-form glyph names: {suggested_positional_names}",
        f"- Suggested glyph names missing in both masters: {suggested_missing_both}",
        f"- Required mark glyphs present: {present_marks} / {required_marks}",
        f"- U+25CC dotted circle present: {dotted_circle}",
        f"- Source anchors present: {source_anchors}",
        f"- Built mark/mkmk GPOS features present: {mark_features}",
        f"- Arabic GSUB smoke pass: {arab_gsub_count} / {font_count} fonts",
        f"- Arabic GPOS smoke pass: {arab_gpos_count} / {font_count} fonts",
        f"- Smoke strings shape without .notdef: {'yes' if no_notdef else 'no'}",
        f"- Lam-alef smoke rows passing: {lam_alef_rows}",
        f"- Metadata script record present: {script_record}",
        f"- Metadata primary script: `{primary_script}`",
        f"- Downstream preview subsets match target: {preview_subsets}",
        f"- Downstream preview primary_script matches target: {preview_primary}",
        f"- Compared Arabic package examples present: {compared_arabic_packages}",
        f"- Compared examples with `arabic` subset: {compared_arabic_subset}",
        f"- Compared examples with `primary_script: \"Arab\"`: {compared_arab_primary}",
        f"- Compared non-Noto Arabic examples omit `languages`: {compared_non_noto_languages_absent}",
        f"- Compared non-Noto Arabic examples omit `sample_text`: {compared_non_noto_sample_text_absent}",
        f"- Fontspector dotted_circle warning present: {'yes' if dotted_warning else 'no'}",
        f"- Fontspector soft_dotted warning present: {'yes' if soft_dotted_warning else 'no'}",
        f"- Unreachable Arabic helper/form glyphs: {unreachable_arabic_helpers}",
        f"- Unreachable Arabic mark helper glyphs: {unreachable_mark_helpers}",
        "",
        "## Drawing And Source Work Buckets",
        "",
        f"1. Draw {suggested_shared_names} shared punctuation and symbol glyphs also needed by Latin Core.",
        "2. Draw Extended Arabic-Indic digits U+06F0-U+06F9.",
        f"3. Draw Urdu/Persian joining letters and {suggested_positional_names} required positional-form glyph names.",
        "4. Add missing Arabic marks and U+25CC dotted circle.",
        "5. Add source anchors and compile mark/mkmk GPOS features.",
        "6. Resolve or intentionally remove unreachable Arabic helper and mark helper glyphs.",
        "7. Rebuild, regenerate reports, and visually proof shaped Arabic samples.",
        "",
        "## Recent Arabic Google Fonts Reference",
        "",
        "`documentation/google-fonts-language-metadata.md` compares the current",
        "Virtua metadata target against several Arabic `METADATA.pb` files in",
        "the synced local `google/fonts` checkout. Estedad remains the closest",
        "recent new-family package in that set; the broader table is package",
        "metadata evidence, not a drawing model for Virtua Grotesk.",
        "",
        f"- Package path: `ofl/estedad`",
        f"- Source repo: `{estedad_source_repo}`",
        f"- Source commit: `{estedad_commit}`",
        f"- Source branch: `{estedad_branch}`",
        f"- Primary script: `{estedad_primary_script}`",
        f"- Subsets: `{estedad_subsets}`",
        f"- Variable source file under `fonts/variable/`: {'yes' if estedad_variable_source else 'no'}",
        f"- `source.config_yaml`: `{estedad_config_yaml}`",
        f"- Downstream `upstream_info.md`: {estedad_upstream_info}",
        "",
        "Implications for Virtua Grotesk:",
        "",
        "- Keeping `primary_script: \"Arab\"` is aligned with a recent Arabic-script",
        "  new-family package while Arabic remains in first-submission scope.",
        "- `source.config_yaml` has recent Arabic-script precedent, but only when the",
        "  final Packager source strategy deliberately supports a reproducible source",
        "  build.",
        "- Estedad exposes its served variable font from `fonts/variable/`; Virtua's",
        "  generated-font policy still needs the separate Packager source-strategy",
        "  decision recorded in `documentation/google-fonts-decisions.md`.",
        "",
        "## Evidence Reports",
        "",
        "- `documentation/missing-gf-arabic-core.md`",
        "- `documentation/arabic-source-work-checklist.md`",
        "- `documentation/arabic-mark-readiness.md`",
        "- `documentation/arabic-shaping-smoke-test.md`",
        "- `documentation/google-fonts-language-metadata.md`",
        "- `documentation/gf-glyphset-readiness.md`",
        "- `documentation/recent-google-fonts-packages.md`",
        "- `documentation/glyph-reachability.md`",
        "- `documentation/fontspector-warnings.md`",
        "",
        "## References",
        "",
        "- https://googlefonts.github.io/gf-guide/requirements.html",
        "- https://googlefonts.github.io/gf-guide/lang.html",
        "- https://github.com/googlefonts/glyphsets",
        "",
    ]
    if "Missing Codepoint Worklist" in checklist_text:
        lines.extend(
            [
                "The source glyph worklist is intentionally kept in",
                "`documentation/arabic-source-work-checklist.md` so drawing work can",
                "use the per-codepoint UFO/master status table directly.",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_arabic_review_packet.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
