# Contour Cleanup Decision Log

This file preserves manual review decisions for the remaining contour-count
findings. `make contour-cleanup-proof` regenerates the queue while keeping
the editable Status, Decision, Notes, and Reviewed cells for matching
source glyph names.

Use Status values such as `pending`, `fix-now`, `fixed`, `accepted`, or
`deferred`. Only mark a warning accepted when the drawing decision is
intentional and reviewable.

Use `make contour-decision-update GLYPH=<source> STATUS=<status>
DECISION="<short decision>"` to update one row without hand-editing
the wide table.

- Unique review items: 4
- Pending: 4
- Fix-now: 0
- Fixed: 0
- Accepted: 0
- Deferred: 0

| Source glyph | Fontspector glyph | Batch | Category | Command | Status | Decision | Notes | Reviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dad-ar.init` | `uni0636.init` | 1. Component-only source forms | source outline review | `/edit-glyph dad-ar.init --master both` | pending | pending |  |  |
| `hah-ar.fina` | `uni062D.fina` | 6. Source-outline judgment calls | source outline review | `/edit-glyph hah-ar.fina --master both` | pending | pending |  |  |
| `jeem-ar.fina` | `uni062C.fina` | 6. Source-outline judgment calls | source outline review | `/edit-glyph jeem-ar.fina --master both` | pending | pending |  |  |
| `sad-ar.init` | `uni0635.init` | 6. Source-outline judgment calls | source outline review | `/edit-glyph sad-ar.init --master both` | pending | pending |  |  |
