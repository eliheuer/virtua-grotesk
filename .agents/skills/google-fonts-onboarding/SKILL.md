---
name: google-fonts-onboarding
description: Audit Google Fonts readiness and coordinate repository preparation, release scope, and remaining onboarding work. Use for onboarding or submission-readiness requests; use google-fonts-qa for a focused binary QA run.
---

# Google Fonts onboarding

Read `.agents/google-fonts-onboarding-checklists.md` and the project checklist
at `documentation/google-fonts/README.md`. Refresh relevant official pages and
the [Add Font template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md).
Do not treat old audits or copied checklist boxes as current evidence.

Check the active sources, build recipe, license/authorship, README, intended
script/style scope, and public binary strategy. Run the build and current
Fontspector profile; inspect compiled metadata, coverage, interpolation,
shaping, and proofs as appropriate. Use the QA skill for that work.

Keep one concise project checklist with concrete findings, evidence, and
remaining maintainer decisions. Avoid generating a separate report for each
metadata field or workflow step. Retain historical design decisions without
presenting them as current measurements.

Distinguish three states: ready to discuss onboarding, ready for submission
review, and accepted/published. An Add Font issue can honestly carry unchecked
requirements; a finished font is not required merely to ask the team for review.
An issue must precede the PR. Search existing issues before drafting another.

Do not make copyright, CLA, or image-license attestations for the maintainer.
Do not post public messages or publish without authorization. Local cleanup,
QA, issue drafting, and package preparation may proceed within the request.

## Scope and completion

Read-only review requests produce findings without source edits. For preparation
or repair requests, complete authorized engineering work and verify it. A
pending human decision does not block independent checks or fixes. Preserve
existing session approvals; ask only for missing choices that change the result.

Finish with the source/artifact identity, checks actually run, observed results,
and remaining decisions. Do not claim readiness from file presence or report
counts alone, and do not rerun a build merely for a documentation-only change.
