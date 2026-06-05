# Google Fonts Readiness

This repo is being prepared for Google Fonts onboarding while drawing work is still in progress.

## Current scope

- Family: Virtua Grotesk
- License: SIL Open Font License v1.1
- Sources: UFO masters plus `sources/VirtuaGrotesk.designspace`
- Axis: `wght` 400-700
- Build entrypoint: `./build.sh`
- Make targets: `make help`, `make decisions`, `make build`, `make test`,
  `make reports`, `make proof`, `make preflight`, `make handoff`,
  `make blockers`, `make issue-draft`, `make decision-readiness-check`,
  `make handoff-readiness-check`, `make release-check`,
  `make release-archive-check`, `make release-archive-build`,
  `make release-archive-verify`, `make release-archive-test`,
  `make release-draft-check`,
  `make source-strategy-check`, `make package-readiness-check`,
  `make recent-gf-check`,
  `make pr-readiness-check`,
  `make kerning-check`, `make kerning-proof-check`,
  `make github-auth-check`,
  `make designer-profile-check`, `make designer-profile-prepare-check`,
  `make public-upstream-url-check`,
  `make downstream-metadata-check`, `make downstream-metadata-helper-test`,
  `make package-wrapper-test`,
  `make package-dry-run`
- Preferred GF build config: `sources/config.yaml`
- Post-build metadata patch: `scripts/fix_gf_metadata.py`
- Primary automated QA command: `scripts/check_gf_fonts.sh` using Fontspector's `googlefonts` profile
- Primary visual QA command: `make kerning-proof-check` using `gftools qa --proof`
- Last tested Fontspector: 1.6.0

## Open decisions

See `documentation/google-fonts/google-fonts-decision-questions.md` for the short answer
sheet, and `documentation/google-fonts/google-fonts-decisions.md` for the canonical decision
log.
For the fastest maintainer pass, run `make decisions` or
`make decision-readiness-check`, or open
`documentation/google-fonts/google-fonts-decision-answer-sheet.md`; it sorts the same open
questions by handoff priority without applying answers.

- Author/contact display is decided as `Eli Heuer`; keep display-only
  `AUTHORS.txt` and `CONTRIBUTORS.txt` entries unless Google Fonts asks for
  contact-formatted lines.
- Arabic is in scope for the Google Fonts submission; cover at least Google's
  `GF_Arabic_Core` character set and proof shaping before submission.
- Confirm whether the private-use icon block should ship in the Google Fonts submission.
- Confirm whether kerning is completed before the first Google Fonts PR or
  explicitly deferred.

Decided first-submission defaults are recorded in
`documentation/google-fonts/google-fonts-decisions.md`: use the public upstream URL
`https://github.com/eliheuer/virtua-grotesk`, package generated fonts through a
GitHub release/archive with `GFT_PACKAGER_SOURCE_MODE=latest-release`, keep
`Virtua Grotesk` as the final name with confirmed namecheck/trademark/RFN/CLA
readiness, use Vendor ID `FTGD` for Font Garden, use Article flow, do not add custom
`sample_text`, use version `1.000`, tag final upstream source as `v1.000`,
ship the current linear `wght` axis with an identity `avar` table, and defer
project-template automation for the first submission.

## Engineering checklist

- [x] Add GF-style `AUTHORS.txt` and `CONTRIBUTORS.txt` files.
- [x] Keep `AUTHORS.txt` as the single author source of truth.
- [x] Add pinned `requirements.txt` for the Python build/QA toolchain.
- [x] Add `requirements.in` and Python tooling notes for direct dependency
  review.
- [x] Add `sources/config.yaml` for `gftools builder`.
- [x] Add Make targets for build, QA, and generated readiness reports.
- [x] Add `make help` target for command discovery.
- [x] Add `make decisions` target for open Google Fonts decisions.
- [x] Add generated priority-sorted Google Fonts decision answer sheet.
- [x] Add Make target for DrawBot proof generation using the local
  `eliheuer/drawbot-skia` fork.
- [x] Add preflight and handoff targets that build, regenerate proof evidence,
      then run reports and preflight.
- [x] Add quick handoff-readiness check target for the submission handoff,
  final blocker summary, and next-action queue.
- [x] Add guarded Packager dry-run target with a local `GF_REPO_PATH` default.
- [x] Add Packager wrapper gate tests for source-mode metadata blockers.
- [x] Add quick GitHub API auth check for Packager prerequisites.
- [x] Add generated package dry-run readiness report for local `google/fonts`
  fork state, source-mode, required inputs, and GitHub API credentials.
- [x] Add generated local workflow readiness report for Make targets, local
  tools, build outputs, generated reports, and local repo dependencies.
- [x] Add local preflight that allows only documented drawing/source blockers.
- [x] Add generated variable-font metadata report for `fvar`, `STAT`, and
  `avar` review.
- [x] Add generated `avar` readiness report for the current linear weight-axis
  mapping, identity `avar` table, and resolved warning.
- [x] Add generated Google Fonts axis-registry audit for `wght` display name,
  default, and fallback label review.
- [x] Add GF Arabic Core coverage report for the intended Arabic submission scope.
- [x] Add Google Fonts glyphset readiness report for Latin and Arabic metadata review.
- [x] Add generated PUA/private-use scope report for Google Fonts subsetting
  review.
- [x] Add Arabic shaping smoke test report and preflight checks for GSUB features.
- [x] Add Arabic mark-readiness report for dotted circle, GDEF/GPOS mark tables,
  and source anchors.
- [x] Add consolidated Arabic review packet for coverage, marks, shaping,
  metadata, and proofing handoff.
- [x] Add generated glyph reachability report for unreachable Arabic helper
  glyph and PUA/source cleanup review.
- [x] Add master compatibility report for the Regular and Bold UFO masters.
- [x] Add draft `documentation/google-fonts/DESCRIPTION.en_us.html`.
- [x] Add draft `documentation/google-fonts/ARTICLE.en_us.html` for the newer Google Fonts
  Article flow.
- [x] Keep `documentation/google-fonts/DESCRIPTION.en_us.html` public-facing rather than
  exposing internal submission/review wording.
- [x] Add downstream Google Fonts packaging checklist.
- [x] Add Google Fonts open decision log.
- [x] Add concise Google Fonts decision questionnaire.
- [x] Add name/trademark/CLA and version strategy to the decision surface.
- [x] Add current `google/fonts` Add Font issue-template checks for
  namecheck, copyright authorship, and AI-use disclosure.
- [x] Add generated Add Font issue-template audit from the local
  `google/fonts` fork.
- [x] Add quick Add Font issue draft target tied to the local template audit.
- [x] Add downstream sample-text decision and metadata review notes.
- [x] Add Google Fonts `METADATA.pb` review checklist.
- [x] Add generated designer-profile readiness audit against the local
  `google/fonts/catalog/designers` tree.
- [x] Add generated designer-profile package draft for the expected
  `catalog/designers/eliheuer` profile files.
- [x] Add quick designer-profile check target for the current author and
  metadata designer-string readiness.
- [x] Add guarded designer-profile prepare helper that validates approved
  `info.pb`, `bio.html`, and avatar inputs before writing to `google/fonts`.
- [x] Add designer-profile validator gate tests for `info.pb`, image filename
  and size, biography voice, and placeholder-link rejection.
- [x] Add generated Google Fonts language-metadata audit for the Arabic script,
  Arabic Core language records, and recent Arabic package metadata.
- [x] Add draft Google Fonts submission handoff note.
- [x] Add upstream release/tag checklist for final Google Fonts packaging.
- [x] Add generated release metadata report for source version, built name ID 5,
  and suggested upstream tag review.
- [x] Add generated release/source readiness report for public source commit,
  tag, branch, Packager source mode, and local `google/fonts` fork state.
- [x] Add quick release check target for version, suggested tag, current commit,
  dirty state, and Packager source-state readiness.
- [x] Add generated family-name readiness report for built name IDs, RFN status,
  namecheck, trademark, and CLA review.
- [x] Add generated authorship and AI-disclosure readiness report for the
  current Add Font issue checkbox.
- [x] Add quick PR readiness check target for local Git identity, GitHub auth,
  expected downstream PR shape, and `google/fonts` fork scope.
- [x] Add upstream readiness audit mapped to Google Fonts docs.
- [x] Add Google Fonts project template and recent merged PR audit.
- [x] Add generated local `google/fonts` recent-package audit for selected
  merged examples.
- [x] Add quick recent-GF comparison target for recent downstream packages and
  cited upstream GitHub repos.
- [x] Record project template automation as an explicit maintainer decision.
- [x] Add downstream Google Fonts package preview for final `METADATA.pb` and
  file-layout review.
- [x] Add generated open-placeholder audit for public URL and pending decision
  cleanup before downstream packaging.
- [x] Add generated public upstream URL readiness report from the current git
  remote and placeholder replacement surface.
- [x] Add generated package source-file audit for `METADATA.pb` `source.files`
  and build-from-source/release strategy review.
- [x] Add quick release/source strategy check for public source, tag, and
  Packager mode readiness.
- [x] Add generated release/archive manifest for the selected
  `latest-release` Packager path.
- [x] Add local release/archive zip builder for the final GitHub release asset
  review path.
- [x] Add local release/archive verifier and Packager wrapper gate for the
  selected `latest-release` path.
- [x] Add generated downstream metadata readiness report comparing the package
  preview to the built variable font.
- [x] Add downstream metadata helper test coverage for final `date_added` and
  source commit-hash validation before applying `METADATA.pb`.
- [x] Add generated kerning readiness report for source kerning and generated
  GPOS `kern` status.
- [x] Add `make kerning-proof-check` as a core Google Fonts visual QA target
  using `gftools qa --proof` for spacing and kerning review.
- [x] Add `make kerning-proof-review-check` and
  `documentation/google-fonts/kerning-proof-review.md` so the gftools QA proof review is
  auditable by humans and agents.
- [x] Add `make reference-index-check` and
  `documentation/google-fonts/google-fonts-reference-index.md` so official Google Fonts
  docs and Google Fonts GitHub references are mapped to local evidence.
- [x] Add `documentation/core-qa-process.md` as the canonical human/agent QA
  checklist tying together Fontspector, `gftools qa --proof`, DrawBot proofing,
  readiness reports, and Packager dry runs.
- [x] Add generated final-submission blocker summary across decisions,
  packaging, glyph coverage, Arabic marks, and Fontspector.
- [x] Add quick final-submission blocker target for handoff audits.
- [x] Add generated submission handoff readiness report so the draft Add Font
  issue text stays aligned with the current template and generated reports.
- [x] Add generated upstream structure readiness report against the Google
  Fonts upstream guide and project-template expectations.
- [x] Add generated decision readiness report so maintainer questions, open
  decisions, and downstream apply-to surfaces stay aligned.
- [x] Add generated decision application blocker report so remaining choices
  are mapped to downstream metadata, package dry-run, and final submission gates.
- [x] Add README specimen image in `documentation/assets/readme-specimen.png`.
- [x] Add documentation image provenance note.
- [x] Add the generated specimen image to the Article draft and downstream
  package preview.
- [x] Add generated Fontspector warning report.
- [x] Add generated full Fontspector Markdown report.
- [x] Install `gftools` in the project build environment.
- [x] Build with `gftools builder sources/config.yaml`.
- [x] Run Fontspector with the `googlefonts` profile.
- [x] Fix non-drawing metadata failures found so far: fsType, license names, copyright names, underline thickness, and vertical metrics.
- [x] Add source UFO metadata checks for GF-facing names, metrics, license strings, and installable embedding.
- [x] Add generated source UFO metadata report for source/binary metadata review.
- [x] Add generated Vendor ID readiness report for source UFO
  `openTypeOS2VendorID`, built OS/2 `achVendID`, and Fontspector warning review.
- [x] Check that only the active Virtua Grotesk designspace lives at the top
  level of `sources/`.
- [x] Check that only the active Virtua Grotesk UFO masters live at the top
  level of `sources/`.
- [x] Add `sources/README.md` to document active Google Fonts build inputs.
- [x] Add `sources/archive/README.md` so archived sources are clearly excluded
  from Google Fonts build and packaging inputs.
- [x] Add `.ignore` so generated build artifacts do not pollute repo-wide
  searches during source and handoff review.
- [x] Add generated-font metadata report for names, metrics, licenses, script
  tags, and OS/2 fields.
- [x] Add generated-font checks for GF name length, ASCII family naming, and version strings.
- [x] Add OFL check that no Reserved Font Names are declared after the copyright line.
- [x] Record remaining drawing/glyphset blockers separately from engineering blockers.

## Known baseline issues

- `gftools builder` needs `flattenComponents: false` and `decomposeTransformedComponents: false` for the current UFOs; direct Fontmake fails when those extra builder filters are enabled.
- `build.sh` removes stale builder intermediates before each build so source
  edits do not reuse old generated instance UFOs.
- Static instance generation currently drops the copyright string and turns UFO `openTypeOS2Type` bit data into fsType restrictions; `scripts/fix_gf_metadata.py` patches generated TTFs after build.
- The Google Fonts builder path is the only supported build path in this repo.
- `gftools packager` requires `GitPython`; this is listed in `requirements.txt`.
- `make package-dry-run` defaults to the selected `latest-release` source mode.
  Set `GF_REPO_PATH=/path/to/google/fonts` or use ignored `local.mk` for the
  local `google/fonts` checkout.
- The package dry-run wrapper now requires that checkout to be on `main`, with
  `main` aligned to cached `upstream/main` and `origin/main` when present.
- The package dry-run wrapper refuses to rerun from an existing downstream
  `METADATA.pb` that still contains the placeholder upstream URL, so the known
  unavailable-source failure is surfaced before invoking Packager.
- Keep `GFT_PACKAGER_SOURCE_MODE=latest-release` explicit in copied handoff
  commands even though it is the Make default, so logs and shell history show
  the selected release/archive source mode. Use
  `GFT_PACKAGER_SOURCE_MODE=build-from-source` only if Google Fonts review asks
  to test the source-build path.
- Use the same `GFT_PACKAGER_SOURCE_MODE` with `make package-readiness-check`,
  `make downstream-metadata-check`, and `make package-dry-run` so
  `source.config_yaml`, release/archive metadata, and the no-PR Packager pass
  are reviewed in the same source mode.
- `make package-wrapper-test` creates a temporary `google/fonts`-shaped repo
  and checks that the Packager wrapper blocks source-mode metadata mistakes
  before GitHub auth or Packager can run.
- `make release-archive-test` checks that unsafe release/archive source paths,
  duplicate `source.files`, and unsafe zip entries are blocked.
- `make kerning-proof-check` writes Google Fonts QA HTML proofs to
  `documentation/google-fonts/gftools-qa/` for human spacing and kerning review. This is a
  core QA step before final handoff, especially after kerning changes or a
  kerning deferral decision.
- `make kerning-proof-review-check` regenerates
  `documentation/google-fonts/kerning-proof-review.md`, which enumerates the expected proof
  files by weight and proof type and records the visual review checklist.
- `make test` is expected to fail until the drawing/source FAILs are resolved; use `make preflight` for current handoff readiness. The preflight allows those known FAILs to disappear as drawing work lands, but it fails on any new Fontspector FAIL.

## Latest QA snapshot

Command:

```bash
./scripts/check_gf_fonts.sh
```

Result after the current engineering pass using Fontspector:

- ERROR: 0
- FAIL: 10
- WARN: 54
- PASS: 474

The local command checks the generated variable font and four static TTFs. The
ten FAIL results collapse to the two known check IDs below.

Remaining fails:

- `googlefonts/glyph_coverage`: missing required Google Fonts glyph coverage; drawing/glyphset work.
- `contour_count`: existing encoded glyphs with missing/empty outlines; drawing/source cleanup work.

The current missing-codepoint checklist is in `documentation/google-fonts/missing-gf-latin-core.md`.
It currently reports 219 missing GF Latin Core codepoints out of 319 required.
The current Arabic missing-codepoint checklist is in `documentation/google-fonts/missing-gf-arabic-core.md`.
It tracks Google's `GF_Arabic_Core` glyphset as the minimum Arabic character
coverage target. The report groups missing codepoints into Arabic letters,
Arabic marks, Arabic numbers, Arabic punctuation/symbols, and shared
punctuation/symbols so drawing work can be planned by script behavior. Arabic
shaping still needs separate proofing for positional forms, mark behavior, and
OpenType layout.
The current glyphset readiness summary is in `documentation/google-fonts/gf-glyphset-readiness.md`.
It compares the built variable font against `GF_Latin_Kernel`,
`GF_Latin_Core`, `GF_Arabic_Core`, and `GF_Arabic_Plus`, and records the
language codes associated with the Arabic Core target for metadata review.
The current Google Fonts language-metadata report is in
`documentation/google-fonts/google-fonts-language-metadata.md`. It checks the local
`google/fonts` Arabic script record, Arabic Core language records, and recent
Arabic packages so the planned `subsets: "arabic"` and
`primary_script: "Arab"` metadata remain tied to current downstream evidence.
The current PUA/private-use scope report is in `documentation/google-fonts/pua-scope.md`.
It inventories the 23 currently encoded Private Use Area codepoints in the
built variable font and checks that the active Regular/Bold UFO sources and all
built TTFs expose the same encoded PUA set.
The current Arabic shaping smoke test is in `documentation/glyph-review/arabic-shaping-smoke-test.md`.
It confirms the generated variable font and static TTFs have GSUB features and
that HarfBuzz reaches contextual forms and lam-alef substitution for
representative strings.
The current Arabic mark-readiness report is in `documentation/glyph-review/arabic-mark-readiness.md`.
It tracks the `GF_Arabic_Core` combining marks, U+25CC dotted circle, source
anchors, GDEF mark classification, and built `mark`/`mkmk` GPOS status.
The current Arabic review packet is in `documentation/glyph-review/arabic-review-packet.md`.
It consolidates Arabic Core coverage, missing drawing buckets, mark readiness,
shaping smoke status, language metadata, and Fontspector warning state for
handoff review.
The current contour-count checklist is in `documentation/google-fonts/fontspector-contour-count.md`.
It currently reports 117 contour-count findings: 104 empty/no-contour glyphs and 13 unexpected contour-count glyphs.
The current master compatibility report is in `documentation/source/master-compatibility.md`.
It currently reports 0 blocking structure mismatches and 63 width-only
differences between the Regular and Bold UFO masters.
The current variable-font metadata report is in `documentation/google-fonts/variable-font-metadata.md`.
It records `fvar`, `STAT`, and `avar` status from the built variable TTF so axis
metadata can be reviewed before downstream packaging.
The current Google Fonts axis-registry audit is in
`documentation/google-fonts/google-fonts-axis-registry-audit.md`. It compares the built
`wght` axis against the local `google/fonts` `weight.textproto` entry so
registry naming, default value, and fallback style labels can be reviewed.
The current generated-font metadata report is in `documentation/google-fonts/generated-font-metadata.md`.
It records built name-table, OS/2, vertical metrics, script metadata, and
license strings for the variable font and all static TTFs.
The current source UFO metadata report is in `documentation/source/source-ufo-metadata.md`.
It records source names, versions, metrics, license strings, embedding state,
and glyph counts for the active Regular and Bold UFO masters.
The current designer-profile readiness report is in
`documentation/google-fonts/designer-profile-readiness.md`. It checks current author and
contributor names against the local `google/fonts/catalog/designers` profiles
so the final `METADATA.pb` designer string has an explicit profile follow-up.
Use `make designer-profile-prepare-check` only after the profile link,
biography, and square `eliheuer.png` image are approved; it dry-runs the
guarded copy into the local `google/fonts` fork and writes only with
`scripts/prepare_designer_profile.py --apply`.
The current Article draft is in `documentation/google-fonts/ARTICLE.en_us.html`. Its
contribution link should match the public URL in `OFL.txt` and the source UFO
metadata; revise all three together if the canonical upstream URL changes.
The current project-template and recent-PR audit is in
`documentation/google-fonts/google-fonts-template-and-pr-audit.md`. It records how this repo
maps to the official Google Fonts project template, which optional template
automation is not yet adopted, and what recent merged `google/fonts` PRs imply
for the final package.
The current generated recent-package audit is in
`documentation/google-fonts/recent-google-fonts-packages.md`. It reads selected merged
families from the configured `GF_REPO_PATH` checkout so local package patterns such as
Article use, `primary_script`, `upstream.yaml`/`upstream_info.md`, and
`METADATA.pb` fields can be refreshed.
The current generated Add Font issue-template audit is in
`documentation/google-fonts/google-fonts-add-font-template-audit.md`. It reads the template
from the configured `GF_REPO_PATH` checkout so labels, prompts, and requirement checkboxes
can be refreshed before opening the final issue.
The current generated project-template automation readiness report is in
`documentation/google-fonts/project-template-automation-readiness.md`. It separates
mandatory upstream structure from optional CI, Pages, Renovate, release, and
template-update automation so that decision stays explicit.
The current downstream package preview is in
`documentation/google-fonts/google-fonts-downstream-package-preview.md`. It records the
expected `ofl/virtuagrotesk` layout and a draft `METADATA.pb` shape for final
packaging review.
The current package source-file audit is in
`documentation/google-fonts/package-source-files-audit.md`. It checks the local files listed
in the expected `METADATA.pb` `source.files` block and records whether any are
generated/ignored for the selected GitHub release/archive source strategy.
The current release/source readiness report is in
`documentation/google-fonts/release-source-readiness.md`. It ties the final Packager source
strategy to the current repo commit, suggested tag, dirty state, placeholder
URL status, downstream `source.files`, and local `google/fonts` fork alignment.
The current release/archive manifest is in
`documentation/google-fonts/release-archive-manifest.md`. It records the local
`latest-release` archive inputs, file hashes, whole-archive hash,
deterministic ZIP metadata, and variable-font freshness check before a GitHub
release archive is created. `make release-archive-build` creates the local
ignored review archive at `dist/VirtuaGrotesk-1.000.zip`;
`make release-archive-verify` checks it against the current `source.files`
mapping without rebuilding. `make release-archive-test` checks the path-safety
guards around the release/archive builder and verifier. The GitHub release
command draft is in `documentation/google-fonts/github-release-draft.md`; the matching
release notes are in `documentation/google-fonts/github-release-notes.md`. Regenerate both
with `make release-draft-check`.
The current upstream structure readiness report is in
`documentation/google-fonts/upstream-structure-readiness.md`. It checks mandatory upstream
paths, active build inputs, generated output ignore state, and the
`gftools builder` entrypoint against the Google Fonts upstream and build
guides.
The current decision readiness report is in
`documentation/google-fonts/decision-readiness.md`. It checks the open maintainer questions
against `documentation/google-fonts/google-fonts-decisions.md` and the current Add Font
template audit so policy and metadata answers can be applied consistently.
The current priority-sorted answer sheet is in
`documentation/google-fonts/google-fonts-decision-answer-sheet.md`. It is what
`make decisions` prints for a focused maintainer review pass.
The current decision application blocker map is in
`documentation/google-fonts/decision-application-blockers.md`. It shows which remaining
answers block downstream metadata, package dry runs, or final submission only.
The current Article readiness report is in `documentation/google-fonts/article-readiness.md`.
It checks the Article HTML, image references, size limits, provenance file, and
the decided upstream URL.
The current final-submission blocker summary is in
`documentation/google-fonts/final-submission-blockers.md`. It aggregates open decisions,
placeholder cleanup, Packager source availability, downstream metadata,
Article assets, glyphset coverage, Arabic mark readiness, and Fontspector results.
The current submission handoff readiness report is in
`documentation/google-fonts/submission-handoff-readiness.md`. It checks the draft Add Font
issue text against the current template labels, requirement checkbox count,
version, Fontspector summary, Latin/Arabic gap counts, and handoff report links.
The current Python tooling notes are in
`documentation/python-tooling-notes.md`. They separate direct Python
dependencies from external tools such as Fontspector and DrawBot-skia, and
the local proof tools.
The current warning report is in `documentation/google-fonts/fontspector-warnings.md`.
It starts with a triage summary by check ID, category, affected fonts, and
recommended next action, then keeps the full warning messages for audit.
The current kerning readiness report is in `documentation/google-fonts/kerning-readiness.md`.
It now includes the Google Fonts visual QA proof status and the
`gftools qa --proof` command used for spacing and kerning review.
The current gftools proof review packet is in
`documentation/google-fonts/kerning-proof-review.md`.
Regenerate it with:

```bash
make reports
```

Remaining warnings:

- `gpos_kerning_info`: source kerning is asymmetric between masters and the
  static TTFs do not expose GPOS `kern`; track this in
  `documentation/google-fonts/kerning-readiness.md`.
- `unreachable_glyphs` and `googlefonts/metadata/unreachable_subsetting`: some encoded/substitution reachability needs review.
- `dotted_circle`: U+25CC is required for Arabic mark display and is listed
  in the Arabic Core missing-codepoint report.
- Arabic mark positioning: source anchors and built `mark`/`mkmk` GPOS features
  are not complete yet; track this in `documentation/glyph-review/arabic-mark-readiness.md`.
- `outline_alignment_miss` and `outline_direction`: outline cleanup.
- `googlefonts/vendor_id`: vendor ID is unknown.
- `rupee` and `soft_dotted`: glyphset/source behavior related to the current character set.

Network-dependent checks were skipped in this snapshot.

Fixed during this pass:

- `case_mapping`: added `Aacute` to match existing `aacute`.
- `nested_components`: changed `aacute` to reference the drawn `acute` glyph directly instead of the component-only `acutecomb`.
- `whitespace_glyphs`: added U+00A0 to both masters.
- `valid_glyphnames`: renamed U+00A0 from `nbspace` to `uni00A0`.
- `googlefonts/separator_glyphs`: added U+2028 and U+2029 separator glyphs to both masters.
- Builder config layout: moved the canonical Google Fonts builder config to
  `sources/config.yaml`, matching the official project template convention.
- Article draft: added `documentation/google-fonts/ARTICLE.en_us.html` for the newer Google
  Fonts Article flow.
- Downstream preview: added `documentation/google-fonts/google-fonts-downstream-package-preview.md`
  for the expected `ofl/virtuagrotesk` package layout and `METADATA.pb` shape.
- Downstream metadata tags: recorded that recent new-font PR checklist `tags`
  are a PR/release-review item, while current `METADATA.pb` review should use
  documented `category`, `stroke`, and optional `classifications` fields.
- Python tooling: added `requirements.in`, pinned `requirements.txt`, and
  `documentation/python-tooling-notes.md` so the direct dependency list is
  clear, the install snapshot is reproducible, and Fontspector remains the
  documented QA entrypoint.
- README image: `documentation/assets/readme-specimen.png` is retained as the current README and Article image asset.
- README guide alignment: added GF-recommended changelog, credits, and license
  sections to the root README.
- Article image readiness: reused the generated README specimen image in the
  Article draft and downstream package preview, with provenance in
  `documentation/assets/image-license.txt`.
- Downstream source mapping: added Article HTML and image assets to the
  expected `METADATA.pb` `source.files` mapping.
- Sample text strategy: recorded the conservative default of no custom
  `sample_text` unless Google Fonts review requests it or Arabic specimen text
  needs an explicit override.
- Packager dry run: added `make package-dry-run` as the guarded local command
  for the final no-PR `gftools packager` pass against the configured
  `GF_REPO_PATH` checkout.
- Package readiness check: added `make package-readiness-check` to print
  source strategy, dry-run readiness, downstream metadata readiness/diff, and
  downstream PR readiness with the selected `GFT_PACKAGER_SOURCE_MODE`.
- Downstream metadata check: added source-mode-aware validation for
  `source.config_yaml` before writing into the local `google/fonts` fork.
- Proof generation: use this repo's `./.venv/bin/python`; set
  `DRAWBOT_SKIA_REPO=/path/to/drawbot-skia` or ignored `local.mk` to proof
  against the `eliheuer/drawbot-skia` fork checkout.
- Submission handoff: drafted `documentation/google-fonts/google-fonts-submission-handoff.md` for the eventual Google Fonts issue/packaging step.
- Packaging checklist: drafted `documentation/google-fonts/google-fonts-package-checklist.md` so the final downstream PR step follows `gftools packager` rather than manual copying.
- Metadata review: drafted `documentation/google-fonts/google-fonts-metadata-review.md` for downstream `METADATA.pb` review.
- Generated metadata: added `documentation/google-fonts/generated-font-metadata.md` to audit
  built font names, versions, metrics, license strings, and script tags.
- Source metadata: added `documentation/source/source-ufo-metadata.md` to audit active
  UFO names, versions, metrics, license strings, embedding state, and glyph
  counts.
- Release checklist: drafted `documentation/google-fonts/google-fonts-release-checklist.md`
  so the final upstream tag, commit, version, and source URL are recorded before
  downstream packaging.
- Fontspector warnings: generated `documentation/google-fonts/fontspector-warnings.md` for review alongside the drawing reports.
- Fontspector warning triage: grouped warning report by check ID and handoff
  category so drawing, metadata, and user-decision items are easier to separate.
- Master compatibility: added a report to check glyph presence, Unicode
  assignments, contour structure, components, anchors, and width-only
  differences across the two masters.
- Variable metadata: added a report for built `fvar`, `STAT`, axis values,
  linked Regular/Bold styling, and `avar` status.
- Axis registry metadata: added a report comparing the built `wght` axis to
  the local Google Fonts `axisregistry` Weight entry.
- 600 style naming: changed from `Semi-Bold` to Google Fonts-style `SemiBold`.
- Arabic scope: recorded Arabic as intended submission scope and added the
  `GF_Arabic_Core` missing-codepoint report.
- Arabic coverage planning: grouped the `GF_Arabic_Core` missing-codepoint
  report by drawing/proofing category.
- Glyphset readiness: added a generated report that summarizes Latin/Arabic
  authoring glyphset coverage and metadata implications before downstream
  `METADATA.pb` review.
- Arabic layout: added `features.fea` to the Regular master so all generated
  fonts emit Arabic GSUB features (`init`, `medi`, `fina`, `rlig`) and lam-alef
  substitutions.
- Arabic mark classes: added GDEF mark classification for the current Latin and
  Arabic combining marks; U+25CC dotted circle remains drawing work.
- Arabic mark readiness: added a generated report for Core combining marks,
  dotted circle, source anchors, and `mark`/`mkmk` GPOS feature status.
- Script/language metadata: generated fonts now include OpenType `meta` `dlng`
  and `slng` entries for `Arab, Latn`.
- Source root cleanup: moved old Kinderhugel source files into
  `sources/archive/` so the active source root contains only the Virtua Grotesk
  designspace and UFO masters.
- Source documentation: added `sources/README.md` so the active source set is
  clear before downstream packaging or reviewer handoff.
- Source archive documentation: added `sources/archive/README.md` so older
  Virtua Grotesk and Kinderhugel Grotesk snapshots are clearly reference-only.
- Search hygiene: added `.ignore` so generated instance UFO JSON and other
  local build artifacts stay out of ordinary repo-wide `rg` results.

## Reference docs

- Google Fonts upstream structure: https://googlefonts.github.io/gf-guide/upstream.html
- Google Fonts build guide: https://googlefonts.github.io/gf-guide/build.html
- Google Fonts onboarding criteria: https://googlefonts.github.io/gf-guide/onboarding.html
- Google Fonts PR guide: https://googlefonts.github.io/gf-guide/making-pr.html
- Google Fonts metadata guide: https://googlefonts.github.io/gf-guide/metadata.html
- Google Fonts font requirements: https://googlefonts.github.io/gf-guide/requirements.html
- Google Fonts vertical metrics: https://googlefonts.github.io/gf-guide/metrics.html
- Google Fonts QA: https://googlefonts.github.io/gf-guide/qa.html
- Google Fonts local testing: https://googlefonts.github.io/gf-guide/testing.html
- Google Fonts tools and gftools QA: https://googlefonts.github.io/gf-guide/tools.html
- Google Fonts onboarder visual QA workflow: https://googlefonts.github.io/gf-guide/onboarder-workflow.html
- Fontspector: https://github.com/fonttools/fontspector
