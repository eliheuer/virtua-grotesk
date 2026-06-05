#!/usr/bin/env python3
"""Audit Google Fonts script/language metadata targets for Virtua Grotesk."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
OUTPUT_DEFAULT = Path("documentation/google-fonts/google-fonts-language-metadata.md")
DOWNSTREAM_PREVIEW = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")
SCRIPT_ID = "Arab"
SUBSETS = ("arabic", "latin", "menu")
CORE_LANGUAGES = ("ar_Arab", "fa_Arab", "ur_Arab")
RECENT_ARABIC_PACKAGES = (
    "ofl/estedad/METADATA.pb",
    "ofl/scheherazadenew/METADATA.pb",
    "ofl/playpensansarabic/METADATA.pb",
    "ofl/readexpro/METADATA.pb",
    "ofl/cairo/METADATA.pb",
    "ofl/amiri/METADATA.pb",
    "ofl/notosansarabic/METADATA.pb",
    "ofl/notonaskharabic/METADATA.pb",
    "ofl/notokufiarabic/METADATA.pb",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def first_value(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def preview_block() -> str:
    text = read_text(ROOT / DOWNSTREAM_PREVIEW)
    match = re.search(
        r"^## Expected METADATA\.pb shape\s*```text\n(?P<body>.*?)\n```",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if match:
        return match.group("body")
    match = re.search(r"```text\n(?P<body>.*?)\n```", text, flags=re.DOTALL)
    return match.group("body") if match else text


def preview_values(text: str, key: str) -> tuple[str, ...]:
    return tuple(re.findall(rf'^\s*{re.escape(key)}:\s*"([^"]+)"', text, flags=re.MULTILINE))


def package_metadata(gf_repo: Path, rel_path: str) -> dict[str, object]:
    path = gf_repo / rel_path
    text = read_text(path)
    name = first_value(r'^name:\s*"([^"]+)"', text)
    languages = tuple(re.findall(r'languages:\s*"([^"]+)"', text))
    sample_text = tuple(re.findall(r'sample_text:\s*"([^"]+)"', text))
    source_config = first_value(r'config_yaml:\s*"([^"]+)"', text)
    font_files = tuple(re.findall(r'filename:\s*"([^"]+)"', text))
    return {
        "path": rel_path,
        "name": name,
        "exists": path.exists(),
        "primary_script": first_value(r'primary_script:\s*"([^"]+)"', text),
        "subsets": tuple(re.findall(r'subsets:\s*"([^"]+)"', text)),
        "languages": languages,
        "sample_text": sample_text,
        "source_config": source_config,
        "font_count": len(font_files),
        "variable_fonts": tuple(font for font in font_files if "[" in font and "]" in font),
    }


def language_name(text: str) -> str:
    return first_value(r'name:\s*"([^"]+)"', text) or "missing"


def markdown_report(gf_repo: Path) -> str:
    preview = preview_block()
    preview_subsets = preview_values(preview, "subsets")
    preview_primary_scripts = preview_values(preview, "primary_script")
    preview_languages = preview_values(preview, "languages")
    preview_sample_text = preview_values(preview, "sample_text")
    preview_has_expected_subsets = preview_subsets == SUBSETS
    preview_has_primary_script = preview_primary_scripts == (SCRIPT_ID,)
    preview_languages_absent = not preview_languages
    preview_sample_text_absent = not preview_sample_text
    script_path = gf_repo / "lang/Lib/gflanguages/data/scripts/Arab.textproto"
    language_paths = {
        code: gf_repo / f"lang/Lib/gflanguages/data/languages/{code}.textproto"
        for code in CORE_LANGUAGES
    }
    script_text = read_text(script_path)
    script_id = first_value(r'id:\s*"([^"]+)"', script_text) or "missing"
    script_name = first_value(r'name:\s*"([^"]+)"', script_text) or "missing"
    package_rows = [package_metadata(gf_repo, rel_path) for rel_path in RECENT_ARABIC_PACKAGES]
    existing_package_rows = [row for row in package_rows if row["exists"]]
    non_noto_rows = [
        row
        for row in existing_package_rows
        if not str(row["name"]).startswith("Noto ")
    ]
    non_noto_languages_absent = all(not row["languages"] for row in non_noto_rows)
    non_noto_sample_text_absent = all(not row["sample_text"] for row in non_noto_rows)
    arabic_subset_packages = sum(
        1
        for row in existing_package_rows
        if "arabic" in row["subsets"]
    )
    arab_primary_packages = sum(
        1
        for row in existing_package_rows
        if row["primary_script"] == SCRIPT_ID
    )

    lines = [
        "# Google Fonts Language Metadata",
        "",
        "This generated report records the local Google Fonts language metadata",
        "evidence behind the current Virtua Grotesk downstream metadata target:",
        "`subsets: \"arabic\"` and `primary_script: \"Arab\"`.",
        "",
        "## Local Google Fonts Lang Data",
        "",
        f"- Checkout: `{gf_repo}`",
        f"- Script record: `{script_path.relative_to(gf_repo)}`",
        f"- Script record exists: {yes_no(script_path.exists())}",
        f"- Script id: `{script_id}`",
        f"- Script name: `{script_name}`",
        "",
        "## Arabic Core Language Records",
        "",
        "| Language code | Exists | Script | Name |",
        "| --- | --- | --- | --- |",
    ]
    for code, path in language_paths.items():
        text = read_text(path)
        script = first_value(r'script:\s*"([^"]+)"', text) or "missing"
        name = language_name(text)
        lines.append(
            f"| `{code}` | {yes_no(path.exists())} | "
            f"`{script}` | "
            f"`{name}` |"
        )

    lines.extend(
        [
            "",
            "## Current Virtua Grotesk Target",
            "",
            f"- `primary_script`: `{SCRIPT_ID}`",
            f"- Expected downstream subsets after drawing: {', '.join(f'`{subset}`' for subset in SUBSETS)}",
            f"- Preview `subsets` match target: {yes_no(preview_has_expected_subsets)}",
            f"- Preview `primary_script` matches target: {yes_no(preview_has_primary_script)}",
            f"- Preview non-Noto `languages` entries absent: {yes_no(preview_languages_absent)}",
            f"- Preview custom `sample_text` absent: {yes_no(preview_sample_text_absent)}",
            f"- Compared Arabic package examples present: {len(existing_package_rows)} / {len(package_rows)}",
            f"- Compared examples with `arabic` subset: {arabic_subset_packages} / {len(existing_package_rows)}",
            f"- Compared examples with `primary_script: \"Arab\"`: {arab_primary_packages} / {len(existing_package_rows)}",
            f"- Compared non-Noto Arabic examples omit `languages`: {yes_no(non_noto_languages_absent)}",
            f"- Compared non-Noto Arabic examples omit `sample_text`: {yes_no(non_noto_sample_text_absent)}",
            "- Do not add `languages` entries for this non-Noto family unless Google",
            "  Fonts review asks for a narrower language scope.",
            "- Do not add custom `sample_text` unless Google Fonts review asks for it",
            "  or the default Arabic specimen text is unsuitable.",
            "",
            "## Downstream Preview Alignment",
            "",
            "| Field | Preview value | Target | Aligned |",
            "| --- | --- | --- | --- |",
            f"| `subsets` | {', '.join(f'`{subset}`' for subset in preview_subsets) if preview_subsets else 'missing'} | {', '.join(f'`{subset}`' for subset in SUBSETS)} | {yes_no(preview_has_expected_subsets)} |",
            f"| `primary_script` | {', '.join(f'`{script}`' for script in preview_primary_scripts) if preview_primary_scripts else 'missing'} | `{SCRIPT_ID}` | {yes_no(preview_has_primary_script)} |",
            f"| `languages` | {', '.join(f'`{language}`' for language in preview_languages) if preview_languages else 'absent'} | absent for non-Noto package | {yes_no(preview_languages_absent)} |",
            f"| `sample_text` | {', '.join(f'`{sample}`' for sample in preview_sample_text) if preview_sample_text else 'absent'} | absent unless reviewer requests override | {yes_no(preview_sample_text_absent)} |",
            "",
            "## Recent Arabic Package Evidence",
            "",
            "This table reads current `METADATA.pb` files from the local synced",
            "`google/fonts` checkout. Noto Arabic families are included to show the",
            "`languages` exception; non-Noto Arabic examples generally omit",
            "`languages` and rely on generated language support.",
            "",
            "| Package | Family | Exists | Fonts | Variable | primary_script | Has arabic subset | Languages | sample_text | config_yaml | Subsets |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in package_rows:
        subsets = row["subsets"]
        languages = row["languages"]
        sample_text = row["sample_text"]
        variable_fonts = row["variable_fonts"]
        assert isinstance(subsets, tuple)
        assert isinstance(languages, tuple)
        assert isinstance(sample_text, tuple)
        assert isinstance(variable_fonts, tuple)
        lines.append(
            f"| `{row['path']}` | `{row['name'] or 'missing'}` | {yes_no(bool(row['exists']))} | "
            f"{row['font_count']} | {yes_no(bool(variable_fonts))} | "
            f"`{row['primary_script'] or 'none'}` | {yes_no('arabic' in subsets)} | "
            f"{len(languages)} | {len(sample_text)} | "
            f"`{row['source_config'] or 'none'}` | "
            f"{', '.join(f'`{subset}`' for subset in subsets) if subsets else 'missing'} |"
        )

    lines.extend(
        [
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://googlefonts.github.io/gf-guide/lang.html",
            "- https://googlefonts.github.io/gf-guide/googlefonts.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_gf_language_metadata.py [google_fonts_repo] [output.md]")
    if len(argv) == 1:
        return DEFAULT_GF_REPO, OUTPUT_DEFAULT
    if len(argv) == 2:
        return DEFAULT_GF_REPO, Path(argv[1])
    return Path(argv[1]), Path(argv[2])


def main(argv: list[str]) -> int:
    gf_repo, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(gf_repo), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
