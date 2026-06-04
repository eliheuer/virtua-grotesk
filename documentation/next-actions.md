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
- GitHub release draft: `v1.000` / `Virtua Grotesk 1.000`; archive files: yes; hashes: no
- Fontspector googlefonts profile: 10 FAIL, 20 WARN, 517 PASS
- UFO editor handoff ready: yes
- Arabic snapshot evidence ready: yes
- Arabic first-batch source checkpoint ready: yes
- Arabic pending source checkpoint ready: yes
- Contour cleanup decisions: 4 source glyph findings, 4 all-font rows; decisions pending: 4, fix-now: 0, fixed: 0, accepted: 0, deferred: 0
- GF visual kerning proof: every master has source kerning: yes; static GPOS kern: yes; warnings: 0; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review

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
| Keep GF Latin Core coverage at zero missing codepoints. | 0 missing codepoints | `documentation/missing-gf-latin-core.md` |
| Keep GF Arabic Core coverage at zero missing codepoints. | 0 missing codepoints | `documentation/missing-gf-arabic-core.md` |
| Plan Arabic source construction batches. | missing codepoints: 0; suggested glyph names: 0; positional forms: 0; missing in both masters: 0; reuse prerequisites checked: 0; missing prerequisites: 0; dotted circle missing: no | `documentation/arabic-source-work-checklist.md` |
| Add Arabic marks, dotted circle, anchors, and mark/mkmk if Arabic remains in scope. | 0 missing marks; dotted circle: yes; anchors: yes; mark/mkmk: yes | `documentation/arabic-review-packet.md` |
| Review the next Arabic visual proof packet and record outcomes. | fonts: 5; GSUB arab/dflt: 5/5; GPOS arab/dflt: 5/5; no .notdef: yes; lam-alef rows: 10; 0 missing marks; dotted circle: yes; anchors: yes; mark/mkmk: yes | `documentation/arabic-drawing-session-checklist.md`; `documentation/arabic-current-review-worksheet.md`; `documentation/arabic-batch-recorder.md`; `documentation/arabic-first-review-batch.md`; `documentation/arabic-full-queue-ai-sweep.md`; `documentation/arabic-hand-review-session.md`; `documentation/arabic-next-review-packet.md`; `documentation/arabic-goal-completion-audit.md`; `documentation/arabic-visual-review-log.md` |
| Open the UFOs for hand cleanup only after editor/package checks stay green. | UFO editor: yes; snapshot evidence: yes; first-batch source checkpoint: yes; pending source checkpoint: yes | `documentation/arabic-drawing-session-checklist.md`; `documentation/ufo-editor-readiness.md`; `documentation/arabic-snapshot-integrity.md`; `documentation/arabic-first-batch-source-checkpoint.md`; `documentation/arabic-pending-source-checkpoint.md`; `documentation/arabic-manual-edit-targets.md` |
| Keep source contour/no-contour cleanup closed after drawing edits. | 4 source glyph findings, 4 all-font rows; decisions pending: 4, fix-now: 0, fixed: 0, accepted: 0, deferred: 0 | `documentation/arabic-manual-review-batches.md`; `documentation/arabic-manual-edit-targets.md`; `documentation/fontspector-contour-count.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/contour-cleanup-batches.md`; `documentation/contour-cleanup-ai-triage.md`; `documentation/contour-cleanup-decision-log.md` |
| Reduce Fontspector warnings without hiding intended serving scope. | honest zero possible: no; package floor: 6 WARN; menu+latin probe: 5 WARN but drops Arabic; menu+latin+arabic probe: 6 WARN; contour findings: 4; Arabic subset threshold needs: 591; latin-ext threshold needs: 120; Latin Core missing: 0; blockers: meet or revise the broad Google Fonts subset threshold for the intended subsets; resolve or get reviewer acceptance for required support codepoints that are not covered by serving subsets; clean up package-context contour-count warnings. | `documentation/fontspector-metadata-warning-probe.md`; `documentation/fontspector-zero-warning-worklist.md`; `documentation/contour-cleanup-edit-plan.md` |
| Review GF visual spacing/kerning proof. | every master has source kerning: yes; static GPOS kern: yes; warnings: 0; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review | `documentation/kerning-readiness.md`; `documentation/kerning-proof-review.md` |
| Resolve or intentionally keep PUA and unreachable helper glyphs. | 0 unique unreachable; Arabic helpers: 0; mark helpers: 0; source cleanup: 0 | `documentation/glyph-reachability.md` |

## Packaging And Handoff

| Action | Current state | Evidence |
| --- | --- | --- |
| Monitor placeholder audit; no public placeholder strings currently block handoff. | public blockers: 0 URLs, 0 pending markers; generated echoes: 2; internal/total URL echoes: 1 | `documentation/open-placeholder-audit.md` |
| Replace the Packager starter `METADATA.pb` with final downstream metadata and restore API auth. | reaches Packager: no; first blocker: existing downstream METADATA.pb is still the Packager starter template; blockers: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable; auth: no; inputs: yes | `documentation/downstream-metadata-diff.md` |
| Align Git/GitHub identity before downstream commits. | source identity: yes; google/fonts identity: yes; downstream name matches CLA: yes; final commit identity: yes; gh auth: invalid token; API auth: no; source: unavailable; CLA: confirmed by maintainer for the copyright holder | `documentation/pr-identity-readiness.md`; `documentation/downstream-pr-readiness.md` |
| Create the final release/archive source package for Packager. | 0 missing locally, 1 ignored/generated, tracked: 3/4, untracked: 1; release/archive source mode: `latest-release`; archive must include currently untracked package files: `fonts/variable/VirtuaGrotesk[wght].ttf`; `source.config_yaml` review: no | `documentation/packager-source-strategy.md` |
| Publish the final GitHub release asset after the final source commit and tag. | tag: v1.000; title: Virtua Grotesk 1.000; command: yes; archive: `dist/VirtuaGrotesk-1.000.zip`; notes: `documentation/github-release-notes.md`; notes final: no; expected files: yes; hashes: no; source commit: Pending final release/source commit | `documentation/github-release-draft.md` |
| Prepare the Google Fonts designer profile request for `Eli Heuer`. | author candidates: 1; contributor-only: 0; missing profiles: 1; metadata placeholders: 0; draft inputs: 3; path collision: no | `documentation/designer-profile-package-draft.md` |
| Clean or review the local `google/fonts` fork before the final package pass. | origin: eliheuer/fonts; upstream: google/fonts; topology: yes; exists: yes; branch: main; upstream/main: 0/0; clean: no; dirty outside package: 0 | `documentation/package-dry-run-readiness.md` |
| Keep Add Font issue and submission handoff synchronized with generated evidence. | template labels: `I New Font, II Submission`; handoff labels: yes; issue draft: yes; Fontspector: no; maintenance: yes; unchecked: yes; report refs: 40; source modes: yes | `documentation/submission-handoff-readiness.md` |

## Run Order

1. Record the remaining maintainer decisions in `documentation/google-fonts-decisions.md`.
2. Apply the PUA, kerning, and final release metadata decisions to source and package-preview files.
3. Complete the remaining drawing/source blockers by reviewing the Arabic visual packet and recording each row as pass, fix-needed, or deferred.
4. During Arabic hand review, start with `documentation/arabic-drawing-session-checklist.md`, then use `documentation/arabic-current-review-worksheet.md` for the current five-row fill-in sheet, `documentation/arabic-first-review-batch.md` for the structure/wrong-glyph packet, `documentation/arabic-first-batch-source-checkpoint.md` for the first-batch Regular/Bold source checkpoint, `documentation/arabic-pending-source-checkpoint.md` for all unresolved review-row source targets, and `documentation/arabic-manual-edit-targets.md` to jump from any `fix-needed` row to the matching Regular and Bold GLIF files.
5. Run `make kerning-proof-check`, run `make kerning-proof-review-check`, and review `documentation/gftools-qa/Proof` after kerning changes or explicit deferral.
6. Create the final `v1.000` release archive with every file listed in downstream `source.files`.
7. Review `documentation/github-release-draft.md`, then publish the final GitHub release asset after the final tag is pushed.
8. Prepare the `Eli Heuer` designer-profile link, biography, and square image, or record a profile-request plan.
9. Align source-repo and `google/fonts` fork Git names, GitHub auth, and API credentials with `documentation/pr-identity-readiness.md` before downstream commits.
10. Run `make preflight` so the build, proof PDF, generated reports, and local gate stay synchronized.
11. Run `make downstream-metadata-check`; when it is ready, apply the checked preview to downstream `ofl/virtuagrotesk/METADATA.pb`.
12. Rerun `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` and review the generated package.
13. Open or update the Google Fonts issue and downstream PR only after the no-PR package is reviewed.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/metadata.html
