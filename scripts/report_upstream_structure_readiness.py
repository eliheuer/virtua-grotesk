#!/usr/bin/env python3
"""Generate a Google Fonts upstream repository structure readiness report."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/upstream-structure-readiness.md")


MANDATORY_PATHS = [
    ("AUTHORS.txt", "author contact file"),
    ("CONTRIBUTORS.txt", "contributor contact file"),
    ("OFL.txt", "OFL license file"),
    ("README.md", "project README"),
    ("documentation", "expanded documentation and images"),
    ("fonts", "generated font output directory"),
    ("fonts/ttf", "static TTF output directory"),
    ("fonts/variable", "variable TTF output directory"),
    ("sources", "source directory"),
    ("requirements.txt", "Python requirements"),
    (".gitignore", "ignored local/generated files"),
]
SOURCE_INPUTS = [
    "sources/config.yaml",
    "sources/VirtuaGrotesk.designspace",
    "sources/VirtuaGrotesk-Regular.ufo",
    "sources/VirtuaGrotesk-Bold.ufo",
]
GENERATED_SOURCE_DIRS = [
    "sources/instance_ufos",
    "sources/.fontc-build",
    "sources/build.ninja",
    "sources/.ninja_log",
]
EXPECTED_FONT_OUTPUTS = [
    "fonts/variable/VirtuaGrotesk[wght].ttf",
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]


@dataclass(frozen=True)
class PathStatus:
    path: str
    purpose: str
    exists: bool
    ignored: bool


def read_text(path: str) -> str:
    target = ROOT / path
    return target.read_text(encoding="utf-8") if target.exists() else ""


def git_check_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def path_statuses(paths: list[tuple[str, str]]) -> list[PathStatus]:
    return [
        PathStatus(path, purpose, (ROOT / path).exists(), git_check_ignored(path))
        for path, purpose in paths
    ]


def non_comment_entries(path: str) -> list[str]:
    return [
        line.strip()
        for line in read_text(path).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def markdown_report() -> str:
    mandatory = path_statuses(MANDATORY_PATHS)
    sources = path_statuses([(path, "active source input") for path in SOURCE_INPUTS])
    generated = path_statuses([(path, "generated source/build output") for path in GENERATED_SOURCE_DIRS])
    fonts = path_statuses([(path, "generated font output") for path in EXPECTED_FONT_OUTPUTS])
    readme = read_text("README.md")
    ofl = read_text("OFL.txt")
    gitignore = read_text(".gitignore")
    config = read_text("sources/config.yaml")
    build_sh = read_text("build.sh")
    doc_files = [path.name for path in (ROOT / "documentation").glob("*") if path.is_file()] if (ROOT / "documentation").exists() else []
    source_root_ufos = sorted(path.name for path in (ROOT / "sources").glob("*.ufo")) if (ROOT / "sources").exists() else []
    source_root_designspaces = sorted(path.name for path in (ROOT / "sources").glob("*.designspace")) if (ROOT / "sources").exists() else []

    lines = [
        "# Upstream Structure Readiness",
        "",
        "This generated report maps the repository to the Google Fonts upstream",
        "structure and build-guide requirements that can be checked locally. It",
        "does not claim that drawing, spacing, kerning, or script coverage is",
        "complete.",
        "",
        "## Summary",
        "",
        f"- Mandatory upstream paths present: {sum(item.exists for item in mandatory)} / {len(mandatory)}",
        f"- AUTHORS.txt entries present: {yes_no(bool(non_comment_entries('AUTHORS.txt')))}",
        f"- CONTRIBUTORS.txt entries present: {yes_no(bool(non_comment_entries('CONTRIBUTORS.txt')))}",
        f"- OFL first line has copyright: {yes_no(ofl.startswith('Copyright '))}",
        f"- README has short description: {yes_no('Virtua Grotesk is' in readme)}",
        f"- README has build instructions: {yes_no('make build' in readme or './build.sh' in readme)}",
        f"- README references an image: {yes_no('documentation/assets/readme-specimen.png' in readme)}",
        f"- documentation/assets/image-license.txt present: {yes_no((ROOT / 'documentation/assets/image-license.txt').exists())}",
        f"- Active source inputs present: {sum(item.exists for item in sources)} / {len(sources)}",
        f"- One-command build entrypoint present: {yes_no((ROOT / 'build.sh').exists() or (ROOT / 'sources/config.yaml').exists())}",
        f"- `sources/config.yaml` uses gftools builder shape: {yes_no('sources:' in config and 'familyName:' in config)}",
        f"- build.sh invokes gftools builder: {yes_no('gftools builder sources/config.yaml' in build_sh)}",
        f"- Expected generated font outputs present: {sum(item.exists for item in fonts)} / {len(fonts)}",
        f"- Generated font outputs ignored by git: {yes_no(all(item.ignored for item in fonts))}",
        f"- Generated source/build outputs ignored by git: {yes_no(all(item.ignored for item in generated if item.exists))}",
        f"- Local venv ignored by git: {yes_no(git_check_ignored('venv'))}",
        f"- Active source root UFOs: `{', '.join(source_root_ufos) if source_root_ufos else 'none'}`",
        f"- Active source root designspaces: `{', '.join(source_root_designspaces) if source_root_designspaces else 'none'}`",
        "",
        "## Mandatory Paths",
        "",
        "| Path | Purpose | Exists | Ignored by git |",
        "| --- | --- | --- | --- |",
    ]
    for item in mandatory:
        lines.append(f"| `{item.path}` | {item.purpose} | {yes_no(item.exists)} | {yes_no(item.ignored)} |")

    lines.extend(
        [
            "",
            "## Active Source Inputs",
            "",
            "| Path | Exists | Ignored by git |",
            "| --- | --- | --- |",
        ]
    )
    for item in sources:
        lines.append(f"| `{item.path}` | {yes_no(item.exists)} | {yes_no(item.ignored)} |")

    lines.extend(
        [
            "",
            "## Generated Outputs",
            "",
            "| Path | Exists | Ignored by git |",
            "| --- | --- | --- |",
        ]
    )
    for item in [*fonts, *generated]:
        lines.append(f"| `{item.path}` | {yes_no(item.exists)} | {yes_no(item.ignored)} |")

    lines.extend(
        [
            "",
            "## Documentation Inventory",
            "",
            f"- Documentation files: {len(doc_files)}",
            f"- Article draft present: {yes_no('ARTICLE.en_us.html' in doc_files)}",
            f"- Description draft present: {yes_no('DESCRIPTION.en_us.html' in doc_files)}",
            f"- Image provenance present: {yes_no('image-license.txt' in doc_files)}",
            f"- README specimen image present: {yes_no('readme-specimen.png' in doc_files)}",
            "",
            "## Apply Before Final Upstream Release",
            "",
            "- Confirm whether generated fonts remain ignored, are committed on the",
            "  public branch, or are exposed through a release/archive strategy.",
            "- Keep generated build artifacts out of the source root except for",
            "  documented, ignored local outputs.",
            "- Rerun `make preflight` after build, documentation, source-layout,",
            "  or package-source strategy changes.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/build.html",
            "- https://github.com/googlefonts/googlefonts-project-template",
            "",
        ]
    )
    assert "venv" in gitignore
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_upstream_structure_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
