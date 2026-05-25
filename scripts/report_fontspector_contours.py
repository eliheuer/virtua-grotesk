#!/usr/bin/env python3
"""Report Fontspector contour-count findings for built fonts."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]


def fontspector_json(command: list[str], report_path: Path) -> dict:
    if shutil.which("fontspector") is None:
        raise RuntimeError("Missing fontspector. Install https://github.com/fonttools/fontspector and rerun.")

    (Path.home() / ".fontspector").mkdir(exist_ok=True)
    result = subprocess.run(
        command,
        check=False,
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Fontspector failed with exit code {result.returncode}.")

    try:
        return json.loads(report_path.read_text())
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Fontspector wrote invalid JSON: {exc}") from exc


def contour_results(font_paths: list[Path]) -> dict[str, list[dict]]:
    with tempfile.NamedTemporaryFile(suffix=".json") as report:
        command = [
            "fontspector",
            "-p",
            "googlefonts",
            *[str(path) for path in font_paths],
            "--checkid",
            "contour_count",
            "--json",
            report.name,
            "--loglevel",
            "error",
            "--skip-network",
        ]
        data = fontspector_json(command, Path(report.name))

    results = {}
    for family_results in data["results"].values():
        for checks in family_results.values():
            for check in checks:
                if check["check_id"] == "contour_count":
                    results[check["filename"]] = check.get("subresults", [])
    return results


def glyph_problem_rows(subresult: dict) -> list[str]:
    rows = []
    for item in subresult.get("metadata", []):
        problem = item["GlyphProblem"]
        codepoint = problem["actual"].get("codepoint")
        codepoint_label = f"U+{codepoint:04X}" if codepoint is not None else "unencoded"
        actual = problem["actual"]["contour_count"]
        expected = problem["expected"]
        if "allowed_counts" in expected:
            expected_label = ", ".join(str(value) for value in expected["allowed_counts"])
        else:
            expected_label = f"at least {expected['min_contours']}"
        rows.append(
            f"| `{problem['glyph_name']}` | {codepoint_label} | {actual} | {expected_label} |"
        )
    return rows


def markdown_report(font_paths: list[Path]) -> str:
    results = contour_results(font_paths)
    lines = [
        "# Fontspector Contour Count Findings",
        "",
        "Fonts:",
        "",
        *[f"- `{path}`" for path in font_paths],
        "",
        "These are source/drawing issues reported by Fontspector's `contour_count` check.",
        "",
    ]

    for font_path, subresults in results.items():
        lines.extend([f"## `{font_path}`", ""])
        if not subresults:
            lines.extend(["No contour-count findings.", ""])
            continue

        for subresult in subresults:
            lines.extend(
                [
                    f"### {subresult['severity']}: `{subresult.get('code', '')}`",
                    "",
                    "| Glyph | Codepoint | Actual contours | Expected contours |",
                    "| --- | --- | --- | --- |",
                ]
            )
            lines.extend(glyph_problem_rows(subresult))
            lines.append("")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = [Path(arg) for arg in argv[1:]]
    if not args:
        font_paths = DEFAULT_FONT_PATHS
        output_path = None
    elif len(args) == 1:
        font_paths = args
        output_path = None
    else:
        font_paths = args[:-1]
        output_path = args[-1]
    try:
        report = markdown_report(font_paths)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
