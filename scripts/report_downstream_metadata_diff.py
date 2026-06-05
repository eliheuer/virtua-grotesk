#!/usr/bin/env python3
"""Compare the local Packager METADATA.pb with the expected preview."""

from __future__ import annotations

import ast
from datetime import datetime
import importlib.util
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/downstream-metadata-diff.md")
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
DOWNSTREAM_METADATA = GF_REPO_PATH / "ofl/virtuagrotesk/METADATA.pb"
PREVIEW = ROOT / "documentation/google-fonts/google-fonts-downstream-package-preview.md"
PREPARE_HELPER = ROOT / "scripts/prepare_downstream_metadata.py"
STARTER_TEMPLATE_MARKERS = [
    'designer: "UNKNOWN"',
    'repository_url: "https://github.com/user/repo"',
    'fonts/variable/MyFont[wght].ttf',
    'primary_script: "Deva"',
]
EXPECTED_LINES = [
    'name: "Virtua Grotesk"',
    'license: "OFL"',
    'category: "SANS_SERIF"',
    'filename: "VirtuaGrotesk[wght].ttf"',
    'post_script_name: "VirtuaGrotesk-Regular"',
    'full_name: "Virtua Grotesk Regular"',
    'subsets: "arabic"',
    'subsets: "latin"',
    'subsets: "menu"',
    'tag: "wght"',
    'min_value: 400.0',
    'max_value: 700.0',
    'source_file: "OFL.txt"',
    'dest_file: "OFL.txt"',
    'source_file: "fonts/variable/VirtuaGrotesk[wght].ttf"',
    'dest_file: "VirtuaGrotesk[wght].ttf"',
    'source_file: "documentation/google-fonts/ARTICLE.en_us.html"',
    'dest_file: "article/ARTICLE.en_us.html"',
    'source_file: "documentation/assets/readme-specimen.png"',
    'dest_file: "article/readme-specimen.png"',
    'primary_script: "Arab"',
    'stroke: "SANS_SERIF"',
]
CONFIG_YAML_LINE = 'config_yaml: "sources/config.yaml"'
DATE_ADDED_REVIEW_LINE = 'date_added with final valid "YYYY-MM-DD" Google Fonts date'


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def load_prepare_helper():
    spec = importlib.util.spec_from_file_location("prepare_downstream_metadata", PREPARE_HELPER)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fenced_metadata_preview(text: str) -> str:
    match = re.search(r"## Expected METADATA\.pb shape\s*\n+```text\n(.*?)\n```", text, flags=re.DOTALL)
    return match.group(1) if match else ""


def line_present(text: str, line: str) -> bool:
    return re.search(rf"^\s*{re.escape(line)}\s*$", text, flags=re.MULTILINE) is not None


def valid_date_added(text: str) -> bool:
    match = re.search(r'^\s*date_added:\s+"(20\d{2}-\d{2}-\d{2})"\s*$', text, flags=re.MULTILINE)
    if not match:
        return False
    try:
        datetime.strptime(match.group(1), "%Y-%m-%d")
    except ValueError:
        return False
    return True


def source_mappings(text: str) -> list[tuple[str, str]]:
    mappings: list[tuple[str, str]] = []
    for block in re.findall(r"files\s*\{(.*?)\n\s*\}", text, flags=re.DOTALL):
        source = re.search(r'source_file:\s+"([^"]+)"', block)
        dest = re.search(r'dest_file:\s+"([^"]+)"', block)
        if source and dest:
            mappings.append((source.group(1), dest.group(1)))
    return mappings


def helper_required_lines() -> list[str]:
    if not PREPARE_HELPER.exists():
        return []
    tree = ast.parse(PREPARE_HELPER.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "REQUIRED_LINES" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        if isinstance(value, tuple) and all(isinstance(item, str) for item in value):
            return list(value)
    return []


def markdown_report() -> str:
    preview_text = PREVIEW.read_text(encoding="utf-8")
    expected_text = fenced_metadata_preview(preview_text)
    actual_exists = DOWNSTREAM_METADATA.exists()
    actual_text = DOWNSTREAM_METADATA.read_text(encoding="utf-8") if actual_exists else ""
    prepare_helper = load_prepare_helper()
    prepare_source_mode = (
        prepare_helper.source_mode_from_environment() if prepare_helper is not None else "unknown"
    )
    try:
        prepare_metadata = (
            prepare_helper.extract_metadata(preview_text) if prepare_helper is not None else ""
        )
        prepare_errors = (
            prepare_helper.validation_errors(prepare_metadata, GF_REPO_PATH, prepare_source_mode)
            if prepare_helper is not None
            else ["prepare helper could not be loaded"]
        )
    except ValueError as error:
        prepare_errors = [f"prepare helper could not extract preview: {error}"]
    ready_to_apply = not prepare_errors
    starter_markers = [marker for marker in STARTER_TEMPLATE_MARKERS if marker in actual_text]
    starter_template = bool(starter_markers)
    missing_expected = [line for line in EXPECTED_LINES if not line_present(actual_text, line)]
    config_yaml_present = line_present(actual_text, CONFIG_YAML_LINE)
    preview_config_yaml_present = line_present(expected_text, CONFIG_YAML_LINE)
    unexpected_starter_mappings = [
        mapping for mapping in source_mappings(actual_text) if mapping not in source_mappings(expected_text)
    ]
    helper_lines = helper_required_lines()
    missing_from_helper = sorted(set(EXPECTED_LINES) - set(helper_lines))
    extra_in_helper = sorted(set(helper_lines) - set(EXPECTED_LINES))
    date_added_final = valid_date_added(expected_text)
    helper_checks_date_added = (
        "valid_date_added" in PREPARE_HELPER.read_text(encoding="utf-8")
        if PREPARE_HELPER.exists()
        else False
    )
    helper_checks_source_commit = (
        "SOURCE_COMMIT_PATTERN" in PREPARE_HELPER.read_text(encoding="utf-8")
        if PREPARE_HELPER.exists()
        else False
    )
    helper_checks_latest_release_archive_url = (
        "valid_latest_release_archive_url" in PREPARE_HELPER.read_text(encoding="utf-8")
        and "release download URL ending in .zip" in PREPARE_HELPER.read_text(encoding="utf-8")
        if PREPARE_HELPER.exists()
        else False
    )

    lines = [
        "# Downstream Metadata Diff",
        "",
        "This generated report compares the local Packager-created downstream",
        "`METADATA.pb` with the expected repository preview. It is intentionally",
        "a review aid only; it does not apply maintainer decisions or edit the",
        "local `google/fonts` checkout.",
        "",
        "## Summary",
        "",
        "- Expected preview: `documentation/google-fonts/google-fonts-downstream-package-preview.md`",
        f"- Actual downstream metadata: `{DOWNSTREAM_METADATA}`",
        f"- Actual downstream METADATA.pb present: {yes_no(actual_exists)}",
        f"- Actual downstream METADATA.pb is starter template: {yes_no(starter_template)}",
        f"- Starter-template markers present: {len(starter_markers)} / {len(STARTER_TEMPLATE_MARKERS)}",
        f"- Expected metadata lines missing from actual downstream file: {len(missing_expected)} / {len(EXPECTED_LINES)}",
        f"- Actual downstream `source.config_yaml` present: {yes_no(config_yaml_present)}",
        f"- Expected preview `source.config_yaml` present: {yes_no(preview_config_yaml_present)}",
        f"- Expected preview has final `date_added`: {yes_no(date_added_final)}",
        f"- Unexpected starter source mappings: {len(unexpected_starter_mappings)}",
        f"- Prepare helper source mode: `{prepare_source_mode}`",
        f"- Ready to apply preview via helper: {yes_no(ready_to_apply)}",
        f"- Prepare helper blocking findings: {len(prepare_errors)}",
        f"- Prepare helper required-line count: {len(helper_lines)}",
        f"- Diff/helper required-line lists match: {yes_no(not missing_from_helper and not extra_in_helper)}",
        "",
        "## Starter Template Markers",
        "",
    ]
    lines.extend(f"- `{marker}`" for marker in starter_markers)
    if not starter_markers:
        lines.append("- None")

    lines.extend(["", "## Missing Expected Lines", ""])
    if missing_expected:
        lines.extend(f"- `{line}`" for line in missing_expected)
    else:
        lines.append("- None")

    lines.extend(["", "## Actual Source Mappings Not In Preview", ""])
    if unexpected_starter_mappings:
        lines.extend(f"- `{source}` -> `{dest}`" for source, dest in unexpected_starter_mappings)
    else:
        lines.append("- None")

    lines.extend(["", "## Replacement Readiness Gate", ""])
    lines.extend(
        [
            "This mirrors the same validation used by `make downstream-metadata-check`.",
            "It intentionally does not run `--apply` or write to the local",
            "`google/fonts` checkout.",
            "",
            f"- Source mode: `{prepare_source_mode}`",
            f"- Ready to apply: {yes_no(ready_to_apply)}",
            "- Apply command intentionally not run: yes",
            "- Check command: `make downstream-metadata-check`",
            "- Apply command after all blockers clear: `scripts/prepare_downstream_metadata.py --apply`",
            "",
            "Blocking findings:",
        ]
    )
    if prepare_errors:
        lines.extend(f"- {error}" for error in prepare_errors)
    else:
        lines.append("- None")

    lines.extend(["", "## Prepare Helper Alignment", ""])
    lines.extend(
        [
            "The dry-run/apply helper must reject the same required-line",
            "regressions this report tracks, otherwise a bad preview could be",
            "written into the local `google/fonts` fork before the diff report",
            "flags it.",
            "",
            f"- Expected lines in diff report: {len(EXPECTED_LINES)}",
            f"- Required lines in prepare helper: {len(helper_lines)}",
            f"- Date-added format validation in prepare helper: {yes_no(helper_checks_date_added)}",
            f"- Source commit hash validation in prepare helper: {yes_no(helper_checks_source_commit)}",
            f"- Latest-release archive URL validation in prepare helper: {yes_no(helper_checks_latest_release_archive_url)}",
            f"- Missing from helper: {', '.join(f'`{line}`' for line in missing_from_helper) if missing_from_helper else 'none'}",
            f"- Extra in helper: {', '.join(f'`{line}`' for line in extra_in_helper) if extra_in_helper else 'none'}",
            f"- Date-added final requirement: `{DATE_ADDED_REVIEW_LINE}`",
        ]
    )

    lines.extend(
        [
            "",
            "## Apply Before Rerunning Packager",
            "",
            "- Replace the Packager starter template with the final downstream",
            "  metadata after the selected release/archive commit, branch,",
            "  archive, and `date_added` value are settled.",
            "- First run `make downstream-metadata-check` to validate the preview",
            "  without writing to the local `google/fonts` checkout.",
            "- When that dry run reports `Ready to apply: yes`, run",
            "  `scripts/prepare_downstream_metadata.py --apply` to write",
            "  `/Users/eli/GH/forks/fonts/ofl/virtuagrotesk/METADATA.pb`.",
            "- Use `documentation/google-fonts/google-fonts-downstream-package-preview.md` as",
            "  the expected shape, then rerun `make preflight` so proof evidence",
            "  and generated reports stay synchronized before",
            "  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.",
            "- Keep `source.config_yaml` only when the selected Packager source mode",
            "  is build-from-source, unless Google Fonts review asks for build metadata.",
            "- Keep the first rerun as a no-PR dry run until the generated package",
            "  is reviewed.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_downstream_metadata_diff.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
