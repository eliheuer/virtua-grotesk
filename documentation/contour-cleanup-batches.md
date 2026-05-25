# Contour Cleanup Batches

This generated batch sheet turns the remaining Fontspector contour-count
warnings into short hand-edit sessions. It is designed for Runebender
cleanup plus AI comparison notes. Rubik is a structural reference only;
do not copy outlines from it into Virtua Grotesk.

- Source report: `documentation/fontspector-contour-count.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Source edit runlist: `documentation/contour-cleanup-source-edit-runlist.md`
- First edit batch: `documentation/contour-cleanup-first-edit-batch.md`
- Detailed prompt cards: `documentation/arabic-cleanup-drawing-briefs.md`
- Unique review items: 0
- All-font finding rows: 0

## Recommended Session Order

1. Component-only source forms: decide whether the component structure is
   intentional or should be decomposed/redrawn in both masters.
2. Referenced Arabic marks and ligatures: use Rubik only to understand
   expected structure and mark stacking behavior.
3. Dot-stack helpers: check Bold collisions and readability first.
4. Arabic letterform review: judge skeleton, joins, counters, and chamfers.
5. Shared punctuation: keep Latin and Arabic text behavior aligned.
6. Source-outline judgment calls: accept, defer, or redraw deliberately.

After each batch:

```bash
make contour-cleanup-proof
make preflight-only
```
