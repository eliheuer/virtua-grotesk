#!/usr/bin/env python3
"""Crop focused Arabic-row zoom snapshots for the first review batch."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = ROOT / "documentation/glyph-review/review-snapshots"
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-first-review-zoom-snapshots.md"
CROP_HEIGHT = 520
CROP_WIDTH = 1440
CROP_OFFSET_Y = 230
CROP_OFFSET_X = 0
OUTPUT_SCALE = 2


@dataclass(frozen=True)
class ZoomSnapshot:
    key: str
    label: str
    source_png: Path
    output_png: Path


ROWS = [
    ZoomSnapshot(
        "proof-regular-glyphs",
        "Regular Arabic glyph rows",
        SNAPSHOT_DIR / "proof-regular-glyphs.png",
        SNAPSHOT_DIR / "proof-regular-glyphs-arabic-zoom.png",
    ),
    ZoomSnapshot(
        "proof-medium-glyphs",
        "Medium Arabic glyph rows",
        SNAPSHOT_DIR / "proof-medium-glyphs.png",
        SNAPSHOT_DIR / "proof-medium-glyphs-arabic-zoom.png",
    ),
    ZoomSnapshot(
        "proof-semibold-glyphs",
        "SemiBold Arabic glyph rows",
        SNAPSHOT_DIR / "proof-semibold-glyphs.png",
        SNAPSHOT_DIR / "proof-semibold-glyphs-arabic-zoom.png",
    ),
    ZoomSnapshot(
        "proof-bold-glyphs",
        "Bold Arabic glyph rows",
        SNAPSHOT_DIR / "proof-bold-glyphs.png",
        SNAPSHOT_DIR / "proof-bold-glyphs-arabic-zoom.png",
    ),
]


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def crop_with_sips(sips: str, row: ZoomSnapshot) -> None:
    if not row.source_png.exists():
        raise FileNotFoundError(display_path(row.source_png))
    row.output_png.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sips,
        "--cropToHeightWidth",
        str(CROP_HEIGHT),
        str(CROP_WIDTH),
        "--cropOffset",
        str(CROP_OFFSET_Y),
        str(CROP_OFFSET_X),
        str(row.source_png),
        "--out",
        str(row.output_png),
    ]
    result = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    resample = [
        sips,
        "--resampleHeightWidth",
        str(CROP_HEIGHT * OUTPUT_SCALE),
        str(CROP_WIDTH * OUTPUT_SCALE),
        str(row.output_png),
        "--out",
        str(row.output_png),
    ]
    result = subprocess.run(resample, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    if not row.output_png.exists() or row.output_png.stat().st_size == 0:
        raise RuntimeError(f"{display_path(row.output_png)} was not written")


def markdown_report(rendered: list[ZoomSnapshot], errors: list[str], sips: str | None) -> str:
    lines = [
        "# Arabic First Review Zoom Snapshots",
        "",
        "This generated report crops the full glyph-proof snapshots down to the",
        "Arabic rows for the current structure/wrong-glyph review batch. These",
        "PNGs are still review aids only; open the full proof HTML before recording",
        "a `pass`, `fix-needed`, or `deferred` status.",
        "",
        f"- Crop source: `documentation/glyph-review/arabic-next-review-snapshots.md`",
        f"- Crop size: {CROP_WIDTH}x{CROP_HEIGHT}",
        f"- Output scale: {OUTPUT_SCALE}x",
        f"- Output size: {CROP_WIDTH * OUTPUT_SCALE}x{CROP_HEIGHT * OUTPUT_SCALE}",
        f"- Crop offset: y={CROP_OFFSET_Y}, x={CROP_OFFSET_X}",
        f"- `sips` executable: `{sips or 'not found'}`",
        f"- Requested zoom snapshots: {len(ROWS)}",
        f"- Rendered zoom snapshots: {len(rendered)}",
        f"- Errors: {len(errors)}",
        "",
        "## Zoom Snapshots",
        "",
        "| Review key | Label | Source PNG | Zoom PNG |",
        "| --- | --- | --- | --- |",
    ]
    for row in rendered:
        lines.append(
            f"| `{row.key}` | {row.label} | `{display_path(row.source_png)}` | `{display_path(row.output_png)}` |"
        )
    if errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
    lines.extend(
        [
            "",
            "## Review Use",
            "",
            "Use these crops to scan Arabic glyph coverage and obvious clipping faster.",
            "They do not prove small mark placement, dot collisions, or wrong-codepoint",
            "details; use the linked gftools proof HTML and source GLIF targets for",
            "final row decisions.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    sips = shutil.which("sips")
    rendered: list[ZoomSnapshot] = []
    errors: list[str] = []
    if sips:
        for row in ROWS:
            try:
                crop_with_sips(sips, row)
            except Exception as exc:
                errors.append(f"{row.key}: {exc}")
            else:
                rendered.append(row)
    else:
        errors.append("sips is not available on this system")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(rendered, errors, sips), encoding="utf-8")
    print(display_path(output))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
