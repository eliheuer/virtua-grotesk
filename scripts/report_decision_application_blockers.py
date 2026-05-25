#!/usr/bin/env python3
"""Generate a decision-to-packaging blocker map for GF onboarding."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/decision-application-blockers.md")


@dataclass(frozen=True)
class DecisionRow:
    decision: str
    status: str
    downstream_metadata: str
    package_dry_run: str
    final_submission: str
    blocker_markers: str
    apply_surfaces: str


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def decision_statuses(decisions_text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    matches = list(re.finditer(r"^## (.+)$", decisions_text, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(decisions_text)
        body = decisions_text[start:end]
        status_match = re.search(r"^Status: (open|decided)$", body, flags=re.MULTILINE)
        if status_match:
            statuses[heading] = status_match.group(1)
    return statuses


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def summary_int(label: str, text: str, default: int = 0) -> int:
    value = summary_value(label, text, str(default))
    try:
        return int(value)
    except ValueError:
        return default


def pending_line_count(text: str) -> int:
    return len(re.findall(r"^- `documentation/google-fonts-downstream-package-preview\.md:", text, flags=re.MULTILINE))


def first_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def unanswered_answer_sheet_items(answer_sheet: str) -> list[str]:
    items: list[str] = []
    matches = list(re.finditer(r"^### (.+)$", answer_sheet, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(answer_sheet)
        body = answer_sheet[start:end]
        if "TBD by maintainer" in body:
            items.append(heading)
    return items


def markdown_report() -> str:
    decisions = read_text("documentation/google-fonts-decisions.md")
    answer_sheet = read_text("documentation/google-fonts-decision-answer-sheet.md")
    decision_readiness = read_text("documentation/decision-readiness.md")
    downstream_metadata = read_text("documentation/downstream-metadata-readiness.md")
    package_dry_run = read_text("documentation/package-dry-run-readiness.md")
    open_placeholders = read_text("documentation/open-placeholder-audit.md")
    final_blockers = read_text("documentation/final-submission-blockers.md")
    designer_profile = read_text("documentation/designer-profile-readiness.md")
    pua_scope = read_text("documentation/pua-scope.md")
    kerning = read_text("documentation/kerning-readiness.md")
    release_archive = read_text("documentation/release-archive-manifest.md")

    statuses = decision_statuses(decisions)
    open_decisions = summary_value("Open decisions", decision_readiness)
    decided_decisions = summary_value("Decided decisions", decision_readiness)
    pending_fields = summary_value("Pending or placeholder metadata lines", downstream_metadata)
    raw_actionable_pending = summary_int("Actionable pending decision markers", open_placeholders)
    decision_blocker_section = open_placeholders.split("## Internal Guards", 1)[0]
    self_echo_pending = "`documentation/decision-application-blockers.md`" in decision_blocker_section
    actionable_pending = max(0, raw_actionable_pending - int(self_echo_pending))
    package_reaches = summary_value("Wrapper can reach Packager", package_dry_run)
    first_blocker = summary_value("First blocker", package_dry_run)
    api_ready = summary_value("GitHub API credentials ready", package_dry_run)
    release_url_recorded = summary_value("Final GitHub release archive URL recorded", release_archive)
    metadata_pending_lines = pending_line_count(downstream_metadata)
    unanswered_items = unanswered_answer_sheet_items(answer_sheet)
    designer_marker_present = "Pending decision: confirm designer string" in downstream_metadata
    date_added_marker_present = "Pending final Google Fonts date_added" in downstream_metadata
    pua_codepoints = first_value(r"^Variable font PUA codepoints: (\d+)$", pua_scope)
    missing_profiles = summary_value("Candidate profiles missing", designer_profile)

    rows = [
        DecisionRow(
            decision="Author/contact lines",
            status=statuses.get("Author/contact lines", "unknown"),
            downstream_metadata="blocks" if designer_marker_present else "does not block metadata text",
            package_dry_run="blocks" if designer_marker_present else "does not block directly",
            final_submission="blocks until matching profile exists or request is prepared",
            blocker_markers=(
                "`Pending decision` in `designer` and metadata review"
                if designer_marker_present
                else "final designer string applied; designer profile still missing"
            ),
            apply_surfaces="`AUTHORS.txt`; `CONTRIBUTORS.txt`; metadata preview; designer profile draft",
        ),
        DecisionRow(
            decision="Private-use icon block",
            status=statuses.get("Private-use icon block", "unknown"),
            downstream_metadata="does not block",
            package_dry_run="does not block directly",
            final_submission="blocks until included or deferred",
            blocker_markers=f"{pua_codepoints} PUA codepoints; subsetting/reachability warnings",
            apply_surfaces="source glyphset; metadata review; Google Fonts issue rationale",
        ),
        DecisionRow(
            decision="Kerning",
            status=statuses.get("Kerning", "unknown"),
            downstream_metadata="does not block",
            package_dry_run="does not block directly",
            final_submission="blocks until completed or deferred",
            blocker_markers=f"{summary_value('Fontspector `gpos_kerning_info` warnings', kerning)} kerning warnings",
            apply_surfaces="UFO kerning/groups/features; build path if needed; warning triage",
        ),
        DecisionRow(
            decision="Final release/source commit",
            status="pending final source state",
            downstream_metadata="blocks",
            package_dry_run="blocks",
            final_submission="blocks",
            blocker_markers="`Pending final` in `source.commit`; final release archive URL pending",
            apply_surfaces="metadata preview; release/source checklist; GitHub `v1.000` release archive",
        ),
        DecisionRow(
            decision="Final Google Fonts date_added",
            status="pending final package date",
            downstream_metadata="blocks" if date_added_marker_present else "does not block metadata text",
            package_dry_run="blocks" if date_added_marker_present else "does not block directly",
            final_submission="blocks until final downstream metadata date is set",
            blocker_markers=(
                "`Pending final Google Fonts date_added` in metadata preview"
                if date_added_marker_present
                else "final date_added value applied"
            ),
            apply_surfaces="metadata preview; downstream metadata helper; final package review",
        ),
        DecisionRow(
            decision="GitHub API credentials",
            status="local environment pending",
            downstream_metadata="does not block metadata text",
            package_dry_run="blocks",
            final_submission="blocks package verification",
            blocker_markers=f"GitHub API credentials ready: {api_ready}",
                apply_surfaces="local `gh auth` or short-lived `GH_TOKEN` before `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`",
        ),
    ]

    lines = [
        "# Decision Application Blockers",
        "",
        "This generated report maps each remaining maintainer decision or",
        "finalization item to the exact Google Fonts packaging gate it affects.",
        "It is intended as the handoff surface between answering decisions and",
        "applying them to metadata, source, or downstream package files.",
        "",
        "## Summary",
        "",
        f"- Open maintainer decisions: {open_decisions}",
        f"- Decided maintainer decisions: {decided_decisions}",
        f"- Maintainer answer sheet unanswered prompts: {len(unanswered_items)}",
        f"- Maintainer answer sheet unanswered prompt names: {', '.join(unanswered_items) if unanswered_items else 'none'}",
        f"- Downstream metadata pending/placeholder lines: {pending_fields}",
        f"- Downstream preview pending field lines listed: {metadata_pending_lines}",
        f"- Actionable pending decision markers: {actionable_pending}",
        f"- Package dry run reaches Packager: {package_reaches}",
        f"- Package dry-run first blocker: {first_blocker}",
        f"- GitHub API credentials ready: {api_ready}",
        f"- Final GitHub release archive URL recorded: {release_url_recorded}",
        "",
        "## Blocker Map",
        "",
        "| Item | Status | Downstream metadata | Package dry run | Final submission | Current blocker markers | Apply surfaces |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.decision} | {row.status} | {row.downstream_metadata} | "
            f"{row.package_dry_run} | {row.final_submission} | {row.blocker_markers} | {row.apply_surfaces} |"
        )

    lines.extend(
        [
            "",
            "## Current Metadata Markers",
            "",
            "- Designer marker: "
            + (
                "present"
                if designer_marker_present
                else "absent"
            ),
            "- Source commit marker: "
            + (
                "present"
                if "Pending final release/source commit" in downstream_metadata
                else "absent"
            ),
            "- Final date_added marker: "
            + (
                "present"
                if date_added_marker_present
                else "absent"
            ),
            "- Designer profile final metadata strings present: "
            + summary_value("Final metadata designer strings present", designer_profile),
            "- Designer profile missing catalog profiles: "
            + missing_profiles,
            "",
            "## Maintainer Answer Sheet State",
            "",
            "This section mirrors `documentation/google-fonts-decision-answer-sheet.md`",
            "so an open decision cannot lose its maintainer-facing answer prompt",
            "without the application blocker report noticing.",
            "",
            "| Prompt | Answer still TBD | Blocks final submission |",
            "| --- | --- | --- |",
        ]
    )
    if unanswered_items:
        for item in unanswered_items:
            lines.append(f"| {item} | yes | yes |")
    else:
        lines.append("| none | no | no |")

    lines.extend(
        [
            "",
            "## Apply Order",
            "",
            "1. Prepare or request the matching designer profile for the final",
            "   `Eli Heuer` metadata designer string.",
            "2. Decide whether PUA glyphs ship or are deferred, then update the issue",
            "   rationale and any source glyph cleanup plan.",
            "3. Decide whether kerning is required before the first PR or explicitly",
            "   deferred in the submission notes.",
            "4. After drawing/source work is complete, create the final public source",
            "   commit, tag `v1.000`, and GitHub release archive.",
            "5. Replace the pending downstream `date_added` value with the final",
            "   Google Fonts package date.",
            "6. Restore GitHub API credentials, run `make downstream-metadata-check`,",
                "   apply the checked preview, then run the no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_decision_application_blockers.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output = ROOT / parse_args(argv)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
