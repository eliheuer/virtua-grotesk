# Arabic Print Proof Index

This generated index maps `documentation/arabic-print-proof.pdf` pages to
the Arabic visual-review pass. The PDF is a fast print/PDF aid; keep the
Google Fonts HTML proof and source GLIF files authoritative for final
review decisions.

- PDF: `documentation/arabic-print-proof.pdf`
- Pages: 12
- Review log: `documentation/arabic-visual-review-log.md`
- Current worksheet: `documentation/arabic-current-review-worksheet.md`
- Next packet: `documentation/arabic-next-review-packet.md`

## Page Map

| Page | Style | Section | Use during review |
| ---: | --- | --- | --- |
| 1 | Regular | Arabic samples | Shaping strings, Persian/Urdu letters, dot stacks, and mark attachment samples. |
| 2 | Regular | Arabic numerals and punctuation | Arabic-Indic digits, extended Arabic-Indic digits, and Arabic punctuation at multiple sizes. |
| 3 | Regular | Arabic cmap grid | Encoded Arabic and dotted-circle cmap grid. |
| 4 | Medium | Arabic samples | Shaping strings, Persian/Urdu letters, dot stacks, and mark attachment samples. |
| 5 | Medium | Arabic numerals and punctuation | Arabic-Indic digits, extended Arabic-Indic digits, and Arabic punctuation at multiple sizes. |
| 6 | Medium | Arabic cmap grid | Encoded Arabic and dotted-circle cmap grid. |
| 7 | SemiBold | Arabic samples | Shaping strings, Persian/Urdu letters, dot stacks, and mark attachment samples. |
| 8 | SemiBold | Arabic numerals and punctuation | Arabic-Indic digits, extended Arabic-Indic digits, and Arabic punctuation at multiple sizes. |
| 9 | SemiBold | Arabic cmap grid | Encoded Arabic and dotted-circle cmap grid. |
| 10 | Bold | Arabic samples | Shaping strings, Persian/Urdu letters, dot stacks, and mark attachment samples. |
| 11 | Bold | Arabic numerals and punctuation | Arabic-Indic digits, extended Arabic-Indic digits, and Arabic punctuation at multiple sizes. |
| 12 | Bold | Arabic cmap grid | Encoded Arabic and dotted-circle cmap grid. |

## Review Shortcut

1. For the current structure/wrong-glyph sweep, scan the `Arabic cmap grid`
   pages for each style first, then open the matching Google Fonts glyphs
   proof if anything looks missing, clipped, blank, duplicated, malformed,
   or wrong-codepoint.
2. For marks and dotted-circle rows, scan each `Arabic samples` page, then
   open `documentation/arabic-mark-review-proof.html` and the source glyphs
   for anything that needs drawing or anchor edits.
3. For numeral and punctuation rows, scan each `Arabic numerals and
   punctuation` page before checking the proofer/text HTML.
4. Record review outcomes only through
   `make arabic-visual-review-update ...` after checking the linked proof
   or source evidence.
