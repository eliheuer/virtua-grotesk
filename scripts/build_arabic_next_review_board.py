#!/usr/bin/env python3
"""Build a local HTML board for the current Arabic next-review packet."""

from __future__ import annotations

from pathlib import Path
import html
import os
import re
import sys

import report_arabic_manual_edit_targets as edit_targets
from report_arabic_manual_review_batches import BATCHES as REVIEW_BATCHES
from report_arabic_visual_review_runbook import (
    ROOT,
    command,
    evidence_lines,
    machine_precheck_lines,
    row_priority,
    visual_rows,
)


TRIAGE = ROOT / "documentation/arabic-next-review-ai-triage.md"
OBSERVATIONS = ROOT / "documentation/arabic-next-review-ai-observations.md"
SNAPSHOTS = ROOT / "documentation/arabic-next-review-snapshots.md"
EDIT_TARGETS = ROOT / "documentation/arabic-manual-edit-targets.md"
CURRENT_WORKSHEET = ROOT / "documentation/arabic-current-review-worksheet.md"
BATCH_RECORDER = ROOT / "documentation/arabic-batch-recorder.md"
FULL_QUEUE_SWEEP = ROOT / "documentation/arabic-full-queue-ai-sweep.md"
FIRST_REVIEW_SWEEP = ROOT / "documentation/arabic-first-review-ai-sweep.md"
FIRST_REVIEW_ZOOM = ROOT / "documentation/arabic-first-review-zoom-snapshots.md"
OUTPUT_DEFAULT = ROOT / "documentation/arabic-next-review-board.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def relative_href(repo_path: str, output_path: Path) -> str:
    target = ROOT / repo_path
    if not target.exists():
        return ""
    return html.escape(os.path.relpath(target.resolve(), output_path.parent.resolve()))


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    body = text[start + len(heading) :]
    next_heading = re.search(r"\n## ", body)
    return body[: next_heading.start()] if next_heading else body


def code_to_html(value: str) -> str:
    escaped = html.escape(value)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def parse_triage_rows(text: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    triage = section(text, "## First-Batch AI Triage Summary")
    if not triage:
        triage = section(text, "## AI Triage Summary")
    for line in triage.splitlines():
        if not line.startswith("| `"):
            continue
        row = cells(line)
        if len(row) < 5:
            continue
        key = row[0].strip("`")
        snapshot_cells = row[1].split("<br>")
        snapshots: list[tuple[str, str]] = []
        for item in snapshot_cells:
            match = re.search(r"`([^`]+\.png)` from `([^`]+\.html)`", item)
            if match:
                snapshots.append((match.group(1), match.group(2)))
        rows.append(
            {
                "key": key,
                "snapshots": snapshots,
                "blockers": row[2],
                "classification": row[3],
                "human_need": row[4],
            }
        )
    return rows


def parse_prompt_rows(text: str) -> list[tuple[str, str, str]]:
    prompts = section(text, "## Structure Prompts To Inspect")
    rows: list[tuple[str, str, str]] = []
    for line in prompts.splitlines():
        if not line.startswith("| `"):
            continue
        row = cells(line)
        if len(row) >= 3:
            rows.append((row[0].strip("`"), row[1].strip("`"), row[2]))
    return rows


def parse_commands(text: str) -> list[str]:
    commands = section(text, "## Guarded Update Commands")
    match = re.search(r"```bash\n(?P<body>.*?)\n```", commands, flags=re.DOTALL)
    if not match:
        return []
    return [line for line in match.group("body").splitlines() if line.strip()]


def parse_observations(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    observations = section(text, "## Observations")
    for line in observations.splitlines():
        if not line.startswith("| `"):
            continue
        row = cells(line)
        if len(row) >= 3:
            rows[row[0].strip("`")] = (row[1], row[2])
    return rows


def parse_snapshot_rows(text: str) -> dict[str, list[tuple[str, str, str]]]:
    rows: dict[str, list[tuple[str, str, str]]] = {}
    snapshots_section = section(text, "## Snapshots")
    for line in snapshots_section.splitlines():
        if not line.startswith("| `"):
            continue
        row = cells(line)
        if len(row) < 4:
            continue
        key = row[0].strip("`")
        label = row[1]
        source = row[2].strip("`")
        png = row[3].strip("`")
        rows.setdefault(key, []).append((label, source, png))
    return rows


def parse_full_queue_ai_rows(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    observations = section(text, "## Row Observations")
    for line in observations.splitlines():
        if not line.startswith("| `"):
            continue
        row = cells(line)
        if len(row) >= 4:
            rows[row[0].strip("`")] = (row[2], row[3])
    return rows


def parse_edit_target_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    current_key = ""
    for line in text.splitlines():
        match = re.match(r"^### `([^`]+)`", line)
        if match:
            current_key = match.group(1)
            rows[current_key] = []
            continue
        if line.startswith("### "):
            current_key = ""
            continue
        if not current_key:
            continue
        if (
            line.startswith("- Source targets:")
            or line.startswith("- Edit target guidance:")
            or re.match(r"^- `", line)
            or re.match(r"^  - `", line)
        ):
            rows[current_key].append(line)
    return rows


def commands_for_key(commands: list[str], key: str) -> list[str]:
    needle = f"REVIEW_KEY={key} "
    return [command for command in commands if needle in command]


def row_update_commands(row) -> str:
    return "\n".join(
        html.escape(command(row, status, note))
        for status, note in (
            ("pass", "reviewed current proof"),
            ("fix-needed", "specific glyph or proof issue"),
            ("deferred", "needs Arabic native-reader review"),
        )
    )


def markdown_lines_to_html(lines: list[str], output_path: Path) -> str:
    items: list[str] = []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        text = text.removeprefix("- ").strip()
        escaped = html.escape(text)

        def link_path(match: re.Match[str]) -> str:
            repo_path = match.group(1)
            link = relative_href(repo_path, output_path)
            if not link:
                return f"<code>{html.escape(repo_path)}</code>"
            return f"<a href='{link}'><code>{html.escape(repo_path)}</code></a>"

        escaped = re.sub(r"`([^`]+)`", link_path, escaped)
        items.append(f"<li>{escaped}</li>")
    if not items:
        return "<p class='muted'>None recorded.</p>"
    return f"<ul>{''.join(items)}</ul>"


def edit_target_html(
    key: str,
    edit_targets: dict[str, list[str]],
    output_path: Path,
    target_limit: int = 12,
) -> str:
    lines = edit_targets.get(key, [])
    if not lines:
        lines = [
            "- Edit target guidance: no row-specific source targets were generated; record exact glyph names if this row becomes `fix-needed`."
        ]

    kept: list[str] = []
    omitted = 0
    target_count = 0
    for line in lines:
        if re.match(r"^  - `", line):
            target_count += 1
            if target_count > target_limit:
                omitted += 1
                continue
        kept.append(line)

    if omitted:
        kept.append(f"- Additional GLIF targets omitted here: {omitted}; open the full target report before editing.")
    kept.append(f"- Full target report: `{display_path(EDIT_TARGETS)}`")
    return markdown_lines_to_html(kept, output_path)


def linked_resource(path: Path, output_path: Path) -> str:
    link = relative_href(display_path(path), output_path)
    label = display_path(path)
    if not link:
        return f"<code>{html.escape(label)}</code>"
    return f"<a href='{link}'><code>{html.escape(label)}</code></a>"


def snapshot_links_for_key(
    key: str,
    snapshots: dict[str, list[tuple[str, str, str]]],
    output_path: Path,
) -> str:
    found = snapshots.get(key, [])
    if not found:
        return "<span class='muted'>No PNG</span>"
    items: list[str] = []
    for label, source, png in found:
        source_link = relative_href(source, output_path)
        png_link = relative_href(png, output_path)
        source_html = (
            f"<a href='{source_link}'>Source</a>"
            if source_link
            else "<span class='muted'>Source missing</span>"
        )
        if png_link:
            image_html = (
                f"<a href='{png_link}'><img class='queue-thumb' src='{png_link}' "
                f"alt='{html.escape(key)} {html.escape(label)} snapshot'></a>"
            )
        else:
            image_html = "<span class='muted'>PNG missing</span>"
        items.append(
            "<figure class='queue-shot'>"
            f"{image_html}"
            f"<figcaption>{html.escape(label)} · {source_html}</figcaption>"
            "</figure>"
        )
    return "".join(items)


def full_queue_table(
    output_path: Path,
    snapshots: dict[str, list[tuple[str, str, str]]],
    edit_targets: dict[str, list[str]],
    full_queue_ai_rows: dict[str, tuple[str, str]],
) -> str:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    rows = sorted(rows, key=row_priority)
    body: list[str] = []
    for index, row in enumerate(rows, start=1):
        evidence_html = markdown_lines_to_html(evidence_lines(row), output_path)
        precheck_html = markdown_lines_to_html(machine_precheck_lines(row), output_path)
        edit_target_details = edit_target_html(row.key, edit_targets, output_path)
        ai_observation, human_follow_up = full_queue_ai_rows.get(
            row.key,
            ("No AI observation recorded for this row.", "Open the linked evidence and record a human decision."),
        )
        body.append(
            "<tr>"
            f"<td>{index}</td>"
            f"<td><code>{html.escape(row.key)}</code></td>"
            f"<td>{html.escape(row.area)}</td>"
            f"<td>{html.escape(row.item)}</td>"
            f"<td><span class='status'>{html.escape(row.status)}</span></td>"
            f"<td>{snapshot_links_for_key(row.key, snapshots, output_path)}</td>"
            f"<td>{html.escape(row.cue)}</td>"
            f"<td>{code_to_html(ai_observation)}</td>"
            f"<td>{code_to_html(human_follow_up)}</td>"
            "<td>"
            "<details><summary>Evidence</summary>"
            f"{evidence_html}"
            "</details>"
            "<details><summary>Precheck</summary>"
            f"{precheck_html}"
            "</details>"
            "<details><summary>Edit targets</summary>"
            f"{edit_target_details}"
            "</details>"
            "<details><summary>Update commands</summary>"
            f"<pre>{row_update_commands(row)}</pre>"
            "</details>"
            "</td>"
            "</tr>"
        )
    return "\n".join(body)


def review_steps(rows: list[dict[str, object]]) -> str:
    items: list[str] = []
    for index, row in enumerate(rows, start=1):
        key = str(row["key"])
        items.append(
            "<li>"
            f"<a href='#{html.escape(key)}'><code>{html.escape(key)}</code></a>"
            f"<span>{html.escape(str(row['human_need']))}</span>"
            "</li>"
        )
    return "\n".join(items)


def batch_punchlist_html(output_path: Path) -> str:
    pending_keys = {row.key for row in visual_rows() if row.status in {"pending", "fix-needed"}}
    sections: list[str] = []
    for batch in REVIEW_BATCHES:
        keys = [key for key in batch["visual_keys"] if key in pending_keys]
        if not keys:
            continue

        by_glyph: dict[str, dict[str, set[str]]] = {}
        for key in keys:
            for target in edit_targets.row_targets(key):
                entry = by_glyph.setdefault(
                    target.glyph_name, {"masters": set(), "sources": set()}
                )
                entry["masters"].add(
                    target.ufo.name.replace("VirtuaGrotesk-", "").replace(".ufo", "")
                )
                entry["sources"].add(target.source)

        if not by_glyph:
            continue

        rows: list[str] = []
        for glyph_name in sorted(by_glyph):
            entry = by_glyph[glyph_name]
            rows.append(
                "<tr>"
                f"<td><code>{html.escape(glyph_name)}</code></td>"
                f"<td>{html.escape(', '.join(sorted(entry['masters'])))}</td>"
                f"<td>{code_to_html('; '.join(sorted(entry['sources'])))}</td>"
                "</tr>"
            )
        sections.append(
            "<details class='punchlist' open>"
            f"<summary>{html.escape(str(batch['name']))}</summary>"
            "<table class='compact-table'>"
            "<thead><tr><th>Glyph</th><th>Masters</th><th>Review prompt source</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody>"
            "</table>"
            "</details>"
        )

    if not sections:
        return "<p class='muted'>No pending batch source-glyph punchlists.</p>"
    return "".join(sections)


def row_card(
    row: dict[str, object],
    commands: list[str],
    observations: dict[str, tuple[str, str]],
    edit_targets: dict[str, list[str]],
    output_path: Path,
) -> str:
    key = str(row["key"])
    snapshots = row["snapshots"]
    snapshot_html = []
    for png, source in snapshots:  # type: ignore[assignment]
        source_link = relative_href(source, output_path)
        png_link = relative_href(png, output_path)
        if png_link:
            image = f"<a href='{png_link}'><img src='{png_link}' alt='{html.escape(key)} snapshot'></a>"
        else:
            image = "<div class='missing'>Snapshot missing</div>"
        source_caption = (
            f"<a href='{source_link}'>{html.escape(source)}</a>"
            if source_link
            else html.escape(source)
        )
        snapshot_html.append(
            "<figure>"
            f"{image}"
            f"<figcaption>{source_caption}</figcaption>"
            "</figure>"
        )
    command_html = "\n".join(html.escape(command) for command in commands_for_key(commands, key))
    observation = observations.get(key)
    edit_target_details = edit_target_html(key, edit_targets, output_path)
    observation_html = ""
    if observation:
        ai_observation, human_action = observation
        observation_html = (
            "<div class='observation'>"
            "<h3>AI First-Pass Observation</h3>"
            f"<p>{code_to_html(ai_observation)}</p>"
            "<h3>Suggested Human Action</h3>"
            f"<p>{code_to_html(human_action)}</p>"
            "</div>"
        )
    return (
        f"<section class='card' id='{html.escape(key)}'>"
        f"<h2><code>{html.escape(key)}</code></h2>"
        "<dl>"
        f"<dt>Mechanical blockers</dt><dd>{html.escape(str(row['blockers']))}</dd>"
        f"<dt>AI-safe classification</dt><dd>{html.escape(str(row['classification']))}</dd>"
        f"<dt>Human decision needed</dt><dd>{html.escape(str(row['human_need']))}</dd>"
        "</dl>"
        f"<div class='snapshots'>{''.join(snapshot_html)}</div>"
        f"{observation_html}"
        "<details>"
        "<summary>Edit targets</summary>"
        f"{edit_target_details}"
        "</details>"
        "<details>"
        "<summary>Update commands</summary>"
        f"<pre>{command_html}</pre>"
        "</details>"
        "</section>"
    )


def html_report(output_path: Path) -> str:
    triage_text = read(TRIAGE)
    observation_text = read(OBSERVATIONS)
    snapshot_text = read(SNAPSHOTS)
    edit_target_text = read(EDIT_TARGETS)
    full_queue_text = read(FULL_QUEUE_SWEEP)
    rows = parse_triage_rows(triage_text)
    prompts = parse_prompt_rows(triage_text)
    commands = parse_commands(triage_text)
    observations = parse_observations(observation_text)
    snapshots = parse_snapshot_rows(snapshot_text)
    edit_targets = parse_edit_target_rows(edit_target_text)
    full_queue_ai_rows = parse_full_queue_ai_rows(full_queue_text)
    observations_link = relative_href(display_path(OBSERVATIONS), output_path)
    edit_targets_link = relative_href(display_path(EDIT_TARGETS), output_path)
    cards = "\n".join(row_card(row, commands, observations, edit_targets, output_path) for row in rows)
    steps = review_steps(rows)
    queue_rows = full_queue_table(output_path, snapshots, edit_targets, full_queue_ai_rows)
    batch_punchlists = batch_punchlist_html(output_path)
    prompt_rows = "\n".join(
        f"<tr><td><code>{html.escape(codepoint)}</code></td><td><code>{html.escape(glyphs)}</code></td><td>{code_to_html(prompt)}</td></tr>"
        for codepoint, glyphs, prompt in prompts
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virtua Grotesk Arabic Next Review Board</title>
<style>
:root {{
  --bg: #f5f3ee;
  --paper: #fffdfa;
  --ink: #171717;
  --muted: #62605b;
  --line: #d8d2c8;
  --accent: #006c67;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
main {{
  max-width: 1440px;
  margin: 0 auto;
  padding: 28px 22px 60px;
}}
header {{
  margin-bottom: 22px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 30px;
  line-height: 1.1;
}}
p {{
  max-width: 860px;
  color: var(--muted);
  line-height: 1.45;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 18px;
  align-items: start;
}}
.review-flow {{
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(320px, 1.25fr);
  gap: 18px;
  margin: 18px 0 24px;
}}
.card {{
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
}}
.panel {{
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
}}
h2 {{
  margin: 0 0 12px;
  font-size: 18px;
}}
.panel h2 {{
  margin-bottom: 10px;
}}
.review-list {{
  margin: 0;
  padding-left: 24px;
}}
.review-list li {{
  margin-bottom: 10px;
  padding-left: 4px;
}}
.review-list span {{
  display: block;
  margin-top: 3px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.35;
}}
.decision-rules {{
  margin: 0;
  padding-left: 20px;
  color: var(--muted);
  line-height: 1.45;
}}
.decision-rules li {{
  margin-bottom: 8px;
}}
.punchlist {{
  margin: 0 0 12px;
}}
.compact-table {{
  margin: 12px 0 0;
}}
.compact-table th,
.compact-table td {{
  font-size: 13px;
  padding: 7px 9px;
}}
dl {{
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 8px 12px;
  margin: 0 0 14px;
  font-size: 14px;
}}
dt {{ color: var(--muted); }}
dd {{ margin: 0; }}
.snapshots {{
  display: grid;
  gap: 12px;
}}
figure {{
  margin: 0;
  border: 1px solid var(--line);
  background: white;
}}
img {{
  display: block;
  width: 100%;
  height: auto;
}}
.queue-shot {{
  margin: 0 0 8px;
  max-width: 220px;
}}
.queue-thumb {{
  max-width: 220px;
  border: 1px solid var(--line);
}}
figcaption {{
  padding: 8px 10px;
  border-top: 1px solid var(--line);
  font-size: 12px;
  color: var(--muted);
  overflow-wrap: anywhere;
}}
a {{ color: var(--accent); }}
details {{
  margin-top: 12px;
}}
summary {{
  cursor: pointer;
  color: var(--accent);
  font-weight: 600;
}}
pre {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f2eee7;
  border: 1px solid var(--line);
  padding: 10px;
  border-radius: 6px;
  font-size: 12px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--paper);
  border: 1px solid var(--line);
  margin: 24px 0;
}}
th, td {{
  border-bottom: 1px solid var(--line);
  padding: 9px 10px;
  text-align: left;
  vertical-align: top;
  font-size: 14px;
}}
th {{
  color: var(--muted);
  font-weight: 600;
}}
.observation {{
  margin-top: 12px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #f8f6f1;
}}
.observation h3 {{
  margin: 0 0 6px;
  font-size: 13px;
  color: var(--muted);
}}
.observation p {{
  margin: 0 0 10px;
  color: var(--ink);
  font-size: 14px;
}}
.observation p:last-child {{
  margin-bottom: 0;
}}
.muted {{
  color: var(--muted);
}}
.status {{
  display: inline-block;
  padding: 2px 7px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: #f8f6f1;
  color: var(--muted);
  font-size: 12px;
  white-space: nowrap;
}}
code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.92em;
}}
.missing {{
  padding: 60px 16px;
  text-align: center;
  color: #8a2d20;
}}
</style>
</head>
<body>
<main>
<header>
<h1>Arabic Next Review Board</h1>
<p>Generated from <code>{display_path(TRIAGE)}</code>, <a href="{observations_link}"><code>{display_path(OBSERVATIONS)}</code></a>, and <a href="{edit_targets_link}"><code>{display_path(EDIT_TARGETS)}</code></a>. This page embeds the current first-batch snapshots, AI first-pass observations, edit targets, and update commands for hand review. It is a triage aid only; final row status still comes from reviewing the proof HTML/source glyphs.</p>
<p class="muted">Review resources: {linked_resource(CURRENT_WORKSHEET, output_path)} for the current fill-in review sheet, {linked_resource(BATCH_RECORDER, output_path)} for copy-ready guarded status commands, {linked_resource(FULL_QUEUE_SWEEP, output_path)} for all pending-row AI observations, {linked_resource(FIRST_REVIEW_SWEEP, output_path)} for the current first-batch sweep, and {linked_resource(FIRST_REVIEW_ZOOM, output_path)} for focused Arabic-row crop PNGs.</p>
</header>
<section class="review-flow">
<div class="panel">
<h2>First-Batch Order</h2>
<ol class="review-list">
{steps}
</ol>
</div>
<div class="panel">
<h2>Decision Rules</h2>
<ul class="decision-rules">
<li>Use the PNG snapshot only for a quick first pass; open the linked proof HTML or source evidence before recording a row outcome.</li>
<li>Record <code>pass</code> only when the linked proof/source evidence has no visible missing, clipped, malformed, duplicated, wrong-codepoint, spacing, mark, or structure issue for that row.</li>
<li>Record <code>fix-needed</code> with the exact glyph, proof location, or source file when a concrete drawing, spacing, mark, or shaping problem is visible.</li>
<li>Record <code>deferred</code> when the row needs Arabic native-reader or script-specialist judgment rather than more mechanical checks.</li>
</ul>
</div>
</section>
<section class="panel">
<h2>Batch Glyph Punchlists</h2>
<p class="muted">These source-glyph lists are generated from <code>{display_path(EDIT_TARGETS)}</code>. Use them as an overview before editing; only change outlines after a row is marked <code>fix-needed</code>.</p>
{batch_punchlists}
</section>
<div class="grid">
{cards}
</div>
<h2>Structure Prompts</h2>
<table>
<thead><tr><th>Codepoint</th><th>Glyphs</th><th>Prompt</th></tr></thead>
<tbody>
{prompt_rows}
</tbody>
</table>
<h2>Full Pending Queue</h2>
<p>This queue comes from <code>documentation/arabic-visual-review-log.md</code> and the PNG coverage report. Use the first-batch cards above for the fastest current pass, then continue through this table without regenerating context.</p>
<table>
<thead><tr><th>#</th><th>Key</th><th>Area</th><th>Item</th><th>Status</th><th>Snapshot</th><th>Review cue</th><th>AI observation</th><th>Human follow-up</th><th>Links and commands</th></tr></thead>
<tbody>
{queue_rows}
</tbody>
</table>
</main>
</body>
</html>
"""


def validate_local_links(output_path: Path) -> list[str]:
    text = output_path.read_text(encoding="utf-8")
    missing: list[str] = []
    for attr, _, value in re.findall(r"\b(href|src)=(['\"])(.*?)\2", text):
        if value.startswith(("http:", "https:", "mailto:", "#")):
            continue
        target = (output_path.parent / html.unescape(value)).resolve()
        if not target.exists():
            missing.append(f"{attr}={value}")
    return missing


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_report(output), encoding="utf-8")
    missing = validate_local_links(output)
    if missing:
        for item in missing:
            print(f"missing board link: {item}", file=sys.stderr)
        return 1
    print(display_path(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
