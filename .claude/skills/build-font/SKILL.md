# /build-font

Build Virtua Grotesk fonts from UFO/designspace sources.

## Usage

```bash
/build-font
```

## Instructions

Use the repository build entrypoint:

```bash
./build.sh
```

or:

```bash
make build
```

The Google Fonts-ready path uses `gftools builder sources/config.yaml` when
`gftools` is installed in the active Python environment. `build.sh` keeps a
fallback `fontc`/`fontmake` path for local development, but Google Fonts
onboarding work should prefer the `gftools builder` path.

## Environment

Recommended setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Optional fallback dependency:

```bash
cargo install fontc
```

## Outputs

Expected generated fonts:

- `fonts/variable/VirtuaGrotesk[wght].ttf`
- `fonts/ttf/VirtuaGrotesk-Regular.ttf`
- `fonts/ttf/VirtuaGrotesk-Medium.ttf`
- `fonts/ttf/VirtuaGrotesk-SemiBold.ttf`
- `fonts/ttf/VirtuaGrotesk-Bold.ttf`

Generated fonts are ignored by git unless the built-fonts upstream decision
changes.

## After Building

Run one of:

```bash
make preflight-only
make reports-only
./scripts/check_gf_fonts.sh
```

Use `make preflight` when you want a fresh build plus reports plus local
handoff validation in one command.
