#!/usr/bin/env python3
"""Generate a downstream METADATA.pb readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/downstream-metadata-readiness.md")
VARIABLE_FONT = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
PREVIEW = Path("documentation/google-fonts-downstream-package-preview.md")
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"


def read_text(relative: Path | str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def name_value(font: TTFont, name_id: int) -> str:
    values = []
    for record in font["name"].names:
        if record.nameID == name_id:
            value = record.toUnicode()
            if value not in values:
                values.append(value)
    return values[0] if values else ""


def variable_font_metadata() -> dict[str, str | float]:
    font = TTFont(ROOT / VARIABLE_FONT)
    try:
        axes = {axis.axisTag: axis for axis in font["fvar"].axes}
        wght = axes["wght"]
        return {
            "filename": VARIABLE_FONT.name,
            "family": name_value(font, 1),
            "subfamily": name_value(font, 2),
            "full_name": name_value(font, 4),
            "post_script_name": name_value(font, 6),
            "copyright": name_value(font, 0),
            "wght_min": wght.minValue,
            "wght_default": wght.defaultValue,
            "wght_max": wght.maxValue,
        }
    finally:
        font.close()


def text_block_values(text: str, key: str) -> list[str]:
    return re.findall(rf'^\s*{re.escape(key)}:\s+"([^"]+)"', text, flags=re.MULTILINE)


def valid_latest_release_archive_url(url: str | None) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    return (
        parsed.scheme == "https"
        and parsed.netloc.lower() == "github.com"
        and len(parts) >= 6
        and parts[2] == "releases"
        and parts[3] == "download"
        and parts[-1].endswith(".zip")
    )


def has_line(text: str, line: str) -> bool:
    return re.search(rf"^\s*{re.escape(line)}\s*$", text, flags=re.MULTILINE) is not None


def pending_lines(text: str) -> list[tuple[int, str]]:
    lines = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "Pending" in line or PLACEHOLDER_URL in line:
            lines.append((line_number, line.strip()))
    return lines


def source_file_mappings(text: str) -> list[tuple[str, str]]:
    mappings: list[tuple[str, str]] = []
    for block in re.findall(r"files\s*\{(.*?)\n\s*\}", text, flags=re.DOTALL):
        source_match = re.search(r'source_file:\s+"([^"]+)"', block)
        dest_match = re.search(r'dest_file:\s+"([^"]+)"', block)
        if source_match and dest_match:
            mappings.append((source_match.group(1), dest_match.group(1)))
    return mappings


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def metadata_value(text: str, key: str) -> str:
    values = text_block_values(text, key)
    return values[0] if values else "missing"


def valid_date_added(value: str) -> bool:
    if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def markdown_report() -> str:
    preview = read_text(PREVIEW)
    prepare_script = read_text("scripts/prepare_downstream_metadata.py")
    font = variable_font_metadata()
    pending = pending_lines(preview)
    names = text_block_values(preview, "name")
    designers = text_block_values(preview, "designer")
    subsets = text_block_values(preview, "subsets")
    source_files = text_block_values(preview, "source_file")
    source_mappings = source_file_mappings(preview)
    has_static_entries = any(
        static_name in preview
        for static_name in [
            "VirtuaGrotesk-Regular.ttf",
            "VirtuaGrotesk-Medium.ttf",
            "VirtuaGrotesk-SemiBold.ttf",
            "VirtuaGrotesk-Bold.ttf",
        ]
    )
    designer_final = bool(designers and not any("Pending" in value for value in designers))
    date_added = metadata_value(preview, "date_added")
    date_added_final = valid_date_added(date_added)
    source_commits = text_block_values(preview, "commit")
    source_commit = source_commits[0] if source_commits else "missing"
    source_commit_final = re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None

    expected_source_files = [
        "OFL.txt",
        "fonts/variable/VirtuaGrotesk[wght].ttf",
        "documentation/ARTICLE.en_us.html",
        "documentation/readme-specimen.png",
    ]
    expected_source_mappings = [
        ("OFL.txt", "OFL.txt"),
        ("fonts/variable/VirtuaGrotesk[wght].ttf", "VirtuaGrotesk[wght].ttf"),
        ("documentation/ARTICLE.en_us.html", "article/ARTICLE.en_us.html"),
        ("documentation/readme-specimen.png", "article/readme-specimen.png"),
    ]
    all_expected_sources = all(path in source_files for path in expected_source_files)
    all_expected_mappings = all(mapping in source_mappings for mapping in expected_source_mappings)
    source_block_fields = [
        'repository_url: "https://github.com/eliheuer/virtua-grotesk"',
        'commit: "Pending final release/source commit"',
        'archive_url: "https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip"',
        'branch: "main"',
    ]
    source_block_shape = all(has_line(preview, line) for line in source_block_fields)
    has_config_yaml = has_line(preview, 'config_yaml: "sources/config.yaml"')
    archive_urls = text_block_values(preview, "archive_url")
    archive_url = archive_urls[0] if archive_urls else None
    has_archive_url = bool(archive_url)
    archive_url_required_for_latest_release = True
    archive_url_ready_for_latest_release = valid_latest_release_archive_url(archive_url)
    source_mode_review_needed = has_config_yaml
    axis_matches = (
        f'min_value: {font["wght_min"]:.1f}' in preview
        and f'max_value: {font["wght_max"]:.1f}' in preview
    )
    variable_names_match = (
        'style: "normal"' in preview
        and "weight: 400" in preview
        and f'filename: "{font["filename"]}"' in preview
        and f'post_script_name: "{font["post_script_name"]}"' in preview
        and f'full_name: "{font["full_name"]}"' in preview
    )
    metadata_review = read_text("documentation/google-fonts-metadata-review.md")
    canonical_semibold = "VirtuaGrotesk-SemiBold.ttf" in metadata_review
    unneeded_fields_absent = all(
        f"{key}:" not in preview
        for key in ("languages", "display_name", "minisite_url", "classifications", "sample_text", "tags")
    )
    helper_blocks_unapproved_optional_fields = (
        "PROHIBITED_OPTIONAL_FIELDS" in prepare_script
        and "optional metadata field requires explicit Google Fonts review before apply" in prepare_script
    )

    lines = [
        "# Downstream Metadata Readiness",
        "",
        "This generated report checks the draft downstream `METADATA.pb` preview",
        "against the current built variable font and the expected Google Fonts",
        "package source mapping. It does not replace a `gftools packager` run.",
        "",
        "## Summary",
        "",
        f"- Preview file: `{PREVIEW}`",
        f"- Top-level family name present: {yes_no(bool(names and names[0] == font['family']))}",
        f"- Top-level designer string final: {yes_no(designer_final)}",
        f"- `date_added` final date present: {yes_no(date_added_final)}",
        f"- `date_added` current value: `{date_added}`",
        f"- `source.commit` final hash present: {yes_no(source_commit_final)}",
        f"- `source.commit` current value: `{source_commit}`",
        f"- Variable filename/name fields match built font: {yes_no(variable_names_match)}",
        f"- Weight axis min/max match built `fvar`: {yes_no(axis_matches)}",
        f"- Variable font only in preview: {yes_no(not has_static_entries)}",
        f"- Expected subsets present and sorted: {yes_no(subsets == ['arabic', 'latin', 'menu'])}",
        f"- `primary_script: \"Arab\"` present: {yes_no('primary_script: \"Arab\"' in preview)}",
        f"- `category: \"SANS_SERIF\"` present: {yes_no('category: \"SANS_SERIF\"' in preview)}",
        f"- `stroke: \"SANS_SERIF\"` present: {yes_no('stroke: \"SANS_SERIF\"' in preview)}",
        f"- Non-Noto `languages` entries absent: {yes_no('languages:' not in preview)}",
        f"- Custom `sample_text` absent: {yes_no('sample_text:' not in preview)}",
        f"- `tags` field absent from METADATA preview: {yes_no('tags:' not in preview)}",
        f"- Unneeded optional display/classification fields absent: {yes_no(unneeded_fields_absent)}",
        f"- Apply helper blocks unapproved optional metadata fields: {yes_no(helper_blocks_unapproved_optional_fields)}",
        f"- Expected `source.files` present: {yes_no(all_expected_sources)}",
        f"- Expected `source.files` destination mappings present: {yes_no(all_expected_mappings)}",
        f"- Source block has repository, commit, archive_url, and branch fields: {yes_no(source_block_shape)}",
        f"- `source.archive_url` present: {yes_no(has_archive_url)}",
        f"- `source.archive_url` required for latest-release mode: {yes_no(archive_url_required_for_latest_release)}",
        f"- `source.archive_url` is GitHub release download `.zip`: {yes_no(archive_url_ready_for_latest_release)}",
        f"- `source.archive_url` satisfies latest-release mode: {yes_no(archive_url_ready_for_latest_release)}",
        f"- `source.config_yaml` present: {yes_no(has_config_yaml)}",
        f"- `source.config_yaml` needs source-strategy review: {yes_no(source_mode_review_needed)}",
        f"- Static style-name review uses GF `SemiBold` spelling: {yes_no(canonical_semibold)}",
        f"- Pending or placeholder metadata lines: {len(pending)}",
        "",
        "## Built Variable Font Evidence",
        "",
        "| Field | Built value |",
        "| --- | --- |",
        f"| filename | `{font['filename']}` |",
        f"| name ID 1 | `{font['family']}` |",
        f"| name ID 2 | `{font['subfamily']}` |",
        f"| name ID 4 | `{font['full_name']}` |",
        f"| name ID 6 | `{font['post_script_name']}` |",
        f"| name ID 0 | `{font['copyright']}` |",
        f"| wght min/default/max | `{font['wght_min']:.1f} / {font['wght_default']:.1f} / {font['wght_max']:.1f}` |",
        "",
        "## Preview Source Files",
        "",
        "| Source file | Destination file | Mapping present | Source local file present |",
        "| --- | --- | --- | --- |",
    ]

    for source, dest in expected_source_mappings:
        lines.append(
            f"| `{source}` | `{dest}` | {yes_no((source, dest) in source_mappings)} | "
            f"{yes_no((ROOT / source).exists())} |"
        )

    lines.extend(
        [
            "",
            "## Source Mode Compatibility",
            "",
            "| Source mode | `source.config_yaml` expectation | Preview status |",
            "| --- | --- | --- |",
            "| Default branch `source.files` | omit unless Google Fonts reviewer asks for build metadata | not selected |",
            "| Latest release/archive | omit unless the archive strategy is explicitly paired with build metadata; keep final `archive_url` | selected and previewed |",
            "| Build from source | keep `config_yaml: \"sources/config.yaml\"` | not selected |",
            "",
            (
                "`source.config_yaml` is omitted because the maintainer chose "
                "release/archive packaging. Keep it only for build-from-source, "
                "or if Google Fonts review asks for build metadata."
            ),
            "",
            (
                "For `GFT_PACKAGER_SOURCE_MODE=latest-release`, the preview "
                "includes the intended final GitHub release download `.zip` "
                "`archive_url` documented by the Google Fonts package guide."
            ),
            "",
            "## Date Added Policy",
            "",
            "The Google Fonts package guide notes that Packager automatically",
            "adds `date_added` for a new-family package, and the metadata guide",
            "defines it as the catalog date in `YYYY-MM-DD` format. Do not guess",
            "this value while the upstream source state is still changing.",
            "",
            "This repo keeps `date_added` as a blocking placeholder until the",
            "final package pass. If the checked preview is applied manually before",
            "Packager regenerates metadata, use the final package date supplied by",
            "Packager or Google Fonts review, then rerun `make downstream-metadata-check`.",
            "",
            "## Optional Metadata Field Policy",
            "",
            "The current first-submission preview intentionally omits `languages`,",
            "`display_name`, `minisite_url`, `classifications`, `sample_text`, and",
            "`tags`. The apply helper treats those as review-gated fields and blocks",
            "writing downstream `METADATA.pb` if any appear without an explicit",
            "Google Fonts review decision.",
            "",
            "## Pending Field Decision Map",
            "",
            "| Preview field | Current blocker | Decision or evidence that unblocks it | Apply surface |",
            "| --- | --- | --- | --- |",
            f"| `designer` | `{designers[0] if designers else 'missing'}` | Matching designer profile or profile request | `documentation/google-fonts-downstream-package-preview.md`; designer catalog draft if needed |",
            "| `copyright` | final URL applied; copyright-holder wording still reviewer/maintainer-owned | Confirm copyright-holder wording if it changes from project-author form | `OFL.txt`; source UFO fontinfo; metadata preview |",
            f"| `date_added` | `{date_added}` | Final Google Fonts package date, normally the Packager-generated date for the downstream PR | Metadata preview before applying to local `google/fonts` fork |",
            "| `source.repository_url` | final public URL applied | Public canonical repository URL decision | Metadata preview; Add Font issue; handoff docs |",
            "| `source.commit` | Pending final release/source commit | Final public source commit for the selected release/archive package | Metadata preview; release/source checklist |",
            "| `source.branch` | `main` | Final public branch for release/archive provenance | Metadata preview; package dry-run command context |",
            "| `source.config_yaml` | absent | Omit for release/archive unless Google Fonts review asks for build metadata | Metadata preview; prepare helper source mode |",
            "| `source.archive_url` | intended `v1.000` GitHub release download `.zip` URL present | Release asset must be created after final source work | Metadata preview before `GFT_PACKAGER_SOURCE_MODE=latest-release` |",
            "",
            "Do not apply the downstream metadata preview to the local `google/fonts`",
            "fork until every pending field above has either a final value or an",
            "explicit source-mode reason for being absent.",
        ]
    )

    lines.extend(
        [
            "",
            "## Pending Or Placeholder Lines",
            "",
        ]
    )
    if pending:
        lines.extend(f"- `{PREVIEW}:{line_number}` `{line}`" for line_number, line in pending)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Apply Before Downstream Packaging",
            "",
            "- Replace the pending commit value after the final release/source",
            "  commit.",
            "- Replace the pending `date_added` value only with the final package",
            "  date from Packager or Google Fonts review before applying downstream",
            "  metadata.",
            "- Create the final GitHub release archive before using latest-release",
            "  packaging, and keep `source.archive_url` on a GitHub release",
            "  download URL ending in `.zip`.",
            "- Rerun `make preflight` after metadata-preview or build changes so",
            "  proof evidence and generated reports stay synchronized.",
            "- Run `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` only",
            "  after the final release/archive source commit, archive, and downstream",
            "  metadata are synchronized.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_downstream_metadata_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
