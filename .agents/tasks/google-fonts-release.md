# Task: prepare the Google Fonts submission

## Goal

The repository and the built fonts meet the current Google Fonts guide, so
that Eli can open the Add Font issue. Drawing approval is out of scope: the
glyphs that are not green stay Eli's work.

## Acceptance

- Each requirement on these pages is met, or listed in the report with the
  reason it is not. Read the pages at the start of the task; do not use an
  older copy:
  - https://googlefonts.github.io/gf-guide/upstream.html
  - https://googlefonts.github.io/gf-guide/onboarding.html
  - https://googlefonts.github.io/gf-guide/requirements.html
  - https://googlefonts.github.io/gf-guide/variable.html
  - https://googlefonts.github.io/gf-guide/metadata.html
  - https://googlefonts.github.io/gf-guide/article.html
  - https://googlefonts.github.io/gf-guide/diacritics.html
- `README.md` has a short description, the build instructions and an image
  that is committed under `documentation/`.
- `make build` succeeds, and `make qa-full` reports no
  FAIL, except `googlefonts/repo/dirname_matches_nameid_1`, which applies
  to the google/fonts package directory and not to this repository.
- Each WARN of the full profile is corrected, or listed in the report with
  the reason. Outline warnings (`outline_*`, `contour_count`,
  `overlapping_path_segments`, `interpolation_issues`) are listed with the
  glyph names for Eli, not corrected.
- A local package built as the `google-fonts-release` skill describes
  passes `make qa-package PACKAGE=<directory>` with no FAIL.
- The report contains the text of the Add Font issue, from the template at
  https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md.
- `make test-tools` passes.

## Baseline

On 2026-11-10 the full profile gave 1 FAIL (`dirname_matches_nameid_1`) and
36 WARN. On 2026-11-11 all 70 tests passed.

## Constraints

- Work on a new branch `omp/google-fonts-release` from `main`. Do not push,
  tag, publish, open issues or pull requests, or sign agreements.
- Do not change glyph outlines, mark colors or the family name.
- Engineering changes are allowed: `fontinfo.plist` values, features, the
  build configuration, the scripts, `README.md` and the documentation.
- Follow the layout rules in `AGENTS.md`. Put findings in the report, not in
  new files. Generated output goes under `out/`.

## Autonomy

- Make the engineering decisions that the guide determines.
- Ask Eli about decisions that the guide leaves to the designer: the family
  name, the copyright string, the designer profile, the article text and the
  README image. If he is not available, list them in the report and continue
  with the other work.

## Done

Report the requirements met, the requirements not met with their reason,
the remaining WARN results, the outline warnings by glyph, the commands run
with their results, and the Add Font issue text.
