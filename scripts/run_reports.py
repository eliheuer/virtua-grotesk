#!/usr/bin/env python3
"""Regenerate the project report bundle.

The Makefile should describe workflows, not carry every individual report
command. Keep the long report sequence here so it can be edited, tested, and
grouped like normal Python code.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
VARIABLE_FONT = "fonts/variable/VirtuaGrotesk[wght].ttf"
STATIC_FONTS = [
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]


def gf_weight_axis_registry() -> str:
    explicit = os.environ.get("GF_WEIGHT_AXIS_REGISTRY", "")
    if explicit:
        return explicit
    gf_repo = os.environ.get("GF_REPO_PATH", "")
    if not gf_repo:
        return ""
    return str(Path(gf_repo) / "axisregistry/Lib/axisregistry/data/weight.textproto")


def command(*parts: str, env: dict[str, str] | None = None) -> tuple[list[str], dict[str, str] | None]:
    return list(parts), env


def py(*args: str, env: dict[str, str] | None = None) -> tuple[list[str], dict[str, str] | None]:
    return command(sys.executable, *args, env=env)


def report_commands() -> list[tuple[list[str], dict[str, str] | None]]:
    source_mode = os.environ.get("GFT_PACKAGER_SOURCE_MODE", "latest-release")
    source_mode_env = {"GFT_PACKAGER_SOURCE_MODE": source_mode}
    fonts = [VARIABLE_FONT, *STATIC_FONTS]
    return [
        py("scripts/report_decision_answer_sheet.py", "documentation/google-fonts/google-fonts-decision-answer-sheet.md"),
        py("scripts/report_decision_readiness.py", "documentation/google-fonts/decision-readiness.md"),
        py("scripts/report_gf_reference_index.py", "documentation/google-fonts/google-fonts-reference-index.md"),
        py("scripts/report_agent_reuse_readiness.py", "documentation/google-fonts/google-fonts-agent-reuse-readiness.md"),
        py("scripts/report_source_metadata.py", "sources/VirtuaGrotesk-Regular.ufo", "sources/VirtuaGrotesk-Bold.ufo", "documentation/source/source-ufo-metadata.md"),
        py("scripts/report_master_compatibility.py", "sources/VirtuaGrotesk-Regular.ufo", "sources/VirtuaGrotesk-Bold.ufo", "documentation/source/master-compatibility.md"),
        py("scripts/report_generated_font_metadata.py", VARIABLE_FONT, *STATIC_FONTS, "documentation/google-fonts/generated-font-metadata.md"),
        py("scripts/report_vendor_id_readiness.py", "documentation/google-fonts/vendor-id-readiness.md"),
        py("scripts/report_release_metadata.py", "documentation/google-fonts/release-metadata.md"),
        py("scripts/report_release_source_readiness.py", "documentation/google-fonts/release-source-readiness.md"),
        py("scripts/report_release_archive_manifest.py", "documentation/google-fonts/release-archive-manifest.md"),
        py("scripts/report_github_release_draft.py", "documentation/google-fonts/github-release-draft.md"),
        py("scripts/report_upstream_structure_readiness.py", "documentation/google-fonts/upstream-structure-readiness.md"),
        py("scripts/report_family_name_readiness.py", VARIABLE_FONT, *STATIC_FONTS, "documentation/google-fonts/family-name-readiness.md"),
        py("scripts/report_authorship_disclosure_readiness.py", "documentation/google-fonts/authorship-disclosure-readiness.md"),
        py("scripts/report_pr_identity_readiness.py", "documentation/google-fonts/pr-identity-readiness.md"),
        py("scripts/report_drawbot_runtime_readiness.py", "documentation/google-fonts/drawbot-runtime-readiness.md"),
        py("scripts/report_package_dry_run_readiness.py", "documentation/google-fonts/package-dry-run-readiness.md", env=source_mode_env),
        py("scripts/report_local_workflow_readiness.py", "documentation/google-fonts/local-workflow-readiness.md"),
        py("scripts/report_designer_profile.py", "documentation/google-fonts/designer-profile-readiness.md"),
        py("scripts/report_designer_profile_package.py", "documentation/google-fonts/designer-profile-package-draft.md"),
        py("scripts/report_variable_metadata.py", VARIABLE_FONT, "documentation/google-fonts/variable-font-metadata.md"),
        py("scripts/report_avar_readiness.py", VARIABLE_FONT, "documentation/google-fonts/avar-readiness.md"),
        py("scripts/report_axis_registry.py", VARIABLE_FONT, gf_weight_axis_registry(), "documentation/google-fonts/google-fonts-axis-registry-audit.md"),
        py("scripts/report_gf_glyphset_readiness.py", VARIABLE_FONT, "documentation/google-fonts/gf-glyphset-readiness.md"),
        py("scripts/report_gf_language_metadata.py", "documentation/google-fonts/google-fonts-language-metadata.md"),
        py("scripts/report_ufo_editor_readiness.py", "documentation/source/ufo-editor-readiness.md"),
        py("scripts/report_missing_gf_latin_core.py", VARIABLE_FONT, "documentation/google-fonts/missing-gf-latin-core.md"),
        py("scripts/report_missing_gf_arabic_core.py", VARIABLE_FONT, "documentation/google-fonts/missing-gf-arabic-core.md"),
        py("scripts/report_arabic_source_checklist.py", VARIABLE_FONT, "documentation/glyph-review/arabic-source-work-checklist.md"),
        py("scripts/build_arabic_candidate_glyphs.py", "--output", "documentation/glyph-review/arabic-candidate-glyph-plan.md"),
        py("scripts/report_pua_scope.py", *fonts, "documentation/google-fonts/pua-scope.md"),
        py("scripts/report_public_upstream_readiness.py", "documentation/google-fonts/public-upstream-readiness.md"),
        py("scripts/report_open_placeholders.py", "documentation/google-fonts/open-placeholder-audit.md"),
        py("scripts/report_package_source_files.py", "documentation/google-fonts/package-source-files-audit.md"),
        py("scripts/report_packager_source_strategy.py", "documentation/google-fonts/packager-source-strategy.md"),
        py("scripts/report_downstream_metadata_readiness.py", "documentation/google-fonts/downstream-metadata-readiness.md"),
        py("scripts/report_downstream_metadata_diff.py", "documentation/google-fonts/downstream-metadata-diff.md", env=source_mode_env),
        py("scripts/report_decision_application_blockers.py", "documentation/google-fonts/decision-application-blockers.md"),
        py("scripts/report_article_readiness.py", "documentation/google-fonts/article-readiness.md"),
        py("scripts/report_kerning_readiness.py", *fonts, "documentation/google-fonts/kerning-readiness.md"),
        py("scripts/report_kerning_proof_review.py", "documentation/google-fonts/kerning-proof-review.md"),
        py("scripts/report_arabic_mark_readiness.py", "documentation/glyph-review/arabic-mark-readiness.md"),
        py("scripts/report_arabic_shaping.py", *fonts, "documentation/glyph-review/arabic-shaping-smoke-test.md"),
        py("scripts/report_arabic_visual_risk.py", "documentation/glyph-review/arabic-visual-risk-audit.md"),
        py("scripts/build_arabic_visual_risk_proof.py", "documentation/glyph-review/arabic-visual-risk-proof.html"),
        py("scripts/build_arabic_structure_sweep.py", "documentation/glyph-review/arabic-structure-sweep.html"),
        py("scripts/report_arabic_structure_triage.py", "documentation/glyph-review/arabic-structure-triage.md"),
        py("scripts/build_arabic_mark_review_proof.py", "documentation/glyph-review/arabic-mark-review-proof.html"),
        py("scripts/report_arabic_mark_triage.py", "documentation/glyph-review/arabic-mark-triage.md"),
        py("scripts/report_arabic_visual_review_log.py", "documentation/glyph-review/arabic-visual-review-log.md"),
        py("scripts/report_glyph_reachability.py", *fonts, "documentation/google-fonts/glyph-reachability.md"),
        py("scripts/report_numeric_feature_readiness.py", "documentation/google-fonts/numeric-feature-readiness.md"),
        py("scripts/report_fontspector_contours.py", *fonts, "documentation/google-fonts/fontspector-contour-count.md"),
        py("scripts/build_contour_cleanup_proof.py"),
        py("scripts/build_arabic_manual_review_dashboard.py", "documentation/glyph-review/arabic-manual-review-dashboard.html"),
        py("scripts/report_arabic_manual_edit_targets.py", "documentation/glyph-review/arabic-manual-edit-targets.md"),
        py("scripts/build_arabic_first_review_zoom_snapshots.py", "documentation/glyph-review/arabic-first-review-zoom-snapshots.md"),
        py("scripts/report_arabic_first_review_crop_integrity.py", "documentation/glyph-review/arabic-first-review-crop-integrity.md"),
        py("scripts/report_arabic_first_review_batch.py", "documentation/glyph-review/arabic-first-review-batch.md"),
        py("scripts/report_arabic_first_review_risk_shortlist.py", "documentation/glyph-review/arabic-first-review-risk-shortlist.md"),
        py("scripts/report_arabic_hand_review_session.py", "documentation/glyph-review/arabic-hand-review-session.md"),
        py("scripts/build_arabic_hand_review_contact_sheet.py", "documentation/glyph-review/arabic-hand-review-contact-sheet.html"),
        py("scripts/report_arabic_next_review_packet.py", "documentation/glyph-review/arabic-next-review-packet.md"),
        py("scripts/report_arabic_next_review_ai_triage.py", "documentation/glyph-review/arabic-next-review-ai-triage.md"),
        py("scripts/report_arabic_next_review_ai_observations.py", "documentation/glyph-review/arabic-next-review-ai-observations.md"),
        py("scripts/report_arabic_full_queue_ai_sweep.py", "documentation/glyph-review/arabic-full-queue-ai-sweep.md"),
        py("scripts/report_arabic_manual_review_batches.py", "documentation/glyph-review/arabic-manual-review-batches.md"),
        py("scripts/report_arabic_review_progress.py", "documentation/glyph-review/arabic-review-progress.md"),
        py("scripts/report_arabic_current_review_worksheet.py", "documentation/glyph-review/arabic-current-review-worksheet.md"),
        py("scripts/report_arabic_review_worksheet_bundle.py", "documentation/glyph-review/arabic-review-worksheet-bundle.md"),
        py("scripts/report_arabic_drawing_session_checklist.py", "documentation/glyph-review/arabic-drawing-session-checklist.md"),
        py("scripts/report_arabic_source_edit_diff.py", "documentation/glyph-review/arabic-source-edit-diff.md", "--fail-on-gap"),
        py("scripts/report_arabic_first_batch_source_checkpoint.py", "documentation/glyph-review/arabic-first-batch-source-checkpoint.md"),
        py("scripts/report_arabic_pending_source_checkpoint.py", "documentation/glyph-review/arabic-pending-source-checkpoint.md"),
        py("scripts/report_arabic_visual_review_batch_tsv.py", "documentation/glyph-review/arabic-visual-review-batch.tsv"),
        py("scripts/report_arabic_batch_recorder.py", "documentation/glyph-review/arabic-batch-recorder.md"),
        py("scripts/build_arabic_next_review_board.py", "documentation/glyph-review/arabic-next-review-board.html"),
        py("scripts/report_arabic_snapshot_integrity.py", "documentation/glyph-review/arabic-snapshot-integrity.md"),
        py("scripts/report_arabic_visual_review_runbook.py", "documentation/glyph-review/arabic-visual-review-runbook.md"),
        py("scripts/report_arabic_goal_completion.py", "documentation/glyph-review/arabic-goal-completion-audit.md"),
        py("scripts/report_metadata_warning_probe.py", "documentation/google-fonts/fontspector-metadata-warning-probe.md"),
        py("scripts/report_zero_warning_worklist.py", VARIABLE_FONT, "documentation/google-fonts/fontspector-zero-warning-worklist.md"),
        py("scripts/report_fontspector_warnings.py", VARIABLE_FONT, *STATIC_FONTS, "documentation/google-fonts/fontspector-warnings.md"),
        command("./scripts/report_fontspector_markdown.sh", "documentation/google-fonts/fontspector-googlefonts-report.md"),
        py("scripts/report_arabic_review_packet.py", "documentation/glyph-review/arabic-review-packet.md"),
        py("scripts/report_production_requirements.py", "documentation/google-fonts/google-fonts-production-requirements.md"),
        py("scripts/report_recent_gf_packages.py", "documentation/google-fonts/recent-google-fonts-packages.md"),
        py("scripts/report_gf_add_font_template.py", "documentation/google-fonts/google-fonts-add-font-template-audit.md"),
        py("scripts/report_add_font_issue_draft.py", "documentation/google-fonts/google-fonts-add-font-issue-draft.md"),
        py("scripts/report_downstream_pr_readiness.py", "documentation/google-fonts/downstream-pr-readiness.md"),
        py("scripts/report_project_template_automation.py", "documentation/google-fonts/project-template-automation-readiness.md"),
        py("scripts/report_submission_handoff_readiness.py", "documentation/google-fonts/submission-handoff-readiness.md"),
        py("scripts/report_final_submission_blockers.py", "documentation/google-fonts/final-submission-blockers.md"),
        py("scripts/report_next_actions.py", "documentation/google-fonts/next-actions.md"),
    ]


def main() -> int:
    env_base = os.environ.copy()
    for args, extra_env in report_commands():
        env = env_base.copy()
        if extra_env:
            env.update(extra_env)
        print("+ " + " ".join(args), flush=True)
        result = subprocess.run(args, cwd=ROOT, env=env, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
