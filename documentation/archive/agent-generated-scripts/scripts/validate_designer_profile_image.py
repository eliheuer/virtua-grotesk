#!/usr/bin/env python3
"""Validate a candidate Google Fonts designer profile image."""

from __future__ import annotations

from pathlib import Path
import struct
import sys


MIN_SIZE = 100
MAX_SIZE = 300
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or not header.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG file")
    return struct.unpack(">II", header[16:24])


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG file")
    index = 2
    while index < len(data):
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0x01, *range(0xD0, 0xD8), 0xD9}:
            continue
        if index + 2 > len(data):
            break
        segment_length = int.from_bytes(data[index : index + 2], "big")
        if segment_length < 2:
            break
        segment_start = index + 2
        segment_end = index + segment_length
        if marker in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            if segment_start + 5 > len(data):
                break
            height = int.from_bytes(data[segment_start + 1 : segment_start + 3], "big")
            width = int.from_bytes(data[segment_start + 3 : segment_start + 5], "big")
            return width, height
        index = segment_end
    raise ValueError("could not read JPEG dimensions")


def image_dimensions(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return png_dimensions(path)
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_dimensions(path)
    raise ValueError("image must be PNG or JPEG")


def validation_errors(path: Path, expected_file_name: str | None = None) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"image file does not exist: {path}"]
    if not path.is_file():
        return [f"image path is not a file: {path}"]
    if expected_file_name and path.name != expected_file_name:
        errors.append(
            f"image filename should be {expected_file_name}, got {path.name}"
        )
    if "/" in path.name or "\\" in path.name:
        errors.append("image filename should not include a directory path")
    if not path.name.isascii():
        errors.append("image filename should use ASCII characters")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        errors.append("image extension must be .png, .jpg, or .jpeg")
    try:
        width, height = image_dimensions(path)
    except ValueError as error:
        return [*errors, str(error)]
    if width != height:
        errors.append(f"image must be square, got {width}x{height}")
    if not (MIN_SIZE <= width <= MAX_SIZE and MIN_SIZE <= height <= MAX_SIZE):
        errors.append(f"image must be between {MIN_SIZE}px and {MAX_SIZE}px, got {width}x{height}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: validate_designer_profile_image.py path/to/profile-image.png [expected-file-name]")
        return 2
    path = Path(argv[1])
    expected_file_name = argv[2] if len(argv) == 3 else None
    errors = validation_errors(path, expected_file_name)
    print("# Designer Profile Image Check")
    print()
    print(f"Image: {path}")
    if expected_file_name:
        print(f"Expected filename: {expected_file_name}")
    print(f"Ready: {'no' if errors else 'yes'}")
    if errors:
        print()
        print("Blocking findings:")
        for error in errors:
            print(f"- {error}")
        return 2
    width, height = image_dimensions(path)
    print(f"Format: {path.suffix.lower().lstrip('.')}")
    print(f"Dimensions: {width}x{height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
