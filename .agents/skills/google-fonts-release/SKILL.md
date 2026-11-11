---
name: google-fonts-release
description: Check Google Fonts readiness, run the release QA, and prepare a local package and Add Font issue draft for Virtua Grotesk. Use for onboarding, Fontspector findings, packaging or submission questions.
---

# Google Fonts release

The project facts, open decisions and official links are in
`documentation/google-fonts.md`. The Google Fonts requirements change. Read
the current official page for each requirement. Do not use older audits or
copied checklists as evidence.

## QA

| Command | Use |
| --- | --- |
| `make qa` | Development profile, offline, with the exclusions listed in `scripts/check_gf_fonts.sh`. The CI gate. |
| `make qa-full` | Full profile with network checks and no exclusions. |
| `make qa-package PACKAGE=<dir>` | Full profile on a package with `METADATA.pb`, `OFL.txt` and the article. |
| `make qa-hebrew` | Hebrew coverage and mark attachment. |

Read the JSON report in `out/qa/<mode>/`, not only the terminal output. Count
unique findings, not one finding repeated for each font. Put each finding in
one class: drawing, compiled metadata, package context, maintainer decision
or tool limitation. A FAIL needs a fix or an exception that Eli approves. A
WARN needs a decision by Eli. Do not add exclusions, remove cmap entries or
reduce the script scope to get a cleaner result.

Coverage and table presence do not prove shaping. Look at mark attachment,
joining, right-to-left and mixed text, spacing and the intermediate weights
in a rendered proof (see the `build-and-proof` skill).

## Package

1. Work in a scratch directory under `out/`. Copy the reviewed TTFs and
   `OFL.txt` into `ofl/virtuagrotesk/` and run `gftools add-font` on it.
2. Copy `documentation/article/ARTICLE.en_us.html` and its image to
   `article/`.
3. Check the generated metadata: names, designer, category, axes, subsets,
   primary script, date and source. Keep the Arabic and Hebrew subsets even
   if the subset detection leaves one out.
4. Run `make qa-package PACKAGE=<dir>`.

Read `gftools packager --help` before you use it. Some of its modes commit,
push or open a pull request. Use only a local preview unless Eli authorizes
publication.

## Add Font issue

Search the existing issues first. Draft the issue from the current template.
Leave the copyright, CLA and image-license attestations unchecked: only Eli
can confirm them. The issue comes before a pull request.

Do not post, push, tag or publish without Eli's authorization. Report what is
local, drafted, submitted and published as separate states.
