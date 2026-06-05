#!/usr/bin/env python3
"""Validate Arabic review PNG snapshot coverage and basic image integrity."""

from __future__ import annotations

import re
import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_REPORT = ROOT / "documentation/glyph-review/arabic-next-review-snapshots.md"
VISUAL_LOG = ROOT / "documentation/glyph-review/arabic-visual-review-log.md"
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-snapshot-integrity.md"


@dataclass(frozen=True)
class SnapshotRow:
    key: str
    label: str
    source: str
    png: str


@dataclass(frozen=True)
class PngStats:
    width: int
    height: int
    sample_pixels: int
    non_white_pixels: int
    unique_samples: int


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def pending_review_keys() -> set[str]:
    text = VISUAL_LOG.read_text(encoding="utf-8")
    keys: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        key = cells[0].strip("`")
        status = cells[6]
        if status in {"pending", "fix-needed"}:
            keys.add(key)
    return keys


def snapshot_rows() -> list[SnapshotRow]:
    text = SNAPSHOT_REPORT.read_text(encoding="utf-8")
    rows: list[SnapshotRow] = []
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        key = cells[0].strip("`")
        label = cells[1]
        source = cells[2].strip("`")
        png = cells[3].strip("`")
        if key == "---":
            continue
        rows.append(SnapshotRow(key, label, source, png))
    return rows


def paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    offset = 8
    chunks: list[tuple[bytes, bytes]] = []
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        chunks.append((chunk_type, chunk_data))
        offset += 12 + length
        if chunk_type == b"IEND":
            break
    return chunks


def png_stats(path: Path) -> PngStats:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG file")
    chunks = png_chunks(data)
    ihdr = next((chunk for chunk_type, chunk in chunks if chunk_type == b"IHDR"), None)
    if ihdr is None:
        raise ValueError("missing IHDR")
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
        ">IIBBBBB", ihdr
    )
    if bit_depth != 8 or compression != 0 or filter_method != 0 or interlace != 0:
        raise ValueError("unsupported PNG encoding")
    channels_by_color = {0: 1, 2: 3, 4: 2, 6: 4}
    channels = channels_by_color.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type {color_type}")
    idat = b"".join(chunk for chunk_type, chunk in chunks if chunk_type == b"IDAT")
    raw = zlib.decompress(idat)
    stride = width * channels
    previous = bytearray(stride)
    sample_step_x = max(1, width // 160)
    sample_step_y = max(1, height // 160)
    sample_pixels = 0
    non_white_pixels = 0
    unique_samples: set[tuple[int, ...]] = set()
    offset = 0
    for y in range(height):
        filter_type = raw[offset]
        offset += 1
        row = bytearray(raw[offset : offset + stride])
        offset += stride
        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            above = previous[x]
            upper_left = previous[x - channels] if x >= channels else 0
            if filter_type == 1:
                row[x] = (row[x] + left) & 0xFF
            elif filter_type == 2:
                row[x] = (row[x] + above) & 0xFF
            elif filter_type == 3:
                row[x] = (row[x] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                row[x] = (row[x] + paeth(left, above, upper_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")
        if y % sample_step_y == 0:
            for x in range(0, width, sample_step_x):
                start = x * channels
                sample = tuple(row[start : start + channels])
                unique_samples.add(sample)
                sample_pixels += 1
                rgb = sample[:3] if channels >= 3 else sample[:1] * 3
                if any(channel < 245 for channel in rgb):
                    non_white_pixels += 1
        previous = row
    return PngStats(width, height, sample_pixels, non_white_pixels, len(unique_samples))


def report() -> tuple[str, bool]:
    rows = snapshot_rows()
    pending = pending_review_keys()
    row_keys = {row.key for row in rows}
    missing_keys = sorted(pending - row_keys)
    extra_keys = sorted(row_keys - pending)
    errors: list[str] = []
    table = [
        "| Review key | Label | PNG | Dimensions | Non-white sample | Result |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    readable = 0
    nonblank = 0
    for row in rows:
        path = ROOT / row.png
        try:
            stats = png_stats(path)
        except Exception as exc:
            errors.append(f"{row.png}: {exc}")
            table.append(f"| `{row.key}` | {row.label} | `{row.png}` | n/a | 0 | fail |")
            continue
        readable += 1
        nonblank_result = stats.non_white_pixels > 0 and stats.unique_samples > 1
        if nonblank_result:
            nonblank += 1
        result = "ok" if nonblank_result else "blank-suspect"
        if not nonblank_result:
            errors.append(f"{row.png}: blank or single-color render suspected")
        ratio = f"{stats.non_white_pixels}/{stats.sample_pixels}"
        table.append(
            "| `{}` | {} | `{}` | {}x{} | {} | {} |".format(
                row.key,
                row.label,
                row.png,
                stats.width,
                stats.height,
                ratio,
                result,
            )
        )
    coverage_ok = not missing_keys and not errors
    lines = [
        "# Arabic Snapshot Integrity",
        "",
        "This generated report validates the PNG snapshot evidence used by the",
        "Arabic visual review queue. It does not judge Arabic drawing quality",
        "and does not mark any visual review row as passed.",
        "",
        f"- Visual review pending/fix-needed rows: {len(pending)}",
        f"- Snapshot rows in report: {len(rows)}",
        f"- Unique review keys with snapshots: {len(row_keys)}",
        f"- Readable PNG files: {readable}",
        f"- Nonblank PNG files: {nonblank}",
        f"- Pending/fix-needed rows without snapshot: {len(missing_keys)}",
        f"- Snapshot keys no longer pending/fix-needed: {len(extra_keys)}",
        f"- Integrity errors: {len(errors)}",
        f"- Snapshot evidence ready for hand review: {'yes' if coverage_ok else 'no'}",
        "",
        "## Snapshot Rows",
        "",
        *table,
    ]
    if missing_keys:
        lines.extend(["", "## Missing Review Keys", ""])
        lines.extend(f"- `{key}`" for key in missing_keys)
    if extra_keys:
        lines.extend(["", "## Extra Snapshot Keys", ""])
        lines.extend(f"- `{key}`" for key in extra_keys)
    if errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
    lines.extend(
        [
            "",
            "## Review Use",
            "",
            "If this report is clean, use `documentation/glyph-review/arabic-next-review-board.html`",
            "for navigation and open the linked proof/source HTML before recording",
            "any row status in `documentation/glyph-review/arabic-visual-review-log.md`.",
            "",
        ]
    )
    return "\n".join(lines), coverage_ok


def main(argv: list[str]) -> int:
    output_path = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    text, ok = report()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"Wrote {display_path(output_path)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
