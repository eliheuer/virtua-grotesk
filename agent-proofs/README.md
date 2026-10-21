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

## Current handoff — 2026-10-21

Current case: [ARB-004 — Fathatan and Hamza with Fathatan](cases/arabic-004/README.md).
Checkpoint `d23f1bed` preserves Eli's Bold hamza correction, exact learning pair,
curve diagnostics/skills, earlier Arabic loops and four-reference proof setup.
Only green is frozen; purple identifies unreviewed AI drawings. Continue short
interactive loops; no autonomous run has begun.

ARB-004 repairs component placement in `fathatan-ar` and `hamzaaboveFathatan-ar`
in both masters. Four GLIFs changed; all donor outlines, including Eli's saved
Bold hamza, remain unchanged. Both ordinary أً and explicit hamza/fathatan
combining sequences now show separated strokes. See the case for the helper-only
trial and why shaping required the encoded Fathatan repair too.

Current proof: `cases/arabic-004/working/`, **Before / Working**, with Rubik,
Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro. Build/preflight and 175
shaping comparisons passed; 13 sampled weights retain separate helper pieces.
Eli accepted this placement repair on 2026-10-21 and requested committing and
shipping it. Acceptance does not assign a new source color or establish release
readiness.

**Next priority: Arabic base forms first, in both masters.** Work through their
isolated, initial, medial and final forms where applicable, with joining-context
proofs and all four references. Keep the interactive loops small. Defer further
diacritic drawing, mark stacking and attachment tuning until the base forms are
in a good, stable state: changing bases would invalidate that placement work.
Hamza/Dammatan composition, the inherited Fatha root drawing and other mark
issues remain recorded follow-ups, not the next targets. Preserve manual edits.

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
| Current accepted review and next priority | [ARB-004](cases/arabic-004/README.md); Arabic base forms next; manual Arabic correction in [ARB-003](cases/arabic-003/README.md) |
| Latin measurements and OPEN human decisions | [Design worklog](../documentation/design-pass-worklog.md) |
| UI implementation, spacing contract, recovery instructions | [Web-proof guide](app/README.md) |
| Editable web UI | `agent-proofs/app/index.html`, `review.css`, `review.js` |
| Running-text presets | `agent-proofs/app/reading-samples.json` |
| Preparation and hash-checked asset copying | `agent-proofs/app/prepare.py` |
| Local server and current case target | [agent-proofs/serve.py](serve.py), root `Makefile` target `proof-web` |
| Current generated page, fonts, screenshots | `agent-proofs/cases/arabic-004/working/`; screenshots in its parent case folder |
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
