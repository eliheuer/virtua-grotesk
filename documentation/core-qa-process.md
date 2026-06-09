# Core QA Process

This is the active QA checklist for Virtua Grotesk. Keep it small and update it
when the build, proofing, Fontspector, or source-report workflow changes.

## Local Gates

Run these from the repo root.

| Gate | Command | Purpose |
| --- | --- | --- |
| Setup | `make setup` | Create `.venv/` and install `requirements.txt`. |
| Build | `make build` | Build variable and static TTFs from `sources/config.yaml`. |
| Main proof | `make proof` | Build and render `documentation/proofs/proof.pdf`. |
| Print specimen | `make specimen` | Build and render the landscape spacing specimen PDF. |
| README images | `make readme-images` | Regenerate the 2048x1024 README PNG specimens. |
| Reports | `make reports` | Regenerate source UFO metadata, generated font metadata, and master compatibility reports. |
| Preflight | `make preflight` | Build, proof, specimen, reports, then check expected artifacts exist. |
| Google Fonts QA | `make test` | Build, then run Fontspector's `googlefonts` profile. |

`make preflight` is the normal handoff gate during drawing work. `make test` is
the stricter Google Fonts QA gate and is expected to fail until drawing,
coverage, contour, and metadata blockers are resolved.

## Review Order

1. Edit UFO sources in `sources/`.
2. Run `make build`.
3. Run `make proof` or `make specimen` when the change affects drawing,
   spacing, weight, or rhythm.
4. Run `make reports` and review:
   - `documentation/source/source-ufo-metadata.md`
   - `documentation/source/generated-font-metadata.md`
   - `documentation/source/master-compatibility.md`
5. Run `make preflight` before handing work back.
6. Run `make test` before treating the repo as Google Fonts-submission ready.

## Archive Policy

Older generated review reports and helper scripts live under
`documentation/archive/agent-generated-reports/` and
`documentation/archive/agent-generated-scripts/`. Treat them as historical
context, not current workflow. If one becomes useful again, move it back with a
clear Makefile target and current documentation.
