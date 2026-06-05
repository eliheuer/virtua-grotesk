# Recent Google Fonts Package Audit

This generated report reads selected recently merged new-font examples from
the local `google/fonts` checkout. It keeps the template/PR audit tied to
actual downstream package files instead of a hand-written memory of recent
PRs.

## Local Checkout

- Path: `GF_REPO_PATH_NOT_CONFIGURED`
- Exists: no
- Current commit: `unknown`
- Status: `unknown`
- Dirty paths: 0
- Dirty `ofl/virtuagrotesk` paths: 0
- Alignment with `upstream/main`: `unknown`
- Alignment with `origin/main`: `unknown`
- Sample package directories present: 0 / 4
- Newest selected package example: google/fonts#10546 (Pliant, 2026-05-22)
- Newest Packager merge found locally: none (none)
- Packager merges newer than selected examples: 0

## Package Examples

| PR | Family | Merged | Path | Present | Fonts | Article | upstream.yaml | upstream_info.md | primary_script | Subsets | Axes | Source repo | Source commit | archive_url | Source branch | config_yaml | tags field |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| google/fonts#10546 | Pliant | 2026-05-22 | `ofl/pliant` | no | missing | no | no | no | none | missing | missing | missing | missing | none | missing | none | no |
| google/fonts#10455 | Scheherazade New | 2026-05-01 | `ofl/scheherazadenew` | no | missing | no | no | no | none | missing | missing | missing | missing | none | missing | none | no |
| google/fonts#10468 | Akt | 2026-04-29 | `ofl/akt` | no | missing | no | no | no | none | missing | missing | missing | missing | none | missing | none | no |
| google/fonts#10401 | Estedad | 2026-04-16 | `ofl/estedad` | no | missing | no | no | no | none | missing | missing | missing | missing | none | missing | none | no |

## Recent Packager Merges

This section is derived from the local `google/fonts` first-parent merge history
for `gftools_packager_ofl_*` branches. It is a recency check; the package
examples above remain the detailed comparison set.

| PR | Merged | Path | Commit | Merge subject |
| --- | --- | --- | --- | --- |
| missing | missing | missing | missing | missing |

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
- Akt shows that some recent upstream repos use an `article/` path upstream, while Pliant and Estedad keep images/descriptions under `documentation/`. Virtua's downstream preview can still map `documentation/google-fonts/ARTICLE.en_us.html` into downstream `article/ARTICLE.en_us.html` through `source.files`.

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
