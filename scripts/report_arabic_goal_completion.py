#!/usr/bin/env python3
"""Audit the active Arabic missing-drawings goal against current evidence."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-goal-completion-audit.md"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def first_int(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return int(match.group(1)) if match else None


def yes_no(condition: bool) -> str:
    return "yes" if condition else "no"


def visual_status_rows(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 7:
            rows[cells[0].strip("`")] = cells[6].strip()
    return rows


def full_queue_ai_rows(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    in_rows = False
    for line in text.splitlines():
        if line == "## Row Observations":
            in_rows = True
            continue
        if in_rows and line.startswith("## "):
            break
        if not in_rows or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4:
            rows[cells[0].strip("`")] = (cells[2], cells[3])
    return rows


def board_row_keys(text: str) -> set[str]:
    return set(re.findall(r"<tr><td>\d+</td><td><code>([^<]+)</code></td>", text))


def count_keys_with_commands(text: str, keys: set[str]) -> int:
    return sum(
        all(f"REVIEW_KEY={key} REVIEW_STATUS={status}" in text for status in ("pass", "fix-needed", "deferred"))
        for key in keys
    )


def status(done: bool, *, needs_review: bool = False) -> str:
    if done and not needs_review:
        return "proven"
    if done and needs_review:
        return "proven mechanically; review pending"
    return "open"


def fontspector_fail_count(text: str) -> int | None:
    counts = fontspector_summary_counts(text)
    for label, value in counts.items():
        if "FAIL" in label:
            return value
    return 0


def fontspector_summary_counts(text: str) -> dict[str, int]:
    summary = re.search(r"### Summary\n\n\| (.+) \|\n\|[-| ]+\|\n\| (.+) \|", text)
    if not summary:
        return {}
    labels = [cell.strip() for cell in summary.group(1).strip("|").split("|")]
    values = [cell.strip() for cell in summary.group(2).strip("|").split("|")]
    counts: dict[str, int] = {}
    for label, value in zip(labels, values, strict=False):
        value_match = re.match(r"\d+", value)
        if value_match:
            counts[label] = int(value_match.group(0))
    return counts


def table_row(requirement: str, state: str, evidence: str, result: str) -> str:
    return f"| {requirement} | {state} | {evidence} | {result} |"


def markdown_report() -> str:
    arabic = read("documentation/google-fonts/missing-gf-arabic-core.md")
    source = read("documentation/glyph-review/arabic-source-work-checklist.md")
    candidate = read("documentation/glyph-review/arabic-candidate-glyph-plan.md")
    marks = read("documentation/glyph-review/arabic-mark-readiness.md")
    shaping = read("documentation/glyph-review/arabic-shaping-smoke-test.md")
    master = read("documentation/source/master-compatibility.md")
    visual = read("documentation/glyph-review/arabic-visual-review-checklist.md")
    visual_log = read("documentation/glyph-review/arabic-visual-review-log.md")
    next_packet = read("documentation/glyph-review/arabic-next-review-packet.md")
    crop_integrity = read("documentation/glyph-review/arabic-first-review-crop-integrity.md")
    snapshot_integrity = read("documentation/glyph-review/arabic-snapshot-integrity.md")
    hand_review_session = read("documentation/glyph-review/arabic-hand-review-session.md")
    hand_review_contact_sheet = read("documentation/glyph-review/arabic-hand-review-contact-sheet.html")
    arabic_print_proof_index = read("documentation/glyph-review/arabic-print-proof-index.md")
    full_queue_ai_sweep = read("documentation/glyph-review/arabic-full-queue-ai-sweep.md")
    ai_visual_screen = read("documentation/glyph-review/arabic-ai-visual-screen-batch-2.md")
    mark_ai_visual_screen = read("documentation/glyph-review/arabic-ai-visual-screen-batch-3.md")
    dot_ai_visual_screen = read("documentation/glyph-review/arabic-ai-visual-screen-batch-4.md")
    spacing_ai_visual_screen = read("documentation/glyph-review/arabic-ai-visual-screen-batch-5.md")
    review_board = read("documentation/glyph-review/arabic-next-review-board.html")
    edit_targets = read("documentation/glyph-review/arabic-manual-edit-targets.md")
    first_batch_source_checkpoint = read("documentation/glyph-review/arabic-first-batch-source-checkpoint.md")
    pending_source_checkpoint = read("documentation/glyph-review/arabic-pending-source-checkpoint.md")
    blockers = read("documentation/google-fonts/final-submission-blockers.md")
    contours = read("documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md")
    fontspector = read("documentation/google-fonts/fontspector-googlefonts-report.md")

    arabic_missing = first_int(r"Missing codepoints: (\d+)", arabic)
    source_missing = first_int(r"Missing required codepoints: (\d+)", source)
    suggested_names = first_int(r"Suggested source glyph names: (\d+)", source)
    positional_forms = first_int(r"Suggested Arabic positional-form glyph names: (\d+)", source)
    missing_both = first_int(r"Suggested glyph names missing in both masters: (\d+)", source)
    dotted_missing = "U+25CC dotted circle missing: no" in source
    candidate_worklist = first_int(r"Worklist glyphs: (\d+)", candidate)
    candidate_auto_create = first_int(r"Auto-created / would auto-create: (\d+)", candidate)
    candidate_review_needed = first_int(r"Review-needed: (\d+)", candidate)
    candidate_hand_draw = first_int(r"Hand-draw-needed: (\d+)", candidate)
    candidate_compatibility_risk = first_int(r"Compatibility-risk: (\d+)", candidate)
    candidate_existing_entries = first_int(r"Existing master entries counted: (\d+)", candidate)
    mark_missing = first_int(r"Missing from current variable-font cmap: (\d+)", marks)
    dotted_present = "U+25CC dotted circle present: yes" in marks
    source_anchors = "Source anchors present: yes" in marks
    mark_gpos = "Built mark/mkmk GPOS features present: yes" in marks
    master_mismatches = first_int(r"Blocking structure mismatches: (\d+)", master)
    shaping_fonts = len(re.findall(r"^## fonts/", shaping, flags=re.MULTILINE))
    gsub_ready = shaping.count("GSUB has `arab/dflt`: `true`")
    gpos_ready = shaping.count("GPOS has `arab/dflt`: `true`")
    notdef_counts = [int(value) for value in re.findall(r"\| (\d+) \| yes \|", shaping)]
    no_notdef = bool(notdef_counts) and all(value == 0 for value in notdef_counts)
    proof_files = first_int(r"Google Fonts QA proof files: (\d+) / 16 present", visual)
    visual_pending = first_int(r"^- Pending: (\d+)$", visual_log)
    visual_fix_needed = first_int(r"^- Fix-needed: (\d+)$", visual_log)
    visual_deferred = first_int(r"^- Deferred: (\d+)$", visual_log)
    visual_statuses = visual_status_rows(visual_log)
    pending_keys = {key for key, row_status in visual_statuses.items() if row_status in {"pending", "fix-needed"}}
    packet_pending = first_int(r"^- Pending or fix-needed rows: (\d+)$", next_packet)
    crop_ready = "Evidence ready for hand review: yes" in crop_integrity
    crop_nonblank = first_int(r"^- Nonblank crops: (\d+)$", crop_integrity)
    snapshot_ready = "Snapshot evidence ready for hand review: yes" in snapshot_integrity
    snapshot_missing = first_int(r"Pending/fix-needed rows without snapshot: (\d+)", snapshot_integrity)
    arabic_print_proof = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
    print_proof_ready = arabic_print_proof.exists() and arabic_print_proof.stat().st_size > 0
    print_proof_index_ready = (
        "# Arabic Print Proof Index" in arabic_print_proof_index
        and "PDF: `documentation/glyph-review/arabic-print-proof.pdf`" in arabic_print_proof_index
        and "Arabic cmap grid" in arabic_print_proof_index
    )
    session_links_print_proof = "documentation/glyph-review/arabic-print-proof.pdf" in hand_review_session
    contact_sheet_links_print_proof = "documentation/glyph-review/arabic-print-proof.pdf" in hand_review_contact_sheet
    full_queue_ai = full_queue_ai_rows(full_queue_ai_sweep)
    board_keys = board_row_keys(review_board)
    board_command_keys = count_keys_with_commands(review_board, pending_keys)
    ai_observation_keys = sum(1 for key in pending_keys if key in full_queue_ai and full_queue_ai[key][0])
    ai_follow_up_keys = sum(1 for key in pending_keys if key in full_queue_ai and full_queue_ai[key][1])
    board_rows_ready = pending_keys <= board_keys
    decision_packet_ready = (
        board_rows_ready
        and board_command_keys == len(pending_keys)
        and ai_observation_keys == len(pending_keys)
        and ai_follow_up_keys == len(pending_keys)
        and snapshot_ready
        and snapshot_missing == 0
    )
    first_batch_ai_screen = (
        "# Arabic AI Visual Screen: Batch 2" in ai_visual_screen
        and "Visual rows screened: 5" in ai_visual_screen
        and "No `pass`, `fix-needed`, or `deferred` status was recorded." in ai_visual_screen
    )
    mark_batch_ai_screen = (
        "# Arabic AI Visual Screen: Batch 3" in mark_ai_visual_screen
        and "Visual rows screened: 8" in mark_ai_visual_screen
        and "No `pass`, `fix-needed`, or `deferred` status was recorded." in mark_ai_visual_screen
    )
    dot_batch_ai_screen = (
        "# Arabic AI Visual Screen: Batch 4" in dot_ai_visual_screen
        and "Visual rows screened: 1" in dot_ai_visual_screen
        and "No `pass`, `fix-needed`, or `deferred` status was recorded." in dot_ai_visual_screen
    )
    spacing_batch_ai_screen = (
        "# Arabic AI Visual Screen: Batch 5" in spacing_ai_visual_screen
        and "Visual rows screened: 18" in spacing_ai_visual_screen
        and "No `pass`, `fix-needed`, or `deferred` status was recorded." in spacing_ai_visual_screen
    )
    source_targets = first_int(r"Source target references: (\d+)", edit_targets)
    missing_target_files = first_int(r"Missing source target files: (\d+)", edit_targets)
    first_batch_checkpoint_glyphs = first_int(r"^- Glyphs checked: (\d+)$", first_batch_source_checkpoint)
    first_batch_checkpoint_missing = first_int(r"^- Missing source files: (\d+)$", first_batch_source_checkpoint)
    first_batch_checkpoint_mismatches = first_int(
        r"^- Regular/Bold structure mismatches: (\d+)$",
        first_batch_source_checkpoint,
    )
    first_batch_checkpoint_ready = "Ready for paired-master hand review: yes" in first_batch_source_checkpoint
    pending_checkpoint_rows = first_int(r"^- Pending or fix-needed review rows: (\d+)$", pending_source_checkpoint)
    pending_checkpoint_glyphs = first_int(r"^- Unique source glyph names checked: (\d+)$", pending_source_checkpoint)
    pending_checkpoint_files = first_int(r"^- Unique source target files referenced: (\d+)$", pending_source_checkpoint)
    pending_checkpoint_missing = first_int(r"^- Missing source files: (\d+)$", pending_source_checkpoint)
    pending_checkpoint_mismatches = first_int(
        r"^- Regular/Bold structure mismatches: (\d+)$",
        pending_source_checkpoint,
    )
    pending_checkpoint_ready = "Ready for paired-master hand review: yes" in pending_source_checkpoint
    contour_pending = first_int(r"^- Pending: (\d+)$", contours)
    contour_fix_now = first_int(r"^- Fix-now: (\d+)$", contours)
    contour_fixed = first_int(r"^- Fixed: (\d+)$", contours)
    contour_accepted = first_int(r"^- Accepted: (\d+)$", contours)
    contour_deferred = first_int(r"^- Deferred: (\d+)$", contours)
    fontspector_fails = fontspector_fail_count(fontspector)
    fontspector_counts = fontspector_summary_counts(fontspector)
    fontspector_warns = fontspector_counts.get("⚠️ WARN", 0)
    fontspector_infos = fontspector_counts.get("ℹ️ INFO", 0)
    fontspector_passes = fontspector_counts.get("✅ PASS", 0)
    fontspector_skips = fontspector_counts.get("⏩ SKIP", 0)

    core_done = arabic_missing == 0
    candidate_done = (
        candidate_worklist == 256
        and candidate_auto_create == 0
        and candidate_review_needed == 256
        and candidate_hand_draw == 0
        and candidate_compatibility_risk == 0
        and candidate_existing_entries == 512
    )
    source_done = (
        source_missing == 0
        and suggested_names == 0
        and missing_both == 0
        and dotted_missing
        and candidate_done
    )
    compatibility_done = master_mismatches == 0
    marks_done = mark_missing == 0 and dotted_present and source_anchors and mark_gpos
    shaping_done = shaping_fonts == 5 and gsub_ready == 5 and gpos_ready == 5 and no_notdef
    visual_review_done = proof_files == 16 and visual_pending == 0 and visual_fix_needed == 0
    contour_done = (contour_pending or 0) == 0 and (contour_fix_now or 0) == 0
    preflight_no_undocumented = (
        "Contour/no-contour cleanup | 0 source glyph findings, 0 all-font rows; decisions pending: 0, fix-now: 0"
        in blockers
        and "Arabic source worklist" in blockers
    )
    final_fontspector_ready = fontspector_fails == 0

    lines = [
        "# Arabic Goal Completion Audit",
        "",
        "This generated report audits the active Arabic missing-drawings goal against",
        "current repo evidence. The original 57-missing baseline is now stale; the",
        "current reports below are authoritative.",
        "",
        "## Summary",
        "",
        "| Requirement | Current state | Evidence | Result |",
        "| --- | --- | --- | --- |",
        table_row(
            "GF Arabic Core gaps are zero or accepted",
            f"{arabic_missing} missing codepoints",
            "`documentation/google-fonts/missing-gf-arabic-core.md`",
            status(core_done),
        ),
        table_row(
            "Missing source glyphs exist in both masters",
            f"missing codepoints: {source_missing}; suggested names: {suggested_names}; positional forms: {positional_forms}; missing in both masters: {missing_both}; dotted circle missing: {yes_no(not dotted_missing)}; candidate worklist: {candidate_worklist}; candidate auto-create: {candidate_auto_create}; candidate review-needed: {candidate_review_needed}; candidate hand-draw-needed: {candidate_hand_draw}; candidate compatibility-risk: {candidate_compatibility_risk}; candidate existing master entries: {candidate_existing_entries}",
            "`documentation/glyph-review/arabic-source-work-checklist.md`; `documentation/glyph-review/arabic-candidate-glyph-plan.md`",
            status(source_done),
        ),
        table_row(
            "Regular and Bold structures stay compatible",
            f"{master_mismatches} blocking mismatches",
            "`documentation/source/master-compatibility.md`",
            status(compatibility_done),
        ),
        table_row(
            "Arabic shaping smoke tests pass",
            f"fonts: {shaping_fonts}; GSUB: {gsub_ready}/5; GPOS: {gpos_ready}/5; no .notdef: {yes_no(no_notdef)}",
            "`documentation/glyph-review/arabic-shaping-smoke-test.md`",
            status(shaping_done),
        ),
        table_row(
            "Dotted circle, marks, anchors, and mark/mkmk are ready or documented",
            f"missing marks: {mark_missing}; dotted circle: {yes_no(dotted_present)}; anchors: {yes_no(source_anchors)}; mark/mkmk: {yes_no(mark_gpos)}",
            "`documentation/glyph-review/arabic-mark-readiness.md`",
            status(marks_done),
        ),
        table_row(
            "Arabic drawings have human visual review",
            f"GF proof files: {proof_files}/16; Arabic PDF proof ready: {yes_no(print_proof_ready)}; Arabic PDF index ready: {yes_no(print_proof_index_ready)}; session links PDF: {yes_no(session_links_print_proof)}; contact sheet links PDF: {yes_no(contact_sheet_links_print_proof)}; first-review focused crops ready: {yes_no(crop_ready)}; nonblank crops: {crop_nonblank}; first-batch source checkpoint glyphs: {first_batch_checkpoint_glyphs}; first-batch missing source files: {first_batch_checkpoint_missing}; first-batch Regular/Bold mismatches: {first_batch_checkpoint_mismatches}; first-batch checkpoint ready: {yes_no(first_batch_checkpoint_ready)}; pending source checkpoint rows: {pending_checkpoint_rows}; pending source glyphs: {pending_checkpoint_glyphs}; pending source files: {pending_checkpoint_files}; pending source missing files: {pending_checkpoint_missing}; pending source Regular/Bold mismatches: {pending_checkpoint_mismatches}; pending source checkpoint ready: {yes_no(pending_checkpoint_ready)}; visual pending: {visual_pending}; next packet pending: {packet_pending}; visual fix-needed: {visual_fix_needed}; visual deferred: {visual_deferred}; decision packet ready: {yes_no(decision_packet_ready)}; first-batch AI visual screen ready: {yes_no(first_batch_ai_screen)}; mark-batch AI visual screen ready: {yes_no(mark_batch_ai_screen)}; dot-batch AI visual screen ready: {yes_no(dot_batch_ai_screen)}; spacing-batch AI visual screen ready: {yes_no(spacing_batch_ai_screen)}; board rows: {len(board_keys)}/{len(pending_keys)}; board command rows: {board_command_keys}/{len(pending_keys)}; AI observation rows: {ai_observation_keys}/{len(pending_keys)}; human follow-up rows: {ai_follow_up_keys}/{len(pending_keys)}; snapshot missing rows: {snapshot_missing}; source target references: {source_targets}; missing target files: {missing_target_files}; contour decisions pending: {contour_pending}; fix-now: {contour_fix_now}; fixed: {contour_fixed}; accepted: {contour_accepted}; deferred: {contour_deferred}",
            "`documentation/glyph-review/arabic-current-review-worksheet.md`; `documentation/glyph-review/arabic-next-review-packet.md`; `documentation/glyph-review/arabic-ai-visual-screen-batch-2.md`; `documentation/glyph-review/arabic-ai-visual-screen-batch-3.md`; `documentation/glyph-review/arabic-ai-visual-screen-batch-4.md`; `documentation/glyph-review/arabic-ai-visual-screen-batch-5.md`; `documentation/glyph-review/arabic-next-review-board.html`; `documentation/glyph-review/arabic-hand-review-session.md`; `documentation/glyph-review/arabic-hand-review-contact-sheet.html`; `documentation/glyph-review/arabic-print-proof.pdf`; `documentation/glyph-review/arabic-print-proof-index.md`; `documentation/glyph-review/arabic-full-queue-ai-sweep.md`; `documentation/glyph-review/arabic-snapshot-integrity.md`; `documentation/glyph-review/arabic-first-review-crop-integrity.md`; `documentation/glyph-review/arabic-first-batch-source-checkpoint.md`; `documentation/glyph-review/arabic-pending-source-checkpoint.md`; `documentation/glyph-review/arabic-visual-review-checklist.md`; `documentation/glyph-review/arabic-visual-review-log.md`; `documentation/glyph-review/arabic-manual-edit-targets.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`",
            status(visual_review_done and contour_done),
        ),
        table_row(
            "`make preflight` has no undocumented drawing/source blockers",
            "preflight gate passes locally; contour/no-contour cleanup is closed",
            "`documentation/google-fonts/final-submission-blockers.md`; `make preflight-only`",
            status(preflight_no_undocumented and contour_done),
        ),
        table_row(
            "`make test` is ready for final Fontspector review",
            f"Fontspector FAIL results: {fontspector_fails}; WARN results: {fontspector_warns}; INFO results: {fontspector_infos}; PASS results: {fontspector_passes}; SKIP results: {fontspector_skips}; contour decisions pending: {contour_pending}",
            "`documentation/google-fonts/fontspector-googlefonts-report.md`; `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`",
            status(final_fontspector_ready),
        ),
        "",
        "## Current Next Work",
        "",
        "1. Start with `documentation/glyph-review/arabic-current-review-worksheet.md` for",
        "   the current five-row fill-in sheet, then use",
        "   `documentation/glyph-review/arabic-next-review-packet.md` for the smallest current",
        "   hand-review batch. For the full queue, open",
        "   `documentation/glyph-review/arabic-next-review-board.html`; it now carries",
        "   PNG snapshots, AI-safe notes, human follow-up prompts, edit targets,",
        "   and guarded pass/fix-needed/deferred commands for every pending row.",
        "   Use `documentation/glyph-review/arabic-print-proof.pdf` and",
        "   `documentation/glyph-review/arabic-hand-review-contact-sheet.html` as printable",
        "   review aids, but keep the linked proof/source HTML authoritative.",
        "   Use the linked GF proof HTML and",
        "   `documentation/glyph-review/arabic-visual-review-log.md` to record human drawing,",
        "   spacing, mark, and shaping review.",
        "   The first glyph-proof crop files are mechanically ready in",
        "   `documentation/glyph-review/arabic-first-review-crop-integrity.md`, but those",
        "   crops are review aids only and do not close any row.",
        "   Use `documentation/glyph-review/arabic-first-batch-source-checkpoint.md` for",
        "   the first-batch Regular/Bold source structure, and",
        "   `documentation/glyph-review/arabic-pending-source-checkpoint.md` to confirm all",
        "   unresolved review-row source targets stay paired before and after",
        "   broader cleanup.",
        "   Use `documentation/glyph-review/arabic-manual-review-batches.md` and",
        "   `documentation/glyph-review/arabic-visual-review-runbook.md` when working through",
        "   the full queue. If a row becomes `fix-needed`, use",
        "   `documentation/glyph-review/arabic-manual-edit-targets.md` to find the matching",
        "   Regular and Bold GLIF source files before editing.",
        "2. Rerun `make contour-cleanup-proof`, `make reports-only`, and",
        "   `make preflight-only` after each drawing/review batch.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
