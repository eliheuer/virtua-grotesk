#!/usr/bin/env python3
"""Generate the current Arabic hand-drawing session checklist."""

from __future__ import annotations

from pathlib import Path
import sys

import report_arabic_manual_edit_targets as edit_targets
import report_arabic_manual_review_batches as batches
import report_arabic_visual_review_runbook as runbook


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-drawing-session-checklist.md"


def clean(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|")


def status(row: list[str]) -> str:
    return clean(row[6]).lower()


def current_batch() -> tuple[dict[str, object], dict[str, object]] | None:
    return batches.next_unresolved_batch(batches.visual_rows(), batches.contour_rows())


def unique_current_targets(visual_items: list[list[str]]) -> list[edit_targets.EditTarget]:
    seen: set[tuple[str, str, str]] = set()
    targets: list[edit_targets.EditTarget] = []
    for row in visual_items:
        key = clean(row[0])
        for target in edit_targets.row_targets(key):
            path_key = str(target.path.relative_to(ROOT)) if target.path else "missing"
            target_key = (target.ufo.name, target.glyph_name, path_key)
            if target_key in seen:
                continue
            seen.add(target_key)
            targets.append(target)
    return targets


def glyph_focus_rows(targets: list[edit_targets.EditTarget]) -> list[tuple[str, list[edit_targets.EditTarget], list[str]]]:
    by_glyph: dict[str, list[edit_targets.EditTarget]] = {}
    for target in targets:
        by_glyph.setdefault(target.glyph_name, []).append(target)

    rows: list[tuple[str, list[edit_targets.EditTarget], list[str]]] = []
    for glyph_name, glyph_targets in sorted(by_glyph.items()):
        sources = sorted({target.source for target in glyph_targets})
        rows.append((glyph_name, glyph_targets, sources))
    return rows


def review_command(key: str, outcome: str, notes: str) -> str:
    return (
        f'make arabic-visual-review-update REVIEW_KEY={key} '
        f'REVIEW_STATUS={outcome} REVIEWER="Name YYYY-MM-DD" '
        f'NOTES="{notes}"'
    )


def proof_weight_for_key(key: str) -> str | None:
    for label in ("regular", "medium", "semibold", "bold"):
        if key.startswith(f"proof-{label}-"):
            return {"semibold": "SemiBold"}.get(label, label.capitalize())
    return None


def filter_exact_proof_weight(paths: list[Path], key: str) -> list[Path]:
    weight = proof_weight_for_key(key)
    if weight is None:
        return paths
    proof_paths = [path for path in paths if path.parent.name == "Proof"]
    other_paths = [path for path in paths if path.parent.name != "Proof"]
    exact_proofs = [path for path in proof_paths if path.name.startswith(f"{weight}-")]
    return exact_proofs + other_paths


def resolved_evidence_paths(key: str, evidence: str) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for part in evidence.split(";"):
        token = clean(part)
        if not token:
            continue
        matches = sorted(ROOT.glob(token)) if any(char in token for char in "*?[]") else [ROOT / token]
        for path in matches:
            if path.exists() and path not in seen:
                seen.add(path)
                paths.append(path)
    return filter_exact_proof_weight(paths, key)


def relative_markdown(path: Path) -> str:
    return f"`{path.relative_to(ROOT)}`"


def markdown_report() -> str:
    batch = current_batch()
    rows = runbook.visual_rows()
    pending = [row for row in rows if row.status in {"pending", "fix-needed"}]
    passed = [row for row in rows if row.status == "pass"]
    deferred = [row for row in rows if row.status == "deferred"]

    lines = [
        "# Arabic Drawing Session Checklist",
        "",
        "This generated checklist is the short working surface for today's",
        "Arabic hand-review and cleanup session. It points to the current",
        "batch, the exact source files to touch if a row becomes",
        "`fix-needed`, and the commands that keep the Google Fonts handoff",
        "evidence fresh.",
        "",
        "## Current State",
        "",
        f"- Pending or fix-needed visual rows: {len(pending)}",
        f"- Passed visual rows: {len(passed)}",
        f"- Deferred visual rows: {len(deferred)}",
        "- Edit rule: review first, then edit only the specific glyphs named in a `fix-needed` row.",
        "- Compatibility rule: edit Regular and Bold together and preserve contour order, point count, and point types.",
        "- Style rule: keep Virtua's monoline geometric drawing, even coordinates, and 16-unit chamfer logic.",
        "",
        "## Start Here",
        "",
        "1. Run `make arabic-before-drawing-check` before opening the sources.",
        "2. Open `documentation/glyph-review/arabic-print-proof.pdf` and `documentation/glyph-review/arabic-print-proof-index.md`.",
        "3. Open `documentation/glyph-review/arabic-current-review-worksheet.md` for the current five-row sheet.",
        "4. Open `documentation/glyph-review/arabic-next-review-board.html` for snapshots, AI notes, proof links, and edit targets.",
        "5. Record each row as `pass`, `fix-needed`, or `deferred` using the row commands below; do not leave reviewed rows implicit.",
        "6. Optional: use `make arabic-visual-review-batch-tsv` only if you want a small batch-entry form instead of one command per row.",
        "",
        "Editor checks for this session:",
        "",
        "- `make arabic-before-drawing-check` runs the UFO editor and Runebender/Norad source-load checks.",
        "- `make arabic-source-edit-diff-check` shows whether changed Arabic-like GLIF files are edited in both Regular and Bold.",
        "- `make arabic-first-batch-source-checkpoint` records current Regular/Bold structure for the first-batch watch glyphs.",
        "- `make arabic-pending-source-checkpoint` records Regular/Bold structure for all unresolved review source targets.",
        "- `make ufo-editor-check` validates both UFO packages and every GLIF in strict mode.",
        "- `make runebender-ufo-check` validates both active UFOs with the same Norad loader family Runebender uses.",
        "- The canonical review record is `documentation/glyph-review/arabic-visual-review-log.md`; the TSV is only an optional temporary input form.",
        "- If you use the TSV form, `make arabic-visual-review-batch-apply-check` applies it, regenerates reports, and reruns preflight.",
        "- If either check fails, fix the source package before drawing.",
        "",
    ]

    if batch is None:
        lines.extend(
            [
                "## Current Batch",
                "",
                "No unresolved Arabic review batch remains.",
                "",
            ]
        )
    else:
        batch_def, state = batch
        visual_items = [
            row
            for row in state["visual_items"]
            if status(row) in {"pending", "fix-needed"}
        ]
        targets = unique_current_targets(visual_items)
        existing, missing = edit_targets.target_summary(targets)
        lines.extend(
            [
                "## Current Batch",
                "",
                f"- Name: {batch_def['name']}",
                f"- Why: {batch_def['why']}",
                f"- Visual rows to decide: {len(visual_items)}",
                f"- Source targets if fixes are needed: {existing} existing, {missing} missing",
                "",
                "### Review Rows",
                "",
            ]
        )
        for row in visual_items:
            key = clean(row[0])
            area = clean(row[1])
            item = clean(row[2])
            evidence = clean(row[3])
            cue = clean(row[5])
            paths = resolved_evidence_paths(key, evidence)
            snapshot = ROOT / "documentation/glyph-review/review-snapshots" / f"{key}.png"
            if snapshot.exists() and snapshot not in paths:
                paths.append(snapshot)
            lines.extend(
                [
                    f"- `{key}` ({area}: {item})",
                    f"  - Cue: {cue}",
                ]
            )
            if paths:
                lines.append(
                    "  - Open: " + "; ".join(relative_markdown(path) for path in paths)
                )
            else:
                lines.append(f"  - Evidence: `{evidence}`")
            lines.extend(
                [
                    f"  - Pass: `{review_command(key, 'pass', 'reviewed current proof/source evidence')}`",
                    f"  - Fix: `{review_command(key, 'fix-needed', 'specific glyph or proof issue')}`",
                    f"  - Defer: `{review_command(key, 'deferred', 'needs Arabic native-reader review')}`",
                ]
            )
        lines.extend(["", "### Source Files To Touch Only After `fix-needed`", ""])
        if not targets:
            lines.append("- No direct source targets for this batch; record exact glyph names in the review log if a fix is needed.")
        else:
            for target in targets:
                lines.append(f"- {target.markdown()}")
        lines.append("")

        focus_rows = glyph_focus_rows(targets)
        if focus_rows:
            lines.extend(
                [
                    "### Glyph-Level Drawing Punchlist",
                    "",
                    "Use this as the first-pass inspection order before changing",
                    "outlines. If a glyph needs work, edit the Regular and Bold",
                    "source files as a pair, then run the edit-loop checks below.",
                    "",
                    "| Glyph | Masters | Review prompt source |",
                    "| --- | --- | --- |",
                ]
            )
            for glyph_name, glyph_targets, sources in focus_rows:
                masters = ", ".join(
                    sorted({target.ufo.name.replace("VirtuaGrotesk-", "").replace(".ufo", "") for target in glyph_targets})
                )
                lines.append(
                    f"| `{glyph_name}` | {masters} | {'; '.join(sources)} |"
                )
            lines.append("")

    lines.extend(
        [
            "## Edit Loop",
            "",
            "After any source edit:",
            "",
            "```bash",
            "make arabic-source-edit-diff-check",
            "make arabic-first-batch-source-checkpoint",
            "make arabic-pending-source-checkpoint",
            "make arabic-after-drawing-check",
            "```",
            "",
            "The diff check is a fast git-status guard for one-sided",
            "Arabic-like GLIF edits. The source checkpoint records the first",
            "batch's Regular/Bold structure after edits, and the pending",
            "checkpoint checks every unresolved row's source targets. The",
            "after-drawing target remains the full source/load/build/report/preflight check.",
            "",
            "That target runs `make ufo-editor-check`, `make runebender-ufo-check`,",
            "`./build.sh`, `make reports-only`, and `make preflight-only` in order.",
            "",
            "After shaping-sensitive edits, also run:",
            "",
            "```bash",
            "make preflight",
            "make kerning-proof-check",
            "make kerning-proof-review-check",
            "```",
            "",
            "Before closing the Arabic goal, verify `documentation/glyph-review/arabic-goal-completion-audit.md`",
            "shows every requirement as proven, including human visual review.",
            "",
            "## Optional Batch Recording Shortcut",
            "",
            "The per-row commands above are the clearest path. If you prefer",
            "to record several reviewed rows at once, use the generated TSV",
            "as a temporary input form:",
            "",
            "```bash",
            "make arabic-visual-review-batch-tsv",
            "$EDITOR documentation/glyph-review/arabic-visual-review-batch.tsv",
            "make arabic-visual-review-batch-dry-run",
            "make arabic-visual-review-batch-apply-check",
            "```",
            "",
            "Leave rows blank until they are actually reviewed. Valid statuses are",
            "`pass`, `fix-needed`, and `deferred`. The TSV is not canonical;",
            "the canonical record remains `documentation/glyph-review/arabic-visual-review-log.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
