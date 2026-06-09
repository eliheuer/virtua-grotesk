# Contour Cleanup Source Edit Runlist

This generated runlist is the shortest path from the current contour-count
warnings to source edits. It includes only rows currently marked
`fix-now` in `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`.

Do not copy outlines from Rubik or any other reference. Use references only
for structural comparison, then edit both Virtua masters deliberately.

- Source report: `documentation/google-fonts/fontspector-contour-count.md`
- Decision log: `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`
- Visual proof: `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`
- Drawing briefs: `documentation/glyph-review/arabic-cleanup-drawing-briefs.md`
- Fix-now source glyphs: 0

## Edit Loop

For each glyph:

1. Open the Regular and Bold sources with the listed `/edit-glyph` command.
2. Compare the built glyph in `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html`.
3. Edit both masters if the proof shows a real drawing issue.
4. Preserve matching contour, point, and component structure across masters.
5. Mark the row `fixed`, `accepted`, or `deferred` with proof notes.

After a small batch:

```bash
make contour-cleanup-proof
make reports-only
make preflight-only
```

## Fix-Now Queue

| Order | Source glyph | Batch | Current structure | Rubik reference | Open command | Mark fixed command | Review cue |
| ---: | --- | --- | --- | --- | --- | --- | --- |
|  | none |  |  |  |  |  | No `fix-now` contour rows remain. |

## Defer Or Accept Commands

Use these only after proof review shows the glyph should not be edited now:

```bash
make contour-decision-update GLYPH=<source> STATUS=accepted DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"
make contour-decision-update GLYPH=<source> STATUS=deferred DECISION="needs Arabic native-reader review" REVIEWED="Name YYYY-MM-DD"
```
