# Documentation

## Working documents

- [Design contract](../DESIGN.md): geometry, metrics, curves, and spacing.
- [Design worklog](design-pass-worklog.md): measurements and human decisions.
- [Build and QA](qa.md): setup, commands, proofs, and validation.
- [Google Fonts onboarding](google-fonts/README.md): release scope and blockers.
- [Source guides](source-guides/): UFO, designspace, and kerning editing.
- [Source reports](source/): generated metadata and compatibility reports,
  plus Arabic design records. Check their dates before using measurements.

## Artwork and plans

- [Article draft](article/ARTICLE.en_us.html): the single Google Fonts About draft.
- [Proof specification](proofs/PROOF_SPEC.md): current proof and specimen plans.
- [Artwork and licensing](artwork.md).
- [README image scripts](readme-images/) and [social artwork](social-assets/).
- [Hebrew plan](hebrew-support-plan.md) and [Italic proposal](goal-google-fonts-launch.md).
- [Glyph harness](../harness/) and [pipeline design](../plans/ai-font-completion-harness.md).

Run image scripts from the repository root so font paths resolve. Build fonts
first. Rendered files are generally ignored; selected release artwork must be
explicitly included and licensed before packaging.

[Archive](archive/) contains historical reports and review evidence, including
the September 7 release review. It is not an active worklist. Retired automation
is recoverable from Git history; current scripts are described in
[the script index](../scripts/README.md).
