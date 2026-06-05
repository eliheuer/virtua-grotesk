#!/usr/bin/env python3
"""Report source UFO metadata relevant to Google Fonts onboarding."""

from __future__ import annotations

from pathlib import Path
import plistlib
import sys


DEFAULT_UFO_PATHS = [
    Path("sources/VirtuaGrotesk-Regular.ufo"),
    Path("sources/VirtuaGrotesk-Bold.ufo"),
]


def load_plist(path: Path) -> dict:
    return plistlib.loads(path.read_bytes())


def clean(value) -> str:
    return str(value if value is not None else "").replace("|", "\\|")


def summary_rows(ufo_paths: list[Path]) -> list[str]:
    rows = [
        "| UFO | Family | Style | Version | Glyphs | features.fea |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for ufo_path in ufo_paths:
        info = load_plist(ufo_path / "fontinfo.plist")
        contents = load_plist(ufo_path / "glyphs" / "contents.plist")
        rows.append(
            "| `{}` | {} | {} | {}.{} | {} | {} |".format(
                ufo_path,
                clean(info.get("familyName")),
                clean(info.get("styleName")),
                info.get("versionMajor", ""),
                info.get("versionMinor", ""),
                len(contents),
                "yes" if (ufo_path / "features.fea").exists() else "no",
            )
        )
    return rows


def metric_rows(ufo_paths: list[Path]) -> list[str]:
    rows = [
        "| UFO | UPM | Ascender | Descender | x-height | Cap height | Typo asc/desc/gap | Win asc/desc | hhea asc/desc/gap |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for ufo_path in ufo_paths:
        info = load_plist(ufo_path / "fontinfo.plist")
        rows.append(
            "| `{}` | {} | {} | {} | {} | {} | {}/{}/{} | {}/{} | {}/{}/{} |".format(
                ufo_path,
                info.get("unitsPerEm", ""),
                info.get("ascender", ""),
                info.get("descender", ""),
                info.get("xHeight", ""),
                info.get("capHeight", ""),
                info.get("openTypeOS2TypoAscender", ""),
                info.get("openTypeOS2TypoDescender", ""),
                info.get("openTypeOS2TypoLineGap", ""),
                info.get("openTypeOS2WinAscent", ""),
                info.get("openTypeOS2WinDescent", ""),
                info.get("openTypeHheaAscender", ""),
                info.get("openTypeHheaDescender", ""),
                info.get("openTypeHheaLineGap", ""),
            )
        )
    return rows


def license_rows(ufo_paths: list[Path]) -> list[str]:
    rows = [
        "| UFO | Copyright | License | License URL | Manufacturer URL | OS/2 fsType source | Vendor ID |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for ufo_path in ufo_paths:
        info = load_plist(ufo_path / "fontinfo.plist")
        rows.append(
            "| `{}` | {} | {} | {} | {} | {} | {} |".format(
                ufo_path,
                clean(info.get("openTypeNameCopyright") or info.get("copyright")),
                clean(info.get("openTypeNameLicense")),
                clean(info.get("openTypeNameLicenseURL")),
                clean(info.get("openTypeNameManufacturerURL")),
                "unset" if "openTypeOS2Type" not in info else clean(info.get("openTypeOS2Type")),
                clean(info.get("openTypeOS2VendorID") or "unset"),
            )
        )
    return rows


def markdown_report(ufo_paths: list[Path]) -> str:
    lines = [
        "# Source UFO Metadata",
        "",
        (
            "This report records Google Fonts-facing metadata from the active UFO "
            "sources. Use it with `documentation/google-fonts/generated-font-metadata.md` to "
            "confirm that source metadata and built binary metadata stay aligned."
        ),
        "",
        "## Summary",
        "",
        *summary_rows(ufo_paths),
        "",
        "## Metrics",
        "",
        *metric_rows(ufo_paths),
        "",
        "## License and Embedding",
        "",
        *license_rows(ufo_paths),
        "",
        "## Review Notes",
        "",
        "- `openTypeOS2Type` should remain unset so generated fonts are installable.",
        "- Vendor ID should remain the maintainer-confirmed registered value `FTGD` for Font Garden.",
        "- Copyright should match `OFL.txt` line 1 and generated name ID 0.",
        "- Source metrics should match the generated vertical metrics report.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = [Path(arg) for arg in argv[1:]]
    if not args:
        ufo_paths = DEFAULT_UFO_PATHS
        output_path = None
    elif len(args) == 1:
        ufo_paths = args
        output_path = None
    else:
        ufo_paths = args[:-1]
        output_path = args[-1]
    try:
        report = markdown_report(ufo_paths)
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
