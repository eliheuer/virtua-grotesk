# Downstream PR Readiness

This generated report turns the Google Fonts PR guide into local
preflight evidence for the eventual downstream `google/fonts` pull
request. It does not open an issue, push a branch, or write to the
local `google/fonts` checkout.

## Summary

- Google Fonts issue pending: yes
- Issue draft current: yes
- Issue labels current: yes
- Issue requirement boxes still unchecked: yes
- Expected downstream family path: `ofl/virtuagrotesk`
- Downstream family directory exists locally: yes
- Downstream METADATA.pb exists locally: yes
- Downstream METADATA.pb still starter template: yes
- Downstream metadata preview ready to apply: no
- Downstream metadata apply blockers: 3
- Expected Packager branch: `gftools_packager_ofl_virtuagrotesk`
- Current google/fonts branch: `main`
- google/fonts tracking branch: `origin/main`
- google/fonts main vs origin/main: 0 ahead, 0 behind
- google/fonts main vs upstream/main: 0 ahead, 0 behind
- google/fonts fork base ready for downstream branch: yes
- Dirty google/fonts paths inside family dir: 1
- Dirty google/fonts paths outside family dir: 0
- Current downstream family file count: 1
- Current downstream family files starter-only: yes
- Package dry run reaches Packager: no
- Package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template
- GitHub API credentials ready: no
- GitHub CLI auth status: `invalid token`
- Source repo git identity complete: yes
- Source repo git name matches CLA/author name: yes
- google/fonts fork git identity complete: yes
- google/fonts fork git name matches CLA/author name: yes
- Final downstream commit identity ready: yes
- Google CLA status: confirmed by maintainer for the copyright holder
- Public upstream URL still pending in issue draft: no
- Release tag exists locally: no
- Source tree clean for final commit/tag: no

## Expected PR Shape

- Branch name: `gftools_packager_ofl_virtuagrotesk`
- Family directory: `ofl/virtuagrotesk`
- PR title: `Virtua Grotesk : 1.000 added`
- PR body provenance line: `Taken from the upstream repo <repo-url> at commit <commit-url>.`
- Open or link the Google Fonts Add Font issue before creating the PR.
- Keep the PR scoped to this one family directory.
- Compare from the branch on the `eliheuer/fonts` fork unless a Google
  Fonts team member asks for a direct upstream branch.

## Handoff Coverage

- Handoff names expected Packager branch: yes
- Handoff includes exact downstream PR title: yes
- Handoff includes exact PR provenance body line: yes
- Handoff records issue-first rule: yes
- Handoff records one-family-directory rule: yes
- Handoff records fork comparison path: yes

## google/fonts Fork Evidence

- Fork path: `/Users/eli/GH/forks/fonts`
- Origin: `git@github.com:eliheuer/fonts.git`
- Upstream: `https://github.com/google/fonts.git`
- Tracking branch: `origin/main`
- Alignment with `origin/main`: `0 ahead, 0 behind`
- Alignment with `upstream/main`: `0 ahead, 0 behind`
- Safe to branch after removing or replacing only `ofl/virtuagrotesk`: yes

Dirty paths inside family dir:

- `?? ofl/virtuagrotesk/`

Dirty paths outside family dir:

- None

Current files inside downstream family dir:

- `ofl/virtuagrotesk/METADATA.pb`

## Apply Before Opening Downstream PR

- Open the Google Fonts Add Font issue and record its URL or number in
  the handoff before using Packager with `-p`.
- Resolve maintainer decisions, drawing/source blockers, and Fontspector
  FAILs, or document reviewer-approved exceptions in the issue.
- Confirm Google CLA status and the local `google/fonts` fork git
  identity before committing downstream package changes.
- Refresh GitHub CLI auth or export `GH_TOKEN` before the no-PR
  Packager pass.
- Replace the starter downstream `METADATA.pb` with the checked preview
  only after `make downstream-metadata-check` reports `Ready to apply: yes`.
- Review the expanded downstream family file list above before branching;
  the current starter-only state must be replaced by Packager output
  before opening the PR.
- Rerun `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` after the checked metadata
  is applied and GitHub API auth is restored.
- Review the generated package so the final PR changes only
  `ofl/virtuagrotesk` and uses the expected title/body.

## Safe Local Sequence

Use this only after final drawing/source work, release metadata, and
the Add Font issue are ready. The first Packager pass still omits `-p`
so the generated package can be reviewed before any PR update.

```bash
gh auth status -h github.com
make github-auth-check
git -C /Users/eli/GH/forks/fonts config user.name "Eli Heuer"
git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
./venv/bin/python scripts/prepare_downstream_metadata.py --apply
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Only after reviewing the no-PR package and recording the issue number
should the final Packager run use `-p -i ISSUE_NUMBER`.

References:

- https://googlefonts.github.io/gf-guide/making-pr.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/onboarding.html
