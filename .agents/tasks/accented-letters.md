# Task: build and review the accented letters

Start this task with the set of accented letters from the designer. Without
one, the set is `google-fonts-latin-core`. The base letters and the marks
are drawn already. This task does not draw.

## Goal

Each accented letter of the set is in every master as a composite of its
base letter and its mark. Each new one is purple. Each accented letter has a
review verdict that comes from the proof sheets, and the designer gets the
list of the letters to look at.

## Acceptance

- `.venv/bin/fgtools build-accented-letters` lists 0 accented letters to
  add. The letters that it does not build are in the report with the reason.
- `.venv/bin/fgtools render-accent-proofs` ran after the last change, with the reference fonts.
- `output/accent-proofs/verdicts.json` has one verdict for each accented letter
  of each master: `correct`, `fault` or `designer`, with a reason for the
  last two.
- No purple accented letter has the verdict `fault`.
- `.venv/bin/fgtools check-changes --allow-other` prints PASS.
- `make build` succeeds, and `make test` passes.

## Method

1. Run `.venv/bin/fgtools place-anchors`, read the list, then run it with
   `--write`. It adds only the anchors that are missing. It leaves out green
   glyphs; list those in the report.
2. Run `.venv/bin/fgtools build-accented-letters`, read the list, then run
   it with `--write`.
3. Run `.venv/bin/fgtools render-accent-proofs`. Read `output/accent-proofs/review.json` and look
   at every sheet. The letters with findings are on the first sheets.
4. Review each letter and write a verdict (see "Review" below). If the
   harness has subagents, a different agent does the review. Give it the
   sheets, `review.json` and `CONTEXT.md`, and not the notes of the build.
5. Correct a purple letter that has the verdict `fault`: change the offset of
   its mark component, on the grid of `CONTEXT.md`, the same way in
   every master. Then do steps 3 and 4 again for the changed letters
   (`.venv/bin/fgtools render-accent-proofs --glyphs "<names>" --out output/accent-proofs/again`).
   Stop after three rounds for one letter and give it the verdict `designer`.

## Review

A row of a sheet is one accented letter: the project in the first column,
then each reference font at the same x-height or cap height. `review.json`
has, for each letter, `position` (the center of the mark as a share of the
width of the base; 0.5 is the center), `gap` (the distance between base and
mark as a share of the x-height; negative is an overlap), the range of both
in the reference fonts, and the findings.

Look at the picture first, then at the numbers. Look at every letter, not
only at the letters with findings. Compare a letter with the other letters
of the project that have the same mark, then with the reference fonts, and
check it against rules 57 to 60 of `CONTEXT.md`. The build command does not
build the caron of d, t, l and L or the comma accent of g.

Write `output/accent-proofs/verdicts.json`:

```json
{"Regular": {"kcaron": {"verdict": "fault", "reason": "The caron is at the x-height and cuts into the ascender."}}}
```

- `correct`: the picture agrees with the rules and with the other letters of
  the project. A finding does not prevent this verdict; give the reason.
- `fault`: the letter breaks a rule in a way that every designer would
  correct.
- `designer`: the position is a possible decision of the design, or the
  evidence does not decide. Name the decision.

If the project differs from all reference fonts in the same way on many
letters, that is a decision of the design, and one line in the report
describes it. A verdict is not approval. Only the designer makes a letter
green.

## Constraints

- Work on a new branch from `main`. Do not push, merge or tag.
- Change only purple accented letters, and the anchors that
  `place-anchors` adds. An accented letter of another color with the verdict
  `fault` goes into the report and does not change.
- Do not change a base letter, a mark, or an anchor that is in the sources.
- The reference fonts are for comparison. A position that differs from them
  is a finding to judge. It is not a fault by that fact alone.
- Do not add files to the repository. Write output under `output/`.

## Done

Report the counts: letters added, verdicts of each kind for each master.
Then list the letters with the verdict `fault` or `designer`, each with its
sheet, its numbers and the reason in one line, the largest difference first.
Then list the letters that were not built, and the green glyphs without
anchors.
