# Decision Application Blockers

This generated report maps each remaining maintainer decision or
finalization item to the exact Google Fonts packaging gate it affects.
It is intended as the handoff surface between answering decisions and
applying them to metadata, source, or downstream package files.

## Summary

- Open maintainer decisions: 2
- Decided maintainer decisions: 13
- Maintainer answer sheet unanswered prompts: 2
- Maintainer answer sheet unanswered prompt names: PUA Icon Block, Kerning Scope
- Downstream metadata pending/placeholder lines: 2
- Downstream preview pending field lines listed: 2
- Actionable pending decision markers: 0
- Package dry run reaches Packager: no
- Package dry-run first blocker: existing downstream METADATA.pb is still the Packager starter template
- GitHub API credentials ready: no
- Final GitHub release archive URL recorded: pending

## Blocker Map

| Item | Status | Downstream metadata | Package dry run | Final submission | Current blocker markers | Apply surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| Author/contact lines | decided | does not block metadata text | does not block directly | blocks until matching profile exists or request is prepared | final designer string applied; designer profile still missing | `AUTHORS.txt`; `CONTRIBUTORS.txt`; metadata preview; designer profile draft |
| Private-use icon block | open | does not block | does not block directly | blocks until included or deferred | 23 PUA codepoints; subsetting/reachability warnings | source glyphset; metadata review; Google Fonts issue rationale |
| Kerning | open | does not block | does not block directly | blocks until completed or deferred | 0 kerning warnings | UFO kerning/groups/features; build path if needed; warning triage |
| Final release/source commit | pending final source state | blocks | blocks | blocks | `Pending final` in `source.commit`; final release archive URL pending | metadata preview; release/source checklist; GitHub `v1.000` release archive |
| Final Google Fonts date_added | pending final package date | blocks | blocks | blocks until final downstream metadata date is set | `Pending final Google Fonts date_added` in metadata preview | metadata preview; downstream metadata helper; final package review |
| GitHub API credentials | local environment pending | does not block metadata text | blocks | blocks package verification | GitHub API credentials ready: no | local `gh auth` or short-lived `GH_TOKEN` before `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` |

## Current Metadata Markers

- Designer marker: absent
- Source commit marker: present
- Final date_added marker: present
- Designer profile final metadata strings present: yes
- Designer profile missing catalog profiles: 1

## Maintainer Answer Sheet State

This section mirrors `documentation/google-fonts-decision-answer-sheet.md`
so an open decision cannot lose its maintainer-facing answer prompt
without the application blocker report noticing.

| Prompt | Answer still TBD | Blocks final submission |
| --- | --- | --- |
| PUA Icon Block | yes | yes |
| Kerning Scope | yes | yes |

## Apply Order

1. Prepare or request the matching designer profile for the final
   `Eli Heuer` metadata designer string.
2. Decide whether PUA glyphs ship or are deferred, then update the issue
   rationale and any source glyph cleanup plan.
3. Decide whether kerning is required before the first PR or explicitly
   deferred in the submission notes.
4. After drawing/source work is complete, create the final public source
   commit, tag `v1.000`, and GitHub release archive.
5. Replace the pending downstream `date_added` value with the final
   Google Fonts package date.
6. Restore GitHub API credentials, run `make downstream-metadata-check`,
   apply the checked preview, then run the no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
