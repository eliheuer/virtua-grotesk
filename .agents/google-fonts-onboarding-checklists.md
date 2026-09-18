# Google Fonts workflow

Use the current [Google Fonts guide](https://googlefonts.github.io/gf-guide/)
and issue template. This file holds reusable procedure; project status belongs
in [the onboarding checklist](../documentation/google-fonts/README.md).
Do not create parallel readiness reports for the same decision.

## Repository values

- `{{FAMILY}}`: Virtua Grotesk
- `{{FAMILY_DIR}}`: virtuagrotesk
- `{{AXES}}`: wght 400–700
- `{{REPO_URL}}`: https://github.com/eliheuer/virtua-grotesk
- `{{VF_PATH}}`: fonts/variable/VirtuaGrotesk[wght].ttf

When reusing these skills for another family, replace these values and verify
its build commands, source layout, and release scope.

## Repository and evidence

Keep editable sources and a build recipe in `sources/`, compiled outputs under
`fonts/` by format, and documentation under `documentation/`. The root should
explain the project, build, status, authors, and license. The official project
template is optional; copying all its automation is not a requirement.

Record the source revision, any source modifications, binary hashes, tool
versions, network mode, and QA results. Separate current evidence from historical
reports. Build success, cmap coverage, and table presence do not prove visual
quality or correct shaping.

Use Fontspector's `googlefonts` profile. Development exclusions are not release
exceptions. Full release QA must expose all checks, failures, warnings, and
skips. A warning needs human disposition; a real failure needs a fix or explicit
reviewer exception. Never shrink intended script scope to improve the count.

## Maintainer decisions

Track only unresolved choices that affect the release: script and style scope,
primary script, name availability, copyright/CLA identity, AI disclosure,
artwork licensing, and public binary delivery. Keep answers in the project
checklist or design worklog. Do not infer legal attestations from file presence.

## Onboarding and packaging

An Add Font issue precedes a PR. The current template allows requirements to
remain unchecked while work continues; do not require a completed package just
to start the conversation. Search for an existing issue before creating one.
Posting messages and publishing require the user's authorization.

Use one upstream article at `documentation/article/ARTICLE.en_us.html`. The
legacy DESCRIPTION format is retired. Images must exist, meet the guide's
specifications, and have an approved license; do not grant one on behalf of
the author without permission.

Generate downstream metadata from the reviewed fonts, then inspect designer,
category/stroke, axes, subsets, primary script, date, and source linkage.
`METADATA.pb` and article files belong in the downstream family package.
Do not keep a misleading hand-written package placeholder at the upstream root.

Choose a public source for release binaries: committed artifacts, a published
archive, or a build-from-source path verified with the onboarding team. Ignored
local files and private/expiring CI artifacts are not public Packager inputs.
Inspect `gftools packager --help` before using it; some modes commit, push, or
open a PR. Preview locally, inspect the resulting paths and metadata, and run
package-context QA before publishing the exact reviewed files.
