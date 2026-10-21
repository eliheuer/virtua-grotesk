# ARB-006 — Autonomous Arabic first pass

Eli authorized this pass on 2026-10-21 while repairing Runebender component
editing. Do not wait for per-batch feedback. Apply reversible working drawings
in the active UFOs; retain human grading for the later review. No publication
or release approval is implied.

Baseline checkpoint: `05b8d2e1`, including Beh bases, circular single dots,
scrollbar repair and the updated authorization. Before fonts and exact sources
are saved per batch; full source hashes detect concurrent editor changes.

## Current progress

- Batch 01: Bold Dal and Reh isolated/final outlines, plus five inherited
  wrapper advances. Applied; build/preflight, curve checks, 98 shaping
  comparisons and endpoint/intermediate browser proofs completed. Human
  review remains pending. See [batch evidence](batches/01-dal-reh/README.md).
- All Regular drawings, all green drawings and Eli's manual hamza are preserved.
- The full Arabic first pass is **in progress**, not complete or human-approved.

## Remaining queue

Use `inventory.py` / `inventory.json` to check exact names, source grades and
component dependencies. Recompute before each batch. A component change affects
its descendants even when their files do not change; protect green descendants.
The old `scripts/arabic_*` builders contain historical color semantics and
Bold-equals-Regular recipes. Do not run them wholesale.

1. Waw; Noon / ghunna bowls; Feh and Qaf heads/tails.
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

The thread heartbeat `virtua-arabic-first-pass` is active at 20-minute intervals
for continuation while Eli works on the editor. Keep it quiet except meaningful
milestones, completion or blockers; the queue above remains the durable handoff.
Next bounded family: inspect Waw and its component descendants before drawing.

The live proof now includes Arabic alphabet, joining forms, all-script samples
and the Working font's encoded repertoire. Fixed DesignBot detail PNGs and their
font-hash receipts live with batch 01; use the shared app/render-detail.py runner
for later batches. Preserve current before/working identity when updating proofs.
