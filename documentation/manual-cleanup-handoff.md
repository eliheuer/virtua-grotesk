# Manual Cleanup Handoff

This is the pause point for finishing drawing/source work and hand cleanup
before the final Google Fonts package pass.

## Current State

- Local preflight passes with only documented drawing/source blockers remaining.
- Reusable Google Fonts onboarding knowledge has been captured in `.agents/`.
- The generated Add Font issue draft, downstream package preview, release
  archive plan, Packager dry-run gates, and downstream PR readiness reports are
  in place.
- The local `google/fonts` fork is synced and dirty only inside
  `ofl/virtuagrotesk`, where the current starter-only `METADATA.pb` remains
  quarantined until final metadata can be applied.

## Finish By Hand

Use `documentation/next-actions.md` as the main queue. The drawing/source
cleanup pass should focus on:

1. GF Latin Core coverage.
2. GF Arabic Core coverage.
3. Arabic marks, dotted circle, anchors, and mark/mkmk if Arabic remains in
   first-submission scope.
4. Source contour/no-contour findings.
5. PUA/reachability cleanup or an explicit keep/defer decision.
6. Kerning completion or explicit first-submission deferral.
7. Human review of the `gftools qa --proof` output.

## Resume Commands

After drawing/source edits:

```bash
make preflight
make next-actions
make blockers
```

After final values exist and the tree is ready for packaging:

```bash
make release-archive-build
make release-draft-check
make downstream-metadata-check
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Do not use Packager PR mode until the no-PR package has been reviewed and the
Google Fonts Add Font issue exists.

## Remaining Non-Drawing Inputs

- Decide PUA icon block scope.
- Decide kerning scope.
- Finalize release/source commit, tag, and `date_added`.
- Restore GitHub API auth.
- Provide the designer-profile square image or a profile-request plan.
- Apply checked downstream metadata only after final values are present.

