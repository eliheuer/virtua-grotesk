# Google Fonts Package Checklist

This checklist is for the final handoff after drawing work and scope decisions
are resolved. It follows the current Google Fonts guide structure: upstream
sources stay in this public repo, while the `google/fonts` pull request is
packaged with `gftools packager`.

Resolve `documentation/google-fonts/google-fonts-decisions.md` before using this as the final
package checklist.

## Upstream gate

- Confirm the upstream repository is public and is the canonical source URL.
- Confirm `AUTHORS.txt`, `CONTRIBUTORS.txt`, `OFL.txt`, `README.md`,
  `requirements.txt`, `sources/config.yaml`, `build.sh`, `sources/`,
  `sources/README.md`, `sources/archive/README.md`, and `documentation/` are
  present.
- Confirm the exact copyright-author statement required by the current
  `google/fonts` Add Font issue template.
- Confirm the AI-use disclosure required by the current `google/fonts` Add Font
  issue template, including the rough Arabic candidate drawing scaffolds that
  still require manual cleanup and final drawing review.
- Confirm the current Add Font issue template's combined copyright-author and
  AI-disclosure checkbox is answered in one maintainer-approved statement.
- Confirm `README.md` has a short family description, build instructions, and a
  project image.
- Confirm documentation images have provenance or licensing notes in
  `documentation/assets/image-license.txt`.
- Confirm `OFL.txt` first line exactly matches name ID 0 in the built fonts.
- Confirm whether built font binaries are committed in the upstream repo or
  provided as release/CI artifacts for the final package.
- Confirm `documentation/google-fonts/ARTICLE.en_us.html` is third-person, accurate, and
  ready for the Google Fonts family page.
- Confirm the upstream link in `documentation/google-fonts/ARTICLE.en_us.html` matches the
  final public canonical repository URL.
- Confirm Article images are copied alongside `article/ARTICLE.en_us.html` in
  the downstream package, currently including `readme-specimen.png`.
- Confirm Article images meet the Google Fonts image limits and are documented
  in `documentation/assets/image-license.txt`.
- Confirm the first-submission scope: Latin plus Arabic, and whether the
  private-use icon block ships.

## Local build and QA gate

Run from this repo:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make handoff
make test
```

`make test` must be green before packaging unless a Google Fonts reviewer has
explicitly accepted a remaining Fontspector FAIL. Any accepted FAIL needs a
written reason and a link to the approving issue or reviewer comment.

Review before packaging:

- `documentation/google-fonts/google-fonts-template-and-pr-audit.md`
- `documentation/google-fonts/recent-google-fonts-packages.md`
- `documentation/google-fonts/google-fonts-add-font-template-audit.md`
- `documentation/google-fonts/project-template-automation-readiness.md`
- `documentation/google-fonts/decision-readiness.md`
- `documentation/google-fonts/designer-profile-package-draft.md`
- `documentation/google-fonts/google-fonts-downstream-package-preview.md`
- `documentation/google-fonts/google-fonts-release-checklist.md`
- `documentation/google-fonts/google-fonts-upstream-audit.md`
- `documentation/google-fonts/final-submission-blockers.md`
- `documentation/google-fonts/submission-handoff-readiness.md`
- `documentation/google-fonts/package-source-files-audit.md`
- `documentation/google-fonts/packager-source-strategy.md`
- `documentation/google-fonts/release-archive-manifest.md`
- `documentation/google-fonts/github-release-draft.md`
- `documentation/google-fonts/github-release-notes.md`
- `documentation/google-fonts/package-dry-run-readiness.md`
- `documentation/google-fonts/release-source-readiness.md`
- `documentation/google-fonts/upstream-structure-readiness.md`
- `documentation/google-fonts/downstream-metadata-readiness.md`
- `documentation/google-fonts/downstream-metadata-diff.md`
- `documentation/google-fonts/article-readiness.md`
- `documentation/google-fonts/ARTICLE.en_us.html`
- `documentation/source/source-ufo-metadata.md`
- `documentation/source/master-compatibility.md`
- `documentation/google-fonts/generated-font-metadata.md`
- `documentation/google-fonts/family-name-readiness.md`
- `documentation/google-fonts/authorship-disclosure-readiness.md`
- `documentation/google-fonts/pr-identity-readiness.md`
- `documentation/google-fonts/downstream-pr-readiness.md`
- `documentation/google-fonts/drawbot-runtime-readiness.md`
- `documentation/google-fonts/local-workflow-readiness.md`
- `documentation/google-fonts/vendor-id-readiness.md`
- `documentation/google-fonts/avar-readiness.md`
- `documentation/google-fonts/variable-font-metadata.md`
- `documentation/google-fonts/gf-glyphset-readiness.md`
- `documentation/google-fonts/google-fonts-language-metadata.md`
- `documentation/google-fonts/pua-scope.md`
- `documentation/google-fonts/public-upstream-readiness.md`
- `documentation/google-fonts/kerning-readiness.md`
- `documentation/google-fonts/kerning-proof-review.md`
- `documentation/google-fonts/missing-gf-latin-core.md`
- `documentation/google-fonts/missing-gf-arabic-core.md`
- `documentation/glyph-review/arabic-source-work-checklist.md`
- `documentation/glyph-review/arabic-shaping-smoke-test.md`
- `documentation/glyph-review/arabic-review-packet.md`
- `documentation/google-fonts/glyph-reachability.md`
- `documentation/google-fonts/numeric-feature-readiness.md`
- `documentation/google-fonts/fontspector-contour-count.md`
- `documentation/google-fonts/fontspector-warnings.md`
- `documentation/google-fonts/fontspector-googlefonts-report.md`
- `documentation/proofs/proof.pdf`

## Downstream package gate

Open or confirm a `google/fonts` issue before making the downstream PR. Google
Fonts uses the issue to schedule the work and archive decisions; the PR should
finish the project, not start it.

Before creating the PR:

- Confirm the committer has signed the Google CLA.
- Confirm the family name has no known trademark, catalog-name, or Reserved Font
  Name conflict.
- Confirm the family name passes `namecheck.fontdata.com`.
- Confirm the Google Fonts issue starts with the current default labels:
  `I New Font, II Submission`; request the Arabic/RTL script label once Arabic
  support is ready for review.
- Confirm `documentation/google-fonts/designer-profile-readiness.md` has been reviewed and
  every final `METADATA.pb` designer/foundry string has a matching
  `google/fonts/catalog/designers` profile or a prepared profile request.
- Review `documentation/google-fonts/designer-profile-package-draft.md` and replace its
  biography/image draft inputs before preparing a designer-profile PR.
- Run `make designer-profile-check` after changing `AUTHORS.txt`,
  `CONTRIBUTORS.txt`, or the downstream metadata designer string.
- Confirm the upstream release tag and commit are recorded in the Google Fonts
  issue.
- Confirm `documentation/google-fonts/github-release-draft.md` matches the final archive
  filename, tag, release title, generated release notes file, and downstream
  `source.archive_url`.
- Confirm the source and generated font version is correct for a first
  submission or upgrade.
- Confirm local git `user.name` and `user.email` match the CLA identity.
- Confirm the local `google/fonts` checkout is up to date with upstream `main`.

Do not copy files into `google/fonts` by hand. Package with `gftools packager`
so the downstream PR title, body, and file layout are generated consistently.

Packager command shape:

```bash
gftools packager "Virtua Grotesk" path/to/local/google/fonts
gftools packager "Virtua Grotesk" path/to/local/google/fonts -p -i ISSUE_NUMBER
```

Run without `-p` first to generate and review the downstream package locally
without opening or updating a pull request. Add `-p` only when the PR is ready.
The public Google Fonts package guide shows the `-p` flow; the installed
`gftools packager` also exposes `-i/--issue-number`, which should be used after
the Google Fonts issue exists.

This repo includes a guarded local wrapper for the no-PR pass:

```bash
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

`make package-dry-run` defaults to `latest-release` in this repo, but keep the
environment variable in copied commands so the selected release/archive source
mode is explicit. It defaults to `$GF_REPO_PATH`. Override
`GF_REPO_PATH` to test a different clean `google/fonts` checkout, or a clean
fork checkout with an `upstream` remote pointing at
`https://github.com/google/fonts.git`. It also requires the checkout to be on
`main`, with local `main` aligned to both cached `upstream/main` and
`origin/main` when `origin/main` exists. It refuses to run if required local
package inputs are missing. If
`ofl/virtuagrotesk/METADATA.pb` already exists from the first Packager pass, the
wrapper calls Packager with that metadata file path so the official new-family
two-pass flow can continue. It refuses to rerun from an existing metadata file
that still contains the internal stale-placeholder guard value named in
`scripts/package_gf_dry_run.sh`, because that means the downstream metadata has
not been refreshed from the decided public URL. It also
refuses to rerun from the unpopulated Packager starter template
(`designer: "UNKNOWN"`, `https://github.com/user/repo`, or
`fonts/variable/MyFont[wght].ttf`). It still writes to the local downstream
checkout, so review or discard those downstream changes before rerunning with
`-p`.

The wrapper also exposes Packager's source strategy flags without enabling PR
creation. Use the mode that matches the final upstream release decision:

```bash
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run
```

These pass Packager's `--latest-release` or `--build-from-source` flags during
the no-PR dry run.
Use `GFT_PACKAGER_SOURCE_MODE=default make package-dry-run` only for fallback
review of Packager's default branch-fetch behavior.

Packager uses the GitHub API to fetch `source.files` from
`source.repository_url`. The local wrapper now checks GitHub API credentials
before invoking Packager. It accepts an explicit `GH_TOKEN`, or exports a token
from a valid GitHub CLI login. If `gh auth token` fails, refresh the local
GitHub CLI auth first.

Quick credential check:

```bash
gh auth status -h github.com
make github-auth-check
```

Explicit token example:

```bash
GH_TOKEN="$(gh auth token)" GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Current dry-run status, 2026-05-24: the local `google/fonts` fork checkout is
ready at `$GF_REPO_PATH`, but GitHub API credentials are not
currently usable. The first no-PR Packager pass created
`$GF_REPO_PATH/ofl/virtuagrotesk/METADATA.pb`, which is still the
unpopulated Packager starter template. The current generated state is
`Wrapper can reach Packager: no` and first blocker:
`existing downstream METADATA.pb is still the Packager starter template`.
Current blocking findings:
`existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable`.

Populate that downstream `METADATA.pb` from
`documentation/google-fonts/google-fonts-downstream-package-preview.md` after the final
release/source commit and GitHub release archive are public, and refresh GitHub
CLI/API auth with `gh auth login -h github.com` before rerunning the dry run.
Use the checked local sequence, and keep the first Packager rerun as no-PR:

```bash
git -C $GF_REPO_PATH status --short -- ofl/virtuagrotesk
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
./.venv/bin/python scripts/prepare_downstream_metadata.py --apply
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Packager still cannot complete until the selected `v1.000` release/archive
exposes every file listed in `METADATA.pb` `source.files`. A previous default
branch Packager run reached the download step and failed because
`fonts/variable/VirtuaGrotesk[wght].ttf` was not present on
`https://github.com/eliheuer/virtua-grotesk` branch `main`; the selected
latest-release path avoids committing that generated font to `main` but still
requires the release/archive asset to contain it.
Preview the public URL replacement set with `make public-upstream-url-check`.
The canonical public URL is decided as
`https://github.com/eliheuer/virtua-grotesk`. If new placeholder URL surfaces
are added later, apply the decided URL with
`scripts/apply_public_upstream_url.py --url https://github.com/eliheuer/virtua-grotesk --apply`
before rebuilding fonts and regenerating the reports.
Use the guarded helper before editing the local fork:

```bash
make downstream-metadata-check
```

It reports whether the preview still contains pending placeholders. Once the
metadata is final, run `scripts/prepare_downstream_metadata.py --apply` to write
the checked preview to
`$GF_REPO_PATH/ofl/virtuagrotesk/METADATA.pb`, then rerun
`make package-dry-run`.
Use the same source mode for the metadata check and Packager dry run. For
default branch or latest-release packaging, remove `source.config_yaml` from
the preview unless Google Fonts review asks for build metadata; for
build-from-source packaging, keep it. For latest-release packaging, add the
final GitHub release download `.zip` `archive_url` before applying the
downstream metadata:

```bash
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
GFT_PACKAGER_SOURCE_MODE=build-from-source make downstream-metadata-check
```

For the selected latest-release path, build and inspect the local review
archive before creating the GitHub release asset:

```bash
make release-archive-build
make release-archive-check
make release-archive-verify
```

Expected downstream family path:

```text
ofl/virtuagrotesk
```

Expected downstream file types:

- TTF files served by Google Fonts.
- `METADATA.pb`.
- `article/ARTICLE.en_us.html` copied or adapted from
  `documentation/google-fonts/ARTICLE.en_us.html`.
- Article image assets referenced by `ARTICLE.en_us.html`, currently
  `readme-specimen.png`.
- `DESCRIPTION.en_us.html` only if Google Fonts review explicitly asks for the
  legacy description instead of Article content.
- `OFL.txt`.
- `upstream.yaml` if Packager emits it; the current Google Fonts repository
  guide documents this as the downstream file linking packaged fonts back to
  upstream for future upgrades.
- Optional `upstream_info.md` only if Google Fonts review asks for a
  human-readable provenance note; keep `METADATA.pb` `source { ... }` as the
  authoritative machine-readable source link.

Review the generated `METADATA.pb` even if Fontspector reports no FAILs:

- Family name and style names.
- Designer/author fields.
- Designer profile match status from
  `documentation/google-fonts/designer-profile-readiness.md`.
- Category/classification.
- Axis data and default location.
- `avar` strategy from `documentation/google-fonts/avar-readiness.md`; if the axis stays
  linear, record the accepted warning rationale.
- Vendor ID status from `documentation/google-fonts/vendor-id-readiness.md`.
- Kerning scope from `documentation/google-fonts/kerning-readiness.md`, especially whether
  static fonts need GPOS `kern` before the first PR.
- Visual spacing and kerning proof review from
  `documentation/google-fonts/kerning-proof-review.md`, especially the expected proof files
  by weight and proof type.
- Primary script if Arabic or another non-LCG script is in scope.
- Language metadata evidence from
  `documentation/google-fonts/google-fonts-language-metadata.md`, especially the `Arab`
  script record and recent Arabic package examples.
- License and copyright consistency.
- Source repository URL and commit.
- PUA/private-use scope, after reviewing `documentation/google-fonts/pua-scope.md` and
  deciding whether those glyphs ship in the first package.
- Glyph reachability and subsetting warnings from
  `documentation/google-fonts/glyph-reachability.md` and
  `documentation/google-fonts/fontspector-warnings.md`, especially for Arabic helpers,
  private-use glyphs, and `googlefonts/metadata/unreachable_subsetting`.
- Numeric feature readiness from
  `documentation/google-fonts/numeric-feature-readiness.md`, especially proportional
  default ASCII digits and full-width `tnum` alternates.
- `source.files` mappings for `OFL.txt`, the served variable TTF,
  `article/ARTICLE.en_us.html`, and Article image assets if the package uses
  the Article flow.
- `documentation/google-fonts/package-source-files-audit.md`, especially whether the served
  variable TTF is still ignored/generated or has been made available through
  the selected upstream source strategy.
- `documentation/google-fonts/release-archive-manifest.md`, especially the SHA-256 hashes
  and whether the selected release/archive contains every expected
  `source.files` path with deterministic ZIP metadata.
- Generated `upstream.yaml`, if present, so its archive/branch/file mappings
  agree with the selected source strategy and downstream package files.
- Optional `upstream_info.md` provenance if requested, matching the
  `METADATA.pb` `source { ... }` repository, commit, branch, and config path.
- Designer order, since the first designer appears as principal designer.
- `primary_script: "Arab"` while Arabic is the primary non-Latin support target.
- `category: "SANS_SERIF"` and `stroke: "SANS_SERIF"`.
- Optional `classifications` only if Google Fonts review wants `DISPLAY` or
  another documented classification.
- New-font tags and script labels requested in the linked issue or PR. Treat
  tags as PR/release-review metadata, not as a `METADATA.pb` field unless
  Packager or Google Fonts tooling generates one.
- No custom `sample_text` block unless Google Fonts review asks for it or the
  default Arabic specimen text is clearly unsuitable and the decision is
  recorded.

Use `documentation/google-fonts/google-fonts-metadata-review.md` as the upstream review
checklist for expected names, files, weights, axes, and subset decisions. Use
`documentation/google-fonts/google-fonts-downstream-package-preview.md` as the quick
comparison target for the local package generated by `gftools packager`, and
use `documentation/google-fonts/downstream-metadata-diff.md` to compare the current
Packager-created downstream `METADATA.pb` against that preview.

## PR review notes

The Google Fonts onboarder workflow expects:

- The PR is generated by Packager.
- Fontspector report is reviewed.
- Every WARN receives human review.
- Every ignored FAIL has an explicit justification.
- Decision-linked WARNs are recorded or resolved: vendor ID, kerning, `avar`,
  PUA/reachability, and downstream unreachable subsetting.
- Visual QA proofs are reviewed for design consistency, outline quality,
  spacing, kerning, missing glyphs, shaping issues, and interpolation issues.
- The linked issue and PR carry any script/scope labels needed for review,
  especially if Arabic or PUA/symbol content is included.
- The linked issue includes the copyright-authorship and AI-use disclosure
  required by the current `google/fonts` Add Font issue template.
- The PR body cites the public upstream repository and exact source commit, as
  recent merged new-font PRs do.
- The Article is third-person, includes a working link to the
  public upstream repository, uses only allowed HTML, and its images meet the
  Google Fonts article image requirements.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/article.html
- https://googlefonts.github.io/gf-guide/making-pr.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/qa.html
- https://googlefonts.github.io/gf-guide/onboarder-workflow.html
- https://github.com/google/fonts
- https://github.com/googlefonts/gftools
