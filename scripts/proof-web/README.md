# Virtua proof application

This directory holds the live comparison proof. It renders Virtua Grotesk
beside the fonts in `reference-fonts/` at one em size and weight.

```sh
make proof-web
.venv/bin/python scripts/proof-web/serve.py --current --check
```

`make proof-web` builds the fonts and serves the current build. To compare a
frozen Before font with a Candidate font, prepare a snapshot and pass
`--snapshot <prepared-directory>`; the server remembers that selection in
`out/live-proof-selection.json`. Read [app/README.md](app/README.md) for
the modes, snapshot preparation and the rendering contract.
