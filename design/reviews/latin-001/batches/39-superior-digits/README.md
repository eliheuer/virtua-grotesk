# Batch39 · Encoded superior digits

Applied locally from baseline `a40087a6`: new purple `onesuperior` (U+00B9),
`twosuperior` (U+00B2), and `threesuperior` (U+00B3) in Regular and Bold.
These are standalone outlines derived from protected Virtua figure construction;
all original one/two/three bytes and grades remain exact. Rubik supplied the
visual comparison, never outlines. No ordinary-size aliases, `sups` feature,
kerning, mark anchors, or existing glyph changes were added.

Each master has one contour per new glyph, with matching 16/35/50 points/types.
The nominal envelope is 384 units high at baseline384; rounded forms overshoot
to376/776. One retains the curved flag, three retains rounded upper/lower bowls.
Advances are232/264,328/352,352/376 (Regular/Bold). One stems64/96 and two foot
weights56/80 support small rendering. Exposed cuts16, internal joins8; every new
point and spacing value is on8. `grid.json` records zero findings across six
glyph-masters and descriptive popcounts, without assigning a grade.

The first snapped two trial had unintended diagonal tangent mismatches (up to
2.60 degrees). It was rejected before application; exact before/candidate sources
and endpoint images remain under `trials/01-snapped-diagonal`. The final diagonal
handles meet at G1 in both masters. Signed combs and five-weight sampled profiles
show no within-segment reversal warnings or proper crossings. Intentional terminal
cuts and the three bowl crotch remain G0; other G1 curvature jumps are recorded,
not claimed G2. Two zero-angle line/curve joins in three remain non-smooth-labeled;
`curve-summary.json` distinguishes the classifier label from tangent continuity.

## Preservation and verification

Ten source files: six new GLIFs and four registration plists. All1821 other
existing sources and every old GLIF remain byte-identical. Recomputed reverse
component closure and Arabic reservations are in `dependencies.json`: Arabic326
per master and green131 Regular/74 Bold preserved. Current hash guards ran before
application and after active build; human saves/grades and Arabic60272 are intact.

- 145 scoped checks;4485 exact old VF glyph/weight ink-and-advance comparisons.
- 3587 old static glyph ink-and-advance comparisons, all exact.
- 54 real text-subset/NFD cases across five VF weights and four statics pass.
  NFKD still removes the superior distinction; it is not a display repair.
- 27 Latin and two build-helper methods pass on scratch and active fonts.
- Frozen baseline and candidate each retain exactly216 Hebrew failure subcases,
  with no new or resolved failures. Those remain release blockers.
- Active fonts match scratch table bytes except `head` timestamps. Preflight
  rebuilt the VF/statics, ran raw DesignBot sequentially and regenerated reports;
  artifact presence alone is not a visual or release pass.

## Visual review and QA

Complete forms/reading rasters at400/550/700,224px endpoint details, signed combs,
and12 actual Diffenator screenshots were inspected. Browser review covered both
fonts at400/550/700 in the same-text supplement and first stock mixed-text viewport.
Hashes/scope are in `compiled-proofs.json`, `browser-review.json`, and
`final-identity.json`. Old=Virtua candidate, New=Rubik; the slider governs weight
although the menu label stays Regular. This is sampled agent review, not human
approval or exhaustive language review.

The forms read as superscripts in exponents, footnote markers and square/cubic
units. Regular two/three are lighter than Rubik; the curved one flag and rounded
three intentionally follow Virtua. Bold counters stay open. Weight balance with
ordinary figures, default pair rhythm and small-size optical adjustments remain
human review. Generic acute/cedilla use right-side fallback rather than dedicated
superior attachment. Stock text still has uneven spacing and dense Bold.

Full online unexcluded Fontspector1.9.0 package: **12 FAIL /10 WARN /159 PASS /
10 INFO /40 SKIP**. Exact failure records match batch37; no new semantic warnings.
Raw glyph-ID/path/suggestion-order differences are retained in
`package-failure-delta.json`. Serving-set reachability, soft-hyphen retain/omit
policy, protected Arabic findings and provisional package metadata remain open.
The package uses the scratch VF; active tables match except head. No exclusions,
false subset declarations, licensing attestation or publication.

Pinned Rubik gap is now335 encodings:182 Cyrillic,51 Common,102 Arabic presentation
forms; Latin/combining gap remains zero, not language coverage or approval.
Next inspect remaining superior0/4–9 construction and figure-family coherence
before a bounded extension; do not introduce partial `sups` substitution or change
protected figure donors. Other Common gaps and independent release blockers remain.

Preview: http://127.0.0.1:60273/batch39/comparison/superiors.html.
Local checkpoint only; no push. Diagnostic and display artifacts are not release
inputs. Do not rerun frozen preparation scripts over newer human saves.
