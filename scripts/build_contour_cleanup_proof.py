#!/usr/bin/env python3
"""Build an HTML proof sheet for Fontspector contour-count findings."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import os
from pathlib import Path
import plistlib
import re
import sys
from xml.etree import ElementTree

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.ufoLib import UFOReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "documentation/google-fonts/fontspector-contour-count.md"
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html"
DEFAULT_QUEUE_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-review-queue.md"
DEFAULT_EDIT_PLAN_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-edit-plan.md"
DEFAULT_BRIEF_OUTPUT = ROOT / "documentation/glyph-review/arabic-cleanup-drawing-briefs.md"
DEFAULT_BATCH_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md"
DEFAULT_DECISION_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md"
DEFAULT_TRIAGE_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-ai-triage.md"
DEFAULT_SOURCE_EDIT_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md"
DEFAULT_FIRST_BATCH_OUTPUT = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-first-edit-batch.md"
DEFAULT_REFERENCE_CANDIDATES = (
    [Path(os.environ["ARABIC_REFERENCE_FONT"])]
    if os.environ.get("ARABIC_REFERENCE_FONT")
    else []
)
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]
EDIT_PRIORITY = {
    "source outline review": 1,
    "Arabic letter or positional form": 2,
    "Arabic mark or mark combination": 3,
    "Arabic dot-stack helper": 4,
    "shared punctuation": 5,
}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def reference_path() -> Path | None:
    for path in DEFAULT_REFERENCE_CANDIDATES:
        if path.exists():
            return path
    return None


@dataclass(frozen=True)
class Finding:
    font_path: Path
    glyph_name: str
    codepoint_label: str
    actual: str
    expected: str

    @property
    def codepoint(self) -> int | None:
        if not self.codepoint_label.startswith("U+"):
            return None
        try:
            return int(self.codepoint_label[2:], 16)
        except ValueError:
            return None


@dataclass(frozen=True)
class ReviewItem:
    glyph_name: str
    source_name: str
    codepoint_label: str
    actual_values: tuple[str, ...]
    expected_values: tuple[str, ...]
    font_names: tuple[str, ...]
    category: str
    sample: Finding


@dataclass(frozen=True)
class GlyphStructure:
    contours: int
    points: int
    components: int
    component_bases: tuple[str, ...]
    filename: str

    @property
    def label(self) -> str:
        return f"c{self.contours}/p{self.points}/comp{self.components}"

    @property
    def component_label(self) -> str:
        return ", ".join(f"`{base}`" for base in self.component_bases) if self.component_bases else "none"


def source_name_map() -> dict[str, str]:
    names: dict[str, str] = {}
    for ufo_path in SOURCE_UFOS:
        lib_path = ufo_path / "lib.plist"
        if lib_path.exists():
            with lib_path.open("rb") as file:
                postscript_names = plistlib.load(file).get("public.postscriptNames", {})
            for source_name, production_name in postscript_names.items():
                names.setdefault(production_name, source_name)

        reader = UFOReader(ufo_path)
        for codepoint, source_names in reader.getCharacterMapping().items():
            if source_names:
                names.setdefault(f"U+{codepoint:04X}", source_names[0])
    return names


def source_name_for_finding(finding: Finding, names: dict[str, str]) -> str:
    if finding.glyph_name in names:
        return names[finding.glyph_name]
    if "." not in finding.glyph_name and finding.codepoint_label in names:
        return names[finding.codepoint_label]
    return "review source map"


def source_glyph_structures() -> dict[str, dict[str, GlyphStructure]]:
    structures: dict[str, dict[str, GlyphStructure]] = {}
    for ufo_path in SOURCE_UFOS:
        contents_path = ufo_path / "glyphs/contents.plist"
        with contents_path.open("rb") as file:
            contents = plistlib.load(file)
        master_name = ufo_path.name.replace("VirtuaGrotesk-", "").replace(".ufo", "")
        for glyph_name, filename in contents.items():
            glif_path = ufo_path / "glyphs" / filename
            if not glif_path.exists():
                continue
            root = ElementTree.parse(glif_path).getroot()
            contours = root.findall("./outline/contour")
            components = root.findall("./outline/component")
            point_count = sum(len(contour.findall("./point")) for contour in contours)
            component_bases = tuple(
                component.attrib["base"] for component in components if "base" in component.attrib
            )
            structures.setdefault(glyph_name, {})[master_name] = GlyphStructure(
                contours=len(contours),
                points=point_count,
                components=len(components),
                component_bases=component_bases,
                filename=filename,
            )
    return structures


def source_structure_label(source_name: str, structures: dict[str, dict[str, GlyphStructure]]) -> str:
    masters = structures.get(source_name, {})
    return "<br>".join(
        f"{master}: `{masters[master].label}`" if master in masters else f"{master}: missing"
        for master in ("Regular", "Bold")
    )


def source_structure_compatible(source_name: str, structures: dict[str, dict[str, GlyphStructure]]) -> str:
    regular = structures.get(source_name, {}).get("Regular")
    bold = structures.get(source_name, {}).get("Bold")
    if not regular or not bold:
        return "missing master"
    return "yes" if (regular.contours, regular.points, regular.components) == (bold.contours, bold.points, bold.components) else "review"


def parse_findings(report_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    current_font: Path | None = None
    row_re = re.compile(r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$")

    for line in report_path.read_text().splitlines():
        if line.startswith("## `") and line.endswith("`"):
            current_font = ROOT / line.removeprefix("## `").removesuffix("`")
            continue
        match = row_re.match(line)
        if not match or current_font is None:
            continue
        glyph_name, codepoint_label, actual, expected = [part.strip() for part in match.groups()]
        if glyph_name == "Glyph":
            continue
        findings.append(Finding(current_font, glyph_name, codepoint_label, actual, expected))
    return findings


def finding_category(glyph_name: str, codepoint_label: str) -> str:
    if glyph_name in {"braceleft", "braceright"}:
        return "shared punctuation"
    if glyph_name.startswith(("uni065", "smallHigh", "noonGhunna")):
        return "Arabic mark or mark combination"
    if any(token in glyph_name for token in ("dots", "dot", "sixdots", "Threedots")):
        return "Arabic dot-stack helper"
    if codepoint_label.startswith("U+06") or glyph_name.endswith("ar") or glyph_name.startswith("uni064"):
        return "Arabic letter or positional form"
    return "source outline review"


def review_items(findings: list[Finding]) -> list[ReviewItem]:
    source_names = source_name_map()
    grouped: dict[tuple[str, str], list[Finding]] = {}
    for finding in findings:
        grouped.setdefault((finding.glyph_name, finding.codepoint_label), []).append(finding)

    items: list[ReviewItem] = []
    for (glyph_name, codepoint_label), rows in grouped.items():
        items.append(
            ReviewItem(
                glyph_name=glyph_name,
                source_name=source_name_for_finding(rows[0], source_names),
                codepoint_label=codepoint_label,
                actual_values=tuple(sorted({row.actual for row in rows})),
                expected_values=tuple(sorted({row.expected for row in rows})),
                font_names=tuple(sorted({row.font_path.name for row in rows})),
                category=finding_category(glyph_name, codepoint_label),
                sample=rows[0],
            )
        )
    return sorted(items, key=lambda item: (item.category, item.glyph_name, item.codepoint_label))


class FontRenderer:
    def __init__(self, path: Path):
        self.path = path
        self.font = TTFont(path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap() or {}
        self.upm = self.font["head"].unitsPerEm

    def glyph_for_codepoint(self, codepoint: int) -> str | None:
        return self.cmap.get(codepoint)

    def has_glyph(self, glyph_name: str) -> bool:
        return glyph_name in self.glyph_set

    def svg_for_glyph(self, glyph_name: str | None) -> str:
        if not glyph_name or glyph_name not in self.glyph_set:
            return '<div class="missing">not present</div>'

        glyph = self.glyph_set[glyph_name]
        bounds_pen = BoundsPen(self.glyph_set)
        glyph.draw(bounds_pen)
        bounds = bounds_pen.bounds
        advance = getattr(glyph, "width", 0) or 0

        if bounds is None:
            xmin, ymin, xmax, ymax = 0, -120, max(advance, 160), 120
        else:
            xmin, ymin, xmax, ymax = bounds
            xmin = min(xmin, 0)
            xmax = max(xmax, advance, 0)

        pad = 80
        view_x = xmin - pad
        view_y = -(ymax + pad)
        view_w = max(120, (xmax - xmin) + (pad * 2))
        view_h = max(160, (ymax - ymin) + (pad * 2))

        path_pen = SVGPathPen(self.glyph_set)
        glyph.draw(path_pen)
        path = path_pen.getCommands()
        baseline = -view_y
        origin_x = -view_x
        advance_x = origin_x + advance

        return "\n".join(
            [
                f'<svg viewBox="{view_x:.0f} {view_y:.0f} {view_w:.0f} {view_h:.0f}" role="img">',
                f'  <line class="metric" x1="{view_x:.0f}" y1="{baseline:.0f}" x2="{view_x + view_w:.0f}" y2="{baseline:.0f}"/>',
                f'  <line class="sidebearing" x1="{origin_x:.0f}" y1="{view_y:.0f}" x2="{origin_x:.0f}" y2="{view_y + view_h:.0f}"/>',
                f'  <line class="sidebearing" x1="{advance_x:.0f}" y1="{view_y:.0f}" x2="{advance_x:.0f}" y2="{view_y + view_h:.0f}"/>',
                f'  <g transform="scale(1,-1)"><path d="{escape(path)}"/></g>',
                "</svg>",
            ]
        )


def reference_name_candidates(item: ReviewItem) -> list[str]:
    source_name = item.source_name
    source_ar = source_name.replace("-ar.", "ar.").replace("-ar", "ar")
    production = item.glyph_name
    candidates = [
        production,
        source_name,
        source_ar,
        f"{production}.1",
        f"{source_ar}.1",
    ]
    if source_name.startswith("lam_alef") and not source_ar.endswith(".fina"):
        candidates.append(f"{source_ar}.fina")
    return list(dict.fromkeys(candidates))


def reference_glyph_for_item(reference: FontRenderer | None, item: ReviewItem) -> str | None:
    if not reference:
        return None
    if item.sample.codepoint:
        cmap_glyph = reference.glyph_for_codepoint(item.sample.codepoint)
        if cmap_glyph:
            return cmap_glyph
    for candidate in reference_name_candidates(item):
        if reference.has_glyph(candidate):
            return candidate
    return None


def reference_status(reference: FontRenderer | None, item: ReviewItem) -> str:
    glyph_name = reference_glyph_for_item(reference, item)
    return f"yes: `{glyph_name}`" if glyph_name else "no"


def grouped_findings(findings: list[Finding]) -> dict[str, list[Finding]]:
    grouped: dict[str, list[Finding]] = {}
    for finding in findings:
        grouped.setdefault(finding.font_path.name, []).append(finding)
    return grouped


def category_counts(items: list[ReviewItem]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.category] = counts.get(item.category, 0) + 1
    return counts


def recommended_action(category: str) -> str:
    if category == "shared punctuation":
        return "Redraw deliberately in both masters only if visual review shows a real issue."
    if category == "Arabic mark or mark combination":
        return "Review mark positioning and whether the glyph should stay precomposed or decompose to anchors."
    if category == "Arabic dot-stack helper":
        return "Review dot collisions and weight behavior before changing contour structure."
    if category == "Arabic letter or positional form":
        return "Review the intended Arabic drawing; do not add/delete contours only to satisfy the heuristic."
    return "Inspect source outline structure and compare the rendered proof before editing."


def review_question(category: str) -> str:
    if category == "shared punctuation":
        return "Does the current punctuation shape fit the family and interpolate cleanly, or should it be redrawn as a deliberate two-master shape?"
    if category == "Arabic mark or mark combination":
        return "Is this mark or mark combination positioned correctly in real Arabic strings and on dotted circle?"
    if category == "Arabic dot-stack helper":
        return "Do the dots remain clear, evenly spaced, and collision-free across Regular and Bold?"
    if category == "Arabic letter or positional form":
        return "Does this Arabic form match the intended skeleton, joining behavior, counter rhythm, and Virtua chamfer style?"
    return "Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence?"


def triage_lane(
    item: ReviewItem,
    structures: dict[str, dict[str, GlyphStructure]],
    reference: FontRenderer | None,
) -> tuple[str, str, str, str]:
    batch = review_batch(item, structures, reference)
    masters = structures.get(item.source_name, {})
    regular = masters.get("Regular")
    bold = masters.get("Bold")
    component_only = bool(
        regular
        and bold
        and regular.contours == 0
        and bold.contours == 0
        and regular.components > 0
        and bold.components > 0
    )
    has_reference = reference_glyph_for_item(reference, item) is not None
    all_fonts = len(item.font_names) >= 5

    if component_only:
        return (
            "component-source-review",
            "medium",
            "Inspect the composed output first; the source has components only, so the contour count may be a build-time decomposition artifact.",
            "Accept only if joins and dots look intentional in the proof; otherwise redraw or decompose both masters deliberately.",
        )
    if item.category == "shared punctuation":
        return (
            "low-risk-punctuation-review",
            "low",
            "Review Latin and Arabic text behavior before changing; this is probably a style/overlap heuristic unless the proof shows malformed braces.",
            "If the shape is clean, record an accepted style divergence; if not, redraw both masters as a punctuation cleanup.",
        )
    if item.category == "Arabic dot-stack helper":
        return (
            "dot-collision-review",
            "medium",
            "Check Bold and variable output first; dot-stack warnings are useful when dots collide or merge at heavier weights.",
            "Fix spacing/scale if dots merge; otherwise accept or defer with a note that dot readability was reviewed.",
        )
    if item.category == "Arabic mark or mark combination":
        return (
            "mark-position-review",
            "high" if all_fonts else "medium",
            "Check dotted circle and real Arabic bases; contour heuristics are secondary to mark placement and stacking clarity.",
            "Fix if mark stacks collide or attach off-center; otherwise record accepted/deferred with proof evidence.",
        )
    if item.category == "Arabic letter or positional form":
        return (
            "arabic-letterform-review",
            "high" if all_fonts else "medium",
            "Judge skeleton, counter, joins, and chamfer style. Do not add contours just to satisfy the heuristic.",
            "Fix if the glyph is structurally wrong or unreadable; otherwise defer to native-reader review or accept as a documented style divergence.",
        )
    if has_reference:
        return (
            "reference-assisted-review",
            "medium",
            "Use Rubik only to understand expected structure; compare the Virtua drawing to its own style before editing.",
            "Record whether the warning is a true source issue, an accepted divergence, or a native-reader deferral.",
        )
    return (
        "source-outline-review",
        "medium",
        "Inspect source and proof together before changing contours.",
        "Fix only when the rendered glyph is actually wrong; otherwise record the reviewed decision.",
    )


def acceptance_criteria(category: str) -> list[str]:
    common = [
        "Regular and Bold keep matching contour, point, and component structure.",
        "`make contour-cleanup-proof` reflects the intended decision after editing.",
        "`make preflight-only` still passes with only documented blockers.",
    ]
    if category == "Arabic mark or mark combination":
        return [
            "Mark position is visually acceptable on dotted circle and representative Arabic bases.",
            "Anchor behavior and built `mark`/`mkmk` remain intact.",
            *common,
        ]
    if category == "Arabic letter or positional form":
        return [
            "Default and positional forms keep coherent joins and sidebearings.",
            "Counters, terminals, and chamfers fit the existing Virtua Arabic style.",
            *common,
        ]
    if category == "Arabic dot-stack helper":
        return [
            "Dot stacks remain distinguishable in Bold and do not collide with the base.",
            "Dot placement follows existing Virtua dot helper rhythm.",
            *common,
        ]
    if category == "shared punctuation":
        return [
            "Shape follows Virtua punctuation rhythm and does not regress Latin text.",
            "Any overlap flattening is deliberate and mirrored in both masters.",
            *common,
        ]
    return [
        "Compiled output and source structure tell the same story after review.",
        "Any component decomposition or contour addition is intentional and mirrored.",
        *common,
    ]


def edit_plan_priority(category: str) -> str:
    if category == "source outline review":
        return "P1 source-structure check"
    if category == "Arabic letter or positional form":
        return "P2 Arabic form review"
    if category == "Arabic mark or mark combination":
        return "P3 mark-placement review"
    if category == "Arabic dot-stack helper":
        return "P4 dot-collision review"
    return "P5 shared punctuation review"


def source_structure_lines(source_name: str, structures: dict[str, dict[str, GlyphStructure]]) -> list[str]:
    masters = structures.get(source_name, {})
    lines = []
    for master in ("Regular", "Bold"):
        if master in masters:
            structure = masters[master]
            lines.append(
                f"- {master}: `{structure.label}` in `{structure.filename}`; "
                f"components: {structure.component_label}"
            )
        else:
            lines.append(f"- {master}: missing")
    return lines


def review_batch(
    item: ReviewItem,
    structures: dict[str, dict[str, GlyphStructure]],
    reference: FontRenderer | None,
) -> str:
    masters = structures.get(item.source_name, {})
    has_reference = reference_glyph_for_item(reference, item) is not None
    regular = masters.get("Regular")
    bold = masters.get("Bold")
    component_only = bool(
        regular
        and bold
        and regular.contours == 0
        and bold.contours == 0
        and regular.components > 0
        and bold.components > 0
    )

    if component_only:
        return "1. Component-only source forms"
    if item.category == "Arabic mark or mark combination" and has_reference:
        return "2. Referenced Arabic marks and ligatures"
    if item.category == "Arabic dot-stack helper":
        return "3. Dot-stack helpers"
    if item.category == "Arabic letter or positional form":
        return "4. Arabic letterform review"
    if item.category == "shared punctuation":
        return "5. Shared punctuation"
    return "6. Source-outline judgment calls"


def build_batch_plan(findings: list[Finding], reference_path: Path | None) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    grouped: dict[str, list[ReviewItem]] = {}
    for item in items:
        grouped.setdefault(review_batch(item, structures, reference), []).append(item)

    lines = [
        "# Contour Cleanup Batches",
        "",
        "This generated batch sheet turns the remaining Fontspector contour-count",
        "warnings into short hand-edit sessions. It is designed for Runebender",
        "cleanup plus AI comparison notes. Rubik is a structural reference only;",
        "do not copy outlines from it into Virtua Grotesk.",
        "",
        f"- Source report: `documentation/google-fonts/fontspector-contour-count.md`",
        f"- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`",
        f"- Source edit runlist: `documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md`",
        f"- First edit batch: `documentation/glyph-review/contour-cleanup/contour-cleanup-first-edit-batch.md`",
        f"- Detailed prompt cards: `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`",
        f"- Unique review items: {len(items)}",
        f"- All-font finding rows: {len(findings)}",
        "",
        "## Recommended Session Order",
        "",
        "1. Component-only source forms: decide whether the component structure is",
        "   intentional or should be decomposed/redrawn in both masters.",
        "2. Referenced Arabic marks and ligatures: use Rubik only to understand",
        "   expected structure and mark stacking behavior.",
        "3. Dot-stack helpers: check Bold collisions and readability first.",
        "4. Arabic letterform review: judge skeleton, joins, counters, and chamfers.",
        "5. Shared punctuation: keep Latin and Arabic text behavior aligned.",
        "6. Source-outline judgment calls: accept, defer, or redraw deliberately.",
        "",
        "After each batch:",
        "",
        "```bash",
        "make contour-cleanup-proof",
        "make preflight-only",
        "```",
        "",
    ]

    for batch_name in sorted(grouped):
        batch_items = grouped[batch_name]
        lines.extend(
            [
                f"## {batch_name}",
                "",
                f"- Items: {len(batch_items)}",
                "",
                "| Source glyph | Fontspector glyph | Actual | Expected | Source structure | Reference | Command | First decision |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in batch_items:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item.source_name}`",
                        f"`{item.glyph_name}`",
                        ", ".join(item.actual_values),
                        ", ".join(item.expected_values),
                        source_structure_label(item.source_name, structures),
                        reference_status(reference, item),
                        f"`/edit-glyph {item.source_name} --master both`",
                        review_question(item.category),
                    ]
                )
                + " |"
            )
        lines.extend(
            [
                "",
                "AI batch prompt:",
                "",
                "```text",
                (
                    f"Review the {len(batch_items)} Virtua Grotesk glyphs in the "
                    f"'{batch_name}' batch. Use the contour proof and Rubik only as "
                    "structure references. Do not copy outlines. For each glyph, "
                    "classify the warning as fix now, accept as style divergence, "
                    "or defer for Arabic native-reader review, and explain the "
                    "minimal two-master edit if a fix is needed."
                ),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def clean_table_cell(value: str) -> str:
    return value.strip().strip("`").replace("\\|", "|")


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def split_markdown_row(line: str) -> list[str]:
    """Split a simple Markdown table row while preserving escaped pipes."""
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


def existing_decisions(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    decisions: dict[str, dict[str, str]] = {}
    for line in path.read_text().splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 9:
            continue
        source_name = clean_table_cell(cells[0])
        decisions[source_name] = {
            "status": clean_table_cell(cells[5]) or "pending",
            "decision": clean_table_cell(cells[6]) or "pending",
            "notes": clean_table_cell(cells[7]),
            "reviewed": clean_table_cell(cells[8]),
        }
    return decisions


def build_decision_log(findings: list[Finding], reference_path: Path | None, existing_path: Path) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    saved = existing_decisions(existing_path)
    status_counts: dict[str, int] = {}

    rows: list[str] = []
    for item in items:
        decision = saved.get(
            item.source_name,
            {"status": "pending", "decision": "pending", "notes": "", "reviewed": ""},
        )
        status = decision["status"] or "pending"
        status_counts[status] = status_counts.get(status, 0) + 1
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{item.source_name}`",
                    f"`{item.glyph_name}`",
                    review_batch(item, structures, reference),
                    item.category,
                    f"`/edit-glyph {item.source_name} --master both`",
                    escape_table_cell(status),
                    escape_table_cell(decision["decision"]),
                    escape_table_cell(decision["notes"]),
                    escape_table_cell(decision["reviewed"]),
                ]
            )
            + " |"
        )

    lines = [
        "# Contour Cleanup Decision Log",
        "",
        "This file preserves manual review decisions for the remaining contour-count",
        "findings. `make contour-cleanup-proof` regenerates the queue while keeping",
        "the editable Status, Decision, Notes, and Reviewed cells for matching",
        "source glyph names.",
        "",
        "Use Status values such as `pending`, `fix-now`, `fixed`, `accepted`, or",
        "`deferred`. Only mark a warning accepted when the drawing decision is",
        "intentional and reviewable.",
        "",
        "Use `make contour-decision-update GLYPH=<source> STATUS=<status>",
        'DECISION="<short decision>"` to update one row without hand-editing',
        "the wide table.",
        "",
        f"- Unique review items: {len(items)}",
        f"- Pending: {status_counts.get('pending', 0)}",
        f"- Fix-now: {status_counts.get('fix-now', 0)}",
        f"- Fixed: {status_counts.get('fixed', 0)}",
        f"- Accepted: {status_counts.get('accepted', 0)}",
        f"- Deferred: {status_counts.get('deferred', 0)}",
        "",
        "| Source glyph | Fontspector glyph | Batch | Category | Command | Status | Decision | Notes | Reviewed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        *rows,
        "",
    ]
    return "\n".join(lines)


def build_cleanup_briefs(findings: list[Finding], reference_path: Path | None) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    reference_label = display_path(reference_path) if reference and reference_path else "none"
    lines = [
        "# Arabic Cleanup Drawing Briefs",
        "",
        "These generated briefs are prompt cards for the remaining manual Arabic",
        "drawing cleanup. They are meant for Runebender review, AI-assisted",
        "comparison notes, and hand editing. Do not copy outlines from Rubik or",
        "any other reference font into Virtua Grotesk.",
        "",
        f"- Source report: `documentation/google-fonts/fontspector-contour-count.md`",
        f"- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`",
        f"- Edit plan: `documentation/glyph-review/contour-cleanup/contour-cleanup-edit-plan.md`",
        f"- Source edit runlist: `documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md`",
        f"- First edit batch: `documentation/glyph-review/contour-cleanup/contour-cleanup-first-edit-batch.md`",
        f"- Reference font availability: `{reference_label}`",
        f"- Briefs: {len(items)}",
        "",
        "## How To Use",
        "",
        "For each brief:",
        "",
        "1. Open the source glyph in both masters with the listed command.",
        "2. Compare Virtua against the proof HTML and reference only for structure cues.",
        "3. Decide whether the warning is a real drawing issue, an acceptable style divergence, or a deferral.",
        "4. If editing, preserve master compatibility and rerun the batch commands.",
        "",
    ]
    for index, item in enumerate(items, start=1):
        reference_name = reference_glyph_for_item(reference, item)
        reference_label = f"available as `{reference_name}`" if reference_name else "not available"
        lines.extend(
            [
                f"## {index}. {item.source_name}",
                "",
                f"- Priority: {edit_plan_priority(item.category)}",
                f"- Category: {item.category}",
                f"- Fontspector glyph: `{item.glyph_name}`",
                f"- Codepoint: {item.codepoint_label}",
                f"- Built fonts flagged: {', '.join(f'`{font_name}`' for font_name in item.font_names)}",
                f"- Actual contour count(s): {', '.join(item.actual_values)}",
                f"- Expected contour count(s): {', '.join(item.expected_values)}",
                f"- Rubik reference glyph: {reference_label}",
                f"- Command: `/edit-glyph {item.source_name} --master both`",
                "",
                "Source structure:",
                "",
                *source_structure_lines(item.source_name, structures),
                "",
                "Review question:",
                "",
                f"- {review_question(item.category)}",
                "",
                "AI comparison prompt:",
                "",
                "```text",
                (
                    f"Review Virtua Grotesk `{item.source_name}` in Regular and Bold. "
                    f"Fontspector flags `{item.glyph_name}` with contour count "
                    f"{', '.join(item.actual_values)} where it expects {', '.join(item.expected_values)}. "
                    "Compare the current drawing to the family style and to Rubik only as a structural reference. "
                    "Do not copy reference outlines. Identify whether this should be fixed now, accepted as a style divergence, "
                    "or deferred for Arabic native-reader review."
                ),
                "```",
                "",
                "Acceptance criteria:",
                "",
                *[f"- {criterion}" for criterion in acceptance_criteria(item.category)],
                "",
                "Batch commands after edits:",
                "",
                "```bash",
                "make contour-cleanup-proof",
                "make preflight-only",
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def build_ai_triage(findings: list[Finding], reference_path: Path | None) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    lane_counts: dict[str, int] = {}
    rows: list[str] = []
    for item in items:
        lane, risk, why, next_step = triage_lane(item, structures, reference)
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
        accept_command = (
            f"make contour-decision-update GLYPH={item.source_name} STATUS=accepted "
            'DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"'
        )
        fix_command = (
            f"make contour-decision-update GLYPH={item.source_name} STATUS=fix-now "
            'DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"'
        )
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{item.source_name}`",
                    f"`{item.glyph_name}`",
                    lane,
                    risk,
                    review_batch(item, structures, reference),
                    reference_status(reference, item),
                    why,
                    next_step,
                    f"`{fix_command}`<br>`{accept_command}`",
                ]
            )
            + " |"
        )

    lines = [
        "# Contour Cleanup AI Triage",
        "",
        "This generated sheet is an AI-assisted starting point for the manual",
        "contour/no-contour review. It does not mark anything accepted, fixed,",
        "or deferred. Use it to choose a review lane, then inspect the proof and",
        "record the human decision in `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`.",
        "",
        "- Source report: `documentation/google-fonts/fontspector-contour-count.md`",
        "- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`",
        "- Decision log: `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`",
        f"- Triage items: {len(items)}",
        "",
        "## Lane Counts",
        "",
        "| Lane | Items |",
        "| --- | ---: |",
    ]
    for lane, count in sorted(lane_counts.items()):
        lines.append(f"| {lane} | {count} |")

    lines.extend(
        [
            "",
            "## Review Table",
            "",
            "| Source glyph | Fontspector glyph | Triage lane | Risk | Batch | Rubik reference | Why this lane | Next review step | Decision command patterns |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## How To Use",
            "",
            "1. Open `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html` and the matching glyph in Runebender.",
            "2. Use the triage lane to decide whether to inspect components, mark placement, dot collisions, letterform structure, or punctuation rhythm first.",
            "3. If the glyph needs source edits, use the `fix-now` command pattern and edit both masters.",
            "4. If the glyph is visually intentional, use the `accepted` command pattern with a specific proof note.",
            "5. If native-reader review is needed, record `STATUS=deferred` with the reviewed evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def build_source_edit_runlist(
    findings: list[Finding],
    reference_path: Path | None,
    decision_path: Path,
) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    decisions = existing_decisions(decision_path)
    fix_items = [item for item in items if decisions.get(item.source_name, {}).get("status") == "fix-now"]

    lines = [
        "# Contour Cleanup Source Edit Runlist",
        "",
        "This generated runlist is the shortest path from the current contour-count",
        "warnings to source edits. It includes only rows currently marked",
        "`fix-now` in `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`.",
        "",
        "Do not copy outlines from Rubik or any other reference. Use references only",
        "for structural comparison, then edit both Virtua masters deliberately.",
        "",
        "- Source report: `documentation/google-fonts/fontspector-contour-count.md`",
        "- Decision log: `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`",
        "- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`",
        "- Drawing briefs: `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`",
        f"- Fix-now source glyphs: {len(fix_items)}",
        "",
        "## Edit Loop",
        "",
        "For each glyph:",
        "",
        "1. Open the Regular and Bold sources with the listed `/edit-glyph` command.",
        "2. Compare the built glyph in `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`.",
        "3. Edit both masters if the proof shows a real drawing issue.",
        "4. Preserve matching contour, point, and component structure across masters.",
        "5. Mark the row `fixed`, `accepted`, or `deferred` with proof notes.",
        "",
        "After a small batch:",
        "",
        "```bash",
        "make contour-cleanup-proof",
        "make reports-only",
        "make preflight-only",
        "```",
        "",
        "## Fix-Now Queue",
        "",
        "| Order | Source glyph | Batch | Current structure | Rubik reference | Open command | Mark fixed command | Review cue |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for index, item in enumerate(fix_items, start=1):
        fixed_command = (
            f"make contour-decision-update GLYPH={item.source_name} STATUS=fixed "
            'DECISION="source edited and proof reviewed" REVIEWED="Name YYYY-MM-DD"'
        )
        lines.append(
            "| {} | `{}` | {} | {} | {} | `{}` | `{}` | {} |".format(
                index,
                item.source_name,
                review_batch(item, structures, reference),
                source_structure_label(item.source_name, structures),
                reference_status(reference, item),
                f"/edit-glyph {item.source_name} --master both",
                fixed_command,
                review_question(item.category),
            )
        )

    if not fix_items:
        lines.append("|  | none |  |  |  |  |  | No `fix-now` contour rows remain. |")

    lines.extend(
        [
            "",
            "## Defer Or Accept Commands",
            "",
            "Use these only after proof review shows the glyph should not be edited now:",
            "",
            "```bash",
            'make contour-decision-update GLYPH=<source> STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"',
            'make contour-decision-update GLYPH=<source> STATUS=deferred DECISION="needs Arabic native-reader review" REVIEWED="Name YYYY-MM-DD"',
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_first_edit_batch(
    findings: list[Finding],
    reference_path: Path | None,
    decision_path: Path,
) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    decisions = existing_decisions(decision_path)
    fix_items = [
        item
        for item in items
        if decisions.get(item.source_name, {}).get("status") == "fix-now"
        and review_batch(item, structures, reference) == "1. Component-only source forms"
    ]

    lines = [
        "# Contour Cleanup First Edit Batch",
        "",
        "This generated packet isolates the first recommended hand-edit session:",
        "component-only Arabic source forms. These are good first targets because",
        "the source glyphs are component compositions in both masters, so the first",
        "decision is whether the composed output is intentional or whether the form",
        "should be decomposed/redrawn deliberately in both masters.",
        "",
        "Do not edit these only to satisfy Fontspector. Compare the built proof,",
        "the component bases, and the surrounding Arabic letterforms before making",
        "source changes.",
        "",
        "- Source edit runlist: `documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md`",
        "- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`",
        "- Next review page: `documentation/glyph-review/arabic-next-review-batch.html`",
        f"- First-batch fix-now glyphs: {len(fix_items)}",
        "",
        "## Work Order",
        "",
        "| Order | Source glyph | Component bases | Built contour warning | Open command | If edited, mark fixed | If intentional, mark accepted |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]

    for index, item in enumerate(fix_items, start=1):
        master_structures = structures.get(item.source_name, {})
        component_sets = []
        for master in ("Regular", "Bold"):
            structure = master_structures.get(master)
            if structure:
                component_sets.append(f"{master}: {structure.component_label}")
        fixed_command = (
            f"make contour-decision-update GLYPH={item.source_name} STATUS=fixed "
            'DECISION="component source edited and proof reviewed" REVIEWED="Name YYYY-MM-DD"'
        )
        accepted_command = (
            f"make contour-decision-update GLYPH={item.source_name} STATUS=accepted "
            'DECISION="component composition reviewed in proof" REVIEWED="Name YYYY-MM-DD"'
        )
        lines.append(
            "| {} | `{}` | {} | `{}` actual {}; expected {} | `{}` | `{}` | `{}` |".format(
                index,
                item.source_name,
                "<br>".join(component_sets) if component_sets else "missing",
                item.glyph_name,
                ", ".join(item.actual_values),
                ", ".join(item.expected_values),
                f"/edit-glyph {item.source_name} --master both",
                fixed_command,
                accepted_command,
            )
        )

    if not fix_items:
        lines.append("|  | none |  |  |  |  | No component-only `fix-now` rows remain. |")

    lines.extend(
        [
            "",
            "## Review Checklist",
            "",
            "- The composed glyph is not blank, clipped, duplicated, or mapped to the wrong form.",
            "- Dot position remains clear in Bold and the variable font.",
            "- Join shape matches the related sad/dad/tah/zah source forms.",
            "- If components are decomposed, do it in both masters and preserve interpolation compatibility.",
            "- If no edit is needed, record `accepted` with a proof-specific note instead of leaving it `fix-now`.",
            "",
            "## Regenerate After This Batch",
            "",
            "```bash",
            "make contour-cleanup-proof",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_edit_plan(findings: list[Finding]) -> str:
    items = sorted(
        review_items(findings),
        key=lambda item: (
            EDIT_PRIORITY.get(item.category, 99),
            len(item.font_names) * -1,
            item.source_name,
        ),
    )
    structures = source_glyph_structures()
    lines = [
        "# Contour Cleanup Edit Plan",
        "",
        "This generated checklist converts Fontspector production glyph names into",
        "source glyph names for the manual drawing pass. Work from this file when",
        "opening glyphs in Runebender or with the local `/edit-glyph` helper, then",
        "compare against `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html` before changing",
        "contour structure.",
        "For the shortest active edit queue, use",
        "`documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md`.",
        "For the first component-only drawing session, use",
        "`documentation/glyph-review/contour-cleanup/contour-cleanup-first-edit-batch.md`.",
        "",
        "Do not add or remove contours only to satisfy Fontspector. Edit both",
        "masters deliberately, preserve interpolation compatibility, and rerun",
        "`make contour-cleanup-proof` plus `make preflight-only` after each small",
        "batch.",
        "",
        "Source structure uses `c` = source contours, `p` = source points, and",
        "`comp` = source components. `Compatible` means Regular and Bold have",
        "matching counts before editing; it is a quick triage signal, not a",
        "substitute for `documentation/source/master-compatibility.md`.",
        "",
        f"- Unique source glyphs: {len({item.source_name for item in items})}",
        f"- Unique Fontspector glyph items: {len(items)}",
        f"- All-font finding rows: {len(findings)}",
        "",
        "## Source Glyph Command Queue",
        "",
        "| Order | Priority | Source glyph | Fontspector glyph | Category | Source structure | Compatible | Fonts | Command | Review cue |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, item in enumerate(items, start=1):
        command = f"/edit-glyph {item.source_name} --master both"
        lines.append(
            "| {} | {} | `{}` | `{}` | {} | {} | {} | {} | `{}` | {} |".format(
                index,
                edit_plan_priority(item.category),
                item.source_name,
                item.glyph_name,
                item.category,
                source_structure_label(item.source_name, structures),
                source_structure_compatible(item.source_name, structures),
                "<br>".join(f"`{font_name}`" for font_name in item.font_names),
                command,
                recommended_action(item.category),
            )
        )

    lines.extend(
        [
            "",
            "## Batch Commands",
            "",
            "After each group of related edits:",
            "",
            "```bash",
            "make contour-cleanup-proof",
            "make preflight-only",
            "```",
            "",
            "After shaping-sensitive Arabic edits:",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_markdown_queue(findings: list[Finding], reference_path: Path | None) -> str:
    items = review_items(findings)
    counts = category_counts(items)
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    reference_label = display_path(reference_path) if reference and reference_path else "none"
    lines = [
        "# Contour Cleanup Review Queue",
        "",
        "This generated queue deduplicates `documentation/google-fonts/fontspector-contour-count.md`",
        "so manual drawing cleanup can work through unique glyph decisions before",
        "checking repeated built-font rows in `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`.",
        "",
        f"- Unique glyph review items: {len(items)}",
        f"- All-font finding rows: {len(findings)}",
        f"- Reference font: `{reference_label}`",
        "",
        "## Category Counts",
        "",
        "| Category | Unique glyphs |",
        "| --- | ---: |",
    ]
    for category, count in sorted(counts.items()):
        lines.append(f"| {category} | {count} |")

    lines.extend(
        [
            "",
            "## Queue",
            "",
            "| Glyph | Source glyph | Codepoint | Category | Fonts | Actual | Expected | Reference | Recommended action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in items:
        ref_status = reference_status(reference, item)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.glyph_name}`",
                    f"`{item.source_name}`",
                    item.codepoint_label,
                    item.category,
                    "<br>".join(f"`{font_name}`" for font_name in item.font_names),
                    ", ".join(item.actual_values),
                    ", ".join(item.expected_values),
                    ref_status,
                    recommended_action(item.category),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def build_html(findings: list[Finding], reference_path: Path | None) -> str:
    renderers = {finding.font_path: FontRenderer(finding.font_path) for finding in findings}
    reference = FontRenderer(reference_path) if reference_path and reference_path.exists() else None
    reference_label = display_path(reference_path) if reference and reference_path else "none"
    items = review_items(findings)
    source_names = source_name_map()
    counts = category_counts(items)

    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Virtua Grotesk Contour Cleanup Proof</title>",
        "<style>",
        "body{font:14px/1.45 system-ui,-apple-system,BlinkMacSystemFont,sans-serif;margin:32px;background:#f7f7f4;color:#1f1f1f}",
        "h1{font-size:28px;margin:0 0 8px} h2{margin-top:36px;font-size:20px}",
        ".meta{color:#666;margin-bottom:24px}.summary{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 28px}.pill{background:#fff;border:1px solid #d8d8d2;border-radius:999px;padding:5px 10px}",
        ".queue{width:100%;border-collapse:collapse;margin:12px 0 36px;background:#fff}.queue th,.queue td{border:1px solid #d8d8d2;padding:8px;text-align:left;vertical-align:top}.queue th{background:#ecece7}",
        ".grid{display:grid;grid-template-columns:180px 1fr 1fr 110px 130px;gap:1px;background:#d8d8d2;border:1px solid #d8d8d2}",
        ".cell{background:#fff;padding:10px;min-height:92px}.head{font-weight:700;background:#ecece7;min-height:auto}",
        ".glyph-name{font-weight:700}.sub{color:#666;font-size:12px}.missing{color:#999;padding:30px 0;text-align:center}",
        "svg{width:100%;height:132px;background:#fbfbf8}path{fill:#111}.metric{stroke:#e26b5f;stroke-width:1}.sidebearing{stroke:#76a9e0;stroke-width:1;stroke-dasharray:8 8}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Virtua Grotesk Contour Cleanup Proof</h1>",
        f'<p class="meta">Generated from <code>{escape(str(DEFAULT_REPORT.relative_to(ROOT)))}</code>. Reference: <code>{escape(reference_label)}</code>. Red line is baseline; blue lines are origin and advance width.</p>',
        '<div class="summary">',
        f'<span class="pill">{len(items)} unique glyph review items</span>',
        f'<span class="pill">{len(findings)} all-font rows</span>',
    ]
    for category, count in sorted(counts.items()):
        lines.append(f'<span class="pill">{escape(category)}: {count}</span>')
    lines.extend(
        [
            "</div>",
            "<h2>Unique Review Queue</h2>",
            '<table class="queue">',
            "<thead><tr><th>Glyph</th><th>Source glyph</th><th>Category</th><th>Fonts</th><th>Actual</th><th>Expected</th><th>Reference</th></tr></thead>",
            "<tbody>",
        ]
    )
    for item in items:
        ref_status = reference_status(reference, item)
        lines.extend(
            [
                "<tr>",
                f'<td><strong>{escape(item.glyph_name)}</strong><br><span class="sub">{escape(item.codepoint_label)}</span></td>',
                f"<td>{escape(item.source_name)}</td>",
                f"<td>{escape(item.category)}</td>",
                f"<td>{escape(', '.join(item.font_names))}</td>",
                f"<td>{escape(', '.join(item.actual_values))}</td>",
                f"<td>{escape(', '.join(item.expected_values))}</td>",
                f"<td>{ref_status}</td>",
                "</tr>",
            ]
        )
    lines.extend(["</tbody>", "</table>"])

    for font_name, rows in grouped_findings(findings).items():
        lines.extend(
            [
                f"<h2>{escape(font_name)}</h2>",
                '<div class="grid">',
                '<div class="cell head">Finding</div>',
                '<div class="cell head">Virtua glyph</div>',
                '<div class="cell head">Rubik reference</div>',
                '<div class="cell head">Actual</div>',
                '<div class="cell head">Expected</div>',
            ]
        )
        for finding in rows:
            renderer = renderers[finding.font_path]
            item = ReviewItem(
                glyph_name=finding.glyph_name,
                source_name=source_name_for_finding(finding, source_names),
                codepoint_label=finding.codepoint_label,
                actual_values=(finding.actual,),
                expected_values=(finding.expected,),
                font_names=(finding.font_path.name,),
                category=finding_category(finding.glyph_name, finding.codepoint_label),
                sample=finding,
            )
            ref_glyph = reference_glyph_for_item(reference, item)
            reference_svg = reference.svg_for_glyph(ref_glyph) if reference else '<div class="missing">no reference</div>'
            lines.extend(
                [
                    '<div class="cell">',
                    f'<div class="glyph-name">{escape(finding.glyph_name)}</div>',
                    f'<div class="sub">source: {escape(source_name_for_finding(finding, source_names))}</div>',
                    f'<div class="sub">{escape(finding.codepoint_label)}</div>',
                    "</div>",
                    f'<div class="cell">{renderer.svg_for_glyph(finding.glyph_name)}</div>',
                    f'<div class="cell">{reference_svg}</div>',
                    f'<div class="cell">{escape(finding.actual)}</div>',
                    f'<div class="cell">{escape(finding.expected)}</div>',
                ]
            )
        lines.append("</div>")

    lines.extend(["</body>", "</html>", ""])
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    report_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_REPORT
    output_path = Path(argv[2]) if len(argv) > 2 else DEFAULT_OUTPUT
    queue_output_path = DEFAULT_QUEUE_OUTPUT if output_path == DEFAULT_OUTPUT else output_path.with_suffix(".md")
    edit_plan_output_path = (
        DEFAULT_EDIT_PLAN_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-edit-plan.md")
    )
    brief_output_path = (
        DEFAULT_BRIEF_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-drawing-briefs.md")
    )
    batch_output_path = (
        DEFAULT_BATCH_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-batches.md")
    )
    decision_output_path = (
        DEFAULT_DECISION_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-decision-log.md")
    )
    triage_output_path = (
        DEFAULT_TRIAGE_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-ai-triage.md")
    )
    source_edit_output_path = (
        DEFAULT_SOURCE_EDIT_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-source-edit-runlist.md")
    )
    first_batch_output_path = (
        DEFAULT_FIRST_BATCH_OUTPUT
        if output_path == DEFAULT_OUTPUT
        else output_path.with_name(f"{output_path.stem}-first-edit-batch.md")
    )
    findings = parse_findings(report_path)
    rubik_reference = reference_path()
    output_path.write_text(build_html(findings, rubik_reference))
    queue_output_path.write_text(build_markdown_queue(findings, rubik_reference))
    edit_plan_output_path.write_text(build_edit_plan(findings))
    brief_output_path.write_text(build_cleanup_briefs(findings, rubik_reference))
    batch_output_path.write_text(build_batch_plan(findings, rubik_reference))
    decision_output_path.write_text(build_decision_log(findings, rubik_reference, decision_output_path))
    triage_output_path.write_text(build_ai_triage(findings, rubik_reference))
    source_edit_output_path.write_text(build_source_edit_runlist(findings, rubik_reference, decision_output_path))
    first_batch_output_path.write_text(build_first_edit_batch(findings, rubik_reference, decision_output_path))
    print(
        f"Wrote {display_path(output_path)}, "
        f"{display_path(queue_output_path)}, "
        f"{display_path(edit_plan_output_path)}, and "
        f"{display_path(brief_output_path)}, and "
        f"{display_path(batch_output_path)}, and "
        f"{display_path(decision_output_path)}, and "
        f"{display_path(triage_output_path)}, and "
        f"{display_path(source_edit_output_path)}, and "
        f"{display_path(first_batch_output_path)} with {len(findings)} findings."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
