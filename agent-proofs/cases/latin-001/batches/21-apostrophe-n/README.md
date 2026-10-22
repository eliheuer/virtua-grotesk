# LAT-001 batch21 · Apostrophe-n

Adds `napostrophe` (ŉ U+0149) in both masters as purple drafts. Actual Rubik
reference inspection shows a small diagonal apostrophe above-left of n. Each
new glyph retains green n as a component, translated80 Regular /96 Bold, plus
an eight-point local outline copied from the current commaaccent draft at
(-48,832). No donor is edited. The local mark has64/96 nominal horizontal weight,
16-unit corner cuts and y632–792; its40-unit gap above the n crown592 persists
through the weight axis. No external outlines copied.

Six source files: two new GLIFs and four registration plists. All1785 other
existing files remain exact, including326 Arabic reservations/master, manual
sources and all green sources. Full source hashes, donor/consumer closure,
before snapshots, candidates and guarded application receipt are retained.
The apostrophe and commaaccent are not live-linked; subsequent human correction
to that donor does not silently change this new glyph.

Regular advance672=512+128+32, bounds(48,0,600,792), bearings48/72.
Bold advance816=512+256+32+16, bounds(32,0,744,792), bearings32/72.
Top anchors(376,792)/(456,792), bottom(376,0)/(456,0). New outline points,
component offsets, anchors, advances and actual bearings are all on8. Six grid
findings remain in the unchanged green n component: y508 Regular /452 Bold.
No feature, kerning, font-metric or existing quote changes. Existing ʼn/’n
sequences stay two glyphs and retain their existing rendering; this batch does
not force compatibility decomposition or replace modern text with U0149.
Python Unicode data records U0149 compatibility decomposition02BC006E, not
canonical decomposition; no canonical-composition equivalence is claimed.

## Checks and visual evidence

95 scoped checks and14 Latin methods pass. All old compiled ink and advances
remain exact at400/475/550/625/700; compatible component/contour topology in both
masters. Exact216 baseline Hebrew failures reproduce, with zero new failures.
Active preflight complete; active/scratch font tables match except head timestamps.
Preflight establishes artifact presence, not release readiness.

Five-weight decomposed profiles retain the original n curves. No sampled proper
crossings or profile warnings. The n inherits tangent G1 line joins, smooth
extrema and a G0 shoulder/shelf junction; these were not redrawn or declared
perfect. Local apostrophe is line-only and vertically separate. Source curve lint
and profiles are retained alongside the before/after proofs.

Inspected full FreeType/RAQM forms/marked rows and sequential DesignBot word rows
at400/550/700, plus224px endpoint detail. [Large Bold](large-700.png).
Actual Diffenator same-text supplement inspected in both Virtua/Rubik at all three
weights; stock coverage first viewport inspected in Virtua. Stock text omits ŉ,
so supplement is essential. [Review](diffenator/review.json),
[commands/font/report hashes](diffenator/generated.json).
Local preview <http://127.0.0.1:60273/batch21/comparison/napostrophe.html>
(Old=Virtua, New=Rubik). Arabic live proof60272 unchanged.

## Unresolved / next

The mark is lighter and farther left than Rubik, and the Bold n remains dense.
Default pairs, mark balance and the inherited shoulder need human optical review;
these sample words do not establish native-reader approval. Existing Hebrew,
compound-mark/subset, protected attachment and spacing findings remain open.
Pinned Rubik Latin gap3→2: ﬁ ﬂ; other gaps remain182 Cyrillic,4 combining marks,
62 common symbols and102 Arabic presentation forms. Codepoint counts are not
language counts. Next inspect fi/fl constructions, dot/crossbar clearance,
ligature feature behavior and mark attachment before independent release fixes.
Local checkpoint only; no push or release approval.
