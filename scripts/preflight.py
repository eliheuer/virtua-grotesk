#!/usr/bin/env python3
"""Small local preflight for the active workflow."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "fonts/variable/VirtuaGrotesk[wght].ttf",
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
    "documentation/proofs/proof.pdf",
    "documentation/proofs/print-spacing-specimen.pdf",
    "documentation/source/source-ufo-metadata.md",
    "documentation/source/master-compatibility.md",
    "documentation/source/generated-font-metadata.md",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    for path in missing:
        print(f"missing: {path}")

    if missing:
        return 1
    print("preflight artifacts present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
