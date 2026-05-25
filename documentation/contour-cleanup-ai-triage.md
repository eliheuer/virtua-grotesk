# Contour Cleanup AI Triage

This generated sheet is an AI-assisted starting point for the manual
contour/no-contour review. It does not mark anything accepted, fixed,
or deferred. Use it to choose a review lane, then inspect the proof and
record the human decision in `documentation/contour-cleanup-decision-log.md`.

- Source report: `documentation/fontspector-contour-count.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Decision log: `documentation/contour-cleanup-decision-log.md`
- Triage items: 0

## Lane Counts

| Lane | Items |
| --- | ---: |

## Review Table

| Source glyph | Fontspector glyph | Triage lane | Risk | Batch | Rubik reference | Why this lane | Next review step | Decision command patterns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## How To Use

1. Open `documentation/contour-cleanup-proof.html` and the matching glyph in Runebender.
2. Use the triage lane to decide whether to inspect components, mark placement, dot collisions, letterform structure, or punctuation rhythm first.
3. If the glyph needs source edits, use the `fix-now` command pattern and edit both masters.
4. If the glyph is visually intentional, use the `accepted` command pattern with a specific proof note.
5. If native-reader review is needed, record `STATUS=deferred` with the reviewed evidence.
