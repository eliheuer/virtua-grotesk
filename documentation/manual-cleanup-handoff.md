# Manual Cleanup Handoff

Use this page as the pause/resume checkpoint while the source drawings are
being cleaned up by hand.

## Current Focus

- Finish the source drawings in both masters.
- Keep Regular and Bold structurally compatible for every glyph.
- Preserve the 1024 UPM, 2-unit grid, and 16-unit chamfer design logic.
- Review Latin, Hebrew, Arabic, figures, punctuation, marks, and symbols as one
  design system instead of treating non-Latin scripts as add-ons.
- Rebuild and proof after drawing, spacing, kerning, or metrics changes.

## Resume Commands

```bash
make build
make proof
make specimen
make reports
make preflight
```

Before a Google Fonts submission pass, also run:

```bash
make test
```

## Active Review Files

- `documentation/core-qa-process.md`
- `documentation/source-guides/design-philosophy.md`
- `documentation/source-guides/ufo-editing.md`
- `documentation/source/master-compatibility.md`
- `documentation/source/source-ufo-metadata.md`
- `documentation/source/generated-font-metadata.md`
- `documentation/proofs/proof.pdf`
- `documentation/proofs/print-spacing-specimen.pdf`

Older generated Arabic and Google Fonts reports were archived under
`documentation/archive/agent-generated-reports/` so they do not read as active
instructions.
