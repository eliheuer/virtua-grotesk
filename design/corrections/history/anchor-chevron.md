# 2026-07-28 — chevron tips need a flat (Eli correction)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


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
