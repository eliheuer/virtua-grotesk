# Anchor-sheet production

Load the anchor-sheet-glyphs skill and the target's from-image context packet.
The design library owns grid/colors/construction; historical LESSONS instructions
are evidence, not current procedure. Capture the exact supplied image and its role.

1. Calibrate a sheet containing a known green anchor (often n):
   `.venv/bin/python scripts/anchor_sheet.py SHEET.png n less equal greater --json out/sheet.json`.
   Names follow image order; inspect --help for spanning/anchor options. Verify the
   anchor's current source hash, baseline, scale, ink bounds and a measured stroke.
   Compare against source geometry, not a universal hardcoded width palette.
2. For line-grammar symbols use scripts/symbol_gen.py with measured axis, box,
   stroke, gaps and angles. Preserve green donor order, including components.
   Run `scripts/symbol_gen.py <names> --out out/<fresh-revision>` to emit
   standalone per-master GLIFs and context. It refuses active-source writes.
   Its historical recipes still need review/refitting against the 8-grid contract;
   they do not guarantee compliant geometry. Register output only in a scratch font.
3. For organic glyphs crop against white, without neighboring ink, and use
   img2bez masters on scratch with the calibrated fit band. See RUNBOOK-codex.md.
   Morphological emboldening is a proposal, not an approved weight-transfer rule;
   inspect counters, turns and joining forms in both masters.
4. Use the shared 8-grid draft, interpolation and curve checks; preserve intentional
   cuts and human optics. Resolve contour overlaps carefully in scratch and retain
   matching topology. Do not blindly boolean-union protected donor source files.
5. Build and inspect large/reading-size, shaped endpoint/intermediate proofs.
   New AI drawings are purple; Eli grades. Record his feedback and exact pairs
   under design/reviews and index reusable corrections under design/corrections.

No dated production queue is active here. Read design/reviews/current.json and the
user's named scope. The former runbook remains in design/migration/original-documents.
