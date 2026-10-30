# 2026-07-28 — second batch (n [ \ ] ^ _ ` sheet)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


- **Mirror-partner rule**: when a glyph's mirror or family partner already
  exists green, DERIVE it instead of tracing: backslash := slash mirrored
  in its advance; greater := less mirrored. Encoded in
  `symbol_gen._mirror_of_source`.
- **Mark components mirror about the INK CENTER, not the advance**: grave
  := acute mirrored about acute's ink center (164), which also matched the
  old grave's center — so every grave-composite's xOffset stayed valid.
  Accent-family consistency (grave matches acute) OUTRANKS the sheet.
- **Sheets give ink, not spacing**: glyph boxes/strokes come from the
  sheet; advances and sidebearings come from class rules or refs (a sheet
  cannot express its font's sidebearings).
- **Always check winding**: first caret came out clockwise and rendered
  invisible in the strict checker. `symbol_gen.write()` now asserts CCW
  (positive signed area) on every contour.
- Underscore: kept the sheet's floating width (ink 464 in adv 600) over
  HN's tiling sb-0 convention; HN also never boldens underscore — followed
  (72 both masters). Flag for Eli's grade.
- Also red-listed: acute (and the whole accent-mark set) is UNBOLDED —
  Bold == Regular. Bolding the marks is a future batch; grave inherits
  this (kept consistent with acute rather than "fixed" alone).
