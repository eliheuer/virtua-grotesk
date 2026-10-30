---
name: draw-outline
description: Draw or redraw a glyph outline from scratch in both UFO masters, following Virtua Grotesk vector conventions (16-unit chamfers, master compatibility). Use when adding a new glyph or redrawing an existing one.
---

# Draw or redraw an outline

Read [the design workflow](../../../design/README.md). Retrieve scoped context with
`.venv/bin/python scripts/design_context.py --glyph <name> --operation draw`;
repeat --glyph for a bounded group. Save a JSON packet before edits and verify it
immediately before applying. Read selected evidence, not the entire review archive.
Current scope and stopped work come from `design/reviews/current.json` and the user.

For a redraw select --operation redraw. Name glyphs/masters and purpose, reuse
approved scope, preserve baseline bytes, and inspect the selected source pairs.
Green Virtua geometry governs construction across scripts. External fonts inform
script structure and comparisons; they do not supply Virtua's curve recipe.

1. Identify whole-glyph silhouette, strokes/counters, bounded turns, terminals,
   intended corners and fixed weight alignments before placing points.
2. Reuse actual green donor geometry where applicable. Read the applicable
   [construction](../../../design/constructions/README.md) and glyph contract.
   Exact historical dimensions and unequal/equal handles are local evidence.
3. Place new on/off-curve points, anchors and metrics on the 8-unit draft grid;
   preserve inherited human optics. Target economical cubic structure with useful
   extrema and intentional tangent continuations. Preserve short cuts/landings.
4. Keep both masters compatible in contour order, point count/type and components.
   Do not independently reorder shared contours. Register new glyphs in GLIF,
   contents.plist and public.glyphOrder. Use surgical XML, never whole-UFO saves.
5. Run the named draft grid check, compatibility --check, curve_lint --joins and
   signed curve_profile where relevant. Build, inspect intermediates and shaped
   reading-size/large proofs under [verification](../../../design/system/verification.md).
6. Record exact correction pairs and human verdicts; use purple for new AI drawing,
   never green. A numerical pass does not accept the silhouette.

For bowl letters use bowl-from-o. For a user image, follow anchor-sheet-glyphs
or harness/RUNBOOK-codex.md; do not replace tracing with hand approximation.
