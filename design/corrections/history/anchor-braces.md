# 2026-07-28 — third batch (n { | } ~ ¡ ¢ sheet) + START RULE

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


- **START RULE (Eli)**: contour start points go at the LOWER-LEFT on-curve
  point (min y, then min x). Now automatic: `symbol_gen.normalize_start`
  runs in `write()`. Applies to all future generation; existing graded
  glyphs left as-is until a cleanup pass.
- **Rotation vs mirror winding**: 180-degree rotation PRESERVES winding
  (transform in order, no reversal); mirrors REVERSE it (reverse the list
  and shift segment types incoming->outgoing). Encoded as
  `reverse_contour` / `mirror`; the write() assertion catches mistakes.
- Derivations this batch: exclamdown := exclam rotated 180 about its
  advance center, top seated at 656 (family consistency with exclam over
  the sheet's taller proportions); cent := c + lc-stem bar (96/192)
  through the ink center, y -96..656 per sheet.
- First CURVED generations: braces (chevron-style beak + cubic hooks,
  bracket band -128..848) and tilde (cubic S centerline, vertical stroke
  offset, center 370 per sheet). Generator now supports typed points
  (line/curve/offcurve, smooth) — expect these to need Eli polish; log
  the corrections here when they land.
