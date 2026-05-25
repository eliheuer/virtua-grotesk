#!/usr/bin/env python3
"""Generate a family-name, RFN, namecheck, and CLA readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/family-name-readiness.md")
DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]


def read_lines(relative: str) -> list[str]:
    return (ROOT / relative).read_text(encoding="utf-8").splitlines()


def entries(relative: str) -> list[str]:
    return [
        line.strip()
        for line in read_lines(relative)
        if line.strip() and not line.lstrip().startswith("#")
    ]


def name_values(font_path: Path) -> dict[int, list[str]]:
    font = TTFont(ROOT / font_path)
    try:
        values: dict[int, list[str]] = {1: [], 2: [], 4: [], 6: [], 16: [], 17: []}
        for record in font["name"].names:
            if record.nameID in values:
                value = record.toUnicode()
                if value not in values[record.nameID]:
                    values[record.nameID].append(value)
        return values
    finally:
        font.close()


def family_names(font_paths: list[Path]) -> list[str]:
    names: set[str] = set()
    for font_path in font_paths:
        values = name_values(font_path)
        names.update(values[16] or values[1])
    return sorted(names)


def ofl_rfn_status() -> tuple[str, list[str]]:
    lines = read_lines("OFL.txt")
    rfn_lines = [
        line.strip()
        for line in lines[:12]
        if "reserved font name" in line.lower() and "terms" not in line.lower()
    ]
    second_line_blank = len(lines) > 1 and lines[1].strip() == ""
    if second_line_blank and not rfn_lines:
        return "none declared after copyright line", []
    return "review required", rfn_lines


def ascii_safe(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9 ]+", value))


def decision_status() -> str:
    text = (ROOT / "documentation/google-fonts-decisions.md").read_text(encoding="utf-8")
    match = re.search(r"## Family name, namecheck, trademarks, and CLA\s+Status: ([a-z]+)", text)
    return match.group(1) if match else "unknown"


def confirmation_status(family_decision_status: str) -> tuple[str, str, str]:
    if family_decision_status == "decided":
        return (
            "confirmed by maintainer at `namecheck.fontdata.com`",
            "confirmed by maintainer",
            "confirmed by maintainer for the copyright holder",
        )
    return (
        "pending maintainer check at `namecheck.fontdata.com`",
        "pending maintainer confirmation",
        "pending maintainer confirmation",
    )


def markdown_report(font_paths: list[Path]) -> str:
    authors = entries("AUTHORS.txt")
    contributors = entries("CONTRIBUTORS.txt")
    names = family_names(font_paths)
    rfn_status, rfn_lines = ofl_rfn_status()
    author_names = [entry.split("<", 1)[0].strip() for entry in authors]
    app_menu_candidate = "Virtua Grotesk"
    app_menu_present = app_menu_candidate in names
    author_in_name = any(author in name for author in author_names for name in names)
    family_decision_status = decision_status()
    namecheck_status, trademark_status, cla_status = confirmation_status(family_decision_status)
    namecheck_ready = family_decision_status == "decided"
    trademark_ready = family_decision_status == "decided"
    cla_ready = family_decision_status == "decided"

    lines = [
        "# Family Name Readiness",
        "",
        "This generated report tracks the Google Fonts family-name decision",
        "surface: app-menu naming, namecheck confirmation, Reserved Font Name",
        "status, and Google CLA readiness. It records objective local evidence",
        "separately from maintainer confirmations that cannot be inferred from",
        "the source tree.",
        "",
        "## Summary",
        "",
        f"- Family names from built fonts: `{', '.join(names)}`",
        f"- Family names are ASCII letters/digits/spaces only: {'yes' if all(ascii_safe(name) for name in names) else 'no'}",
        f"- Longest family name length: {max(len(name) for name in names) if names else 0}",
        f"- OFL Reserved Font Name status: {rfn_status}",
        f"- Namecheck confirmation: {namecheck_status}",
        f"- Trademark/catalog-name clearance: {trademark_status}",
        f"- Google CLA status: {cla_status}",
        f"- Decision log status: {family_decision_status}",
        "",
        "## Built Font Names",
        "",
        "| Font | nameID 1 | nameID 2 | nameID 4 | nameID 6 | nameID 16 | nameID 17 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for font_path in font_paths:
        values = name_values(font_path)
        cells = [
            "<br>".join(f"`{value}`" for value in values[name_id]) or "`unset`"
            for name_id in [1, 2, 4, 6, 16, 17]
        ]
        lines.append(f"| `{font_path}` | {' | '.join(cells)} |")

    lines.extend(
        [
            "",
            "## Authorship And App-Menu Name Check",
            "",
            f"- AUTHORS.txt entries: `{', '.join(authors)}`",
            f"- CONTRIBUTORS.txt entries: `{', '.join(contributors)}`",
            f"- Built family names include copyright-author full name: {'yes' if author_in_name else 'no'}",
            f"- Current definitive app-menu family name candidate: `{app_menu_candidate}`",
            f"- App-menu family name candidate appears in built names: {'yes' if app_menu_present else 'no'}",
            "",
            "## Add Font Name Requirements",
            "",
            "| Requirement | Current evidence | Status |",
            "| --- | --- | --- |",
            f"| Unique according to `namecheck.fontdata.com` | {namecheck_status} | {'ready' if namecheck_ready else 'pending'} |",
            f"| No Reserved Font Names in OFL or known upstream docs | {rfn_status} | {'ready' if rfn_status == 'none declared after copyright line' else 'review'} |",
            f"| Definitive app-menu family name | `{app_menu_candidate}` present in built names: {'yes' if app_menu_present else 'no'} | {'ready' if app_menu_present else 'review'} |",
            f"| App-menu name avoids copyright-holder full names/acronyms | built names include author full name: {'yes' if author_in_name else 'no'} | {'ready' if not author_in_name else 'review'} |",
            f"| Trademark/catalog-name clearance | {trademark_status} | {'ready' if trademark_ready else 'pending'} |",
            f"| Google CLA | {cla_status} | {'ready' if cla_ready else 'pending'} |",
            "",
            "## Reserved Font Name Evidence",
            "",
            f"- OFL line 2 is blank after the copyright line: {'yes' if len(read_lines('OFL.txt')) > 1 and read_lines('OFL.txt')[1].strip() == '' else 'no'}",
        ]
    )
    if rfn_lines:
        lines.extend(f"- Potential RFN line: `{line}`" for line in rfn_lines)
    else:
        lines.append("- No project-specific RFN declaration found immediately after the copyright line.")

    lines.extend(
        [
            "",
            "## Apply Before Final Submission",
            "",
            "- Keep the confirmed namecheck, trademark/RFN, and CLA statements in",
            "  `documentation/google-fonts-decisions.md` and the Google Fonts issue",
            "  text.",
            "- Confirm the local git name and email match the signed CLA identity",
            "  before opening the downstream pull request.",
            "- Rerun `make preflight` after any family-name metadata change.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[list[Path], Path]:
    args = [Path(arg) for arg in argv[1:]]
    if not args:
        return DEFAULT_FONT_PATHS, OUTPUT_DEFAULT
    if len(args) == 1:
        return DEFAULT_FONT_PATHS, args[0]
    return args[:-1], args[-1]


def main(argv: list[str]) -> int:
    font_paths, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(font_paths), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
