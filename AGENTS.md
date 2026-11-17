# Agent guidance

Virtua Grotesk is an OFL variable font (wght 400 to 700) for Latin, Arabic
and Hebrew, intended for Google Fonts. The release target is every glyph
green in both masters. Eli draws and approves. Agents draft named glyphs,
build, proof, measure and report.

## The files

| File | Content |
| --- | --- |
| `AGENTS.md` | How to work. This file. |
| [CONTEXT.md](CONTEXT.md) | The design: the description of the font, the idea and the numbered rules, with the values that the tools check in `toml` blocks. Runebender gives it to its agents. |
| [STATUS.md](STATUS.md) | Progress, written by `make status` from the mark colors. |
| `Makefile` | The daily commands. `make help` lists them. |
| `sources/` | The designspace, the Regular and Bold UFOs, `sources/config.yaml` (the gftools builder recipe), `sources/held-out-glyphs.toml` (cases of the drafting evaluation) and `sources/proof-samples.toml` (proof texts). Two Python files hold what only this font needs: `sources/fix_gf_metadata.py` (three metadata fixes that `make build` applies) and `sources/fontspector_checks.py` (the Fontspector checks of this font, which `make test` runs with the Font.Garden profile). |
| [documentation/google-fonts.md](documentation/google-fonts.md) | The release: facts, QA, package and the Add Font issue. |
| `.agents/tasks/` | Contracts for unattended runs: glyph drafts and accented letters. |

`CONTEXT.md` is the one design file. Do not state a design value or a design
rule in another file. Take direction from Eli, not from older reports or
records in the Git history.

## Tools

The source tools are in
[fgtools](https://github.com/fontgarden/fgtools), a shared
package with the command `fgtools`. `make setup` installs it, pinned to a
commit in `requirements.in` and `requirements.txt`, with the pinned fontc and
Fontspector binaries. `.venv/bin/fgtools --help` lists every command. Change
a general tool there, not here. The design checks need the `runebender`
command on `PATH`:

```sh
cargo install --locked --git https://github.com/fontgarden/runebender runebender
```

The guide of the Font.Garden system is at https://font.garden/docs. Its
source is https://github.com/fontgarden/fontgarden.github.io. When you change
a command, a `make` target, a mark color, the layout or a workflow here,
update the chapter of the guide in the same session. The README of that
repository lists the chapter for each kind of change.

## Work loop

1. **Choose.** `make queue` ranks the glyphs that most composites wait on.
   Eli names the glyphs to work on.
2. **Draft.** Read all of `CONTEXT.md`. Draw the glyph as a Runebender
   proposal, or in the source with a purple mark. Where an edit is a
   calculation, use `fgtools edit` and do not type the coordinates: it moves
   an edge, sets the sidebearings or makes a mirrored copy, and a second run
   changes nothing. Commit the draft before Eli edits it, so that the Git
   history holds the draft and the correction.
3. **Look and check.** Run `.venv/bin/fgtools render "<glyphs>"` before and
   after every edit, and read the picture: the change, the filled glyph, its
   points, the green glyphs of the same construction (`--beside`) and the
   reference fonts. Under the glyph is the glyph in a line of text, sharp and
   blurred, with its color as a number: in the blurred line a glyph that is
   too heavy is a dark spot, and a glyph that is too light is a hole. Review
   the draft against each rule of `CONTEXT.md` by number. Run `make check-design GLYPHS="..."` and `make check-changes`,
   and correct the findings.
4. **Second review.** Before a draft goes to Eli, a second agent reviews
   it. It gets the picture of `fgtools render`, `CONTEXT.md` and the glyph
   names, and not the notes of the agent that drew. It gives each glyph in
   each master the verdict `pass`, or `fault` with the rule number and the
   place. The first agent corrects each fault and asks again, at most three
   times. A fault that remains goes into the report. A harness without
   subagents does the review in a new session.
5. **Build and compare.** Run `make build`, then `make diff`. It builds main
   and the working tree and compares them with diffenator3. Every changed
   glyph, word, table or language result must be one that the edit explains.
   Look at the glyph in words at 400, 550 and 700, with the marks, joining
   forms and composites that use it (`make proof-web` or Runebender).
6. **Review.** Eli grades the glyph. The review commit changes the purple
   mark to red (broken), orange (better), yellow (close) or green.
7. **Learn.** When Eli asks, run `.venv/bin/fgtools corrections`. It lists
   the reviews in which Eli changed a purple draft and that no file or commit
   message cites yet. Propose one change for each, and cite the review
   commit:

| The correction shows | Change |
| --- | --- |
| a mistake that a script can find | a value in a `toml` block of `CONTEXT.md`, or a check in fgtools |
| a principle of the design, or a decision about one glyph | a rule in `CONTEXT.md`, with "Seen in" and the commit |
| a decision that a drafting method has to learn | a case in `sources/held-out-glyphs.toml`, with a comment |

Eli approves or rejects each change. One correction is not a rule. When the
same mistake occurs again, add the glyph and the commit to the existing rule.

The checks are a filter. They do not measure quality, and a pass is not
approval: the checks also flag some approved green drawings. Command success
is not visual review. Report each visible fault, for example a swollen join
or a pinched counter, even when every check passes.

## Source rules

- Draw or redraw only glyphs Eli names, in the masters Eli names.
- A request to clean up a glyph, or to make it "more X", is the smallest
  change to the current drawing, usually handle edits. It is not a new design.
- Green contour glyphs are frozen. Eli approves contour glyphs. Mark new AI
  drawing purple. Only green glyphs are references and training data.
- A change to a component donor also changes every glyph that uses it. Do not
  change a donor that a green glyph uses.
- A composite that `fgtools check-design --ready` lists can be marked green.
- Keep contour, point and component structure the same in both masters.
  `.venv/bin/fgtools lint-glifs` checks it.
- Edit GLIF XML and plists surgically in the existing style (tabs, double
  quotes, no space before `/>`). Never call whole-UFO `font.save()`.
- In a GLIF, a point without a `type` is an off-curve point. To change the
  left sidebearing, move every point and component by the same amount. To
  change the right sidebearing, change the advance only.
- Register new glyphs in `contents.plist` and `public.glyphOrder` in both
  masters.
- Do not add a script that writes whole glyph sets into the UFOs.
- Files that people edit use TOML with comments. JSON is only for data that
  a program writes. `sources/config.yaml` is YAML because gftools requires it.

## Proofs

- Use the same em size, origin and baseline for every font in a comparison.
- A proof is valid only for the sources it was built from. Do not reuse a
  proof after an edit. For a "before" state, build a known revision in a
  separate checkout.
- `fgtools check-changes --glyphs "..." --proof <directory>` draws Runebender
  proof sheets of changed glyphs, before and after.
- A picture for review has a dark gray background and light gray ink, never
  pure black and white.

## Unattended tasks

A task contract in `.agents/tasks/` gives the goal, the acceptance checks,
the constraints and the form of the report. Run a contract in a separate
checkout, on its own branch, for example with OMP:

```sh
git worktree add ../virtua-grotesk-omp main
cd ../virtua-grotesk-omp
mkdir .omp && ln -s ../AGENTS.md .omp/RULES.md
omp -p --wait-async --max-time 60m \
  "Do the task in .agents/tasks/glyph-drafts.md for: acute caron circumflex, Regular."
```

The link gives the subagents of OMP these rules: OMP gives them
`.omp/RULES.md` and not this file. Git ignores `.omp/`, as it ignores the
files of every single agent tool. After any agent edits glyphs, run `make check-changes`. It fails
when a green glyph changed, or when the contours of a glyph changed and it is
not purple.

## What belongs in the repository

The repository holds sources and the documents in the table above. It
does not hold records of work.

- Do not add worklogs, handoffs, receipts, reports, plans, audits or dated
  documents. The Git history and commit messages are the record of work.
- Do not add a document. Extend the one in the table that covers the subject.
  A fact is stated in one file only.
- Generated output goes to `output/`, which Git ignores. A tracked file has at
  most 500 KB, because a file stays in every clone of the history.
- `fgtools check-repository` (in `make test`) fails when a tracked file has
  no place in the layout of Font.Garden projects, or when a document names a
  file or a `make` target that does not exist.
- Commit messages are plain, with no agent credit or trailers.

## How to work with Eli

- Report finished work in a few short lines: what changed, and what needs a
  decision. Give details only when Eli asks.
- Write documents, comments and commit messages in simple technical English:
  short sentences, one word for one thing, no em dashes, no slogans. Choose
  the names that an engineer would write in a specification.
- Do not add a mechanism (an option, a tag, a file, a convention) for a fact
  that an existing mechanism records. A workflow that Eli has to remember is
  not used.
- A repository file names only a command that can be installed, with its
  install line. It never names a path or a link on one machine.
- Use `~/Temp/` for temporary files.
- Commit and push only when Eli asks.
