# 2026-07-28 — tilde rebuild + extrema rule (Eli correction)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


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
