# Authorship And AI Disclosure Readiness

This generated report tracks the Google Fonts Add Font issue requirement
that copyright authorship and AI-use disclosure are confirmed together.
It records local evidence separately from maintainer confirmations that
cannot be inferred from the source tree.

## Summary

- AUTHORS.txt entries: `Eli Heuer`
- CONTRIBUTORS.txt entries: `Eli Heuer`
- AUTHORS.txt contact-formatted entries: 0 / 1
- CONTRIBUTORS.txt contact-formatted entries: 0 / 1
- Contact-formatted credit lines absent by current decision: yes
- OFL copyright line: `Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)`
- OFL uses project-author copyright holder: yes
- Combined Add Font checkbox present: yes
- AI-use disclosure recorded: yes
- Approved authorship/AI statement recorded: yes
- Email/contact line change required now: no
- Decision status: decided

## Current Evidence

- `AUTHORS.txt` is the current copyright-author source of truth for
  Google Fonts review.
- `CONTRIBUTORS.txt` is the current contributor-attribution source of
  truth.
- The local file comments ask for `Name <email address>` lines, and
  the Google Fonts upstream guide describes both files as contact
  information files.
- The official Authors and Contributors guide's templates use
  `Name or Organization <email address>` for authors and
  `Name <email address>` for contributors; the maintainer has chosen
  to keep the current display-only names unless Google Fonts asks for
  email/contact-formatted credit lines.
- `OFL.txt` currently uses a collective project-author copyright line,
  while the local author and contributor files each contain one named
  person.
- The current `google/fonts` Add Font issue template combines sole
  copyright-author authority and AI-use disclosure into one checkbox.
- Final AI-use disclosure wording is recorded in
  `documentation/google-fonts/google-fonts-decisions.md` and synchronized into
  the submission handoff.

## Approved Add Font Statement

```text
The Google Fonts Add Font issue can state that Eli Heuer is the sole copyright author/controller for the project as submitted under the OFL. AI-use disclosure: AI tools were used for engineering, proofing, onboarding, repository preparation assistance, and rough Arabic candidate drawing scaffolds that still require manual cleanup and final drawing review.
```

## Maintainer Input Checklist

| Input | Current value | Needed before Add Font issue |
| --- | --- | --- |
| Copyright-author authority | `Eli Heuer` sole copyright author/controller statement recorded | Keep synchronized with Add Font issue text. |
| AI-use disclosure | Recorded | Keep synchronized with Add Font issue text. |
| Email/contact-formatted credit lines | AUTHORS.txt: 0 / 1; CONTRIBUTORS.txt: 0 / 1 | Keep current display-only names unless Google Fonts asks for contact-formatted lines. |
| OFL copyright holder | `Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)` | Keep current project-author wording unless the copyright-holder model changes. |
| Add Font checkbox wording | Combined copyright-authorship and AI-use checkbox is present in current template | Use the approved statement above in the Google Fonts Add Font issue. |

Decision-safe default: keep `AUTHORS.txt`, `CONTRIBUTORS.txt`, and
`OFL.txt` unchanged because the maintainer-approved Add Font statement
is already recorded and no email/contact line change is required now.

## Apply After Maintainer Confirmation

- Use the approved copyright-authorship and AI-use statement above in the
  Add Font issue.
- Keep the copyright-authorship and AI-use disclosure answer as one
  combined maintainer-approved statement.
- Update `AUTHORS.txt`, `CONTRIBUTORS.txt`, and `OFL.txt` if the confirmed
  authorship or copyright-holder wording differs from the current files.
- Add email/contact strings to `AUTHORS.txt` and `CONTRIBUTORS.txt` only
  if Google Fonts asks for explicit contact-formatted credit lines.
- Rerun `make preflight` after any authorship, copyright, or disclosure
  wording change.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/making-pr.html
- https://openfontlicense.org
