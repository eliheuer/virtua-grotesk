---
name: edit-glyph
description: Read, display, and edit a glyph in the UFO sources. Use for inspecting or modifying an existing glyph's outline, advance width, or sidebearings.
---

# Edit a glyph

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation inspect`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

Use the operation matching the requested edit (spacing, components, curve-repair,
weight-transfer, etc.). Default inspection covers both masters. Resolve filenames
through each contents.plist; never guess GLIF filenames.

1. Inspect exact sources and component dependencies. For ink bounds/sidebearings,
   use a curve-aware bounds pen with components resolved; control-point extrema
   are not ink bounds. Inspect the filled glyph before diagnosing optics.
2. Reuse named authorization. Preserve before bytes and make a reversible candidate
   unless active edits are already authorized. Keep application and approval separate.
3. Edit XML/plists surgically. For LSB shifts, include contours, component offsets
   and anchors as appropriate; changing width alone changes RSB. Check consumers.
4. Match structural changes across masters. Use the selected construction contract,
   live green geometry and exceptions, not a coordinate scale or generic curve recipe.
5. Follow [verification](../../../design/system/verification.md), inspect compiled
   forms, record feedback in the case, and index reusable correction evidence.

For new outlines use draw-outline; for an image use anchor-sheet-glyphs or the
organic-image runbook. Do not substitute an imagined outline for the requested trace.
