# Downstream Metadata Diff

This generated report compares the local Packager-created downstream
`METADATA.pb` with the expected repository preview. It is intentionally
a review aid only; it does not apply maintainer decisions or edit the
local `google/fonts` checkout.

## Summary

- Expected preview: `documentation/google-fonts/google-fonts-downstream-package-preview.md`
- Actual downstream metadata: `GF_REPO_PATH_NOT_CONFIGURED/ofl/virtuagrotesk/METADATA.pb`
- Actual downstream METADATA.pb present: no
- Actual downstream METADATA.pb is starter template: no
- Starter-template markers present: 0 / 4
- Expected metadata lines missing from actual downstream file: 22 / 22
- Actual downstream `source.config_yaml` present: no
- Expected preview `source.config_yaml` present: no
- Expected preview has final `date_added`: no
- Unexpected starter source mappings: 0
- Prepare helper source mode: `latest-release`
- Ready to apply preview via helper: no
- Prepare helper blocking findings: 4
- Prepare helper required-line count: 22
- Diff/helper required-line lists match: yes

## Starter Template Markers

- None

## Missing Expected Lines

- `name: "Virtua Grotesk"`
- `license: "OFL"`
- `category: "SANS_SERIF"`
- `filename: "VirtuaGrotesk[wght].ttf"`
- `post_script_name: "VirtuaGrotesk-Regular"`
- `full_name: "Virtua Grotesk Regular"`
- `subsets: "arabic"`
- `subsets: "latin"`
- `subsets: "menu"`
- `tag: "wght"`
- `min_value: 400.0`
- `max_value: 700.0`
- `source_file: "OFL.txt"`
- `dest_file: "OFL.txt"`
- `source_file: "fonts/variable/VirtuaGrotesk[wght].ttf"`
- `dest_file: "VirtuaGrotesk[wght].ttf"`
- `source_file: "documentation/google-fonts/ARTICLE.en_us.html"`
- `dest_file: "article/ARTICLE.en_us.html"`
- `source_file: "documentation/assets/readme-specimen.png"`
- `dest_file: "article/readme-specimen.png"`
- `primary_script: "Arab"`
- `stroke: "SANS_SERIF"`

## Actual Source Mappings Not In Preview

- None

## Replacement Readiness Gate

This mirrors the same validation used by `make downstream-metadata-check`.
It intentionally does not run `--apply` or write to the local
`google/fonts` checkout.

- Source mode: `latest-release`
- Ready to apply: no
- Apply command intentionally not run: yes
- Check command: `make downstream-metadata-check`
- Apply command after all blockers clear: `scripts/prepare_downstream_metadata.py --apply`

Blocking findings:
- blocked marker still present: Pending final
- required metadata line missing: date_added with final valid "YYYY-MM-DD" Google Fonts date
- required metadata line missing: source.commit with final 40-character lowercase git hash
- google/fonts checkout does not exist: GF_REPO_PATH_NOT_CONFIGURED

## Prepare Helper Alignment

The dry-run/apply helper must reject the same required-line
regressions this report tracks, otherwise a bad preview could be
written into the local `google/fonts` fork before the diff report
flags it.

- Expected lines in diff report: 22
- Required lines in prepare helper: 22
- Date-added format validation in prepare helper: yes
- Source commit hash validation in prepare helper: yes
- Latest-release archive URL validation in prepare helper: yes
- Missing from helper: none
- Extra in helper: none
- Date-added final requirement: `date_added with final valid "YYYY-MM-DD" Google Fonts date`

## Apply Before Rerunning Packager

- Replace the Packager starter template with the final downstream
  metadata after the selected release/archive commit, branch,
  archive, and `date_added` value are settled.
- First run `make downstream-metadata-check` to validate the preview
  without writing to the local `google/fonts` checkout.
- When that dry run reports `Ready to apply: yes`, run
  `scripts/prepare_downstream_metadata.py --apply` to write
  `$GF_REPO_PATH/ofl/virtuagrotesk/METADATA.pb`.
- Use `documentation/google-fonts/google-fonts-downstream-package-preview.md` as
  the expected shape, then rerun `make preflight` so proof evidence
  and generated reports stay synchronized before
  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.
- Keep `source.config_yaml` only when the selected Packager source mode
  is build-from-source, unless Google Fonts review asks for build metadata.
- Keep the first rerun as a no-PR dry run until the generated package
  is reviewed.
