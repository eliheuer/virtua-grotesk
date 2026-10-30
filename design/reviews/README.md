# Design reviews

Current state lives in [current.json](current.json). Read it with `make design-status`.
It identifies the current case, displayed proof and unresolved work. It is not an
automatic queue. Dated case instructions do not override current user decisions.

Review directories retain original source snapshots, proofs, user feedback and
hash receipts. `history/` preserves the previous central guide and feedback log.
[Latin worklog](latin-worklog.md) retains OPEN decisions. Reusable correction
metadata is owned by [../corrections/](../corrections/README.md).

For each bounded revision preserve the baseline and candidate source bytes, built
fonts, proof selection, checks, actual visual findings and human verdict. Keep
application and approval separate. Update current.json after selecting the next
review. The proof app reads `proof_snapshot` and applies its `proof_label` only to
that exact selected snapshot. An explicitly selected different snapshot retains
its own recorded labels.

Use repository-relative paths in new records. Historical receipts keep their
original paths and hashes; [legacy-paths.json](../migration/legacy-paths.json)
and the `agent-proofs/cases` compatibility link resolve the move. Do not rewrite
old receipts as if they had been created under the new layout.
