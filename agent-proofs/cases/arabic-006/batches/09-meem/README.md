# ARB-006 batch 09 — Bold Meem

Applied four red Bold roots: `meem-ar`, `.init`, `.medi`, `.fina`. All four
Regular forms remain green and byte-identical. No component descendants were
found. Recomputed and preserved the 18-file Beh reservation; saved manual hamza,
all other sources, anchors and features are unchanged. AI redraws are purple.

## Drawing and observed faults

The baseline Bold initial/final outlines retained Regular weight. Final Meem's
932-unit advance exceeded its 656-unit incoming edge, producing a broken join.
The repaired final arm ends at its 880-unit advance. Isolated/initial/medial
advances are 800/568/608. The shared isolated/initial/final head is 480 high,
with 160-unit side weight, 144-unit crown, 176-unit base and a 160-unit counter.
Tails are 160 wide with 16-unit end cuts. Counter/shoulder landings retain 8 cuts.
These are provisional Arabic dimensions, not replacements for DESIGN.md's Latin
weight ladder. Green Regular Meem supplies topology and the tail/head relation;
Bold o supplies axis-tangent round construction and H the 16/8 corner pattern.
No external outlines were copied.

Medial Meem now rises above its 176-unit joining bar, with a round open counter
and two deliberate S-shaped shoulders that enter the bar horizontally. It keeps
the protected Regular master's four-contour structure. Positive bar overlaps
are intentional and resolved by compilation. This is a symmetric machined trial;
the references' asymmetric counters and lower relief differ. Human review is
still needed; do not call the full family complete.

The first round medial trial had small shoulder notches at its bar intersections
(`medial-v1.glif`, `medial-large.png`). A narrower smoothing trial then made the
shoulders too thin (`medial-v2.glif`, `meem-v2-700.png`); rejected. The final wider
S shoulders retain more mass and avoid that notch. The final-form concave return
was also reduced from a 4.4:1 endpoint-curvature magnitude mismatch to about
1.08:1 opposite signs. It is G1 at that intended S transition, not G2. No claim
that a numeric score establishes the drawing's quality.

## Verification

- Canonical variable/static build and `make preflight` completed; zero blocking
  master-structure mismatches (500 width-only differences).
- 287 compiled shaping comparisons at 400/450/500/550/600/650/700, including
  `ممم م`, words, Beh controls and ZWJ/ZWNJ contexts. Glyph identities, clusters
  and offsets preserved; only declared advance changes. Compiled differences
  confined to the four Meem forms; Regular endpoint unchanged.
- Signed profiles and curve lint inspected. No sampled within-contour crossings,
  undefined joins or tangent kinks. The medial S-curve sign reversals and hidden
  overlap joins are recorded explicitly in `quality-check.json`; final Meem's
  intended G1 S transition is retained rather than misreported as G2.
- New outline coordinates/advances/bounds on 8. The grid tool reports four
  preserved existing anchor exceptions: isolated bottomDots -284/topDots460,
  final bottomDots -380/topDots396. No anchors were moved in this base-form pass.
- Actual six-panel 400/550/700 PNGs inspected. All counters stay open. Final
  joining gap is closed. Large final source render and 256-px compiled medial
  render inspected; live browser proof at 700 inspected and captured.

`candidate.json` / `applied.json` contain exact before/current hashes and the
Beh dependency reservation. Exact GLIFs are under before-sources/candidate-sources.
`verify.py` rejects any unrecorded source edits rather than overwriting them.

## Remaining findings

- Green Regular medial Meem sits lower than the other forms/reference skeletons;
  the interpolation inherits that relationship. Requires a named Regular
  exception before changing it. Do not silently make a new shared topology.
- Existing mark anchors are low relative to the revised Bold heads. Mark placement
  is deferred, explicitly not verified as correct by unchanged shaping offsets.
- `glyph_canvas.rs` raw source rendering filled the counter on the S-shoulder
  trial (`medial-v2-large.png` / recheck). Source and compiled winding tests at
  three counter points are outside ink, and actual compiled DesignBot/browser
  rendering shows the hole. Keep this as a source-renderer discrepancy for a
  separate harness fix; do not "repair" valid source winding from that image.
- Lam–Alef remains a separate green-source structural follow-up.

The detail runner now exempts ZWJ/ZWNJ from visible cmap coverage requirements,
so `ZWJ + Meem + ZWJ` can proof a real shaped medial form. Other missing visible
characters still fail. This was exercised by `medial-compiled-large.png` with
all four references. No layout changes were made.

Next independent family: Hah/Jeem/Khah; inspect shared roots and green descendants
before choosing the bounded editable scope. Preserve Beh and its donors.
