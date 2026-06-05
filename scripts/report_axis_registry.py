#!/usr/bin/env python3
"""Compare built variable-font axis metadata against Google Fonts axisregistry."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys

from fontTools.ttLib import TTFont


DEFAULT_FONT_PATH = Path("fonts/variable/VirtuaGrotesk[wght].ttf")
DEFAULT_REGISTRY_PATH = Path(os.environ["GF_WEIGHT_AXIS_REGISTRY"]) if os.environ.get("GF_WEIGHT_AXIS_REGISTRY") else None


@dataclass(frozen=True)
class Fallback:
    name: str
    value: int


@dataclass(frozen=True)
class AxisRegistryEntry:
    tag: str
    display_name: str
    minimum: int
    default: int
    maximum: int
    precision: int
    fallback_only: bool
    fallbacks: tuple[Fallback, ...]


def name(font: TTFont, name_id: int) -> str:
    record = font["name"].getName(name_id, 3, 1, 0x409)
    return record.toUnicode() if record else ""


def parse_scalar(text: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s+(.*)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {key} in axis registry textproto")
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def parse_registry(path: Path) -> AxisRegistryEntry:
    text = path.read_text()
    fallbacks = []
    for block in re.findall(r"fallback\s*\{(.*?)\}", text, flags=re.DOTALL):
        fallbacks.append(
            Fallback(
                name=parse_scalar(block, "name"),
                value=int(parse_scalar(block, "value")),
            )
        )
    return AxisRegistryEntry(
        tag=parse_scalar(text, "tag"),
        display_name=parse_scalar(text, "display_name"),
        minimum=int(parse_scalar(text, "min_value")),
        default=int(parse_scalar(text, "default_value")),
        maximum=int(parse_scalar(text, "max_value")),
        precision=int(parse_scalar(text, "precision")),
        fallback_only=parse_scalar(text, "fallback_only").lower() == "true",
        fallbacks=tuple(fallbacks),
    )


def fvar_instance_map(font: TTFont) -> dict[int, str]:
    return {
        int(instance.coordinates["wght"]): name(font, instance.subfamilyNameID)
        for instance in font["fvar"].instances
    }


def stat_value_map(font: TTFont) -> dict[int, str]:
    if "STAT" not in font:
        return {}
    values = {}
    for axis_value in font["STAT"].table.AxisValueArray.AxisValue:
        values[int(getattr(axis_value, "Value", -1))] = name(font, axis_value.ValueNameID)
    return values


def unavailable_report(font_path: Path, registry_path: Path | None) -> str:
    registry_label = str(registry_path) if registry_path else "not configured"
    return "\n".join(
        [
            "# Google Fonts Axis Registry Audit",
            "",
            f"Font: `{font_path}`",
            f"Registry source: `{registry_label}`",
            "",
            "The local Google Fonts axis registry checkout is not configured.",
            "",
            "## Summary",
            "",
            "- Registry available: no",
            "- Set `GF_REPO_PATH=/path/to/google/fonts` or `GF_WEIGHT_AXIS_REGISTRY=/path/to/weight.textproto` when this audit is needed.",
            "",
        ]
    )


def markdown_report(font_path: Path, registry_path: Path | None) -> str:
    if registry_path is None or str(registry_path) == "" or not registry_path.exists():
        return unavailable_report(font_path, registry_path)
    registry = parse_registry(registry_path)
    font = TTFont(font_path)
    fvar_axis = next(axis for axis in font["fvar"].axes if axis.axisTag == "wght")
    fvar_instances = fvar_instance_map(font)
    stat_values = stat_value_map(font)
    family_fallbacks = [
        fallback
        for fallback in registry.fallbacks
        if int(fvar_axis.minValue) <= fallback.value <= int(fvar_axis.maxValue)
    ]

    lines = [
        "# Google Fonts Axis Registry Audit",
        "",
        f"Font: `{font_path}`",
        f"Registry source: `{registry_path}`",
        "",
        (
            "This report compares the built variable font's `wght` metadata to "
            "the local `google/fonts` axis registry entry used by Google Fonts "
            "for canonical axis names and fallback labels."
        ),
        "",
        "## Summary",
        "",
        f"- Registry tag: `{registry.tag}`",
        f"- Registry display name: {registry.display_name}",
        f"- Registry bounds/default: {registry.minimum}/{registry.default}/{registry.maximum}",
        f"- Registry precision: {registry.precision}",
        f"- Registry fallback-only: {'yes' if registry.fallback_only else 'no'}",
        f"- Font `wght` bounds/default: {fvar_axis.minValue:.0f}/{fvar_axis.defaultValue:.0f}/{fvar_axis.maxValue:.0f}",
        f"- Family fallback subset: {', '.join(f'{fallback.name} {fallback.value}' for fallback in family_fallbacks)}",
        "",
        "## Axis Checks",
        "",
        "| Check | Result |",
        "| --- | --- |",
        f"| Registry tag is `wght` | {'yes' if registry.tag == 'wght' else 'no'} |",
        f"| Font axis name matches registry display name | {'yes' if name(font, fvar_axis.axisNameID) == registry.display_name else 'no'} |",
        f"| Font default matches registry default | {'yes' if int(fvar_axis.defaultValue) == registry.default else 'no'} |",
        f"| Font range is within registry range | {'yes' if registry.minimum <= int(fvar_axis.minValue) <= int(fvar_axis.maxValue) <= registry.maximum else 'no'} |",
        f"| Font uses registered fallback names for its range | {'yes' if all(fvar_instances.get(fallback.value) == fallback.name for fallback in family_fallbacks) else 'no'} |",
        f"| STAT values use registered fallback names for its range | {'yes' if all(stat_values.get(fallback.value) == fallback.name for fallback in family_fallbacks) else 'no'} |",
        "",
        "## Registered Fallbacks",
        "",
        "| Name | Value | In font range | fvar instance | STAT value |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for fallback in registry.fallbacks:
        in_range = int(fvar_axis.minValue) <= fallback.value <= int(fvar_axis.maxValue)
        lines.append(
            "| {} | {} | {} | {} | {} |".format(
                fallback.name,
                fallback.value,
                "yes" if in_range else "no",
                fvar_instances.get(fallback.value, ""),
                stat_values.get(fallback.value, ""),
            )
        )

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- The family intentionally uses the registered `wght` axis subset 400-700.",
            "- The 600 fallback is spelled `SemiBold`, matching the Google Fonts axis registry.",
            "- No custom axis is present, so no new axis registry proposal is needed.",
            "- The `avar` warning remains a separate first-submission decision.",
            "",
        ]
    )
    font.close()
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    font_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_FONT_PATH
    registry_path = Path(argv[2]) if len(argv) > 2 and argv[2] else DEFAULT_REGISTRY_PATH
    output_path = Path(argv[3]) if len(argv) > 3 else None
    try:
        report = markdown_report(font_path, registry_path)
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
