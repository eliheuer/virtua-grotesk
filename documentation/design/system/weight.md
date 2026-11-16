# Weight and proportions

Virtua aims for monolinear apparent stroke weight. Identify which contour edges,
alignments, counters and straight-to-curve boundaries are fixed for the specific
glyph before transferring weight. Counter reduction is an established Latin
construction pattern; do not assume every Arabic/Hebrew outer contour is fixed.

Use live green O/H/n/o and same-script donors, checking source grades at lookup.
Measure the current sources with `fgtools check-design --observe`; the
stroke ranges are in `sources/design.toml`. Script-wide weight remains subject
to cross-script visual review.

Transfer construction relationships rather than scaling all coordinates or
translating every turn with a thicker bar. Inspect opposing-edge weight, full
silhouette and shaped words. Zayin Bold's compact turn and hamza's unequal handles
show why one universal handle ratio is insufficient.

## More weights

The family is planned from Thin (100) to Black (900). `make draft-weights`
calculates the Thin and Black masters from Regular and Bold and writes them
to `out/weights/`, with a variable font of all four masters. The targets of
each weight are the `[weights.<name>]` tables of `sources/design.toml`. The
drafts become masters of the designspace only after Regular and Bold are
approved, because the calculation makes every difference between the two
masters larger. The work is described in `.agents/tasks/weight-masters.md`
and `.agents/tasks/italic-masters.md`.

## Rules

The rules of this subject are numbered in `context.md`.
