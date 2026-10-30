# Virtua design context

This is the entry point for drawing in Virtua's style and grid. Start with a
named task. Fetch its applicable rules and exact correction evidence instead of
reading every past review. Source geometry and human decisions remain authoritative.

```sh
make design-status
make design-context GLYPH=seen-ar OPERATION=curve-repair
.venv/bin/python scripts/design_context.py --glyph seen-ar --master both \
  --operation curve-repair --json --output out/seen-context.json
# Immediately before applying an already authorized edit:
.venv/bin/python scripts/design_context.py --verify out/seen-context.json
make design-check
```

Operations: inspect, draw, redraw, curve-repair, weight-transfer, spacing,
kerning, anchors, components, from-image. Repeat `--glyph` for a bounded group.
The packet names why each record was selected, its scope and exceptions,
current source colors/hashes, component dependencies and affected green consumers.
Inspect referenced GLIFs and actual images; summaries cannot show curve quality.
Missing/unclassified references are reported rather than silently approved.

1. Inspect Git status, current review state and named authorization. Read the
   relevant skill. Choose exact targets and masters; keep OPEN choices open.
2. Generate context and a JSON guard packet. Read selected construction examples
   and counterexamples. Measure the current green donors in the applicable master.
   For curves, identify the broad path, opposing edges, turns and intended cuts.
For style/weight regressions, use the [construction review gate](constructions/review-gates.md) before another candidate. It makes preservation constraints inspectable; it does not grade artwork.

3. Preserve before sources and make a bounded candidate. Use the 8-unit draft grid
   without resnapping inherited human optics. Follow [source safety](system/source-safety.md).
4. Run [verification](system/verification.md), inspect the actual proofs, and record
   application separately from Eli's verdict. Recheck guards before active edits.
   A changed guard means reread the changed inputs and prepare new context; never
   just update stored hashes to silence a stale-context failure.
5. Save exact feedback, pairs, proof receipts and limitations in the current review.
   Index a reusable correction in [corrections](corrections/README.md). Update the
   appropriate canonical rule only when evidence supports it, retaining exceptions.

| Place | Owns |
| --- | --- |
| [system/](system/grid.md) | Shared design, grid, weight, safety, verification |
| [constructions/](constructions/README.md) | Reusable geometric relationships |
| [writing-systems/](writing-systems/README.md) | Script-specific shaping and conventions |
| [glyphs/](glyphs/README.md) | Named intent, exceptions and reference choices |
| [references/](references/README.md) | Reference roles; approved Virtua donors versus external script examples |
| [corrections/](corrections/README.md) | Indexed, scoped feedback and source-pair metadata |
| [reviews/](reviews/README.md) | Session history, immutable source/proof evidence, current state |
| [catalog.json](catalog.json) | Retrieval routes; no duplicated correction records |

`agent-proofs/` owns the comparison application. `.agents/skills/` owns procedures.
`documentation/` owns build/release/QA guides. Local external fonts remain in
`reference-fonts/`. Temporary context and experiments belong under `out/`.

The library does not train model weights or guarantee good drawings. It makes
relevant evidence discoverable and checks provenance. Start new glyph families
with a small reviewed trial and add retrieval coverage when a missing lesson is
found. [Migration notes](migration/README.md) explain compatibility and limitations.
