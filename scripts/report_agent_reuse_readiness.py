#!/usr/bin/env python3
"""Generate a reusable-agent Google Fonts onboarding readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts-agent-reuse-readiness.md")

AGENT_FILES = [
    ".agents/README.md",
    ".agents/google-fonts-onboarding-checklists.md",
    ".agents/google-fonts-official-reference-map.md",
    ".agents/skills/google-fonts-onboarding/SKILL.md",
    ".agents/skills/google-fonts-qa/SKILL.md",
    ".agents/skills/google-fonts-packaging/SKILL.md",
]

SKILL_FILES = [
    ".agents/skills/google-fonts-onboarding/SKILL.md",
    ".agents/skills/google-fonts-qa/SKILL.md",
    ".agents/skills/google-fonts-packaging/SKILL.md",
]

OFFICIAL_REFERENCE_URLS = [
    "https://googlefonts.github.io/gf-guide/onboarding.html",
    "https://googlefonts.github.io/gf-guide/upstream.html",
    "https://googlefonts.github.io/gf-guide/requirements.html",
    "https://googlefonts.github.io/gf-guide/variable.html",
    "https://googlefonts.github.io/gf-guide/metadata.html",
    "https://googlefonts.github.io/gf-guide/package.html",
    "https://googlefonts.github.io/gf-guide/article.html",
    "https://googlefonts.github.io/gf-guide/making-pr.html",
    "https://googlefonts.github.io/gf-guide/onboarder-workflow.html",
    "https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
    "https://github.com/google/fonts",
    "https://github.com/googlefonts/googlefonts-project-template",
    "https://github.com/googlefonts/glyphsets",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def markdown_report() -> str:
    readme = read_text("README.md")
    agents = read_text("AGENTS.md")
    checklist = read_text(".agents/google-fonts-onboarding-checklists.md")
    reference_map = read_text(".agents/google-fonts-official-reference-map.md")
    skill_texts = {path: read_text(path) for path in SKILL_FILES}

    present_files = [path for path in AGENT_FILES if (ROOT / path).exists()]
    linked_in_readme = [path for path in AGENT_FILES[1:] if path in readme]
    linked_in_agents = [path for path in AGENT_FILES[1:] if path in agents]
    official_refs_present = [
        url for url in OFFICIAL_REFERENCE_URLS if url in reference_map
    ]
    reusable_report_refs = sorted(
        set(re.findall(r"`(documentation/[^`]+\.md)`", reference_map))
    )
    checklist_sections = re.findall(r"^## \d+\. ", checklist, flags=re.MULTILINE)
    portable_copy_notes = (
        "Copy this file" in checklist
        and "replace family-specific paths" in checklist
        and "refresh official Google Fonts docs" in checklist
    )
    portable_gate_shape = (
        "Portable Gate Shape" in reference_map
        and "make preflight" in reference_map
        and "fails only for known and documented blockers" in reference_map
    )
    skills_portable = all(
        ("portable" in text.lower() or "copy" in text.lower())
        and "Google Fonts" in text
        for text in skill_texts.values()
    )
    ready = (
        len(present_files) == len(AGENT_FILES)
        and len(linked_in_readme) == len(AGENT_FILES[1:])
        and len(linked_in_agents) == len(AGENT_FILES[1:])
        and len(official_refs_present) == len(OFFICIAL_REFERENCE_URLS)
        and len(reusable_report_refs) >= 20
        and len(checklist_sections) >= 14
        and portable_copy_notes
        and portable_gate_shape
        and skills_portable
    )

    lines = [
        "# Google Fonts Agent Reuse Readiness",
        "",
        "This generated report checks whether the reusable agent-facing",
        "Google Fonts onboarding knowledge is present, linked, and portable",
        "enough to copy into the next font repository.",
        "",
        "## Summary",
        "",
        f"- Reusable agent bundle ready: {yes_no(ready)}",
        f"- Required reusable agent files present: {len(present_files)} / {len(AGENT_FILES)}",
        f"- Reusable files linked from README: {len(linked_in_readme)} / {len(AGENT_FILES[1:])}",
        f"- Reusable files linked from AGENTS.md: {len(linked_in_agents)} / {len(AGENT_FILES[1:])}",
        f"- Official Google Fonts references mapped: {len(official_refs_present)} / {len(OFFICIAL_REFERENCE_URLS)}",
        f"- Reusable report categories listed: {len(reusable_report_refs)}",
        f"- Copy checklist sections: {len(checklist_sections)}",
        f"- Copy-to-next-font notes present: {yes_no(portable_copy_notes)}",
        f"- Portable gate shape present: {yes_no(portable_gate_shape)}",
        f"- Google Fonts skills written for reuse: {yes_no(skills_portable)}",
        "",
        "## Required Reusable Files",
        "",
    ]
    lines.extend(
        f"- `{path}`: {yes_no(path in present_files)}" for path in AGENT_FILES
    )
    lines.extend(
        [
            "",
            "## Official References",
            "",
        ]
    )
    lines.extend(
        f"- {url}: {yes_no(url in official_refs_present)}"
        for url in OFFICIAL_REFERENCE_URLS
    )
    lines.extend(
        [
            "",
            "## Reusable Report Categories",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in reusable_report_refs)
    lines.extend(
        [
            "",
            "## Copy Guidance",
            "",
            "- Copy `.agents/README.md`, `.agents/google-fonts-onboarding-checklists.md`,",
            "  `.agents/google-fonts-official-reference-map.md`, and the three",
            "  `.agents/skills/google-fonts-*` skill directories first.",
            "- Replace family names, source paths, axis data, downstream directory,",
            "  designer identity, script scope, and source package strategy before",
            "  treating the copied docs as authoritative.",
            "- Refresh the official references in",
            "  `.agents/google-fonts-official-reference-map.md` before opening a",
            "  real Google Fonts issue or PR.",
            "- Recreate the report categories above in the new repo, even if the",
            "  script names differ.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_agent_reuse_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

