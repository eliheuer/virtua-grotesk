#!/usr/bin/env python3
"""Prepare AI-assisted glyph drawing packets for Virtua Grotesk.

The harness uses Runebender's UFO mark colors as source metadata:
green glyphs are treated as good references, rendered from the active UFO
outlines via the designbot canvas toolchain (harness/designbot/
glyph_canvas.rs), and packaged with prompts plus img2bez trace commands
for a target glyph.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import plistlib
import shlex
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

from fontTools.pens.boundsPen import BoundsPen
from ufoLib2 import Font
from design_context import build_packet, color_state, read_json, verify_packet, markdown


ROOT = Path(__file__).resolve().parents[1]
MASTER_UFOS = {
    "regular": ROOT / "sources" / "VirtuaGrotesk-Regular.ufo",
    "bold": ROOT / "sources" / "VirtuaGrotesk-Bold.ufo",
}
DEFAULT_OUTPUT_ROOT = ROOT / ".glyph-ai-runs"

CONTRACT = read_json(ROOT / "design/system/contract.json")

IMAGE_SIZE = 1536
IMAGE_PADDING = 256
DESIGN_CHAMFER = 16


@dataclass(frozen=True)
class GlyphRecord:
    master: str
    glyph: str
    glif: str
    unicode: str | None
    width: int | None
    mark_color: str | None
    role: str
    contours: int
    components: int
    path: str


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def split_glyph_list(values: list[str] | None) -> list[str]:
    glyphs: list[str] = []
    for value in values or []:
        for part in value.replace(",", " ").split():
            if part and part not in glyphs:
                glyphs.append(part)
    return glyphs


def mark_role(mark_color: str | None, label: str | None = None) -> str:
    state = color_state({"public.markColor": mark_color,
                         "com.runebender.markLabel": label}, CONTRACT)
    return "good-reference" if state["reference_eligible"] else state["name"] + "-mark"


def plist_value_after_key(dict_element: ET.Element, key_name: str) -> str | None:
    children = list(dict_element)
    for index, child in enumerate(children[:-1]):
        if child.tag == "key" and child.text == key_name:
            return children[index + 1].text
    return None


def glif_record(master: str, ufo_path: Path, glyph_name: str, file_name: str) -> GlyphRecord:
    path = ufo_path / "glyphs" / file_name
    root = ET.parse(path).getroot()
    advance = root.find("advance")
    width = None
    if advance is not None and advance.attrib.get("width"):
        width = round(float(advance.attrib["width"]))
    unicode_element = root.find("unicode")
    unicode_hex = unicode_element.attrib.get("hex") if unicode_element is not None else None
    lib_dict = root.find("lib/dict")
    mark_color = plist_value_after_key(lib_dict, "public.markColor") if lib_dict is not None else None
    outline = root.find("outline")
    contours = len(outline.findall("contour")) if outline is not None else 0
    components = len(outline.findall("component")) if outline is not None else 0
    return GlyphRecord(
        master=master,
        glyph=glyph_name,
        glif=file_name,
        unicode=unicode_hex,
        width=width,
        mark_color=mark_color,
        role=mark_role(mark_color, plist_value_after_key(lib_dict, "com.runebender.markLabel") if lib_dict is not None else None),
        contours=contours,
        components=components,
        path=display_path(path),
    )


def scan_ufo(master: str, ufo_path: Path) -> dict[str, GlyphRecord]:
    contents_path = ufo_path / "glyphs" / "contents.plist"
    contents = plistlib.loads(contents_path.read_bytes())
    return {
        glyph_name: glif_record(master, ufo_path, glyph_name, file_name)
        for glyph_name, file_name in sorted(contents.items())
    }


def scan_sources() -> dict[str, dict[str, GlyphRecord]]:
    return {
        master: scan_ufo(master, ufo_path)
        for master, ufo_path in MASTER_UFOS.items()
    }


def write_inventory(output_root: Path) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    records_by_master = scan_sources()
    records = [
        asdict(record)
        for master_records in records_by_master.values()
        for record in master_records.values()
    ]
    payload = {
        "schema": "virtua-grotesk.glyph-ai-inventory.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "color_contract": "design/system/contract.json",
        "masters": {master: display_path(path) for master, path in MASTER_UFOS.items()},
        "records": records,
    }
    json_path = output_root / "inventory.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# AI Glyph Harness Inventory",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "Verified green variants in design/system/contract.json qualify as references; conflicting labels do not.",
        "Other colors are reported by color only; this harness does not assign design approval semantics to them.",
        "",
    ]
    for master, master_records in records_by_master.items():
        lines.extend([f"## {master.title()}", "", "| Role | Count | Glyphs |", "| --- | ---: | --- |"])
        roles: dict[str, list[str]] = {}
        for record in master_records.values():
            roles.setdefault(record.role, []).append(record.glyph)
        for role in sorted(roles):
            glyphs = ", ".join(f"`{name}`" for name in roles[role])
            lines.append(f"| {role} | {len(roles[role])} | {glyphs} |")
        lines.append("")
    markdown_path = output_root / "inventory.md"
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, markdown_path


def load_font(ufo_path: Path) -> Font:
    return Font.open(ufo_path, lazy=False)


def glyph_bounds(font: Font, glyph_name: str) -> tuple[float, float, float, float] | None:
    glyph = font[glyph_name]
    pen = BoundsPen(font)
    glyph.draw(pen)
    return pen.bounds


def render_glyph_png(master: str, glyph_name: str, output_path: Path) -> dict[str, object]:
    """Render one glyph on the canvas-template frame via the designbot
    toolchain (harness/designbot/glyph_canvas.rs glyphbox mode) — pure Rust
    rendering, 1 font unit = 1 px, metric lines + advance box included."""
    ufo_path = MASTER_UFOS[master]
    font = load_font(ufo_path)
    if glyph_name not in font:
        raise KeyError(f"{glyph_name} is missing from {display_path(ufo_path)}")
    width = float(font[glyph_name].width or 0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    designbot = shutil.which("designbot")
    if designbot is None:
        raise SystemExit(
            "designbot is required (install: cargo install --path designbot-cli "
            "in ~/GH/repos/designbot)."
        )
    command = [
        designbot,
        "--render",
        str(ROOT / "harness" / "designbot" / "glyph_canvas.rs"),
        "--output",
        str(output_path),
        "--",
        "glyphbox",
        str(ufo_path),
        glyph_name,
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            f"designbot glyphbox failed for {master}/{glyph_name}:\n{result.stderr}"
        )

    return {
        "master": master,
        "glyph": glyph_name,
        "path": display_path(output_path),
        "width": round(width),
        "bounds": glyph_bounds(font, glyph_name),
        "image_size": IMAGE_SIZE,
        "padding": IMAGE_PADDING,
        "scale": 1.0,
        "template": "glyph-canvas (1 unit = 1 px, metric lines, advance box)",
    }


def target_metadata(records_by_master: dict[str, dict[str, GlyphRecord]], target: str) -> dict[str, object]:
    per_master = {
        master: asdict(master_records[target])
        for master, master_records in records_by_master.items()
        if target in master_records
    }
    unicode_values = [record["unicode"] for record in per_master.values() if record.get("unicode")]
    widths = [record["width"] for record in per_master.values() if record.get("width")]
    return {
        "glyph": target,
        "unicode": unicode_values[0] if unicode_values else None,
        "width": widths[0] if widths else None,
        "masters": per_master,
    }


def prompt_text(
    target: str,
    master: str,
    references: list[dict[str, object]],
    current_render: dict[str, object] | None,
    metadata: dict[str, object],
) -> str:
    reference_lines = "\n".join(
        f"- `{item['glyph']}`: `{item['path']}`" for item in references if item["master"] == master
    )
    if not reference_lines:
        reference_lines = "- No same-master green references were rendered; use the cross-master references in the run manifest."
    current_line = (
        f"Current target render, if useful for comparison: `{current_render['path']}`"
        if current_render
        else "The target glyph is missing in this master or has no usable current render."
    )
    unicode_line = f"Unicode: U+{metadata['unicode']}" if metadata.get("unicode") else "Unicode: none or unknown"
    width_line = f"Advance width target: {metadata['width']} units" if metadata.get("width") else "Advance width target: infer from related glyphs, then set explicitly before tracing"

    return "\n".join(
        [
            f"# OpenAI Image Generation Brief: `{target}` {master.title()}",
            "",
            f"Generate one high-resolution black-on-white raster image for the Virtua Grotesk glyph `{target}` in the {master.title()} master.",
            "",
            "Output requirements:",
            f"- Canvas: {IMAGE_SIZE} x {IMAGE_SIZE} px.",
            "- White background, solid black glyph silhouette only.",
            "- No labels, grid, shadow, texture, paper, outlines, antialiasing notes, or extra marks.",
            "- Keep the glyph centered in its advance box with baseline and vertical scale matching the references.",
            f"- {unicode_line}",
            f"- {width_line}",
            "",
            "Style requirements:",
            "- Geometric grotesk, monolinear strokes, no contrast.",
            f"- Virtua Grotesk's sharp joins use 45-degree chamfers, usually {DESIGN_CHAMFER} font units.",
            "- Keep curved glyphs smooth; the img2bez trace defaults to no automatic chamfering.",
            "- Coordinates should be compatible with a 1024 UPM, ascender 768, descender -256 source.",
            "- Prefer simple contours that will trace cleanly; avoid fuzzy, painterly, or ornamental edges.",
            "",
            "Same-master green reference renders:",
            reference_lines,
            "",
            current_line,
            "",
            "Save the generated image for tracing as:",
            f"`generated/{master}/{target}.png`",
            "",
        ]
    )


def img2bez_command(target, metadata, run_dir):
    command = ["img2bez", "masters", str(run_dir / "trace/VirtuaGrotesk.designspace"),
               "--glyph", target, "--fit", metadata["fit"], "--profile", "wild",
               "--fail-on-low-confidence", "--report", str(run_dir / "trace/report.json")]
    for master in MASTER_UFOS:
        command += ["--image", f"{master.title()}={run_dir / 'generated' / master / (target + '.png')}"]
    if metadata.get("unicode"):
        command += ["--unicode", metadata["unicode"]]
    if metadata.get("width"):
        command += ["--preserve-existing-metrics"]
    return command


def shell_join(parts):
    return " ".join(shlex.quote(str(part)) for part in parts)


def write_trace_script(run_dir, target, metadata, masters):
    script_path = run_dir / "trace-commands.sh"
    script_path.write_text("#!/usr/bin/env bash\nset -euo pipefail\ncd " + shlex.quote(str(ROOT)) +
                          "\nexec " + shell_join([sys.executable, "scripts/glyph_ai_harness.py", "trace", "--run-dir", str(run_dir.resolve())]) + "\n")
    script_path.chmod(0o755)
    return script_path


def prepare_run(target: str, references: list[str], masters: list[str], run_dir: Path, fit: str) -> Path:
    if set(masters) != set(MASTER_UFOS):
        raise SystemExit("Prepare both masters for compatible tracing; use render for single-master inspection")
    if run_dir.exists() and any(run_dir.iterdir()):
        raise SystemExit("Run directory is not empty; choose a fresh --out to preserve evidence")
    packet = build_packet(ROOT, [target], [m.title() for m in masters], "from-image")
    if not fit or ":" not in fit:
        raise SystemExit("Supply the calibrated --fit bottom:top band")
    records_by_master = scan_sources()
    default_reference_map = {m: [g["glyph"] for g in packet["references"]
                                if g["master"] == m.title() and g.get("color", {}).get("reference_eligible")]
                             for m in masters}
    reference_map = (
        {master: references for master in masters}
        if references
        else {master: default_reference_map[master] for master in masters}
    )
    if not all(reference_map.values()):
        raise SystemExit("Choose existing green construction references with --references; do not regrade sources")
    selected_references = []
    for master, names in reference_map.items():
        for name in names:
            if name not in records_by_master[master] or records_by_master[master][name].role != "good-reference":
                raise SystemExit(f"{master}/{name}: not a verified green construction reference")
        reference_packet = build_packet(ROOT, names, [master.title()], "inspect")
        packet["guard_hashes"].update(reference_packet["guard_hashes"])
        selected_references.extend(reference_packet["targets"])

    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "generated").mkdir(exist_ok=True)
    (run_dir / "context.json").write_text(json.dumps(packet, indent=2) + "\n")
    (run_dir / "context.md").write_text(markdown(packet))
    # A deliberately unfilled construction study precedes fitting; not approval.
    from construction_review import make_plan, render as render_construction
    study = make_plan({**packet, "references": selected_references})
    (run_dir / "construction.json").write_text(json.dumps(study, indent=2) + "\n")
    (run_dir / "construction.html").write_text(render_construction(ROOT, study))

    rendered_references: list[dict[str, object]] = []
    rendered_current: dict[str, dict[str, object] | None] = {}
    warnings: list[str] = []

    for master in masters:
        master_records = records_by_master[master]
        for glyph_name in reference_map[master]:
            record = master_records.get(glyph_name)
            if record is None:
                warnings.append(f"{glyph_name} is missing in {master}; skipped reference render.")
                continue
            if record.role != "good-reference":
                warnings.append(
                    f"{glyph_name} in {master} is {record.role}, not green good-reference."
                )
            rendered_references.append(
                render_glyph_png(
                    master,
                    glyph_name,
                    run_dir / "references" / master / f"{glyph_name}.png",
                )
            )
        if target in master_records and (master_records[target].contours or master_records[target].components):
            rendered_current[master] = render_glyph_png(
                master,
                target,
                run_dir / "current" / master / f"{target}.png",
            )
        else:
            rendered_current[master] = None

    metadata = target_metadata(records_by_master, target)
    metadata["fit"] = fit
    prompt_paths: dict[str, str] = {}
    prompts_dir = run_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    for master in masters:
        path = prompts_dir / f"{master}-{target}.md"
        path.write_text(
            prompt_text(
                target,
                master,
                rendered_references,
                rendered_current[master],
                metadata,
            ) + "\nRead context.md for construction, corrections, exceptions and current source guards.\n",
            encoding="utf-8",
        )
        prompt_paths[master] = display_path(path)

    trace_script = write_trace_script(run_dir, target, metadata, masters)
    manifest = {
        "schema": "virtua-grotesk.glyph-ai-run.v2",
        "context": "context.json",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": metadata,
        "masters": masters,
        "references_requested": reference_map,
        "reference_renders": rendered_references,
        "current_target_renders": rendered_current,
        "prompts": prompt_paths,
        "trace_script": display_path(trace_script),
        "trace_commands": [
            shell_join(img2bez_command(target, metadata, run_dir))
        ],
        "warnings": warnings,
    }
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    readme = [
        f"# Glyph AI Run: `{target}`",
        "",
        "1. Read `context.md`, `manifest.json` and the rendered green references; retain named authorization.",
        "2. Use each file in `prompts/` with OpenAI image generation.",
        "3. Save generated PNGs to `generated/<master>/<glyph>.png`.",
        "4. Run `./trace-commands.sh` to trace into scratch UFOs.",
        "5. Review the trace report, fit and compatibility. Refit to the 8-unit draft contract, check grid/curves, build and visually inspect. Apply only within named authorization; checks do not grade artwork.",
        "",
        f"Trace script: `{display_path(trace_script)}`",
        "",
    ]
    if warnings:
        readme.extend(["## Warnings", ""])
        readme.extend(f"- {warning}" for warning in warnings)
        readme.append("")
    (run_dir / "README.md").write_text("\n".join(readme), encoding="utf-8")
    return manifest_path


def trace_run(run_dir: Path, img2bez: str) -> int:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {display_path(manifest_path)}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "virtua-grotesk.glyph-ai-run.v2":
        raise SystemExit("Legacy packet: prepare a fresh context-aware packet before tracing")
    packet = read_json(run_dir / "context.json")
    changed = verify_packet(ROOT, packet)
    if changed:
        raise SystemExit("Context changed; regenerate the packet: " + ", ".join(changed))
    trace_dir = run_dir / "trace"
    if trace_dir.exists():
        raise SystemExit("Trace already exists; preserve it and use a new run directory")
    for master in manifest["masters"]:
        generated = run_dir / "generated" / master / f"{manifest['target']['glyph']}.png"
        if not generated.exists():
            raise SystemExit(f"Missing generated image: {display_path(generated)}")
    trace_dir.mkdir()
    for master in manifest["masters"]:
        shutil.copytree(MASTER_UFOS[master], trace_dir / MASTER_UFOS[master].name)
    shutil.copy2(ROOT / "sources/VirtuaGrotesk.designspace", trace_dir / "VirtuaGrotesk.designspace")
    command = img2bez_command(manifest["target"]["glyph"], manifest["target"], run_dir.resolve())
    command[0] = img2bez
    subprocess.run(command, cwd=ROOT, check=True)
    report = read_json(trace_dir / "report.json")
    # Do not infer compatibility when the tracer returns an unfamiliar report.
    if report.get("compatible") is not True or report.get("lowConfidence") is not False:
        raise SystemExit("Trace report is incompatible, low-confidence or unknown; inspect before proceeding")
    subprocess.run([sys.executable, "scripts/report_master_compatibility.py",
                    str(trace_dir / MASTER_UFOS["regular"].name),
                    str(trace_dir / MASTER_UFOS["bold"].name),
                    str(trace_dir / "master-compatibility.md"), "--check"], cwd=ROOT, check=True)
    print("Scratch trace only. Inspect fit, refit to the draft grid, build and review before any authorized application.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory", help="scan UFO mark colors")
    inventory.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_ROOT)

    render = subparsers.add_parser("render", help="render source glyphs to PNG")
    render.add_argument("--glyph", action="append", required=True)
    render.add_argument("--master", choices=MASTER_UFOS, action="append")
    render.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_ROOT / "renders")

    prepare = subparsers.add_parser("prepare", help="prepare an AI/image/img2bez run packet")
    prepare.add_argument("--target", required=True)
    prepare.add_argument("--fit", required=True, help="Calibrated bottom:top band in font units or metric zones; never guess")
    prepare.add_argument("--references", nargs="*", help="glyph names, comma- or space-separated")
    prepare.add_argument("--master", choices=MASTER_UFOS, action="append")
    prepare.add_argument("--out", type=Path)

    trace = subparsers.add_parser("trace", help="trace generated images into scratch UFOs")
    trace.add_argument("--run-dir", type=Path, required=True)
    trace.add_argument("--img2bez", default=shutil.which("img2bez") or "img2bez")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "inventory":
        json_path, markdown_path = write_inventory(args.out)
        print(f"Wrote {display_path(json_path)}")
        print(f"Wrote {display_path(markdown_path)}")
        return 0
    if args.command == "render":
        masters = args.master or list(MASTER_UFOS)
        for master in masters:
            for glyph_name in split_glyph_list(args.glyph):
                result = render_glyph_png(master, glyph_name, args.out / master / f"{glyph_name}.png")
                print(f"Wrote {result['path']}")
        return 0
    if args.command == "prepare":
        masters = args.master or list(MASTER_UFOS)
        references = split_glyph_list(args.references)
        run_dir = args.out or DEFAULT_OUTPUT_ROOT / args.target
        manifest = prepare_run(args.target, references, masters, run_dir, args.fit)
        print(f"Wrote {display_path(manifest)}")
        return 0
    if args.command == "trace":
        return trace_run(args.run_dir, args.img2bez)
    parser.error("unreachable")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
