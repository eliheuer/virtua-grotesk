# Project Template Automation Readiness

This generated report separates the Google Fonts project template's
optional automation conveniences from the mandatory upstream structure.
The current decision is to defer template automation for the first
submission. The local Google Fonts handoff gate should stay independent
of CI, Pages, Renovate, or template refresh tooling that has not been
adopted yet.

## Summary

- Decision log status: decided
- Optional template automation present: 0 / 6
- Local equivalent Make targets present: 4 / 6
- Local QA target uses Fontspector: yes
- Local Makefile references FontBakery: no
- Local google/fonts workflows use Fontspector: no
- Local google/fonts workflows reference FontBakery: no
- Official QA guide says FontBakery was previous and Fontspector is current: yes
- Current project-template README still describes `make test` as
  FontBakery-based QA: yes
- Older tools/template prose still describes FontBakery-based
  setup or template QA: yes
- Mandatory upstream structure report: `documentation/google-fonts/upstream-structure-readiness.md`
- Template and recent PR audit: `documentation/google-fonts/google-fonts-template-and-pr-audit.md`

## Optional Template Automation

| Feature | Template path or target | Present | Purpose |
| --- | --- | --- | --- |
| GitHub Actions workflows | `.github/workflows` | no | Run build/proof/report automation in public CI. |
| GitHub Pages publishing | `.github/workflows/*pages* or workflow mentioning pages` | no | Publish proof and QA artifacts for reviewer inspection. |
| Renovate configuration | `renovate.json` | no | Automate dependency update PRs. |
| Project-template config | `.templaterc.json` | no | Allow future `googlefonts-project-template` refreshes. |
| Template update Make target | `update-project-template` | no | Expose a one-command template refresh path. |
| Automated release bundle publishing | `.github/workflows release packaging` | no | Publish generated fonts or source archives for Packager source strategy. |

## Local Equivalent Commands

| Local workflow | Make target | Present |
| --- | --- | --- |
| Build fonts | `build` | yes |
| Run Fontspector | `test` | yes |
| Regenerate reports | `reports` | yes |
| Run synchronized preflight | `preflight` | yes |
| Render proof PDF only | `proof-only` | no |
| Full local handoff | `handoff` | no |

## Apply Before Final Submission

- Keep `documentation/google-fonts/upstream-structure-readiness.md` as the source of truth
  for mandatory Google Fonts upstream shape.
- Revisit template automation only after choosing the public repository
  workflow for CI, proof publishing, dependency updates, and
  release/source artifacts.
- If template automation is adopted, add it deliberately instead of copying
  the project template wholesale over the existing UFO/designspace workflow.
- Treat the official project-template prose as structure guidance, not as
  a command to reintroduce legacy FontBakery QA. The guide's template
  section, tools page, and the current project-template README still
  contain FontBakery-era automation or setup prose, while the current
  official QA page and local `google/fonts` workflow evidence point at
  Fontspector.
- Any future CI should run this repo's Fontspector-based `make test`
  gate. Do not introduce FontBakery unless a reviewer explicitly asks
  for a legacy check.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/qa.html
- https://googlefonts.github.io/gf-guide/tools.html
- https://github.com/googlefonts/googlefonts-project-template
