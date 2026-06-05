# Family Name Readiness

This generated report tracks the Google Fonts family-name decision
surface: app-menu naming, namecheck confirmation, Reserved Font Name
status, and Google CLA readiness. It records objective local evidence
separately from maintainer confirmations that cannot be inferred from
the source tree.

## Summary

- Family names from built fonts: `Virtua Grotesk`
- Family names are ASCII letters/digits/spaces only: yes
- Longest family name length: 14
- OFL Reserved Font Name status: none declared after copyright line
- Namecheck confirmation: confirmed by maintainer at `namecheck.fontdata.com`
- Trademark/catalog-name clearance: confirmed by maintainer
- Google CLA status: confirmed by maintainer for the copyright holder
- Decision log status: decided

## Built Font Names

| Font | nameID 1 | nameID 2 | nameID 4 | nameID 6 | nameID 16 | nameID 17 |
| --- | --- | --- | --- | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `Virtua Grotesk` | `Regular` | `Virtua Grotesk Regular` | `VirtuaGrotesk-Regular` | `unset` | `unset` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `Virtua Grotesk` | `Regular` | `Virtua Grotesk Regular` | `VirtuaGrotesk-Regular` | `unset` | `unset` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `Virtua Grotesk Medium` | `Regular` | `Virtua Grotesk Medium` | `VirtuaGrotesk-Medium` | `Virtua Grotesk` | `Medium` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `Virtua Grotesk SemiBold` | `Regular` | `Virtua Grotesk SemiBold` | `VirtuaGrotesk-SemiBold` | `Virtua Grotesk` | `SemiBold` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `Virtua Grotesk` | `Bold` | `Virtua Grotesk Bold` | `VirtuaGrotesk-Bold` | `unset` | `unset` |

## Authorship And App-Menu Name Check

- AUTHORS.txt entries: `Eli Heuer`
- CONTRIBUTORS.txt entries: `Eli Heuer`
- Built family names include copyright-author full name: no
- Current definitive app-menu family name candidate: `Virtua Grotesk`
- App-menu family name candidate appears in built names: yes

## Add Font Name Requirements

| Requirement | Current evidence | Status |
| --- | --- | --- |
| Unique according to `namecheck.fontdata.com` | confirmed by maintainer at `namecheck.fontdata.com` | ready |
| No Reserved Font Names in OFL or known upstream docs | none declared after copyright line | ready |
| Definitive app-menu family name | `Virtua Grotesk` present in built names: yes | ready |
| App-menu name avoids copyright-holder full names/acronyms | built names include author full name: no | ready |
| Trademark/catalog-name clearance | confirmed by maintainer | ready |
| Google CLA | confirmed by maintainer for the copyright holder | ready |

## Reserved Font Name Evidence

- OFL line 2 is blank after the copyright line: yes
- No project-specific RFN declaration found immediately after the copyright line.

## Apply Before Final Submission

- Keep the confirmed namecheck, trademark/RFN, and CLA statements in
  `documentation/google-fonts/google-fonts-decisions.md` and the Google Fonts issue
  text.
- Confirm the local git name and email match the signed CLA identity
  before opening the downstream pull request.
- Rerun `make preflight` after any family-name metadata change.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/making-pr.html
