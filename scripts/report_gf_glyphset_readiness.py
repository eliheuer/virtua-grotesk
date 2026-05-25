#!/usr/bin/env python3
"""Report Google Fonts glyphset/subset readiness for a built font."""

from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont
import glyphsets


DEFAULT_FONT_PATH = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
TRACKED_GLYPHSETS = [
    "GF_Latin_Kernel",
    "GF_Latin_Core",
    "GF_Arabic_Core",
    "GF_Arabic_Plus",
]


def glyphset_row(name: str, result: dict) -> str:
    required_count = len(result["has"]) + len(result["missing"])
    languages = glyphsets.languages_per_glyphset(name)
    script = glyphsets.get_script(name)
    return "| `{}` | {} | {} | {} | {} | {:.2f}% | {} |".format(
        name,
        script,
        required_count,
        len(result["has"]),
        len(result["missing"]),
        result["percentage"] * 100,
        ", ".join(f"`{language}`" for language in languages) if languages else "none",
    )


def markdown_report(font_path: Path) -> str:
    font = TTFont(font_path)
    results = glyphsets.get_glyphsets_fulfilled(font)
    font.close()

    lines = [
        "# Google Fonts Glyphset Readiness",
        "",
        f"Font: `{font_path}`",
        "",
        (
            "This report summarizes Google Fonts authoring glyphset coverage for "
            "the intended Latin plus Arabic submission scope. It is generated "
            "from the installed `glyphsets` package and should be reviewed with "
            "the downstream `METADATA.pb` subset and primary-script decisions."
        ),
        "",
        "## Tracked Glyphsets",
        "",
        "| Glyphset | Script | Required codepoints | Present | Missing | Coverage | Language codes |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]

    for name in TRACKED_GLYPHSETS:
        lines.append(glyphset_row(name, results[name]))

    lines.extend(
        [
            "",
            "## Metadata Implications",
            "",
            "- First-submission subsets should include `menu`, `latin`, and `arabic` after drawing work is complete; add `latin-ext` only after enough coverage exists.",
            "- `primary_script: \"Arab\"` remains the current metadata review target because Arabic is in first-submission scope.",
            "- `GF_Arabic_Core` is the current minimum Arabic target; `GF_Arabic_Plus` is tracked here only to show the cost of expanding scope.",
            "- This report is coverage evidence only; shaping, mark behavior, and visual proofing are tracked separately.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    font_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_FONT_PATH
    output_path = Path(argv[2]) if len(argv) > 2 else None
    try:
        report = markdown_report(font_path)
    except Exception as exc:
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
