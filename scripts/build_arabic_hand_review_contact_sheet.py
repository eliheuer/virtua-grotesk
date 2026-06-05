#!/usr/bin/env python3
"""Build a print-friendly Arabic hand-review contact sheet."""

from __future__ import annotations

from pathlib import Path
import html
import os
import re
import sys

from report_arabic_hand_review_session import EDIT_TARGETS, SESSION_GROUPS
from report_arabic_visual_review_runbook import (
    ROOT,
    command,
    evidence_lines,
    machine_precheck_lines,
    row_priority,
    visual_rows,
)


SNAPSHOTS = ROOT / "documentation/glyph-review/arabic-next-review-snapshots.md"
ZOOM_SNAPSHOTS = ROOT / "documentation/glyph-review/arabic-first-review-zoom-snapshots.md"
SNAPSHOT_INTEGRITY = ROOT / "documentation/glyph-review/arabic-snapshot-integrity.md"
CROP_INTEGRITY = ROOT / "documentation/glyph-review/arabic-first-review-crop-integrity.md"
SESSION = ROOT / "documentation/glyph-review/arabic-hand-review-session.md"
BOARD = ROOT / "documentation/glyph-review/arabic-next-review-board.html"
CURRENT_WORKSHEET = ROOT / "documentation/glyph-review/arabic-current-review-worksheet.md"
ARABIC_PRINT_PROOF = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-hand-review-contact-sheet.html"


def read_text(path: Path) -> str:
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


def parse_snapshots(text: str) -> dict[str, list[tuple[str, str, str]]]:
    snapshots: dict[str, list[tuple[str, str, str]]] = {}
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 4:
            continue
        key = cells[0].strip("`")
        label = cells[1]
        source = cells[2].strip("`")
        png = cells[3].strip("`")
        snapshots.setdefault(key, []).append((label, source, png))
    return snapshots


def merge_zoom_snapshots(snapshots: dict[str, list[tuple[str, str, str]]], text: str) -> None:
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 4:
            continue
        key = cells[0].strip("`")
        label = f"{cells[1]} focused 2x crop"
        source = cells[2].strip("`")
        png = cells[3].strip("`")
        snapshots.setdefault(key, []).append((label, source, png))


def linked_lines(lines: list[str], output_path: Path, limit: int = 4) -> str:
    items: list[str] = []
    for line in lines[:limit]:
        text = line.strip().removeprefix("- ").strip()
        text = html.escape(text)

        def link_path(match: re.Match[str]) -> str:
            repo_path = match.group(1)
            link = relative_href(repo_path, output_path)
            if not link:
                return f"<code>{html.escape(repo_path)}</code>"
            return f"<a href='{link}'><code>{html.escape(repo_path)}</code></a>"

        text = re.sub(r"`([^`]+)`", link_path, text)
        items.append(f"<li>{text}</li>")
    if len(lines) > limit:
        items.append(f"<li class='muted'>{len(lines) - limit} more lines in the session sheet.</li>")
    return f"<ul>{''.join(items)}</ul>"


def report_bullet(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return html.escape(match.group(1)) if match else "unknown"


def integrity_summary(output_path: Path) -> str:
    snapshot_text = read_text(SNAPSHOT_INTEGRITY)
    crop_text = read_text(CROP_INTEGRITY)
    snapshot_link = relative_href(display_path(SNAPSHOT_INTEGRITY), output_path)
    crop_link = relative_href(display_path(CROP_INTEGRITY), output_path)
    rows = [
        (
            "Full queue snapshots",
            display_path(SNAPSHOT_INTEGRITY),
            snapshot_link,
            report_bullet(snapshot_text, "Snapshot evidence ready for hand review"),
            report_bullet(snapshot_text, "Readable PNG files"),
            report_bullet(snapshot_text, "Nonblank PNG files"),
        ),
        (
            "First glyph-row focused crops",
            display_path(CROP_INTEGRITY),
            crop_link,
            report_bullet(crop_text, "Evidence ready for hand review"),
            report_bullet(crop_text, "Readable crops"),
            report_bullet(crop_text, "Nonblank crops"),
        ),
    ]
    body = "\n".join(
        "<tr>"
        f"<th>{html.escape(label)}</th>"
        f"<td><a href='{link}'><code>{html.escape(path)}</code></a></td>"
        f"<td>{ready}</td>"
        f"<td>{readable}</td>"
        f"<td>{nonblank}</td>"
        "</tr>"
        if link
        else "<tr>"
        f"<th>{html.escape(label)}</th>"
        f"<td><code>{html.escape(path)}</code></td>"
        f"<td>{ready}</td>"
        f"<td>{readable}</td>"
        f"<td>{nonblank}</td>"
        "</tr>"
        for label, path, link, ready, readable, nonblank in rows
    )
    return (
        "<section class='integrity'>"
        "<h2>Evidence Integrity</h2>"
        "<p>These checks only verify that review images exist, load, and are not blank. "
        "They do not mark Arabic drawing rows as passed.</p>"
        "<table>"
        "<thead><tr><th>Evidence set</th><th>Report</th><th>Ready</th><th>Readable</th><th>Nonblank</th></tr></thead>"
        f"<tbody>{body}</tbody>"
        "</table>"
        "</section>"
    )


def snapshot_html(key: str, snapshots: dict[str, list[tuple[str, str, str]]], output_path: Path) -> str:
    found = snapshots.get(key, [])
    if not found:
        return "<p class='missing'>No snapshot for this row.</p>"
    figures: list[str] = []
    for label, source, png in found:
        png_link = relative_href(png, output_path)
        source_link = relative_href(source, output_path)
        image = (
            f"<a href='{png_link}'><img src='{png_link}' alt='{html.escape(key)} {html.escape(label)}'></a>"
            if png_link
            else "<div class='missing'>PNG missing</div>"
        )
        source_html = f"<a href='{source_link}'>source</a>" if source_link else "source missing"
        figures.append(
            "<figure>"
            f"{image}"
            f"<figcaption>{html.escape(label)} · {source_html}</figcaption>"
            "</figure>"
        )
    return "".join(figures)


def row_card(row, snapshots: dict[str, list[tuple[str, str, str]]], output_path: Path) -> str:
    pass_command = html.escape(command(row, "pass", "reviewed current proof"))
    fix_command = html.escape(command(row, "fix-needed", "specific glyph or proof issue"))
    defer_command = html.escape(command(row, "deferred", "needs Arabic native-reader review"))
    evidence = linked_lines(evidence_lines(row), output_path, limit=5)
    precheck = linked_lines(machine_precheck_lines(row), output_path, limit=4)
    return (
        f"<article class='card' id='{html.escape(row.key)}'>"
        "<div class='card-head'>"
        f"<h3><code>{html.escape(row.key)}</code></h3>"
        f"<span>{html.escape(row.status)}</span>"
        "</div>"
        f"<p class='cue'>{html.escape(row.cue)}</p>"
        f"<div class='shots'>{snapshot_html(row.key, snapshots, output_path)}</div>"
        "<details open><summary>Evidence</summary>"
        f"{evidence}"
        "</details>"
        "<details><summary>Machine precheck</summary>"
        f"{precheck}"
        "</details>"
        "<details><summary>Record outcome</summary>"
        f"<pre>{pass_command}\n{fix_command}\n{defer_command}</pre>"
        "</details>"
        "</article>"
    )


def html_report(output_path: Path) -> str:
    snapshots = parse_snapshots(read_text(SNAPSHOTS))
    merge_zoom_snapshots(snapshots, read_text(ZOOM_SNAPSHOTS))
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    rows = sorted(rows, key=row_priority)
    row_by_key = {row.key: row for row in rows}
    nav_items = "\n".join(
        f"<li><a href='#{html.escape(key)}'><code>{html.escape(key)}</code></a></li>"
        for row in rows
        for key in [row.key]
    )
    groups: list[str] = []
    for group_name, keys in SESSION_GROUPS:
        group_rows = [row_by_key[key] for key in keys if key in row_by_key]
        if not group_rows:
            continue
        cards = "\n".join(row_card(row, snapshots, output_path) for row in group_rows)
        groups.append(f"<section><h2>{html.escape(group_name)}</h2><div class='grid'>{cards}</div></section>")

    session_link = relative_href(display_path(SESSION), output_path)
    board_link = relative_href(display_path(BOARD), output_path)
    worksheet_link = relative_href(display_path(CURRENT_WORKSHEET), output_path)
    target_link = relative_href(display_path(EDIT_TARGETS), output_path)
    print_proof_link = relative_href(display_path(ARABIC_PRINT_PROOF), output_path)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virtua Grotesk Arabic Hand Review Contact Sheet</title>
<style>
:root {{
  --bg: #f6f4ef;
  --paper: #fffdfa;
  --ink: #191817;
  --muted: #66615a;
  --line: #d9d1c6;
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
  max-width: 1600px;
  margin: 0 auto;
  padding: 28px 22px 64px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 30px;
}}
h2 {{
  margin: 28px 0 12px;
  font-size: 20px;
}}
h3 {{
  margin: 0;
  font-size: 15px;
}}
p {{
  max-width: 920px;
  line-height: 1.45;
  color: var(--muted);
}}
a {{ color: var(--accent); }}
.links, .toc {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  padding: 0;
  margin: 14px 0;
  list-style: none;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 14px;
}}
.integrity {{
  margin: 18px 0;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--paper);
  border: 1px solid var(--line);
}}
th, td {{
  padding: 8px 10px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}}
th {{
  font-size: 13px;
}}
td {{
  color: var(--muted);
  font-size: 13px;
}}
.card {{
  break-inside: avoid;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
}}
.card-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}}
.card-head span {{
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 2px 8px;
  color: var(--muted);
  font-size: 12px;
}}
.cue {{
  margin: 8px 0 10px;
  font-size: 13px;
}}
.shots {{
  display: grid;
  gap: 8px;
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
figcaption {{
  padding: 6px 8px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}}
details {{
  margin-top: 8px;
}}
summary {{
  cursor: pointer;
  color: var(--accent);
  font-weight: 600;
  font-size: 13px;
}}
ul {{
  margin: 7px 0 0;
  padding-left: 20px;
}}
li {{
  margin-bottom: 4px;
  overflow-wrap: anywhere;
}}
pre {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f1ece4;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px;
  font-size: 11px;
}}
code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.92em;
}}
.muted, .missing {{
  color: var(--muted);
}}
@media print {{
  body {{ background: white; }}
  main {{ padding: 0; }}
  .card {{ border-color: #bbb; }}
  a {{ color: black; }}
}}
</style>
</head>
<body>
<main>
<h1>Arabic Hand Review Contact Sheet</h1>
<p>This generated contact sheet shows the remaining Arabic review snapshots in
the current queue. It accelerates hand review, but final status still requires
opening the linked proof/source evidence before recording pass, fix-needed, or
deferred.</p>
<ul class="links">
<li><a href="{worksheet_link}"><code>{display_path(CURRENT_WORKSHEET)}</code></a></li>
<li><a href="{session_link}"><code>{display_path(SESSION)}</code></a></li>
<li><a href="{board_link}"><code>{display_path(BOARD)}</code></a></li>
<li><a href="{print_proof_link}"><code>{display_path(ARABIC_PRINT_PROOF)}</code></a></li>
<li><a href="{target_link}"><code>{display_path(EDIT_TARGETS)}</code></a></li>
</ul>
{integrity_summary(output_path)}
<ul class="toc">
{nav_items}
</ul>
{''.join(groups)}
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
            print(f"missing contact-sheet link: {item}", file=sys.stderr)
        return 1
    print(display_path(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
