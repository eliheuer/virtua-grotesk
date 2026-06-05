#!/usr/bin/env python3
"""Small local preflight for the simplified workflow."""

from __future__ import annotations

from pathlib import Path
import re
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
    "documentation/google-fonts/fontspector-googlefonts-report.md",
    "documentation/google-fonts/final-submission-blockers.md",
    "documentation/google-fonts/next-actions.md",
]


def markdown_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def fontspector_summary(text: str) -> str:
    table = re.search(
        r"\| 🔥 FAIL \| ⚠️ WARN \| ℹ️ INFO \| ✅ PASS \| ⏩ SKIP \|\n"
        r"\| ---\|---\|---\|---\|---\|\n"
        r"\| (?P<fail>\d+) \| (?P<warn>\d+) \| (?P<info>\d+) \| (?P<pass>\d+) \| (?P<skip>\d+) \|",
        text,
    )
    if table:
        return (
            f"FAIL {table.group('fail')}, WARN {table.group('warn')}, "
            f"INFO {table.group('info')}, PASS {table.group('pass')}, SKIP {table.group('skip')}"
        )
    return markdown_value(r"Summary:\n\s+(.+)", text)


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    for path in missing:
        print(f"missing: {path}")

    fontspector = ROOT / "documentation/google-fonts/fontspector-googlefonts-report.md"
    if fontspector.exists():
        text = fontspector.read_text(encoding="utf-8", errors="replace")
        print(f"fontspector: {fontspector_summary(text)}")

    blockers = ROOT / "documentation/google-fonts/final-submission-blockers.md"
    if blockers.exists():
        text = blockers.read_text(encoding="utf-8", errors="replace")
        first_blocker = markdown_value(r"^- First blocker: (.+)$", text, "see blocker report")
        print(f"first blocker: {first_blocker}")

    if missing:
        return 1
    print("preflight artifacts present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
