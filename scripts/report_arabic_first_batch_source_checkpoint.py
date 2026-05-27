#!/usr/bin/env python3
"""Report source structure for the current Arabic first-review glyphs."""

from __future__ import annotations

from dataclasses import dataclass
import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/arabic-first-batch-source-checkpoint.md"
MASTERS = {
    "Regular": ROOT / "sources/VirtuaGrotesk-Regular.ufo/glyphs",
    "Bold": ROOT / "sources/VirtuaGrotesk-Bold.ufo/glyphs",
}
GLYPHS = [
    "hamzaabove-ar",
    "hamzabelow-ar",
    "madda-ar",
    "seen-ar",
    "sheen-ar",
    "theh-ar",
    "waw-ar",
]
COMPONENT_ATTRS = ("base", "xOffset", "yOffset", "xScale", "xyScale", "yxScale", "yScale")


@dataclass(frozen=True)
class GlyphState:
    master: str
    glyph_name: str
    path: Path
    exists: bool
    width: str
    unicodes: tuple[str, ...]
    contour_count: int
    component_count: int
    point_count: int
    bbox: str
    contour_signature: tuple[tuple[str, ...], ...]
    component_signature: tuple[tuple[tuple[str, str], ...], ...]


def glyph_path(master: str, glyph_name: str) -> Path:
    return MASTERS[master] / f"{glyph_name}.glif"


def glyph_state(master: str, glyph_name: str) -> GlyphState:
    path = glyph_path(master, glyph_name)
    if not path.exists():
        return GlyphState(
            master=master,
            glyph_name=glyph_name,
            path=path,
            exists=False,
            width="missing",
            unicodes=(),
            contour_count=0,
            component_count=0,
            point_count=0,
            bbox="missing",
            contour_signature=(),
            component_signature=(),
        )

    root = ET.parse(path).getroot()
    advance = root.find("advance")
    width = advance.get("width") if advance is not None and advance.get("width") else "0"
    unicodes = tuple(node.get("hex", "") for node in root.findall("unicode") if node.get("hex"))
    contours = root.findall("outline/contour")
    components = root.findall("outline/component")

    xs: list[float] = []
    ys: list[float] = []
    point_count = 0
    contour_signature: list[tuple[str, ...]] = []
    for contour in contours:
        points = contour.findall("point")
        point_count += len(points)
        contour_signature.append(tuple(point.get("type", "offcurve") for point in points))
        for point in points:
            x = point.get("x")
            y = point.get("y")
            if x is not None and y is not None:
                xs.append(float(x))
                ys.append(float(y))

    component_signature: list[tuple[tuple[str, str], ...]] = []
    for component in components:
        attrs = tuple(
            (attr, component.get(attr, ""))
            for attr in COMPONENT_ATTRS
            if component.get(attr) is not None
        )
        component_signature.append(attrs)

    bbox = "none" if not xs else f"{min(xs):.0f},{min(ys):.0f},{max(xs):.0f},{max(ys):.0f}"
    return GlyphState(
        master=master,
        glyph_name=glyph_name,
        path=path,
        exists=True,
        width=width,
        unicodes=unicodes,
        contour_count=len(contours),
        component_count=len(components),
        point_count=point_count,
        bbox=bbox,
        contour_signature=tuple(contour_signature),
        component_signature=tuple(component_signature),
    )


def compatible(regular: GlyphState, bold: GlyphState) -> bool:
    return (
        regular.exists
        and bold.exists
        and regular.contour_signature == bold.contour_signature
        and regular.component_signature == bold.component_signature
    )


def component_text(state: GlyphState) -> str:
    if not state.component_signature:
        return "-"
    parts: list[str] = []
    for component in state.component_signature:
        values = dict(component)
        base = values.pop("base", "")
        offsets = ", ".join(f"{key}={value}" for key, value in values.items())
        parts.append(f"`{base}`" + (f" ({offsets})" if offsets else ""))
    return "<br>".join(parts)


def markdown_report() -> str:
    states = {
        glyph_name: {master: glyph_state(master, glyph_name) for master in MASTERS}
        for glyph_name in GLYPHS
    }
    missing = [
        state
        for master_states in states.values()
        for state in master_states.values()
        if not state.exists
    ]
    incompatible = [
        glyph_name
        for glyph_name, master_states in states.items()
        if not compatible(master_states["Regular"], master_states["Bold"])
    ]

    lines = [
        "# Arabic First Batch Source Checkpoint",
        "",
        "This generated report records source-side structure for the glyphs",
        "called out by the current structure and wrong-glyph review batch.",
        "Use it before and after hand edits to catch accidental Regular/Bold",
        "structure drift. It is not visual approval and does not mark any",
        "review row as passed.",
        "",
        "## Summary",
        "",
        f"- Glyphs checked: {len(GLYPHS)}",
        f"- Masters checked: {len(MASTERS)}",
        f"- Missing source files: {len(missing)}",
        f"- Regular/Bold structure mismatches: {len(incompatible)}",
        f"- Ready for paired-master hand review: {'yes' if not missing and not incompatible else 'no'}",
        "",
        "## Glyph Structure",
        "",
        "| Glyph | Regular | Bold | Structure match | Components |",
        "| --- | --- | --- | --- | --- |",
    ]

    for glyph_name in GLYPHS:
        regular = states[glyph_name]["Regular"]
        bold = states[glyph_name]["Bold"]
        regular_text = (
            f"width {regular.width}; unicode {','.join(regular.unicodes) or '-'}; "
            f"contours {regular.contour_count}; components {regular.component_count}; "
            f"points {regular.point_count}; bbox `{regular.bbox}`"
        )
        bold_text = (
            f"width {bold.width}; unicode {','.join(bold.unicodes) or '-'}; "
            f"contours {bold.contour_count}; components {bold.component_count}; "
            f"points {bold.point_count}; bbox `{bold.bbox}`"
        )
        lines.append(
            f"| `{glyph_name}` | {regular_text} | {bold_text} | "
            f"{'yes' if compatible(regular, bold) else 'no'} | {component_text(regular)} |"
        )

    lines.extend(
        [
            "",
            "## Source Files",
            "",
            "| Glyph | Regular GLIF | Bold GLIF |",
            "| --- | --- | --- |",
        ]
    )
    for glyph_name in GLYPHS:
        regular = states[glyph_name]["Regular"]
        bold = states[glyph_name]["Bold"]
        lines.append(
            f"| `{glyph_name}` | `{regular.path.relative_to(ROOT)}` | `{bold.path.relative_to(ROOT)}` |"
        )

    lines.extend(
        [
            "",
            "## Use",
            "",
            "- If a visual row becomes `fix-needed`, edit the Regular and Bold",
            "  source files together and preserve the structure match unless a",
            "  deliberate mirrored structural change is required.",
            "- Rerun `make arabic-first-batch-source-checkpoint` after source edits",
            "  and before `make arabic-after-drawing-check`.",
            "- Keep visual decisions in `documentation/arabic-visual-review-log.md`;",
            "  this file is only a source-structure checkpoint.",
            "",
        ]
    )
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main(argv: list[str]) -> int:
    args = parser().parse_args(argv[1:])
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
