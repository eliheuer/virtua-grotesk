# Batch 04 — Bold initial / medial Feh and Qaf heads

Baseline `1f7dc7f6`. Applied working drawings; human review remains pending.

Rebuilt the red Bold `fehDotless-ar.init` and `fehDotless-ar.medi` shared
heads on the 8-unit grid. Regular's green bases remain byte-identical. The
initial now has 160-unit head walls and a 176-unit connecting bar, replacing
an almost-Regular weight. The medial replaces kinked, slanted handles with
axis-aligned extrema, a clean oval counter and 8-unit shoulder landings above
the joining bar. Exposed joining chamfers remain 16 units. Contour order,
point types/counts, component donors and anchors are preserved.

Fourteen red component wrappers now match their base advances: 544 initial,
560 medial. This removes the initial-to-medial joining discontinuity in the
Feh proof. Above-dot wrappers move with the heads: initial +32 x / +64 y,
medial -32 x / +104 y. The single-dot centers are now 256 and 272; both have
48 units of clearance above the new heads. Dot drawings are unchanged.
Below-dot offsets remain for the later placement pass. The manifest records
all inherited glyphs; none is green. Only the two new root drawings are
regraded purple; existing wrapper grades are retained.

## Evidence inspected

- `detail-400.png` / `detail-700.png`: actual shaped `ففف ف`, 144 px/em,
  Before / Working and all four reference fonts. A 176 px attempt was rejected
  by the panel bounds guard; all fonts use the same reduced size.
- `qaf-400.png` / `qaf-700.png`: `ققق ق`, 128 px/em, same six-font comparison.
- `initial-large.png` / `medial-large.png`: DesignBot source-scale glyphbox
  renders, inspecting the initial's tight return and medial counter/shoulders.
- `browser-550*.jpg`: intermediate weight, all four references visible across
  the two captures. No browser warnings/errors were reported.

The new counters remain open, curved extrema are smooth, and above dots clear
both heads. This is a technical/visual agent inspection, not human approval.
The initial has a tight, flattened return beneath its head; retain it as a
specific later human review point rather than declaring it a design rule.

## Checks and unresolved findings

Build and preflight passed; source compatibility report has zero blocking
mismatches. `verification.json` records 217 shaped comparisons across seven
weights, unchanged glyph order/clusters/offsets, declared advance differences,
and compiled changes limited to the named component family. All Regular source
bytes and the manual Bold hamza hash are unchanged.

Signed curvature profiles and combs are retained. No sampled reversal or
zero-speed warnings; curve lint reports no crest/tension/kink flags. G1 joins
with unequal curvature remain deliberate; this is not a claim of universal G2.
Every new outline point and advance is on 8. `grid.json` retains three existing
anchor exceptions: initial bottomDots x=228, medial bottom/bottomDots x=306.

**Next:** isolated/final Feh and Qaf. The unchanged Bold isolated Feh/Qaf
counters show pinches/crossing artifacts, final Feh has a malformed counter,
and final Qaf still has a connection gap / insufficient weight. These defects
are visible in this batch's comparison sheets; the current batch does not
claim the whole Feh/Qaf family is finished. Multi-dot spacing and all attachment
anchors remain later passes after base silhouettes settle.
