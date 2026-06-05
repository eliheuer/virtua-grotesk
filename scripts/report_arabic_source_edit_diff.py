#!/usr/bin/env python3
"""Report active source GLIF edits that may need paired master cleanup."""

from __future__ import annotations

from dataclasses import dataclass
import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-source-edit-diff.md"
MASTER_DIRS = {
    "Regular": ROOT / "sources/VirtuaGrotesk-Regular.ufo/glyphs",
    "Bold": ROOT / "sources/VirtuaGrotesk-Bold.ufo/glyphs",
}


@dataclass(frozen=True)
class StatusPath:
    status: str
    path: Path


def git_status_paths() -> list[StatusPath]:
    args = [
        "git",
        "status",
        "--porcelain",
        "--",
        *[str(path.relative_to(ROOT)) for path in MASTER_DIRS.values()],
    ]
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    rows: list[StatusPath] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        raw_path = line[3:]
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]
        path = ROOT / raw_path
        if path.suffix == ".glif":
            rows.append(StatusPath(status=status, path=path))
    return rows


def master_for_path(path: Path) -> str | None:
    for master, glyph_dir in MASTER_DIRS.items():
        try:
            path.relative_to(glyph_dir)
        except ValueError:
            continue
        return master
    return None


def glyph_file_for_path(path: Path) -> str:
    return path.name


def is_arabic_like(glyph_file: str) -> bool:
    lowered = glyph_file.lower()
    return (
        lowered.endswith("-ar.glif")
        or "arabic" in lowered
        or "farsi" in lowered
        or "persian" in lowered
    )


def markdown_report() -> str:
    rows, _arabic_like, _pairing_gaps, _ready = edit_state()
    return markdown_from_state(rows, _arabic_like, _pairing_gaps, _ready)


def edit_state() -> tuple[list[StatusPath], dict[str, dict[str, StatusPath]], list[str], bool]:
    rows = git_status_paths()
    grouped: dict[str, dict[str, StatusPath]] = {}
    for row in rows:
        master = master_for_path(row.path)
        if master is None:
            continue
        grouped.setdefault(glyph_file_for_path(row.path), {})[master] = row

    arabic_like = {
        glyph_file: masters
        for glyph_file, masters in grouped.items()
        if is_arabic_like(glyph_file)
    }
    pairing_gaps = [
        glyph_file
        for glyph_file, masters in arabic_like.items()
        if set(masters) != set(MASTER_DIRS)
    ]
    ready = not pairing_gaps
    return rows, arabic_like, pairing_gaps, ready


def markdown_from_state(
    rows: list[StatusPath],
    arabic_like: dict[str, dict[str, StatusPath]],
    pairing_gaps: list[str],
    ready: bool,
) -> str:
    lines = [
        "# Arabic Source Edit Diff",
        "",
        "This generated report checks current worktree GLIF edits in the",
        "active Regular and Bold source UFOs. Use it during hand drawing to",
        "catch one-sided Arabic edits before relying on interpolation or",
        "running the full after-drawing check.",
        "",
        "## Summary",
        "",
        f"- Changed active source GLIF files: {len(rows)}",
        f"- Changed Arabic-like GLIF names: {len(arabic_like)}",
        f"- Arabic-like Regular/Bold pairing gaps: {len(pairing_gaps)}",
        f"- Ready for paired-master review: {'yes' if ready else 'no'}",
        "",
    ]

    if not arabic_like:
        lines.extend(
            [
                "No Arabic-like source GLIF edits are currently visible in git status.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Arabic-Like GLIF Edits",
                "",
                "| Glyph file | Regular | Bold | Pairing |",
                "| --- | --- | --- | --- |",
            ]
        )
        for glyph_file in sorted(arabic_like):
            masters = arabic_like[glyph_file]
            regular = masters.get("Regular")
            bold = masters.get("Bold")
            pairing = "paired" if regular and bold else "one-sided"
            regular_text = f"`{regular.status.strip() or 'M'}`" if regular else "missing"
            bold_text = f"`{bold.status.strip() or 'M'}`" if bold else "missing"
            lines.append(f"| `{glyph_file}` | {regular_text} | {bold_text} | {pairing} |")
        lines.append("")

    lines.extend(
        [
            "## Use",
            "",
            "- If a row is `one-sided`, inspect whether the same structural edit",
            "  is needed in the other master before continuing.",
            "- This check does not replace `make arabic-after-drawing-check`; it is",
            "  a fast git-status guard for the middle of a drawing session.",
            "",
        ]
    )
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--fail-on-gap",
        action="store_true",
        help="Exit nonzero if any Arabic-like GLIF edit is one-sided.",
    )
    return parser


def main(argv: list[str]) -> int:
    args = parser().parse_args(argv[1:])
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    rows, arabic_like, pairing_gaps, ready = edit_state()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        markdown_from_state(rows, arabic_like, pairing_gaps, ready),
        encoding="utf-8",
    )
    print(output.relative_to(ROOT))
    if args.fail_on_gap and not ready:
        print(
            f"ERR Arabic-like Regular/Bold pairing gaps: {len(pairing_gaps)}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
