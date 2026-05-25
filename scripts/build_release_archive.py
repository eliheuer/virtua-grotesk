#!/usr/bin/env python3
"""Build the local release/archive zip used for Google Fonts dry-run review."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_PATH = Path("documentation/google-fonts-downstream-package-preview.md")
OUTPUT_DEFAULT = Path("dist/VirtuaGrotesk-1.000.zip")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o644 << 16


def root_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def source_file_pairs_from_preview(preview_path: Path) -> list[tuple[str, str]]:
    text = root_path(preview_path).read_text(encoding="utf-8")
    return re.findall(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        text,
        flags=re.DOTALL,
    )


def unsafe_source_paths(paths: list[str]) -> list[str]:
    unsafe = []
    for path in paths:
        parts = Path(path).parts
        if Path(path).is_absolute() or ".." in parts:
            unsafe.append(path)
    return unsafe


def duplicate_paths(paths: list[str]) -> list[str]:
    seen = set()
    duplicates = []
    for path in paths:
        if path in seen and path not in duplicates:
            duplicates.append(path)
        seen.add(path)
    return duplicates


def validate_inputs(pairs: list[tuple[str, str]]) -> None:
    if not pairs:
        raise SystemExit("no source.files entries found in package preview")
    source_paths = [source for source, _ in pairs]
    dest_paths = [dest for _, dest in pairs]
    unsafe_sources = unsafe_source_paths(source_paths)
    if unsafe_sources:
        formatted = "\n".join(f"- {path}" for path in unsafe_sources)
        raise SystemExit(f"release archive inputs contain unsafe paths:\n{formatted}")
    duplicate_sources = duplicate_paths(source_paths)
    if duplicate_sources:
        formatted = "\n".join(f"- {path}" for path in duplicate_sources)
        raise SystemExit(f"release archive inputs contain duplicate source_file paths:\n{formatted}")
    unsafe_dests = unsafe_source_paths(dest_paths)
    if unsafe_dests:
        formatted = "\n".join(f"- {path}" for path in unsafe_dests)
        raise SystemExit(f"release archive inputs contain unsafe dest_file paths:\n{formatted}")
    duplicate_dests = duplicate_paths(dest_paths)
    if duplicate_dests:
        formatted = "\n".join(f"- {path}" for path in duplicate_dests)
        raise SystemExit(f"release archive inputs contain duplicate dest_file paths:\n{formatted}")
    missing = [path for path in source_paths if not (ROOT / path).is_file()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"release archive inputs are missing:\n{formatted}")


def build_archive(preview_path: Path, output_path: Path) -> None:
    source_pairs = source_file_pairs_from_preview(preview_path)
    validate_inputs(source_pairs)
    source_files = [source for source, _ in source_pairs]
    output = root_path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(source_files):
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = ZIP_FILE_MODE
            archive.writestr(info, (ROOT / relative).read_bytes())
    print(f"Wrote {output}")
    print("Included:")
    for relative in sorted(source_files):
        print(f"- {relative}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("legacy_output", nargs="?", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--preview", type=Path, default=PREVIEW_PATH)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv[1:])
    if args.legacy_output is not None and args.output is not None:
        raise SystemExit("use either positional output.zip or --output, not both")
    args.output = args.output or args.legacy_output or OUTPUT_DEFAULT
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    build_archive(args.preview, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
