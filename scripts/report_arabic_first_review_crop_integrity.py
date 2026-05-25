#!/usr/bin/env python3
"""Report mechanical integrity for first-review Arabic focused crops."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from PIL import Image, ImageChops

from report_arabic_visual_review_runbook import ROOT


DEFAULT_OUTPUT = ROOT / "documentation/arabic-first-review-crop-integrity.md"
EXPECTED_WIDTH = 2880
EXPECTED_HEIGHT = 1040
NONWHITE_THRESHOLD = 245


@dataclass(frozen=True)
class Crop:
    key: str
    weight: str
    path: Path


CROPS = [
    Crop(
        "proof-regular-glyphs",
        "Regular",
        ROOT / "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png",
    ),
    Crop(
        "proof-medium-glyphs",
        "Medium",
        ROOT / "documentation/arabic-review-snapshots/proof-medium-glyphs-arabic-zoom.png",
    ),
    Crop(
        "proof-semibold-glyphs",
        "SemiBold",
        ROOT / "documentation/arabic-review-snapshots/proof-semibold-glyphs-arabic-zoom.png",
    ),
    Crop(
        "proof-bold-glyphs",
        "Bold",
        ROOT / "documentation/arabic-review-snapshots/proof-bold-glyphs-arabic-zoom.png",
    ),
]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def inspect_crop(crop: Crop) -> dict[str, object]:
    if not crop.path.exists():
        return {
            "status": "missing",
            "dimensions": "n/a",
            "dimension_match": False,
            "nonblank": False,
            "nonwhite_ratio": "n/a",
            "bbox": "n/a",
            "result": "missing",
        }
    try:
        with Image.open(crop.path) as image:
            rgb = image.convert("RGB")
    except Exception as exc:
        return {
            "status": f"unreadable: {exc}",
            "dimensions": "n/a",
            "dimension_match": False,
            "nonblank": False,
            "nonwhite_ratio": "n/a",
            "bbox": "n/a",
            "result": "unreadable",
        }
    width, height = rgb.size
    total = width * height
    data = rgb.tobytes()
    nonwhite = sum(
        1
        for index in range(0, len(data), 3)
        if min(data[index], data[index + 1], data[index + 2]) < NONWHITE_THRESHOLD
    )
    bbox = ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white")).getbbox()
    dimension_match = width == EXPECTED_WIDTH and height == EXPECTED_HEIGHT
    nonblank = nonwhite > 0 and bbox is not None
    result = "ok" if dimension_match and nonblank else "needs regeneration"
    return {
        "status": "readable",
        "dimensions": f"{width}x{height}",
        "dimension_match": dimension_match,
        "nonblank": nonblank,
        "nonwhite_ratio": f"{(nonwhite / total):.4%}",
        "bbox": "n/a" if bbox is None else f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "result": result,
    }


def markdown_report() -> str:
    rows = [(crop, inspect_crop(crop)) for crop in CROPS]
    readable = sum(1 for _, row in rows if row["status"] == "readable")
    dimensions = sum(1 for _, row in rows if row["dimension_match"])
    nonblank = sum(1 for _, row in rows if row["nonblank"])
    errors = len(CROPS) - sum(1 for _, row in rows if row["result"] == "ok")
    ready = "yes" if readable == len(CROPS) and dimensions == len(CROPS) and nonblank == len(CROPS) else "no"
    lines = [
        "# Arabic First Review Crop Integrity",
        "",
        "This generated report mechanically checks the focused Arabic-row PNG",
        "crops for the first hand-review batch. It proves only that the crop files",
        "are readable, correctly sized, and nonblank; it is not a human Arabic",
        "drawing review.",
        "",
        f"- Expected dimensions: {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}",
        f"- Requested crops: {len(CROPS)}",
        f"- Readable crops: {readable}",
        f"- Dimension matches: {dimensions}",
        f"- Nonblank crops: {nonblank}",
        f"- Crop errors: {errors}",
        f"- Evidence ready for hand review: {ready}",
        "",
        "## Crop Checks",
        "",
        "| Review key | Weight | Crop path | Dimensions | File status | Nonwhite sample | Content bbox | Result |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for crop, row in rows:
        lines.append(
            f"| `{crop.key}` | {crop.weight} | `{display_path(crop.path)}` | "
            f"{row['dimensions']} | {row['status']} | {row['nonwhite_ratio']} | "
            f"{row['bbox']} | {row['result']} |"
        )
    lines.extend(
        [
            "",
            "## Non-Decisions",
            "",
            "- No row was marked `pass`.",
            "- No row was marked `fix-needed`.",
            "- No row was deferred.",
            "- Do not edit Arabic outlines, marks, or sidebearings from this report alone.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    print(display_path(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
