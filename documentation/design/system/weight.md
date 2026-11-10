# Weight and proportions

Virtua aims for monolinear apparent stroke weight. Identify which contour edges,
alignments, counters and straight-to-curve boundaries are fixed for the specific
glyph before transferring weight. Counter reduction is an established Latin
construction pattern; do not assume every Arabic/Hebrew outer contour is fixed.

Use live green O/H/n/o and same-script donors, checking source grades at lookup.
Measure the current sources with `scripts/check_design.py --observe`; the
stroke ranges are in `sources/design.toml`. Script-wide weight remains subject
to cross-script visual review.

Transfer construction relationships rather than scaling all coordinates or
translating every turn with a thicker bar. Inspect opposing-edge weight, full
silhouette and shaped words. Zayin Bold's compact turn and hamza's unequal handles
show why one universal handle ratio is insufficient.

## Rule entries

### Open a Bold counter with width, not a thinner stem

Bold lowercase stems stay 192. When a Bold counter closes up, make the advance
wider.
Seen in: Bold n b d (9fb03696).
