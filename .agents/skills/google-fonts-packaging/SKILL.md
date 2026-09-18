---
name: google-fonts-packaging
description: Prepare and review a local Google Fonts package and submission draft before authorized publication.
---

# Google Fonts packaging

Read `.agents/google-fonts-onboarding-checklists.md` and the project checklist.
Refresh the official [package](https://googlefonts.github.io/gf-guide/package.html),
[metadata](https://googlefonts.github.io/gf-guide/metadata.html), and
[article](https://googlefonts.github.io/gf-guide/article.html) pages.

## Local preview

Work in a scratch output directory, separate from live source files and any
shared google/fonts checkout. Copy the exact reviewed TTFs and OFL.txt into
`ofl/virtuagrotesk/`, then run `gftools add-font` on that directory. Copy the
upstream article to `article/ARTICLE.en_us.html`. Inspect generated metadata;
its defaults are not approved scope or release values.

Check names, designer, category/stroke, axes, subsets including menu, primary
script, date, and source linkage. Confirm all declared files exist. Preserve
intended Arabic and Hebrew support even when the automatic subset detector
omits a subset. A preview can carry provisional values if clearly identified;
do not present it as ready to publish.

Run `make qa-package PACKAGE=<directory>`. Keep network failures/skips distinct
from font defects. Review package-context findings and actual proof output.
The variable font is the current downstream proposal; static outputs remain
upstream build artifacts unless the release plan changes.

## Public source and Packager

Choose a reviewed public binary source before finalizing `source.files` or
`source.archive_url`. Ignored local fonts are not public branch files. Verify
archive contents and hashes if using a release. Do not invent URLs, tags,
commits, dates, or designer approvals.

Read `gftools packager --help` for the installed version before invoking it.
Do not copy old command syntax. Identify modes that commit, push, or open a PR;
keep the preview local until those actions are authorized. Inspect every path
and ensure only the intended downstream family is affected.

## Submission

Search for an existing Add Font issue. Prepare an honest draft from the current
template; leave maintainer attestations unchecked until confirmed. The issue
can begin while requirements are still being completed. It must precede a PR.

Before publication, resolve actual QA failures, record warning dispositions,
confirm drawing/script acceptance and artwork licensing, and ensure public
artifacts are exactly the reviewed binaries. User authorization is required
for public messages or publication. Report local, submitted, approved, and
published states separately.
