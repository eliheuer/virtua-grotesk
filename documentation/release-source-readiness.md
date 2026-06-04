# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `e30fc2fdfc541b2832ac6de68902eae8478fedcf`
- Origin URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`
- Normalized origin differs from placeholder: yes
- Source version from release metadata: `1.000`
- Suggested tag from release metadata: `v1.000`
- Suggested tag matches source version: yes
- Suggested tag exists locally: no
- Working tree clean: no
- Branch upstream: `origin/main`
- Ahead/behind branch upstream: `2	0`
- Ahead/behind origin branch: `2	0`
- Placeholder upstream URL still present: no
- Pending source fields in downstream preview: 1
- Downstream `source.files` entries: 4
- Downstream source destination mapping ready: yes
- Downstream source mapping is variable-font-first: yes
- Missing local `source.files`: 0
- Ignored/generated `source.files`: 1
- Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`
- Local google/fonts fork exists: yes
- Local google/fonts branch: `main`
- Local google/fonts main vs upstream/main: `0	0`
- Local google/fonts worktree clean: no
- Local google/fonts dirty paths inside `ofl/virtuagrotesk`: 1
- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0
- Local google/fonts dirty state isolated to `ofl/virtuagrotesk`: yes

## Current Repo Git State

| Field | Value |
| --- | --- |
| branch | `main` |
| commit | `e30fc2fdfc541b2832ac6de68902eae8478fedcf` |
| short commit | `e30fc2f` |
| origin | `git@github.com:eliheuer/virtua-grotesk.git` |
| normalized GitHub origin candidate | `https://github.com/eliheuer/virtua-grotesk` |
| upstream | `origin/main` |
| upstream ahead/behind | `2	0` |
| origin ahead/behind | `2	0` |
| source version | `1.000` |
| suggested tag | `v1.000` |
| suggested tag matches source version | yes |
| suggested tag exists | no |

## Current Dirty State

- `M documentation/arabic-mark-readiness.md`
- ` M documentation/arabic-pending-source-checkpoint.md`
- ` M documentation/arabic-source-edit-diff.md`
- ` M documentation/fontspector-contour-count.md`
- ` M documentation/fontspector-googlefonts-report.md`
- ` M documentation/fontspector-metadata-warning-probe.md`
- ` M documentation/fontspector-warnings.md`
- ` M documentation/github-release-draft.md`
- ` M documentation/github-release-notes.md`
- ` M documentation/release-archive-manifest.md`
- ` M documentation/release-source-readiness.md`
- ` M documentation/upstream-structure-readiness.md`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/ain-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/ain-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/alefM_aksura-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/alefM_aksura-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/behD_otless-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/behD_otless-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/eight-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/eightFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/farsiYeh-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/fehD_otless-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/fehD_otless-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/five-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/fiveFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/four-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/fourFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/hah-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/hah-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/hah-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/heh-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/jeem-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/kaf-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/kaf-ar.init.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/kaf-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/keheh-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/keheh-ar.init.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/keheh-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/lam_alef-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/meem-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/meem-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/meem-ar.init.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/meem-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/nine-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/nineFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/noonghunna-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/noonghunna-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/qafD_otless-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/qafD_otless-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/reh-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/sad-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/sad-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/sad-ar.init.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/sad-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/shadda-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/tah-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/tah-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/tah-ar.init.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/tah-ar.medi.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/three-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/threeFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/ain-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/ain-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/alefM_aksura-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/alefM_aksura-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/behD_otless-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/behD_otless-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/eight-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/eightFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/farsiYeh-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/fehD_otless-ar.fina.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/fehD_otless-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/five-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/fiveFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/four-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/fourFarsi-ar.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/hah-ar.fina.glif`
- ... 36 more entries omitted

## Downstream Source Mapping

| Source file | Destination file | Local status |
| --- | --- | --- |
| `OFL.txt` | `OFL.txt` | present and not ignored |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | ignored/generated |
| `documentation/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | present and not ignored |
| `documentation/readme-specimen.png` | `article/readme-specimen.png` | present and not ignored |

## Pending Downstream Source Fields

- `commit: "Pending final release/source commit"`

## Local google/fonts Fork

| Field | Value |
| --- | --- |
| path | `/Users/eli/GH/forks/fonts` |
| exists | yes |
| branch | `main` |
| origin | `git@github.com:eliheuer/fonts.git` |
| upstream | `https://github.com/google/fonts.git` |
| main vs upstream/main | `0	0` |
| dirty entries | 1 |
| dirty inside `ofl/virtuagrotesk` | 1 |
| dirty outside `ofl/virtuagrotesk` | 0 |
| dirty isolated to `ofl/virtuagrotesk` | yes |

## Apply Before Final Packager Run

- Keep the decided public upstream URL synchronized with OFL, source
  metadata, Article links, handoff text, and downstream metadata.
- Use the selected release/archive source strategy for the first
  Packager pass unless Google Fonts review asks for another mode.
- Ensure the final release archive contains every mapped
  `source.files` path before the latest-release Packager run.
- Create or update the final upstream tag only after drawing/source
  work and maintainer decisions are complete.
- Record the final repository URL, commit, branch, GitHub release download `.zip` URL, and source mode in
  `documentation/google-fonts-downstream-package-preview.md`.
- Rerun `make preflight` so proof evidence and generated reports
  stay synchronized, then run
  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` from
  an aligned local `google/fonts` fork.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
