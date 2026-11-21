# Agent rules

Virtua Grotesk is an OFL variable font for Latin, Arabic and Hebrew, for
Google Fonts. Eli draws and approves. Agents draft, build, proof and report.
Every agent tool reads this file. Keep it under 70 lines.

## Scope

- Do what Eli asked, and nothing beside it. An idea is one line in the report.
- Change only the glyphs and the masters that Eli names.
- Before you change a shared file, state what the file is for. A view or a fix for one problem does not go into a generic file.
- Check the result of a subagent against the request before you report it.
- A general tool is in [fgtools](https://github.com/fontgarden/fgtools). Change it there, not here.
- Do not add a file, an option or a convention for a fact that an existing one records.
- Commit and push only when Eli asks. Commit messages are plain, with no agent credit.

## Glyphs

- Read `CONTEXT.md` before editing glyphs. Run `.venv/bin/python sources/drawing_harness.py --help` for reference selection, candidate proofs and edge comparison.
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
- For changes that affect the exported font, run `make build` and `make diff`. Explain each difference.
- A second agent reviews a draft before Eli sees it: `pass`, or `fault` with the drawing fault and its location.
- A pass is not approval. Report each visible fault.

## Proofs

- Use the existing proof system for review. Create another specimen, renderer or review page only if Eli asks for one.
- Use `fgtools render` for glyph comparisons and MCP `review_proof` for unsaved edits.
- Include this Proofs section in subagent assignments. Subagents return findings to the coordinating agent.
- After the batch lands, the coordinating agent runs `make proofs` once to rebuild Print, Full and both grid PDFs from the current sources.
- Start `.venv/bin/python sources/proof_review.py` if the index is offline. Verify the index and its four PDF links before handoff.
- Give Eli the review index at http://127.0.0.1:8770/. Link individual files only when requested.
- Keep the Print Proof generic.
- A layout follows the “Proofs and media” section of `CONTEXT.md`.

## Repository

- The repository holds the sources, this file, `CONTEXT.md`, `WORKLOG.md`, `README.md`, `Makefile` and `documentation/`.
- Use Git history for completed work. Keep durable instructions in their owning files.
- Generated output goes to `output/`. Temporary files go to `~/Temp/`. A tracked file has at most 500 KB.
- A file names only a command that can be installed. It never names a path on one machine.
- When a command, a `make` target or a workflow changes, update the guide at https://font.garden/docs in the same session.

## Reports and writing

- Report in a few short lines: what changed, and what needs a decision.
- Write simple technical English: short sentences, one word for one thing, no em dashes.
