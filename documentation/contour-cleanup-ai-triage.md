# Contour Cleanup AI Triage

This generated sheet is an AI-assisted starting point for the manual
contour/no-contour review. It does not mark anything accepted, fixed,
or deferred. Use it to choose a review lane, then inspect the proof and
record the human decision in `documentation/contour-cleanup-decision-log.md`.

- Source report: `documentation/fontspector-contour-count.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Decision log: `documentation/contour-cleanup-decision-log.md`
- Triage items: 4

## Lane Counts

| Lane | Items |
| --- | ---: |
| component-source-review | 1 |
| source-outline-review | 3 |

## Review Table

| Source glyph | Fontspector glyph | Triage lane | Risk | Batch | Rubik reference | Why this lane | Next review step | Decision command patterns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dad-ar.init` | `uni0636.init` | component-source-review | medium | 1. Component-only source forms | no | Inspect the composed output first; the source has components only, so the contour count may be a build-time decomposition artifact. | Accept only if joins and dots look intentional in the proof; otherwise redraw or decompose both masters deliberately. | `make contour-decision-update GLYPH=dad-ar.init STATUS=fix-now DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"`<br>`make contour-decision-update GLYPH=dad-ar.init STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"` |
| `hah-ar.fina` | `uni062D.fina` | source-outline-review | medium | 6. Source-outline judgment calls | no | Inspect source and proof together before changing contours. | Fix only when the rendered glyph is actually wrong; otherwise record the reviewed decision. | `make contour-decision-update GLYPH=hah-ar.fina STATUS=fix-now DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"`<br>`make contour-decision-update GLYPH=hah-ar.fina STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"` |
| `jeem-ar.fina` | `uni062C.fina` | source-outline-review | medium | 6. Source-outline judgment calls | no | Inspect source and proof together before changing contours. | Fix only when the rendered glyph is actually wrong; otherwise record the reviewed decision. | `make contour-decision-update GLYPH=jeem-ar.fina STATUS=fix-now DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"`<br>`make contour-decision-update GLYPH=jeem-ar.fina STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"` |
| `sad-ar.init` | `uni0635.init` | source-outline-review | medium | 6. Source-outline judgment calls | no | Inspect source and proof together before changing contours. | Fix only when the rendered glyph is actually wrong; otherwise record the reviewed decision. | `make contour-decision-update GLYPH=sad-ar.init STATUS=fix-now DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"`<br>`make contour-decision-update GLYPH=sad-ar.init STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"` |

## How To Use

1. Open `documentation/contour-cleanup-proof.html` and the matching glyph in Runebender.
2. Use the triage lane to decide whether to inspect components, mark placement, dot collisions, letterform structure, or punctuation rhythm first.
3. If the glyph needs source edits, use the `fix-now` command pattern and edit both masters.
4. If the glyph is visually intentional, use the `accepted` command pattern with a specific proof note.
5. If native-reader review is needed, record `STATUS=deferred` with the reviewed evidence.
