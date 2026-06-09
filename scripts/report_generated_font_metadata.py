#!/usr/bin/env python3
"""Report generated font name, license, metric, and OS/2 metadata."""

from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont


DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]


def name(font: TTFont, name_id: int) -> str:
    record = font["name"].getName(name_id, 3, 1, 0x409)
    return record.toUnicode() if record else ""


def clean(value: str) -> str:
    return value.replace("|", "\\|")


def name_rows(font_paths: list[Path]) -> list[str]:
    rows = [
        "| Font | ID 1 family | ID 2 subfamily | ID 4 full name | ID 6 PostScript | ID 16 preferred family | ID 17 preferred subfamily |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for path in font_paths:
        font = TTFont(path)
        rows.append(
            "| `{}` | {} | {} | {} | `{}` | {} | {} |".format(
                path,
                clean(name(font, 1)),
                clean(name(font, 2)),
                clean(name(font, 4)),
                clean(name(font, 6)),
                clean(name(font, 16) or ""),
                clean(name(font, 17) or ""),
            )
        )
        font.close()
    return rows


def technical_rows(font_paths: list[Path]) -> list[str]:
    rows = [
        "| Font | Version | Weight | Width | fsType | Vendor ID | dlng | slng |",
        "| --- | --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for path in font_paths:
        font = TTFont(path)
        os2 = font["OS/2"]
        meta_data = font["meta"].data if "meta" in font else {}
        rows.append(
            "| `{}` | {} | {} | {} | {} | `{}` | `{}` | `{}` |".format(
                path,
                clean(name(font, 5)),
                os2.usWeightClass,
                os2.usWidthClass,
                os2.fsType,
                os2.achVendID,
                meta_data.get("dlng", ""),
                meta_data.get("slng", ""),
            )
        )
        font.close()
    return rows


def metric_rows(font_paths: list[Path]) -> list[str]:
    rows = [
        "| Font | OS/2 Typo asc/desc/gap | OS/2 Win asc/desc | hhea asc/desc/gap |",
        "| --- | --- | --- | --- |",
    ]
    for path in font_paths:
        font = TTFont(path)
        os2 = font["OS/2"]
        hhea = font["hhea"]
        rows.append(
            "| `{}` | {}/{}/{} | {}/{} | {}/{}/{} |".format(
                path,
                os2.sTypoAscender,
                os2.sTypoDescender,
                os2.sTypoLineGap,
                os2.usWinAscent,
                os2.usWinDescent,
                hhea.ascent,
                hhea.descent,
                hhea.lineGap,
            )
        )
        font.close()
    return rows


def license_rows(font_paths: list[Path]) -> list[str]:
    rows = [
        "| Font | Copyright/name ID 0 | License/name ID 13 | License URL/name ID 14 |",
        "| --- | --- | --- | --- |",
    ]
    for path in font_paths:
        font = TTFont(path)
        rows.append(
            "| `{}` | {} | {} | {} |".format(
                path,
                clean(name(font, 0)),
                clean(name(font, 13)),
                clean(name(font, 14)),
            )
        )
        font.close()
    return rows


def markdown_report(font_paths: list[Path]) -> str:
    lines = [
        "# Generated Font Metadata",
        "",
        (
            "This report records metadata from the built variable and static TTFs. "
            "It is generated from binaries after the post-build metadata patch, so "
            "it should match the files used for local QA and downstream packaging."
        ),
        "",
        "## Names",
        "",
        *name_rows(font_paths),
        "",
        "## Technical Metadata",
        "",
        *technical_rows(font_paths),
        "",
        "## Vertical Metrics",
        "",
        *metric_rows(font_paths),
        "",
        "## License Strings",
        "",
        *license_rows(font_paths),
        "",
        "## Review Notes",
        "",
        "- OS/2 `fsType` should be `0` for installable embedding.",
        "- `dlng` and `slng` should declare `Arab, Latn` while Arabic remains in first-submission scope.",
        "- Vendor ID should remain the maintainer-confirmed registered value `FTGD` for Font Garden.",
        "- Copyright/name ID 0 should match `OFL.txt` line 1.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = [Path(arg) for arg in argv[1:]]
    if not args:
        font_paths = DEFAULT_FONT_PATHS
        output_path = None
    elif len(args) == 1:
        font_paths = args
        output_path = None
    else:
        font_paths = args[:-1]
        output_path = args[-1]
    try:
        report = markdown_report(font_paths)
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
