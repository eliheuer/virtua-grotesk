# ARB-006 batch 06 — Medial loop correction

Eli identified the medial Feh/Qaf shape as wrong against the references, then
authorized continuing independent Arabic base families without awaiting feedback.
Beh and all recursive component donors remain reserved in both masters.

## Scope

Bold `fehDotless-ar.medi` (shared by medial Feh/Qaf) and `fehDotless-ar.fina`,
plus seven direct upper-dot wrapper placements: nine GLIFs in all, eleven
affected glyphs. No dot donor or Beh source changed. Regular, green drawings,
human hamza, existing widths, anchors and wrapper colors remain byte-identical.
The drawing roots remain purple. The manifests include 18 reserved Beh/component
file hashes and the complete source baseline; before/candidate XML is retained.

## Drawing interpretation and trials

The previous circle on broad shoulders read as a bump on a bar. The references
show a narrower loop return and a counter tapering toward the joining stroke.
This is the agent's interpretation, not a new human-approved design rule.

Raise the loop center/crown 88 units (352/584), narrow the lower return from
400 to 224 units at the joining bar, and use 8-unit chamfered landings. Keep
160-unit top/side weight, the 176-unit bar and a 144-wide counter. The counter
bottom is 248, below its 352 center; its upper cap is 424. Opposed side tangents
and matched signed curvature are retained. Upper dots move 88 units with the
crown; shared dot shapes are untouched. The same head correction transfers to
final Feh and its Veh derivative. Final Qaf is structurally different and stays
as batch 05; its compact bowl remains a later human design-review item.

`trial-01/` preserves the excessively long, pinched counter; `trial-02/` preserves
the too-narrow pedestal. The current candidate opens the counter and broadens
the joining neck. It retains the existing flat lower joining contour: it does
not import the references' calligraphic stroke crossing. Regular's green round
counter and existing skeleton are intentionally untouched.

## Verification and raster review

- Built variable/static fonts and preflight completed; no blocking master
  structure mismatches. 210 compiled shaping comparisons across seven weights
  preserve glyph IDs/clusters and verify the declared component-placement deltas.
- Curve profiles: no sampled inflection warnings or smooth-node kinks; matched
  counter joins; outer side jumps under 20%. Sampled proper crossings: zero.
  Both old and new shapes pass this geometric check: that explicitly demonstrates
  why curvature scores alone cannot catch a script-structure/design problem.
- Grid: four retained off-grid anchor x coordinates; new outlines stay on 8.
  Existing anchors are not silently moved. Full attachment refinement is later.
- Actually inspected `feh-400/700.png`, `qaf-400/700.png`, `mixed-550.png`,
  `veh-700.png`, `medial-large.png` and `final-large.png`. The lower loop is
  distinguishable, its counter stays open, the joining stroke stays continuous,
  and upper dots are clear. No crossing artifact or disconnected Qaf join seen.
- Intermediate PNG uses actual 550 for variable fonts and explicitly labels
  Plex's nearest supplied static weight (500); its receipt records that weight.
  The raster runner now supports intermediate weights with this disclosure.
- Batch 05's unchanged initial and final Qaf source-scale renders were also
  inspected. The retained compact Qaf bowl differs from the references and is
  recorded for human review; no claim of final style approval is made.

Current status: applied working draft, inspected and technically checked;
human review pending. Proceed independently to Bold Lam, preserving Beh.
