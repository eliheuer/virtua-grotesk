# Virtua proof application

Design context, corrections and review history now live in
[design/README.md](../design/README.md). Start there for glyph work and current state.
This directory owns the live comparison app and proof tooling.

```sh
make proof-web
.venv/bin/python agent-proofs/serve.py --check
```

Read [app/README.md](app/README.md) for rendering and snapshot preparation.
The current portable proof is selected by `design/reviews/current.json` unless a
local explicit selection is recorded in `out/live-proof-selection.json`.
`cases` is a compatibility symlink to `design/reviews`; create new reviews at the
canonical location. [Previous central guide](../design/reviews/history/workflow-2026-10-29.md)
is historical, including its dated authorizations and next-phase queues.
