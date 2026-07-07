# Glyph AI Harness Workflow

This document defines the intended AI-assisted glyph expansion workflow for
Virtua Grotesk. The target use case is a maintainer prompt such as:

> add the missing Hebrew to this font

The harness should turn that into a staged, inspectable pipeline: discover the
missing glyphs, render green reference glyphs, generate raster proposals with
OpenAI image generation, trace compatible masters with img2bez, place and space
the result, render specimens, then iterate until the new glyphs match the green
reference standard.

## Research Notes

- OpenAI's image generation guide documents two useful paths: the Images API
  and the Responses API image-generation tool. Both can use image inputs as
  references; the Images API `images.edit` endpoint accepts multiple input
  images for reference-driven generation.
- GPT Image outputs are base64 image data by default. For this harness, outputs
  should be saved as PNGs under `.glyph-ai-runs/<run>/generated/`.
- `gpt-image-2` supports reference-image workflows and high-fidelity image
  inputs, but does not support transparent backgrounds. The harness should ask
  for black glyph silhouettes on solid white backgrounds, not transparency.
- OpenAI vision models can inspect rendered proof/specimen images through the
  Responses API with `input_image` parts. This is useful for structured feedback
  about weight, baseline, spacing, and rhythm after a specimen is rendered.
- Upstream img2bez now documents a `masters` workflow for variable-font
  compatibility. The locally installed binary currently exposes only the older
  single-master CLI. Until the local tool is updated, generated traces must be
  treated as sketches unless compatibility is proven after tracing.

Sources:

- <https://developers.openai.com/api/docs/guides/image-generation>
- <https://developers.openai.com/api/docs/guides/images-vision>
- <https://developers.openai.com/api/reference/resources/images>
- <https://github.com/eliheuer/img2bez>

## Design Principles

1. Green glyphs are the design authority. A generated glyph is never considered
   good because the image looks plausible; it must match the structure, weight,
   spacing, and rhythm of green references.
2. Build everything in `.glyph-ai-runs/` first. Active UFO sources are
   touched only during a promotion step.
3. Multi-master compatibility is a hard gate. Same contour count, point count,
   point types, component structure, anchors, Unicode, and glyph presence are
   required before promotion.
4. OpenAI-generated rasters are sketches, not source drawings. They are useful
   for silhouette exploration and optical review, but the harness must be ready
   to redraw or regularize them.
5. Placement and spacing belong in the headless pipeline, not only in the UI.
   Runebender is the review surface, but agents need deterministic placement,
   sidebearing, and proof loops without manual UI operations.
6. Every decision must be inspectable: prompt, inputs, generated image, trace
   command, placement transform, compatibility report, specimen, and AI feedback
   should live in the run packet.

## Run Packet Layout

Each run should live under:

```text
.glyph-ai-runs/<run-id>/
```

Recommended structure:

```text
manifest.json
README.md
inventory.json
references/
  regular/*.png
  bold/*.png
target/
  glyphset.json
  per-glyph/*.json
prompts/
  regular/*.md
  bold/*.md
generated/
  regular/*.png
  bold/*.png
trace/
  regular/*.glif or *.ufo
  bold/*.glif or *.ufo
  master-compatibility.md
placement/
  proposals.json
  applied.json
specimens/
  proof-before.png
  proof-after.png
  mixed-string-regular.png
  mixed-string-bold.png
feedback/
  ai-review.json
  maintainer-notes.md
promotion/
  promoted-files.json
```

## Phase 1: Inventory And Reference Selection

Run:

```bash
make glyph-ai-inventory
```

The inventory should record:

- master UFO paths
- every glyph's Unicode, width, contour/component counts, and mark color
- green reference glyphs (`public.markColor` `0.09,0.72,0.44,1`)
- orange/red review queues
- missing target glyphs for the requested script or glyphset

For Hebrew, the first target scope should be explicit:

- basic Rubik-like Hebrew coverage, or
- full Google Fonts Hebrew subset coverage

The first automated pass should prefer a small batch of simple forms before a
full script expansion.

## Phase 2: Reference Rendering

Render green references from the active UFOs with drawbot-skia. For each master,
produce:

- individual glyph PNGs on a consistent white canvas
- reference sheets by category: straight stems, rounds, counters, joins,
  chamfers, marks, punctuation, script-specific forms
- metrics JSON: bounds, advance width, left/right sidebearings, stem widths,
  overshoot, baseline/cap/x-height relation

For missing Hebrew, include green Latin and Arabic references plus an external
script-shape reference such as Rubik. External references are for skeleton and
script logic, not direct copying.

## Phase 3: Prompt And Image Generation

Use OpenAI image generation through a repo script, not manual copy/paste, when
an API key is available. The script should support two modes:

1. `images.edit` with rendered green reference images as input images.
2. Responses API with the `image_generation` tool and the same reference images.

Required prompt constraints:

- one glyph only
- solid black silhouette on solid white background
- no labels, grid, shadows, texture, outlines, or extra marks
- match Virtua Grotesk weight, stroke logic, chamfer behavior, and proportions
- keep baseline, vertical scale, and sidebearings aligned to supplied metrics
- state target glyph name and Unicode
- state target master and intended advance width

The generated image must be saved into the run packet before tracing.

## Phase 4: Multi-Master Tracing

Preferred path once local img2bez is updated:

```bash
img2bez masters ...
```

The harness should use img2bez's multi-master workflow when available so the
trace can enforce interpolation-compatible structure at the point of creation.

Fallback path with the currently installed CLI:

```bash
img2bez --input generated/regular/<glyph>.png --output trace/Regular.ufo --name <glyph> ...
img2bez --input generated/bold/<glyph>.png --output trace/Bold.ufo --name <glyph> ...
python scripts/report_master_compatibility.py trace/Regular.ufo trace/Bold.ufo trace/master-compatibility.md
```

Fallback traces are not promotable until a structure reconciliation step makes
them compatible. If reconciliation cannot be made deterministic, use the trace
as a visual template and redraw compatible outlines.

For Virtua Grotesk, default trace metrics are:

```text
target-height: 1088
y-offset: -256
grid: 2
chamfer: 0 by default, opt into 16 only for intentionally line-based sharp forms
```

## Phase 5: Placement And Spacing

The harness should make placement/spacing proposals headlessly before Runebender
review. The proposal should be stored as JSON and include:

- glyph bbox
- target bbox from references
- scale factor
- x/y translation
- advance width
- left/right sidebearings
- baseline and overshoot relationship
- nearest green reference glyphs used for comparison

For a first implementation, use deterministic measurements:

- align script baseline to baseline
- align Hebrew letter height to the selected Hebrew reference height or to a
  chosen Virtua vertical band
- derive simple glyph sidebearings from related green glyph classes
- keep Regular/Bold advances compatible with existing axis spacing behavior

An AI vision review can then inspect a specimen image and return structured
adjustments, but those adjustments should be applied only after the deterministic
proposal is recorded.

## Phase 6: Specimen And AI Review

Render a specimen after tracing and placement. For script expansion, the
specimen must include:

- the target glyph repeated in long strings
- target glyphs mixed with green references
- target script words or pseudo-words
- Regular and Bold rows
- baseline guides and optional spacing marks

Use a vision-capable OpenAI model to inspect the specimen and return JSON:

```json
{
  "glyph": "vav-hb",
  "status": "adjust",
  "issues": [
    {"type": "weight", "severity": 2, "message": "too heavy next to yod-hb"},
    {"type": "spacing", "severity": 1, "message": "right sidebearing too tight"}
  ],
  "adjustments": {
    "scale_x": 0.98,
    "scale_y": 1.0,
    "translate_y": 0,
    "lsb_delta": 8,
    "rsb_delta": 12
  }
}
```

Treat this feedback as advisory. The harness should apply only bounded numeric
adjustments and rerun compatibility/build/specimen after each pass.

## Phase 7: Structure Matching And Cleanup

Before promotion, inspect the green glyphs structurally:

- point placement at extrema
- line vs curve decisions
- handle direction rules
- chamfer size and orientation
- component reuse patterns
- mark color semantics
- anchors and GDEF class membership

New glyphs should be edited to match those patterns. If img2bez produces too
many points, wrong extrema, rounded corners, incompatible contours, or poor
sidebearings, the correct action is to simplify/redraw, not to promote.

## Phase 8: Promotion Gate

Promote into `sources/` only after all of these are true:

- Regular and Bold structures are compatible
- Unicode assignments and glyph names are correct
- generated specimen looks acceptable
- source metadata reports are clean
- `make build` passes
- `make proof` passes
- relevant script shaping and text rendering smoke tests pass
- new glyphs are marked orange for review until the maintainer marks them green

Promotion should record the files changed in `promotion/promoted-files.json`.

## Implementation Gaps

The current harness already handles inventory, green reference rendering,
single-glyph prompt packets, single-master img2bez tracing into scratch UFOs,
and compatibility reporting.

Needed next:

1. Add script/glyphset planning: `glyph_ai_harness.py plan --script hebrew`.
2. Add OpenAI API generation: `glyph_ai_harness.py generate --run-dir ...`.
3. Add img2bez version detection and prefer `img2bez masters` when present.
4. Add deterministic placement/spacing proposals.
5. Add specimen rendering for mixed target/reference strings.
6. Add vision-based review that returns bounded JSON adjustments.
7. Add a promotion command that refuses to write sources when compatibility or
   build gates fail.

Until those are implemented, agents should follow this document manually and
keep all generated/traced output staged under `.glyph-ai-runs/`.
