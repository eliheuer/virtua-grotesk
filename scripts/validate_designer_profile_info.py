#!/usr/bin/env python3
"""Validate a candidate Google Fonts designer profile info.pb file."""

from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import urlparse


INFO_RE = re.compile(
    r'^\s*designer:\s*"(?P<designer>[^"]*)"\s*\n'
    r'\s*link:\s*"(?P<link>[^"]*)"\s*\n'
    r"\s*avatar\s*\{\s*\n"
    r'\s*file_name:\s*"(?P<file_name>[^"]*)"\s*\n'
    r"\s*\}\s*$",
    flags=re.MULTILINE,
)
PLACEHOLDER_MARKERS = ("example.com", "REPLACE-WITH", "TODO", "TBD", "user/repo")


def validation_errors(path: Path, expected_designer: str, expected_avatar: str) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"info.pb file does not exist: {path}"]
    if not path.is_file():
        return [f"info.pb path is not a file: {path}"]
    if path.name != "info.pb":
        errors.append("designer profile info file should be named info.pb")

    text = path.read_text(encoding="utf-8").strip()
    match = INFO_RE.fullmatch(text)
    if not match:
        return [
            *errors,
            "info.pb should contain designer, link, and avatar.file_name fields in the Google Fonts profile shape",
        ]

    designer = match.group("designer")
    link = match.group("link")
    file_name = match.group("file_name")
    if designer != expected_designer:
        errors.append(f'designer should be "{expected_designer}", got "{designer}"')
    if file_name != expected_avatar:
        errors.append(f'avatar.file_name should be "{expected_avatar}", got "{file_name}"')
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", file_name):
        errors.append("avatar.file_name should be ASCII and pathless")
    if "/" in file_name or "\\" in file_name:
        errors.append("avatar.file_name should not include a directory path")
    if link:
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append("link should be empty or a full http(s) URL")
        if any(marker.lower() in link.lower() for marker in PLACEHOLDER_MARKERS):
            errors.append("link should be empty or an approved real profile URL, not a placeholder")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: validate_designer_profile_info.py path/to/info.pb 'Designer Name' avatar.png")
        return 2
    path = Path(argv[1])
    expected_designer = argv[2]
    expected_avatar = argv[3]
    errors = validation_errors(path, expected_designer, expected_avatar)
    print("# Designer Profile info.pb Check")
    print()
    print(f"Info: {path}")
    print(f"Expected designer: {expected_designer}")
    print(f"Expected avatar: {expected_avatar}")
    print(f"Ready: {'no' if errors else 'yes'}")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2

    text = path.read_text(encoding="utf-8").strip()
    match = INFO_RE.fullmatch(text)
    assert match is not None
    link = match.group("link")
    print(f"Designer: {match.group('designer')}")
    print(f"Link present: {'yes' if link else 'no'}")
    print(f"Avatar file: {match.group('file_name')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
