# Release Source Readiness

This generated report ties the final Google Fonts Packager source
strategy to the current git state, release tag recommendation,
downstream `source.files`, and local `google/fonts` fork. It is the
handoff check for the source state that `METADATA.pb` will claim.

## Summary

- Current repo branch: `main`
- Current repo commit: `26e0236674a98c7700b1ab639deeab2dcec4fff8`
- Origin URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`
- Normalized origin differs from placeholder: yes
- Source version from release metadata: `1.000`
- Suggested tag from release metadata: `v1.000`
- Suggested tag matches source version: yes
- Suggested tag exists locally: no
- Working tree clean: no
- Branch upstream: `origin/main`
- Ahead/behind branch upstream: `0	0`
- Ahead/behind origin branch: `0	0`
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
| commit | `26e0236674a98c7700b1ab639deeab2dcec4fff8` |
| short commit | `26e0236` |
| origin | `git@github.com:eliheuer/virtua-grotesk.git` |
| normalized GitHub origin candidate | `https://github.com/eliheuer/virtua-grotesk` |
| upstream | `origin/main` |
| upstream ahead/behind | `0	0` |
| origin ahead/behind | `0	0` |
| source version | `1.000` |
| suggested tag | `v1.000` |
| suggested tag matches source version | yes |
| suggested tag exists | no |

## Current Dirty State

- `M .claude/rules/design-philosophy.md`
- ` M .claude/rules/designspace-editing.md`
- ` M .claude/rules/kerning-editing.md`
- ` M .claude/rules/ufo-editing.md`
- ` M .claude/settings.json`
- ` M .claude/skills/build-font/SKILL.md`
- ` M .claude/skills/edit-glyph/SKILL.md`
- ` M .claude/skills/font-qa/SKILL.md`
- ` M .claude/skills/proof/SKILL.md`
- ` M .claude/skills/render-specimen/SKILL.md`
- ` M .gitignore`
- ` M AUTHORS`
- ` M CLAUDE.md`
- ` M OFL.txt`
- ` M README.md`
- ` M build.sh`
- ` M designbot/001.rs`
- ` M designbot/002.rs`
- ` M designbot/card.rs`
- ` M proof.pdf`
- ` M proof.py`
- ` M sources/VirtuaGrotesk-Bold.ufo/features.fea`
- ` M sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/aacute.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/contents.plist`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/exclam.glif`
- ` D sources/VirtuaGrotesk-Bold.ufo/glyphs/newG_lyph.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/quotedblleft.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
- ` M sources/VirtuaGrotesk-Bold.ufo/lib.plist`
- ` M sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/aacute.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/contents.plist`
- ` D sources/VirtuaGrotesk-Regular.ufo/glyphs/newG_lyph.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/glyphs/quotedblleft.glif`
- ` M sources/VirtuaGrotesk-Regular.ufo/lib.plist`
- ` M sources/VirtuaGrotesk.designspace`
- ` D sources/kinderhugel-grotesk-bold.ufo/features.fea`
- ` D sources/kinderhugel-grotesk-bold.ufo/fontinfo.plist`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/A_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/B_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/C_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/D_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_000.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_004.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_005.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_006.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_007.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_008.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_009.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_010.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_011.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_012.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_013.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_014.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_015.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_016.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_017.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_018.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_019.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_020.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/E_021.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/F_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/F_001.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/F_002.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/F_003.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/G_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/H_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/I_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/J_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/K_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/L_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/M_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/N_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/O_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/P_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/Q_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/R_.glif`
- ` D sources/kinderhugel-grotesk-bold.ufo/glyphs/S_.glif`
- ... 267 more entries omitted

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
