# Virtua Design Review

The entry point for the human-and-agent font-development loop. The **live web
proof** is its comparison interface; **Virtua Design Review** names the whole
workflow: inspect → propose → proof → feedback → revise → apply → verify.
Keep this guide as a map, not a duplicate of the design rules or feedback log.

Everything belonging to this review system has one root-level home:

```text
agent-proofs/
├── README.md          Start here: workflow and current handoff
├── FEEDBACK.md        Confirmed preferences and review index
├── app/               Browser UI, text presets and preparation tool
├── serve.py           Local server
└── cases/             Glyph reviews, decisions, fonts and proof evidence
    ├── hebrew-001/
    └── hebrew-002/
```

Moved here on 2026-10-19 from `documentation/design-review/`,
`documentation/proofs/browser_review/` and `scripts/serve_proof.py`.
Recorded JSON receipts retain their original paths and hashes as historical
evidence. For locating their moved files, map the old review's `hebrew-001/`
and `hebrew-002/` folders to `agent-proofs/cases/`, and the old browser-review
folder to `agent-proofs/app/`. Current commands and maintained links use the
new locations. This relocation changes no font drawings or proof layout.

## Resume in a new session

Open the Virtua repository and say:

> Resume Virtua Design Review. Read AGENTS.md and
> agent-proofs/README.md, then the current case and confirmed
> preferences. Check the working tree, open the existing live web proof, and
> summarize the last applied changes and unresolved decisions before proposing
> the next small glyph group. Preserve the current proof layout and font snapshots.

The same prompt works as a starting instruction for any agent with repository,
shell, and browser access. Agents that do not automatically read AGENTS.md must
read it explicitly. Claude's CLAUDE.md imports it and `.claude/skills` points to
the shared `.agents/skills`. No Codex chat history or private memory is required.

From the repository root:

```sh
make proof-web
```

Open the printed URL, currently <http://127.0.0.1:60272/>. The launcher verifies
the frozen fonts and reuses a matching server. Leave a newly started server
running. This opens the recorded comparison, not a live rebuild of the UFOs.
The files survive closing the browser or chat; the server may need restarting.
Custom text and UI settings are not yet persisted: record important passages,
settings and feedback in the case before refreshing or ending a session.

## Standing drawing authorization — 2026-10-20

Eli authorized continuing Hebrew development directly in the active Regular and
Bold UFOs, then Arabic after Hebrew. Do not ask for per-batch application approval.
Preserve a before snapshot, check source colors and current file hashes, make
bounded compatible edits, rebuild and show the comparison with Rubik. Active
sources are the working drawings visible in Runebender; application does not
mean final visual approval, green grading, or release readiness. Preserve manual
corrections and unrelated edits. Keep recording exact correction pairs and
promote measured lessons into DESIGN.md and the shared skills.

## Autonomous Arabic first pass — 2026-10-21

Eli asked for a first pass on the full Arabic while he repairs Runebender's
component editing. This supersedes the earlier short-loop / no-unattended-run
restriction. Continue bounded batches in the active Regular and Bold sources,
with backups, hashes, source-color checks, builds, curve checks and four-reference
proofs. Do not wait for visual feedback between batches. Human grading and final
release approval remain separate; no green grades are assigned by the agent.

Preserve all green sources and their inherited drawings, and the saved manual
hamza and Hebrew corrections. Finish base families and joining forms before
revisiting dependent dots, diacritics, attachment and spacing. Record uncertain
script/design choices for later review rather than inventing human approval.
Check current file hashes before every application so editor saves are not lost.

Progress and the remaining queue live in
[cases/arabic-006/README.md](cases/arabic-006/README.md).

## Current handoff — 2026-10-21

Eli renewed autonomous continuation after the Feh/Qaf repair. Batch 06 has
400/550/700 raster inspection, curve/shaping checks and preflight; it remains a
working draft for later human review. Continue bounded independent families.

Current case: [ARB-006](cases/arabic-006/README.md).
Current proof: `cases/arabic-006/batches/06-medial-loop/working/`, with all four
references. Next: Bold Lam, then Meem. Eli is editing Beh (`ببب ب`): reserve
those forms in both masters and every recursive component donor, including dots.
Check live hashes before each write and preserve human saves.

### Earlier Beh checkpoint
Checkpoint `211c3b8d` is pushed and preserves the accepted Fathatan repair and
base-forms-first direction; `d23f1bed` preserves the manual Bold hamza correction
and curve-tool lessons. Eli has now authorized an autonomous Arabic first pass;
see the authorization below.

ARB-005 revises the four red Bold `behDotless-ar` bases (isolated, initial,
medial and final). Approved green Regular sources remain byte-identical and
are shown at 400. The four bases feed 41 Bold dependent glyphs; their inherited
changes are recorded and none is green. Dots, marks, anchors, wrappers and
features are unchanged. New Bold root drawings are purple, pending human review.

Earlier proof: `cases/arabic-005/round-dots/working/`, **Before / Working**, with Rubik,
Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro. Default sample **ببب ب**
shows all four forms through real shaping. Inspect 400 and 700, plus intermediate
weights; saved screenshots cover both endpoints and related-base context.
Build/preflight and 112 shaping comparisons passed. Exact Regular sources are
unchanged; shared cubic-to-quadratic conversion changes their compiled
approximation by less than 0.7 units in the sampled base comparisons. The full
grid report retains existing anchor/green-geometry exceptions rather than
silently normalizing them. This is an applied working trial awaiting feedback.

Eli judged the base trial better, then requested near-circular Arabic letter
dots on the grid. The [round-dot correction](cases/arabic-005/round-dots/README.md)
updates only the two Bold single-dot donors; green Regular and the base trial
are preserved. That proof’s Before is the previous Beh trial; Working adds the dot
correction. Build/preflight and 147 shaping comparisons passed for this later
revision. Multi-dot drawings and existing placement issues are deferred.

**Arabic base forms first, in both masters.** Work through isolated, initial,
medial and final forms where applicable, with joined-plus-isolated samples like
`ببب ب`, word contexts and all four references. Use bounded technical batches
without waiting for feedback between them. Defer
further diacritic drawing, stacking and attachment tuning until base drawings
are stable. Hamza/Dammatan composition, Fatha root drawing and inherited dot
issues remain follow-ups, not the next targets. Preserve manual corrections.

ARB-003's exact correction and signed comb evidence remain in
`cases/arabic-003/manual-correction-01/`. The reusable
[curve-quality workflow](../.agents/skills/draw-outline/references/curve-quality.md)
records the unwanted AI S-bend, improved inner continuity and deliberately
preserved human shoulder; do not equate machine precision with equal handles.

Previous Hebrew evidence remains at `cases/hebrew-010/applied-v3/`; manual
correction lessons and exact snapshots remain in their original case folders.

HEB-001 through HEB-005 are approved and applied: Dalet/Resh, He/Het/Tav,
Bet/Kaf/Final Kaf, Pe/Final Pe, and Mem/Final Mem/Samekh (13 of 27 base letters/final forms in this
review sequence). Applications and exact hashes live in their cases; no glyph
was auto-graded. Historical comparisons, GLIFs, licenses and binaries remain.
Standalone marks and cross-script weight remain follow-up. No public
release or Google Fonts readiness claim has been made.

Eli's continuing objective is Hebrew parity with Rubik. The frozen-reference
coverage audit in HEB-005 finds all 76 of Rubik's encoded Hebrew/presentation
codepoints already present with nonempty outlines. This only establishes cmap
coverage. Compare drawing quality and mark behavior in the existing 400–700
Virtua range; Rubik's additional 300–900 range is not a silent scope expansion.

Remaining review sequence (adapt grouping to feedback):

| Group | State / focus |
| --- | --- |
| מ ם ס — Mem, Final Mem, Samekh | HEB-005 v5 approved and applied; v4 redesign rejected |
| י ו ז נ ן — Yod, Vav, Zayin, Nun, Final Nun | HEB-006 accepted for continuation, including both manual Zayin corrections |
| ג ל ק — Gimel, Lamed, Qof | HEB-007: Gimel v4 accepted for continuation; Lamed/Qof v2 active |
| ט ע — Tet, Ayin | HEB-008 active working drawings; visual review pending |
| א צ ץ ש — Alef, Tsadi, Final Tsadi, Shin | HEB-008 active working drawings; visual review pending |

The 29 marked forms have been reconciled in HEB-009. Next review niqqud
and combined marks/mark-to-mark positioning,
Hebrew punctuation and mixed-direction text, then full spacing/kerning and
Latin–Hebrew weight texture. Native-reader review and fresh release QA remain
required before calling Hebrew shippable. Use the maintained Google Fonts
checklist for submission checks rather than creating another release checklist.

### Hebrew resumed — 2026-10-19

Eli requested reopening the proof and choosing the next group, with Hebrew
completion for Google Fonts as the goal and Rubik as a reference. Read-only
inspection confirmed the current sources match the UI-start source snapshot,
all six HEB-002 application hashes match, and the current variable binary equals
the proof's Applied font. No new drawings were made in this resumption.

Recommended next base group: **ב כ ך — bet, kaf, final kaf**. All three still
have identical Regular/Bold outline XML and widths; this is also true of 19 of
the 27 Hebrew letters/finals overall. Their related right-hand curves and the
bet/kaf distinction make a bounded next comparison. This is a proposal, not an
applied or approved candidate. Keep the earlier dalet/resh/he/het/tav dotted
presentation forms on the follow-up list: they are standalone outlines and do
not inherit the applied base changes; respect their existing color permissions.

Rubik's local source checkout is `/Users/eli/GH/repos/rubik/`, origin
`https://github.com/googlefonts/rubik`, inspected revision
`e337a5f69a9bea30e58d05bd40184d79cc099628`. Its original upright source is
`sources/Rubik.glyphs`. A local, untracked conversion already exists at
`sources/designspace/Rubik.designspace`, with Light/Black UFOs in its `masters/`
directory and a sparse intermediate layer. Both endpoint UFOs opened successfully;
bet, kaf and final kaf contain outlines and positioning anchors. No conversion
or modification was needed. Treat these as local derived references, not a newly
verified build of the exact Rubik binary used in the proof. Preserve the proof's
existing reference hash. Consult Rubik for structure, spacing and attachment;
Virtua's live green Latin geometry remains the style authority.

## Where everything lives

All paths below are relative to `/Users/eli/GH/repos/virtua-grotesk/` on Eli's
current machine. Relative links keep the guide usable in another checkout.

| Responsibility | Canonical location |
| --- | --- |
| Session entry, source permissions, agent behavior | [AGENTS.md](../AGENTS.md) |
| Drawing rules and unresolved design contracts | [DESIGN.md](../DESIGN.md) |
| Confirmed user preferences and case index | [Design review and feedback](FEEDBACK.md) |
| Current accepted review and next priority | [ARB-006](cases/arabic-006/README.md); autonomous Arabic queue; manual Arabic correction in [ARB-003](cases/arabic-003/README.md) |
| Latin measurements and OPEN human decisions | [Design worklog](../documentation/design-pass-worklog.md) |
| UI implementation, spacing contract, recovery instructions | [Web-proof guide](app/README.md) |
| Editable web UI | `agent-proofs/app/index.html`, `review.css`, `review.js` |
| Running-text presets | `agent-proofs/app/reading-samples.json` |
| Preparation and hash-checked asset copying | `agent-proofs/app/prepare.py` |
| Local server and current case target | [agent-proofs/serve.py](serve.py), root `Makefile` target `proof-web` |
| Current generated page, fonts, screenshots | `agent-proofs/cases/arabic-006/batches/06-medial-loop/working/`; raster and browser evidence in its parent batch folder |
| Current editable font | `sources/VirtuaGrotesk.designspace`, `sources/VirtuaGrotesk-Regular.ufo/`, `sources/VirtuaGrotesk-Bold.ufo/` |
| Build, compiled shaping, proof and QA procedures | [Build and QA](../documentation/qa.md) |
| Shared agent procedures | [.agents/skills/](../.agents/skills), starting with [render-specimen](../.agents/skills/render-specimen/SKILL.md) |
| Raw scratch sources, builds and historical baseline assets | `out/qa/` (ignored; paths/hashes in each case's evidence) |
| Release scope, distinct from design acceptance | [Google Fonts onboarding](../documentation/google-fonts/README.md) |

Edit the canonical web UI, not the generated copy in `layout-v3`. Follow the
web-proof guide to prepare and inspect changes. `image-viewer.html` and older
PNG sheets are historical; `make review` is a separate Diffenator3 QA report.

## Working loop across agents

1. Read this map, AGENTS.md, confirmed preferences, and the latest case. Inspect
   dirty files and other worktrees; do not overwrite another session's work.
2. Read the relevant design rules and drawing skill. Inspect source colors,
   dependencies and actual compiled-font freshness. Choose a named small scope.
3. Preserve a real baseline. Under the standing authorization above, write bounded
   drawing updates to the active sources without another application question.
   Build and verify the exact font identities used for the comparison.
4. Review equal-scale before/candidate/reference samples and running text in
   the browser. Screenshots support the review; actual fonts render the samples.
   A text-only agent should ask Eli to inspect the browser, not claim it saw it.
5. Record Eli's feedback, scope and approval state in the case before continuing.
   Follow existing application authorization; preserve reversible before states.
   Apply only the authorized source changes and run the required font checks.
6. End with the actual state, evidence paths, unresolved choices and next bounded
   question. Promote confirmed lessons to their existing owner, linked to the
   case. Never convert model opinion or a passing test into a human color grade.

The detailed loop and feedback schema live in [the review record](FEEDBACK.md#the-loop).
Update this guide's current-case pointer and the server target when advancing to
a new case. Update study definitions and real font roles deliberately: study manifests can set each font role label; a scratch candidate must use an
accurate Candidate label. Do not rewrite old case evidence to imply a new state.

## Preservation and recovery

The proof system and HEB-002's exact served font snapshots are retained in Git,
including the font licenses. A fresh checkout can open the committed comparison
with `python3 agent-proofs/serve.py` (standard library only), or `make proof-web`
after creating the project's Python environment. These historical Before/Applied
binaries are review assets, not a claim that the checkout's UFOs match Applied.

To refresh the UI from its canonical code without depending on this machine's
build paths (requires the project's Python environment with fontTools):

```sh
.venv/bin/python agent-proofs/app/prepare.py \
  --evidence agent-proofs/cases/hebrew-002/layout-v3/snapshot.json \
  --output-dir agent-proofs/cases/hebrew-002/layout-v3
```

A local recovery archive for this handoff is stored in
`out/backups/virtua-design-review/` with a SHA-256 companion file. It includes
the web proof, review records, frozen served fonts and linked project guidance.
It is a local safety copy, not a remote backup or a complete repository backup.
Extract into a separate directory first, inspect, then restore selected files.
The served folder can run directly using
`.venv/bin/python agent-proofs/serve.py --directory <folder>`.
The portable `snapshot.json` resolves font paths relative to itself. Original
receipts retain their historical absolute paths and hashes. Never rebuild today's
sources as an old Before. Older cases' raw scratch builds under `out/qa/` remain
local; their retained evidence is not a promise that every historic recipe is
self-contained.

Keep future case assets explicit: retain the exact reviewed binaries and licenses
alongside their manifest, or record a verified recovery location. Do not sweep
unrelated dirty sources into a proof-system commit. Verify hashes after recovery.

## Scope and future portability

This is a Virtua-specific system today: glyph identities, text presets, design
contracts, current case, reference roles and some preparation logic are specific
to this font and Hebrew study. The UI is static HTML/CSS/JavaScript and the
preparation/server tools use Python. There is no model API or Codex dependency
in the proof renderer. Codex supplies the conversation, file edits and browser
inspection; another capable agent can perform those roles with the same files.

Eli wants Codex to remain the primary use case while this matures. A future
Runebender local-chat workflow could pair the editor with a visible browser
proof beside it. It is not integrated today. A headless browser could automate
captures, but the human comparison panel needs a visible browser. Anthropic,
local models, Hermes or Pi should reuse this documented loop where their tools
permit; compatibility has not been tested. Generic extraction, editor embedding
and automatic agent coordination are future work, not part of this handoff.

## Required visual checkpoint — 2026-10-21

For each Arabic drawing batch, render and inspect fixed DesignBot raster proofs
at 400 and 700 with Before, Working and the four references. Retain the PNGs,
font-hash receipts and observed findings in the case. Add large details or
reading-size context when needed; fix visible faults before continuing.
See [the raster workflow](app/README.md#whole-font-views-and-image-inspection).
This is a core check alongside curve diagnostics and compiled shaping, not
human grading or release approval.
