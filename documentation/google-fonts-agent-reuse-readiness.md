# Google Fonts Agent Reuse Readiness

This generated report checks whether the reusable agent-facing
Google Fonts onboarding knowledge is present, linked, and portable
enough to copy into the next font repository.

## Summary

- Reusable agent bundle ready: yes
- Required reusable agent files present: 6 / 6
- Reusable files linked from README: 5 / 5
- Reusable files linked from AGENTS.md: 5 / 5
- Official Google Fonts references mapped: 13 / 13
- Reusable report categories listed: 26
- Copy checklist sections: 14
- Copy-to-next-font notes present: yes
- Portable gate shape present: yes
- Google Fonts skills written for reuse: yes

## Required Reusable Files

- `.agents/README.md`: yes
- `.agents/google-fonts-onboarding-checklists.md`: yes
- `.agents/google-fonts-official-reference-map.md`: yes
- `.agents/skills/google-fonts-onboarding/SKILL.md`: yes
- `.agents/skills/google-fonts-qa/SKILL.md`: yes
- `.agents/skills/google-fonts-packaging/SKILL.md`: yes

## Official References

- https://googlefonts.github.io/gf-guide/onboarding.html: yes
- https://googlefonts.github.io/gf-guide/upstream.html: yes
- https://googlefonts.github.io/gf-guide/requirements.html: yes
- https://googlefonts.github.io/gf-guide/variable.html: yes
- https://googlefonts.github.io/gf-guide/metadata.html: yes
- https://googlefonts.github.io/gf-guide/package.html: yes
- https://googlefonts.github.io/gf-guide/article.html: yes
- https://googlefonts.github.io/gf-guide/making-pr.html: yes
- https://googlefonts.github.io/gf-guide/onboarder-workflow.html: yes
- https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md: yes
- https://github.com/google/fonts: yes
- https://github.com/googlefonts/googlefonts-project-template: yes
- https://github.com/googlefonts/glyphsets: yes

## Reusable Report Categories

- `documentation/decision-readiness.md`
- `documentation/designer-profile-readiness.md`
- `documentation/downstream-metadata-diff.md`
- `documentation/downstream-metadata-readiness.md`
- `documentation/downstream-pr-readiness.md`
- `documentation/final-submission-blockers.md`
- `documentation/fontspector-googlefonts-report.md`
- `documentation/fontspector-warnings.md`
- `documentation/generated-font-metadata.md`
- `documentation/gf-glyphset-readiness.md`
- `documentation/google-fonts-add-font-issue-draft.md`
- `documentation/google-fonts-add-font-template-audit.md`
- `documentation/google-fonts-decisions.md`
- `documentation/google-fonts-language-metadata.md`
- `documentation/google-fonts-production-requirements.md`
- `documentation/google-fonts-reference-index.md`
- `documentation/kerning-proof-review.md`
- `documentation/kerning-readiness.md`
- `documentation/next-actions.md`
- `documentation/package-dry-run-readiness.md`
- `documentation/package-source-files-audit.md`
- `documentation/packager-source-strategy.md`
- `documentation/pr-identity-readiness.md`
- `documentation/release-archive-manifest.md`
- `documentation/release-source-readiness.md`
- `documentation/variable-font-metadata.md`

## Copy Guidance

- Copy `.agents/README.md`, `.agents/google-fonts-onboarding-checklists.md`,
  `.agents/google-fonts-official-reference-map.md`, and the three
  `.agents/skills/google-fonts-*` skill directories first.
- Replace family names, source paths, axis data, downstream directory,
  designer identity, script scope, and source package strategy before
  treating the copied docs as authoritative.
- Refresh the official references in
  `.agents/google-fonts-official-reference-map.md` before opening a
  real Google Fonts issue or PR.
- Recreate the report categories above in the new repo, even if the
  script names differ.
