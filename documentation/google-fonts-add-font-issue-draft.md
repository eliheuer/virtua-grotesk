# Google Fonts Add Font Issue Draft

This generated draft follows the current Add Font issue template from the
local `google/fonts` checkout. It is intentionally not ready to paste until
the open maintainer decisions and drawing/source blockers are resolved.

## Template Evidence

- Template path: `/Users/eli/GH/forks/fonts/.github/ISSUE_TEMPLATE/1_add-font.md`
- Template commit: `c5b52261e`
- Template checkout status: `## main...origin/main`
- Alignment with `upstream/main`: `0 ahead, 0 behind`
- Alignment with `origin/main`: `0 ahead, 0 behind`
- Title pattern: `Add [Font Name]`
- Default labels: `I New Font, II Submission`
- Requirement checkbox count: 10

## Issue Title

```text
Add Virtua Grotesk
```

## Labels

```text
I New Font, II Submission
```

Request Arabic/RTL script labeling only after Arabic coverage, shaping,
and proof review are ready for Google Fonts review.

## Draft Body

**Font Project Git Repo URL:**

https://github.com/eliheuer/virtua-grotesk

**Super short description of the Font Family:**

Virtua Grotesk is a variable geometric grotesk with a Weight axis and Latin plus Arabic support in preparation.

**Requirements:**

By opening this issue, I confirm the project meets the following requirements:

- [ ] The entire font project is available in a Github repository (repo) and licensed under the [OFL](https://openfontlicense.org/open-font-license-official-text/)
  - Draft status: Local evidence: public canonical upstream URL is recorded.
- [ ] The source files are available in the repo
  - Draft status: Blocked until the final release/archive exposes every `source.files` input.
- [ ] I am the sole copyright author of the entire project, or all other copyright authors have licensed their work to me under the OFL, and I commit to clearly disclosing if AI tools were used in the creation of this project.
  - Draft status: Local evidence: copyright-authorship and AI-use wording is recorded.
- [ ] There are no "Reserved Font Names" in the OFL license information, or in the project documentation of any known upstream projects. If there are RFNs, they are not used in whole or in part in this family name, or, I want to discuss how Google can work with my use of them.
  - Draft status: Local evidence: none declared after copyright line; trademark/catalog-name clearance: confirmed by maintainer.
- [ ] The family name is unique according to [namecheck.fontdata.com](https://namecheck.fontdata.com/)
  - Draft status: Maintainer confirmation: confirmed by maintainer at `namecheck.fontdata.com`.
- [ ] The name of the font family expected to appear on app menus must be very clearly communicated and definitive. It should not include any copyright holder's full names or acronyms.
  - Draft status: Local evidence: app-menu candidate appears in built names: yes.
- [ ] The font supports at least the Google Fonts 'Latin Core' glyphset from [github.com/googlefonts/glyphsets](https://github.com/googlefonts/glyphsets) ([direct link](https://github.com/googlefonts/glyphsets/blob/main/data/results/txt/nice-names/GF_Latin_Core.txt))
  - Draft status: Blocked by drawing/source work: GF Latin Core missing codepoints: 219.
- [ ] The repo has the [Google Fonts preferred upstream repo structure](https://googlefonts.github.io/gf-guide/upstream.html)
  - Draft status: Local evidence: 11 / 11.
- [ ] I have read, agree with, and comply with, the full [Google Fonts contributing requirements](https://googlefonts.github.io/gf-guide/index#pre-production-getting-your-fonts-ready-for-gf)
  - Draft status: Blocked until documented final blockers are resolved or accepted; 10 FAIL results.
- [ ] I will maintain the repository and participate in the onboarding process (addressing, solving, and responding to issues, merging pull requests, etc)
  - Draft status: Maintainer confirmation required before opening the issue.

**Image:**

Attach `documentation/readme-specimen.png` or an updated specimen image
after final drawing/source work is complete.

## Arabic Scope Status

Arabic support is in first-submission scope. Do not ask for Arabic/RTL
review labels until these generated reports show the coverage and layout
work is ready for review.

- GF Arabic Core missing codepoints: 57.
- Arabic letters missing: 13.
- Arabic marks missing from GF Arabic Core: 3.
- U+25CC dotted circle present: no.
- Built mark/mkmk GPOS features present: no.
- Fonts with `arab/dflt` GSUB smoke coverage: 5 / 5.
- Fonts with `arab/dflt` GPOS smoke coverage: 1 / 5.
- Required evidence: `documentation/arabic-review-packet.md`,
  `documentation/missing-gf-arabic-core.md`,
  `documentation/arabic-mark-readiness.md`, and
  `documentation/arabic-shaping-smoke-test.md`.

## Numeric Feature Status

Google Fonts expects default ASCII digits to be proportional and
complemented by a Tabular Numbers (`tnum`) feature.

- Default ASCII digits present in every built font: yes.
- Default ASCII digits are proportional in every built font: yes.
- `tnum` feature present in every built font: yes.
- `tnum` substitutes all ten ASCII digits in every built font: yes.
- `tnum` substitutes to equal-width digits in every built font: yes.
- Numeric feature requirement ready: yes.
- Required evidence: `documentation/numeric-feature-readiness.md`.

## Designer Profile Status

The final downstream `designer` string needs a matching Google Fonts
`catalog/designers` profile, or a profile request prepared alongside
the family submission.

- Current candidate designer string: `Eli Heuer`.
- Candidate catalog slug: `eliheuer`.
- Candidate downstream profile directory: `catalog/designers/eliheuer`.
- AUTHORS catalog-credit candidates: 1.
- Candidate designer profiles missing: 1.
- Final metadata designer strings present: yes.
- Pending metadata designer placeholders: 0.
- Target profile directory already exists: no.
- Expected profile files already present: 0 / 3.
- Draft profile inputs still unresolved: 3.
- Required evidence: `documentation/designer-profile-readiness.md` and
  `documentation/designer-profile-package-draft.md`.

## Decision-Linked Warning Status

These are not glyph drawing tasks, but they need a maintainer decision
or explicit deferral before checking the Add Font requirements.

- Vendor ID: source UFO IDs `FTGD`; generated fonts use
  `FTGD`; Fontspector vendor warnings: 0;
  decision: decided.
- Kerning: source kerning in every master: no;
  static GPOS `kern`: no; warnings: 4;
  GF visual proof output: yes;
  proof covers expected instances: yes;
  proof review packet files: 16 / 16;
  decision: open.
- `avar`: table present: no; warning count: 1;
  decision: decided.
- PUA/reachability: PUA codepoints: 23;
  `unreachable_glyphs` warnings: 5;
  `googlefonts/metadata/unreachable_subsetting` warnings:
  5; decide whether private-use glyphs
  ship in the first submission.
- Required evidence: `documentation/vendor-id-readiness.md`,
  `documentation/kerning-readiness.md`,
  `documentation/kerning-proof-review.md`,
  `documentation/avar-readiness.md`,
  `documentation/pua-scope.md`, and
  `documentation/fontspector-warnings.md`.

## Package Dry-Run Status

Do not open the downstream PR from this state. The first package pass
should stay as a no-PR local dry run until the release/archive,
metadata, and GitHub auth blockers are cleared.

- Selected Packager source mode: `latest-release`.
- Wrapper can reach Packager: no.
- First package dry-run blocker: existing downstream METADATA.pb is still the Packager starter template.
- GitHub API credentials ready: no.
- Required local package inputs tracked: 1 / 5.
- Required local package inputs untracked: 4.
- Default branch mode has untracked source-file blocker: yes.
- Latest-release/archive mode has untracked source-file blocker: yes.
- Build-from-source mode has untracked build-input blocker: yes.
- Downstream METADATA.pb is starter template: yes.
- Expected metadata lines missing from downstream file: 17 / 23.
- Downstream metadata preview ready to apply: no.
- Downstream metadata apply blockers: 3.
- Source strategy note: review `documentation/packager-source-strategy.md`.
- Run `make downstream-metadata-check` before applying final metadata,
  using the same `GFT_PACKAGER_SOURCE_MODE` planned for Packager so
  `source.config_yaml` and `source.archive_url` are validated against
  the selected source mode. For `latest-release`, `source.archive_url`
  must be a GitHub release download URL ending in `.zip`,
  then use `scripts/prepare_downstream_metadata.py --apply` only after
  the dry run reports `Ready to apply: yes`.
- Required evidence: `documentation/package-dry-run-readiness.md`,
  `documentation/downstream-metadata-diff.md`, and
  `documentation/packager-source-strategy.md`.

## Finalize Before Opening

- Confirm the public repository URL still matches the final release source.
- Keep the approved authorship and AI-use disclosure wording synchronized.
- Confirm the family name at `namecheck.fontdata.com`.
- Clear the package dry-run blocker stack or document the reviewed
  no-PR Packager result.
- Resolve or explicitly document accepted Fontspector FAILs.
- Regenerate this draft with `make preflight` after final source,
  metadata, or Google Fonts template changes.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md
