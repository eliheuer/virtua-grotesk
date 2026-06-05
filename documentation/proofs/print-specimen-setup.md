# Print Specimen Setup

This repo now has a landscape PDF specimen dedicated to paper review of
weight, spacing, texture, numerals, punctuation, and Arabic rhythm.

## Command

```bash
make print-spacing-specimen
```

Outputs:

- `documentation/proofs/print-spacing-specimen.pdf`
- `documentation/proofs/print-spacing-specimen-index.md`

## Format

- Landscape US Letter: 792 x 612 pt.
- Static review weights: Regular, Medium, SemiBold, Bold.
- Built with the local `eliheuer/drawbot-skia` runtime, matching the other
  repo-local DrawBot proof commands.
- The Makefile uses this repo's virtualenv by default:
  `./.venv/bin/python`.
- Set `DRAWBOT_SKIA_REPO=/path/to/drawbot-skia` or use ignored `local.mk`
  when proofing directly from a checked-out fork.

## Review Coverage

- weight-axis overview with the same string across all weights;
- Latin waterfalls at multiple text sizes;
- paragraph texture in all weights;
- numeral, punctuation, and mixed numeric contexts;
- Arabic shaping, marks, numerals, punctuation, and Persian/Urdu letters;
- generated lowercase and uppercase spacing strings;
- compact encoded glyph grid for print scanning.

## Review Rules

- Print at 100% scale in landscape mode; avoid fit-to-page scaling when judging
  spacing and weight.
- Use the PDF as a fast paper review aid, then verify any suspected issue in
  the source UFOs and Google Fonts HTML proof before recording final status.
- Regenerate after drawing, spacing, kerning, metrics, or build changes.

## Research Notes

- DrawBot is designed for scripted, repeatable graphic documents and supports
  PDF/image output, which makes it appropriate for reproducible font proofs.
- RoboFont's DrawBot proof examples use generated spacing strings and alphabet
  groups to make sidebearing problems visible quickly.
- Older local OFL specimen scripts in `mekorot` used landscape pages for weight
  axis review; this specimen keeps that orientation and expands it into a
  multi-page print proof for Virtua.
