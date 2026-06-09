#!/usr/bin/env python3
"""Dry-run or apply the maintainer-approved public upstream URL."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"
PLACEHOLDER_DISPLAY_URL = "github.com/fontgarden/virtua-grotesk"
PENDING_URL = "Pending decision: public upstream URL"
TARGET_FILES = [
    "OFL.txt",
    "sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist",
    "sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist",
    "scripts/fix_gf_metadata.py",
    "documentation/google-fonts/ARTICLE.en_us.html",
    "documentation/google-fonts/google-fonts-decision-questions.md",
    "documentation/google-fonts/google-fonts-decisions.md",
    "documentation/google-fonts/google-fonts-downstream-package-preview.md",
    "documentation/google-fonts/google-fonts-metadata-review.md",
    "documentation/google-fonts/google-fonts-package-checklist.md",
    "documentation/google-fonts/google-fonts-submission-handoff.md",
]


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def normalize_github_url(remote: str) -> str:
    remote = remote.strip()
    ssh_match = re.match(r"git@github\.com:([^/]+/[^.]+)(?:\.git)?$", remote)
    if ssh_match:
        return f"https://github.com/{ssh_match.group(1)}"
    https_match = re.match(r"https://github\.com/([^/]+/[^.]+)(?:\.git)?$", remote)
    if https_match:
        return f"https://github.com/{https_match.group(1)}"
    return remote


def origin_candidate() -> str:
    return normalize_github_url(git_output("remote", "get-url", "origin"))


def validate_url(url: str) -> list[str]:
    errors: list[str] = []
    if url == PLACEHOLDER_URL:
        errors.append("refusing to apply the placeholder upstream URL")
    if not re.fullmatch(r"https://github\.com/[^/\s]+/[^/\s]+", url):
        errors.append("URL must be an https://github.com/owner/repo URL without .git")
    return errors


def replacement_text(text: str, url: str) -> str:
    display_url = url.replace("https://", "")
    return (
        text.replace(PLACEHOLDER_URL, url)
        .replace(PLACEHOLDER_DISPLAY_URL, display_url)
        .replace(PENDING_URL, url)
    )


def changed_files(url: str) -> list[tuple[Path, int]]:
    changed: list[tuple[Path, int]] = []
    for relative in TARGET_FILES:
        path = ROOT / relative
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        after = replacement_text(before, url)
        if before != after:
            changed.append((path, sum(1 for old, new in zip(before.splitlines(), after.splitlines()) if old != new)))
    return changed


def apply_changes(url: str) -> None:
    for relative in TARGET_FILES:
        path = ROOT / relative
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        after = replacement_text(before, url)
        if before != after:
            path.write_text(after, encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=origin_candidate(), help="approved public upstream URL")
    parser.add_argument("--apply", action="store_true", help="write replacements after validation")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    url = args.url.rstrip("/")
    errors = validate_url(url)
    changes = changed_files(url)

    print("# Public Upstream URL Apply Helper")
    print()
    print(f"Candidate URL: {url}")
    print(f"Origin-derived candidate: {origin_candidate()}")
    print(f"Mode: {'apply' if args.apply else 'dry-run'}")
    print(f"Files with replacements: {len(changes)}")
    if changes:
        print()
        print("Replacement files:")
        for path, changed_line_count in changes:
            print(f"- {path.relative_to(ROOT)} ({changed_line_count} changed lines)")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2
    if not changes:
        print()
        print("No public upstream placeholder replacements remain.")
        return 0
    if not args.apply:
        print()
        print("Dry run only. Re-run with --apply after the maintainer approves this URL.")
        return 0

    apply_changes(url)
    print()
    print("Applied public upstream URL replacements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
