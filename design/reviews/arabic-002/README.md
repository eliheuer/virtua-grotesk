# ARB-002 — Bold Alef with Hamza Above

Eli accepted the expanded four-reference proof and requested the next small
interactive Arabic loop on 2026-10-21. Keep Rubik, Noto Sans Arabic, IBM Plex
Sans Arabic and Readex Pro. No unattended run starts here. That response approves
continuation and the reference setup; it does not assign human glyph grades.

Scope: U+0623, **Bold `alefHamzaabove-ar` and `alefHamzaabove-ar.fina` only**.
Both are red. Preserve every Regular file and all component donor outlines.
Starting snapshot is ARB-001's working font, including its Bold Alef trial.

The isolated composite still has advance 224 against its base's 296; the final
composite has advance 256 against its base's 336, putting the joining edge 80
units past the advance. Both hamza components are still at x=0, while the current
base top anchors are 152/160 and the mark's attachment anchor is 112.

Trial: inherit the base advances 296/336; use hamza x offsets 40/48 so its `_top`
meets the base's `top`. Keep y=0, preserving the existing vertical gap. This is a
component/spacing repair, not a hamza outline redesign. The existing Bold hamza
has irregular curves and stretched corners; those remain visible and need a
separate drawing loop. Its inherited off-grid geometry is not a new compliant
draft. All new widths and offsets are on 8. Preserve before/candidate files and
compiled shaping evidence. Purple marks these AI-edited composites as awaiting
human review; no green promotion.

## Result and verification

Installed the two Bold composites in the active UFO, with exact before/candidate
files and hashes in `applied.json`. No other source bytes changed in this loop.
All Regular compiled outlines and advances are identical to the preceding
working font at weight 400. Component order remains compatible across masters.

- `make preflight`: passed (build, PDF, source/compatibility reports, presence).
- `verify.py`: 126 before/working shaping contexts across seven weights; no
  missing glyphs, unchanged substitution sequences/clusters. Compiled changes
  are confined to the two Alef-with-Hamza forms and the dependent final Lam-Alef
  with Hamza ligature. At Bold, isolated/final advances are 296/336.
- Diffenator3 proof generated at `out/review/diff3proof.html`.
- Full selected-glyph grid gate: **not clean**, 113 inherited findings across
  four glyph-masters. `grid-delta.json` shows 49/48 Bold findings before and
  after, with no new failure fields. Donor contours and Regular optical
  coordinates were not normalized. New advance/offset values all divide by 8.
- Browser inspected at Bold: isolated/final forms and joined contexts, beside
  all four references. Evidence: `compare-bold.jpg`, `joining-bold.jpg`.
  Hamza alignment improves and the exaggerated joining overlap is reduced.
  **Existing Bold hamza counter is collapsed** and its outline reads as a blob
  in both Before and Working. This spacing repair does not make that drawing
  acceptable. Next interactive loop should repair `hamzaabove-ar` itself,
  with its affected composites/mark combinations included in proof scope.

No human grade or release approval was inferred. Keep this trial available for
Eli's corrections; maintain the four-reference setup and interactive cadence.
