# Package Source Files Audit

This generated report checks the local files listed in the expected
`METADATA.pb` `source.files` block before a Google Fonts Packager dry run.
It does not prove the files are public on GitHub; it shows which files are
present locally and which are ignored/generated, so the selected
GitHub release/archive source strategy can be checked deliberately.

## Summary

- Mapping source: `documentation/google-fonts-downstream-package-preview.md`
- Expected `source.files` entries: 4
- Missing local files: 0
- Ignored local files: 1
- Tracked `source.files`: 3 / 4
- Untracked local `source.files`: 1
- Destination mapping matches expected downstream layout: yes
- Unsafe `source.files` paths: 0
- Duplicate `source.files` paths: 0
- Unsafe `dest_file` paths: 0
- Duplicate `dest_file` paths: 0
- Variable-font-first source mapping: yes
- Static TTFs generated locally for QA: 4 / 4
- Static TTFs included in `source.files`: 0
- Downstream `static/` destinations planned: 0
- Static package omission documented in preview: yes
- Article assets map into `article/`: yes
- Build-from-source inputs tracked: 6 / 6
- Build script uses `gftools builder sources/config.yaml`: yes
- Build script runs metadata post-processing: yes
- Builder config outputs to `fonts/`: yes
- `branch` field present for default/source-build mode: yes
- `archive_url` present for selected release/archive strategy: yes
- `archive_url` is GitHub release download `.zip`: yes
- Expected Packager branch name: `gftools_packager_ofl_virtuagrotesk`

## Expected Packager Source Files

| Source file | Destination file | Purpose | Exists locally | Ignored by git | Tracked by git | Destination OK |
| --- | --- | --- | --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | license | yes | no | yes | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | served variable font | yes | yes | no | yes |
| `documentation/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | article HTML | yes | no | yes | yes |
| `documentation/readme-specimen.png` | `article/readme-specimen.png` | article image | yes | no | yes | yes |

## Source Strategy Impact

- Default Packager mode expects every `source_file` path above to be available from the public upstream branch recorded in `METADATA.pb`.
- `fonts/variable/VirtuaGrotesk[wght].ttf` is generated build output; if it stays ignored, the final package needs a release/archive strategy or an explicit build-from-source flow.
- `--latest-release` can work only after the public upstream release exposes the expected files through a GitHub release download `.zip` URL.
- `--build-from-source` can work only if Google Fonts accepts the repo build path and the required source/build files are public and reproducible.
- Packager creates a branch named like `gftools_packager_ofl_fontname`; for this family the expected branch is `gftools_packager_ofl_virtuagrotesk`.
- Static TTFs are generated for local QA, proofs, and release review,
  but are intentionally omitted from the preview package unless Google
  Fonts review asks for a downstream `static/` directory.

## Static Output Handling

| Static font output | Exists locally | Ignored by git | Included in source.files |
| --- | --- | --- | --- |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | yes | no |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | yes | no |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | yes | no |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | yes | no |

## Build-From-Source Inputs

| Path | Exists locally | Ignored by git | Tracked by git |
| --- | --- | --- | --- |
| `sources/config.yaml` | yes | no | yes |
| `sources/VirtuaGrotesk.designspace` | yes | no | yes |
| `sources/VirtuaGrotesk-Regular.ufo` | yes | no | yes |
| `sources/VirtuaGrotesk-Bold.ufo` | yes | no | yes |
| `build.sh` | yes | no | yes |
| `requirements.txt` | yes | no | yes |

## Build Command Evidence

| Check | Status |
| --- | --- |
| `build.sh` exists | yes |
| `build.sh` is tracked by git | yes |
| `build.sh` is not ignored | yes |
| `build.sh` invokes `gftools builder sources/config.yaml` | yes |
| `build.sh` runs `scripts/fix_gf_metadata.py` after build | yes |
| `sources/config.yaml` exists | yes |
| `sources/config.yaml` is tracked by git | yes |
| `sources/config.yaml` is not ignored | yes |
| `sources/config.yaml` builds `VirtuaGrotesk.designspace` | yes |
| `sources/config.yaml` outputs to `../fonts` | yes |

## Before Final Dry Run

- Keep the selected release/archive source strategy synchronized
  with `documentation/google-fonts-downstream-package-preview.md`.
- Confirm the final GitHub release/archive contains every
  `source.files` entry above at the same path.
- Confirm `source.archive_url` is the final GitHub release download
  URL ending in `.zip`.
- Confirm `documentation/google-fonts-downstream-package-preview.md` matches the final `source.files` mapping.
- Confirm no `source_file` or `dest_file` path is absolute, parent-relative, or duplicated.
- Regenerate this report with `make preflight` after changing the source strategy.

References:

- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
- https://googlefonts.github.io/gf-guide/upstream.html
