# Google Fonts Open Decisions

This is the canonical decision log for the Google Fonts onboarding pass. Update
this file first when a decision is made, then apply the decision to source
metadata, docs, and generated review artifacts.

## Public upstream URL

Status: decided

Decision:

```text
https://github.com/eliheuer/virtua-grotesk
```

The canonical public upstream URL for Google Fonts is
`https://github.com/eliheuer/virtua-grotesk`.

Current local evidence:

- Origin-derived candidate:
  `https://github.com/eliheuer/virtua-grotesk`
- Replacement surface and preview:
  `documentation/public-upstream-readiness.md`

Why it matters:

- Used in `OFL.txt` first line and generated name ID 0.
- Used in `documentation/google-fonts-submission-handoff.md`.
- Used in downstream `METADATA.pb` `source.repository_url`.
- Packager fetches `source.files` from this URL and branch through the GitHub
  API; the URL cannot remain a placeholder for a successful dry run.

Apply to:

- `OFL.txt`
- `sources/*/fontinfo.plist`
- `scripts/fix_gf_metadata.py`
- `documentation/google-fonts-submission-handoff.md`
- `documentation/google-fonts-metadata-review.md`

## Packager source strategy

Status: decided

Decision:

- Keep `fonts/` generated locally and package from a GitHub release/archive.
- Create a GitHub release for the final source state and publish a release
  archive that contains the files mapped in downstream `source.files`.
- Use `source.archive_url` in downstream `METADATA.pb` and run Packager with
  `GFT_PACKAGER_SOURCE_MODE=latest-release`.
- Omit `source.config_yaml` from the downstream metadata preview for the
  release/archive path unless Google Fonts review asks for build metadata.

Reference patterns:

- `ofl/googlesanscode/METADATA.pb` uses a GitHub release `archive_url` for
  Google Sans Code prebuilt variable fonts.
- `ofl/scheherazadenew/METADATA.pb` uses a GitHub release `archive_url` for an
  Arabic-script family.
- `ofl/amiri/METADATA.pb` uses a GitHub release `archive_url` for another
  Arabic-script family.
- `ofl/kedebideri/METADATA.pb` uses a GitHub release `archive_url` for a recent
  non-Latin Google Fonts package.

Options:

- Use the default public-branch source mapping and make every downstream
  `source.files` path available from the public upstream branch.
- Commit built fonts under `fonts/` in this upstream repo if that is the chosen
  way to expose the served variable TTF.
- Keep fonts generated locally/CI only and package from a verified build.
- Publish a release archive and use `source.archive_url` for the downstream
  Packager pass.
- Use Packager's `--build-from-source` mode if Google Fonts accepts the public
  source/build path as reproducible.

Current recommendation:

- Use the release/archive strategy deliberately because generated binaries
  should stay out of the public branch.
- Make the release archive the reviewed source of the packaged files.
- Treat build-from-source as a separate review choice, because it depends on
  public/tracked build inputs and Google Fonts acceptance of
  `source.config_yaml` for this family.
- Estedad is the closest sampled Arabic-script upstream comparison. It keeps
  `primary_script: "Arab"` downstream and records `source.config_yaml`, so
  Virtua can cite that pattern only if build-from-source is chosen deliberately.

Why it matters:

- The GF upstream structure guide lists `fonts/` as part of the expected repo
  shape.
- This repo currently treats `fonts/` as generated output and ignores it.
- `build.sh` deletes and recreates `fonts/` at build start to prevent stale
  binaries.
- A local Packager dry run on 2026-05-22 reached the download step and failed
  because `fonts/variable/VirtuaGrotesk[wght].ttf` was not available from the
  placeholder upstream URL on branch `main`.
- The final `METADATA.pb` must either point at a branch/tag where the listed
  `source.files` exist, or use a GitHub release download `.zip` archive URL
  that contains them.
- `documentation/package-source-files-audit.md` shows the current served
  variable TTF exists locally but is ignored/generated, so default branch fetch
  cannot work until this decision is applied.
- The same audit currently shows `source.files` as 1/4 tracked and
  build-from-source inputs as 4/6 tracked; the final strategy must expose the
  untracked local inputs before Packager can cite a public branch, release, or
  reproducible source build.
- Recent merged upstream repos in the local audit expose built fonts in
  `fonts/`, so Virtua's ignored generated font policy must be reconciled with
  the final Packager source strategy before the downstream dry run can be final.

Apply to:

- `.gitignore`
- `README.md`
- `build.sh`
- `scripts/package_gf_dry_run.sh`
- `documentation/google-fonts-package-checklist.md`
- `documentation/google-fonts-downstream-package-preview.md`
- `documentation/package-source-files-audit.md`

## Author/contact lines

Status: decided

Decision:

```text
Eli Heuer
```

Use `Eli Heuer` as the final upstream author/designer display string and the
candidate downstream `METADATA.pb` `designer` value. Keep `AUTHORS.txt` and
`CONTRIBUTORS.txt` as-is for now unless Google Fonts asks for email/contact
formatted lines.

Why it matters:

- `AUTHORS.txt` is the copyright-author source of truth.
- `CONTRIBUTORS.txt` is contributor attribution.
- The downstream `METADATA.pb` `designer` string and any designer profile work
  need a confirmed display string.

Apply to:

- `AUTHORS.txt`
- `CONTRIBUTORS.txt`
- `documentation/google-fonts-metadata-review.md`

## Family name, namecheck, trademarks, and CLA

Status: decided

Decision:

- `Virtua Grotesk` is confirmed as the final public app-menu family name.
- The family name is maintainer-confirmed as unique according to
  `namecheck.fontdata.com`.
- No trademark, catalog-name, or Reserved Font Name concerns are known for the
  submission.
- The copyright holder has signed the Google CLA for the downstream Google
  Fonts contribution.

Current family name:

```text
Virtua Grotesk
```

Current preliminary name check:

- A quick web search on 2026-05-22 for `"Virtua Grotesk" font`,
  `"Virtua Grotesk" typeface`, and `"VirtuaGrotesk"` did not show another
  obvious typeface using the same family name.
- This is only a project-screening note, not legal or trademark clearance.

Why it matters:

- Google Fonts expects family names to be clear, ASCII, and acceptable for the
  catalog.
- The current `google/fonts` Add Font issue template asks submitters to confirm
  uniqueness according to `namecheck.fontdata.com`.
- The template also asks for the app-menu family name to be definitive and to
  avoid copyright holder full names or acronyms.
- Google Fonts strongly discourages Reserved Font Names in OFL submissions.
- Copyright holders must sign the Google CLA before a downstream PR can be
  accepted.

Apply to:

- `documentation/google-fonts-submission-handoff.md`
- `documentation/google-fonts-package-checklist.md`
- downstream Google Fonts issue/PR text

## Copyright authorship and AI disclosure

Status: decided

Decision:

- The Google Fonts Add Font issue can state that Eli Heuer is the sole
  copyright author/controller for the project as submitted under the OFL.
- AI-use disclosure: AI tools were used for engineering, proofing, onboarding,
  and repository preparation assistance, not for glyph drawing.

Recorded Add Font issue constraints:

- The issue can state that Eli Heuer is the sole copyright author/controller
  for the project as submitted under the OFL.
- The issue should disclose that AI tools were used for engineering, proofing,
  onboarding, and repository preparation assistance, not for glyph drawing.
- The current Add Font template combines copyright authorship and AI disclosure
  into one checkbox; keep the final issue wording as one maintainer-approved
  statement.

Why it matters:

- The current `google/fonts` Add Font issue template requires this authorship
  confirmation and AI-use disclosure.
- This is a maintainer/legal statement, not a drawing task.

Apply to:

- `AUTHORS.txt`
- `CONTRIBUTORS.txt`
- `OFL.txt`, if the copyright string changes
- `documentation/google-fonts-submission-handoff.md`
- downstream Google Fonts issue text

## Custom sample text

Status: decided

Decision:

- Do not add a custom `sample_text` block for the first Google Fonts package.
- Rely on Google Fonts language data through `primary_script: "Arab"` and
  default Arabic textprotos unless review identifies a specific specimen
  problem.

Current state:

- No custom `sample_text` block is planned in the downstream `METADATA.pb`
  preview.
- Arabic is in first-submission scope, and `primary_script: "Arab"` is the
  current metadata target.
- Local Arabic shaping/proofing is tracked separately in generated reports and
  proof artifacts.

Why it matters:

- The metadata guide documents `sample_text` as an override and says to use it
  sparingly.
- Custom sample text can make the Google Fonts specimen less flexible.
- Arabic visual proofing is still required, but proofing and catalog text
  overrides are separate decisions.

Apply to:

- downstream `METADATA.pb`, only if a custom override is accepted
- `documentation/google-fonts-metadata-review.md`
- `documentation/google-fonts-package-checklist.md`

## First-submission script scope

Status: decided

Decision:

- Include Arabic support in the Google Fonts submission.
- Use Google's `GF_Arabic_Core` glyphset as the minimum Arabic character
  coverage target.
- Keep Arabic shaping, positional forms, mark behavior, and OpenType layout
  proofing as required work before final submission.

Rejected option:

- Latin-only first submission.

Why it matters:

- Arabic scope affects `METADATA.pb` subsets and `primary_script`.
- Arabic scope affects proofing expectations and Fontspector warning review.
- Arabic support requires both Unicode coverage and shaping/proof review; the
  codepoint coverage checklist alone is not sufficient.

Apply to:

- `documentation/google-fonts-submission-handoff.md`
- `documentation/google-fonts-metadata-review.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/fontspector-warnings.md`
- source glyphset, features, and proofs

## Private-use icon block

Status: open

Options:

- Include the PUA icon block in the Google Fonts submission.
- Defer/remove the PUA icon block for the first Google Fonts submission.

Why it matters:

- `documentation/pua-scope.md` records the current generated PUA inventory and
  should be regenerated after any PUA encoding decision.
- Private-use glyphs can complicate reachability/subsetting review.
- If kept, they need an explicit rationale in the Google Fonts issue/PR.

Apply to:

- source glyphset
- `documentation/google-fonts-submission-handoff.md`
- `documentation/google-fonts-metadata-review.md`

## Vendor ID

Status: decided

Decision:

```text
FTGD
```

`FTGD` is registered to Font Garden in the Microsoft registered font vendor
list. Verified against Microsoft Learn's registered font vendors page on
2026-05-24.

Why it matters:

- Fontspector reports `googlefonts/vendor_id` when generated fonts use `NONE`.
- A real four-character vendor ID should be applied consistently in both source
  UFOs and generated fonts.

Apply to:

- `sources/*/fontinfo.plist`
- `scripts/fix_gf_metadata.py` if post-build patching remains necessary
- `documentation/fontspector-warnings.md`

## Kerning

Status: open

Current state:

- The generated variable font exposes a GPOS `kern` feature.
- The generated static TTFs do not expose GPOS `kern`.
- Regular UFO currently has no `kerning.plist`; Bold UFO has source kerning
  data.
- The GF builder path is the current source of truth.
- `make kerning-proof-check` runs Google Fonts `gftools qa --proof`; the latest
  generated proof output covers Regular, Medium, SemiBold, and Bold.

Why it matters:

- Fontspector reports `gpos_kerning_info`.
- Kerning may be required for the design quality expected in the first PR.
- Google Fonts visual proof review should include the generated
  `gftools qa --proof` HTML output whether kerning is completed now or
  explicitly deferred.

Apply to:

- UFO kerning/groups/features
- `build.sh`
- `make kerning-proof-check`
- `documentation/kerning-readiness.md`
- `documentation/fontspector-warnings.md`

## `avar`

Status: decided

Decision:

- Ship the current linear `wght` 400-700 axis without an `avar` table for the
  first Google Fonts submission.
- Treat Fontspector's `mandatory_avar_table` result as a reviewed warning while
  the axis remains intentionally linear.

Current state:

- The axis is linear from `wght=400` to `wght=700`.
- No `avar` table is emitted.

Why it matters:

- Fontspector reports `mandatory_avar_table`.
- The warning can be acceptable for a linear axis, but the decision should be
  explicit before submission.

Apply to:

- `sources/VirtuaGrotesk.designspace`, if a non-linear mapping is added
- `documentation/google-fonts-submission-handoff.md`
- `documentation/fontspector-warnings.md`

## Version strategy

Status: decided

Decision:

- Use version `1.000` for the first Google Fonts submission.
- Revisit versioning only after the first public release or if the final source
  state requires a pre-submission version bump.

Current state:

- Source UFOs and generated fonts expose version `1.000`.

Why it matters:

- Google Fonts requires version increments for upgrades.
- If this is the first public Google Fonts submission, `1.000` is a reasonable
  initial version; if there is already a public release, upgrade semantics
  should be confirmed.

Apply to:

- `sources/*/fontinfo.plist`
- `documentation/google-fonts-metadata-review.md`
- `documentation/google-fonts-release-checklist.md`
- downstream `METADATA.pb`

## Upstream release tag

Status: decided

Decision:

- Use `v1.000` as the final upstream tag name for the first Google Fonts
  package, aligned with the `1.000` font version.
- Create the tag only after drawing/source work, metadata decisions, and the
  final public source commit are complete.

Current recommendation:

```text
v1.000
```

Why it matters:

- The Google Fonts upstream structure guide notes that releases should be
  tagged.
- The Google Fonts issue and downstream packaging notes should point to a stable
  upstream commit or tag.
- The tag should match the confirmed version strategy and the built font version
  strings.

Apply to:

- `documentation/google-fonts-release-checklist.md`
- `documentation/google-fonts-submission-handoff.md`
- downstream Google Fonts issue/PR text

## Article or legacy description

Status: decided

Decision:

- Use the Article flow for the first Google Fonts package.
- Keep `documentation/DESCRIPTION.en_us.html` as a shorter legacy fallback only
  if Google Fonts review asks for it.

Current state:

- `documentation/ARTICLE.en_us.html` exists as the upstream Article draft.
- `documentation/DESCRIPTION.en_us.html` exists as a shorter legacy description.

Why it matters:

- Recent merged new-font PRs commonly include `article/ARTICLE.en_us.html`.
- The Article needs a final upstream repository link.
- Article images, if added, need provenance and Google Fonts image-size review.

Apply to:

- `documentation/ARTICLE.en_us.html`
- `documentation/google-fonts-package-checklist.md`
- downstream package generated by `gftools packager`

## Project template automation

Status: decided

Decision:

- Defer Google Fonts project-template automation for the first submission.
- Keep the local `make handoff` / `make preflight` gate as the required
  onboarding workflow until the public URL, source strategy, and Arabic drawing
  work are settled.
- If CI is added later, adapt it deliberately around this repo's Fontspector,
  DrawBot, DesignBot, and readiness-report workflow.

Current state:

- The repo follows the required Google Fonts upstream structure and keeps a
  local `make handoff` gate.
- The Google Fonts project template also includes GitHub Actions, GitHub Pages
  QA/proof publishing, Renovate, `make customize`, and `make
  update-project-template`.
- The local QA gate uses Fontspector through `make test`; do not copy the
  older FontBakery-oriented template QA workflow without adapting it.
- Those template automations have not been added.

Why it matters:

- The upstream guide says template scripts and actions are useful but not
  mandatory.
- This repo has project-specific UFO/designspace, DrawBot, DesignBot, and
  report-generation workflows that need a deliberate CI adaptation.
- Any adopted CI should call the same Fontspector-based checks used locally.
- Public GitHub Pages or release automation should not expose stale proofs or
  incomplete onboarding reports.

Apply to:

- `.github/workflows/`, if adopted
- `Makefile`
- `README.md`
- `documentation/google-fonts-template-and-pr-audit.md`
- `documentation/google-fonts-release-checklist.md`
