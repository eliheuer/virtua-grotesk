# Batch 13 — Bold Ain/Ghain medial

Applied working drafts under the autonomous Arabic authorization. Baseline
`2db1d06d`. Human review is pending; final and isolated forms remain unfinished.

## Scope and construction

Only Bold `ain-ar.medi` and `ghain-ar.medi` changed. Both are purple awaiting
human review. All Regular source bytes, the 18 recursively reserved Beh sources,
manual hamza and unrelated drawings remain unchanged. Green Regular medial Ain
is preserved. Exact before/candidate bytes and source hashes are retained.

The existing 26-point outer and 17-point counter structures remain compatible.
Bold joins increase from 104 to 176 units; the crown is 160 units thick. Advance
and right drawing edge now agree at 704 (the old 644 advance left a 36-unit
joining gap). The head has a flat crown from x256 to448 at y512. The counter
opens to y352 and ends at y184 with a small 8-unit cut, replacing the old Bold
duplicate tip. Diagonal strokes are not claimed to be uniformly 160 units.
Exposed connector corners have 16-unit chamfers; the two head-to-bar transitions
retain small deliberate cut/landing details. All new outline coordinates and
advance are multiples of eight.

Ghain follows the 704 advance; its existing dot moves locally to offset
(200,-64), centered at x352 with 80 units of clearance above the head. The shared
donor and stored anchors are unchanged. Above-mark shaping consequently follows
the existing donor anchor with the declared component offset.

## Inspection and verification

- `ain-400/550/700.png` and `ghain-400/550/700.png` inspected with Rubik,
  Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro. Plex at 550 is explicitly
  labeled nearest supplied static weight 500. The intermediate counter remains
  open; the medial has a more coherent weight beside the repaired initial.
- `medial-large.png` inspected for counter shape, curves and cuts.
  `joins-700.png` shows marked joined contexts with no new visible joining break
  or mark collision in these samples. Beh is rendered, never modified.
- The first counter draft had two unintended curvature reversals. Its GLIF,
  comb and diagnostic are preserved as `counter-v1.*`; `refine.py` removes those
  reversals before the final font build. Current sampled curves have no sign
  reversals or tangent kinks. Remaining curvature jumps are explicit: about 43%
  at the outer vertical turns and 50% at the small inner turns. Deliberate
  corners remain corners. This is not an all-G2 claim.
- `quality-check.py` and `interpolation-check.py` find no sampled contour
  crossings at 400, 475, 550, 625 and 700. Sampling is not exact certification.
- `verify.py`: 413 shaping comparisons at seven weights. Substitutions/clusters
  remain stable; only declared width and interpolated Ghain placement deltas
  occur. Compiled changes are confined to these two medial glyphs.
- Nine grid findings are preserved inherited anchor coordinates, including
  donor anchors. No new outline, advance or component offset is off the 8 grid.
- `make preflight` completed build, print proof, reports and artifact checks.
  Zero blocking master mismatches; 510 width-only differences. The preflight
  rebuild differs from the raster snapshot only in head timestamp/checksum;
  `preflight.json` binds both identities. No release-readiness claim.

## Next

Bold final Ain/Ghain still have an underweight, pinched loop; isolated Bold has
an unfinished head. Repair final next, then isolated, preserving green Regular
medial/final sources. Regular Ghain initial still has the recorded 468-versus-496
advance mismatch for a later wrapper pass. Keep Beh and its donors reserved.
Do not rerun historical apply scripts over newer editor saves.
