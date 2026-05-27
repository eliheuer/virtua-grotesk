#!/usr/bin/env python3
"""Local Google Fonts onboarding preflight.

This intentionally allows the known drawing/source FAILs while this project is
still in glyph production. Everything else should be fixed or documented.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import struct
import subprocess
import tempfile
import unicodedata

from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ttLib import TTFont
import glyphsets
import yaml


ROOT = Path(__file__).resolve().parents[1]
VARIABLE_FONT = ROOT / "fonts" / "variable" / "VirtuaGrotesk[wght].ttf"
DRAWBOT_SKIA_REPO = Path("/Users/eli/GH/repos/drawbot-skia")
DRAWBOT_SKIA_PYTHON = DRAWBOT_SKIA_REPO / ".venv/bin/python"
DRAWBOT_SKIA_SRC = DRAWBOT_SKIA_REPO / "src"
EXPECTED_DRAWBOT_ORIGINS = {
    "git@github.com:eliheuer/drawbot-skia.git",
    "https://github.com/eliheuer/drawbot-skia",
    "https://github.com/eliheuer/drawbot-skia.git",
}
GF_REPO_PATH = Path("/Users/eli/GH/forks/fonts")
GF_WEIGHT_AXIS_REGISTRY = GF_REPO_PATH / "axisregistry/Lib/axisregistry/data/weight.textproto"
ALLOWED_DRAWING_FAILS = {
    "googlefonts/glyph_coverage",
    "contour_count",
    "googlefonts/glyphsets/shape_languages",
}
EXPECTED_FONT_OUTPUTS = [
    "fonts/variable/VirtuaGrotesk[wght].ttf",
    "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
EXPECTED_STATIC_WEIGHTS = {
    "fonts/ttf/VirtuaGrotesk-Regular.ttf": 400,
    "fonts/ttf/VirtuaGrotesk-Medium.ttf": 500,
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf": 600,
    "fonts/ttf/VirtuaGrotesk-Bold.ttf": 700,
}
EXPECTED_NAME_IDS = {
    "fonts/variable/VirtuaGrotesk[wght].ttf": {
        1: "Virtua Grotesk",
        2: "Regular",
        4: "Virtua Grotesk Regular",
        6: "VirtuaGrotesk-Regular",
    },
    "fonts/ttf/VirtuaGrotesk-Regular.ttf": {
        1: "Virtua Grotesk",
        2: "Regular",
        4: "Virtua Grotesk Regular",
        6: "VirtuaGrotesk-Regular",
    },
    "fonts/ttf/VirtuaGrotesk-Medium.ttf": {
        1: "Virtua Grotesk Medium",
        2: "Regular",
        4: "Virtua Grotesk Medium",
        6: "VirtuaGrotesk-Medium",
        16: "Virtua Grotesk",
        17: "Medium",
    },
    "fonts/ttf/VirtuaGrotesk-SemiBold.ttf": {
        1: "Virtua Grotesk SemiBold",
        2: "Regular",
        4: "Virtua Grotesk SemiBold",
        6: "VirtuaGrotesk-SemiBold",
        16: "Virtua Grotesk",
        17: "SemiBold",
    },
    "fonts/ttf/VirtuaGrotesk-Bold.ttf": {
        1: "Virtua Grotesk",
        2: "Bold",
        4: "Virtua Grotesk Bold",
        6: "VirtuaGrotesk-Bold",
    },
}
EXPECTED_DESIGNSPACE_SOURCES = {
    "VirtuaGrotesk-Regular.ufo": 400,
    "VirtuaGrotesk-Bold.ufo": 700,
}
EXPECTED_DESIGNSPACE_INSTANCES = {
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
}
EXPECTED_SOURCE_FONTINFO = {
    "familyName": "Virtua Grotesk",
    "unitsPerEm": 1024,
    "ascender": 832,
    "descender": -256,
    "xHeight": 576,
    "capHeight": 768,
    "openTypeNameLicense": (
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
        "This license is available with a FAQ at: https://openfontlicense.org"
    ),
    "openTypeNameLicenseURL": "https://openfontlicense.org",
    "openTypeOS2TypoAscender": 1024,
    "openTypeOS2TypoDescender": -296,
    "openTypeOS2TypoLineGap": 0,
    "openTypeOS2WinAscent": 1024,
    "openTypeOS2WinDescent": 296,
    "openTypeHheaAscender": 1024,
    "openTypeHheaDescender": -296,
    "openTypeHheaLineGap": 0,
}
EXPECTED_SOURCE_STYLES = {
    "sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist": "Regular",
    "sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist": "Bold",
}
EXPECTED_BUILDER_CONFIG = {
    "sources": ["VirtuaGrotesk.designspace"],
    "axisOrder": ["wght"],
    "familyName": "Virtua Grotesk",
    "outputDir": "../fonts",
    "buildOTF": False,
    "buildWebfont": False,
    "flattenComponents": False,
    "decomposeTransformedComponents": False,
}
EXPECTED_VERSION_MAJOR = 1
EXPECTED_VERSION_MINOR = 0
EXPECTED_NAME_VERSION = "Version 1.000"
REQUIRED_FILES = [
    ".ignore",
    "AGENTS.md",
    ".agents/README.md",
    ".agents/google-fonts-onboarding-checklists.md",
    ".agents/google-fonts-official-reference-map.md",
    ".agents/skills/google-fonts-onboarding/SKILL.md",
    ".agents/skills/google-fonts-qa/SKILL.md",
    ".agents/skills/google-fonts-packaging/SKILL.md",
    ".agents/skills/google-fonts-nonlatin-drawing/SKILL.md",
    "AUTHORS.txt",
    "CONTRIBUTORS.txt",
    "OFL.txt",
    "README.md",
    "Makefile",
    "requirements.in",
    "requirements.txt",
    "sources/config.yaml",
    "sources/README.md",
    "sources/archive/README.md",
    "sources/VirtuaGrotesk-Regular.ufo/features.fea",
    "sources/VirtuaGrotesk-Bold.ufo/features.fea",
    "documentation/ARTICLE.en_us.html",
    "documentation/DESCRIPTION.en_us.html",
    "documentation/core-qa-process.md",
    "documentation/arabic-candidate-glyph-plan.md",
    "documentation/arabic-mark-readiness.md",
    "documentation/arabic-review-packet.md",
    "documentation/arabic-shaping-smoke-test.md",
    "documentation/arabic-source-work-checklist.md",
    "documentation/arabic-goal-completion-audit.md",
    "documentation/arabic-visual-risk-audit.md",
    "documentation/arabic-visual-risk-proof.html",
    "documentation/arabic-structure-sweep.html",
    "documentation/arabic-structure-triage.md",
    "documentation/arabic-mark-review-proof.html",
    "documentation/arabic-mark-triage.md",
    "documentation/arabic-visual-review-checklist.md",
    "documentation/arabic-visual-review-log.md",
    "documentation/arabic-manual-review-dashboard.html",
    "documentation/arabic-next-review-batch.html",
    "documentation/arabic-manual-review-batches.md",
    "documentation/arabic-current-review-worksheet.md",
    "documentation/arabic-review-worksheet-bundle.md",
    "documentation/arabic-batch-recorder.md",
    "documentation/arabic-first-review-zoom-snapshots.md",
    "documentation/arabic-first-review-crop-integrity.md",
    "documentation/arabic-first-review-batch.md",
    "documentation/arabic-first-review-risk-shortlist.md",
    "documentation/arabic-first-review-ai-sweep.md",
    "documentation/arabic-manual-edit-targets.md",
    "documentation/arabic-hand-review-session.md",
    "documentation/arabic-hand-review-contact-sheet.html",
    "documentation/arabic-print-proof-index.md",
    "documentation/arabic-next-review-packet.md",
    "documentation/arabic-next-review-ai-triage.md",
    "documentation/arabic-next-review-ai-observations.md",
    "documentation/arabic-full-queue-ai-sweep.md",
    "documentation/arabic-next-review-board.html",
    "documentation/arabic-snapshot-integrity.md",
    "documentation/arabic-visual-review-runbook.md",
    "documentation/google-fonts-decision-questions.md",
    "documentation/google-fonts-decision-answer-sheet.md",
    "documentation/google-fonts-decisions.md",
    "documentation/decision-readiness.md",
    "documentation/google-fonts-reference-index.md",
    "documentation/google-fonts-agent-reuse-readiness.md",
    "documentation/decision-application-blockers.md",
    "documentation/google-fonts-downstream-package-preview.md",
    "documentation/google-fonts-package-checklist.md",
    "documentation/python-tooling-notes.md",
    "documentation/google-fonts-release-checklist.md",
    "documentation/google-fonts-metadata-review.md",
    "documentation/google-fonts-submission-handoff.md",
    "documentation/google-fonts-template-and-pr-audit.md",
    "documentation/google-fonts-upstream-audit.md",
    "documentation/final-submission-blockers.md",
    "documentation/next-actions.md",
    "documentation/manual-cleanup-handoff.md",
    "documentation/submission-handoff-readiness.md",
    "documentation/recent-google-fonts-packages.md",
    "documentation/google-fonts-add-font-template-audit.md",
    "documentation/google-fonts-add-font-issue-draft.md",
    "documentation/project-template-automation-readiness.md",
    "documentation/generated-font-metadata.md",
    "documentation/google-fonts-production-requirements.md",
    "documentation/numeric-feature-readiness.md",
    "documentation/family-name-readiness.md",
    "documentation/authorship-disclosure-readiness.md",
    "documentation/pr-identity-readiness.md",
    "documentation/downstream-pr-readiness.md",
    "documentation/drawbot-runtime-readiness.md",
    "documentation/local-workflow-readiness.md",
    "documentation/vendor-id-readiness.md",
    "documentation/release-metadata.md",
    "documentation/release-source-readiness.md",
    "documentation/release-archive-manifest.md",
    "documentation/github-release-draft.md",
    "documentation/github-release-notes.md",
    "documentation/upstream-structure-readiness.md",
    "documentation/designer-profile-readiness.md",
    "documentation/designer-profile-package-draft.md",
    "documentation/designer-profile-candidate/info.pb",
    "documentation/designer-profile-candidate/bio.html",
    "documentation/avar-readiness.md",
    "documentation/google-fonts-axis-registry-audit.md",
    "documentation/gf-glyphset-readiness.md",
    "documentation/google-fonts-language-metadata.md",
    "documentation/master-compatibility.md",
    "documentation/ufo-editor-readiness.md",
    "documentation/open-placeholder-audit.md",
    "documentation/public-upstream-readiness.md",
    "documentation/package-source-files-audit.md",
    "documentation/packager-source-strategy.md",
    "documentation/package-dry-run-readiness.md",
    "documentation/downstream-metadata-readiness.md",
    "documentation/downstream-metadata-diff.md",
    "documentation/article-readiness.md",
    "documentation/kerning-readiness.md",
    "documentation/kerning-proof-review.md",
    "documentation/pua-scope.md",
    "documentation/source-ufo-metadata.md",
    "documentation/variable-font-metadata.md",
    "documentation/missing-gf-arabic-core.md",
    "documentation/missing-gf-latin-core.md",
    "documentation/glyph-reachability.md",
    "documentation/fontspector-contour-count.md",
    "documentation/contour-cleanup-proof.html",
    "documentation/contour-cleanup-review-queue.md",
    "documentation/contour-cleanup-edit-plan.md",
    "documentation/arabic-cleanup-drawing-briefs.md",
    "documentation/contour-cleanup-batches.md",
    "documentation/contour-cleanup-decision-log.md",
    "documentation/contour-cleanup-ai-triage.md",
    "documentation/contour-cleanup-source-edit-runlist.md",
    "documentation/contour-cleanup-first-edit-batch.md",
    "documentation/fontspector-warnings.md",
    "documentation/fontspector-metadata-warning-probe.md",
    "documentation/fontspector-zero-warning-worklist.md",
    "documentation/fontspector-googlefonts-report.md",
    "documentation/image-license.txt",
    "documentation/readme-specimen.png",
    "scripts/check_gf_fonts.sh",
    "scripts/check_gf_variable.sh",
    "scripts/check_github_api_auth.py",
    "scripts/build_release_archive.py",
    "scripts/verify_release_archive.py",
    "scripts/apply_public_upstream_url.py",
    "scripts/apply_vendor_id.py",
    "scripts/fix_gf_metadata.py",
    "scripts/package_gf_dry_run.sh",
    "scripts/test_package_gf_dry_run_gates.sh",
    "scripts/test_downstream_metadata_helper.sh",
    "scripts/test_release_archive_gates.sh",
    "scripts/test_contour_decision_update.sh",
    "scripts/test_arabic_visual_review_update.sh",
    "scripts/test_designer_profile_validators.sh",
    "scripts/prepare_downstream_metadata.py",
    "scripts/report_arabic_shaping.py",
    "scripts/report_arabic_mark_readiness.py",
    "scripts/report_arabic_review_packet.py",
    "scripts/report_arabic_source_checklist.py",
    "scripts/report_arabic_goal_completion.py",
    "scripts/report_arabic_visual_risk.py",
    "scripts/build_arabic_visual_risk_proof.py",
    "scripts/build_arabic_structure_sweep.py",
    "scripts/report_arabic_structure_triage.py",
    "scripts/build_arabic_mark_review_proof.py",
    "scripts/report_arabic_mark_triage.py",
    "scripts/report_arabic_visual_review_log.py",
    "scripts/build_arabic_manual_review_dashboard.py",
    "scripts/report_arabic_manual_review_batches.py",
    "scripts/report_arabic_current_review_worksheet.py",
    "scripts/report_arabic_review_worksheet_bundle.py",
    "scripts/report_arabic_batch_recorder.py",
    "scripts/build_arabic_first_review_zoom_snapshots.py",
    "scripts/report_arabic_first_review_crop_integrity.py",
    "scripts/report_arabic_first_review_batch.py",
    "scripts/report_arabic_first_review_risk_shortlist.py",
    "scripts/report_arabic_manual_edit_targets.py",
    "scripts/report_arabic_hand_review_session.py",
    "scripts/build_arabic_hand_review_contact_sheet.py",
    "scripts/report_arabic_next_review_packet.py",
    "scripts/report_arabic_next_review_ai_triage.py",
    "scripts/report_arabic_next_review_ai_observations.py",
    "scripts/report_arabic_full_queue_ai_sweep.py",
    "scripts/build_arabic_next_review_board.py",
    "scripts/build_arabic_next_review_snapshots.py",
    "scripts/report_arabic_snapshot_integrity.py",
    "scripts/report_arabic_visual_review_runbook.py",
    "scripts/update_arabic_visual_review.py",
    "scripts/check_runebender_norad_load.sh",
    "scripts/test_arabic_visual_review_update.sh",
    "scripts/report_decision_answer_sheet.py",
    "scripts/report_decision_readiness.py",
    "scripts/report_gf_reference_index.py",
    "scripts/report_agent_reuse_readiness.py",
    "scripts/build_arabic_candidate_glyphs.py",
    "scripts/report_decision_application_blockers.py",
    "scripts/report_generated_font_metadata.py",
    "scripts/report_production_requirements.py",
    "scripts/report_numeric_feature_readiness.py",
    "scripts/report_vendor_id_readiness.py",
    "scripts/report_release_metadata.py",
    "scripts/report_release_source_readiness.py",
    "scripts/report_release_archive_manifest.py",
    "scripts/report_github_release_draft.py",
    "scripts/report_upstream_structure_readiness.py",
    "scripts/report_family_name_readiness.py",
    "scripts/report_authorship_disclosure_readiness.py",
    "scripts/report_pr_identity_readiness.py",
    "scripts/report_downstream_pr_readiness.py",
    "scripts/report_drawbot_runtime_readiness.py",
    "scripts/report_local_workflow_readiness.py",
    "scripts/report_designer_profile.py",
    "scripts/report_designer_profile_package.py",
    "scripts/prepare_designer_profile.py",
    "scripts/validate_designer_profile_info.py",
    "scripts/validate_designer_profile_image.py",
    "scripts/validate_designer_profile_bio.py",
    "scripts/report_avar_readiness.py",
    "scripts/report_axis_registry.py",
    "scripts/report_gf_glyphset_readiness.py",
    "scripts/report_gf_language_metadata.py",
    "scripts/report_master_compatibility.py",
    "scripts/report_ufo_editor_readiness.py",
    "scripts/report_source_metadata.py",
    "scripts/report_variable_metadata.py",
    "scripts/report_missing_gf_arabic_core.py",
    "scripts/report_missing_gf_latin_core.py",
    "scripts/report_final_submission_blockers.py",
    "scripts/report_next_actions.py",
    "scripts/report_submission_handoff_readiness.py",
    "scripts/report_recent_gf_packages.py",
    "scripts/report_gf_add_font_template.py",
    "scripts/report_add_font_issue_draft.py",
    "scripts/report_project_template_automation.py",
    "scripts/report_open_placeholders.py",
    "scripts/report_public_upstream_readiness.py",
    "scripts/report_package_source_files.py",
    "scripts/report_packager_source_strategy.py",
    "scripts/report_package_dry_run_readiness.py",
    "scripts/report_downstream_metadata_readiness.py",
    "scripts/report_downstream_metadata_diff.py",
    "scripts/report_article_readiness.py",
    "scripts/report_kerning_readiness.py",
    "scripts/report_kerning_proof_review.py",
    "scripts/report_pua_scope.py",
    "scripts/report_glyph_reachability.py",
    "scripts/build_contour_cleanup_proof.py",
    "scripts/update_contour_decision.py",
    "scripts/test_contour_decision_update.sh",
    "scripts/check_runebender_norad_load.sh",
    "scripts/report_fontspector_contours.py",
    "scripts/report_fontspector_markdown.sh",
    "scripts/report_fontspector_warnings.py",
    "scripts/report_metadata_warning_probe.py",
    "scripts/report_zero_warning_worklist.py",
]
REQUIRED_EXECUTABLES = [
    "build.sh",
    "scripts/check_gf_fonts.sh",
    "scripts/check_gf_variable.sh",
    "scripts/check_github_api_auth.py",
    "scripts/build_release_archive.py",
    "scripts/verify_release_archive.py",
    "scripts/apply_public_upstream_url.py",
    "scripts/apply_vendor_id.py",
    "scripts/fix_gf_metadata.py",
    "scripts/gf_preflight.py",
    "scripts/package_gf_dry_run.sh",
    "scripts/test_package_gf_dry_run_gates.sh",
    "scripts/test_downstream_metadata_helper.sh",
    "scripts/test_release_archive_gates.sh",
    "scripts/test_contour_decision_update.sh",
    "scripts/test_arabic_visual_review_update.sh",
    "scripts/test_designer_profile_validators.sh",
    "scripts/prepare_downstream_metadata.py",
    "scripts/report_arabic_shaping.py",
    "scripts/report_arabic_mark_readiness.py",
    "scripts/report_arabic_review_packet.py",
    "scripts/report_arabic_source_checklist.py",
    "scripts/report_arabic_goal_completion.py",
    "scripts/report_arabic_visual_risk.py",
    "scripts/build_arabic_visual_risk_proof.py",
    "scripts/build_arabic_structure_sweep.py",
    "scripts/report_arabic_structure_triage.py",
    "scripts/build_arabic_mark_review_proof.py",
    "scripts/report_arabic_mark_triage.py",
    "scripts/report_arabic_visual_review_log.py",
    "scripts/update_arabic_visual_review.py",
    "scripts/report_arabic_manual_review_batches.py",
    "scripts/report_arabic_current_review_worksheet.py",
    "scripts/report_arabic_review_worksheet_bundle.py",
    "scripts/report_arabic_batch_recorder.py",
    "scripts/report_arabic_first_review_crop_integrity.py",
    "scripts/report_arabic_first_review_batch.py",
    "scripts/report_arabic_manual_edit_targets.py",
    "scripts/report_arabic_hand_review_session.py",
    "scripts/build_arabic_hand_review_contact_sheet.py",
    "scripts/report_arabic_next_review_packet.py",
    "scripts/report_arabic_next_review_ai_triage.py",
    "scripts/report_arabic_next_review_ai_observations.py",
    "scripts/report_arabic_full_queue_ai_sweep.py",
    "scripts/build_arabic_next_review_board.py",
    "scripts/build_arabic_next_review_snapshots.py",
    "scripts/report_arabic_snapshot_integrity.py",
    "scripts/report_arabic_visual_review_runbook.py",
    "scripts/test_arabic_visual_review_update.sh",
    "scripts/report_decision_answer_sheet.py",
    "scripts/report_decision_readiness.py",
    "scripts/report_gf_reference_index.py",
    "scripts/report_decision_application_blockers.py",
    "scripts/report_generated_font_metadata.py",
    "scripts/report_production_requirements.py",
    "scripts/report_numeric_feature_readiness.py",
    "scripts/report_vendor_id_readiness.py",
    "scripts/report_release_metadata.py",
    "scripts/report_release_source_readiness.py",
    "scripts/report_release_archive_manifest.py",
    "scripts/report_github_release_draft.py",
    "scripts/report_upstream_structure_readiness.py",
    "scripts/report_family_name_readiness.py",
    "scripts/report_authorship_disclosure_readiness.py",
    "scripts/report_pr_identity_readiness.py",
    "scripts/report_downstream_pr_readiness.py",
    "scripts/report_drawbot_runtime_readiness.py",
    "scripts/report_local_workflow_readiness.py",
    "scripts/report_designer_profile.py",
    "scripts/report_designer_profile_package.py",
    "scripts/validate_designer_profile_info.py",
    "scripts/validate_designer_profile_image.py",
    "scripts/validate_designer_profile_bio.py",
    "scripts/report_avar_readiness.py",
    "scripts/report_axis_registry.py",
    "scripts/report_gf_glyphset_readiness.py",
    "scripts/report_gf_language_metadata.py",
    "scripts/report_master_compatibility.py",
    "scripts/report_ufo_editor_readiness.py",
    "scripts/report_source_metadata.py",
    "scripts/report_variable_metadata.py",
    "scripts/report_missing_gf_arabic_core.py",
    "scripts/report_missing_gf_latin_core.py",
    "scripts/report_final_submission_blockers.py",
    "scripts/report_next_actions.py",
    "scripts/report_recent_gf_packages.py",
    "scripts/report_gf_add_font_template.py",
    "scripts/report_add_font_issue_draft.py",
    "scripts/report_project_template_automation.py",
    "scripts/report_open_placeholders.py",
    "scripts/report_public_upstream_readiness.py",
    "scripts/report_package_source_files.py",
    "scripts/report_packager_source_strategy.py",
    "scripts/report_package_dry_run_readiness.py",
    "scripts/report_downstream_metadata_readiness.py",
    "scripts/report_downstream_metadata_diff.py",
    "scripts/report_kerning_readiness.py",
    "scripts/report_kerning_proof_review.py",
    "scripts/report_pua_scope.py",
    "scripts/report_glyph_reachability.py",
    "scripts/build_contour_cleanup_proof.py",
    "scripts/update_contour_decision.py",
    "scripts/test_contour_decision_update.sh",
    "scripts/report_fontspector_contours.py",
    "scripts/report_fontspector_markdown.sh",
    "scripts/report_fontspector_warnings.py",
    "scripts/report_metadata_warning_probe.py",
    "scripts/report_zero_warning_worklist.py",
]
REQUIRED_PYTHON_MODULES = {
    "fontTools": "fonttools",
    "diffenator2": "gftools[qa]",
    "glyphsets": "glyphsets",
    "gftools": "gftools[qa]",
    "git": "GitPython",
    "uharfbuzz": "uharfbuzz",
    "yaml": "PyYAML",
}
EXPECTED_DIRECT_REQUIREMENTS = {
    "fontmake",
    "fonttools",
    "gftools[qa]",
    "GitPython",
    "glyphsets",
    "PyYAML",
    "uharfbuzz",
}


def check(condition: bool, message: str, errors: list[str]) -> None:
    if condition:
        print(f"OK  {message}")
    else:
        print(f"ERR {message}")
        errors.append(message)


def command_ok(command: list[str], message: str, errors: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    check(result.returncode == 0, message, errors)


def command_stdout(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return result.stdout if result.returncode == 0 else ""


def downstream_metadata_apply_blockers() -> str | None:
    text = (ROOT / "documentation/downstream-metadata-diff.md").read_text()
    match = re.search(r"Prepare helper blocking findings: (\d+)", text)
    return match.group(1) if match else None


def name_record(font: TTFont, name_id: int) -> str:
    name = font["name"].getName(name_id, 3, 1, 0x409)
    return name.toUnicode() if name else ""


def font_name_strings(font: TTFont) -> list[str]:
    names = []
    for record in font["name"].names:
        try:
            names.append(record.toUnicode())
        except UnicodeDecodeError:
            continue
    return names


def font_codepoints(font_path: Path) -> set[int]:
    font = TTFont(font_path)
    codepoints = set()
    for table in font["cmap"].tables:
        codepoints.update(table.cmap.keys())
    font.close()
    return codepoints


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def report_count(text: str, label: str) -> int | None:
    match = re.search(rf"^{re.escape(label)}:\s+(\d+)$", text, re.MULTILINE)
    return int(match.group(1)) if match else None


def section_missing_count(text: str, heading: str) -> int | None:
    match = re.search(rf"^{re.escape(heading)}\s*\n\nMissing:\s+(\d+)$", text, re.MULTILINE)
    return int(match.group(1)) if match else None


def summary_count(text: str, label: str) -> int | None:
    match = re.search(rf"{re.escape(label)}: (\d+)", text)
    return int(match.group(1)) if match else None


def markdown_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def markdown_rows(text: str, first_cell_prefix: str = "`") -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = split_markdown_row(line)
        if not cells or cells[0] == "---" or not cells[0].startswith(first_cell_prefix):
            continue
        rows.append(cells)
    return rows


def split_markdown_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in line.strip().strip("|"):
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\":
            current.append(character)
            escaped = True
            continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    cells.append("".join(current).strip())
    return cells


def unbacktick(value: str) -> str:
    return value.strip().strip("`")


def fontspector_summary_counts(text: str) -> dict[str, int]:
    summary_match = re.search(
        r"^### Summary\s+"
        r"(?P<header>\|[^\n]*\|)\s+"
        r"\|[^\n]+\|\s+"
        r"(?P<values>\|[^\n]*\|)",
        text,
        re.MULTILINE,
    )
    if not summary_match:
        return {}
    headers = [cell.strip() for cell in summary_match.group("header").strip("|").split("|")]
    values = [cell.strip() for cell in summary_match.group("values").strip("|").split("|")]
    raw_counts = dict(zip(headers, values, strict=False))
    labels = {
        "💥 ERROR": "ERROR",
        "🔥 FAIL": "FAIL",
        "⚠️ WARN": "WARN",
        "ℹ️ INFO": "INFO",
        "✅ PASS": "PASS",
        "⏩ SKIP": "SKIP",
    }
    return {target: int(raw_counts.get(label, 0)) for label, target in labels.items()}


def generated_variable_version(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("| `fonts/variable/VirtuaGrotesk[wght].ttf` | Version "):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            return cells[1] if len(cells) > 1 else ""
    return ""


def axis_registry_fallbacks() -> dict[int, str]:
    text = GF_WEIGHT_AXIS_REGISTRY.read_text()
    fallbacks = {}
    for block in re.findall(r"fallback\s*\{(.*?)\}", text, flags=re.DOTALL):
        name_match = re.search(r'name:\s+"([^"]+)"', block)
        value_match = re.search(r"value:\s+(\d+)", block)
        if name_match and value_match:
            fallbacks[int(value_match.group(1))] = name_match.group(1)
    return fallbacks


def copyright_url(copyright_line: str) -> str:
    match = re.search(r"\((https?://[^)]+)\)", copyright_line)
    return match.group(1) if match else ""


def font_metadata_errors(errors: list[str]) -> None:
    check(VARIABLE_FONT.exists(), "variable font exists", errors)
    ofl_first_line = (ROOT / "OFL.txt").read_text().splitlines()[0]

    for relative in EXPECTED_FONT_OUTPUTS:
        path = ROOT / relative
        if not path.exists():
            continue
        font = TTFont(path)
        copyright_string = name_record(font, 0)
        family_name = name_record(font, 1)
        style_name = name_record(font, 2)
        preferred_family_name = name_record(font, 16) or family_name
        version_string = name_record(font, 5)
        name_values = {
            name_id: name_record(font, name_id)
            for name_id in EXPECTED_NAME_IDS[relative]
        }
        license_string = name_record(font, 13)
        license_url = name_record(font, 14)
        fs_type = font["OS/2"].fsType
        meta_data = font["meta"].data if "meta" in font else {}
        font.close()

        check(copyright_string == ofl_first_line, f"OFL first line matches name ID 0: {relative}", errors)
        for name_id, expected_value in EXPECTED_NAME_IDS[relative].items():
            check(
                name_values[name_id] == expected_value,
                f"name ID {name_id} matches expected value: {relative}",
                errors,
            )
        check(
            len(f"{family_name} {style_name}") <= 32,
            f"family plus style name is within GF 32-character limit: {relative}",
            errors,
        )
        check(
            re.fullmatch(r"[A-Za-z0-9 ]+", preferred_family_name) is not None,
            f"preferred family name uses only GF-safe ASCII letters, digits, and spaces: {relative}",
            errors,
        )
        check(
            version_string.startswith(EXPECTED_NAME_VERSION),
            f"name ID 5 starts with GF version {EXPECTED_NAME_VERSION}: {relative}",
            errors,
        )
        check(fs_type == 0, f"OS/2 fsType is installable: {relative}", errors)
        check("https://openfontlicense.org" in license_string, f"license string uses GF URL: {relative}", errors)
        check(license_url == "https://openfontlicense.org", f"license URL matches GF requirement: {relative}", errors)
        check(meta_data.get("dlng") == "Arab, Latn", f"meta dlng declares Arabic and Latin: {relative}", errors)
        check(meta_data.get("slng") == "Arab, Latn", f"meta slng declares Arabic and Latin: {relative}", errors)


def layout_table_errors(errors: list[str]) -> None:
    for relative in EXPECTED_FONT_OUTPUTS:
        path = ROOT / relative
        if not path.exists():
            continue
        font = TTFont(path)
        has_gsub = "GSUB" in font
        features = set()
        if has_gsub and font["GSUB"].table.FeatureList is not None:
            features = {
                record.FeatureTag
                for record in font["GSUB"].table.FeatureList.FeatureRecord
            }
        font.close()
        check(has_gsub, f"Arabic GSUB table exists: {relative}", errors)
        check({"init", "medi", "fina", "rlig"}.issubset(features), f"Arabic GSUB features are present: {relative}", errors)


def build_output_errors(errors: list[str]) -> None:
    for relative in EXPECTED_FONT_OUTPUTS:
        check((ROOT / relative).exists(), f"expected built font exists: {relative}", errors)

    generated_fonts = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "fonts").glob("**/*")
        if path.is_file() and path.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2"}
    ]
    unexpected = sorted(set(generated_fonts) - set(EXPECTED_FONT_OUTPUTS))
    check(not unexpected, f"no stale unexpected generated font outputs: {unexpected}", errors)


def axis_errors(errors: list[str]) -> None:
    if not VARIABLE_FONT.exists():
        return

    check(GF_WEIGHT_AXIS_REGISTRY.exists(), "local google/fonts weight axis registry exists", errors)
    registry_text = GF_WEIGHT_AXIS_REGISTRY.read_text() if GF_WEIGHT_AXIS_REGISTRY.exists() else ""
    check('tag: "wght"' in registry_text, "local GF axis registry has wght tag", errors)
    check('display_name: "Weight"' in registry_text, "local GF axis registry names wght as Weight", errors)
    check("default_value: 400" in registry_text, "local GF axis registry default wght is 400", errors)
    fallback_names = axis_registry_fallbacks() if GF_WEIGHT_AXIS_REGISTRY.exists() else {}
    check(
        {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}.items() <= fallback_names.items(),
        "local GF axis registry includes required Virtua Grotesk fallback names",
        errors,
    )

    font = TTFont(VARIABLE_FONT)
    fvar = font["fvar"]
    axes = {axis.axisTag: axis for axis in fvar.axes}
    check(set(axes) == {"wght"}, f"variable font only has the wght axis: {sorted(axes)}", errors)
    if "wght" in axes:
        axis = axes["wght"]
        check(axis.minValue == 400, "wght min is 400", errors)
        check(axis.defaultValue == 400, "wght default is 400", errors)
        check(axis.maxValue == 700, "wght max is 700", errors)

    instance_weights = sorted(int(instance.coordinates["wght"]) for instance in fvar.instances)
    check(instance_weights == [400, 500, 600, 700], f"fvar instance weights match static set: {instance_weights}", errors)

    fvar_instances = {
        name_record(font, instance.subfamilyNameID): int(instance.coordinates["wght"])
        for instance in fvar.instances
    }
    fvar_instances_by_value = {
        int(instance.coordinates["wght"]): name_record(font, instance.subfamilyNameID)
        for instance in fvar.instances
    }
    check(fvar_instances.get("SemiBold") == 600, "fvar 600 instance is named SemiBold", errors)
    if fallback_names:
        check(
            fvar_instances_by_value == {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"},
            f"fvar instance names match GF axis registry fallback subset: {fvar_instances_by_value}",
            errors,
        )
    check("STAT" in font, "variable font has STAT table", errors)
    if "STAT" in font:
        stat = font["STAT"].table
        stat_axes = {axis.AxisTag: axis for axis in stat.DesignAxisRecord.Axis}
        check(set(stat_axes) == {"wght"}, f"STAT only has the wght axis: {sorted(stat_axes)}", errors)
        if "wght" in stat_axes:
            check(name_record(font, stat_axes["wght"].AxisNameID) == "Weight", "STAT wght axis is named Weight", errors)
            check(stat_axes["wght"].AxisOrdering == 0, "STAT wght axis ordering is 0", errors)
        stat_values = {}
        regular_linked_to_bold = False
        for axis_value in stat.AxisValueArray.AxisValue:
            value_name = name_record(font, axis_value.ValueNameID)
            value = int(getattr(axis_value, "Value", -1))
            stat_values[value_name] = value
            if value_name == "Regular":
                regular_linked_to_bold = (
                    axis_value.Format == 3
                    and int(getattr(axis_value, "LinkedValue", -1)) == 700
                    and axis_value.Flags == 2
                )
        check(
            stat_values == {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700},
            f"STAT axis values match expected weights: {stat_values}",
            errors,
        )
        if fallback_names:
            check(
                {value: label for label, value in stat_values.items()}
                == {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"},
                "STAT axis values match GF axis registry fallback subset",
                errors,
            )
        check(regular_linked_to_bold, "STAT Regular axis value links to Bold", errors)
    font.close()

    for relative, expected_weight in EXPECTED_STATIC_WEIGHTS.items():
        path = ROOT / relative
        if not path.exists():
            continue
        font = TTFont(path)
        actual_weight = font["OS/2"].usWeightClass
        font.close()
        check(actual_weight == expected_weight, f"static usWeightClass is {expected_weight}: {relative}", errors)


def naming_errors(errors: list[str]) -> None:
    for relative in EXPECTED_FONT_OUTPUTS:
        path = ROOT / relative
        if not path.exists():
            continue
        font = TTFont(path)
        names = font_name_strings(font)
        font.close()
        check(
            not any("Semi-Bold" in name for name in names),
            f"name table does not contain Semi-Bold: {relative}",
            errors,
        )

    semibold_path = ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf"
    if semibold_path.exists():
        font = TTFont(semibold_path)
        check(name_record(font, 4) == "Virtua Grotesk SemiBold", "static 600 full name is SemiBold", errors)
        check(name_record(font, 6) == "VirtuaGrotesk-SemiBold", "static 600 PostScript name is SemiBold", errors)
        font.close()


def designspace_errors(errors: list[str]) -> None:
    path = ROOT / "sources/VirtuaGrotesk.designspace"
    sources_readme = (ROOT / "sources/README.md").read_text()
    top_level_designspaces = sorted(
        candidate.name for candidate in (ROOT / "sources").glob("*.designspace")
    )
    top_level_ufos = sorted(
        candidate.name for candidate in (ROOT / "sources").glob("*.ufo")
    )
    check(
        top_level_designspaces == ["VirtuaGrotesk.designspace"],
        f"only active Virtua Grotesk designspace is at sources/ root: {top_level_designspaces}",
        errors,
    )
    check(
        top_level_ufos == ["VirtuaGrotesk-Bold.ufo", "VirtuaGrotesk-Regular.ufo"],
        f"only active Virtua Grotesk UFOs are at sources/ root: {top_level_ufos}",
        errors,
    )
    check("archive/" in sources_readme, "sources README documents archived sources", errors)
    for active_source in ["VirtuaGrotesk.designspace", "VirtuaGrotesk-Regular.ufo", "VirtuaGrotesk-Bold.ufo"]:
        check(active_source in sources_readme, f"sources README documents active source: {active_source}", errors)
    archive_readme = (ROOT / "sources/archive/README.md").read_text()
    check("not active Google Fonts build inputs" in archive_readme, "archive README excludes archived sources from active GF build", errors)
    check("Do not package files from this archive" in archive_readme, "archive README excludes archived sources from downstream package", errors)
    try:
        doc = DesignSpaceDocument.fromfile(path)
    except Exception as exc:
        check(False, f"designspace parses ({exc})", errors)
        return

    axes = {axis.tag: axis for axis in doc.axes}
    check(set(axes) == {"wght"}, f"designspace only has the wght axis: {sorted(axes)}", errors)
    if "wght" in axes:
        axis = axes["wght"]
        check(axis.name == "Weight", "designspace wght axis is named Weight", errors)
        check(axis.minimum == 400, "designspace wght min is 400", errors)
        check(axis.default == 400, "designspace wght default is 400", errors)
        check(axis.maximum == 700, "designspace wght max is 700", errors)

    sources = {}
    for source in doc.sources:
        if source.path:
            source_path = Path(source.path)
            sources[source_path.name] = int(source.location.get("Weight", -1))
            check(source_path.exists(), f"designspace source exists: {source_path.name}", errors)
            check(source.familyName == "Virtua Grotesk", f"designspace source family is Virtua Grotesk: {source_path.name}", errors)

    check(sources == EXPECTED_DESIGNSPACE_SOURCES, f"designspace sources match expected masters: {sources}", errors)

    instances = {
        instance.styleName: int(instance.location.get("Weight", -1))
        for instance in doc.instances
    }
    check(instances == EXPECTED_DESIGNSPACE_INSTANCES, f"designspace instances match expected weights: {instances}", errors)


def builder_config_errors(errors: list[str]) -> None:
    path = ROOT / "sources/config.yaml"
    try:
        config = yaml.safe_load(path.read_text())
    except Exception as exc:
        check(False, f"sources/config.yaml parses as YAML ({exc})", errors)
        return

    for key, expected_value in EXPECTED_BUILDER_CONFIG.items():
        check(
            config.get(key) == expected_value,
            f"sources/config.yaml {key} matches expected value: {expected_value}",
            errors,
        )

    check(not (ROOT / "config.yaml").exists(), "root config.yaml is not duplicated outside sources/", errors)
    check((path.parent / config["sources"][0]).exists(), "sources/config.yaml source designspace exists", errors)


def plist_errors(errors: list[str]) -> None:
    plist_paths = [
        ROOT / "sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist",
        ROOT / "sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist",
        ROOT / "sources/VirtuaGrotesk-Regular.ufo/glyphs/contents.plist",
        ROOT / "sources/VirtuaGrotesk-Bold.ufo/glyphs/contents.plist",
    ]
    for path in plist_paths:
        try:
            plistlib.loads(path.read_bytes())
            print(f"OK  valid plist: {path.relative_to(ROOT)}")
        except Exception as exc:
            print(f"ERR valid plist: {path.relative_to(ROOT)} ({exc})")
            errors.append(f"invalid plist: {path.relative_to(ROOT)}")


def source_fontinfo_errors(errors: list[str]) -> None:
    ofl_first_line = (ROOT / "OFL.txt").read_text().splitlines()[0]
    ofl_url = copyright_url(ofl_first_line)

    for relative, expected_style in EXPECTED_SOURCE_STYLES.items():
        path = ROOT / relative
        try:
            data = plistlib.loads(path.read_bytes())
        except Exception as exc:
            check(False, f"source fontinfo parses: {relative} ({exc})", errors)
            continue

        check(data.get("styleName") == expected_style, f"source styleName is {expected_style}: {relative}", errors)
        check(data.get("versionMajor") == EXPECTED_VERSION_MAJOR, f"source versionMajor is {EXPECTED_VERSION_MAJOR}: {relative}", errors)
        check(data.get("versionMinor") == EXPECTED_VERSION_MINOR, f"source versionMinor is {EXPECTED_VERSION_MINOR}: {relative}", errors)
        check(data.get("copyright") == ofl_first_line, f"source copyright matches OFL: {relative}", errors)
        check(
            "openTypeNameCopyright" not in data,
            f"source omits Norad-incompatible openTypeNameCopyright: {relative}",
            errors,
        )
        check(data.get("openTypeNameManufacturerURL") == ofl_url, f"source manufacturer URL matches OFL URL: {relative}", errors)
        check(
            "openTypeOS2Type" not in data,
            f"source leaves OS/2 fsType installable: {relative}",
            errors,
        )

        for key, expected_value in EXPECTED_SOURCE_FONTINFO.items():
            check(
                data.get(key) == expected_value,
                f"source {key} matches expected value: {relative}",
                errors,
            )


def fontspector_failures(errors: list[str]) -> None:
    font_paths = [ROOT / relative for relative in EXPECTED_FONT_OUTPUTS]
    if not all(path.exists() for path in font_paths):
        return
    if shutil.which("fontspector") is None:
        check(False, "Fontspector is installed", errors)
        return

    with tempfile.NamedTemporaryFile(suffix=".json") as report:
        command = [
            "fontspector",
            "-p",
            "googlefonts",
            *[str(path.relative_to(ROOT)) for path in font_paths],
            "--exclude-checkid",
            "googlefonts/repo/dirname_matches_nameid_1",
            "--json",
            report.name,
            "--loglevel",
            "error",
            "--skip-network",
        ]
        (Path.home() / ".fontspector").mkdir(exist_ok=True)
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        report_text = Path(report.name).read_text()

    check(result.returncode in (0, 1), "Fontspector produced a report", errors)
    if result.returncode not in (0, 1):
        return

    try:
        data = json.loads(report_text)
    except json.JSONDecodeError:
        check(False, "Fontspector JSON report is readable", errors)
        return

    failures = set()
    for family_results in data["results"].values():
        for checks in family_results.values():
            for item in checks:
                if item.get("worst_status") == "FAIL":
                    failures.add(item["check_id"])

    unexpected = failures - ALLOWED_DRAWING_FAILS
    check(
        not unexpected,
        f"Fontspector FAILs are only documented drawing/source blockers: {sorted(failures)}",
        errors,
    )


def required_file_errors(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        check((ROOT / relative).exists(), f"required repo artifact exists: {relative}", errors)
    ignore_text = (ROOT / ".ignore").read_text()
    check(
        "sources/instance_ufos/" in ignore_text,
        ".ignore hides generated instance UFO JSON from repo searches",
        errors,
    )
    check(
        "sources/build.ninja" in ignore_text and "sources/.ninja_log" in ignore_text,
        ".ignore hides sources-local ninja build files",
        errors,
    )
    gitignore_text = (ROOT / ".gitignore").read_text()
    check("dist/" in gitignore_text, ".gitignore hides local release archives", errors)


def executable_errors(errors: list[str]) -> None:
    for relative in REQUIRED_EXECUTABLES:
        check(os.access(ROOT / relative, os.X_OK), f"command entrypoint is executable: {relative}", errors)


def python_dependency_errors(errors: list[str]) -> None:
    def requirement_name(line: str) -> str:
        name = re.split(r"==|>=|<=|~=|!=|<|>|;", line.strip(), maxsplit=1)[0]
        return name.split("[", 1)[0]

    requirement_lines = [
        line.strip()
        for line in (ROOT / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    requirements = {
        requirement_name(line)
        for line in requirement_lines
    }
    direct_requirements = {
        line.strip().split("==", 1)[0].split(">=", 1)[0].split("<", 1)[0]
        for line in (ROOT / "requirements.in").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    expected_install_packages = {requirement_name(requirement) for requirement in EXPECTED_DIRECT_REQUIREMENTS}
    check(
        all("==" in line for line in requirement_lines),
        "requirements.txt is a pinned install snapshot",
        errors,
    )
    check(
        len(requirement_lines) > len(EXPECTED_DIRECT_REQUIREMENTS),
        "requirements.txt includes transitive pinned dependencies",
        errors,
    )
    check(
        direct_requirements == EXPECTED_DIRECT_REQUIREMENTS,
        f"requirements.in direct dependencies match expected set: {sorted(EXPECTED_DIRECT_REQUIREMENTS)}",
        errors,
    )
    check(
        expected_install_packages.issubset(requirements),
        "requirements.txt includes every direct dependency from requirements.in as pinned packages",
        errors,
    )
    for module_name, package_name in REQUIRED_PYTHON_MODULES.items():
        check(
            importlib.util.find_spec(module_name) is not None,
            f"Python dependency is importable: {package_name}",
            errors,
        )
        check(
            requirement_name(package_name) in requirements,
            f"Python dependency is declared in requirements.txt: {package_name}",
            errors,
        )


def meaningful_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def legal_credit_errors(errors: list[str]) -> None:
    legacy_authors_text = (ROOT / "AUTHORS").read_text()
    authors = meaningful_lines(ROOT / "AUTHORS.txt")
    contributors = meaningful_lines(ROOT / "CONTRIBUTORS.txt")
    ofl_text = (ROOT / "OFL.txt").read_text()

    check("AUTHORS.txt as authoritative" in legacy_authors_text, "legacy AUTHORS points to AUTHORS.txt", errors)
    check(bool(authors), "AUTHORS.txt has at least one non-comment entry", errors)
    check(bool(contributors), "CONTRIBUTORS.txt has at least one non-comment entry", errors)
    check("SIL OPEN FONT LICENSE Version 1.1" in ofl_text, "OFL.txt contains the OFL 1.1 text", errors)
    check("Copyright 2025 The Virtua Grotesk Project Authors" in ofl_text, "OFL.txt contains project copyright", errors)
    check("Reserved Font Name" in ofl_text, "OFL.txt includes Reserved Font Name terms", errors)
    check(
        ofl_text.splitlines()[1] == "",
        "OFL.txt has no Reserved Font Name declaration after the copyright line",
        errors,
    )


def report_errors(errors: list[str]) -> None:
    shaping_report = ROOT / "documentation/arabic-shaping-smoke-test.md"
    mark_report = ROOT / "documentation/arabic-mark-readiness.md"
    arabic_review_report = ROOT / "documentation/arabic-review-packet.md"
    arabic_source_report = ROOT / "documentation/arabic-source-work-checklist.md"
    arabic_candidate_report = ROOT / "documentation/arabic-candidate-glyph-plan.md"
    arabic_goal_report = ROOT / "documentation/arabic-goal-completion-audit.md"
    arabic_visual_risk_report = ROOT / "documentation/arabic-visual-risk-audit.md"
    arabic_visual_risk_proof = ROOT / "documentation/arabic-visual-risk-proof.html"
    arabic_structure_sweep = ROOT / "documentation/arabic-structure-sweep.html"
    arabic_structure_triage = ROOT / "documentation/arabic-structure-triage.md"
    arabic_mark_review_proof = ROOT / "documentation/arabic-mark-review-proof.html"
    arabic_mark_triage = ROOT / "documentation/arabic-mark-triage.md"
    arabic_visual_report = ROOT / "documentation/arabic-visual-review-checklist.md"
    arabic_visual_log_report = ROOT / "documentation/arabic-visual-review-log.md"
    arabic_manual_review_dashboard = ROOT / "documentation/arabic-manual-review-dashboard.html"
    arabic_next_review_batch = ROOT / "documentation/arabic-next-review-batch.html"
    arabic_manual_review_batches = ROOT / "documentation/arabic-manual-review-batches.md"
    arabic_current_review_worksheet = ROOT / "documentation/arabic-current-review-worksheet.md"
    arabic_review_worksheet_bundle = ROOT / "documentation/arabic-review-worksheet-bundle.md"
    arabic_batch_recorder = ROOT / "documentation/arabic-batch-recorder.md"
    arabic_first_review_zoom_snapshots = ROOT / "documentation/arabic-first-review-zoom-snapshots.md"
    arabic_first_review_crop_integrity = ROOT / "documentation/arabic-first-review-crop-integrity.md"
    arabic_first_review_batch = ROOT / "documentation/arabic-first-review-batch.md"
    arabic_first_review_risk_shortlist = ROOT / "documentation/arabic-first-review-risk-shortlist.md"
    arabic_first_review_ai_sweep = ROOT / "documentation/arabic-first-review-ai-sweep.md"
    arabic_manual_edit_targets = ROOT / "documentation/arabic-manual-edit-targets.md"
    arabic_hand_review_session = ROOT / "documentation/arabic-hand-review-session.md"
    arabic_hand_review_contact_sheet = ROOT / "documentation/arabic-hand-review-contact-sheet.html"
    arabic_print_proof_index = ROOT / "documentation/arabic-print-proof-index.md"
    arabic_next_review_packet = ROOT / "documentation/arabic-next-review-packet.md"
    arabic_next_review_ai_triage = ROOT / "documentation/arabic-next-review-ai-triage.md"
    arabic_next_review_ai_observations = ROOT / "documentation/arabic-next-review-ai-observations.md"
    arabic_full_queue_ai_sweep = ROOT / "documentation/arabic-full-queue-ai-sweep.md"
    arabic_next_review_board = ROOT / "documentation/arabic-next-review-board.html"
    arabic_snapshot_integrity = ROOT / "documentation/arabic-snapshot-integrity.md"
    arabic_visual_runbook = ROOT / "documentation/arabic-visual-review-runbook.md"
    generated_metadata_report = ROOT / "documentation/generated-font-metadata.md"
    production_requirements_report = ROOT / "documentation/google-fonts-production-requirements.md"
    numeric_feature_report = ROOT / "documentation/numeric-feature-readiness.md"
    release_metadata_report = ROOT / "documentation/release-metadata.md"
    release_source_report = ROOT / "documentation/release-source-readiness.md"
    release_archive_report = ROOT / "documentation/release-archive-manifest.md"
    github_release_report = ROOT / "documentation/github-release-draft.md"
    github_release_notes = ROOT / "documentation/github-release-notes.md"
    packager_strategy_report = ROOT / "documentation/packager-source-strategy.md"
    upstream_structure_report = ROOT / "documentation/upstream-structure-readiness.md"
    glyphset_report = ROOT / "documentation/gf-glyphset-readiness.md"
    pua_report = ROOT / "documentation/pua-scope.md"
    variable_report = ROOT / "documentation/variable-font-metadata.md"
    axis_registry_report = ROOT / "documentation/google-fonts-axis-registry-audit.md"
    source_report = ROOT / "documentation/source-ufo-metadata.md"
    master_report = ROOT / "documentation/master-compatibility.md"
    ufo_editor_report = ROOT / "documentation/ufo-editor-readiness.md"
    arabic_report = ROOT / "documentation/missing-gf-arabic-core.md"
    missing_report = ROOT / "documentation/missing-gf-latin-core.md"
    reachability_report = ROOT / "documentation/glyph-reachability.md"
    contour_report = ROOT / "documentation/fontspector-contour-count.md"
    contour_proof_report = ROOT / "documentation/contour-cleanup-proof.html"
    contour_queue_report = ROOT / "documentation/contour-cleanup-review-queue.md"
    contour_edit_plan_report = ROOT / "documentation/contour-cleanup-edit-plan.md"
    cleanup_briefs_report = ROOT / "documentation/arabic-cleanup-drawing-briefs.md"
    contour_batches_report = ROOT / "documentation/contour-cleanup-batches.md"
    contour_decision_report = ROOT / "documentation/contour-cleanup-decision-log.md"
    contour_ai_triage_report = ROOT / "documentation/contour-cleanup-ai-triage.md"
    contour_source_edit_report = ROOT / "documentation/contour-cleanup-source-edit-runlist.md"
    contour_first_batch_report = ROOT / "documentation/contour-cleanup-first-edit-batch.md"
    warning_report = ROOT / "documentation/fontspector-warnings.md"
    metadata_warning_probe_report = ROOT / "documentation/fontspector-metadata-warning-probe.md"
    zero_warning_report = ROOT / "documentation/fontspector-zero-warning-worklist.md"
    full_report = ROOT / "documentation/fontspector-googlefonts-report.md"
    shaping_text = shaping_report.read_text()
    mark_text = mark_report.read_text()
    arabic_review_text = arabic_review_report.read_text()
    arabic_source_text = arabic_source_report.read_text()
    arabic_candidate_text = arabic_candidate_report.read_text()
    arabic_goal_text = arabic_goal_report.read_text()
    arabic_visual_risk_text = arabic_visual_risk_report.read_text()
    arabic_visual_risk_proof_text = arabic_visual_risk_proof.read_text()
    arabic_structure_sweep_text = arabic_structure_sweep.read_text()
    arabic_structure_triage_text = arabic_structure_triage.read_text()
    arabic_mark_review_proof_text = arabic_mark_review_proof.read_text()
    arabic_mark_triage_text = arabic_mark_triage.read_text()
    arabic_visual_text = arabic_visual_report.read_text()
    arabic_visual_log_text = arabic_visual_log_report.read_text()
    arabic_manual_review_dashboard_text = arabic_manual_review_dashboard.read_text()
    arabic_next_review_batch_text = arabic_next_review_batch.read_text()
    arabic_manual_review_batches_text = arabic_manual_review_batches.read_text()
    arabic_current_review_worksheet_text = arabic_current_review_worksheet.read_text()
    arabic_review_worksheet_bundle_text = arabic_review_worksheet_bundle.read_text()
    arabic_batch_recorder_text = arabic_batch_recorder.read_text()
    arabic_first_review_zoom_snapshots_text = arabic_first_review_zoom_snapshots.read_text()
    arabic_first_review_crop_integrity_text = arabic_first_review_crop_integrity.read_text()
    arabic_first_review_batch_text = arabic_first_review_batch.read_text()
    arabic_first_review_risk_shortlist_text = arabic_first_review_risk_shortlist.read_text()
    arabic_first_review_ai_sweep_text = arabic_first_review_ai_sweep.read_text()
    arabic_manual_edit_targets_text = arabic_manual_edit_targets.read_text()
    arabic_hand_review_session_text = arabic_hand_review_session.read_text()
    arabic_hand_review_contact_sheet_text = arabic_hand_review_contact_sheet.read_text()
    arabic_print_proof_index_text = arabic_print_proof_index.read_text()
    arabic_next_review_packet_text = arabic_next_review_packet.read_text()
    arabic_next_review_ai_triage_text = arabic_next_review_ai_triage.read_text()
    arabic_next_review_ai_observations_text = arabic_next_review_ai_observations.read_text()
    arabic_full_queue_ai_sweep_text = arabic_full_queue_ai_sweep.read_text()
    arabic_next_review_board_text = arabic_next_review_board.read_text()
    arabic_snapshot_integrity_text = arabic_snapshot_integrity.read_text()
    arabic_visual_runbook_text = arabic_visual_runbook.read_text()
    generated_metadata_text = generated_metadata_report.read_text()
    production_requirements_text = production_requirements_report.read_text()
    numeric_feature_text = numeric_feature_report.read_text()
    release_metadata_text = release_metadata_report.read_text()
    release_source_text = release_source_report.read_text()
    release_archive_text = release_archive_report.read_text()
    github_release_text = github_release_report.read_text()
    github_release_notes_text = github_release_notes.read_text()
    packager_strategy_text = packager_strategy_report.read_text()
    upstream_structure_text = upstream_structure_report.read_text()
    glyphset_text = glyphset_report.read_text()
    pua_text = pua_report.read_text()
    variable_text = variable_report.read_text()
    axis_registry_text = axis_registry_report.read_text()
    source_text = source_report.read_text()
    master_text = master_report.read_text()
    ufo_editor_text = ufo_editor_report.read_text()
    arabic_text = arabic_report.read_text()
    missing_text = missing_report.read_text()
    reachability_text = reachability_report.read_text()
    contour_text = contour_report.read_text()
    contour_proof_text = contour_proof_report.read_text()
    contour_queue_text = contour_queue_report.read_text()
    contour_edit_plan_text = contour_edit_plan_report.read_text()
    cleanup_briefs_text = cleanup_briefs_report.read_text()
    contour_batches_text = contour_batches_report.read_text()
    contour_decision_text = contour_decision_report.read_text()
    contour_ai_triage_text = contour_ai_triage_report.read_text()
    contour_source_edit_text = contour_source_edit_report.read_text()
    contour_first_batch_text = contour_first_batch_report.read_text()
    warning_text = warning_report.read_text()
    metadata_warning_probe_text = metadata_warning_probe_report.read_text()
    zero_warning_text = zero_warning_report.read_text()
    full_report_text = full_report.read_text()
    check("Has GSUB: `true`" in shaping_text, "Arabic shaping report confirms GSUB table", errors)
    check("GSUB script records:" in shaping_text, "Arabic shaping report records GSUB script records", errors)
    check("GSUB has `arab/dflt`: `true`" in shaping_text, "Arabic shaping report confirms arab/dflt GSUB script record", errors)
    check("GPOS script records:" in shaping_text, "Arabic shaping report records GPOS script records", errors)
    check("GPOS has `arab/dflt`:" in shaping_text, "Arabic shaping report tracks arab/dflt GPOS script record", errors)
    check("uni06440627" in shaping_text, "Arabic shaping report confirms lam-alef substitution", errors)
    check("HarfBuzz buffer: direction `rtl`, script `Arab`, language `ar`" in shaping_text, "Arabic shaping report records HarfBuzz Arabic buffer settings", errors)
    check(".notdef` count" in shaping_text, "Arabic shaping report includes notdef counts", errors)
    check("Contextual forms present" in shaping_text, "Arabic shaping report tracks contextual forms", errors)
    check("Lam-alef ligature present" in shaping_text, "Arabic shaping report tracks lam-alef ligature behavior", errors)
    shaping_rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in shaping_text.splitlines()
        if line.startswith("| `")
    ]
    notdef_counts = [int(row[3]) for row in shaping_rows if len(row) >= 8 and row[3].isdigit()]
    check(bool(notdef_counts), "Arabic shaping report has sample rows", errors)
    check(
        all(count == 0 for count in notdef_counts),
        "Arabic shaping smoke samples have no .notdef glyphs",
        errors,
    )
    contextual_rows = [row for row in shaping_rows if len(row) >= 8 and row[4] == "yes"]
    lam_alef_rows = [row for row in shaping_rows if len(row) >= 8 and row[6] == "yes"]
    check(bool(contextual_rows), "Arabic shaping report has contextual-form expectation rows", errors)
    check(
        contextual_rows and all(row[5] == "yes" for row in contextual_rows),
        "Arabic shaping samples meet contextual-form expectations",
        errors,
    )
    check(bool(lam_alef_rows), "Arabic shaping report has lam-alef expectation rows", errors)
    check(
        lam_alef_rows and all(row[7] == "yes" for row in lam_alef_rows),
        "Arabic shaping samples meet lam-alef ligature expectations",
        errors,
    )
    for font_path in EXPECTED_FONT_OUTPUTS:
        check(font_path in shaping_text, f"Arabic shaping report includes {font_path}", errors)
    check("# Arabic Mark Readiness" in mark_text, "Arabic mark readiness report has expected heading", errors)
    check("Minimum Arabic target: `GF_Arabic_Core`" in mark_text, "Arabic mark readiness report documents Arabic Core target", errors)
    check("U+25CC dotted circle present:" in mark_text, "Arabic mark readiness report tracks dotted circle", errors)
    check("Source anchors present:" in mark_text, "Arabic mark readiness report tracks source anchors", errors)
    check("Built mark/mkmk GPOS features present:" in mark_text, "Arabic mark readiness report tracks mark GPOS features", errors)
    check("## Required Arabic Marks" in mark_text, "Arabic mark readiness report lists required Arabic marks", errors)
    for font_path in EXPECTED_FONT_OUTPUTS:
        check(font_path in mark_text, f"Arabic mark readiness report includes {font_path}", errors)
    check("# Arabic Review Packet" in arabic_review_text, "Arabic review packet has expected heading", errors)
    check("Minimum target: `GF_Arabic_Core`" in arabic_review_text, "Arabic review packet records Arabic Core target", errors)
    arabic_missing = report_count(arabic_text, "Missing codepoints")
    check(
        arabic_missing is not None
        and f"Missing codepoints: {arabic_missing}" in arabic_review_text,
        "Arabic review packet records current Arabic Core gap",
        errors,
    )
    check("Arabic GSUB smoke pass: 5 / 5 fonts" in arabic_review_text, "Arabic review packet summarizes GSUB smoke status", errors)
    check("Arabic GPOS smoke pass: 5 / 5 fonts" in arabic_review_text, "Arabic review packet summarizes GPOS smoke status", errors)
    check("U+25CC dotted circle present: yes" in arabic_review_text, "Arabic review packet summarizes dotted-circle status", errors)
    check("Drawing And Source Work Buckets" in arabic_review_text, "Arabic review packet includes drawing/source work buckets", errors)
    check("## Recent Arabic Google Fonts Reference" in arabic_review_text, "Arabic review packet includes recent Arabic GF reference section", errors)
    check("Package path: `ofl/estedad`" in arabic_review_text, "Arabic review packet cites Estedad package path", errors)
    check("Source repo: `https://github.com/aminabedi68/Estedad`" in arabic_review_text, "Arabic review packet cites Estedad upstream repo", errors)
    check("Primary script: `Arab`" in arabic_review_text, "Arabic review packet cites Estedad primary_script", errors)
    check("Subsets: `arabic, latin, latin-ext, menu, vietnamese`" in arabic_review_text, "Arabic review packet cites Estedad subsets", errors)
    check("Variable source file under `fonts/variable/`: yes" in arabic_review_text, "Arabic review packet cites Estedad variable font source path", errors)
    check("`source.config_yaml`: `sources/config.yaml`" in arabic_review_text, "Arabic review packet cites Estedad source.config_yaml", errors)
    check("final Packager source strategy deliberately supports a reproducible source" in arabic_review_text, "Arabic review packet limits config_yaml precedent to source-strategy decision", errors)
    check("Estedad exposes its served variable font from `fonts/variable/`" in arabic_review_text, "Arabic review packet links Estedad to Virtua source-strategy decision", errors)
    for report_path in [
        "documentation/missing-gf-arabic-core.md",
        "documentation/arabic-source-work-checklist.md",
        "documentation/arabic-mark-readiness.md",
        "documentation/arabic-shaping-smoke-test.md",
        "documentation/google-fonts-language-metadata.md",
        "documentation/recent-google-fonts-packages.md",
        "documentation/glyph-reachability.md",
    ]:
        check(report_path in arabic_review_text, f"Arabic review packet links {report_path}", errors)
    check("# Arabic Visual Review Checklist" in arabic_visual_text, "Arabic visual review checklist has expected heading", errors)
    check("GF Arabic Core coverage: 224 / 224 present; 0 missing." in arabic_visual_text, "Arabic visual review checklist records current Arabic coverage", errors)
    check("Google Fonts QA proof files: 16 / 16 present" in arabic_visual_text, "Arabic visual review checklist records current proof coverage", errors)
    check("Human visual review: 32 pending rows" in arabic_visual_text, "Arabic visual review checklist records current pending review count", errors)
    check("Contour-count cleanup: 0 current review items" in arabic_visual_text, "Arabic visual review checklist records closed contour queue", errors)
    check("documentation/arabic-manual-review-dashboard.html" in arabic_visual_text, "Arabic visual review checklist links manual dashboard", errors)
    check("documentation/arabic-next-review-batch.html" in arabic_visual_text, "Arabic visual review checklist links focused next-batch page", errors)
    check("documentation/gftools-qa/Proof" in arabic_visual_text, "Arabic visual review checklist links proof directory", errors)
    check("documentation/contour-cleanup-edit-plan.md" in arabic_visual_text, "Arabic visual review checklist links contour edit plan", errors)
    check("documentation/arabic-cleanup-drawing-briefs.md" in arabic_visual_text, "Arabic visual review checklist links cleanup drawing briefs", errors)
    check("documentation/contour-cleanup-batches.md" in arabic_visual_text, "Arabic visual review checklist links contour cleanup batches", errors)
    check("documentation/contour-cleanup-decision-log.md" in arabic_visual_text, "Arabic visual review checklist links contour cleanup decision log", errors)
    check("documentation/arabic-manual-review-batches.md" in arabic_visual_text, "Arabic visual review checklist links manual review batches", errors)
    check("If a later build reintroduces contour findings" in arabic_visual_text, "Arabic visual review checklist explains contour artifacts are evidence unless findings return", errors)
    for proof_type in ["Glyphs", "Text", "Proofer", "Waterfall"]:
        check(f"| {proof_type} |" in arabic_visual_text, f"Arabic visual review checklist includes {proof_type} proof row", errors)
    for sample_label in ["salaam", "arabic", "bismillah", "lam-alef"]:
        check(f"| {sample_label} |" in arabic_visual_text, f"Arabic visual review checklist includes {sample_label} smoke string", errors)
    for phrase in [
        "dotted circle with top and bottom marks",
        "`smallHighTah-ar`, `noonGhunna-ar`, and `smallHighThreeDots-ar`",
        "Arabic letter structures",
        "Arabic mark combinations",
        "Dot-stack letters and helpers",
        "Arabic and Farsi numerals",
        "Arabic punctuation",
        "make contour-cleanup-proof",
        "make kerning-proof-check",
        "make kerning-proof-review-check",
        "make preflight",
    ]:
        check(phrase in arabic_visual_text, f"Arabic visual review checklist records: {phrase}", errors)
    check("# Arabic Visual Review Log" in arabic_visual_log_text, "Arabic visual review log has expected heading", errors)
    check("Visual review ready:" in arabic_visual_log_text, "Arabic visual review log keeps review readiness explicit", errors)
    check("Review rows: 32" in arabic_visual_log_text, "Arabic visual review log records current row count", errors)
    check("Pending:" in arabic_visual_log_text, "Arabic visual review log records pending count", errors)
    check("Pass:" in arabic_visual_log_text, "Arabic visual review log records pass count", errors)
    check("Fix-needed:" in arabic_visual_log_text, "Arabic visual review log records fix-needed count", errors)
    check("Deferred:" in arabic_visual_log_text, "Arabic visual review log records deferred count", errors)
    check("Google Fonts QA proof files: 16 / 16 present" in arabic_visual_log_text, "Arabic visual review log records current proof count", errors)
    check("Manual review dashboard: `documentation/arabic-manual-review-dashboard.html`" in arabic_visual_log_text, "Arabic visual review log records dashboard evidence", errors)
    check("Status values: `pending`, `pass`, `fix-needed`, or `deferred`." in arabic_visual_log_text, "Arabic visual review log documents status values", errors)
    check("| Key | Area | Item | Evidence | Machine precheck | Review cue | Status | Reviewer | Notes |" in arabic_visual_log_text, "Arabic visual review log includes machine precheck column", errors)
    check("Structure triage mechanical blockers: 0" in arabic_visual_log_text, "Arabic visual review log surfaces structure triage blocker count", errors)
    check("Mark triage mechanical blockers: 0" in arabic_visual_log_text, "Arabic visual review log surfaces mark triage blocker count", errors)
    check("Shaping smoke mechanical pass: yes" in arabic_visual_log_text, "Arabic visual review log surfaces shaping smoke pass state", errors)
    check("make arabic-visual-review-update" in arabic_visual_log_text, "Arabic visual review log documents guarded update helper", errors)
    for key in [
        "proof-regular-glyphs",
        "proof-bold-waterfall",
        "smoke-lam-alef",
        "mark-dotted-circle",
        "class-dot-stack-helpers",
    ]:
        check(f"`{key}`" in arabic_visual_log_text, f"Arabic visual review log includes {key}", errors)
    visual_log_rows = markdown_rows(arabic_visual_log_text)
    visual_log_statuses = [row[6] if len(row) >= 9 else row[5] for row in visual_log_rows if len(row) >= 8]
    allowed_visual_statuses = {"pending", "pass", "fix-needed", "deferred"}
    check(
        len(visual_log_rows) == 32,
        "Arabic visual review log has one row per expected review item",
        errors,
    )
    check("Virtua Grotesk Arabic Manual Review Dashboard" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard has expected title", errors)
    check("Visual review pending:" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard records visual pending count", errors)
    check("Contour decisions pending:" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard records contour pending count", errors)
    check("Visual risk rows:" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard records risk row count", errors)
    check("Contour Decision Queue" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard keeps contour queue section", errors)
    check("Contour decisions pending: 0" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard records current contour pending state", errors)
    check("Rubik previews are structural references only" in arabic_manual_review_dashboard_text, "Arabic manual review dashboard explains Rubik reference limits", errors)
    for sample in ["سلام", "العربية", "بسم الله", "لا لأ لإ لآ", "٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹"]:
        check(sample in arabic_manual_review_dashboard_text, f"Arabic manual review dashboard includes sample {sample}", errors)
    for section in ["Embedded Arabic Samples", "Visual Risk Rows", "Contour Decision Queue", "Google Fonts Proof Links"]:
        check(section in arabic_manual_review_dashboard_text, f"Arabic manual review dashboard includes {section}", errors)
    check("Virtua Grotesk Arabic Next Review Batch" in arabic_next_review_batch_text, "Arabic next review batch has expected title", errors)
    check("Structure And Wrong-Glyph Sweep" in arabic_next_review_batch_text, "Arabic next review batch names current batch", errors)
    check("Visual rows: 5" in arabic_next_review_batch_text, "Arabic next review batch records current visual row count", errors)
    check("Contour rows: 0" in arabic_next_review_batch_text, "Arabic next review batch records current contour row count", errors)
    check("Glyph proof links: 4" in arabic_next_review_batch_text, "Arabic next review batch records current glyph proof count", errors)
    check("Rubik previews are structural references only" in arabic_next_review_batch_text, "Arabic next review batch explains Rubik reference limits", errors)
    check("make arabic-visual-review-update" in arabic_next_review_batch_text, "Arabic next review batch includes visual update command", errors)
    check("<tbody></tbody>" in arabic_next_review_batch_text, "Arabic next review batch records current empty contour table", errors)
    check("diffbrowsers_glyphs" in arabic_next_review_batch_text, "Arabic next review batch links glyph proof files", errors)
    check("Virtua Grotesk Arabic Structure Sweep" in arabic_structure_sweep_text, "Arabic structure sweep has expected title", errors)
    check("GF_Arabic_Core" in arabic_structure_sweep_text, "Arabic structure sweep records GF Arabic Core source", errors)
    check("U+25CC" in arabic_structure_sweep_text, "Arabic structure sweep includes dotted circle", errors)
    check("ARABIC LETTER BEH" in arabic_structure_sweep_text, "Arabic structure sweep includes Arabic letter rows", errors)
    check("VirtuaStructureRegular" in arabic_structure_sweep_text, "Arabic structure sweep embeds Regular font face", errors)
    check("VirtuaStructureBold" in arabic_structure_sweep_text, "Arabic structure sweep embeds Bold font face", errors)
    check("# Arabic Structure Triage" in arabic_structure_triage_text, "Arabic structure triage has expected heading", errors)
    check("Mechanical blocking risks: 0" in arabic_structure_triage_text, "Arabic structure triage has no mechanical blockers", errors)
    check("Shared visible cmap mappings: 0" in arabic_structure_triage_text, "Arabic structure triage has no shared visible cmap mappings", errors)
    check("large-negative-left-sidebearing" in arabic_structure_triage_text, "Arabic structure triage records sidebearing review prompts", errors)
    check("Virtua Grotesk Arabic Mark Review Proof" in arabic_mark_review_proof_text, "Arabic mark review proof has expected title", errors)
    check("mark-base+fatha" in arabic_mark_review_proof_text, "Arabic mark review proof links fatha review row", errors)
    check("mark-dotted-circle" in arabic_mark_review_proof_text, "Arabic mark review proof links dotted-circle review row", errors)
    check("Required mark inventory" in arabic_mark_review_proof_text, "Arabic mark review proof includes required mark inventory", errors)
    check("VirtuaMarkRegular" in arabic_mark_review_proof_text, "Arabic mark review proof embeds Regular font face", errors)
    check("VirtuaMarkBold" in arabic_mark_review_proof_text, "Arabic mark review proof embeds Bold font face", errors)
    check("# Arabic Mark Triage" in arabic_mark_triage_text, "Arabic mark triage has expected heading", errors)
    check("Mechanical blocking risks: 0" in arabic_mark_triage_text, "Arabic mark triage has no mechanical blockers", errors)
    check("No-offset mark review prompts:" in arabic_mark_triage_text, "Arabic mark triage records no-offset review prompts", errors)
    check("## Review Sections" in arabic_mark_triage_text, "Arabic mark triage lists review sections", errors)
    for review_key in [
        "mark-base+fatha",
        "mark-base+damma",
        "mark-base+kasra",
        "mark-shadda+sukun",
        "mark-tanween",
        "mark-hamza-above-below",
        "mark-dotted-circle",
        "class-mark-combinations",
    ]:
        check(f"`{review_key}`" in arabic_mark_triage_text, f"Arabic mark triage includes {review_key}", errors)
    check("# Arabic Manual Review Batches" in arabic_manual_review_batches_text, "Arabic manual review batches report has expected heading", errors)
    check("## Next Unresolved Batch" in arabic_manual_review_batches_text, "Arabic manual review batches report names next unresolved batch", errors)
    check("Start with **2. Structure And Wrong-Glyph Sweep**." in arabic_manual_review_batches_text, "Arabic manual review batches report points at current next review batch", errors)
    check("Open decisions: 5" in arabic_manual_review_batches_text, "Arabic manual review batches report records current next-batch decision count", errors)
    check("First visual-review command pattern:" in arabic_manual_review_batches_text, "Arabic manual review batches report includes first visual command pattern", errors)
    check("Contour rows: 0 (none)" in arabic_manual_review_batches_text, "Arabic manual review batches report records current contour command rows", errors)
    check("Snapshot evidence:" in arabic_manual_review_batches_text, "Arabic manual review batches include snapshot evidence summary", errors)
    check("Snapshot evidence ready for hand review: yes" in arabic_manual_review_batches_text, "Arabic manual review batches confirm snapshot evidence readiness", errors)
    check("Readable PNG files: 33" in arabic_manual_review_batches_text, "Arabic manual review batches confirm readable snapshot count", errors)
    check("Nonblank PNG files: 33" in arabic_manual_review_batches_text, "Arabic manual review batches confirm nonblank snapshot count", errors)
    check("Pending/fix-needed rows without snapshot: 0" in arabic_manual_review_batches_text, "Arabic manual review batches confirm no missing snapshots", errors)
    check("documentation/arabic-first-review-zoom-snapshots.md" in arabic_manual_review_batches_text, "Arabic manual review batches link focused zoom snapshot report", errors)
    check("documentation/arabic-full-queue-ai-sweep.md" in arabic_manual_review_batches_text, "Arabic manual review batches link full queue AI sweep", errors)
    check("AI observation" in arabic_manual_review_batches_text, "Arabic manual review batches include AI observation column", errors)
    check("Human follow-up" in arabic_manual_review_batches_text, "Arabic manual review batches include human follow-up column", errors)
    check("not Arabic drawing proof by itself" in arabic_manual_review_batches_text, "Arabic manual review batches carry proofer non-decision guidance", errors)
    check("Snapshot aids:" in arabic_manual_review_batches_text, "Arabic manual review batches include per-batch snapshot aids", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs.png" in arabic_manual_review_batches_text, "Arabic manual review batches link first proof snapshot", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_manual_review_batches_text, "Arabic manual review batches link first focused zoom crop", errors)
    check("focused 2x crop" in arabic_manual_review_batches_text, "Arabic manual review batches label focused zoom crops", errors)
    check("documentation/arabic-review-snapshots/mark-base+fatha.png" in arabic_manual_review_batches_text, "Arabic manual review batches link mark proof snapshot", errors)
    for batch_heading in [
        "Open The Fast Dashboard",
        "Structure And Wrong-Glyph Sweep",
        "Marks, Dotted Circle, And Stacking",
        "Dot-Stack Helpers And Urdu/Persian Texture",
        "RTL Text, Punctuation, Numerals, And Spacing",
    ]:
        check(batch_heading in arabic_manual_review_batches_text, f"Arabic manual review batches include {batch_heading}", errors)
    for evidence_path in [
        "documentation/arabic-visual-review-log.md",
        "documentation/contour-cleanup-decision-log.md",
        "documentation/arabic-manual-review-dashboard.html",
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-mark-review-proof.html",
        "documentation/arabic-mark-triage.md",
        "documentation/arabic-next-review-batch.html",
        "documentation/arabic-next-review-snapshots.md",
        "documentation/arabic-snapshot-integrity.md",
        "documentation/gftools-qa/Proof/",
    ]:
        check(evidence_path in arabic_manual_review_batches_text, f"Arabic manual review batches link {evidence_path}", errors)
    for command_text in [
        "make arabic-manual-review-dashboard",
        "make arabic-visual-review-update",
        "make reports-only",
        "make preflight-only",
    ]:
        check(command_text in arabic_manual_review_batches_text, f"Arabic manual review batches include {command_text}", errors)
    check("# Arabic Current Review Worksheet" in arabic_current_review_worksheet_text, "Arabic current review worksheet has expected heading", errors)
    check("Name: 2. Structure And Wrong-Glyph Sweep" in arabic_current_review_worksheet_text, "Arabic current review worksheet points at current batch", errors)
    check("Visual rows: 5 (pending: 5)" in arabic_current_review_worksheet_text, "Arabic current review worksheet records visual row count", errors)
    check("Contour rows: 0 (none)" in arabic_current_review_worksheet_text, "Arabic current review worksheet records current contour rows", errors)
    check("documentation/arabic-first-review-ai-sweep.md" in arabic_current_review_worksheet_text, "Arabic current review worksheet links AI sweep notes", errors)
    check("## AI Triage Notes" in arabic_current_review_worksheet_text, "Arabic current review worksheet embeds AI triage notes", errors)
    check("They are not review decisions" in arabic_current_review_worksheet_text, "Arabic current review worksheet keeps AI notes non-decisional", errors)
    check("documentation/arabic-print-proof.pdf" in arabic_current_review_worksheet_text, "Arabic current review worksheet links Arabic print proof", errors)
    check("documentation/arabic-print-proof-index.md" in arabic_current_review_worksheet_text, "Arabic current review worksheet links Arabic print proof index", errors)
    check("## Print-Proof Pass" in arabic_current_review_worksheet_text, "Arabic current review worksheet includes print-proof pass guidance", errors)
    check("The PDF is a review aid" in arabic_current_review_worksheet_text, "Arabic current review worksheet keeps print proof non-decisional", errors)
    check("| Key | Current status | Machine precheck | Review cue | Observed issue or `none` | Source/proof location | Final status |" in arabic_current_review_worksheet_text, "Arabic current review worksheet includes fill-in table", errors)
    for key in [
        "proof-regular-glyphs",
        "proof-medium-glyphs",
        "proof-semibold-glyphs",
        "proof-bold-glyphs",
        "class-letter-structures",
    ]:
        check(f"`{key}`" in arabic_current_review_worksheet_text, f"Arabic current review worksheet includes row {key}", errors)
        check(
            f"REVIEW_KEY={key} REVIEW_STATUS=fix-needed" in arabic_current_review_worksheet_text,
            f"Arabic current review worksheet includes fix-needed command for {key}",
            errors,
        )
    for expected_text in [
        "documentation/arabic-structure-sweep.html",
        "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png",
        "outcomes only after opening the linked proof/source evidence",
        "documentation/arabic-manual-edit-targets.md",
        "make reports-only",
        "make preflight-only",
    ]:
        check(expected_text in arabic_current_review_worksheet_text, f"Arabic current review worksheet includes {expected_text}", errors)
    check("# Arabic Review Worksheet Bundle" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle has expected heading", errors)
    check("Pending/fix-needed visual rows: 32" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle records pending row count", errors)
    check("Worksheet rows: 32" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle covers every pending row", errors)
    check("Matches pending/fix-needed visual rows: yes" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle audit passes", errors)
    check("### 2. Structure And Wrong-Glyph Sweep" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes structure batch", errors)
    check("### 3. Marks, Dotted Circle, And Stacking" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes marks batch", errors)
    check("### 5. RTL Text, Punctuation, Numerals, And Spacing" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes spacing batch", errors)
    check("AI observation" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes AI observation column", errors)
    check("Observed issue or `none`" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes fill-in observed issue column", errors)
    check("REVIEW_STATUS=fix-needed" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle includes fix-needed commands", errors)
    check("documentation/arabic-manual-edit-targets.md" in arabic_review_worksheet_bundle_text, "Arabic review worksheet bundle links edit-target report", errors)
    check("# Arabic Batch Recorder" in arabic_batch_recorder_text, "Arabic batch recorder has expected heading", errors)
    check("It does not apply any" in arabic_batch_recorder_text, "Arabic batch recorder keeps no-apply framing", errors)
    check("Batch: 2. Structure And Wrong-Glyph Sweep" in arabic_batch_recorder_text, "Arabic batch recorder points at current unresolved batch", errors)
    check("Visual rows: 5 (pending: 5)" in arabic_batch_recorder_text, "Arabic batch recorder records current visual row count", errors)
    check("Contour rows: 0 (none)" in arabic_batch_recorder_text, "Arabic batch recorder records current contour rows", errors)
    for key in [
        "proof-regular-glyphs",
        "proof-medium-glyphs",
        "proof-semibold-glyphs",
        "proof-bold-glyphs",
        "class-letter-structures",
    ]:
        check(f"### `{key}`" in arabic_batch_recorder_text, f"Arabic batch recorder includes row {key}", errors)
        for status in ["pass", "fix-needed", "deferred"]:
            check(
                f"REVIEW_KEY={key} REVIEW_STATUS={status}" in arabic_batch_recorder_text,
                f"Arabic batch recorder includes {status} command for {key}",
                errors,
            )
    for expected_text in [
        "make reports-only",
        "make preflight-only",
        "documentation/arabic-manual-edit-targets.md",
        "Full Batch Order",
    ]:
        check(expected_text in arabic_batch_recorder_text, f"Arabic batch recorder includes {expected_text}", errors)
    check("# Arabic First Review Zoom Snapshots" in arabic_first_review_zoom_snapshots_text, "Arabic first review zoom snapshot report has expected heading", errors)
    check("Rendered zoom snapshots: 4" in arabic_first_review_zoom_snapshots_text, "Arabic first review zoom snapshot report renders all four crops", errors)
    check("Errors: 0" in arabic_first_review_zoom_snapshots_text, "Arabic first review zoom snapshot report records no crop errors", errors)
    check("Output scale: 2x" in arabic_first_review_zoom_snapshots_text, "Arabic first review zoom snapshot report records enlarged output scale", errors)
    check("Output size: 2880x1040" in arabic_first_review_zoom_snapshots_text, "Arabic first review zoom snapshot report records enlarged output size", errors)
    for expected_text in [
        "proof-regular-glyphs-arabic-zoom.png",
        "proof-medium-glyphs-arabic-zoom.png",
        "proof-semibold-glyphs-arabic-zoom.png",
        "proof-bold-glyphs-arabic-zoom.png",
        "They do not prove small mark placement",
    ]:
        check(expected_text in arabic_first_review_zoom_snapshots_text, f"Arabic first review zoom snapshot report includes {expected_text}", errors)
    for expected_text in [
        "# Arabic First Review Crop Integrity",
        "Expected dimensions: 2880x1040",
        "Readable crops: 4",
        "Nonblank crops: 4",
        "Evidence ready for hand review: yes",
        "proof-regular-glyphs-arabic-zoom.png",
        "No row was marked `pass`",
    ]:
        check(expected_text in arabic_first_review_crop_integrity_text, f"Arabic first review crop integrity report includes {expected_text}", errors)
    check("# Arabic First Review Batch" in arabic_first_review_batch_text, "Arabic first review batch has expected heading", errors)
    check("Review rows: 5" in arabic_first_review_batch_text, "Arabic first review batch records row count", errors)
    check("Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint" in arabic_first_review_batch_text, "Arabic first review batch records structure-first goal", errors)
    for key in [
        "proof-regular-glyphs",
        "proof-medium-glyphs",
        "proof-semibold-glyphs",
        "proof-bold-glyphs",
        "class-letter-structures",
    ]:
        check(f"### `{key}`" in arabic_first_review_batch_text, f"Arabic first review batch includes row {key}", errors)
        check(
            f"make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS=pass" in arabic_first_review_batch_text,
            f"Arabic first review batch includes pass command for {key}",
            errors,
        )
    for expected_text in [
        "documentation/gftools-qa/Proof/",
        "documentation/arabic-structure-triage.md",
        "documentation/arabic-visual-risk-proof.html",
        "documentation/arabic-manual-edit-targets.md",
        "documentation/arabic-first-review-ai-sweep.md",
        "documentation/arabic-first-review-zoom-snapshots.md",
        "documentation/arabic-first-review-crop-integrity.md",
        "documentation/arabic-first-review-risk-shortlist.md",
        "documentation/arabic-review-snapshots/proof-regular-glyphs.png",
        "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png",
        "sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif",
        "REVIEW_STATUS=fix-needed",
        "REVIEW_STATUS=deferred",
        "./build.sh",
        "make reports-only",
        "make preflight-only",
    ]:
        check(expected_text in arabic_first_review_batch_text, f"Arabic first review batch includes {expected_text}", errors)
    check("# Arabic First Review Risk Shortlist" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist has expected heading", errors)
    check("It is not a human" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist keeps non-human-review framing", errors)
    check("proof-regular-glyphs-arabic-zoom.png" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist references Regular focused crop", errors)
    check("documentation/arabic-first-review-crop-integrity.md" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist links crop integrity report", errors)
    check("No obvious tofu boxes" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist records AI-visible structure screen", errors)
    check("No row was marked `pass`" in arabic_first_review_risk_shortlist_text, "Arabic first review risk shortlist keeps non-decision framing", errors)
    check("# Arabic First Review AI Sweep" in arabic_first_review_ai_sweep_text, "Arabic first review AI sweep has expected heading", errors)
    check("It is not a human Arabic review" in arabic_first_review_ai_sweep_text, "Arabic first review AI sweep keeps non-human-review framing", errors)
    check(
        "documentation/arabic-review-snapshots/proof-medium-glyphs.png" in arabic_first_review_ai_sweep_text,
        "Arabic first review AI sweep records Medium snapshot evidence",
        errors,
    )
    check(
        "documentation/arabic-review-snapshots/proof-semibold-glyphs.png" in arabic_first_review_ai_sweep_text,
        "Arabic first review AI sweep records SemiBold snapshot evidence",
        errors,
    )
    check(
        "documentation/arabic-first-review-zoom-snapshots.md" in arabic_first_review_ai_sweep_text
        and "focused 2x crops make Arabic-row structure screening easier" in arabic_first_review_ai_sweep_text,
        "Arabic first review AI sweep records focused crop evidence and limits",
        errors,
    )
    check(
        "documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_first_review_ai_sweep_text,
        "Arabic first review AI sweep records Regular focused crop evidence",
        errors,
    )
    for key in [
        "proof-regular-glyphs",
        "proof-medium-glyphs",
        "proof-semibold-glyphs",
        "proof-bold-glyphs",
        "class-letter-structures",
    ]:
        check(f"`{key}`" in arabic_first_review_ai_sweep_text, f"Arabic first review AI sweep references {key}", errors)
    for expected_text in [
        "No row was marked `pass`",
        "No source glyph was marked `fix-needed`",
        "No spacing edit is recommended from this sweep alone",
    ]:
        check(expected_text in arabic_first_review_ai_sweep_text, f"Arabic first review AI sweep includes {expected_text}", errors)
    check("# Arabic Manual Edit Targets" in arabic_manual_edit_targets_text, "Arabic manual edit-target report has expected heading", errors)
    check("Use it only after a row is" in arabic_manual_edit_targets_text, "Arabic manual edit-target report keeps review-before-edit framing", errors)
    check("marked `fix-needed`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report ties edits to fix-needed rows", errors)
    check("Compatibility rule: edit Regular and Bold together" in arabic_manual_edit_targets_text, "Arabic manual edit-target report preserves master compatibility rule", errors)
    check("### `class-letter-structures`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report includes letter structure targets", errors)
    check("### `mark-shadda+sukun`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report includes mark prompt targets", errors)
    check("### `class-dot-stack-helpers`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report includes dot-stack helper targets", errors)
    check("### `class-arabic-farsi-numerals`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report includes numeral targets", errors)
    check("### `class-arabic-punctuation`" in arabic_manual_edit_targets_text, "Arabic manual edit-target report includes punctuation targets", errors)
    for path in [
        "sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif",
        "sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif",
        "sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif",
        "sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif",
        "sources/VirtuaGrotesk-Regular.ufo/glyphs/zeroFarsi-ar.glif",
        "sources/VirtuaGrotesk-Bold.ufo/glyphs/question-ar.glif",
    ]:
        check(path in arabic_manual_edit_targets_text, f"Arabic manual edit-target report links {path}", errors)
    check("# Arabic Hand Review Session" in arabic_hand_review_session_text, "Arabic hand-review session report has expected heading", errors)
    check("Pending/fix-needed rows in this sheet: 32" in arabic_hand_review_session_text, "Arabic hand-review session records pending queue count", errors)
    check("## Glyph Proof First Pass" in arabic_hand_review_session_text, "Arabic hand-review session includes glyph proof batch", errors)
    check("## Marks And Dotted Circle" in arabic_hand_review_session_text, "Arabic hand-review session includes mark batch", errors)
    check("## Proof Texture And Spacing" in arabic_hand_review_session_text, "Arabic hand-review session includes proof texture batch", errors)
    check("## Smoke Strings And Classes" in arabic_hand_review_session_text, "Arabic hand-review session includes smoke/class batch", errors)
    check("documentation/arabic-next-review-board.html" in arabic_hand_review_session_text, "Arabic hand-review session links local review board", errors)
    check("documentation/arabic-print-proof.pdf" in arabic_hand_review_session_text, "Arabic hand-review session links Arabic PDF proof", errors)
    check("documentation/arabic-print-proof-index.md" in arabic_hand_review_session_text, "Arabic hand-review session links Arabic PDF proof index", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_hand_review_session_text, "Arabic hand-review session links first focused zoom crop", errors)
    check("sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif" in arabic_hand_review_session_text, "Arabic hand-review session includes source GLIF targets", errors)
    check("make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass" in arabic_hand_review_session_text, "Arabic hand-review session includes pass command pattern", errors)
    check("REVIEW_STATUS=fix-needed" in arabic_hand_review_session_text, "Arabic hand-review session includes fix-needed command pattern", errors)
    check("Arabic Hand Review Contact Sheet" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet has expected title", errors)
    check("documentation/arabic-current-review-worksheet.md" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links current worksheet", errors)
    check("documentation/arabic-hand-review-session.md" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links session sheet", errors)
    check("documentation/arabic-print-proof.pdf" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links Arabic PDF proof", errors)
    check("documentation/arabic-manual-edit-targets.md" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links edit targets", errors)
    check("Evidence Integrity" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet includes evidence integrity summary", errors)
    check("documentation/arabic-snapshot-integrity.md" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links snapshot integrity report", errors)
    check("documentation/arabic-first-review-crop-integrity.md" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet links first-review crop integrity report", errors)
    check("They do not mark Arabic drawing rows as passed." in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet keeps integrity checks non-decisional", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs.png" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet embeds first proof snapshot", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet embeds first focused zoom crop", errors)
    check("focused 2x crop" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet labels focused zoom crops", errors)
    check("documentation/arabic-review-snapshots/class-arabic-punctuation.png" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet embeds final class snapshot", errors)
    check("make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass" in arabic_hand_review_contact_sheet_text, "Arabic hand-review contact sheet includes pass command pattern", errors)
    check("# Arabic Visual Review Runbook" in arabic_visual_runbook_text, "Arabic visual review runbook has expected heading", errors)
    check("Pending or fix-needed: 32" in arabic_visual_runbook_text, "Arabic visual review runbook records current pending count", errors)
    check("## Next Five Review Cards" in arabic_visual_runbook_text, "Arabic visual review runbook includes next-card section", errors)
    check("## Full Pending Queue" in arabic_visual_runbook_text, "Arabic visual review runbook includes full pending queue", errors)
    check("AI comparison prompt:" in arabic_visual_runbook_text, "Arabic visual review runbook includes AI comparison prompts", errors)
    check("Machine precheck:" in arabic_visual_runbook_text, "Arabic visual review runbook includes machine precheck summaries", errors)
    check("Snapshot report: `documentation/arabic-next-review-snapshots.md`" in arabic_visual_runbook_text, "Arabic visual review runbook links snapshot report", errors)
    check("Snapshot aids:" in arabic_visual_runbook_text, "Arabic visual review runbook includes per-row snapshot aids", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs.png" in arabic_visual_runbook_text, "Arabic visual review runbook links first proof snapshot", errors)
    check("documentation/arabic-first-review-zoom-snapshots.md" in arabic_visual_runbook_text, "Arabic visual review runbook links focused zoom snapshot report", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_visual_runbook_text, "Arabic visual review runbook links first focused zoom crop", errors)
    check("Structure triage mechanical blockers: 0" in arabic_visual_runbook_text, "Arabic visual review runbook surfaces structure triage blocker count", errors)
    check("| Key | Area | Item | Status | Machine precheck | Review cue |" in arabic_visual_runbook_text, "Arabic visual review runbook full queue includes machine precheck column", errors)
    check("Mark triage mechanical blockers: 0" in arabic_visual_runbook_text, "Arabic visual review runbook surfaces mark triage blocker count", errors)
    check("Shaping smoke mechanical pass: yes" in arabic_visual_runbook_text, "Arabic visual review runbook surfaces shaping smoke pass state", errors)
    check("make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass" in arabic_visual_runbook_text, "Arabic visual review runbook includes pass command pattern", errors)
    check("REVIEW_STATUS=fix-needed" in arabic_visual_runbook_text, "Arabic visual review runbook includes fix-needed command pattern", errors)
    check("REVIEW_STATUS=deferred" in arabic_visual_runbook_text, "Arabic visual review runbook includes deferred command pattern", errors)
    check("documentation/arabic-next-review-batch.html" in arabic_visual_runbook_text, "Arabic visual review runbook links focused next-batch page", errors)
    check("# Arabic Next Review Packet" in arabic_next_review_packet_text, "Arabic next review packet has expected heading", errors)
    check("Pending or fix-needed rows: 32" in arabic_next_review_packet_text, "Arabic next review packet records current pending count", errors)
    check("## Next Rows" in arabic_next_review_packet_text, "Arabic next review packet includes next rows table", errors)
    check("## Shared Structure Prompt Details" in arabic_next_review_packet_text, "Arabic next review packet includes shared structure prompt details", errors)
    check("Focused Arabic PDF proof: `documentation/arabic-print-proof.pdf`" in arabic_next_review_packet_text, "Arabic next review packet links focused Arabic PDF proof", errors)
    check("Focused Arabic PDF index: `documentation/arabic-print-proof-index.md`" in arabic_next_review_packet_text, "Arabic next review packet links focused Arabic PDF index", errors)
    check("## Fast Review Order" in arabic_next_review_packet_text, "Arabic next review packet includes fast review order", errors)
    check("The PDF speeds review; it does not replace source/proof" in arabic_next_review_packet_text, "Arabic next review packet keeps PDF proof non-decisional", errors)
    check("proof-regular-glyphs" in arabic_next_review_packet_text, "Arabic next review packet includes first proof row", errors)
    check("class-letter-structures" in arabic_next_review_packet_text, "Arabic next review packet includes current class review row", errors)
    check("make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass" in arabic_next_review_packet_text, "Arabic next review packet includes pass command pattern", errors)
    check("REVIEW_STATUS=fix-needed" in arabic_next_review_packet_text, "Arabic next review packet includes fix-needed command pattern", errors)
    check("REVIEW_STATUS=deferred" in arabic_next_review_packet_text, "Arabic next review packet includes deferred command pattern", errors)
    check("documentation/arabic-next-review-batch.html" in arabic_next_review_packet_text, "Arabic next review packet links focused next-batch page", errors)
    check("make arabic-next-review-ai-triage" in arabic_next_review_packet_text, "Arabic next review packet links AI-safe triage command", errors)
    check("make arabic-next-review-board" in arabic_next_review_packet_text, "Arabic next review packet links local board command", errors)
    check("ARABIC_SNAPSHOT_ARGS=\"--all-pending --limit 32 --timeout 20\"" in arabic_next_review_packet_text, "Arabic next review packet documents full-queue snapshot probe", errors)
    check("ARABIC_SNAPSHOT_ARGS=\"--all-pending --limit 32 --list-only --timeout 20\"" in arabic_next_review_packet_text, "Arabic next review packet documents non-GUI snapshot coverage check", errors)
    check("ARABIC_SNAPSHOT_ARGS=\"--all-pending --limit 32 --reuse-existing\"" in arabic_next_review_packet_text, "Arabic next review packet documents existing-PNG snapshot report rebuild", errors)
    check("documentation/arabic-review-snapshots/proof-regular-glyphs-arabic-zoom.png" in arabic_next_review_packet_text, "Arabic next review packet links first focused zoom crop", errors)
    check("# Arabic Next Review AI Triage" in arabic_next_review_ai_triage_text, "Arabic next review AI triage has expected heading", errors)
    check("## First-Batch AI Triage Summary" in arabic_next_review_ai_triage_text, "Arabic next review AI triage includes first-batch summary", errors)
    check("## Full Pending Queue AI Triage" in arabic_next_review_ai_triage_text, "Arabic next review AI triage includes full queue", errors)
    check("| 32 | `class-arabic-punctuation`" in arabic_next_review_ai_triage_text, "Arabic next review AI triage includes final pending row", errors)
    check("mechanical shaping passes; needs visual rhythm review" in arabic_next_review_ai_triage_text, "Arabic next review AI triage classifies smoke rows without passing them", errors)
    check("ready for mark-proof pass/fix/defer review" in arabic_next_review_ai_triage_text, "Arabic next review AI triage classifies mark rows", errors)
    check("documentation/arabic-next-review-board.html" in arabic_next_review_ai_triage_text, "Arabic next review AI triage links local board", errors)
    check("# Arabic Next Review AI Observations" in arabic_next_review_ai_observations_text, "Arabic next review AI observations has expected heading", errors)
    check("It is not a human Arabic review" in arabic_next_review_ai_observations_text, "Arabic next review AI observations keeps non-final-review framing", errors)
    check("## Full Queue Snapshot Evidence" in arabic_next_review_ai_observations_text, "Arabic next review AI observations includes full snapshot evidence table", errors)
    check("| `class-arabic-punctuation` |" in arabic_next_review_ai_observations_text, "Arabic next review AI observations includes final pending row", errors)
    check("Snapshot evidence ready for hand review: yes" in arabic_next_review_ai_observations_text, "Arabic next review AI observations records snapshot integrity readiness", errors)
    check("Focused zoom snapshot report" in arabic_next_review_ai_observations_text, "Arabic next review AI observations includes focused zoom snapshot source", errors)
    check("proof-regular-glyphs-arabic-zoom.png" in arabic_next_review_ai_observations_text, "Arabic next review AI observations includes focused glyph crop evidence", errors)
    check("# Arabic Full Queue AI Sweep" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep has expected heading", errors)
    check("Pending/fix-needed rows covered: 32" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep covers all pending rows", errors)
    check("## Coverage Audit" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep includes coverage audit", errors)
    check("Rows with AI observation: 32 / 32" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep covers every row with AI observations", errors)
    check("Rows with human follow-up: 32 / 32" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep covers every row with human follow-up", errors)
    check("Rows with snapshot evidence: 32 / 32" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep covers every row with snapshot evidence", errors)
    check("Coverage ready for human review: yes" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep marks coverage ready for human review", errors)
    check("Focused zoom snapshot source" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep includes focused zoom snapshot source", errors)
    check("proof-regular-glyphs-arabic-zoom.png" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep includes focused glyph crop evidence", errors)
    check("documentation/arabic-review-snapshots/mark-shadda+sukun.png" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep records inspected mark snapshot", errors)
    check("documentation/arabic-review-snapshots/proof-bold-text.png" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep records inspected text snapshot", errors)
    check("Proofer tofu in GF_Latin_Core proof snapshots" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep separates Latin Core tofu from Arabic drawing review", errors)
    check("No row was marked `pass`" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep keeps non-decision framing", errors)
    check("| `class-arabic-punctuation` | punctuation |" in arabic_full_queue_ai_sweep_text, "Arabic full queue AI sweep includes final pending row", errors)
    check("Arabic Next Review Board" in arabic_next_review_board_text, "Arabic next review board has expected title", errors)
    check("First-Batch Order" in arabic_next_review_board_text, "Arabic next review board includes first-batch order", errors)
    check("Decision Rules" in arabic_next_review_board_text, "Arabic next review board includes decision rules", errors)
    check("Record <code>fix-needed</code> with the exact glyph" in arabic_next_review_board_text, "Arabic next review board records fix-needed decision rule", errors)
    check("AI First-Pass Observation" in arabic_next_review_board_text, "Arabic next review board embeds AI observations", errors)
    check("Edit targets" in arabic_next_review_board_text, "Arabic next review board embeds edit-target sections", errors)
    check("arabic-manual-edit-targets.md" in arabic_next_review_board_text, "Arabic next review board links manual edit-target report", errors)
    check("arabic-current-review-worksheet.md" in arabic_next_review_board_text, "Arabic next review board links current review worksheet", errors)
    check("arabic-batch-recorder.md" in arabic_next_review_board_text, "Arabic next review board links batch recorder", errors)
    check("arabic-full-queue-ai-sweep.md" in arabic_next_review_board_text, "Arabic next review board links full queue AI sweep", errors)
    check("arabic-first-review-ai-sweep.md" in arabic_next_review_board_text, "Arabic next review board links first review AI sweep", errors)
    check("arabic-first-review-zoom-snapshots.md" in arabic_next_review_board_text, "Arabic next review board links first review zoom snapshots", errors)
    check(
        "sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif" in arabic_next_review_board_text,
        "Arabic next review board links a source GLIF target",
        errors,
    )
    check("Full Pending Queue" in arabic_next_review_board_text, "Arabic next review board includes full pending queue", errors)
    check("<tr><td>32</td><td><code>class-arabic-punctuation</code>" in arabic_next_review_board_text, "Arabic next review board includes final pending row", errors)
    check("<th>AI observation</th>" in arabic_next_review_board_text, "Arabic next review board includes full-queue AI observation column", errors)
    check("<th>Human follow-up</th>" in arabic_next_review_board_text, "Arabic next review board includes full-queue human follow-up column", errors)
    check(
        "Proofer snapshot currently reflects GF_Latin_Core content" in arabic_next_review_board_text,
        "Arabic next review board carries full-queue AI observations into the queue",
        errors,
    )
    check("arabic-next-review-ai-observations.md" in arabic_next_review_board_text, "Arabic next review board links observation source", errors)
    check("proof-regular-glyphs" in arabic_next_review_board_text, "Arabic next review board includes first proof row", errors)
    check("make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass" in arabic_next_review_board_text, "Arabic next review board includes pass command pattern", errors)
    check("# Arabic Snapshot Integrity" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report has expected heading", errors)
    check("Visual review pending/fix-needed rows: 32" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report records pending queue count", errors)
    check("Snapshot rows in report: 33" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report records expected snapshot count", errors)
    check("Unique review keys with snapshots: 32" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report covers every pending key", errors)
    check("Readable PNG files: 33" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report confirms readable PNGs", errors)
    check("Nonblank PNG files: 33" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report confirms nonblank PNGs", errors)
    check("Pending/fix-needed rows without snapshot: 0" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report has no missing pending snapshots", errors)
    check("Integrity errors: 0" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report has zero errors", errors)
    check("Snapshot evidence ready for hand review: yes" in arabic_snapshot_integrity_text, "Arabic snapshot integrity report marks evidence ready", errors)
    arabic_print_proof = ROOT / "documentation/arabic-print-proof.pdf"
    check(
        arabic_print_proof.exists() and arabic_print_proof.stat().st_size > 0,
        "Arabic print proof PDF exists and is nonempty",
        errors,
    )
    check("# Arabic Print Proof Index" in arabic_print_proof_index_text, "Arabic print proof index has expected heading", errors)
    check("PDF: `documentation/arabic-print-proof.pdf`" in arabic_print_proof_index_text, "Arabic print proof index links PDF", errors)
    check("Regular" in arabic_print_proof_index_text and "Bold" in arabic_print_proof_index_text, "Arabic print proof index maps Regular and Bold pages", errors)
    check("Arabic cmap grid" in arabic_print_proof_index_text, "Arabic print proof index includes cmap grid pages", errors)
    check("Record review outcomes only through" in arabic_print_proof_index_text, "Arabic print proof index keeps status updates guarded", errors)
    check(
        all(status in allowed_visual_statuses for status in visual_log_statuses),
        "Arabic visual review log uses only known statuses",
        errors,
    )
    check("# Arabic Source Work Checklist" in arabic_source_text, "Arabic source checklist has expected heading", errors)
    check("Minimum Arabic target: `GF_Arabic_Core`" in arabic_source_text, "Arabic source checklist documents Arabic Core target", errors)
    check("## Suggested Source Inventory" in arabic_source_text, "Arabic source checklist includes source glyph inventory", errors)
    check("## Batch Work Plan" in arabic_source_text, "Arabic source checklist includes batch work plan", errors)
    check("## Batch Glyph Lists" in arabic_source_text, "Arabic source checklist includes batch glyph lists", errors)
    check("Suggested source glyph names: 0" in arabic_source_text, "Arabic source checklist records current missing suggested source glyph count", errors)
    check("Suggested glyph names missing in both masters: 0" in arabic_source_text, "Arabic source checklist records current missing suggested names across masters", errors)
    check("# Arabic Candidate Glyph Plan" in arabic_candidate_text, "Arabic candidate glyph plan has expected heading", errors)
    check("Worklist glyphs: 256" in arabic_candidate_text, "Arabic candidate glyph plan preserves managed glyph worklist size", errors)
    check("Glyph-level buckets:" in arabic_candidate_text, "Arabic candidate glyph plan includes goal-level bucket summary", errors)
    check("Auto-created / would auto-create: 0" in arabic_candidate_text, "Arabic candidate glyph plan records current auto-created bucket count", errors)
    check("Review-needed: 256" in arabic_candidate_text, "Arabic candidate glyph plan records current review-needed bucket count", errors)
    check("Hand-draw-needed: 0" in arabic_candidate_text, "Arabic candidate glyph plan records current hand-draw-needed bucket count", errors)
    check("Compatibility-risk: 0" in arabic_candidate_text, "Arabic candidate glyph plan records current compatibility-risk bucket count", errors)
    check("Master-entry action counts:" in arabic_candidate_text, "Arabic candidate glyph plan keeps master-entry action counts separate", errors)
    check("Existing master entries counted: 512" in arabic_candidate_text, "Arabic candidate glyph plan counts both-master scaffold entries", errors)
    check("Compatibility-risk glyphs: 0" in arabic_candidate_text, "Arabic candidate glyph plan records compatibility-risk count", errors)
    check("## joining-letters" in arabic_candidate_text and "tteh-ar" in arabic_candidate_text, "Arabic candidate glyph plan includes Urdu/Persian joining-letter work", errors)
    check("## farsi-digits" in arabic_candidate_text and "zeroFarsi-ar" in arabic_candidate_text, "Arabic candidate glyph plan includes extended Arabic-Indic digit work", errors)
    check("## shared-punctuation" in arabic_candidate_text and "dottedCircle" in arabic_candidate_text, "Arabic candidate glyph plan includes dotted circle work", errors)
    check("# Arabic Goal Completion Audit" in arabic_goal_text, "Arabic goal completion audit has expected heading", errors)
    check("GF Arabic Core gaps are zero or accepted | 0 missing codepoints" in arabic_goal_text, "Arabic goal audit confirms Arabic Core coverage", errors)
    check("Missing source glyphs exist in both masters | missing codepoints: 0; suggested names: 0" in arabic_goal_text, "Arabic goal audit confirms source glyph worklist is closed", errors)
    check("Regular and Bold structures stay compatible | 0 blocking mismatches" in arabic_goal_text, "Arabic goal audit confirms master compatibility", errors)
    check("Arabic shaping smoke tests pass | fonts: 5; GSUB: 5/5; GPOS: 5/5; no .notdef: yes" in arabic_goal_text, "Arabic goal audit confirms shaping smoke status", errors)
    check("Dotted circle, marks, anchors, and mark/mkmk are ready or documented | missing marks: 0; dotted circle: yes; anchors: yes; mark/mkmk: yes" in arabic_goal_text, "Arabic goal audit confirms mark readiness", errors)
    check("first-review focused crops ready: yes; nonblank crops: 4" in arabic_goal_text, "Arabic goal audit includes first-review crop integrity readiness", errors)
    check("documentation/arabic-current-review-worksheet.md" in arabic_goal_text, "Arabic goal audit links current review worksheet", errors)
    check("documentation/arabic-next-review-board.html" in arabic_goal_text, "Arabic goal audit links next review board", errors)
    check("documentation/arabic-full-queue-ai-sweep.md" in arabic_goal_text, "Arabic goal audit links full queue AI sweep", errors)
    check("documentation/arabic-snapshot-integrity.md" in arabic_goal_text, "Arabic goal audit links snapshot integrity", errors)
    check("documentation/arabic-first-review-crop-integrity.md" in arabic_goal_text, "Arabic goal audit links first-review crop integrity report", errors)
    check("decision packet ready: yes" in arabic_goal_text, "Arabic goal audit confirms hand-review decision packet readiness", errors)
    check("board rows: 32/32" in arabic_goal_text, "Arabic goal audit confirms review board covers pending rows", errors)
    check("board command rows: 32/32" in arabic_goal_text, "Arabic goal audit confirms review board command coverage", errors)
    check("AI observation rows: 32/32" in arabic_goal_text, "Arabic goal audit confirms AI observation coverage", errors)
    check("human follow-up rows: 32/32" in arabic_goal_text, "Arabic goal audit confirms human follow-up coverage", errors)
    check("snapshot missing rows: 0" in arabic_goal_text, "Arabic goal audit confirms no missing review snapshots", errors)
    check("source target references: 180; missing target files: 0" in arabic_goal_text, "Arabic goal audit includes manual edit-target readiness", errors)
    check("# Arabic Visual Risk Audit" in arabic_visual_risk_text, "Arabic visual risk audit has expected heading", errors)
    check("Target glyphset: `GF_Arabic_Core` plus U+25CC dotted circle" in arabic_visual_risk_text, "Arabic visual risk audit records target glyphset", errors)
    check("Fonts checked: 5" in arabic_visual_risk_text, "Arabic visual risk audit checks all built fonts", errors)
    check("Codepoints checked per font:" in arabic_visual_risk_text, "Arabic visual risk audit records checked codepoint count", errors)
    check("## Risk Counts" in arabic_visual_risk_text, "Arabic visual risk audit includes risk counts", errors)
    check("## Risk Rows" in arabic_visual_risk_text, "Arabic visual risk audit includes risk rows table", errors)
    check("blank-visible-glyph" in arabic_visual_risk_text, "Arabic visual risk audit documents blank glyph risk", errors)
    check("Arabic Visual Risk Proof" in arabic_visual_risk_proof_text, "Arabic visual risk proof has expected title", errors)
    check("Risk rows:" in arabic_visual_risk_proof_text, "Arabic visual risk proof records risk row count", errors)
    check("sidebearing" in arabic_visual_risk_proof_text, "Arabic visual risk proof documents sidebearing review purpose", errors)
    check("VirtuaRiskRegular" in arabic_visual_risk_proof_text, "Arabic visual risk proof embeds Regular font face", errors)
    check("VirtuaRiskBold" in arabic_visual_risk_proof_text, "Arabic visual risk proof embeds Bold font face", errors)
    check(
        "Arabic drawings have human visual review" in arabic_goal_text
        and "visual pending:" in arabic_goal_text
        and "contour decisions pending: 0; fix-now: 0" in arabic_goal_text,
        "Arabic goal audit keeps visual review open and contour edits queued",
        errors,
    )
    check("# Generated Font Metadata" in generated_metadata_text, "generated font metadata report has expected heading", errors)
    check("## Names" in generated_metadata_text, "generated font metadata report includes names", errors)
    check("## Technical Metadata" in generated_metadata_text, "generated font metadata report includes technical metadata", errors)
    check("## Vertical Metrics" in generated_metadata_text, "generated font metadata report includes vertical metrics", errors)
    check("## License Strings" in generated_metadata_text, "generated font metadata report includes license strings", errors)
    for font_path in EXPECTED_FONT_OUTPUTS:
        check(font_path in generated_metadata_text, f"generated font metadata report includes {font_path}", errors)
    check("VirtuaGrotesk-SemiBold" in generated_metadata_text, "generated font metadata report includes SemiBold PostScript name", errors)
    check("Arab, Latn" in generated_metadata_text, "generated font metadata report includes script metadata", errors)
    check("1024/-296/0" in generated_metadata_text, "generated font metadata report includes vertical metric values", errors)
    check("https://openfontlicense.org" in generated_metadata_text, "generated font metadata report includes OFL URL", errors)
    check("# Google Fonts Production Requirements Audit" in production_requirements_text, "production requirements report has expected heading", errors)
    check("Built TTF outputs present: yes" in production_requirements_text, "production requirements report confirms built TTF outputs", errors)
    check("All handoff font binaries are `.ttf`: yes" in production_requirements_text, "production requirements report confirms TTF binary format", errors)
    check("One-command build path present: yes" in production_requirements_text, "production requirements report confirms one-command build path", errors)
    check("Open-source build toolchain documented: yes" in production_requirements_text, "production requirements report confirms open-source build toolchain", errors)
    check("Source UFO/designspace inputs present: yes" in production_requirements_text, "production requirements report confirms source inputs", errors)
    check("Installable embedding fsType across built fonts: yes" in production_requirements_text, "production requirements report confirms installable embedding", errors)
    check("Version strings match first-submission version `1.000`: yes" in production_requirements_text, "production requirements report confirms version strings", errors)
    check("Vertical metrics match GF source metrics: yes" in production_requirements_text, "production requirements report confirms vertical metrics", errors)
    check("Variable font has `fvar`: yes" in production_requirements_text, "production requirements report confirms fvar", errors)
    check("Variable font has `STAT`: yes" in production_requirements_text, "production requirements report confirms STAT", errors)
    check("Variable `wght` axis includes 400: yes" in production_requirements_text, "production requirements report confirms wght includes 400", errors)
    check("Variable `fvar` instance names are GF-allowed: yes" in production_requirements_text, "production requirements report confirms GF-allowed fvar names", errors)
    check("Tabular Numbers (`tnum`) feature present in any built font: yes" in production_requirements_text, "production requirements report tracks tnum source-feature readiness", errors)
    check("Default ASCII digits are proportional in every built font: yes" in production_requirements_text, "production requirements report confirms proportional default digits", errors)
    check("`tnum` substitutes all ten ASCII digits in every built font: yes" in production_requirements_text, "production requirements report confirms full tnum coverage", errors)
    check("`tnum` substitutes to equal-width digits in every built font: yes" in production_requirements_text, "production requirements report confirms tabular tnum widths", errors)
    check("Numeric feature requirement ready: yes" in production_requirements_text, "production requirements report confirms numeric feature readiness", errors)
    latin_missing = report_count(missing_text, "Missing codepoints")
    check(
        latin_missing is not None
        and f"GF Latin Core missing codepoints: {latin_missing}" in production_requirements_text,
        "production requirements report tracks Latin Core gap",
        errors,
    )
    check(
        arabic_missing is not None
        and f"GF Arabic Core missing codepoints: {arabic_missing}" in production_requirements_text,
        "production requirements report tracks Arabic Core gap",
        errors,
    )
    check(
        re.search(r"Fontspector googlefonts profile: \d+ FAIL, \d+ WARN, \d+ PASS", production_requirements_text)
        is not None,
        "production requirements report tracks Fontspector summary",
        errors,
    )
    check("Open maintainer decisions: 2" in production_requirements_text, "production requirements report counts open maintainer decisions", errors)
    check("Decided maintainer decisions: 13" in production_requirements_text, "production requirements report counts decided maintainer decisions", errors)
    check("Open decision names: Private-use icon block, Kerning" in production_requirements_text, "production requirements report lists only current open decisions", errors)
    check("Numeric feature status: default ASCII digits are proportional" in production_requirements_text, "production requirements report records numeric work bucket resolved", errors)
    check("numeric feature readiness is no longer a\n  production blocker" in production_requirements_text, "production requirements report does not treat ready numeric feature as blocker", errors)
    check("confirm public URL, source strategy, namecheck" not in production_requirements_text, "production requirements report avoids stale decided-decision blocker wording", errors)
    check("# Numeric Feature Readiness" in numeric_feature_text, "numeric feature report has expected heading", errors)
    check("Default ASCII digits present in every built font: yes" in numeric_feature_text, "numeric feature report confirms default digit coverage", errors)
    check("Default ASCII digits are proportional in every built font: yes" in numeric_feature_text, "numeric feature report confirms proportional defaults", errors)
    check("`tnum` feature present in every built font: yes" in numeric_feature_text, "numeric feature report confirms tnum feature in every font", errors)
    check("`tnum` substitutes all ten ASCII digits in every built font: yes" in numeric_feature_text, "numeric feature report confirms tnum substitution coverage", errors)
    check("`tnum` substitutes to equal-width digits in every built font: yes" in numeric_feature_text, "numeric feature report confirms tabular alternate widths", errors)
    check("Numeric feature requirement ready: yes" in numeric_feature_text, "numeric feature report confirms GF numeric feature readiness", errors)
    check("zero->zero.tf" in numeric_feature_text, "numeric feature report records digit substitutions", errors)
    for reference in [
        "https://googlefonts.github.io/gf-guide/production.html",
        "https://googlefonts.github.io/gf-guide/requirements.html",
        "https://googlefonts.github.io/gf-guide/variable.html",
        "https://googlefonts.github.io/gf-guide/statics.html",
        "https://googlefonts.github.io/gf-guide/build.html",
    ]:
        check(reference in production_requirements_text, f"production requirements report cites {reference}", errors)
    check("# Release Metadata" in release_metadata_text, "release metadata report has expected heading", errors)
    check("Source version: `1.000`" in release_metadata_text, "release metadata report records source version", errors)
    check("Expected built name ID 5 prefix: `Version 1.000`" in release_metadata_text, "release metadata report records built version prefix", errors)
    check("Suggested first-submission tag: `v1.000`" in release_metadata_text, "release metadata report records suggested tag", errors)
    check("Built fonts match source version: yes" in release_metadata_text, "release metadata report confirms built versions match source", errors)
    for font_path in EXPECTED_FONT_OUTPUTS:
        check(font_path in release_metadata_text, f"release metadata report includes {font_path}", errors)
    check("# Release Source Readiness" in release_source_text, "release/source readiness report has expected heading", errors)
    check("Current repo branch: `main`" in release_source_text, "release/source report records current repo branch", errors)
    check("Suggested tag from release metadata: `v1.000`" in release_source_text, "release/source report records suggested tag", errors)
    check("Placeholder upstream URL still present: no" in release_source_text, "release/source report records placeholder upstream URL state", errors)
    check("Downstream `source.files` entries: 4" in release_source_text, "release/source report records source file count", errors)
    check("Ignored/generated `source.files`: 1" in release_source_text, "release/source report records ignored generated source file count", errors)
    check("Local google/fonts fork exists: yes" in release_source_text, "release/source report records local google/fonts fork", errors)
    check("Local google/fonts dirty paths inside `ofl/virtuagrotesk`: 1" in release_source_text, "release/source report records local google/fonts target-package dirtiness", errors)
    check("Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0" in release_source_text, "release/source report records no unrelated google/fonts dirtiness", errors)
    check("Local google/fonts dirty state isolated to `ofl/virtuagrotesk`: yes" in release_source_text, "release/source report records google/fonts dirtiness isolation", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in release_source_text, "release/source report cites GF package guide", errors)
    check("# Release Archive Manifest" in release_archive_text, "release archive manifest has expected heading", errors)
    check("Selected source mode: `latest-release`" in release_archive_text, "release archive manifest records selected source mode", errors)
    check("Archive inputs expected: 4" in release_archive_text, "release archive manifest counts expected source files", errors)
    check("Archive inputs present locally: 4 / 4" in release_archive_text, "release archive manifest confirms local archive inputs", errors)
    check("Unsafe `source.files` paths: 0" in release_archive_text, "release archive manifest confirms source_file paths are safe", errors)
    check("Duplicate `source.files` paths: 0" in release_archive_text, "release archive manifest confirms source_file paths are unique", errors)
    check("Unsafe `dest_file` paths: 0" in release_archive_text, "release archive manifest confirms dest_file paths are safe", errors)
    check("Duplicate `dest_file` paths: 0" in release_archive_text, "release archive manifest confirms dest_file paths are unique", errors)
    check("Variable font newer than source/build inputs:" in release_archive_text, "release archive manifest checks variable font freshness", errors)
    check("SHA-256" in release_archive_text, "release archive manifest records SHA-256 hashes", errors)
    check("Local release archive: `dist/VirtuaGrotesk-1.000.zip`" in release_archive_text, "release archive manifest records local archive path", errors)
    check("Preview release archive URL: `https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip`" in release_archive_text, "release archive manifest records preview archive URL", errors)
    check("Preview release archive URL is GitHub release download `.zip`: yes" in release_archive_text, "release archive manifest records preview archive URL shape", errors)
    check("Preview archive filename matches local archive: yes" in release_archive_text, "release archive manifest checks preview archive filename", errors)
    check("Local release archive contains expected files:" in release_archive_text, "release archive manifest checks local archive entries", errors)
    check("Local release archive has unsafe paths: no" in release_archive_text, "release archive manifest checks archive path safety", errors)
    check("Local release archive hashes match source files:" in release_archive_text, "release archive manifest checks local archive hashes", errors)
    check("Local release archive metadata deterministic:" in release_archive_text, "release archive manifest checks deterministic zip metadata", errors)
    check("Local release archive SHA-256:" in release_archive_text, "release archive manifest records whole archive hash", errors)
    check("make release-archive-build" in release_archive_text, "release archive manifest documents local archive build target", errors)
    check("fonts/variable/VirtuaGrotesk[wght].ttf" in release_archive_text, "release archive manifest tracks served variable font", errors)
    check("documentation/ARTICLE.en_us.html" in release_archive_text, "release archive manifest tracks article HTML", errors)
    check("documentation/readme-specimen.png" in release_archive_text, "release archive manifest tracks article image", errors)
    check("Final GitHub release archive URL recorded: pending" in release_archive_text, "release archive manifest leaves final archive URL pending", errors)
    check("make downstream-metadata-check" in release_archive_text, "release archive manifest includes downstream metadata final gate", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in release_archive_text, "release archive manifest cites GF package guide", errors)
    check("# GitHub Release Draft" in github_release_text, "GitHub release draft report has expected heading", errors)
    check("selected Google Fonts `latest-release` Packager path" in github_release_text, "GitHub release draft records selected source mode", errors)
    check("does\nnot create a tag, push a tag, publish a release, or contact GitHub" in github_release_text, "GitHub release draft is non-mutating", errors)
    check("Upstream URL: `https://github.com/eliheuer/virtua-grotesk`" in github_release_text, "GitHub release draft records upstream URL", errors)
    check("Release tag: `v1.000`" in github_release_text, "GitHub release draft records release tag", errors)
    check("Release title: `Virtua Grotesk 1.000`" in github_release_text, "GitHub release draft records release title", errors)
    check("Local archive: `dist/VirtuaGrotesk-1.000.zip`" in github_release_text, "GitHub release draft records local archive", errors)
    check("Local archive contains expected files: yes" in github_release_text, "GitHub release draft mirrors archive contents check", errors)
    check("Local archive hashes match source files:" in github_release_text, "GitHub release draft mirrors archive hash check", errors)
    check("Local archive metadata deterministic: yes" in github_release_text, "GitHub release draft mirrors deterministic archive metadata check", errors)
    check("Local archive SHA-256:" in github_release_text, "GitHub release draft records whole archive hash", errors)
    check("Release notes file: `documentation/github-release-notes.md`" in github_release_text, "GitHub release draft records release notes file", errors)
    check("Release notes source commit final: no" in github_release_text, "GitHub release draft marks release notes source commit unfinished before final downstream commit", errors)
    check("Downstream preview archive URL: `https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip`" in github_release_text, "GitHub release draft records downstream archive URL", errors)
    check("Downstream preview archive URL contract: GitHub release download `.zip`" in github_release_text, "GitHub release draft records archive URL shape contract", errors)
    check("Downstream preview source commit: `Pending final release/source commit`" in github_release_text, "GitHub release draft keeps pending commit visible", errors)
    check("gh release create v1.000 dist/VirtuaGrotesk-1.000.zip" in github_release_text, "GitHub release draft includes gh release command", errors)
    check("--notes-file documentation/github-release-notes.md" in github_release_text, "GitHub release draft uses generated release notes file", errors)
    check("## Post-Publish Verification" in github_release_text, "GitHub release draft includes post-publish verification section", errors)
    check("gh release view v1.000 --repo eliheuer/virtua-grotesk" in github_release_text, "GitHub release draft includes release view verification command", errors)
    check("gh release download v1.000 --repo eliheuer/virtua-grotesk --pattern VirtuaGrotesk-1.000.zip" in github_release_text, "GitHub release draft includes release asset download verification command", errors)
    check("shasum -a 256 /tmp/virtua-grotesk-release-check/VirtuaGrotesk-1.000.zip" in github_release_text, "GitHub release draft includes downloaded archive hash check", errors)
    check("./venv/bin/python scripts/verify_release_archive.py --archive /tmp/virtua-grotesk-release-check/VirtuaGrotesk-1.000.zip --expected-sha256" in github_release_text, "GitHub release draft verifies downloaded archive with local contract and SHA", errors)
    check("Expected SHA-256:" in github_release_text, "GitHub release draft records expected downloaded archive hash", errors)
    check("The downloaded archive must contain exactly the `source.files` paths" in github_release_text, "GitHub release draft requires downloaded archive contents match source.files", errors)
    check("release notes `Source commit` matches the\nfinal downstream `source.commit`" in github_release_text, "GitHub release draft blocks publishing until release notes and downstream commit match", errors)
    check("path/to/release-notes.md" not in github_release_text, "GitHub release draft has no release-notes placeholder path", errors)
    check("Virtua Grotesk 1.000 release candidate for Google Fonts onboarding." in github_release_notes_text, "GitHub release notes record release purpose", errors)
    check("Google Fonts source mode: latest-release" in github_release_notes_text, "GitHub release notes record source mode", errors)
    check("fonts/variable/VirtuaGrotesk[wght].ttf" in github_release_notes_text, "GitHub release notes list served variable font", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check" in github_release_text, "GitHub release draft includes latest-release metadata check", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in github_release_text, "GitHub release draft includes no-PR latest-release package dry run", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in github_release_text, "GitHub release draft cites GF package guide", errors)
    check("# Packager Source Strategy Matrix" in packager_strategy_text, "Packager source strategy report has expected heading", errors)
    check("Default branch `source.files`" in packager_strategy_text, "Packager source strategy report tracks default branch mode", errors)
    check("Latest release/archive" in packager_strategy_text, "Packager source strategy report tracks latest-release mode", errors)
    check("Build from source" in packager_strategy_text, "Packager source strategy report tracks build-from-source mode", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release" in packager_strategy_text, "Packager source strategy report documents latest-release command", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source" in packager_strategy_text, "Packager source strategy report documents build-from-source command", errors)
    check("Build-from-source inputs present and tracked:" in packager_strategy_text, "Packager source strategy report summarizes build inputs", errors)
    check("Tracked source.files:" in packager_strategy_text, "Packager source strategy report summarizes tracked source.files", errors)
    check("Untracked local source.files:" in packager_strategy_text, "Packager source strategy report summarizes untracked source.files", errors)
    check("Build script uses GF builder config: yes" in packager_strategy_text, "Packager source strategy report checks build script builder config", errors)
    check("Build script runs metadata post-processing: yes" in packager_strategy_text, "Packager source strategy report checks metadata post-processing", errors)
    check("Builder config outputs package fonts directory: yes" in packager_strategy_text, "Packager source strategy report checks builder output directory", errors)
    check("Downstream preview includes `source.config_yaml`: no" in packager_strategy_text, "Packager source strategy report tracks source.config_yaml preview state", errors)
    check("Downstream preview includes release `archive_url`: yes" in packager_strategy_text, "Packager source strategy report tracks archive_url preview state", errors)
    check("Downstream preview `archive_url` is GitHub release download `.zip`: yes" in packager_strategy_text, "Packager source strategy report tracks archive_url shape", errors)
    check("`source.config_yaml` is reproducible-builder-only: no" in packager_strategy_text, "Packager source strategy report validates config_yaml against selected release/archive path", errors)
    check("removed non-buildable or misleading `config_yaml` fields" in packager_strategy_text, "Packager source strategy report records recent google/fonts config_yaml caution", errors)
    check("Local google/fonts fork topology ready: yes" in packager_strategy_text, "Packager source strategy report separates google/fonts fork topology readiness", errors)
    check("Local google/fonts checkout clean: no" in packager_strategy_text, "Packager source strategy report separates dirty downstream checkout state", errors)
    check("Dirty paths outside `ofl/virtuagrotesk`: 0" in packager_strategy_text, "Packager source strategy report confirms only family package dirt is present", errors)
    check("Downstream METADATA.pb starter template present: yes" in packager_strategy_text, "Packager source strategy report tracks downstream starter template state", errors)
    check("fonts/variable/VirtuaGrotesk[wght].ttf" in packager_strategy_text, "Packager source strategy report tracks served variable source file", errors)
    check("Tracked locally" in packager_strategy_text, "Packager source strategy report lists local tracked state for source files", errors)
    check("commit or otherwise expose untracked source files" in packager_strategy_text, "Packager source strategy report records untracked source-file blocker", errors)
    check("Latest release/archive" in packager_strategy_text, "Packager source strategy report records selected release/archive strategy option", errors)
    check("## Selected Latest-Release Action Plan" in packager_strategy_text, "Packager source strategy report includes selected latest-release action plan", errors)
    check("## Per-Strategy Mechanical Checklist" in packager_strategy_text, "Packager source strategy report includes per-strategy mechanical checklist", errors)
    check("### If Default Public-Branch Packaging Is Chosen" in packager_strategy_text, "Packager source strategy report includes default-branch checklist", errors)
    check("Track the current untracked source files:" in packager_strategy_text, "Packager source strategy report lists default-branch files to track", errors)
    check("### If Latest Release Or Archive Packaging Is Chosen" in packager_strategy_text, "Packager source strategy report includes release/archive checklist", errors)
    check("Ensure the release archive contains every mapped source file:" in packager_strategy_text, "Packager source strategy report lists release/archive required files", errors)
    check("Add the final GitHub release download `.zip` `source.archive_url`" in packager_strategy_text, "Packager source strategy report requires release download archive_url in checklist", errors)
    check("### If Build-From-Source Packaging Is Chosen" in packager_strategy_text, "Packager source strategy report includes build-from-source checklist", errors)
    check("Track every currently untracked build input:" in packager_strategy_text, "Packager source strategy report lists build-from-source inputs to track", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run" in packager_strategy_text, "Packager source strategy report includes build-from-source dry-run command in checklist", errors)
    check(
        "Release archive files currently present but untracked: `fonts/variable/VirtuaGrotesk[wght].ttf`" in packager_strategy_text,
        "Packager source strategy report lists untracked release/archive files",
        errors,
    )
    check(
        "Release archive files currently blocked by `.gitignore`: `fonts/variable/VirtuaGrotesk[wght].ttf`" in packager_strategy_text,
        "Packager source strategy report identifies variable TTF gitignore blocker",
        errors,
    )
    check(
        "The maintainer-selected first-submission strategy keeps generated fonts out of the public branch" in packager_strategy_text,
        "Packager source strategy report records selected release/archive strategy",
        errors,
    )
    check("https://googlefonts.github.io/gf-guide/package.html" in packager_strategy_text, "Packager source strategy report cites GF package guide", errors)
    check("# Upstream Structure Readiness" in upstream_structure_text, "upstream structure readiness report has expected heading", errors)
    check("Mandatory upstream paths present: 11 / 11" in upstream_structure_text, "upstream structure report confirms mandatory paths", errors)
    check("Active source inputs present: 4 / 4" in upstream_structure_text, "upstream structure report confirms active source inputs", errors)
    check("Expected generated font outputs present: 5 / 5" in upstream_structure_text, "upstream structure report confirms generated font outputs", errors)
    check("Generated font outputs ignored by git: yes" in upstream_structure_text, "upstream structure report records generated fonts ignored", errors)
    check("Generated source/build outputs ignored by git: yes" in upstream_structure_text, "upstream structure report records generated build outputs ignored", errors)
    check("`sources/config.yaml` uses gftools builder shape: yes" in upstream_structure_text, "upstream structure report checks gftools builder config shape", errors)
    check("build.sh invokes gftools builder: yes" in upstream_structure_text, "upstream structure report checks build.sh builder command", errors)
    check("https://googlefonts.github.io/gf-guide/upstream.html" in upstream_structure_text, "upstream structure report cites GF upstream guide", errors)
    check("https://googlefonts.github.io/gf-guide/build.html" in upstream_structure_text, "upstream structure report cites GF build guide", errors)
    check("https://github.com/googlefonts/googlefonts-project-template" in upstream_structure_text, "upstream structure report cites Google Fonts project template", errors)
    check("# Source UFO Metadata" in source_text, "source metadata report has expected heading", errors)
    check("sources/VirtuaGrotesk-Regular.ufo" in source_text, "source metadata report includes Regular UFO", errors)
    check("sources/VirtuaGrotesk-Bold.ufo" in source_text, "source metadata report includes Bold UFO", errors)
    check("| `sources/VirtuaGrotesk-Regular.ufo` | Virtua Grotesk | Regular | 1.0 |" in source_text, "source metadata report records Regular source identity", errors)
    check("| `sources/VirtuaGrotesk-Bold.ufo` | Virtua Grotesk | Bold | 1.0 |" in source_text, "source metadata report records Bold source identity", errors)
    check("1024/-296/0" in source_text, "source metadata report includes GF vertical metrics", errors)
    check("https://openfontlicense.org" in source_text, "source metadata report includes OFL URL", errors)
    check("OS/2 fsType source" in source_text and "unset" in source_text, "source metadata report records installable embedding source state", errors)
    if VARIABLE_FONT.exists():
        required_arabic_marks = [
            cp
            for cp in glyphsets.unicodes_per_glyphset("GF_Arabic_Core")
            if unicodedata.category(chr(cp)).startswith("M")
            and (0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF)
        ]
        present_arabic_marks = set(required_arabic_marks) & font_codepoints(VARIABLE_FONT)
        missing_arabic_marks = set(required_arabic_marks) - present_arabic_marks
        check(
            f"Required Arabic combining marks in `GF_Arabic_Core`: {len(required_arabic_marks)}" in mark_text,
            "Arabic mark readiness report matches installed glyphsets mark count",
            errors,
        )
        check(
            f"Present in current variable-font cmap: {len(present_arabic_marks)}" in mark_text,
            "Arabic mark readiness report matches current mark coverage",
            errors,
        )
        check(
            f"Missing from current variable-font cmap: {len(missing_arabic_marks)}" in mark_text,
            "Arabic mark readiness report matches current missing mark count",
            errors,
        )
    check("# Master Compatibility Report" in master_text, "master compatibility report has expected heading", errors)
    check("Blocking structure mismatches: 0" in master_text, "master compatibility report has zero blocking mismatches", errors)
    check("Width-only differences:" in master_text, "master compatibility report includes width-only count", errors)
    check("# UFO Editor Readiness" in ufo_editor_text, "UFO editor readiness report has expected heading", errors)
    check("UFO editor handoff ready: yes" in ufo_editor_text, "UFO editor readiness report confirms editor handoff readiness", errors)
    check("UFOs checked: 2" in ufo_editor_text, "UFO editor readiness report checks both active UFOs", errors)
    check("GLIF read errors: 0" in ufo_editor_text, "UFO editor readiness report confirms zero GLIF read errors", errors)
    check("Missing GLIF files: 0" in ufo_editor_text, "UFO editor readiness report confirms zero missing GLIF files", errors)
    check("Duplicate GLIF filenames: 0" in ufo_editor_text, "UFO editor readiness report confirms zero duplicate GLIF filenames", errors)
    check("`sources/VirtuaGrotesk-Regular.ufo` | yes | `public.default` |" in ufo_editor_text, "UFO editor readiness report includes Regular UFO row", errors)
    check("`sources/VirtuaGrotesk-Bold.ufo` | yes | `public.default` |" in ufo_editor_text, "UFO editor readiness report includes Bold UFO row", errors)
    check("make ufo-editor-check" in ufo_editor_text, "UFO editor readiness report documents make target", errors)
    check("make runebender-ufo-check" in ufo_editor_text, "UFO editor readiness report documents Runebender/Norad check", errors)
    check("RUNEBENDER_REPO=/path/to/runebender-xilem" in ufo_editor_text, "UFO editor readiness report documents Runebender repo override", errors)
    check("# Variable Font Metadata" in variable_text, "variable metadata report has expected heading", errors)
    check("Has `fvar`: yes" in variable_text, "variable metadata report confirms fvar", errors)
    check("Has `STAT`: yes" in variable_text, "variable metadata report confirms STAT", errors)
    check("Has `avar`: yes" in variable_text, "variable metadata report records avar status", errors)
    check("| `wght` | Weight | 400 | 400 | 700 | 0 |" in variable_text, "variable metadata report records wght axis bounds", errors)
    check("| SemiBold | `wght=600` |" in variable_text, "variable metadata report records SemiBold instance", errors)
    check("| 3 | Regular | 0 | 400 | 700 | 2 |" in variable_text, "variable metadata report records Regular linked to Bold", errors)
    check("# Google Fonts Axis Registry Audit" in axis_registry_text, "axis registry audit has expected heading", errors)
    check("Registry source: `/Users/eli/GH/forks/fonts/axisregistry/Lib/axisregistry/data/weight.textproto`" in axis_registry_text, "axis registry audit records local google/fonts source", errors)
    check("Registry display name: Weight" in axis_registry_text, "axis registry audit records Weight display name", errors)
    check("Font `wght` bounds/default: 400/400/700" in axis_registry_text, "axis registry audit records font wght bounds", errors)
    check("Family fallback subset: Regular 400, Medium 500, SemiBold 600, Bold 700" in axis_registry_text, "axis registry audit records family fallback subset", errors)
    check("| Font axis name matches registry display name | yes |" in axis_registry_text, "axis registry audit confirms axis display name", errors)
    check("| Font default matches registry default | yes |" in axis_registry_text, "axis registry audit confirms default value", errors)
    check("| Font uses registered fallback names for its range | yes |" in axis_registry_text, "axis registry audit confirms fvar fallback names", errors)
    check("| STAT values use registered fallback names for its range | yes |" in axis_registry_text, "axis registry audit confirms STAT fallback names", errors)
    check("| SemiBold | 600 | yes | SemiBold | SemiBold |" in axis_registry_text, "axis registry audit confirms SemiBold registry spelling", errors)
    check("no new axis registry proposal is needed" in axis_registry_text, "axis registry audit records no custom-axis proposal needed", errors)
    check("# Google Fonts Glyphset Readiness" in glyphset_text, "glyphset readiness report has expected heading", errors)
    check("## Metadata Implications" in glyphset_text, "glyphset readiness report includes metadata implications", errors)
    for glyphset_name in ["GF_Latin_Kernel", "GF_Latin_Core", "GF_Arabic_Core", "GF_Arabic_Plus"]:
        check(f"`{glyphset_name}`" in glyphset_text, f"glyphset readiness report includes {glyphset_name}", errors)
    check("`ar_Arab`, `fa_Arab`, `ur_Arab`" in glyphset_text, "glyphset readiness report includes Arabic Core language codes", errors)
    check("primary_script: \"Arab\"" in glyphset_text, "glyphset readiness report records Arabic primary-script target", errors)
    check("# Private-Use Glyph Scope" in pua_text, "PUA scope report has expected heading", errors)
    check("Variable font PUA codepoints:" in pua_text, "PUA scope report records variable-font count", errors)
    check("PUA scope is a maintainer decision" in pua_text, "PUA scope report records maintainer decision status", errors)
    check("unreachable_glyphs" in pua_text, "PUA scope report tracks unreachable glyph warning impact", errors)
    check("googlefonts/metadata/unreachable_subsetting" in pua_text, "PUA scope report tracks unreachable subsetting warning impact", errors)
    check("## Local Google Fonts PUA Precedent" in pua_text, "PUA scope report includes local Google Fonts precedent sample", errors)
    check("ScheherazadeNew-Regular.ttf" in pua_text and "Kedebideri-Regular.ttf" in pua_text, "PUA scope report includes Arabic-script package precedents", errors)
    check("## PUA Codepoint Inventory" in pua_text, "PUA scope report includes codepoint inventory", errors)
    check("U+E000" in pua_text and "U+F003" in pua_text, "PUA scope report includes current PUA range endpoints", errors)
    check("newGlyph" not in pua_text, "PUA scope report has no placeholder source glyph names", errors)
    for font_path in EXPECTED_FONT_OUTPUTS:
        check(font_path in pua_text, f"PUA scope report includes {font_path}", errors)
    if VARIABLE_FONT.exists():
        font = TTFont(VARIABLE_FONT)
        glyphset_results = glyphsets.get_glyphsets_fulfilled(font)
        pua_codepoints = [
            cp
            for cp in (font.getBestCmap() or {})
            if 0xE000 <= cp <= 0xF8FF
        ]
        font.close()
        check(
            f"Variable font PUA codepoints: {len(pua_codepoints)}" in pua_text,
            "PUA scope report matches current variable-font PUA count",
            errors,
        )
        for glyphset_name in ["GF_Latin_Core", "GF_Arabic_Core"]:
            result = glyphset_results[glyphset_name]
            required_count = len(result["has"]) + len(result["missing"])
            expected = "| `{}` |".format(glyphset_name)
            check(expected in glyphset_text, f"glyphset readiness report has row for {glyphset_name}", errors)
            check(
                f"| {required_count} | {len(result['has'])} | {len(result['missing'])} |" in glyphset_text,
                f"glyphset readiness report matches current counts for {glyphset_name}",
                errors,
            )
    check("Missing codepoints:" in arabic_text, "Arabic Core report includes a missing-codepoint count", errors)
    check("GF Arabic Core required codepoints:" in arabic_text, "Arabic Core report includes required-codepoint count", errors)
    check("## Submission target" in arabic_text, "Arabic Core report documents submission target", errors)
    check("Coverage source: `glyphsets.unicodes_per_glyphset(\"GF_Arabic_Core\")`" in arabic_text, "Arabic Core report documents glyphsets source", errors)
    if VARIABLE_FONT.exists():
        required_arabic = set(glyphsets.unicodes_per_glyphset("GF_Arabic_Core"))
        missing_arabic = required_arabic - font_codepoints(VARIABLE_FONT)
        check(
            report_count(arabic_text, "GF Arabic Core required codepoints") == len(required_arabic),
            "Arabic Core report matches installed glyphsets required count",
            errors,
        )
        check(
            report_count(arabic_text, "Missing codepoints") == len(missing_arabic),
            "Arabic Core report matches current built font missing count",
            errors,
        )
    for heading in [
        "## Arabic letters",
        "## Arabic marks",
        "## Arabic numbers",
        "## Arabic punctuation and symbols",
        "## Shared punctuation and symbols",
    ]:
        check(heading in arabic_text, f"Arabic Core report includes {heading}", errors)
    check("## Reuse Prerequisite Audit" in arabic_source_text, "Arabic source checklist includes reuse prerequisite audit", errors)
    check("Arabic reuse prerequisites checked: 0 codepoints" in arabic_source_text, "Arabic source checklist counts reuse prerequisite codepoints", errors)
    check("Missing reuse prerequisites across masters: 0" in arabic_source_text, "Arabic source checklist verifies reuse prerequisites are present", errors)
    check("Reuse Prerequisite Audit" in arabic_source_text, "Arabic source checklist records dot and skeleton prerequisites", errors)
    check("Missing codepoints:" in missing_text, "Latin Core report includes a missing-codepoint count", errors)
    check("GF Latin Core required codepoints:" in missing_text, "Latin Core report includes required-codepoint count", errors)
    if VARIABLE_FONT.exists():
        required_latin = set(glyphsets.unicodes_per_glyphset("GF_Latin_Core"))
        missing_latin = required_latin - font_codepoints(VARIABLE_FONT)
        check(
            report_count(missing_text, "GF Latin Core required codepoints") == len(required_latin),
            "Latin Core report matches installed glyphsets required count",
            errors,
        )
        check(
            report_count(missing_text, "Missing codepoints") == len(missing_latin),
            "Latin Core report matches current built font missing count",
            errors,
        )
    check("# Fontspector Contour Count Findings" in contour_text, "contour report has expected heading", errors)
    check("Virtua Grotesk Contour Cleanup Proof" in contour_proof_text, "contour cleanup proof has expected heading", errors)
    check("Unique Review Queue" in contour_proof_text, "contour cleanup proof includes unique review queue", errors)
    check("0 unique glyph review items" in contour_proof_text, "contour cleanup proof records current unique review count", errors)
    check("0 all-font rows" in contour_proof_text, "contour cleanup proof records current all-font row count", errors)
    check("Reference:" in contour_proof_text, "contour cleanup proof records reference font path", errors)
    check("# Contour Cleanup Review Queue" in contour_queue_text, "contour cleanup queue has expected heading", errors)
    check("Unique glyph review items: 0" in contour_queue_text, "contour cleanup queue records current unique review count", errors)
    check("All-font finding rows: 0" in contour_queue_text, "contour cleanup queue records current all-font row count", errors)
    check("| Arabic dot-stack helper |" not in contour_queue_text, "contour cleanup queue confirms dot-stack warnings are cleared", errors)
    check("| shared punctuation |" not in contour_queue_text, "contour cleanup queue confirms shared punctuation warnings are cleared", errors)
    check("Recommended action" in contour_queue_text, "contour cleanup queue includes recommended actions", errors)
    check("yes: `uni06540652`" not in contour_queue_text, "contour cleanup queue confirms cleared unencoded mark Rubik reference", errors)
    check("| Glyph | Source glyph | Codepoint | Category | Fonts | Actual | Expected | Reference | Recommended action |" in contour_queue_text, "contour cleanup queue preserves review queue table", errors)
    check("# Contour Cleanup Edit Plan" in contour_edit_plan_text, "contour cleanup edit plan has expected heading", errors)
    check("Unique source glyphs: 0" in contour_edit_plan_text, "contour cleanup edit plan records current source glyph count", errors)
    check("| Order | Priority | Source glyph | Fontspector glyph | Category | Source structure | Compatible | Fonts | Command | Review cue |" in contour_edit_plan_text, "contour cleanup edit plan preserves source edit table", errors)
    check("Source structure uses `c` = source contours" in contour_edit_plan_text, "contour cleanup edit plan explains source structure counts", errors)
    check("# Arabic Cleanup Drawing Briefs" in cleanup_briefs_text, "Arabic cleanup drawing briefs have expected heading", errors)
    check("Briefs: 0" in cleanup_briefs_text, "Arabic cleanup drawing briefs record current brief count", errors)
    check("Do not copy outlines from Rubik" in cleanup_briefs_text, "Arabic cleanup drawing briefs preserve reference-font boundary", errors)
    check("Rubik reference glyph: available as `uni06540652`" not in cleanup_briefs_text, "Arabic cleanup drawing briefs omit cleared Rubik mark reference", errors)
    check("For each brief:" in cleanup_briefs_text, "Arabic cleanup drawing briefs preserve review workflow", errors)
    check("# Contour Cleanup Batches" in contour_batches_text, "contour cleanup batches have expected heading", errors)
    check("Unique review items: 0" in contour_batches_text, "contour cleanup batches record current unique review count", errors)
    check("All-font finding rows: 0" in contour_batches_text, "contour cleanup batches record current all-font row count", errors)
    check("Component-only source forms" in contour_batches_text, "contour cleanup batches include component-only source bucket", errors)
    check("Referenced Arabic marks and ligatures" in contour_batches_text, "contour cleanup batches include referenced Arabic bucket", errors)
    check("Recommended Session Order" in contour_batches_text, "contour cleanup batches preserve session order", errors)
    check("do not copy outlines" in contour_batches_text, "contour cleanup batches preserve reference-font boundary", errors)
    check("After each batch:" in contour_batches_text, "contour cleanup batches preserve regenerate commands", errors)
    check("# Contour Cleanup Decision Log" in contour_decision_text, "contour cleanup decision log has expected heading", errors)
    check("Unique review items: 0" in contour_decision_text, "contour cleanup decision log records current unique review count", errors)
    check("Pending:" in contour_decision_text, "contour cleanup decision log records pending review count", errors)
    check("Status values such as `pending`, `fix-now`, `fixed`, `accepted`, or" in contour_decision_text, "contour cleanup decision log documents status values", errors)
    check("make contour-decision-update" in contour_decision_text, "contour cleanup decision log documents guarded update helper", errors)
    check("| Source glyph | Fontspector glyph | Batch | Category | Command | Status | Decision | Notes | Reviewed |" in contour_decision_text, "contour cleanup decision log preserves decision table", errors)
    check("# Contour Cleanup AI Triage" in contour_ai_triage_text, "contour cleanup AI triage has expected heading", errors)
    check("Triage items: 0" in contour_ai_triage_text, "contour cleanup AI triage records current item count", errors)
    check("| Source glyph | Fontspector glyph | Triage lane | Risk | Batch | Rubik reference | Why this lane | Next review step | Decision command patterns |" in contour_ai_triage_text, "contour cleanup AI triage preserves triage table", errors)
    check("mark-position-review" not in contour_ai_triage_text, "contour cleanup AI triage confirms mark position lane is cleared", errors)
    check("dot-collision-review" not in contour_ai_triage_text, "contour cleanup AI triage confirms dot collision lane is cleared", errors)
    check("fix-now" in contour_ai_triage_text, "contour cleanup AI triage keeps fix-now workflow guidance", errors)
    check("accepted" in contour_ai_triage_text, "contour cleanup AI triage keeps accepted workflow guidance", errors)
    check("# Contour Cleanup Source Edit Runlist" in contour_source_edit_text, "contour cleanup source edit runlist has expected heading", errors)
    check("Fix-now source glyphs: 0" in contour_source_edit_text, "contour cleanup source edit runlist records current fix-now count", errors)
    check("documentation/contour-cleanup-decision-log.md" in contour_source_edit_text, "contour cleanup source edit runlist links decision log", errors)
    check("documentation/contour-cleanup-proof.html" in contour_source_edit_text, "contour cleanup source edit runlist links visual proof", errors)
    check("No `fix-now` contour rows remain." in contour_source_edit_text, "contour cleanup source edit runlist records empty edit state", errors)
    check("Mark fixed command" in contour_source_edit_text, "contour cleanup source edit runlist preserves fixed-command column", errors)
    check("Do not copy outlines from Rubik" in contour_source_edit_text, "contour cleanup source edit runlist preserves reference-font boundary", errors)
    check("# Contour Cleanup First Edit Batch" in contour_first_batch_text, "contour cleanup first edit batch has expected heading", errors)
    check("First-batch fix-now glyphs: 0" in contour_first_batch_text, "contour cleanup first edit batch records current glyph count", errors)
    check("No component-only `fix-now` rows remain." in contour_first_batch_text, "contour cleanup first edit batch records component-only completion", errors)
    check("Component bases" in contour_first_batch_text, "contour cleanup first edit batch lists component bases", errors)
    check("make reports-only" in contour_first_batch_text and "make preflight-only" in contour_first_batch_text, "contour cleanup first edit batch includes regenerate commands", errors)
    contour_queue_sources = {unbacktick(row[1]) for row in markdown_rows(contour_queue_text) if len(row) >= 2}
    contour_decision_rows = markdown_rows(contour_decision_text)
    contour_decision_sources = {unbacktick(row[0]) for row in contour_decision_rows if len(row) >= 9}
    contour_decision_statuses = [row[5] for row in contour_decision_rows if len(row) >= 9]
    contour_decision_summary = {
        "pending": summary_count(contour_decision_text, "Pending") or 0,
        "fix-now": summary_count(contour_decision_text, "Fix-now") or 0,
        "fixed": summary_count(contour_decision_text, "Fixed") or 0,
        "accepted": summary_count(contour_decision_text, "Accepted") or 0,
        "deferred": summary_count(contour_decision_text, "Deferred") or 0,
    }
    allowed_contour_statuses = {"pending", "fix-now", "fixed", "accepted", "deferred"}
    counted_contour_statuses = {
        status: contour_decision_statuses.count(status)
        for status in allowed_contour_statuses
    }
    check(
        contour_decision_sources == contour_queue_sources,
        "contour cleanup decision log source glyphs match current review queue",
        errors,
    )
    check(
        len(contour_decision_rows) == len(contour_queue_sources),
        "contour cleanup decision log has one row per source glyph",
        errors,
    )
    check(
        all(status in allowed_contour_statuses for status in contour_decision_statuses),
        "contour cleanup decision log uses only known statuses",
        errors,
    )
    check(
        contour_decision_summary["pending"] == counted_contour_statuses["pending"],
        "contour cleanup decision log pending summary matches rows",
        errors,
    )
    check(
        contour_decision_summary["fix-now"] == counted_contour_statuses["fix-now"],
        "contour cleanup decision log fix-now summary matches rows",
        errors,
    )
    check(
        contour_decision_summary["fixed"] == counted_contour_statuses["fixed"],
        "contour cleanup decision log fixed summary matches rows",
        errors,
    )
    check(
        contour_decision_summary["accepted"] == counted_contour_statuses["accepted"],
        "contour cleanup decision log accepted summary matches rows",
        errors,
    )
    check(
        contour_decision_summary["deferred"] == counted_contour_statuses["deferred"],
        "contour cleanup decision log deferred summary matches rows",
        errors,
    )
    check("# Glyph Reachability" in reachability_text, "glyph reachability report has expected heading", errors)
    check("Unique unreachable glyphs: 0" in reachability_text, "glyph reachability report records current unique unreachable count", errors)
    check(
        re.search(r"Unique component-reachable glyphs: [1-9]\d*", reachability_text) is not None,
        "glyph reachability report records component-reachable source helpers",
        errors,
    )
    check("Unique Arabic helper/form glyphs: 0" in reachability_text, "glyph reachability report records unique Arabic helper count", errors)
    check("Unique Arabic mark helper glyphs: 0" in reachability_text, "glyph reachability report records unique Arabic mark-helper count", errors)
    check("Unique source cleanup glyphs: 0" in reachability_text, "glyph reachability report records unique source-cleanup count", errors)
    check("## Unique Category Counts" in reachability_text, "glyph reachability report includes unique category counts", errors)
    check("Fontspector warning linkage: `unreachable_glyphs`" in reachability_text, "glyph reachability report links Fontspector unreachable_glyphs warning", errors)
    check("`googlefonts/metadata/unreachable_subsetting`" in reachability_text, "glyph reachability report links unreachable subsetting warning", errors)
    check(
        re.search(r"\| `fonts/variable/VirtuaGrotesk\[wght\]\.ttf` \| \d+ \| \d+ \| 0 \|", reachability_text) is not None,
        "glyph reachability report records variable font counts",
        errors,
    )
    check("## Unique Category Counts" in reachability_text, "glyph reachability report retains category section for future unreachable glyphs", errors)
    check("# Fontspector Warnings" in warning_text, "warning report has expected heading", errors)
    check("## Triage Summary" in warning_text, "warning report includes triage summary", errors)
    check("## Decision-Linked Warnings" in warning_text, "warning report includes decision-linked warning summary", errors)
    check("## Package-Context Warning Floor" in warning_text, "warning report includes package-context warning floor", errors)
    check(
        "Package-context warning floor: 3 WARN" in warning_text,
        "warning report records current package-context warning floor",
        errors,
    )
    check(
        "Honest zero-warning state possible with current scope: no" in warning_text,
        "warning report records honest zero-warning status",
        errors,
    )
    check("## Warning Codes" in warning_text, "warning report includes warning code summary", errors)
    check("## Full Warning Messages" in warning_text, "warning report includes full warning messages", errors)
    for warning_id in [
        "googlefonts/metadata/unreachable_subsetting",
    ]:
        check(warning_id in warning_text, f"warning report tracks decision-linked warning: {warning_id}", errors)
    check(
        "gpos_kerning_info" not in warning_text,
        "warning report no longer tracks resolved gpos_kerning_info warning",
        errors,
    )
    check(
        "mandatory_avar_table" not in warning_text,
        "warning report no longer tracks resolved mandatory_avar_table warning",
        errors,
    )
    check(
        "unreachable_glyphs" not in warning_text,
        "warning report no longer tracks resolved unreachable_glyphs warning",
        errors,
    )
    check("fonts/ttf/VirtuaGrotesk-Regular.ttf" in warning_text, "warning report includes static fonts", errors)
    check("fonts/ttf/VirtuaGrotesk-Regular.ttf" in contour_text, "contour report includes static fonts", errors)
    check("Warnings:" in warning_text, "warning report includes all-font warning count", errors)
    check("# Fontspector Metadata Warning Probe" in metadata_warning_probe_text, "metadata warning probe has expected heading", errors)
    check("## Subset Variant Probe" in metadata_warning_probe_text, "metadata warning probe includes subset variants", errors)
    check("| menu + latin only | 2 |" in metadata_warning_probe_text, "metadata warning probe records lower-count subset trap", errors)
    check("drops intended Arabic serving subset" in metadata_warning_probe_text, "metadata warning probe flags dropped Arabic serving scope", errors)
    check("# Fontspector Zero-Warning Worklist" in zero_warning_text, "zero-warning worklist has expected heading", errors)
    check("## Subset Threshold Math" in zero_warning_text, "zero-warning worklist includes subset threshold math", errors)
    check("| `arabic` | 50% | 1432 | 123 | 717 | 8.59% | 594 | no |" in zero_warning_text, "zero-warning worklist records current Arabic subset threshold gap", errors)
    check(
        re.search(r"\| `latin-ext` \| 20% \| 1144 \| \d+ \| 229 \| [^|]+ \| \d+ \| no \|", zero_warning_text) is not None,
        "zero-warning worklist records current latin-ext subset threshold gap",
        errors,
    )
    check(
        "U+0237, U+200F, U+20B9, and U+25CC reachability" in zero_warning_text
        and "does not create replacement warnings" in zero_warning_text
        and "deleting or broad-rescuing them is worse" in zero_warning_text,
        "zero-warning worklist warns against stripping reachability codepoints",
        errors,
    )
    check("FontSpector report" in full_report_text, "full Fontspector report has expected heading", errors)
    check(
        "Summary" in full_report_text
        and "| 10 | 38 | 529 | 302 |" in full_report_text
        and "FAIL" not in full_report_text,
        "full Fontspector report records current zero-FAIL summary",
        errors,
    )
    fontspector_version_output = command_stdout(["fontspector", "--version"])
    fontspector_version = fontspector_version_output.splitlines()[0].split()[1] if fontspector_version_output else ""
    check(
        bool(fontspector_version) and f"fontspector version: {fontspector_version}" in full_report_text,
        "full Fontspector report matches installed Fontspector version",
        errors,
    )


def metadata_review_errors(errors: list[str]) -> None:
    text = (ROOT / "documentation/google-fonts-metadata-review.md").read_text()
    downstream_preview_text = (ROOT / "documentation/google-fonts-downstream-package-preview.md").read_text()
    downstream_metadata_text = (ROOT / "documentation/downstream-metadata-readiness.md").read_text()
    prepare_downstream_metadata_text = (ROOT / "scripts/prepare_downstream_metadata.py").read_text()
    metadata_apply_blockers = downstream_metadata_apply_blockers()
    vendor_id_text = (ROOT / "documentation/vendor-id-readiness.md").read_text()
    family_name_text = (ROOT / "documentation/family-name-readiness.md").read_text()
    authorship_disclosure_text = (ROOT / "documentation/authorship-disclosure-readiness.md").read_text()
    pr_identity_text = (ROOT / "documentation/pr-identity-readiness.md").read_text()
    designer_profile_text = (ROOT / "documentation/designer-profile-readiness.md").read_text()
    designer_profile_package_text = (ROOT / "documentation/designer-profile-package-draft.md").read_text()
    avar_text = (ROOT / "documentation/avar-readiness.md").read_text()
    language_metadata_text = (ROOT / "documentation/google-fonts-language-metadata.md").read_text()
    check("name: \"Virtua Grotesk\"" in text, "metadata review includes family name", errors)
    check("filename: \"VirtuaGrotesk[wght].ttf\"" in text, "metadata review includes variable filename", errors)
    check("filename: \"VirtuaGrotesk-SemiBold.ttf\"" in text, "metadata review includes SemiBold static filename", errors)
    check("axes {" in text and "tag: \"wght\"" in text, "metadata review includes wght axis", errors)
    check("min_value: 400.0" in text and "max_value: 700.0" in text, "metadata review includes wght axis bounds", errors)
    check("default location is reviewed from the built font's `fvar`" in text, "metadata review records fvar default-source convention", errors)
    check("documentation/google-fonts-axis-registry-audit.md" in text, "metadata review points to axis registry audit", errors)
    check("Google Fonts axis registry display name" in text, "metadata review records axis-registry naming review", errors)
    check("# Vendor ID Readiness" in vendor_id_text, "vendor ID report has expected heading", errors)
    check("Source UFO vendor IDs: `FTGD`" in vendor_id_text, "vendor ID report records confirmed source value", errors)
    check("Generated font vendor IDs: `FTGD`" in vendor_id_text, "vendor ID report records generated FTGD value", errors)
    check("Source UFO vendor IDs internally consistent: yes" in vendor_id_text, "vendor ID report checks source consistency", errors)
    check("Generated font vendor IDs internally consistent: yes" in vendor_id_text, "vendor ID report checks generated-font consistency", errors)
    check("Source and generated vendor states aligned: yes" in vendor_id_text, "vendor ID report checks source/generated alignment", errors)
    check("Fontspector `googlefonts/vendor_id` warnings: 0" in vendor_id_text, "vendor ID report records current Fontspector warning count", errors)
    check("Decision log status: decided" in vendor_id_text, "vendor ID report records decision-log status", errors)
    check("Vendor ID decision unresolved: no" in vendor_id_text, "vendor ID report records resolved decision", errors)
    check("Vendor ID apply helper present: yes" in vendor_id_text, "vendor ID report records apply helper presence", errors)
    check(
        "Vendor ID apply helper validates four-character non-NONE IDs: yes" in vendor_id_text,
        "vendor ID report records apply helper validation behavior",
        errors,
    )
    check(
        "Vendor ID apply helper dry-runs by default: yes" in vendor_id_text,
        "vendor ID report records apply helper dry-run behavior",
        errors,
    )
    check("Microsoft registered vendor entry confirmed: yes" in vendor_id_text, "vendor ID report records Microsoft registration confirmation", errors)
    check("Confirmed vendor ID owner: `FTGD` = Font Garden" in vendor_id_text, "vendor ID report records confirmed owner", errors)
    check("Registered vendor list verification date: 2026-05-24" in vendor_id_text, "vendor ID report records verification date", errors)
    check("confirmed registered: Font Garden" in vendor_id_text, "vendor ID report marks generated fonts as confirmed registered", errors)
    check("sources/VirtuaGrotesk-Regular.ufo" in vendor_id_text, "vendor ID report includes Regular UFO", errors)
    check("fonts/variable/VirtuaGrotesk[wght].ttf" in vendor_id_text, "vendor ID report includes variable font", errors)
    check("https://learn.microsoft.com/en-us/typography/vendors/" in vendor_id_text, "vendor ID report cites current Microsoft vendor list", errors)
    vendor_helper_text = (ROOT / "scripts/apply_vendor_id.py").read_text()
    check(
        "valid_vendor_id" in vendor_helper_text and "must not be NONE" in vendor_helper_text,
        "vendor ID helper rejects invalid IDs and NONE",
        errors,
    )
    vendor_report_helper_text = (ROOT / "scripts/report_vendor_id_readiness.py").read_text()
    check(
        r"[A-Za-z0-9 ]{4}" in vendor_report_helper_text,
        "vendor ID report uses helper-aligned alphanumeric/space validation",
        errors,
    )
    check(
        "--apply" in vendor_helper_text and "Dry run only" in vendor_helper_text,
        "vendor ID helper keeps writes behind apply flag",
        errors,
    )
    check(
        "openTypeOS2VendorID" in vendor_helper_text
        and "sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist" in vendor_helper_text,
        "vendor ID helper writes active source UFO fontinfo.plist files",
        errors,
    )
    check("documentation/vendor-id-readiness.md" in text, "metadata review points to vendor ID report", errors)
    check("# Family Name Readiness" in family_name_text, "family-name readiness report has expected heading", errors)
    check("Family names from built fonts: `Virtua Grotesk`" in family_name_text, "family-name report records built family name", errors)
    check("Family names are ASCII letters/digits/spaces only: yes" in family_name_text, "family-name report records ASCII-safe family name", errors)
    check("OFL Reserved Font Name status: none declared after copyright line" in family_name_text, "family-name report records no RFN declaration", errors)
    check("Namecheck confirmation: confirmed by maintainer at `namecheck.fontdata.com`" in family_name_text, "family-name report tracks confirmed namecheck", errors)
    check("Decision log status: decided" in family_name_text, "family-name report records decision-log status", errors)
    check("## Add Font Name Requirements" in family_name_text, "family-name report includes Add Font name requirement matrix", errors)
    check("Unique according to `namecheck.fontdata.com`" in family_name_text, "family-name report tracks Add Font namecheck requirement", errors)
    check("App-menu family name candidate appears in built names: yes" in family_name_text, "family-name report confirms app-menu candidate appears in built names", errors)
    check("Google CLA status: confirmed by maintainer for the copyright holder" in family_name_text, "family-name report tracks confirmed CLA status", errors)
    check("Built family names include copyright-author full name: no" in family_name_text, "family-name report checks author-name app-menu constraint", errors)
    check("`VirtuaGrotesk-SemiBold`" in family_name_text, "family-name report includes SemiBold PostScript name", errors)
    check("https://googlefonts.github.io/gf-guide/onboarding.html" in family_name_text, "family-name report cites GF onboarding guide", errors)
    check("# Authorship And AI Disclosure Readiness" in authorship_disclosure_text, "authorship and AI disclosure report has expected heading", errors)
    check("AUTHORS.txt entries: `Eli Heuer`" in authorship_disclosure_text, "authorship report reads AUTHORS.txt", errors)
    check("CONTRIBUTORS.txt entries: `Eli Heuer`" in authorship_disclosure_text, "authorship report reads CONTRIBUTORS.txt", errors)
    check("AUTHORS.txt contact-formatted entries: 0 / 1" in authorship_disclosure_text, "authorship report tracks AUTHORS.txt contact-line format", errors)
    check("CONTRIBUTORS.txt contact-formatted entries: 0 / 1" in authorship_disclosure_text, "authorship report tracks CONTRIBUTORS.txt contact-line format", errors)
    check("Contact-formatted credit lines absent by current decision: yes" in authorship_disclosure_text, "authorship report records current contact-line state", errors)
    check("Email/contact line change required now: no" in authorship_disclosure_text, "authorship report records decided contact-line default", errors)
    check(
        "OFL copyright line: `Copyright 2025 The Virtua Grotesk Project Authors" in authorship_disclosure_text,
        "authorship report reads OFL copyright line",
        errors,
    )
    check("Combined Add Font checkbox present: yes" in authorship_disclosure_text, "authorship report records combined Add Font checkbox", errors)
    check("AI-use disclosure recorded: yes" in authorship_disclosure_text, "authorship report records approved AI-use disclosure", errors)
    check("Approved authorship/AI statement recorded: yes" in authorship_disclosure_text, "authorship report records approved combined statement", errors)
    check("## Approved Add Font Statement" in authorship_disclosure_text, "authorship report includes approved Add Font statement", errors)
    check("Eli Heuer is the sole copyright author/controller" in authorship_disclosure_text, "authorship report includes sole-author approved wording", errors)
    check("AI tools were used for engineering, proofing, onboarding" in authorship_disclosure_text, "authorship report includes AI-use approved wording", errors)
    check("## Maintainer Input Checklist" in authorship_disclosure_text, "authorship report includes maintainer input checklist", errors)
    check("Copyright-author authority" in authorship_disclosure_text, "authorship checklist tracks copyright-author authority", errors)
    check("AI-use disclosure | Recorded" in authorship_disclosure_text, "authorship checklist tracks recorded AI-use disclosure", errors)
    check(
        "Email/contact-formatted credit lines" in authorship_disclosure_text,
        "authorship checklist tracks email/contact-formatted credit lines",
        errors,
    )
    check(
        "`Name or Organization <email address>` for authors" in authorship_disclosure_text
        and "`Name <email address>` for contributors" in authorship_disclosure_text,
        "authorship report documents official author/contributor email templates",
        errors,
    )
    check("OFL copyright holder" in authorship_disclosure_text, "authorship checklist tracks OFL copyright holder", errors)
    check("Add Font checkbox wording" in authorship_disclosure_text, "authorship checklist tracks Add Font checkbox wording", errors)
    check("Decision-safe default: keep `AUTHORS.txt`, `CONTRIBUTORS.txt`, and" in authorship_disclosure_text, "authorship report keeps legal files unchanged under approved decision", errors)
    check("no email/contact line change is required now" in authorship_disclosure_text, "authorship report treats email/contact lines as not required now", errors)
    check("Decision status: decided" in authorship_disclosure_text, "authorship report records decided decision", errors)
    check("https://googlefonts.github.io/gf-guide/onboarding.html" in authorship_disclosure_text, "authorship report cites GF onboarding guide", errors)
    check("https://googlefonts.github.io/gf-guide/upstream.html" in authorship_disclosure_text, "authorship report cites GF upstream guide for contact files", errors)
    check("# PR Identity Readiness" in pr_identity_text, "PR identity readiness report has expected heading", errors)
    check("Expected CLA/author name: `Eli Heuer`" in pr_identity_text, "PR identity report records expected CLA/author name", errors)
    check("Source repo git identity complete:" in pr_identity_text, "PR identity report records source repo git identity completeness", errors)
    check("Source repo git user.name matches expected CLA/author name:" in pr_identity_text, "PR identity report checks source repo git name against CLA/author name", errors)
    check("google/fonts fork git checkout present:" in pr_identity_text, "PR identity report records google/fonts fork checkout presence", errors)
    check("google/fonts fork git identity complete:" in pr_identity_text, "PR identity report records google/fonts fork git identity completeness", errors)
    check("google/fonts fork git user.name matches expected CLA/author name:" in pr_identity_text, "PR identity report checks google/fonts fork git name against CLA/author name", errors)
    check("## Git Identity Evidence" in pr_identity_text, "PR identity report includes per-repo git identity evidence", errors)
    check("/Users/eli/GH/forks/fonts" in pr_identity_text, "PR identity report points at local google/fonts fork", errors)
    check("Final downstream commit identity ready:" in pr_identity_text, "PR identity report checks final downstream commit identity readiness", errors)
    check("git user.email: `" in pr_identity_text, "PR identity report records redacted git email", errors)
    check(
        re.search(r"GitHub CLI auth status: `[^`]+`", pr_identity_text) is not None,
        "PR identity report records current GitHub CLI auth state",
        errors,
    )
    check(
        re.search(r"GitHub API credentials ready: (yes|no)", pr_identity_text) is not None,
        "PR identity report records GitHub API credential readiness",
        errors,
    )
    check(
        re.search(r"GitHub API credential source: `[^`]+`", pr_identity_text) is not None,
        "PR identity report records GitHub API credential source",
        errors,
    )
    check("Google CLA status: confirmed by maintainer for the copyright holder" in pr_identity_text, "PR identity report records confirmed CLA status", errors)
    check("`gh auth status` exit code:" in pr_identity_text, "PR identity report records gh auth command evidence", errors)
    check("Credential detail:" in pr_identity_text, "PR identity report records credential detail", errors)
    check("short-lived `GH_TOKEN`" in pr_identity_text, "PR identity report documents GH_TOKEN option", errors)
    check("## Local Auth Commands" in pr_identity_text, "PR identity report includes local auth command section", errors)
    check("gh auth status -h github.com" in pr_identity_text, "PR identity report documents GitHub auth status command", errors)
    check("GH_TOKEN=<token> make github-auth-check" in pr_identity_text, "PR identity report documents one-command GH_TOKEN check", errors)
    check("https://googlefonts.github.io/gf-guide/making-pr.html" in pr_identity_text, "PR identity report cites GF PR guide", errors)
    downstream_pr_text = (ROOT / "documentation/downstream-pr-readiness.md").read_text()
    check("# Downstream PR Readiness" in downstream_pr_text, "downstream PR readiness report has expected heading", errors)
    check("Google Fonts issue pending: yes" in downstream_pr_text, "downstream PR report records issue-first blocker", errors)
    check("Expected downstream family path: `ofl/virtuagrotesk`" in downstream_pr_text, "downstream PR report records family path", errors)
    check("Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`" in downstream_pr_text, "downstream PR report records expected Packager branch", errors)
    check("PR title: `Virtua Grotesk : 1.000 added`" in downstream_pr_text, "downstream PR report records expected PR title", errors)
    check("PR body provenance line: `Taken from the upstream repo <repo-url> at commit <commit-url>.`" in downstream_pr_text, "downstream PR report records expected PR body provenance line", errors)
    check("Downstream metadata preview ready to apply: no" in downstream_pr_text, "downstream PR report records downstream metadata apply readiness", errors)
    check(metadata_apply_blockers is not None, "downstream metadata diff records prepare-helper blocker count", errors)
    check(
        metadata_apply_blockers is not None
        and f"Downstream metadata apply blockers: {metadata_apply_blockers}" in downstream_pr_text,
        "downstream PR report matches downstream metadata apply blocker count",
        errors,
    )
    check("Source repo git name matches CLA/author name:" in downstream_pr_text, "downstream PR report mirrors source git name match state", errors)
    check("google/fonts fork git name matches CLA/author name:" in downstream_pr_text, "downstream PR report mirrors google/fonts git name match state", errors)
    check("Final downstream commit identity ready:" in downstream_pr_text, "downstream PR report mirrors final commit identity readiness", errors)
    check("google/fonts tracking branch: `origin/main`" in downstream_pr_text, "downstream PR report records google/fonts tracking branch", errors)
    check("google/fonts main vs origin/main: 0 ahead, 0 behind" in downstream_pr_text, "downstream PR report records origin/main alignment", errors)
    check("google/fonts main vs upstream/main: 0 ahead, 0 behind" in downstream_pr_text, "downstream PR report records upstream/main alignment", errors)
    check("google/fonts fork base ready for downstream branch: yes" in downstream_pr_text, "downstream PR report records fork base readiness", errors)
    check("make downstream-metadata-check" in downstream_pr_text and "Ready to apply: yes" in downstream_pr_text, "downstream PR report gates metadata apply on dry-run readiness", errors)
    check("Dirty google/fonts paths outside family dir: 0" in downstream_pr_text, "downstream PR report confirms no dirty paths outside family directory", errors)
    check("Current downstream family file count: 1" in downstream_pr_text, "downstream PR report records current expanded family file count", errors)
    check("Current downstream family files starter-only: yes" in downstream_pr_text, "downstream PR report identifies current starter-only downstream family dir", errors)
    check("Current files inside downstream family dir:" in downstream_pr_text, "downstream PR report expands current family directory contents", errors)
    check("`ofl/virtuagrotesk/METADATA.pb`" in downstream_pr_text, "downstream PR report lists current downstream METADATA.pb file", errors)
    check("Public upstream URL still pending in issue draft: no" in downstream_pr_text, "downstream PR report records applied public upstream URL", errors)
    check("Handoff includes exact downstream PR title: yes" in downstream_pr_text, "downstream PR report checks handoff PR title", errors)
    check("Handoff includes exact PR provenance body line: yes" in downstream_pr_text, "downstream PR report checks handoff PR body", errors)
    check("Handoff records one-family-directory rule: yes" in downstream_pr_text, "downstream PR report checks one-directory PR rule", errors)
    check("Handoff records fork comparison path: yes" in downstream_pr_text, "downstream PR report checks fork comparison path", errors)
    check("## Safe Local Sequence" in downstream_pr_text, "downstream PR report includes safe local sequence", errors)
    check("gh auth status -h github.com" in downstream_pr_text, "downstream PR report documents GitHub auth status command", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk" in downstream_pr_text, "downstream PR report documents scoped google/fonts status command", errors)
    check("Only after reviewing the no-PR package" in downstream_pr_text, "downstream PR report gates Packager PR mode on no-PR review", errors)
    check("https://googlefonts.github.io/gf-guide/making-pr.html" in downstream_pr_text, "downstream PR report cites GF PR guide", errors)
    check("# avar Readiness" in avar_text, "avar readiness report has expected heading", errors)
    check("Axis: `wght` 400-700, default 400" in avar_text, "avar readiness report records wght axis bounds", errors)
    check("Has `avar`: yes" in avar_text, "avar readiness report records current avar presence", errors)
    check("Fontspector `mandatory_avar_table` warnings: 0" in avar_text, "avar readiness report records current Fontspector warning count", errors)
    check("Current decision: decided" in avar_text, "avar readiness report records decided linear-axis decision", errors)
    for instance_row in [
        "| Regular | 400 | 0.0000 |",
        "| Medium | 500 | 0.3333 |",
        "| SemiBold | 600 | 0.6667 |",
        "| Bold | 700 | 1.0000 |",
    ]:
        check(instance_row in avar_text, f"avar readiness report includes mapping row: {instance_row}", errors)
    check("https://googlefonts.github.io/gf-guide/variable.html" in avar_text, "avar readiness report cites GF variable font guide", errors)
    check("documentation/avar-readiness.md" in text, "metadata review points to avar readiness report", errors)
    check("subsets: \"menu\"" in text, "metadata review includes mandatory menu subset", errors)
    check("subsets: \"arabic\"" in text, "metadata review includes Arabic subset", errors)
    check("primary_script: \"Arab\"" in text, "metadata review includes Arabic primary script", errors)
    check("source {" in text and "repository_url" in text, "metadata review includes downstream source block review", errors)
    check("archive_url: \"https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip\"" in text, "metadata review includes selected release archive URL", errors)
    check("branch: \"main\"" in text, "metadata review records current release/archive branch", errors)
    check("Omit `source.config_yaml` for this selected release/archive path" in text, "metadata review documents config_yaml omission for release/archive path", errors)
    check("config_yaml: \"sources/config.yaml\"" not in text, "metadata review does not show config_yaml in selected release/archive source block", errors)
    check("article/ARTICLE.en_us.html" in text, "metadata review tracks Article package option", errors)
    check("source_file: \"documentation/ARTICLE.en_us.html\"" in text, "metadata review source block maps Article HTML", errors)
    check("dest_file: \"article/ARTICLE.en_us.html\"" in text, "metadata review source block maps Article destination", errors)
    check("source_file: \"documentation/readme-specimen.png\"" in text, "metadata review source block maps Article image", errors)
    check("dest_file: \"article/readme-specimen.png\"" in text, "metadata review source block maps Article image destination", errors)
    check("category: \"SANS_SERIF\"" in text, "metadata review includes SANS_SERIF category", errors)
    check("stroke: \"SANS_SERIF\"" in text, "metadata review includes SANS_SERIF stroke", errors)
    check('date_added: "Pending final Google Fonts date_added"' in text, "metadata review keeps date_added pending until final package date", errors)
    check("Replace the pending `date_added` placeholder" in text, "metadata review documents final date_added replacement", errors)
    check("Do not add a `tags` field to `METADATA.pb`" in text, "metadata review treats tags as PR review metadata", errors)
    check("Do not add custom `sample_text`" in text, "metadata review treats sample_text as an explicit override decision", errors)
    check("Google Fonts' language textprotos" in text, "metadata review relies on Google Fonts textprotos by default", errors)
    check("documentation/pua-scope.md" in text, "metadata review points to PUA scope report", errors)
    check("ofl/virtuagrotesk" in downstream_preview_text, "downstream package preview includes expected family path", errors)
    check("Current dry-run status, 2026-05-24" in downstream_preview_text, "downstream package preview has current dry-run status date", errors)
    check("VirtuaGrotesk[wght].ttf" in downstream_preview_text, "downstream package preview includes variable font", errors)
    check("chosen source strategy" in downstream_preview_text, "downstream package preview tracks source strategy decision", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release" in downstream_preview_text, "downstream package preview tracks selected latest-release source mode", errors)
    check("min_value: 400.0" in downstream_preview_text and "max_value: 700.0" in downstream_preview_text, "downstream package preview includes wght axis bounds", errors)
    check("default `wght=400` is reviewed in `fvar`" in downstream_preview_text, "downstream package preview records fvar default-source convention", errors)
    check("article/readme-specimen.png" in downstream_preview_text, "downstream package preview includes Article image asset", errors)
    check("source_file: \"documentation/ARTICLE.en_us.html\"" in downstream_preview_text, "downstream package preview source block maps Article HTML", errors)
    check("source_file: \"documentation/readme-specimen.png\"" in downstream_preview_text, "downstream package preview source block maps Article image", errors)
    check("documentation/package-source-files-audit.md" in downstream_preview_text, "downstream package preview points to package source-file audit", errors)
    check("`archive_url`" in downstream_preview_text and "latest-release" in downstream_preview_text, "downstream package preview documents latest-release archive_url requirement", errors)
    check("documentation/downstream-metadata-readiness.md" in text, "metadata review points to downstream metadata readiness report", errors)
    check("# Downstream Metadata Readiness" in downstream_metadata_text, "downstream metadata readiness report has expected heading", errors)
    check("Top-level family name present: yes" in downstream_metadata_text, "downstream metadata report records top-level family name", errors)
    check("`date_added` final date present: no" in downstream_metadata_text, "downstream metadata report blocks pending date_added", errors)
    check(
        "`date_added` current value: `Pending final Google Fonts date_added`" in downstream_metadata_text,
        "downstream metadata report records pending date_added value",
        errors,
    )
    check("Variable filename/name fields match built font: yes" in downstream_metadata_text, "downstream metadata report matches variable name fields", errors)
    check("Weight axis min/max match built `fvar`: yes" in downstream_metadata_text, "downstream metadata report matches built axis bounds", errors)
    check("Variable font only in preview: yes" in downstream_metadata_text, "downstream metadata report records variable-only preview", errors)
    check("Expected subsets present and sorted: yes" in downstream_metadata_text, "downstream metadata report records expected subsets", errors)
    check("`primary_script: \"Arab\"` present: yes" in downstream_metadata_text, "downstream metadata report records Arabic primary script", errors)
    check("Non-Noto `languages` entries absent: yes" in downstream_metadata_text, "downstream metadata report records languages omission", errors)
    check("Custom `sample_text` absent: yes" in downstream_metadata_text, "downstream metadata report records sample_text omission", errors)
    check("`tags` field absent from METADATA preview: yes" in downstream_metadata_text, "downstream metadata report records tags omission", errors)
    check("Unneeded optional display/classification fields absent: yes" in downstream_metadata_text, "downstream metadata report records optional display/classification omission", errors)
    check(
        "Apply helper blocks unapproved optional metadata fields: yes" in downstream_metadata_text,
        "downstream metadata report confirms apply helper blocks review-gated optional fields",
        errors,
    )
    check(
        "PROHIBITED_OPTIONAL_FIELDS" in prepare_downstream_metadata_text
        and "optional metadata field requires explicit Google Fonts review before apply" in prepare_downstream_metadata_text,
        "downstream metadata apply helper blocks unapproved optional metadata fields",
        errors,
    )
    check("Expected `source.files` present: yes" in downstream_metadata_text, "downstream metadata report records source file mapping", errors)
    check("Expected `source.files` destination mappings present: yes" in downstream_metadata_text, "downstream metadata report records source destination mappings", errors)
    for source, dest in [
        ("OFL.txt", "OFL.txt"),
        ("fonts/variable/VirtuaGrotesk[wght].ttf", "VirtuaGrotesk[wght].ttf"),
        ("documentation/ARTICLE.en_us.html", "article/ARTICLE.en_us.html"),
        ("documentation/readme-specimen.png", "article/readme-specimen.png"),
    ]:
        check(
            f"| `{source}` | `{dest}` | yes | yes |" in downstream_metadata_text,
            f"downstream metadata report records source destination mapping: {source}",
            errors,
        )
    check("Source block has repository, commit, archive_url, and branch fields: yes" in downstream_metadata_text, "downstream metadata report records source block shape", errors)
    check("`source.archive_url` present: yes" in downstream_metadata_text, "downstream metadata report records archive_url presence", errors)
    check("`source.archive_url` required for latest-release mode: yes" in downstream_metadata_text, "downstream metadata report records latest-release archive_url requirement", errors)
    check("`source.archive_url` is GitHub release download `.zip`: yes" in downstream_metadata_text, "downstream metadata report records latest-release archive_url shape", errors)
    check("`source.archive_url` satisfies latest-release mode: yes" in downstream_metadata_text, "downstream metadata report records latest-release archive_url readiness", errors)
    check("`source.config_yaml` present: no" in downstream_metadata_text, "downstream metadata report records config_yaml absence", errors)
    check("`source.config_yaml` needs source-strategy review: no" in downstream_metadata_text, "downstream metadata report records config_yaml source-strategy review state", errors)
    check("## Source Mode Compatibility" in downstream_metadata_text, "downstream metadata report includes source mode compatibility table", errors)
    check("selected and previewed" in downstream_metadata_text, "downstream metadata report marks latest-release archive_url previewed", errors)
    check("| Build from source | keep `config_yaml: \"sources/config.yaml\"` | not selected |" in downstream_metadata_text, "downstream metadata report marks build-from-source not selected", errors)
    check("## Date Added Policy" in downstream_metadata_text, "downstream metadata report documents date_added policy", errors)
    check(
        "Packager automatically" in downstream_metadata_text and "Do not guess" in downstream_metadata_text,
        "downstream metadata report records Packager/date_added policy",
        errors,
    )
    check("## Pending Field Decision Map" in downstream_metadata_text, "downstream metadata report maps pending fields to decisions", errors)
    for field in [
        "`designer`",
        "`copyright`",
        "`date_added`",
        "`source.repository_url`",
        "`source.commit`",
        "`source.branch`",
        "`source.config_yaml`",
        "`source.archive_url`",
    ]:
        check(field in downstream_metadata_text, f"downstream metadata pending-field map covers {field}", errors)
    check(
        "Do not apply the downstream metadata preview to the local `google/fonts`" in downstream_metadata_text,
        "downstream metadata report blocks apply until pending fields are final",
        errors,
    )
    check("Static style-name review uses GF `SemiBold` spelling: yes" in downstream_metadata_text, "downstream metadata report records SemiBold style-name review", errors)
    check("Pending or placeholder metadata lines: 2" in downstream_metadata_text, "downstream metadata report counts pending placeholder lines", errors)
    check(
        "Rerun `make preflight` after metadata-preview or build changes" in downstream_metadata_text,
        "downstream metadata readiness report uses synchronized preflight after changes",
        errors,
    )
    check("https://googlefonts.github.io/gf-guide/metadata.html" in downstream_metadata_text, "downstream metadata report cites GF metadata guide", errors)
    check("primary_script: \"Arab\"" in downstream_preview_text, "downstream package preview includes Arabic primary script", errors)
    check("stroke: \"SANS_SERIF\"" in downstream_preview_text, "downstream package preview includes SANS_SERIF stroke", errors)
    check("Do not add a `tags` field" in downstream_preview_text, "downstream package preview treats tags as PR review metadata", errors)
    check("Do not add custom `sample_text`" in downstream_preview_text, "downstream package preview treats sample_text as an explicit override decision", errors)
    check("source.config_yaml" in downstream_preview_text and "release/archive" in downstream_preview_text, "downstream package preview documents config_yaml omission for release/archive", errors)
    check("source.archive_url" in downstream_preview_text and "VirtuaGrotesk-1.000.zip" in downstream_preview_text, "downstream package preview includes release archive_url", errors)
    check("non-buildable or misleading configs" in downstream_preview_text, "downstream package preview records recent google/fonts config_yaml caution", errors)
    check("Pending final release/source commit" in downstream_preview_text, "downstream package preview keeps final commit as open item", errors)
    check(
        "upstream_info.md" in downstream_preview_text and "optional" in downstream_preview_text,
        "downstream package preview tracks optional upstream_info provenance",
        errors,
    )
    check(
        "upstream.yaml" in downstream_preview_text and "Packager uses" in downstream_preview_text,
        "downstream package preview tracks generated upstream.yaml review",
        errors,
    )
    check("# Designer Profile Readiness" in designer_profile_text, "designer profile report has expected heading", errors)
    check("AUTHORS.txt: `Eli Heuer`" in designer_profile_text, "designer profile report reads AUTHORS.txt", errors)
    check("AUTHORS catalog-credit candidates: 1" in designer_profile_text, "designer profile report counts AUTHORS catalog-credit candidates", errors)
    check("Contributor-only candidates: 0" in designer_profile_text, "designer profile report counts contributor-only candidates", errors)
    check("Candidate profiles missing: 1" in designer_profile_text, "designer profile report counts missing candidate profiles", errors)
    check("Final metadata designer strings present: yes" in designer_profile_text, "designer profile report records final metadata designer string", errors)
    check(
        "Final comma-separated designer entities present: yes" in designer_profile_text,
        "designer profile report records comma-separated designer entity state",
        errors,
    )
    check("Pending metadata designer placeholders: 0" in designer_profile_text, "designer profile report counts pending metadata designer placeholders", errors)
    check("## Metadata Designer String Status" in designer_profile_text, "designer profile report includes metadata designer string status", errors)
    check("## Final Metadata Designer Entity Status" in designer_profile_text, "designer profile report includes per-entity metadata designer status", errors)
    check("Re-run this report after profile files, metadata, or catalog checkout\n  state change." in designer_profile_text, "designer profile report rerun guidance matches current decided designer state", errors)
    check("Source | Expected catalog slug" in designer_profile_text, "designer profile report records candidate source and expected catalog slug", errors)
    check("`eliheuer`" in designer_profile_text, "designer profile report records expected Eli Heuer slug", errors)
    check("Exact profile found | Matching profile path" in designer_profile_text, "designer profile report records profile match status", errors)
    check("https://googlefonts.github.io/gf-guide/profile.html" in designer_profile_text, "designer profile report cites GF profile guide", errors)
    check("# Designer Profile Package Draft" in designer_profile_package_text, "designer profile package draft has expected heading", errors)
    check("Designer string: `Eli Heuer`" in designer_profile_package_text, "designer profile package draft uses AUTHORS designer string", errors)
    check("Catalog slug: `eliheuer`" in designer_profile_package_text, "designer profile package draft records expected slug", errors)
    check("Catalog slug ASCII-only: yes" in designer_profile_package_text, "designer profile package draft validates ASCII slug", errors)
    check("Catalog slug has hyphen: no" in designer_profile_package_text, "designer profile package draft validates no-hyphen slug", errors)
    check("Avatar filename matches slug: yes" in designer_profile_package_text, "designer profile package draft validates avatar filename", errors)
    check("Local google/fonts checkout: `/Users/eli/GH/forks/fonts`" in designer_profile_package_text, "designer profile package draft records local google/fonts checkout", errors)
    check("Local designers directory exists: yes" in designer_profile_package_text, "designer profile package draft checks local designers catalog", errors)
    check("`gftools add-designer` available: yes" in designer_profile_package_text, "designer profile package draft checks gftools add-designer", errors)
    check("Candidate info.pb validator present: yes" in designer_profile_package_text, "designer profile package draft checks info.pb validator helper", errors)
    check("Candidate info.pb draft exists: yes" in designer_profile_package_text, "designer profile package draft tracks candidate info.pb file", errors)
    check("Candidate info.pb draft passes validator: yes" in designer_profile_package_text, "designer profile package draft confirms candidate info.pb validates", errors)
    check("Candidate info.pb link: `https://github.com/eliheuer`" in designer_profile_package_text, "designer profile package draft records candidate info.pb link", errors)
    check("Candidate image validator present: yes" in designer_profile_package_text, "designer profile package draft checks image validator helper", errors)
    check("Candidate image validator enforces filename: yes" in designer_profile_package_text, "designer profile package draft checks image filename validator helper", errors)
    check("Candidate bio validator present: yes" in designer_profile_package_text, "designer profile package draft checks bio validator helper", errors)
    check("Candidate bio validator enforces third-person voice: yes" in designer_profile_package_text, "designer profile package draft checks third-person bio validator helper", errors)
    check("Candidate bio draft exists: yes" in designer_profile_package_text, "designer profile package draft tracks candidate bio file", errors)
    check("Candidate bio draft passes validator: yes" in designer_profile_package_text, "designer profile package draft confirms candidate bio validates", errors)
    check("Candidate bio links: `https://github.com/eliheuer`" in designer_profile_package_text, "designer profile package draft records candidate bio links", errors)
    check("Candidate info/bio link consistency: yes" in designer_profile_package_text, "designer profile package draft checks candidate info/bio link consistency", errors)
    check("Designer profile prepare helper present: yes" in designer_profile_package_text, "designer profile package draft checks prepare helper presence", errors)
    check("Designer profile prepare helper checks info/bio link consistency: yes" in designer_profile_package_text, "designer profile package draft confirms prepare helper link consistency check", errors)
    check("Designer profile prepare helper dry-run ready: no" in designer_profile_package_text, "designer profile package draft records current prepare helper readiness", errors)
    check("Designer profile prepare helper blocking findings:" in designer_profile_package_text, "designer profile package draft records prepare helper blockers", errors)
    check("Prepare blocker is missing approved image input: yes" in designer_profile_package_text, "designer profile package draft classifies missing approved image blocker", errors)
    check("Prepare blocker is downstream checkout cleanliness: yes" in designer_profile_package_text, "designer profile package draft classifies downstream checkout cleanliness blocker", errors)
    check("Approved profile inputs ready to apply: no" in designer_profile_package_text, "designer profile package draft summarizes profile input readiness", errors)
    check("Downstream profile checkout ready to apply: no" in designer_profile_package_text, "designer profile package draft summarizes downstream profile checkout readiness", errors)
    check("Current dry-run blocker details:" in designer_profile_package_text, "designer profile package draft lists prepare helper blocker details", errors)
    check("image file does not exist:" in designer_profile_package_text, "designer profile package draft records missing profile image blocker", errors)
    check("google/fonts checkout has dirty paths outside the designer profile path:" in designer_profile_package_text, "designer profile package draft records downstream dirty-path blocker", errors)
    check("ofl/virtuagrotesk" in designer_profile_package_text, "designer profile package draft names the quarantined family package dirty path", errors)
    check("Target profile directory already exists: no" in designer_profile_package_text, "designer profile package draft checks target directory collision", errors)
    check("Expected profile files already present: 0 / 3" in designer_profile_package_text, "designer profile package draft counts existing target files", errors)
    check("Profile path collision risk: no" in designer_profile_package_text, "designer profile package draft records collision risk", errors)
    check("Draft placeholders still unresolved: 3" in designer_profile_package_text, "designer profile package draft counts unresolved inputs", errors)
    check("Missing final inputs: designer profile link decision, maintainer-approved biography, square 100-300px profile image" in designer_profile_package_text, "designer profile package draft lists unresolved inputs", errors)
    check('Profile link may be blank if the approved Google Fonts profile uses' in designer_profile_package_text, "designer profile package draft records blank-link option from GF practice", errors)
    check("## Maintainer Input Checklist" in designer_profile_package_text, "designer profile package draft includes maintainer input checklist", errors)
    check("| Final `METADATA.pb` designer string | `Eli Heuer` applied in downstream preview | Keep profile `info.pb` spelling exactly matched. |" in designer_profile_package_text, "designer profile package draft records final metadata designer string", errors)
    check("| Designer profile link | candidate `https://github.com/eliheuer`; maintainer approval pending | Approve this URL, provide one canonical website/social URL, or deliberately leave `link: \"\"` in `info.pb`. |" in designer_profile_package_text, "designer profile package draft asks for profile link approval or blank-link choice", errors)
    check("if `info.pb` uses a non-empty link, include that same URL in the bio links" in designer_profile_package_text, "designer profile package draft asks for approved bio with matching info.pb link", errors)
    check("| Profile image | `path/to/eliheuer.png` placeholder | Provide a square 100-300px image that passes `make designer-profile-image-check`. |" in designer_profile_package_text, "designer profile package draft asks for validated image", errors)
    check("do not create files in\n  `/Users/eli/GH/forks/fonts/catalog/designers` until the biography and\n  image are approved" in designer_profile_package_text, "designer profile package draft avoids premature downstream profile writes", errors)
    check("commit, stash,\n  or review that work before applying a separate designer-profile branch" in designer_profile_package_text, "designer profile package draft explains family-package dirty checkout handling before profile work", errors)
    check("Keep this work separate from the family package branch" in designer_profile_package_text, "designer profile package draft keeps profile PR separate from family package", errors)
    check("test ! -e /Users/eli/GH/forks/fonts/catalog/designers/eliheuer" in designer_profile_package_text, "designer profile package draft checks target path before downstream writes", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short -- catalog/designers/eliheuer" in designer_profile_package_text, "designer profile package draft gives scoped profile status command", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short" in designer_profile_package_text, "designer profile package draft gives full downstream status command", errors)
    check("## Guarded Prepare Helper" in designer_profile_package_text, "designer profile package draft includes guarded prepare helper section", errors)
    check("requires any non-empty `info.pb` link to appear in `bio.html`" in designer_profile_package_text, "designer profile package draft documents prepare helper info/bio link consistency", errors)
    check("make designer-profile-prepare-check" in designer_profile_package_text, "designer profile package draft documents profile prepare dry-run target", errors)
    check("./venv/bin/python scripts/prepare_designer_profile.py --image path/to/eliheuer.png --apply" in designer_profile_package_text, "designer profile package draft documents explicit prepare apply command", errors)
    check("Default image candidate: `documentation/designer-profile-candidate/eliheuer.png`" in designer_profile_package_text, "designer profile package draft records default image candidate", errors)
    check("## Candidate `bio.html`" in designer_profile_package_text, "designer profile package draft includes candidate bio section", errors)
    check("make designer-profile-bio-check BIO=documentation/designer-profile-candidate/bio.html" in designer_profile_package_text, "designer profile package draft documents candidate bio validation command", errors)
    check("GitHub profile as a temporary profile link" in designer_profile_package_text, "designer profile package draft marks candidate profile link as temporary", errors)
    check("candidate passes local validation now" in designer_profile_package_text, "designer profile package draft records candidate validation state", errors)
    check("## Candidate `info.pb`" in designer_profile_package_text, "designer profile package draft includes candidate info.pb section", errors)
    check("documentation/designer-profile-candidate/info.pb" in designer_profile_package_text, "designer profile package draft records candidate info.pb path", errors)
    check("make designer-profile-info-check INFO=documentation/designer-profile-candidate/info.pb" in designer_profile_package_text, "designer profile package draft documents candidate info.pb validation command", errors)
    check("catalog/designers/eliheuer/info.pb" in designer_profile_package_text, "designer profile package draft includes info.pb path", errors)
    check("catalog/designers/eliheuer/bio.html" in designer_profile_package_text, "designer profile package draft includes bio.html path", errors)
    check("catalog/designers/eliheuer/eliheuer.png" in designer_profile_package_text, "designer profile package draft includes image path", errors)
    check('designer: "Eli Heuer"' in designer_profile_package_text, "designer profile package draft includes info.pb designer field", errors)
    check('link: "https://github.com/eliheuer"' in designer_profile_package_text, "designer profile package draft includes temporary candidate info.pb link", errors)
    check('file_name: "eliheuer.png"' in designer_profile_package_text, "designer profile package draft includes avatar filename", errors)
    check("If `link` is non-empty, the guarded prepare helper requires the same\nURL to appear in `bio.html`" in designer_profile_package_text, "designer profile package draft documents non-empty info link must appear in bio", errors)
    check("The avatar `file_name` must match the image file inside the same" in designer_profile_package_text, "designer profile package draft records avatar file rule", errors)
    check("make designer-profile-info-check INFO=/Users/eli/GH/forks/fonts/catalog/designers/eliheuer/info.pb" in designer_profile_package_text, "designer profile package draft documents info.pb validator command", errors)
    check("make designer-profile-image-check IMAGE=/Users/eli/GH/forks/fonts/catalog/designers/eliheuer/eliheuer.png" in designer_profile_package_text, "designer profile package draft documents downstream image validator command", errors)
    check("make designer-profile-bio-check BIO=/Users/eli/GH/forks/fonts/catalog/designers/eliheuer/bio.html" in designer_profile_package_text, "designer profile package draft documents downstream bio validator command", errors)
    check("First-person pronouns are rejected by the local validator" in designer_profile_package_text, "designer profile package draft records first-person bio guard", errors)
    check(
        "More than 200 characters and less than 1000 characters" in designer_profile_package_text,
        "designer profile package draft records bio length requirement",
        errors,
    )
    check("Filename must match the profile directory slug exactly" in designer_profile_package_text, "designer profile package draft records profile image filename requirement", errors)
    check("Between 100px and 300px" in designer_profile_package_text, "designer profile package draft records image size requirement", errors)
    check("make designer-profile-image-check IMAGE=path/to/eliheuer.png" in designer_profile_package_text, "designer profile package draft documents image validator command", errors)
    check("make designer-profile-bio-check BIO=path/to/bio.html" in designer_profile_package_text, "designer profile package draft documents bio validator command", errors)
    check("gftools add-designer" in designer_profile_package_text, "designer profile package draft documents add-designer workflow", errors)
    check("## Profile Request Form Packet" in designer_profile_package_text, "designer profile package draft includes official form packet", errors)
    check("https://docs.google.com/forms/d/e/1FAIpQLSehvbqqgL5Dlv9WG0mmBVNfFAjoMIx-2d1YJNrU7C-zKBNkcw/viewform" in designer_profile_package_text, "designer profile package draft cites official profile request form", errors)
    check("Linked family: `Virtua Grotesk`" in designer_profile_package_text, "designer profile package draft records linked family for profile form", errors)
    check("roughly 2-4 weeks" in designer_profile_package_text, "designer profile package draft records GF profile publication timing", errors)
    check("one designer profile per PR" in designer_profile_package_text, "designer profile package draft documents one-profile PR scope", errors)
    check("Designer profile` and `Ready for review` labels" in designer_profile_package_text, "designer profile package draft documents profile PR labels", errors)
    check("Traffic Jam" in designer_profile_package_text, "designer profile package draft documents Traffic Jam workflow note", errors)
    check("https://googlefonts.github.io/gf-guide/profile.html" in designer_profile_package_text, "designer profile package draft cites GF profile guide", errors)
    image_validator_text = (ROOT / "scripts/validate_designer_profile_image.py").read_text()
    check("expected-file-name" in image_validator_text, "designer profile image validator accepts expected filename", errors)
    check("image filename should be" in image_validator_text, "designer profile image validator enforces expected filename", errors)
    check("MIN_SIZE = 100" in image_validator_text and "MAX_SIZE = 300" in image_validator_text, "designer profile image validator enforces GF profile size range", errors)
    check("png_dimensions" in image_validator_text and "jpeg_dimensions" in image_validator_text, "designer profile image validator reads PNG and JPEG dimensions", errors)
    check("image must be square" in image_validator_text, "designer profile image validator enforces square images", errors)
    bio_validator_text = (ROOT / "scripts/validate_designer_profile_bio.py").read_text()
    check("MIN_CHARS = 200" in bio_validator_text and "MAX_CHARS = 1000" in bio_validator_text, "designer profile bio validator enforces GF profile bio length range", errors)
    check("bio.html should use paragraph tags" in bio_validator_text, "designer profile bio validator checks paragraph snippets", errors)
    check("FIRST_PERSON_PRONOUN_RE" in bio_validator_text, "designer profile bio validator defines first-person pronoun guard", errors)
    check("third person, not first person" in bio_validator_text, "designer profile bio validator enforces third-person voice", errors)
    check("one or two links" in bio_validator_text, "designer profile bio validator checks link count", errors)
    check("target=\\\"_blank\\\"" in bio_validator_text, "designer profile bio validator checks target blank links", errors)
    check("PLACEHOLDER_MARKERS" in bio_validator_text, "designer profile bio validator defines placeholder markers", errors)
    check("should not use a placeholder URL" in bio_validator_text, "designer profile bio validator rejects placeholder URLs", errors)
    check("should not use placeholder link text" in bio_validator_text, "designer profile bio validator rejects placeholder link labels", errors)
    check("label should omit the URL protocol" in bio_validator_text, "designer profile bio validator rejects protocol-prefixed link labels", errors)
    check("social link label should be" in bio_validator_text, "designer profile bio validator checks social link labels", errors)
    info_validator_text = (ROOT / "scripts/validate_designer_profile_info.py").read_text()
    check("validate_designer_profile_info.py path/to/info.pb" in info_validator_text, "designer profile info validator has expected CLI usage", errors)
    check("designer should be" in info_validator_text, "designer profile info validator checks designer spelling", errors)
    check("avatar.file_name should be" in info_validator_text, "designer profile info validator checks avatar file name", errors)
    check("link should be empty or a full http(s) URL" in info_validator_text, "designer profile info validator checks link URL shape", errors)
    check("not a placeholder" in info_validator_text, "designer profile info validator rejects placeholder links", errors)
    prepare_designer_profile_text = (ROOT / "scripts/prepare_designer_profile.py").read_text()
    check("info.pb link should match one bio.html link" in prepare_designer_profile_text, "designer profile prepare helper checks info/bio link consistency", errors)
    designer_profile_test_text = (ROOT / "scripts/test_designer_profile_validators.sh").read_text()
    check("profile prepare link mismatch" in designer_profile_test_text, "designer profile tests cover info/bio link mismatch", errors)
    check("prepare helper should allow a blank info.pb link" in designer_profile_test_text, "designer profile tests cover blank info.pb link option", errors)
    check("Social links should be labeled by service name" in designer_profile_package_text, "designer profile package draft documents social link label rule", errors)
    check("Website link text should omit the `http://` or `https://` protocol" in designer_profile_package_text, "designer profile package draft documents website link label rule", errors)
    check("# Google Fonts Language Metadata" in language_metadata_text, "language metadata report has expected heading", errors)
    check("Script record exists: yes" in language_metadata_text, "language metadata report finds Arabic script record", errors)
    check("Script id: `Arab`" in language_metadata_text, "language metadata report confirms Arab script id", errors)
    check("Script name: `Arabic`" in language_metadata_text, "language metadata report confirms Arabic script name", errors)
    for language_code in ["ar_Arab", "fa_Arab", "ur_Arab"]:
        check(f"| `{language_code}` | yes | `Arab` |" in language_metadata_text, f"language metadata report includes {language_code}", errors)
    check("`primary_script`: `Arab`" in language_metadata_text, "language metadata report records target primary script", errors)
    check("Preview `subsets` match target: yes" in language_metadata_text, "language metadata report checks preview subsets against target", errors)
    check("Preview `primary_script` matches target: yes" in language_metadata_text, "language metadata report checks preview primary_script against target", errors)
    check("Preview non-Noto `languages` entries absent: yes" in language_metadata_text, "language metadata report checks preview languages omission", errors)
    check("Preview custom `sample_text` absent: yes" in language_metadata_text, "language metadata report checks preview sample_text omission", errors)
    check("Compared Arabic package examples present: 9 / 9" in language_metadata_text, "language metadata report compares current Arabic package examples", errors)
    check("Compared examples with `arabic` subset: 9 / 9" in language_metadata_text, "language metadata report confirms compared Arabic packages keep arabic subset", errors)
    check("Compared examples with `primary_script: \"Arab\"`: 9 / 9" in language_metadata_text, "language metadata report confirms compared Arabic packages keep Arab primary_script", errors)
    check("Compared non-Noto Arabic examples omit `languages`: yes" in language_metadata_text, "language metadata report confirms non-Noto Arabic examples omit languages", errors)
    check("Compared non-Noto Arabic examples omit `sample_text`: yes" in language_metadata_text, "language metadata report confirms non-Noto Arabic examples omit sample_text", errors)
    check("## Downstream Preview Alignment" in language_metadata_text, "language metadata report includes downstream preview alignment table", errors)
    for subset in ["arabic", "latin", "latin-ext", "menu"]:
        check(f"`{subset}`" in language_metadata_text, f"language metadata report records expected subset: {subset}", errors)
    for package_path in [
        "ofl/estedad/METADATA.pb",
        "ofl/scheherazadenew/METADATA.pb",
        "ofl/playpensansarabic/METADATA.pb",
        "ofl/readexpro/METADATA.pb",
        "ofl/cairo/METADATA.pb",
        "ofl/amiri/METADATA.pb",
        "ofl/notosansarabic/METADATA.pb",
        "ofl/notonaskharabic/METADATA.pb",
        "ofl/notokufiarabic/METADATA.pb",
    ]:
        check(
            f"| `{package_path}` |" in language_metadata_text,
            f"language metadata report confirms recent Arabic package metadata: {package_path}",
            errors,
        )
    check("https://googlefonts.github.io/gf-guide/lang.html" in language_metadata_text, "language metadata report cites GF language guide", errors)
    check("documentation/google-fonts-language-metadata.md" in text, "metadata review points to language metadata report", errors)


def decision_log_errors(errors: list[str]) -> None:
    text = (ROOT / "documentation/google-fonts-decisions.md").read_text()
    questions_text = (ROOT / "documentation/google-fonts-decision-questions.md").read_text()
    answer_sheet_text = (ROOT / "documentation/google-fonts-decision-answer-sheet.md").read_text()
    decision_readiness_text = (ROOT / "documentation/decision-readiness.md").read_text()
    decision_application_text = (ROOT / "documentation/decision-application-blockers.md").read_text()
    required_headings = [
        "## Public upstream URL",
        "## Packager source strategy",
        "## Author/contact lines",
        "## Family name, namecheck, trademarks, and CLA",
        "## Copyright authorship and AI disclosure",
        "## First-submission script scope",
        "## Private-use icon block",
        "## Vendor ID",
        "## Kerning",
        "## `avar`",
        "## Version strategy",
        "## Upstream release tag",
        "## Article or legacy description",
        "## Project template automation",
        "## Custom sample text",
    ]
    for heading in required_headings:
        check(heading in text, f"decision log includes {heading}", errors)
    required_questions = [
        "## 1. Public Upstream URL",
        "## 2. Packager Source Strategy",
        "## 3. Author and Contributor Strings",
        "## 4. Family Name, Namecheck, Trademarks, and CLA",
        "## 5. PUA Icon Block",
        "## 6. Vendor ID",
        "## 7. Kerning Scope",
        "## 8. Copyright Authorship and AI Disclosure",
    ]
    for heading in required_questions:
        check(heading in questions_text, f"decision questions include {heading}", errors)
    check(
        "documentation/google-fonts-decisions.md" in questions_text,
        "decision questions point back to canonical decision log",
        errors,
    )
    check("# Google Fonts Decision Answer Sheet" in answer_sheet_text, "decision answer sheet has expected heading", errors)
    check("documentation/google-fonts-decision-questions.md" in answer_sheet_text, "decision answer sheet points to canonical question list", errors)
    check("documentation/google-fonts-decisions.md" in answer_sheet_text, "decision answer sheet points to canonical decision log", errors)
    check("## Priority 3" in answer_sheet_text, "decision answer sheet groups remaining decisions by priority", errors)
    for expected in [
        "### PUA Icon Block",
        "### Kerning Scope",
    ]:
        check(expected in answer_sheet_text, f"decision answer sheet includes {expected}", errors)
    for decided in [
        "### Public Upstream URL",
        "### Packager Source Strategy",
        "### Family Name, Namecheck, Trademarks, and CLA",
        "### Copyright Authorship and AI Disclosure",
        "### Vendor ID",
        "### Article or Legacy Description",
        "### `avar`",
        "### Custom Sample Text",
        "### Version Strategy",
        "### Upstream Release Tag",
        "### Project Template Automation",
    ]:
        check(decided not in answer_sheet_text, f"decision answer sheet omits decided item {decided}", errors)
    check("Apply targets:" in answer_sheet_text, "decision answer sheet includes per-decision apply targets", errors)
    check(answer_sheet_text.count("Apply targets:") == 2, "decision answer sheet includes apply targets for every open decision", errors)
    check("documentation/google-fonts-submission-handoff.md" in answer_sheet_text, "decision answer sheet includes final-submission rationale apply targets", errors)
    check("documentation/google-fonts-submission-handoff.md" in answer_sheet_text, "decision answer sheet includes handoff apply targets", errors)
    check("Maintainer answer:" in answer_sheet_text and "TBD by maintainer" in answer_sheet_text, "decision answer sheet keeps answers explicit and maintainer-owned", errors)
    check(
        "Rerun `make preflight` so proof evidence and generated reports stay synchronized." in answer_sheet_text,
        "decision answer sheet points maintainers at synchronized preflight",
        errors,
    )
    check(
        "2026-05-22" in questions_text and "not legal or trademark clearance" in questions_text,
        "decision questions record preliminary name check limitations",
        errors,
    )
    check(
        "Origin-derived candidate:" in text
        and "Origin-derived candidate:" in questions_text
        and "https://github.com/eliheuer/virtua-grotesk" in text
        and "https://github.com/eliheuer/virtua-grotesk" in questions_text
        and "documentation/public-upstream-readiness.md" in text
        and "documentation/public-upstream-readiness.md" in questions_text,
        "decision docs record origin-derived public upstream candidate",
        errors,
    )
    check("namecheck.fontdata.com" in text and "namecheck.fontdata.com" in questions_text, "decision docs track GF namecheck requirement", errors)
    for expected in [
        "Commit built fonts",
        "Release/archive assets",
        "Build from source",
        "documentation/package-source-files-audit.md",
    ]:
        check(expected in questions_text, f"decision questions track Packager source option: {expected}", errors)
    check(
        "`source.files` as 3/4 tracked" in questions_text
        and "Build-from-source inputs are 6/6 tracked" in questions_text,
        "decision questions expose current tracked/untracked package-source evidence",
        errors,
    )
    check(
        "### Packager Source Strategy" not in answer_sheet_text
        and "## Packager source strategy" in text
        and "Status: decided" in text,
        "decision answer sheet omits closed Packager source-strategy decision",
        errors,
    )
    check(
        "Release/archive assets" in questions_text
        and "Selected answer: use the release/archive strategy for the first submission" in questions_text
        and "Build-from-source remains a\nseparate review choice" in questions_text,
        "decision questions preserve release/archive and build-from-source source strategy alternatives",
        errors,
    )
    check(
        "documentation/recent-google-fonts-packages.md" in questions_text
        and "All three sampled\n  upstream repos expose built fonts under `fonts/`, including\n  `fonts/variable/`" in questions_text
        and "Estedad as the closest Arabic-script\n  example" in questions_text,
        "decision questions cite recent upstream repo comparison for source strategy",
        errors,
    )
    check(
        "Use the release/archive strategy deliberately" in text
        and "Make the release archive the reviewed source of the packaged files" in text
        and "Treat build-from-source as a separate review" in text,
        "decision log surfaces decided Packager source-strategy recommendation",
        errors,
    )
    check(
        "ofl/googlesanscode/METADATA.pb" in text
        and "ofl/scheherazadenew/METADATA.pb" in text
        and "ofl/amiri/METADATA.pb" in text,
        "decision log records release/archive Google Fonts source-strategy references",
        errors,
    )
    check(
        "Status: decided" in text
        and "GFT_PACKAGER_SOURCE_MODE=latest-release" in text
        and "Omit `source.config_yaml`" in text,
        "decision log records chosen release/archive source strategy",
        errors,
    )
    check(
        "Recent merged upstream repos in the local audit expose built fonts in\n  `fonts/`" in text
        and "Estedad is the closest sampled Arabic-script upstream comparison" in text,
        "decision log records recent upstream source-strategy evidence",
        errors,
    )
    check(
        "`source.files` as 3/4 tracked" in text
        and "build-from-source inputs as 6/6 tracked" in text,
        "decision log records tracked/untracked package-source evidence",
        errors,
    )
    check("--build-from-source" in text and "--build-from-source" in questions_text, "decision docs track build-from-source source strategy", errors)
    check("--latest-release" in questions_text, "decision questions track latest-release source strategy", errors)
    check("AI-use disclosure" in text and "AI-use disclosure" in questions_text, "decision docs track GF AI-use disclosure requirement", errors)
    check("one checkbox" in text and "one checkbox" in questions_text, "decision docs track combined copyright and AI checkbox", errors)
    check("sole copyright author" in questions_text, "decision questions track GF copyright authorship statement", errors)
    check("documentation/pua-scope.md" in text and "documentation/pua-scope.md" in questions_text, "decision docs point to generated PUA scope report", errors)
    check("23 currently encoded PUA codepoints" in questions_text, "decision questions record current PUA count", errors)
    check("not a continuous encoded range" in questions_text, "decision questions describe current PUA set accurately", errors)
    check("ScheherazadeNew" in questions_text and "Kedebideri" in questions_text, "decision questions include local GF PUA precedent", errors)
    check("make kerning-proof-check" in text and "make kerning-proof-check" in questions_text, "decision docs track gftools QA kerning proof target", errors)
    check("gftools qa --proof" in text and "gftools qa --proof" in questions_text, "decision docs track GF visual kerning proof command", errors)
    check("Regular, Medium, SemiBold, and Bold" in text and "Regular, Medium, SemiBold, and Bold" in questions_text, "decision docs track kerning proof instance coverage", errors)
    check("sample_text" in text, "decision log tracks custom sample_text decision", errors)
    check("default Arabic textprotos" in text and "`primary_script: \"Arab\"`" in text, "decision log records GF sample_text default path", errors)
    check("# Decision Readiness" in decision_readiness_text, "decision readiness report has expected heading", errors)
    check("Open decisions: 2" in decision_readiness_text, "decision readiness report records open decision count", errors)
    check("Decided decisions: 13" in decision_readiness_text, "decision readiness report records decided decision count", errors)
    check("Decision question prompts: 8" in decision_readiness_text, "decision readiness report records question count", errors)
    check(
        "Decision question prompts with answer guidance: 8 / 8" in decision_readiness_text,
        "decision readiness report verifies question prompts are answer-ready",
        errors,
    )
    check("Open decisions with matching question prompts: 2 / 2" in decision_readiness_text, "decision readiness report maps open decisions to questions", errors)
    check("Open decisions with apply-to blocks: 2 / 2" in decision_readiness_text, "decision readiness report confirms apply-to blocks", errors)
    check("Open decision apply-to surface items: 8" in decision_readiness_text, "decision readiness report counts apply-to surface items", errors)
    check("Open decision local path patterns present: 5 / 5" in decision_readiness_text, "decision readiness report checks local apply-to path patterns", errors)
    check("Open decision non-file or downstream surfaces: 3" in decision_readiness_text, "decision readiness report counts non-file and downstream surfaces", errors)
    check("## Question Prompt Inventory" in decision_readiness_text, "decision readiness report includes question prompt inventory", errors)
    check("## Prioritized Question Packet" in decision_readiness_text, "decision readiness report includes prioritized question packet", errors)
    check("| Family name, namecheck, trademarks, and CLA | decided | yes | yes |" in decision_readiness_text, "decision readiness report records resolved family/namecheck decision", errors)
    check("## Apply-To Surface Inventory" in decision_readiness_text, "decision readiness report includes apply-to surface inventory", errors)
    check("## Mechanical Apply Coverage" in decision_readiness_text, "decision readiness report includes mechanical apply coverage", errors)
    for expected_apply_surface in [
        "`scripts/apply_public_upstream_url.py`",
        "`make downstream-metadata-check`",
        "`make package-dry-run`",
        "`make designer-profile-check`",
        "Decision-linked warnings",
    ]:
        check(
            expected_apply_surface in decision_readiness_text,
            f"decision readiness report covers mechanical apply surface: {expected_apply_surface}",
            errors,
        )
    check(
        "Rerun `make preflight` after any decision is answered" in decision_readiness_text,
        "decision readiness report points decision follow-up at synchronized preflight",
        errors,
    )
    check(".github/workflows/" in decision_readiness_text, "decision readiness report tracks optional template workflow surface", errors)
    check("Add Font template authorship prompt tracked: yes" in decision_readiness_text, "decision readiness report tracks Add Font authorship prompt", errors)
    check("Add Font template namecheck prompt tracked: yes" in decision_readiness_text, "decision readiness report tracks Add Font namecheck prompt", errors)
    check("https://googlefonts.github.io/gf-guide/onboarding.html" in decision_readiness_text, "decision readiness report cites GF onboarding guide", errors)
    check("https://googlefonts.github.io/gf-guide/metadata.html" in decision_readiness_text, "decision readiness report cites GF metadata guide", errors)
    check("# Decision Application Blockers" in decision_application_text, "decision application blocker report has expected heading", errors)
    check("Open maintainer decisions: 2" in decision_application_text, "decision application blocker report records open decision count", errors)
    check("Decided maintainer decisions: 13" in decision_application_text, "decision application blocker report records decided decision count", errors)
    check("Maintainer answer sheet unanswered prompts: 2" in decision_application_text, "decision application blocker report records unanswered answer-sheet prompt count", errors)
    check("Maintainer answer sheet unanswered prompt names: PUA Icon Block, Kerning Scope" in decision_application_text, "decision application blocker report records unanswered answer-sheet prompt names", errors)
    check("Downstream metadata pending/placeholder lines: 2" in decision_application_text, "decision application blocker report records metadata blocker count", errors)
    check("Actionable pending decision markers: 0" in decision_application_text, "decision application blocker report records actionable pending markers", errors)
    check("Package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template" in decision_application_text, "decision application blocker report records package first blocker", errors)
    for expected in [
        "| Author/contact lines | decided | does not block metadata text | does not block directly | blocks until matching profile exists or request is prepared |",
        "| Private-use icon block | open | does not block | does not block directly | blocks until included or deferred |",
        "| Kerning | open | does not block | does not block directly | blocks until completed or deferred |",
        "| Final release/source commit | pending final source state | blocks | blocks | blocks |",
        "| Final Google Fonts date_added | pending final package date | blocks | blocks | blocks until final downstream metadata date is set |",
        "| GitHub API credentials | local environment pending | does not block metadata text | blocks | blocks package verification |",
    ]:
        check(expected in decision_application_text, f"decision application blocker report maps gate: {expected}", errors)
    check("Designer marker: absent" in decision_application_text, "decision application blocker report tracks designer marker", errors)
    check("Source commit marker: present" in decision_application_text, "decision application blocker report tracks source commit marker", errors)
    check("Final date_added marker: present" in decision_application_text, "decision application blocker report tracks date_added marker", errors)
    check("## Maintainer Answer Sheet State" in decision_application_text, "decision application blocker report includes answer-sheet state section", errors)
    check("| PUA Icon Block | yes | yes |" in decision_application_text, "decision application blocker report maps PUA prompt as unanswered", errors)
    check("| Kerning Scope | yes | yes |" in decision_application_text, "decision application blocker report maps kerning prompt as unanswered", errors)
    check("GitHub release archive" in decision_application_text, "decision application blocker report tracks release archive finalization", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in decision_application_text, "decision application blocker report cites GF package guide", errors)


def upstream_audit_errors(errors: list[str]) -> None:
    text = (ROOT / "documentation/google-fonts-upstream-audit.md").read_text()
    template_pr_text = (ROOT / "documentation/google-fonts-template-and-pr-audit.md").read_text()
    recent_packages_text = (ROOT / "documentation/recent-google-fonts-packages.md").read_text()
    template_automation_text = (ROOT / "documentation/project-template-automation-readiness.md").read_text()
    open_decision_names = [
        "Public upstream URL",
        "Packager source strategy",
        "Author/contact",
        "Family name, namecheck",
        "Copyright-authorship and AI-use disclosure",
        "PUA/private icon block",
        "Vendor ID",
        "Kerning scope",
    ]
    required_sections = [
        "## Satisfied upstream artifacts",
        "## Satisfied build and QA gates",
        "## Current drawing/source blockers",
        "## Current decision blockers",
        "## Current final-submission gate",
    ]
    for section in required_sections:
        check(section in text, f"upstream audit includes {section}", errors)
    check("make preflight" in text, "upstream audit documents current preflight gate", errors)
    check("make test" in text, "upstream audit documents final QA gate", errors)
    check("documentation/final-submission-blockers.md" in text, "upstream audit points to final-submission blocker summary", errors)
    for decision_name in open_decision_names:
        check(decision_name in text, f"upstream audit tracks open decision blocker: {decision_name}", errors)
    for report_name, report_pattern in [
        ("Google Fonts axis-registry audit", r"Google Fonts axis-registry audit"),
        ("decision readiness report", r"decision readiness\s+report"),
        ("Vendor ID readiness report", r"Vendor ID readiness\s+report"),
        ("avar readiness report", r"avar readiness\s+report"),
        ("authorship and AI-disclosure readiness report", r"authorship and AI-disclosure readiness\s+report"),
        ("family-name readiness report", r"family-name readiness\s+report"),
        ("release metadata report", r"release metadata\s+report"),
        ("release/source readiness report", r"release/source readiness\s+report"),
        ("upstream structure readiness report", r"upstream structure readiness\s+report"),
        ("designer-profile readiness audit", r"designer-profile readiness audit"),
        ("designer-profile package draft", r"designer-profile package\s+draft"),
        ("Google Fonts language-metadata audit", r"Google Fonts language-metadata\s+audit"),
        ("open-placeholder audit", r"open-placeholder audit"),
        ("public upstream URL readiness report", r"public upstream URL readiness\s+report"),
        ("package source-file audit", r"package source-file\s+audit"),
        ("downstream metadata readiness report", r"downstream metadata readiness\s+report"),
        ("submission handoff readiness report", r"submission handoff readiness\s+report"),
        ("kerning readiness report", r"kerning readiness\s+report"),
        ("glyph reachability report", r"glyph\s+reachability report"),
        ("recent-package audit", r"recent-package audit"),
    ]:
        check(
            re.search(report_pattern, text) is not None,
            f"upstream audit documents reports-only artifact: {report_name}",
            errors,
        )
    check(
        "Add Font" in text and "issue-template audit" in text,
        "upstream audit documents reports-only artifact: Add Font issue-template audit",
        errors,
    )
    check("release metadata" in text and "final-handoff view" in text, "upstream audit includes release metadata in final blocker summary", errors)
    check("https://googlefonts.github.io/gf-guide/upstream.html" in text, "upstream audit cites GF upstream guide", errors)
    check("https://googlefonts.github.io/gf-guide/qa.html" in text, "upstream audit cites GF QA guide", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in text, "upstream audit cites GF package guide", errors)
    check(
        "# Google Fonts Template and Recent PR Audit" in template_pr_text,
        "template and PR audit has expected heading",
        errors,
    )
    check("googlefonts-project-template" in template_pr_text, "template and PR audit cites project template", errors)
    check("documentation/recent-google-fonts-packages.md" in template_pr_text, "template and PR audit points to generated recent-package report", errors)
    check(".templaterc.json" in template_pr_text, "template and PR audit records current template maintenance files", errors)
    check("Renovate" in template_pr_text, "template and PR audit records current dependency automation option", errors)
    check("documentation/google-fonts-decisions.md" in template_pr_text, "template and PR audit points to template automation decision", errors)
    check(
        "The maintainer decision for the first\n"
        "submission is to defer CI, Pages, Renovate, and template-maintenance\n"
        "automation" in template_pr_text,
        "template and PR audit records decided template automation deferral",
        errors,
    )
    check("google/fonts#10401" in template_pr_text, "template and PR audit includes recent Arabic new-font PR", errors)
    check("google/fonts#10455" in template_pr_text, "template and PR audit includes recent Arabic release/archive PR", errors)
    check("primary_script: \"Arab\"" in template_pr_text, "template and PR audit tracks Arabic primary script pattern", errors)
    check(
        "Scheherazade New" in template_pr_text
        and "GitHub release download `.zip`" in template_pr_text
        and "source.archive_url" in template_pr_text,
        "template and PR audit tracks recent Arabic release/archive source pattern",
        errors,
    )
    check("article/ARTICLE.en_us.html" in template_pr_text, "template and PR audit tracks current Article pattern", errors)
    check(
        "The Article flow is the decided first-submission path" in template_pr_text
        and "map it into downstream `article/ARTICLE.en_us.html`" in template_pr_text,
        "template and PR audit records decided Article flow",
        errors,
    )
    check("A final Article decision is still needed" not in template_pr_text, "template and PR audit has no stale Article-decision blocker", errors)
    check(
        "removed `config_yaml` fields" in template_pr_text
        and "build-from-source strategy" in template_pr_text
        and "default branch or release/archive packaging" in template_pr_text,
        "template and PR audit records recent google/fonts config_yaml cleanup implications",
        errors,
    )
    check(
        "FontSpector report" in template_pr_text
        and "fontspector version: 1.6.0" in template_pr_text
        and "FontBakery-era automation" in template_pr_text,
        "template and PR audit preserves current Fontspector PR evidence",
        errors,
    )
    check(
        "drawing/source blockers, after rebuilding, regenerating the PDF proof, and\n"
        "  regenerating reports from that proof evidence" in template_pr_text,
        "template and PR audit documents synchronized preflight path",
        errors,
    )
    check(
        "upstream_info.md" in template_pr_text and "optional" in template_pr_text,
        "template and PR audit tracks optional upstream_info provenance",
        errors,
    )
    check(
        "upstream.yaml" in template_pr_text and "Packager-linked" in template_pr_text,
        "template and PR audit tracks upstream.yaml provenance",
        errors,
    )
    check("no\n  `tags` field" in template_pr_text, "template and PR audit records recent packages do not use METADATA tags field", errors)
    check("# Recent Google Fonts Package Audit" in recent_packages_text, "recent-package audit has expected heading", errors)
    check(
        "Alignment with `upstream/main`: `0 ahead, 0 behind`" in recent_packages_text
        and "Alignment with `origin/main`: `0 ahead, 0 behind`" in recent_packages_text,
        "recent-package audit records synced local google/fonts fork state",
        errors,
    )
    check("Dirty paths:" in recent_packages_text, "recent-package audit discloses local google/fonts dirty path count", errors)
    check(
        "Dirty `ofl/virtuagrotesk` paths:" in recent_packages_text,
        "recent-package audit discloses local Virtua Grotesk dry-run artifacts",
        errors,
    )
    check(
        "Newest selected package example: google/fonts#10546 (Pliant, 2026-05-22)" in recent_packages_text,
        "recent-package audit records newest selected package example",
        errors,
    )
    check(
        "Newest Packager merge found locally: google/fonts#10546 (2026-05-22)" in recent_packages_text,
        "recent-package audit records newest local Packager merge",
        errors,
    )
    check(
        "Packager merges newer than selected examples: 0" in recent_packages_text,
        "recent-package audit confirms no newer local Packager merges are omitted from the selected examples",
        errors,
    )
    check("Sample package directories present: 4 / 4" in recent_packages_text, "recent-package audit confirms sampled package directories exist", errors)
    check("| PR | Family | Merged | Path | Present |" in recent_packages_text, "recent-package audit table exposes sample presence column", errors)
    check("google/fonts#10546" in recent_packages_text, "recent-package audit includes Pliant PR", errors)
    check("google/fonts#10455" in recent_packages_text, "recent-package audit includes Scheherazade New PR", errors)
    check("google/fonts#10468" in recent_packages_text, "recent-package audit includes Akt PR", errors)
    check("google/fonts#10401" in recent_packages_text, "recent-package audit includes Estedad PR", errors)
    check("## Recent Packager Merges" in recent_packages_text, "recent-package audit includes generated recent Packager merge list", errors)
    check("gftools_packager_ofl_" in recent_packages_text, "recent-package audit derives recent package merges from google/fonts history", errors)
    recent_merge_section = markdown_section(recent_packages_text, "Recent Packager Merges")
    check(
        len(set(re.findall(r"google/fonts#\d+", recent_merge_section))) >= 5,
        "recent-package audit lists at least five recent Packager merges",
        errors,
    )
    check("primary_script" in recent_packages_text and "`Arab`" in recent_packages_text, "recent-package audit tracks Arabic primary_script", errors)
    check(
        "Source repo" in recent_packages_text
        and "Source commit" in recent_packages_text
        and "archive_url" in recent_packages_text,
        "recent-package audit exposes upstream source repo, commit, and archive_url columns",
        errors,
    )
    check(
        "https://github.com/silnrsi/font-scheherazade/releases/download/v4.500/ScheherazadeNew-4.500.zip" in recent_packages_text,
        "recent-package audit captures recent Arabic GitHub release archive_url pattern",
        errors,
    )
    check("## Upstream Repo Comparison" in recent_packages_text, "recent-package audit includes upstream repo comparison", errors)
    check(
        "`https://github.com/TheJonassss/Pliant`" in recent_packages_text
        and "`https://github.com/dimgrenev/akt`" in recent_packages_text
        and "`https://github.com/aminabedi68/Estedad`" in recent_packages_text,
        "recent-package audit compares upstream GitHub repos",
        errors,
    )
    check(
        "| Virtua Grotesk | `https://github.com/eliheuer/virtua-grotesk` | `pending final source commit` | yes | yes | documentation | yes | yes (ignored: yes)" in recent_packages_text,
        "recent-package audit compares Virtua upstream structure against recent repos",
        errors,
    )
    check(
        "The sampled upstream repos expose built fonts under `fonts/`, including `fonts/variable/` for variable examples" in recent_packages_text,
        "recent-package audit records upstream font exposure pattern",
        errors,
    )
    check(
        "Estedad is the closest Arabic-script comparison" in recent_packages_text
        and "source strategy is build-from-source" in recent_packages_text,
        "recent-package audit records Arabic upstream/source-config comparison",
        errors,
    )
    check(
        "Scheherazade New is the closest recent Arabic package for Virtua's selected release/archive path" in recent_packages_text
        and "source.archive_url` points to a GitHub release download `.zip`" in recent_packages_text,
        "recent-package audit records Arabic release/archive comparison",
        errors,
    )
    check(
        "mirror the Scheherazade New pattern" in recent_packages_text
        and "omit `source.config_yaml`" in recent_packages_text,
        "recent-package audit records selected latest-release source metadata pattern",
        errors,
    )
    check("source.commit" in recent_packages_text and "exact upstream commits" in recent_packages_text, "recent-package audit records exact source commit pattern", errors)
    check(
        "removed non-buildable `config_yaml` fields" in recent_packages_text
        and "reproducible build path" in recent_packages_text,
        "recent-package audit records config_yaml reproducibility caution",
        errors,
    )
    check("upstream.yaml" in recent_packages_text, "recent-package audit tracks upstream.yaml presence", errors)
    check("upstream_info.md" in recent_packages_text, "recent-package audit tracks upstream_info presence", errors)
    check("tags field" in recent_packages_text, "recent-package audit tracks METADATA tags field absence", errors)
    check("# Project Template Automation Readiness" in template_automation_text, "project-template automation report has expected heading", errors)
    check(
        "handoff gate should stay independent\n"
        "of CI, Pages, Renovate, or template refresh tooling" in template_automation_text,
        "project-template automation report clearly defers optional template tooling",
        errors,
    )
    check("Decision log status: decided" in template_automation_text, "project-template automation report records deferred decision status", errors)
    check("Optional template automation present:" in template_automation_text, "project-template automation report counts optional automation", errors)
    check("Local equivalent Make targets present:" in template_automation_text, "project-template automation report counts local equivalent targets", errors)
    check("Local QA target uses Fontspector: yes" in template_automation_text, "project-template automation report preserves Fontspector QA gate", errors)
    check("Local Makefile references FontBakery: no" in template_automation_text, "project-template automation report avoids stale FontBakery QA", errors)
    check("Local google/fonts workflows use Fontspector: yes" in template_automation_text, "project-template automation report checks current google/fonts CI uses Fontspector", errors)
    check("Local google/fonts workflows reference FontBakery: no" in template_automation_text, "project-template automation report checks current google/fonts CI avoids FontBakery", errors)
    check(
        "Official QA guide says FontBakery was previous and Fontspector is current: yes" in template_automation_text,
        "project-template automation report records current official QA Fontspector guidance",
        errors,
    )
    check(
        "Current project-template README still describes `make test` as" in template_automation_text
        and "FontBakery-based QA: yes" in template_automation_text,
        "project-template automation report records current template README FontBakery caveat",
        errors,
    )
    check(
        "Older tools/template prose still describes FontBakery-based" in template_automation_text,
        "project-template automation report records older guide/template QA caveat",
        errors,
    )
    check(
        "Fontspector-based `make test`" in template_automation_text
        and "official QA page" in template_automation_text
        and "local `google/fonts` workflow evidence point at" in template_automation_text
        and "Fontspector" in template_automation_text
        and "Do not introduce FontBakery" in template_automation_text,
        "project-template automation report documents future CI should stay on Fontspector",
        errors,
    )
    for feature in [
        "GitHub Actions workflows",
        "GitHub Pages publishing",
        "Renovate configuration",
        "Project-template config",
        "Template update Make target",
        "Automated release bundle publishing",
    ]:
        check(feature in template_automation_text, f"project-template automation report tracks optional feature: {feature}", errors)
    for target in ["build", "test", "reports", "preflight", "proof-only", "handoff"]:
        check(f"`{target}`" in template_automation_text, f"project-template automation report tracks local target: {target}", errors)
    check("https://googlefonts.github.io/gf-guide/upstream.html" in template_automation_text, "project-template automation report cites GF upstream guide", errors)
    check("https://googlefonts.github.io/gf-guide/qa.html" in template_automation_text, "project-template automation report cites GF QA guide", errors)
    check("https://googlefonts.github.io/gf-guide/tools.html" in template_automation_text, "project-template automation report cites GF tools guide", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in template_pr_text, "template and PR audit cites GF package guide", errors)
    check("https://github.com/googlefonts/googlefonts-project-template" in template_automation_text, "project-template automation report cites GF project template", errors)


def package_checklist_errors(errors: list[str]) -> None:
    text = (ROOT / "documentation/google-fonts-package-checklist.md").read_text()
    release_text = (ROOT / "documentation/google-fonts-release-checklist.md").read_text()
    handoff_text = (ROOT / "documentation/google-fonts-submission-handoff.md").read_text()
    arabic_report_text = (ROOT / "documentation/missing-gf-arabic-core.md").read_text()
    latin_report_text = (ROOT / "documentation/missing-gf-latin-core.md").read_text()
    fontspector_report_text = (ROOT / "documentation/fontspector-googlefonts-report.md").read_text()
    production_requirements_text = (ROOT / "documentation/google-fonts-production-requirements.md").read_text()
    generated_metadata_text = (ROOT / "documentation/generated-font-metadata.md").read_text()
    package_source_text = (ROOT / "documentation/package-source-files-audit.md").read_text()
    packager_source_strategy_text = (ROOT / "documentation/packager-source-strategy.md").read_text()
    release_archive_text = (ROOT / "documentation/release-archive-manifest.md").read_text()
    package_dry_run_text = (ROOT / "documentation/package-dry-run-readiness.md").read_text()
    local_workflow_text = (ROOT / "documentation/local-workflow-readiness.md").read_text()
    downstream_metadata_text = (ROOT / "documentation/downstream-metadata-readiness.md").read_text()
    downstream_metadata_diff_text = (ROOT / "documentation/downstream-metadata-diff.md").read_text()
    release_source_text = (ROOT / "documentation/release-source-readiness.md").read_text()
    upstream_structure_text = (ROOT / "documentation/upstream-structure-readiness.md").read_text()
    handoff_readiness_text = (ROOT / "documentation/submission-handoff-readiness.md").read_text()
    kerning_text = (ROOT / "documentation/kerning-readiness.md").read_text()
    kerning_proof_review_text = (ROOT / "documentation/kerning-proof-review.md").read_text()
    reference_index_text = (ROOT / "documentation/google-fonts-reference-index.md").read_text()
    decisions_text = (ROOT / "documentation/google-fonts-decisions.md").read_text()
    questions_text = (ROOT / "documentation/google-fonts-decision-questions.md").read_text()
    package_script_text = (ROOT / "scripts/package_gf_dry_run.sh").read_text()
    makefile_text = (ROOT / "Makefile").read_text()
    readme_text = (ROOT / "README.md").read_text()
    readiness_text = (ROOT / "GF_READINESS.md").read_text()
    core_qa_text = (ROOT / "documentation/core-qa-process.md").read_text()
    check("# Core QA Process" in core_qa_text, "core QA process document has expected heading", errors)
    for command in [
        "make build",
        "make test",
        "make kerning-proof-check",
        "make kerning-proof-review-check",
        "make proof",
        "make reports",
        "make designer-profile-validator-test",
        "make preflight",
        "make preflight-only",
        "make handoff",
        "make package-readiness-check",
        "GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check",
        "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
    ]:
        check(command in core_qa_text, f"core QA process documents command: {command}", errors)
    check("Fontspector is this repo's automated Google Fonts QA entrypoint" in core_qa_text, "core QA process records Fontspector policy", errors)
    check("FontBakery unless a Google Fonts reviewer asks" in core_qa_text, "core QA process records FontBakery legacy caveat", errors)
    check("`make kerning-proof-check` is a core QA step" in core_qa_text, "core QA process marks gftools proof as core QA", errors)
    check("make kerning-proof-review-check" in core_qa_text, "core QA process documents gftools proof review packet", errors)
    check("documentation/kerning-proof-review.md" in core_qa_text, "core QA process records gftools proof review packet path", errors)
    check("documentation/gftools-qa/" in core_qa_text, "core QA process records gftools proof output directory", errors)
    check(
        "https://fonts.google.com/metadata/fonts" in core_qa_text,
        "core QA process records gftools proof network dependency",
        errors,
    )
    check("GF_Arabic_Core" in core_qa_text, "core QA process records Arabic Core QA scope", errors)
    check("https://googlefonts.github.io/gf-guide/onboarder-workflow.html" in core_qa_text, "core QA process cites GF onboarder workflow", errors)
    check("https://googlefonts.github.io/gf-guide/qa.html" in core_qa_text, "core QA process cites GF QA guide", errors)
    check("https://googlefonts.github.io/gf-guide/testing.html" in core_qa_text, "core QA process cites GF local testing guide", errors)
    check("https://github.com/fonttools/fontspector" in core_qa_text, "core QA process cites Fontspector", errors)
    check("# Google Fonts Reference Index" in reference_index_text, "Google Fonts reference index has expected heading", errors)
    check("References tracked: 17" in reference_index_text, "Google Fonts reference index tracks expected reference count", errors)
    check("Official-doc references only: yes" in reference_index_text, "Google Fonts reference index records official-doc policy", errors)
    check("Google Fonts GitHub references included: yes" in reference_index_text, "Google Fonts reference index records GitHub reference coverage", errors)
    for expected in [
        "https://googlefonts.github.io/gf-guide/onboarding.html",
        "https://googlefonts.github.io/gf-guide/upstream.html",
        "https://googlefonts.github.io/gf-guide/requirements.html",
        "https://googlefonts.github.io/gf-guide/production.html",
        "https://googlefonts.github.io/gf-guide/variable.html",
        "https://googlefonts.github.io/gf-guide/build.html",
        "https://googlefonts.github.io/gf-guide/package.html",
        "https://googlefonts.github.io/gf-guide/metadata.html",
        "https://googlefonts.github.io/gf-guide/article.html",
        "https://googlefonts.github.io/gf-guide/lang.html",
        "https://googlefonts.github.io/gf-guide/making-pr.html",
        "https://googlefonts.github.io/gf-guide/tools.html",
        "https://googlefonts.github.io/gf-guide/onboarder-workflow.html",
        "https://googlefonts.github.io/gf-guide/googlefonts.html",
        "https://googlefonts.github.io/gf-guide/profile.html",
        "https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
        "https://github.com/googlefonts/gftools",
        "documentation/article-readiness.md",
        "documentation/arabic-review-packet.md",
        "documentation/google-fonts-language-metadata.md",
        "documentation/google-fonts-add-font-issue-draft.md",
        "documentation/package-dry-run-readiness.md",
        "documentation/designer-profile-package-draft.md",
        "documentation/kerning-proof-review.md",
    ]:
        check(expected in reference_index_text, f"Google Fonts reference index records {expected}", errors)
    check("documentation/core-qa-process.md" in readme_text, "README links core QA process document", errors)
    check("documentation/kerning-proof-review.md" in readme_text, "README links kerning proof review packet", errors)
    check("documentation/core-qa-process.md" in readiness_text, "GF_READINESS records core QA process document", errors)
    check("make designer-profile-prepare-check" in readiness_text, "GF_READINESS records designer profile prepare target", errors)
    check("scripts/prepare_designer_profile.py --apply" in readiness_text, "GF_READINESS records guarded designer profile apply helper", errors)
    check("gftools packager \"Virtua Grotesk\" path/to/local/google/fonts" in text, "package checklist uses current gftools packager local syntax", errors)
    check("gftools packager \"Virtua Grotesk\" path/to/local/google/fonts -p -i ISSUE_NUMBER" in text, "package checklist uses current gftools packager PR syntax", errors)
    check("-i/--issue-number" in text, "package checklist documents issue-number flag", errors)
    check("--latest-release" in text, "package checklist documents latest-release packager mode", errors)
    check("--build-from-source" in text, "package checklist documents build-from-source packager mode", errors)
    check(
        'GH_TOKEN="$(gh auth token)" GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run' in text,
        "package checklist keeps explicit token example on selected latest-release source mode",
        errors,
    )
    check(
        "aligned to both cached" in text and "`upstream/main`" in text and "`origin/main`" in text,
        "package checklist documents google/fonts fork alignment requirement",
        errors,
    )
    check("make package-dry-run" in readme_text, "README documents package dry-run command", errors)
    check("make package-wrapper-test" in readme_text, "README documents package wrapper metadata gate test command", errors)
    check("/Users/eli/GH/forks/fonts" in readme_text, "README documents default google/fonts fork path", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in readme_text, "README documents latest-release dry-run mode", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run" in readme_text, "README documents build-from-source dry-run mode", errors)
    check(
        "GFT_PACKAGER_SOURCE_MODE=latest-release make package-readiness-check" in readme_text
        and "GFT_PACKAGER_SOURCE_MODE=build-from-source make package-readiness-check" in readme_text,
        "README documents package readiness source-mode examples",
        errors,
    )
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check" in readme_text, "README documents latest-release downstream metadata check mode", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source make downstream-metadata-check" in readme_text, "README documents build-from-source downstream metadata check mode", errors)
    check("source.archive_url" in readme_text, "README documents latest-release archive_url wrapper gate", errors)
    check("GitHub release download `.zip` `archive_url`" in readme_text, "README documents latest-release archive_url shape", errors)
    check("sample_text" in readme_text, "README documents review-gated optional field wrapper gate", errors)
    check("Vendor ID readiness report" in readme_text, "README includes Vendor ID report in reports list", errors)
    check("public upstream URL readiness report" in readme_text, "README includes public upstream URL report in reports list", errors)
    check(
        "release/source" in readme_text and "readiness report" in readme_text,
        "README includes release/source readiness report in reports list",
        errors,
    )
    check("upstream structure readiness report" in readme_text, "README includes upstream structure readiness report in reports list", errors)
    check("decision readiness report" in readme_text, "README includes decision readiness report in reports list", errors)
    check(
        "Google Fonts language-metadata" in readme_text and "audit" in readme_text,
        "README includes language metadata report in reports list",
        errors,
    )
    check(
        "final-submission blocker" in readme_text and "summary" in readme_text,
        "README includes final blocker report in reports list",
        errors,
    )
    check("package dry-run readiness report" in readme_text, "README includes package dry-run readiness report in reports list", errors)
    check(
        "submission" in readme_text
        and "handoff readiness report" in readme_text,
        "README includes submission handoff readiness report in reports list",
        errors,
    )
    check("local workflow readiness report" in readme_text, "README includes local workflow readiness report in reports list", errors)
    check("owner-grouped next-action" in readme_text, "README includes owner-grouped next-action report in reports list", errors)
    check("make decision-readiness-check" in readme_text, "README documents decision readiness check target", errors)
    check("make next-actions" in readme_text, "README documents next-actions target", errors)
    check("make blockers" in readme_text, "README documents final-submission blocker target", errors)
    check("make issue-draft" in readme_text, "README documents Add Font issue draft target", errors)
    check("make handoff-readiness-check" in readme_text, "README documents handoff readiness check target", errors)
    check("make release-check" in readme_text, "README documents release readiness check target", errors)
    check("make release-archive-check" in readme_text, "README documents release archive manifest target", errors)
    check("make release-archive-build" in readme_text, "README documents release archive build target", errors)
    check("make release-archive-verify" in readme_text, "README documents release archive verify target", errors)
    check("make release-archive-test" in readme_text, "README documents release archive path-safety test target", errors)
    check("make release-draft-check" in readme_text, "README documents GitHub release draft target", errors)
    check("make source-strategy-check" in readme_text, "README documents release/source strategy check target", errors)
    check("make package-readiness-check" in readme_text, "README documents packaging readiness check target", errors)
    check("make recent-gf-check" in readme_text, "README documents recent GF comparison check target", errors)
    check("make family-name-check" in readme_text, "README documents family-name readiness check target", errors)
    check("make authorship-check" in readme_text, "README documents authorship readiness check target", errors)
    check("make pr-readiness-check" in readme_text, "README documents downstream PR readiness check target", errors)
    check("make vendor-id-check" in readme_text, "README documents vendor ID readiness check target", errors)
    check("make kerning-check" in readme_text, "README documents kerning readiness check target", errors)
    check("make kerning-proof-check" in readme_text, "README documents gftools QA kerning proof target", errors)
    check(
        "Treat this as a core QA step" in readme_text
        and "HTML proof in `documentation/gftools-qa/`" in readme_text,
        "README marks gftools QA proof review as core QA",
        errors,
    )
    check("make pua-scope-check" in readme_text, "README documents PUA scope check target", errors)
    check("make avar-check" in readme_text, "README documents avar readiness check target", errors)
    check("make warnings-check" in readme_text, "README documents Fontspector warning triage target", errors)
    check("make github-auth-check" in readme_text, "README documents GitHub API auth check target", errors)
    check("make designer-profile-check" in readme_text, "README documents designer profile check target", errors)
    check("make designer-profile-prepare-check" in readme_text, "README documents designer profile prepare dry-run target", errors)
    check("make designer-profile-info-check INFO=path/to/info.pb" in readme_text, "README documents designer profile info.pb check target", errors)
    check("make designer-profile-image-check IMAGE=path/to/eliheuer.png" in readme_text, "README documents designer profile image check target", errors)
    check("make designer-profile-bio-check BIO=path/to/bio.html" in readme_text, "README documents designer profile bio check target", errors)
    check("make designer-profile-validator-test" in readme_text, "README documents designer profile validator test target", errors)
    check("make public-upstream-url-check" in readme_text, "README documents public upstream URL replacement preview target", errors)
    check(
        "The canonical public URL is `https://github.com/eliheuer/virtua-grotesk`" in readme_text,
        "README records decided public upstream URL",
        errors,
    )
    check(
        "scripts/apply_public_upstream_url.py --url https://github.com/eliheuer/virtua-grotesk --apply" in readme_text,
        "README documents explicit decided public upstream URL apply command",
        errors,
    )
    check(
        "scripts/apply_public_upstream_url.py --url https://github.com/owner/repo --apply" not in readme_text,
        "README avoids generic owner/repo public URL command after URL decision",
        errors,
    )
    check("make downstream-metadata-check" in readme_text, "README documents downstream metadata check target", errors)
    check("scripts/prepare_downstream_metadata.py --apply" in readme_text, "README documents explicit downstream metadata apply command", errors)
    check("consolidated Arabic review packet" in readme_text, "README includes Arabic review packet in reports list", errors)
    check("documentation/local-workflow-readiness.md" in text, "package checklist includes local workflow readiness report", errors)
    check("# Local Workflow Readiness" in local_workflow_text, "local workflow readiness report has expected heading", errors)
    check("| `family-name-check` | yes |" in local_workflow_text, "local workflow readiness report tracks family-name check target", errors)
    check("| `authorship-check` | yes |" in local_workflow_text, "local workflow readiness report tracks authorship check target", errors)
    check("| `vendor-id-check` | yes |" in local_workflow_text, "local workflow readiness report tracks vendor ID check target", errors)
    check("| `kerning-check` | yes |" in local_workflow_text, "local workflow readiness report tracks kerning check target", errors)
    check("| `kerning-proof-check` | yes |" in local_workflow_text, "local workflow readiness report tracks kerning proof check target", errors)
    check("| `kerning-proof-review-check` | yes |" in local_workflow_text, "local workflow readiness report tracks kerning proof review target", errors)
    check("| `pua-scope-check` | yes |" in local_workflow_text, "local workflow readiness report tracks PUA scope check target", errors)
    check("| `avar-check` | yes |" in local_workflow_text, "local workflow readiness report tracks avar check target", errors)
    check("| `warnings-check` | yes |" in local_workflow_text, "local workflow readiness report tracks warning triage target", errors)
    check("| `designer-profile-info-check` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile info.pb check target", errors)
    check("| `designer-profile-image-check` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile image check target", errors)
    check("| `designer-profile-bio-check` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile bio check target", errors)
    check("| `designer-profile-validator-test` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile validator test target", errors)
    check("Local preflight command ready to run: yes" in local_workflow_text, "local workflow readiness report confirms preflight command prerequisites", errors)
    check("requirements.in direct dependencies expected: yes" in local_workflow_text, "local workflow readiness report confirms expected direct requirements", errors)
    check("requirements.in direct dependencies: 7" in local_workflow_text, "local workflow readiness report records direct requirement count", errors)
    check("requirements.txt pinned packages: " in local_workflow_text, "local workflow readiness report records pinned package count", errors)
    check("requirements.txt fully pinned: yes" in local_workflow_text, "local workflow readiness report confirms pinned requirements snapshot", errors)
    check("requirements.txt includes transitive dependencies: yes" in local_workflow_text, "local workflow readiness report confirms transitive requirements are captured", errors)
    check("requirements.txt includes direct dependency package names: yes" in local_workflow_text, "local workflow readiness report confirms direct requirements are represented", errors)
    check("requirements.in directly includes FontBakery: no" in local_workflow_text, "local workflow readiness report confirms FontBakery is not a direct dependency", errors)
    check("requirements.txt includes FontBakery transitively: yes" in local_workflow_text, "local workflow readiness report explains transitive FontBakery pin", errors)
    check("Automated QA entrypoint remains Fontspector: yes" in local_workflow_text, "local workflow readiness report confirms Fontspector remains QA entrypoint", errors)
    check("Transitive FontBakery pin from `gftools[qa]`: yes" in local_workflow_text, "local workflow requirements section records FontBakery transitive source", errors)
    check("Fontspector command available: yes" in local_workflow_text, "local workflow readiness report confirms Fontspector command availability", errors)
    check("Fontspector command path: `" in local_workflow_text, "local workflow readiness report records Fontspector command path", errors)
    check("Fontspector version: `fontspector " in local_workflow_text, "local workflow readiness report records Fontspector version", errors)
    check("Fontspector home exists: yes" in local_workflow_text, "local workflow readiness report confirms ~/.fontspector exists", errors)
    check("Fontspector local templates ready: yes" in local_workflow_text, "local workflow readiness report confirms local Fontspector templates", errors)
    check("DrawBot fork runtime ready: yes" in local_workflow_text, "local workflow readiness report confirms DrawBot fork runtime", errors)
    check("Proof PDF artifact present: yes" in local_workflow_text, "local workflow readiness report confirms proof PDF artifact exists", errors)
    check("gftools QA proof tooling ready: yes" in local_workflow_text, "local workflow readiness report confirms gftools QA proof tooling", errors)
    check("gftools QA proof output present: yes" in local_workflow_text, "local workflow readiness report confirms gftools QA proof output", errors)
    check("gftools QA proof covers expected instances: yes" in local_workflow_text, "local workflow readiness report confirms gftools QA proof instance coverage", errors)
    check(
        re.search(r"Proof PDF page count: [1-9]\d*", local_workflow_text) is not None,
        "local workflow readiness report records nonzero proof PDF page count",
        errors,
    )
    check("## Proof Artifact" in local_workflow_text and "Render command: `make proof-only`" in local_workflow_text, "local workflow readiness report records proof artifact command", errors)
    check("## Google Fonts QA Proof Artifact" in local_workflow_text and "Render command: `make kerning-proof-check`" in local_workflow_text, "local workflow readiness report records gftools QA proof artifact command", errors)
    check("Local google/fonts fork ready: yes" in local_workflow_text, "local workflow readiness report confirms google/fonts fork", errors)
    check("Local google/fonts tracking branch: `origin/main`" in local_workflow_text, "local workflow readiness report records google/fonts tracking branch", errors)
    check("Local google/fonts main vs origin/main: 0 ahead, 0 behind" in local_workflow_text, "local workflow readiness report records origin/main alignment", errors)
    check("Local google/fonts main vs upstream/main: 0 ahead, 0 behind" in local_workflow_text, "local workflow readiness report records upstream/main alignment", errors)
    check("Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0" in local_workflow_text, "local workflow readiness report records no unrelated google/fonts dirtiness", errors)
    check(
        re.search(r"GitHub API credentials ready: (yes|no)", local_workflow_text) is not None,
        "local workflow readiness report records current GitHub auth state",
        errors,
    )
    package_report_reaches = re.search(r"Wrapper can reach Packager: (yes|no)", package_dry_run_text)
    package_report_first_blocker = re.search(r"First blocker: ([^\n]+)", package_dry_run_text)
    package_report_blocking_findings = re.search(r"Blocking findings: ([^\n]+)", package_dry_run_text)
    check(
        package_report_reaches is not None
        and f"Package dry-run report says wrapper can reach Packager: {package_report_reaches.group(1)}" in local_workflow_text,
        "local workflow readiness report mirrors package dry-run reachability",
        errors,
    )
    check(
        package_report_first_blocker is not None
        and f"Package dry-run first blocker: {package_report_first_blocker.group(1)}" in local_workflow_text,
        "local workflow readiness report mirrors package dry-run first blocker",
        errors,
    )
    check(
        package_report_blocking_findings is not None
        and f"Package dry-run blocking findings: {package_report_blocking_findings.group(1)}" in local_workflow_text,
        "local workflow readiness report mirrors all package dry-run blockers",
        errors,
    )
    check("Command safety gates ready: yes" in local_workflow_text, "local workflow readiness report confirms command safety gates", errors)
    check("## Command Safety Gates" in local_workflow_text, "local workflow readiness report includes command safety gate table", errors)
    check("## Python Requirements Snapshot" in local_workflow_text, "local workflow readiness report includes Python requirements snapshot section", errors)
    check("Refresh command: `./venv/bin/python -m pip freeze --all > requirements.txt`" in local_workflow_text, "local workflow readiness report documents pinned requirements refresh command", errors)
    for direct_requirement in [
        "GitPython",
        "PyYAML",
        "fontmake",
        "fonttools",
        "gftools[qa]",
        "glyphsets",
        "uharfbuzz",
    ]:
        check(
            f"| `{direct_requirement}` | yes |" in local_workflow_text,
            f"local workflow readiness report confirms pinned snapshot includes {direct_requirement}",
            errors,
        )
    for safety_gate in [
        "| GF_REPO_PATH defaults to local google/fonts fork | yes |",
        "| package-dry-run target invokes local wrapper | yes |",
        "| package-dry-run target omits PR creation flags | yes |",
        "| package-dry-run wrapper does not add PR creation flags | yes |",
        "| downstream-metadata-check target is preview-only | yes |",
        "| downstream metadata apply remains explicit | yes |",
        "| Packager source mode is surfaced | yes |",
        "| package wrapper metadata gates have a local test | yes |",
        "| downstream metadata helper final-value gates have a local test | yes |",
        "| designer profile validators and prepare helper have a local test | yes |",
        "| release archive path-safety gates have a local test | yes |",
        "| proof target uses eliheuer/drawbot-skia fork | yes |",
    ]:
        check(
            safety_gate in local_workflow_text,
            f"local workflow readiness report passes command safety gate: {safety_gate}",
            errors,
        )
    check("| `next-actions` | yes |" in local_workflow_text, "local workflow readiness report tracks next-actions target", errors)
    check("| `blockers` | yes |" in local_workflow_text, "local workflow readiness report tracks final-submission blocker target", errors)
    check("| `issue-draft` | yes |" in local_workflow_text, "local workflow readiness report tracks Add Font issue draft target", errors)
    check("| `handoff-readiness-check` | yes |" in local_workflow_text, "local workflow readiness report tracks handoff readiness check target", errors)
    check("| `release-check` | yes |" in local_workflow_text, "local workflow readiness report tracks release check target", errors)
    check("| `release-archive-check` | yes |" in local_workflow_text, "local workflow readiness report tracks release archive check target", errors)
    check("| `release-archive-build` | yes |" in local_workflow_text, "local workflow readiness report tracks release archive build target", errors)
    check("| `release-archive-verify` | yes |" in local_workflow_text, "local workflow readiness report tracks release archive verify target", errors)
    check("| `release-archive-test` | yes |" in local_workflow_text, "local workflow readiness report tracks release archive test target", errors)
    check("| `release-draft-check` | yes |" in local_workflow_text, "local workflow readiness report tracks release draft target", errors)
    check("| `source-strategy-check` | yes |" in local_workflow_text, "local workflow readiness report tracks release/source strategy check target", errors)
    check("| `package-readiness-check` | yes |" in local_workflow_text, "local workflow readiness report tracks package readiness check target", errors)
    check("| `recent-gf-check` | yes |" in local_workflow_text, "local workflow readiness report tracks recent GF comparison target", errors)
    check("| `pr-readiness-check` | yes |" in local_workflow_text, "local workflow readiness report tracks downstream PR readiness check target", errors)
    check("| `github-auth-check` | yes |" in local_workflow_text, "local workflow readiness report tracks GitHub API auth check target", errors)
    check("| `designer-profile-check` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile check target", errors)
    check("| `designer-profile-prepare-check` | yes |" in local_workflow_text, "local workflow readiness report tracks designer profile prepare target", errors)
    check("| `public-upstream-url-check` | yes |" in local_workflow_text, "local workflow readiness report tracks public upstream URL target", errors)
    check("| `downstream-metadata-check` | yes |" in local_workflow_text, "local workflow readiness report tracks downstream metadata check target", errors)
    check("| `downstream-metadata-helper-test` | yes |" in local_workflow_text, "local workflow readiness report tracks downstream metadata helper test target", errors)
    check("| `package-wrapper-test` | yes |" in local_workflow_text, "local workflow readiness report tracks package wrapper test target", errors)
    check("| `decision-readiness-check` | yes |" in local_workflow_text, "local workflow readiness report tracks decision readiness check target", errors)
    check("documentation/next-actions.md" in local_workflow_text, "local workflow readiness report includes next-actions report", errors)
    check(
        "Package report auth ready: no" in local_workflow_text or "Package report auth ready: yes" in local_workflow_text,
        "local workflow readiness report mirrors package dry-run auth state",
        errors,
    )
    check(
        "Review `documentation/package-dry-run-readiness.md` before running `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`." in local_workflow_text,
        "local workflow readiness report uses selected latest-release package command in next action",
        errors,
    )
    check("GFT_PACKAGER_SOURCE_MODE=latest-release" in readiness_text, "readiness notes document latest-release dry-run mode", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source" in readiness_text, "readiness notes document build-from-source dry-run mode", errors)
    check("make handoff-readiness-check" in readiness_text, "readiness notes document handoff readiness check target", errors)
    check("make decision-readiness-check" in readiness_text, "readiness notes document decision readiness check target", errors)
    check("make release-check" in readiness_text, "readiness notes document release check target", errors)
    check("make release-draft-check" in readiness_text, "readiness notes document GitHub release draft target", errors)
    check("make pr-readiness-check" in readiness_text, "readiness notes document downstream PR readiness check target", errors)
    check("make package-readiness-check" in readiness_text, "readiness notes document packaging readiness check target", errors)
    check("make recent-gf-check" in readiness_text, "readiness notes document recent GF comparison check target", errors)
    check("make downstream-metadata-check" in readiness_text, "readiness notes document downstream metadata check target", errors)
    check("make downstream-metadata-helper-test" in readiness_text, "readiness notes document downstream metadata helper test target", errors)
    check("make package-wrapper-test" in readiness_text, "readiness notes document package wrapper metadata gate test target", errors)
    check("make release-archive-test" in readiness_text, "readiness notes document release archive path-safety test target", errors)
    check(
        "Author/contact display is decided as `Eli Heuer`" in readiness_text
        and "unless Google Fonts asks for\n  contact-formatted lines" in readiness_text,
        "readiness notes record decided author/contact display handling",
        errors,
    )
    check(
        "Confirm author email/contact formatting" not in readiness_text,
        "readiness notes avoid stale author/contact open-decision wording",
        errors,
    )
    check(
        "identity `avar` table, and resolved warning" in readiness_text,
        "readiness notes record resolved avar warning review",
        errors,
    )
    check(
        "mapping and open maintainer decision" not in readiness_text,
        "readiness notes avoid stale avar open-decision wording",
        errors,
    )
    check(
        "Use the same `GFT_PACKAGER_SOURCE_MODE` with `make package-readiness-check`" in readiness_text,
        "readiness notes document package readiness source-mode alignment",
        errors,
    )
    check(
        "`source.config_yaml`, release/archive metadata, and the no-PR Packager pass\n  are reviewed in the same source mode" in readiness_text,
        "readiness notes document source-mode-aware metadata validation",
        errors,
    )
    check(
        "Packager wrapper gate tests for source-mode metadata blockers" in readiness_text,
        "readiness notes document package wrapper metadata gate coverage",
        errors,
    )
    check("the decided upstream URL" in readiness_text, "readiness notes describe Article URL state as decided", errors)
    check(
        "the remaining placeholder upstream URL" not in readiness_text,
        "readiness notes avoid stale Article placeholder URL wording",
        errors,
    )
    check(
        "Rerun `make preflight` so proof evidence and generated reports\n"
        "  stay synchronized, then run\n"
        "  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`" in release_source_text,
        "release/source readiness report uses synchronized preflight before Packager",
        errors,
    )
    check("upstream/main" in readme_text and "upstream/main" in readiness_text, "human docs record google/fonts fork alignment requirement", errors)
    check("GF_REPO_PATH ?= /Users/eli/GH/forks/fonts" in makefile_text, "Makefile has default google/fonts fork path", errors)
    check("decision-readiness-check" in makefile_text, "Makefile exposes decision readiness check target", errors)
    check("report_decision_readiness.py" in makefile_text, "Makefile wires decision readiness report", errors)
    check("blockers" in makefile_text, "Makefile exposes final-submission blocker target", errors)
    check("issue-draft" in makefile_text, "Makefile exposes Add Font issue draft target", errors)
    check("handoff-readiness-check" in makefile_text, "Makefile exposes handoff readiness check target", errors)
    check("report_submission_handoff_readiness.py" in makefile_text, "Makefile wires submission handoff readiness report", errors)
    check("report_final_submission_blockers.py" in makefile_text, "Makefile wires final-submission blocker report", errors)
    check("report_next_actions.py" in makefile_text, "Makefile wires next-actions report", errors)
    check("release-check" in makefile_text, "Makefile exposes release readiness check target", errors)
    check("report_release_metadata.py" in makefile_text, "Makefile wires release metadata report", errors)
    check("report_release_source_readiness.py" in makefile_text, "Makefile wires release/source readiness report", errors)
    check("release-draft-check" in makefile_text, "Makefile exposes GitHub release draft target", errors)
    check("report_github_release_draft.py" in makefile_text, "Makefile wires GitHub release draft report", errors)
    check("source-strategy-check" in makefile_text, "Makefile exposes release/source strategy check target", errors)
    check("package-readiness-check" in makefile_text, "Makefile exposes packaging readiness check target", errors)
    check("recent-gf-check" in makefile_text, "Makefile exposes recent GF comparison check target", errors)
    check("reference-index-check" in makefile_text, "Makefile exposes Google Fonts reference index target", errors)
    check("report_gf_reference_index.py" in makefile_text, "Makefile wires Google Fonts reference index report", errors)
    check("report_recent_gf_packages.py" in makefile_text, "Makefile wires recent GF comparison report", errors)
    check("report_package_dry_run_readiness.py" in makefile_text, "Makefile wires package dry-run readiness report", errors)
    check("report_downstream_pr_readiness.py" in makefile_text, "Makefile wires downstream PR readiness report", errors)
    check("family-name-check" in makefile_text, "Makefile exposes family-name readiness check target", errors)
    check("report_family_name_readiness.py" in makefile_text, "Makefile wires family-name readiness report", errors)
    check("authorship-check" in makefile_text, "Makefile exposes authorship readiness check target", errors)
    check("report_authorship_disclosure_readiness.py" in makefile_text, "Makefile wires authorship readiness report", errors)
    check("pr-readiness-check" in makefile_text, "Makefile exposes downstream PR readiness check target", errors)
    check("report_pr_identity_readiness.py" in makefile_text, "Makefile wires PR identity readiness report", errors)
    check("report_downstream_pr_readiness.py" in makefile_text, "Makefile wires downstream PR readiness report", errors)
    check("vendor-id-check" in makefile_text, "Makefile exposes vendor ID readiness check target", errors)
    check("report_vendor_id_readiness.py" in makefile_text, "Makefile wires vendor ID readiness report", errors)
    check("kerning-check" in makefile_text, "Makefile exposes kerning readiness check target", errors)
    check("report_kerning_readiness.py" in makefile_text, "Makefile wires kerning readiness report", errors)
    check("kerning-proof-check" in makefile_text, "Makefile exposes kerning proof check target", errors)
    check("kerning-proof-review-check" in makefile_text, "Makefile exposes kerning proof review target", errors)
    check("report_kerning_proof_review.py" in makefile_text, "Makefile wires kerning proof review report", errors)
    check("gftools qa --proof" in makefile_text, "Makefile wires kerning proof target to gftools qa", errors)
    check("report_arabic_visual_risk.py" in makefile_text, "Makefile wires Arabic visual risk audit report", errors)
    check("documentation/arabic-visual-risk-audit.md" in makefile_text, "Makefile wires Arabic visual risk audit output", errors)
    check("arabic-visual-risk-proof" in makefile_text, "Makefile exposes Arabic visual risk proof target", errors)
    check("build_arabic_visual_risk_proof.py" in makefile_text, "Makefile wires Arabic visual risk proof builder", errors)
    check("documentation/arabic-visual-risk-proof.html" in makefile_text, "Makefile wires Arabic visual risk proof output", errors)
    check("arabic-structure-sweep" in makefile_text, "Makefile exposes Arabic structure sweep target", errors)
    check("build_arabic_structure_sweep.py" in makefile_text, "Makefile wires Arabic structure sweep builder", errors)
    check("documentation/arabic-structure-sweep.html" in makefile_text, "Makefile wires Arabic structure sweep output", errors)
    check("arabic-structure-triage" in makefile_text, "Makefile exposes Arabic structure triage target", errors)
    check("report_arabic_structure_triage.py" in makefile_text, "Makefile wires Arabic structure triage report", errors)
    check("documentation/arabic-structure-triage.md" in makefile_text, "Makefile wires Arabic structure triage output", errors)
    check("arabic-mark-review-proof" in makefile_text, "Makefile exposes Arabic mark review proof target", errors)
    check("build_arabic_mark_review_proof.py" in makefile_text, "Makefile wires Arabic mark review proof builder", errors)
    check("documentation/arabic-mark-review-proof.html" in makefile_text, "Makefile wires Arabic mark review proof output", errors)
    check("arabic-mark-triage" in makefile_text, "Makefile exposes Arabic mark triage target", errors)
    check("report_arabic_mark_triage.py" in makefile_text, "Makefile wires Arabic mark triage report", errors)
    check("documentation/arabic-mark-triage.md" in makefile_text, "Makefile wires Arabic mark triage output", errors)
    check("arabic-manual-review-dashboard" in makefile_text, "Makefile exposes Arabic manual review dashboard target", errors)
    check("build_arabic_manual_review_dashboard.py" in makefile_text, "Makefile wires Arabic manual review dashboard builder", errors)
    check("documentation/arabic-manual-review-dashboard.html" in makefile_text, "Makefile wires Arabic manual review dashboard output", errors)
    check("arabic-manual-review-batches" in makefile_text, "Makefile exposes Arabic manual review batches target", errors)
    check("report_arabic_manual_review_batches.py" in makefile_text, "Makefile wires Arabic manual review batches report", errors)
    check("documentation/arabic-manual-review-batches.md" in makefile_text, "Makefile wires Arabic manual review batches output", errors)
    check("arabic-current-review-worksheet" in makefile_text, "Makefile exposes Arabic current review worksheet target", errors)
    check("report_arabic_current_review_worksheet.py" in makefile_text, "Makefile wires Arabic current review worksheet report", errors)
    check("documentation/arabic-current-review-worksheet.md" in makefile_text, "Makefile wires Arabic current review worksheet output", errors)
    check("arabic-review-worksheet-bundle" in makefile_text, "Makefile exposes Arabic review worksheet bundle target", errors)
    check("report_arabic_review_worksheet_bundle.py" in makefile_text, "Makefile wires Arabic review worksheet bundle report", errors)
    check("documentation/arabic-review-worksheet-bundle.md" in makefile_text, "Makefile wires Arabic review worksheet bundle output", errors)
    check("arabic-batch-recorder" in makefile_text, "Makefile exposes Arabic batch recorder target", errors)
    check("report_arabic_batch_recorder.py" in makefile_text, "Makefile wires Arabic batch recorder report", errors)
    check("documentation/arabic-batch-recorder.md" in makefile_text, "Makefile wires Arabic batch recorder output", errors)
    check("arabic-first-review-zoom-snapshots" in makefile_text, "Makefile exposes Arabic first review zoom snapshot target", errors)
    check("build_arabic_first_review_zoom_snapshots.py" in makefile_text, "Makefile wires Arabic first review zoom snapshot builder", errors)
    check("documentation/arabic-first-review-zoom-snapshots.md" in makefile_text, "Makefile wires Arabic first review zoom snapshot output", errors)
    check("arabic-first-review-crop-integrity" in makefile_text, "Makefile exposes Arabic first review crop integrity target", errors)
    check("report_arabic_first_review_crop_integrity.py" in makefile_text, "Makefile wires Arabic first review crop integrity report", errors)
    check("documentation/arabic-first-review-crop-integrity.md" in makefile_text, "Makefile wires Arabic first review crop integrity output", errors)
    check("arabic-first-review-batch" in makefile_text, "Makefile exposes Arabic first review batch target", errors)
    check("report_arabic_first_review_batch.py" in makefile_text, "Makefile wires Arabic first review batch report", errors)
    check("documentation/arabic-first-review-batch.md" in makefile_text, "Makefile wires Arabic first review batch output", errors)
    check("arabic-first-review-risk-shortlist" in makefile_text, "Makefile exposes Arabic first review risk shortlist target", errors)
    check("report_arabic_first_review_risk_shortlist.py" in makefile_text, "Makefile wires Arabic first review risk shortlist report", errors)
    check("documentation/arabic-first-review-risk-shortlist.md" in makefile_text, "Makefile wires Arabic first review risk shortlist output", errors)
    check("arabic-manual-edit-targets" in makefile_text, "Makefile exposes Arabic manual edit-target report", errors)
    check("report_arabic_manual_edit_targets.py" in makefile_text, "Makefile wires Arabic manual edit-target report", errors)
    check("documentation/arabic-manual-edit-targets.md" in makefile_text, "Makefile wires Arabic manual edit-target output", errors)
    check("arabic-hand-review-session" in makefile_text, "Makefile exposes Arabic hand-review session report", errors)
    check("report_arabic_hand_review_session.py" in makefile_text, "Makefile wires Arabic hand-review session report", errors)
    check("documentation/arabic-hand-review-session.md" in makefile_text, "Makefile wires Arabic hand-review session output", errors)
    check("arabic-hand-review-contact-sheet" in makefile_text, "Makefile exposes Arabic hand-review contact sheet", errors)
    check("build_arabic_hand_review_contact_sheet.py" in makefile_text, "Makefile wires Arabic hand-review contact sheet builder", errors)
    check("documentation/arabic-hand-review-contact-sheet.html" in makefile_text, "Makefile wires Arabic hand-review contact sheet output", errors)
    check("arabic-next-review-packet" in makefile_text, "Makefile exposes Arabic next review packet target", errors)
    check("report_arabic_next_review_packet.py" in makefile_text, "Makefile wires Arabic next review packet report", errors)
    check("documentation/arabic-next-review-packet.md" in makefile_text, "Makefile wires Arabic next review packet output", errors)
    check("arabic-next-review-ai-triage" in makefile_text, "Makefile exposes Arabic next review AI triage target", errors)
    check("report_arabic_next_review_ai_triage.py" in makefile_text, "Makefile wires Arabic next review AI triage report", errors)
    check("documentation/arabic-next-review-ai-triage.md" in makefile_text, "Makefile wires Arabic next review AI triage output", errors)
    check("arabic-next-review-ai-observations" in makefile_text, "Makefile exposes Arabic next review AI observations target", errors)
    check("report_arabic_next_review_ai_observations.py" in makefile_text, "Makefile wires Arabic next review AI observations report", errors)
    check("documentation/arabic-next-review-ai-observations.md" in makefile_text, "Makefile wires Arabic next review AI observations output", errors)
    check("arabic-full-queue-ai-sweep" in makefile_text, "Makefile exposes Arabic full queue AI sweep target", errors)
    check("report_arabic_full_queue_ai_sweep.py" in makefile_text, "Makefile wires Arabic full queue AI sweep report", errors)
    check("documentation/arabic-full-queue-ai-sweep.md" in makefile_text, "Makefile wires Arabic full queue AI sweep output", errors)
    check("arabic-next-review-board" in makefile_text, "Makefile exposes Arabic next review board target", errors)
    check("build_arabic_next_review_board.py" in makefile_text, "Makefile wires Arabic next review board builder", errors)
    check("documentation/arabic-next-review-board.html" in makefile_text, "Makefile wires Arabic next review board output", errors)
    check("arabic-next-review-snapshots" in makefile_text, "Makefile exposes Arabic next review snapshots target", errors)
    check("build_arabic_next_review_snapshots.py" in makefile_text, "Makefile wires Arabic next review snapshots builder", errors)
    check("ARABIC_SNAPSHOT_ARGS" in makefile_text, "Makefile allows optional Arabic snapshot args", errors)
    check("--list-only" in makefile_text, "Makefile documents non-GUI Arabic snapshot coverage check", errors)
    check("--timeout 20" in makefile_text, "Makefile documents bounded Arabic snapshot rendering", errors)
    check("--reuse-existing" in makefile_text, "Makefile documents existing-PNG Arabic snapshot report rebuild", errors)
    check("arabic-snapshot-integrity" in makefile_text, "Makefile exposes Arabic snapshot integrity target", errors)
    check("report_arabic_snapshot_integrity.py" in makefile_text, "Makefile wires Arabic snapshot integrity report", errors)
    check("documentation/arabic-snapshot-integrity.md" in makefile_text, "Makefile wires Arabic snapshot integrity output", errors)
    check("arabic-visual-review-runbook" in makefile_text, "Makefile exposes Arabic visual review runbook target", errors)
    check("report_arabic_visual_review_runbook.py" in makefile_text, "Makefile wires Arabic visual review runbook report", errors)
    check("documentation/arabic-visual-review-runbook.md" in makefile_text, "Makefile wires Arabic visual review runbook output", errors)
    check("arabic-visual-review-check" in makefile_text, "Makefile exposes Arabic visual review checklist target", errors)
    check("documentation/arabic-visual-review-checklist.md" in makefile_text, "Makefile wires Arabic visual review checklist", errors)
    check("arabic-visual-review-log" in makefile_text, "Makefile exposes Arabic visual review log target", errors)
    check("arabic-visual-review-update" in makefile_text, "Makefile exposes Arabic visual review update target", errors)
    check("update_arabic_visual_review.py" in makefile_text, "Makefile wires Arabic visual review update helper", errors)
    check("arabic-visual-review-helper-test" in makefile_text, "Makefile exposes Arabic visual review helper test target", errors)
    check("test_arabic_visual_review_update.sh" in makefile_text, "Makefile wires Arabic visual review helper test", errors)
    check("contour-decision-helper-test" in makefile_text, "Makefile exposes contour decision helper test target", errors)
    check("test_contour_decision_update.sh" in makefile_text, "Makefile wires contour decision helper test", errors)
    check("pua-scope-check" in makefile_text, "Makefile exposes PUA scope check target", errors)
    check("report_pua_scope.py" in makefile_text, "Makefile wires PUA scope report", errors)
    check("avar-check" in makefile_text, "Makefile exposes avar readiness check target", errors)
    check("report_avar_readiness.py" in makefile_text, "Makefile wires avar readiness report", errors)
    check("warnings-check" in makefile_text, "Makefile exposes Fontspector warning triage target", errors)
    check("report_fontspector_warnings.py" in makefile_text, "Makefile wires Fontspector warning report", errors)
    check("github-auth-check" in makefile_text, "Makefile exposes GitHub API auth check target", errors)
    check("designer-profile-check" in makefile_text, "Makefile exposes designer profile check target", errors)
    check("designer-profile-prepare-check" in makefile_text, "Makefile exposes designer profile prepare dry-run target", errors)
    check("designer-profile-info-check" in makefile_text, "Makefile exposes designer profile info.pb check target", errors)
    check("designer-profile-image-check" in makefile_text, "Makefile exposes designer profile image check target", errors)
    check("designer-profile-bio-check" in makefile_text, "Makefile exposes designer profile bio check target", errors)
    check("designer-profile-validator-test" in makefile_text, "Makefile exposes designer profile validator test target", errors)
    check("validate_designer_profile_info.py" in makefile_text, "Makefile wires designer profile info.pb validator", errors)
    check("validate_designer_profile_image.py" in makefile_text and "$(DESIGNER_PROFILE_AVATAR)" in makefile_text, "Makefile wires designer profile image validator with expected avatar filename", errors)
    check("validate_designer_profile_bio.py" in makefile_text, "Makefile wires designer profile bio validator", errors)
    check("prepare_designer_profile.py" in makefile_text, "Makefile wires designer profile prepare helper", errors)
    check("scripts/test_designer_profile_validators.sh" in makefile_text, "Makefile wires designer profile validator gate tests", errors)
    check("public-upstream-url-check" in makefile_text, "Makefile exposes public upstream URL replacement preview target", errors)
    check(
        "package-readiness-check:\n"
        "\t@$(PYTHON) scripts/report_package_source_files.py documentation/package-source-files-audit.md\n"
        "\t@$(PYTHON) scripts/report_packager_source_strategy.py documentation/packager-source-strategy.md\n"
        "\t@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_package_dry_run_readiness.py documentation/package-dry-run-readiness.md" in makefile_text,
        "Makefile package-readiness-check passes selected source mode into package dry-run readiness report",
        errors,
    )
    check(
        "\t@GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py documentation/downstream-metadata-diff.md" in makefile_text,
        "Makefile package-readiness-check passes selected source mode into downstream metadata diff report",
        errors,
    )
    check("GF_REPO_PATH='$(GF_REPO_PATH)' GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' ./scripts/package_gf_dry_run.sh" in makefile_text, "Makefile passes GF_REPO_PATH and selected source mode into package dry-run wrapper", errors)
    expected_preflight_order = (
        "preflight: build\n"
        "\t$(MAKE) proof-only\n"
        "\t$(MAKE) arabic-print-proof-only\n"
        "\t$(MAKE) reports-only\n"
        "\t$(MAKE) preflight-only"
    )
    check(expected_preflight_order in makefile_text, "Makefile preflight renders proofs before reports and local gate", errors)
    expected_handoff_order = (
        "handoff: build\n"
        "\t$(MAKE) proof-only\n"
        "\t$(MAKE) arabic-print-proof-only\n"
        "\t$(MAKE) reports-only\n"
        "\t$(MAKE) preflight-only"
    )
    check(expected_handoff_order in makefile_text, "Makefile handoff renders proofs before reports and preflight", errors)
    check(
        "writes the proof and focused Arabic PDF proof from that\n"
        "build, regenerates reports with the proof artifact evidence, then runs\n"
        "preflight" in readme_text
        or "writes the proof and focused Arabic PDF proof from that build,\n"
        "regenerates reports with the proof artifact evidence, then runs the local gate" in readme_text,
        "README documents synchronized proof-before-report order",
        errors,
    )
    check(
        "writes the proof and focused Arabic PDF proof from that build,\n"
        "regenerates reports with the proof artifact evidence, then runs the local gate" in readme_text,
        "README documents preflight proof-before-report order",
        errors,
    )
    check(
        "writes the proof and focused Arabic PDF proof from that\n"
        "build, regenerates reports with the proof artifact evidence, then runs\n"
        "preflight" in readme_text,
        "README documents handoff proof-before-report order",
        errors,
    )
    check(
        "regenerates the main proof PDF, the focused Arabic PDF proof, and reports" in (ROOT / "documentation/core-qa-process.md").read_text(),
        "core QA process documents synchronized Arabic PDF proof preflight",
        errors,
    )
    check(
        "make arabic-print-proof" in readme_text,
        "README documents standalone Arabic print proof target",
        errors,
    )
    check(
        "make arabic-print-proof" in (ROOT / "AGENTS.md").read_text(),
        "AGENTS documents standalone Arabic print proof target",
        errors,
    )
    check(
        "arabic-print-proof-only" in makefile_text,
        "Makefile exposes Arabic print proof-only target",
        errors,
    )
    check(
        "scripts/build_arabic_print_proof.py" in makefile_text,
        "Makefile wires Arabic print proof builder",
        errors,
    )
    check(
        "documentation/arabic-print-proof.pdf" in readme_text
        and "documentation/arabic-print-proof.pdf" in (ROOT / "AGENTS.md").read_text(),
        "human and agent docs record Arabic print proof output",
        errors,
    )
    check(
        "documentation/arabic-print-proof-index.md" in readme_text
        and "documentation/arabic-print-proof-index.md" in (ROOT / "AGENTS.md").read_text(),
        "human and agent docs record Arabic print proof index output",
        errors,
    )
    check(
        "documentation/arabic-print-proof.pdf" in (ROOT / "documentation/arabic-visual-review-checklist.md").read_text(),
        "Arabic visual review checklist records Arabic print proof output",
        errors,
    )
    check(
        "documentation/arabic-print-proof-index.md" in (ROOT / "documentation/arabic-visual-review-checklist.md").read_text(),
        "Arabic visual review checklist records Arabic print proof index output",
        errors,
    )
    check(
        "documentation/arabic-print-proof.pdf" in (ROOT / "documentation/arabic-goal-completion-audit.md").read_text(),
        "Arabic goal audit records Arabic print proof evidence",
        errors,
    )
    check(
        "Arabic PDF proof ready: yes" in (ROOT / "documentation/arabic-goal-completion-audit.md").read_text(),
        "Arabic goal audit confirms Arabic print proof readiness",
        errors,
    )
    check(
        "session links PDF: yes" in (ROOT / "documentation/arabic-goal-completion-audit.md").read_text()
        and "contact sheet links PDF: yes" in (ROOT / "documentation/arabic-goal-completion-audit.md").read_text(),
        "Arabic goal audit confirms review aids link Arabic print proof",
        errors,
    )
    check(
        "PYTHONPATH=\"$(DRAWBOT_SKIA_REPO)/src" in makefile_text
        and "scripts/build_arabic_print_proof.py" in makefile_text,
        "Arabic print proof uses drawbot-skia PYTHONPATH runtime",
        errors,
    )
    check(
        "Wrote {output_path}" not in (ROOT / "scripts/build_arabic_print_proof.py").read_text()
        or "drawbot_skia" in (ROOT / "scripts/build_arabic_print_proof.py").read_text(),
        "Arabic print proof script uses drawbot-skia",
        errors,
    )
    check("GFT_PACKAGER_SOURCE_MODE" in package_script_text, "package dry-run script exposes source mode env var", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in package_script_text, "package dry-run script error text documents selected Make target", errors)
    check("GF_REPO_PATH=/path/to/fonts GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in package_script_text, "package dry-run script documents GF_REPO_PATH override with selected source mode", errors)
    check(
        "GH_TOKEN" in package_script_text
        and "gh auth token" in package_script_text
        and "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in package_script_text,
        "package dry-run script validates GitHub token access for selected Make target",
        errors,
    )
    check("ensure_github_token()" in package_script_text, "package dry-run script validates GitHub API credentials before Packager", errors)
    check("gh auth login -h github.com" in package_script_text, "package dry-run script gives GitHub CLI reauth command", errors)
    check("--latest-release" in package_script_text, "package dry-run script supports latest-release mode", errors)
    check("--build-from-source" in package_script_text, "package dry-run script supports build-from-source mode", errors)
    check("current_branch" in package_script_text and "upstream/main" in package_script_text, "package dry-run script checks google/fonts branch alignment", errors)
    check("main...origin/main" in package_script_text, "package dry-run script checks fork origin alignment", errors)
    check(
        "stale_placeholder_upstream_url" in package_script_text
        and "Replace it with the decided public upstream URL" in package_script_text,
        "package dry-run script fails early on placeholder upstream URL in existing metadata",
        errors,
    )
    check(
        "starter_template_markers" in package_script_text
        and 'designer: "UNKNOWN"' in package_script_text
        and "Packager starter template" in package_script_text,
        "package dry-run script fails early on unpopulated Packager starter template",
        errors,
    )
    check(
        "unresolved_metadata_markers" in package_script_text
        and "Pending decision" in package_script_text
        and "make downstream-metadata-check" in package_script_text,
        "package dry-run script fails early on unresolved downstream metadata markers",
        errors,
    )
    check(
        "prohibited_optional_metadata_fields" in package_script_text
        and "review-gated optional field" in package_script_text,
        "package dry-run script rejects review-gated optional metadata fields",
        errors,
    )
    check(
        "metadata_has_config_yaml" in package_script_text
        and "source.config_yaml" in package_script_text
        and "build-from-source mode" in package_script_text,
        "package dry-run script enforces source.config_yaml by selected source mode",
        errors,
    )
    check(
        "metadata_has_archive_url" in package_script_text
        and "source.archive_url" in package_script_text
        and "latest-release mode" in package_script_text,
        "package dry-run script enforces archive_url for latest-release mode",
        errors,
    )
    check(
        "releases/download" in package_script_text
        and "release download URL ending in .zip" in package_script_text,
        "package dry-run script validates latest-release archive URL shape",
        errors,
    )
    metadata_prepare_text = (ROOT / "scripts/prepare_downstream_metadata.py").read_text()
    check("BLOCKED_MARKERS" in metadata_prepare_text, "downstream metadata helper blocks unresolved placeholders", errors)
    check("REQUIRED_LINES" in metadata_prepare_text, "downstream metadata helper validates required metadata lines", errors)
    check("SUPPORTED_SOURCE_MODES" in metadata_prepare_text, "downstream metadata helper validates supported Packager source modes", errors)
    check("GFT_PACKAGER_SOURCE_MODE" in metadata_prepare_text, "downstream metadata helper reads Packager source mode from environment", errors)
    check(
        "PROHIBITED_OPTIONAL_FIELDS" in metadata_prepare_text
        and "optional metadata field requires explicit Google Fonts review before apply" in metadata_prepare_text,
        "downstream metadata helper rejects review-gated optional metadata fields",
        errors,
    )
    check(
        "source.config_yaml is present but should be omitted" in metadata_prepare_text,
        "downstream metadata helper rejects config_yaml for non-build-from-source modes",
        errors,
    )
    check(
        "required metadata line missing for build-from-source mode" in metadata_prepare_text,
        "downstream metadata helper requires config_yaml for build-from-source mode",
        errors,
    )
    check(
        "source.archive_url is required for latest-release source mode" in metadata_prepare_text,
        "downstream metadata helper requires archive_url for latest-release mode",
        errors,
    )
    check(
        "valid_latest_release_archive_url" in metadata_prepare_text
        and "release download URL ending in .zip" in metadata_prepare_text,
        "downstream metadata helper validates latest-release archive URL shape",
        errors,
    )
    check("DATE_ADDED_PATTERN" in metadata_prepare_text, "downstream metadata helper validates final date_added format", errors)
    check("SOURCE_COMMIT_PATTERN" in metadata_prepare_text, "downstream metadata helper validates final source commit hash", errors)
    release_archive_builder_text = (ROOT / "scripts/build_release_archive.py").read_text()
    release_archive_test_text = (ROOT / "scripts/test_release_archive_gates.sh").read_text()
    check(
        "no source.files entries found in package preview" in release_archive_builder_text,
        "release archive builder rejects previews without source.files entries",
        errors,
    )
    check(
        "builder rejects missing source_file entries" in release_archive_test_text
        and "verifier rejects missing source_file entries" in release_archive_test_text,
        "release archive tests cover empty source.files previews",
        errors,
    )
    check(
        "builder rejects unsafe dest_file paths" in release_archive_test_text
        and "verifier rejects duplicate dest_file paths" in release_archive_test_text,
        "release archive tests cover unsafe and duplicate dest_file paths",
        errors,
    )
    check(
        'date_added with final valid "YYYY-MM-DD" Google Fonts date' in metadata_prepare_text,
        "downstream metadata helper blocks pending date_added before apply",
        errors,
    )
    check(
        "source.commit with final 40-character lowercase git hash" in metadata_prepare_text,
        "downstream metadata helper blocks pending source commit before apply",
        errors,
    )
    for required_metadata_line in [
        'post_script_name: "VirtuaGrotesk-Regular"',
        'full_name: "Virtua Grotesk Regular"',
        'min_value: 400.0',
        'max_value: 700.0',
        'dest_file: "article/readme-specimen.png"',
    ]:
        check(
            required_metadata_line in metadata_prepare_text,
            f"downstream metadata helper validates required line: {required_metadata_line}",
            errors,
        )
    check("--apply" in metadata_prepare_text, "downstream metadata helper requires explicit apply mode", errors)
    check("Ready to apply:" in metadata_prepare_text, "downstream metadata helper reports dry-run readiness", errors)
    check("ofl/virtuagrotesk" in metadata_prepare_text, "downstream metadata helper targets Virtua Grotesk family path", errors)
    check(
        "main...upstream/main" in metadata_prepare_text and "main...origin/main" in metadata_prepare_text,
        "downstream metadata helper checks google/fonts main alignment before apply",
        errors,
    )
    check("make downstream-metadata-check" in makefile_text, "Makefile exposes downstream metadata dry-run target", errors)
    check("downstream-metadata-helper-test:" in makefile_text, "Makefile exposes downstream metadata helper test target", errors)
    check("accepts GFT_PACKAGER_SOURCE_MODE=latest-release or build-from-source" in makefile_text, "Makefile help documents downstream metadata source modes", errors)
    check("GF_REPO_PATH='$(GF_REPO_PATH)' GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/prepare_downstream_metadata.py" in makefile_text, "Makefile passes GF_REPO_PATH and source mode through downstream metadata helper", errors)
    check(
        "GFT_PACKAGER_SOURCE_MODE='$(GFT_PACKAGER_SOURCE_MODE)' $(PYTHON) scripts/report_downstream_metadata_diff.py" in makefile_text,
        "Makefile passes selected source mode into downstream metadata diff report",
        errors,
    )
    check(
        'packager_args+=("-p")' not in package_script_text
        and 'packager_args+=("--pr")' not in package_script_text,
        "package dry-run script never enables PR creation",
        errors,
    )
    check("-py" not in text, "package checklist does not use stale packager flags", errors)
    check("documentation/google-fonts-release-checklist.md" in text, "package checklist includes release checklist", errors)
    check("documentation/google-fonts-template-and-pr-audit.md" in text, "package checklist includes template and PR audit", errors)
    check("documentation/recent-google-fonts-packages.md" in text, "package checklist includes recent-package audit", errors)
    check("documentation/google-fonts-add-font-template-audit.md" in text, "package checklist includes Add Font template audit", errors)
    check("documentation/project-template-automation-readiness.md" in text, "package checklist includes project-template automation readiness report", errors)
    check("documentation/decision-readiness.md" in text, "package checklist includes decision readiness report", errors)
    check("documentation/designer-profile-package-draft.md" in text, "package checklist includes designer profile package draft", errors)
    check("make designer-profile-check" in text, "package checklist documents designer profile check target", errors)
    check("documentation/family-name-readiness.md" in text, "package checklist includes family-name readiness report", errors)
    check("documentation/authorship-disclosure-readiness.md" in text, "package checklist includes authorship and AI disclosure readiness report", errors)
    check("documentation/pr-identity-readiness.md" in text, "package checklist includes PR identity readiness report", errors)
    check("documentation/downstream-pr-readiness.md" in text, "package checklist includes downstream PR readiness report", errors)
    check("documentation/vendor-id-readiness.md" in text, "package checklist includes vendor ID readiness report", errors)
    check("documentation/avar-readiness.md" in text, "package checklist includes avar readiness report", errors)
    check("documentation/public-upstream-readiness.md" in text, "package checklist includes public upstream URL readiness report", errors)
    check(
        "The canonical public URL is decided as\n`https://github.com/eliheuer/virtua-grotesk`" in text,
        "package checklist records decided public upstream URL",
        errors,
    )
    check(
        "scripts/apply_public_upstream_url.py --url https://github.com/eliheuer/virtua-grotesk --apply" in text,
        "package checklist documents decided public upstream URL apply command",
        errors,
    )
    check(
        "scripts/apply_public_upstream_url.py --url https://github.com/owner/repo --apply" not in text,
        "package checklist avoids generic owner/repo public URL command after URL decision",
        errors,
    )
    check("documentation/google-fonts-downstream-package-preview.md" in text, "package checklist includes downstream package preview", errors)
    check("documentation/final-submission-blockers.md" in text, "package checklist includes final-submission blocker summary", errors)
    check("documentation/submission-handoff-readiness.md" in text, "package checklist includes submission handoff readiness report", errors)
    check("documentation/package-source-files-audit.md" in text, "package checklist includes package source-file audit", errors)
    check("documentation/packager-source-strategy.md" in text, "package checklist includes Packager source strategy matrix", errors)
    check("documentation/release-archive-manifest.md" in text, "package checklist includes release archive manifest", errors)
    check("documentation/github-release-draft.md" in text, "package checklist includes GitHub release draft", errors)
    check("documentation/github-release-notes.md" in text, "package checklist includes GitHub release notes", errors)
    check("documentation/package-dry-run-readiness.md" in text, "package checklist includes package dry-run readiness report", errors)
    check("documentation/release-source-readiness.md" in text, "package checklist includes release/source readiness report", errors)
    check("documentation/upstream-structure-readiness.md" in text, "package checklist includes upstream structure readiness report", errors)
    check("documentation/downstream-metadata-readiness.md" in text, "package checklist includes downstream metadata readiness report", errors)
    check("make downstream-metadata-check" in text, "package checklist documents downstream metadata dry-run helper", errors)
    check("scripts/prepare_downstream_metadata.py --apply" in text, "package checklist documents explicit downstream metadata apply command", errors)
    check("GFT_PACKAGER_SOURCE_MODE=build-from-source make downstream-metadata-check" in text, "package checklist documents build-from-source metadata check mode", errors)
    check("documentation/kerning-readiness.md" in text, "package checklist includes kerning readiness report", errors)
    check("documentation/kerning-proof-review.md" in text, "package checklist includes kerning proof review report", errors)
    check("documentation/glyph-reachability.md" in text, "package checklist includes glyph reachability report", errors)
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in text, "package checklist documents selected latest-release package dry-run command", errors)
    check("GFT_PACKAGER_SOURCE_MODE=default make package-dry-run" in text, "package checklist documents explicit default-mode fallback command", errors)
    check("make github-auth-check" in text, "package checklist documents GitHub API auth check command", errors)
    check("gh auth status -h github.com" in text, "package checklist documents GitHub auth status command", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk" in text, "package checklist documents scoped google/fonts status command", errors)
    check(
        "Mapping source: `documentation/google-fonts-downstream-package-preview.md`" in package_source_text,
        "package source-file audit reads expected source.files from downstream package preview",
        errors,
    )
    check("Destination mapping matches expected downstream layout: yes" in package_source_text, "package source-file audit validates downstream destination mapping", errors)
    check("Unsafe `source.files` paths: 0" in package_source_text, "package source-file audit validates safe source_file paths", errors)
    check("Duplicate `source.files` paths: 0" in package_source_text, "package source-file audit validates unique source_file paths", errors)
    check("Unsafe `dest_file` paths: 0" in package_source_text, "package source-file audit validates safe dest_file paths", errors)
    check("Duplicate `dest_file` paths: 0" in package_source_text, "package source-file audit validates unique dest_file paths", errors)
    check("Variable-font-first source mapping: yes" in package_source_text, "package source-file audit validates variable-font-first mapping", errors)
    check("Static TTFs generated locally for QA: 4 / 4" in package_source_text, "package source-file audit records generated static QA outputs", errors)
    check("Static TTFs included in `source.files`: 0" in package_source_text, "package source-file audit confirms static fonts omitted from source.files", errors)
    check("Downstream `static/` destinations planned: 0" in package_source_text, "package source-file audit confirms no downstream static directory planned", errors)
    check("Tracked `source.files`:" in package_source_text, "package source-file audit summarizes tracked source.files", errors)
    check("Untracked local `source.files`:" in package_source_text, "package source-file audit summarizes untracked source.files", errors)
    check("Build-from-source inputs tracked:" in package_source_text, "package source-file audit summarizes tracked build inputs", errors)
    check("Tracked by git" in package_source_text, "package source-file audit includes tracked-by-git columns", errors)
    check("Static package omission documented in preview: yes" in package_source_text, "package source-file audit confirms static omission documented", errors)
    check("## Static Output Handling" in package_source_text, "package source-file audit includes static output handling table", errors)
    check("Article assets map into `article/`: yes" in package_source_text, "package source-file audit validates Article asset destination", errors)
    check("Build script uses `gftools builder sources/config.yaml`: yes" in package_source_text, "package source-file audit validates GF builder command", errors)
    check("Build script runs metadata post-processing: yes" in package_source_text, "package source-file audit validates metadata post-processing command", errors)
    check("Builder config outputs to `fonts/`: yes" in package_source_text, "package source-file audit validates builder output path", errors)
    check("`sources/config.yaml` is tracked by git" in package_source_text, "package source-file audit checks sources/config.yaml tracked state", errors)
    check("## Build Command Evidence" in package_source_text, "package source-file audit includes build command evidence table", errors)
    check("`branch` field present for default/source-build mode: yes" in package_source_text, "package source-file audit validates branch field presence", errors)
    check("`archive_url` present for selected release/archive strategy: yes" in package_source_text, "package source-file audit validates archive_url presence for selected release/archive strategy", errors)
    check("`archive_url` is GitHub release download `.zip`: yes" in package_source_text, "package source-file audit validates latest-release archive_url shape", errors)
    check("Keep the selected release/archive source strategy synchronized" in package_source_text, "package source-file audit final dry-run guidance records selected source strategy", errors)
    check("Confirm the final GitHub release/archive contains every" in package_source_text, "package source-file audit final dry-run guidance records archive file requirement", errors)
    check("Confirm no `source_file` or `dest_file` path is absolute, parent-relative, or duplicated." in package_source_text, "package source-file audit final dry-run guidance records path-safety check", errors)
    check("Expected Packager branch name: `gftools_packager_ofl_virtuagrotesk`" in package_source_text, "package source-file audit records expected Packager branch name", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in package_source_text, "package source-file audit cites GF package guide", errors)
    check("# Release Archive Manifest" in release_archive_text, "release archive manifest has expected heading", errors)
    check("Mapping source: `documentation/google-fonts-downstream-package-preview.md`" in release_archive_text, "release archive manifest reads downstream package preview", errors)
    check("Selected source mode: `latest-release`" in release_archive_text, "release archive manifest records selected source mode", errors)
    check("Archive inputs expected: 4" in release_archive_text, "release archive manifest counts expected source files", errors)
    check("Archive inputs present locally: 4 / 4" in release_archive_text, "release archive manifest confirms all archive inputs exist", errors)
    check("Ignored archive inputs:" in release_archive_text, "release archive manifest summarizes ignored inputs", errors)
    check("Untracked archive inputs:" in release_archive_text, "release archive manifest summarizes untracked inputs", errors)
    check("Variable font newer than source/build inputs:" in release_archive_text, "release archive manifest records variable-font freshness", errors)
    check("Unsafe `source.files` paths: 0" in release_archive_text, "release archive manifest records safe source paths", errors)
    check("Duplicate `source.files` paths: 0" in release_archive_text, "release archive manifest records unique source paths", errors)
    check("Unsafe `dest_file` paths: 0" in release_archive_text, "release archive manifest records safe destination paths", errors)
    check("Duplicate `dest_file` paths: 0" in release_archive_text, "release archive manifest records unique destination paths", errors)
    check("Suggested final release tag: `v1.000`" in release_archive_text, "release archive manifest records suggested final tag", errors)
    check("Final GitHub release tag exists locally:" in release_archive_text, "release archive manifest checks local final tag state", errors)
    check("Final GitHub release archive URL recorded: pending" in release_archive_text, "release archive manifest keeps archive URL pending", errors)
    check("Preview release archive URL is GitHub release download `.zip`: yes" in release_archive_text, "release archive manifest validates preview archive URL shape", errors)
    check("Preview archive filename matches local archive: yes" in release_archive_text, "release archive manifest confirms preview/local archive filename match", errors)
    check("SHA-256" in release_archive_text, "release archive manifest records file hashes", errors)
    check("fonts/variable/VirtuaGrotesk[wght].ttf" in release_archive_text, "release archive manifest includes served variable font", errors)
    check("documentation/ARTICLE.en_us.html" in release_archive_text, "release archive manifest includes article HTML", errors)
    check("documentation/readme-specimen.png" in release_archive_text, "release archive manifest includes article image", errors)
    check("make release-archive-check" in release_archive_text, "release archive manifest documents regeneration target", errors)
    check("make downstream-metadata-check" in release_archive_text, "release archive manifest documents downstream metadata final gate", errors)
    check("Local release archive: `dist/VirtuaGrotesk-1.000.zip`" in release_archive_text, "release archive manifest documents local archive path", errors)
    check("Local release archive contains expected files:" in release_archive_text, "release archive manifest checks local archive file coverage", errors)
    check("Local release archive hashes match source files:" in release_archive_text, "release archive manifest checks local archive hash parity", errors)
    check("Local release archive metadata deterministic:" in release_archive_text, "release archive manifest checks local archive metadata determinism", errors)
    check("Local release archive SHA-256:" in release_archive_text, "release archive manifest records local archive SHA-256", errors)
    check("Deterministic metadata" in release_archive_text, "release archive manifest records per-entry deterministic metadata", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in release_archive_text, "release archive manifest cites GF package guide", errors)
    check("# Packager Source Strategy Matrix" in packager_source_strategy_text, "Packager source strategy report has expected heading", errors)
    check("Default branch `source.files`" in packager_source_strategy_text, "Packager source strategy report includes default branch strategy", errors)
    check("Latest release/archive" in packager_source_strategy_text, "Packager source strategy report includes latest-release strategy", errors)
    check("Build from source" in packager_source_strategy_text, "Packager source strategy report includes build-from-source strategy", errors)
    check("Downstream preview includes release `archive_url`: yes" in packager_source_strategy_text, "Packager source strategy report tracks archive_url preview state", errors)
    check("Downstream preview `archive_url` is GitHub release download `.zip`: yes" in packager_source_strategy_text, "Packager source strategy report tracks archive_url shape", errors)
    check("Latest-release packaging must add the final GitHub release download `.zip` `archive_url`" in packager_source_strategy_text, "Packager source strategy report documents archive_url requirement", errors)
    check("Source Files To Expose" in packager_source_strategy_text, "Packager source strategy report lists source files to expose", errors)
    check("Tracked source.files:" in packager_source_strategy_text, "Packager source strategy report summarizes tracked source.files", errors)
    check("Untracked local source.files:" in packager_source_strategy_text, "Packager source strategy report summarizes untracked source.files", errors)
    check("Tracked locally" in packager_source_strategy_text, "Packager source strategy report lists source-file tracked state", errors)
    check("source.config_yaml" in packager_source_strategy_text, "Packager source strategy report includes config_yaml policy", errors)
    check("upstream.yaml" in packager_source_strategy_text, "Packager source strategy report tracks upstream.yaml review", errors)
    check("## Selected Latest-Release Action Plan" in packager_source_strategy_text, "Packager source strategy report includes selected latest-release action plan", errors)
    check("## Per-Strategy Mechanical Checklist" in packager_source_strategy_text, "Packager source strategy report includes per-strategy mechanical checklist", errors)
    check("### If Default Public-Branch Packaging Is Chosen" in packager_source_strategy_text, "Packager source strategy report includes default-branch checklist", errors)
    check("### If Latest Release Or Archive Packaging Is Chosen" in packager_source_strategy_text, "Packager source strategy report includes release/archive checklist", errors)
    check("### If Build-From-Source Packaging Is Chosen" in packager_source_strategy_text, "Packager source strategy report includes build-from-source checklist", errors)
    check("Track every currently untracked build input: none" in packager_source_strategy_text, "Packager source strategy report lists untracked build inputs", errors)
    check(
        "Release archive files currently present but untracked: `fonts/variable/VirtuaGrotesk[wght].ttf`" in packager_source_strategy_text,
        "Packager source strategy report lists untracked release/archive files",
        errors,
    )
    check(
        "Release archive files currently blocked by `.gitignore`: `fonts/variable/VirtuaGrotesk[wght].ttf`" in packager_source_strategy_text,
        "Packager source strategy report identifies variable TTF gitignore blocker",
        errors,
    )
    check("# Package Dry-Run Readiness" in package_dry_run_text, "package dry-run readiness report has expected heading", errors)
    check("Wrapper command: `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`" in package_dry_run_text, "package dry-run readiness report records selected wrapper command", errors)
    check("Local google/fonts fork ready: yes" in package_dry_run_text, "package dry-run readiness report checks local google/fonts fork", errors)
    check("Origin GitHub repo: `eliheuer/fonts`" in package_dry_run_text, "package dry-run readiness report records Eli's google/fonts fork origin", errors)
    check("Origin is fork candidate: yes" in package_dry_run_text, "package dry-run readiness report confirms origin is a fork candidate", errors)
    check("Upstream is canonical google/fonts: yes" in package_dry_run_text, "package dry-run readiness report confirms canonical google/fonts upstream", errors)
    check("google/fonts remote topology ready: yes" in package_dry_run_text, "package dry-run readiness report validates fork-plus-upstream topology", errors)
    check("Dirty paths inside `ofl/virtuagrotesk`:" in package_dry_run_text, "package dry-run readiness report records family-package dirty paths", errors)
    check("Dirty paths outside `ofl/virtuagrotesk`: 0" in package_dry_run_text, "package dry-run readiness report confirms no unrelated google/fonts dirtiness", errors)
    check("Dirty state is isolated to `ofl/virtuagrotesk`: yes" in package_dry_run_text, "package dry-run readiness report confirms dirty state is isolated to target package", errors)
    check("## Source Mode Gate" in package_dry_run_text, "package dry-run readiness report includes source-mode gate", errors)
    check("| `default` | `make package-dry-run` | no |" in package_dry_run_text, "package dry-run readiness report evaluates default source mode", errors)
    check("| `latest-release` | `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` | no |" in package_dry_run_text, "package dry-run readiness report evaluates latest-release source mode", errors)
    check("| `build-from-source` | `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` | no |" in package_dry_run_text, "package dry-run readiness report evaluates build-from-source source mode", errors)
    check("public branch must expose ignored/generated source files" in package_dry_run_text, "package dry-run readiness report records default-mode public-file blocker", errors)
    check("public branch must expose untracked source files" in package_dry_run_text, "package dry-run readiness report records default-mode untracked source-file blocker", errors)
    check("release/archive must include untracked local source files" in package_dry_run_text, "package dry-run readiness report records latest-release untracked source-file blocker", errors)
    check("keep `source.config_yaml` for build-from-source" in package_dry_run_text, "package dry-run readiness report records build-from-source source-mode policy", errors)
    check("release/archive must include untracked local source files" in package_dry_run_text, "package dry-run readiness report records latest-release archive/source blocker", errors)
    check("keep `source.config_yaml` for build-from-source" in package_dry_run_text, "package dry-run readiness report records config_yaml policy for build-from-source mode", errors)
    check("preview still has pending/placeholder source fields" in package_dry_run_text, "package dry-run readiness report records unresolved preview source fields", errors)
    check("Required local package inputs ready: yes" in package_dry_run_text, "package dry-run readiness report checks local package inputs", errors)
    check("Required local package inputs tracked: 4 / 5" in package_dry_run_text, "package dry-run readiness report summarizes tracked local package inputs", errors)
    check("Required local package inputs untracked: 1" in package_dry_run_text, "package dry-run readiness report summarizes untracked local package inputs", errors)
    check("Downstream preview `source.files` inputs: 4" in package_dry_run_text, "package dry-run readiness report separates downstream source.files count", errors)
    check("Wrapper-only local sanity inputs: `sources/config.yaml`" in package_dry_run_text, "package dry-run readiness report separates wrapper-only config input", errors)
    check("Existing downstream METADATA.pb reusable: no" in package_dry_run_text, "package dry-run readiness report summarizes downstream metadata reusability", errors)
    check("Existing downstream METADATA.pb has stale placeholder URL: no" in package_dry_run_text, "package dry-run readiness report distinguishes stale placeholder URL state", errors)
    check("Existing downstream METADATA.pb has starter-template markers: yes" in package_dry_run_text, "package dry-run readiness report distinguishes starter-template marker state", errors)
    check("Starter template quarantined in downstream package path: yes" in package_dry_run_text, "package dry-run readiness report summarizes starter template quarantine state", errors)
    check("Existing downstream METADATA.pb has unresolved metadata markers: no" in package_dry_run_text, "package dry-run readiness report distinguishes unresolved metadata marker state", errors)
    check("Existing downstream METADATA.pb source-mode compatible: no" in package_dry_run_text, "package dry-run readiness report distinguishes source-mode compatibility state", errors)
    check("## Downstream Starter Template Policy" in package_dry_run_text, "package dry-run readiness report includes downstream starter template policy", errors)
    check("Treat that file as quarantined" in package_dry_run_text, "package dry-run readiness report marks starter metadata as quarantined evidence", errors)
    check("Replacement source of truth: `documentation/google-fonts-downstream-package-preview.md`" in package_dry_run_text, "package dry-run readiness report names downstream preview as replacement source of truth", errors)
    check("Replacement gate: `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`" in package_dry_run_text, "package dry-run readiness report documents checked replacement gate", errors)
    check("| Input | Role | Present locally | Ignored by git | Tracked by git |" in package_dry_run_text, "package dry-run readiness report includes package input roles and git state", errors)
    check("not part of the selected latest-release `source.files` mapping" in package_dry_run_text, "package dry-run readiness report documents config_yaml source-mode distinction", errors)
    check(
        re.search(r"GitHub API credentials ready: (yes|no)", package_dry_run_text) is not None,
        "package dry-run readiness report records current GitHub auth state",
        errors,
    )
    check(
        re.search(r"Wrapper can reach Packager: (yes|no)", package_dry_run_text) is not None,
        "package dry-run readiness report predicts whether wrapper reaches Packager",
        errors,
    )
    check(
        re.search(r"First blocker: [^\n]+", package_dry_run_text) is not None,
        "package dry-run readiness report records first blocker",
        errors,
    )
    check(
        re.search(r"Blocking findings: [^\n]+", package_dry_run_text) is not None,
        "package dry-run readiness report records all current blockers",
        errors,
    )
    check("## Wrapper Alignment" in package_dry_run_text, "package dry-run readiness report checks shell wrapper alignment", errors)
    check("Report/wrapper required-input lists match: yes" in package_dry_run_text, "package dry-run readiness report confirms required-input alignment", errors)
    check("Report/wrapper starter-marker lists match: yes" in package_dry_run_text, "package dry-run readiness report confirms starter-marker alignment", errors)
    check("Report/wrapper unresolved-marker lists match: yes" in package_dry_run_text, "package dry-run readiness report confirms unresolved-marker alignment", errors)
    check("Report/wrapper source-mode lists match: yes" in package_dry_run_text, "package dry-run readiness report confirms source-mode alignment", errors)
    check("Report/wrapper source-mode metadata gates present: yes" in package_dry_run_text, "package dry-run readiness report confirms source-mode metadata gate alignment", errors)
    check("Report/wrapper release-archive gate present: yes" in package_dry_run_text, "package dry-run readiness report confirms release archive gate alignment", errors)
    check("Report/wrapper final metadata value gates present: yes" in package_dry_run_text, "package dry-run readiness report confirms date_added/source.commit final-value gate alignment", errors)
    check("Local release archive verified:" in package_dry_run_text, "package dry-run readiness report confirms local release archive verification", errors)
    check("Required inputs missing from wrapper: none" in package_dry_run_text, "package dry-run readiness report confirms no missing wrapper inputs", errors)
    check("Starter markers missing from wrapper: none" in package_dry_run_text, "package dry-run readiness report confirms no missing wrapper starter markers", errors)
    check("Unresolved markers missing from wrapper: none" in package_dry_run_text, "package dry-run readiness report confirms no missing wrapper unresolved markers", errors)
    check(
        "GitHub API credentials unavailable" in package_dry_run_text,
        "package dry-run readiness report includes GitHub auth among blocking findings",
        errors,
    )
    check(
        "Existing downstream METADATA.pb is starter template:" in package_dry_run_text,
        "package dry-run readiness report records Packager starter-template state",
        errors,
    )
    check(
        "Existing downstream METADATA.pb starter markers:" in package_dry_run_text,
        "package dry-run readiness report records Packager starter-template markers",
        errors,
    )
    check(
        "Existing downstream METADATA.pb unresolved markers:" in package_dry_run_text,
        "package dry-run readiness report records unresolved downstream metadata markers",
        errors,
    )
    check(
        "Existing downstream METADATA.pb source-mode blockers:" in package_dry_run_text,
        "package dry-run readiness report records downstream source-mode metadata blockers",
        errors,
    )
    package_auth_unready = "GitHub API credentials ready: no" in package_dry_run_text
    check(
        (not package_auth_unready) or "gh auth login -h github.com" in package_dry_run_text,
        "package dry-run readiness report gives GitHub CLI reauth command when auth is unavailable",
        errors,
    )
    check("gh auth status -h github.com" in package_dry_run_text, "package dry-run readiness report gives GitHub auth status command", errors)
    check("make github-auth-check" in package_dry_run_text, "package dry-run readiness report gives local auth check command", errors)
    check("export GH_TOKEN=REPLACE_WITH_SHORT_LIVED_TOKEN" in package_dry_run_text, "package dry-run readiness report documents short-lived GH_TOKEN option", errors)
    check("Never put `GH_TOKEN` in tracked files" in package_dry_run_text, "package dry-run readiness report warns against committing GH_TOKEN", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk" in package_dry_run_text, "package dry-run readiness report gives scoped google/fonts status command", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short" in package_dry_run_text, "package dry-run readiness report gives full google/fonts status command", errors)
    check("./venv/bin/python scripts/prepare_downstream_metadata.py --apply" in package_dry_run_text, "package dry-run readiness report documents checked downstream metadata apply command", errors)
    check("git -C /Users/eli/GH/forks/fonts diff -- ofl/virtuagrotesk/METADATA.pb" in package_dry_run_text, "package dry-run readiness report documents downstream metadata diff review command", errors)
    check("Do not run Packager with `-p`" in package_dry_run_text, "package dry-run readiness report blocks PR mode before no-PR review", errors)
    package_first_blocker_match = re.search(r"First blocker: ([^\n]+)", package_dry_run_text)
    package_first_blocker = package_first_blocker_match.group(1) if package_first_blocker_match else ""
    package_blocking_findings_match = re.search(r"Blocking findings: ([^\n]+)", package_dry_run_text)
    package_blocking_findings = package_blocking_findings_match.group(1) if package_blocking_findings_match else ""
    package_reaches_packager_match = re.search(r"Wrapper can reach Packager: (yes|no)", package_dry_run_text)
    package_reaches_packager = package_reaches_packager_match.group(1) if package_reaches_packager_match else ""
    check("# Kerning Readiness" in kerning_text, "kerning readiness report has expected heading", errors)
    check("Source kerning exists in at least one master: yes" in kerning_text, "kerning report records source kerning in one master", errors)
    check("Source kerning exists in every master: yes" in kerning_text, "kerning report records source kerning in every master", errors)
    check("All built fonts expose GPOS `kern`: yes" in kerning_text, "kerning report records full built GPOS kern coverage", errors)
    check("All built static fonts expose GPOS `kern`: yes" in kerning_text, "kerning report records static GPOS kern coverage", errors)
    check("Fontspector `gpos_kerning_info` warnings: 0" in kerning_text, "kerning report records current Fontspector warning count", errors)
    check("`gftools qa --proof` importable: yes" in kerning_text, "kerning report records gftools qa proof readiness", errors)
    check("Latest `gftools qa --proof` HTML output present: yes" in kerning_text, "kerning report records latest gftools QA proof output", errors)
    check("Latest proof covers expected instances: yes" in kerning_text, "kerning report records expected proof instance coverage", errors)
    check("## Google Fonts Visual QA" in kerning_text, "kerning report includes Google Fonts visual QA section", errors)
    check("This is part of the core QA process for Virtua Grotesk" in kerning_text, "kerning report marks visual proof as core QA", errors)
    check("make kerning-proof-check" in kerning_text, "kerning report documents gftools qa proof command", errors)
    check("venv/bin` on `PATH`" in kerning_text, "kerning report documents gftools QA helper PATH requirement", errors)
    check(
        "https://fonts.google.com/metadata/fonts" in kerning_text,
        "kerning report documents gftools proof network dependency",
        errors,
    )
    check("basic spacing and kerning" in kerning_text, "kerning report connects QA proof to spacing and kerning review", errors)
    check("Review the generated HTML before treating kerning, spacing, or a" in kerning_text, "kerning report requires HTML proof review before final kerning state", errors)
    check("Proof covers Regular, Medium, SemiBold, Bold | yes" in kerning_text, "kerning report confirms proof covers all expected weight instances", errors)
    check("Decision status: open" in kerning_text, "kerning report records open decision", errors)
    check("https://googlefonts.github.io/gf-guide/testing.html" in kerning_text, "kerning report cites GF local testing guide", errors)
    check("https://googlefonts.github.io/gf-guide/tools.html" in kerning_text, "kerning report cites GF tools guide", errors)
    check("https://googlefonts.github.io/gf-guide/onboarder-workflow.html" in kerning_text, "kerning report cites GF onboarder workflow", errors)
    check("# Kerning Proof Review" in kerning_proof_review_text, "kerning proof review packet has expected heading", errors)
    check("auditable for humans and agents" in kerning_proof_review_text, "kerning proof review packet explains human/agent role", errors)
    check("Expected HTML proofs present: 16 / 16" in kerning_proof_review_text, "kerning proof review packet counts expected proof HTML files", errors)
    check("Expected instances covered: yes" in kerning_proof_review_text, "kerning proof review packet confirms expected instances", errors)
    check("Review status: pending human visual review" in kerning_proof_review_text, "kerning proof review packet keeps review status explicit", errors)
    for instance in ["Regular", "Medium", "SemiBold", "Bold"]:
        for proof_type in ["glyphs", "proofer", "text", "waterfall"]:
            check(
                f"| {instance} | `{proof_type}` | yes |" in kerning_proof_review_text,
                f"kerning proof review packet tracks {instance} {proof_type} proof",
                errors,
            )
    for phrase in [
        "Open every `*-diffbrowsers_proofer.html` file",
        "Open every `*-diffbrowsers_text.html` file",
        "Open every `*-diffbrowsers_waterfall.html` file",
        "Open every `*-diffbrowsers_glyphs.html` file",
        "Compare Regular, Medium, SemiBold, and Bold",
        "make kerning-proof-check",
        "make kerning-check",
        "make preflight",
        "https://github.com/googlefonts/gftools",
    ]:
        check(phrase in kerning_proof_review_text, f"kerning proof review packet records: {phrase}", errors)
    check("# Downstream Metadata Readiness" in downstream_metadata_text, "downstream metadata readiness report has expected heading", errors)
    check("Top-level family name present: yes" in downstream_metadata_text, "downstream metadata report confirms top-level family name", errors)
    check("`date_added` final date present: no" in downstream_metadata_text, "downstream metadata report confirms pending date_added", errors)
    check("Variable filename/name fields match built font: yes" in downstream_metadata_text, "downstream metadata report matches built variable metadata", errors)
    check("Expected subsets present and sorted: yes" in downstream_metadata_text, "downstream metadata report confirms sorted subsets", errors)
    check("Non-Noto `languages` entries absent: yes" in downstream_metadata_text, "downstream metadata report confirms languages omitted", errors)
    check("Unneeded optional display/classification fields absent: yes" in downstream_metadata_text, "downstream metadata report confirms optional fields omitted", errors)
    check("Expected `source.files` destination mappings present: yes" in downstream_metadata_text, "downstream metadata report confirms source destination mappings", errors)
    check("Source block has repository, commit, archive_url, and branch fields: yes" in downstream_metadata_text, "downstream metadata report confirms source block shape", errors)
    check("`source.archive_url` required for latest-release mode: yes" in downstream_metadata_text, "downstream metadata report confirms latest-release archive_url requirement", errors)
    check("`source.archive_url` is GitHub release download `.zip`: yes" in downstream_metadata_text, "downstream metadata report confirms latest-release archive_url shape", errors)
    check("`source.archive_url` satisfies latest-release mode: yes" in downstream_metadata_text, "downstream metadata report confirms latest-release archive_url readiness", errors)
    check("Static style-name review uses GF `SemiBold` spelling: yes" in downstream_metadata_text, "downstream metadata report confirms SemiBold spelling review", errors)
    check("## Date Added Policy" in downstream_metadata_text, "downstream metadata report includes date_added policy section", errors)
    check("## Pending Field Decision Map" in downstream_metadata_text, "downstream metadata report includes pending-field decision map", errors)
    check("Pending or placeholder metadata lines: 2" in downstream_metadata_text, "downstream metadata report records unresolved metadata lines", errors)
    check("# Downstream Metadata Diff" in downstream_metadata_diff_text, "downstream metadata diff report has expected heading", errors)
    check("Actual downstream METADATA.pb present: yes" in downstream_metadata_diff_text, "downstream metadata diff report sees Packager-created metadata", errors)
    check("Actual downstream METADATA.pb is starter template: yes" in downstream_metadata_diff_text, "downstream metadata diff report identifies Packager starter template", errors)
    check("Expected metadata lines missing from actual downstream file:" in downstream_metadata_diff_text, "downstream metadata diff report counts missing expected lines", errors)
    check("Actual downstream `source.config_yaml` present:" in downstream_metadata_diff_text, "downstream metadata diff report records config_yaml presence separately", errors)
    check("Expected preview `source.config_yaml` present:" in downstream_metadata_diff_text, "downstream metadata diff report records preview config_yaml presence separately", errors)
    check("Expected preview has final `date_added`: no" in downstream_metadata_diff_text, "downstream metadata diff report records pending date_added", errors)
    check("## Replacement Readiness Gate" in downstream_metadata_diff_text, "downstream metadata diff report includes replacement readiness gate", errors)
    check("Ready to apply preview via helper: no" in downstream_metadata_diff_text, "downstream metadata diff report mirrors prepare-helper apply readiness", errors)
    check("- Apply command intentionally not run: yes" in downstream_metadata_diff_text, "downstream metadata diff report stays dry-run only", errors)
    check("blocked marker still present: Pending final" in downstream_metadata_diff_text, "downstream metadata diff report records pending-final blocker", errors)
    check(
        'required metadata line missing: date_added with final valid "YYYY-MM-DD" Google Fonts date' in downstream_metadata_diff_text,
        "downstream metadata diff report records pending date_added blocker",
        errors,
    )
    check(
        "required metadata line missing: source.commit with final 40-character lowercase git hash" in downstream_metadata_diff_text,
        "downstream metadata diff report records pending source commit blocker",
        errors,
    )
    check("Actual downstream `source.config_yaml` present: no" in downstream_metadata_diff_text, "downstream metadata diff report records current source-mode state", errors)
    check("## Prepare Helper Alignment" in downstream_metadata_diff_text, "downstream metadata diff report checks prepare-helper alignment", errors)
    check("Diff/helper required-line lists match: yes" in downstream_metadata_diff_text, "downstream metadata diff report confirms helper/report required-line match", errors)
    check("Date-added format validation in prepare helper: yes" in downstream_metadata_diff_text, "downstream metadata diff report confirms helper validates date_added", errors)
    check("Source commit hash validation in prepare helper: yes" in downstream_metadata_diff_text, "downstream metadata diff report confirms helper validates source commit", errors)
    check("Latest-release archive URL validation in prepare helper: yes" in downstream_metadata_diff_text, "downstream metadata diff report confirms helper validates release archive URL shape", errors)
    check("Missing from helper: none" in downstream_metadata_diff_text, "downstream metadata diff report confirms no required lines missing from helper", errors)
    check("Extra in helper: none" in downstream_metadata_diff_text, "downstream metadata diff report confirms no extra helper required lines", errors)
    check('`fonts/variable/MyFont[wght].ttf` -> `MyFont[wght].ttf`' in downstream_metadata_diff_text, "downstream metadata diff report records starter source mapping", errors)
    check("make downstream-metadata-check" in downstream_metadata_diff_text, "downstream metadata diff report points to dry-run helper", errors)
    check("scripts/prepare_downstream_metadata.py --apply" in downstream_metadata_diff_text, "downstream metadata diff report points to explicit apply helper", errors)
    check(
        "rerun `make preflight` so proof evidence" in downstream_metadata_diff_text,
        "downstream metadata diff report uses synchronized preflight before Packager",
        errors,
    )
    check("/Users/eli/GH/forks/fonts/ofl/virtuagrotesk/METADATA.pb" in downstream_metadata_diff_text, "downstream metadata diff report names downstream target path", errors)
    check("# Release Source Readiness" in release_source_text, "release/source readiness report has expected heading", errors)
    check("Current repo commit:" in release_source_text, "release/source readiness report records current commit", errors)
    check("Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`" in release_source_text, "release/source readiness report records normalized GitHub origin candidate", errors)
    check("Suggested tag matches source version: yes" in release_source_text, "release/source readiness report checks tag/version alignment", errors)
    check("Pending source fields in downstream preview:" in release_source_text, "release/source readiness report records pending source fields", errors)
    check("Downstream source destination mapping ready: yes" in release_source_text, "release/source readiness report checks downstream source destination mapping", errors)
    check("Downstream source mapping is variable-font-first: yes" in release_source_text, "release/source readiness report checks variable-font-first source mapping", errors)
    for source, dest in [
        ("OFL.txt", "OFL.txt"),
        ("fonts/variable/VirtuaGrotesk[wght].ttf", "VirtuaGrotesk[wght].ttf"),
        ("documentation/ARTICLE.en_us.html", "article/ARTICLE.en_us.html"),
        ("documentation/readme-specimen.png", "article/readme-specimen.png"),
    ]:
        check(
            f"| `{source}` | `{dest}` |" in release_source_text,
            f"release/source readiness report records destination mapping: {source}",
            errors,
        )
    check("Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`" in release_source_text, "release/source readiness report records expected Packager branch", errors)
    check("Local google/fonts main vs upstream/main:" in release_source_text, "release/source readiness report records local google/fonts alignment", errors)
    check("| dirty inside `ofl/virtuagrotesk` | 1 |" in release_source_text, "release/source readiness report tables target-package dirtiness", errors)
    check("| dirty outside `ofl/virtuagrotesk` | 0 |" in release_source_text, "release/source readiness report tables unrelated google/fonts dirtiness", errors)
    check("# Upstream Structure Readiness" in upstream_structure_text, "upstream structure readiness report has expected heading", errors)
    check("Mandatory upstream paths present: 11 / 11" in upstream_structure_text, "upstream structure report confirms mandatory paths for package checklist", errors)
    check("# Submission Handoff Readiness" in handoff_readiness_text, "submission handoff readiness report has expected heading", errors)
    check("Template default labels match handoff: yes" in handoff_readiness_text, "submission handoff report checks labels", errors)
    check("Issue draft title is current: yes" in handoff_readiness_text, "submission handoff report checks issue draft title", errors)
    check("Issue draft labels are current: yes" in handoff_readiness_text, "submission handoff report checks issue draft labels", errors)
    check("Issue draft template checkout status is current: yes" in handoff_readiness_text, "submission handoff report checks issue draft template checkout status", errors)
    check("Issue draft template is aligned with upstream/main: yes" in handoff_readiness_text, "submission handoff report checks issue draft upstream alignment", errors)
    check("Issue draft template is aligned with origin/main: yes" in handoff_readiness_text, "submission handoff report checks issue draft origin alignment", errors)
    check("Issue draft leaves boxes unchecked: yes" in handoff_readiness_text, "submission handoff report checks issue draft checkbox state", errors)
    check("Issue draft status notes match checkbox count: yes" in handoff_readiness_text, "submission handoff report checks issue draft status notes", errors)
    check("Issue draft includes current Latin Core gap: yes" in handoff_readiness_text, "submission handoff report checks issue draft Latin Core gap", errors)
    check("Issue draft includes current Arabic Core gap: yes" in handoff_readiness_text, "submission handoff report checks issue draft Arabic Core gap", errors)
    check("Issue draft references Arabic readiness reports: yes" in handoff_readiness_text, "submission handoff report checks issue draft Arabic report references", errors)
    check("Issue draft includes decision-linked warning status: yes" in handoff_readiness_text, "submission handoff report checks issue draft decision-linked warning status", errors)
    check("Issue draft references decision-warning reports: yes" in handoff_readiness_text, "submission handoff report checks issue draft decision-warning report references", errors)
    check("Issue draft includes downstream metadata apply gate: yes" in handoff_readiness_text, "submission handoff report checks issue draft downstream metadata apply gate", errors)
    check("Issue draft includes current Fontspector FAIL count: yes" in handoff_readiness_text, "submission handoff report checks issue draft Fontspector count", errors)
    check("Issue draft includes GF visual kerning proof status: yes" in handoff_readiness_text, "submission handoff report checks issue draft kerning proof status", errors)
    check("Issue draft references GF visual proof review packet: yes" in handoff_readiness_text, "submission handoff report checks issue draft kerning proof review reference", errors)
    check("Issue draft tracks repository maintenance commitment: yes" in handoff_readiness_text, "submission handoff report checks issue draft maintenance commitment", errors)
    check("Kerning report has current GF visual proof output: yes" in handoff_readiness_text, "submission handoff report mirrors kerning proof output", errors)
    check("Kerning report proof covers expected instances: yes" in handoff_readiness_text, "submission handoff report mirrors kerning proof instance coverage", errors)
    check("Kerning proof review packet has expected proof files: 16 / 16" in handoff_readiness_text, "submission handoff report mirrors kerning proof review file count", errors)
    check("Kerning proof review packet covers expected instances: yes" in handoff_readiness_text, "submission handoff report mirrors kerning proof review instance coverage", errors)
    check("Handoff points to generated Add Font issue draft: yes" in handoff_readiness_text, "submission handoff report checks generated Add Font issue draft link", errors)
    check("Handoff includes current Fontspector summary: yes" in handoff_readiness_text, "submission handoff report checks Fontspector summary", errors)
    check("Handoff includes current Latin Core gap: yes" in handoff_readiness_text, "submission handoff report checks Latin Core gap", errors)
    check("Handoff includes current Arabic category gaps: yes" in handoff_readiness_text, "submission handoff report checks Arabic category gaps", errors)
    check("Handoff records decided Vendor ID state: yes" in handoff_readiness_text, "submission handoff report records decided Vendor ID state", errors)
    check(
        "Handoff records decided authorship/namecheck/public URL state: yes" in handoff_readiness_text,
        "submission handoff report records decided authorship/namecheck/public URL state",
        errors,
    )
    check("Handoff records decided Article flow: yes" in handoff_readiness_text, "submission handoff report records decided Article flow", errors)
    check(
        "Handoff avoids stale Vendor ID confirmation blocker: yes" in handoff_readiness_text,
        "submission handoff report avoids stale Vendor ID blocker",
        errors,
    )
    check(
        "Handoff avoids stale authorship/public URL confirmation blocker: yes" in handoff_readiness_text,
        "submission handoff report avoids stale authorship/public URL blocker",
        errors,
    )
    check(
        "Handoff avoids stale Article URL confirmation blocker: yes" in handoff_readiness_text,
        "submission handoff report avoids stale Article URL blocker",
        errors,
    )
    check("Template includes repository maintenance checkbox: yes" in handoff_readiness_text, "submission handoff report checks template maintenance checkbox", errors)
    check("Handoff includes repository maintenance checkbox: yes" in handoff_readiness_text, "submission handoff report checks handoff maintenance checkbox", errors)
    check("Repository maintenance confirmation remains unchecked until issue opening: yes" in handoff_readiness_text, "submission handoff report keeps maintenance checkbox unchecked until final issue", errors)
    check("Handoff points to Arabic review packet: yes" in handoff_readiness_text, "submission handoff report checks Arabic review packet link", errors)
    check("Handoff points to decision readiness report: yes" in handoff_readiness_text, "submission handoff report checks decision readiness link", errors)
    check("Handoff points to release/source readiness report: yes" in handoff_readiness_text, "submission handoff report checks release/source report link", errors)
    check("Handoff points to release archive manifest: yes" in handoff_readiness_text, "submission handoff report checks release archive manifest link", errors)
    check("Handoff points to GitHub release draft and notes: yes" in handoff_readiness_text, "submission handoff report checks GitHub release draft and notes links", errors)
    check("Release archive manifest validates local review zip:" in handoff_readiness_text, "submission handoff report checks release archive local zip validation", errors)
    check("Handoff points to upstream structure readiness report: yes" in handoff_readiness_text, "submission handoff report checks upstream structure link", errors)
    check("Handoff points to package source-file audit: yes" in handoff_readiness_text, "submission handoff report checks package source audit link", errors)
    check("Handoff points to package dry-run readiness report: yes" in handoff_readiness_text, "submission handoff report checks package dry-run readiness link", errors)
    check("Handoff points to downstream metadata readiness report: yes" in handoff_readiness_text, "submission handoff report checks downstream metadata link", errors)
    check("Handoff points to Article readiness report: yes" in handoff_readiness_text, "submission handoff report checks Article readiness link", errors)
    check("Handoff points to authorship and AI disclosure report: yes" in handoff_readiness_text, "submission handoff report checks authorship and AI disclosure link", errors)
    check("Handoff points to PR identity readiness report: yes" in handoff_readiness_text, "submission handoff report checks PR identity link", errors)
    check("Handoff points to designer profile reports: yes" in handoff_readiness_text, "submission handoff report checks designer profile links", errors)
    check("Handoff points to DrawBot fork runtime report: yes" in handoff_readiness_text, "submission handoff report checks DrawBot fork runtime link", errors)
    check("Handoff points to local workflow readiness report: yes" in handoff_readiness_text, "submission handoff report checks local workflow link", errors)
    check("Handoff points to recent-package audit: yes" in handoff_readiness_text, "submission handoff report checks recent-package audit link", errors)
    check("Recent-package audit includes generated Packager merge evidence: yes" in handoff_readiness_text, "submission handoff report checks recent Packager merge evidence", errors)
    check("Handoff points to decision-linked warning reports: yes" in handoff_readiness_text, "submission handoff report checks decision-linked warning report links", errors)
    check("Handoff points to GF visual proof review packet: yes" in handoff_readiness_text, "submission handoff report checks kerning proof review packet link", errors)
    check("Handoff mentions decision-linked warning buckets: yes" in handoff_readiness_text, "submission handoff report checks decision-linked warning bucket mention", errors)
    check("Handoff points to final blocker summary: yes" in handoff_readiness_text, "submission handoff report checks final blocker summary link", errors)
    check("Handoff mentions expected Packager branch: yes" in handoff_readiness_text, "submission handoff report checks expected Packager branch", errors)
    check("Handoff mentions Packager source-mode options: yes" in handoff_readiness_text, "submission handoff report checks Packager source mode options", errors)
    check("Handoff mentions current package dry-run first blocker: yes" in handoff_readiness_text, "submission handoff report checks current package dry-run first blocker", errors)
    check("Handoff mentions current package dry-run blocking findings: yes" in handoff_readiness_text, "submission handoff report checks current package dry-run blocking findings", errors)
    check("Handoff mentions tracked package input count: yes" in handoff_readiness_text, "submission handoff report checks tracked package input count", errors)
    check("Handoff mentions untracked package input count: yes" in handoff_readiness_text, "submission handoff report checks untracked package input count", errors)
    check("Handoff mentions source-mode untracked input blockers: yes" in handoff_readiness_text, "submission handoff report checks source-mode untracked input blockers", errors)
    check("Handoff mentions downstream metadata check helper: yes" in handoff_readiness_text, "submission handoff report checks downstream metadata helper mention", errors)
    check("Handoff mentions prioritized decision packet: yes" in handoff_readiness_text, "submission handoff report checks prioritized decision packet mention", errors)
    check("Handoff mentions local drawbot-skia fork: yes" in handoff_readiness_text, "submission handoff report checks local drawbot-skia fork mention", errors)
    check("Decision readiness has mapped open questions: yes" in handoff_readiness_text, "submission handoff report checks decision readiness status", errors)
    check("Upstream structure has all mandatory paths: yes" in handoff_readiness_text, "submission handoff report checks upstream structure status", errors)
    check("Package source audit validates destination mapping: yes" in handoff_readiness_text, "submission handoff report checks package source audit status", errors)
    check("Downstream metadata preview has expected source block: yes" in handoff_readiness_text, "submission handoff report checks downstream metadata status", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in handoff_readiness_text, "submission handoff report cites GF package guide", errors)
    for source_file in [
        "OFL.txt",
        "fonts/variable/VirtuaGrotesk[wght].ttf",
        "documentation/ARTICLE.en_us.html",
        "documentation/readme-specimen.png",
    ]:
        check(
            f"`{source_file}`" in package_source_text,
            f"package source-file audit includes preview source file: {source_file}",
            errors,
        )
    check("defaults to `/Users/eli/GH/forks/fonts`" in text, "package checklist documents default local google/fonts fork", errors)
    check("documentation/pua-scope.md" in text, "package checklist includes PUA scope report", errors)
    check("article/ARTICLE.en_us.html" in text, "package checklist tracks Article package option", errors)
    check("primary_script: \"Arab\"" in text, "package checklist tracks Arabic primary script review", errors)
    check("category: \"SANS_SERIF\"" in text, "package checklist tracks category review", errors)
    check("stroke: \"SANS_SERIF\"" in text, "package checklist tracks stroke review", errors)
    check("source.files" in text and "article/ARTICLE.en_us.html" in text, "package checklist tracks source file mappings for Article assets", errors)
    check("variable TTF is still ignored/generated" in text, "package checklist tracks generated binary source strategy review", errors)
    check(
        "upstream_info.md" in text and "optional" in text.lower(),
        "package checklist tracks optional upstream_info provenance",
        errors,
    )
    check(
        "upstream.yaml" in text and "Packager emits" in text,
        "package checklist tracks upstream.yaml review",
        errors,
    )
    check("tags as PR/release-review metadata" in text, "package checklist treats tags as PR review metadata", errors)
    check("No custom `sample_text` block" in text, "package checklist tracks sample_text omission by default", errors)
    check("namecheck.fontdata.com" in text, "package checklist tracks current Add Font issue namecheck requirement", errors)
    check("AI-use disclosure" in text, "package checklist tracks current Add Font issue AI disclosure requirement", errors)
    check("copyright-authorship" in text, "package checklist tracks current Add Font issue authorship requirement", errors)
    check("combined copyright-author and" in text, "package checklist tracks combined copyright and AI checkbox", errors)
    check("I New Font, II Submission" in text, "package checklist tracks current Add Font default labels", errors)
    check("PUA" in text and "METADATA.pb" in text, "package checklist tracks PUA decision before METADATA review", errors)
    check("documentation/fontspector-warnings.md" in text, "package checklist includes Fontspector warnings report", errors)
    check("Decision-linked WARNs are recorded or resolved" in text, "package checklist tracks decision-linked warning resolution", errors)
    check("**Font Project Git Repo URL:**" in handoff_text, "submission handoff follows current Add Font issue template repo URL prompt", errors)
    check("**Super short description of the Font Family:**" in handoff_text, "submission handoff follows current Add Font issue template description prompt", errors)
    check("I New Font, II Submission" in handoff_text, "submission handoff records current Add Font default labels", errors)
    check("google-fonts-add-font-template-audit.md" in handoff_text, "submission handoff points to generated Add Font template audit", errors)
    check("recent-google-fonts-packages.md" in handoff_text, "submission handoff points to generated recent-package audit", errors)
    check("source files are available in the repo" in handoff_text, "submission handoff tracks source-files-in-repo checkbox", errors)
    check("I am the sole copyright author" in handoff_text and "AI tools" in handoff_text, "submission handoff tracks combined copyright and AI checkbox", errors)
    check("app-menu family name is definitive" in handoff_text, "submission handoff tracks definitive app-menu name checkbox", errors)
    check("copyright holder's full name or acronym" in handoff_text, "submission handoff tracks app-menu copyright-name constraint", errors)
    check("full [Google Fonts contributing requirements]" in handoff_text, "submission handoff tracks GF contributing requirements checkbox", errors)
    check("The font supports at least the Google Fonts `GF_Latin_Core` glyphset" in handoff_text, "submission handoff tracks GF Latin Core issue checkbox", errors)
    check("AI-use disclosure" in handoff_text, "submission handoff tracks AI-use disclosure", errors)
    check("namecheck.fontdata.com" in handoff_text, "submission handoff tracks namecheck requirement", errors)
    check(
        "documentation/vendor-id-readiness.md" in handoff_text
        and "documentation/kerning-readiness.md" in handoff_text
        and "documentation/avar-readiness.md" in handoff_text
        and "documentation/pua-scope.md" in handoff_text
        and "documentation/glyph-reachability.md" in handoff_text
        and "documentation/fontspector-warnings.md" in handoff_text,
        "submission handoff points to decision-linked warning evidence reports",
        errors,
    )
    check(
        "decision-linked warning buckets" in handoff_text
        and "vendor ID, kerning, `avar`" in handoff_text
        and "PUA/reachability" in handoff_text,
        "submission handoff groups decision-linked warning buckets",
        errors,
    )
    check(
        "documentation/google-fonts-language-metadata.md" in handoff_text
        and "documentation/arabic-review-packet.md" in handoff_text
        and 'primary_script: "Arab"' in handoff_text
        and 'subsets: "arabic"' in handoff_text,
        "submission handoff tracks Arabic language metadata report",
        errors,
    )
    check(
        "documentation/arabic-review-packet.md" in handoff_text
        and "documentation/missing-gf-arabic-core.md" in handoff_text
        and "documentation/arabic-mark-readiness.md" in handoff_text
        and "documentation/arabic-shaping-smoke-test.md" in handoff_text,
        "submission handoff points to Arabic coverage, marks, and shaping packet",
        errors,
    )
    check("GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in handoff_text, "submission handoff documents selected latest-release package dry-run command", errors)
    check("make downstream-metadata-check" in handoff_text, "submission handoff documents downstream metadata check command", errors)
    check("documentation/github-release-draft.md" in handoff_text, "submission handoff points to GitHub release draft", errors)
    check("documentation/github-release-notes.md" in handoff_text, "submission handoff points to GitHub release notes", errors)
    check(
        "GitHub release download URL ending in `.zip`" in handoff_text
        and "final GitHub release download `.zip` asset" in handoff_text,
        "submission handoff documents latest-release archive URL shape",
        errors,
    )
    check("scripts/prepare_downstream_metadata.py --apply" in handoff_text, "submission handoff documents explicit downstream metadata apply command", errors)
    check("gh auth login -h github.com" in handoff_text, "submission handoff documents GitHub CLI auth refresh command", errors)
    check("gh auth status -h github.com" in handoff_text, "submission handoff documents GitHub CLI auth status command", errors)
    check("git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk" in handoff_text, "submission handoff documents scoped google/fonts status command", errors)
    check("./venv/bin/python scripts/prepare_downstream_metadata.py --apply" in handoff_text, "submission handoff documents checked downstream metadata apply command", errors)
    check("Latest local dry-run status, 2026-05-24" in handoff_text, "submission handoff has current dry-run status date", errors)
    check("Current dry-run status, 2026-05-24" in text, "package checklist has current dry-run status date", errors)
    check("4/5 are tracked by git" in handoff_text, "submission handoff records tracked package input count", errors)
    check("1/5 is currently untracked" in handoff_text, "submission handoff records untracked package input count", errors)
    check(
        "default branch packaging must expose untracked `source.files`" in handoff_text
        and "release/archive\npackaging must include those untracked local source files" in handoff_text
        and "build-from-source\npackaging must keep the source build path public and tracked" in handoff_text,
        "submission handoff records source-mode-specific untracked input blockers",
        errors,
    )
    check(
        package_first_blocker
        and package_first_blocker in handoff_text
        and package_first_blocker in text,
        "submission handoff and package checklist include current package dry-run first blocker",
        errors,
    )
    check(
        package_blocking_findings
        and package_blocking_findings in handoff_text
        and package_blocking_findings in text,
        "submission handoff and package checklist include current package dry-run blocking findings",
        errors,
    )
    check(
        package_reaches_packager
        and f"Wrapper can reach Packager: {package_reaches_packager}" in handoff_text
        and f"Wrapper can reach Packager: {package_reaches_packager}" in text,
        "submission handoff and package checklist include current package dry-run reachability",
        errors,
    )
    variable_version = generated_variable_version(generated_metadata_text)
    issue_version = variable_version.removeprefix("Version ")
    check(
        variable_version
        and f"- Version: {issue_version}" in handoff_text
        and f"generated fonts expose version `{issue_version}`" in handoff_text,
        "submission handoff version matches generated font metadata",
        errors,
    )
    latin_missing = report_count(latin_report_text, "Missing codepoints")
    check(
        latin_missing is not None
        and f"GF Latin Core missing codepoints: {latin_missing}" in handoff_text,
        "submission handoff Latin Core gap count matches generated report",
        errors,
    )
    production_summary_match = re.search(
        r"Fontspector googlefonts profile: (?P<summary>\d+ FAIL, \d+ WARN, \d+ PASS)",
        production_requirements_text,
    )
    if production_summary_match:
        production_summary = production_summary_match.group("summary")
    else:
        report_summary = re.search(
            r"Summary: .*?PASS: (?P<pass>\d+) WARN: (?P<warn>\d+) FAIL: (?P<fail>\d+)",
            full_report_text,
        )
        production_summary = (
            f"{report_summary.group('fail')} FAIL, {report_summary.group('warn')} WARN, {report_summary.group('pass')} PASS"
            if report_summary
            else ""
        )
    expected_fontspector_summary = f"Current Fontspector googlefonts profile: {production_summary}" if production_summary else ""
    check(
        expected_fontspector_summary
        and expected_fontspector_summary in handoff_text
        and "documentation/fontspector-googlefonts-report.md" in handoff_text,
        "submission handoff Fontspector snapshot matches generated report",
        errors,
    )
    for label, heading in [
        ("Arabic letters", "## Arabic letters"),
        ("Arabic marks", "## Arabic marks"),
        ("Arabic numbers", "## Arabic numbers"),
        ("Arabic punctuation and symbols", "## Arabic punctuation and symbols"),
        ("Shared punctuation and symbols", "## Shared punctuation and symbols"),
    ]:
        count = section_missing_count(arabic_report_text, heading)
        check(
            count is not None and f"{label}: {count}" in handoff_text,
            f"submission handoff Arabic Core gap count matches generated report: {label}",
            errors,
        )
    check("app-menu family name" in decisions_text and "copyright holder full names or acronyms" in decisions_text, "decision log tracks app-menu naming constraint", errors)
    check("app-menu family name" in questions_text and "copyright holder full names or acronyms" in questions_text, "decision questions track app-menu naming constraint", errors)
    check("# Google Fonts Release Checklist" in release_text, "release checklist has expected heading", errors)
    check("Suggested first-submission tag shape:" in release_text, "release checklist documents tag shape", errors)
    check("v1.000" in release_text, "release checklist records first-submission tag recommendation", errors)
    check("documentation/release-metadata.md" in release_text, "release checklist points to generated release metadata report", errors)
    check("documentation/release-source-readiness.md" in release_text, "release checklist points to release/source readiness report", errors)
    check("Upstream URL: https://github.com/eliheuer/virtua-grotesk" in release_text, "release checklist tracks decided upstream URL", errors)
    check("https://googlefonts.github.io/gf-guide/upstream.html" in release_text, "release checklist cites GF upstream guide", errors)
    check("https://googlefonts.github.io/gf-guide/package.html" in release_text, "release checklist cites GF package guide", errors)
    check("documentation/ARTICLE.en_us.html" in release_text, "release checklist includes Article review", errors)
    check(
        "documentation/google-fonts-downstream-package-preview.md" in release_text,
        "release checklist includes downstream package preview",
        errors,
    )


def proof_runtime_errors(errors: list[str]) -> None:
    makefile_text = (ROOT / "Makefile").read_text()
    proof_text = (ROOT / "proof.py").read_text()
    readme_text = (ROOT / "README.md").read_text()
    gf_readiness_text = (ROOT / "GF_READINESS.md").read_text()
    tooling_text = (ROOT / "documentation/python-tooling-notes.md").read_text()
    drawbot_report_text = (ROOT / "documentation/drawbot-runtime-readiness.md").read_text()
    agents_text = (ROOT / "AGENTS.md").read_text()
    claude_text = (ROOT / "CLAUDE.md").read_text()
    proof_skill_text = (ROOT / ".claude/skills/proof/SKILL.md").read_text()
    claude_settings_text = (ROOT / ".claude/settings.json").read_text()
    check(
        "DRAWBOT_SKIA_REPO ?= /Users/eli/GH/repos/drawbot-skia" in makefile_text,
        "Makefile points proof generation at local eliheuer/drawbot-skia checkout",
        errors,
    )
    check(
        "DRAWBOT_PYTHON ?= $(DRAWBOT_SKIA_REPO)/.venv/bin/python" in makefile_text,
        "Makefile uses drawbot-skia venv for proof generation",
        errors,
    )
    check(
        'PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src' in makefile_text,
        "Makefile prepends drawbot-skia src to PYTHONPATH for proof generation",
        errors,
    )
    check(
        "from drawbot_skia.drawing import Drawing" in proof_text,
        "proof.py supports drawbot-skia Drawing API",
        errors,
    )
    check(
        "import drawBot as db" not in proof_text,
        "proof.py requires eliheuer/drawbot-skia instead of generic DrawBot fallback",
        errors,
    )
    check(
        "/Users/eli/GH/repos/drawbot-skia" in readme_text
        and "/Users/eli/GH/repos/drawbot-skia" in gf_readiness_text
        and "/Users/eli/GH/repos/drawbot-skia" in tooling_text,
        "human-facing docs record eliheuer/drawbot-skia proof runtime",
        errors,
    )
    check(
        "eliheuer/drawbot-skia" in agents_text and "eliheuer/drawbot-skia" in claude_text,
        "agent-facing docs record eliheuer/drawbot-skia proof runtime",
        errors,
    )
    check(
        "eliheuer/drawbot-skia" in proof_skill_text,
        "proof skill records eliheuer/drawbot-skia proof runtime",
        errors,
    )
    check(
        "classic `drawBot`" not in proof_skill_text
        and "classic drawBot" not in proof_skill_text,
        "proof skill does not document a classic DrawBot fallback",
        errors,
    )
    check(
        "basic-fonts" not in proof_skill_text
        and "basic-fonts" not in claude_settings_text
        and "basic-fonts" not in makefile_text,
        "proof workflow does not point to stale basic-fonts DrawBot runtime",
        errors,
    )
    check(
        "drawbot-skia/.venv/bin/python proof.py" in claude_settings_text,
        "Claude settings allow drawbot-skia proof command",
        errors,
    )
    check(
        "Origin is Eli Heuer fork: yes" in drawbot_report_text,
        "generated DrawBot runtime report verifies eliheuer/drawbot-skia origin",
        errors,
    )
    check(
        "Expected fork origin owner/repo: `eliheuer/drawbot-skia`" in drawbot_report_text
        and "Accepted origin URL forms:" in drawbot_report_text,
        "generated DrawBot runtime report accepts SSH or HTTPS origin forms for eliheuer/drawbot-skia",
        errors,
    )
    check(
        "Drawing API importable: yes" in drawbot_report_text,
        "generated DrawBot runtime report verifies Drawing API import",
        errors,
    )
    check(
        "`proof.py` requires eliheuer/drawbot-skia instead of generic DrawBot: yes" in drawbot_report_text,
        "generated DrawBot runtime report verifies proof.py requires eliheuer/drawbot-skia",
        errors,
    )
    check(DRAWBOT_SKIA_REPO.exists(), "local eliheuer/drawbot-skia checkout exists", errors)
    if DRAWBOT_SKIA_REPO.exists():
        drawbot_origin = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=DRAWBOT_SKIA_REPO,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        ).stdout.strip()
        check(
            drawbot_origin in EXPECTED_DRAWBOT_ORIGINS,
            "local drawbot-skia origin is eliheuer/drawbot-skia",
            errors,
        )
    check(DRAWBOT_SKIA_PYTHON.exists(), "local drawbot-skia Python exists", errors)
    check(DRAWBOT_SKIA_SRC.exists(), "local drawbot-skia src directory exists", errors)
    if DRAWBOT_SKIA_PYTHON.exists() and DRAWBOT_SKIA_SRC.exists():
        result = subprocess.run(
            [
                str(DRAWBOT_SKIA_PYTHON),
                "-c",
                "from drawbot_skia.drawing import Drawing; db = Drawing(); assert hasattr(db, 'saveImage')",
            ],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(DRAWBOT_SKIA_SRC)},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        check(result.returncode == 0, "drawbot-skia Drawing API is importable for proof generation", errors)


def descriptive_artifact_errors(errors: list[str]) -> None:
    metadata_apply_blockers = downstream_metadata_apply_blockers()
    readme_text = (ROOT / "README.md").read_text()
    tooling_text = (ROOT / "documentation/python-tooling-notes.md").read_text()
    article_readiness_text = (ROOT / "documentation/article-readiness.md").read_text()
    article_text = (ROOT / "documentation/ARTICLE.en_us.html").read_text()
    agents_text = (ROOT / "AGENTS.md").read_text()
    claude_text = (ROOT / "CLAUDE.md").read_text()
    manual_handoff_text = (ROOT / "documentation/manual-cleanup-handoff.md").read_text()
    reusable_agents_text = (ROOT / ".agents/google-fonts-onboarding-checklists.md").read_text()
    reusable_reference_map_text = (ROOT / ".agents/google-fonts-official-reference-map.md").read_text()
    reusable_onboarding_skill_text = (ROOT / ".agents/skills/google-fonts-onboarding/SKILL.md").read_text()
    reusable_qa_skill_text = (ROOT / ".agents/skills/google-fonts-qa/SKILL.md").read_text()
    reusable_packaging_skill_text = (ROOT / ".agents/skills/google-fonts-packaging/SKILL.md").read_text()
    reusable_nonlatin_skill_text = (ROOT / ".agents/skills/google-fonts-nonlatin-drawing/SKILL.md").read_text()
    agent_reuse_report_text = (ROOT / "documentation/google-fonts-agent-reuse-readiness.md").read_text()
    workflow_texts = {
        "AGENTS.md": agents_text,
        "CLAUDE.md": claude_text,
        ".claude/skills/build-font/SKILL.md": (ROOT / ".claude/skills/build-font/SKILL.md").read_text(),
        ".claude/skills/edit-glyph/SKILL.md": (ROOT / ".claude/skills/edit-glyph/SKILL.md").read_text(),
        ".claude/skills/font-qa/SKILL.md": (ROOT / ".claude/skills/font-qa/SKILL.md").read_text(),
        ".claude/skills/proof/SKILL.md": (ROOT / ".claude/skills/proof/SKILL.md").read_text(),
        ".claude/skills/render-specimen/SKILL.md": (ROOT / ".claude/skills/render-specimen/SKILL.md").read_text(),
        ".claude/rules/design-philosophy.md": (ROOT / ".claude/rules/design-philosophy.md").read_text(),
        ".claude/rules/designspace-editing.md": (ROOT / ".claude/rules/designspace-editing.md").read_text(),
        ".claude/rules/kerning-editing.md": (ROOT / ".claude/rules/kerning-editing.md").read_text(),
        ".claude/rules/ufo-editing.md": (ROOT / ".claude/rules/ufo-editing.md").read_text(),
    }
    description_text = (ROOT / "documentation/DESCRIPTION.en_us.html").read_text()
    image_license_text = (ROOT / "documentation/image-license.txt").read_text()
    readme_image = ROOT / "documentation/readme-specimen.png"

    check("Virtua Grotesk is" in readme_text, "README includes a short family description", errors)
    check("](documentation/readme-specimen.png)" in readme_text, "README references the specimen image", errors)
    check("## Changelog" in readme_text, "README includes GF-recommended changelog section", errors)
    check("## Credits" in readme_text, "README includes GF-recommended credits section", errors)
    check("## License" in readme_text, "README includes GF-recommended license section", errors)
    check("SIL Open Font License" in readme_text, "README mentions the OFL license", errors)
    for reusable_path in [
        ".agents/google-fonts-onboarding-checklists.md",
        ".agents/google-fonts-official-reference-map.md",
        ".agents/skills/google-fonts-onboarding/SKILL.md",
        ".agents/skills/google-fonts-qa/SKILL.md",
        ".agents/skills/google-fonts-packaging/SKILL.md",
        ".agents/skills/google-fonts-nonlatin-drawing/SKILL.md",
    ]:
        check(reusable_path in readme_text, f"README links reusable Google Fonts agent artifact: {reusable_path}", errors)
        check(reusable_path in agents_text, f"AGENTS.md links reusable Google Fonts agent artifact: {reusable_path}", errors)
    check("documentation/manual-cleanup-handoff.md" in readme_text, "README links manual cleanup handoff checkpoint", errors)
    check("documentation/manual-cleanup-handoff.md" in agents_text, "AGENTS.md links manual cleanup handoff checkpoint", errors)
    check(
        "# Manual Cleanup Handoff" in manual_handoff_text
        and "make preflight" in manual_handoff_text
        and "make contour-cleanup-proof" in manual_handoff_text
        and "make ufo-editor-check" in manual_handoff_text
        and "make runebender-ufo-check" in manual_handoff_text
        and "make arabic-snapshot-integrity" in manual_handoff_text
        and "make arabic-manual-review-batches" in manual_handoff_text
        and "make arabic-current-review-worksheet" in manual_handoff_text
        and "make arabic-first-review-batch" in manual_handoff_text
        and "make arabic-manual-edit-targets" in manual_handoff_text
        and "make arabic-hand-review-session" in manual_handoff_text
        and "make arabic-hand-review-contact-sheet" in manual_handoff_text
        and "documentation/arabic-snapshot-integrity.md" in manual_handoff_text
        and "documentation/arabic-manual-review-batches.md" in manual_handoff_text
        and "documentation/arabic-current-review-worksheet.md" in manual_handoff_text
        and "documentation/arabic-first-review-batch.md" in manual_handoff_text
        and "documentation/arabic-manual-edit-targets.md" in manual_handoff_text
        and "documentation/arabic-hand-review-session.md" in manual_handoff_text
        and "documentation/arabic-hand-review-contact-sheet.html" in manual_handoff_text
        and "documentation/contour-cleanup-review-queue.md" in manual_handoff_text
        and "documentation/contour-cleanup-edit-plan.md" in manual_handoff_text
        and "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in manual_handoff_text
        and "Do not use Packager PR mode" in manual_handoff_text,
        "manual cleanup handoff records resume commands, editor checks, snapshot integrity, contour proof, and Packager PR guard",
        errors,
    )
    check(
        "Copy this file" in reusable_agents_text
        and "replace family-specific paths" in reusable_agents_text
        and "refresh official Google Fonts docs" in reusable_agents_text,
        "reusable Google Fonts checklist is portable to future font repos",
        errors,
    )
    check(
        "Last checked: 2026-05-25." in reusable_reference_map_text
        and "https://googlefonts.github.io/gf-guide/onboarding.html" in reusable_reference_map_text
        and "https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md" in reusable_reference_map_text
        and "Reusable Report Set" in reusable_reference_map_text
        and "make preflight" in reusable_reference_map_text,
        "reusable Google Fonts official reference map records checked docs, templates, and gate shape",
        errors,
    )
    check("# Google Fonts Agent Reuse Readiness" in agent_reuse_report_text, "agent reuse readiness report has expected heading", errors)
    check("Reusable agent bundle ready: yes" in agent_reuse_report_text, "agent reuse readiness report confirms reusable bundle readiness", errors)
    check("Required reusable agent files present: 7 / 7" in agent_reuse_report_text, "agent reuse readiness report confirms required file coverage", errors)
    check("Official Google Fonts references mapped: 13 / 13" in agent_reuse_report_text, "agent reuse readiness report confirms official reference coverage", errors)
    check("Portable gate shape present: yes" in agent_reuse_report_text, "agent reuse readiness report confirms portable gate shape", errors)
    check(".agents/google-fonts-official-reference-map.md" in agent_reuse_report_text, "agent reuse readiness report includes official reference map", errors)
    for label, text in [
        ("Google Fonts onboarding skill", reusable_onboarding_skill_text),
        ("Google Fonts QA skill", reusable_qa_skill_text),
        ("Google Fonts packaging skill", reusable_packaging_skill_text),
        ("Google Fonts non-Latin drawing skill", reusable_nonlatin_skill_text),
    ]:
        check("https://googlefonts.github.io/gf-guide/" in text or "Google Fonts" in text, f"{label} records Google Fonts context", errors)
        check("portable" in text or "Portable" in text or "copy" in text, f"{label} is written for reuse beyond Virtua Grotesk", errors)
    check("contact sheet" in reusable_agents_text, "reusable checklist records non-Latin contact-sheet review pattern", errors)
    check("contact sheet" in reusable_nonlatin_skill_text, "non-Latin drawing skill records contact-sheet review pattern", errors)
    check(
        "treat Fontspector as this" in readme_text
        and "repo's QA entrypoint" in readme_text
        and "Google Fonts upstream/template" in readme_text,
        "README clarifies Fontspector is the local QA entrypoint despite older template references",
        errors,
    )
    check("`~/.fontspector`" in readme_text, "README documents persistent Fontspector directory", errors)
    check(
        "requirements.txt` is\n"
        "the pinned install snapshot" in readme_text,
        "README documents pinned requirements.txt snapshot",
        errors,
    )
    check(
        "`requirements.txt` is the pinned install snapshot" in tooling_text
        and "./venv/bin/python -m pip freeze --all > requirements.txt" in tooling_text,
        "Python tooling notes document pinned requirements refresh path",
        errors,
    )
    check(
        "Those are not project entrypoints" in tooling_text
        and "Use\nFontspector for Google Fonts QA" in tooling_text,
        "Python tooling notes clarify transitive FontBakery pins are not QA entrypoints",
        errors,
    )
    check(
        "Older Google Fonts upstream/template" in tooling_text
        and "do not replace the local" in tooling_text
        and "Fontspector workflow" in tooling_text,
        "Python tooling notes clarify Fontspector vs legacy FontBakery references",
        errors,
    )
    check("`~/.fontspector`" in tooling_text, "Python tooling notes document persistent Fontspector directory", errors)
    check(
        'mkdir -p "$HOME/.fontspector"' in (ROOT / "scripts/check_gf_fonts.sh").read_text(),
        "Fontspector QA script uses persistent local Fontspector directory",
        errors,
    )
    check(
        'mkdir -p "$HOME/.fontspector"' in (ROOT / "scripts/report_fontspector_markdown.sh").read_text(),
        "Fontspector report script uses persistent local Fontspector directory",
        errors,
    )
    for label, text in [("AGENTS.md", agents_text), ("CLAUDE.md", claude_text)]:
        check("make preflight" in text, f"{label} documents current preflight command", errors)
        check("make test" in text, f"{label} documents current Fontspector command", errors)
        check("make kerning-proof-check" in text, f"{label} documents current gftools QA proof command", errors)
        check("make kerning-proof-review-check" in text, f"{label} documents current gftools QA proof review command", errors)
        check("make designer-profile-prepare-check" in text, f"{label} documents designer profile prepare command", errors)
        check("documentation/kerning-proof-review.md" in text, f"{label} links kerning proof review packet", errors)
        check("documentation/core-qa-process.md" in text, f"{label} links core QA process document", errors)
        check(
            "`make kerning-proof-check` is part of the core visual QA process" in text,
            f"{label} marks gftools QA proof review as core agent QA",
            errors,
        )
        check(".Codex/" not in text, f"{label} does not point to stale .Codex path", errors)
        check(".claude/rules/design-philosophy.md" in text, f"{label} links to existing design philosophy rules", errors)
    check(
        "`make kerning-proof-check` is part of the core visual QA process" in agents_text
        and "Agents should regenerate or re-review that proof" in agents_text,
        "AGENTS.md marks gftools QA proof review as core agent QA",
        errors,
    )
    for label, text in workflow_texts.items():
        check("--check masters" not in text, f"{label} does not point to stale master-check flag", errors)
        check("--check kerning" not in text, f"{label} does not point to stale kerning-check flag", errors)
        check("Semi-Bold" not in text, f"{label} uses GF-style SemiBold spelling", errors)
        check(
            "gftools builder config.yaml" not in text,
            f"{label} does not point to stale root gftools config path",
            errors,
        )
        check("fonts/VirtuaGrotesk-Regular.ttf" not in text, f"{label} does not point to stale flat regular TTF path", errors)
        check("fonts/VirtuaGrotesk-VF.ttf" not in text, f"{label} does not point to stale flat VF path", errors)
        if label != ".claude/skills/font-qa/SKILL.md":
            check("/font-qa" not in text, f"{label} does not point to stale /font-qa command", errors)
    build_skill_text = workflow_texts[".claude/skills/build-font/SKILL.md"]
    check(
        "gftools builder sources/config.yaml" in build_skill_text,
        "build-font skill documents sources/config.yaml builder path",
        errors,
    )
    check(readme_image.stat().st_size > 0, "README specimen image is nonempty", errors)
    check("readme-specimen.png" in image_license_text, "image license file documents README specimen", errors)
    check("Article draft" in image_license_text, "image license file documents Article image use", errors)
    check("third-party" in image_license_text, "image license file states third-party asset provenance", errors)
    check("# Article Readiness" in article_readiness_text, "Article readiness report has expected heading", errors)
    check("More than 100 text characters: yes" in article_readiness_text, "Article readiness report checks text length", errors)
    check("Around 500 words target met: yes" in article_readiness_text, "Article readiness report checks GF word-count target", errors)
    check("Primary script target from metadata: `Arab`" in article_readiness_text, "Article readiness report records primary script target", errors)
    check(
        re.search(r"Localized Arabic text present: (yes|no)", article_readiness_text) is not None,
        "Article readiness report checks Arabic/localized text presence",
        errors,
    )
    check("Upstream repository link present: yes" in article_readiness_text, "Article readiness report checks upstream link", errors)
    check("Placeholder upstream URL still present: no" in article_readiness_text, "Article readiness report records applied upstream URL decision", errors)
    check("Referenced images exist locally: yes" in article_readiness_text, "Article readiness report checks image existence", errors)
    check("Raster images within 1.75 MB limit: yes" in article_readiness_text, "Article readiness report checks image size limit", errors)
    check("Images meet 1000 px recommended width: yes" in article_readiness_text, "Article readiness report checks recommended image width", errors)
    check("Image license/provenance file exists: yes" in article_readiness_text, "Article readiness report checks image provenance file", errors)
    check(
        "Article image sources covered by provenance file: 1 / 1" in article_readiness_text,
        "Article readiness report checks image provenance coverage",
        errors,
    )
    check("Forbidden HTML tags: 0" in article_readiness_text, "Article readiness report checks forbidden tags", errors)
    check("https://googlefonts.github.io/gf-guide/article.html" in article_readiness_text, "Article readiness report cites GF Article guide", errors)

    check("<p>" in article_text and "</p>" in article_text, "ARTICLE uses paragraph HTML", errors)
    check("<figure>" in article_text and "<figcaption>" in article_text, "ARTICLE includes a figure with caption", errors)
    article_image_refs = re.findall(r'<img\s+[^>]*src="([^"]+)"', article_text)
    check(bool(article_image_refs), "ARTICLE includes at least one image", errors)
    for image_ref in article_image_refs:
        image_path = ROOT / "documentation" / image_ref
        check(image_path.exists(), f"ARTICLE image exists: {image_ref}", errors)
        check(image_ref in image_license_text, f"ARTICLE image provenance is documented: {image_ref}", errors)
        if image_path.exists():
            image_size = image_path.stat().st_size
            check(image_size <= 1.75 * 1024 * 1024, f"ARTICLE image is within 1.75 MB limit: {image_ref}", errors)
            try:
                width, height = png_dimensions(image_path)
            except ValueError as exc:
                check(False, f"ARTICLE image dimensions readable: {image_ref} ({exc})", errors)
            else:
                check(width >= 1000, f"ARTICLE image width is at least 1000px: {image_ref} ({width}x{height})", errors)
    check("readme-specimen.png" in article_text, "ARTICLE references the generated specimen image", errors)
    check("Virtua Grotesk" in article_text, "ARTICLE names the family", errors)
    ofl_first_line = (ROOT / "OFL.txt").read_text().splitlines()[0]
    ofl_url_match = re.search(r"\((https://github\.com/[^)]+)\)", ofl_first_line)
    ofl_url = ofl_url_match.group(1) if ofl_url_match else ""
    check(bool(ofl_url) and ofl_url in article_text, "ARTICLE link matches OFL upstream URL", errors)
    check("TODO" not in article_text and "Pending" not in article_text, "ARTICLE contains no TODO placeholders", errors)
    check(
        "Google Fonts submission" not in article_text,
        "ARTICLE does not expose internal submission wording",
        errors,
    )
    check(
        "reviewed against" not in article_text,
        "ARTICLE does not expose internal review wording",
        errors,
    )
    normalized_article = f" {article_text.lower()} "
    first_person_markers = (" I ", " me ", " my ", " we ", " our ")
    check(
        not any(marker in normalized_article for marker in first_person_markers),
        "ARTICLE is not written in first person",
        errors,
    )
    check("<p>" in description_text and "</p>" in description_text, "DESCRIPTION uses paragraph HTML", errors)
    check("Virtua Grotesk" in description_text, "DESCRIPTION names the family", errors)
    check("TODO" not in description_text, "DESCRIPTION contains no TODO placeholders", errors)
    check(
        "Google Fonts submission" not in description_text,
        "DESCRIPTION does not expose internal submission wording",
        errors,
    )
    check(
        "reviewed against" not in description_text,
        "DESCRIPTION does not expose internal review wording",
        errors,
    )
    normalized_description = f" {description_text.lower()} "
    check(
        not any(marker in normalized_description for marker in first_person_markers),
        "DESCRIPTION is not written in first person",
        errors,
    )

    placeholder_audit_path = ROOT / "documentation" / "open-placeholder-audit.md"
    check(placeholder_audit_path.exists(), "open placeholder audit report exists", errors)
    if placeholder_audit_path.exists():
        placeholder_audit_text = placeholder_audit_path.read_text()
        check(
            "Placeholder upstream URL occurrences:" in placeholder_audit_text
            and "Public placeholder blocker count: 0" in placeholder_audit_text,
            "open placeholder audit tracks placeholder upstream URL occurrences",
            errors,
        )
        check(
            "Pending decision markers:" in placeholder_audit_text,
            "open placeholder audit tracks pending decision markers",
            errors,
        )
        check(
            "Internal stale-placeholder guards: 1" in placeholder_audit_text,
            "open placeholder audit separates internal stale-placeholder guards",
            errors,
        )
        check(
            "Internal metadata guard markers: 5" in placeholder_audit_text,
            "open placeholder audit separates internal metadata guard markers",
            errors,
        )
        check(
            "Actionable placeholder upstream URL occurrences: 0" in placeholder_audit_text,
            "open placeholder audit separates actionable placeholder URL occurrences",
            errors,
        )
        check(
            "Actionable pending decision markers: 0" in placeholder_audit_text,
            "open placeholder audit separates actionable pending decision markers",
            errors,
        )
        check(
            "Generated evidence echoes: 2" in placeholder_audit_text
            and "## Generated Evidence Echoes" in placeholder_audit_text,
            "open placeholder audit separates generated evidence echoes",
            errors,
        )
        check(
            "Apply Before Downstream Packaging If Public Blockers Appear" in placeholder_audit_text
            and "Keep intentional stale-placeholder guard strings" in placeholder_audit_text,
            "open placeholder audit records conditional downstream packaging cleanup steps",
            errors,
        )

    public_upstream_path = ROOT / "documentation" / "public-upstream-readiness.md"
    check(public_upstream_path.exists(), "public upstream URL readiness report exists", errors)
    if public_upstream_path.exists():
        public_upstream_text = public_upstream_path.read_text()
        check("# Public Upstream URL Readiness" in public_upstream_text, "public upstream URL report has expected heading", errors)
        check("Origin fetch URL: `git@github.com:eliheuer/virtua-grotesk.git`" in public_upstream_text, "public upstream URL report records origin fetch URL", errors)
        check("Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`" in public_upstream_text, "public upstream URL report records normalized origin candidate", errors)
        check("Placeholder URL: `https://github.com/fontgarden/virtua-grotesk`" in public_upstream_text, "public upstream URL report records placeholder URL", errors)
        check("Origin candidate differs from placeholder: yes" in public_upstream_text, "public upstream URL report compares origin candidate with placeholder", errors)
        check("Placeholder or pending URL findings:" in public_upstream_text, "public upstream URL report tracks replacement finding count", errors)
        check("## Candidate Replacement Preview" in public_upstream_text, "public upstream URL report includes candidate replacement preview", errors)
        check("Candidate URL: `https://github.com/eliheuer/virtua-grotesk`" in public_upstream_text, "public upstream URL report previews normalized origin candidate", errors)
        check("Candidate copyright line: `Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)`" in public_upstream_text, "public upstream URL report previews copyright replacement", errors)
        check("Replacement Surface" in public_upstream_text and "Placeholder or pending URL findings: 0" in public_upstream_text, "public upstream URL report confirms replacement surface is clear", errors)
        check("Placeholder URL replacements:" in public_upstream_text, "public upstream URL report counts placeholder URL replacements", errors)
        check("Placeholder URL replacements: 0" in public_upstream_text, "public upstream URL report excludes stale-placeholder guard from replacements", errors)
        check("Pending URL field replacements:" in public_upstream_text, "public upstream URL report counts pending URL field replacements", errors)
        check("## Apply Helper Alignment" in public_upstream_text, "public upstream URL report checks apply-helper target alignment", errors)
        check("Report/helper target lists match: yes" in public_upstream_text, "public upstream URL report confirms helper/report target list match", errors)
        check("Missing from helper: none" in public_upstream_text, "public upstream URL report confirms no report targets are missing from helper", errors)
        check("Extra in helper: none" in public_upstream_text, "public upstream URL report confirms helper has no extra replacement targets", errors)
        check("## Stale Placeholder Guards" in public_upstream_text, "public upstream URL report documents stale-placeholder guards", errors)
        check(
            "Do not replace these with the" in public_upstream_text
            and "stale_placeholder_upstream_url" in public_upstream_text,
            "public upstream URL report preserves package dry-run stale-placeholder guard",
            errors,
        )
        check("OFL.txt" in public_upstream_text, "public upstream URL report includes OFL replacement surface", errors)
        check("Report target files: 11" in public_upstream_text, "public upstream URL report includes tracked replacement targets", errors)
        check("https://googlefonts.github.io/gf-guide/upstream.html" in public_upstream_text, "public upstream URL report cites GF upstream guide", errors)
        check(
            "Rerun `make preflight` so proof evidence and generated reports\n"
            "  stay synchronized, then run\n"
            "  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`" in public_upstream_text,
            "public upstream URL report uses synchronized preflight before Packager",
            errors,
        )
    public_upstream_helper_text = (ROOT / "scripts/apply_public_upstream_url.py").read_text()
    check("PLACEHOLDER_URL = \"https://github.com/fontgarden/virtua-grotesk\"" in public_upstream_helper_text, "public upstream URL helper preserves placeholder source", errors)
    check("PENDING_URL = \"Pending decision: public upstream URL\"" in public_upstream_helper_text, "public upstream URL helper handles pending URL field", errors)
    check("--apply" in public_upstream_helper_text, "public upstream URL helper is dry-run by default with explicit apply flag", errors)
    check("stale_placeholder_upstream_url" not in public_upstream_helper_text, "public upstream URL helper does not rewrite stale-placeholder guards", errors)
    check("documentation/google-fonts-downstream-package-preview.md" in public_upstream_helper_text, "public upstream URL helper updates downstream preview surface", errors)

    blocker_report_path = ROOT / "documentation" / "final-submission-blockers.md"
    check(blocker_report_path.exists(), "final-submission blocker report exists", errors)
    if blocker_report_path.exists():
        blocker_text = blocker_report_path.read_text()
        for expected in [
            "Maintainer decisions",
            "Decision readiness",
            "Placeholder strings",
            "Packager source files",
            "Selected release/archive package plan",
            "Build-from-source path",
            "Static package shape",
            "Downstream metadata preview",
            "Article package assets",
            "Family name and namecheck",
            "Authorship and AI disclosure",
            "PR identity and auth",
            "Downstream PR readiness",
            "DrawBot proof runtime",
            "Local workflow readiness",
            "Release metadata",
            "Release/source strategy",
            "Release archive manifest",
            "GitHub release draft",
            "Package dry-run readiness",
            "Upstream structure",
            "Local google/fonts fork",
            "Template and recent PR evidence",
            "Language metadata",
            "Project template automation",
            "Submission handoff",
            "Designer profile",
            "Vendor ID",
            "Kerning",
            "GF Latin Core coverage",
            "GF Arabic Core coverage",
            "Arabic source worklist",
            "Arabic manual edit targets",
            "Arabic shaping smoke test",
            "Arabic marks",
            "Numeric feature readiness",
            "Glyph reachability",
            "Fontspector warning triage",
            "Fontspector metadata preview probe",
            "Fontspector zero-warning path",
            "Fontspector googlefonts profile",
            "Contour/no-contour cleanup",
        ]:
            check(expected in blocker_text, f"final-submission blocker report tracks {expected}", errors)
        check(
            "version 1.000, tag v1.000, built/source match: yes" in blocker_text
            and "documentation/release-metadata.md" in blocker_text,
            "final-submission blocker report includes generated release metadata evidence",
            errors,
        )
        check(
            "tag exists:" in blocker_text
            and "clean tree:" in blocker_text
            and "ignored source files:" in blocker_text,
            "final-submission blocker report summarizes release/source strategy state",
            errors,
        )
        check(
            re.search(
                r"Release archive manifest \| inputs: 4/4; unsafe sources: 0; duplicates: 0; local zip: yes; expected files: yes; unsafe entries: no; hashes: (yes|no); URL filename: yes; final URL: pending",
                blocker_text,
            )
            is not None,
            "final-submission blocker report summarizes release archive manifest state",
            errors,
        )
        check(
            re.search(
                r"GitHub release draft \| tag: v1\.000; title: Virtua Grotesk 1\.000; command: yes; archive: `dist/VirtuaGrotesk-1\.000\.zip`; notes: `documentation/github-release-notes\.md`; notes final: no; expected files: yes; hashes: (yes|no); source commit: Pending final release/source commit",
                blocker_text,
            )
            is not None,
            "final-submission blocker report summarizes GitHub release draft state",
            errors,
        )
        check(
            "tracked: 3/4, untracked: 1" in blocker_text
            and "tracked inputs: 6/6" in blocker_text
            and "untracked source files: 1" in blocker_text,
            "final-submission blocker report summarizes tracked/untracked source package state",
            errors,
        )
        check(
            "Selected release/archive package plan | action plan: yes; untracked: `fonts/variable/VirtuaGrotesk[wght].ttf`; gitignore-blocked: `fonts/variable/VirtuaGrotesk[wght].ttf`" in blocker_text,
            "final-submission blocker report summarizes selected release/archive action plan",
            errors,
        )
        check(
            re.search(
                r"Package dry-run readiness \| reaches Packager: (yes|no); first blocker: [^;|]+; blockers: [^|]+; auth: (yes|no); inputs: (yes|no)",
                blocker_text,
            )
            is not None,
            "final-submission blocker report summarizes package dry-run readiness state",
            errors,
        )
        check(
            "blockers: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable"
            in blocker_text,
            "final-submission blocker report summarizes all package dry-run blockers",
            errors,
        )
        check(
            re.search(
                r"Local workflow readiness \| preflight: (yes|no); proof: (yes|no); package reaches Packager: (yes|no); auth: (yes|no)",
                blocker_text,
            )
            is not None,
            "final-submission blocker report summarizes local workflow readiness state",
            errors,
        )
        check(
            "mandatory paths: 11/11; active source inputs: 4/4; generated fonts ignored: yes" in blocker_text,
            "final-submission blocker report summarizes upstream structure state",
            errors,
        )
        check(
            re.search(
                r"Local google/fonts fork \| origin: eliheuer/fonts; upstream: google/fonts; topology: yes; exists: yes; branch: main; upstream/main: 0/0; clean: (yes|no); dirty outside package: 0",
                blocker_text,
            )
            is not None,
            "final-submission blocker report summarizes local google/fonts fork state",
            errors,
        )
    check(
        re.search(
            r"project template checked: yes; recent examples: 4; recent Packager merges: [5-9]\d*; Arabic example: yes",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes project-template and recent PR evidence",
        errors,
    )
    check(
        "script record: yes; script id: `Arab`; preview subsets: yes; primary_script: yes; languages absent: yes; sample_text absent: yes" in blocker_text,
        "final-submission blocker report summarizes language metadata alignment",
        errors,
    )
    check(
        re.search(
            r"Project template automation \| optional automation: \d+ / \d+; local targets: \d+ / \d+; Fontspector QA: yes; FontBakery refs: no; decision: [a-z]+",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes project-template automation state",
        errors,
    )
    check(
        re.search(
            r"template labels: `I New Font, II Submission`; handoff labels: yes; issue draft: yes; Fontspector: (yes|no); maintenance: yes; unchecked: yes; report refs: ([3-9]\d|[1-9]\d{2,}); source modes: yes",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes submission handoff state",
        errors,
    )
    check(
        "open: 2; decided: 13; questions: 8; guided: 8/8; mapped: 2/2; surfaces: 8; local paths: 5/5" in blocker_text,
        "final-submission blocker report summarizes decision readiness state",
        errors,
    )
    check(
        "public blockers: 0 URLs, 0 pending markers; generated echoes: 2; internal/total URL echoes: 1" in blocker_text,
        "final-submission blocker report summarizes public placeholder blocker state",
        errors,
    )
    check(
        "Add Font checkbox: yes; AI disclosure recorded: yes" in blocker_text,
        "final-submission blocker report summarizes authorship and AI disclosure state",
        errors,
    )
    check(
        re.search(
            r"PR identity and auth \| source identity: (yes|no|unknown); google/fonts identity: (yes|no|unknown); downstream name matches CLA: (yes|no|unknown); final commit identity: (yes|no|unknown); gh auth: [^;|]+; API auth: (yes|no|unknown); source: [^;|]+; CLA: [^|]+",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes PR identity and auth state",
        errors,
    )
    check(
        metadata_apply_blockers is not None
        and (
            "Downstream PR readiness | issue pending: yes; path: `ofl/virtuagrotesk`; "
            f"starter metadata: yes; metadata apply-ready: no; apply blockers: {metadata_apply_blockers}; "
            "dirty outside path: 0; family files: 1; starter-only family dir: yes; handoff shape: yes"
        )
        in blocker_text,
        "final-submission blocker report summarizes downstream PR readiness state",
        errors,
    )
    check(
        "Eli Heuer fork origin: yes; importable: yes;" in blocker_text,
        "final-submission blocker report summarizes DrawBot proof runtime state",
        errors,
    )
    check(
        "ASCII: yes; app-menu present: yes; author-name in menu: no; RFN: none declared after copyright line; namecheck pending: no; decision: decided" in blocker_text,
        "final-submission blocker report summarizes family-name and namecheck state",
        errors,
    )
    check(
        "variable names match: yes; pending/placeholder lines:" in blocker_text,
        "final-submission blocker report summarizes downstream metadata state",
        errors,
    )
    check(
        "generated for QA: 4 / 4; source.files: 0; static destinations: 0; omission documented: yes" in blocker_text,
        "final-submission blocker report summarizes static package shape",
        errors,
    )
    check(
        "Build-from-source path | gftools builder: yes; metadata fix: yes; outputs fonts: yes; tracked inputs:" in blocker_text,
        "final-submission blocker report summarizes build-from-source path",
        errors,
    )
    check(
        re.search(
            r"Article package assets \| words: \d+; target: yes; script: `Arab`; localized Arabic: (yes|no); placeholder URL: no; forbidden tags: 0; images exist: yes; image size: yes; provenance: 1/1",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes Article package asset state",
        errors,
    )
    check(
        "every master has source kerning: yes; static GPOS kern: yes; warnings: 0; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review" in blocker_text,
        "final-submission blocker report summarizes kerning state",
        errors,
    )
    check(
        "author candidates: 1; contributor-only: 0; missing profiles: 1; metadata placeholders: 0; draft inputs: 3; path collision: no" in blocker_text,
        "final-submission blocker report summarizes designer profile unresolved inputs",
        errors,
    )
    check(
        "Vendor ID | sources: `FTGD`; fonts: `FTGD`; aligned: yes; warnings: 0; decision: decided" in blocker_text,
        "final-submission blocker report summarizes vendor ID state",
        errors,
    )
    check(
        "fonts: 5; GSUB arab/dflt: 5/5; GPOS arab/dflt: 5/5; no .notdef: yes" in blocker_text,
        "final-submission blocker report summarizes Arabic shaping smoke state",
        errors,
    )
    check(
        "Arabic source worklist | missing codepoints: 0; suggested glyph names: 0; positional forms: 0; missing in both masters: 0; reuse prerequisites checked: 0; missing prerequisites: 0; dotted circle missing: no" in blocker_text,
        "final-submission blocker report summarizes Arabic source worklist state",
        errors,
    )
    check(
        "Arabic manual edit targets | source target references: 180; missing source target files: 0" in blocker_text,
        "final-submission blocker report summarizes Arabic manual edit-target state",
        errors,
    )
    check(
        "Glyph reachability | 0 unique unreachable; Arabic helpers: 0; mark helpers: 0; source cleanup: 0" in blocker_text,
        "final-submission blocker report summarizes glyph reachability state",
        errors,
    )
    check(
        "Numeric feature readiness | digits: yes; proportional defaults: yes; `tnum`: yes; coverage: yes; tabular widths: yes; ready: yes" in blocker_text,
        "final-submission blocker report summarizes numeric feature readiness",
        errors,
    )
    check(
        "PUA/private-use scope | 23 codepoints; Regular matches variable: yes; Bold matches variable: yes" in blocker_text,
        "final-submission blocker report summarizes PUA/private-use scope",
        errors,
    )
    check(
        "Fontspector warning triage | 10 WARN results; decision-linked warnings: 5" in blocker_text,
        "final-submission blocker report summarizes Fontspector warning triage",
        errors,
    )
    check(
        re.search(
            r"Fontspector zero-warning path \| honest zero possible: no; package floor: 3 WARN; "
            r"menu\+latin probe: 2 WARN but drops Arabic; menu\+latin\+arabic probe: 3 WARN; "
            r"contour findings: 0; Arabic subset threshold needs: \d+; latin-ext threshold needs: \d+; "
            r"Latin Core missing: 0; blockers: "
            r"meet or revise the broad Google Fonts subset threshold for the intended subsets; "
            r"resolve or get reviewer acceptance for required support codepoints that are not covered by serving subsets\.",
            blocker_text,
        )
        is not None,
        "final-submission blocker report summarizes zero-warning path tradeoffs",
        errors,
    )
    check(
        "Contour/no-contour cleanup | 0 source glyph findings, 0 all-font rows; decisions pending: 0, fix-now: 0" in blocker_text,
        "final-submission blocker report summarizes contour cleanup decision status",
        errors,
    )
    check(
        "documentation/vendor-id-readiness.md" in blocker_text,
        "final-submission blocker report includes vendor ID evidence",
        errors,
    )
    check(
        "documentation/family-name-readiness.md" in blocker_text,
        "final-submission blocker report includes family-name evidence",
        errors,
    )
    check(
        "documentation/authorship-disclosure-readiness.md" in blocker_text,
        "final-submission blocker report includes authorship and AI disclosure evidence",
        errors,
    )
    check(
        "documentation/pr-identity-readiness.md" in blocker_text,
        "final-submission blocker report includes PR identity evidence",
        errors,
    )
    check(
        "documentation/downstream-pr-readiness.md" in blocker_text,
        "final-submission blocker report includes downstream PR readiness evidence",
        errors,
    )
    check(
        "documentation/drawbot-runtime-readiness.md" in blocker_text,
        "final-submission blocker report includes DrawBot runtime evidence",
        errors,
    )
    check(
        "documentation/local-workflow-readiness.md" in blocker_text,
        "final-submission blocker report includes local workflow readiness evidence",
        errors,
    )
    check(
        "documentation/public-upstream-readiness.md" in blocker_text,
        "final-submission blocker report includes public upstream URL evidence",
        errors,
    )
    check(
        "documentation/decision-readiness.md" in blocker_text,
        "final-submission blocker report includes decision readiness evidence",
        errors,
    )
    check(
        "documentation/decision-application-blockers.md" in blocker_text,
        "final-submission blocker report includes decision application blocker evidence",
        errors,
    )
    check(
        "documentation/downstream-metadata-readiness.md" in blocker_text,
        "final-submission blocker report includes downstream metadata evidence",
        errors,
    )
    check(
        "documentation/downstream-metadata-diff.md" in blocker_text,
        "final-submission blocker report includes downstream metadata diff evidence",
        errors,
    )
    check(
        "documentation/package-dry-run-readiness.md" in blocker_text,
        "final-submission blocker report includes package dry-run readiness evidence",
        errors,
    )
    check(
        "documentation/packager-source-strategy.md" in blocker_text,
        "final-submission blocker report includes Packager source strategy evidence",
        errors,
    )
    check(
        "documentation/article-readiness.md" in blocker_text,
        "final-submission blocker report includes Article readiness evidence",
        errors,
    )
    check(
        "documentation/kerning-readiness.md" in blocker_text,
        "final-submission blocker report includes kerning evidence",
        errors,
    )
    check(
        "documentation/kerning-proof-review.md" in blocker_text,
        "final-submission blocker report includes kerning proof review evidence",
        errors,
    )
    check(
        "documentation/avar-readiness.md" in blocker_text,
        "final-submission blocker report includes avar evidence",
        errors,
    )
    check(
        "documentation/release-source-readiness.md" in blocker_text,
        "final-submission blocker report includes release/source evidence",
        errors,
    )
    check(
        "documentation/release-archive-manifest.md" in blocker_text,
        "final-submission blocker report includes release archive manifest evidence",
        errors,
    )
    check(
        "documentation/github-release-draft.md" in blocker_text,
        "final-submission blocker report includes GitHub release draft evidence",
        errors,
    )
    check(
        "documentation/upstream-structure-readiness.md" in blocker_text,
        "final-submission blocker report includes upstream structure evidence",
        errors,
    )
    check(
        "documentation/google-fonts-template-and-pr-audit.md" in blocker_text,
        "final-submission blocker report includes template and PR audit evidence",
        errors,
    )
    check(
        "documentation/recent-google-fonts-packages.md" in blocker_text,
        "final-submission blocker report includes recent package evidence",
        errors,
    )
    check(
        "documentation/google-fonts-add-font-template-audit.md" in blocker_text,
        "final-submission blocker report includes Add Font template evidence",
        errors,
    )
    check(
        "documentation/google-fonts-add-font-issue-draft.md" in blocker_text,
        "final-submission blocker report includes Add Font issue draft evidence",
        errors,
    )
    check(
        "documentation/project-template-automation-readiness.md" in blocker_text,
        "final-submission blocker report includes project-template automation evidence",
        errors,
    )
    check(
        "documentation/submission-handoff-readiness.md" in blocker_text,
        "final-submission blocker report includes submission handoff readiness evidence",
        errors,
    )
    check(
        "documentation/designer-profile-readiness.md" in blocker_text,
        "final-submission blocker report includes designer profile evidence",
        errors,
    )
    check(
        "documentation/designer-profile-package-draft.md" in blocker_text,
        "final-submission blocker report includes designer profile package draft evidence",
        errors,
    )
    check(
        "documentation/google-fonts-language-metadata.md" in blocker_text,
        "final-submission blocker report includes language metadata evidence",
        errors,
    )
    check(
        "documentation/arabic-shaping-smoke-test.md" in blocker_text,
        "final-submission blocker report includes Arabic shaping smoke evidence",
        errors,
    )
    check(
        "documentation/arabic-source-work-checklist.md" in blocker_text,
        "final-submission blocker report includes Arabic source checklist evidence",
        errors,
    )
    check(
        "documentation/arabic-first-review-batch.md" in blocker_text,
        "final-submission blocker report includes Arabic first review batch evidence",
        errors,
    )
    check(
        "documentation/arabic-current-review-worksheet.md" in blocker_text,
        "final-submission blocker report includes Arabic current worksheet evidence",
        errors,
    )
    check(
        "documentation/arabic-full-queue-ai-sweep.md" in blocker_text,
        "final-submission blocker report includes Arabic full queue AI sweep evidence",
        errors,
    )
    check(
        "documentation/arabic-manual-edit-targets.md" in blocker_text,
        "final-submission blocker report includes Arabic manual edit-target evidence",
        errors,
    )
    check(
        "documentation/arabic-review-packet.md" in blocker_text,
        "final-submission blocker report includes Arabic review packet evidence",
        errors,
    )
    check(
        "documentation/arabic-goal-completion-audit.md" in blocker_text,
        "final-submission blocker report includes Arabic goal completion audit evidence",
        errors,
    )
    check(
        "documentation/arabic-next-review-packet.md" in blocker_text,
        "final-submission blocker report includes Arabic next review packet evidence",
        errors,
    )
    check(
        "documentation/arabic-visual-review-log.md" in blocker_text,
        "final-submission blocker report includes Arabic visual review log evidence",
        errors,
    )
    check(
        "documentation/pua-scope.md" in blocker_text,
        "final-submission blocker report includes PUA scope evidence",
        errors,
    )
    check(
        "documentation/glyph-reachability.md" in blocker_text,
        "final-submission blocker report includes glyph reachability evidence",
        errors,
    )
    check(
        "documentation/fontspector-warnings.md" in blocker_text,
        "final-submission blocker report includes Fontspector warnings evidence",
        errors,
    )
    check(
        "documentation/fontspector-metadata-warning-probe.md" in blocker_text,
        "final-submission blocker report includes Fontspector metadata warning probe evidence",
        errors,
    )
    check(
        "documentation/fontspector-zero-warning-worklist.md" in blocker_text,
        "final-submission blocker report includes Fontspector zero-warning worklist evidence",
        errors,
    )
    check(
        "documentation/arabic-cleanup-drawing-briefs.md" in blocker_text,
        "final-submission blocker report includes Arabic cleanup drawing briefs evidence",
        errors,
    )
    check(
        "documentation/contour-cleanup-batches.md" in blocker_text,
        "final-submission blocker report includes contour cleanup batches evidence",
        errors,
    )
    check(
        "documentation/contour-cleanup-ai-triage.md" in blocker_text,
        "final-submission blocker report includes contour cleanup AI triage evidence",
        errors,
    )
    check(
        "documentation/contour-cleanup-decision-log.md" in blocker_text,
        "final-submission blocker report includes contour cleanup decision log evidence",
        errors,
    )

    next_actions_path = ROOT / "documentation" / "next-actions.md"
    check(next_actions_path.exists(), "next-actions report exists", errors)
    if next_actions_path.exists():
        next_actions_text = next_actions_path.read_text()
        check("# Google Fonts Next Actions" in next_actions_text, "next-actions report has expected heading", errors)
        for heading in [
            "## Snapshot",
            "## Maintainer Decisions",
            "## Decision Unblock Order",
            "## Drawing And Source Work",
            "## Packaging And Handoff",
            "## Run Order",
        ]:
            check(heading in next_actions_text, f"next-actions report includes {heading}", errors)
        check("Maintainer decisions: 2 open, 13 decided" in next_actions_text, "next-actions report summarizes decision count", errors)
        check("Decision answer packet ready: yes" in next_actions_text, "next-actions report confirms decision packet readiness", errors)
        check("Package dry run reaches Packager: no" in next_actions_text, "next-actions report summarizes package dry-run state", errors)
        check("Package dry-run blocking findings:" in next_actions_text, "next-actions report summarizes all package dry-run blockers", errors)
        check("GitHub API credentials unavailable" in next_actions_text, "next-actions report includes GitHub auth package blocker", errors)
        check("Contour cleanup decisions:" in next_actions_text, "next-actions report summarizes contour cleanup decision state", errors)
        check("UFO editor handoff ready: yes" in next_actions_text, "next-actions report summarizes UFO editor readiness", errors)
        check("Arabic snapshot evidence ready: yes" in next_actions_text, "next-actions report summarizes Arabic snapshot integrity", errors)
        check(
            "Monitor placeholder audit; no public placeholder strings currently block handoff." in next_actions_text,
            "next-actions report avoids treating internal placeholder guards as public blockers",
            errors,
        )
        check("Downstream starter METADATA.pb present: yes" in next_actions_text, "next-actions report summarizes starter metadata state", errors)
        check("Downstream `source.config_yaml` present: no; source-strategy review needed: no" in next_actions_text, "next-actions report summarizes config_yaml source-strategy review state", errors)
        check(
            re.search(
                r"GitHub release draft: `v1\.000` / `Virtua Grotesk 1\.000`; archive files: yes; hashes: (yes|no)",
                next_actions_text,
            )
            is not None,
            "next-actions report summarizes GitHub release draft state",
            errors,
        )
        check(
            "Fontspector googlefonts profile: 0 FAIL results" in next_actions_text
            or re.search(r"Fontspector googlefonts profile: \d+ FAIL, \d+ WARN, \d+ PASS", next_actions_text)
            is not None,
            "next-actions report summarizes Fontspector state",
            errors,
        )
        check(
            "release/archive source mode: `latest-release`; archive must include currently untracked package files: `fonts/variable/VirtuaGrotesk[wght].ttf`" in next_actions_text,
            "next-actions report summarizes release/archive source-file blockers",
            errors,
        )
        check(
            "Publish the final GitHub release asset after the final source commit and tag." in next_actions_text
            and "documentation/github-release-draft.md" in next_actions_text,
            "next-actions report includes GitHub release publication action",
            errors,
        )
        check(
            "Prepare the Google Fonts designer profile request for `Eli Heuer`." in next_actions_text
            and "documentation/designer-profile-package-draft.md" in next_actions_text,
            "next-actions report includes designer profile package action",
            errors,
        )
        check(
            "Align Git/GitHub identity before downstream commits." in next_actions_text
            and "documentation/pr-identity-readiness.md" in next_actions_text,
            "next-actions report includes PR identity and auth action",
            errors,
        )
        check(
            "Prepare the `Eli Heuer` designer-profile link, biography, and square image" in next_actions_text,
            "next-actions run order includes designer profile inputs",
            errors,
        )
        check(
            "Align source-repo and `google/fonts` fork Git names, GitHub auth, and API credentials with `documentation/pr-identity-readiness.md` before downstream commits." in next_actions_text,
            "next-actions run order includes PR identity alignment",
            errors,
        )
        next_actions_handoff_refs = summary_count(next_actions_text, "report refs")
        check(
            next_actions_handoff_refs is not None and next_actions_handoff_refs >= 32,
            "next-actions report summarizes current handoff evidence count",
            errors,
        )
        check(
            "Run `make preflight` so the build, proof PDF, generated reports, and local gate stay synchronized." in next_actions_text,
            "next-actions run order uses synchronized preflight",
            errors,
        )
        check("Review `documentation/github-release-draft.md`" in next_actions_text, "next-actions run order includes release draft review", errors)
        for expected_action in [
            "PUA Icon Block",
            "Kerning Scope",
            "make downstream-metadata-check",
        ]:
            check(expected_action in next_actions_text, f"next-actions decision unblock order includes {expected_action}", errors)
        check("make downstream-metadata-check" in next_actions_text, "next-actions report includes downstream metadata check in run order", errors)
        check(
            "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run" in next_actions_text,
            "next-actions report uses selected latest-release package dry-run command",
            errors,
        )
        for expected in [
            "documentation/google-fonts-decision-answer-sheet.md",
            "documentation/missing-gf-latin-core.md",
            "documentation/missing-gf-arabic-core.md",
            "documentation/arabic-review-packet.md",
            "documentation/arabic-goal-completion-audit.md",
            "documentation/arabic-current-review-worksheet.md",
            "documentation/arabic-first-review-batch.md",
            "documentation/arabic-full-queue-ai-sweep.md",
            "documentation/arabic-hand-review-session.md",
            "documentation/arabic-next-review-packet.md",
            "documentation/arabic-visual-review-log.md",
            "documentation/ufo-editor-readiness.md",
            "documentation/arabic-snapshot-integrity.md",
            "documentation/arabic-manual-review-batches.md",
            "documentation/arabic-manual-edit-targets.md",
            "documentation/fontspector-contour-count.md",
            "documentation/arabic-cleanup-drawing-briefs.md",
            "documentation/contour-cleanup-batches.md",
            "documentation/contour-cleanup-ai-triage.md",
            "documentation/contour-cleanup-decision-log.md",
            "documentation/fontspector-metadata-warning-probe.md",
            "documentation/fontspector-zero-warning-worklist.md",
            "documentation/contour-cleanup-edit-plan.md",
            "documentation/downstream-metadata-diff.md",
            "documentation/packager-source-strategy.md",
            "documentation/github-release-draft.md",
            "documentation/submission-handoff-readiness.md",
        ]:
            check(expected in next_actions_text, f"next-actions report references {expected}", errors)
        check("https://googlefonts.github.io/gf-guide/package.html" in next_actions_text, "next-actions report cites GF package guide", errors)

    add_font_template_path = ROOT / "documentation" / "google-fonts-add-font-template-audit.md"
    check(add_font_template_path.exists(), "Add Font issue-template audit exists", errors)
    if add_font_template_path.exists():
        add_font_template_text = add_font_template_path.read_text()
        for expected in [
            "Alignment with `upstream/main`: `0 ahead, 0 behind`",
            "Alignment with `origin/main`: `0 ahead, 0 behind`",
            "Default labels: `I New Font, II Submission`",
            "Font Project Git Repo URL",
            "Super short description of the Font Family",
            "sole copyright author",
            "AI tools were used",
            "namecheck.fontdata.com",
            "Latin Core",
            "preferred upstream repo structure",
            "maintain the repository",
        ]:
            check(expected in add_font_template_text, f"Add Font issue-template audit tracks {expected}", errors)

    add_font_issue_draft_path = ROOT / "documentation" / "google-fonts-add-font-issue-draft.md"
    check(add_font_issue_draft_path.exists(), "Add Font issue draft exists", errors)
    if add_font_issue_draft_path.exists():
        issue_draft_text = add_font_issue_draft_path.read_text()
        for expected in [
            "# Google Fonts Add Font Issue Draft",
            "Add Virtua Grotesk",
            "I New Font, II Submission",
            "Template checkout status: `## main...origin/main`",
            "Alignment with `upstream/main`: `0 ahead, 0 behind`",
            "Alignment with `origin/main`: `0 ahead, 0 behind`",
            "**Font Project Git Repo URL:**",
            "https://github.com/eliheuer/virtua-grotesk",
            "**Super short description of the Font Family:**",
            "Virtua Grotesk is a variable geometric grotesk",
            "**Requirements:**",
            "The entire font project is available in a Github repository",
            "The source files are available in the repo",
            "sole copyright author",
            "namecheck.fontdata.com",
            "Google Fonts 'Latin Core' glyphset",
            "## Arabic Scope Status",
            "GF Arabic Core missing codepoints:",
            "documentation/arabic-review-packet.md",
            "documentation/missing-gf-arabic-core.md",
            "documentation/arabic-mark-readiness.md",
            "documentation/arabic-shaping-smoke-test.md",
            "## Numeric Feature Status",
            "Default ASCII digits are proportional in every built font: yes",
            "`tnum` substitutes all ten ASCII digits in every built font: yes",
            "`tnum` substitutes to equal-width digits in every built font: yes",
            "Numeric feature requirement ready: yes",
            "documentation/numeric-feature-readiness.md",
            "## Designer Profile Status",
            "Current candidate designer string: `Eli Heuer`",
            "Candidate catalog slug: `eliheuer`",
            "Candidate designer profiles missing: 1",
            "Final metadata designer strings present: yes",
            "Pending metadata designer placeholders: 0",
            "Target profile directory already exists: no",
            "Expected profile files already present: 0 / 3",
            "Draft profile inputs still unresolved: 3",
            "documentation/designer-profile-readiness.md",
            "documentation/designer-profile-package-draft.md",
            "## Decision-Linked Warning Status",
            "Vendor ID:",
            "Kerning:",
            "GF visual proof output: yes",
            "proof covers expected instances: yes",
            "proof review packet files: 16 / 16",
            "`avar`:",
            "PUA/reachability:",
            "documentation/vendor-id-readiness.md",
            "documentation/kerning-readiness.md",
            "documentation/kerning-proof-review.md",
            "documentation/avar-readiness.md",
            "documentation/pua-scope.md",
            "documentation/fontspector-warnings.md",
            "## Package Dry-Run Status",
            "Wrapper can reach Packager: no",
            "existing downstream METADATA.pb is still the Packager starter template",
            "GitHub API credentials ready: no",
            "Required local package inputs tracked: 4 / 5",
            "Required local package inputs untracked: 1",
            "Default branch mode has untracked source-file blocker: yes",
            "Latest-release/archive mode has untracked source-file blocker: yes",
            "Build-from-source mode has untracked build-input blocker: no",
            "Downstream METADATA.pb is starter template: yes",
            "Expected metadata lines missing from downstream file: 16 / 22",
            "Downstream metadata preview ready to apply: no",
            "Downstream metadata apply blockers:",
            "make downstream-metadata-check",
            "using the same `GFT_PACKAGER_SOURCE_MODE` planned for Packager",
            "must be a GitHub release download URL ending in `.zip`",
            "scripts/prepare_downstream_metadata.py --apply",
            "documentation/package-dry-run-readiness.md",
            "documentation/downstream-metadata-diff.md",
            "documentation/packager-source-strategy.md",
            "preferred upstream repo structure",
            "Draft status:",
            "Attach `documentation/readme-specimen.png`",
            "https://googlefonts.github.io/gf-guide/package.html",
        ]:
            check(expected in issue_draft_text, f"Add Font issue draft tracks {expected}", errors)
        check(
            metadata_apply_blockers is not None
            and f"Downstream metadata apply blockers: {metadata_apply_blockers}." in issue_draft_text,
            "Add Font issue draft matches downstream metadata apply blocker count",
            errors,
        )
        check(
            "- [x]" not in issue_draft_text,
            "Add Font issue draft leaves requirement boxes unchecked until final decisions",
            errors,
        )


def main() -> int:
    errors: list[str] = []
    required_file_errors(errors)
    executable_errors(errors)
    python_dependency_errors(errors)
    legal_credit_errors(errors)
    plist_errors(errors)
    source_fontinfo_errors(errors)
    command_ok(
        [
            "bash",
            "-n",
            "build.sh",
            "scripts/check_gf_fonts.sh",
            "scripts/check_gf_variable.sh",
            "scripts/package_gf_dry_run.sh",
            "scripts/test_package_gf_dry_run_gates.sh",
            "scripts/test_release_archive_gates.sh",
            "scripts/test_contour_decision_update.sh",
            "scripts/check_runebender_norad_load.sh",
        ],
        "shell scripts parse",
        errors,
    )
    command_ok(
        [
            "make",
            "-n",
            "help",
            "decisions",
            "decision-readiness-check",
            "next-actions",
            "blockers",
            "issue-draft",
            "handoff-readiness-check",
            "release-check",
            "release-archive-check",
            "release-archive-build",
            "release-archive-verify",
            "release-archive-test",
            "release-draft-check",
            "source-strategy-check",
            "package-readiness-check",
            "recent-gf-check",
            "kerning-check",
            "kerning-proof-check",
            "kerning-proof-review-check",
            "pr-readiness-check",
            "metadata-warning-check",
            "zero-warning-check",
            "github-auth-check",
            "designer-profile-check",
            "runebender-ufo-check",
            "public-upstream-url-check",
            "downstream-metadata-check",
            "downstream-metadata-helper-test",
            "package-wrapper-test",
            "arabic-manual-review-batches",
            "arabic-batch-recorder",
            "arabic-manual-edit-targets",
            "arabic-next-review-packet",
            "arabic-structure-sweep",
            "arabic-structure-triage",
            "arabic-mark-review-proof",
            "arabic-mark-triage",
            "arabic-visual-review-runbook",
            "contour-decision-helper-test",
            "arabic-visual-review-helper-test",
            "build",
            "test",
            "reports",
            "proof",
            "preflight",
            "handoff",
            "package-dry-run",
            "clean",
        ],
        "Make targets are defined",
        errors,
    )
    command_ok(["fontspector", "--version"], "Fontspector command is available", errors)
    command_ok(["./venv/bin/gftools", "builder", "--help"], "gftools builder is importable", errors)
    command_ok(["./venv/bin/gftools", "packager", "--help"], "gftools packager is importable", errors)
    command_ok(["./venv/bin/gftools", "qa", "--help"], "gftools QA proof tooling is importable", errors)
    command_ok(["./scripts/test_package_gf_dry_run_gates.sh"], "package dry-run wrapper metadata gate tests pass", errors)
    command_ok(["./scripts/test_downstream_metadata_helper.sh"], "downstream metadata helper final-value gate tests pass", errors)
    command_ok(["./scripts/test_release_archive_gates.sh"], "release archive path-safety gate tests pass", errors)
    command_ok(["./scripts/test_contour_decision_update.sh"], "contour decision update helper tests pass", errors)
    command_ok(["./scripts/test_arabic_visual_review_update.sh"], "Arabic visual review update helper tests pass", errors)
    builder_config_errors(errors)
    designspace_errors(errors)
    build_output_errors(errors)
    font_metadata_errors(errors)
    axis_errors(errors)
    layout_table_errors(errors)
    naming_errors(errors)
    report_errors(errors)
    metadata_review_errors(errors)
    decision_log_errors(errors)
    upstream_audit_errors(errors)
    package_checklist_errors(errors)
    proof_runtime_errors(errors)
    descriptive_artifact_errors(errors)
    fontspector_failures(errors)

    if errors:
        print("")
        print("Preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("")
    print("Preflight passed with only documented drawing/source blockers remaining.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
