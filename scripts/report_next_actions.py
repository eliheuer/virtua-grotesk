#!/usr/bin/env python3
"""Generate an owner-grouped Google Fonts onboarding next-actions report."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/next-actions.md")


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def table_state(area: str, final_blockers: str) -> str:
    pattern = rf"^\| {re.escape(area)} \| (?P<state>[^|]+) \| (?P<requirement>[^|]+) \|$"
    match = re.search(pattern, final_blockers, flags=re.MULTILINE)
    if not match:
        return "not found"
    return match.group("state").strip()


def placeholder_action(final_blockers: str) -> str:
    state = table_state("Placeholder strings", final_blockers)
    if state.startswith("public blockers: 0 URLs, 0 pending markers"):
        return "Monitor placeholder audit; no public placeholder strings currently block handoff."
    return "Resolve remaining public placeholder or pending metadata markers."


def first_blocker(package_dry_run: str) -> str:
    return summary_value("First blocker", package_dry_run)


def blocking_findings(package_dry_run: str) -> str:
    return summary_value("Blocking findings", package_dry_run)


def fontspector_state(report: str, final_blockers: str) -> str:
    table_match = re.search(
        r"^\| (?P<fail>\d+) \| (?P<warn>\d+) \| \d+ \| (?P<pass>\d+) \| \d+ \|",
        report,
        flags=re.MULTILINE,
    )
    if table_match:
        return (
            f"{table_match.group('fail')} FAIL, "
            f"{table_match.group('warn')} WARN, "
            f"{table_match.group('pass')} PASS"
        )
    fallback = table_state("Fontspector googlefonts profile", final_blockers)
    fail_match = re.search(r"(\d+) FAIL", fallback)
    return f"{fail_match.group(1)} FAIL results" if fail_match else fallback


def prioritized_open_rows(decision_readiness: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    in_table = False
    for line in decision_readiness.splitlines():
        if line.startswith("| Priority | Question | Why answer now |"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4 or cells[0] == "---":
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def unblock_follow_up(question: str) -> str:
    if question == "Author and Contributor Strings":
        return "Update source/package metadata, designer profile draft, and release checklist before the no-PR Packager run."
    if question == "PUA Icon Block":
        return "Resolve or explicitly defer private-use glyph scope and reachable/subsetting warnings before final submission."
    if question == "Kerning Scope":
        return "Complete kerning or record an explicit first-submission deferral, then run `make kerning-proof-check` and `make kerning-proof-review-check`."
    if question == "Family Name, Namecheck, Trademarks, and CLA":
        return "Update the Add Font issue draft and handoff text, then rerun `make preflight`."
    return "Apply the decision to the listed source, metadata, or downstream package surfaces."


def markdown_report() -> str:
    final_blockers = read_text("documentation/google-fonts/final-submission-blockers.md")
    decisions = read_text("documentation/google-fonts/decision-readiness.md")
    package_dry_run = read_text("documentation/google-fonts/package-dry-run-readiness.md")
    downstream_diff = read_text("documentation/google-fonts/downstream-metadata-diff.md")
    downstream_metadata = read_text("documentation/google-fonts/downstream-metadata-readiness.md")
    packager_strategy = read_text("documentation/google-fonts/packager-source-strategy.md")
    github_release = read_text("documentation/google-fonts/github-release-draft.md")
    arabic_review = read_text("documentation/glyph-review/arabic-review-packet.md")
    ufo_editor = read_text("documentation/source/ufo-editor-readiness.md")
    arabic_snapshot_integrity = read_text("documentation/glyph-review/arabic-snapshot-integrity.md")
    arabic_first_batch_source_checkpoint = read_text("documentation/glyph-review/arabic-first-batch-source-checkpoint.md")
    arabic_pending_source_checkpoint = read_text("documentation/glyph-review/arabic-pending-source-checkpoint.md")
    fontspector = read_text("documentation/google-fonts/fontspector-googlefonts-report.md")
    local_workflow = read_text("documentation/google-fonts/local-workflow-readiness.md")

    open_decisions = summary_value("Open decisions", decisions, "unknown")
    decided_decisions = summary_value("Decided decisions", decisions, "unknown")
    priority_packet_ready = (
        re.search(r"Decision question prompts with answer guidance: (\d+) / \1", decisions)
        is not None
        and re.search(r"Open decisions with matching question prompts: (\d+) / \1", decisions)
        is not None
    )
    package_reaches = summary_value("Wrapper can reach Packager", package_dry_run)
    starter_template = summary_value("Actual downstream METADATA.pb is starter template", downstream_diff)
    config_yaml_present = summary_value("`source.config_yaml` present", downstream_metadata)
    config_yaml_review = summary_value("`source.config_yaml` needs source-strategy review", downstream_metadata)
    release_archive_untracked = summary_value("Release archive files currently present but untracked", packager_strategy)
    release_tag = summary_value("Release tag", github_release).strip("`")
    release_title = summary_value("Release title", github_release).strip("`")
    release_archive_ready = summary_value("Local archive contains expected files", github_release)
    release_hashes_ready = summary_value("Local archive hashes match source files", github_release)
    font_qa_state = fontspector_state(fontspector, final_blockers)
    first_batch_source_ready = summary_value("Ready for paired-master hand review", arabic_first_batch_source_checkpoint)
    pending_source_ready = summary_value("Ready for paired-master hand review", arabic_pending_source_checkpoint)
    source_mode = summary_value("Source mode", package_dry_run).strip("`")
    open_rows = prioritized_open_rows(decisions)

    lines = [
        "# Google Fonts Next Actions",
        "",
        (
            "This generated report condenses the final blocker stack into an "
            "owner-grouped queue. It does not replace the detailed evidence "
            "reports; it points to the next concrete work needed before the "
            "Google Fonts issue, package dry run, and downstream PR."
        ),
        "",
        "## Snapshot",
        "",
        f"- Maintainer decisions: {open_decisions} open, {decided_decisions} decided",
        f"- Decision answer packet ready: {yes_no(priority_packet_ready)}",
        f"- Local workflow preflight ready: {summary_value('Local preflight command ready to run', local_workflow)}",
        f"- Package dry run reaches Packager: {package_reaches}",
        f"- Package dry-run first blocker: {first_blocker(package_dry_run)}",
        f"- Package dry-run blocking findings: {blocking_findings(package_dry_run)}",
        f"- Selected Packager source mode: `{source_mode}`",
        f"- Downstream starter METADATA.pb present: {starter_template}",
        f"- Downstream `source.config_yaml` present: {config_yaml_present}; source-strategy review needed: {config_yaml_review}",
        f"- GitHub release draft: `{release_tag}` / `{release_title}`; archive files: {release_archive_ready}; hashes: {release_hashes_ready}",
        f"- Fontspector googlefonts profile: {font_qa_state}",
        f"- UFO editor handoff ready: {summary_value('UFO editor handoff ready', ufo_editor)}",
        f"- Arabic snapshot evidence ready: {summary_value('Snapshot evidence ready for hand review', arabic_snapshot_integrity)}",
        f"- Arabic first-batch source checkpoint ready: {first_batch_source_ready}",
        f"- Arabic pending source checkpoint ready: {pending_source_ready}",
        f"- Contour cleanup decisions: {table_state('Contour/no-contour cleanup', final_blockers)}",
        f"- GF visual kerning proof: {table_state('Kerning', final_blockers)}",
        "",
        "## Maintainer Decisions",
        "",
        "| Priority | Action | Evidence |",
        "| --- | --- | --- |",
    ]
    for priority, question, why in open_rows:
        lines.append(
            f"| P{priority} | Resolve {question}. {why} | `documentation/google-fonts/google-fonts-decision-answer-sheet.md` |"
        )
    lines.extend(
        [
        "",
        "## Decision Unblock Order",
        "",
        "| Order | Maintainer answer needed | Mechanical follow-up after answer |",
        "| --- | --- | --- |",
        *[
            f"| {index} | {question} | {unblock_follow_up(question)} |"
            for index, (_, question, _) in enumerate(open_rows, start=1)
        ],
        "",
        "## Drawing And Source Work",
        "",
        "| Action | Current state | Evidence |",
        "| --- | --- | --- |",
        f"| Keep GF Latin Core coverage at zero missing codepoints. | {table_state('GF Latin Core coverage', final_blockers)} | `documentation/google-fonts/missing-gf-latin-core.md` |",
        f"| Keep GF Arabic Core coverage at zero missing codepoints. | {table_state('GF Arabic Core coverage', final_blockers)} | `documentation/google-fonts/missing-gf-arabic-core.md` |",
        f"| Plan Arabic source construction batches. | {table_state('Arabic source worklist', final_blockers)} | `documentation/glyph-review/arabic-source-work-checklist.md` |",
        f"| Add Arabic marks, dotted circle, anchors, and mark/mkmk if Arabic remains in scope. | {table_state('Arabic marks', final_blockers)} | `documentation/glyph-review/arabic-review-packet.md` |",
        f"| Review the next Arabic visual proof packet and record outcomes. | {table_state('Arabic shaping smoke test', final_blockers)}; {table_state('Arabic marks', final_blockers)} | `documentation/glyph-review/arabic-drawing-session-checklist.md`; `documentation/glyph-review/arabic-current-review-worksheet.md`; `documentation/glyph-review/arabic-batch-recorder.md`; `documentation/glyph-review/arabic-first-review-batch.md`; `documentation/glyph-review/arabic-full-queue-ai-sweep.md`; `documentation/glyph-review/arabic-hand-review-session.md`; `documentation/glyph-review/arabic-next-review-packet.md`; `documentation/glyph-review/arabic-goal-completion-audit.md`; `documentation/glyph-review/arabic-visual-review-log.md` |",
        f"| Open the UFOs for hand cleanup only after editor/package checks stay green. | UFO editor: {summary_value('UFO editor handoff ready', ufo_editor)}; snapshot evidence: {summary_value('Snapshot evidence ready for hand review', arabic_snapshot_integrity)}; first-batch source checkpoint: {first_batch_source_ready}; pending source checkpoint: {pending_source_ready} | `documentation/glyph-review/arabic-drawing-session-checklist.md`; `documentation/source/ufo-editor-readiness.md`; `documentation/glyph-review/arabic-snapshot-integrity.md`; `documentation/glyph-review/arabic-first-batch-source-checkpoint.md`; `documentation/glyph-review/arabic-pending-source-checkpoint.md`; `documentation/glyph-review/arabic-manual-edit-targets.md` |",
        f"| Keep source contour/no-contour cleanup closed after drawing edits. | {table_state('Contour/no-contour cleanup', final_blockers)} | `documentation/glyph-review/arabic-manual-review-batches.md`; `documentation/glyph-review/arabic-manual-edit-targets.md`; `documentation/google-fonts/fontspector-contour-count.md`; `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-ai-triage.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md` |",
        f"| Reduce Fontspector warnings without hiding intended serving scope. | {table_state('Fontspector zero-warning path', final_blockers)} | `documentation/google-fonts/fontspector-metadata-warning-probe.md`; `documentation/google-fonts/fontspector-zero-warning-worklist.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-edit-plan.md` |",
        f"| Review GF visual spacing/kerning proof. | {table_state('Kerning', final_blockers)} | `documentation/google-fonts/kerning-readiness.md`; `documentation/google-fonts/kerning-proof-review.md` |",
        f"| Resolve or intentionally keep PUA and unreachable helper glyphs. | {table_state('Glyph reachability', final_blockers)} | `documentation/google-fonts/glyph-reachability.md` |",
        "",
        "## Packaging And Handoff",
        "",
        "| Action | Current state | Evidence |",
        "| --- | --- | --- |",
        f"| {placeholder_action(final_blockers)} | {table_state('Placeholder strings', final_blockers)} | `documentation/google-fonts/open-placeholder-audit.md` |",
        f"| Replace the Packager starter `METADATA.pb` with final downstream metadata and restore API auth. | {table_state('Package dry-run readiness', final_blockers)} | `documentation/google-fonts/downstream-metadata-diff.md` |",
        f"| Align Git/GitHub identity before downstream commits. | {table_state('PR identity and auth', final_blockers)} | `documentation/google-fonts/pr-identity-readiness.md`; `documentation/google-fonts/downstream-pr-readiness.md` |",
        f"| Create the final release/archive source package for Packager. | {table_state('Packager source files', final_blockers)}; release/archive source mode: `{source_mode}`; archive must include currently untracked package files: {release_archive_untracked}; `source.config_yaml` review: {config_yaml_review} | `documentation/google-fonts/packager-source-strategy.md` |",
        f"| Publish the final GitHub release asset after the final source commit and tag. | {table_state('GitHub release draft', final_blockers)} | `documentation/google-fonts/github-release-draft.md` |",
        f"| Prepare the Google Fonts designer profile request for `Eli Heuer`. | {table_state('Designer profile', final_blockers)} | `documentation/google-fonts/designer-profile-package-draft.md` |",
        f"| Clean or review the local `google/fonts` fork before the final package pass. | {table_state('Local google/fonts fork', final_blockers)} | `documentation/google-fonts/package-dry-run-readiness.md` |",
        f"| Keep Add Font issue and submission handoff synchronized with generated evidence. | {table_state('Submission handoff', final_blockers)} | `documentation/google-fonts/submission-handoff-readiness.md` |",
        "",
        "## Run Order",
        "",
        "1. Record the remaining maintainer decisions in `documentation/google-fonts/google-fonts-decisions.md`.",
        "2. Apply the PUA, kerning, and final release metadata decisions to source and package-preview files.",
        "3. Complete the remaining drawing/source blockers by reviewing the Arabic visual packet and recording each row as pass, fix-needed, or deferred.",
        "4. During Arabic hand review, start with `documentation/glyph-review/arabic-drawing-session-checklist.md`, then use `documentation/glyph-review/arabic-current-review-worksheet.md` for the current five-row fill-in sheet, `documentation/glyph-review/arabic-first-review-batch.md` for the structure/wrong-glyph packet, `documentation/glyph-review/arabic-first-batch-source-checkpoint.md` for the first-batch Regular/Bold source checkpoint, `documentation/glyph-review/arabic-pending-source-checkpoint.md` for all unresolved review-row source targets, and `documentation/glyph-review/arabic-manual-edit-targets.md` to jump from any `fix-needed` row to the matching Regular and Bold GLIF files.",
        "5. Run `make kerning-proof-check`, run `make kerning-proof-review-check`, and review `documentation/google-fonts/gftools-qa/Proof` after kerning changes or explicit deferral.",
        "6. Create the final `v1.000` release archive with every file listed in downstream `source.files`.",
        "7. Review `documentation/google-fonts/github-release-draft.md`, then publish the final GitHub release asset after the final tag is pushed.",
        "8. Prepare the `Eli Heuer` designer-profile link, biography, and square image, or record a profile-request plan.",
        "9. Align source-repo and `google/fonts` fork Git names, GitHub auth, and API credentials with `documentation/google-fonts/pr-identity-readiness.md` before downstream commits.",
        "10. Run `make preflight` so the build, proof PDF, generated reports, and local gate stay synchronized.",
        "11. Run `make downstream-metadata-check`; when it is ready, apply the checked preview to downstream `ofl/virtuagrotesk/METADATA.pb`.",
        "12. Rerun `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` and review the generated package.",
        "13. Open or update the Google Fonts issue and downstream PR only after the no-PR package is reviewed.",
        "",
        "References:",
        "",
        "- https://googlefonts.github.io/gf-guide/onboarding.html",
        "- https://googlefonts.github.io/gf-guide/upstream.html",
        "- https://googlefonts.github.io/gf-guide/package.html",
        "- https://googlefonts.github.io/gf-guide/metadata.html",
        "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_next_actions.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
