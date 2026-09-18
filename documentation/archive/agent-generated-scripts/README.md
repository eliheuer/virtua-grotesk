# Retired automation

The old report, review-packet, donor-copy, and packaging scripts were removed
because they are not used by the active workflow. Their last pre-cleanup tree
is commit `f9edce3221d79114859374df2edf63f939f96185`; recover individual files
from Git if needed. Review their assumptions before using them again.

Historical reports and human review records remain in
`../agent-generated-reports/`. Current commands are documented in
`../../core-qa-process.md` and the root Makefile.
