# Google Fonts Submission Handoff

This is a draft handoff note for the eventual Google Fonts issue/packaging step.
It should be updated after drawing work and the remaining open decisions are resolved.
Track those decisions in `documentation/google-fonts/google-fonts-decisions.md`.
Regenerate `documentation/google-fonts/google-fonts-add-font-template-audit.md` from the
local `google/fonts` fork before opening the issue, then update this handoff if
the template changed.
Use `documentation/google-fonts/google-fonts-add-font-issue-draft.md` as the canonical
generated Add Font issue draft; the body below is a handoff summary and must be
kept synchronized with that generated draft before pasting into GitHub.

## Current status

- Upstream repo: `https://github.com/eliheuer/virtua-grotesk`
- Google Fonts issue: pending; open or link before downstream PR
- Family name: Virtua Grotesk
- Namecheck: maintainer-confirmed unique according to `namecheck.fontdata.com`
- License: SIL Open Font License v1.1, no Reserved Font Names currently declared
- Copyright authorship statement: Eli Heuer is the sole copyright
  author/controller for the project as submitted under the OFL
- AI-use disclosure: AI tools were used for engineering, proofing, onboarding,
  repository preparation assistance, and rough Arabic candidate drawing
  scaffolds that still require manual cleanup and final drawing review
- Version: 1.000
- Preliminary name check: no obvious conflicting typeface found in quick web search on 2026-05-22; maintainer has confirmed namecheck/trademark/RFN readiness
- Source format: UFO masters plus `sources/VirtuaGrotesk.designspace`
- Upstream release tag: planned `v1.000` after the final source commit
- Build command: `make build`
- Current handoff gate: `make preflight`
- Final QA gate after drawing: `make test`
- Current Fontspector googlefonts profile: 0 FAIL, 10 WARN, 529 PASS; see
  `documentation/google-fonts/fontspector-googlefonts-report.md`
- Variable font: `fonts/variable/VirtuaGrotesk[wght].ttf`
- Static TTFs: `fonts/ttf/`
- Current Arabic target: `GF_Arabic_Core`; see
  `documentation/glyph-review/arabic-review-packet.md` and
  `documentation/google-fonts/missing-gf-arabic-core.md`
- Current Arabic metadata target: `subsets: "arabic"` and
  `primary_script: "Arab"`; see
  `documentation/google-fonts/google-fonts-language-metadata.md`
- Current complex-script issue label to request/review: `II Arabic / Hebrew / Semitic / RTL`
- Current Article draft: `documentation/google-fonts/ARTICLE.en_us.html`
- Recent downstream PR pattern to follow: cite the upstream repo and exact
  commit in the PR body, include the linked Google Fonts issue, and review
  `primary_script`, subsets, designer order, and Article/Description content.

## Draft Google Fonts issue text

Title:

```text
Add Virtua Grotesk
```

Default issue labels from the current Add Font template:

```text
I New Font, II Submission
```

Body:

```markdown
**Font Project Git Repo URL:**

https://github.com/eliheuer/virtua-grotesk

**Super short description of the Font Family:**

Virtua Grotesk is a geometric grotesk with a Weight axis from Regular to Bold.
Its defining construction detail is a system of 16-unit chamfered corners,
giving sharp junctions a consistent 45-degree bevel while preserving a
monolinear texture.

**Requirements:**

- [ ] The entire font project is available in a GitHub repository and licensed under the [OFL](https://openfontlicense.org/open-font-license-official-text/).
- [ ] The source files are available in the repo.
- [ ] I am the sole copyright author/controller for the project as submitted under the OFL. AI tools were used for engineering, proofing, onboarding, repository preparation assistance, and rough Arabic candidate drawing scaffolds that still require manual cleanup and final drawing review.
- [ ] There are no "Reserved Font Names" in the OFL license information, or in the project documentation of any known upstream projects. If there are RFNs, they are not used in whole or in part in this family name, or this issue should discuss how Google can work with their use.
- [ ] The family name is unique according to [namecheck.fontdata.com](https://namecheck.fontdata.com/).
- [ ] The app-menu family name is definitive: `Virtua Grotesk`, and it does not include any copyright holder's full name or acronym.
- [ ] The font supports at least the Google Fonts `GF_Latin_Core` glyphset from [github.com/googlefonts/glyphsets](https://github.com/googlefonts/glyphsets).
- [ ] The repo has the [Google Fonts preferred upstream repo structure](https://googlefonts.github.io/gf-guide/upstream.html).
- [ ] The maintainer has read, agrees with, and complies with the full [Google Fonts contributing requirements](https://googlefonts.github.io/gf-guide/index#pre-production-getting-your-fonts-ready-for-gf).
- [ ] The maintainer will maintain the repository and participate in the onboarding process.

**Version:**

Current source and generated fonts expose version `1.000`. Confirm this is the
intended first Google Fonts submission version before packaging.

**Sources and Build:**

Sources are UFO masters with a designspace:

- `sources/VirtuaGrotesk-Regular.ufo`
- `sources/VirtuaGrotesk-Bold.ufo`
- `sources/VirtuaGrotesk.designspace`

Build:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make build
```

Local QA:

```bash
make preflight
make test
make kerning-proof-check
```

`make preflight` allows only documented drawing/source blockers while the
family is still in production. `make test` should be green before submission.
`make kerning-proof-check` generates the Google Fonts visual QA HTML proof used
for spacing and kerning review; review that output before calling kerning,
spacing, or a kerning deferral final.

**Scope:**

First-submission script scope:

- Latin plus Arabic
- Arabic minimum coverage target: Google Fonts `GF_Arabic_Core`
- PUA/private icon block included or deferred after reviewing
  `documentation/google-fonts/pua-scope.md`

Current Arabic Core gaps from the latest generated report:

- Arabic letters: 0
- Arabic marks: 0
- Arabic numbers: 0
- Arabic punctuation and symbols: 0
- Shared punctuation and symbols: 0

Current Latin Core gap from the latest generated report:

- GF Latin Core missing codepoints: 0

## Current blockers before submission

- Human-review and clean up the generated Latin Core candidate outlines.
- Clean the scaffolded Arabic candidate drawings now that GF Arabic Core cmap coverage is present.
- Resolve Fontspector `contour_count` / `no-contour` findings.
- Proof Arabic shaping, positional forms, marks, and OpenType layout.
- Complete Arabic mark positioning readiness: dotted circle, source anchors,
  and built `mark`/`mkmk` GPOS features.
- Review `documentation/glyph-review/arabic-shaping-smoke-test.md` after each drawing/build pass.
- Review `documentation/glyph-review/arabic-mark-readiness.md` after each Arabic mark pass.
- Review `documentation/glyph-review/arabic-review-packet.md` as the consolidated Arabic
  coverage, mark, shaping, metadata, and proofing handoff packet.
- Decide whether PUA/private icons are in scope for the first submission, then
  regenerate `documentation/google-fonts/pua-scope.md`.
- Decide whether kerning must be completed before submission.
- Vendor ID is decided as `FTGD` for Font Garden and is applied in sources and
  generated fonts; keep reviewing `documentation/google-fonts/vendor-id-readiness.md` after
  source or build changes.
- Review decision-linked warning buckets together: vendor ID, kerning, `avar`,
  PUA/reachability, and downstream unreachable subsetting.
- Author/contact display, copyright-authorship statement, AI-use disclosure,
  namecheck result, and public upstream URL are decided; keep them synchronized
  with `documentation/google-fonts/authorship-disclosure-readiness.md`,
  `documentation/google-fonts/family-name-readiness.md`, and
  `documentation/google-fonts/public-upstream-readiness.md`.
- Use the planned `v1.000` upstream release tag after the final source commit;
  see
  `documentation/google-fonts/google-fonts-release-checklist.md`.
- Keep the decided Article flow in the downstream package and recheck
  `documentation/google-fonts/ARTICLE.en_us.html` with `documentation/google-fonts/article-readiness.md`
  after final source or URL changes.

**Image:**

Use `documentation/assets/readme-specimen.png` unless a better final specimen image is
prepared before opening the issue.
```

## Packaging notes

Google Fonts packaging should happen only after a `google/fonts` issue exists
and after `make test` is green, or after any remaining FAILs are explicitly
accepted by a Google Fonts reviewer. The local `gftools packager` entrypoint is
importable in the project .venv:

```bash
./.venv/bin/gftools packager --help
```

The packager requires a checkout of `google/fonts` as its `repo_path`.
The public Google Fonts package guide shows the first packaging pass without
`-p`, then rerunning with `-p` when ready to open or update the pull request.
The installed `gftools packager` also supports `-i ISSUE_NUMBER`; pass the issue
number once it exists so the PR is linked to the submission discussion. Use
`-p` only when the downstream package is ready to open or update a pull request.
This repo's guarded local dry-run command for the selected release/archive
source mode is:

```bash
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

`make package-dry-run` currently defaults to `latest-release`, but keep the
environment variable in copied handoff commands so the selected source mode is
visible in logs and shell history.

Expected downstream PR shape if the final package is opened manually or
reviewed after Packager:

```text
Branch: gftools_packager_ofl_virtuagrotesk
Changed directory: ofl/virtuagrotesk
Title: Virtua Grotesk : 1.000 added
Body: Taken from the upstream repo <repo-url> at commit <commit-url>.
```

The Google Fonts PR guide says to open an issue before submitting a PR. Keep
the downstream PR scoped to one changed directory, `ofl/virtuagrotesk`, and
compare across forks from the branch on the `eliheuer/fonts` fork unless a
Google Fonts team member asks for a direct upstream branch.

The local wrapper checks GitHub API credentials before invoking Packager. It
accepts an explicit `GH_TOKEN`, or exports one from a valid GitHub CLI login.
Check the current credential state before a dry run:

```bash
gh auth status -h github.com
make github-auth-check
```

If local GitHub CLI auth is stale, refresh it first:

```bash
gh auth login -h github.com
```

Latest local dry-run status, 2026-05-24: the fork checkout at
`$GF_REPO_PATH` is synced to `google/fonts` `main`, but GitHub API
credentials are not currently usable. The first no-PR Packager pass
created `$GF_REPO_PATH/ofl/virtuagrotesk/METADATA.pb`, which is
still the unpopulated Packager starter template. Current generated state:
`Wrapper can reach Packager: no`; first blocker:
`existing downstream METADATA.pb is still the Packager starter template`.
Current blocking findings:
`existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable`.
Required local package inputs are present, and 4/5 are tracked by git;
1/5 is currently untracked. The source-mode dry-run gate also records that
default branch packaging must expose untracked `source.files`, release/archive
packaging must include those untracked local source files, and build-from-source
packaging must keep the source build path public and tracked.

Populate that downstream `METADATA.pb` from
`documentation/google-fonts/google-fonts-downstream-package-preview.md` after the final
release/source commit and GitHub release archive are public, and refresh GitHub
CLI/API auth with `gh auth login -h github.com` before rerunning the dry run.
For the selected `latest-release` path, the downstream `source.archive_url`
must be a GitHub release download URL ending in `.zip`, not a generic
repository or tag URL.
Use the checked local sequence, and keep the first Packager rerun as no-PR:

```bash
git -C $GF_REPO_PATH status --short -- ofl/virtuagrotesk
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
./.venv/bin/python scripts/prepare_downstream_metadata.py --apply
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

The next known blocker is upstream/source availability: Packager cannot fetch
the final `source.files` payload from branch `main` yet, or from the selected
`v1.000` release/archive until that release exists. Publish the final upstream
source commit and release asset, then rerun
`GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` before using
`-p`.
Before writing into the local fork, run:

```bash
make downstream-metadata-check
```

This dry-run helper extracts the expected `METADATA.pb` from
`documentation/google-fonts/google-fonts-downstream-package-preview.md`, rejects pending
placeholders and Packager starter values, and reports the exact target file.
Use the same `GFT_PACKAGER_SOURCE_MODE` here that will be used for Packager, so
`source.config_yaml` and `source.archive_url` are validated against the selected
source mode. In `latest-release` mode, `source.archive_url` must resolve to the
final GitHub release download `.zip` asset.
After the preview is final, use `scripts/prepare_downstream_metadata.py --apply`
to write the checked metadata into
`$GF_REPO_PATH/ofl/virtuagrotesk/METADATA.pb`.

See `documentation/google-fonts/google-fonts-package-checklist.md` for the final upstream
and downstream review checklist. Use
`documentation/google-fonts/downstream-pr-readiness.md` to check the issue-first rule,
expected `gftools_packager_ofl_virtuagrotesk` branch, one-directory PR scope,
title/body provenance, local fork state, CLA identity, and GitHub auth before
opening the downstream pull request. Use
`documentation/google-fonts/decision-readiness.md` to confirm open maintainer decisions
still map one-to-one to the active question list, and review its prioritized
question packet before public package or PR work. Use
`documentation/google-fonts/upstream-structure-readiness.md` to confirm the repo still
matches the preferred Google Fonts upstream shape before packaging. Use
`documentation/google-fonts/google-fonts-metadata-review.md` when reviewing generated
`METADATA.pb`. Use `documentation/google-fonts/google-fonts-template-and-pr-audit.md` and
`documentation/google-fonts/recent-google-fonts-packages.md` to compare the final package
against the official template, detailed recent package examples, and the latest
local `gftools_packager_ofl_*` merge evidence. Use
`documentation/google-fonts/google-fonts-language-metadata.md` to confirm the Arabic
language/subset metadata evidence before reviewing the final `METADATA.pb`. Use
`documentation/google-fonts/google-fonts-downstream-package-preview.md` as the expected
downstream file-layout and `METADATA.pb` shape during local package review.
Use `documentation/google-fonts/downstream-metadata-readiness.md` to check the generated
metadata preview fields, including the source block, subsets, and SemiBold
style spelling. Use `documentation/google-fonts/downstream-metadata-diff.md` to compare the
current Packager-created downstream `METADATA.pb` against the expected preview.
Use `make downstream-metadata-check` before applying that preview into the
local `google/fonts` fork.
Use `documentation/google-fonts/package-source-files-audit.md` to confirm the `source.files`
mapping, variable-font-first source layout, Article asset destinations, and
expected Packager branch
`gftools_packager_ofl_virtuagrotesk`. Use
`documentation/google-fonts/package-dry-run-readiness.md` to review the current
source-mode blockers, including tracked/untracked package inputs, before
running Packager.
Use `documentation/google-fonts/authorship-disclosure-readiness.md` to keep the Add Font
authorship and AI-use disclosure wording explicit before checking the combined
template requirement. Use `documentation/google-fonts/pr-identity-readiness.md` to confirm
git identity, GitHub API credentials, and CLA status before packaging or
opening a downstream PR. Use `documentation/google-fonts/designer-profile-readiness.md` and
`documentation/google-fonts/designer-profile-package-draft.md` to confirm the designer
string has a matching or prepared Google Fonts catalog profile. Use
`make designer-profile-check` after changing author or metadata designer
strings. Use
`documentation/google-fonts/drawbot-runtime-readiness.md` and
`documentation/google-fonts/local-workflow-readiness.md` to confirm final proofs use the
local `eliheuer/drawbot-skia` fork and that the local handoff commands are
runnable.
Use `documentation/google-fonts/missing-gf-latin-core.md` and
`documentation/google-fonts/missing-gf-arabic-core.md` to keep the issue text aligned with
current glyphset coverage gaps. Use `documentation/glyph-review/arabic-review-packet.md` as
the compact Arabic scope and proofing packet before requesting Arabic/RTL
review labels.
Use `documentation/google-fonts/vendor-id-readiness.md`,
`documentation/google-fonts/kerning-readiness.md`,
`documentation/google-fonts/kerning-proof-review.md`, `documentation/google-fonts/avar-readiness.md`,
`documentation/google-fonts/pua-scope.md`, `documentation/google-fonts/glyph-reachability.md`,
`documentation/google-fonts/numeric-feature-readiness.md`, and
`documentation/google-fonts/fontspector-warnings.md` to review decision-linked warning
buckets, the gftools QA proof review packet, and numeric-feature requirements
before checking the Add Font contributing requirements.
Use `documentation/google-fonts/release-source-readiness.md` to confirm the final public
source commit, tag, branch, selected source mode, and local `google/fonts` fork
state. Use `documentation/google-fonts/release-archive-manifest.md` to confirm the local
review zip contains every expected release/archive file and matching SHA-256
hashes before creating the GitHub release asset. Use
`documentation/google-fonts/github-release-draft.md` and
`documentation/google-fonts/github-release-notes.md` to review the exact release command,
tag, title, archive asset, and release notes before publishing the final
GitHub release. Use
`documentation/google-fonts/article-readiness.md` to confirm Article HTML, image,
and upstream-link readiness. Use `documentation/google-fonts/next-actions.md` as the
owner-grouped remaining-work queue. Use
`documentation/google-fonts/final-submission-blockers.md` as the final compact open-blocker
summary. Regenerate
`documentation/google-fonts/submission-handoff-readiness.md` before opening the Add Font
issue to catch stale values in this handoff note.

Run the final no-PR package pass with the selected latest-release source mode;
use build-from-source only if Google Fonts review asks for that fallback:

```bash
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run
```
