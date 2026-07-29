# Lessons — anchor-sheet glyph generation

Running log of optical corrections and workflow findings. Newest first.
Every entry: date, glyph(s), what was wrong, the rule, where it's encoded.
These rules OUTRANK the generator formulas — when in doubt, match the
latest graded (green) example of the same construction.

---

## 2026-07-28 — chevron tips need a flat (Eli correction)

**Glyphs:** less, greater (first generated batch).
**Wrong:** generated tips ended edge → 16u bevel → vertical face; the tip
read too pointy.
**Rule:** diagonal-arm tips land on a **16u axis-aligned flat** before the
bevel: outer edge → 16u flat → 16u bevel → face. Same anatomy as V/W/v
baseline terminals. Applies to any arm tip on a line-grammar glyph.
**Encoded:** `symbol_gen.chevron_left` (TIP_FLAT), round-trips Eli's
corrected files exactly.
**Also noted:** Eli kept the notch at its original x (182/322) rather than
the strict inner-parallel recomputation (194 would match the new outer
slope) — a slight arm taper toward the apex is acceptable; don't "fix" it.

## 2026-07-28 — pilot findings (n < = > sheet)

- **Anchor calibration works**: n px-height ↔ 592u gave scale + baseline;
  symbol stroke measured from the sheet (71.2) matched the system-derived
  expectation (hyphen 88 × HN 64/80 = 70.4) within 1u. Always run this
  cross-check; agreement = trust the sheet.
- **The sheet is authoritative**: the pilot sheet was NOT Helvetica Neue
  (HN math axis ≈ 282 vs the sheet's 352). Refs fill gaps (e.g. Bold
  stroke ratio when no Bold sheet exists); they never override the sheet.
- **Math class values set**: axis 352, stroke 72/132, advance 600,
  equal-bar centers ±100 R / ±132 B (gap≈1.78×bar R, ≈1×bar B, per HN).
- **Bold hyphen is unbolded** (88 = Regular value) — on the red list; do
  not use it as the Bold symbol-class anchor until fixed.

## 2026-07-28 — second batch (n [ \ ] ^ _ ` sheet)

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

## 2026-07-28 — third batch (n { | } ~ ¡ ¢ sheet) + START RULE

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

## 2026-07-28 — tilde rebuild + extrema rule (Eli correction)

- **EXTREMA RULE (the img2bez discipline)**: on-curve points go AT the
  extremes — every curve extremum (crest, trough, side extreme) is an
  on-curve point with an axis-aligned tangent; segments between extrema
  are monotonic. The first tilde put on-curves mid-slope and was "close
  to unusable." Any parametric curve construction must place extrema
  first, then fill in handles. For curved shapes too complex to
  parametrize confidently, DELEGATE to img2bez on a calibrated sheet crop
  (it gets extrema right by construction) — that is the preferred path
  for organic/curvy glyphs.
- **START RULE clarified**: lower-left = leftmost first, lowest tiebreak
  (min x, then min y). Min-y-first wrongly started the tilde at its
  trough. All generator glyphs regenerated with the corrected rule.
