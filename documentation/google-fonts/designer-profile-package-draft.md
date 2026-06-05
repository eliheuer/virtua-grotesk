# Designer Profile Package Draft

This generated draft prepares the Google Fonts designer-profile files
for maintainer review. It is not a finished downstream profile until
the biography text and square image are approved.

## Readiness Status

| Gate | Current state | Required before action |
| --- | --- | --- |
| Author/contact decision | decided | decided |
| Downstream metadata designer string | not blocked by pending decision | exact final string |
| Final source commit/tag | blocked by pending release commit | required for family package, not for profile draft |
| Local designer profile path | missing | inspect existing profile or create one |
| Profile inputs | 3 unresolved | final link, biography, and image |

## Target Profile

- Designer string: `Eli Heuer`
- Catalog slug: `eliheuer`
- Catalog slug ASCII-only: yes
- Catalog slug has hyphen: no
- Downstream directory: `catalog/designers/eliheuer`
- Avatar filename matches slug: yes
- Profile PR scope: one designer profile only
- Local google/fonts checkout: `GF_REPO_PATH_NOT_CONFIGURED`
- Local designers directory exists: no
- `gftools add-designer` available: yes
- Candidate info.pb validator present: yes
- Candidate info.pb draft exists: yes
- Candidate info.pb draft passes validator: yes
- Candidate info.pb link: `https://github.com/eliheuer`
- Candidate image validator present: yes
- Candidate image validator enforces filename: yes
- Candidate bio validator present: yes
- Candidate bio validator enforces third-person voice: yes
- Candidate bio draft exists: yes
- Candidate bio draft passes validator: yes
- Candidate bio links: `https://github.com/eliheuer`
- Candidate info/bio link consistency: yes
- Designer profile prepare helper present: yes
- Designer profile prepare helper checks info/bio link consistency: yes
- Designer profile prepare helper dry-run ready: no
- Designer profile prepare helper blocking findings: 2
- Prepare blocker is missing approved image input: yes
- Prepare blocker is downstream checkout cleanliness: no
- Approved profile inputs ready to apply: no
- Downstream profile checkout ready to apply: no
- Target profile directory already exists: no
- Expected profile files already present: 0 / 3
- Profile path collision risk: no
- Draft placeholders still unresolved: 3
- Missing final inputs: designer profile link decision, maintainer-approved biography, square 100-300px profile image
- Profile link may be blank if the approved Google Fonts profile uses
  `link: ""`; many current `google/fonts` designer profiles do this.
- Suggested profile branch: `designer/eli-heuer-profile`
- Expected family package branch: `virtuagrotesk`
- Profile timing default: create or update the designer profile before
  the family package if Google Fonts review needs a catalog match first;
  keep it separate unless reviewers ask for a combined patch.

## Required Downstream Files

- `catalog/designers/eliheuer/info.pb`
- `catalog/designers/eliheuer/bio.html`
- `catalog/designers/eliheuer/eliheuer.png`

## Local google/fonts Collision Check

| Downstream path | Exists locally |
| --- | --- |
| `catalog/designers/eliheuer/info.pb` | no |
| `catalog/designers/eliheuer/bio.html` | no |
| `catalog/designers/eliheuer/eliheuer.png` | no |

If the target directory exists before the profile decision is applied,
inspect it manually and decide whether the existing profile can be reused
or needs a separate update PR.

## Guarded Prepare Helper

Use the guarded helper after the profile link, biography, and image
are approved. It validates `info.pb`, `bio.html`, and the avatar image,
requires any non-empty `info.pb` link to appear in `bio.html`,
checks the local `google/fonts` checkout, and writes files only when
`--apply` is passed.

```bash
make designer-profile-prepare-check
./.venv/bin/python scripts/prepare_designer_profile.py --image path/to/eliheuer.png --apply
```

- Default info candidate: `documentation/google-fonts/designer-profile-candidate/info.pb`
- Default bio candidate: `documentation/google-fonts/designer-profile-candidate/bio.html`
- Default image candidate: `documentation/google-fonts/designer-profile-candidate/eliheuer.png`
- Candidate info/bio link consistency: yes
- Link consistency check implemented in prepare helper: yes
- Current dry-run ready: no
- Current dry-run blocking findings: 2
- Missing approved image input blocks prepare helper: yes
- Downstream checkout cleanliness blocks prepare helper: no
- Approved profile inputs ready to apply: no
- Downstream profile checkout ready to apply: no
- Current dry-run blocker details:
  - image file does not exist: ./documentation/google-fonts/designer-profile-candidate/eliheuer.png
  - google/fonts checkout does not exist: GF_REPO_PATH_NOT_CONFIGURED

## Exact Downstream Worktree Plan

Use this only after the biography, link, and image are approved.
Keep this work separate from the family package branch unless a
Google Fonts reviewer explicitly asks for a combined patch.

```bash
cd GF_REPO_PATH_NOT_CONFIGURED
git switch main
git pull --ff-only upstream main
git switch -c designer/eli-heuer-profile
```

Before creating files in the downstream checkout, confirm the target
profile path is still absent and the worktree is clean outside any
intentional profile files:

```bash
test ! -e GF_REPO_PATH_NOT_CONFIGURED/catalog/designers/eliheuer
git -C GF_REPO_PATH_NOT_CONFIGURED status --short -- catalog/designers/eliheuer
git -C GF_REPO_PATH_NOT_CONFIGURED status --short
```

Create the profile with `gftools add-designer`, then hand-edit
`info.pb` and `bio.html` to match the approved profile text:

```bash
./.venv/bin/gftools add-designer GF_REPO_PATH_NOT_CONFIGURED/catalog/designers "Eli Heuer" --img_path path/to/eliheuer.png
```

Validate the profile inputs from this repo before committing the
downstream profile files:

```bash
cd /path/to/virtua-grotesk
./.venv/bin/python scripts/validate_designer_profile_info.py GF_REPO_PATH_NOT_CONFIGURED/catalog/designers/eliheuer/info.pb "Eli Heuer" eliheuer.png
./.venv/bin/python scripts/validate_designer_profile_image.py GF_REPO_PATH_NOT_CONFIGURED/catalog/designers/eliheuer/eliheuer.png eliheuer.png
./.venv/bin/python scripts/validate_designer_profile_bio.py GF_REPO_PATH_NOT_CONFIGURED/catalog/designers/eliheuer/bio.html
make reports
```

Expected downstream commit scope:

- `catalog/designers/eliheuer/info.pb`
- `catalog/designers/eliheuer/bio.html`
- `catalog/designers/eliheuer/eliheuer.png`

## Maintainer Input Checklist

| Input | Current value | Needed before downstream profile work |
| --- | --- | --- |
| Final `METADATA.pb` designer string | `Eli Heuer` applied in downstream preview | Keep profile `info.pb` spelling exactly matched. |
| Designer profile link | candidate `https://github.com/eliheuer`; maintainer approval pending | Approve this URL, provide one canonical website/social URL, or deliberately leave `link: ""` in `info.pb`. |
| Biography | candidate draft in `documentation/google-fonts/designer-profile-candidate/bio.html`; maintainer approval pending | Approve or replace a third-person `bio.html` snippet that passes `make designer-profile-bio-check`; if `info.pb` uses a non-empty link, include that same URL in the bio links. |
| Profile image | `path/to/eliheuer.png` placeholder | Provide a square 100-300px image that passes `make designer-profile-image-check`. |
| PR timing | profile missing in local google/fonts checkout | Decide whether this profile PR should land before, alongside, or after the family PR. |

Decision-safe default:

- Use `Eli Heuer` as the profile name because it is the decided
  downstream metadata designer string and the only current AUTHORS
  catalog-credit candidate.
- Keep this as a separate designer-profile draft; do not create files in
  `$GF_REPO_PATH/catalog/designers` until the biography and
  image are approved.
- If the family package has intentional dirty files under
  `$GF_REPO_PATH/ofl/virtuagrotesk`, either commit, stash,
  or review that work before applying a separate designer-profile branch.

## Candidate `bio.html`

A validator-ready but unapproved biography draft lives at `documentation/google-fonts/designer-profile-candidate/bio.html`.
It uses the GitHub profile as a temporary profile link; replace the link
if a website or different social profile should be the canonical
Google Fonts designer-profile URL.

Validate the candidate before using it downstream:

```bash
make designer-profile-bio-check BIO=documentation/google-fonts/designer-profile-candidate/bio.html
```

The candidate passes local validation now, but it still needs
maintainer approval before it is copied into `google/fonts`.

## Candidate `info.pb`

A validator-ready but unapproved `info.pb` draft lives at `documentation/google-fonts/designer-profile-candidate/info.pb`.
It uses the GitHub profile as a temporary `link` value; replace it
if a website or different social profile should be the canonical
Google Fonts designer-profile URL, or set `link: ""` if no public
profile link should be shown.

Validate the candidate before using it downstream:

```bash
make designer-profile-info-check INFO=documentation/google-fonts/designer-profile-candidate/info.pb
```

The candidate passes local validation now, but the profile `link`
is still temporary until the canonical public URL is approved or
the blank-link option is explicitly chosen.
If `link` is non-empty, the guarded prepare helper requires the same
URL to appear in `bio.html`; this keeps the visible biography link and
`info.pb` profile link from drifting.

Current candidate shape:

```proto
designer: "Eli Heuer"
link: "https://github.com/eliheuer"
avatar {
  file_name: "eliheuer.png"
}
```

The `designer` value must exactly match the final downstream
`METADATA.pb` designer string.
The avatar `file_name` must match the image file inside the same
profile directory.

Validate the final candidate `info.pb` before committing the designer
profile:

```bash
./.venv/bin/python scripts/validate_designer_profile_info.py GF_REPO_PATH_NOT_CONFIGURED/catalog/designers/eliheuer/info.pb "Eli Heuer" eliheuer.png
```

## `bio.html` Requirements

- Maintainer-authored English biography.
- Third-person voice.
- First-person pronouns are rejected by the local validator.
- More than 200 characters and less than 1000 characters.
- Around 100 words.
- One or two links to a website or social profile.
- HTML snippet using paragraph tags, not a complete HTML document.
- Links should use real `http` or `https` URLs, visible link text,
  and `target="_blank"`.
- If `info.pb` uses a non-empty `link`, include that exact URL in one
  biography link.
- Social links should be labeled by service name, such as `GitHub`,
  `Instagram`, `LinkedIn`, `Twitter`, or `X`.
- Website link text should omit the `http://` or `https://` protocol,
  using only the readable domain or site name.

Draft shape:

```html
<p>Eli Heuer is ...</p>

<p><a href="https://REPLACE-WITH-APPROVED-URL" target="_blank">REPLACE-WITH-APPROVED-LABEL</a></p>
```

Validate the final candidate biography before creating or updating the
designer profile:

```bash
make designer-profile-bio-check BIO=path/to/bio.html
```

## Image Requirements

- Filename: `eliheuer.png`
- Filename must match the profile directory slug exactly.
- PNG or JPEG.
- Square 1:1 image.
- Between 100px and 300px.
- Crops cleanly as a circle.

## Suggested Local Creation Command

Validate the final candidate image before running `gftools add-designer`:

```bash
make designer-profile-image-check IMAGE=path/to/eliheuer.png
```

Use `gftools add-designer` to create the initial downstream profile
directory once the final image is available, then hand-edit
`bio.html` as needed:

```bash
./.venv/bin/gftools add-designer GF_REPO_PATH_NOT_CONFIGURED/catalog/designers "Eli Heuer" --img_path path/to/eliheuer.png
```

## Relationship To Family Package

- The designer profile does not unblock the local release archive by
  itself; that still needs the final source commit/tag.
- The designer profile does unblock the downstream `METADATA.pb` designer
  profile check because the final metadata designer string is already
  applied.
- The family package should still be limited to
  `ofl/virtuagrotesk/*`; the profile path belongs in a separate
  `catalog/designers/*` PR unless Google Fonts asks otherwise.
- Google Fonts also accepts designer profile additions or updates through
  the official profile form; if that route is chosen, keep this draft as
  the local evidence packet and record the submitted profile link, bio,
  and image before final packaging.

## Profile Request Form Packet

Use this packet if the profile is submitted through the Google Fonts
designer-profile form instead of a direct `catalog/designers` PR.

- Form: https://docs.google.com/forms/d/e/1FAIpQLSehvbqqgL5Dlv9WG0mmBVNfFAjoMIx-2d1YJNrU7C-zKBNkcw/viewform
- Name: `Eli Heuer`
- Linked family: `Virtua Grotesk`
- Canonical profile link: pending maintainer input, or explicit blank-link choice
- Biography: pending maintainer-approved `bio.html` text
- Image: pending validated square `eliheuer.png`
- Keep the submitted profile text and image in sync with the downstream
  `METADATA.pb` designer string.
- The profile guide says platform updates appear after team review; allow
  roughly 2-4 weeks after merge/registration before expecting the public
  profile to appear.

## Before Profile PR

- Confirm the profile `designer` value still exactly matches the final
  downstream `METADATA.pb` designer string.
- Replace the draft biography with maintainer-approved text.
- Add the final square profile image.
- Run this repo's Google Fonts preflight.
- Add or update one designer profile per PR if Google Fonts asks for
  the profile before or alongside the family submission.
- Mention the linked font family in the designer-profile PR.
- Request the `Designer profile` and `Ready for review` labels.
- Add the PR to Traffic Jam if following the Google Fonts onboarder
  workflow.

References:

- https://googlefonts.github.io/gf-guide/profile.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/onboarding.html
- https://github.com/google/fonts/tree/main/catalog/designers
- https://docs.google.com/forms/d/e/1FAIpQLSehvbqqgL5Dlv9WG0mmBVNfFAjoMIx-2d1YJNrU7C-zKBNkcw/viewform
