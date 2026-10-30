# 2026-07-29 — THE FLAT RULE (Eli) + dollar done right

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


- **FLAT RULE: no overlapping contours in sources, ever.** The viewer sees
  figure and ground; the sources must be the same flat form. Compose from
  donors, then UNION (booleanOperations, cubic-aware) and clean. This
  supersedes the overlay constructions — dollar rebuilt this way;
  yen, euro, cent, sterling, registered still carry overlays and need the
  same flattening pass (queued).
- **Union recipe**: build overlapped construction in a scratch defcon
  glyph -> BooleanOperationManager.union -> extract typed points -> round
  to 2-grid -> write with donor order (normalize=False) -> gates.
- **Union hazards found on dollar**: (1) masters can flatten to DIFFERENT
  structures (Regular got an 8u sliver segment + extra point where Bold's
  curve landed directly on the bar edge) — diff the masters' on-curve
  sequences and merge slivers so counts match; (2) grid-rounding after
  union can tilt a smooth point past tangency (the 4.3-degree kink) —
  the sliver merge fixed both at once. The continuity gate + fontmake
  compatibility check catch both; never skip them on unions.
- Dollar params from the n$ sheet: bar 64/104 wide, y -96..848, centered
  on the S ink; body = the green S verbatim.
