# Contour Cleanup First Edit Batch

This generated packet isolates the first recommended hand-edit session:
component-only Arabic source forms. These are good first targets because
the source glyphs are component compositions in both masters, so the first
decision is whether the composed output is intentional or whether the form
should be decomposed/redrawn deliberately in both masters.

Do not edit these only to satisfy Fontspector. Compare the built proof,
the component bases, and the surrounding Arabic letterforms before making
source changes.

- Source edit runlist: `documentation/contour-cleanup-source-edit-runlist.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Next review page: `documentation/arabic-next-review-batch.html`
- First-batch fix-now glyphs: 0

## Work Order

| Order | Source glyph | Component bases | Built contour warning | Open command | If edited, mark fixed | If intentional, mark accepted |
| ---: | --- | --- | --- | --- | --- | --- |
|  | none |  |  |  |  | No component-only `fix-now` rows remain. |

## Review Checklist

- The composed glyph is not blank, clipped, duplicated, or mapped to the wrong form.
- Dot position remains clear in Bold and the variable font.
- Join shape matches the related sad/dad/tah/zah source forms.
- If components are decomposed, do it in both masters and preserve interpolation compatibility.
- If no edit is needed, record `accepted` with a proof-specific note instead of leaving it `fix-now`.

## Regenerate After This Batch

```bash
make contour-cleanup-proof
make reports-only
make preflight-only
```
