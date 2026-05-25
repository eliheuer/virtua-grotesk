# Contour Cleanup Edit Plan

This generated checklist converts Fontspector production glyph names into
source glyph names for the manual drawing pass. Work from this file when
opening glyphs in Runebender or with the local `/edit-glyph` helper, then
compare against `documentation/contour-cleanup-proof.html` before changing
contour structure.
For the shortest active edit queue, use
`documentation/contour-cleanup-source-edit-runlist.md`.
For the first component-only drawing session, use
`documentation/contour-cleanup-first-edit-batch.md`.

Do not add or remove contours only to satisfy Fontspector. Edit both
masters deliberately, preserve interpolation compatibility, and rerun
`make contour-cleanup-proof` plus `make preflight-only` after each small
batch.

Source structure uses `c` = source contours, `p` = source points, and
`comp` = source components. `Compatible` means Regular and Bold have
matching counts before editing; it is a quick triage signal, not a
substitute for `documentation/master-compatibility.md`.

- Unique source glyphs: 0
- Unique Fontspector glyph items: 0
- All-font finding rows: 0

## Source Glyph Command Queue

| Order | Priority | Source glyph | Fontspector glyph | Category | Source structure | Compatible | Fonts | Command | Review cue |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Batch Commands

After each group of related edits:

```bash
make contour-cleanup-proof
make preflight-only
```

After shaping-sensitive Arabic edits:

```bash
make reports-only
make preflight-only
```
