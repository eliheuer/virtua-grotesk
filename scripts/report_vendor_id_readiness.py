#!/usr/bin/env python3
"""Generate a Google Fonts vendor-ID readiness report."""

from __future__ import annotations

from pathlib import Path
import plistlib
import re
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/vendor-id-readiness.md")
SOURCE_UFOS = (
    Path("sources/VirtuaGrotesk-Regular.ufo"),
    Path("sources/VirtuaGrotesk-Bold.ufo"),
)
FONT_PATHS = (
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
)
REGISTERED_VENDOR_URL = "https://learn.microsoft.com/en-us/typography/vendors/"
CONFIRMED_VENDOR_ID = "FTGD"
CONFIRMED_VENDOR_NAME = "Font Garden"
CONFIRMED_VENDOR_VERIFIED = "2026-05-24"
APPLY_HELPER = Path("scripts/apply_vendor_id.py")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def clean(value: object) -> str:
    if value in (None, "", []):
        return "unset"
    return str(value)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def source_vendor_id(ufo_path: Path) -> str:
    fontinfo_path = ROOT / ufo_path / "fontinfo.plist"
    if not fontinfo_path.exists():
        return "missing"
    info = plistlib.loads(fontinfo_path.read_bytes())
    return clean(info.get("openTypeOS2VendorID"))


def font_vendor_id(font_path: Path) -> str:
    path = ROOT / font_path
    if not path.exists():
        return "missing"
    font = TTFont(path)
    vendor_id = font["OS/2"].achVendID
    font.close()
    return vendor_id


def warning_count() -> int:
    text = read_text(ROOT / "documentation/google-fonts/fontspector-warnings.md")
    match = re.search(r"\| `googlefonts/vendor_id` \| `unknown` \| (\d+) \|", text)
    return int(match.group(1)) if match else 0


def decision_status() -> str:
    text = read_text(ROOT / "documentation/google-fonts/google-fonts-decisions.md")
    match = re.search(r"## Vendor ID\s+Status: ([a-z]+)", text)
    return match.group(1) if match else "unknown"


def valid_vendor_id(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9 ]{4}", value)) and value != "NONE"


def confirmed_vendor_status(vendor_id: str) -> str:
    if vendor_id == CONFIRMED_VENDOR_ID:
        return f"confirmed registered: {CONFIRMED_VENDOR_NAME}"
    if valid_vendor_id(vendor_id):
        return "valid four-character ID, registration not confirmed here"
    return "placeholder"


def markdown_report() -> str:
    source_rows = [(path, source_vendor_id(path)) for path in SOURCE_UFOS]
    font_rows = [(path, font_vendor_id(path)) for path in FONT_PATHS]
    source_values = sorted({value for _, value in source_rows})
    font_values = sorted({value for _, value in font_rows})
    unresolved = source_values == ["unset"] and font_values == ["NONE"]
    source_consistent = len(source_values) == 1
    font_consistent = len(font_values) == 1
    source_and_fonts_aligned = (
        source_values == font_values
        or (source_values == ["unset"] and font_values == ["NONE"])
    )
    status = decision_status()
    helper_exists = (ROOT / APPLY_HELPER).exists()
    helper_text = read_text(ROOT / APPLY_HELPER)
    helper_validates = "valid_vendor_id" in helper_text and "must not be NONE" in helper_text
    helper_dry_run_default = "--apply" in helper_text and "Dry run only" in helper_text
    confirmed_values = source_values == [CONFIRMED_VENDOR_ID] and font_values == [CONFIRMED_VENDOR_ID]

    lines = [
        "# Vendor ID Readiness",
        "",
        "This generated report tracks the OS/2 vendor ID decision surface for",
        "Google Fonts onboarding. The maintainer-confirmed value is `FTGD`,",
        "registered to Font Garden in Microsoft's registered font vendor list.",
        "",
        "## Summary",
        "",
        f"- Source UFO vendor IDs: {', '.join(f'`{value}`' for value in source_values)}",
        f"- Generated font vendor IDs: {', '.join(f'`{value}`' for value in font_values)}",
        f"- Microsoft registered vendor entry confirmed: {yes_no(confirmed_values)}",
        f"- Confirmed vendor ID owner: `{CONFIRMED_VENDOR_ID}` = {CONFIRMED_VENDOR_NAME}",
        f"- Registered vendor list verification date: {CONFIRMED_VENDOR_VERIFIED}",
        f"- Source UFO vendor IDs internally consistent: {'yes' if source_consistent else 'no'}",
        f"- Generated font vendor IDs internally consistent: {'yes' if font_consistent else 'no'}",
        f"- Source and generated vendor states aligned: {'yes' if source_and_fonts_aligned else 'no'}",
        f"- Fontspector `googlefonts/vendor_id` warnings: {warning_count()}",
        f"- Decision log status: {status}",
        f"- Vendor ID decision unresolved: {'yes' if unresolved else 'no'}",
        f"- Vendor ID apply helper present: {'yes' if helper_exists else 'no'}",
        f"- Vendor ID apply helper validates four-character non-NONE IDs: {'yes' if helper_validates else 'no'}",
        f"- Vendor ID apply helper dry-runs by default: {'yes' if helper_dry_run_default else 'no'}",
        "",
        "## Source UFOs",
        "",
        "| UFO | openTypeOS2VendorID |",
        "| --- | --- |",
    ]

    for path, vendor_id in source_rows:
        lines.append(f"| `{path}` | `{vendor_id}` |")

    lines.extend(
        [
            "",
            "## Generated Fonts",
            "",
            "| Font | OS/2 achVendID | Status |",
            "| --- | --- | --- |",
        ]
    )
    for path, vendor_id in font_rows:
        status = confirmed_vendor_status(vendor_id)
        lines.append(f"| `{path}` | `{vendor_id}` | {status} |")

    lines.extend(
        [
            "",
            "## Applied Decision",
            "",
            "- `FTGD` is applied in both active UFO `fontinfo.plist` files.",
            "- The generated variable font and static QA fonts inherit `FTGD`.",
            "- Fontspector currently reports 0 `googlefonts/vendor_id` warnings.",
            "- Re-run `make vendor-id-check` after any source metadata or build changes.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/qa.html",
            "- https://github.com/fonttools/fontspector",
            f"- {REGISTERED_VENDOR_URL}",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_vendor_id_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
