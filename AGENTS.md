# Agent guidance

Virtua Grotesk is an OFL variable font in development for Google Fonts.
Use the [onboarding checklist](documentation/google-fonts/README.md) for release
scope and remaining work.
Dated audits are snapshots, not current build or review results.

Codex reads this file directly. Shared workflows live in `.agents/skills/`;
`CLAUDE.md` and `.claude/skills` provide compatibility for Claude Code.
Edit the canonical files, not separate model-specific copies.

## Working style and scope

Use the user's requested outcome and current release scope to choose the work.
Load the relevant skill and referenced evidence as needed; do not load the whole
archive or every skill. Use current files and command results over dated prose.

Complete authorized, reversible work without repeated permission questions.
When a missing design, licensing, or release decision blocks one step, ask a
focused question and continue independent work. Reuse decisions and approvals
already given in the task. Review-only requests remain review-only; onboarding
preparation does not authorize public messages or publication.

Keep updates concise: outcome, evidence, remaining blockers. Do not create new
checklists or reports that duplicate maintained ones. Preserve unresolved human
choices through handoffs; distinguish proposed, verified, approved, and published.
Use plain commit messages without agent self-credit or generated-by trailers.

For onboarding/readiness use `$google-fonts-onboarding`; for binary or package
checks use `$google-fonts-qa`; for a downstream preview use
`$google-fonts-packaging`. Source-only checks belong to `$font-qa`.

## Sources and design

The active sources are `sources/VirtuaGrotesk.designspace` and the Regular
and Bold UFOs beside it. The weight axis runs from 400 to 700. `sources/archive/`
is historical material, not build input. Builds use `sources/config.yaml`.

Read `DESIGN.md` before drawing. The font uses 16-unit chamfers, monolinear
strokes, and smooth cubic curves. Weight gain generally reduces counters;
follow the glyph-specific contract rather than assuming every outer contour
is fixed.

| Metric | Units |
| --- | --- |
| Units per em | 1024 |
| Ascender | 832 |
| Cap height | 768 |
| x-height | 576 |
| Descender | -256 |
| Grid | 2; prefer even coordinates |

Before touching A–Z or a–z, read `documentation/design-pass-worklog.md`.
Append measurements and design decisions there. OPEN decisions belong to Eli;
measure and propose without resolving them by editing sources.

## Source safety

- Green glyphs are human-approved: do not edit them. Purple means do not touch.
- Blue means AI output awaiting human grading. Yellow/orange needs polish;
  red needs repair. Uncolored glyphs are outside automatic completion work.
  Classify unfamiliar colors before acting; never auto-grade AI output green.
- Both masters must have matching contours, point counts, and point types.
  Mirror structural changes and verify master compatibility.
- Preserve unrelated work. Check the working tree and other worktrees before
  starting a source batch.
- Do not save whole UFOs with `defcon`/`ufoLib` `font.save()`: it reformats the
  sources. Edit GLIF XML and plists surgically in their existing style (tabs,
  double-quoted attributes, no space before `/>`, point attribute order
  `x`, `y`, `type`, `smooth`).
- Register new glyphs in each master's `glyphs/contents.plist`,
  `public.glyphOrder` in `lib.plist`, and the GLIF file itself.

## Drawing from images

Use `.agents/skills/anchor-sheet-glyphs/SKILL.md` and
`harness/RUNBOOK-anchor-sheets.md` for reference sheets. Read the skill's
`LESSONS.md` before generating; record Eli's corrections there. Calibrate
pixel-to-font coordinates against a known green anchor. Use `symbol_gen.py`
for line-grammar symbols and img2bez for organic outlines.

For a single organic glyph, follow `harness/RUNBOOK-codex.md`: trace on a
scratch copy, review against `DESIGN.md`, port in the repository's style,
mark blue, and verify. Use `img2bez masters --help` for current flags.
Do not replace tracing with a hand-drawn approximation.

Inspect the trace report before installation: `compatible` must be true;
`lowConfidence` requires review or regeneration. Check bounds, advance,
point counts, and profile. Tune and retrace poor results. Trace logging uses
`IMG2BEZ_LOG` (normally `~/.img2bez/virtua-grotesk-traces.jsonl`).

The broader harness design is in `plans/ai-font-completion-harness.md`.
Runebender is the human visual review and final editing surface.

## Commands

Run from the repository root. Use `.venv/bin/python` for Python tools.

| Command | Purpose |
| --- | --- |
| `make setup` | Create the Python environment and install requirements. |
| `make build` | Build the variable and four static TTFs into `fonts/`. |
| `make proof` | Build and render the main PDF with designbot. |
| `make review` | Build a diffenator2 browser proof. |
| `make reports` | Refresh source, built-font, and compatibility reports. |
| `make preflight` | Build, proof, reports, and required-file checks. |
| `make test` | Build and run the configured Fontspector checks. |
| `make runebender` | Open the designspace with the native GPUI launcher. |
| `make runebender-web` | Open the web editor in an app window. |
| `make runebender-tab` | Open the web editor in a browser tab. |

`make specimen` is an unimplemented marketing-specimen target; do not use it
as a completed proof workflow. `make help` lists additional development tools.
When explicitly asked to open a font in the web editor, use
`runebender-serve <path> --open` and leave the server running for the session.
Do not use the old `~/.cargo/bin/runebender` binary.

## Verification and release

Follow `documentation/qa.md`. After drawing, spacing, kerning,
or feature changes, build and inspect the compiled fonts, render the affected
forms, review proofs, and run preflight. After curve edits, also run
`scripts/curve_lint.py <Master> <glyphs>` and inspect a large single-glyph render.
Verify shaping with the built font, not just the feature source.

The main proof is `designbot proof <font> --output <pdf>`; `make proof` uses
the variable font. For harness renders, use `harness/designbot/glyph_canvas.rs`.
Read `documentation/proofs/PROOF_SPEC.md` for the proof layout. Inspect actual
rendered output before claiming visual review.

Preflight only checks artifact presence. `make skeleton` tolerates QA failures;
neither establishes release readiness. Do not add Fontspector exclusions to
force a passing result. Review each existing exclusion and remove it when the
check passes. Human grading remains separate from automated QA.

Use `.agents/google-fonts-onboarding-checklists.md` and the onboarding, QA,
and packaging skills for submission work. Keep release results tied to the
source revision and built artifacts that were actually checked.
