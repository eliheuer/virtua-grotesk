#!/usr/bin/env python3
"""Report Google Fonts project-template automation readiness."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/project-template-automation-readiness.md")
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")


OPTIONAL_TEMPLATE_FEATURES = [
    (
        "GitHub Actions workflows",
        ".github/workflows",
        lambda: (ROOT / ".github/workflows").is_dir(),
        "Run build/proof/report automation in public CI.",
    ),
    (
        "GitHub Pages publishing",
        ".github/workflows/*pages* or workflow mentioning pages",
        lambda: any(
            "pages" in path.name.lower() or "pages" in path.read_text(encoding="utf-8", errors="ignore").lower()
            for path in (ROOT / ".github/workflows").glob("*.yml")
        )
        if (ROOT / ".github/workflows").is_dir()
        else False,
        "Publish proof and QA artifacts for reviewer inspection.",
    ),
    (
        "Renovate configuration",
        "renovate.json",
        lambda: (ROOT / "renovate.json").exists(),
        "Automate dependency update PRs.",
    ),
    (
        "Project-template config",
        ".templaterc.json",
        lambda: (ROOT / ".templaterc.json").exists(),
        "Allow future `googlefonts-project-template` refreshes.",
    ),
    (
        "Template update Make target",
        "update-project-template",
        lambda: "update-project-template" in make_targets(),
        "Expose a one-command template refresh path.",
    ),
    (
        "Automated release bundle publishing",
        ".github/workflows release packaging",
        lambda: any(
            ("release" in path.name.lower() or "archive" in path.name.lower())
            for path in (ROOT / ".github/workflows").glob("*.yml")
        )
        if (ROOT / ".github/workflows").is_dir()
        else False,
        "Publish generated fonts or source archives for Packager source strategy.",
    ),
]

LOCAL_EQUIVALENT_TARGETS = [
    ("Build fonts", "build"),
    ("Run Fontspector", "test"),
    ("Regenerate reports", "reports"),
    ("Run synchronized preflight", "preflight"),
    ("Render proof PDF only", "proof-only"),
    ("Full local handoff", "handoff"),
]


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_external_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def workflow_text(repo: Path) -> str:
    workflows = repo / ".github/workflows"
    if not workflows.is_dir():
        return ""
    parts: list[str] = []
    for path in sorted(workflows.glob("*.y*ml")):
        parts.append(read_external_text(path))
    return "\n".join(parts)


def make_targets() -> set[str]:
    makefile = read_text("Makefile")
    targets: set[str] = set()
    for line in makefile.splitlines():
        if not line or line.startswith("\t") or line.startswith(".") or ":" not in line:
            continue
        head = line.split(":", 1)[0].strip()
        if head and " " not in head and "=" not in head:
            targets.add(head)
    return targets


def decision_status() -> str:
    decisions = read_text("documentation/google-fonts/google-fonts-decisions.md")
    match = re.search(r"## Project template automation\s*\n\s*Status: ([a-z]+)", decisions)
    return match.group(1) if match else "unknown"


def markdown_report() -> str:
    targets = make_targets()
    makefile = read_text("Makefile")
    gf_workflows = workflow_text(DEFAULT_GF_REPO)
    optional_rows = [(name, path, present(), purpose) for name, path, present, purpose in OPTIONAL_TEMPLATE_FEATURES]
    optional_present = sum(1 for _, _, present, _ in optional_rows if present)
    local_rows = [(name, target, target in targets) for name, target in LOCAL_EQUIVALENT_TARGETS]
    local_present = sum(1 for _, _, present in local_rows if present)
    status = decision_status()
    test_target_uses_fontspector = "scripts/check_gf_fonts.sh" in makefile
    local_qa_mentions_fontbakery = "fontbakery" in makefile.lower()
    gf_workflows_use_fontspector = "fontspector" in gf_workflows.lower()
    gf_workflows_reference_fontbakery = "fontbakery" in gf_workflows.lower()

    lines = [
        "# Project Template Automation Readiness",
        "",
        "This generated report separates the Google Fonts project template's",
        "optional automation conveniences from the mandatory upstream structure.",
        "The current decision is to defer template automation for the first",
        "submission. The local Google Fonts handoff gate should stay independent",
        "of CI, Pages, Renovate, or template refresh tooling that has not been",
        "adopted yet.",
        "",
        "## Summary",
        "",
        f"- Decision log status: {status}",
        f"- Optional template automation present: {optional_present} / {len(optional_rows)}",
        f"- Local equivalent Make targets present: {local_present} / {len(local_rows)}",
        f"- Local QA target uses Fontspector: {yes_no(test_target_uses_fontspector)}",
        f"- Local Makefile references FontBakery: {yes_no(local_qa_mentions_fontbakery)}",
        f"- Local google/fonts workflows use Fontspector: {yes_no(gf_workflows_use_fontspector)}",
        f"- Local google/fonts workflows reference FontBakery: {yes_no(gf_workflows_reference_fontbakery)}",
        "- Official QA guide says FontBakery was previous and Fontspector is current: yes",
        "- Current project-template README still describes `make test` as",
        "  FontBakery-based QA: yes",
        "- Older tools/template prose still describes FontBakery-based",
        "  setup or template QA: yes",
        "- Mandatory upstream structure report: `documentation/google-fonts/upstream-structure-readiness.md`",
        "- Template and recent PR audit: `documentation/google-fonts/google-fonts-template-and-pr-audit.md`",
        "",
        "## Optional Template Automation",
        "",
        "| Feature | Template path or target | Present | Purpose |",
        "| --- | --- | --- | --- |",
    ]
    for name, path, present, purpose in optional_rows:
        lines.append(f"| {name} | `{path}` | {yes_no(present)} | {purpose} |")

    lines.extend(
        [
            "",
            "## Local Equivalent Commands",
            "",
            "| Local workflow | Make target | Present |",
            "| --- | --- | --- |",
        ]
    )
    for name, target, present in local_rows:
        lines.append(f"| {name} | `{target}` | {yes_no(present)} |")

    lines.extend(
        [
            "",
            "## Apply Before Final Submission",
            "",
            "- Keep `documentation/google-fonts/upstream-structure-readiness.md` as the source of truth",
            "  for mandatory Google Fonts upstream shape.",
            "- Revisit template automation only after choosing the public repository",
            "  workflow for CI, proof publishing, dependency updates, and",
            "  release/source artifacts.",
            "- If template automation is adopted, add it deliberately instead of copying",
            "  the project template wholesale over the existing UFO/designspace workflow.",
            "- Treat the official project-template prose as structure guidance, not as",
            "  a command to reintroduce legacy FontBakery QA. The guide's template",
            "  section, tools page, and the current project-template README still",
            "  contain FontBakery-era automation or setup prose, while the current",
            "  official QA page and local `google/fonts` workflow evidence point at",
            "  Fontspector.",
            "- Any future CI should run this repo's Fontspector-based `make test`",
            "  gate. Do not introduce FontBakery unless a reviewer explicitly asks",
            "  for a legacy check.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/qa.html",
            "- https://googlefonts.github.io/gf-guide/tools.html",
            "- https://github.com/googlefonts/googlefonts-project-template",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_project_template_automation.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output = ROOT / parse_args(argv)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
