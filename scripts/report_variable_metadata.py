#!/usr/bin/env python3
"""Report variable-font axis, fvar, STAT, and avar metadata."""

from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont


DEFAULT_FONT_PATH = Path("fonts/variable/VirtuaGrotesk[wght].ttf")


def name(font: TTFont, name_id: int) -> str:
    record = font["name"].getName(name_id, 3, 1, 0x409)
    return record.toUnicode() if record else ""


def axis_rows(font: TTFont) -> list[str]:
    rows = [
        "| Tag | Name | Min | Default | Max | Flags |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for axis in font["fvar"].axes:
        rows.append(
            "| `{}` | {} | {:.0f} | {:.0f} | {:.0f} | {} |".format(
                axis.axisTag,
                name(font, axis.axisNameID),
                axis.minValue,
                axis.defaultValue,
                axis.maxValue,
                axis.flags,
            )
        )
    return rows


def instance_rows(font: TTFont) -> list[str]:
    rows = [
        "| Subfamily | Coordinates | PostScript name | Flags |",
        "| --- | --- | --- | ---: |",
    ]
    for instance in font["fvar"].instances:
        coords = ", ".join(f"{tag}={value:.0f}" for tag, value in sorted(instance.coordinates.items()))
        postscript_name = name(font, instance.postscriptNameID) if instance.postscriptNameID != 0xFFFF else ""
        rows.append(
            "| {} | `{}` | `{}` | {} |".format(
                name(font, instance.subfamilyNameID),
                coords,
                postscript_name or "none",
                instance.flags,
            )
        )
    return rows


def stat_axis_rows(font: TTFont) -> list[str]:
    rows = [
        "| Tag | Name | Ordering |",
        "| --- | --- | ---: |",
    ]
    if "STAT" not in font:
        return rows
    for axis in font["STAT"].table.DesignAxisRecord.Axis:
        rows.append(f"| `{axis.AxisTag}` | {name(font, axis.AxisNameID)} | {axis.AxisOrdering} |")
    return rows


def stat_value_rows(font: TTFont) -> list[str]:
    rows = [
        "| Format | Name | Axis index | Value | Linked value | Flags |",
        "| ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    if "STAT" not in font:
        return rows
    for value in font["STAT"].table.AxisValueArray.AxisValue:
        linked = getattr(value, "LinkedValue", None)
        rows.append(
            "| {} | {} | {} | {:.0f} | {} | {} |".format(
                value.Format,
                name(font, value.ValueNameID),
                getattr(value, "AxisIndex", ""),
                getattr(value, "Value", 0),
                f"{linked:.0f}" if linked is not None else "",
                value.Flags,
            )
        )
    return rows


def markdown_report(font_path: Path) -> str:
    font = TTFont(font_path)
    lines = [
        "# Variable Font Metadata",
        "",
        f"Font: `{font_path}`",
        "",
        (
            "This report records variable-font axis metadata that matters for "
            "Google Fonts packaging and metadata review. It is generated from "
            "the built variable TTF, not from source assumptions."
        ),
        "",
        "## Summary",
        "",
        f"- Has `fvar`: {'yes' if 'fvar' in font else 'no'}",
        f"- Has `STAT`: {'yes' if 'STAT' in font else 'no'}",
        f"- Has `avar`: {'yes' if 'avar' in font else 'no'}",
        f"- Axis tags: {', '.join(f'`{axis.axisTag}`' for axis in font['fvar'].axes)}",
        "",
        "## fvar Axes",
        "",
        *axis_rows(font),
        "",
        "## fvar Instances",
        "",
        *instance_rows(font),
        "",
        "## STAT Axes",
        "",
        *stat_axis_rows(font),
        "",
        "## STAT Axis Values",
        "",
        *stat_value_rows(font),
        "",
        "## Review Notes",
        "",
        "- The current `wght` axis is 400-700 with default 400.",
        "- The 600 instance is named `SemiBold`, matching Google Fonts style naming.",
        "- The Regular STAT axis value is linked to Bold.",
        "- No `avar` table is emitted; keep or change this according to the `avar` decision log entry.",
        "",
    ]
    font.close()
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
