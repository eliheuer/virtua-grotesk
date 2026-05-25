#!/usr/bin/env python3
"""Dry-run or apply a maintainer-approved OpenType vendor ID."""

from __future__ import annotations

from pathlib import Path
import argparse
import plistlib
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FONTINFO = [
    Path("sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist"),
    Path("sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist"),
]


def valid_vendor_id(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9 ]{4}", value)) and value != "NONE"


def read_plist(path: Path) -> dict[str, object]:
    return plistlib.loads(path.read_bytes())


def write_plist(path: Path, data: dict[str, object]) -> None:
    path.write_bytes(plistlib.dumps(data, sort_keys=False))


def current_vendor_id(path: Path) -> str:
    data = read_plist(path)
    value = data.get("openTypeOS2VendorID")
    return str(value) if value not in (None, "") else "unset"


def planned_changes(vendor_id: str) -> list[tuple[Path, str, str]]:
    changes = []
    for relative in SOURCE_FONTINFO:
        path = ROOT / relative
        changes.append((relative, current_vendor_id(path), vendor_id))
    return changes


def apply_changes(vendor_id: str) -> None:
    for relative in SOURCE_FONTINFO:
        path = ROOT / relative
        data = read_plist(path)
        data["openTypeOS2VendorID"] = vendor_id
        write_plist(path, data)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vendor_id", help="four-character registered vendor ID")
    parser.add_argument("--apply", action="store_true", help="write source UFO fontinfo.plist changes")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    vendor_id = args.vendor_id
    if not valid_vendor_id(vendor_id):
        print("ERR vendor ID must be four ASCII letters/digits/spaces and must not be NONE")
        return 2

    print(f"Mode: {'apply' if args.apply else 'dry-run'}")
    print(f"Vendor ID: {vendor_id!r}")
    print("")
    print("| File | Current | New |")
    print("| --- | --- | --- |")
    for relative, current, new in planned_changes(vendor_id):
        print(f"| `{relative}` | `{current}` | `{new}` |")

    if not args.apply:
        print("")
        print("Dry run only. Re-run with --apply after the maintainer confirms this registered vendor ID.")
        return 0

    apply_changes(vendor_id)
    print("")
    print("Applied vendor ID to active source UFO fontinfo.plist files.")
    print("Run `make preflight` to rebuild fonts and verify generated OS/2 achVendID values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
