# Decision Readiness

This generated report checks that the maintainer-facing Google Fonts
decision log and question list stay aligned. It does not answer
policy, legal, authorship, source-release, or design-scope questions
on the maintainer's behalf.

## Summary

- Decision log entries: 15
- Open decisions: 2
- Decided decisions: 13
- Decision question prompts: 8
- Decision question prompts with answer guidance: 8 / 8
- Open decisions with matching question prompts: 2 / 2
- Decided decisions omitted from question prompts: no
- Open decisions with apply-to blocks: 2 / 2
- Open decision apply-to surface items: 8
- Open decision local path patterns present: 5 / 5
- Open decision non-file or downstream surfaces: 3
- Add Font template audit present: yes
- Add Font template authorship prompt tracked: yes
- Add Font template namecheck prompt tracked: yes

## Decision Map

| Decision | Status | Question prompt | Apply-to block |
| --- | --- | --- | --- |
| Public upstream URL | decided | yes | yes |
| Packager source strategy | decided | yes | yes |
| Author/contact lines | decided | yes | yes |
| Family name, namecheck, trademarks, and CLA | decided | yes | yes |
| Copyright authorship and AI disclosure | decided | yes | yes |
| Custom sample text | decided | no | yes |
| First-submission script scope | decided | n/a | yes |
| Private-use icon block | open | yes | yes |
| Vendor ID | decided | yes | yes |
| Kerning | open | yes | yes |
| `avar` | decided | no | yes |
| Version strategy | decided | no | yes |
| Upstream release tag | decided | no | yes |
| Article or legacy description | decided | no | yes |
| Project template automation | decided | no | yes |

## Prioritized Question Packet

Answer priority `1` items before public package or PR work. Priority `2`
items should be settled before final handoff text is frozen. Priority `3`
items can be decided while drawing and QA cleanup continue, but should not
remain open for the final submission.

| Priority | Question | Why answer now | Prompt present |
| --- | --- | --- | --- |
| 3 | PUA Icon Block | Affects glyph scope, subsetting review, and whether PUA rationale belongs in the issue. | yes |
| 3 | Kerning Scope | Decides whether kerning warnings are blockers or explicitly deferred. | yes |

## Question Prompt Inventory

| Question | Has question text | Has answer guidance | Has why-it-matters |
| --- | --- | --- | --- |
| Public Upstream URL | yes | yes | yes |
| Packager Source Strategy | yes | yes | yes |
| Author and Contributor Strings | yes | yes | yes |
| Family Name, Namecheck, Trademarks, and CLA | yes | yes | yes |
| PUA Icon Block | yes | yes | yes |
| Vendor ID | yes | yes | yes |
| Kerning Scope | yes | yes | yes |
| Copyright Authorship and AI Disclosure | yes | yes | yes |

## Apply-To Surface Inventory

| Decision | Surface | Local path patterns | Present now |
| --- | --- | --- | --- |
| Public upstream URL | `OFL.txt` | `OFL.txt` | 1 / 1 |
| Public upstream URL | `sources/*/fontinfo.plist` | `sources/*/fontinfo.plist` | 1 / 1 |
| Public upstream URL | `scripts/fix_gf_metadata.py` | `scripts/fix_gf_metadata.py` | 1 / 1 |
| Public upstream URL | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| Public upstream URL | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| Packager source strategy | `.gitignore` | `.gitignore` | 1 / 1 |
| Packager source strategy | `README.md` | `README.md` | 1 / 1 |
| Packager source strategy | `build.sh` | `build.sh` | 1 / 1 |
| Packager source strategy | `scripts/package_gf_dry_run.sh` | `scripts/package_gf_dry_run.sh` | 1 / 1 |
| Packager source strategy | `documentation/google-fonts/google-fonts-package-checklist.md` | `documentation/google-fonts/google-fonts-package-checklist.md` | 1 / 1 |
| Packager source strategy | `documentation/google-fonts/google-fonts-downstream-package-preview.md` | `documentation/google-fonts/google-fonts-downstream-package-preview.md` | 1 / 1 |
| Packager source strategy | `documentation/google-fonts/package-source-files-audit.md` | `documentation/google-fonts/package-source-files-audit.md` | 1 / 1 |
| Author/contact lines | `AUTHORS.txt` | `AUTHORS.txt` | 1 / 1 |
| Author/contact lines | `CONTRIBUTORS.txt` | `CONTRIBUTORS.txt` | 1 / 1 |
| Author/contact lines | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| Family name, namecheck, trademarks, and CLA | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| Family name, namecheck, trademarks, and CLA | `documentation/google-fonts/google-fonts-package-checklist.md` | `documentation/google-fonts/google-fonts-package-checklist.md` | 1 / 1 |
| Family name, namecheck, trademarks, and CLA | downstream Google Fonts issue/PR text | n/a | n/a |
| Copyright authorship and AI disclosure | `AUTHORS.txt` | `AUTHORS.txt` | 1 / 1 |
| Copyright authorship and AI disclosure | `CONTRIBUTORS.txt` | `CONTRIBUTORS.txt` | 1 / 1 |
| Copyright authorship and AI disclosure | `OFL.txt`, if the copyright string changes | `OFL.txt` | 1 / 1 |
| Copyright authorship and AI disclosure | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| Copyright authorship and AI disclosure | downstream Google Fonts issue text | n/a | n/a |
| Custom sample text | downstream `METADATA.pb`, only if a custom override is accepted | n/a | n/a |
| Custom sample text | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| Custom sample text | `documentation/google-fonts/google-fonts-package-checklist.md` | `documentation/google-fonts/google-fonts-package-checklist.md` | 1 / 1 |
| First-submission script scope | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| First-submission script scope | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| First-submission script scope | `documentation/google-fonts/missing-gf-arabic-core.md` | `documentation/google-fonts/missing-gf-arabic-core.md` | 1 / 1 |
| First-submission script scope | `documentation/google-fonts/fontspector-warnings.md` | `documentation/google-fonts/fontspector-warnings.md` | 1 / 1 |
| First-submission script scope | source glyphset, features, and proofs | n/a | n/a |
| Private-use icon block | source glyphset | n/a | n/a |
| Private-use icon block | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| Private-use icon block | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| Vendor ID | `sources/*/fontinfo.plist` | `sources/*/fontinfo.plist` | 1 / 1 |
| Vendor ID | `scripts/fix_gf_metadata.py` if post-build patching remains necessary | `scripts/fix_gf_metadata.py` | 1 / 1 |
| Vendor ID | `documentation/google-fonts/fontspector-warnings.md` | `documentation/google-fonts/fontspector-warnings.md` | 1 / 1 |
| Kerning | UFO kerning/groups/features | n/a | n/a |
| Kerning | `build.sh` | `build.sh` | 1 / 1 |
| Kerning | `make kerning-proof-check` | n/a | n/a |
| Kerning | `documentation/google-fonts/kerning-readiness.md` | `documentation/google-fonts/kerning-readiness.md` | 1 / 1 |
| Kerning | `documentation/google-fonts/fontspector-warnings.md` | `documentation/google-fonts/fontspector-warnings.md` | 1 / 1 |
| `avar` | `scripts/fix_gf_metadata.py` | `scripts/fix_gf_metadata.py` | 1 / 1 |
| `avar` | `sources/VirtuaGrotesk.designspace`, if a non-linear mapping is added later | `sources/VirtuaGrotesk.designspace` | 1 / 1 |
| `avar` | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| `avar` | `documentation/google-fonts/fontspector-warnings.md` | `documentation/google-fonts/fontspector-warnings.md` | 1 / 1 |
| Version strategy | `sources/*/fontinfo.plist` | `sources/*/fontinfo.plist` | 1 / 1 |
| Version strategy | `documentation/google-fonts/google-fonts-metadata-review.md` | `documentation/google-fonts/google-fonts-metadata-review.md` | 1 / 1 |
| Version strategy | `documentation/google-fonts/google-fonts-release-checklist.md` | `documentation/google-fonts/google-fonts-release-checklist.md` | 1 / 1 |
| Version strategy | downstream `METADATA.pb` | n/a | n/a |
| Upstream release tag | `documentation/google-fonts/google-fonts-release-checklist.md` | `documentation/google-fonts/google-fonts-release-checklist.md` | 1 / 1 |
| Upstream release tag | `documentation/google-fonts/google-fonts-submission-handoff.md` | `documentation/google-fonts/google-fonts-submission-handoff.md` | 1 / 1 |
| Upstream release tag | downstream Google Fonts issue/PR text | n/a | n/a |
| Article or legacy description | `documentation/google-fonts/ARTICLE.en_us.html` | `documentation/google-fonts/ARTICLE.en_us.html` | 1 / 1 |
| Article or legacy description | `documentation/google-fonts/google-fonts-package-checklist.md` | `documentation/google-fonts/google-fonts-package-checklist.md` | 1 / 1 |
| Article or legacy description | downstream package generated by `gftools packager` | n/a | n/a |
| Project template automation | `.github/workflows/`, if adopted | n/a | n/a |
| Project template automation | `Makefile` | `Makefile` | 1 / 1 |
| Project template automation | `README.md` | `README.md` | 1 / 1 |
| Project template automation | `documentation/google-fonts/google-fonts-template-and-pr-audit.md` | `documentation/google-fonts/google-fonts-template-and-pr-audit.md` | 1 / 1 |
| Project template automation | `documentation/google-fonts/google-fonts-release-checklist.md` | `documentation/google-fonts/google-fonts-release-checklist.md` | 1 / 1 |

## Mechanical Apply Coverage

| Surface | Helper or report | Current coverage | Notes |
| --- | --- | --- | --- |
| Public upstream URL | `scripts/apply_public_upstream_url.py` | ready after maintainer-approved URL | Dry-runs and applies placeholder URL replacements across source metadata, handoff docs, and downstream preview surfaces. |
| Downstream METADATA.pb | `make downstream-metadata-check` and `scripts/prepare_downstream_metadata.py --apply` | guarded until placeholders clear | Validates the preview and writes into the local `google/fonts` fork only after pending URL, designer, commit, and branch values are resolved. |
| Packager dry run | `make package-dry-run` | guarded no-PR dry run | Checks local `google/fonts` topology, package inputs, source mode, starter metadata, and GitHub API auth before invoking Packager. |
| Add Font issue and handoff text | `make issue-draft` and `documentation/google-fonts/submission-handoff-readiness.md` | generated drafts | Keeps current template labels, issue text, Fontspector counts, Arabic scope, and report references synchronized after decisions are applied. |
| Designer profile package | `make designer-profile-check` | audit and draft only | Checks whether final designer strings have matching Google Fonts catalog profiles or a prepared designer-profile request. |
| Decision-linked warnings | `documentation/google-fonts/fontspector-warnings.md` and `documentation/google-fonts/final-submission-blockers.md` | evidence only | Groups Vendor ID, kerning, avar, PUA/reachability, and subsetting warnings for maintainer acceptance or follow-up fixes. |

## Apply Before Final Submission

- Record maintainer answers in `documentation/google-fonts/google-fonts-decisions.md`
  before editing source metadata or downstream package previews.
- Keep `documentation/google-fonts/google-fonts-decision-questions.md` focused on
  open questions only; decided scope belongs in the decision log and
  generated evidence reports.
- Rerun `make preflight` after any decision is answered so proof
  evidence, generated reports, handoff draft, and package checklist
  stay synchronized.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
