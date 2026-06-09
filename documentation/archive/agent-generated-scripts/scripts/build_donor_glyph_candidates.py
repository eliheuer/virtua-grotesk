#!/usr/bin/env python3
"""Build scratch Arabic glyph candidates from an OFL donor source.

This is intentionally a source-to-source prototype: it never writes into the
production UFOs. The output is a copied target designspace/UFO with selected
glyphs replaced by transformed donor outlines, plus lightweight proof files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
import json
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import ufoLib2


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "sources/VirtuaGrotesk.designspace"
DEFAULT_DONOR = (
    Path(os.environ["DONOR_DESIGNSPACE"])
    if os.environ.get("DONOR_DESIGNSPACE")
    else None
)
DEFAULT_OUTPUT = ROOT / "build/arabic-donor-candidates/donor-to-virtua"
PENDING_SOURCE_CHECKPOINT = ROOT / "documentation/glyph-review/arabic-pending-source-checkpoint.md"

SAMPLE_GLYPHS = [
    "beh-ar",
    "seen-ar",
    "sad-ar",
    "tah-ar",
    "meem-ar",
    "heh-ar",
    "peh-ar",
    "keheh-ar",
    "gaf-ar",
    "farsiYeh-ar",
]

DONOR_NAME_OVERRIDES = {
    "farsiYeh-ar": "yeh-farsi",
    "farsiYeh-ar.fina": "yeh-farsi.fina",
    "farsiYeh-ar.init": "yeh-farsi.init",
    "farsiYeh-ar.medi": "yeh-farsi.medi",
    "zeroFarsi-ar": "zero-persian",
    "oneFarsi-ar": "one-persian",
    "twoFarsi-ar": "two-persian",
    "threeFarsi-ar": "three-persian",
    "fourFarsi-ar": "four-persian",
    "fiveFarsi-ar": "five-persian",
    "sixFarsi-ar": "six-persian",
    "sevenFarsi-ar": "seven-persian",
    "eightFarsi-ar": "eight-persian",
    "nineFarsi-ar": "nine-persian",
    "threedotsdowncenter-ar": "threedotsdownbelow-ar",
}

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
    name: str
    style: str
    weight: float


@dataclass
class GlyphResult:
    glyph: str
    donor_glyph: str
    master: str
    status: str
    x_scale: float = 0.0
    y_scale: float = 0.0
    target_width: int = 0
    donor_width: int = 0
    missing_components: tuple[str, ...] = ()


def read_sources(path: Path) -> list[Source]:
    if path.suffix.lower() == ".ufo":
        return [Source(path=path.resolve(), name=path.stem, style=path.stem, weight=0)]
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
                name=source.get("name") or Path(filename).stem,
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


def copy_target_source(target: Path, output: Path, force: bool) -> Path:
    if output.exists():
        if not force:
            raise FileExistsError(f"{output} exists; pass --force to replace it")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    if target.suffix.lower() == ".ufo":
        shutil.copytree(target, output / target.name)
        return output / target.name

    shutil.copy2(target, output / target.name)
    for source in read_sources(target):
        rel = source.path.relative_to(target.parent.resolve())
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source.path, dest)
    return output / target.name


def font_metric(font: ufoLib2.Font, name: str, fallback: float) -> float:
    return float(getattr(font.info, name, None) or fallback)


def round_even(value: float) -> int:
    return int(round(value / 2.0) * 2)


def glyph_bounds(font: ufoLib2.Font, glyph_name: str) -> tuple[float, float, float, float] | None:
    if glyph_name not in font:
        return None
    pen = BoundsPen(font)
    try:
        font[glyph_name].draw(pen)
    except Exception:
        return None
    return pen.bounds


def copy_transformed_glyph(
    target_font: ufoLib2.Font,
    donor_font: ufoLib2.Font,
    glyph_name: str,
    donor_name: str,
    x_scale_mode: str,
) -> GlyphResult:
    donor_name = resolve_donor_name(donor_font, glyph_name, donor_name)
    if donor_name not in donor_font:
        return GlyphResult(glyph_name, donor_name, target_font.info.styleName or "target", "missing-donor")

    donor_glyph = donor_font[donor_name]
    target_exists = glyph_name in target_font
    if not target_exists:
        target_font.newGlyph(glyph_name)
    target_glyph = target_font[glyph_name]
    previous_width = int(target_glyph.width or 0)
    previous_unicodes = list(target_glyph.unicodes or [])
    donor_width = int(donor_glyph.width or 0)

    target_upm = font_metric(target_font, "unitsPerEm", 1000)
    donor_upm = font_metric(donor_font, "unitsPerEm", 1000)
    target_x_height = font_metric(target_font, "xHeight", target_upm * 0.5)
    donor_x_height = font_metric(donor_font, "xHeight", donor_upm * 0.5)
    y_scale = target_x_height / donor_x_height if donor_x_height else target_upm / donor_upm

    if x_scale_mode == "same-as-y":
        x_scale = y_scale
    elif x_scale_mode == "target-advance" and previous_width and donor_width:
        x_scale = previous_width / donor_width
    else:
        x_scale = target_upm / donor_upm

    target_glyph.clear()
    recording_pen = DecomposingRecordingPen(donor_font)
    donor_glyph.draw(recording_pen)
    recording_pen.replay(TransformPen(target_glyph.getPen(), (x_scale, 0, 0, y_scale, 0, 0)))
    round_glyph_coordinates(target_glyph)
    for anchor in donor_glyph.anchors:
        target_glyph.appendAnchor(
            {
                "name": anchor.name,
                "x": round_even(anchor.x * x_scale),
                "y": round_even(anchor.y * y_scale),
                "color": anchor.color,
            }
        )
    target_glyph.width = previous_width or round_even(donor_width * x_scale)
    target_glyph.unicodes = previous_unicodes or list(donor_glyph.unicodes or [])
    target_glyph.lib["com.virtuaGrotesk.donorCandidate"] = {
        "donorGlyph": donor_name,
        "xScale": round(x_scale, 5),
        "yScale": round(y_scale, 5),
    }

    missing_components = tuple(
        sorted({component.baseGlyph for component in target_glyph.components if component.baseGlyph not in target_font})
    )
    return GlyphResult(
        glyph=glyph_name,
        donor_glyph=donor_name,
        master=target_font.info.styleName or "target",
        status="candidate",
        x_scale=x_scale,
        y_scale=y_scale,
        target_width=int(target_glyph.width or 0),
        donor_width=donor_width,
        missing_components=missing_components,
    )


def resolve_donor_name(donor_font: ufoLib2.Font, glyph_name: str, donor_name: str) -> str:
    if donor_name in donor_font:
        return donor_name
    if glyph_name in donor_font:
        return glyph_name
    if glyph_name.endswith("Farsi-ar"):
        candidate = glyph_name.removesuffix("Farsi-ar").lower() + "-persian"
        if candidate in donor_font:
            return candidate
    if glyph_name.endswith("Farsi-ar.fina"):
        candidate = glyph_name.removesuffix("Farsi-ar.fina").lower() + "-persian.fina"
        if candidate in donor_font:
            return candidate
    return donor_name


def round_glyph_coordinates(glyph: ufoLib2.objects.Glyph) -> None:
    for contour in glyph.contours:
        for point in contour.points:
            point.x = round_even(point.x)
            point.y = round_even(point.y)
    for component in glyph.components:
        xx, xy, yx, yy, dx, dy = tuple(component.transformation)
        component.transformation = Transform(xx, xy, yx, yy, round_even(dx), round_even(dy))


def glyph_path(font: ufoLib2.Font, glyph_name: str) -> str:
    if glyph_name not in font:
        return ""
    pen = DecomposingRecordingPen(font)
    try:
        font[glyph_name].draw(pen)
    except Exception:
        return ""
    svg_pen = SVGPathPen(font)
    pen.replay(svg_pen)
    return svg_pen.getCommands()


def svg_panel(font: ufoLib2.Font, glyph_name: str, color: str, title: str) -> str:
    bounds = glyph_bounds(font, glyph_name)
    width = int(font[glyph_name].width or 600) if glyph_name in font else 600
    if bounds:
        x_min, y_min, x_max, y_max = bounds
        x_min = min(x_min, 0)
        x_max = max(x_max, width)
    else:
        x_min, y_min, x_max, y_max = 0, -200, width, 800
    pad = 80
    view_x = x_min - pad
    view_y = -(y_max + pad)
    view_w = max(200, (x_max - x_min) + pad * 2)
    view_h = max(200, (y_max - y_min) + pad * 2)
    path = glyph_path(font, glyph_name)
    label = html.escape(title)
    if not path:
        body = "<text x='20' y='-20' fill='#c44' transform='scale(1,-1)'>missing</text>"
    else:
        body = f"<path d='{html.escape(path)}' fill='{color}' fill-opacity='0.74'/>"
    return (
        f"<figure><figcaption>{label}</figcaption>"
        f"<svg viewBox='{view_x} {view_y} {view_w} {view_h}'>{body}</svg></figure>"
    )


def write_proof(
    output: Path,
    glyphs: list[str],
    target_font: ufoLib2.Font,
    donor_font: ufoLib2.Font,
    candidate_font: ufoLib2.Font,
) -> Path:
    proof_dir = output / "proofs"
    proof_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for glyph in glyphs:
        donor_name = DONOR_NAME_OVERRIDES.get(glyph, glyph)
        rows.append(
            "<section class='glyph-row'>"
            f"<h2>{html.escape(glyph)} <small>donor: {html.escape(donor_name)}</small></h2>"
            "<div class='panels'>"
            + svg_panel(target_font, glyph, "#9aa0a6", "target placeholder")
            + svg_panel(donor_font, donor_name, "#4d8bf5", "raw donor")
            + svg_panel(candidate_font, glyph, "#2fbf71", "transformed candidate")
            + "</div></section>"
        )
    html_text = """<!doctype html>
<meta charset="utf-8">
<title>Arabic Donor Candidate Proof</title>
<style>
body { font: 14px system-ui, sans-serif; margin: 24px; background: #111; color: #ddd; }
h1, h2 { font-weight: 600; }
small { color: #999; }
.glyph-row { border-top: 1px solid #333; padding: 18px 0; }
.panels { display: grid; grid-template-columns: repeat(3, minmax(180px, 1fr)); gap: 14px; }
figure { margin: 0; background: #1d1d1d; border: 1px solid #333; padding: 10px; }
figcaption { color: #aaa; margin-bottom: 8px; }
svg { width: 100%; height: 220px; background: #080808; overflow: visible; }
</style>
<h1>Arabic Donor Candidate Proof</h1>
""" + "\n".join(rows)
    proof_path = proof_dir / "arabic-donor-candidate-proof.html"
    proof_path.write_text(html_text, encoding="utf-8")
    return proof_path


def write_reports(output: Path, results: list[GlyphResult], proof_path: Path, args: argparse.Namespace) -> None:
    data = {
        "target": str(args.target),
        "donor": str(args.donor),
        "output": str(output),
        "x_scale_mode": args.x_scale_mode,
        "excluded_glyphs": sorted(parse_glyphs(args.exclude_glyphs, Path(args.target))) if args.exclude_glyphs else [],
        "proof": str(proof_path),
        "results": [result.__dict__ for result in results],
    }
    (output / "glyph-candidate-report.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Arabic Donor Glyph Candidate Report",
        "",
        f"- Target: `{args.target}`",
        f"- Donor: `{args.donor}`",
        f"- Output: `{output}`",
        f"- Proof: `{proof_path}`",
        f"- X scale mode: `{args.x_scale_mode}`",
        "",
        "## Recommendation",
        "",
        "Use deterministic donor normalization first. Add local vision ranking after",
        "the proof output is useful. Do not train a LoRA until this source-to-source",
        "prototype produces candidates worth comparing.",
        "",
        "## Results",
        "",
        "| Glyph | Donor glyph | Master | Status | x scale | y scale | Width | Missing components |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        missing = ", ".join(result.missing_components) if result.missing_components else "-"
        lines.append(
            f"| `{result.glyph}` | `{result.donor_glyph}` | {result.master} | {result.status} | "
            f"{result.x_scale:.3f} | {result.y_scale:.3f} | {result.target_width} | {missing} |"
        )
    (output / "glyph-candidate-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_glyphs(raw: str, target: Path = DEFAULT_TARGET) -> list[str]:
    if raw == "sample":
        return SAMPLE_GLYPHS
    if raw in {"pending-review", "pending-source"}:
        return pending_source_glyphs()
    if raw.startswith(("mark:", "marked:")):
        color_name = raw.split(":", 1)[1].strip().lower()
        return marked_glyphs(target, color_name)
    path = Path(raw).expanduser()
    if path.exists():
        glyphs = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                glyphs.append(line)
        return glyphs
    return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


def arabic_glyph_filter(glyphs: list[str]) -> list[str]:
    return [
        glyph
        for glyph in glyphs
        if "-ar" in glyph
        or glyph.endswith("Farsi")
        or "Farsi-ar" in glyph
        or glyph in {"dottedCircle"}
    ]


def marked_glyphs(target: Path, color_name: str) -> list[str]:
    expected = MARK_COLORS.get(color_name)
    if expected is None:
        known = ", ".join(sorted(MARK_COLORS))
        raise ValueError(f"Unknown mark color {color_name!r}; expected one of: {known}")
    glyphs: set[str] = set()
    for source in read_sources(target):
        font = ufoLib2.Font.open(source.path)
        for glyph in font:
            raw = glyph.lib.get("public.markColor")
            if raw and rgba_matches(raw, expected):
                glyphs.add(glyph.name)
    return sorted(glyphs)


def rgba_matches(raw: str, expected: tuple[float, float, float, float], tolerance: float = 0.08) -> bool:
    try:
        values = tuple(float(part.strip()) for part in str(raw).split(","))
    except ValueError:
        return False
    if len(values) != 4:
        return False
    return all(abs(value - target) <= tolerance for value, target in zip(values, expected, strict=True))


def pending_source_glyphs() -> list[str]:
    if not PENDING_SOURCE_CHECKPOINT.exists():
        raise FileNotFoundError(f"{PENDING_SOURCE_CHECKPOINT} not found")
    glyphs: list[str] = []
    in_table = False
    for line in PENDING_SOURCE_CHECKPOINT.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Glyph |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("| `"):
            if glyphs:
                break
            continue
        glyph = line.split("|", 2)[1].strip().strip("`")
        if glyph:
            glyphs.append(glyph)
    return glyphs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--donor", type=Path, default=DEFAULT_DONOR)
    parser.add_argument("--glyphs", default="sample")
    parser.add_argument(
        "--exclude-glyphs",
        default="",
        help="comma-separated glyphs or a text file to preserve from the target source",
    )
    parser.add_argument(
        "--arabic-only",
        action="store_true",
        help="filter the selected glyph list to Arabic-named glyphs",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--x-scale-mode", choices=("target-advance", "upm", "same-as-y"), default="target-advance")
    parser.add_argument("--write", action="store_true", help="write scratch candidate sources")
    parser.add_argument("--force", action="store_true", help="replace existing output directory")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if args.donor is None:
        raise SystemExit("Set --donor /path/to/reference.designspace or DONOR_DESIGNSPACE=/path/to/reference.designspace.")
    donor = args.donor.expanduser().resolve()
    output = args.output.expanduser().resolve()
    glyphs = parse_glyphs(args.glyphs, target)
    if args.arabic_only:
        glyphs = arabic_glyph_filter(glyphs)
    excluded_glyphs = set(parse_glyphs(args.exclude_glyphs, target)) if args.exclude_glyphs else set()
    glyphs_to_replace = [glyph for glyph in glyphs if glyph not in excluded_glyphs]

    target_regular, target_bold = master_pair(target)
    donor_light, donor_black = master_pair(donor)
    print(f"target masters: {target_regular.path}, {target_bold.path}")
    print(f"donor masters: {donor_light.path}, {donor_black.path}")
    print(f"glyphs: {', '.join(glyphs)}")
    if excluded_glyphs:
        print(f"preserving from target: {', '.join(sorted(excluded_glyphs))}")

    if not args.write:
        print("dry run: pass --write to create scratch candidate sources")
        return 0

    candidate_source = copy_target_source(target, output, force=args.force)
    candidate_regular, candidate_bold = master_pair(candidate_source)
    original_regular = ufoLib2.Font.open(target_regular.path)
    donor_regular = ufoLib2.Font.open(donor_light.path)
    donor_bold = ufoLib2.Font.open(donor_black.path)
    candidate_regular_font = ufoLib2.Font.open(candidate_regular.path)
    candidate_bold_font = ufoLib2.Font.open(candidate_bold.path)

    results: list[GlyphResult] = []
    for glyph_name in glyphs_to_replace:
        donor_name = DONOR_NAME_OVERRIDES.get(glyph_name, glyph_name)
        results.append(
            copy_transformed_glyph(candidate_regular_font, donor_regular, glyph_name, donor_name, args.x_scale_mode)
        )
        results.append(
            copy_transformed_glyph(candidate_bold_font, donor_bold, glyph_name, donor_name, args.x_scale_mode)
        )

    candidate_regular_font.save(candidate_regular.path, overwrite=True)
    candidate_bold_font.save(candidate_bold.path, overwrite=True)
    for glyph_name in sorted(excluded_glyphs):
        results.append(
            GlyphResult(
                glyph=glyph_name,
                donor_glyph=DONOR_NAME_OVERRIDES.get(glyph_name, glyph_name),
                master="both",
                status="preserved-target",
            )
        )

    proof_path = write_proof(output, glyphs, original_regular, donor_regular, candidate_regular_font)
    write_reports(output, results, proof_path, args)
    print(output / "glyph-candidate-report.md")
    print(proof_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
