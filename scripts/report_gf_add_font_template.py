#!/usr/bin/env python3
"""Audit the local google/fonts Add Font issue template."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
TEMPLATE_RELATIVE = Path(".github/ISSUE_TEMPLATE/1_add-font.md")
OUTPUT_DEFAULT = Path("documentation/google-fonts-add-font-template-audit.md")

EXPECTED_REQUIREMENT_SNIPPETS = [
    "entire font project is available",
    "source files are available",
    "sole copyright author",
    "AI tools were used",
    "Reserved Font Names",
    "namecheck.fontdata.com",
    "app menus",
    "copyright holder's full names or acronyms",
    "Latin Core",
    "preferred upstream repo structure",
    "contributing requirements",
    "maintain the repository",
]


@dataclass(frozen=True)
class TemplateAudit:
    gf_repo: Path
    exists: bool
    commit: str
    status_line: str
    name: str
    title: str
    labels: str
    prompts: tuple[str, ...]
    requirements: tuple[str, ...]
    missing_snippets: tuple[str, ...]


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def ahead_behind(repo: Path, left: str, right: str) -> str:
    output = git_output(repo, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    if not output:
        return "unknown"
    parts = output.split()
    if len(parts) != 2:
        return "unknown"
    ahead, behind = parts
    return f"{ahead} ahead, {behind} behind"


def frontmatter_value(key: str, text: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*'?([^'\n]+)'?\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def audit_template(gf_repo: Path) -> TemplateAudit:
    template_path = gf_repo / TEMPLATE_RELATIVE
    if not template_path.exists():
        return TemplateAudit(
            gf_repo=gf_repo,
            exists=False,
            commit="",
            status_line="",
            name="",
            title="",
            labels="",
            prompts=(),
            requirements=(),
            missing_snippets=tuple(EXPECTED_REQUIREMENT_SNIPPETS),
        )

    text = template_path.read_text(encoding="utf-8")
    prompts = tuple(re.findall(r"^\*\*([^*]+):\*\*$", text, flags=re.MULTILINE))
    requirements = tuple(
        line.strip()[6:].strip()
        for line in text.splitlines()
        if line.strip().startswith("- [ ] ")
    )
    missing_snippets = tuple(
        snippet for snippet in EXPECTED_REQUIREMENT_SNIPPETS if snippet not in text
    )
    status = git_output(gf_repo, ["status", "--short", "--branch"])
    return TemplateAudit(
        gf_repo=gf_repo,
        exists=True,
        commit=git_output(gf_repo, ["rev-parse", "--short", "HEAD"]),
        status_line=status.splitlines()[0] if status else "",
        name=frontmatter_value("name", text),
        title=frontmatter_value("title", text),
        labels=frontmatter_value("labels", text),
        prompts=prompts,
        requirements=requirements,
        missing_snippets=missing_snippets,
    )


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def markdown_report(gf_repo: Path) -> str:
    audit = audit_template(gf_repo)
    lines = [
        "# Google Fonts Add Font Template Audit",
        "",
        "This generated report reads the current Add Font issue template from the",
        "local `google/fonts` checkout. It keeps the submission handoff aligned with",
        "the exact current template prompts and requirement checkboxes.",
        "",
        "## Local Template",
        "",
        f"- Repo path: `{audit.gf_repo}`",
        f"- Template path: `{TEMPLATE_RELATIVE}`",
        f"- Exists: {yes_no(audit.exists)}",
        f"- Current commit: `{audit.commit or 'unknown'}`",
        f"- Status: `{audit.status_line or 'unknown'}`",
        f"- Alignment with `upstream/main`: `{ahead_behind(gf_repo, 'main', 'upstream/main') if gf_repo.exists() else 'unknown'}`",
        f"- Alignment with `origin/main`: `{ahead_behind(gf_repo, 'main', 'origin/main') if gf_repo.exists() else 'unknown'}`",
        f"- Name: `{audit.name or 'missing'}`",
        f"- Title pattern: `{audit.title or 'missing'}`",
        f"- Default labels: `{audit.labels or 'missing'}`",
        "",
        "## Prompts",
        "",
    ]
    lines.extend(f"- {prompt}" for prompt in audit.prompts) if audit.prompts else lines.append("- missing")

    lines.extend(["", "## Requirement Checkboxes", ""])
    if audit.requirements:
        for index, requirement in enumerate(audit.requirements, start=1):
            lines.append(f"{index}. {requirement}")
    else:
        lines.append("1. missing")

    lines.extend(["", "## Expected Snippet Coverage", "", "| Snippet | Present |", "| --- | --- |"])
    for snippet in EXPECTED_REQUIREMENT_SNIPPETS:
        lines.append(f"| `{snippet}` | {yes_no(snippet not in audit.missing_snippets)} |")

    lines.extend(
        [
            "",
            "## Virtua Grotesk Handoff Implications",
            "",
            "- Keep the Google Fonts issue labels as `I New Font, II Submission` at creation, then request Arabic/RTL labeling when Arabic support is ready for review.",
            "- The copyright-authorship and AI-use statement is one combined checkbox in the current template; do not split it into unrelated issue answers.",
            "- The final issue must confirm source files are available in the public repo and that the app-menu family name is definitive.",
            "- Regenerate this report with `make reports-only` after updating `/Users/eli/GH/forks/fonts`.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_gf_add_font_template.py [google_fonts_repo] [output.md]")
    if len(argv) == 1:
        return DEFAULT_GF_REPO, OUTPUT_DEFAULT
    if len(argv) == 2:
        return DEFAULT_GF_REPO, Path(argv[1])
    return Path(argv[1]), Path(argv[2])


def main(argv: list[str]) -> int:
    gf_repo, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(gf_repo), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
