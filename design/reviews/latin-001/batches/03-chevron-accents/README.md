# LAT-001 batch03 · Bold circumflex and caron

Two Bold spacing donors change: `circumflex` and `caron`. Their previous outlines
were exact Regular copies. The new marks have thicker arms, clipped end caps and
a64-unit apex flat. Both keep16-point compatible polygons and the same advances
and attachment anchors. New bounds are x48–368/y640–832; the circumflex's inner
landing is32 units wide at y712. Caron mirrors that contour vertically about y736.
Their ink area increases from23488 to37248 square units (about59%); this is a local
weight decision, not a universal accent formula. Green H/n and the prior acute/
macron proofs provide internal weight context; Rubik is a comparison only.

Both Regular GLIFs are byte-identical. All other source bytes, including Arabic
recursive donors, green drawings and the reversed-Nun dot calibration, are
preserved. The reverse dependency closure contains51 glyphs per master, with no
green or Arabic consumers. Only the two red Bold donors receive purple grades;
consumer grades are unchanged. The40 grid findings are unchanged Regular geometry
and retained anchors/advances. All new outline coordinates are on8.

Whole attachment, reading and stacking images were inspected at400/550/700, plus
104px/em detail and224px/em whole-letter detail at700. The new marks read with
Bold letters and keep the notch open; the apex is deliberately flattened rather
than ending in the earlier narrow point. Complete Esperanto/Czech/French rows
and stacked upper marks show no new collisions in the sampled contexts. Regular
ink is unchanged. These remain human-review drafts, not visual approval.

The angular Regular chevrons, alternate carons on tall lowercase, small square
ring and thin breve remain unfinished. Wider hats are a review choice; no native
reader approval is claimed. No new curves occur in this batch: both are polygons.

Verification: complete source master compatibility; five-weight winding/edge/
intersection checks; compiled changed-ink closure;90 shaped-context checks with
unchanged glyph positions and clear stacks; all three Latin tests over VF/four
statics; exactly216 pre-existing engineering failures reproduced on the frozen
baseline, zero new failures. Build and preflight complete. Existing online
Fontspector findings have not been re-certified by these source checks.

Exact before/candidate XML, source hashes, baseline fonts and raster receipts are
retained. `apply.py` refuses changed source hashes. `render.py` reuses batch02's
frozen standard recipe and this folder's large recipe. The local checkpoint does
not imply permission to publish or push. Eli explicitly approved and pushed the
earlier attachment/coverage commit1e8dd28e during this batch; later drawings remain
local. Next bounded work: ring/breve, then tilde/bottom marks and alternate carons.
