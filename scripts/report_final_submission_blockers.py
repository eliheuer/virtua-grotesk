#!/usr/bin/env python3
"""Generate a concise final Google Fonts submission blocker report."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/final-submission-blockers.md")


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def yes_no_from_line(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else "unknown"


def text_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def markdown_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def missing_designer_profile_names(report_text: str) -> set[str]:
    names: set[str] = set()
    for heading in ("Candidate Designer Profiles", "Final Metadata Designer Entity Status"):
        section = markdown_section(report_text, heading)
        for line in section.splitlines():
            if "| missing |" not in line:
                continue
            match = re.search(r"\| `([^`]+)` \|", line)
            if match and match.group(1) != "none":
                names.add(match.group(1))
    return names


def fontspector_fail_count(report_text: str) -> int:
    match = re.search(
        r"### Summary\s*\n\s*\|[^\n]*FAIL[^\n]*\|\s*\n\|[^\n]*\|\s*\n\|\s*(\d+)\s*\|",
        report_text,
        flags=re.MULTILINE,
    )
    return int(match.group(1)) if match else 0


def contour_source_finding_count(report_text: str) -> tuple[int, int]:
    rows = re.findall(r"^\| `([^`]+)` \|", report_text, flags=re.MULTILINE)
    return len(set(rows)), len(rows)


def contour_decision_counts(report_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for label in ("Pending", "Fix-now", "Fixed", "Accepted", "Deferred"):
        match = re.search(rf"^- {label}: (\d+)$", report_text, flags=re.MULTILINE)
        counts[label.lower()] = int(match.group(1)) if match else 0
    return counts


def decision_counts(decisions_text: str) -> tuple[int, int]:
    open_count = len(re.findall(r"^Status: open$", decisions_text, flags=re.MULTILINE))
    decided_count = len(re.findall(r"^Status: decided$", decisions_text, flags=re.MULTILINE))
    return open_count, decided_count


def decision_headings(decisions_text: str) -> list[str]:
    headings: list[str] = []
    current_heading = ""
    for line in decisions_text.splitlines():
        if line.startswith("## "):
            current_heading = line[3:]
        elif line == "Status: open" and current_heading:
            headings.append(current_heading)
    return headings


def markdown_report() -> str:
    decisions_text = read_text("documentation/google-fonts/google-fonts-decisions.md")
    decision_readiness_text = read_text("documentation/google-fonts/decision-readiness.md")
    placeholder_text = read_text("documentation/google-fonts/open-placeholder-audit.md")
    package_source_text = read_text("documentation/google-fonts/package-source-files-audit.md")
    packager_source_strategy_text = read_text("documentation/google-fonts/packager-source-strategy.md")
    downstream_metadata_text = read_text("documentation/google-fonts/downstream-metadata-readiness.md")
    article_text = read_text("documentation/google-fonts/article-readiness.md")
    kerning_text = read_text("documentation/google-fonts/kerning-readiness.md")
    kerning_proof_review_text = read_text("documentation/google-fonts/kerning-proof-review.md")
    vendor_text = read_text("documentation/google-fonts/vendor-id-readiness.md")
    release_metadata_text = read_text("documentation/google-fonts/release-metadata.md")
    release_source_text = read_text("documentation/google-fonts/release-source-readiness.md")
    release_archive_text = read_text("documentation/google-fonts/release-archive-manifest.md")
    github_release_text = read_text("documentation/google-fonts/github-release-draft.md")
    package_dry_run_text = read_text("documentation/google-fonts/package-dry-run-readiness.md")
    upstream_structure_text = read_text("documentation/google-fonts/upstream-structure-readiness.md")
    template_pr_text = read_text("documentation/google-fonts/google-fonts-template-and-pr-audit.md")
    recent_packages_text = read_text("documentation/google-fonts/recent-google-fonts-packages.md")
    add_font_template_text = read_text("documentation/google-fonts/google-fonts-add-font-template-audit.md")
    template_automation_text = read_text("documentation/google-fonts/project-template-automation-readiness.md")
    handoff_readiness_text = read_text("documentation/google-fonts/submission-handoff-readiness.md")
    designer_profile_text = read_text("documentation/google-fonts/designer-profile-readiness.md")
    authorship_text = read_text("documentation/google-fonts/authorship-disclosure-readiness.md")
    pr_identity_text = read_text("documentation/google-fonts/pr-identity-readiness.md")
    downstream_pr_text = read_text("documentation/google-fonts/downstream-pr-readiness.md")
    drawbot_runtime_text = read_text("documentation/google-fonts/drawbot-runtime-readiness.md")
    local_workflow_text = read_text("documentation/google-fonts/local-workflow-readiness.md")
    family_name_text = read_text("documentation/google-fonts/family-name-readiness.md")
    glyphset_text = read_text("documentation/google-fonts/gf-glyphset-readiness.md")
    language_metadata_text = read_text("documentation/google-fonts/google-fonts-language-metadata.md")
    reachability_text = read_text("documentation/google-fonts/glyph-reachability.md")
    numeric_text = read_text("documentation/google-fonts/numeric-feature-readiness.md")
    pua_text = read_text("documentation/google-fonts/pua-scope.md")
    arabic_source_text = read_text("documentation/glyph-review/arabic-source-work-checklist.md")
    arabic_manual_edit_targets_text = read_text("documentation/glyph-review/arabic-manual-edit-targets.md")
    arabic_mark_text = read_text("documentation/glyph-review/arabic-mark-readiness.md")
    arabic_shaping_text = read_text("documentation/glyph-review/arabic-shaping-smoke-test.md")
    warnings_text = read_text("documentation/google-fonts/fontspector-warnings.md")
    metadata_warning_probe_text = read_text("documentation/google-fonts/fontspector-metadata-warning-probe.md")
    zero_warning_text = read_text("documentation/google-fonts/fontspector-zero-warning-worklist.md")
    fontspector_text = read_text("documentation/google-fonts/fontspector-googlefonts-report.md")
    contour_text = read_text("documentation/google-fonts/fontspector-contour-count.md")
    contour_decision_text = read_text("documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md")

    open_decisions, decided_decisions = decision_counts(decisions_text)
    open_decision_headings = decision_headings(decisions_text)
    decision_questions = first_int(r"Decision question prompts: (\d+)", decision_readiness_text)
    decision_guided_questions = text_value(r"Decision question prompts with answer guidance: (\d+ / \d+)", decision_readiness_text)
    decision_mapped = text_value(r"Open decisions with matching question prompts: (\d+ / \d+)", decision_readiness_text)
    decision_surface_items = first_int(r"Open decision apply-to surface items: (\d+)", decision_readiness_text)
    decision_surface_paths = text_value(r"Open decision local path patterns present: (\d+ / \d+)", decision_readiness_text)
    placeholder_urls = first_int(r"Placeholder upstream URL occurrences: (\d+)", placeholder_text)
    pending_markers = first_int(r"Pending decision markers: (\d+)", placeholder_text)
    actionable_placeholder_urls = first_int(r"Actionable placeholder upstream URL occurrences: (\d+)", placeholder_text)
    actionable_pending_markers = first_int(r"Actionable pending decision markers: (\d+)", placeholder_text)
    generated_placeholder_echoes = first_int(r"Generated evidence echoes: (\d+)", placeholder_text)
    source_missing = first_int(r"Missing local files: (\d+)", package_source_text)
    source_ignored = first_int(r"Ignored local files: (\d+)", package_source_text)
    source_tracked = text_value(r"Tracked `source\.files`: ([^\n]+)", package_source_text)
    source_untracked = first_int(r"Untracked local `source\.files`: (\d+)", package_source_text)
    release_archive_action_plan = yes_no("## Selected Latest-Release Action Plan" in packager_source_strategy_text)
    release_archive_untracked = text_value(r"Release archive files currently present but untracked: ([^\n]+)", packager_source_strategy_text, "unknown")
    release_archive_ignored = text_value(r"Release archive files currently blocked by `\.gitignore`: ([^\n]+)", packager_source_strategy_text, "unknown")
    static_generated = text_value(r"Static TTFs generated locally for QA: ([^\n]+)", package_source_text)
    static_source_files = first_int(r"Static TTFs included in `source\.files`: (\d+)", package_source_text)
    static_destinations = first_int(r"Downstream `static/` destinations planned: (\d+)", package_source_text)
    static_omission_documented = yes_no_from_line(r"Static package omission documented in preview: (yes|no)", package_source_text)
    build_uses_builder = yes_no_from_line(r"Build script uses `gftools builder sources/config\.yaml`: (yes|no)", package_source_text)
    build_uses_metadata_fix = yes_no_from_line(r"Build script runs metadata post-processing: (yes|no)", package_source_text)
    builder_outputs_fonts = yes_no_from_line(r"Builder config outputs to `fonts/`: (yes|no)", package_source_text)
    build_inputs_tracked = text_value(r"Build-from-source inputs tracked: ([^\n]+)", package_source_text)
    metadata_pending = first_int(r"Pending or placeholder metadata lines: (\d+)", downstream_metadata_text)
    metadata_names_match = yes_no_from_line(r"Variable filename/name fields match built font: (yes|no)", downstream_metadata_text)
    article_placeholder_url = yes_no_from_line(r"Placeholder upstream URL still present: (yes|no)", article_text)
    article_words = first_int(r"Text length: (\d+) words", article_text)
    article_word_target = yes_no_from_line(r"Around 500 words target met: (yes|no)", article_text)
    article_primary_script = text_value(r"Primary script target from metadata: `([^`]+)`", article_text)
    article_localized_arabic = yes_no_from_line(r"Localized Arabic text present: (yes|no)", article_text)
    article_forbidden_tags = first_int(r"Forbidden HTML tags: (\d+)", article_text)
    article_images_exist = yes_no_from_line(r"Referenced images exist locally: (yes|no)", article_text)
    article_image_size = yes_no_from_line(r"Raster images within 1\.75 MB limit: (yes|no)", article_text)
    article_image_provenance = text_value(r"Article image sources covered by provenance file: (\d+ / \d+)", article_text)
    source_kerning_every_master = yes_no_from_line(r"Source kerning exists in every master: (yes|no)", kerning_text)
    static_gpos_kern = yes_no_from_line(r"All built static fonts expose GPOS `kern`: (yes|no)", kerning_text)
    kerning_warnings = first_int(r"Fontspector `gpos_kerning_info` warnings: (\d+)", kerning_text)
    kerning_proof_importable = yes_no_from_line(r"`gftools qa --proof` importable: (yes|no)", kerning_text)
    kerning_proof_output = yes_no_from_line(r"Latest `gftools qa --proof` HTML output present: (yes|no)", kerning_text)
    kerning_proof_instances = yes_no_from_line(r"Latest proof covers expected instances: (yes|no)", kerning_text)
    kerning_proof_review_files = text_value(r"Expected HTML proofs present: ([^\n]+)", kerning_proof_review_text)
    kerning_proof_review_status = text_value(r"Review status: ([^\n]+)", kerning_proof_review_text)
    vendor_source_values = text_value(r"Source UFO vendor IDs: (.+)", vendor_text)
    vendor_font_values = text_value(r"Generated font vendor IDs: (.+)", vendor_text)
    vendor_source_consistent = yes_no_from_line(r"Source UFO vendor IDs internally consistent: (yes|no)", vendor_text)
    vendor_font_consistent = yes_no_from_line(r"Generated font vendor IDs internally consistent: (yes|no)", vendor_text)
    vendor_aligned = yes_no_from_line(r"Source and generated vendor states aligned: (yes|no)", vendor_text)
    vendor_warnings = first_int(r"Fontspector `googlefonts/vendor_id` warnings: (\d+)", vendor_text)
    vendor_decision_status = text_value(r"Decision log status: ([a-z]+)", vendor_text)
    release_version = text_value(r"Source version: `([^`]+)`", release_metadata_text)
    release_tag = text_value(r"Suggested first-submission tag: `([^`]+)`", release_metadata_text)
    release_match = text_value(r"Built fonts match source version: (yes|no)", release_metadata_text)
    release_tag_exists = yes_no_from_line(r"Suggested tag exists locally: (yes|no)", release_source_text)
    release_dirty = yes_no_from_line(r"Working tree clean: (yes|no)", release_source_text)
    release_placeholder = yes_no_from_line(r"Placeholder upstream URL still present: (yes|no)", release_source_text)
    release_ignored_sources = first_int(r"Ignored/generated `source.files`: (\d+)", release_source_text)
    release_archive_inputs = text_value(r"Archive inputs present locally: ([^\n]+)", release_archive_text)
    release_archive_unsafe_sources = first_int(r"Unsafe `source.files` paths: (\d+)", release_archive_text)
    release_archive_duplicate_sources = first_int(r"Duplicate `source.files` paths: (\d+)", release_archive_text)
    release_archive_local_exists = yes_no_from_line(r"Local release archive exists: (yes|no)", release_archive_text)
    release_archive_contains = yes_no_from_line(r"Local release archive contains expected files: (yes|no)", release_archive_text)
    release_archive_unsafe_entries = yes_no_from_line(r"Local release archive has unsafe paths: (yes|no)", release_archive_text)
    release_archive_hashes = yes_no_from_line(r"Local release archive hashes match source files: (yes|no)", release_archive_text)
    release_archive_filename_match = yes_no_from_line(r"Preview archive filename matches local archive: (yes|no)", release_archive_text)
    release_archive_final_url = text_value(r"Final GitHub release archive URL recorded: ([^\n]+)", release_archive_text)
    github_release_tag = text_value(r"Release tag: `([^`]+)`", github_release_text)
    github_release_title = text_value(r"Release title: `([^`]+)`", github_release_text)
    github_release_command = yes_no("gh release create" in github_release_text)
    github_release_archive = text_value(r"Local archive: `([^`]+)`", github_release_text)
    github_release_notes = text_value(r"Release notes file: `([^`]+)`", github_release_text)
    github_release_notes_final = yes_no_from_line(r"Release notes source commit final: (yes|no)", github_release_text)
    github_release_archive_ok = yes_no_from_line(r"Local archive contains expected files: (yes|no)", github_release_text)
    github_release_hashes = yes_no_from_line(r"Local archive hashes match source files: (yes|no)", github_release_text)
    github_release_pending_commit = text_value(r"Downstream preview source commit: `([^`]+)`", github_release_text)
    dry_run_reaches_packager = yes_no_from_line(r"Wrapper can reach Packager: (yes|no)", package_dry_run_text)
    dry_run_first_blocker = text_value(r"First blocker: ([^\n]+)", package_dry_run_text)
    dry_run_blocking_findings = text_value(r"Blocking findings: ([^\n]+)", package_dry_run_text)
    dry_run_auth_ready = yes_no_from_line(r"GitHub API credentials ready: (yes|no)", package_dry_run_text)
    dry_run_inputs_ready = yes_no_from_line(r"Required local package inputs ready: (yes|no)", package_dry_run_text)
    gf_origin_slug = text_value(r"Origin GitHub repo: `([^`]+)`", package_dry_run_text)
    gf_upstream_slug = text_value(r"Upstream GitHub repo: `([^`]+)`", package_dry_run_text)
    gf_topology_ready = yes_no_from_line(r"google/fonts remote topology ready: (yes|no)", package_dry_run_text)
    gf_fork_exists = yes_no_from_line(r"Local google/fonts fork exists: (yes|no)", release_source_text)
    gf_fork_branch = text_value(r"Local google/fonts branch: `([^`]+)`", release_source_text)
    gf_fork_alignment = text_value(r"Local google/fonts main vs upstream/main: `([^`]+)`", release_source_text).replace("\t", "/")
    gf_fork_clean = yes_no_from_line(r"Local google/fonts worktree clean: (yes|no)", release_source_text)
    gf_dirty_outside = text_value(r"Dirty paths outside `ofl/virtuagrotesk`: (\d+)", package_dry_run_text)
    upstream_mandatory = text_value(r"Mandatory upstream paths present: (\d+ / \d+)", upstream_structure_text)
    upstream_sources = text_value(r"Active source inputs present: (\d+ / \d+)", upstream_structure_text)
    upstream_fonts_ignored = yes_no_from_line(r"Generated font outputs ignored by git: (yes|no)", upstream_structure_text)
    template_checked = "googlefonts/googlefonts-project-template" in template_pr_text
    template_automation_present = text_value(r"Optional template automation present: ([^\n]+)", template_automation_text)
    template_local_targets = text_value(r"Local equivalent Make targets present: ([^\n]+)", template_automation_text)
    template_fontspector_qa = yes_no_from_line(r"Local QA target uses Fontspector: (yes|no)", template_automation_text)
    template_fontbakery_refs = yes_no_from_line(r"Local Makefile references FontBakery: (yes|no)", template_automation_text)
    template_automation_status = text_value(r"Decision log status: ([a-z]+)", template_automation_text)
    recent_package_examples_text = markdown_section(recent_packages_text, "Package Examples")
    recent_merge_text = markdown_section(recent_packages_text, "Recent Packager Merges")
    recent_pr_examples = len(set(re.findall(r"google/fonts#\d+", recent_package_examples_text)))
    recent_packager_merges = len(set(re.findall(r"google/fonts#\d+", recent_merge_text)))
    recent_arabic_example = 'primary_script: "Arab"' in template_pr_text and "`Arab`" in recent_packages_text
    language_script_record = yes_no_from_line(r"Script record exists: (yes|no)", language_metadata_text)
    language_script_id = text_value(r"Script id: `([^`]+)`", language_metadata_text)
    language_preview_subsets = yes_no_from_line(r"Preview `subsets` match target: (yes|no)", language_metadata_text)
    language_preview_primary_script = yes_no_from_line(r"Preview `primary_script` matches target: (yes|no)", language_metadata_text)
    language_preview_languages_absent = yes_no_from_line(r"Preview non-Noto `languages` entries absent: (yes|no)", language_metadata_text)
    language_preview_sample_text_absent = yes_no_from_line(r"Preview custom `sample_text` absent: (yes|no)", language_metadata_text)
    add_font_template_labels = text_value(r"Default labels: `([^`]+)`", add_font_template_text)
    handoff_template_labels = yes_no_from_line(r"Template default labels match handoff: (yes|no)", handoff_readiness_text)
    handoff_fontspector = yes_no_from_line(r"Handoff includes current Fontspector summary: (yes|no)", handoff_readiness_text)
    handoff_report_refs = len(re.findall(r"^\| `documentation/[^`]+` \| yes \|$", handoff_readiness_text, flags=re.MULTILINE))
    handoff_source_modes = yes_no_from_line(r"Handoff mentions Packager source-mode options: (yes|no)", handoff_readiness_text)
    handoff_maintenance = yes_no_from_line(r"Issue draft tracks repository maintenance commitment: (yes|no)", handoff_readiness_text)
    handoff_maintenance_unchecked = yes_no_from_line(r"Repository maintenance confirmation remains unchecked until issue opening: (yes|no)", handoff_readiness_text)
    issue_draft_current = yes_no(
        all(
            f"{line}: yes" in handoff_readiness_text
            for line in [
                "Issue draft title is current",
                "Issue draft labels are current",
                "Issue draft template checkout status is current",
                "Issue draft template is aligned with upstream/main",
                "Issue draft template is aligned with origin/main",
                "Issue draft leaves boxes unchecked",
                "Issue draft status notes match checkbox count",
                "Issue draft includes current Latin Core gap",
                "Issue draft includes current Fontspector FAIL count",
                "Issue draft points to specimen image",
            ]
        )
    )
    designer_author_candidates = first_int(r"AUTHORS catalog-credit candidates: (\d+)", designer_profile_text)
    designer_contributor_only_candidates = first_int(r"Contributor-only candidates: (\d+)", designer_profile_text)
    designer_missing = len(missing_designer_profile_names(designer_profile_text))
    designer_metadata_pending = first_int(r"Pending metadata designer placeholders: (\d+)", designer_profile_text)
    designer_profile_package_text = read_text("documentation/google-fonts/designer-profile-package-draft.md")
    designer_draft_placeholders = first_int(r"Draft placeholders still unresolved: (\d+)", designer_profile_package_text)
    designer_profile_collision = yes_no_from_line(r"Profile path collision risk: (yes|no)", designer_profile_package_text)
    ai_disclosure = yes_no_from_line(r"AI-use disclosure recorded: (yes|no)", authorship_text)
    combined_checkbox = yes_no_from_line(r"Combined Add Font checkbox present: (yes|no)", authorship_text)
    pr_source_git_identity = yes_no_from_line(r"Source repo git identity complete: (yes|no)", pr_identity_text)
    pr_gf_git_identity = yes_no_from_line(r"google/fonts fork git identity complete: (yes|no)", pr_identity_text)
    pr_gf_git_name_match = yes_no_from_line(
        r"google/fonts fork git user\.name matches expected CLA/author name: (yes|no)",
        pr_identity_text,
    )
    pr_final_commit_identity = yes_no_from_line(r"Final downstream commit identity ready: (yes|no)", pr_identity_text)
    pr_gh_auth = text_value(r"GitHub CLI auth status: `([^`]+)`", pr_identity_text)
    pr_api_auth = yes_no_from_line(r"GitHub API credentials ready: (yes|no)", pr_identity_text)
    pr_api_source = text_value(r"GitHub API credential source: `([^`]+)`", pr_identity_text)
    pr_cla = text_value(r"Google CLA status: ([^\n]+)", pr_identity_text)
    downstream_pr_issue_pending = yes_no_from_line(r"Google Fonts issue pending: (yes|no)", downstream_pr_text)
    downstream_pr_path = text_value(r"Expected downstream family path: `([^`]+)`", downstream_pr_text)
    downstream_pr_starter = yes_no_from_line(r"Downstream METADATA\.pb still starter template: (yes|no)", downstream_pr_text)
    downstream_pr_metadata_ready = yes_no_from_line(r"Downstream metadata preview ready to apply: (yes|no)", downstream_pr_text)
    downstream_pr_metadata_blockers = text_value(r"Downstream metadata apply blockers: (\d+)", downstream_pr_text)
    downstream_pr_dirty_outside = text_value(r"Dirty google/fonts paths outside family dir: (\d+)", downstream_pr_text)
    downstream_pr_family_file_count = text_value(r"Current downstream family file count: (\d+)", downstream_pr_text)
    downstream_pr_starter_only = yes_no_from_line(r"Current downstream family files starter-only: (yes|no)", downstream_pr_text)
    downstream_pr_handoff_shape = yes_no(
        "Handoff includes exact downstream PR title: yes" in downstream_pr_text
        and "Handoff includes exact PR provenance body line: yes" in downstream_pr_text
        and "Handoff records one-family-directory rule: yes" in downstream_pr_text
        and "Handoff records fork comparison path: yes" in downstream_pr_text
    )
    drawbot_origin = yes_no_from_line(r"Origin is Eli Heuer fork: (yes|no)", drawbot_runtime_text)
    drawbot_import = yes_no_from_line(r"Drawing API importable: (yes|no)", drawbot_runtime_text)
    drawbot_clean = yes_no_from_line(r"Local drawbot-skia worktree clean: (yes|no)", drawbot_runtime_text)
    local_preflight_ready = yes_no_from_line(r"Local preflight command ready to run: (yes|no)", local_workflow_text)
    local_proof_ready = yes_no_from_line(r"Proof command ready to run: (yes|no)", local_workflow_text)
    local_package_ready = yes_no_from_line(r"Package dry-run ready to reach Packager: (yes|no)", local_workflow_text)
    local_workflow_auth = yes_no_from_line(r"GitHub API credentials ready: (yes|no)", local_workflow_text)
    family_ascii = yes_no_from_line(r"Family names are ASCII letters/digits/spaces only: (yes|no)", family_name_text)
    family_rfn = text_value(r"OFL Reserved Font Name status: ([^\n]+)", family_name_text)
    family_namecheck_pending = "Namecheck confirmation: pending" in family_name_text
    family_author_name = yes_no_from_line(r"Built family names include copyright-author full name: (yes|no)", family_name_text)
    family_app_menu = yes_no_from_line(r"App-menu family name candidate appears in built names: (yes|no)", family_name_text)
    family_decision = text_value(r"Decision log status: ([a-z]+)", family_name_text)
    latin_missing = first_int(r"\| `GF_Latin_Core` \| Latin \| \d+ \| \d+ \| (\d+) \|", glyphset_text)
    arabic_missing = first_int(r"\| `GF_Arabic_Core` \| Arabic \| \d+ \| \d+ \| (\d+) \|", glyphset_text)
    arabic_source_missing = first_int(r"Missing required codepoints: (\d+)", arabic_source_text)
    arabic_suggested_names = first_int(r"Suggested source glyph names: (\d+)", arabic_source_text)
    arabic_positional_names = first_int(r"Suggested Arabic positional-form glyph names: (\d+)", arabic_source_text)
    arabic_suggested_missing_both = first_int(r"Suggested glyph names missing in both masters: (\d+)", arabic_source_text)
    arabic_reuse_checked = first_int(r"Arabic reuse prerequisites checked: (\d+) codepoints", arabic_source_text)
    arabic_reuse_missing = first_int(r"Missing reuse prerequisites across masters: (\d+)", arabic_source_text)
    arabic_dotted_circle_missing = yes_no_from_line(r"U\+25CC dotted circle missing: (yes|no)", arabic_source_text)
    arabic_edit_targets = first_int(r"Source target references: (\d+)", arabic_manual_edit_targets_text)
    arabic_edit_targets_missing = first_int(r"Missing source target files: (\d+)", arabic_manual_edit_targets_text)
    mark_missing = first_int(r"Missing from current variable-font cmap: (\d+)", arabic_mark_text)
    dotted_circle = yes_no_from_line(r"U\+25CC dotted circle present: (yes|no)", arabic_mark_text)
    source_anchors = yes_no_from_line(r"Source anchors present: (yes|no)", arabic_mark_text)
    mark_gpos = yes_no_from_line(r"Built mark/mkmk GPOS features present: (yes|no)", arabic_mark_text)
    shaping_font_count = len(re.findall(r"^## fonts/", arabic_shaping_text, flags=re.MULTILINE))
    shaping_arab_gsub = arabic_shaping_text.count("GSUB has `arab/dflt`: `true`")
    shaping_arab_gpos = arabic_shaping_text.count("GPOS has `arab/dflt`: `true`")
    shaping_notdef_counts = [int(value) for value in re.findall(r"\|\s*(\d+)\s*\| yes \|", arabic_shaping_text)]
    shaping_no_notdef = all(value == 0 for value in shaping_notdef_counts) if shaping_notdef_counts else False
    shaping_lam_alef_rows = re.findall(r"\|\s*yes\s*\|\s*yes\s*\|$", arabic_shaping_text, flags=re.MULTILINE)
    reachability_unique = first_int(r"Unique unreachable glyphs: (\d+)", reachability_text)
    reachability_arabic_helpers = first_int(r"Unique Arabic helper/form glyphs: (\d+)", reachability_text)
    reachability_mark_helpers = first_int(r"Unique Arabic mark helper glyphs: (\d+)", reachability_text)
    reachability_source_cleanup = first_int(r"Unique source cleanup glyphs: (\d+)", reachability_text)
    numeric_default_digits = yes_no_from_line(r"Default ASCII digits present in every built font: (yes|no)", numeric_text)
    numeric_default_proportional = yes_no_from_line(r"Default ASCII digits are proportional in every built font: (yes|no)", numeric_text)
    numeric_tnum_feature = yes_no_from_line(r"`tnum` feature present in every built font: (yes|no)", numeric_text)
    numeric_tnum_coverage = yes_no_from_line(r"`tnum` substitutes all ten ASCII digits in every built font: (yes|no)", numeric_text)
    numeric_tnum_tabular = yes_no_from_line(r"`tnum` substitutes to equal-width digits in every built font: (yes|no)", numeric_text)
    numeric_ready = yes_no_from_line(r"Numeric feature requirement ready: (yes|no)", numeric_text)
    pua_codepoints = first_int(r"Variable font PUA codepoints: (\d+)", pua_text)
    pua_regular_matches = yes_no_from_line(r"\| `sources/VirtuaGrotesk-Regular\.ufo` \| \d+ \| (yes|no) \|", pua_text)
    pua_bold_matches = yes_no_from_line(r"\| `sources/VirtuaGrotesk-Bold\.ufo` \| \d+ \| (yes|no) \|", pua_text)
    warnings_total = first_int(r"Warnings: (\d+)", warnings_text)
    decision_warnings_section = warnings_text.split("## Decision-Linked Warnings", 1)[1].split("## Warning Codes", 1)[0]
    decision_warning_counts = [
        int(count)
        for count in re.findall(
            r"^\| `(?:googlefonts/metadata/unreachable_subsetting|googlefonts/vendor_id|gpos_kerning_info|mandatory_avar_table|unreachable_glyphs)` \| (\d+) \|",
            decision_warnings_section,
            flags=re.MULTILINE,
        )
    ]
    decision_warnings = sum(decision_warning_counts)
    metadata_probe_warnings = sum(
        int(count)
        for count in re.findall(r"^\| `[^`]+` \| `[^`]+` \| (\d+) \|", metadata_warning_probe_text, flags=re.MULTILINE)
    )
    metadata_probe_unreachable = len(
        re.findall(r"^- `U\+[0-9A-F]{4,6} ", metadata_warning_probe_text, flags=re.MULTILINE)
    )
    metadata_probe_remove_rlm = first_int(r"\| remove U\+200F RLM \| (\d+) \|", metadata_warning_probe_text)
    metadata_probe_remove_dotted = first_int(r"\| remove U\+25CC dotted circle \| (\d+) \|", metadata_warning_probe_text)
    metadata_probe_menu_latin = first_int(r"\| menu \+ latin only \| (\d+) \|", metadata_warning_probe_text)
    metadata_probe_menu_latin_arabic = first_int(r"\| menu \+ latin \+ arabic \| (\d+) \|", metadata_warning_probe_text)
    zero_warning_possible = text_value(
        r"(?m)^- Honest zero-warning state possible with current scope: (.+)$",
        zero_warning_text,
    )
    zero_warning_blockers = text_value(
        r"(?m)^Blockers: (.+)$",
        zero_warning_text,
    )
    arabic_subset_additional = first_int(r"\| `arabic` \| 50% \| \d+ \| \d+ \| \d+ \| [^|]+ \| (\d+) \|", zero_warning_text)
    latin_ext_subset_additional = first_int(r"\| `latin-ext` \| 20% \| \d+ \| \d+ \| \d+ \| [^|]+ \| (\d+) \|", zero_warning_text)
    fontspector_fails = fontspector_fail_count(fontspector_text)
    contour_source_findings, contour_all_font_rows = contour_source_finding_count(contour_text)
    contour_decisions = contour_decision_counts(contour_decision_text)

    lines = [
        "# Final Submission Blockers",
        "",
        "This generated report summarizes the current blockers that remain before a",
        "final Google Fonts submission. It intentionally includes drawing/source",
        "work, maintainer decisions, packaging availability, and QA gates so the",
        "final handoff cannot hide behind one green local check.",
        "",
        "## Summary",
        "",
        "| Area | Current state | Final-submission requirement |",
        "| --- | --- | --- |",
        f"| Maintainer decisions | {open_decisions} open, {decided_decisions} decided | 0 open decisions |",
        f"| Decision readiness | open: {open_decisions}; decided: {decided_decisions}; questions: {decision_questions}; guided: {decision_guided_questions.replace(' / ', '/')}; mapped: {decision_mapped.replace(' / ', '/')}; surfaces: {decision_surface_items}; local paths: {decision_surface_paths.replace(' / ', '/')} | Decision log, question prompts, and apply-to surfaces stay aligned |",
        f"| Placeholder strings | public blockers: {actionable_placeholder_urls} URLs, {actionable_pending_markers} pending markers; generated echoes: {generated_placeholder_echoes}; internal/total URL echoes: {placeholder_urls} | 0 public placeholder strings |",
        f"| Packager source files | {source_missing} missing locally, {source_ignored} ignored/generated, tracked: {source_tracked.replace(' / ', '/')}, untracked: {source_untracked} | Public branch, release, or source build exposes every source file |",
        f"| Selected release/archive package plan | action plan: {release_archive_action_plan}; untracked: {release_archive_untracked}; gitignore-blocked: {release_archive_ignored} | Final GitHub release/archive contains every listed source file |",
        f"| Build-from-source path | gftools builder: {build_uses_builder}; metadata fix: {build_uses_metadata_fix}; outputs fonts: {builder_outputs_fonts}; tracked inputs: {build_inputs_tracked.replace(' / ', '/')} | Public build path is reproducible if build-from-source packaging is chosen |",
        f"| Static package shape | generated for QA: {static_generated}; source.files: {static_source_files}; static destinations: {static_destinations}; omission documented: {static_omission_documented} | Static TTFs are included only if Google Fonts review asks for them |",
        f"| Downstream metadata preview | variable names match: {metadata_names_match}; pending/placeholder lines: {metadata_pending} | Generated METADATA.pb has final designer, URL, commit, branch, subsets, and source files |",
        f"| Article package assets | words: {article_words}; target: {article_word_target}; script: `{article_primary_script}`; localized Arabic: {article_localized_arabic}; placeholder URL: {article_placeholder_url}; forbidden tags: {article_forbidden_tags}; images exist: {article_images_exist}; image size: {article_image_size}; provenance: {article_image_provenance.replace(' / ', '/')} | Final Article URL, HTML, images, localized text, and provenance are accepted |",
        f"| Family name and namecheck | ASCII: {family_ascii}; app-menu present: {family_app_menu}; author-name in menu: {family_author_name}; RFN: {family_rfn}; namecheck pending: {yes_no(family_namecheck_pending)}; decision: {family_decision} | Namecheck, trademarks, RFN status, app-menu name, and CLA are confirmed |",
        f"| Authorship and AI disclosure | Add Font checkbox: {combined_checkbox}; AI disclosure recorded: {ai_disclosure} | Copyright authorship and AI-use wording confirmed in issue text |",
        f"| PR identity and auth | source identity: {pr_source_git_identity}; google/fonts identity: {pr_gf_git_identity}; downstream name matches CLA: {pr_gf_git_name_match}; final commit identity: {pr_final_commit_identity}; gh auth: {pr_gh_auth}; API auth: {pr_api_auth}; source: {pr_api_source}; CLA: {pr_cla} | Git identity, GitHub auth, API credentials, and CLA identity are ready before downstream PR |",
        f"| Downstream PR readiness | issue pending: {downstream_pr_issue_pending}; path: `{downstream_pr_path}`; starter metadata: {downstream_pr_starter}; metadata apply-ready: {downstream_pr_metadata_ready}; apply blockers: {downstream_pr_metadata_blockers}; dirty outside path: {downstream_pr_dirty_outside}; family files: {downstream_pr_family_file_count}; starter-only family dir: {downstream_pr_starter_only}; handoff shape: {downstream_pr_handoff_shape} | Issue exists first, checked metadata is applied, PR is scoped to one family directory, and title/body/provenance are ready |",
        f"| DrawBot proof runtime | Eli Heuer fork origin: {drawbot_origin}; importable: {drawbot_import}; checkout clean: {drawbot_clean} | Final proofs are regenerated with the intended local drawbot-skia fork |",
        f"| Local workflow readiness | preflight: {local_preflight_ready}; proof: {local_proof_ready}; package reaches Packager: {local_package_ready}; auth: {local_workflow_auth} | Local handoff commands are runnable before final package work |",
        f"| Release metadata | version {release_version}, tag {release_tag}, built/source match: {release_match} | Confirmed version strategy and upstream tag/commit recorded |",
        f"| Release/source strategy | tag exists: {release_tag_exists}; clean tree: {release_dirty}; placeholder URL: {release_placeholder}; ignored source files: {release_ignored_sources}; untracked source files: {source_untracked} | Final public source commit, tag, branch, and Packager mode are recorded |",
        f"| Release archive manifest | inputs: {release_archive_inputs.replace(' / ', '/')}; unsafe sources: {release_archive_unsafe_sources}; duplicates: {release_archive_duplicate_sources}; local zip: {release_archive_local_exists}; expected files: {release_archive_contains}; unsafe entries: {release_archive_unsafe_entries}; hashes: {release_archive_hashes}; URL filename: {release_archive_filename_match}; final URL: {release_archive_final_url} | Final GitHub release archive matches local reviewed files, filename, path safety, and hashes |",
        f"| GitHub release draft | tag: {github_release_tag}; title: {github_release_title}; command: {github_release_command}; archive: `{github_release_archive}`; notes: `{github_release_notes}`; notes final: {github_release_notes_final}; expected files: {github_release_archive_ok}; hashes: {github_release_hashes}; source commit: {github_release_pending_commit} | Final release command and downstream `source.archive_url` contract are reviewed before publishing |",
        f"| Package dry-run readiness | reaches Packager: {dry_run_reaches_packager}; first blocker: {dry_run_first_blocker}; blockers: {dry_run_blocking_findings}; auth: {dry_run_auth_ready}; inputs: {dry_run_inputs_ready} | No-PR Packager dry run reaches Packager before opening or updating a downstream PR |",
        f"| Upstream structure | mandatory paths: {upstream_mandatory.replace(' / ', '/')}; active source inputs: {upstream_sources.replace(' / ', '/')}; generated fonts ignored: {upstream_fonts_ignored} | Public upstream repo follows GF structure and final font artifact strategy is explicit |",
        f"| Local google/fonts fork | origin: {gf_origin_slug}; upstream: {gf_upstream_slug}; topology: {gf_topology_ready}; exists: {gf_fork_exists}; branch: {gf_fork_branch}; upstream/main: {gf_fork_alignment}; clean: {gf_fork_clean}; dirty outside package: {gf_dirty_outside} | Clean fork checkout is synced before packaging or template refresh |",
        f"| Template and recent PR evidence | project template checked: {yes_no(template_checked)}; recent examples: {recent_pr_examples}; recent Packager merges: {recent_packager_merges}; Arabic example: {yes_no(recent_arabic_example)} | Final package follows current GF template expectations and recent new-font patterns |",
        f"| Language metadata | script record: {language_script_record}; script id: `{language_script_id}`; preview subsets: {language_preview_subsets}; primary_script: {language_preview_primary_script}; languages absent: {language_preview_languages_absent}; sample_text absent: {language_preview_sample_text_absent} | Downstream metadata language fields stay aligned with Arabic first-submission scope |",
        f"| Project template automation | optional automation: {template_automation_present}; local targets: {template_local_targets}; Fontspector QA: {template_fontspector_qa}; FontBakery refs: {template_fontbakery_refs}; decision: {template_automation_status} | Public CI/template automation is added only if maintainer chooses that workflow |",
        f"| Submission handoff | template labels: `{add_font_template_labels}`; handoff labels: {handoff_template_labels}; issue draft: {issue_draft_current}; Fontspector: {handoff_fontspector}; maintenance: {handoff_maintenance}; unchecked: {handoff_maintenance_unchecked}; report refs: {handoff_report_refs}; source modes: {handoff_source_modes} | Add Font issue draft and package handoff are current before opening issue or PR |",
        f"| Designer profile | author candidates: {designer_author_candidates}; contributor-only: {designer_contributor_only_candidates}; missing profiles: {designer_missing}; metadata placeholders: {designer_metadata_pending}; draft inputs: {designer_draft_placeholders}; path collision: {designer_profile_collision} | Final METADATA.pb designer string has matching catalog profile or prepared request |",
        f"| Vendor ID | sources: {vendor_source_values}; fonts: {vendor_font_values}; aligned: {vendor_aligned}; warnings: {vendor_warnings}; decision: {vendor_decision_status} | Registered four-character vendor ID is applied consistently, or deferral is explicitly accepted |",
        f"| Kerning | every master has source kerning: {source_kerning_every_master}; static GPOS kern: {static_gpos_kern}; warnings: {kerning_warnings}; gftools proof importable: {kerning_proof_importable}; proof output: {kerning_proof_output}; proof instances: {kerning_proof_instances}; review files: {kerning_proof_review_files}; review: {kerning_proof_review_status} | Kerning completed or explicitly deferred, and `gftools qa --proof` spacing/kerning proof reviewed |",
        f"| GF Latin Core coverage | {latin_missing} missing codepoints | 0 missing codepoints or reviewer-approved scope change |",
        f"| GF Arabic Core coverage | {arabic_missing} missing codepoints | 0 missing codepoints or reviewer-approved scope change |",
        f"| Arabic source worklist | missing codepoints: {arabic_source_missing}; suggested glyph names: {arabic_suggested_names}; positional forms: {arabic_positional_names}; missing in both masters: {arabic_suggested_missing_both}; reuse prerequisites checked: {arabic_reuse_checked}; missing prerequisites: {arabic_reuse_missing}; dotted circle missing: {arabic_dotted_circle_missing} | Missing Arabic glyphs are drawn from verified source bases in both masters |",
        f"| Arabic manual edit targets | source target references: {arabic_edit_targets}; missing source target files: {arabic_edit_targets_missing} | Any `fix-needed` Arabic visual-review row can be traced to Regular and Bold GLIF files before editing |",
        f"| Arabic shaping smoke test | fonts: {shaping_font_count}; GSUB arab/dflt: {shaping_arab_gsub}/{shaping_font_count}; GPOS arab/dflt: {shaping_arab_gpos}/{shaping_font_count}; no .notdef: {yes_no(shaping_no_notdef)}; lam-alef rows: {len(shaping_lam_alef_rows)} | Arabic GSUB shaping remains intact, and missing GPOS/mark support is tracked separately |",
        f"| Arabic marks | {mark_missing} missing marks; dotted circle: {dotted_circle}; anchors: {source_anchors}; mark/mkmk: {mark_gpos} | Required marks, dotted circle, anchors, and mark/mkmk ready or explicitly accepted |",
        f"| Numeric feature readiness | digits: {numeric_default_digits}; proportional defaults: {numeric_default_proportional}; `tnum`: {numeric_tnum_feature}; coverage: {numeric_tnum_coverage}; tabular widths: {numeric_tnum_tabular}; ready: {numeric_ready} | Default ASCII digits are proportional and complemented by full tabular `tnum` alternates |",
        f"| PUA/private-use scope | {pua_codepoints} codepoints; Regular matches variable: {pua_regular_matches}; Bold matches variable: {pua_bold_matches} | Private-use glyphs are kept with rationale, made reachable, or deferred before final packaging |",
        f"| Glyph reachability | {reachability_unique} unique unreachable; Arabic helpers: {reachability_arabic_helpers}; mark helpers: {reachability_mark_helpers}; source cleanup: {reachability_source_cleanup} | Arabic helper glyphs are reachable, encoded, decomposed, or deliberately removed before final packaging |",
        f"| Fontspector warning triage | {warnings_total} WARN results; decision-linked warnings: {decision_warnings} | Every warning is reviewed, resolved, or explicitly accepted before final submission |",
        f"| Fontspector metadata preview probe | preview WARNs: {metadata_probe_warnings}; unreachable codepoints: {metadata_probe_unreachable}; removing U+200F: {metadata_probe_remove_rlm} WARN; removing U+25CC: {metadata_probe_remove_dotted} WARN | Final metadata warning decisions are based on package-visible METADATA.pb, not loose-font noise |",
        f"| Fontspector zero-warning path | honest zero possible: {zero_warning_possible}; package floor: {metadata_probe_warnings} WARN; menu+latin probe: {metadata_probe_menu_latin} WARN but drops Arabic; menu+latin+arabic probe: {metadata_probe_menu_latin_arabic} WARN; contour findings: {contour_source_findings}; Arabic subset threshold needs: {arabic_subset_additional}; latin-ext threshold needs: {latin_ext_subset_additional}; Latin Core missing: {latin_missing}; blockers: {zero_warning_blockers} | Reduce warnings through real coverage, drawing cleanup, and reviewed subset scope, not by hiding intended Arabic support |",
        f"| Fontspector googlefonts profile | {fontspector_fails} FAIL results | 0 FAIL results or explicit reviewer acceptance |",
        f"| Contour/no-contour cleanup | {contour_source_findings} source glyph findings, {contour_all_font_rows} all-font rows; decisions pending: {contour_decisions['pending']}, fix-now: {contour_decisions['fix-now']}, fixed: {contour_decisions['fixed']}, accepted: {contour_decisions['accepted']}, deferred: {contour_decisions['deferred']} | 0 unresolved source-outline findings or explicit reviewer acceptance |",
        "",
        "## Open Maintainer Decisions",
        "",
    ]

    if open_decision_headings:
        lines.extend(f"- {heading}" for heading in open_decision_headings)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Evidence Reports",
            "",
            "- `documentation/google-fonts/google-fonts-decisions.md`",
            "- `documentation/google-fonts/google-fonts-decision-answer-sheet.md`",
            "- `documentation/google-fonts/decision-readiness.md`",
            "- `documentation/google-fonts/decision-application-blockers.md`",
            "- `documentation/google-fonts/open-placeholder-audit.md`",
            "- `documentation/google-fonts/public-upstream-readiness.md`",
            "- `documentation/google-fonts/package-source-files-audit.md`",
            "- `documentation/google-fonts/packager-source-strategy.md`",
            "- `documentation/google-fonts/package-dry-run-readiness.md`",
            "- `documentation/google-fonts/downstream-metadata-readiness.md`",
            "- `documentation/google-fonts/downstream-metadata-diff.md`",
            "- `documentation/google-fonts/article-readiness.md`",
            "- `documentation/google-fonts/kerning-readiness.md`",
            "- `documentation/google-fonts/kerning-proof-review.md`",
            "- `documentation/google-fonts/family-name-readiness.md`",
            "- `documentation/google-fonts/authorship-disclosure-readiness.md`",
            "- `documentation/google-fonts/pr-identity-readiness.md`",
            "- `documentation/google-fonts/downstream-pr-readiness.md`",
            "- `documentation/google-fonts/drawbot-runtime-readiness.md`",
            "- `documentation/google-fonts/local-workflow-readiness.md`",
            "- `documentation/google-fonts/vendor-id-readiness.md`",
            "- `documentation/google-fonts/avar-readiness.md`",
            "- `documentation/google-fonts/release-metadata.md`",
            "- `documentation/google-fonts/release-source-readiness.md`",
            "- `documentation/google-fonts/release-archive-manifest.md`",
            "- `documentation/google-fonts/github-release-draft.md`",
            "- `documentation/google-fonts/github-release-notes.md`",
            "- `documentation/google-fonts/upstream-structure-readiness.md`",
            "- `documentation/google-fonts/google-fonts-template-and-pr-audit.md`",
            "- `documentation/google-fonts/recent-google-fonts-packages.md`",
            "- `documentation/google-fonts/google-fonts-add-font-template-audit.md`",
            "- `documentation/google-fonts/google-fonts-add-font-issue-draft.md`",
            "- `documentation/google-fonts/project-template-automation-readiness.md`",
            "- `documentation/google-fonts/submission-handoff-readiness.md`",
            "- `documentation/google-fonts/designer-profile-readiness.md`",
            "- `documentation/google-fonts/designer-profile-package-draft.md`",
            "- `documentation/google-fonts/gf-glyphset-readiness.md`",
            "- `documentation/google-fonts/google-fonts-language-metadata.md`",
            "- `documentation/google-fonts/missing-gf-latin-core.md`",
            "- `documentation/google-fonts/missing-gf-arabic-core.md`",
            "- `documentation/glyph-review/arabic-source-work-checklist.md`",
            "- `documentation/glyph-review/arabic-current-review-worksheet.md`",
            "- `documentation/glyph-review/arabic-batch-recorder.md`",
            "- `documentation/glyph-review/arabic-first-review-batch.md`",
            "- `documentation/glyph-review/arabic-full-queue-ai-sweep.md`",
            "- `documentation/glyph-review/arabic-manual-edit-targets.md`",
            "- `documentation/glyph-review/arabic-shaping-smoke-test.md`",
            "- `documentation/glyph-review/arabic-mark-readiness.md`",
            "- `documentation/glyph-review/arabic-review-packet.md`",
            "- `documentation/glyph-review/arabic-goal-completion-audit.md`",
            "- `documentation/glyph-review/arabic-next-review-packet.md`",
            "- `documentation/glyph-review/arabic-visual-review-log.md`",
            "- `documentation/google-fonts/numeric-feature-readiness.md`",
            "- `documentation/google-fonts/pua-scope.md`",
            "- `documentation/google-fonts/glyph-reachability.md`",
            "- `documentation/google-fonts/fontspector-warnings.md`",
            "- `documentation/google-fonts/fontspector-metadata-warning-probe.md`",
            "- `documentation/google-fonts/fontspector-zero-warning-worklist.md`",
            "- `documentation/google-fonts/fontspector-googlefonts-report.md`",
            "- `documentation/google-fonts/fontspector-contour-count.md`",
            "- `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`",
            "- `documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md`",
            "- `documentation/glyph-review/contour-cleanup/contour-cleanup-ai-triage.md`",
            "- `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`",
            "",
            "Regenerate this report with `make preflight` after drawing work,",
            "metadata decisions, or packaging-source decisions change.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_final_submission_blockers.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
