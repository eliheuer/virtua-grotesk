# ARB-006 — Autonomous Arabic first pass

Eli authorized this pass on 2026-10-21 while repairing Runebender component
editing. Do not wait for per-batch feedback. Apply reversible working drawings
in the active UFOs; retain human grading for the later review. No publication
or release approval is implied.

Baseline checkpoint: `05b8d2e1`, including Beh bases, circular single dots,
scrollbar repair and the updated authorization. Before fonts and exact sources
are saved per batch; full source hashes detect concurrent editor changes.

## Quality hold — 2026-10-21

Eli rejected the latest 700 proof as lumpy/broken. The agent paused the recurring
run to diagnose the failed visual gate. Repair and re-evaluate the current
Feh/Qaf proof before continuing the queue; batch 04 is not a successful visual
checkpoint. See its human-rejection record. No font sources were changed during
this diagnosis. Standing drawing authorization remains; the pause is a quality
hold, not a user withdrawal of authorization.

## Concurrent human editing — 2026-10-21

Eli has finished the component-editor repair and is manually editing `ببب ب`.
Reserve the Beh isolated/initial/medial/final forms in both masters and their
recursive component donors, including shared dots. Do not modify their geometry,
metrics, anchors, placements or grades. Recompute dependencies before other
batches and exclude any shared donor that could change this human work.

## Current progress

- Batch 01: Bold Dal and Reh isolated/final outlines, plus five inherited
  wrapper advances. Applied; build/preflight, curve checks, 98 shaping
  comparisons and endpoint/intermediate browser proofs completed. Human
  review remains pending. See [batch evidence](batches/01-dal-reh/README.md).
- Batch 02: Bold Waw isolated/final and two inherited wrapper advances applied.
  Both endpoint raster sheets inspected; build/preflight and 133 shaping checks
  passed. See [Waw evidence](batches/02-waw/README.md).
- Batch 03: Bold Noon / ghunna shared bowls and two wrapper advances applied.
  Raster inspection exposed and resolved the final dot/stem collision. Both
  endpoint sheets inspected; build/preflight and 161 shaping checks passed.
  See [Noon evidence](batches/03-noon/README.md).
- Batch 04: Bold initial/medial Feh–Qaf shared heads and 14 wrapper advances
  applied. Four endpoint raster sheets, two source-scale renders and the 550
  browser proof inspected; build/preflight and 217 shaping checks passed.
  See [shared-head evidence](batches/04-feh-qaf-heads/README.md).
- Batch 05: repaired the full Bold Feh/Qaf family and circular two/three-dot
  donors. 308 shaping comparisons, scoped regression checks and preflight pass.
  Final visual review remains incomplete at the requested Git checkpoint.
  See [repair evidence](batches/05-feh-qaf-repair/README.md).
- All Regular drawings, all green drawings and Eli's manual hamza are preserved.
- The full Arabic first pass is **in progress**, not complete or human-approved.

## Remaining queue

Use `inventory.py` / `inventory.json` to check exact names, source grades and
component dependencies. Recompute before each batch. A component change affects
its descendants even when their files do not change; protect green descendants.
The old `scripts/arabic_*` builders contain historical color semantics and
Bold-equals-Regular recipes. Do not run them wholesale.

1. Complete final visual review of batch 05 Feh/Qaf repair, including 550.
   Keep the recurring run paused until the repair review is resolved.
2. Meem, Lam and Lam–Alef; keep joining bar heights consistent.
3. Hah/Jeem/Khah and Ain/Ghain: head, counter and descender construction.
4. Seen/Sheen, Sad/Dad and Tah/Zah: teeth and loop families.
5. Kaf/Keheh/Gaf and Heh/Goal/Doachashmee, Yeh/Maksura/Barree variants.
6. Reconcile duplicated Beh-family outlines (Teh/Peh/Tteh/Yeh extensions)
   with the shared roots; inspect separately drawn Dal/Reh variants too.
7. Dot groups and wrapper placements after base silhouettes stabilize.
8. Diacritics, composite attachment, stacking and spacing; Arabic/Farsi digits,
   punctuation and remaining signs. Keep script uncertainties explicit.
9. Whole-script proof and technical QA, then hand back for human edits/grading.

Inspect both masters, but green Regular shapes are fixed construction evidence.
Orange/yellow shapes may be refined without replacing their design. Do not
invent a grade for uncolored glyphs. Preserve the saved manual Bold hamza and
all Hebrew corrections. Newly redrawn outlines use purple, never green.

## Batch contract

Name targets, preserve before state, prepare exact compatible outlines, profile
curves/joins, inspect large renders, and apply only after source hash checks.
Use the 8-unit machine grid and 16-unit exposed / 8-unit small chamfers; do not
snap protected optical coordinates or force equal handles. Existing anchors
are recorded exceptions until the placement phase, not silently repaired.

Build, inspect compiled endpoint/intermediate proofs with Rubik, Noto Sans Arabic,
IBM Plex Sans Arabic and Readex Pro. Use joined-plus-isolated forms such as
`ببب ب`, and right-joining contexts such as `بد د بر ر`. Verify substitutions,
clusters, metrics changes and component closure. Run preflight and preserve
its scope: passing does not mean release-ready or visually approved.

Update this progress section and each batch record at every checkpoint. Commit
only owned paths. If a human source edit arrives, preserve it and refresh the
baseline for the affected family; independent families may continue. Stop only
for a genuine unresolved dependency/decision, not routine application approval.

## Continuation and proof tools

The thread heartbeat `virtua-arabic-first-pass` is paused for the quality hold;
its configured recurrence is 20 minutes
for continuation while Eli works on the editor. Keep it quiet except meaningful
milestones, completion or blockers; the queue above remains the durable handoff.
Next action: finish batch 05 visual review; Beh and its component donors are
reserved for Eli.
Preserve green Regular initial/medial Feh bases. Regular Noon final dot is low
and remains a recorded follow-up for the placement pass.

The live proof now includes Arabic alphabet, joining forms, all-script samples
and the Working font's encoded repertoire. Fixed DesignBot detail PNGs and their
font-hash receipts live with batch 01; use the shared app/render-detail.py runner
for later batches. Preserve current before/working identity when updating proofs.
