# Downstream Metadata Readiness

This generated report checks the draft downstream `METADATA.pb` preview
against the current built variable font and the expected Google Fonts
package source mapping. It does not replace a `gftools packager` run.

## Summary

- Preview file: `documentation/google-fonts/google-fonts-downstream-package-preview.md`
- Top-level family name present: yes
- Top-level designer string final: yes
- `date_added` final date present: no
- `date_added` current value: `Pending final Google Fonts date_added`
- `source.commit` final hash present: no
- `source.commit` current value: `Pending final release/source commit`
- Variable filename/name fields match built font: yes
- Weight axis min/max match built `fvar`: yes
- Variable font only in preview: yes
- Expected subsets present and sorted: yes
- `primary_script: "Arab"` present: yes
- `category: "SANS_SERIF"` present: yes
- `stroke: "SANS_SERIF"` present: yes
- Non-Noto `languages` entries absent: yes
- Custom `sample_text` absent: yes
- `tags` field absent from METADATA preview: yes
- Unneeded optional display/classification fields absent: yes
- Apply helper blocks unapproved optional metadata fields: yes
- Expected `source.files` present: yes
- Expected `source.files` destination mappings present: yes
- Source block has repository, commit, archive_url, and branch fields: yes
- `source.archive_url` present: yes
- `source.archive_url` required for latest-release mode: yes
- `source.archive_url` is GitHub release download `.zip`: yes
- `source.archive_url` satisfies latest-release mode: yes
- `source.config_yaml` present: no
- `source.config_yaml` needs source-strategy review: no
- Static style-name review uses GF `SemiBold` spelling: yes
- Pending or placeholder metadata lines: 2

## Built Variable Font Evidence

| Field | Built value |
| --- | --- |
| filename | `VirtuaGrotesk[wght].ttf` |
| name ID 1 | `Virtua Grotesk` |
| name ID 2 | `Regular` |
| name ID 4 | `Virtua Grotesk Regular` |
| name ID 6 | `VirtuaGrotesk-Regular` |
| name ID 0 | `Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)` |
| wght min/default/max | `400.0 / 400.0 / 700.0` |

## Preview Source Files

| Source file | Destination file | Mapping present | Source local file present |
| --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | yes | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | yes | yes |
| `documentation/google-fonts/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | yes | yes |
| `documentation/assets/readme-specimen.png` | `article/readme-specimen.png` | yes | yes |

## Source Mode Compatibility

| Source mode | `source.config_yaml` expectation | Preview status |
| --- | --- | --- |
| Default branch `source.files` | omit unless Google Fonts reviewer asks for build metadata | not selected |
| Latest release/archive | omit unless the archive strategy is explicitly paired with build metadata; keep final `archive_url` | selected and previewed |
| Build from source | keep `config_yaml: "sources/config.yaml"` | not selected |

`source.config_yaml` is omitted because the maintainer chose release/archive packaging. Keep it only for build-from-source, or if Google Fonts review asks for build metadata.

For `GFT_PACKAGER_SOURCE_MODE=latest-release`, the preview includes the intended final GitHub release download `.zip` `archive_url` documented by the Google Fonts package guide.

## Date Added Policy

The Google Fonts package guide notes that Packager automatically
adds `date_added` for a new-family package, and the metadata guide
defines it as the catalog date in `YYYY-MM-DD` format. Do not guess
this value while the upstream source state is still changing.

This repo keeps `date_added` as a blocking placeholder until the
final package pass. If the checked preview is applied manually before
Packager regenerates metadata, use the final package date supplied by
Packager or Google Fonts review, then rerun `make downstream-metadata-check`.

## Optional Metadata Field Policy

The current first-submission preview intentionally omits `languages`,
`display_name`, `minisite_url`, `classifications`, `sample_text`, and
`tags`. The apply helper treats those as review-gated fields and blocks
writing downstream `METADATA.pb` if any appear without an explicit
Google Fonts review decision.

## Pending Field Decision Map

| Preview field | Current blocker | Decision or evidence that unblocks it | Apply surface |
| --- | --- | --- | --- |
| `designer` | `Eli Heuer` | Matching designer profile or profile request | `documentation/google-fonts/google-fonts-downstream-package-preview.md`; designer catalog draft if needed |
| `copyright` | final URL applied; copyright-holder wording still reviewer/maintainer-owned | Confirm copyright-holder wording if it changes from project-author form | `OFL.txt`; source UFO fontinfo; metadata preview |
| `date_added` | `Pending final Google Fonts date_added` | Final Google Fonts package date, normally the Packager-generated date for the downstream PR | Metadata preview before applying to local `google/fonts` fork |
| `source.repository_url` | final public URL applied | Public canonical repository URL decision | Metadata preview; Add Font issue; handoff docs |
| `source.commit` | Pending final release/source commit | Final public source commit for the selected release/archive package | Metadata preview; release/source checklist |
| `source.branch` | `main` | Final public branch for release/archive provenance | Metadata preview; package dry-run command context |
| `source.config_yaml` | absent | Omit for release/archive unless Google Fonts review asks for build metadata | Metadata preview; prepare helper source mode |
| `source.archive_url` | intended `v1.000` GitHub release download `.zip` URL present | Release asset must be created after final source work | Metadata preview before `GFT_PACKAGER_SOURCE_MODE=latest-release` |

Do not apply the downstream metadata preview to the local `google/fonts`
fork until every pending field above has either a final value or an
explicit source-mode reason for being absent.

## Pending Or Placeholder Lines

- `documentation/google-fonts/google-fonts-downstream-package-preview.md:71` `date_added: "Pending final Google Fonts date_added"`
- `documentation/google-fonts/google-fonts-downstream-package-preview.md:91` `commit: "Pending final release/source commit"`

## Apply Before Downstream Packaging

- Replace the pending commit value after the final release/source
  commit.
- Replace the pending `date_added` value only with the final package
  date from Packager or Google Fonts review before applying downstream
  metadata.
- Create the final GitHub release archive before using latest-release
  packaging, and keep `source.archive_url` on a GitHub release
  download URL ending in `.zip`.
- Rerun `make preflight` after metadata-preview or build changes so
  proof evidence and generated reports stay synchronized.
- Run `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` only
  after the final release/archive source commit, archive, and downstream
  metadata are synchronized.

References:

- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
