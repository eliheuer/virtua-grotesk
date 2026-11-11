# Verify the proposed change

Use a bounded source scope and preserve exact before/candidate files. First inspect
filled silhouettes against relevant green Virtua construction. Check new geometry
on 8, preserve inherited human exceptions, and verify master correspondence.
For curves, use `scripts/curve_lint.py <Master> <glyphs> --joins` and the signed
`curve_profile.py` comparison; pair opposing edges when apparent weight is at issue.

Build the candidate with the repository build pipeline. Check compiled shaping,
advances and affected components; inspect endpoints 400/700 and intermediate weights.
Use `make proof-web` to compare the current build with `reference-fonts/`. For a
Before/Candidate comparison, prepare a snapshot with `scripts/proof-web/app/prepare.py`
and serve it with `scripts/proof-web/serve.py --snapshot`. The proof renders actual
verified fonts. `make review` is a separate Diffenator
report, and `make proof` is the print PDF.

For Arabic batches retain and inspect fixed 400/700 details with the recorded
references using `scripts/proof-web/app/render-detail.py`. Show the focused comparison
promptly; broader reports can follow an accepted group or an explicit QA request.
Follow `documentation/qa.md` for required build and release checks.

Describe observed shape faults honestly. A candidate with a visible swollen join,
wrong construction, accidental notch or pinched counter stays unresolved even when
numerical checks pass. Human grading remains Eli's decision.
