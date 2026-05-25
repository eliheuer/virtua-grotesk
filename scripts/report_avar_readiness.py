#!/usr/bin/env python3
"""Generate an avar decision-readiness report for the variable font."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONT_PATH = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
OUTPUT_DEFAULT = Path("documentation/avar-readiness.md")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def warning_count() -> int:
    text = read_text(ROOT / "documentation/fontspector-warnings.md")
    match = re.search(r"\| `mandatory_avar_table` \| `missing-avar` \| (\d+) \|", text)
    return int(match.group(1)) if match else 0


def decision_status() -> str:
    decisions = read_text(ROOT / "documentation/google-fonts-decisions.md")
    match = re.search(r"## `avar`\s*\n\s*Status: ([a-z]+)", decisions)
    return match.group(1) if match else "unknown"


def normalized(value: float, minimum: float, default: float, maximum: float) -> float:
    if value == default:
        return 0.0
    if value < default:
        return (value - default) / (default - minimum)
    return (value - default) / (maximum - default)


def markdown_report(font_path: Path) -> str:
    font = TTFont(ROOT / font_path)
    axis = next(axis for axis in font["fvar"].axes if axis.axisTag == "wght")
    instances = [
        (name.toUnicode(), instance.coordinates["wght"])
        for instance in font["fvar"].instances
        for name in [font["name"].getName(instance.subfamilyNameID, 3, 1, 0x409)]
        if name is not None
    ]
    has_avar = "avar" in font
    minimum = float(axis.minValue)
    default = float(axis.defaultValue)
    maximum = float(axis.maxValue)

    lines = [
        "# avar Readiness",
        "",
        "This generated report tracks the `avar` decision surface for Google",
        "Fonts onboarding. The Google Fonts variable-font guide explains that a",
        "linear interpolation can make `avar` unnecessary, while non-linear",
        "weight progression should be encoded with an `avar` table.",
        "",
        "## Summary",
        "",
        f"- Font: `{font_path}`",
        f"- Axis: `wght` {minimum:.0f}-{maximum:.0f}, default {default:.0f}",
        f"- Has `avar`: {'yes' if has_avar else 'no'}",
        f"- Fontspector `mandatory_avar_table` warnings: {warning_count()}",
        f"- Current decision: {decision_status()}",
        "",
        "## Current Linear Mapping",
        "",
        "| Instance | User coordinate | Normalized coordinate |",
        "| --- | ---: | ---: |",
    ]

    for instance_name, coordinate in sorted(instances, key=lambda item: item[1]):
        lines.append(
            f"| {instance_name} | {coordinate:.0f} | {normalized(coordinate, minimum, default, maximum):.4f} |"
        )

    lines.extend(
        [
            "",
            "## Review Options",
            "",
            "- Keep the axis linear and record that `avar` is intentionally omitted.",
            "- Add a non-linear `avar` mapping if Medium, SemiBold, or another",
            "  interpolated style should sit at a different design-space pace than",
            "  the current linear coordinates.",
            "",
            "## Apply After Maintainer Decision",
            "",
            "- If keeping the axis linear, record the decision in",
            "  `documentation/google-fonts-decisions.md` and the downstream issue or",
            "  PR notes if Fontspector still warns.",
            "- If adding `avar`, update the source designspace/build config, rebuild,",
            "  and regenerate `documentation/variable-font-metadata.md`,",
            "  `documentation/google-fonts-axis-registry-audit.md`, this report, and",
            "  Fontspector reports.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/variable.html",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://github.com/fonttools/fontspector",
            "",
        ]
    )
    font.close()
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_avar_readiness.py [font.ttf] [output.md]")
    if len(argv) == 1:
        return DEFAULT_FONT_PATH, OUTPUT_DEFAULT
    if len(argv) == 2:
        return DEFAULT_FONT_PATH, Path(argv[1])
    return Path(argv[1]), Path(argv[2])


def main(argv: list[str]) -> int:
    font_path, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(font_path), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
