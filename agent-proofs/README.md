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

Open the printed URL, normally <http://127.0.0.1:60271/>. The launcher verifies
the frozen fonts and reuses a matching server. Leave a newly started server
running. This opens the recorded comparison, not a live rebuild of the UFOs.
The files survive closing the browser or chat; the server may need restarting.
Custom text and UI settings are not yet persisted: record important passages,
settings and feedback in the case before refreshing or ending a session.

## Current handoff — 2026-10-19

Eli said the interface is better and ready to move on after the custom-text
editor pass. The intensive UI pass is complete enough to resume font review;
this is not final approval of every UI detail or blanket approval of new drawings.

- Current case: [HEB-002 — He, Het and Tav](cases/hebrew-002/README.md).
  Candidate v2 was applied to both masters; see its application receipt.
- Prior case: [HEB-001 — Dalet and Resh](cases/hebrew-001/README.md).
- Hebrew/Arabic weight relative to Latin remains provisional. Read the case's
  open questions and DESIGN.md before choosing the next bounded task.
- Latest UI evidence: HEB-002 `layout-v3/ui-pass-22-custom-editor.png` and
  `ui-pass-22-verification.json`. Later case updates supersede this handoff.
- Next: inspect the current source state and dependent marked forms, then
  propose the next small review scope. Do not rerun an old application script
  merely because a new session started.

## Where everything lives

All paths below are relative to `/Users/eli/GH/repos/virtua-grotesk/` on Eli's
current machine. Relative links keep the guide usable in another checkout.

| Responsibility | Canonical location |
| --- | --- |
| Session entry, source permissions, agent behavior | [AGENTS.md](../AGENTS.md) |
| Drawing rules and unresolved design contracts | [DESIGN.md](../DESIGN.md) |
| Confirmed user preferences and case index | [Design review and feedback](FEEDBACK.md) |
| Current decisions, application receipt, evidence | [HEB-002](cases/hebrew-002/README.md) |
| Latin measurements and OPEN human decisions | [Design worklog](../documentation/design-pass-worklog.md) |
| UI implementation, spacing contract, recovery instructions | [Web-proof guide](app/README.md) |
| Editable web UI | `agent-proofs/app/index.html`, `review.css`, `review.js` |
| Running-text presets | `agent-proofs/app/reading-samples.json` |
| Preparation and hash-checked asset copying | `agent-proofs/app/prepare.py` |
| Local server and current case target | [agent-proofs/serve.py](serve.py), root `Makefile` target `proof-web` |
| Generated page, exact served fonts, screenshots | `agent-proofs/cases/hebrew-002/layout-v3/` |
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
3. Preserve a real baseline. Prepare authorized candidates in scratch sources,
   build them and verify the exact font identities used for the comparison.
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
a new case. Update study definitions and real font roles deliberately: current
preparation labels the second font **Applied**, so a scratch candidate needs an
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
