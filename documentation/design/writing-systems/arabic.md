# Arabic context

Keep Virtua's green source construction while preserving Arabic distinctions and
joining behavior. External Arabic fonts are structural and reading references.
Before editing joins, measure both edges in actual neighbor forms; matching shaping
positions alone cannot detect an ink-height step.

For dual-joining letters, prove initial/medial/final/isolated forms through normal
shaping, such as three repetitions plus an isolated letter. Include words and mark
contexts as appropriate, RTL and language ar, at 400/550/700. Right-joining letters
only require forms their script behavior supports.

Inspect recursive base/dot/mark dependencies and reserved human work. Letter-dot
anchors and harakat anchors have separate roles. Preserve green inherited drawings.
Do not copy Hebrew mark shapes into Arabic letter dots.

Progress is in `STATUS.md`. Kaf and final Yeh have glyph intent records in
`design/glyphs/`; read them before treating reference differences as defects.

## Rule entries

### Finish base forms before marks

Draw and correct the base letters before their marks.
Seen in: ARB-004 (211c3b8d).

### Isolated boats and cups have even terminals

The two terminals of an isolated boat or cup have the same thickness.
Seen in: behDotless-ar, terminal 432 reduced to 288 (67f4d301).
