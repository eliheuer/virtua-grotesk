# Local Workflow Readiness

This generated report summarizes whether the local checkout can run the main Google Fonts handoff commands. It is intentionally local-state focused and does not run a build, proof, Fontspector, or Packager.

## Summary

- Python executable: `.venv/bin/python`
- Expected project .venv: `.venv/bin/python`
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
- Fontspector command path: `fontspector`
- Fontspector version: `fontspector 1.6.0 branch:master commit_hash:42bfc355 build_time:2026-04-03 14:09:01 -07:00 build_env:rustc 1.93.0-nightly (f15a7f385 2025-11-04),nightly-aarch64-apple-darwin`
- Fontspector home exists: yes
- Fontspector local templates ready: yes
- gftools builder importable: yes
- gftools packager importable: yes
- gftools QA proof tooling ready: yes
- gftools QA proof output present: yes
- gftools QA proof HTML files: 16
- gftools QA proof covers expected instances: yes
- DrawBot fork runtime ready: no
- Proof PDF artifact present: yes
- Proof PDF page count: 11
- Local google/fonts fork ready: no
- Local google/fonts branch: `not configured`
- Local google/fonts tracking branch: `not configured`
- Local google/fonts main vs origin/main: not configured ahead, not configured behind
- Local google/fonts main vs upstream/main: not configured ahead, not configured behind
- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: 0
- GitHub API credentials ready: no
- Local preflight command ready to run: yes
- Proof command ready to run: no
- Command safety gates ready: yes
- Package dry-run ready to reach Packager: no
- Package dry-run report says wrapper can reach Packager: no
- Package dry-run first blocker: local google/fonts fork is not ready
- Package dry-run blocking findings: local google/fonts fork is not ready; GitHub API credentials unavailable

## Make Targets

| Target | Present |
| --- | --- |
| `setup` | yes |
| `build` | yes |
| `test` | yes |
| `qa` | yes |
| `reports` | yes |
| `preflight` | yes |
| `proof` | yes |
| `specimen` | yes |
| `drawing-check` | yes |
| `release-check` | yes |
| `package-check` | yes |
| `clean` | yes |

## Command Safety Gates

| Gate | Pass | Evidence |
| --- | --- | --- |
| GF_REPO_PATH has no machine-specific default | yes | Set `GF_REPO_PATH=/path/to/google/fonts` in the environment or ignored `local.mk`. |
| reports target uses Python orchestration | yes | `make reports` keeps the long report sequence out of Makefile. |
| package check target omits PR creation flags | yes | `make package-check` only regenerates readiness reports. |
| proof target supports optional eliheuer/drawbot-skia fork | yes | `make proof` runs the project .venv and prepends `DRAWBOT_SKIA_REPO/src` only when configured. |

## External Commands

- `fontspector`: `fontspector`
- `fontspector --version`: `fontspector 1.6.0 branch:master commit_hash:42bfc355 build_time:2026-04-03 14:09:01 -07:00 build_env:rustc 1.93.0-nightly (f15a7f385 2025-11-04),nightly-aarch64-apple-darwin`
- `~/.fontspector`: `~/.fontspector`
- Fontspector templates directory exists: yes
- Fontspector markdown template exists: yes
- Fontspector HTML template exists: yes
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
- Refresh command: `./.venv/bin/python -m pip freeze --all > requirements.txt`

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
- Size: 110363 bytes
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

- google/fonts path: `not configured`
- google/fonts origin: `not configured`
- google/fonts upstream: `not configured`
- google/fonts branch: `not configured`
- Package report google/fonts ready: no
- Package report inputs ready: yes
- Package report auth ready: no
- drawbot-skia path: `not configured`
- project .venv Python for DrawBot exists: yes
- drawbot-skia src exists: no

## Next Actions

- Configure `DRAWBOT_SKIA_REPO=/path/to/drawbot-skia` or install `drawbot-skia` in `.venv` before running `make proof` or `make handoff`.
- Resolve package dry-run first blocker: local google/fonts fork is not ready.
- Resolve all package dry-run blockers: local google/fonts fork is not ready; GitHub API credentials unavailable.
- Review `documentation/google-fonts/package-dry-run-readiness.md` before running `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.
