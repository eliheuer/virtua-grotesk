# ARB-004 — Fathatan and Hamza with Fathatan

2026-10-21: Eli requested a Git checkpoint of his hamza correction and the
curve lessons, then the next small Arabic loop with all four references.
Checkpoint: `d23f1bed`. Scope: `fathatan-ar` (U+064B) and `hamzaaboveFathatan-ar` component placement in
Regular and Bold, under the standing active-source authorization. Preserve
all donor outlines, including the saved human Bold hamza, and all other glyphs.

The helper contains hamza plus two Fatha components. Regular's Fatha offsets
254/184 crowd the hamza and leave the strokes overlapping. Bold's 214/−818
places one stroke through the hamza and the other far below it. Repair those
four translations in the helper, plus the encoded Fathatan pair below; no
curve edits or automatic grades are part of this loop.

Trial: Regular upper/lower Fatha offsets 464/352; Bold 608/432. These are on 8.
Minimum bounding-box clearance from hamza to the lower stroke is 32 Regular,
48 Bold. Stroke separation is measured against the sloping outlines (not their
overlapping bounding boxes): minimum vertical gap 40 Regular, 46 Bold.
The original components and existing donor drawings are reused, with matching
component order in both masters. This is a placement trial, not approval of
the inherited Fatha drawing quality or a universal mark-stacking recipe.

Use the new signed curve profile on the preserved hamza donors; do not
harmonize or balance them to improve a score. Decompose the helper only on
scratch for geometry inspection. Verify the three pieces stay separate at
intermediate weights and compare compiled sequences in both combining orders.
Keep Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro.

The first helper-only trial was retained in `trials/helper-only/`. Compiled
shaping showed that ordinary أً uses precomposed Alef/Hamza plus standalone
Fathatan, rather than the helper; therefore a helper-only fix would not repair
the displayed problem. Scope was explicitly extended in commentary within the
same Fathatan loop. `extend-fathatan.py` records that bounded application.

Encoded Fathatan reuses the same two Fatha components with upper/lower offsets
112/0 Regular and 176/0 Bold. Its `_top` attachment stays unchanged. `bottom`
now follows ink bottom (704/664) and `top` is 48 above ink (1000/1104).
This restores separated parallel strokes in both encoded and helper forms.
Existing source labels are preserved: this is a translation/anchor repair,
not a newly drawn outline or a human grade.

Known separate issues: Hamza/Dammatan remains malformed; Fatha's Bold root
drawing and Regular hamza still require their own review. This is not a repair
of all tanwin or a claim of Arabic readiness.

## Verification and proof

- `make preflight` passed (build, PDF, source reports and artifact presence).
- `verify.py`: 175 shaped comparisons across seven weights. Only U+064B and
  the Hamza/Fathatan helper have different compiled outlines; every advance
  and all tested substitutions/clusters remain unchanged. Other sampled
  mark contexts retain their positioning. Compiled Fathatan has two contours
  and the helper three at all checked weights, rather than merged strokes.
- `geometry.py`: three helper pieces remain separate at 13 sampled weights.
  The same upper/lower separation applies to standalone Fathatan. Minimum
  sampled outline clearance across pairs is about 38.46 units. This sampled
  measurement is distinct from the vertical-gap construction numbers above.
- New curve tooling: `hamza-curve-profile.json` and `hamza-curve-comb.svg`
  record the unchanged donor curves. No sampled sign reversals; existing
  continuity differences remain recorded. No bulk harmonization or donor
  edits were performed to improve diagnostic scores.
- Exact source hashes verify only four GLIFs changed. Hamza and Fatha donor
  hashes remain identical, including Eli's human Bold correction.
- Live proof: `working/`, **Before / Working** with Rubik, Noto Sans Arabic,
  IBM Plex Sans Arabic and Readex Pro. Regular and Bold carrier screenshots
  are saved as `regular-carriers.png` and `bold-carriers.png`. The explicit
  helper sequence is retained in `bold-helper.png`. Existing hamza/dot crowding
  on Teh remains visible and belongs to a separate base/mark attachment loop.

Status: Eli accepted the applied Regular/Bold placement repair on 2026-10-21:
“ok looks good, ship it.” Preserve the Before / Working proof as review evidence;
no automatic grade, release-readiness claim or unattended batch.

Eli also changed the work order: finish Arabic base forms before further
diacritics. Base drawings must stabilize before spending more time on dependent
mark placement. The mark issues above are deferred. Continue small interactive
base-form loops in both masters, with all four reference fonts.
