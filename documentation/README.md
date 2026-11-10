# Documentation

| Document | Content |
| --- | --- |
| [Design rules](design/README.md) | Construction, grid, weight, spacing, scripts, source editing and the learning loop. |
| [Build and QA](qa.md) | Setup, commands and the checks after a source edit. |
| [Google Fonts release](google-fonts.md) | Release scope, open decisions and links to the official guide. |
| [Helper model workflow](native-model-workflow.md) | The experimental Arabic repair model in Runebender. |
| [Live web proof](../scripts/proof-web/app/README.md) | The comparison of the current build with `reference-fonts/`. |

Material for the Google Fonts page and for publicity:

- `article/`: the Google Fonts About text and its image
  (`scripts/article_specimen.py` renders the image).
- `readme-images/`: the DesignBot script for the README image.
- `social-assets/`: DesignBot scripts for social media. See its
  [README](social-assets/README.md).

Run image scripts from the repository root after `make build`. Rendered
images are ignored by Git. Commit a final image explicitly, with its license.

Review records, worklogs and handoffs from before 2026-11-09 are on branch
`archive/agent-records-2026-11-09`. They are history, not instructions.
