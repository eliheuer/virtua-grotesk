#!/usr/bin/env python3
"""Probe Fontspector metadata warnings with the downstream METADATA preview."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "documentation/google-fonts-downstream-package-preview.md"
VARIABLE_FONT = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"
LICENSE = ROOT / "OFL.txt"
OUTPUT_DEFAULT = ROOT / "documentation/fontspector-metadata-warning-probe.md"
PLACEHOLDER_COMMIT = "0123456789abcdef0123456789abcdef01234567"
PLACEHOLDER_DATE = "2026-05-25"
PROBE_CODEPOINTS = {
    "none": (),
    "remove U+0237 dotless j": (0x0237,),
    "remove U+20B9 rupee": (0x20B9,),
    "remove U+0237 + U+20B9": (0x0237, 0x20B9),
    "remove U+200F RLM": (0x200F,),
    "remove U+25CC dotted circle": (0x25CC,),
    "remove U+200F + U+25CC": (0x200F, 0x25CC),
    "remove all current unreachable": (0x0237, 0x20B9, 0x200F, 0x25CC),
}
SUBSET_PROBES = {
    "menu + latin only": ("menu", "latin"),
    "menu + latin + arabic": ("menu", "latin", "arabic"),
    "menu + latin-ext only": ("menu", "latin-ext"),
    "menu only": ("menu",),
}
REACHABILITY_SUBSET_PROBES = {
    "add symbols": ("arabic", "latin", "latin-ext", "menu", "symbols"),
    "add hebrew + symbols": ("arabic", "latin", "latin-ext", "menu", "hebrew", "symbols"),
    "remove latin-ext, add hebrew + symbols": ("menu", "latin", "arabic", "hebrew", "symbols"),
}


def extract_metadata_preview() -> str:
    text = PREVIEW.read_text(encoding="utf-8")
    match = re.search(
        r"## Expected METADATA\.pb shape\s*```text\n(?P<body>.*?)\n```",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find expected METADATA.pb preview block.")
    metadata = match.group("body")
    metadata = metadata.replace("Pending final Google Fonts date_added", PLACEHOLDER_DATE)
    metadata = metadata.replace("Pending final release/source commit", PLACEHOLDER_COMMIT)
    return metadata.strip() + "\n"


def fontspector_json(metadata: str, remove_codepoints: tuple[int, ...]) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        package_dir = Path(tmp) / "ofl" / "virtuagrotesk"
        package_dir.mkdir(parents=True)
        metadata_path = package_dir / "METADATA.pb"
        font_path = package_dir / VARIABLE_FONT.name
        report_path = Path(tmp) / "fontspector.json"

        metadata_path.write_text(metadata, encoding="utf-8")
        shutil.copy(LICENSE, package_dir / LICENSE.name)
        shutil.copy(VARIABLE_FONT, font_path)

        if remove_codepoints:
            font = TTFont(font_path)
            for table in font["cmap"].tables:
                for codepoint in remove_codepoints:
                    table.cmap.pop(codepoint, None)
            font.save(font_path)

        command = [
            "fontspector",
            "-p",
            "googlefonts",
            str(metadata_path),
            str(font_path),
            "--exclude-checkid",
            "googlefonts/repo/dirname_matches_nameid_1",
            "--json",
            str(report_path),
            "--loglevel",
            "error",
            "--skip-network",
        ]
        result = subprocess.run(
            command,
            check=False,
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError(f"Fontspector failed with exit code {result.returncode}.")
        return json.loads(report_path.read_text(encoding="utf-8"))


def records(data: dict, severities: set[str] | None = None) -> list[tuple[str, str, str, str]]:
    found: list[tuple[str, str, str, str]] = []
    for family_results in data["results"].values():
        for checks in family_results.values():
            for result in checks:
                check_id = result["check_id"]
                for subresult in result.get("subresults", []):
                    severity = subresult.get("severity", "")
                    if severities and severity not in severities:
                        continue
                    found.append(
                        (
                            severity,
                            check_id,
                            subresult.get("code", ""),
                            clean_message(subresult.get("message", "")),
                        )
                    )
    return found


def clean_message(message: str) -> str:
    return re.sub(r"\s+", " ", message).strip().replace("|", "\\|")


def warning_summary_rows(found: list[tuple[str, str, str, str]]) -> list[str]:
    counts = Counter((check_id, code) for severity, check_id, code, _ in found if severity == "WARN")
    rows = [
        "| Check | Code | Count |",
        "| --- | --- | ---: |",
    ]
    for (check_id, code), count in sorted(counts.items()):
        rows.append(f"| `{check_id}` | `{code}` | {count} |")
    return rows


def warning_rows(found: list[tuple[str, str, str, str]]) -> list[str]:
    rows = [
        "| Severity | Check | Code | Message |",
        "| --- | --- | --- | --- |",
    ]
    for severity, check_id, code, message in found:
        if severity != "WARN":
            continue
        rows.append(f"| {severity} | `{check_id}` | `{code}` | {message} |")
    return rows


def removal_probe_rows(metadata: str) -> list[str]:
    rows = [
        "| Temporary cmap change | WARN count | Warning checks | Notes |",
        "| --- | ---: | --- | --- |",
    ]
    for label, codepoints in PROBE_CODEPOINTS.items():
        data = fontspector_json(metadata, codepoints)
        found = records(data, {"WARN"})
        warn_checks = Counter(check_id for _, check_id, _, _ in found)
        warning_checks = "<br>".join(f"`{check}`: {count}" for check, count in sorted(warn_checks.items()))
        notes: list[str] = []
        if any(check == "dotted_circle" for _, check, _, _ in found):
            notes.append("triggers missing dotted circle")
        if any(check == "rupee" for _, check, _, _ in found):
            notes.append("triggers missing rupee")
        if any(check == "googlefonts/glyphsets/shape_languages" for _, check, _, _ in found):
            notes.append("triggers Arabic shaping-language warning")
        if any(check == "unreachable_glyphs" for _, check, _, _ in found):
            notes.append("creates unreachable glyph warning")
        rows.append(
            "| {} | {} | {} | {} |".format(
                label,
                len(found),
                warning_checks or "none",
                "; ".join(notes) if notes else "baseline",
            )
        )
    return rows


def metadata_with_subsets(metadata: str, subsets: tuple[str, ...]) -> str:
    metadata = re.sub(r'subsets: "[^"]+"\n', "", metadata)
    subset_block = "".join(f'subsets: "{subset}"\n' for subset in subsets)
    return metadata.replace("axes {\n", f"{subset_block}axes {{\n")


def extract_subsets(metadata: str) -> tuple[str, ...]:
    return tuple(re.findall(r'^subsets: "([^"]+)"$', metadata, flags=re.MULTILINE))


def subset_probe_rows(metadata: str) -> list[str]:
    rows = [
        "| Subset variant | WARN count | Warning checks | Unreachable sample | Notes |",
        "| --- | ---: | --- | --- | --- |",
    ]
    probes = {"current preview": extract_subsets(metadata), **SUBSET_PROBES}
    for label, subsets in probes.items():
        data = fontspector_json(metadata_with_subsets(metadata, subsets), ())
        found = records(data, {"WARN"})
        warn_checks = Counter(check_id for _, check_id, _, _ in found)
        warning_checks = "<br>".join(f"`{check}`: {count}" for check, count in sorted(warn_checks.items()))
        unreachable = unreachable_codepoints(found)
        unreachable_sample = "<br>".join(f"`{codepoint}`" for codepoint in unreachable[:6])
        if len(unreachable) > 6:
            unreachable_sample += f"<br>... and {len(unreachable) - 6} others"
        notes: list[str] = []
        if "arabic" not in subsets:
            notes.append("drops intended Arabic serving subset")
        if "latin" not in subsets:
            notes.append("drops required Latin serving subset")
        if any(check == "googlefonts/metadata/subsets_correct" for _, check, _, _ in found):
            notes.append("subset threshold warning remains")
        rows.append(
            "| {} | {} | {} | {} | {} |".format(
                label,
                len(found),
                warning_checks or "none",
                unreachable_sample or "none",
                "; ".join(notes) if notes else "baseline intended scope",
            )
        )
    return rows


def reachability_subset_probe_rows(metadata: str) -> list[str]:
    rows = [
        "| Subset variant | WARN count | Warning checks | Unreachable sample | Notes |",
        "| --- | ---: | --- | --- | --- |",
    ]
    probes = {"current preview": extract_subsets(metadata), **REACHABILITY_SUBSET_PROBES}
    for label, subsets in probes.items():
        data = fontspector_json(metadata_with_subsets(metadata, subsets), ())
        found = records(data, {"WARN"})
        warn_checks = Counter(check_id for _, check_id, _, _ in found)
        warning_checks = "<br>".join(f"`{check}`: {count}" for check, count in sorted(warn_checks.items()))
        unreachable = unreachable_codepoints(found)
        unreachable_sample = "<br>".join(f"`{codepoint}`" for codepoint in unreachable[:6])
        if len(unreachable) > 6:
            unreachable_sample += f"<br>... and {len(unreachable) - 6} others"
        notes: list[str] = []
        if "symbols" in subsets:
            notes.append("attempts to cover U+25CC")
        if "hebrew" in subsets:
            notes.append("attempts to cover U+200F")
        if any(check == "googlefonts/metadata/subsets_correct" for _, check, _, _ in found):
            notes.append("adds or keeps unsupported-subset warnings")
        rows.append(
            "| {} | {} | {} | {} | {} |".format(
                label,
                len(found),
                warning_checks or "none",
                unreachable_sample or "none",
                "; ".join(notes) if notes else "baseline",
            )
        )
    return rows


def unreachable_codepoints(found: list[tuple[str, str, str, str]]) -> list[str]:
    codepoints: set[str] = set()
    for _, check_id, _, message in found:
        if check_id != "googlefonts/metadata/unreachable_subsetting":
            continue
        codepoints.update(re.findall(r"U\+[0-9A-F]{4,6} [A-Z0-9 -]+", message))
    return sorted(codepoints)


def markdown_report() -> str:
    metadata = extract_metadata_preview()
    baseline = records(fontspector_json(metadata, ()), {"WARN"})
    codepoints = unreachable_codepoints(baseline)
    lines = [
        "# Fontspector Metadata Warning Probe",
        "",
        "This report runs Fontspector against a temporary Google Fonts-style",
        "package containing the built variable font and the downstream",
        "`METADATA.pb` preview from",
        "`documentation/google-fonts-downstream-package-preview.md`.",
        "",
        "It exists to separate loose-font warning noise from warnings that remain",
        "after the intended package metadata is visible to Fontspector. The",
        "temporary metadata replaces pending date and commit placeholders only",
        "for this local probe.",
        "",
        "## Baseline With Preview Metadata",
        "",
        *warning_summary_rows(baseline),
        "",
        "## Remaining Unreachable Codepoints",
        "",
    ]
    if codepoints:
        lines.extend(f"- `{codepoint}`" for codepoint in codepoints)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Cmap Removal Probe",
            "",
            "These rows are temporary binary probes only. They do not edit sources",
            "or built fonts. A warning count increase here means the codepoint",
            "should not be stripped just to reduce `unreachable_subsetting`.",
            "",
            *removal_probe_rows(metadata),
            "",
            "## Subset Variant Probe",
            "",
            "These rows test temporary `METADATA.pb` subset changes only. A lower",
            "warning count is not useful when it removes the intended Google Fonts",
            "serving scope for the first submission.",
            "",
            *subset_probe_rows(metadata),
            "",
            "## Reachability Rescue Probe",
            "",
            "These rows test whether adding broad subsets just to cover U+200F or",
            "U+25CC can honestly reduce the warning floor. In the current font,",
            "that route increases unsupported-subset warnings instead of producing",
            "a cleaner Google Fonts profile.",
            "",
            *reachability_subset_probe_rows(metadata),
            "",
            "## Full Baseline Warning Messages",
            "",
            *warning_rows(baseline),
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output_path = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    try:
        report = markdown_report()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
