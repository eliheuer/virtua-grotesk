# Open Placeholder Audit

This generated report tracks unresolved text that must be reviewed before a
public Google Fonts handoff. It deliberately separates known maintainer
decisions from drawing/source blockers so the final package pass is not
blocked by hidden placeholder strings. Internal guard strings are kept
separate because they protect the workflow from stale generated files
and are not public handoff text.

## Summary

- Public placeholder blocker count: 0
- Placeholder upstream URL occurrences: 0
- Pending decision markers: 0
- TODO/FIXME markers: 0
- Internal stale-placeholder guards: 1
- Internal metadata guard markers: 5
- Actionable placeholder upstream URL occurrences: 0
- Actionable pending decision markers: 0
- Generated evidence echoes: 0

## Decision Blockers

No unresolved public placeholder strings were found in the audited files.

## Internal Guards

These strings intentionally retain old placeholder values to reject stale generated files. They are not public replacement surfaces.

| Kind | File | Line | Text |
| --- | --- | ---: | --- |
| stale placeholder guard | `scripts/package_gf_dry_run.sh` | 99 | `stale_placeholder_upstream_url="https://github.com/fontgarden/virtua-grotesk"` |
| metadata pending guard | `scripts/package_gf_dry_run.sh` | 106 | `unresolved_metadata_markers=(` |
| metadata pending guard | `scripts/package_gf_dry_run.sh` | 107 | `"Pending decision"` |
| metadata pending guard | `scripts/package_gf_dry_run.sh` | 108 | `"Pending:"` |
| metadata pending guard | `scripts/package_gf_dry_run.sh` | 109 | `"Pending final"` |
| metadata pending guard | `scripts/package_gf_dry_run.sh` | 149 | `for marker in "${unresolved_metadata_markers[@]}"; do` |

## Generated Evidence Echoes

No generated report echoes were found.

## Apply Before Downstream Packaging If Public Blockers Appear

- Replace placeholder upstream URLs in license, source metadata, public docs, and metadata preview files.
- Replace public `Pending decision` markers with final maintainer-approved wording or move them to internal notes.
- Remove public `TODO` or `FIXME` markers from handoff artifacts.
- Keep intentional stale-placeholder guard strings in scripts that reject bad generated files.
- Regenerate this report with `make preflight` after decisions are applied.
