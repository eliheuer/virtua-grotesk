# Arabic Source Work Checklist

This generated checklist translates the current `GF_Arabic_Core` cmap gaps into source-glyph work across both active UFO masters. It is a production aid for drawing and compatibility work; the authoritative coverage target remains the installed `glyphsets` definition, and visual Arabic review is still required.

## Summary

- Font checked: `fonts/variable/VirtuaGrotesk[wght].ttf`
- Minimum Arabic target: `GF_Arabic_Core`
- Missing required codepoints: 0
- Arabic-range missing codepoints: 0
- Shared punctuation/symbol missing codepoints: 0
- U+25CC dotted circle missing: no
- Suggested source glyph names: 0
- Suggested Arabic source glyph names: 0
- Suggested shared punctuation/symbol glyph names: 0
- Suggested Arabic default glyph names: 0
- Suggested Arabic positional-form glyph names: 0
- Suggested glyph names present in both masters: 0
- Suggested glyph names missing in both masters: 0
- Suggested glyph names partial across masters: 0
- Arabic reuse prerequisites checked: 0 codepoints
- Missing reuse prerequisites across masters: 0
- Active source masters checked: `sources/VirtuaGrotesk-Regular.ufo`, `sources/VirtuaGrotesk-Bold.ufo`

## Suggested Source Inventory

| Bucket | Count |
| --- | ---: |
| Total suggested source glyph names | 0 |
| Arabic suggested source glyph names | 0 |
| Shared punctuation/symbol suggested glyph names | 0 |
| Arabic default glyph names | 0 |
| Arabic positional-form glyph names | 0 |
| Suggested glyph names already present in both masters | 0 |
| Suggested glyph names missing in both masters | 0 |
| Suggested glyph names partial across masters | 0 |

## Source Rules

- Add every required encoded glyph to both active UFO masters.
- For joining Arabic letters, keep the same default/final/initial/medial glyph structure in both masters.
- Preserve master compatibility: same contour/component structure, point counts, and point types in Regular and Bold.
- Add dotted circle and mark anchors before final Arabic mark proofing.
- Rerun `make preflight` after each source batch.

## Missing Codepoint Worklist

| Codepoint | Unicode name | Type | Suggested source glyphs | Built cmap glyph | Regular source | Bold source | Reuse note |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Reuse Prerequisite Audit

These rows check whether suggested Arabic source reuse bases already exist in both active masters. They do not replace drawing review; they only verify that the referenced skeleton or dot helper names are available before new glyphs are built.

| Codepoint | Target glyphs | Reuse prerequisites | Regular prerequisites | Bold prerequisites |
| --- | --- | --- | --- | --- |

## Batch Work Plan

These batches group the same `GF_Arabic_Core` gaps by production
dependency so drawing work can move in source-compatible passes.
The per-codepoint table above remains the source of truth for
which encoded characters are still missing.

| Order | Batch | Codepoints | Source glyph names | Notes |
| ---: | --- | ---: | ---: | --- |

## Batch Glyph Lists

## Batch Order Suggestion

1. Shared punctuation and symbols that are also needed by Latin Core.
2. Extended Arabic-Indic digits U+06F0-U+06F9.
3. Urdu/Persian joining letters and their positional forms.
4. Missing Arabic marks plus U+25CC dotted circle.
5. Source anchors and built `mark`/`mkmk` features.
