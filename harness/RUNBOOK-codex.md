# Organic image to glyph

Start with [design context](../design/README.md) and the glyph-ai-harness skill.
Use anchor-sheet-glyphs when a sheet supplies calibration. Images are for an
explicit image-generation/tracing task; existing source geometry is the preferred
construction evidence for source edits. Never replace a requested trace with a
hand-drawn approximation.

## Prepare

Name glyphs/masters and retain authorization, baseline sources and supplied image
provenance. Read the current case and selected corrections. Inspect actual green
Virtua donors, including their current hashes and component geometry. Compare
external references for script structure only.

`harness/designbot/glyph_canvas.rs` is the canonical source-render canvas. Use
scripts/glyph_ai_harness.py render for current source renders. Existing canvas
options can be inspected through the script/CLI; preserve a shared baseline and
em scale. A canvas's full height is not the glyph's calibrated ink extent.

```sh
make glyph-ai-inventory
make glyph-ai-prepare TARGET=<glyph> REFERENCES="n,o" FIT=<bottom:top>
```

FIT is required: derive bottom/top from the calibrated image and intended source
metrics (e.g. baseline:xheight only when that is the actual ink band). Preparation
requires a fresh run directory, both masters and verified green references. It
saves context.md, context.json, rendered references, per-master prompts and the
manifest. Read them before generating. Specify --out on the Python CLI for a fresh
revision; never overwrite a previous proof packet.

## Generate and trace

Use the selected image tool with the reference renders and scoped context.
Inspect the returned artwork and tune/regenerate poor forms before tracing. Save
one image per master at generated/regular/<glyph>.png and generated/bold/<glyph>.png.

```sh
.venv/bin/python scripts/glyph_ai_harness.py trace --run-dir .glyph-ai-runs/<glyph>
```

The harness rechecks input hashes, copies both UFOs/designspace into a new scratch
trace directory and runs img2bez masters. It refuses legacy packets and existing
trace directories. It requires compatible=true, lowConfidence=false and strict
source compatibility. Inspect the report's bounds, fit, advance, point counts,
profile and warnings. Compatible topology can still be a bad drawing. Tune and
retrace poor results into a fresh revision. IMG2BEZ_LOG may retain trace history.

## Refit and review

Preserve the supplied form, broad path and counter rhythm. Apply the selected
construction contract, 8-unit draft lattice and deliberate 16/8-unit cuts. Preserve
human corrections; do not optimize every measurement to a low popcount. Check
whole-glyph silhouette, opposing-edge weight, then joins and curvature. A smooth
local join does not repair a lumpy overall path. Use the selected correction pairs
and signed curve_profile with shared scale.

Run draft_grid_check on named scratch glyphs, strict master compatibility, curve
checks and a build. Inspect endpoint/intermediate compiled shaping, actual large
and reading-size proofs, marks and joins. Arabic also needs the raster gate in
[verification](../design/system/verification.md). Record actual observations.

Port only within named active-application authorization, after rechecking guards
and source colors. Edit only relevant GLIF/plist entries in repository style;
never save a whole active UFO. Preserve component donors, anchors, metrics and
other work. Label new AI drawing purple, never green. Capture exact feedback,
source pairs, proof hashes and approval/application state in design/reviews;
index reusable lessons in design/corrections. A check pass is not human approval.
