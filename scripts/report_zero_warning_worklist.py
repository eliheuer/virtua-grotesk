#!/usr/bin/env python3
"""Report the concrete work needed to reach a zero-warning Fontspector run."""

from __future__ import annotations

from pathlib import Path
import math
import re
import sys
import unicodedata

from fontTools.ttLib import TTFont
from gfsubsets import CodepointsInSubset


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONT = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"
DEFAULT_OUTPUT = ROOT / "documentation/fontspector-zero-warning-worklist.md"
METADATA_PROBE = ROOT / "documentation/fontspector-metadata-warning-probe.md"
CONTOUR_DECISIONS = ROOT / "documentation/contour-cleanup-decision-log.md"
GF_GLYPHSET_REPORT = ROOT / "documentation/gf-glyphset-readiness.md"
SUBSET_THRESHOLDS = {
    "arabic": 50,
    "latin-ext": 20,
}
IGNORED_FOR_SUBSET_COVERAGE = {0x0000, 0x000D, 0x0020, 0x00A0}


def font_codepoints(font_path: Path) -> set[int]:
    font = TTFont(font_path)
    codepoints = set(font.getBestCmap() or {})
    font.close()
    return codepoints - IGNORED_FOR_SUBSET_COVERAGE


def codepoint_label(codepoint: int) -> str:
    try:
        name = unicodedata.name(chr(codepoint))
    except ValueError:
        name = "UNNAMED"
    return f"`U+{codepoint:04X} {name}`"


def threshold_required(total: int, threshold_percent: int) -> int:
    # Fontspector/gfsubsets uses a strict greater-than threshold comparison.
    return math.floor(total * threshold_percent / 100) + 1


def subset_row(subset: str, present_codepoints: set[int]) -> tuple[str, list[int]]:
    subset_codepoints = set(CodepointsInSubset(subset, unique_glyphs=True))
    present = sorted(subset_codepoints & present_codepoints)
    missing = sorted((subset_codepoints - present_codepoints) - IGNORED_FOR_SUBSET_COVERAGE)
    required = threshold_required(len(subset_codepoints), SUBSET_THRESHOLDS[subset])
    additional = max(0, required - len(present))
    coverage = 100 * len(present) / len(subset_codepoints)
    row = "| `{}` | {}% | {} | {} | {} | {:.2f}% | {} | {} |".format(
        subset,
        SUBSET_THRESHOLDS[subset],
        len(subset_codepoints),
        len(present),
        required,
        coverage,
        additional,
        "yes" if additional == 0 else "no",
    )
    return row, missing[: min(additional, 40)]


def contour_status_summary(text: str) -> str:
    counts = {
        label.lower(): int(value)
        for label, value in re.findall(r"^- ([A-Za-z-]+): (\d+)$", text, flags=re.MULTILINE)
    }
    unique = re.search(r"^- Unique review items: (\d+)$", text, flags=re.MULTILINE)
    return "; ".join(
        [
            f"unique review items: {unique.group(1) if unique else 'unknown'}",
            f"pending: {counts.get('pending', 0)}",
            f"fix-now: {counts.get('fix-now', 0)}",
            f"fixed: {counts.get('fixed', 0)}",
            f"accepted: {counts.get('accepted', 0)}",
            f"deferred: {counts.get('deferred', 0)}",
        ]
    )


def contour_unique_count(text: str) -> int | None:
    match = re.search(r"^- Unique review items: (\d+)$", text, flags=re.MULTILINE)
    return int(match.group(1)) if match else None


def metadata_probe_summary(text: str) -> str:
    baseline_rows = re.findall(
        r"^\| `([^`]+)` \| `([^`]+)` \| (\d+) \|$",
        text,
        flags=re.MULTILINE,
    )
    return ", ".join(f"`{check}`: {count}" for check, _, count in baseline_rows) or "none"


def metadata_probe_counts(text: str) -> dict[str, int]:
    baseline_rows = re.findall(
        r"^\| `([^`]+)` \| `([^`]+)` \| (\d+) \|$",
        text,
        flags=re.MULTILINE,
    )
    return {check: int(count) for check, _, count in baseline_rows}


def metadata_preview_subsets() -> tuple[str, ...]:
    preview = (ROOT / "documentation/google-fonts-downstream-package-preview.md").read_text(encoding="utf-8")
    match = re.search(
        r"## Expected METADATA\.pb shape\s*```text\n(?P<body>.*?)\n```",
        preview,
        flags=re.DOTALL,
    )
    body = match.group("body") if match else preview
    return tuple(re.findall(r'^subsets: "([^"]+)"$', body, flags=re.MULTILINE))


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_report(font_path: Path) -> str:
    present_codepoints = font_codepoints(font_path)
    metadata_text = METADATA_PROBE.read_text()
    contour_text = CONTOUR_DECISIONS.read_text()
    glyphset_text = GF_GLYPHSET_REPORT.read_text()
    preview_subsets = metadata_preview_subsets()

    subset_rows: list[str] = []
    missing_sections: list[str] = []
    for subset in SUBSET_THRESHOLDS:
        row, missing_sample = subset_row(subset, present_codepoints)
        subset_rows.append(row)
        missing_sections.extend([f"### `{subset}` Threshold Worklist Sample", ""])
        if missing_sample:
            missing_sections.extend(f"- {codepoint_label(codepoint)}" for codepoint in missing_sample)
            if len(missing_sample) == 40:
                missing_sections.append("- ... sample truncated; regenerate this report after choosing this expansion path.")
        else:
            missing_sections.append("- None")
        missing_sections.append("")

    latin_core_match = re.search(r"\| `GF_Latin_Core` \| Latin \| \d+ \| \d+ \| (\d+) \|", glyphset_text)
    arabic_core_match = re.search(r"\| `GF_Arabic_Core` \| Arabic \| \d+ \| \d+ \| (\d+) \|", glyphset_text)
    probe_counts = metadata_probe_counts(metadata_text)
    contour_package_warnings = probe_counts.get("contour_count", 0)
    contour_unique = contour_unique_count(contour_text)
    subset_warnings = probe_counts.get("googlefonts/metadata/subsets_correct", 0)
    reachability_warnings = probe_counts.get("googlefonts/metadata/unreachable_subsetting", 0)
    total_package_warnings = sum(probe_counts.values())
    zero_without_scope_change = (
        total_package_warnings == 0
        and (latin_core_match and latin_core_match.group(1) == "0")
        and (arabic_core_match and arabic_core_match.group(1) == "0")
    )
    true_zero_blockers: list[str] = []
    if latin_core_match and latin_core_match.group(1) != "0":
        true_zero_blockers.append(
            f"finish GF Latin Core coverage ({latin_core_match.group(1)} missing)"
        )
    if arabic_core_match and arabic_core_match.group(1) != "0":
        true_zero_blockers.append(
            f"finish GF Arabic Core coverage ({arabic_core_match.group(1)} missing)"
        )
    if subset_warnings:
        true_zero_blockers.append(
            "meet or revise the broad Google Fonts subset threshold for the intended subsets"
        )
    if reachability_warnings:
        true_zero_blockers.append(
            "resolve or get reviewer acceptance for required support codepoints that are not covered by serving subsets"
        )
    if contour_package_warnings:
        true_zero_blockers.append("clean up package-context contour-count warnings")
    active_threshold_subsets = [
        subset for subset in SUBSET_THRESHOLDS if subset in preview_subsets
    ]
    honest_minimum_lines = [
        f"The package-context probe currently bottoms out at {total_package_warnings} warnings",
        "without hiding intended script scope or removing shaping support:",
        "",
    ]
    if contour_package_warnings:
        honest_minimum_lines.extend(
            [
                f"- {contour_package_warnings} contour-count warning(s): require source drawing cleanup or",
                "  explicit reviewed acceptance.",
            ]
        )
    if subset_warnings:
        active_subset_label = "/".join(
            f"`{subset}`" for subset in (active_threshold_subsets or list(SUBSET_THRESHOLDS))
        )
        honest_minimum_lines.extend(
            [
                f"- {subset_warnings} subset-threshold warning(s): require broader {active_subset_label}",
                "  coverage, narrower final subset declarations, or reviewer",
                "  acceptance for the first-submission scope.",
            ]
        )
    if reachability_warnings:
        honest_minimum_lines.extend(
            [
                "- 1 reachability warning for U+0237, U+200F, U+20B9, and U+25CC:",
                "  do not strip these codepoints just to reduce warnings; the",
                "  metadata probe shows that removal or broad rescue subsets can",
                "  keep the warning floor unchanged or create worse warnings.",
            ]
        )
    if not contour_package_warnings:
        if contour_unique == 0:
            honest_minimum_lines.extend(
                [
                    "- Contour-count cleanup is currently closed in both package-context",
                    "  and loose-font QA reports.",
                ]
            )
        else:
            honest_minimum_lines.extend(
                [
                    "- Current variable-font package context has no `contour_count` warning,",
                    "  but loose-font static QA still has contour-count rows that need",
                    "  source cleanup or reviewed acceptance.",
                ]
            )

    latin_core_missing = latin_core_match.group(1) if latin_core_match else "unknown"
    arabic_core_missing = arabic_core_match.group(1) if arabic_core_match else "unknown"

    return "\n".join(
        [
            "# Fontspector Zero-Warning Worklist",
            "",
            f"Font: `{display_path(font_path)}`",
            "",
            "This generated report turns the remaining Fontspector warning floor into",
            "explicit drawing, coverage, metadata, and reviewer-decision work. It is",
            "not a recommendation to hide intended Arabic support.",
            "",
            "## Current Warning Floor",
            "",
            f"- Honest zero-warning state possible with current scope: {'yes' if zero_without_scope_change else 'no'}",
            f"- Package-context warning checks: {metadata_probe_summary(metadata_text)}",
            f"- Intended package subsets in preview: {', '.join(f'`{subset}`' for subset in preview_subsets) or 'none'}",
            f"- Contour decision state: {contour_status_summary(contour_text)}",
            f"- GF Latin Core missing codepoints: {latin_core_missing}",
            f"- GF Arabic Core missing codepoints: {arabic_core_missing}",
            "",
            "## Zero-Warning Verdict",
            "",
            (
                "True zero is possible with the current intended scope."
                if zero_without_scope_change
                else "True zero is not possible with the current intended scope without changing coverage, metadata scope, or reviewer policy."
            ),
            "",
            (
                "Blockers: "
                + ("; ".join(true_zero_blockers) if true_zero_blockers else "none")
                + "."
            ),
            "",
            "Do not spend the Arabic hand-review pass trying to force these warnings",
            "to zero by deleting U+200F, U+25CC, dotless forms, rupee support, or",
            "the intended `arabic` subset. Those experiments are tracked in the",
            "metadata probe and either preserve the warning floor, create worse",
            "Fontspector results, or misrepresent the first-submission scope.",
            "",
            "## Current Honest Minimum",
            "",
            *honest_minimum_lines,
            "",
            "## Subset Threshold Math",
            "",
            "Google Fonts `subsets_correct` warnings use broad serving subsets, not just",
            "`GF_Arabic_Core`. Passing the threshold by coverage alone would require:",
            "",
            "| Subset | Threshold | Subset codepoints | Present | Present needed | Coverage | Additional needed | Threshold met |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
            *subset_rows,
            "",
            "## Practical Zero-Warning Paths",
            "",
            "### Release-Scope Path",
            "",
            "This is the practical first-submission path when the intended scope remains",
            "`menu`, `latin`, and Arabic Core:",
            "",
            "1. Keep the loose-font `make test` WARN count in context: until a final",
            "   downstream `METADATA.pb` is packaged with the fonts, loose Fontspector",
            "   runs can repeat the same subset warning once per built font.",
            "2. Keep contour-count cleanup closed by rerunning the contour proof after",
            "   any source drawing changes.",
            f"3. Finish the {latin_core_missing} missing `GF_Latin_Core` codepoints so the current",
            "   `googlefonts/glyph_coverage` FAIL bucket can close.",
            "4. Finish Arabic visual review for the current Arabic Core drawings and",
            "   carry the package-context 2-WARN floor as review evidence.",
            "5. Ask Google Fonts review whether the intentional Arabic Core first",
            "   submission may keep `subsets: \"arabic\"` before the family reaches",
            "   broad `arabic` subset threshold coverage.",
            "",
            "### True Zero-Warning Path",
            "",
            "This is a larger coverage project, not a final-cleanup tweak:",
            "",
            f"1. Add at least the missing {latin_core_missing} `GF_Latin_Core` codepoints.",
            "2. Add enough broad `arabic` subset codepoints to pass the 50% threshold",
            "   shown above, or get a reviewer-approved narrower metadata path.",
            "3. Do not add `latin-ext` until the broad subset reaches the 20% threshold",
            "   shown above; otherwise it adds another `subsets_correct` warning.",
            "4. Resolve U+0237, U+200F, U+20B9, and U+25CC reachability in a way that",
            "   does not create replacement warnings. The current probe shows that",
            "   deleting or broad-rescuing them is worse than carrying the warning.",
            "",
            "## Fastest Honest Next Step",
            "",
            "For this project, the fastest honest path is to close the actual drawing",
            "and coverage blockers first: complete `GF_Latin_Core`, finish Arabic Core",
            "visual review, and keep the metadata probe current. Do not suppress the",
            "remaining package warnings by dropping `arabic` or removing required",
            "support codepoints unless a Google Fonts reviewer explicitly approves",
            "that narrower first-submission scope.",
            "",
            "## Missing Threshold Samples",
            "",
            *missing_sections,
        ]
    )


def main(argv: list[str]) -> int:
    font_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_FONT
    output_path = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(font_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
