#!/usr/bin/env python3
"""Audit local files intended for Google Fonts Packager source.files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/package-source-files-audit.md")
PREVIEW_PATH = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")

SOURCE_FILE_PURPOSES = {
    "OFL.txt": "license",
    "fonts/variable/VirtuaGrotesk[wght].ttf": "served variable font",
    "documentation/google-fonts/ARTICLE.en_us.html": "article HTML",
    "documentation/assets/readme-specimen.png": "article image",
}
EXPECTED_DEST_FILES = {
    "OFL.txt": "OFL.txt",
    "fonts/variable/VirtuaGrotesk[wght].ttf": "VirtuaGrotesk[wght].ttf",
    "documentation/google-fonts/ARTICLE.en_us.html": "article/ARTICLE.en_us.html",
    "documentation/assets/readme-specimen.png": "article/readme-specimen.png",
}
BUILD_FROM_SOURCE_FILES = [
    "sources/config.yaml",
    "sources/VirtuaGrotesk.designspace",
    "sources/VirtuaGrotesk-Regular.ufo",
    "sources/VirtuaGrotesk-Bold.ufo",
    "build.sh",
    "requirements.txt",
]
STATIC_FONT_OUTPUTS = [
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
BUILD_SCRIPT = Path("build.sh")
GF_BUILDER_CONFIG = Path("sources/config.yaml")
LATEST_RELEASE_ARCHIVE_URL_PATTERN = re.compile(
    r'^https://github\.com/[^/"]+/[^/"]+/releases/download/[^/"]+/[^"]+\.zip$'
)


@dataclass(frozen=True)
class FileStatus:
    source_file: str
    dest_file: str
    purpose: str
    exists: bool
    ignored: bool
    tracked: bool


def git_check_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def git_is_tracked(path: str) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--", path],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


def preview_source_files() -> list[tuple[str, str, str]]:
    preview = (ROOT / PREVIEW_PATH).read_text(encoding="utf-8")
    pairs = []
    for match in re.finditer(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        preview,
        flags=re.DOTALL,
    ):
        source_file, dest_file = match.groups()
        purpose = SOURCE_FILE_PURPOSES.get(source_file, "package source")
        pairs.append((source_file, dest_file, purpose))
    return pairs


def text_values(text: str, key: str) -> list[str]:
    return re.findall(rf'^\s*{re.escape(key)}:\s*"([^"]+)"', text, flags=re.MULTILINE)


def unsafe_paths(paths: list[str]) -> list[str]:
    unsafe = []
    for path in paths:
        parts = Path(path).parts
        if Path(path).is_absolute() or ".." in parts:
            unsafe.append(path)
    return unsafe


def duplicate_paths(paths: list[str]) -> list[str]:
    seen = set()
    duplicates = []
    for path in paths:
        if path in seen and path not in duplicates:
            duplicates.append(path)
        seen.add(path)
    return duplicates


def source_file_statuses() -> list[FileStatus]:
    statuses = []
    for source_file, dest_file, purpose in preview_source_files():
        path = ROOT / source_file
        statuses.append(
            FileStatus(
                source_file=source_file,
                dest_file=dest_file,
                purpose=purpose,
                exists=path.exists(),
                ignored=git_check_ignored(source_file),
                tracked=git_is_tracked(source_file),
            )
        )
    return statuses


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def build_command_evidence() -> dict[str, bool]:
    build_text = (ROOT / BUILD_SCRIPT).read_text(encoding="utf-8") if (ROOT / BUILD_SCRIPT).exists() else ""
    config_text = (ROOT / GF_BUILDER_CONFIG).read_text(encoding="utf-8") if (ROOT / GF_BUILDER_CONFIG).exists() else ""
    return {
        "build_script_exists": (ROOT / BUILD_SCRIPT).exists(),
        "build_script_tracked": not git_check_ignored(str(BUILD_SCRIPT)),
        "uses_gftools_builder": "gftools builder sources/config.yaml" in build_text,
        "uses_metadata_fix": "scripts/fix_gf_metadata.py" in build_text,
        "config_exists": (ROOT / GF_BUILDER_CONFIG).exists(),
        "config_tracked": not git_check_ignored(str(GF_BUILDER_CONFIG)),
        "config_uses_sources_designspace": "VirtuaGrotesk.designspace" in config_text,
        "config_outputs_fonts_dir": "outputDir: ../fonts" in config_text,
    }


def markdown_report() -> str:
    preview = (ROOT / PREVIEW_PATH).read_text(encoding="utf-8")
    statuses = source_file_statuses()
    build_evidence = build_command_evidence()
    build_source_statuses = [
        (path, (ROOT / path).exists(), git_check_ignored(path), git_is_tracked(path))
        for path in BUILD_FROM_SOURCE_FILES
    ]
    missing = [status.source_file for status in statuses if not status.exists]
    ignored = [status.source_file for status in statuses if status.ignored]
    untracked = [status.source_file for status in statuses if status.exists and not status.tracked]
    dest_mismatches = [
        status
        for status in statuses
        if EXPECTED_DEST_FILES.get(status.source_file) != status.dest_file
    ]
    source_paths = [status.source_file for status in statuses]
    dest_paths = [status.dest_file for status in statuses]
    unsafe_source_paths = unsafe_paths(source_paths)
    duplicate_source_paths = duplicate_paths(source_paths)
    unsafe_dest_paths = unsafe_paths(dest_paths)
    duplicate_dest_paths = duplicate_paths(dest_paths)
    has_static_source_files = any(path.startswith("fonts/ttf/") for path in source_paths)
    static_outputs_present = [(path, (ROOT / path).exists(), git_check_ignored(path)) for path in STATIC_FONT_OUTPUTS]
    static_destinations = [path for path in dest_paths if path.startswith("static/")]
    article_sources = [path for path in source_paths if path.startswith("documentation/") and path != "documentation/google-fonts/ARTICLE.en_us.html"]
    article_destinations = [path for path in dest_paths if path.startswith("article/")]
    branch_values = text_values(preview, "branch")
    archive_values = text_values(preview, "archive_url")
    archive_url_ready = any(LATEST_RELEASE_ARCHIVE_URL_PATTERN.match(value) for value in archive_values)

    lines = [
        "# Package Source Files Audit",
        "",
        "This generated report checks the local files listed in the expected",
        "`METADATA.pb` `source.files` block before a Google Fonts Packager dry run.",
        "It does not prove the files are public on GitHub; it shows which files are",
        "present locally and which are ignored/generated, so the selected",
        "GitHub release/archive source strategy can be checked deliberately.",
        "",
        "## Summary",
        "",
        f"- Mapping source: `{PREVIEW_PATH}`",
        f"- Expected `source.files` entries: {len(statuses)}",
        f"- Missing local files: {len(missing)}",
        f"- Ignored local files: {len(ignored)}",
        f"- Tracked `source.files`: {sum(1 for status in statuses if status.tracked)} / {len(statuses)}",
        f"- Untracked local `source.files`: {len(untracked)}",
        f"- Destination mapping matches expected downstream layout: {yes_no(not dest_mismatches)}",
        f"- Unsafe `source.files` paths: {len(unsafe_source_paths)}",
        f"- Duplicate `source.files` paths: {len(duplicate_source_paths)}",
        f"- Unsafe `dest_file` paths: {len(unsafe_dest_paths)}",
        f"- Duplicate `dest_file` paths: {len(duplicate_dest_paths)}",
        f"- Variable-font-first source mapping: {yes_no('fonts/variable/VirtuaGrotesk[wght].ttf' in source_paths and not has_static_source_files)}",
        f"- Static TTFs generated locally for QA: {sum(1 for _, exists, _ in static_outputs_present if exists)} / {len(STATIC_FONT_OUTPUTS)}",
        f"- Static TTFs included in `source.files`: {sum(1 for path in source_paths if path.startswith('fonts/ttf/'))}",
        f"- Downstream `static/` destinations planned: {len(static_destinations)}",
        f"- Static package omission documented in preview: {yes_no('Include static TTFs only if Google Fonts asks' in preview)}",
        f"- Article assets map into `article/`: {yes_no('article/ARTICLE.en_us.html' in dest_paths and all(path in article_destinations for path in ['article/readme-specimen.png']))}",
        f"- Build-from-source inputs tracked: {sum(1 for _, _, _, tracked in build_source_statuses if tracked)} / {len(BUILD_FROM_SOURCE_FILES)}",
        f"- Build script uses `gftools builder sources/config.yaml`: {yes_no(build_evidence['uses_gftools_builder'])}",
        f"- Build script runs metadata post-processing: {yes_no(build_evidence['uses_metadata_fix'])}",
        f"- Builder config outputs to `fonts/`: {yes_no(build_evidence['config_outputs_fonts_dir'])}",
        f"- `branch` field present for default/source-build mode: {yes_no(bool(branch_values))}",
        f"- `archive_url` present for selected release/archive strategy: {yes_no(bool(archive_values))}",
        f"- `archive_url` is GitHub release download `.zip`: {yes_no(archive_url_ready)}",
        f"- Expected Packager branch name: `gftools_packager_ofl_virtuagrotesk`",
        "",
        "## Expected Packager Source Files",
        "",
        "| Source file | Destination file | Purpose | Exists locally | Ignored by git | Tracked by git |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for status in statuses:
        dest_ok = EXPECTED_DEST_FILES.get(status.source_file) == status.dest_file
        lines.append(
            f"| `{status.source_file}` | `{status.dest_file}` | {status.purpose} | "
            f"{yes_no(status.exists)} | {yes_no(status.ignored)} | {yes_no(status.tracked)} | {yes_no(dest_ok)} |"
        )
    lines[lines.index("| Source file | Destination file | Purpose | Exists locally | Ignored by git | Tracked by git |")] = (
        "| Source file | Destination file | Purpose | Exists locally | Ignored by git | Tracked by git | Destination OK |"
    )
    lines[lines.index("| --- | --- | --- | --- | --- | --- |")] = "| --- | --- | --- | --- | --- | --- | --- |"

    lines.extend(
        [
            "",
            "## Source Strategy Impact",
            "",
            "- Default Packager mode expects every `source_file` path above to be available from the public upstream branch recorded in `METADATA.pb`.",
            "- `fonts/variable/VirtuaGrotesk[wght].ttf` is generated build output; if it stays ignored, the final package needs a release/archive strategy or an explicit build-from-source flow.",
            "- `--latest-release` can work only after the public upstream release exposes the expected files through a GitHub release download `.zip` URL.",
            "- `--build-from-source` can work only if Google Fonts accepts the repo build path and the required source/build files are public and reproducible.",
            "- Packager creates a branch named like `gftools_packager_ofl_fontname`; for this family the expected branch is `gftools_packager_ofl_virtuagrotesk`.",
            "- Static TTFs are generated for local QA, proofs, and release review,",
            "  but are intentionally omitted from the preview package unless Google",
            "  Fonts review asks for a downstream `static/` directory.",
            "",
            "## Static Output Handling",
            "",
            "| Static font output | Exists locally | Ignored by git | Included in source.files |",
            "| --- | --- | --- | --- |",
        ]
    )
    for path, exists, ignored_status in static_outputs_present:
        lines.append(f"| `{path}` | {yes_no(exists)} | {yes_no(ignored_status)} | {yes_no(path in source_paths)} |")

    lines.extend(
        [
            "",
            "## Build-From-Source Inputs",
            "",
            "| Path | Exists locally | Ignored by git | Tracked by git |",
            "| --- | --- | --- | --- |",
        ]
    )
    for path, exists, ignored_status, tracked in build_source_statuses:
        lines.append(f"| `{path}` | {yes_no(exists)} | {yes_no(ignored_status)} | {yes_no(tracked)} |")

    lines.extend(
        [
            "",
            "## Build Command Evidence",
            "",
            "| Check | Status |",
            "| --- | --- |",
            f"| `build.sh` exists | {yes_no(build_evidence['build_script_exists'])} |",
            f"| `build.sh` is tracked by git | {yes_no(git_is_tracked(str(BUILD_SCRIPT)))} |",
            f"| `build.sh` is not ignored | {yes_no(build_evidence['build_script_tracked'])} |",
            f"| `build.sh` invokes `gftools builder sources/config.yaml` | {yes_no(build_evidence['uses_gftools_builder'])} |",
            f"| `build.sh` runs `scripts/fix_gf_metadata.py` after build | {yes_no(build_evidence['uses_metadata_fix'])} |",
            f"| `sources/config.yaml` exists | {yes_no(build_evidence['config_exists'])} |",
            f"| `sources/config.yaml` is tracked by git | {yes_no(git_is_tracked(str(GF_BUILDER_CONFIG)))} |",
            f"| `sources/config.yaml` is not ignored | {yes_no(build_evidence['config_tracked'])} |",
            f"| `sources/config.yaml` builds `VirtuaGrotesk.designspace` | {yes_no(build_evidence['config_uses_sources_designspace'])} |",
            f"| `sources/config.yaml` outputs to `../fonts` | {yes_no(build_evidence['config_outputs_fonts_dir'])} |",
        ]
    )

    lines.extend(
        [
            "",
            "## Before Final Dry Run",
            "",
            "- Keep the selected release/archive source strategy synchronized",
            "  with `documentation/google-fonts/google-fonts-downstream-package-preview.md`.",
            "- Confirm the final GitHub release/archive contains every",
            "  `source.files` entry above at the same path.",
            "- Confirm `source.archive_url` is the final GitHub release download",
            "  URL ending in `.zip`.",
            "- Confirm `documentation/google-fonts/google-fonts-downstream-package-preview.md` matches the final `source.files` mapping.",
            "- Confirm no `source_file` or `dest_file` path is absolute, parent-relative, or duplicated.",
            "- Regenerate this report with `make preflight` after changing the source strategy.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_package_source_files.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
