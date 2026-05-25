#!/usr/bin/env python3
"""Generate a compact batch plan for the remaining Arabic manual review."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

from report_arabic_visual_review_runbook import split_markdown_row


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "documentation/arabic-manual-review-batches.md"
VISUAL_LOG = ROOT / "documentation/arabic-visual-review-log.md"
CONTOUR_LOG = ROOT / "documentation/contour-cleanup-decision-log.md"
SNAPSHOT_REPORT = ROOT / "documentation/arabic-next-review-snapshots.md"
SNAPSHOT_INTEGRITY = ROOT / "documentation/arabic-snapshot-integrity.md"
ZOOM_SNAPSHOT_REPORT = ROOT / "documentation/arabic-first-review-zoom-snapshots.md"
FULL_QUEUE_AI_SWEEP = ROOT / "documentation/arabic-full-queue-ai-sweep.md"


BATCHES = [
    {
        "name": "1. Open The Fast Dashboard",
        "why": "Start with one screen that shows embedded Arabic samples, visual-risk rows, contour previews, and proof links.",
        "visual_keys": [],
        "contour_categories": [],
        "commands": [
            "make arabic-manual-review-dashboard",
            "open documentation/arabic-manual-review-dashboard.html",
            "open documentation/arabic-next-review-batch.html",
        ],
        "decision": "Use this only to orient the review; record pass/fix decisions in the logs below.",
    },
    {
        "name": "2. Structure And Wrong-Glyph Sweep",
        "why": "Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.",
        "visual_keys": [
            "proof-regular-glyphs",
            "proof-medium-glyphs",
            "proof-semibold-glyphs",
            "proof-bold-glyphs",
            "class-letter-structures",
        ],
        "contour_categories": ["source outline review", "Arabic letter or positional form"],
        "extra_evidence": [
            "documentation/arabic-structure-sweep.html",
            "documentation/arabic-structure-triage.md",
        ],
        "decision": "Mark contour rows `fix-now` for source edits, or `accepted` only after comparing source and rendered proof.",
    },
    {
        "name": "3. Marks, Dotted Circle, And Stacking",
        "why": "Arabic Core is mechanically present, but marks still need visual attachment and stacking review.",
        "visual_keys": [
            "mark-base+fatha",
            "mark-base+damma",
            "mark-base+kasra",
            "mark-shadda+sukun",
            "mark-tanween",
            "mark-hamza-above-below",
            "mark-dotted-circle",
            "class-mark-combinations",
        ],
        "contour_categories": ["Arabic mark or mark combination"],
        "extra_evidence": [
            "documentation/arabic-mark-review-proof.html",
            "documentation/arabic-mark-triage.md",
        ],
        "decision": "Review real-base attachment and dotted-circle behavior before accepting or editing mark composites.",
    },
    {
        "name": "4. Dot-Stack Helpers And Urdu/Persian Texture",
        "why": "Three-dot and six-dot helpers are likely to need Bold/variable separation checks.",
        "visual_keys": ["class-dot-stack-helpers"],
        "contour_categories": ["Arabic dot-stack helper"],
        "decision": "Fix only if dots merge, collide, or break the intended geometric texture.",
    },
    {
        "name": "5. RTL Text, Punctuation, Numerals, And Spacing",
        "why": "Once glyph structures look sane, review the typography in proof text, proofer, and waterfall views.",
        "visual_keys": [
            "proof-regular-text",
            "proof-regular-proofer",
            "proof-regular-waterfall",
            "proof-medium-text",
            "proof-medium-proofer",
            "proof-medium-waterfall",
            "proof-semibold-text",
            "proof-semibold-proofer",
            "proof-semibold-waterfall",
            "proof-bold-text",
            "proof-bold-proofer",
            "proof-bold-waterfall",
            "smoke-salaam",
            "smoke-arabic",
            "smoke-bismillah",
            "smoke-lam-alef",
            "class-arabic-farsi-numerals",
            "class-arabic-punctuation",
        ],
        "contour_categories": ["shared punctuation"],
        "decision": "Use `fix-needed` for visual log rows when spacing or rhythm needs drawing work; use `pass` only after checking all weights.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rows(text: str) -> list[list[str]]:
    parsed: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] == "---":
            continue
        parsed.append(cells)
    return parsed


def clean(value: str) -> str:
    return value.strip().strip("`")


def visual_rows() -> dict[str, list[str]]:
    items: dict[str, list[str]] = {}
    for row in rows(read(VISUAL_LOG)):
        if len(row) >= 8 and row[0].startswith("`"):
            items[clean(row[0])] = row
    return items


def contour_rows() -> list[list[str]]:
    return [row for row in rows(read(CONTOUR_LOG)) if len(row) >= 9 and row[0].startswith("`")]


def snapshot_rows() -> dict[str, list[list[str]]]:
    by_key: dict[str, list[list[str]]] = {}
    for row in rows(read(SNAPSHOT_REPORT)):
        if len(row) == 4 and row[0].startswith("`"):
            by_key.setdefault(clean(row[0]), []).append(row)
    return by_key


def zoom_snapshot_rows() -> dict[str, list[list[str]]]:
    by_key: dict[str, list[list[str]]] = {}
    for row in rows(read(ZOOM_SNAPSHOT_REPORT)):
        if len(row) == 4 and row[0].startswith("`"):
            by_key.setdefault(clean(row[0]), []).append(
                [
                    row[0],
                    f"{row[1]} focused 2x crop",
                    row[2],
                    row[3],
                ]
            )
    return by_key


def ai_observation_rows() -> dict[str, tuple[str, str]]:
    by_key: dict[str, tuple[str, str]] = {}
    if not FULL_QUEUE_AI_SWEEP.exists():
        return by_key
    for line in read(FULL_QUEUE_AI_SWEEP).splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 4:
            continue
        key = clean(cells[0])
        by_key[key] = (cells[2], cells[3])
    return by_key


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    for line in text.splitlines():
        prefix = f"- {label}: "
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return default


def visual_status(row: list[str]) -> str:
    return row[6] if len(row) >= 9 else row[5]


def visual_cue(row: list[str]) -> str:
    return row[5] if len(row) >= 9 else row[4]


def contour_status(row: list[str]) -> str:
    return row[5]


def visual_command(key: str, status: str = "pass") -> str:
    return (
        f'make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS={status} '
        'REVIEWER="Name YYYY-MM-DD" NOTES="reviewed"'
    )


def evidence_paths(row: list[str]) -> list[str]:
    if len(row) < 4:
        return []
    paths: list[str] = []
    for raw_part in row[3].split(";"):
        part = raw_part.strip().strip("`")
        if not part.startswith("documentation/"):
            continue
        if "*" in part:
            paths.extend(
                str(path.relative_to(ROOT)) for path in sorted(ROOT.glob(part))
            )
        elif (ROOT / part).exists():
            paths.append(part)
        else:
            paths.append(part)
    return paths


def unique_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def batch_snapshot_rows(
    visual_items: list[list[str]],
    snapshots_by_key: dict[str, list[list[str]]],
    zoom_snapshots_by_key: dict[str, list[list[str]]],
) -> list[list[str]]:
    found: list[list[str]] = []
    for row in visual_items:
        key = clean(row[0])
        found.extend(snapshots_by_key.get(key, []))
        found.extend(zoom_snapshots_by_key.get(key, []))
    return found


def batch_evidence_paths(
    batch: dict[str, object],
    visual_items: list[list[str]],
    contour_items: list[list[str]],
) -> list[str]:
    paths = list(batch.get("extra_evidence", []))
    for row in visual_items:
        paths.extend(evidence_paths(row))
    for row in contour_items:
        for cell in row:
            cleaned = cell.strip().strip("`")
            if cleaned.startswith("documentation/") and (ROOT / cleaned).exists():
                paths.append(cleaned)
    return unique_paths(paths)


def contour_command(glyph: str, status: str = "fix-now") -> str:
    decision = "needs source edit" if status == "fix-now" else "reviewed style divergence"
    return (
        f"make contour-decision-update GLYPH={glyph} STATUS={status} "
        f'DECISION="{decision}" REVIEWED="Name YYYY-MM-DD"'
    )


def status_summary(values: list[str]) -> str:
    if not values:
        return "none"
    counts = Counter(values)
    order = ["pending", "pass", "fix-needed", "deferred", "fix-now", "fixed", "accepted"]
    parts = [f"{label}: {counts[label]}" for label in order if counts[label]]
    parts.extend(f"{label}: {count}" for label, count in sorted(counts.items()) if label not in order)
    return "; ".join(parts)


def pending_values(values: list[str]) -> int:
    return sum(1 for value in values if value in {"pending", "fix-needed", "fix-now"})


def batch_status(batch: dict[str, object], visual: dict[str, list[str]], contours: list[list[str]]) -> dict[str, object]:
    visual_items = [visual[key] for key in batch["visual_keys"] if key in visual]
    contour_items = [
        row for row in contours if row[3] in batch["contour_categories"]
    ]
    visual_statuses = [visual_status(row) for row in visual_items]
    contour_statuses = [contour_status(row) for row in contour_items]
    return {
        "visual_items": visual_items,
        "contour_items": contour_items,
        "visual_statuses": visual_statuses,
        "contour_statuses": contour_statuses,
        "pending": pending_values(visual_statuses) + pending_values(contour_statuses),
    }


def decision_rule(batch: dict[str, object], contour_items: list[list[str]]) -> str:
    decision = str(batch["decision"])
    if contour_items:
        return decision
    if "contour rows" in decision:
        return "Confirm the contour queue is empty, then record the visual review rows only."
    return decision


def next_unresolved_batch(
    visual: dict[str, list[str]],
    contours: list[list[str]],
) -> tuple[dict[str, object], dict[str, object]] | None:
    for batch in BATCHES:
        status = batch_status(batch, visual, contours)
        if status["pending"]:
            return batch, status
    return None


def markdown_report() -> str:
    visual = visual_rows()
    contours = contour_rows()
    snapshots_by_key = snapshot_rows()
    zoom_snapshots_by_key = zoom_snapshot_rows()
    ai_rows = ai_observation_rows()
    snapshot_integrity_text = read(SNAPSHOT_INTEGRITY)
    next_batch = next_unresolved_batch(visual, contours)
    lines = [
        "# Arabic Manual Review Batches",
        "",
        "This generated report turns the remaining Arabic visual-review and contour-decision queues into a short hand-cleanup order. It does not make design decisions; it gives the fastest sequence for recording them.",
        "",
        "Authoritative logs:",
        "",
        "- `documentation/arabic-visual-review-log.md`",
        "- `documentation/contour-cleanup-decision-log.md`",
        "- `documentation/contour-cleanup-source-edit-runlist.md`",
        "- `documentation/contour-cleanup-first-edit-batch.md`",
        "- `documentation/arabic-manual-review-dashboard.html`",
        "- `documentation/arabic-next-review-batch.html`",
        "- `documentation/arabic-next-review-snapshots.md`",
        "- `documentation/arabic-first-review-zoom-snapshots.md`",
        "- `documentation/arabic-snapshot-integrity.md`",
        "- `documentation/arabic-full-queue-ai-sweep.md`",
        "- `documentation/gftools-qa/Proof/`",
        "",
        "Snapshot evidence:",
        "",
        f"- Snapshot evidence ready for hand review: {summary_value('Snapshot evidence ready for hand review', snapshot_integrity_text)}",
        f"- Readable PNG files: {summary_value('Readable PNG files', snapshot_integrity_text)}",
        f"- Nonblank PNG files: {summary_value('Nonblank PNG files', snapshot_integrity_text)}",
        f"- Pending/fix-needed rows without snapshot: {summary_value('Pending/fix-needed rows without snapshot', snapshot_integrity_text)}",
        "- Focused first-batch zoom crops: `documentation/arabic-first-review-zoom-snapshots.md`",
        "",
        "## Next Unresolved Batch",
        "",
    ]
    if next_batch:
        batch, status = next_batch
        visual_items = status["visual_items"]
        contour_items = status["contour_items"]
        evidence = batch_evidence_paths(batch, visual_items, contour_items)
        batch_snapshots = batch_snapshot_rows(visual_items, snapshots_by_key, zoom_snapshots_by_key)
        lines.extend(
            [
                f"Start with **{batch['name']}**.",
                "",
                f"- Why: {batch['why']}",
                f"- Open decisions: {status['pending']}",
                f"- Visual rows: {len(visual_items)} ({status_summary(status['visual_statuses'])})",
                f"- Contour rows: {len(contour_items)} ({status_summary(status['contour_statuses'])})",
                f"- Decision rule: {decision_rule(batch, contour_items)}",
                "",
            ]
        )
        if evidence:
            lines.extend(["Evidence to open:", ""])
            lines.extend(f"- `{path}`" for path in evidence)
            lines.append("")
        if batch_snapshots:
            lines.extend(["Snapshot aids:", ""])
            lines.extend(
                f"- `{clean(row[0])}` {row[1]}: `{row[3].strip('`')}` from `{row[2].strip('`')}`"
                for row in batch_snapshots
            )
            lines.append("")
        if visual_items:
            first_visual = clean(visual_items[0][0])
            lines.extend(
                [
                    "First visual-review command pattern:",
                    "",
                    "```bash",
                    visual_command(first_visual),
                    "```",
                    "",
                ]
            )
        if contour_items:
            first_contour = clean(contour_items[0][0])
            lines.extend(
                [
                    "First contour-decision command patterns:",
                    "",
                    "```bash",
                    contour_command(first_contour, "fix-now"),
                    contour_command(first_contour, "accepted"),
                    "```",
                    "",
                ]
            )
    else:
        lines.extend(
            [
                "No unresolved visual-review or contour-decision rows remain.",
                "",
            ]
        )
    lines.extend(
        [
        "## Batch Queue",
        "",
        ]
    )
    for batch in BATCHES:
        status = batch_status(batch, visual, contours)
        visual_items = status["visual_items"]
        contour_items = status["contour_items"]
        evidence = batch_evidence_paths(batch, visual_items, contour_items)
        batch_snapshots = batch_snapshot_rows(visual_items, snapshots_by_key, zoom_snapshots_by_key)
        lines.extend(
            [
                f"### {batch['name']}",
                "",
                batch["why"],
                "",
                f"- Visual rows: {len(visual_items)} ({status_summary(status['visual_statuses'])})",
                f"- Contour rows: {len(contour_items)} ({status_summary(status['contour_statuses'])})",
                f"- Decision rule: {decision_rule(batch, contour_items)}",
                "",
            ]
        )
        if evidence:
            lines.extend(["Evidence to open:", ""])
            lines.extend(f"- `{path}`" for path in evidence)
            lines.append("")
        if batch_snapshots:
            lines.extend(["Snapshot aids:", ""])
            lines.extend(
                f"- `{clean(row[0])}` {row[1]}: `{row[3].strip('`')}` from `{row[2].strip('`')}`"
                for row in batch_snapshots
            )
            lines.append("")
        commands = batch.get("commands", [])
        if commands:
            lines.extend(["Commands:", ""])
            lines.extend(f"```bash\n{command}\n```" for command in commands)
            lines.append("")
        if visual_items:
            lines.extend(
                [
                    "Visual review rows:",
                    "",
                    "| Key | Area | Item | Machine precheck | Review cue | AI observation | Human follow-up | Status | Record command |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                ]
            )
            for row in visual_items:
                key = clean(row[0])
                ai_observation, human_follow_up = ai_rows.get(key, ("", ""))
                lines.append(
                    f"| `{key}` | {row[1]} | {row[2]} | {row[4]} | {visual_cue(row)} | {ai_observation} | {human_follow_up} | {visual_status(row)} | `{visual_command(key)}` |"
                )
            lines.append("")
        if contour_items:
            lines.extend(["Contour decision rows:", "", "| Source glyph | Fontspector glyph | Category | Status | Fix command | Accept command |", "| --- | --- | --- | --- | --- | --- |"])
            for row in contour_items:
                glyph = clean(row[0])
                lines.append(
                    f"| `{glyph}` | {row[1]} | {row[3]} | {contour_status(row)} | `{contour_command(glyph, 'fix-now')}` | `{contour_command(glyph, 'accepted')}` |"
                )
            lines.append("")
    lines.extend(
        [
            "## After Each Batch",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
            "Run `make contour-cleanup-proof` after source edits so the proof, queue, and decision log stay synchronized.",
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
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
