# Local Workflow Readiness

This generated report summarizes whether the local checkout can run the main Google Fonts handoff commands. It is intentionally local-state focused and does not run a build, proof, Fontspector, or Packager.

## Summary

- Python executable: `/Users/eli/GH/repos/virtua-grotesk/venv/bin/python`
- Expected project venv: `/Users/eli/GH/repos/virtua-grotesk/venv/bin/python`
- Main Make targets present: yes
- Built font outputs present: yes
- Required generated reports present: yes
- Python package imports ready: yes
- requirements.in direct dependencies expected: yes
- requirements.in direct dependencies: 7
- requirements.txt pinned packages: 120
- requirements.txt fully pinned: yes
- requirements.txt includes transitive dependencies: yes
- requirements.txt includes direct dependency package names: yes
- requirements.in directly includes FontBakery: no
- requirements.txt includes FontBakery transitively: yes
- Automated QA entrypoint remains Fontspector: yes
- Fontspector command available: yes
- Fontspector command path: `/Users/eli/.cargo/bin/fontspector`
- Fontspector version: `fontspector 1.6.0 branch:master commit_hash:42bfc355 build_time:2026-04-03 14:09:01 -07:00 build_env:rustc 1.93.0-nightly (f15a7f385 2025-11-04),nightly-aarch64-apple-darwin`
- Fontspector home exists: yes
- Fontspector local templates ready: yes
- gftools builder importable: yes
- gftools packager importable: yes
- gftools QA proof tooling ready: yes
- gftools QA proof output present: yes
- gftools QA proof HTML files: 16
- gftools QA proof covers expected instances: yes
- DrawBot fork runtime ready: yes
- Proof PDF artifact present: yes
- Proof PDF page count: 11
- Local google/fonts fork ready: yes
- Local google/fonts branch: `main`
- Local google/fonts tracking branch: `origin/main`
- Local google/fonts main vs origin/main: 0 ahead, 0 behind
- Local google/fonts main vs upstream/main: 0 ahead, 0 behind
- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0
- GitHub API credentials ready: no
- Local preflight command ready to run: yes
- Proof command ready to run: yes
- Command safety gates ready: yes
- Package dry-run ready to reach Packager: no
- Package dry-run report says wrapper can reach Packager: no
- Package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template
- Package dry-run blocking findings: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable

## Make Targets

| Target | Present |
| --- | --- |
| `decisions` | yes |
| `decision-readiness-check` | yes |
| `next-actions` | yes |
| `blockers` | yes |
| `issue-draft` | yes |
| `handoff-readiness-check` | yes |
| `release-check` | yes |
| `release-archive-check` | yes |
| `release-archive-build` | yes |
| `release-archive-verify` | yes |
| `release-archive-test` | yes |
| `release-draft-check` | yes |
| `source-strategy-check` | yes |
| `package-readiness-check` | yes |
| `recent-gf-check` | yes |
| `family-name-check` | yes |
| `authorship-check` | yes |
| `pr-readiness-check` | yes |
| `vendor-id-check` | yes |
| `kerning-check` | yes |
| `kerning-proof-check` | yes |
| `kerning-proof-review-check` | yes |
| `pua-scope-check` | yes |
| `avar-check` | yes |
| `warnings-check` | yes |
| `github-auth-check` | yes |
| `designer-profile-check` | yes |
| `designer-profile-prepare-check` | yes |
| `designer-profile-info-check` | yes |
| `designer-profile-image-check` | yes |
| `designer-profile-bio-check` | yes |
| `designer-profile-validator-test` | yes |
| `public-upstream-url-check` | yes |
| `downstream-metadata-check` | yes |
| `downstream-metadata-helper-test` | yes |
| `package-wrapper-test` | yes |
| `build` | yes |
| `test` | yes |
| `reports` | yes |
| `reports-only` | yes |
| `preflight` | yes |
| `preflight-only` | yes |
| `proof` | yes |
| `proof-only` | yes |
| `handoff` | yes |
| `package-dry-run` | yes |
| `clean` | yes |

## Command Safety Gates

| Gate | Pass | Evidence |
| --- | --- | --- |
| GF_REPO_PATH defaults to local google/fonts fork | yes | `GF_REPO_PATH ?= /Users/eli/GH/forks/fonts` |
| package-dry-run target invokes local wrapper | yes | `make package-dry-run` -> `scripts/package_gf_dry_run.sh` |
| package-dry-run target omits PR creation flags | yes | Make target does not pass `-p` or `--pr`. |
| package-dry-run wrapper does not add PR creation flags | yes | Wrapper builds Packager args without PR flags. |
| package wrapper metadata gates have a local test | yes | `make package-wrapper-test` exercises source-mode metadata blockers. |
| designer profile validators and prepare helper have a local test | yes | `make designer-profile-validator-test` exercises info.pb, image, bio, and guarded prepare-helper blockers. |
| release archive path-safety gates have a local test | yes | `make release-archive-test` exercises unsafe source/destination paths, duplicate source/destination mappings, deterministic metadata, and SHA mismatch blockers. |
| downstream-metadata-check target is preview-only | yes | `make downstream-metadata-check` does not pass `--apply`. |
| downstream metadata apply remains explicit | yes | Use `scripts/prepare_downstream_metadata.py --apply` only after review. |
| downstream metadata helper final-value gates have a local test | yes | `make downstream-metadata-helper-test` checks final date and source commit validation. |
| Packager source mode is surfaced | yes | `GFT_PACKAGER_SOURCE_MODE` is shared by metadata preview and Packager dry run. |
| proof target uses eliheuer/drawbot-skia fork | yes | `make proof-only` runs the project venv with the fork source on `PYTHONPATH`. |

## External Commands

- `fontspector`: `/Users/eli/.cargo/bin/fontspector`
- `fontspector --version`: `fontspector 1.6.0 branch:master commit_hash:42bfc355 build_time:2026-04-03 14:09:01 -07:00 build_env:rustc 1.93.0-nightly (f15a7f385 2025-11-04),nightly-aarch64-apple-darwin`
- `~/.fontspector`: `/Users/eli/.fontspector`
- Fontspector templates directory exists: yes
- Fontspector markdown template exists: yes
- Fontspector HTML template exists: yes
- `designbot`: `/Users/eli/.cargo/bin/designbot`
- GitHub auth detail: `github.com X Failed to log in to github.com account eliheuer (default) - Active account: true - The token in default is invalid. - To re-authenticate, run: gh auth login -h github.com - To forget about this account, run: gh auth logout -h github.com -u eliheuer`
- Package report GitHub API credentials ready: no

## Python Requirements Snapshot

- Direct dependency file: `requirements.in`
- Direct dependencies match expected onboarding set: yes
- Direct dependency count: 7
- Pinned install snapshot: `requirements.txt`
- Pinned package count: 120
- Fully pinned with `==`: yes
- Includes transitive dependencies: yes
- Includes direct dependency package names: yes
- Direct FontBakery dependency: no
- Transitive FontBakery pin from `gftools[qa]`: yes
- FontBakery appears in the pinned snapshot only because current `gftools[qa]` depends on it; local automated QA still runs Fontspector.
- Refresh command: `./venv/bin/python -m pip freeze --all > requirements.txt`

| Direct requirement | Present in pinned snapshot |
| --- | --- |
| `fontmake` | yes |
| `fonttools` | yes |
| `gftools[qa]` | yes |
| `GitPython` | yes |
| `glyphsets` | yes |
| `PyYAML` | yes |
| `uharfbuzz` | yes |

## Required Generated Reports

| Report | Present |
| --- | --- |
| `documentation/google-fonts/final-submission-blockers.md` | yes |
| `documentation/google-fonts/next-actions.md` | yes |
| `documentation/google-fonts/package-dry-run-readiness.md` | yes |
| `documentation/google-fonts/drawbot-runtime-readiness.md` | yes |
| `documentation/google-fonts/submission-handoff-readiness.md` | yes |
| `documentation/google-fonts/release-archive-manifest.md` | yes |
| `documentation/google-fonts/github-release-draft.md` | yes |
| `documentation/google-fonts/github-release-notes.md` | yes |
| `documentation/google-fonts/missing-gf-arabic-core.md` | yes |
| `documentation/glyph-review/arabic-mark-readiness.md` | yes |
| `documentation/glyph-review/arabic-shaping-smoke-test.md` | yes |
| `documentation/google-fonts/fontspector-googlefonts-report.md` | yes |

## Built Fonts

| Font | Present |
| --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes |

## Proof Artifact

- Path: `documentation/proofs/proof.pdf`
- Exists: yes
- Size: 110365 bytes
- Page count: 11
- Render command: `make proof-only`

## Google Fonts QA Proof Artifact

- Path: `documentation/google-fonts/gftools-qa/Proof`
- Exists: yes
- HTML files: 16
- Covers Regular, Medium, SemiBold, Bold: yes
- Tooling ready: yes
- Render command: `make kerning-proof-check`

## Local Repository Dependencies

- google/fonts path: `/Users/eli/GH/forks/fonts`
- google/fonts origin: `git@github.com:eliheuer/fonts.git`
- google/fonts upstream: `https://github.com/google/fonts.git`
- google/fonts branch: `main`
- Package report google/fonts ready: yes
- Package report inputs ready: yes
- Package report auth ready: no
- drawbot-skia path: `/Users/eli/GH/repos/drawbot-skia`
- project venv Python for DrawBot exists: yes
- drawbot-skia src exists: yes

## Next Actions

- Resolve package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template.
- Resolve all package dry-run blockers: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable.
- Review `documentation/google-fonts/package-dry-run-readiness.md` before running `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.
