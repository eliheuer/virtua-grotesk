#!/usr/bin/env python3
"""Validate or install the Google Fonts designer profile draft."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from validate_designer_profile_bio import validation_errors as bio_errors
from validate_designer_profile_image import validation_errors as image_errors
from validate_designer_profile_info import validation_errors as info_errors


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path(os.environ["GF_REPO_PATH"]) if os.environ.get("GF_REPO_PATH") else Path("GF_REPO_PATH_NOT_CONFIGURED")
DEFAULT_INFO = Path("documentation/google-fonts/designer-profile-candidate/info.pb")
DEFAULT_BIO = Path("documentation/google-fonts/designer-profile-candidate/bio.html")
DEFAULT_IMAGE = Path("documentation/google-fonts/designer-profile-candidate/eliheuer.png")
DESIGNER = "Eli Heuer"
SLUG = "eliheuer"
AVATAR = "eliheuer.png"
PROFILE_DIR = Path("catalog/designers") / SLUG


class BioLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attr_map = {name.lower(): value or "" for name, value in attrs}
        href = attr_map.get("href", "").strip()
        if href:
            self.hrefs.append(href)


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def path_from_status(line: str) -> str:
    return line[3:] if len(line) > 3 else line


def info_link(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = re.search(r'^\s*link:\s*"([^"]*)"', path.read_text(encoding="utf-8"), flags=re.MULTILINE)
    return match.group(1) if match else None


def bio_links(path: Path) -> list[str]:
    if not path.is_file():
        return []
    parser = BioLinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.hrefs


def validation_errors(
    info: Path,
    bio: Path,
    image: Path,
    gf_repo: Path,
    replace: bool,
) -> list[str]:
    errors: list[str] = []
    errors.extend(info_errors(info, DESIGNER, AVATAR))
    errors.extend(bio_errors(bio))
    errors.extend(image_errors(image, AVATAR))
    link = info_link(info)
    if link:
        links = bio_links(bio)
        if link not in links:
            errors.append(
                "info.pb link should match one bio.html link; "
                f'info.pb has "{link}" but bio links are: {", ".join(links) or "none"}'
            )

    target_dir = gf_repo / PROFILE_DIR
    if not gf_repo.exists():
        errors.append(f"google/fonts checkout does not exist: {gf_repo}")
    elif not (gf_repo / ".git").exists():
        errors.append(f"google/fonts path is not a git checkout: {gf_repo}")
    else:
        branch = git_output(gf_repo, ["rev-parse", "--abbrev-ref", "HEAD"])
        if branch == "HEAD":
            errors.append("google/fonts checkout should not be in detached HEAD state")
        dirty_outside_profile = [
            line
            for line in git_output(gf_repo, ["status", "--porcelain"]).splitlines()
            if line and not path_from_status(line).startswith(str(PROFILE_DIR) + "/")
        ]
        if dirty_outside_profile:
            dirty_paths = ", ".join(path_from_status(line) for line in dirty_outside_profile[:5])
            if len(dirty_outside_profile) > 5:
                dirty_paths += f", and {len(dirty_outside_profile) - 5} more"
            errors.append(
                "google/fonts checkout has dirty paths outside the designer profile path: "
                f"{dirty_paths}"
            )
    if target_dir.exists() and not replace:
        errors.append(
            f"target designer profile already exists: {target_dir}; pass --replace after manual review"
        )
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--info", type=Path, default=DEFAULT_INFO)
    parser.add_argument("--bio", type=Path, default=DEFAULT_BIO)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--gf-repo", type=Path, default=DEFAULT_GF_REPO)
    parser.add_argument("--replace", action="store_true", help="allow replacing an existing profile directory")
    parser.add_argument("--apply", action="store_true", help="write profile files after validation")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    info = ROOT / args.info if not args.info.is_absolute() else args.info
    bio = ROOT / args.bio if not args.bio.is_absolute() else args.bio
    image = ROOT / args.image if not args.image.is_absolute() else args.image
    target_dir = args.gf_repo / PROFILE_DIR
    errors = validation_errors(info, bio, image, args.gf_repo, args.replace)

    print("# Designer Profile Preparation")
    print()
    print(f"Info: {info}")
    print(f"Bio: {bio}")
    print(f"Image: {image}")
    print(f"Target: {target_dir}")
    print(f"Ready to apply: {'no' if errors else 'yes'}")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2 if args.apply else 0

    if not args.apply:
        print()
        print("Dry run only. Re-run with --apply to write the profile files.")
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(info, target_dir / "info.pb")
    shutil.copy2(bio, target_dir / "bio.html")
    shutil.copy2(image, target_dir / AVATAR)
    print()
    print("Wrote designer profile files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
