# Documentation

| Document | Content |
| --- | --- |
| [Design rules](design/README.md) | Construction, grid, weight, spacing, scripts, source editing and the learning loop. |
| [Build and QA](qa.md) | Setup, commands and the checks after a source edit. |
| [Google Fonts release](google-fonts.md) | Release scope, open decisions and links to the official guide. |
| [Live web proof](../scripts/proof-web/app/README.md) | The comparison of the current build with `reference-fonts/`. |

Material for the Google Fonts page and for publicity:

- `article/`: the Google Fonts About text and its image
  (`weight-specimen.rs` renders the image with DesignBot).
- `readme-images/`: the DesignBot script for the README image.

Run image scripts from the repository root after `make build`. Rendered
images are ignored by Git. Commit a final image explicitly, with its license.

Review records, worklogs and handoffs from before 2026-11-09 are in the Git
history before commit 1db2dfc7. They are history, not instructions.
