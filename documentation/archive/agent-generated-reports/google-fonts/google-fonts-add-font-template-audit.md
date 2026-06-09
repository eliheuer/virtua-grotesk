# Google Fonts Add Font Template Audit

This generated report reads the current Add Font issue template from the
local `google/fonts` checkout. It keeps the submission handoff aligned with
the exact current template prompts and requirement checkboxes.

## Local Template

- Repo path: `GF_REPO_PATH_NOT_CONFIGURED`
- Template path: `.github/ISSUE_TEMPLATE/1_add-font.md`
- Exists: no
- Current commit: `unknown`
- Status: `unknown`
- Alignment with `upstream/main`: `unknown`
- Alignment with `origin/main`: `unknown`
- Name: `missing`
- Title pattern: `missing`
- Default labels: `missing`

## Prompts

- missing

## Requirement Checkboxes

1. missing

## Expected Snippet Coverage

| Snippet | Present |
| --- | --- |
| `entire font project is available` | no |
| `source files are available` | no |
| `sole copyright author` | no |
| `AI tools were used` | no |
| `Reserved Font Names` | no |
| `namecheck.fontdata.com` | no |
| `app menus` | no |
| `copyright holder's full names or acronyms` | no |
| `Latin Core` | no |
| `preferred upstream repo structure` | no |
| `contributing requirements` | no |
| `maintain the repository` | no |

## Virtua Grotesk Handoff Implications

- Keep the Google Fonts issue labels as `I New Font, II Submission` at creation, then request Arabic/RTL labeling when Arabic support is ready for review.
- The copyright-authorship and AI-use statement is one combined checkbox in the current template; do not split it into unrelated issue answers.
- The final issue must confirm source files are available in the public repo and that the app-menu family name is definitive.
- Regenerate this report with `make reports-only` after updating `$GF_REPO_PATH`.
