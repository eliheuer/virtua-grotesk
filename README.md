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

- `make test`: development Fontspector checks, with documented exclusions.
- `make qa-full`: all configured Google Fonts profile checks, without exclusions.
- `make review`: a diffenator2 browser proof.
- `make proof`: the main PDF, requiring the separately installed designbot CLI.
- `make help`: editor and other development commands.

See [QA and tool setup](documentation/qa.md), the [design contract](DESIGN.md),
and the [documentation index](documentation/README.md). Report problems or
propose changes through [GitHub issues](https://github.com/eliheuer/virtua-grotesk/issues).

AI tools have assisted with code, documentation, and candidate glyph generation.
Source colors distinguish human-approved drawings from candidates awaiting
review. See [AGENTS.md](AGENTS.md) before editing sources with an agent.

## License

The font is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
Copyright holders are listed in [AUTHORS.txt](AUTHORS.txt); other contributors
are listed in [CONTRIBUTORS.txt](CONTRIBUTORS.txt).
