# Virtua Grotesk

Virtua Grotesk is a geometric sans serif by Eli Heuer for Latin, Arabic and
Hebrew. It is drawn on a power-of-two grid with 16-unit chamfered corners. The
variable font has a weight axis from Regular (400) to Bold (700), with Medium
and SemiBold instances.

![Virtua Grotesk construction sheet showing the word Grid](https://elih.net/og/virtua-grotesk.png)

The font is in development and is intended for Google Fonts. The progress of
each script is in [STATUS.md](STATUS.md). The release scope, open decisions
and links to the Google Fonts guide are in
[documentation/google-fonts.md](documentation/google-fonts.md). The design
background is in the article
[Grid Systems as Datasets](https://elih.net/blog/virtua-grotesk).

## Build

Install Python 3.11 or later, then run from the repository root:

```sh
make setup
make build
```

The build writes `fonts/variable/VirtuaGrotesk[wght].ttf` and four static
fonts in `fonts/ttf/`. Git ignores `fonts/`. The editable sources are the two
UFO masters and the designspace in `sources/`.

## Work on the font

| Command | Use |
| --- | --- |
| `make runebender` | Open the sources in the Runebender web editor. |
| `make proof-web` | Build, then compare the font with the fonts in `reference-fonts/` in a browser. |
| `make check-design GLYPHS="n a"` | Check glyphs against the grid and stroke targets. |
| `make status` | Write `STATUS.md` from the mark colors. |
| `make qa` | Google Fonts checks with Fontspector. |
| `make help` | All commands. |

The commands and checks are described in
[documentation/qa.md](documentation/qa.md). The design rules are in
[documentation/design/](documentation/design/README.md).

## Mark colors

Each glyph has a mark color in each master. The color tells people and agents
what they can do with the glyph. The full policies are in
[sources/design.toml](sources/design.toml).

| Color | Meaning |
| --- | --- |
| Green | Approved by Eli. A reference for other glyphs. Frozen. |
| Yellow | Good drawing that needs more work. |
| Orange | Poor drawing with useful construction to keep. |
| Red | Can be replaced. |
| Purple | AI drawing that Eli has not reviewed. |
| Blue | Composite that needs diagnosis. |
| Pink | Composite that needs small edits. |

Only green glyphs are references. The release target is every glyph green in
both masters.

## Tools

The source tools are shared by all Font.Garden fonts and are in
[fontgarden-tools](https://github.com/fontgarden/fontgarden-tools), with the
command `fgtools`: status, design checks, change checks, curve checks, the
build, build comparisons, the drafting evaluation and the list of
corrections. `make setup` installs them, pinned to a commit in
`requirements.txt`, with the pinned fontc and Fontspector binaries. The
`make` targets run them. The fonts are built with fontc, and `make diff`
compares builds with diffenator3. The
Font.Garden QA profile is `scripts/fontspector_fontgarden.py`; its Rust
version, which will replace it, is
[fontspector-fontgarden](https://github.com/fontgarden/fontspector-fontgarden).
`scripts/` holds only the tools that are specific to Virtua Grotesk.

AI tools help with code, documentation and draft glyphs. Eli draws, reviews
and approves the glyphs. The rules for agents are in [AGENTS.md](AGENTS.md).

## License

The font is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
The copyright holders are in [AUTHORS.txt](AUTHORS.txt) and the contributors
in [CONTRIBUTORS.txt](CONTRIBUTORS.txt). Report problems in
[GitHub issues](https://github.com/eliheuer/virtua-grotesk/issues).
