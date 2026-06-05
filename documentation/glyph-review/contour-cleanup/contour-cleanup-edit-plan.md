# Contour Cleanup Edit Plan

This generated checklist converts Fontspector production glyph names into
source glyph names for the manual drawing pass. Work from this file when
opening glyphs in Runebender or with the local `/edit-glyph` helper, then
compare against `documentation/glyph-review/contour-cleanup/contour-cleanup-proof.html` before changing
contour structure.
For the shortest active edit queue, use
`documentation/glyph-review/contour-cleanup/contour-cleanup-source-edit-runlist.md`.
For the first component-only drawing session, use
`documentation/glyph-review/contour-cleanup/contour-cleanup-first-edit-batch.md`.

Do not add or remove contours only to satisfy Fontspector. Edit both
masters deliberately, preserve interpolation compatibility, and rerun
`make contour-cleanup-proof` plus `make preflight-only` after each small
batch.

Source structure uses `c` = source contours, `p` = source points, and
`comp` = source components. `Compatible` means Regular and Bold have
matching counts before editing; it is a quick triage signal, not a
substitute for `documentation/source/master-compatibility.md`.

- Unique source glyphs: 4
- Unique Fontspector glyph items: 4
- All-font finding rows: 4

## Source Glyph Command Queue

| Order | Priority | Source glyph | Fontspector glyph | Category | Source structure | Compatible | Fonts | Command | Review cue |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P1 source-structure check | `dad-ar.init` | `uni0636.init` | source outline review | Regular: `c0/p0/comp2`<br>Bold: `c0/p0/comp2` | yes | `VirtuaGrotesk[wght].ttf` | `/edit-glyph dad-ar.init --master both` | Inspect source outline structure and compare the rendered proof before editing. |
| 2 | P1 source-structure check | `hah-ar.fina` | `uni062D.fina` | source outline review | Regular: `c3/p67/comp0`<br>Bold: `c3/p67/comp0` | yes | `VirtuaGrotesk[wght].ttf` | `/edit-glyph hah-ar.fina --master both` | Inspect source outline structure and compare the rendered proof before editing. |
| 3 | P1 source-structure check | `jeem-ar.fina` | `uni062C.fina` | source outline review | Regular: `c4/p83/comp0`<br>Bold: `c4/p83/comp0` | yes | `VirtuaGrotesk[wght].ttf` | `/edit-glyph jeem-ar.fina --master both` | Inspect source outline structure and compare the rendered proof before editing. |
| 4 | P1 source-structure check | `sad-ar.init` | `uni0635.init` | source outline review | Regular: `c1/p49/comp0`<br>Bold: `c1/p49/comp0` | yes | `VirtuaGrotesk[wght].ttf` | `/edit-glyph sad-ar.init --master both` | Inspect source outline structure and compare the rendered proof before editing. |

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
