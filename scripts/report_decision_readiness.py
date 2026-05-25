#!/usr/bin/env python3
"""Generate a Google Fonts maintainer-decision readiness report."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/decision-readiness.md")


@dataclass(frozen=True)
class Decision:
    heading: str
    status: str
    body: str


@dataclass(frozen=True)
class ApplyToSurface:
    decision: str
    item: str
    path_patterns: tuple[str, ...]
    existing_count: int | None
    expected_count: int | None


@dataclass(frozen=True)
class QuestionPrompt:
    heading: str
    body: str


QUESTION_ALIASES = {
    "Public upstream URL": "Public Upstream URL",
    "Packager source strategy": "Packager Source Strategy",
    "Author/contact lines": "Author and Contributor Strings",
    "Family name, namecheck, trademarks, and CLA": "Family Name, Namecheck, Trademarks, and CLA",
    "Copyright authorship and AI disclosure": "Copyright Authorship and AI Disclosure",
    "Custom sample text": "Custom Sample Text",
    "First-submission script scope": "",
    "Private-use icon block": "PUA Icon Block",
    "Vendor ID": "Vendor ID",
    "Kerning": "Kerning Scope",
    "`avar`": "`avar`",
    "Version strategy": "Version Strategy",
    "Upstream release tag": "Upstream Release Tag",
    "Article or legacy description": "Article or Legacy Description",
    "Project template automation": "Project Template Automation",
}

QUESTION_PRIORITIES = [
    (
        "Public Upstream URL",
        "1",
        "Unlocks public metadata, copyright URL strings, package source fetches, and issue/PR text.",
    ),
    (
        "Packager Source Strategy",
        "1",
        "Determines whether Packager consumes committed binaries, release assets, or a source build.",
    ),
    (
        "Family Name, Namecheck, Trademarks, and CLA",
        "1",
        "Blocks downstream review because name clearance and CLA identity must be maintainer-confirmed.",
    ),
    (
        "Copyright Authorship and AI Disclosure",
        "1",
        "Maps directly to the current Google Fonts Add Font legal/authorship checkbox.",
    ),
    (
        "Author and Contributor Strings",
        "2",
        "Feeds AUTHORS, CONTRIBUTORS, METADATA designer strings, and designer-profile matching.",
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
        "Decides whether to add public CI/proof publishing now or keep the local handoff gate.",
    ),
    (
        "PUA Icon Block",
        "3",
        "Affects glyph scope, subsetting review, and whether PUA rationale belongs in the issue.",
    ),
    (
        "Vendor ID",
        "3",
        "Can clear recurring Fontspector warnings if a registered ID is available.",
    ),
    (
        "Kerning Scope",
        "3",
        "Decides whether kerning warnings are blockers or explicitly deferred.",
    ),
    (
        "`avar`",
        "3",
        "Decides whether the linear weight axis intentionally ships without an avar table.",
    ),
    (
        "Custom Sample Text",
        "3",
        "Keeps Arabic catalog sample text on the default path unless a specific override is needed.",
    ),
]

MECHANICAL_APPLY_COVERAGE = [
    (
        "Public upstream URL",
        "`scripts/apply_public_upstream_url.py`",
        "ready after maintainer-approved URL",
        "Dry-runs and applies placeholder URL replacements across source metadata, handoff docs, and downstream preview surfaces.",
    ),
    (
        "Downstream METADATA.pb",
        "`make downstream-metadata-check` and `scripts/prepare_downstream_metadata.py --apply`",
        "guarded until placeholders clear",
        "Validates the preview and writes into the local `google/fonts` fork only after pending URL, designer, commit, and branch values are resolved.",
    ),
    (
        "Packager dry run",
        "`make package-dry-run`",
        "guarded no-PR dry run",
        "Checks local `google/fonts` topology, package inputs, source mode, starter metadata, and GitHub API auth before invoking Packager.",
    ),
    (
        "Add Font issue and handoff text",
        "`make issue-draft` and `documentation/submission-handoff-readiness.md`",
        "generated drafts",
        "Keeps current template labels, issue text, Fontspector counts, Arabic scope, and report references synchronized after decisions are applied.",
    ),
    (
        "Designer profile package",
        "`make designer-profile-check`",
        "audit and draft only",
        "Checks whether final designer strings have matching Google Fonts catalog profiles or a prepared designer-profile request.",
    ),
    (
        "Decision-linked warnings",
        "`documentation/fontspector-warnings.md` and `documentation/final-submission-blockers.md`",
        "evidence only",
        "Groups Vendor ID, kerning, avar, PUA/reachability, and subsetting warnings for maintainer acceptance or follow-up fixes.",
    ),
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def parse_decisions(text: str) -> list[Decision]:
    sections = re.split(r"^## ", text, flags=re.MULTILINE)
    decisions: list[Decision] = []
    for section in sections[1:]:
        heading, _, body = section.partition("\n")
        status_match = re.search(r"^Status: (open|decided)$", body, flags=re.MULTILINE)
        if status_match:
            decisions.append(Decision(heading.strip(), status_match.group(1), body))
    return decisions


def parse_questions(text: str) -> set[str]:
    return {question.heading for question in parse_question_prompts(text)}


def parse_question_prompts(text: str) -> list[QuestionPrompt]:
    prompts: list[QuestionPrompt] = []
    matches = list(re.finditer(r"^## \d+\. (.+)$", text, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        prompts.append(QuestionPrompt(match.group(1).strip(), text[start:end]))
    return prompts


def parse_question_headings(text: str) -> set[str]:
    headings = set()
    for match in re.finditer(r"^## \d+\. (.+)$", text, flags=re.MULTILINE):
        headings.add(match.group(1).strip())
    return headings


def question_has_answer_guidance(prompt: QuestionPrompt) -> bool:
    guidance_markers = [
        "Recommended answer:",
        "Current placeholder:",
        "Current state:",
        "Current preliminary check:",
        "Options:",
    ]
    return (
        "Question:" in prompt.body
        and "Why it matters:" in prompt.body
        and any(marker in prompt.body for marker in guidance_markers)
    )


def has_apply_to_block(body: str) -> bool:
    match = re.search(r"^Apply to:\n\n(?P<items>(?:- .+\n?)+)", body, flags=re.MULTILINE)
    return bool(match and match.group("items").strip())


def parse_apply_to_items(body: str) -> list[str]:
    match = re.search(r"^Apply to:\n\n(?P<items>(?:- .+\n?)+)", body, flags=re.MULTILINE)
    if not match:
        return []
    return [
        line.removeprefix("- ").strip()
        for line in match.group("items").splitlines()
        if line.startswith("- ")
    ]


def local_path_patterns(item: str) -> tuple[str, ...]:
    if re.search(r"\bif adopted\b", item, flags=re.IGNORECASE):
        return ()
    patterns: list[str] = []
    for token in re.findall(r"`([^`]+)`", item):
        if token.startswith("documentation/") or token.startswith("sources/"):
            patterns.append(token)
        elif token in {"AUTHORS.txt", "CONTRIBUTORS.txt", "OFL.txt", "README.md", "Makefile", "build.sh"}:
            patterns.append(token)
        elif token.startswith("scripts/") or token.startswith(".github/") or token.startswith(".gitignore"):
            patterns.append(token)
    return tuple(patterns)


def count_existing_patterns(patterns: tuple[str, ...]) -> tuple[int, int]:
    expected = 0
    existing = 0
    for pattern in patterns:
        expected += 1
        matches = list(ROOT.glob(pattern)) if "*" in pattern else [ROOT / pattern]
        if any(path.exists() for path in matches):
            existing += 1
    return existing, expected


def apply_to_surfaces(decisions: list[Decision]) -> list[ApplyToSurface]:
    surfaces: list[ApplyToSurface] = []
    for decision in decisions:
        for item in parse_apply_to_items(decision.body):
            patterns = local_path_patterns(item)
            if patterns:
                existing, expected = count_existing_patterns(patterns)
            else:
                existing = None
                expected = None
            surfaces.append(
                ApplyToSurface(
                    decision=decision.heading,
                    item=item,
                    path_patterns=patterns,
                    existing_count=existing,
                    expected_count=expected,
                )
            )
    return surfaces


def surface_path_status(surface: ApplyToSurface) -> str:
    if surface.expected_count is None or surface.existing_count is None:
        return "n/a"
    return f"{surface.existing_count} / {surface.expected_count}"


def markdown_report() -> str:
    decisions = parse_decisions(read_text("documentation/google-fonts-decisions.md"))
    question_text = read_text("documentation/google-fonts-decision-questions.md")
    question_prompts = parse_question_prompts(question_text)
    questions = {question.heading for question in question_prompts}
    add_font_audit = read_text("documentation/google-fonts-add-font-template-audit.md")
    open_decisions = [decision for decision in decisions if decision.status == "open"]
    decided_decisions = [decision for decision in decisions if decision.status == "decided"]
    open_with_questions = [
        decision
        for decision in open_decisions
        if QUESTION_ALIASES.get(decision.heading, decision.heading) in questions
    ]
    decided_without_questions = [
        decision
        for decision in decided_decisions
        if not QUESTION_ALIASES.get(decision.heading, decision.heading)
        or QUESTION_ALIASES.get(decision.heading, decision.heading) not in questions
    ]
    open_with_apply_to = [decision for decision in open_decisions if has_apply_to_block(decision.body)]
    surfaces = apply_to_surfaces(decisions)
    open_surfaces = apply_to_surfaces(open_decisions)
    path_backed_surfaces = [surface for surface in open_surfaces if surface.path_patterns]
    existing_path_count = sum(surface.existing_count or 0 for surface in path_backed_surfaces)
    expected_path_count = sum(surface.expected_count or 0 for surface in path_backed_surfaces)
    external_surfaces = [surface for surface in open_surfaces if not surface.path_patterns]
    guided_questions = [prompt for prompt in question_prompts if question_has_answer_guidance(prompt)]
    open_question_headings = {
        QUESTION_ALIASES.get(decision.heading, decision.heading)
        for decision in open_decisions
        if QUESTION_ALIASES.get(decision.heading, decision.heading)
    }

    lines = [
        "# Decision Readiness",
        "",
        "This generated report checks that the maintainer-facing Google Fonts",
        "decision log and question list stay aligned. It does not answer",
        "policy, legal, authorship, source-release, or design-scope questions",
        "on the maintainer's behalf.",
        "",
        "## Summary",
        "",
        f"- Decision log entries: {len(decisions)}",
        f"- Open decisions: {len(open_decisions)}",
        f"- Decided decisions: {len(decided_decisions)}",
        f"- Decision question prompts: {len(questions)}",
        f"- Decision question prompts with answer guidance: {len(guided_questions)} / {len(question_prompts)}",
        f"- Open decisions with matching question prompts: {len(open_with_questions)} / {len(open_decisions)}",
        f"- Decided decisions omitted from question prompts: {yes_no(len(decided_without_questions) == len(decided_decisions))}",
        f"- Open decisions with apply-to blocks: {len(open_with_apply_to)} / {len(open_decisions)}",
        f"- Open decision apply-to surface items: {len(open_surfaces)}",
        f"- Open decision local path patterns present: {existing_path_count} / {expected_path_count}",
        f"- Open decision non-file or downstream surfaces: {len(external_surfaces)}",
        f"- Add Font template audit present: {yes_no('# Google Fonts Add Font Template Audit' in add_font_audit)}",
        f"- Add Font template authorship prompt tracked: {yes_no('AI tools were used' in add_font_audit and 'sole copyright author' in add_font_audit)}",
        f"- Add Font template namecheck prompt tracked: {yes_no('namecheck.fontdata.com' in add_font_audit)}",
        "",
        "## Decision Map",
        "",
        "| Decision | Status | Question prompt | Apply-to block |",
        "| --- | --- | --- | --- |",
    ]
    for decision in decisions:
        question = QUESTION_ALIASES.get(decision.heading, decision.heading)
        question_status = "n/a" if not question else yes_no(question in questions)
        lines.append(
            f"| {decision.heading} | {decision.status} | {question_status} | {yes_no(has_apply_to_block(decision.body))} |"
        )

    lines.extend(
        [
            "",
            "## Prioritized Question Packet",
            "",
            "Answer priority `1` items before public package or PR work. Priority `2`",
            "items should be settled before final handoff text is frozen. Priority `3`",
            "items can be decided while drawing and QA cleanup continue, but should not",
            "remain open for the final submission.",
            "",
            "| Priority | Question | Why answer now | Prompt present |",
            "| --- | --- | --- | --- |",
        ]
    )
    for heading, priority, reason in QUESTION_PRIORITIES:
        if heading not in open_question_headings:
            continue
        lines.append(
            f"| {priority} | {heading} | {reason} | {yes_no(heading in questions)} |"
        )

    lines.extend(
        [
            "",
            "## Question Prompt Inventory",
            "",
            "| Question | Has question text | Has answer guidance | Has why-it-matters |",
            "| --- | --- | --- | --- |",
        ]
    )
    for prompt in question_prompts:
        lines.append(
            f"| {prompt.heading} | {yes_no('Question:' in prompt.body)} | "
            f"{yes_no(question_has_answer_guidance(prompt))} | "
            f"{yes_no('Why it matters:' in prompt.body)} |"
        )

    lines.extend(
        [
            "",
            "## Apply-To Surface Inventory",
            "",
            "| Decision | Surface | Local path patterns | Present now |",
            "| --- | --- | --- | --- |",
        ]
    )
    for surface in surfaces:
        patterns = "<br>".join(f"`{pattern}`" for pattern in surface.path_patterns) if surface.path_patterns else "n/a"
        lines.append(
            f"| {surface.decision} | {surface.item} | {patterns} | {surface_path_status(surface)} |"
        )

    lines.extend(
        [
            "",
            "## Mechanical Apply Coverage",
            "",
            "| Surface | Helper or report | Current coverage | Notes |",
            "| --- | --- | --- | --- |",
        ]
    )
    for surface, helper, status, notes in MECHANICAL_APPLY_COVERAGE:
        lines.append(f"| {surface} | {helper} | {status} | {notes} |")

    lines.extend(
        [
            "",
            "## Apply Before Final Submission",
            "",
            "- Record maintainer answers in `documentation/google-fonts-decisions.md`",
            "  before editing source metadata or downstream package previews.",
            "- Keep `documentation/google-fonts-decision-questions.md` focused on",
            "  open questions only; decided scope belongs in the decision log and",
            "  generated evidence reports.",
            "- Rerun `make preflight` after any decision is answered so proof",
            "  evidence, generated reports, handoff draft, and package checklist",
            "  stay synchronized.",
            "",
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
        raise SystemExit("usage: report_decision_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
