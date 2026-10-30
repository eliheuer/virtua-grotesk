# Design context migration handoff — 2026-10-29

For **Fix Google Fonts QA issues** (`01a14c57-7273-7c22-9cf8-01907fb0cf87`).
The migration is complete in the shared working directory. Eli confirmed that
chat had stopped editing. No font drawings were changed by this migration.
Changes are local and uncommitted; do not reset or restore the old tree layout.

## Read this before resuming

Read the new [AGENTS.md](../../AGENTS.md), [design workflow](../../design/README.md)
and [current state](../../design/reviews/current.json). Existing chat context about
where to find rules/feedback is stale. The latest user scope and unresolved human
choices still govern work; the migration does not restart timed drawing queues.

- Active isolated Seen is **v3**, still optically unresolved. **v4 was rejected and
  never applied.** Its continuous underside/diagonal sweep lost Virtua articulation.
  Inspect the green Regular `seen-ar.init` and `seen-ar.medi` construction before
  another proposal. The current proof compares active v3 with rejected v4.
- Bold initial S-like Kaf was approved/applied in its exact named scope. Green
  Regular Kaf remains protected. The medial candidate is not approved.
- Final Yeh's raised return is intentional; the rejected replacement stays rejected.
- The applied at r4 was “better, but still bad,” intended for hand editing. Applied
  does not mean visually approved, green or positive training evidence.
- Preserve OPEN Latin decisions in [the worklog](../../design/reviews/latin-worklog.md).

The two Seen source GLIF modifications that existed before migration remain
untouched. Exact source hashes associated with the active review are recorded in
current.json; `make design-status` reports whether those claims still match disk.

## First workflow trial

Start with a read-only retrieval trial, then continue drawing only under the
user's applicable named scope. Do not resume an old autonomous queue.

```sh
make design-status
make design-check
make design-context GLYPH=seen-ar OPERATION=curve-repair
.venv/bin/python scripts/design_context.py --glyph seen-ar --master both \
  --operation curve-repair --json --output out/seen-context.json
.venv/bin/python scripts/design_context.py --verify out/seen-context.json
make proof-web
```

The packet should include Seen intent, rejected v4, the earlier Seen splice
lesson, live green joining-form sources, and the Zayin/hamza turn counterexample.
Read the exact linked GLIFs and rendered evidence; metadata is not a visual proof.
Inspect broad articulation, local junctions and paired edges before proposing
coordinates. Note any missing context as a retrieval defect and add a scoped route.

For an authorized edit: preserve exact before bytes, make a bounded candidate,
run the relevant grid/curve/compatibility/build/shaping checks, inspect the actual
large and reading-size proof, then show the focused result promptly. Recheck the
JSON source guards immediately before active application. If they changed, inspect
and reconcile the changed source; do not merely refresh the recorded hashes.

Record feedback in the current case before the next edit. Create a scoped correction
record with immutable evidence, exact before/after hashes and separate application,
visual verdict and training-eligibility fields. Reuse authorization already given
for the exact scope; this handoff itself grants no new source-editing scope.

## Where things moved

| Old place | Current owner |
| --- | --- |
| agent-proofs/cases | design/reviews; compatibility symlink retained |
| agent-proofs/README.md | design/README.md for design work; old path now proof-app entry |
| agent-proofs/FEEDBACK.md | design/corrections/records plus current review; full history retained |
| DESIGN.md monolith | design/system, constructions, writing-systems, glyphs; DESIGN.md routes |
| anchor-sheet LESSONS.md | 20 scoped historical correction records and frozen excerpts |
| documentation/design-pass-worklog.md | design/reviews/latin-worklog.md; redirect retained |
| source-guides/design-philosophy.md | historical text under design/system; redirect retained |

The library contains 21 topic routes and 32 correction records. Corrections point
to exact source/proof evidence in the original case packets. Feedback from mutable
READMEs is frozen separately under design/corrections/evidence; source_path records
its original context. Existing receipts retain their original paths and hashes.
See [legacy paths](../../design/migration/legacy-paths.json).

The live app stays in agent-proofs/app. Its guide is now operational; the previous
UI planning history is preserved separately. The displayed v4 proof was copied
from ignored out into the case for restart/checkout recovery. Local reference
fonts remain under reference-fonts. The existing layout/CSS/JS were preserved.

## Command changes

- `make design-context GLYPH=... MASTER=both OPERATION=...`, `make design-check`,
  `make design-status`; repeat --glyph with the Python command for a bounded set.
- `report_master_compatibility.py --check` now fails on blocking differences;
  report-only invocation remains compatible.
- `make glyph-ai-prepare` requires `FIT=<calibrated-bottom:top>`. The harness
  prepares both masters, rejects non-green references, saves context guards and
  uses img2bez masters. Legacy packets/existing trace output are refused. This
  migration did not execute image generation or a real glyph trace.
- `symbol_gen.py <names> --out out/<fresh-revision>` emits standalone purple GLIFs
  and context. It no longer writes active sources or defaults to generating all
  symbols. Historical recipes need review/refitting to the current 8-grid contract;
  numerical compliance is not guaranteed. Register only into scratch before review.
- New proof snapshots default to Candidate. Current-state status/note/label is
  overlaid only on its exact selected snapshot; frozen evidence is not rewritten.

## Verification and remaining QA

Completed locally:

- All **3,134 source files** and **9,244 original review artifacts** preserved byte
  for byte against the pre-migration manifest. All 9,206 previously tracked case
  files remain visible to Git at their new paths. No font build/source edits made.
- **14** context/harness/protection regression tests pass; **11** proof Python
  tests and the JS reference-selection test pass. Updated skills validate.
- Design catalog/related ids/pair hashes/portable proof validate. Maintained topic
  links and `git diff --check` pass. Source compatibility has **0 blocking mismatches**.
- Browser inspection confirmed all six font columns, retained layout and the
  **Seen v4 · Rejected · Not applied** label in heading/footer. Proof server is at
  http://127.0.0.1:60272/. Screenshot and local logs are under out/design-transition.
- The broader repository suite ran 67 tests at that point and reported **216 failing
  subcases in two existing binary tests**: 105 cantillation clearance and 111 meteg/
  nun-dot cases. They run against existing compiled fonts. Their test code, input
  sources and binaries were not modified here. Other tests in that run passed.
  This is not a release-readiness pass. Rebuild and investigate in the QA workflow
  under the user's existing scope; do not alter drawings just to clear the count.

Local recovery evidence: out/design-transition/baseline.json and
before-context.tar.gz; hashes cover the moved evidence. Git retains older versions.
No commit, push, public publication or model training was performed. The companion
font-garden-lab extraction/training code is outside this migration and unvalidated.
