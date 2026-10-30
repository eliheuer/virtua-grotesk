# Batch 01 — Bold Dal and Reh

Baseline: `05b8d2e1`. Applied working trial, awaiting later human review.

Changed Bold `dal-ar`, `dal-ar.fina`, `reh-ar`, `reh-ar.fina` outlines. Removed
inflated inner turns, established weight gain in the formerly Regular-like Dal
final, and retained compact grid/chamfer construction. Updated five inherited
wrapper advances (`thal-ar`, `jeh-ar`, `rreh-ar`, `zain-ar`, `zain-ar.fina`) to
match their bases. No component offsets or anchors changed. All Regular source
bytes and Eli's manual Bold hamza remain unchanged. Four redrawn outlines are
purple, not human-approved green.

`prepare.py` preserves exact before files and candidate files and guards apply
with all-source hashes. `applied.json` records the receipt. `verify.py` and
`verification.json` cover the nine changed files, compatible point structures,
component closure and 98 compiled shaping comparisons at seven weights. Font
compilation may round compatible curves differently even at the unchanged
Regular endpoint; source identity and compiled effects are recorded separately.

Build and preflight passed. Curve lint and combs are retained; deliberate Dal
final notch corners are not forced smooth. Grid exceptions are existing anchor
coordinates, not new outline points. Browser proofs inspected 400, 550 and 700
with Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro. Script quality
and the small Dal final counter still need human review. These technical checks
do not establish release readiness.

`detail-400.png` / `detail-700.png` are fixed 1600×1120 DesignBot comparisons;
their JSON files identify exact inputs, recipe and output hashes. The live UI
adds whole-alphabet and all-script overviews; its missing-coverage notices avoid
substituting a system font for an unsupported reference script.
