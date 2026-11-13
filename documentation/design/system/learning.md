# Learning loop

This document defines how design work is checked, and where a correction is
recorded. The aim is to keep what the project learns without adding a file for
each event.

## The loop

1. **Choose.** `make queue` ranks the glyphs that most composites wait on.
   Eli names the glyphs to draw.
2. **Draft.** An agent or a model drafts the glyph as a Runebender proposal,
   or in the source with a purple mark. The draft is committed before Eli
   edits it.
3. **Measure.** `make check-design GLYPHS="..."` compares the draft with the
   targets in [design.toml](../../../sources/design.toml). Correct the findings before
   review. A pass is a filter, not approval.
4. **Review.** Eli compares the glyph with the reference fonts in Runebender
   or `make proof-web`, then corrects it or marks it green. The correction is
   committed.
5. **Learn.** Turn repeated corrections into rules, as described below.

## The trace is the Git history

The draft commit and the correction commit are the record of a decision. Do
not copy drafts, corrections, hashes or receipts into files. To read a trace:

```sh
git log --follow -p -- sources/VirtuaGrotesk-Regular.ufo/glyphs/<file>.glif
```

## Turn repeated corrections into rules

A correction is the difference between an agent's purple draft and Eli's next
edit of the same glyph. The Git history holds both, so no record is written
when a correction is made.

When Eli asks, an agent reads the recent draft and correction pairs: the
diffs, renders before and after, and Eli's commit messages. It proposes rule
entries for mistakes that repeat. Eli approves or rejects each entry.

- One correction is not a rule.
- When the same mistake occurs again, add the glyph and commit to the
  existing entry. Do not write a second entry.

A rule entry has this form:

```markdown
### Turns keep one direction of curvature

A convex turn must not reverse its curvature. Read the comb before review.
Seen in: hamzaabove-ar Bold (a1b2c3d4), at Regular (e5f6a7b8).
```

If a script can test the rule (a number, a range, a grid), put the value in
`sources/design.toml` or the check in `scripts/check_design.py`, and keep only
the reason in the rule document. If a correction shows a decision that a
drafting method has to learn, add the glyph to `sources/held-out-glyphs.toml`
when it is green. If a correction applies to one glyph only and a later agent would
repeat the error, add one line to its record in [glyphs/](../glyphs/README.md).

A rule document has at most 200 lines; the layout test enforces this. When a
document is full, merge entries or move checkable values into scripts.

## Checks and their limits

`scripts/check_design.py` uses Runebender for measurement and holds the
Virtua policy. On 2026-11-10 the checks passed 50 of the 72 glyphs that are
green in both masters. The other 22 are approved drawings that the checks
flag: 5 icon glyphs with corners that the analyzer reports as kinks, and 17
letters and figures, most with a stroke that crosses a junction or a
diagonal. Thus a finding is a prompt to look, not an error.

Run `check_design.py --green` after a change to the targets or the checks.
If fewer green glyphs pass, the change made the checks worse.

Stroke targets exist only where green glyphs exist: Regular Latin, Regular
Arabic and Bold Latin. Add targets for Bold Arabic and Hebrew with
`check_design.py --observe` when those scripts have green glyphs.

## Drafting evaluation

`scripts/evaluate_drafting.py` tests a drafting method (an agent, a model or
a script) on green glyphs that it has not seen. The glyphs are in
`sources/held-out-glyphs.toml`, in four tasks:

| Task | The method gets | It must |
| --- | --- | --- |
| redraw | the sources without the glyph | draw the glyph in both masters |
| bold | the green Regular, without the Bold | draw the Bold |
| repair | the glyph with some points moved | move the points back |
| relatives | green glyphs of the same construction | draw the glyph from them |

1. `make prepare-drafting TASK=bold RUN=out/drafting/bold-1` copies the
   sources to `RUN/sources` and sets the task.
2. The method edits only `RUN/sources`. A method that reads `sources/` or the
   Git history has seen the references, so its score is not valid.
3. `make score-drafting RUN=...` scores the overlap and distance from Eli's
   drawing, the master compatibility, the grid and the project checks.
4. `make compare-drafting A=... B=...` compares two runs of the same task.

Baselines on 2026-11-12: for bold, the Regular copied into the Bold scores a
mean overlap of 0.585 and a mean distance of 32.6 units. For repair, the
moved glyphs without a repair score 0.962 and 2.3 units. A method is useful
only if it scores better than these.

## Grades

Eli approves contour glyphs. A composite is green when its parts are green
and `check_design.py --ready` lists it. An agent can mark such a composite
green. Model scores and evaluation scores do not approve a glyph.

Training data comes from green glyphs only. Keep the glyphs of one
construction family, and the two masters of one glyph, on the same side of a
training and evaluation division.
