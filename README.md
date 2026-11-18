# Virtua Grotesk

Virtua Grotesk is a typeface designed by Eli Heuer for Latin, Arabic and
Hebrew. It is a grid-based neo-grotesk drawn on a dyadic self-labeling grid
system: nested grids built on powers of two. The grid records drawing intent
and limits the number of possible points. The variable font has a weight axis
from Thin (100) to Black (900) and an optical size axis from 14 to 144 pt.

The description of the design, with its idea, its precedents and its rules,
is in [CONTEXT.md](CONTEXT.md).

![Virtua Grotesk letters and numerals at four weights](documentation/article/weight-specimen.svg)

The font is in development and is intended for Google Fonts. The progress of
each script is in [STATUS.md](STATUS.md). The release scope, open decisions
and links to the Google Fonts guide are in
[documentation/google-fonts.md](documentation/google-fonts.md). The design
background is in the article
[Virtua Grotesk: Grid Systems for Dataset Engineering](https://elih.net/blog/virtua-grotesk).

## Build

Install Python 3.13 or later, then run from the repository root:

```sh
make setup
make build
```

The build writes `fonts/variable/VirtuaGrotesk[opsz,wght].ttf` and nine static
fonts in `fonts/ttf/`. Git ignores `fonts/`. The editable sources are the two
UFO masters and the designspace in `sources/`.

## Work on the font

| Command | Use |
| --- | --- |
| `make runebender` | Open the sources in Runebender. Install it with `cargo install --locked --git https://github.com/fontgarden/runebender runebender`. |
| `make formats` | List the formats, the canvases and the pages of the proof. `make proof PAGE="spacing kerning"`, `make specimen PAGE=words` and `make media FORMAT=videos` or `make media FORMAT=weight-axis CANVAS=landscape` make a part only. `make copy-format FORMAT=words` copies a default format into the project, to change it for this font. |
| `make proof` | Build, then write the print proof, a PDF of A4 pages, to `output/proof/proof.pdf`: the character set, the sizes, reading text, spacing, kerning, diacritics, the weight axis and the tables of the Arabic script. Needs DesignBot, which `make setup` installs. |
| `make media` | Build, then render the marketing media (images, carousels and video for Instagram, LinkedIn and X) into `output/media/`. Needs DesignBot, and `ffmpeg` for video. |
| `make specimen` | Build, then write the print specimen, a PDF of A4 pages, to `output/specimen/`. |
| `make site` | Build, then make the proof, the specimen and the media, and collect them into `output/site/`. CI publishes this folder. |
| `make render GLYPHS="a n"` | Draw glyphs large for review, with the change since `main`. |
| `make proof-web` | Build, then compare the font with the fonts in `reference-fonts/` in a browser. |
| `make test` | Build, then check the repository and check the fonts with Fontspector. |
| `make help` | All commands. |

The design rules, with the values that the tools check, are also in
`CONTEXT.md`. The rules for work on the sources are in
[AGENTS.md](AGENTS.md).

## Mark colors

Each glyph has a mark color in each master. The color tells people and agents
what they can do with the glyph. The full policies are in
[CONTEXT.md](CONTEXT.md).

| Color | Meaning |
| --- | --- |
| Green | Approved by Eli. A reference for other glyphs. Frozen. |
| Yellow | Close. Needs small edits. |
| Orange | Better, not good enough. Keep the useful construction. |
| Red | Broken. Can be replaced. |
| Purple | AI drawing that Eli has not reviewed. |
| Blue | Composite that needs diagnosis. |
| Pink | Composite that needs small edits. |

Only green glyphs are references. The release target is every glyph green in
every master.

## Tools

The source tools are shared by all Font.Garden fonts and are in
[fgtools](https://github.com/fontgarden/fgtools), with the
command `fgtools`. `make setup` installs them. The fonts are built with
fontc and checked with Fontspector. The guide is at https://font.garden/docs.

AI tools help with code, documentation and draft glyphs. Eli draws, reviews
and approves the glyphs.

## License

The font is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
The copyright holders are in [AUTHORS.txt](AUTHORS.txt) and the contributors
in [CONTRIBUTORS.txt](CONTRIBUTORS.txt). Report problems in
[GitHub issues](https://github.com/eliheuer/virtua-grotesk/issues).
