# Verify the proposed change

Use a bounded source scope and preserve exact before/candidate files. First inspect
filled silhouettes against relevant green Virtua construction. Check new geometry
on 8, preserve inherited human exceptions, and verify master correspondence.
For curves, use `scripts/curve_lint.py <Master> <glyphs> --joins` and the signed
`curve_profile.py` comparison; pair opposing edges when apparent weight is at issue.

Build the candidate with the repository build pipeline. Check compiled shaping,
advances and affected components; inspect endpoints 400/700 and intermediate weights.
Use `agent-proofs/app/prepare.py` and `make proof-web` for the live comparison.
The proof renders actual verified fonts. Retain an explicit Candidate, Applied or
Rejected label and the exact font hashes. `make review` is a separate Diffenator
report, and `make proof` is the print PDF.

For Arabic batches retain and inspect fixed 400/700 details with the recorded
references using `agent-proofs/app/render-detail.py`. Show the focused comparison
promptly; broader reports can follow an accepted group or an explicit QA request.
Follow `documentation/qa.md` for required build/preflight and release checks.

Describe observed shape faults honestly. A candidate with a visible swollen join,
wrong construction, accidental notch or pinched counter stays unresolved even when
numerical checks pass. Human grading remains Eli's decision.
