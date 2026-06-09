#!/usr/bin/env python3
"""Regenerate the small active project report bundle."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
VARIABLE_FONT = "fonts/variable/VirtuaGrotesk[wght].ttf"
STATIC_FONTS = [
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]


def py(*args: str) -> list[str]:
    return [sys.executable, *args]


def report_commands() -> list[list[str]]:
    return [
        py("scripts/report_source_metadata.py", "sources/VirtuaGrotesk-Regular.ufo", "sources/VirtuaGrotesk-Bold.ufo", "documentation/source/source-ufo-metadata.md"),
        py("scripts/report_master_compatibility.py", "sources/VirtuaGrotesk-Regular.ufo", "sources/VirtuaGrotesk-Bold.ufo", "documentation/source/master-compatibility.md"),
        py("scripts/report_generated_font_metadata.py", VARIABLE_FONT, *STATIC_FONTS, "documentation/source/generated-font-metadata.md"),
    ]


def main() -> int:
    for args in report_commands():
        print("+ " + " ".join(args), flush=True)
        result = subprocess.run(args, cwd=ROOT, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
