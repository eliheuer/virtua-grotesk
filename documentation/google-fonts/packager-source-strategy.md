# Packager Source Strategy Matrix

This generated report compares the source modes available for the final Google Fonts Packager dry run. The maintainer-selected first-submission path is latest release/archive; the other modes remain documented fallback paths if Google Fonts review asks for a different source strategy.

## Current Evidence

- Normalized upstream candidate: `https://github.com/eliheuer/virtua-grotesk`
- Placeholder upstream URL still present: no
- Working tree clean: no
- Suggested release tag exists locally: no
- Pending downstream source fields: 1
- Local `source.files` entries: 4
- Missing local `source.files`: 0
- Ignored/generated `source.files`: 2
- Tracked source.files: 1 / 4
- Untracked local source.files: 3
- Build-from-source inputs present and tracked: 6 / 6
- Build script uses GF builder config: yes
- Build script runs metadata post-processing: yes
- Builder config outputs package fonts directory: yes
- Downstream preview includes `source.config_yaml`: no
- `source.config_yaml` is reproducible-builder-only: no
- Downstream preview includes release `archive_url`: yes
- Downstream preview `archive_url` is GitHub release download `.zip`: yes
- Selected first-submission source mode: `latest-release`
- Local google/fonts fork topology ready: yes
- Local google/fonts checkout clean: no
- Dirty paths outside `ofl/virtuagrotesk`: 0
- Downstream METADATA.pb starter template present: yes

## Strategy Matrix

| Strategy | Dry-run command | Needs | Current blockers | Best fit |
| --- | --- | --- | --- | --- |
| Default branch `source.files` | `make package-dry-run` | Public branch exposes every listed `source_file`; final `branch` and `commit` recorded | replace pending commit/branch fields<br>served variable TTF is ignored/generated locally<br>commit or otherwise expose untracked source files<br>finish/commit source tree before citing a commit | Best if final public branch commits the served variable TTF or otherwise exposes it at the listed path |
| Latest release/archive | `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` | Public GitHub release download `.zip` exposes the expected files; final `archive_url` and tag strategy recorded | create final release tag after source work<br>replace pending commit/branch fields<br>commit or package untracked source files into release archive<br>finish/commit source tree before tagging | Best if generated fonts should stay out of `main` but be published as release assets |
| Build from source | `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` | Public repo build path is reproducible and accepted by Google Fonts; source/build inputs tracked | replace pending commit/branch fields<br>finish/commit source tree before citing a commit | Best if Google Fonts accepts building from `sources/config.yaml` instead of fetching generated font binaries |

## Source Files To Expose

| Source file | Downstream destination | Exists locally | Ignored/generated locally | Tracked locally |
| --- | --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | yes | no | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | yes | yes | no |
| `documentation/google-fonts/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | yes | no | no |
| `documentation/assets/readme-specimen.png` | `article/readme-specimen.png` | yes | yes | no |

## Selected Latest-Release Action Plan

The maintainer-selected first-submission strategy keeps generated fonts out of the public branch and publishes the Packager inputs through a GitHub release archive. The next mechanical work is:

1. Keep the public upstream URL and release/archive metadata preview synchronized.
2. Finish drawing/source work and make the final `v1.000` source commit.
3. Create a GitHub release archive that contains every listed `source.files` path.
4. Keep `source.config_yaml` omitted unless Google Fonts asks for build metadata.
5. Regenerate reports, run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`, then run a no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.

- Release archive files currently present but untracked: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/google-fonts/ARTICLE.en_us.html`, `documentation/assets/readme-specimen.png`
- Release archive files currently blocked by `.gitignore`: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/assets/readme-specimen.png`
- `make package-dry-run` now defaults to `GFT_PACKAGER_SOURCE_MODE=latest-release`; set `GFT_PACKAGER_SOURCE_MODE=default` or `build-from-source` only for fallback review.

## Per-Strategy Mechanical Checklist

These are conditional checklists. Apply only the section that matches the maintainer-approved source strategy.

### If Default Public-Branch Packaging Is Chosen

1. Apply the final public upstream URL everywhere reported by `make public-upstream-url-check`.
2. Add a narrow `.gitignore` exception for the served variable font only.
3. Track the current untracked source files: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/google-fonts/ARTICLE.en_us.html`, `documentation/assets/readme-specimen.png`.
4. Remove `source.config_yaml` from the downstream metadata preview unless Google Fonts review asks for build metadata.
5. Regenerate reports, verify `GFT_PACKAGER_SOURCE_MODE=default make downstream-metadata-check`, then run the no-PR `GFT_PACKAGER_SOURCE_MODE=default make package-dry-run`.

### If Latest Release Or Archive Packaging Is Chosen

1. Keep generated fonts out of the public branch if that is the selected policy.
2. Ensure the release archive contains every mapped source file: `OFL.txt`, `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/google-fonts/ARTICLE.en_us.html`, `documentation/assets/readme-specimen.png`.
3. Create the final release tag only after drawing/source work and metadata decisions are complete.
4. Add the final GitHub release download `.zip` `source.archive_url` to the downstream metadata preview.
5. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` before opening the downstream PR.

### If Build-From-Source Packaging Is Chosen

1. Keep `source.config_yaml: "sources/config.yaml"` in the downstream metadata preview.
2. Track every currently untracked build input: none.
3. Keep `build.sh` on `gftools builder sources/config.yaml` followed by `scripts/fix_gf_metadata.py`.
4. Confirm Google Fonts accepts this family using the reproducible build path before treating the dry run as final.
5. Run `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` without `-p` before opening the downstream PR.

## Decision Notes

- Do not run Packager with `-p` until the Google Fonts issue exists, final QA is reviewed, and the selected release/archive source is public.
- Keep the local no-PR dry run on `/Users/eli/GH/forks/fonts` before opening or updating a downstream PR.
- The local dry-run wrapper accepts an explicit `GH_TOKEN` or exports one from a valid `gh auth token` before invoking Packager.
- Keep `source.config_yaml` only for the build-from-source path. Recent `google/fonts` commits removed non-buildable or misleading `config_yaml` fields, so default branch or release/archive packaging should omit it unless Google Fonts specifically asks for build metadata.
- Latest-release packaging must add the final GitHub release download `.zip` `archive_url` to the downstream metadata preview before `make downstream-metadata-check` can be ready.
- If the strategy changes, update `documentation/google-fonts/google-fonts-downstream-package-preview.md` first, then regenerate reports.
- If `upstream.yaml` is emitted, review it against the selected source mode before opening the PR.

## References

- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/googlefonts.html
- https://googlefonts.github.io/gf-guide/making-pr.html
