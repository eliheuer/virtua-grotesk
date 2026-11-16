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
- `out/accent-proofs/verdicts.json` has one verdict for each accented letter
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
3. Run `.venv/bin/fgtools render-accent-proofs`. Read `out/accent-proofs/review.json` and look
   at every sheet. The letters with findings are on the first sheets.
4. Review each letter with the `accent-review` skill. If the harness has
   subagents, a different agent does the review. Give it the sheets and
   `review.json`, and not the notes of the build.
5. Correct a purple letter that has the verdict `fault`: change the offset of
   its mark component, on the grid of `CONTEXT.md`, the same way in
   every master. Then do steps 3 and 4 again for the changed letters
   (`.venv/bin/fgtools render-accent-proofs --glyphs "<names>" --out out/accent-proofs/again`).
   Stop after three rounds for one letter and give it the verdict `designer`.

## Constraints

- Work on a new branch from `main`. Do not push, merge or tag.
- Change only purple accented letters, and the anchors that
  `place-anchors` adds. An accented letter of another color with the verdict
  `fault` goes into the report and does not change.
- Do not change a base letter, a mark, or an anchor that is in the sources.
- The reference fonts are for comparison. A position that differs from them
  is a finding to judge. It is not a fault by that fact alone.
- Do not add files to the repository. Write output under `out/`.

## Done

Report the counts: letters added, verdicts of each kind for each master.
Then list the letters with the verdict `fault` or `designer`, each with its
sheet, its numbers and the reason in one line, the largest difference first.
Then list the letters that were not built, and the green glyphs without
anchors.
