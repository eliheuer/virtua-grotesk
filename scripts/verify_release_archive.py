#!/usr/bin/env python3
"""Verify the local release/archive zip against downstream source.files."""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_DEFAULT = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")
ARCHIVE_DEFAULT = Path("dist/VirtuaGrotesk-1.000.zip")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o644 << 16


def source_file_pairs_from_preview(path: Path) -> list[tuple[str, str]]:
    text = (ROOT / path).read_text(encoding="utf-8")
    return re.findall(
        r'files\s*\{\s*source_file:\s*"([^"]+)"\s*dest_file:\s*"([^"]+)"\s*\}',
        text,
        flags=re.DOTALL,
    )


def unsafe_paths(paths: list[str]) -> list[str]:
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def archive_hashes(path: Path) -> dict[str, tuple[int, str]]:
    entries: dict[str, tuple[int, str]] = {}
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            digest = hashlib.sha256(archive.read(info.filename)).hexdigest()
            entries[info.filename] = (info.file_size, digest)
    return entries


def archive_metadata_errors(path: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if info.date_time != ZIP_TIMESTAMP:
                errors.append(f"archive entry has nondeterministic timestamp: {info.filename}")
            if info.external_attr != ZIP_FILE_MODE:
                errors.append(f"archive entry has nondeterministic file mode: {info.filename}")
    return errors


def verification_errors(preview: Path, archive: Path) -> list[str]:
    errors: list[str] = []
    pairs = source_file_pairs_from_preview(preview)
    if not pairs:
        errors.append(f"no source.files entries found in {preview}")
        return errors
    expected = [source for source, _ in pairs]
    dest_paths = [dest for _, dest in pairs]
    errors.extend(f"unsafe source.files path: {path}" for path in unsafe_paths(expected))
    errors.extend(f"duplicate source.files path: {path}" for path in duplicate_paths(expected))
    errors.extend(f"unsafe source.files dest_file path: {path}" for path in unsafe_paths(dest_paths))
    errors.extend(f"duplicate source.files dest_file path: {path}" for path in duplicate_paths(dest_paths))
    if errors:
        return errors
    missing_local = [path for path in expected if not (ROOT / path).is_file()]
    errors.extend(f"missing local source file: {path}" for path in missing_local)
    archive_path = ROOT / archive
    if not archive_path.is_file():
        errors.append(f"local release archive is missing: {archive}")
        return errors
    try:
        entries = archive_hashes(archive_path)
        errors.extend(archive_metadata_errors(archive_path))
    except zipfile.BadZipFile:
        errors.append(f"local release archive is not a valid zip: {archive}")
        return errors

    expected_set = set(expected)
    entry_set = set(entries)
    for path in sorted(unsafe_paths(list(entry_set))):
        errors.append(f"archive contains unsafe path: {path}")
    for path in sorted(expected_set - entry_set):
        errors.append(f"archive is missing expected file: {path}")
    for path in sorted(entry_set - expected_set):
        errors.append(f"archive contains unexpected file: {path}")
    for path in expected:
        local_path = ROOT / path
        if path not in entries or not local_path.is_file():
            continue
        archive_size, archive_digest = entries[path]
        local_size = local_path.stat().st_size
        local_digest = sha256(local_path)
        if archive_size != local_size:
            errors.append(f"archive size mismatch for {path}: {archive_size} != {local_size}")
        if archive_digest != local_digest:
            errors.append(f"archive hash mismatch for {path}")
    return errors


def expected_sha_errors(archive: Path, expected_sha256: str | None) -> list[str]:
    if not expected_sha256:
        return []
    archive_path = ROOT / archive if not archive.is_absolute() else archive
    if not archive_path.is_file():
        return []
    digest = sha256(archive_path)
    if digest != expected_sha256:
        return [
            f"archive SHA-256 mismatch: {digest} != {expected_sha256}",
        ]
    return []


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, default=PREVIEW_DEFAULT)
    parser.add_argument("--archive", type=Path, default=ARCHIVE_DEFAULT)
    parser.add_argument("--expected-sha256", default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    errors = verification_errors(args.preview, args.archive)
    errors.extend(expected_sha_errors(args.archive, args.expected_sha256))
    if errors:
        if not args.quiet:
            print("Release archive verification failed:")
            for error in errors:
                print(f"- {error}")
            print()
            print("Run `make release-archive-build` after rebuilding fonts or changing package files.")
        return 2
    if not args.quiet:
        print(f"Release archive verified: {args.archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
