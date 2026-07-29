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
