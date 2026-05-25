# Google Fonts Official Reference Map

Last checked: 2026-05-25.

Use this map when copying the Google Fonts onboarding skills to another font
repo. Refresh these references before final issue or PR work because Google
Fonts docs, templates, and tooling expectations can change.

## Core Google Fonts Docs

| Reference | Use it for | Reusable agent surface |
| --- | --- | --- |
| https://googlefonts.github.io/gf-guide/onboarding.html | New-family acceptance criteria, OFL/RFN/CLA/name/source/build/TTF/glyphset/QA expectations, issue-first entrypoint | `.agents/google-fonts-onboarding-checklists.md`; `.agents/skills/google-fonts-onboarding/SKILL.md` |
| https://googlefonts.github.io/gf-guide/upstream.html | Preferred upstream repository shape and public source expectations | repo baseline checklist; release/source strategy |
| https://googlefonts.github.io/gf-guide/requirements.html | Overall production requirements and exception handling | QA and final blocker reports |
| https://googlefonts.github.io/gf-guide/variable.html | Variable font axis, instance, `STAT`, and variable-specific review | QA skill; metadata checklist |
| https://googlefonts.github.io/gf-guide/metadata.html | Downstream `METADATA.pb` fields and source linkage | packaging skill; downstream metadata checklist |
| https://googlefonts.github.io/gf-guide/package.html | Packager behavior, package branch naming, `source.files`, release archive `archive_url`, no-PR review before PR mode | packaging skill; package dry-run checklist |
| https://googlefonts.github.io/gf-guide/article.html | `ARTICLE.en_us.html`, image, and provenance expectations | article/image checklist |
| https://googlefonts.github.io/gf-guide/making-pr.html | Issue-first rule, CLA/git identity, local fork setup, downstream PR expectations | PR identity and downstream PR checklists |
| https://googlefonts.github.io/gf-guide/onboarder-workflow.html | Onboarder review workflow, proof review expectations, handoff expectations | visual QA and handoff checklists |

## GitHub References

| Reference | Use it for | Reusable agent surface |
| --- | --- | --- |
| https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md | Current Add Font issue fields, labels, requirement checkboxes, and maintenance commitment | Add Font issue draft checklist |
| https://github.com/google/fonts | Downstream package layout, recent family directories, current PR conventions | downstream PR readiness |
| https://github.com/googlefonts/googlefonts-project-template | Optional automation and baseline upstream project conventions | project-template automation decision |
| https://github.com/googlefonts/glyphsets | GF Latin Core and script-specific glyphset coverage targets | glyphset/script QA |

## Reusable Report Set

For a new font repo, recreate these as generated or manually maintained reports.
Names can change, but the evidence categories should remain visible:

- `documentation/google-fonts-reference-index.md`
- `documentation/google-fonts-production-requirements.md`
- `documentation/google-fonts-decisions.md`
- `documentation/decision-readiness.md`
- `documentation/final-submission-blockers.md`
- `documentation/next-actions.md`
- `documentation/generated-font-metadata.md`
- `documentation/variable-font-metadata.md`
- `documentation/gf-glyphset-readiness.md`
- `documentation/google-fonts-language-metadata.md`
- `documentation/fontspector-googlefonts-report.md`
- `documentation/fontspector-warnings.md`
- `documentation/kerning-readiness.md`
- `documentation/kerning-proof-review.md`
- `documentation/package-source-files-audit.md`
- `documentation/packager-source-strategy.md`
- `documentation/release-source-readiness.md`
- `documentation/release-archive-manifest.md`
- `documentation/downstream-metadata-readiness.md`
- `documentation/downstream-metadata-diff.md`
- `documentation/package-dry-run-readiness.md`
- `documentation/google-fonts-add-font-template-audit.md`
- `documentation/google-fonts-add-font-issue-draft.md`
- `documentation/pr-identity-readiness.md`
- `documentation/downstream-pr-readiness.md`
- `documentation/designer-profile-readiness.md`

## Portable Gate Shape

Every copied onboarding setup should have one synchronized command that:

1. builds or verifies current build output,
2. regenerates generated reports,
3. checks official-reference coverage,
4. checks decision-log coverage,
5. checks Fontspector and proof evidence,
6. checks package source and metadata readiness,
7. checks downstream fork/PR readiness,
8. fails only for known and documented blockers.

For Virtua Grotesk this command is:

```bash
make preflight
```

In a future font repo, keep the command name if practical. The important part is
that agents and humans have one handoff gate to run before issue or PR work.

