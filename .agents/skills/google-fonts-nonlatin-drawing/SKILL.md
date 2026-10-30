---
name: google-fonts-nonlatin-drawing
description: Finish missing non-Latin (e.g. Arabic) drawings for a Google Fonts submission while keeping masters compatible and script shaping intact.
---

# Non-Latin drawing for Google Fonts

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation draw`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Use the onboarding checklist for release scope, then the applicable Arabic/Hebrew
context and current case. A coverage gap is not permission to redraw every glyph.
Inventory missing forms, source colors, recursive donors, anchors, substitutions
and joining/mark dependencies. Choose a bounded authorized group.

Use edit-glyph/draw-outline for source work and the image skills for supplied
artwork. Preserve human corrections and named intent; external script references
must not replace Virtua's construction. Keep both masters compatible.

Follow [design verification](../../../design/system/verification.md): build,
compiled shaping at endpoints/intermediates, large and reading-size comparisons,
marks/joining/bidi coverage and the Arabic raster proof gate. Retain exact before,
candidate/applied sources, font hashes and visible findings. Distinguish application,
human approval and release QA. Use google-fonts-qa for the latter.
