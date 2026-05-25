#!/usr/bin/env python3
"""Render PNG snapshots for the next Arabic visual review packet."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from urllib.parse import quote
from dataclasses import dataclass
from pathlib import Path

from report_arabic_visual_review_runbook import row_priority, visual_rows


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "documentation/arabic-next-review-packet.md"
OUTPUT_DIR = ROOT / "documentation/arabic-review-snapshots"
OUTPUT_REPORT = ROOT / "documentation/arabic-next-review-snapshots.md"
DEFAULT_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
)


@dataclass(frozen=True)
class Snapshot:
    key: str
    label: str
    source: Path
    output: Path
    fragment: str | None = None


def chrome_path() -> str | None:
    configured = os.environ.get("CHROME")
    candidates = (configured,) if configured else DEFAULT_CHROME_CANDIDATES
    for candidate in candidates:
        if not candidate:
            continue
        path = shutil.which(candidate) if "/" not in candidate else candidate
        if path and Path(path).exists():
            return path
    return None


def next_keys(limit: int) -> list[str]:
    text = PACKET.read_text(encoding="utf-8")
    keys: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\| \d+ \| `([^`]+)` \|", line)
        if match:
            keys.append(match.group(1))
        if len(keys) >= limit:
            break
    return keys


def pending_keys(limit: int) -> list[str]:
    rows = [row for row in visual_rows() if row.status in {"pending", "fix-needed"}]
    return [row.key for row in sorted(rows, key=row_priority)[:limit]]


def html_sources_for_key(key: str) -> list[tuple[str, Path]]:
    proof_match = re.match(r"^proof-(regular|medium|semibold|bold)-(.+)$", key)
    if proof_match:
        instance, proof_type = proof_match.groups()
        instance_name = {
            "regular": "Regular",
            "medium": "Medium",
            "semibold": "SemiBold",
            "bold": "Bold",
        }[instance]
        path = ROOT / f"documentation/gftools-qa/Proof/{instance_name}-diffbrowsers_{proof_type}.html"
        return [(f"{instance_name} {proof_type}", path)]
    if key == "class-letter-structures":
        return [
            ("Arabic structure sweep", ROOT / "documentation/arabic-structure-sweep.html"),
            ("Arabic visual risk proof", ROOT / "documentation/arabic-visual-risk-proof.html"),
        ]
    if key == "class-mark-combinations":
        return [("Arabic mark proof", ROOT / "documentation/arabic-mark-review-proof.html")]
    if key.startswith("mark-"):
        return [("Arabic mark proof", ROOT / "documentation/arabic-mark-review-proof.html")]
    if key.startswith("smoke-"):
        return [("Arabic manual dashboard", ROOT / "documentation/arabic-manual-review-dashboard.html")]
    if key in {
        "class-dot-stack-helpers",
        "class-arabic-farsi-numerals",
        "class-arabic-punctuation",
    }:
        return [("Arabic manual dashboard", ROOT / "documentation/arabic-manual-review-dashboard.html")]
    return []


def html_fragment_for_key(key: str) -> str | None:
    if key.startswith("mark-") or key == "class-mark-combinations":
        return key
    if key.startswith("smoke-") or key in {
        "class-dot-stack-helpers",
        "class-arabic-farsi-numerals",
        "class-arabic-punctuation",
    }:
        return key
    return None


def snapshots(keys: list[str], output_dir: Path) -> tuple[list[Snapshot], list[str]]:
    rows: list[Snapshot] = []
    skipped: list[str] = []
    for key in keys:
        sources = html_sources_for_key(key)
        if not sources:
            skipped.append(key)
            continue
        for index, (label, source) in enumerate(sources, start=1):
            suffix = "" if index == 1 else f"-{index}"
            rows.append(
                Snapshot(
                    key=key,
                    label=label,
                    source=source,
                    output=output_dir / f"{key}{suffix}.png",
                    fragment=html_fragment_for_key(key),
                )
            )
    return rows, skipped


def render_snapshot(chrome: str, snapshot: Snapshot, width: int, height: int, timeout: int) -> None:
    if not snapshot.source.exists():
        raise FileNotFoundError(snapshot.source)
    snapshot.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="virtua-arabic-chrome-", dir="/private/tmp") as user_data_dir:
        tmp_output = Path(user_data_dir) / snapshot.output.name
        source_uri = snapshot.source.resolve().as_uri()
        if snapshot.fragment:
            source_uri = f"{source_uri}#{quote(snapshot.fragment, safe='')}"
        command = [
            chrome,
            "--headless=new",
            "--allow-file-access-from-files",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-features=MediaRouter,OptimizationHints",
            "--hide-scrollbars",
            "--no-sandbox",
            "--no-first-run",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=5000",
            f"--user-data-dir={user_data_dir}",
            f"--window-size={width},{height}",
            f"--screenshot={tmp_output}",
            source_uri,
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
            if tmp_output.exists() and tmp_output.stat().st_size > 0:
                shutil.move(str(tmp_output), snapshot.output)
                return
            raise RuntimeError(f"Chrome timed out before writing {snapshot.output}") from exc
        if tmp_output.exists() and tmp_output.stat().st_size > 0:
            shutil.move(str(tmp_output), snapshot.output)
            return
        if process.returncode != 0:
            raise RuntimeError(
                f"Chrome failed for {snapshot.source} with exit code {process.returncode}: "
                f"{stderr.strip() or stdout.strip()}"
            )
    raise RuntimeError(f"Chrome did not write {snapshot.output}")


def render_snapshots(
    chrome: str,
    rows: list[Snapshot],
    width: int,
    height: int,
    timeout: int,
) -> tuple[list[Snapshot], list[str]]:
    rendered: list[Snapshot] = []
    errors: list[str] = []
    rendered_sources: dict[tuple[Path, str | None], Path] = {}
    for index, row in enumerate(rows, start=1):
        source_key = (row.source, row.fragment)
        cached = rendered_sources.get(source_key)
        if cached and cached.exists():
            print(
                f"[{index}/{len(rows)}] copy {display_path(cached)} -> {display_path(row.output)}",
                flush=True,
            )
            row.output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(cached, row.output)
            rendered.append(row)
            continue
        print(
            f"[{index}/{len(rows)}] render {display_path(row.source)} -> {display_path(row.output)}",
            flush=True,
        )
        try:
            render_snapshot(chrome, row, width, height, timeout)
        except Exception as exc:
            errors.append(f"{display_path(row.source)}: {exc}")
        else:
            rendered_sources[source_key] = row.output
            rendered.append(row)
    return rendered, errors


def reuse_existing_snapshots(rows: list[Snapshot]) -> tuple[list[Snapshot], list[str]]:
    rendered: list[Snapshot] = []
    errors: list[str] = []
    for row in rows:
        if row.output.exists() and row.output.stat().st_size > 0:
            rendered.append(row)
        else:
            errors.append(f"{display_path(row.output)}: existing PNG not found or empty")
    return rendered, errors


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def image_alt(row: Snapshot) -> str:
    return f"{row.key} {row.label}".replace("|", " ")


def report(
    keys: list[str],
    snapshot_rows: list[Snapshot],
    rendered: list[Snapshot],
    skipped: list[str],
    errors: list[str],
    chrome: str | None,
    all_pending: bool,
    list_only: bool,
    reuse_existing: bool,
    timeout: int,
) -> str:
    lines = [
        "# Arabic Next Review Snapshots",
        "",
        "This generated report lists local PNG snapshots for the current Arabic",
        "next-review packet. The images are review aids only; they do not replace",
        "human inspection of the proof HTML or source glyphs.",
        "",
        f"- Source packet: `{display_path(PACKET)}`",
        f"- Key source: {'all pending/fix-needed rows' if all_pending else 'current next-review packet'}",
        f"- List only: {'yes' if list_only else 'no'}",
        f"- Reuse existing PNGs: {'yes' if reuse_existing else 'no'}",
        f"- Chrome executable: `{chrome or 'not found'}`",
        f"- Chrome render timeout: {timeout}s",
        f"- Requested review rows: {len(keys)}",
        f"- Requested snapshots: {len(snapshot_rows)}",
        f"- Rendered snapshots: {len(rendered)}",
        f"- Rows without snapshot source: {len(skipped)}",
        f"- Errors: {len(errors)}",
        "",
        "## Snapshots",
        "",
        "| Review key | Label | Source HTML | PNG |",
        "| --- | --- | --- | --- |",
    ]
    table_rows = rendered if rendered else (snapshot_rows if list_only else [])
    for row in table_rows:
        lines.append(
            f"| `{row.key}` | {row.label} | `{display_path(row.source)}` | `{display_path(row.output)}` |"
        )
    if not table_rows:
        lines.append("| none | none | none | none |")
    if table_rows and not list_only:
        lines.extend(["", "## Contact Sheet", ""])
        lines.append(
            "These thumbnails are for quick navigation only. Open the linked proof "
            "HTML/source evidence before recording a final review status."
        )
        lines.append("")
        for row in table_rows:
            png = display_path(row.output)
            source = display_path(row.source)
            lines.extend(
                [
                    f"<details><summary><code>{row.key}</code> - {row.label}</summary>",
                    "",
                    f"<p><a href=\"{source}\">Source HTML</a></p>",
                    f"<p><a href=\"{png}\"><img src=\"{png}\" alt=\"{image_alt(row)}\" style=\"max-width: 420px;\"></a></p>",
                    "",
                    "</details>",
                    "",
                ]
            )
    if skipped:
        lines.extend(["", "## Rows Without Snapshot Source", ""])
        lines.extend(f"- `{key}`" for key in skipped)
    if errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
    lines.extend(
        [
            "",
            "## Review Use",
            "",
            "1. Open the PNG for a quick first pass.",
            "2. Open the matching source HTML for detailed zoom and browser text behavior.",
            "3. Record the row outcome with `make arabic-visual-review-update`.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=5, help="number of next packet rows to snapshot")
    parser.add_argument("--all-pending", action="store_true", help="snapshot all pending/fix-needed rows up to --limit")
    parser.add_argument("--list-only", action="store_true", help="write coverage report without launching Chrome")
    parser.add_argument("--reuse-existing", action="store_true", help="write report from existing PNGs without launching Chrome")
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1800)
    parser.add_argument("--timeout", type=int, default=20, help="seconds to allow each unique Chrome render")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--report", type=Path, default=OUTPUT_REPORT)
    args = parser.parse_args(argv[1:])

    chrome = chrome_path()
    keys = pending_keys(args.limit) if args.all_pending else next_keys(args.limit)
    rows, skipped = snapshots(keys, args.output_dir)
    rendered: list[Snapshot] = []
    errors: list[str] = []
    if args.list_only:
        pass
    elif args.reuse_existing:
        rendered, errors = reuse_existing_snapshots(rows)
    elif chrome is None:
        errors.append("Chrome/Chromium executable not found. Set CHROME=/path/to/chrome and rerun.")
    else:
        rendered, errors = render_snapshots(chrome, rows, args.width, args.height, args.timeout)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        report(
            keys,
            rows,
            rendered,
            skipped,
            errors,
            chrome,
            args.all_pending,
            args.list_only,
            args.reuse_existing,
            args.timeout,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {display_path(args.report)}")
    if errors:
        for error in errors:
            print(f"ERR {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
