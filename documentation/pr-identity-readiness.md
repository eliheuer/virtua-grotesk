# PR Identity Readiness

This generated report records local Git and GitHub CLI identity state for the future Google Fonts issue and downstream PR. It reads the maintainer-confirmed Google CLA decision from the canonical decision log.

## Summary

- Expected CLA/author name: `Eli Heuer`
- Source repo git identity complete: yes
- Source repo git user.name matches expected CLA/author name: yes
- google/fonts fork git checkout present: yes
- google/fonts fork git identity complete: yes
- google/fonts fork git user.name matches expected CLA/author name: yes
- Final downstream commit identity ready: yes
- GitHub CLI auth status: `invalid token`
- GitHub CLI account: `eliheuer`
- GitHub API credentials ready: no
- GitHub API credential source: `unavailable`
- Google CLA status: confirmed by maintainer for the copyright holder

## Git Identity Evidence

### Source repo identity

- Repo path: `/Users/eli/GH/repos/virtua-grotesk`
- Git checkout present: yes
- git user.name configured: yes
- git user.email configured: yes
- git identity complete: yes
- git user.name matches expected CLA/author name: yes
- git user.name: `Eli Heuer`
- git user.email: `e***@protonmail.com`

### google/fonts fork identity

- Repo path: `/Users/eli/GH/forks/fonts`
- Git checkout present: yes
- git user.name configured: yes
- git user.email configured: yes
- git identity complete: yes
- git user.name matches expected CLA/author name: yes
- git user.name: `Eli Heuer`
- git user.email: `e***@protonmail.com`

## GitHub CLI Evidence

- `gh auth status` exit code: 1
- Sanitized status: `github.com X Failed to log in to github.com account eliheuer (default) - Active account: true - The token in default is invalid. - To re-authenticate, run: gh auth login -h github.com - To forget about this account, run: gh auth logout -h github.com -u eliheuer`
- Credential detail: `github.com X Failed to log in to github.com account eliheuer (default) - Active account: true - The token in default is invalid. - To re-authenticate, run: gh auth login -h github.com - To forget about this account, run: gh auth logout -h github.com -u eliheuer`

## Why This Matters

- The Google Fonts PR guide asks contributors to sign the Google CLA.
- The same guide asks contributors to configure Git commits with the
  name and email that match the signed CLA identity.
- The downstream Google Fonts commit will be made from the local
  `/Users/eli/GH/forks/fonts` checkout, so that repo's git identity is the final
  commit-identity gate.
- The local Packager dry run needs GitHub API access through `GH_TOKEN`
  or equivalent authenticated GitHub CLI credentials.
- The final downstream PR should not be opened until this identity state
  matches the confirmed CLA identity.

## Apply Before Downstream PR

- Confirm the final commit identity matches the signed Google CLA identity.
- Confirm the source repo and local `google/fonts` fork git name and
  email match the CLA identity before making release or downstream commits.
- If the signed CLA identity should be `Eli Heuer`, update the
  repo-local identities before making downstream `google/fonts` commits:

```bash
git config user.name "Eli Heuer"
git -C /Users/eli/GH/forks/fonts config user.name "Eli Heuer"
```

- Refresh GitHub CLI authentication before using `gh auth token` or
  running `make package-dry-run` with API-backed downloads.
- Alternatively, export a short-lived `GH_TOKEN` for the Packager dry
  run if you do not want to refresh stored GitHub CLI credentials.
- Rerun `make reports-only` after changing local Git or GitHub auth state.

## Local Auth Commands

These commands are intentionally local and do not open an issue, push a
branch, or create a downstream PR:

```bash
gh auth status -h github.com
gh auth login -h github.com
make github-auth-check
```

If using a short-lived token instead of stored GitHub CLI credentials,
set `GH_TOKEN` only for the command that needs it:

```bash
GH_TOKEN=<token> make github-auth-check
GH_TOKEN=<token> GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

References:

- https://googlefonts.github.io/gf-guide/making-pr.html
- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/package.html
