# Virtua Grotesk

Virtua Grotesk is a geometric sans serif by Eli Heuer, built on a power-of-two
grid with 16-unit chamfered corners. The upright family has a weight axis from
Regular (400) to Bold (700), with Medium and SemiBold instances.

![Virtua Grotesk construction sheet showing the word Grid](https://elih.net/og/virtua-grotesk.png)

The font is in development. Latin, Arabic, and Hebrew are planned for the first
Google Fonts release; drawings and script behavior still need review. Italic
is a separate future proposal. See the [onboarding checklist](documentation/google-fonts/README.md)
for measured blockers and remaining decisions.

[Design background: Grid Systems as Datasets](https://elih.net/blog/virtua-grotesk)

## Build

Install Python 3.11 or later, then run from the repository root:

```sh
make setup
make build
```

On Linux, the Python dependencies also need Cairo development headers,
`pkg-config`, and Python development headers. On macOS, install Cairo and
`pkg-config` before setup if they are not already available.

`scripts/build.sh` uses the pinned Python requirements and `sources/config.yaml`, then
applies the repository's compiled-font metadata fixes. Outputs are:

- `fonts/variable/VirtuaGrotesk[wght].ttf`
- `fonts/ttf/VirtuaGrotesk-{Regular,Medium,SemiBold,Bold}.ttf`

Builds replace generated files under `fonts/` and `build/`; the UFO sources are
the editable originals. Binaries are ignored in Git. CI uploads build artifacts;
a public release for onboarding is still pending.

## Review and contribute

Read [AGENTS.md](AGENTS.md) before you edit sources with an agent. The design
rules are in [documentation/design/README.md](documentation/design/README.md). Progress is in
[STATUS.md](STATUS.md).

- `make status`: write STATUS.md from the mark colors in both masters.
- `make proof-web`: build, then compare the fonts with `reference-fonts/` in a browser.
- `make lint-grid` and `make grid-qa`: check outlines against the 8-unit grid.
- `make test`: development Fontspector checks, with documented exclusions.
- `make qa-full`: all configured Google Fonts profile checks, without exclusions.
- `make review`: a separate Diffenator3 QA browser proof.
- `make proof`: the main PDF. This target needs the designbot CLI.
- `make help`: all other commands.

See [QA and tool setup](documentation/qa.md) and the
[documentation index](documentation/README.md). Report problems or propose
changes in [GitHub issues](https://github.com/eliheuer/virtua-grotesk/issues).

AI tools have assisted with code, documentation, and candidate glyph generation.
Source colors describe drawing quality, composite status, and what may be changed.

## Helper model workflow

Use the local helper model with a coding agent and **native Runebender** to propose
point edits, review them in Runebender's Agent Proof view, and take turns editing
with the agent.

**Start here:** [Helper model workflow guide](documentation/native-model-workflow.md).
Use the [red-pencil review loop](documentation/native-model-workflow.md#red-pencil-review-loop)
to mark corrections or sketch another form directly in native Agent Proof. Agents
receive the annotated PNG through MCP, interpret your intent, and prepare a scratch
candidate. The model takes geometry and a point mask; it does not read the sketch.

It covers Linux setup, model inference, the required MCP connection, scratch
comparisons, and handing control between you and the agent.

Give your agent this instruction:

> Read AGENTS.md and the Helper model workflow section of README.md, then follow
> documentation/native-model-workflow.md. Start with the bundled sample in a
> scratch font in native Runebender. Keep Virtua's actual font unchanged and pause
> for my review before further edits.

The [Regular Arabic helper model](models/arabic-repair-hour-v1/README.md) is included
in this repository (148 KiB, 36,578 parameters) and runs locally on CPU. It remains
experimental: it changes clean held-out drawings and is not approved for automatic
cleanup. Pull and build the required Runebender version as well as this repository;
Pi needs an MCP bridge to control the editor.

## Semantic colors

Glyph colors are editing and reference permissions, not just progress indicators.
The same meanings apply to people and AI tools.

For AI edits, these meanings apply only inside a scope that Eli names: the
glyphs and the masters. Eli gives the verdict, and only Eli assigns green.
Purple identifies AI-drawn or substantially redrawn glyphs that wait for human
review. Purple gives no approval, reference or protection status.

| Color | Meaning | Editing and reference use |
| --- | --- | --- |
| Red | Bad, replaceable, or no drawing. | OK to overwrite or replace. Do not use as reference material. |
| Orange | Bad drawing, but contains useful information worth preserving. | Edits are welcome; do not overwrite the drawing. Do not use as reference material. |
| Yellow | Better drawing, but still needs work. | Edit without overwriting. Not good enough to use as reference material. |
| Green | Approved glyph, whether an outline or composite; frozen by default. | Use as reference material. Changes require Eli's explicit approval naming the glyph and master. |
| Blue | Composite drawing with a problem that needs attention and judgment to resolve. | Inspect the composite and fix the problem. It is not an approved reference. |
| Purple | AI-drawn or substantially redrawn; not yet reviewed or edited by a human. | Editable within authorized scope; not an approved reference. Human review replaces purple with the appropriate grade. Git/proof records retain provenance. |
| Pink | Composite drawing needing a small amount of work, less than blue. | Edits are welcome. Do not use as reference material. |

Blue describes a composite needing attention; it does not mean “AI-generated.”
Only red explicitly permits replacement or overwriting.
When editing a composite, preserve any green component glyphs it uses.
Uncolored or unfamiliar labels do not grant automatic editing or reference permission; clarify their meaning first.
Human grading determines approval; AI tools must not change review colors automatically.
Leave new candidates ungraded unless Eli specifies a review color.

## License

The font is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
Copyright holders are listed in [AUTHORS.txt](AUTHORS.txt); other contributors
are listed in [CONTRIBUTORS.txt](CONTRIBUTORS.txt).
