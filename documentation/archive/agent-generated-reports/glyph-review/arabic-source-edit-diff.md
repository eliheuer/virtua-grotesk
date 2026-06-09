# Arabic Source Edit Diff

This generated report checks current worktree GLIF edits in the
active Regular and Bold source UFOs. Use it during hand drawing to
catch one-sided Arabic edits before relying on interpolation or
running the full after-drawing check.

## Summary

- Changed active source GLIF files: 0
- Changed Arabic-like GLIF names: 0
- Arabic-like Regular/Bold pairing gaps: 0
- Ready for paired-master review: yes

No Arabic-like source GLIF edits are currently visible in git status.

## Use

- If a row is `one-sided`, inspect whether the same structural edit
  is needed in the other master before continuing.
- This check does not replace `make arabic-after-drawing-check`; it is
  a fast git-status guard for the middle of a drawing session.
