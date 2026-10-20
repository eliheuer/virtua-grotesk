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

`build.sh` uses the pinned Python requirements and `sources/config.yaml`, then
applies the repository's compiled-font metadata fixes. Outputs are:

- `fonts/variable/VirtuaGrotesk[wght].ttf`
- `fonts/ttf/VirtuaGrotesk-{Regular,Medium,SemiBold,Bold}.ttf`

Builds replace generated files under `fonts/` and `build/`; the UFO sources are
the editable originals. Binaries are ignored in Git. CI uploads build artifacts;
a public release for onboarding is still pending.

## Review and contribute

Start with [Virtua Design Review](agent-proofs/README.md):
the central map, current handoff and new-session instructions for the font review
loop. Its default comparison interface is the
[live web proof](agent-proofs/app/README.md).

- `make proof-web`: serve or reuse the live design-review interface.
- `make test`: development Fontspector checks, with documented exclusions.
- `make qa-full`: all configured Google Fonts profile checks, without exclusions.
- `make review`: a separate Diffenator3 QA browser proof.
- `make proof`: the main PDF, requiring the separately installed designbot CLI.
- `make help`: editor and other development commands.

See [QA and tool setup](documentation/qa.md), the [design contract](DESIGN.md),
and the [documentation index](documentation/README.md). Report problems or
propose changes through [GitHub issues](https://github.com/eliheuer/virtua-grotesk/issues).

AI tools have assisted with code, documentation, and candidate glyph generation.
Source colors describe drawing quality, composite status, and what may be changed.
See [AGENTS.md](AGENTS.md) before editing sources with an agent.

## Semantic colors

Glyph colors are editing and reference permissions, not just progress indicators.
The same meanings apply to people and AI tools.

For AI edits, these are defaults within a specifically approved scope, not
permission to start a drawing batch. Follow [the approval workflow](AGENTS.md#source-safety):
propose named glyphs and masters, wait for Eli's approval, prepare a reversible
scratch candidate, and show proofs before applying it when only candidate work
was approved. Explicit approval can override a color restriction for those named
glyphs only. Green and purple edits require that explicit exception.

| Color | Meaning | Editing and reference use |
| --- | --- | --- |
| Red | Bad, replaceable, or no drawing. | OK to overwrite or replace. Do not use as reference material. |
| Orange | Bad drawing, but contains useful information worth preserving. | Edits are welcome; do not overwrite the drawing. Do not use as reference material. |
| Yellow | Better drawing, but still needs work. | Edit without overwriting. Not good enough to use as reference material. |
| Green | Good drawing; frozen by default. | Use as reference material. Changes require Eli's explicit approval naming the glyph and master. |
| Blue | Composite drawing with a problem that needs attention and judgment to resolve. | Inspect the composite and fix the problem. It is not an approved reference. |
| Purple | Good composite drawing; frozen by default, like green. | Use as reference material. Changes require Eli's explicit approval naming the glyph and master. |
| Pink | Composite drawing needing a small amount of work, less than blue. | Edits are welcome. Do not use as reference material. |

Blue describes a composite needing attention; it does not mean “AI-generated.”
Only red explicitly permits replacement or overwriting.
When editing a composite, preserve any green or purple component glyphs it uses.
Uncolored or unfamiliar labels do not grant automatic editing or reference permission; clarify their meaning first.
Human grading determines approval; AI tools must not change review colors automatically.
Leave new candidates ungraded unless Eli specifies a review color.

## License

The font is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
Copyright holders are listed in [AUTHORS.txt](AUTHORS.txt); other contributors
are listed in [CONTRIBUTORS.txt](CONTRIBUTORS.txt).
