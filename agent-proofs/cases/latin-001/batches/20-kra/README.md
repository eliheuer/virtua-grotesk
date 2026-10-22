# LAT-001 batch20 · Kra

Adds `kgreenlandic` (ĸ, U+0138) in Regular and Bold as purple drafts. The pinned
Rubik reference shows an x-height k construction. Each new23-point line contour
uses Virtua's corresponding green k branch structure with the stem top shortened
from768 to576. Off8 donor x coordinates move to the next8-unit coordinate in the
new glyph only; the original k drawings and optical widths remain byte-identical.
The8-unit branch landing and16-unit cuts are retained. No external outlines copied.

Six source files: two new GLIFs plus four registration plists. All1783 other
existing sources unchanged, including326 Arabic reservations/master and every
green source. Exact baseline, donor bytes, candidates, application hash guards
and receipts are retained. No feature, kerning or font-metric changes.

Regular advance600=512+64+16+8, bounds(72,0,576,576), bearings72/24.
Bold advance664=512+128+16+8, bounds(72,0,640,576), bearings72/24.
Top anchors(304,576)/(344,576); bottom(304,0)/(344,0). All new points, anchors,
advances and actual bearings on8; zero grid findings. Original Regular k advance596
is preserved. No ordinary-k substitution or automatic donor kerning is added.

## Verification and images

95 scoped checks and13 Latin test methods pass. All previous compiled glyph ink
and advances remain exact at400/475/550/625/700; master structure is compatible.
Five-weight line-contour inspection finds no proper polygon crossings. There are
no cubic curves; curve lint has no cubic profile to score. Frozen engineering
runs reproduce exactly216 existing Hebrew failures, with zero new failures.
Active preflight completes; active/scratch font tables match apart from head
timestamps. Preflight only establishes artifact presence.

Inspected complete FreeType/RAQM forms and marked contexts at400/550/700,
sequential DesignBot reading rows at400/550/700 and224px endpoint details.
[Large Bold proof](large-700.png) exposes the dense inherited branch junction.
Actual Diffenator stock coverage first viewport and separately labeled kra
supplement were inspected at400/550/700, with the same supplement text in Rubik.
Stock coverage omits U0138, so it cannot substitute for that supplement.
[Commands and hashes](diffenator/generated.json); [review and screenshots](diffenator/review.json).
Preview: <http://127.0.0.1:60273/batch20/comparison/kgreenlandic.html>
(Old=Virtua, New=Rubik). Arabic live proof60272 is unchanged.

## Unresolved / next

The dense Bold stem/branch, the inherited angled junction and default pair spacing
need human optical review. The new silhouette is coherent with the existing k;
that does not approve the donor's proportions or the font's overall Bold density.
Sample letter strings are construction tests, not native-reader validation.
Existing protected attachment, compound-mark/subset and Hebrew failures remain.

Pinned Rubik Latin gap4→3: ŉ ﬁ ﬂ. Other gaps remain182 Cyrillic,4 combining marks,
62 common symbols and102 Arabic presentation forms; these are codepoint counts,
not language counts. Next bounded construction: apostrophe-n, then fi/fl and
independent release blockers. Local checkpoint only; no push or release approval.
