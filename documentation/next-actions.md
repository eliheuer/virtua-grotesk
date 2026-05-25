# Google Fonts Next Actions

This generated report condenses the final blocker stack into an owner-grouped queue. It does not replace the detailed evidence reports; it points to the next concrete work needed before the Google Fonts issue, package dry run, and downstream PR.

## Snapshot

- Maintainer decisions: 2 open, 13 decided
- Decision answer packet ready: yes
- Local workflow preflight ready: yes
- Package dry run reaches Packager: no
- Package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template
- Package dry-run blocking findings: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable
- Selected Packager source mode: `latest-release`
- Downstream starter METADATA.pb present: yes
- Downstream `source.config_yaml` present: no; source-strategy review needed: no
- GitHub release draft: `v1.000` / `Virtua Grotesk 1.000`; archive files: yes; hashes: yes
- Fontspector googlefonts profile: 10 FAIL, 49 WARN, 479 PASS
- GF visual kerning proof: every master has source kerning: no; static GPOS kern: no; warnings: 4; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review

## Maintainer Decisions

| Priority | Action | Evidence |
| --- | --- | --- |
| P3 | Resolve PUA Icon Block. Affects glyph scope, subsetting review, and whether PUA rationale belongs in the issue. | `documentation/google-fonts-decision-answer-sheet.md` |
| P3 | Resolve Kerning Scope. Decides whether kerning warnings are blockers or explicitly deferred. | `documentation/google-fonts-decision-answer-sheet.md` |

## Decision Unblock Order

| Order | Maintainer answer needed | Mechanical follow-up after answer |
| --- | --- | --- |
| 1 | PUA Icon Block | Resolve or explicitly defer private-use glyph scope and reachable/subsetting warnings before final submission. |
| 2 | Kerning Scope | Complete kerning or record an explicit first-submission deferral, then run `make kerning-proof-check` and `make kerning-proof-review-check`. |

## Drawing And Source Work

| Action | Current state | Evidence |
| --- | --- | --- |
| Complete GF Latin Core coverage. | 219 missing codepoints | `documentation/missing-gf-latin-core.md` |
| Complete GF Arabic Core coverage. | 57 missing codepoints | `documentation/missing-gf-arabic-core.md` |
| Plan Arabic source construction batches. | missing codepoints: 57; suggested glyph names: 88; positional forms: 31; missing in both masters: 88; reuse prerequisites checked: 13; missing prerequisites: 0; dotted circle missing: yes | `documentation/arabic-source-work-checklist.md` |
| Add Arabic marks, dotted circle, anchors, and mark/mkmk if Arabic remains in scope. | 3 missing marks; dotted circle: no; anchors: no; mark/mkmk: no | `documentation/arabic-review-packet.md` |
| Resolve source contour/no-contour findings. | 117 source glyph findings, 585 all-font rows | `documentation/fontspector-contour-count.md` |
| Review GF visual spacing/kerning proof. | every master has source kerning: no; static GPOS kern: no; warnings: 4; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review | `documentation/kerning-readiness.md`; `documentation/kerning-proof-review.md` |
| Resolve or intentionally keep PUA and unreachable helper glyphs. | 19 unique unreachable; Arabic helpers: 5; mark helpers: 13; source cleanup: 1 | `documentation/glyph-reachability.md` |

## Packaging And Handoff

| Action | Current state | Evidence |
| --- | --- | --- |
| Monitor placeholder audit; no public placeholder strings currently block handoff. | public blockers: 0 URLs, 0 pending markers; generated echoes: 2; internal/total URL echoes: 1 | `documentation/open-placeholder-audit.md` |
| Replace the Packager starter `METADATA.pb` with final downstream metadata and restore API auth. | reaches Packager: no; first blocker: existing downstream METADATA.pb is still the Packager starter template; blockers: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable; auth: no; inputs: yes | `documentation/downstream-metadata-diff.md` |
| Align Git/GitHub identity before downstream commits. | source identity: yes; google/fonts identity: yes; downstream name matches CLA: yes; final commit identity: yes; gh auth: invalid token; API auth: no; source: unavailable; CLA: confirmed by maintainer for the copyright holder | `documentation/pr-identity-readiness.md`; `documentation/downstream-pr-readiness.md` |
| Create the final release/archive source package for Packager. | 0 missing locally, 1 ignored/generated, tracked: 1/4, untracked: 3; release/archive source mode: `latest-release`; archive must include currently untracked package files: `fonts/variable/VirtuaGrotesk[wght].ttf`, `documentation/ARTICLE.en_us.html`, `documentation/readme-specimen.png`; `source.config_yaml` review: no | `documentation/packager-source-strategy.md` |
| Publish the final GitHub release asset after the final source commit and tag. | tag: v1.000; title: Virtua Grotesk 1.000; command: yes; archive: `dist/VirtuaGrotesk-1.000.zip`; notes: `documentation/github-release-notes.md`; notes final: no; expected files: yes; hashes: yes; source commit: Pending final release/source commit | `documentation/github-release-draft.md` |
| Prepare the Google Fonts designer profile request for `Eli Heuer`. | author candidates: 1; contributor-only: 0; missing profiles: 1; metadata placeholders: 0; draft inputs: 3; path collision: no | `documentation/designer-profile-package-draft.md` |
| Clean or review the local `google/fonts` fork before the final package pass. | origin: eliheuer/fonts; upstream: google/fonts; topology: yes; exists: yes; branch: main; upstream/main: 0/0; clean: no; dirty outside package: 0 | `documentation/package-dry-run-readiness.md` |
| Keep Add Font issue and submission handoff synchronized with generated evidence. | template labels: `I New Font, II Submission`; handoff labels: yes; issue draft: yes; Fontspector: yes; maintenance: yes; unchecked: yes; report refs: 40; source modes: yes | `documentation/submission-handoff-readiness.md` |

## Run Order

1. Record the remaining maintainer decisions in `documentation/google-fonts-decisions.md`.
2. Apply the PUA, kerning, and final release metadata decisions to source and package-preview files.
3. Complete drawing/source blockers, especially GF Latin Core and GF Arabic Core coverage.
4. Run `make kerning-proof-check`, run `make kerning-proof-review-check`, and review `documentation/gftools-qa/Proof` after kerning changes or explicit deferral.
5. Create the final `v1.000` release archive with every file listed in downstream `source.files`.
6. Review `documentation/github-release-draft.md`, then publish the final GitHub release asset after the final tag is pushed.
7. Prepare the `Eli Heuer` designer-profile link, biography, and square image, or record a profile-request plan.
8. Align source-repo and `google/fonts` fork Git names, GitHub auth, and API credentials with `documentation/pr-identity-readiness.md` before downstream commits.
9. Run `make preflight` so the build, proof PDF, generated reports, and local gate stay synchronized.
10. Run `make downstream-metadata-check`; when it is ready, apply the checked preview to downstream `ofl/virtuagrotesk/METADATA.pb`.
11. Rerun `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` and review the generated package.
12. Open or update the Google Fonts issue and downstream PR only after the no-PR package is reviewed.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/metadata.html
