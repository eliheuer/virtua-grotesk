# Agent rules

Virtua Grotesk is an OFL variable font for Latin, Arabic and Hebrew, for
Google Fonts. Eli draws and approves. Agents draft, build, proof and report.
Every agent tool reads this file. Keep it under 70 lines.

## Start and stop

- Read all of `CONTEXT.md` (the design) before you change a glyph.
- Read the top five entries of `WORKLOG.md` when you start.
- Add one entry to `WORKLOG.md` when you stop.

## Scope

- Do what Eli asked, and nothing beside it. An idea is one line in the report.
- Change only the glyphs and the masters that Eli names.
- Before you change a shared file, state what the file is for. A view or a fix for one problem does not go into a generic file.
- Check the result of a subagent against the request before you report it.
- A general tool is in [fgtools](https://github.com/fontgarden/fgtools). Change it there, not here.
- Do not add a file, an option or a convention for a fact that an existing one records.
- Commit and push only when Eli asks. Commit messages are plain, with no agent credit.

## Glyphs

- The mark color is the state of a glyph. `CONTEXT.md` has the policy of each color.
- Mark each AI drawing purple. Only Eli marks a contour glyph green. Never change a green contour glyph.
- Every master has the same contours, points and components. `.venv/bin/fgtools lint-glifs` checks it.
- If Runebender has the project open, draw there with `agent_apply`, one step in each call, and do not save.
- If not, edit the GLIF text in its style: tabs, double quotes. Never call `font.save()`.
- For a calculated edit, use `.venv/bin/fgtools edit`. Do not type the coordinates.
- Left sidebearing: move every point and component. Right sidebearing: change the advance only.
- Register a new glyph in `contents.plist` and `public.glyphOrder` of every master.
- Regular and Bold at 14 pt are drawn. After a change of one of them, run `make masters`: it calculates the other masters and keeps hand corrections.

## Checks

- Before and after an edit, run `.venv/bin/fgtools render "<glyphs>"` and read the picture.
- After an edit, run `make check-design GLYPHS="..."` and `make check-changes`.
- Before a report, run `make build` and `make diff`. Each difference must be one that the edit explains.
- A second agent reviews a draft before Eli sees it: `pass`, or `fault` with the rule number and the place.
- A pass is not approval. Report each visible fault.

## Proofs

- Show Eli work only in the proof system. Do not draw a picture with a script of your own.
- One glyph before and after an edit: `fgtools render`. An unsaved edit: the MCP tool `review_proof`. Text and axes: `make proof`.
- `.venv/bin/python sources/proof_review.py` serves the proofs at http://127.0.0.1:8770. Give Eli that address.
- The Print Proof is generic. It gets no page for one problem.
- A proof is valid only for the sources it was built from.
- A layout follows R61 to R67 of `CONTEXT.md`.

## Repository

- The repository holds the sources, this file, `CONTEXT.md`, `WORKLOG.md`, `README.md`, `Makefile`, `documentation/` and `.agents/tasks/`.
- `WORKLOG.md` is the only record of work. Do not add a plan, a report or an audit.
- Generated output goes to `output/`. Temporary files go to `~/Temp/`. A tracked file has at most 500 KB.
- A file names only a command that can be installed. It never names a path on one machine.
- When a command, a `make` target or a workflow changes, update the guide at https://font.garden/docs in the same session.

## Reports and writing

- Report in a few short lines: what changed, and what needs a decision.
- Write simple technical English: short sentences, one word for one thing, no em dashes.

## Worklog entry

Newest first, five lines at most: the date and the agent, what changed, what
is open. When the file passes 150 lines, make the oldest entries one paragraph.
