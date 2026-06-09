# Designer Profile Readiness

This generated report tracks Google Fonts designer-profile readiness for
the downstream `METADATA.pb` designer string. The Google Fonts metadata
guide says each designer listed in `METADATA.pb` needs a matching
`catalog/designers/*/info.pb` entry, and the designer profile guide says
that profile name must be spelled exactly the same as the metadata
designer string.

## Local Google Fonts Checkout

- Path: `GF_REPO_PATH_NOT_CONFIGURED`
- Designer catalog exists: no
- Designer profiles read: 0
- AUTHORS catalog-credit candidates: 1
- Contributor-only candidates: 0
- Candidate profiles missing: 1

## Current Upstream Names

- AUTHORS.txt: `Eli Heuer`
- CONTRIBUTORS.txt: `Eli Heuer`
- Metadata preview designer strings: `Eli Heuer`
- Final metadata designer strings present: yes
- Final comma-separated designer entities present: yes
- Pending metadata designer placeholders: 0

## Candidate Designer Profiles

| Candidate | Source | Expected catalog slug | Exact profile found | Matching profile path |
| --- | --- | --- | --- | --- |
| `Eli Heuer` | `AUTHORS.txt` | `eliheuer` | no | missing |

## Metadata Designer String Status

| Metadata designer string | Final value | Profile found |
| --- | --- | --- |
| `Eli Heuer` | yes | no |

## Final Metadata Designer Entity Status

| Designer entity | Source metadata string | Profile found | Matching profile path |
| --- | --- | --- | --- |
| `Eli Heuer` | `Eli Heuer` | no | missing |

## Before Final Packaging

- Confirm the final `METADATA.pb` `designer` string and designer order.
- Treat `AUTHORS.txt` names as the catalog-credit candidates; use
  `CONTRIBUTORS.txt` to review whether any additional credited
  contributors belong in the metadata designer string.
- Confirm every comma-separated designer/foundry in that string has a
  matching Google Fonts designer profile or a profile request prepared.
- Confirm any new `catalog/designers` profile uses third-person English
  biography text, an image, and an `info.pb` designer string that exactly
  matches `METADATA.pb`.
- Re-run this report after profile files, metadata, or catalog checkout
  state change.

References:

- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/profile.html
- https://googlefonts.github.io/gf-guide/googlefonts.html
