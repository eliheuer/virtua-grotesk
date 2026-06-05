#!/usr/bin/env python3
"""Generate a priority-sorted maintainer answer sheet for GF decisions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/google-fonts-decision-answer-sheet.md")


@dataclass(frozen=True)
class Prompt:
    heading: str
    body: str


PROMPT_BLOCK_MARKERS = {
    "Question:",
    "Current local evidence:",
    "Current placeholder:",
    "Current state:",
    "Current preliminary check:",
    "Current value:",
    "Recommended answer:",
    "Options:",
    "Why it matters:",
}


PRIORITY_ORDER = [
    (
        "Public Upstream URL",
        "1",
        "Unblocks copyright URLs, METADATA.pb source.repository_url, Packager fetches, and issue/PR text.",
    ),
    (
        "Packager Source Strategy",
        "1",
        "Determines whether Packager consumes committed binaries, release assets, or a reproducible source build.",
    ),
    (
        "Family Name, Namecheck, Trademarks, and CLA",
        "1",
        "Blocks downstream review because name clearance and CLA identity must be maintainer-confirmed.",
    ),
    (
        "Copyright Authorship and AI Disclosure",
        "1",
        "Maps directly to the current Google Fonts Add Font authorship and AI-use checkbox.",
    ),
    (
        "Author and Contributor Strings",
        "2",
        "Feeds AUTHORS.txt, CONTRIBUTORS.txt, METADATA.pb designer strings, and designer-profile matching.",
    ),
    (
        "Article or Legacy Description",
        "2",
        "Controls whether the package uses the newer Article flow and whether Arabic-localized text is needed.",
    ),
    (
        "Upstream Release Tag",
        "2",
        "Needs the final public source state and version strategy before package handoff.",
    ),
    (
        "Version Strategy",
        "2",
        "Sets first-release version semantics and should align with any release tag.",
    ),
    (
        "Project Template Automation",
        "2",
        "Decides whether public CI/proof publishing is added now or deferred after source and release strategy settle.",
    ),
    (
        "PUA Icon Block",
        "3",
        "Affects glyph scope, subsetting review, and whether PUA rationale belongs in the issue.",
    ),
    (
        "Vendor ID",
        "3",
        "Can clear recurring Fontspector warnings if a registered four-character ID is available.",
    ),
    (
        "Kerning Scope",
        "3",
        "Decides whether kerning warnings are blockers or explicitly deferred.",
    ),
    (
        "`avar`",
        "3",
        "Decides whether the linear weight axis intentionally ships with an identity avar table.",
    ),
    (
        "Custom Sample Text",
        "3",
        "Keeps Arabic catalog sample text on the default path unless a specific override is needed.",
    ),
]

DECISION_LOG_HEADING = {
    "Author and Contributor Strings": "Author/contact lines",
    "PUA Icon Block": "Private-use icon block",
    "Kerning Scope": "Kerning",
}


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def parse_prompts(text: str) -> dict[str, Prompt]:
    prompts: dict[str, Prompt] = {}
    matches = list(re.finditer(r"^## \d+\. (.+)$", text, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = match.group(1).strip()
        prompts[heading] = Prompt(heading=heading, body=text[start:end].strip())
    return prompts


def extract_block(body: str, marker: str) -> list[str]:
    lines = body.splitlines()
    try:
        start = lines.index(marker) + 1
    except ValueError:
        return []
    block: list[str] = []
    for line in lines[start:]:
        if line in PROMPT_BLOCK_MARKERS:
            break
        block.append(line)
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    return block


def parse_decision_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[start:end].strip()
    return sections


def parse_decision_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for heading, body in parse_decision_sections(text).items():
        match = re.search(r"^Status: (open|decided)$", body, flags=re.MULTILINE)
        if match:
            statuses[heading] = match.group(1)
    return statuses


def normalized_heading(heading: str) -> str:
    return heading.replace("`", "").casefold()


def current_evidence(prompt: Prompt) -> list[str]:
    markers = [
        "Current local evidence:",
        "Current placeholder:",
        "Current state:",
        "Current preliminary check:",
        "Current value:",
        "Recommended answer:",
        "Options:",
    ]
    evidence: list[str] = []
    for marker in markers:
        block = extract_block(prompt.body, marker)
        if block:
            evidence.extend([f"{marker}", *block])
            if marker != "Options:":
                evidence.append("")
    while evidence and not evidence[-1].strip():
        evidence.pop()
    return evidence


def apply_targets(sections: dict[str, str], prompt_heading: str) -> list[str]:
    decision_heading = DECISION_LOG_HEADING.get(prompt_heading, prompt_heading)
    section = sections.get(decision_heading)
    if section is None:
        normalized_sections = {normalized_heading(heading): body for heading, body in sections.items()}
        section = normalized_sections.get(normalized_heading(decision_heading))
    if section is None:
        return []
    return extract_block(section, "Apply to:")


def decision_status(statuses: dict[str, str], prompt_heading: str) -> str:
    decision_heading = DECISION_LOG_HEADING.get(prompt_heading, prompt_heading)
    if decision_heading in statuses:
        return statuses[decision_heading]
    normalized_statuses = {
        normalized_heading(heading): status for heading, status in statuses.items()
    }
    return normalized_statuses.get(normalized_heading(decision_heading), "unknown")


def markdown_report() -> str:
    questions_text = read_text("documentation/google-fonts/google-fonts-decision-questions.md")
    decisions_text = read_text("documentation/google-fonts/google-fonts-decisions.md")
    prompts = parse_prompts(questions_text)
    decision_sections = parse_decision_sections(decisions_text)
    decision_statuses = parse_decision_statuses(decisions_text)
    open_priority_items = [
        (heading, priority, reason)
        for heading, priority, reason in PRIORITY_ORDER
        if decision_status(decision_statuses, heading) == "open"
    ]

    lines = [
        "# Google Fonts Decision Answer Sheet",
        "",
        "This generated sheet is the quickest maintainer-facing place to answer",
        "currently open Google Fonts onboarding decisions. It is priority-sorted from the",
        "canonical question file and does not make decisions on the maintainer's",
        "behalf.",
        "",
        "Use this flow:",
        "",
        "1. Answer a row here.",
        "2. Record the accepted answer in `documentation/google-fonts/google-fonts-decisions.md`.",
        "3. Apply the decision to the listed source, metadata, or downstream package surfaces.",
        "4. Rerun `make preflight` so proof evidence and generated reports stay synchronized.",
        "",
        "Canonical files:",
        "",
        "- `documentation/google-fonts/google-fonts-decision-questions.md`",
        "- `documentation/google-fonts/google-fonts-decisions.md`",
        "- `documentation/google-fonts/decision-readiness.md`",
        "",
    ]

    for priority in ("1", "2", "3"):
        priority_items = [
            (heading, item_priority, reason)
            for heading, item_priority, reason in open_priority_items
            if item_priority == priority
        ]
        if not priority_items:
            continue
        lines.extend([f"## Priority {priority}", ""])
        for heading, item_priority, reason in priority_items:
            prompt = prompts.get(heading)
            lines.extend(
                [
                    f"### {heading}",
                    "",
                    f"Why answer: {reason}",
                    "",
                ]
            )
            if prompt is None:
                lines.extend(["Prompt status: missing", ""])
                continue
            question = extract_block(prompt.body, "Question:")
            if question:
                lines.extend(["Question:", "", *question, ""])
            evidence = current_evidence(prompt)
            if evidence:
                lines.extend(["Current guidance/evidence:", "", *evidence, ""])
            targets = apply_targets(decision_sections, heading)
            if targets:
                lines.extend(["Apply targets:", "", *targets, ""])
            lines.extend(
                [
                    "Maintainer answer:",
                    "",
                    "```text",
                    "TBD by maintainer",
                    "```",
                    "",
                ]
            )

    lines.extend(
        [
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_decision_answer_sheet.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
