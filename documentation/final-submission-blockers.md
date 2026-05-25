# Final Submission Blockers

This generated report summarizes the current blockers that remain before a
final Google Fonts submission. It intentionally includes drawing/source
work, maintainer decisions, packaging availability, and QA gates so the
final handoff cannot hide behind one green local check.

## Summary

| Area | Current state | Final-submission requirement |
| --- | --- | --- |
| Maintainer decisions | 2 open, 13 decided | 0 open decisions |
| Decision readiness | open: 2; decided: 13; questions: 8; guided: 8/8; mapped: 2/2; surfaces: 8; local paths: 5/5 | Decision log, question prompts, and apply-to surfaces stay aligned |
| Placeholder strings | public blockers: 0 URLs, 0 pending markers; generated echoes: 2; internal/total URL echoes: 1 | 0 public placeholder strings |
| Packager source files | 0 missing locally, 1 ignored/generated, tracked: 3/4, untracked: 1 | Public branch, release, or source build exposes every source file |
| Selected release/archive package plan | action plan: yes; untracked: `fonts/variable/VirtuaGrotesk[wght].ttf`; gitignore-blocked: `fonts/variable/VirtuaGrotesk[wght].ttf` | Final GitHub release/archive contains every listed source file |
| Build-from-source path | gftools builder: yes; metadata fix: yes; outputs fonts: yes; tracked inputs: 6/6 | Public build path is reproducible if build-from-source packaging is chosen |
| Static package shape | generated for QA: 4 / 4; source.files: 0; static destinations: 0; omission documented: yes | Static TTFs are included only if Google Fonts review asks for them |
| Downstream metadata preview | variable names match: yes; pending/placeholder lines: 2 | Generated METADATA.pb has final designer, URL, commit, branch, subsets, and source files |
| Article package assets | words: 413; target: yes; script: `Arab`; localized Arabic: yes; placeholder URL: no; forbidden tags: 0; images exist: yes; image size: yes; provenance: 1/1 | Final Article URL, HTML, images, localized text, and provenance are accepted |
| Family name and namecheck | ASCII: yes; app-menu present: yes; author-name in menu: no; RFN: none declared after copyright line; namecheck pending: no; decision: decided | Namecheck, trademarks, RFN status, app-menu name, and CLA are confirmed |
| Authorship and AI disclosure | Add Font checkbox: yes; AI disclosure recorded: yes | Copyright authorship and AI-use wording confirmed in issue text |
| PR identity and auth | source identity: yes; google/fonts identity: yes; downstream name matches CLA: yes; final commit identity: yes; gh auth: invalid token; API auth: no; source: unavailable; CLA: confirmed by maintainer for the copyright holder | Git identity, GitHub auth, API credentials, and CLA identity are ready before downstream PR |
| Downstream PR readiness | issue pending: yes; path: `ofl/virtuagrotesk`; starter metadata: yes; metadata apply-ready: no; apply blockers: 3; dirty outside path: 0; family files: 1; starter-only family dir: yes; handoff shape: yes | Issue exists first, checked metadata is applied, PR is scoped to one family directory, and title/body/provenance are ready |
| DrawBot proof runtime | Eli Heuer fork origin: yes; importable: yes; checkout clean: yes | Final proofs are regenerated with the intended local drawbot-skia fork |
| Local workflow readiness | preflight: yes; proof: yes; package reaches Packager: no; auth: no | Local handoff commands are runnable before final package work |
| Release metadata | version 1.000, tag v1.000, built/source match: yes | Confirmed version strategy and upstream tag/commit recorded |
| Release/source strategy | tag exists: no; clean tree: no; placeholder URL: no; ignored source files: 1; untracked source files: 1 | Final public source commit, tag, branch, and Packager mode are recorded |
| Release archive manifest | inputs: 4/4; unsafe sources: 0; duplicates: 0; local zip: yes; expected files: yes; unsafe entries: no; hashes: no; URL filename: yes; final URL: pending | Final GitHub release archive matches local reviewed files, filename, path safety, and hashes |
| GitHub release draft | tag: v1.000; title: Virtua Grotesk 1.000; command: yes; archive: `dist/VirtuaGrotesk-1.000.zip`; notes: `documentation/github-release-notes.md`; notes final: no; expected files: yes; hashes: no; source commit: Pending final release/source commit | Final release command and downstream `source.archive_url` contract are reviewed before publishing |
| Package dry-run readiness | reaches Packager: no; first blocker: existing downstream METADATA.pb is still the Packager starter template; blockers: existing downstream METADATA.pb is still the Packager starter template; GitHub API credentials unavailable; auth: no; inputs: yes | No-PR Packager dry run reaches Packager before opening or updating a downstream PR |
| Upstream structure | mandatory paths: 11/11; active source inputs: 4/4; generated fonts ignored: yes | Public upstream repo follows GF structure and final font artifact strategy is explicit |
| Local google/fonts fork | origin: eliheuer/fonts; upstream: google/fonts; topology: yes; exists: yes; branch: main; upstream/main: 0/0; clean: no; dirty outside package: 0 | Clean fork checkout is synced before packaging or template refresh |
| Template and recent PR evidence | project template checked: yes; recent examples: 4; recent Packager merges: 8; Arabic example: yes | Final package follows current GF template expectations and recent new-font patterns |
| Language metadata | script record: yes; script id: `Arab`; preview subsets: yes; primary_script: yes; languages absent: yes; sample_text absent: yes | Downstream metadata language fields stay aligned with Arabic first-submission scope |
| Project template automation | optional automation: 0 / 6; local targets: 6 / 6; Fontspector QA: yes; FontBakery refs: no; decision: decided | Public CI/template automation is added only if maintainer chooses that workflow |
| Submission handoff | template labels: `I New Font, II Submission`; handoff labels: yes; issue draft: yes; Fontspector: yes; maintenance: yes; unchecked: yes; report refs: 40; source modes: yes | Add Font issue draft and package handoff are current before opening issue or PR |
| Designer profile | author candidates: 1; contributor-only: 0; missing profiles: 1; metadata placeholders: 0; draft inputs: 3; path collision: no | Final METADATA.pb designer string has matching catalog profile or prepared request |
| Vendor ID | sources: `FTGD`; fonts: `FTGD`; aligned: yes; warnings: 0; decision: decided | Registered four-character vendor ID is applied consistently, or deferral is explicitly accepted |
| Kerning | every master has source kerning: yes; static GPOS kern: yes; warnings: 0; gftools proof importable: yes; proof output: yes; proof instances: yes; review files: 16 / 16; review: pending human visual review | Kerning completed or explicitly deferred, and `gftools qa --proof` spacing/kerning proof reviewed |
| GF Latin Core coverage | 0 missing codepoints | 0 missing codepoints or reviewer-approved scope change |
| GF Arabic Core coverage | 0 missing codepoints | 0 missing codepoints or reviewer-approved scope change |
| Arabic source worklist | missing codepoints: 0; suggested glyph names: 0; positional forms: 0; missing in both masters: 0; reuse prerequisites checked: 0; missing prerequisites: 0; dotted circle missing: no | Missing Arabic glyphs are drawn from verified source bases in both masters |
| Arabic manual edit targets | source target references: 180; missing source target files: 0 | Any `fix-needed` Arabic visual-review row can be traced to Regular and Bold GLIF files before editing |
| Arabic shaping smoke test | fonts: 5; GSUB arab/dflt: 5/5; GPOS arab/dflt: 5/5; no .notdef: yes; lam-alef rows: 10 | Arabic GSUB shaping remains intact, and missing GPOS/mark support is tracked separately |
| Arabic marks | 0 missing marks; dotted circle: yes; anchors: yes; mark/mkmk: yes | Required marks, dotted circle, anchors, and mark/mkmk ready or explicitly accepted |
| Numeric feature readiness | digits: yes; proportional defaults: yes; `tnum`: yes; coverage: yes; tabular widths: yes; ready: yes | Default ASCII digits are proportional and complemented by full tabular `tnum` alternates |
| PUA/private-use scope | 23 codepoints; Regular matches variable: yes; Bold matches variable: yes | Private-use glyphs are kept with rationale, made reachable, or deferred before final packaging |
| Glyph reachability | 0 unique unreachable; Arabic helpers: 0; mark helpers: 0; source cleanup: 0 | Arabic helper glyphs are reachable, encoded, decomposed, or deliberately removed before final packaging |
| Fontspector warning triage | 10 WARN results; decision-linked warnings: 5 | Every warning is reviewed, resolved, or explicitly accepted before final submission |
| Fontspector metadata preview probe | preview WARNs: 3; unreachable codepoints: 9; removing U+200F: 4 WARN; removing U+25CC: 6 WARN | Final metadata warning decisions are based on package-visible METADATA.pb, not loose-font noise |
| Fontspector zero-warning path | honest zero possible: no; package floor: 3 WARN; menu+latin probe: 2 WARN but drops Arabic; menu+latin+arabic probe: 3 WARN; contour findings: 0; Arabic subset threshold needs: 594; latin-ext threshold needs: 120; Latin Core missing: 0; blockers: meet or revise the broad Google Fonts subset threshold for the intended subsets; resolve or get reviewer acceptance for required support codepoints that are not covered by serving subsets. | Reduce warnings through real coverage, drawing cleanup, and reviewed subset scope, not by hiding intended Arabic support |
| Fontspector googlefonts profile | 0 FAIL results | 0 FAIL results or explicit reviewer acceptance |
| Contour/no-contour cleanup | 0 source glyph findings, 0 all-font rows; decisions pending: 0, fix-now: 0, fixed: 0, accepted: 0, deferred: 0 | 0 unresolved source-outline findings or explicit reviewer acceptance |

## Open Maintainer Decisions

- Private-use icon block
- Kerning

## Evidence Reports

- `documentation/google-fonts-decisions.md`
- `documentation/google-fonts-decision-answer-sheet.md`
- `documentation/decision-readiness.md`
- `documentation/decision-application-blockers.md`
- `documentation/open-placeholder-audit.md`
- `documentation/public-upstream-readiness.md`
- `documentation/package-source-files-audit.md`
- `documentation/packager-source-strategy.md`
- `documentation/package-dry-run-readiness.md`
- `documentation/downstream-metadata-readiness.md`
- `documentation/downstream-metadata-diff.md`
- `documentation/article-readiness.md`
- `documentation/kerning-readiness.md`
- `documentation/kerning-proof-review.md`
- `documentation/family-name-readiness.md`
- `documentation/authorship-disclosure-readiness.md`
- `documentation/pr-identity-readiness.md`
- `documentation/downstream-pr-readiness.md`
- `documentation/drawbot-runtime-readiness.md`
- `documentation/local-workflow-readiness.md`
- `documentation/vendor-id-readiness.md`
- `documentation/avar-readiness.md`
- `documentation/release-metadata.md`
- `documentation/release-source-readiness.md`
- `documentation/release-archive-manifest.md`
- `documentation/github-release-draft.md`
- `documentation/github-release-notes.md`
- `documentation/upstream-structure-readiness.md`
- `documentation/google-fonts-template-and-pr-audit.md`
- `documentation/recent-google-fonts-packages.md`
- `documentation/google-fonts-add-font-template-audit.md`
- `documentation/google-fonts-add-font-issue-draft.md`
- `documentation/project-template-automation-readiness.md`
- `documentation/submission-handoff-readiness.md`
- `documentation/designer-profile-readiness.md`
- `documentation/designer-profile-package-draft.md`
- `documentation/gf-glyphset-readiness.md`
- `documentation/google-fonts-language-metadata.md`
- `documentation/missing-gf-latin-core.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/arabic-source-work-checklist.md`
- `documentation/arabic-current-review-worksheet.md`
- `documentation/arabic-batch-recorder.md`
- `documentation/arabic-first-review-batch.md`
- `documentation/arabic-full-queue-ai-sweep.md`
- `documentation/arabic-manual-edit-targets.md`
- `documentation/arabic-shaping-smoke-test.md`
- `documentation/arabic-mark-readiness.md`
- `documentation/arabic-review-packet.md`
- `documentation/arabic-goal-completion-audit.md`
- `documentation/arabic-next-review-packet.md`
- `documentation/arabic-visual-review-log.md`
- `documentation/numeric-feature-readiness.md`
- `documentation/pua-scope.md`
- `documentation/glyph-reachability.md`
- `documentation/fontspector-warnings.md`
- `documentation/fontspector-metadata-warning-probe.md`
- `documentation/fontspector-zero-warning-worklist.md`
- `documentation/fontspector-googlefonts-report.md`
- `documentation/fontspector-contour-count.md`
- `documentation/arabic-cleanup-drawing-briefs.md`
- `documentation/contour-cleanup-batches.md`
- `documentation/contour-cleanup-ai-triage.md`
- `documentation/contour-cleanup-decision-log.md`

Regenerate this report with `make preflight` after drawing work,
metadata decisions, or packaging-source decisions change.
