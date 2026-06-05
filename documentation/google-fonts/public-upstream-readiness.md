# Public Upstream URL Readiness

This generated report keeps the public upstream URL decision tied to the
current git remote and the exact files that still carry placeholder or
pending downstream URL text.

## Current Local Git Evidence

- Current branch: `main`
- Origin fetch URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Origin push URL: `git@github.com:eliheuer/virtua-grotesk.git`
- Normalized GitHub origin candidate: `https://github.com/eliheuer/virtua-grotesk`
- Placeholder URL: `https://github.com/fontgarden/virtua-grotesk`
- Origin candidate differs from placeholder: yes
- Apply helper: `scripts/apply_public_upstream_url.py`
- Report/helper target lists match: yes

## Replacement Surface

- Placeholder or pending URL findings: 0

| File | Line | Text |
| --- | ---: | --- |

## Candidate Replacement Preview

This preview does not apply the decision. It shows the exact replacement
target if the normalized origin candidate is approved as the canonical
public upstream URL.

- Candidate URL: `https://github.com/eliheuer/virtua-grotesk`
- Candidate copyright line: `Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)`
- Placeholder URL replacements: 0
- Pending URL field replacements: 0

| File | Line | Candidate text |
| --- | ---: | --- |

## Apply Helper Alignment

The dry-run/apply helper and this report must stay aligned so the
maintainer-approved URL replacement cannot miss a public metadata
surface that the readiness report already identified.

- Report target files: 11
- Helper target files: 11
- Missing from helper: none
- Extra in helper: none

## Stale Placeholder Guards

These internal guards intentionally retain the old placeholder URL so
stale downstream metadata from earlier dry runs cannot be reused after
the final public URL decision is applied. Do not replace these with the
final canonical URL.

- Internal stale-placeholder guards: 1

| File | Line | Guard text |
| --- | ---: | --- |
| `scripts/package_gf_dry_run.sh` | 100 | `stale_placeholder_upstream_url="https://github.com/fontgarden/virtua-grotesk"` |

## Apply Before Final Packaging

- Keep the normalized origin candidate as the public canonical
  upstream URL for Google Fonts.
- Replace the placeholder URL consistently in `OFL.txt`, UFO font
  metadata, generated metadata patching, downstream package preview,
  and handoff docs.
- Rebuild fonts so generated name ID 0 and generated metadata reports
  carry the final URL.
- Rerun `make preflight` so proof evidence and generated reports
  stay synchronized, then run
  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` after
  the selected release/archive exposes all `source.files` paths.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
