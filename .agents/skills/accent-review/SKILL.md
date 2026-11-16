---
name: accent-review
description: Review where the marks of the accented letters sit, from the accent proof sheets and the measurements against the reference fonts, and give each letter a verdict. Use after accented letters are built or changed, or when asked whether the accents are placed correctly.
---

# Review the accented letters

```sh
.venv/bin/fgtools render-accent-proofs  # sheets and review.json in out/accent-proofs/
.venv/bin/fgtools check-accents         # the same project findings as text
```

`render-accent-proofs` needs the shared reference fonts
(`FONTGARDEN_REFERENCE_FONTS`, see `fgtools fetch-reference-fonts`).

## Read the evidence

A row of a sheet is one accented letter: the project in the first column,
then each reference font at the same x-height or cap height. The lines are
the baseline and the x-height or the cap height. `review.json` has, for each
letter, `position` (the center of the mark as a share of the width of the
base, 0.5 is the center), `gap` (the distance between base and mark as a
share of the x-height, negative is an overlap), the range of both in the
reference fonts, and the findings.

Look at the picture first, then at the numbers. Look at every letter, not
only at the letters with findings. Compare a letter with the other letters
of the project that have the same mark, and then with the reference fonts.

## What a correct accented letter looks like

- A mark has one height over all letters of one height. Over an ascender
  (h, k, l, b, d) and over a capital letter, the mark is above the letter.
  A mark at the x-height that cuts into an ascender is a fault.
- i and j have no dot under a top mark.
- A symmetric mark (dieresis, macron, circumflex, caron, breve, ring, tilde,
  dot) is on the optical center of the letter. On a symmetric letter that is
  the center of its width.
- An acute or a grave points at the center with its lower end. Its bounding
  box is then to the right (acute) or to the left (grave) of the center.
- On a letter that is not symmetric (L, h, k, r, t, f, J), the position is a
  decision of the design: over the stem or over the width. All letters of
  one font follow one decision.
- A cedilla joins the bottom of the bowl of C and S at its center. An ogonek
  joins the letter at the bottom right (A, a, E, e, U, u) or at the stem
  (I, i), without a gap. A comma accent is under the center with a clear gap.
- The caron of d, t, l and L is an apostrophe form at the right of the
  letter. The comma accent of g is a turned comma over the letter. The build
  command does not build these.
- A mark does not touch another part of the letter that it is not designed
  to join, and is not cut by the letter.
- The masters agree: the same components, and the same relative position.

## Verdicts

Write `out/accent-proofs/verdicts.json`:

```json
{"Regular": {"kcaron": {"verdict": "fault", "reason": "The caron is at the x-height and cuts into the ascender."}}}
```

- `correct`: the picture agrees with the rules above and with the other
  letters of the project. A finding does not prevent this verdict. Give the
  reason if the letter has a finding.
- `fault`: the letter breaks a rule above in a way that every designer would
  correct.
- `designer`: the position is a possible decision of the design, or the
  evidence does not decide. Name the decision.

The reference fonts do not dictate the design. If the project differs from
all of them in the same way on many letters, that is a decision of the
design, and one line in the report describes it.

A verdict is not approval. The designer grades the letters, and only the
designer makes a letter green.
