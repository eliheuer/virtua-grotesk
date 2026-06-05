# Arabic Visual Review Checklist

This hand-review checklist bridges the automated Arabic reports and the
Google Fonts proof HTML. It does not approve the drawings; it defines the
manual review pass needed after candidate generation.

## Current Automated State

- GF Arabic Core coverage: 224 / 224 present; 0 missing.
- Arabic source worklist: 0 suggested glyphs missing in either master.
- Master compatibility: 0 blocking structure mismatches.
- Required Arabic marks: 16 / 16 present.
- Dotted circle: present.
- Source anchors: present.
- Built `mark`/`mkmk`: present.
- Arabic shaping smoke: 5 / 5 fonts pass; no `.notdef` in smoke strings.
- Google Fonts QA proof files: 16 / 16 present in `documentation/google-fonts/gftools-qa/Proof`.
- Contour-count cleanup: 0 current review items; keep
  `documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md` as evidence, but do not
  spend review time on contour rows unless new source edits reintroduce them.
- Human visual review: 32 pending rows in
  `documentation/glyph-review/arabic-visual-review-log.md`.

## Proof Files To Open

Review these for every instance: Regular, Medium, SemiBold, and Bold.
Start with `documentation/glyph-review/arabic-manual-review-dashboard.html` for a compact
embedded-font pass over smoke strings, mark combinations, numerals,
punctuation, visual-risk rows, contour decision rows, and proof links.
For a print/PDF review aid, run `make arabic-print-proof` to regenerate
`documentation/glyph-review/arabic-print-proof.pdf`. The PDF uses the same local
`eliheuer/drawbot-skia` runtime as `make proof` and includes Arabic shaping,
mark, numeral, punctuation, and cmap-grid pages for Regular, Medium, SemiBold,
and Bold. Use `documentation/glyph-review/arabic-print-proof-index.md` as the page map when
working through the PDF. Treat both files as review aids; the Google Fonts HTML
proof remains the submission proof source.

| Proof type | Files | Arabic review focus |
| --- | --- | --- |
| Glyphs | `*-diffbrowsers_glyphs.html` | missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs |
| Text | `*-diffbrowsers_text.html` | RTL texture, fallback, unexpected Latin spacing influence, and mark collisions |
| Proofer | `*-diffbrowsers_proofer.html` | sidebearing rhythm, punctuation spacing, numeral rhythm, and weight-specific spacing |
| Waterfall | `*-diffbrowsers_waterfall.html` | size behavior, weight interpolation, and small-size mark clarity |

## Arabic Strings To Check

Use the shaping smoke strings as a minimum visual proof set:

| Label | Text | Expected behavior |
| --- | --- | --- |
| salaam | سلام | contextual forms and lam-alef behavior look intentional |
| arabic | العربية | initial/medial/final joins are shaped and spaced coherently |
| bismillah | بسم الله | word spacing, medial joins, and `heh`/`meem` forms hold together |
| lam-alef | لا | lam-alef ligature is present and weight-compatible |

Also inspect mark attachment manually:

- base + fatha, damma, kasra, shadda, sukun;
- tanween combinations;
- hamza above/below combinations;
- dotted circle with top and bottom marks;
- `smallHighTah-ar`, `noonGhunna-ar`, and `smallHighThreeDots-ar`.

## Review Queue

Use `documentation/glyph-review/arabic-manual-review-batches.md` for the shortest active
review order. It starts with the 5-row structure and wrong-glyph sweep, then
moves through marks, dot-stack helpers, and RTL text/spacing. Use
`documentation/glyph-review/arabic-next-review-batch.html` as the focused working page for
the next unresolved batch and `documentation/glyph-review/arabic-manual-review-dashboard.html`
as the broader embedded-font dashboard.

The contour cleanup artifacts are now evidence, not the active queue:
`documentation/glyph-review/contour-cleanup/contour-cleanup-review-queue.md`,
`documentation/glyph-review/contour-cleanup/contour-cleanup-edit-plan.md`,
`documentation/glyph-review/arabic-cleanup-drawing-briefs.md`,
`documentation/glyph-review/contour-cleanup/contour-cleanup-batches.md`,
`documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md`, and
`documentation/google-fonts/fontspector-contour-count.md` should stay synchronized after
source edits. If a later build reintroduces contour findings, use those files to
map production names back to source glyphs and record the decision.

## High-Priority Glyph Classes

1. Arabic letter structures: `sad`, `dad`, `tah`, `zah`, `meem`, `heh`,
   `wawHamzaabove-ar`, lam-alef forms, and related positional forms.
2. Arabic mark combinations: shadda, hamza, tanween, sukun, and kasra
   composites.
3. Dot-stack letters and helpers: Persian/Urdu three-dot forms,
   `seenSixdots-ar`, `fehThreedotsbelow-ar`, `qafThreedotsabove-ar`,
   `tehThreedotsdown-ar`.
4. Arabic and Farsi numerals: U+0660-U+0669 and U+06F0-U+06F9 for rhythm,
   width, and style fit.
5. Arabic punctuation: `comma-ar`, `semicolon-ar`, `question-ar`,
   `perMille-ar`, `dateSeparator-ar`, `fullStop-ar`, and Arabic parentheses.

## Review Decisions To Record

For each row in `documentation/glyph-review/arabic-visual-review-log.md`, record one of:

- `pass` only after checking the listed proof evidence;
- `fix-needed` when a drawing, spacing, mark, or shaping issue needs source
  edits;
- `deferred` when the row needs Arabic native-reader review, a later
  kerning/spacing pass, or Google Fonts reviewer guidance.

When a visual row needs drawing work, open the affected glyphs in both masters
and preserve compatibility. After source edits, regenerate the contour proof so
the closed contour queue stays honest.

After edits or decisions:

```bash
make contour-cleanup-proof
make kerning-proof-check
make kerning-proof-review-check
make preflight
```

If `make kerning-proof-check` fails because it cannot resolve
`fonts.google.com`, rerun that target with network access.
