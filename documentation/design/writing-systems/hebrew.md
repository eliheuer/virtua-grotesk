# Hebrew context

Use approved Virtua construction and Hebrew-specific distinctions. The Hebrew
reference fonts (Rubik, Noto Sans Hebrew, Heebo, IBM Plex Sans Hebrew and
Assistant) provide script/reading comparisons; their skeletons do not override the project's
terminals, turns or deliberate shelves. Preserve saved Zayin, Gimel and Final Tsadi
corrections and any green component donors.

Hebrew marks share the family's machined construction and chamfers where applicable.
Check base/mark and mark-to-mark attachment with actual compiled shaping at multiple
weights. Coverage alone does not establish drawing or attachment quality. The
Hebrew-to-Latin optical weight relationship remains provisional.

The review sequence `design/reviews/hebrew-001/` to `hebrew-010/` is in the
Git history before commit 1db2dfc7.

## Rule entries

### Stroke weights

The verticals are 96, the Latin lowercase stem. The horizontals are 88, the
Latin crossbar: 0.92 of the stem. Monoline Hebrew looks heavy beside the
Latin, and the 0.79 to 0.88 of the reference fonts is more contrast than this
grotesque has. Both values are on the 8-unit grid. `[targets.Regular.Hebrew]`
in `sources/design.toml` holds the ranges that `make check-design` uses.
Decided by Eli on 2026-11-15, from a measurement of the five Hebrew
reference fonts.

### Rubik is the structural reference

When a Hebrew letter looks wrong, compare its skeleton with Rubik. If the
structure is very different, follow Rubik's structure and draw it with
Virtua's chamfers, grid and own forms. Simplify rather than add.
Seen in: zayin shin finaltsadi samekh (4e900dd0, df38c4a2), gimel (3814ca96).

### Geometric does not mean rectangular

Keep oval bowls and counters. Remove only organic irregularity.
Seen in: samekh v4, rejected by Eli (df38c4a2).
