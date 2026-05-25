#!/usr/bin/env python3
"""Report whether the active UFO sources are ready for editor hand cleanup."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import plistlib
import sys

from fontTools.ufoLib import UFOReader
from fontTools.ufoLib.glifLib import GlyphSet


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/ufo-editor-readiness.md"
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]


@dataclass(frozen=True)
class UfoCheck:
    path: Path
    loadable: bool
    layers: tuple[str, ...]
    glyph_count: int
    glif_read_errors: tuple[str, ...]
    missing_files: tuple[str, ...]
    duplicate_files: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return (
            self.loadable
            and self.layers == ("public.default",)
            and self.glyph_count > 0
            and not self.glif_read_errors
            and not self.missing_files
            and not self.duplicate_files
        )


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def duplicate_values(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return tuple(sorted(duplicates))


def check_ufo(path: Path) -> UfoCheck:
    layers: tuple[str, ...] = ()
    glyph_count = 0
    glif_read_errors: list[str] = []
    missing_files: list[str] = []
    duplicate_files: tuple[str, ...] = ()

    try:
        reader = UFOReader(path, validate=True)
        layers = tuple(reader.getLayerNames())
        glyph_count = len(reader.getGlyphSet().keys())
    except Exception as error:
        return UfoCheck(path, False, layers, glyph_count, (str(error),), (), ())

    contents_path = path / "glyphs/contents.plist"
    with contents_path.open("rb") as file:
        contents = plistlib.load(file)
    filenames = list(contents.values())
    duplicate_files = duplicate_values(filenames)
    for glyph_name, filename in contents.items():
        if not (path / "glyphs" / filename).exists():
            missing_files.append(f"{glyph_name} -> {filename}")

    glyph_set = GlyphSet(str(path / "glyphs"), validateRead=True)
    for glyph_name in sorted(glyph_set.keys()):
        try:
            glyph_set.readGlyph(glyph_name, validate=True)
        except Exception as error:
            glif_read_errors.append(f"{glyph_name}: {error}")

    return UfoCheck(
        path,
        True,
        layers,
        glyph_count,
        tuple(glif_read_errors),
        tuple(sorted(missing_files)),
        duplicate_files,
    )


def markdown_report() -> str:
    checks = [check_ufo(path) for path in SOURCE_UFOS]
    ready = all(check.ready for check in checks)

    lines = [
        "# UFO Editor Readiness",
        "",
        "This generated report checks that the active source UFOs are readable",
        "before hand cleanup in Runebender or another UFO editor. It does not",
        "launch the editor; it validates the on-disk UFO package with",
        "`fontTools.ufoLib` and reads every GLIF in strict mode.",
        "",
        f"- UFO editor handoff ready: {'yes' if ready else 'no'}",
        f"- UFOs checked: {len(checks)}",
        f"- GLIF read errors: {sum(len(check.glif_read_errors) for check in checks)}",
        f"- Missing GLIF files: {sum(len(check.missing_files) for check in checks)}",
        f"- Duplicate GLIF filenames: {sum(len(check.duplicate_files) for check in checks)}",
        "",
        "## Source UFOs",
        "",
        "| UFO | Loadable | Layers | Glyphs | GLIF read errors | Missing files | Duplicate filenames | Ready |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for check in checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{rel(check.path)}`",
                    "yes" if check.loadable else "no",
                    f"`{', '.join(check.layers)}`",
                    str(check.glyph_count),
                    str(len(check.glif_read_errors)),
                    str(len(check.missing_files)),
                    str(len(check.duplicate_files)),
                    "yes" if check.ready else "no",
                ]
            )
            + " |"
        )

    for check in checks:
        if not (check.glif_read_errors or check.missing_files or check.duplicate_files):
            continue
        lines.extend(["", f"## Issues In `{rel(check.path)}`", ""])
        for label, values in [
            ("GLIF read errors", check.glif_read_errors),
            ("Missing files", check.missing_files),
            ("Duplicate filenames", check.duplicate_files),
        ]:
            if not values:
                continue
            lines.extend([f"### {label}", ""])
            lines.extend(f"- `{value}`" for value in values)
            lines.append("")

    lines.extend(
        [
            "",
            "## Hand Cleanup Use",
            "",
            "Run this check before opening a manual cleanup session:",
            "",
        "```bash",
        "make ufo-editor-check",
        "```",
        "",
        "If Runebender specifically failed to load the UFO, run the optional",
        "Norad loader check against the same dependency build Runebender uses:",
        "",
        "```bash",
        "make runebender-ufo-check",
        "```",
        "",
        "Set `RUNEBENDER_REPO=/path/to/runebender-xilem` if the sibling repo",
        "is not at `/Users/eli/GH/repos/runebender-xilem`.",
        "",
        "If this report is not ready, fix the UFO package before drawing work.",
        "If it is ready but an editor still fails to open the source, compare",
        "the editor's loader error against this report and the Norad check to",
        "separate UFO syntax problems from editor-specific loader behavior.",
        "",
    ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
