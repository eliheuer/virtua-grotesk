# Google Fonts Add Font Template Audit

This generated report reads the current Add Font issue template from the
local `google/fonts` checkout. It keeps the submission handoff aligned with
the exact current template prompts and requirement checkboxes.

## Local Template

- Repo path: `/Users/eli/GH/forks/fonts`
- Template path: `.github/ISSUE_TEMPLATE/1_add-font.md`
- Exists: yes
- Current commit: `c5b52261e`
- Status: `## main...origin/main`
- Alignment with `upstream/main`: `0 ahead, 0 behind`
- Alignment with `origin/main`: `0 ahead, 0 behind`
- Name: `Add Font`
- Title pattern: `Add [Font Name]`
- Default labels: `I New Font, II Submission`

## Prompts

- Font Project Git Repo URL
- Super short description of the Font Family
- Requirements
- Image

## Requirement Checkboxes

1. The entire font project is available in a Github repository (repo) and licensed under the [OFL](https://openfontlicense.org/open-font-license-official-text/)
2. The source files are available in the repo
3. I am the sole copyright author of the entire project, or all other copyright authors have licensed their work to me under the OFL, and I commit to clearly disclosing if AI tools were used in the creation of this project.
4. There are no "Reserved Font Names" in the OFL license information, or in the project documentation of any known upstream projects. If there are RFNs, they are not used in whole or in part in this family name, or, I want to discuss how Google can work with my use of them.
5. The family name is unique according to [namecheck.fontdata.com](https://namecheck.fontdata.com/)
6. The name of the font family expected to appear on app menus must be very clearly communicated and definitive. It should not include any copyright holder's full names or acronyms.
7. The font supports at least the Google Fonts 'Latin Core' glyphset from [github.com/googlefonts/glyphsets](https://github.com/googlefonts/glyphsets) ([direct link](https://github.com/googlefonts/glyphsets/blob/main/data/results/txt/nice-names/GF_Latin_Core.txt))
8. The repo has the [Google Fonts preferred upstream repo structure](https://googlefonts.github.io/gf-guide/upstream.html)
9. I have read, agree with, and comply with, the full [Google Fonts contributing requirements](https://googlefonts.github.io/gf-guide/index#pre-production-getting-your-fonts-ready-for-gf)
10. I will maintain the repository and participate in the onboarding process (addressing, solving, and responding to issues, merging pull requests, etc)

## Expected Snippet Coverage

| Snippet | Present |
| --- | --- |
| `entire font project is available` | yes |
| `source files are available` | yes |
| `sole copyright author` | yes |
| `AI tools were used` | yes |
| `Reserved Font Names` | yes |
| `namecheck.fontdata.com` | yes |
| `app menus` | yes |
| `copyright holder's full names or acronyms` | yes |
| `Latin Core` | yes |
| `preferred upstream repo structure` | yes |
| `contributing requirements` | yes |
| `maintain the repository` | yes |

## Virtua Grotesk Handoff Implications

- Keep the Google Fonts issue labels as `I New Font, II Submission` at creation, then request Arabic/RTL labeling when Arabic support is ready for review.
- The copyright-authorship and AI-use statement is one combined checkbox in the current template; do not split it into unrelated issue answers.
- The final issue must confirm source files are available in the public repo and that the app-menu family name is definitive.
- Regenerate this report with `make reports-only` after updating `/Users/eli/GH/forks/fonts`.
