#!/usr/bin/env python3
"""Report source and built version metadata for Google Fonts release tagging."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import plistlib
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/release-metadata.md")
SOURCE_FONTINFO = [
    Path("sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist"),
    Path("sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist"),
]
BUILT_FONTS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]


@dataclass(frozen=True)
class SourceVersion:
    path: Path
    major: int | None
    minor: int | None


@dataclass(frozen=True)
class BuiltVersion:
    path: Path
    name_id_5: str


def source_version(path: Path) -> SourceVersion:
    with (ROOT / path).open("rb") as file:
        info = plistlib.load(file)
    return SourceVersion(
        path=path,
        major=info.get("versionMajor"),
        minor=info.get("versionMinor"),
    )


def built_version(path: Path) -> BuiltVersion:
    font = TTFont(ROOT / path)
    name = font["name"].getName(5, 3, 1, 0x409)
    value = name.toUnicode() if name else ""
    font.close()
    return BuiltVersion(path=path, name_id_5=value)


def source_version_string(version: SourceVersion) -> str:
    if version.major is None or version.minor is None:
        return "missing"
    return f"{version.major}.{version.minor:03d}"


def primary_source_version(versions: list[SourceVersion]) -> str:
    strings = {source_version_string(version) for version in versions}
    return strings.pop() if len(strings) == 1 else "mixed"


def markdown_report() -> str:
    source_versions = [source_version(path) for path in SOURCE_FONTINFO]
    built_versions = [built_version(path) for path in BUILT_FONTS if (ROOT / path).exists()]
    version = primary_source_version(source_versions)
    expected_name_id_5 = f"Version {version}" if version not in {"missing", "mixed"} else ""
    suggested_tag = f"v{version}" if version not in {"missing", "mixed"} else "pending"
    name_id_matches = all(
        built.name_id_5.startswith(expected_name_id_5)
        for built in built_versions
    ) if expected_name_id_5 else False

    lines = [
        "# Release Metadata",
        "",
        "This generated report ties the release checklist to current source UFO",
        "versions and built font name ID 5 values. Use it before tagging the",
        "upstream source state for Google Fonts packaging.",
        "",
        "## Summary",
        "",
        f"- Source version: `{version}`",
        f"- Expected built name ID 5 prefix: `{expected_name_id_5 or 'unknown'}`",
        f"- Suggested first-submission tag: `{suggested_tag}`",
        f"- Built fonts match source version: {'yes' if name_id_matches else 'no'}",
        "",
        "## Source UFO Versions",
        "",
        "| Source | versionMajor | versionMinor | Version string |",
        "| --- | ---: | ---: | --- |",
    ]
    for version_info in source_versions:
        lines.append(
            f"| `{version_info.path}` | {version_info.major} | {version_info.minor} | "
            f"`{source_version_string(version_info)}` |"
        )

    lines.extend(
        [
            "",
            "## Built Font Versions",
            "",
            "| Font | name ID 5 | Matches source version |",
            "| --- | --- | --- |",
        ]
    )
    for built in built_versions:
        matches = bool(expected_name_id_5 and built.name_id_5.startswith(expected_name_id_5))
        lines.append(
            f"| `{built.path}` | `{built.name_id_5}` | {'yes' if matches else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Before Tagging",
            "",
            "- Confirm the version strategy decision in `documentation/google-fonts-decisions.md`.",
            "- Confirm the final upstream tag and commit in `documentation/google-fonts-release-checklist.md`.",
            "- Regenerate this report with `make preflight` after changing source or build versions.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_release_metadata.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
