#!/usr/bin/env python3
"""Apply reviewed donor glyph candidates back into production UFO sources.

This is the guarded counterpart to build_donor_glyph_candidates.py. It copies
only selected existing .glif files from a scratch candidate source into matching
glyph filenames in the target source. It does not save/rewrite whole UFOs.
"""

from __future__ import annotations

import argparse
import json
import plistlib
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "sources/VirtuaGrotesk.designspace"
DEFAULT_REPORT = ROOT / "build/arabic-donor-candidates/red-marked-arabic/glyph-candidate-report.json"
MARK_COLORS = {
    "red": (1.0, 0.3, 0.3, 1.0),
    "orange": (1.0, 0.6, 0.2, 1.0),
    "yellow": (1.0, 0.9, 0.2, 1.0),
    "green": (0.3, 0.7, 0.3, 1.0),
    "blue": (0.1, 0.3, 0.8, 1.0),
    "purple": (0.6, 0.3, 0.9, 1.0),
    "pink": (0.9, 0.3, 0.7, 1.0),
}


@dataclass(frozen=True)
class Source:
    path: Path
    style: str
    weight: float


def read_sources(path: Path) -> list[Source]:
    if path.suffix.lower() == ".ufo":
        return [Source(path=path.resolve(), style=path.stem, weight=0)]
    tree = ET.parse(path)
    sources: list[Source] = []
    for source in tree.findall(".//source"):
        if source.get("layer"):
            continue
        filename = source.get("filename")
        if not filename:
            continue
        weight = 0.0
        dim = source.find("./location/dimension[@name='Weight']")
        if dim is not None and dim.get("xvalue"):
            weight = float(dim.get("xvalue", "0"))
        sources.append(
            Source(
                path=(path.parent / filename).resolve(),
                style=source.get("stylename") or Path(filename).stem,
                weight=weight,
            )
        )
    if not sources:
        raise ValueError(f"No UFO sources found in {path}")
    return sources


def master_pair(path: Path) -> tuple[Source, Source]:
    sources = sorted(read_sources(path), key=lambda item: item.weight)
    if len(sources) == 1:
        return sources[0], sources[0]
    return sources[0], sources[-1]


def contents_map(ufo_path: Path) -> dict[str, str]:
    with (ufo_path / "glyphs" / "contents.plist").open("rb") as handle:
        return plistlib.load(handle)


def glyph_file(ufo_path: Path, glyph_name: str) -> Path | None:
    file_name = contents_map(ufo_path).get(glyph_name)
    if not file_name:
        return None
    return ufo_path / "glyphs" / file_name


def read_report(report_path: Path) -> dict:
    if not report_path.exists():
        raise FileNotFoundError(f"Candidate report not found: {report_path}")
    return json.loads(report_path.read_text(encoding="utf-8"))


def candidate_source_from_report(report: dict, report_path: Path) -> Path:
    output = Path(report.get("output") or report_path.parent).expanduser()
    if not output.is_absolute():
        output = (report_path.parent / output).resolve()
    target_name = Path(report.get("target", DEFAULT_TARGET)).name
    candidate = output / target_name
    if candidate.exists():
        return candidate.resolve()
    designspaces = sorted(output.glob("*.designspace"))
    if designspaces:
        return designspaces[0].resolve()
    ufos = sorted(output.glob("*.ufo"))
    if ufos:
        return ufos[0].resolve()
    raise FileNotFoundError(f"Could not resolve candidate source from {report_path}")


def report_candidate_glyphs(report: dict) -> list[str]:
    return sorted(
        {
            str(result.get("glyph", "")).strip()
            for result in report.get("results", [])
            if result.get("status") == "candidate" and str(result.get("glyph", "")).strip()
        }
    )


def parse_glyphs(raw: str, target: Path, report: dict | None) -> list[str]:
    raw = (raw or "report").strip()
    if raw in {"report", "candidate-report", "report-candidates"}:
        if report is None:
            raise ValueError("--glyphs report requires --report")
        return report_candidate_glyphs(report)
    if raw.startswith(("mark:", "marked:")):
        color_name = raw.split(":", 1)[1].strip().lower()
        glyphs = marked_glyphs(target, color_name)
        if report:
            glyphs = sorted(set(glyphs) & set(report_candidate_glyphs(report)))
        return glyphs
    path = Path(raw).expanduser()
    if path.exists():
        glyphs = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                glyphs.append(line)
        return glyphs
    return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


def marked_glyphs(target: Path, color_name: str) -> list[str]:
    expected = MARK_COLORS.get(color_name)
    if expected is None:
        known = ", ".join(sorted(MARK_COLORS))
        raise ValueError(f"Unknown mark color {color_name!r}; expected one of: {known}")
    glyphs: set[str] = set()
    for source in read_sources(target):
        for path in (source.path / "glyphs").glob("*.glif"):
            name = ET.parse(path).getroot().get("name")
            if not name:
                continue
            raw = mark_color(path.read_bytes())
            if raw and rgba_matches(raw, expected):
                glyphs.add(name)
    return sorted(glyphs)


def rgba_matches(raw: str, expected: tuple[float, float, float, float], tolerance: float = 0.08) -> bool:
    try:
        values = tuple(float(part.strip()) for part in str(raw).split(","))
    except ValueError:
        return False
    return len(values) == 4 and all(abs(value - target) <= tolerance for value, target in zip(values, expected))


def arabic_glyph_filter(glyphs: list[str]) -> list[str]:
    return [
        glyph
        for glyph in glyphs
        if "-ar" in glyph or glyph.endswith("Farsi") or "Farsi-ar" in glyph or glyph == "dottedCircle"
    ]


def mark_color(data: bytes) -> str | None:
    root = ET.fromstring(data)
    dictionary = root.find("lib/dict")
    if dictionary is None:
        return None
    children = list(dictionary)
    for index, child in enumerate(children):
        if child.tag == "key" and child.text == "public.markColor" and index + 1 < len(children):
            return children[index + 1].text
    return None


def set_mark_color(data: bytes, color: str | None) -> bytes:
    root = ET.fromstring(data)
    lib = root.find("lib")
    if lib is None and color is None:
        return data
    if lib is None:
        lib = ET.SubElement(root, "lib")
    dictionary = lib.find("dict")
    if dictionary is None:
        dictionary = ET.SubElement(lib, "dict")
    children = list(dictionary)
    for index, child in enumerate(children):
        if child.tag == "key" and child.text == "public.markColor":
            if color is None:
                dictionary.remove(child)
                if index + 1 < len(children):
                    dictionary.remove(children[index + 1])
            elif index + 1 < len(children):
                children[index + 1].text = color
            return ET.tostring(root, encoding="utf-8", xml_declaration=True)
    if color is not None:
        key = ET.SubElement(dictionary, "key")
        key.text = "public.markColor"
        value = ET.SubElement(dictionary, "string")
        value.text = color
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def apply_glyph(
    candidate_ufo: Path,
    target_ufo: Path,
    glyph_name: str,
    *,
    preserve_mark_color: bool,
    write: bool,
) -> str:
    candidate_file = glyph_file(candidate_ufo, glyph_name)
    target_file = glyph_file(target_ufo, glyph_name)
    if candidate_file is None or not candidate_file.exists():
        return "missing-candidate"
    if target_file is None or not target_file.exists():
        return "missing-target"
    if not write:
        return "would-apply"
    candidate_data = candidate_file.read_bytes()
    if preserve_mark_color:
        candidate_data = set_mark_color(candidate_data, mark_color(target_file.read_bytes()))
    target_file.write_bytes(candidate_data)
    return "applied"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--candidate", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--glyphs", default="report")
    parser.add_argument("--arabic-only", action="store_true")
    parser.add_argument("--clear-mark-color", action="store_true")
    parser.add_argument("--write", action="store_true", help="write candidate glyphs into the target")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    report = read_report(args.report.expanduser().resolve()) if args.report else None
    candidate = args.candidate.expanduser().resolve() if args.candidate else candidate_source_from_report(report, args.report)
    glyphs = parse_glyphs(args.glyphs, target, report)
    if args.arabic_only:
        glyphs = arabic_glyph_filter(glyphs)
    if not glyphs:
        raise ValueError("No glyphs selected for apply")

    candidate_regular, candidate_bold = master_pair(candidate)
    target_regular, target_bold = master_pair(target)
    results = []
    for candidate_master, target_master in ((candidate_regular, target_regular), (candidate_bold, target_bold)):
        for glyph_name in glyphs:
            status = apply_glyph(
                candidate_master.path,
                target_master.path,
                glyph_name,
                preserve_mark_color=not args.clear_mark_color,
                write=args.write,
            )
            results.append((target_master.style, glyph_name, status))

    status_counts: dict[str, int] = {}
    for _, _, status in results:
        status_counts[status] = status_counts.get(status, 0) + 1
    mode = "write" if args.write else "dry-run"
    print(f"mode: {mode}")
    print(f"target: {target}")
    print(f"candidate: {candidate}")
    print(f"glyphs: {len(glyphs)}")
    print(f"status_counts: {status_counts}")
    for style, glyph_name, status in results:
        if status not in {"would-apply", "applied"}:
            print(f"{status}: {style} {glyph_name}")
    if any(status not in {"would-apply", "applied"} for _, _, status in results):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
