#!/usr/bin/env python3
"""Report source structure for all unresolved Arabic review source targets."""

from __future__ import annotations

from collections import defaultdict
import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import report_arabic_first_batch_source_checkpoint as source_checkpoint
import report_arabic_manual_edit_targets as edit_targets
import report_arabic_visual_review_runbook as runbook


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-pending-source-checkpoint.md"


def master_name_for_ufo(ufo: Path) -> str:
    if "Regular" in ufo.name:
        return "Regular"
    if "Bold" in ufo.name:
        return "Bold"
    return ufo.name


def pending_rows() -> list[runbook.ReviewRow]:
    return sorted(
        [row for row in runbook.visual_rows() if row.status in {"pending", "fix-needed"}],
        key=runbook.row_priority,
    )


def row_target_map() -> list[tuple[runbook.ReviewRow, list[edit_targets.EditTarget]]]:
    return [(row, edit_targets.row_targets(row.key)) for row in pending_rows()]


def unique_glyph_names(rows_with_targets: list[tuple[runbook.ReviewRow, list[edit_targets.EditTarget]]]) -> list[str]:
    names = {
        target.glyph_name
        for _row, targets in rows_with_targets
        for target in targets
    }
    return sorted(names)


def target_lookup(
    rows_with_targets: list[tuple[runbook.ReviewRow, list[edit_targets.EditTarget]]],
) -> dict[str, dict[str, Path | None]]:
    lookup: dict[str, dict[str, Path | None]] = defaultdict(dict)
    for _row, targets in rows_with_targets:
        for target in targets:
            lookup[target.glyph_name][master_name_for_ufo(target.ufo)] = target.path
    return lookup


def state_from_path(master: str, glyph_name: str, path: Path | None) -> source_checkpoint.GlyphState:
    if path is None or not path.exists():
        fallback = source_checkpoint.MASTERS[master] / f"{glyph_name}.glif"
        return source_checkpoint.GlyphState(
            master=master,
            glyph_name=glyph_name,
            path=fallback if path is None else path,
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
            for attr in source_checkpoint.COMPONENT_ATTRS
            if component.get(attr) is not None
        )
        component_signature.append(attrs)

    bbox = "none" if not xs else f"{min(xs):.0f},{min(ys):.0f},{max(xs):.0f},{max(ys):.0f}"
    return source_checkpoint.GlyphState(
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


def glyph_states(glyph_name: str, lookup: dict[str, dict[str, Path | None]]) -> dict[str, source_checkpoint.GlyphState]:
    paths_by_master = lookup.get(glyph_name, {})
    return {
        master: state_from_path(master, glyph_name, paths_by_master.get(master))
        for master in source_checkpoint.MASTERS
    }


def structure_match(states: dict[str, source_checkpoint.GlyphState]) -> bool:
    return source_checkpoint.compatible(states["Regular"], states["Bold"])


def state_summary(state: source_checkpoint.GlyphState) -> str:
    if not state.exists:
        return "missing"
    return (
        f"width {state.width}; unicode {','.join(state.unicodes) or '-'}; "
        f"contours {state.contour_count}; components {state.component_count}; "
        f"points {state.point_count}; bbox `{state.bbox}`"
    )


def referenced_rows(
    glyph_name: str,
    rows_with_targets: list[tuple[runbook.ReviewRow, list[edit_targets.EditTarget]]],
) -> str:
    keys = []
    for row, targets in rows_with_targets:
        if any(target.glyph_name == glyph_name for target in targets):
            keys.append(row.key)
    return ", ".join(f"`{key}`" for key in sorted(set(keys), key=runbook.BATCH_REVIEW_PRIORITY.get))


def markdown_report() -> str:
    rows_with_targets = row_target_map()
    all_targets = [target for _row, targets in rows_with_targets for target in targets]
    unique_targets = edit_targets.unique_targets(all_targets)
    glyph_names = unique_glyph_names(rows_with_targets)
    lookup = target_lookup(rows_with_targets)
    states_by_glyph = {glyph_name: glyph_states(glyph_name, lookup) for glyph_name in glyph_names}
    missing_states = [
        state
        for states in states_by_glyph.values()
        for state in states.values()
        if not state.exists
    ]
    mismatches = [
        glyph_name
        for glyph_name, states in states_by_glyph.items()
        if not structure_match(states)
    ]
    rows_with_any_targets = sum(1 for _row, targets in rows_with_targets if targets)
    row_target_counts: dict[str, int] = defaultdict(int)
    for row, targets in rows_with_targets:
        row_target_counts[row.key] = len(edit_targets.unique_targets(targets))

    lines = [
        "# Arabic Pending Source Checkpoint",
        "",
        "This generated report records source-side structure for every unique",
        "Regular/Bold glyph currently referenced by unresolved Arabic visual",
        "review rows. It is a drawing-session guardrail, not visual approval.",
        "",
        "## Summary",
        "",
        f"- Pending or fix-needed review rows: {len(rows_with_targets)}",
        f"- Rows with source targets: {rows_with_any_targets}",
        f"- Unique source glyph names checked: {len(glyph_names)}",
        f"- Unique source target files referenced: {len(unique_targets)}",
        f"- Missing source files: {len(missing_states)}",
        f"- Regular/Bold structure mismatches: {len(mismatches)}",
        f"- Ready for paired-master hand review: {'yes' if not missing_states and not mismatches else 'no'}",
        "",
        "## Row Target Counts",
        "",
        "| Review key | Source targets |",
        "| --- | ---: |",
    ]
    for row, _targets in rows_with_targets:
        lines.append(f"| `{row.key}` | {row_target_counts[row.key]} |")

    lines.extend(
        [
            "",
            "## Glyph Structure",
            "",
            "| Glyph | Referenced by rows | Regular | Bold | Structure match | Components |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for glyph_name in glyph_names:
        states = states_by_glyph[glyph_name]
        regular = states["Regular"]
        bold = states["Bold"]
        lines.append(
            f"| `{glyph_name}` | {referenced_rows(glyph_name, rows_with_targets)} | "
            f"{state_summary(regular)} | {state_summary(bold)} | "
            f"{'yes' if structure_match(states) else 'no'} | {source_checkpoint.component_text(regular)} |"
        )

    lines.extend(
        [
            "",
            "## Use",
            "",
            "- Use this before broad hand cleanup to confirm unresolved review rows",
            "  still map to paired Regular/Bold source files.",
            "- If a row becomes `fix-needed`, edit only the relevant paired source",
            "  glyphs, then rerun this report plus `make arabic-after-drawing-check`.",
            "- Keep review outcomes in `documentation/glyph-review/arabic-visual-review-log.md`;",
            "  this checkpoint only records source structure.",
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
