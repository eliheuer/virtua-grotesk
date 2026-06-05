#!/usr/bin/env python3
"""Generate a release-archive manifest for Google Fonts Packager inputs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import os
from urllib.parse import urlparse
import re
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/release-archive-manifest.md")
PREVIEW_PATH = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")
LOCAL_ARCHIVE_PATH = Path("dist/VirtuaGrotesk-1.000.zip")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o644 << 16
SOURCE_PURPOSES = {
    "OFL.txt": "license",
    "fonts/variable/VirtuaGrotesk[wght].ttf": "served variable font",
    "documentation/google-fonts/ARTICLE.en_us.html": "article HTML",
    "documentation/assets/readme-specimen.png": "article image",
}
BUILD_INPUT_ROOTS = [
    Path("sources/VirtuaGrotesk.designspace"),
    Path("sources/VirtuaGrotesk-Regular.ufo"),
    Path("sources/VirtuaGrotesk-Bold.ufo"),
    Path("sources/config.yaml"),
    Path("build.sh"),
    Path("scripts/fix_gf_metadata.py"),
]
LATEST_RELEASE_ARCHIVE_URL_PATTERN = re.compile(
    r'^https://github\.com/[^/]+/[^/]+/releases/download/[^/]+/[^"]+\.zip$'
)


@dataclass(frozen=True)
class ArchiveInput:
    source_file: str
    dest_file: str
    purpose: str
    exists: bool
    ignored: bool
    tracked: bool
    dirty: bool
    size_bytes: int | None
    sha256: str | None
    mtime: float | None


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )


def git_ok(args: list[str]) -> bool:
    return run_git(args).returncode == 0


def git_check_ignored(path: str) -> bool:
    return run_git(["check-ignore", "-q", path]).returncode == 0


def git_is_tracked(path: str) -> bool:
    return bool(run_git(["ls-files", "--", path]).stdout.strip())


def git_is_dirty(path: str) -> bool:
    return bool(run_git(["status", "--porcelain", "--", path]).stdout.strip())


def source_files_from_preview() -> list[tuple[str, str]]:
    text = (ROOT / PREVIEW_PATH).read_text(encoding="utf-8")
    return re.findall(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        text,
        flags=re.DOTALL,
    )


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


def preview_archive_url() -> str | None:
    text = (ROOT / PREVIEW_PATH).read_text(encoding="utf-8")
    match = re.search(r'archive_url:\s*"([^"]+)"', text)
    return match.group(1) if match else None


def release_tag() -> str:
    release_metadata = (ROOT / "documentation/google-fonts/release-metadata.md").read_text(encoding="utf-8")
    match = re.search(r"Suggested first-submission tag: `([^`]+)`", release_metadata)
    return match.group(1) if match else "v1.000"


def filename_from_url(url: str | None) -> str | None:
    if not url:
        return None
    path = urlparse(url).path
    return Path(path).name if path else None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def archive_inputs() -> list[ArchiveInput]:
    rows = []
    for source_file, dest_file in source_files_from_preview():
        path = ROOT / source_file
        exists = path.exists()
        rows.append(
            ArchiveInput(
                source_file=source_file,
                dest_file=dest_file,
                purpose=SOURCE_PURPOSES.get(source_file, "package source"),
                exists=exists,
                ignored=git_check_ignored(source_file),
                tracked=git_is_tracked(source_file),
                dirty=git_is_dirty(source_file),
                size_bytes=path.stat().st_size if exists and path.is_file() else None,
                sha256=file_sha256(path) if exists and path.is_file() else None,
                mtime=path.stat().st_mtime if exists else None,
            )
        )
    return rows


def local_archive_entries() -> dict[str, tuple[int, str, tuple[int, int, int, int, int, int], int]]:
    archive_path = ROOT / LOCAL_ARCHIVE_PATH
    if not archive_path.exists():
        return {}
    entries: dict[str, tuple[int, str, tuple[int, int, int, int, int, int], int]] = {}
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            digest = hashlib.sha256(archive.read(info.filename)).hexdigest()
            entries[info.filename] = (info.file_size, digest, info.date_time, info.external_attr)
    return entries


def iter_existing_files(path: Path) -> list[Path]:
    absolute = ROOT / path
    if not absolute.exists():
        return []
    if absolute.is_file():
        return [absolute]
    files = []
    for root, dirnames, filenames in os.walk(absolute):
        dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
        for filename in filenames:
            files.append(Path(root) / filename)
    return files


def newest_build_input_mtime() -> tuple[float | None, str | None]:
    newest_time: float | None = None
    newest_path: str | None = None
    for relative in BUILD_INPUT_ROOTS:
        for path in iter_existing_files(relative):
            mtime = path.stat().st_mtime
            if newest_time is None or mtime > newest_time:
                newest_time = mtime
                newest_path = str(path.relative_to(ROOT))
    return newest_time, newest_path


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def fmt_size(size: int | None) -> str:
    if size is None:
        return "n/a"
    return str(size)


def fmt_hash(value: str | None) -> str:
    if value is None:
        return "n/a"
    return value


def markdown_report() -> str:
    rows = archive_inputs()
    local_entries = local_archive_entries()
    archive_url = preview_archive_url()
    tag = release_tag()
    tag_exists = git_ok(["rev-parse", "-q", "--verify", f"refs/tags/{tag}"])
    archive_url_filename = filename_from_url(archive_url)
    local_archive_filename = LOCAL_ARCHIVE_PATH.name
    archive_url_filename_matches = archive_url_filename == local_archive_filename
    archive_url_ready = bool(archive_url and LATEST_RELEASE_ARCHIVE_URL_PATTERN.match(archive_url))
    newest_input_time, newest_input_path = newest_build_input_mtime()
    variable_font = next((row for row in rows if row.source_file.startswith("fonts/variable/")), None)
    variable_font_current = (
        bool(variable_font and variable_font.mtime is not None and newest_input_time is not None)
        and variable_font.mtime >= newest_input_time
    )
    missing = [row.source_file for row in rows if not row.exists]
    dirty = [row.source_file for row in rows if row.dirty]
    ignored = [row.source_file for row in rows if row.ignored]
    untracked = [row.source_file for row in rows if row.exists and not row.tracked]
    source_paths = [row.source_file for row in rows]
    dest_paths = [row.dest_file for row in rows]
    unsafe_source_paths = unsafe_paths(source_paths)
    duplicate_source_paths = duplicate_paths(source_paths)
    unsafe_dest_paths = unsafe_paths(dest_paths)
    duplicate_dest_paths = duplicate_paths(dest_paths)
    expected_entry_names = {row.source_file for row in rows}
    local_entry_names = set(local_entries)
    unsafe_archive_entries = unsafe_paths(list(local_entry_names))
    archive_contains_all = bool(rows) and expected_entry_names.issubset(local_entry_names)
    archive_has_extra = bool(local_entry_names - expected_entry_names)
    archive_hashes_match = archive_contains_all and all(
        row.sha256 is not None and local_entries[row.source_file][1] == row.sha256
        for row in rows
    )
    archive_metadata_stable = bool(local_entries) and all(
        date_time == ZIP_TIMESTAMP and external_attr == ZIP_FILE_MODE
        for _, _, date_time, external_attr in local_entries.values()
    )
    archive_digest = file_sha256(ROOT / LOCAL_ARCHIVE_PATH) if (ROOT / LOCAL_ARCHIVE_PATH).is_file() else None

    lines = [
        "# Release Archive Manifest",
        "",
        "This generated report is the local manifest for the GitHub release/archive",
        "planned for Google Fonts Packager `--latest-release` mode. It checks the",
        "`source.files` paths from the downstream metadata preview and records the",
        "local file state, sizes, and SHA-256 hashes that should match the final",
        "release archive contents.",
        "",
        "## Summary",
        "",
        f"- Mapping source: `{PREVIEW_PATH}`",
        "- Selected source mode: `latest-release`",
        f"- Archive inputs expected: {len(rows)}",
        f"- Archive inputs present locally: {sum(1 for row in rows if row.exists)} / {len(rows)}",
        f"- Missing archive inputs: {len(missing)}",
        f"- Unsafe `source.files` paths: {len(unsafe_source_paths)}",
        f"- Duplicate `source.files` paths: {len(duplicate_source_paths)}",
        f"- Unsafe `dest_file` paths: {len(unsafe_dest_paths)}",
        f"- Duplicate `dest_file` paths: {len(duplicate_dest_paths)}",
        f"- Ignored archive inputs: {len(ignored)}",
        f"- Untracked archive inputs: {len(untracked)}",
        f"- Dirty archive inputs: {len(dirty)}",
        f"- Variable font newer than source/build inputs: {yes_no(variable_font_current)}",
        f"- Newest source/build input: `{newest_input_path or 'unknown'}`",
        f"- Local release archive: `{LOCAL_ARCHIVE_PATH}`",
        f"- Preview release archive URL: `{archive_url or 'missing'}`",
        f"- Preview release archive URL is GitHub release download `.zip`: {yes_no(archive_url_ready)}",
        f"- Preview archive filename matches local archive: {yes_no(archive_url_filename_matches)}",
        f"- Local release archive exists: {yes_no((ROOT / LOCAL_ARCHIVE_PATH).exists())}",
        f"- Local release archive contains expected files: {yes_no(archive_contains_all)}",
        f"- Local release archive has extra files: {yes_no(archive_has_extra)}",
        f"- Local release archive has unsafe paths: {yes_no(bool(unsafe_archive_entries))}",
        f"- Local release archive hashes match source files: {yes_no(archive_hashes_match)}",
        f"- Local release archive metadata deterministic: {yes_no(archive_metadata_stable)}",
        f"- Local release archive SHA-256: `{archive_digest or 'missing'}`",
        f"- Suggested final release tag: `{tag}`",
        f"- Final GitHub release tag exists locally: {yes_no(tag_exists)}",
        "- Final GitHub release archive URL recorded: pending",
        "",
        "## Archive Inputs",
        "",
        "| Source file | Destination in package | Purpose | Exists | Ignored | Tracked | Dirty | Size bytes | SHA-256 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| `{row.source_file}` | `{row.dest_file}` | {row.purpose} | "
            f"{yes_no(row.exists)} | {yes_no(row.ignored)} | {yes_no(row.tracked)} | "
            f"{yes_no(row.dirty)} | {fmt_size(row.size_bytes)} | `{fmt_hash(row.sha256)}` |"
        )

    lines.extend(
        [
            "",
            "## Local Release Archive",
            "",
            f"Run `make release-archive-build` to create `{LOCAL_ARCHIVE_PATH}` from the current `source.files` mapping.",
            "",
            "| Archive entry | Present | Size matches source | SHA-256 matches source | Deterministic metadata |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        entry = local_entries.get(row.source_file)
        size_matches = bool(entry and row.size_bytes is not None and entry[0] == row.size_bytes)
        hash_matches = bool(entry and row.sha256 is not None and entry[1] == row.sha256)
        deterministic_metadata = bool(entry and entry[2] == ZIP_TIMESTAMP and entry[3] == ZIP_FILE_MODE)
        lines.append(
            f"| `{row.source_file}` | {yes_no(entry is not None)} | "
            f"{yes_no(size_matches)} | {yes_no(hash_matches)} | {yes_no(deterministic_metadata)} |"
        )
    for extra in sorted(local_entry_names - expected_entry_names):
        lines.append(f"| `{extra}` | yes | extra | extra | extra |")

    lines.extend(
        [
            "",
            "## Final Release Gate",
            "",
            "Before creating the GitHub release used by Google Fonts Packager:",
            "",
            "1. Finish drawing/source work and rebuild the fonts.",
            "2. Build the local review archive with `make release-archive-build`.",
            "3. Regenerate this report with `make release-archive-check`.",
            "4. Confirm every archive input above is present in the release archive at the same path.",
            "5. Confirm the variable font hash here matches the released file.",
            "6. Confirm the local release archive metadata is deterministic.",
            "7. Confirm the GitHub release asset filename matches the preview `source.archive_url` and the URL is a release download ending in `.zip`.",
            "8. Replace the pending downstream `source.commit` value and keep `source.archive_url` synchronized.",
            "9. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check` and a no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.",
            "",
            "Notes:",
            "",
            "- The generated variable font may stay ignored in the public branch for this selected strategy.",
            "- Article files can be committed or injected into the release archive, but Packager must be able to fetch them from the GitHub release download `.zip` URL.",
            "- This report does not create a release or tag; it is a reproducibility checklist for the release/archive path.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_release_archive_manifest.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
