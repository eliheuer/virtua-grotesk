# /google-fonts-packaging

Prepare the upstream release, downstream metadata, Google Fonts Packager dry
run, Add Font issue, and downstream PR handoff for a font family.

This skill is portable: copy it to another font repo and replace the family
name, downstream directory, release strategy, and local wrapper commands.

## Usage
`/google-fonts-packaging [metadata|release|packager|issue|pr|all]`

Default: `all`

## Preconditions

- Maintainer decisions are recorded.
- Drawing/source blockers are either fixed or explicitly accepted for review.
- Fontspector and visual proof evidence is current.
- Public upstream URL is final.
- Local `google/fonts` fork is synced with upstream.
- Git identity and Google CLA identity are aligned.
- GitHub CLI or `GH_TOKEN` auth is available before Packager needs the API.

## Source Strategy

Choose exactly one strategy for the first package, then document fallback paths:

- Default branch: Packager reads files from the public repo branch.
- Latest release/archive: Packager reads generated files from a GitHub release
  archive URL ending in `.zip`.
- Build from source: Packager builds from public source inputs and a supported
  config, if Google Fonts accepts that path for the family.

For each strategy, verify:

- every `source.files` path exists locally,
- no `source.files` path is unsafe,
- there are no duplicate source or destination paths,
- generated or ignored files are either committed through the selected strategy
  or intentionally excluded,
- `source.config_yaml` is present only for a build-from-source strategy or when
  Google Fonts review asks for it.

## Downstream METADATA.pb

Review and generate downstream metadata from built fonts and decisions. Check:

- family name and designer strings,
- `category`,
- `date_added` final value,
- `fonts` blocks and filenames,
- `axes` and `fvar` alignment,
- `subsets`, including `menu`,
- `primary_script` when needed,
- `source.repository_url`,
- `source.archive_url` or source files strategy fields,
- `source.commit` as a final 40-character lowercase Git commit,
- absence of project-only placeholders.

Do not apply metadata into the local `google/fonts` fork until final values are
available and a dry-run checker says it is ready.

## Release Archive Path

When using latest-release/archive mode:

1. Build final fonts.
2. Generate the release archive from an explicit manifest.
3. Verify archive contents, path safety, duplicates, and hashes.
4. Create the final source commit and tag.
5. Publish the GitHub release asset.
6. Confirm the downstream `source.archive_url` matches the public release asset.

Never cite a release archive URL as final before the tag and asset exist.

## Packager Dry Run

Run Packager without PR mode first:

```bash
gftools packager -n -d /path/to/google/fonts ofl/familyname
```

or the repo's wrapper equivalent.

Review the generated package before any `-p` run:

- changed paths are limited to one family directory,
- `METADATA.pb` matches the reviewed preview,
- fonts, article, images, license, and upstream metadata are present as expected,
- generated `upstream.yaml` or source linkage is sensible,
- no unrelated downstream files changed.

Only after that review and after the Add Font issue exists should the final
Packager run use PR mode with the issue number.

## Add Font Issue

Build the issue draft from the current Google Fonts Add Font template. Keep:

- title concise, usually `Add Family Name`,
- labels from the template, usually `I New Font, II Submission`,
- requirement boxes unchecked until actually opening the issue,
- public repo URL,
- short description,
- copyright and AI-use disclosure,
- namecheck status,
- glyphset/script status,
- known blockers or reviewer questions,
- links to proof, specimen, and evidence reports as appropriate.

Refresh the issue template from `google/fonts` before opening the real issue.

## Downstream PR

Follow the Google Fonts PR guide:

- issue first,
- one family directory per PR,
- branch name from Packager or a clear family-specific branch,
- PR title in the expected package format,
- body includes upstream repo and commit provenance,
- local `google/fonts` fork has no dirty paths outside the family directory,
- current family directory contents are explicitly listed before branching.

If the local downstream family directory contains only a starter `METADATA.pb`,
record that clearly. The starter-only state must be replaced by Packager output
before opening the PR.

## Final Handoff Evidence

Keep durable docs for:

- package source strategy,
- release/archive manifest,
- downstream metadata preview and diff,
- package dry-run readiness,
- Add Font issue draft,
- PR identity/auth readiness,
- downstream PR readiness,
- final blockers,
- next actions.
