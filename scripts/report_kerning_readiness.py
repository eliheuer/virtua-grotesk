#!/usr/bin/env python3
"""Generate a Google Fonts kerning readiness report."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import json

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/kerning-readiness.md")
GFT_QA_OUTPUT = Path("documentation/google-fonts/gftools-qa/Proof")
GF_TESTING_GUIDE = "https://googlefonts.github.io/gf-guide/testing.html"
GF_TOOLS_GUIDE = "https://googlefonts.github.io/gf-guide/tools.html"
GF_ONBOARDER_WORKFLOW = "https://googlefonts.github.io/gf-guide/onboarder-workflow.html"
DEFAULT_FONT_PATHS = [
    Path("fonts/variable/VirtuaGrotesk[wght].ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    Path("fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
SOURCE_UFOS = [
    Path("sources/VirtuaGrotesk-Regular.ufo"),
    Path("sources/VirtuaGrotesk-Bold.ufo"),
]


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def pair_count(kerning: dict[str, dict[str, int]]) -> int:
    return sum(len(rights) for rights in kerning.values())


def group_count(groups: dict[str, list[str]], prefix: str) -> int:
    return sum(1 for name in groups if name.startswith(prefix))


def source_kerning_summary(ufo_path: Path) -> dict[str, int | str]:
    kerning_path = ROOT / ufo_path / "kerning.plist"
    groups_path = ROOT / ufo_path / "groups.plist"
    kerning: dict[str, dict[str, int]] = {}
    groups: dict[str, list[str]] = {}
    if kerning_path.exists():
        with kerning_path.open("rb") as file:
            kerning = plistlib.load(file)
    if groups_path.exists():
        with groups_path.open("rb") as file:
            groups = plistlib.load(file)
    return {
        "ufo": str(ufo_path),
        "kerning_file": "yes" if kerning_path.exists() else "no",
        "pair_count": pair_count(kerning),
        "left_groups": group_count(groups, "public.kern1."),
        "right_groups": group_count(groups, "public.kern2."),
    }


def font_kerning_summary(font_path: Path) -> dict[str, str]:
    font = TTFont(ROOT / font_path)
    try:
        has_kern_table = "kern" in font
        gpos_features: set[str] = set()
        if "GPOS" in font:
            feature_list = font["GPOS"].table.FeatureList
            if feature_list:
                gpos_features = {record.FeatureTag for record in feature_list.FeatureRecord}
        return {
            "font": str(font_path),
            "kern_table": "yes" if has_kern_table else "no",
            "gpos_kern": "yes" if "kern" in gpos_features else "no",
            "gpos_features": ", ".join(sorted(gpos_features)) or "none",
        }
    finally:
        font.close()


def warning_count(font_paths: list[Path]) -> int:
    if shutil.which("fontspector") is not None:
        with tempfile.NamedTemporaryFile(suffix=".json") as report:
            result = subprocess.run(
                [
                    "fontspector",
                    "-p",
                    "googlefonts",
                    *[str(ROOT / path) for path in font_paths],
                    "--exclude-checkid",
                    "googlefonts/repo/dirname_matches_nameid_1",
                    "--checkid",
                    "gpos_kerning_info",
                    "--json",
                    report.name,
                    "--loglevel",
                    "error",
                    "--skip-network",
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if result.returncode in (0, 1):
                data = json.loads(Path(report.name).read_text())
                count = 0
                for family_results in data["results"].values():
                    for checks in family_results.values():
                        for check in checks:
                            if check.get("check_id") != "gpos_kerning_info":
                                continue
                            count += sum(
                                1
                                for subresult in check.get("subresults", [])
                                if subresult.get("severity") == "WARN"
                            )
                return count

    text = read_text("documentation/google-fonts/fontspector-warnings.md")
    match = re.search(r"\| `gpos_kerning_info` \| (\d+) \|", text)
    return int(match.group(1)) if match else 0


def decision_status() -> str:
    text = read_text("documentation/google-fonts/google-fonts-decisions.md")
    match = re.search(r"## Kerning\s*\n\nStatus: ([^\n]+)", text)
    return match.group(1).strip() if match else "unknown"


def command_exists(path: Path) -> bool:
    return (ROOT / path).exists()


def qa_dependency_status() -> dict[str, str]:
    diffenator2_available = importlib.util.find_spec("diffenator2") is not None
    diff3proof_available = importlib.util.find_spec("diff3proof") is not None
    proof_html_count = len(list((ROOT / GFT_QA_OUTPUT).glob("*.html")))
    expected_instances = ["Regular", "Medium", "SemiBold", "Bold"]
    proof_instances = {
        html.name.split("-diffbrowsers_", 1)[0]
        for html in (ROOT / GFT_QA_OUTPUT).glob("*-diffbrowsers_proofer.html")
    }
    return {
        "gftools": "yes" if command_exists(Path("venv/bin/gftools")) else "no",
        "diffenator2": "yes" if diffenator2_available else "no",
        "diff3proof": "yes" if diff3proof_available else "no",
        "qa_importable": "yes" if diffenator2_available else "no",
        "proof_output": "yes" if proof_html_count else "no",
        "proof_html_count": str(proof_html_count),
        "proof_instances": "yes" if all(instance in proof_instances for instance in expected_instances) else "no",
    }


def markdown_report(font_paths: list[Path]) -> str:
    source_rows = [source_kerning_summary(ufo) for ufo in SOURCE_UFOS]
    font_rows = [font_kerning_summary(font_path) for font_path in font_paths]
    qa_status = qa_dependency_status()
    any_source_pairs = any(int(row["pair_count"]) for row in source_rows)
    all_masters_have_pairs = all(int(row["pair_count"]) for row in source_rows)
    all_built_gpos_kern = all(row["gpos_kern"] == "yes" for row in font_rows)
    static_rows = [row for row in font_rows if "/ttf/" in row["font"]]
    all_static_gpos_kern = all(row["gpos_kern"] == "yes" for row in static_rows)

    lines = [
        "# Kerning Readiness",
        "",
        "This generated report tracks the current Google Fonts kerning decision",
        "surface. It records source kerning, generated font kerning tables, and",
        "the Fontspector warning without changing spacing or drawing data.",
        "",
        "## Summary",
        "",
        f"- Source kerning exists in at least one master: {'yes' if any_source_pairs else 'no'}",
        f"- Source kerning exists in every master: {'yes' if all_masters_have_pairs else 'no'}",
        f"- All built fonts expose GPOS `kern`: {'yes' if all_built_gpos_kern else 'no'}",
        f"- All built static fonts expose GPOS `kern`: {'yes' if all_static_gpos_kern else 'no'}",
        f"- Fontspector `gpos_kerning_info` warnings: {warning_count(font_paths)}",
        f"- `gftools qa --proof` importable: {qa_status['qa_importable']}",
        f"- Latest `gftools qa --proof` HTML output present: {qa_status['proof_output']}",
        f"- Latest proof HTML file count: {qa_status['proof_html_count']}",
        f"- Latest proof covers expected instances: {qa_status['proof_instances']}",
        f"- Decision status: {decision_status()}",
        "",
        "## Source UFO Kerning",
        "",
        "| UFO | kerning.plist | Pair count | Left groups | Right groups |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in source_rows:
        lines.append(
            f"| `{row['ufo']}` | {row['kerning_file']} | {row['pair_count']} | "
            f"{row['left_groups']} | {row['right_groups']} |"
        )

    lines.extend(
        [
            "",
            "## Built Font Kerning",
            "",
            "| Font | `kern` table | GPOS `kern` feature | GPOS features |",
            "| --- | --- | --- | --- |",
        ]
    )

    for row in font_rows:
        lines.append(
            f"| `{row['font']}` | {row['kern_table']} | {row['gpos_kern']} | `{row['gpos_features']}` |"
        )

    lines.extend(
        [
            "",
            "## Google Fonts Visual QA",
            "",
        "This is part of the core QA process for Virtua Grotesk. Google Fonts",
        "documentation separates automated checks from visual QA: the local",
        "testing guide calls for checking kerning in local applications, and",
        "the onboarder workflow says new-font QA includes proof review for",
        "basic spacing and kerning. In current gftools this proof path is",
        "exposed through `gftools qa --proof`.",
            "",
            "| Tool or dependency | Ready |",
            "| --- | --- |",
            f"| `venv/bin/gftools` | {qa_status['gftools']} |",
            f"| `diffenator2` Python package | {qa_status['diffenator2']} |",
            f"| `diff3proof` Python package | {qa_status['diff3proof']} |",
            f"| `gftools qa` importable | {qa_status['qa_importable']} |",
            f"| Proof HTML files in `{GFT_QA_OUTPUT}` | {qa_status['proof_output']} ({qa_status['proof_html_count']}) |",
            f"| Proof covers Regular, Medium, SemiBold, Bold | {qa_status['proof_instances']} |",
            "",
            "Core proof command:",
            "",
            "```bash",
            "make kerning-proof-check",
            "```",
            "",
            "The Make target runs `gftools qa --proof` with `venv/bin` on `PATH`",
            "so the Diffenator helper scripts installed by `gftools[qa]` can be",
            "found by the generated Ninja proof steps.",
            "",
            "`gftools qa --proof` also checks the live Google Fonts catalog at",
            "`https://fonts.google.com/metadata/fonts` before rendering proofs.",
            "Run it with network access available, or expect a DNS/connection",
            "failure before any HTML proof files are refreshed.",
            "",
            "Review the generated HTML before treating kerning, spacing, or a",
            "kerning-deferral decision as final. The report is intentionally kept",
            "under `documentation/google-fonts/gftools-qa/` and ignored by git because it is",
            "generated evidence, not source.",
            "",
            "If Google Fonts asks for browser-rendered image proofs, add `--imgs`",
            "after the local Selenium/browser dependencies are installed.",
        ]
    )

    lines.extend(
        [
            "",
            "## Apply After Maintainer Confirmation",
            "",
            "- Decide whether kerning is required before the first Google Fonts PR.",
            "- If kerning is in scope, make source kerning compatible across masters",
            "  and verify generated variable and static fonts expose GPOS `kern`.",
            "- Generate and review the `gftools qa --proof` HTML proof for spacing",
            "  and kerning after kerning is added or explicitly deferred.",
            "- If kerning is deferred, record the explicit reviewer-acceptable",
            "  rationale in `documentation/google-fonts/google-fonts-decisions.md` and the",
            "  submission handoff.",
            "- Rerun `make preflight` and `make test` after kerning changes.",
            "",
            "References:",
            "",
            f"- {GF_TESTING_GUIDE}",
            f"- {GF_TOOLS_GUIDE}",
            f"- {GF_ONBOARDER_WORKFLOW}",
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
