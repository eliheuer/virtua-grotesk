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
5. **Interpret.** Record the correction and count repeats, as the next
   sections describe.

## The trace is the Git history

The draft commit and the correction commit are the record of a decision. Do
not copy drafts, corrections, hashes or receipts into files. To read a trace:

```sh
git log --follow -p -- sources/VirtuaGrotesk-Regular.ufo/glyphs/<file>.glif
```

## Record a correction in the commit message

A commit that corrects a drawing has one line for each correction:

```
Correction: <topic>: <what was wrong, in one sentence>
```

For example, `Correction: curves: the lower-left turn reversed its curvature`.
The topics are in the `[lessons]` table of `sources/design.toml`. Each topic
names one rule document. When Eli corrects a draft, the agent that commits
the correction asks Eli what was wrong if the reason is not clear, then
writes the line. No file is written.

## Turn repeated corrections into rules

`make lessons` counts the correction lines by topic. A correction is
recorded when its commit hash appears in the rule document of its topic.

- One correction is not a rule. Leave it in the commit message.
- When a topic has two or more unrecorded corrections of the same kind, the
  agent proposes one rule entry in the rule document of that topic. Eli
  approves it before it is committed.
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
drafting method has to learn, add the glyph to `tests/benchmark.toml` when it
is green. If a correction applies to one glyph only and a later agent would
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

## Benchmark

`scripts/benchmark.py` hides the green glyphs listed in `tests/benchmark.toml`
in a copy of the sources, then scores a redrawn copy against the green
drawings. Use it to compare two drafting methods or two models on the same
cases. A method that reads `sources/` or the Git history has seen the
references, so its score is not valid.

Baseline on 2026-11-10, where each held-out glyph is replaced by the same
glyph from the other master: mean overlap 0.546, mean outline distance 34.2
units. A drafting method is useful only if it scores better than this.

## Grades

Eli approves contour glyphs. A composite is green when its parts are green
and `check_design.py --ready` lists it. An agent can mark such a composite
green. Model scores and benchmark scores do not approve a glyph.

Training data comes from green glyphs only. Keep the glyphs of one
construction family, and the two masters of one glyph, on the same side of a
training and evaluation division.
