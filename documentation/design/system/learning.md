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
   targets in [contract.json](contract.json). Correct the findings before
   review. A pass is a filter, not approval.
4. **Review.** Eli compares the glyph with the reference fonts in Runebender
   or `make proof-web`, then corrects it or marks it green. The correction is
   committed.
5. **Interpret.** Classify the correction, as the next section describes.

## The trace is the Git history

The draft commit and the correction commit are the record of a decision. Do
not copy drafts, corrections, hashes or receipts into files. To read a trace:

```sh
git log --follow -p -- sources/VirtuaGrotesk-Regular.ufo/glyphs/<file>.glif
```

Write the reason for a correction in the commit message.

## Three outcomes of a correction

Each correction has one of three outcomes. Each outcome has one location.
If none applies, record nothing.

| Outcome | Meaning | Location |
| --- | --- | --- |
| Exception | The correction applies to this glyph only, or the feedback is ambiguous. | A short record in [glyphs/](../glyphs/README.md), only if a later agent would repeat the error. |
| Reusable decision | The same decision will occur in other glyphs. | A case in `tests/benchmark.json`. The green drawing is the reference. |
| System gap | A target, check or rule was wrong or absent. | A change to `contract.json`, `scripts/check_design.py` or one rule document. |

A correction is not a rule by default. Add a rule only when the same
correction occurred in more than one glyph. When a rule changes, edit the
rule document. Do not add a second document.

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

`scripts/benchmark.py` hides the green glyphs listed in `tests/benchmark.json`
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
