#!/usr/bin/env python3
"""Check GitHub API credentials needed by gftools packager."""

from __future__ import annotations

import os
import re
import shutil
import subprocess


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if os.environ.get("GH_TOKEN"):
        print("GitHub API credentials ready: yes")
        print("Credential source: GH_TOKEN")
        return 0

    if not shutil.which("gh"):
        print("GitHub API credentials ready: no")
        print("Credential source: unavailable")
        print("GitHub CLI is not installed or not on PATH.")
        print("Install/authenticate gh, or export GH_TOKEN before packaging.")
        print("Check after fixing with: make github-auth-check")
        return 2

    token_returncode, token_output = run(["gh", "auth", "token"])
    if token_returncode == 0 and token_output:
        print("GitHub API credentials ready: yes")
        print("Credential source: gh auth token")
        return 0

    status_returncode, status_output = run(["gh", "auth", "status", "-h", "github.com"])
    detail = squash(status_output) or f"gh auth status exit {status_returncode}"
    print("GitHub API credentials ready: no")
    print("Credential source: unavailable")
    print(f"GitHub CLI detail: {detail}")
    print("Inspect current auth with: gh auth status -h github.com")
    print("Refresh auth with: gh auth login -h github.com")
    print("Or export a short-lived GH_TOKEN for the package dry run.")
    print("Check after fixing with: make github-auth-check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
