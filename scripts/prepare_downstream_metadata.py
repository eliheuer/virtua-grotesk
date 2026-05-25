#!/usr/bin/env python3
"""Validate or install the final downstream METADATA.pb from the preview."""

from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
DEFAULT_PREVIEW = Path("documentation/google-fonts-downstream-package-preview.md")
PACKAGE_DIR = Path("ofl/virtuagrotesk")
SUPPORTED_SOURCE_MODES = ("default", "latest-release", "build-from-source")
BLOCKED_MARKERS = (
    "Pending decision",
    "Pending:",
    "Pending final",
    "https://github.com/fontgarden/virtua-grotesk",
    'designer: "UNKNOWN"',
    'repository_url: "https://github.com/user/repo"',
    "fonts/variable/MyFont[wght].ttf",
    'primary_script: "Deva"',
)
REQUIRED_LINES = (
    'name: "Virtua Grotesk"',
    'license: "OFL"',
    'category: "SANS_SERIF"',
    'filename: "VirtuaGrotesk[wght].ttf"',
    'post_script_name: "VirtuaGrotesk-Regular"',
    'full_name: "Virtua Grotesk Regular"',
    'subsets: "arabic"',
    'subsets: "latin"',
    'subsets: "latin-ext"',
    'subsets: "menu"',
    'tag: "wght"',
    'min_value: 400.0',
    'max_value: 700.0',
    'source_file: "OFL.txt"',
    'dest_file: "OFL.txt"',
    'source_file: "fonts/variable/VirtuaGrotesk[wght].ttf"',
    'dest_file: "VirtuaGrotesk[wght].ttf"',
    'source_file: "documentation/ARTICLE.en_us.html"',
    'dest_file: "article/ARTICLE.en_us.html"',
    'source_file: "documentation/readme-specimen.png"',
    'dest_file: "article/readme-specimen.png"',
    'primary_script: "Arab"',
    'stroke: "SANS_SERIF"',
)
CONFIG_YAML_LINE = 'config_yaml: "sources/config.yaml"'
ARCHIVE_URL_PATTERN = re.compile(r'^\s*archive_url:\s+"https://github\.com/[^"]+"\s*$', re.MULTILINE)
ARCHIVE_URL_VALUE_PATTERN = re.compile(r'^\s*archive_url:\s+"([^"]+)"\s*$', re.MULTILINE)
DATE_ADDED_PATTERN = re.compile(r'^\s*date_added:\s+"(20\d{2}-\d{2}-\d{2})"\s*$', re.MULTILINE)
SOURCE_COMMIT_PATTERN = re.compile(r'^\s*commit:\s+"([0-9a-f]{40})"\s*$', re.MULTILINE)
PROHIBITED_OPTIONAL_FIELDS = (
    "languages",
    "display_name",
    "minisite_url",
    "classifications",
    "sample_text",
    "tags",
)


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def git_success(repo: Path, args: list[str]) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.returncode == 0


def extract_metadata(preview_text: str) -> str:
    marker = "## Expected METADATA.pb shape"
    start = preview_text.find(marker)
    if start == -1:
        raise ValueError("preview is missing '## Expected METADATA.pb shape'")
    fence_start = preview_text.find("```text", start)
    if fence_start == -1:
        raise ValueError("preview metadata block is missing opening ```text fence")
    content_start = preview_text.find("\n", fence_start)
    fence_end = preview_text.find("```", content_start + 1)
    if content_start == -1 or fence_end == -1:
        raise ValueError("preview metadata block is missing closing fence")
    return preview_text[content_start + 1 : fence_end].strip() + "\n"


def brace_balance(text: str) -> bool:
    balance = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.endswith("{"):
            balance += 1
        elif stripped == "}":
            balance -= 1
        if balance < 0:
            return False
    return balance == 0


def valid_date_added(text: str) -> bool:
    match = DATE_ADDED_PATTERN.search(text)
    if not match:
        return False
    try:
        datetime.strptime(match.group(1), "%Y-%m-%d")
    except ValueError:
        return False
    return True


def archive_url_value(text: str) -> str | None:
    match = ARCHIVE_URL_VALUE_PATTERN.search(text)
    return match.group(1) if match else None


def valid_latest_release_archive_url(text: str) -> bool:
    url = archive_url_value(text)
    if not url:
        return False
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    return (
        parsed.scheme == "https"
        and parsed.netloc.lower() == "github.com"
        and len(path_parts) >= 5
        and path_parts[2] == "releases"
        and path_parts[3] == "download"
        and path_parts[-1].endswith(".zip")
    )


def source_mode_from_environment() -> str:
    return os.environ.get("GFT_PACKAGER_SOURCE_MODE", "default") or "default"


def validation_errors(metadata: str, gf_repo: Path, source_mode: str) -> list[str]:
    errors: list[str] = []
    if source_mode not in SUPPORTED_SOURCE_MODES:
        errors.append(
            "unsupported source mode: "
            f"{source_mode}; expected one of {', '.join(SUPPORTED_SOURCE_MODES)}"
        )
    for marker in BLOCKED_MARKERS:
        if marker in metadata:
            errors.append(f"blocked marker still present: {marker}")
    for required in REQUIRED_LINES:
        if required not in metadata:
            errors.append(f"required metadata line missing: {required}")
    if not valid_date_added(metadata):
        errors.append(
            'required metadata line missing: date_added with final valid "YYYY-MM-DD" Google Fonts date'
        )
    if not SOURCE_COMMIT_PATTERN.search(metadata):
        errors.append(
            "required metadata line missing: source.commit with final 40-character lowercase git hash"
        )
    for field in PROHIBITED_OPTIONAL_FIELDS:
        if re.search(rf"^\s*{re.escape(field)}\s*:", metadata, flags=re.MULTILINE):
            errors.append(
                f"optional metadata field requires explicit Google Fonts review before apply: {field}"
            )
    has_config_yaml = CONFIG_YAML_LINE in metadata
    if source_mode == "build-from-source" and not has_config_yaml:
        errors.append(f"required metadata line missing for build-from-source mode: {CONFIG_YAML_LINE}")
    if source_mode in {"default", "latest-release"} and has_config_yaml:
        errors.append(
            "source.config_yaml is present but should be omitted for "
            f"{source_mode} source mode unless Google Fonts review asks for build metadata"
        )
    if source_mode == "latest-release" and not ARCHIVE_URL_PATTERN.search(metadata):
        errors.append(
            "source.archive_url is required for latest-release source mode; "
            "record the final GitHub release download URL ending in .zip before applying metadata"
        )
    elif source_mode == "latest-release" and not valid_latest_release_archive_url(metadata):
        errors.append(
            "source.archive_url for latest-release mode must be a GitHub "
            "release download URL ending in .zip"
        )
    if not brace_balance(metadata):
        errors.append("metadata braces are unbalanced")
    if not gf_repo.exists():
        errors.append(f"google/fonts checkout does not exist: {gf_repo}")
    elif not (gf_repo / ".git").exists():
        errors.append(f"google/fonts path is not a git checkout: {gf_repo}")
    else:
        branch = git_output(gf_repo, ["rev-parse", "--abbrev-ref", "HEAD"])
        if branch != "main":
            errors.append(f"google/fonts checkout must be on main, got: {branch or 'unknown'}")
        upstream = git_output(gf_repo, ["remote", "get-url", "upstream"])
        origin = git_output(gf_repo, ["remote", "get-url", "origin"])
        if "github.com/google/fonts" not in upstream and "github.com/google/fonts" not in origin:
            errors.append("google/fonts checkout needs origin or upstream pointing at google/fonts")
        if not git_success(gf_repo, ["rev-parse", "--verify", "--quiet", "upstream/main"]):
            errors.append("google/fonts checkout is missing upstream/main")
        else:
            upstream_counts = git_output(gf_repo, ["rev-list", "--left-right", "--count", "main...upstream/main"])
            if upstream_counts != "0\t0":
                errors.append(f"google/fonts main is not aligned with upstream/main: {upstream_counts or 'unknown'}")
        if git_success(gf_repo, ["rev-parse", "--verify", "--quiet", "origin/main"]):
            origin_counts = git_output(gf_repo, ["rev-list", "--left-right", "--count", "main...origin/main"])
            if origin_counts != "0\t0":
                errors.append(f"google/fonts main is not aligned with origin/main: {origin_counts or 'unknown'}")
        dirty_outside = [
            line
            for line in git_output(gf_repo, ["status", "--porcelain"]).splitlines()
            if line and not line[3:].startswith(str(PACKAGE_DIR) + "/")
        ]
        if dirty_outside:
            errors.append("google/fonts checkout has dirty paths outside ofl/virtuagrotesk")
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, default=DEFAULT_PREVIEW)
    parser.add_argument("--gf-repo", type=Path, default=DEFAULT_GF_REPO)
    parser.add_argument(
        "--source-mode",
        choices=SUPPORTED_SOURCE_MODES,
        default=source_mode_from_environment(),
        help="final Packager source mode; defaults to GFT_PACKAGER_SOURCE_MODE or default",
    )
    parser.add_argument("--apply", action="store_true", help="write METADATA.pb after validation")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    preview_path = ROOT / args.preview
    gf_repo = args.gf_repo
    target = gf_repo / PACKAGE_DIR / "METADATA.pb"

    try:
        metadata = extract_metadata(preview_path.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"Could not read preview: {error}")
        return 2
    except ValueError as error:
        print(f"Could not extract metadata preview: {error}")
        return 2

    errors = validation_errors(metadata, gf_repo, args.source_mode)
    print("# Downstream METADATA.pb Preparation")
    print()
    print(f"Preview: {preview_path}")
    print(f"Target: {target}")
    print(f"Source mode: {args.source_mode}")
    print(f"Ready to apply: {'no' if errors else 'yes'}")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2 if args.apply else 0

    if not args.apply:
        print()
        print("Dry run only. Re-run with --apply to write the target METADATA.pb.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(metadata, encoding="utf-8")
    print()
    print("Wrote downstream METADATA.pb.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
