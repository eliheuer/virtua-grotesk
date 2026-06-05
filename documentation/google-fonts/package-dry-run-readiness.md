# Package Dry-Run Readiness

This generated report predicts whether the guarded local `make package-dry-run` command can reach `gftools packager`. It does not run Packager and does not write to the local `google/fonts` checkout.

## Summary

- Wrapper command: `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`
- Source mode: `latest-release`
- Source mode supported by wrapper: yes
- Local google/fonts fork ready: yes
- Required local package inputs ready: yes
- Required local package inputs tracked: 2 / 5
- Required local package inputs untracked: 3
- Downstream preview `source.files` inputs: 4
- Wrapper-only local sanity inputs: `sources/config.yaml`
- Existing downstream METADATA.pb reusable: no
- Existing downstream METADATA.pb has stale placeholder URL: no
- Existing downstream METADATA.pb has starter-template markers: yes
- Starter template quarantined in downstream package path: yes
- Existing downstream METADATA.pb has unresolved metadata markers: no
- Existing downstream METADATA.pb source-mode compatible: no
- GitHub API credentials ready: no
- Wrapper can reach Packager: no
- First blocker: existing downstream METADATA.pb is still the Packager starter template
- Blocking findings: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable
- Report/wrapper required-input lists match: yes
- Report/wrapper starter-marker lists match: yes
- Report/wrapper unresolved-marker lists match: yes
- Report/wrapper source-mode lists match: yes
- Report/wrapper source-mode metadata gates present: yes
- Report/wrapper final metadata value gates present: yes
- Report/wrapper release-archive gate present: yes
- Local release archive verified: yes

## Google Fonts Checkout

- GF_REPO_PATH: `/Users/eli/GH/forks/fonts`
- Checkout exists: yes
- Origin: `git@github.com:eliheuer/fonts.git`
- Upstream: `https://github.com/google/fonts.git`
- Origin GitHub repo: `eliheuer/fonts`
- Upstream GitHub repo: `google/fonts`
- Origin is canonical google/fonts: no
- Origin is fork candidate: yes
- Upstream is canonical google/fonts: yes
- google/fonts remote topology ready: yes
- Current branch: `main`
- upstream/main exists: yes
- main vs upstream/main: `0	0`
- origin/main exists: yes
- main vs origin/main: `0	0`
- Dirty paths inside `ofl/virtuagrotesk`: 1
- Dirty paths outside `ofl/virtuagrotesk`: 0
- Dirty state is isolated to `ofl/virtuagrotesk`: yes

## Downstream Starter Template Policy

The local `google/fonts` checkout may contain a Packager starter
`METADATA.pb` while the upstream release, GitHub release download `.zip` URL, source commit,
and `date_added` are still unresolved. Treat that file as quarantined
evidence only; do not submit it and do not run Packager with `-p` from
that state.

- Starter template present: yes
- Starter template quarantined to `ofl/virtuagrotesk`: yes
- Replacement source of truth: `documentation/google-fonts/google-fonts-downstream-package-preview.md`
- Replacement gate: `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`
- Replacement command after blockers clear: `./venv/bin/python scripts/prepare_downstream_metadata.py --apply`

## Source Mode Gate

These rows compare the same downstream preview against every supported
Packager source mode. They are a decision aid; the wrapper still uses
`GFT_PACKAGER_SOURCE_MODE` to choose the actual Packager flag.

| Source mode | Command | Ready now | Mode-specific blockers |
| --- | --- | --- | --- |
| `default` | `make package-dry-run` | no | downstream METADATA.pb is not populated; GitHub API credentials unavailable; preview still has pending/placeholder source fields; public branch must expose ignored/generated source files: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/assets/readme-specimen.png`; public branch must expose untracked source files: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/google-fonts/ARTICLE.en_us.html`, `documentation/assets/readme-specimen.png` |
| `latest-release` | `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` | no | downstream METADATA.pb is not populated; GitHub API credentials unavailable; preview still has pending/placeholder source fields; release/archive must include untracked local source files: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/google-fonts/ARTICLE.en_us.html`, `documentation/assets/readme-specimen.png` |
| `build-from-source` | `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` | no | downstream METADATA.pb is not populated; GitHub API credentials unavailable; preview still has pending/placeholder source fields; keep `source.config_yaml` for build-from-source |

## GitHub API Credentials

- Credential source: `invalid token`
- Credential detail: `github.com X Failed to log in to github.com account eliheuer (default) - Active account: true - The token in default is invalid. - To re-authenticate, run: gh auth login -h github.com - To forget about this account, run: gh auth logout -h github.com -u eliheuer`

Local auth commands:

```bash
gh auth status -h github.com
gh auth login -h github.com
make github-auth-check
```

If you prefer not to refresh the persistent GitHub CLI login, export a
short-lived token only for the packaging shell and rerun the same local
checks before Packager:

```bash
export GH_TOKEN=REPLACE_WITH_SHORT_LIVED_TOKEN
make github-auth-check
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Never put `GH_TOKEN` in tracked files, generated reports, or shell
history snippets committed to the repo.

## Package Inputs

| Input | Role | Present locally | Ignored by git | Tracked by git |
| --- | --- | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | downstream source.files | yes | yes | no |
| `OFL.txt` | downstream source.files | yes | no | yes |
| `documentation/google-fonts/ARTICLE.en_us.html` | downstream source.files | yes | no | no |
| `documentation/assets/readme-specimen.png` | downstream source.files | yes | yes | no |
| `sources/config.yaml` | local wrapper sanity input | yes | no | yes |

`sources/config.yaml` is checked here as a local build and repo-shape
sanity input because the wrapper is shared by all source modes. It is
not part of the selected latest-release `source.files` mapping unless
the final strategy changes to build-from-source or Google Fonts review
asks for build metadata.

## Wrapper Alignment

This report and `scripts/package_gf_dry_run.sh` must reject the same
known-bad inputs before Packager runs. These checks compare the
report's Python-side constants with the shell wrapper's actual lists.

- Required inputs in report: 5
- Required inputs in wrapper: 5
- Required inputs missing from wrapper: none
- Extra required inputs in wrapper: none
- Starter markers in report: 4
- Starter markers in wrapper: 4
- Starter markers missing from wrapper: none
- Extra starter markers in wrapper: none
- Unresolved markers in report: 3
- Unresolved markers in wrapper: 3
- Unresolved markers missing from wrapper: none
- Extra unresolved markers in wrapper: none
- Source modes in report: `build-from-source`, `default`, `latest-release`
- Source modes in wrapper: `build-from-source`, `default`, `latest-release`
- Release-archive verifier wired in wrapper: yes


## Downstream Metadata State

- Existing downstream metadata path: `/Users/eli/GH/forks/fonts/ofl/virtuagrotesk/METADATA.pb`
- Existing downstream METADATA.pb present: yes
- Existing downstream METADATA.pb has placeholder upstream URL: no
- Existing downstream METADATA.pb has unresolved markers: no
- Existing downstream METADATA.pb unresolved markers: none
- Existing downstream METADATA.pb is starter template: yes
- Existing downstream METADATA.pb starter markers: `designer: "UNKNOWN"`, `repository_url: "https://github.com/user/repo"`, `fonts/variable/MyFont[wght].ttf`, `primary_script: "Deva"`
- Existing downstream METADATA.pb source-mode blockers: `source.commit missing or not a lowercase 40-character git hash`, `source.archive_url missing for latest-release source mode`

Safe local sequence after final release/source metadata is ready:

```bash
gh auth status -h github.com
make github-auth-check
git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk
git -C /Users/eli/GH/forks/fonts status --short
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
./venv/bin/python scripts/prepare_downstream_metadata.py --apply
git -C /Users/eli/GH/forks/fonts diff -- ofl/virtuagrotesk/METADATA.pb
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Do not run Packager with `-p` until the no-PR dry run has reached
Packager, the generated `ofl/virtuagrotesk` package has been reviewed,
and the Google Fonts Add Font issue exists.

## Apply Before Running Packager

- Keep the current starter `METADATA.pb` as Packager evidence until the preview is final, then replace it with the checked downstream preview.
- Inspect GitHub CLI auth with `gh auth status -h github.com`.
- Refresh GitHub CLI auth with `gh auth login -h github.com`, or
  set `GH_TOKEN`, before running `make package-dry-run`.
- Keep the selected public upstream URL and release/archive source
  strategy synchronized with the final GitHub release before expecting
  Packager to complete successfully.
- Keep the first pass as a no-PR dry run; this wrapper does not pass
  `-p` to Packager.

References:

- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
