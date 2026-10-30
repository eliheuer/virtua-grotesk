# 2026-07-29 — fourth batch (n £ ¥ § ¨ © ª sheet)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


- **Multi-part glyphs in sheets**: declare span counts explicitly
  (`dieresis:2`) — a smallest-gap merge heuristic merged the wrong pair
  (crowded £¥). Explicit beats clever.
- **Scaled donors preserve G2**: copyright's inner c (green c x0.74) and
  ordfeminine (a x0.87) pass the continuity gate untouched — scaling
  preserves G-class, so derive-by-scale is a first-class construction.
- **Auto-harmonize**: `symbol_gen.harmonize_g2()` scales adjacent handle
  lengths toward matched endpoint curvature (kappa = 2/3 d/l^2), the CLI
  twin of Runebender's harmonize->G2; sterling's hook apexes went G1->G2
  automatically.
- **Winding rules generalized**: outer CCW, counters CW, decided by
  point-in-polygon nesting parity (bbox tests misclassify overlapped ink
  like yen's bars; parity handles ring-inside-ring-inside-c).
- **Degenerate curve types break the build**: a type="curve" point with no
  offcurves compiles in sources but crashes overlap removal on instances.
  (Candidate: assert in glif() that curve points have 2 offcurves.)
- Values: dieresis = two i-tittles at mark-center 180, gap 88/64;
  yen ink 600/adv 664, bars 72/112 at sheet positions; copyright ring
  dia 832 stroke 44/80 + c x0.74; ordfeminine = a x0.87 seated at 256;
  sterling v1 straight base (sheet wave = upgrade candidate), currency
  sb 32. **section DEFERRED** — proposed as the img2bez pilot (too curvy
  to parametrize honestly; current placeholder is two overlaid S
  components).
