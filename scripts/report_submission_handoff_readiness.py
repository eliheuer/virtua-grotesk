#!/usr/bin/env python3
"""Generate a Google Fonts submission handoff consistency report."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/submission-handoff-readiness.md")
HANDOFF = Path("documentation/google-fonts-submission-handoff.md")


def read_text(relative: Path | str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def fontspector_counts(report_text: str) -> tuple[int, int, int, int, int]:
    match = re.search(
        r"### Summary\s*\n\s*\|[^\n]*FAIL[^\n]*\|\s*\n\|[^\n]*\|\s*\n"
        r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
        report_text,
        flags=re.MULTILINE,
    )
    if not match:
        return (0, 0, 0, 0, 0)
    return tuple(int(value) for value in match.groups())  # type: ignore[return-value]


def arabic_category_counts(report_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for heading in [
        "Arabic letters",
        "Arabic marks",
        "Arabic numbers",
        "Arabic punctuation and symbols",
        "Shared punctuation and symbols",
    ]:
        pattern = rf"## {re.escape(heading)}\s*\n\s*Missing: (\d+)"
        counts[heading] = first_int(pattern, report_text)
    return counts


def markdown_report() -> str:
    handoff = read_text(HANDOFF)
    template = read_text("documentation/google-fonts-add-font-template-audit.md")
    issue_draft = read_text("documentation/google-fonts-add-font-issue-draft.md")
    generated = read_text("documentation/generated-font-metadata.md")
    fontspector = read_text("documentation/fontspector-googlefonts-report.md")
    latin = read_text("documentation/missing-gf-latin-core.md")
    arabic = read_text("documentation/missing-gf-arabic-core.md")
    arabic_review = read_text("documentation/arabic-review-packet.md")
    decisions = read_text("documentation/google-fonts-decisions.md")
    release = read_text("documentation/release-metadata.md")
    release_source = read_text("documentation/release-source-readiness.md")
    release_archive = read_text("documentation/release-archive-manifest.md")
    github_release_draft = read_text("documentation/github-release-draft.md")
    github_release_notes = read_text("documentation/github-release-notes.md")
    decision_readiness = read_text("documentation/decision-readiness.md")
    upstream_structure = read_text("documentation/upstream-structure-readiness.md")
    package_source = read_text("documentation/package-source-files-audit.md")
    package_dry_run = read_text("documentation/package-dry-run-readiness.md")
    downstream_metadata = read_text("documentation/downstream-metadata-readiness.md")
    article = read_text("documentation/article-readiness.md")
    recent_packages = read_text("documentation/recent-google-fonts-packages.md")
    kerning = read_text("documentation/kerning-readiness.md")
    kerning_proof_review = read_text("documentation/kerning-proof-review.md")

    fail, warn, info, pass_count, skip = fontspector_counts(fontspector)
    latin_missing = first_int(r"Missing codepoints: (\d+)", latin)
    arabic_counts = arabic_category_counts(arabic)
    arabic_missing_total = first_int(r"Missing codepoints: (\d+)", arabic)
    source_version = re.search(r"Source version: `([^`]+)`", release)
    version = source_version.group(1) if source_version else ""
    template_labels = re.search(r"Default labels: `([^`]+)`", template)
    labels = template_labels.group(1) if template_labels else ""
    dry_run_first_blocker_match = re.search(r"First blocker: ([^\n]+)", package_dry_run)
    dry_run_first_blocker = dry_run_first_blocker_match.group(1) if dry_run_first_blocker_match else ""
    dry_run_blocking_findings_match = re.search(r"Blocking findings: ([^\n]+)", package_dry_run)
    dry_run_blocking_findings = dry_run_blocking_findings_match.group(1) if dry_run_blocking_findings_match else ""
    dry_run_can_reach_match = re.search(r"Wrapper can reach Packager: (yes|no)", package_dry_run)
    dry_run_can_reach = dry_run_can_reach_match.group(1) if dry_run_can_reach_match else ""
    kerning_proof_output_match = re.search(r"Latest `gftools qa --proof` HTML output present: (yes|no)", kerning)
    kerning_proof_output = kerning_proof_output_match.group(1) if kerning_proof_output_match else ""
    kerning_proof_instances_match = re.search(r"Latest proof covers expected instances: (yes|no)", kerning)
    kerning_proof_instances = kerning_proof_instances_match.group(1) if kerning_proof_instances_match else ""
    kerning_proof_html_count_match = re.search(r"Latest proof HTML file count: (\d+)", kerning)
    kerning_proof_html_count = kerning_proof_html_count_match.group(1) if kerning_proof_html_count_match else ""
    kerning_proof_review_expected_match = re.search(r"Expected HTML proofs present: ([^\n]+)", kerning_proof_review)
    kerning_proof_review_expected = kerning_proof_review_expected_match.group(1) if kerning_proof_review_expected_match else ""
    kerning_proof_review_instances_match = re.search(r"Expected instances covered: (yes|no)", kerning_proof_review)
    kerning_proof_review_instances = (
        kerning_proof_review_instances_match.group(1) if kerning_proof_review_instances_match else ""
    )
    dry_run_inputs_tracked_match = re.search(r"Required local package inputs tracked: ([^\n]+)", package_dry_run)
    dry_run_inputs_tracked = dry_run_inputs_tracked_match.group(1) if dry_run_inputs_tracked_match else ""
    dry_run_inputs_untracked_match = re.search(r"Required local package inputs untracked: (\d+)", package_dry_run)
    dry_run_inputs_untracked = dry_run_inputs_untracked_match.group(1) if dry_run_inputs_untracked_match else ""
    dry_run_untracked_mode_blockers = all(
        phrase in package_dry_run
        for phrase in [
            "public branch must expose untracked source files",
            "release/archive must include untracked local source files",
            "build-from-source inputs are missing, ignored, or untracked",
        ]
    )
    open_decisions = len(re.findall(r"^Status: open$", decisions, flags=re.MULTILINE))
    checkbox_count = len(re.findall(r"^\d+\. ", template, flags=re.MULTILINE))
    handoff_checkbox_count = len(re.findall(r"^- \[ \] ", handoff, flags=re.MULTILINE))
    issue_draft_checkbox_count = len(re.findall(r"^- \[ \] ", issue_draft, flags=re.MULTILINE))
    handoff_expected_fontspector = f"{fail} FAIL, {warn} WARN, {pass_count} PASS"
    issue_draft_checks = {
        "title": "Add Virtua Grotesk" in issue_draft,
        "labels": bool(labels and labels in issue_draft),
        "template_status": "Template checkout status: `## main...origin/main`" in issue_draft,
        "upstream_aligned": "Alignment with `upstream/main`: `0 ahead, 0 behind`" in issue_draft,
        "origin_aligned": "Alignment with `origin/main`: `0 ahead, 0 behind`" in issue_draft,
        "repo_url_current": "https://github.com/eliheuer/virtua-grotesk" in issue_draft,
        "checkbox_count": issue_draft_checkbox_count == checkbox_count,
        "unchecked": "- [x]" not in issue_draft,
        "draft_statuses": issue_draft.count("Draft status:") == checkbox_count,
        "latin_gap": f"GF Latin Core missing codepoints: {latin_missing}" in issue_draft,
        "arabic_gap": f"GF Arabic Core missing codepoints: {arabic_missing_total}" in issue_draft,
        "arabic_refs": (
            "documentation/arabic-review-packet.md" in issue_draft
            and
            "documentation/missing-gf-arabic-core.md" in issue_draft
            and "documentation/arabic-mark-readiness.md" in issue_draft
            and "documentation/arabic-shaping-smoke-test.md" in issue_draft
        ),
        "decision_warning_status": "## Decision-Linked Warning Status" in issue_draft,
        "decision_warning_refs": (
            "documentation/vendor-id-readiness.md" in issue_draft
            and "documentation/kerning-readiness.md" in issue_draft
            and "documentation/avar-readiness.md" in issue_draft
            and "documentation/pua-scope.md" in issue_draft
            and "documentation/fontspector-warnings.md" in issue_draft
        ),
        "metadata_apply_gate": (
            "Downstream metadata preview ready to apply:" in issue_draft
            and "Downstream metadata apply blockers:" in issue_draft
            and "documentation/downstream-metadata-diff.md" in issue_draft
        ),
        "fontspector": f"{fail} FAIL results" in issue_draft,
        "image": "documentation/readme-specimen.png" in issue_draft,
        "kerning_proof": (
            "GF visual proof output:" in issue_draft
            and "proof covers expected instances:" in issue_draft
        ),
        "kerning_proof_review": "documentation/kerning-proof-review.md" in issue_draft,
        "maintenance_commitment": (
            "maintain the repository and participate in the onboarding process" in issue_draft
            and "Maintainer confirmation required before opening the issue." in issue_draft
        ),
    }
    decided_handoff_checks = {
        "vendor_id": (
            "Vendor ID is decided as `FTGD` for Font Garden" in handoff
            and "documentation/vendor-id-readiness.md" in handoff
        ),
        "authorship_name_url": (
            "Author/contact display, copyright-authorship statement, AI-use disclosure,\n"
            "  namecheck result, and public upstream URL are decided" in handoff
            and "documentation/authorship-disclosure-readiness.md" in handoff
            and "documentation/family-name-readiness.md" in handoff
            and "documentation/public-upstream-readiness.md" in handoff
        ),
        "article_flow": (
            "Keep the decided Article flow in the downstream package" in handoff
            and "documentation/article-readiness.md" in handoff
        ),
        "stale_vendor_id": "Confirm vendor ID." not in handoff,
        "stale_authorship_url": "Confirm author/contact lines" not in handoff,
        "stale_article_url": "after the public upstream URL is confirmed" not in handoff,
    }
    maintenance_checks = {
        "template_requirement": "maintain the repository" in template,
        "handoff_checkbox": "will maintain the repository and participate in the onboarding process" in handoff,
        "unchecked": "- [x]" not in issue_draft and "- [x]" not in handoff,
    }

    arabic_matches = {
        heading: f"- {heading}: {count}" in handoff
        for heading, count in arabic_counts.items()
    }
    required_refs = [
        "documentation/google-fonts-decisions.md",
        "documentation/decision-readiness.md",
        "documentation/google-fonts-add-font-template-audit.md",
        "documentation/google-fonts-add-font-issue-draft.md",
        "documentation/fontspector-googlefonts-report.md",
        "documentation/arabic-review-packet.md",
        "documentation/missing-gf-arabic-core.md",
        "documentation/missing-gf-latin-core.md",
        "documentation/release-source-readiness.md",
        "documentation/release-archive-manifest.md",
        "documentation/github-release-draft.md",
        "documentation/github-release-notes.md",
        "documentation/upstream-structure-readiness.md",
        "documentation/google-fonts-package-checklist.md",
        "documentation/package-source-files-audit.md",
        "documentation/package-dry-run-readiness.md",
        "documentation/google-fonts-metadata-review.md",
        "documentation/downstream-metadata-readiness.md",
        "documentation/downstream-metadata-diff.md",
        "documentation/downstream-pr-readiness.md",
        "documentation/google-fonts-language-metadata.md",
        "documentation/google-fonts-downstream-package-preview.md",
        "documentation/article-readiness.md",
        "documentation/authorship-disclosure-readiness.md",
        "documentation/pr-identity-readiness.md",
        "documentation/designer-profile-readiness.md",
        "documentation/designer-profile-package-draft.md",
        "documentation/drawbot-runtime-readiness.md",
        "documentation/local-workflow-readiness.md",
        "documentation/recent-google-fonts-packages.md",
        "documentation/vendor-id-readiness.md",
        "documentation/kerning-readiness.md",
        "documentation/kerning-proof-review.md",
        "documentation/avar-readiness.md",
        "documentation/pua-scope.md",
        "documentation/glyph-reachability.md",
        "documentation/numeric-feature-readiness.md",
        "documentation/fontspector-warnings.md",
        "documentation/final-submission-blockers.md",
        "documentation/next-actions.md",
    ]

    lines = [
        "# Submission Handoff Readiness",
        "",
        "This generated report checks the draft Google Fonts issue and packaging",
        "handoff against the current generated reports and local Add Font issue",
        "template audit. It is meant to catch stale handoff text before opening",
        "the issue or downstream package PR.",
        "",
        "## Summary",
        "",
        f"- Handoff file: `{HANDOFF}`",
        f"- Template default labels match handoff: {yes_no(labels in handoff)}",
        f"- Template requirement checkbox count: {checkbox_count}",
        f"- Handoff requirement checkbox count: {handoff_checkbox_count}",
        f"- Issue draft requirement checkbox count: {issue_draft_checkbox_count}",
        f"- Issue draft title is current: {yes_no(issue_draft_checks['title'])}",
        f"- Issue draft labels are current: {yes_no(issue_draft_checks['labels'])}",
        f"- Issue draft template checkout status is current: {yes_no(issue_draft_checks['template_status'])}",
        f"- Issue draft template is aligned with upstream/main: {yes_no(issue_draft_checks['upstream_aligned'])}",
        f"- Issue draft template is aligned with origin/main: {yes_no(issue_draft_checks['origin_aligned'])}",
        f"- Issue draft includes current public URL: {yes_no(issue_draft_checks['repo_url_current'])}",
        f"- Issue draft leaves boxes unchecked: {yes_no(issue_draft_checks['unchecked'])}",
        f"- Issue draft status notes match checkbox count: {yes_no(issue_draft_checks['draft_statuses'])}",
        f"- Issue draft includes current Latin Core gap: {yes_no(issue_draft_checks['latin_gap'])}",
        f"- Issue draft includes current Arabic Core gap: {yes_no(issue_draft_checks['arabic_gap'])}",
        f"- Issue draft references Arabic readiness reports: {yes_no(issue_draft_checks['arabic_refs'])}",
        f"- Issue draft includes decision-linked warning status: {yes_no(issue_draft_checks['decision_warning_status'])}",
        f"- Issue draft references decision-warning reports: {yes_no(issue_draft_checks['decision_warning_refs'])}",
        f"- Issue draft includes downstream metadata apply gate: {yes_no(issue_draft_checks['metadata_apply_gate'])}",
        f"- Issue draft includes current Fontspector FAIL count: {yes_no(issue_draft_checks['fontspector'])}",
        f"- Issue draft includes GF visual kerning proof status: {yes_no(issue_draft_checks['kerning_proof'])}",
        f"- Issue draft references GF visual proof review packet: {yes_no(issue_draft_checks['kerning_proof_review'])}",
        f"- Issue draft tracks repository maintenance commitment: {yes_no(issue_draft_checks['maintenance_commitment'])}",
        f"- Issue draft points to specimen image: {yes_no(issue_draft_checks['image'])}",
        f"- Handoff points to generated Add Font issue draft: {yes_no('documentation/google-fonts-add-font-issue-draft.md' in handoff)}",
        f"- Handoff includes current version `{version}`: {yes_no(bool(version and version in handoff))}",
        f"- Handoff includes current Fontspector summary: {yes_no(handoff_expected_fontspector in handoff)}",
        f"- Handoff includes current Latin Core gap: {yes_no(f'GF Latin Core missing codepoints: {latin_missing}' in handoff)}",
        f"- Handoff includes current Arabic category gaps: {yes_no(all(arabic_matches.values()))}",
        f"- Handoff records decided Vendor ID state: {yes_no(decided_handoff_checks['vendor_id'])}",
        f"- Handoff records decided authorship/namecheck/public URL state: {yes_no(decided_handoff_checks['authorship_name_url'])}",
        f"- Handoff records decided Article flow: {yes_no(decided_handoff_checks['article_flow'])}",
        f"- Handoff avoids stale Vendor ID confirmation blocker: {yes_no(decided_handoff_checks['stale_vendor_id'])}",
        f"- Handoff avoids stale authorship/public URL confirmation blocker: {yes_no(decided_handoff_checks['stale_authorship_url'])}",
        f"- Handoff avoids stale Article URL confirmation blocker: {yes_no(decided_handoff_checks['stale_article_url'])}",
        f"- Template includes repository maintenance checkbox: {yes_no(maintenance_checks['template_requirement'])}",
        f"- Handoff includes repository maintenance checkbox: {yes_no(maintenance_checks['handoff_checkbox'])}",
        f"- Repository maintenance confirmation remains unchecked until issue opening: {yes_no(maintenance_checks['unchecked'])}",
        f"- Handoff points to Arabic review packet: {yes_no('documentation/arabic-review-packet.md' in handoff)}",
        f"- Handoff points to decision readiness report: {yes_no('documentation/decision-readiness.md' in handoff)}",
        f"- Handoff points to release/source readiness report: {yes_no('documentation/release-source-readiness.md' in handoff)}",
        f"- Handoff points to release archive manifest: {yes_no('documentation/release-archive-manifest.md' in handoff)}",
        f"- Handoff points to GitHub release draft and notes: {yes_no('documentation/github-release-draft.md' in handoff and 'documentation/github-release-notes.md' in handoff)}",
        f"- Handoff points to upstream structure readiness report: {yes_no('documentation/upstream-structure-readiness.md' in handoff)}",
        f"- Handoff points to package source-file audit: {yes_no('documentation/package-source-files-audit.md' in handoff)}",
        f"- Handoff points to package dry-run readiness report: {yes_no('documentation/package-dry-run-readiness.md' in handoff)}",
        f"- Handoff points to downstream metadata readiness report: {yes_no('documentation/downstream-metadata-readiness.md' in handoff)}",
        f"- Handoff points to Article readiness report: {yes_no('documentation/article-readiness.md' in handoff)}",
        f"- Handoff points to authorship and AI disclosure report: {yes_no('documentation/authorship-disclosure-readiness.md' in handoff)}",
        f"- Handoff points to PR identity readiness report: {yes_no('documentation/pr-identity-readiness.md' in handoff)}",
        f"- Handoff points to designer profile reports: {yes_no('documentation/designer-profile-readiness.md' in handoff and 'documentation/designer-profile-package-draft.md' in handoff)}",
        f"- Handoff points to DrawBot fork runtime report: {yes_no('documentation/drawbot-runtime-readiness.md' in handoff)}",
        f"- Handoff points to local workflow readiness report: {yes_no('documentation/local-workflow-readiness.md' in handoff)}",
        f"- Handoff points to recent-package audit: {yes_no('documentation/recent-google-fonts-packages.md' in handoff)}",
        f"- Recent-package audit includes generated Packager merge evidence: {yes_no('## Recent Packager Merges' in recent_packages and 'gftools_packager_ofl_' in recent_packages)}",
        f"- Handoff points to decision-linked warning reports: {yes_no(all(ref in handoff for ref in ['documentation/vendor-id-readiness.md', 'documentation/kerning-readiness.md', 'documentation/kerning-proof-review.md', 'documentation/avar-readiness.md', 'documentation/pua-scope.md', 'documentation/glyph-reachability.md', 'documentation/numeric-feature-readiness.md', 'documentation/fontspector-warnings.md']))}",
        f"- Handoff points to GF visual proof review packet: {yes_no('documentation/kerning-proof-review.md' in handoff)}",
        f"- Handoff mentions decision-linked warning buckets: {yes_no('decision-linked warning buckets' in handoff and 'vendor ID, kerning, `avar`' in handoff and 'PUA/reachability' in handoff)}",
        f"- Kerning report has current GF visual proof output: {kerning_proof_output}",
        f"- Kerning report proof covers expected instances: {kerning_proof_instances}",
        f"- Kerning proof review packet has expected proof files: {kerning_proof_review_expected}",
        f"- Kerning proof review packet covers expected instances: {kerning_proof_review_instances}",
        f"- Handoff points to final blocker summary: {yes_no('documentation/final-submission-blockers.md' in handoff)}",
        f"- Handoff mentions expected Packager branch: {yes_no('gftools_packager_ofl_virtuagrotesk' in handoff)}",
        f"- Handoff mentions downstream PR title/body/scope: {yes_no('Virtua Grotesk : 1.000 added' in handoff and 'Taken from the upstream repo <repo-url> at commit <commit-url>.' in handoff and 'one changed directory' in handoff and 'compare across forks' in handoff)}",
        f"- Handoff mentions Packager source-mode options: {yes_no('GFT_PACKAGER_SOURCE_MODE=latest-release' in handoff and 'GFT_PACKAGER_SOURCE_MODE=build-from-source' in handoff)}",
        f"- Handoff mentions latest-release archive URL shape: {yes_no('GitHub release download URL ending in `.zip`' in handoff and 'final GitHub release download `.zip` asset' in handoff)}",
        f"- Handoff mentions GitHub CLI auth refresh: {yes_no('gh auth login -h github.com' in handoff)}",
        f"- Handoff mentions current package dry-run first blocker: {yes_no(bool(dry_run_first_blocker and dry_run_first_blocker in handoff))}",
        f"- Handoff mentions current package dry-run blocking findings: {yes_no(bool(dry_run_blocking_findings and dry_run_blocking_findings in handoff))}",
        f"- Handoff mentions tracked package input count: {yes_no(bool(dry_run_inputs_tracked and f'only {dry_run_inputs_tracked.replace(' / ', '/')} are tracked by git' in handoff))}",
        f"- Handoff mentions untracked package input count: {yes_no(bool(dry_run_inputs_untracked and f'{dry_run_inputs_untracked}/5 are currently untracked' in handoff))}",
        f"- Handoff mentions source-mode untracked input blockers: {yes_no(dry_run_untracked_mode_blockers and 'default branch packaging must expose untracked `source.files`' in handoff and 'release/archive\npackaging must include those untracked local source files' in handoff and 'build-from-source\npackaging must make `sources/config.yaml` and `requirements.txt` public and\ntracked' in handoff)}",
        f"- Handoff mentions downstream metadata check helper: {yes_no('make downstream-metadata-check' in handoff and 'scripts/prepare_downstream_metadata.py --apply' in handoff)}",
        f"- Handoff mentions upstream/source availability blocker: {yes_no('Packager cannot fetch' in handoff and 'branch `main` yet' in handoff)}",
        f"- Handoff mentions prioritized decision packet: {yes_no('prioritized' in handoff and 'question packet' in handoff)}",
        f"- Handoff mentions local drawbot-skia fork: {yes_no('eliheuer/drawbot-skia' in handoff)}",
        f"- Decision readiness has mapped open questions: {yes_no(re.search(r'Open decisions with matching question prompts: (\d+) / \1', decision_readiness) is not None)}",
        f"- Upstream structure has all mandatory paths: {yes_no('Mandatory upstream paths present: 11 / 11' in upstream_structure)}",
        f"- Package source audit validates destination mapping: {yes_no('Destination mapping matches expected downstream layout: yes' in package_source)}",
        f"- Release archive manifest validates local review zip: {yes_no('Local release archive hashes match source files: yes' in release_archive)}",
        f"- Downstream metadata preview has expected source block: {yes_no('Source block has repository, commit, archive_url, and branch fields: yes' in downstream_metadata)}",
        f"- Downstream metadata report validates latest-release archive URL shape: {yes_no('`source.archive_url` is GitHub release download `.zip`: yes' in downstream_metadata)}",
        f"- Decision log still has open decisions: {yes_no(open_decisions > 0)}",
        f"- Article placeholder URL still present: {yes_no('Placeholder upstream URL still present: yes' in article)}",
        f"- Release/source report says tree is clean: {yes_no('Working tree clean: yes' in release_source)}",
        "",
        "## Current Values Expected In Handoff",
        "",
        "| Field | Current value | Present in handoff |",
        "| --- | --- | --- |",
        f"| Add Font labels | `{labels}` | {yes_no(labels in handoff)} |",
        f"| version | `{version}` | {yes_no(bool(version and version in handoff))} |",
        f"| Fontspector | `{handoff_expected_fontspector}` | {yes_no(handoff_expected_fontspector in handoff)} |",
        f"| package dry-run reaches Packager | `{dry_run_can_reach}` | {yes_no(bool(dry_run_can_reach and f'Wrapper can reach Packager: {dry_run_can_reach}' in handoff))} |",
        f"| package dry-run first blocker | `{dry_run_first_blocker}` | {yes_no(bool(dry_run_first_blocker and dry_run_first_blocker in handoff))} |",
        f"| package dry-run blocking findings | `{dry_run_blocking_findings}` | {yes_no(bool(dry_run_blocking_findings and dry_run_blocking_findings in handoff))} |",
        f"| package inputs tracked | `{dry_run_inputs_tracked}` | {yes_no(bool(dry_run_inputs_tracked and f'only {dry_run_inputs_tracked.replace(' / ', '/')} are tracked by git' in handoff))} |",
        f"| package inputs untracked | `{dry_run_inputs_untracked}` | {yes_no(bool(dry_run_inputs_untracked and f'{dry_run_inputs_untracked}/5 are currently untracked' in handoff))} |",
        f"| GF Latin Core missing | `{latin_missing}` | {yes_no(f'GF Latin Core missing codepoints: {latin_missing}' in handoff)} |",
        f"| GF visual kerning proof output | `{kerning_proof_output}` | {yes_no(bool(kerning_proof_output and 'documentation/kerning-readiness.md' in handoff))} |",
        f"| GF visual kerning proof HTML files | `{kerning_proof_html_count}` | {yes_no(bool(kerning_proof_html_count and 'documentation/kerning-readiness.md' in handoff))} |",
        f"| GF visual kerning proof instances | `{kerning_proof_instances}` | {yes_no(bool(kerning_proof_instances and 'documentation/kerning-readiness.md' in handoff))} |",
        f"| GF visual proof review packet files | `{kerning_proof_review_expected}` | {yes_no(bool(kerning_proof_review_expected and 'documentation/kerning-proof-review.md' in handoff))} |",
        f"| GF visual proof review packet instances | `{kerning_proof_review_instances}` | {yes_no(bool(kerning_proof_review_instances and 'documentation/kerning-proof-review.md' in handoff))} |",
    ]
    for heading, count in arabic_counts.items():
        lines.append(f"| {heading} | `{count}` | {yes_no(arabic_matches[heading])} |")

    lines.extend(
        [
            "",
            "## Current Values Expected In Issue Draft",
            "",
            "| Field | Expected value | Present in issue draft |",
            "| --- | --- | --- |",
            f"| title | `Add Virtua Grotesk` | {yes_no(issue_draft_checks['title'])} |",
            f"| labels | `{labels}` | {yes_no(issue_draft_checks['labels'])} |",
            f"| template checkout status | `## main...origin/main` | {yes_no(issue_draft_checks['template_status'])} |",
            f"| upstream/main alignment | `0 ahead, 0 behind` | {yes_no(issue_draft_checks['upstream_aligned'])} |",
            f"| origin/main alignment | `0 ahead, 0 behind` | {yes_no(issue_draft_checks['origin_aligned'])} |",
            f"| requirement checkboxes | `{checkbox_count}` | {yes_no(issue_draft_checks['checkbox_count'])} |",
            f"| unchecked boxes | `no - [x] entries` | {yes_no(issue_draft_checks['unchecked'])} |",
            f"| Draft status notes | `{checkbox_count}` | {yes_no(issue_draft_checks['draft_statuses'])} |",
            f"| GF Latin Core missing | `{latin_missing}` | {yes_no(issue_draft_checks['latin_gap'])} |",
            f"| GF Arabic Core missing | `{arabic_missing_total}` | {yes_no(issue_draft_checks['arabic_gap'])} |",
            f"| Arabic readiness report references | `review packet, coverage, marks, shaping` | {yes_no(issue_draft_checks['arabic_refs'])} |",
            f"| decision-linked warning status | `vendor, kerning, avar, PUA/reachability` | {yes_no(issue_draft_checks['decision_warning_status'])} |",
            f"| decision-warning report references | `vendor, kerning, avar, PUA, warnings` | {yes_no(issue_draft_checks['decision_warning_refs'])} |",
            f"| GF visual proof review packet | `documentation/kerning-proof-review.md` | {yes_no(issue_draft_checks['kerning_proof_review'])} |",
            f"| downstream metadata apply gate | `ready/apply blockers` | {yes_no(issue_draft_checks['metadata_apply_gate'])} |",
            f"| repository maintenance commitment | `maintain the repository` checkbox and status note | {yes_no(issue_draft_checks['maintenance_commitment'])} |",
            f"| Fontspector FAIL count | `{fail}` | {yes_no(issue_draft_checks['fontspector'])} |",
            "| image | `documentation/readme-specimen.png` | "
            f"{yes_no(issue_draft_checks['image'])} |",
        ]
    )

    lines.extend(
        [
            "",
            "## Required Report References",
            "",
            "| Reference | Present in handoff |",
            "| --- | --- |",
        ]
    )
    for ref in required_refs:
        lines.append(f"| `{ref}` | {yes_no(ref in handoff)} |")

    lines.extend(
        [
            "",
            "## Apply Before Opening The Issue",
            "",
            "- Regenerate this report with `make preflight` after any drawing,",
            "  metadata, issue-template, or packaging-source change.",
            "- Update `documentation/google-fonts-submission-handoff.md` until all",
            "  current values and report references match.",
            "- Regenerate `documentation/google-fonts-add-font-issue-draft.md` from",
            "  the current local `google/fonts` Add Font template before opening",
            "  the issue.",
            "- Do not check the Add Font requirement boxes until maintainer decisions",
            "  and drawing/source blockers have been resolved or explicitly accepted.",
            "- Run `make downstream-metadata-check` before applying final metadata",
            "  into the local `google/fonts` fork for a no-PR Packager rerun.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "",
        ]
    )
    # Keep generated metadata tied to this report even though the handoff only needs the version.
    assert "## Technical Metadata" in generated
    assert "# Arabic Review Packet" in arabic_review
    assert "# Kerning Proof Review" in kerning_proof_review
    assert "# Google Fonts Open Decisions" in decisions
    assert "# Recent Google Fonts Package Audit" in recent_packages
    assert "# GitHub Release Draft" in github_release_draft
    assert "Virtua Grotesk 1.000 release candidate" in github_release_notes
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_submission_handoff_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
