# LAT-001 batch09 · Cedilla

Regular and Bold cedilla donors replace the identical angular spur with an
attached diagonal neck, an open rounded hook and16-unit cuts at the left
landings. Each has one compatible25-point contour with four cubics. Cardinal
bowl weights are48/64; the inner aperture remains64 tall. Outer right turns
use80/96 extents with48/56 handles; inner turns use32 extents and16 handles.
These are local construction choices, not universal curve recipes. Bounds are
Regular x64–224/y-224..0 and Bold x32–240/y-256..0. All new points are on8.

Outgoing bottom anchors in cedilla and cedillacomb move-200→-256/-288,32 below
the new bowls. Incoming anchors(134,0), advances260 and component transforms
remain unchanged. Redrawn donors are purple; combining-wrapper grades remain.
Eight compiled glyphs inherit each donor; none is green or in the326-source
Arabic reservation. All green/base drawings, manual Arabic donors and the
reversed-Nun calibration are unchanged.

Whole attachment, French/Turkish reading and supported-reference rows at
400/550/700 and224px/em endpoint letters were inspected. The hook now has an
open interior and continuous round edge; Bold gains weight rather than repeating
Regular. The wider, deeper hook and angular neck remain for human optical and
reader review. No visual approval or release readiness is claimed. Rubik lacks
Ţ/ţ (U+0162/U+0163), so full coverage panels mark it unavailable; supported
ÇçŞş and actual decomposed strings compare Rubik directly, without fallback.

The large proof's original panel was too short for the deeper hook; its baseline
moves16px up so the complete letter fits. Independent FreeType/RAQM stacked
proofs use taller panels and retain the complete deep forms. The Arabic live
proof layout/current case is unchanged. Mark stacking is diagnostic text, not
an assertion that repeated cedillas are normal orthography.

Stack inspection exposed a new clipping problem: b+two cedillas reaches-544
at700, beyond the old Windows descent512. Both fontinfo files now use576 for
Windows clipping descent, leaving32 units of clearance. Typographic/hhea
metrics, line gaps and USE_TYPO_METRICS stay unchanged. Legacy applications that
use Windows metrics for line spacing may gain64 units of line height; current
platform testing remains a release gate. A new compiled regression test checks
these deep stacks against the actual clipping metric. All proofs were refreshed
after this fix;15 previously inspected images have byte-identical pixels.

Six source files change: four donor/anchor GLIFs and two clipping metadata files.
All1773 other source files remain byte-identical. Twenty grid findings are
inherited x134 anchors/advance260 and resulting sidebearings, including recursive
checks of the unchanged combining component. New geometry/anchor y values are
on8; human/legacy x metrics were not snapped to improve a score.

Signed profiles and the common-scale comb were inspected at endpoint weights.
Five sampled weights have no curvature sign reversals or outline intersections.
Each has two G2 joins at the right extrema and four tangent G1 line/curve joins;
curvature steps at the straight landings remain explicitly documented. Curve
lint finds no crest/tension/kink flags. These diagnostics do not approve the
neck, proportions or complete letters.

90 scoped shaping/ink checks preserve sequences/advances and unaffected-script
positions while confirming below-stack clearance and the clipping fix. Changed
compiled ink is exactly the eight-glyph closure; complete master compatibility
passes. Five Latin tests pass over VF/four statics. The frozen baseline reproduces
exactly216 existing Hebrew engineering failures, with zero new or resolved
failures. Active build/preflight completed; candidate/active VF tables match
except head timestamps. Online Fontspector was not rerun. Local checkpoint only.

Next: ogonek, then alternate carons and the maintained spacing/coverage/release
queue. Generic green g+U0326 attachment remains unresolved from batch08. Do not
change protected geometry or mark anchors without the named exception.
