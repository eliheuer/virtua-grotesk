# Google Fonts Upstream Audit

This audit maps the current repo state to the Google Fonts upstream structure,
build, and QA guidance. It is intentionally limited to repo-readiness work; it
does not claim that drawing, spacing, kerning, or script coverage is complete.

## Satisfied upstream artifacts

- `AUTHORS.txt` exists and has a non-comment author entry.
- `AUTHORS.txt` is the single author source of truth for the project.
- `CONTRIBUTORS.txt` exists and has a non-comment contributor entry.
- `OFL.txt` exists, starts with the project copyright line, and is copied into
  generated name ID 0 by the build metadata patch.
- `README.md` includes a short family description, build instructions, and the
  generated specimen image.
- `documentation/` contains the Google Fonts article and description drafts,
  generated QA reports, packaging checklist, metadata review checklist,
  submission handoff, release checklist, decision questionnaire, decision log,
  project-template and recent-PR audit, downstream package preview, open
  placeholder audit, public upstream URL readiness report, package source-file
  audit, release/source readiness report, downstream metadata readiness report,
  Article readiness report, submission handoff readiness report, kerning readiness report,
  final-submission blocker summary, family-name readiness report, authorship
  and AI-disclosure readiness report, designer-profile readiness audit,
  designer-profile package draft, Vendor ID readiness report, avar readiness
  report, Google Fonts
  language-metadata audit, and image
  provenance note.
- `sources/` contains only the active Virtua Grotesk UFO masters and
  `sources/VirtuaGrotesk.designspace`; older source material is archived under
  `sources/archive/` instead of living in the active source root.
- `sources/README.md` identifies the active designspace and UFO masters so the
  build inputs are clear to reviewers.
- `sources/archive/README.md` marks older source snapshots as reference-only
  material that should not be packaged into the downstream Google Fonts PR.
- `requirements.txt` declares the Python packages required by the local build,
  report, and packaging workflow.
- `requirements.in` and `documentation/python-tooling-notes.md` document direct
  Python dependencies separately from external tools such as Fontspector,
  DesignBot, DrawBot, and optional `fontc`.
- `sources/config.yaml` is the preferred `gftools builder` configuration.
- `build.sh` builds all generated fonts in one command, prefers
  `gftools builder sources/config.yaml`, and keeps the fallback output layout aligned
  with `fonts/variable/` and `fonts/ttf/`.
- `.gitignore` excludes the local virtual environment, generated build files,
  and generated fonts unless the built-fonts decision changes.
- `.ignore` excludes generated build files from ordinary repo-wide source
  searches, including `sources/instance_ufos/` JSON emitted by the builder.

## Satisfied build and QA gates

- `make build` builds the variable font and static TTFs.
- `make reports` builds once, then regenerates the source UFO metadata report,
  master compatibility report, generated-font metadata report, release metadata
  report, release/source readiness report, upstream structure readiness report,
  decision readiness report, family-name readiness report,
  designer-profile readiness audit,
  authorship and AI-disclosure readiness report, variable-font metadata report,
  designer-profile package draft, Vendor ID readiness report,
  avar readiness report,
  Google Fonts axis-registry audit,
  Google Fonts glyphset readiness report, Google Fonts language-metadata
  audit, missing GF Latin Core report, Arabic Core coverage report,
  PUA/private-use scope report, open-placeholder audit, public upstream URL
  readiness report, package source-file
  audit, downstream metadata readiness report, kerning readiness report,
  Arabic mark-readiness report, Arabic shaping smoke test, glyph
  reachability report, Fontspector
  contour-count report, Fontspector warning report, full Fontspector Markdown
  report, final-submission blocker summary, recent-package audit, and Add Font
  issue-template audit.
- `make preflight` builds once, regenerates `documentation/proofs/proof.pdf`, regenerates reports,
  validates source and generated metadata, and allows only the documented
  drawing/source Fontspector FAILs.
- `make handoff` uses the same proof-before-report path for final handoff
  review.
- `documentation/google-fonts/google-fonts-template-and-pr-audit.md` compares this repo to
  the official Google Fonts project template and recently merged new-font PRs,
  so the local workflow stays aligned with current downstream practice.
- `documentation/google-fonts/google-fonts-downstream-package-preview.md` records the
  expected downstream `ofl/virtuagrotesk` file layout and draft `METADATA.pb`
  shape before the final `gftools packager` pass.
- `./scripts/check_gf_fonts.sh` runs Fontspector's `googlefonts` profile
  against the generated variable font and static TTFs. It excludes the
  downstream-only repository directory-name check because this upstream repo is
  not laid out as `ofl/virtuagrotesk`.
- `documentation/google-fonts/final-submission-blockers.md` aggregates the current decision,
  packaging, release metadata, glyphset, Arabic mark, Fontspector, and outline
  blockers into one generated final-handoff view.

## Current drawing/source blockers

These are intentionally excluded from this engineering pass:

- Complete GF Latin Core coverage.
- Complete GF Arabic Core coverage.
- Keep Regular and Bold UFO masters structurally compatible as drawing changes
  land.
- Proof Arabic shaping, positional forms, marks, and OpenType layout.
- Add and proof Arabic mark positioning anchors and built `mark`/`mkmk` GPOS
  features.
- Resolve `contour_count` / `no-contour` findings.
- Review outline-direction and alignment warnings while final drawing changes
  are made.

## Current decision blockers

Resolve these in `documentation/google-fonts/google-fonts-decisions.md` before final
submission. For quick review, answer them first in
`documentation/google-fonts/google-fonts-decision-answer-sheet.md`.

- Public upstream URL.
- Which Packager source strategy should expose generated font binaries:
  committed fonts, release/archive assets, or build-from-source packaging.
- Author/contact display strings.
- Family name, namecheck result, trademarks/RFN status, and Google CLA
  readiness.
- Copyright-authorship and AI-use disclosure wording for the current Add Font
  issue template.
- Whether the PUA/private icon block ships, using
  `documentation/google-fonts/pua-scope.md` as the current inventory.
- Vendor ID.
- Kerning scope before the first PR.

## Current final-submission gate

Before opening the downstream `google/fonts` PR, `make test` should pass with
Fontspector's `googlefonts` profile, or every remaining FAIL must have an
explicit Google Fonts reviewer acceptance recorded in the issue or PR.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/build.html
- https://googlefonts.github.io/gf-guide/qa.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/article.html
- https://github.com/googlefonts/gftools
- https://github.com/fonttools/fontspector
- https://github.com/googlefonts/googlefonts-project-template
