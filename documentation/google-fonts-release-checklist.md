# Google Fonts Release Checklist

Use this after drawing work, QA, and open decisions are resolved, but before
the downstream `gftools packager` pass. The goal is to make the upstream source
state reproducible for Google Fonts review.

## Release candidate gate

- Confirm `documentation/google-fonts-decisions.md` has no unresolved blocker
  for public URL, author strings, family name/trademark/CLA, PUA scope, vendor
  ID, kerning scope, `avar`, and version strategy.
- Confirm the public upstream repository URL is the same URL used in `OFL.txt`,
  generated name ID 0, the Google Fonts issue, and downstream `METADATA.pb`.
- Confirm `make handoff` passes from a clean checkout or clean worktree state.
- Confirm `make test` passes, or that every remaining Fontspector FAIL has a
  Google Fonts reviewer acceptance link recorded in the issue or PR.
- Confirm `proof.pdf`, `documentation/arabic-shaping-smoke-test.md`, and
  `documentation/arabic-mark-readiness.md` have been reviewed after the final
  drawing/build pass.
- Confirm `documentation/ARTICLE.en_us.html` has the final upstream link, or
  confirm Google Fonts wants the legacy `DESCRIPTION.en_us.html` instead.
- Confirm `documentation/google-fonts-downstream-package-preview.md` matches the
  intended `gftools packager` output and final `METADATA.pb` decisions.
- Confirm generated reports match the released build, especially
  `documentation/final-submission-blockers.md`,
  `documentation/missing-gf-latin-core.md`,
  `documentation/missing-gf-arabic-core.md`,
  `documentation/master-compatibility.md`,
  `documentation/generated-font-metadata.md`,
  `documentation/release-source-readiness.md`,
  `documentation/variable-font-metadata.md`,
  `documentation/fontspector-contour-count.md`, and
  `documentation/fontspector-warnings.md`.

## Tagging

Google Fonts' upstream structure guide notes that releases should be tagged.
For the first Google Fonts submission, use the confirmed source version from
`documentation/google-fonts-decisions.md` and verify the current source/build
version evidence in `documentation/release-metadata.md`.
Use `documentation/release-source-readiness.md` for the current commit, dirty
state, suggested tag presence, `source.files` exposure, and local
`google/fonts` fork alignment.

Suggested first-submission tag shape:

```text
v1.000
```

Before tagging:

- Confirm source UFO `versionMajor`/`versionMinor`, built name ID 5, and the
  tag name all describe the same release.
- Confirm there are no uncommitted source, metadata, report, or proof changes
  that should be part of the submission.
- Confirm whether built fonts are intentionally excluded from the upstream tag
  or included as release assets.
- Confirm the final Packager source strategy:
  - branch/tag source files exist at every `source.files.source_file` path, or
  - `source.archive_url` points to a GitHub release download `.zip` archive
    containing those paths.
- Record the final tag name and commit hash in the Google Fonts issue before
  downstream packaging.

## Final handoff data

Record these values before running Packager:

```text
Upstream URL: https://github.com/eliheuer/virtua-grotesk
Upstream tag: v1.000 pending final source commit
Upstream commit: pending release
Google Fonts issue: pending
Version: 1.000
Arabic scope: GF_Arabic_Core
Downstream path: ofl/virtuagrotesk
```

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/onboarder-workflow.html
