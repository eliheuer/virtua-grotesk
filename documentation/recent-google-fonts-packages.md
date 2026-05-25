# Recent Google Fonts Package Audit

This generated report reads selected recently merged new-font examples from
the local `google/fonts` checkout. It keeps the template/PR audit tied to
actual downstream package files instead of a hand-written memory of recent
PRs.

## Local Checkout

- Path: `/Users/eli/GH/forks/fonts`
- Exists: yes
- Current commit: `c5b52261e`
- Status: `## main...origin/main`
- Dirty paths: 1
- Dirty `ofl/virtuagrotesk` paths: 1
- Alignment with `upstream/main`: `0 ahead, 0 behind`
- Alignment with `origin/main`: `0 ahead, 0 behind`
- Sample package directories present: 4 / 4
- Newest selected package example: google/fonts#10546 (Pliant, 2026-05-22)
- Newest Packager merge found locally: google/fonts#10546 (2026-05-22)
- Packager merges newer than selected examples: 0

## Package Examples

| PR | Family | Merged | Path | Present | Fonts | Article | upstream.yaml | upstream_info.md | primary_script | Subsets | Axes | Source repo | Source commit | archive_url | Source branch | config_yaml | tags field |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| google/fonts#10546 | Pliant | 2026-05-22 | `ofl/pliant` | yes | `Pliant-Italic[wdth,wght].ttf`, `Pliant[wdth,wght].ttf` | yes | no | no | none | `cyrillic`, `cyrillic-ext`, `greek`, `greek-ext`, `latin`, `latin-ext`, `menu` | `wdth`, `wght` | `https://github.com/TheJonassss/Pliant` | `dc119b45f0b60597305af387b97b2f5a94b2e1e4` | none | `main` | none | no |
| google/fonts#10455 | Scheherazade New | 2026-05-01 | `ofl/scheherazadenew` | yes | `ScheherazadeNew-Bold.ttf`, `ScheherazadeNew-Medium.ttf`, `ScheherazadeNew-Regular.ttf`, `ScheherazadeNew-SemiBold.ttf` | no | no | yes | `Arab` | `arabic`, `latin`, `latin-ext`, `menu` | missing | `https://github.com/silnrsi/font-scheherazade` | `60e64560db425905f52149398403298747f5f684` | `https://github.com/silnrsi/font-scheherazade/releases/download/v4.500/ScheherazadeNew-4.500.zip` | `master` | none | no |
| google/fonts#10468 | Akt | 2026-04-29 | `ofl/akt` | yes | `Akt[wght].ttf` | yes | no | no | none | `cyrillic`, `cyrillic-ext`, `greek`, `greek-ext`, `latin`, `latin-ext`, `menu`, `vietnamese` | `wght` | `https://github.com/dimgrenev/akt` | `b3935082b52ae393aef02a679505c028a5256c72` | none | `main` | none | no |
| google/fonts#10401 | Estedad | 2026-04-16 | `ofl/estedad` | yes | `Estedad[wght].ttf` | yes | no | yes | `Arab` | `arabic`, `latin`, `latin-ext`, `menu`, `vietnamese` | `wght` | `https://github.com/aminabedi68/Estedad` | `69e879f78a4a1c7c4594baf7da13ba1c9f65ffd3` | none | `master` | `sources/config.yaml` | no |

## Recent Packager Merges

This section is derived from the local `google/fonts` first-parent merge history
for `gftools_packager_ofl_*` branches. It is a recency check; the package
examples above remain the detailed comparison set.

| PR | Merged | Path | Commit | Merge subject |
| --- | --- | --- | --- | --- |
| google/fonts#10546 | 2026-05-22 | `ofl/pliant` | `440b8e455` | Merge pull request #10546 from google/gftools_packager_ofl_pliant |
| google/fonts#10455 | 2026-05-01 | `ofl/scheherazadenew` | `df5c4a17b` | Merge pull request #10455 from google/gftools_packager_ofl_scheherazadenew |
| google/fonts#10491 | 2026-05-01 | `ofl/alienblock` | `4dee5a124` | Merge pull request #10491 from google/gftools_packager_ofl_alienblock |
| google/fonts#10454 | 2026-04-29 | `ofl/finlandicaheadline` | `41b8dbd33` | Merge pull request #10454 from google/gftools_packager_ofl_finlandicaheadline |
| google/fonts#10443 | 2026-04-29 | `ofl/finlandicatext` | `0d2798e6c` | Merge pull request #10443 from google/gftools_packager_ofl_finlandicatext |
| google/fonts#10456 | 2026-04-29 | `ofl/ramsina` | `9e334b484` | Merge pull request #10456 from google/gftools_packager_ofl_ramsina |
| google/fonts#10457 | 2026-04-29 | `ofl/idiqlat` | `6ed1657f1` | Merge pull request #10457 from google/gftools_packager_ofl_idiqlat |
| google/fonts#10468 | 2026-04-29 | `ofl/akt` | `f9bd5eaf8` | Merge pull request #10468 from google/gftools_packager_ofl_akt |

## Upstream Repo Comparison

This section compares the public upstream GitHub repositories cited by
the recent downstream packages above with the current Virtua Grotesk
repo shape. The recent upstream rows are cached from GitHub trees at
the exact commits recorded in their downstream `METADATA.pb` files.

| Family | Upstream repo | Commit | AUTHORS | CONTRIBUTORS | Description | Article | Variable fonts | Static TTFs | Webfonts | sources/config.yaml | Source format | Build entrypoint | Requirements | CI/template automation | Renovate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pliant | `https://github.com/TheJonassss/Pliant` | `dc119b45f0b6` | yes | yes | documentation | no | yes | yes | yes | yes | Glyphs | Makefile | yes | yes | yes |
| Akt | `https://github.com/dimgrenev/akt` | `b3935082b52a` | no | no | no | yes | yes | yes | yes | yes | Glyphs | makefile + tools/build.sh | yes | no | no |
| Estedad | `https://github.com/aminabedi68/Estedad` | `69e879f78a4a` | yes | yes | root | no | yes | yes | yes | yes | Glyphs | scripts | yes | no | no |
| Virtua Grotesk | `https://github.com/eliheuer/virtua-grotesk` | `pending final source commit` | yes | yes | documentation | yes | yes (ignored: yes) | yes | no | yes | UFO + designspace | build.sh + Makefile | yes | no | no |

## Upstream Repo Implications For Virtua Grotesk

- Recent merged upstream repos vary in automation: Pliant follows more of the project-template automation, while Akt and Estedad do not. Virtua Grotesk does not need to copy CI, Renovate, or template refresh tooling for the first submission.
- The sampled upstream repos expose built fonts under `fonts/`, including `fonts/variable/` for variable examples. Virtua Grotesk currently generates those files locally but keeps them ignored, so the Packager source strategy still needs an explicit decision.
- Pliant, Akt, and Estedad include `sources/config.yaml`; Virtua Grotesk already matches that shape with `sources/config.yaml` and `gftools builder`.
- Estedad is the closest Arabic-script comparison: its downstream package keeps `primary_script: "Arab"` and records `source.config_yaml`. That supports keeping Virtua's `source.config_yaml` only if the final source strategy is build-from-source.
- Scheherazade New is the closest recent Arabic package for Virtua's selected release/archive path: its downstream `source.archive_url` points to a GitHub release download `.zip`, and its `source.files` map release-archive members directly into the family directory.
- Akt shows that some recent upstream repos use an `article/` path upstream, while Pliant and Estedad keep images/descriptions under `documentation/`. Virtua's downstream preview can still map `documentation/ARTICLE.en_us.html` into downstream `article/ARTICLE.en_us.html` through `source.files`.

## Virtua Grotesk Implications

- Keep `article/ARTICLE.en_us.html` in the downstream package unless Google Fonts asks for the legacy description flow.
- Keep `primary_script: "Arab"` while Arabic is the primary non-Latin support target.
- Keep `source.repository_url`, `source.commit`, `source.branch`, and optional `source.config_yaml` internally consistent.
- Keep `source.config_yaml` only if it points at a reproducible builder config; recent `google/fonts` commits removed non-buildable `config_yaml` fields from Bitcount packages and misleading override configs from Oxygen/Neuton.
- Virtua Grotesk's `sources/config.yaml` is a real `gftools builder` config today, so the field is valid only if the final source strategy uses the reproducible build path.
- For the selected `latest-release` path, mirror the Scheherazade New pattern: use a final GitHub release download `.zip` in `source.archive_url`, omit `source.config_yaml`, and make every `source.files` entry resolve inside that archive.
- Recent packages record exact upstream commits in `source.commit`; Virtua Grotesk should do the same after the public source state is final.
- Review generated `upstream.yaml` if Packager emits it; the current Google Fonts guide documents it as the downstream file that links packaged fonts back to upstream for future upgrades.
- Treat `upstream_info.md` as optional because recent examples are mixed; Estedad has it, Pliant and Akt do not.
- Treat new-font `tags` as issue/PR review metadata rather than a `METADATA.pb` field unless Google Fonts tooling generates it.
- The local checkout may contain Virtua Grotesk dry-run artifacts; they do not affect the sampled package examples above, but they must be reviewed or discarded before the final Packager pass.
