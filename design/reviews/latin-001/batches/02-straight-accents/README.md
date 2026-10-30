# LAT-001 batch02 · Acute/grave and macron weight

Applied under Eli's renewed independent Latin authorization. These are drafts
for manual review, not green approvals. Exactly four GLIFs change: Bold acute
and grave, and macron in both masters. All Arabic sources and their recursive
donors, all green drawings, all other source bytes, anchors and advances stay
unchanged. `dependencies.json` records the complete reverse closures:13 Regular
and61 Bold consumers including the macron-below combining form. No protected
consumer occurs in either closure. Check current source hashes before replay.

## Drawing

The Bold acute/grave previously had essentially Regular ink. New ten-point
polygons retain their slant and clipped-terminal construction, using parallel
long edges,16-unit end cuts and a192-unit height (y640–832). The pair is mirrored
about the retained attachment x164; their bounds are48–288 and40–280. The old
Regular drawings and their yellow grades are preserved. Their taper and offset
are not silently normalized; this remains an optical review item.

Macron changes from the same48-unit rectangle in both weights to a64-unit Regular
and96-unit Bold bar, with16-unit clipped corners and eight compatible points.
Regular bounds48,672–312,736; Bold32,656–328,752. Advances360 and all attachment
anchors remain unchanged. These mark dimensions are a local trial, not a new
universal stem rule. Green H/n geometry supplied the weight context: H verticals
100/192 and n main stems96/184; the accents intentionally carry less mass than
full stems. New outline points are all on8; retained metric/anchor exceptions
and unchanged Regular acute/grave geometry account for the40 grid findings.
New drawings are purple pending human review; no consumer grades are changed.

## Whole-image review

Inspected complete attachment rows and reading text at400/550/700, detail700,
and below-mark/stacked rows at400/700. The stronger Bold slants and macron read
with the letters instead of looking like Regular marks placed over Bold text.
The macron has visible thickness throughout interpolation. There are no observed
collisions in these samples, including double macrons and acute above macron.
Before/Working/Rubik are independent shaped font contexts at equal em size.
Rubik lacks U+0331; the below-mark panel is explicitly unavailable, never fallback.

The same reading rows still show underweight circumflex/caron, a small square
ring, and unusual alternate-caron construction in žluťoučký. Those are unresolved,
not approved by this batch. Existing Regular grave alignment and precomposed
spacing also remain later optical/metrics work. No source curves were changed;
these four contours are polygons. Raster inspection, not the diagnostics below,
is the basis for keeping this bounded weight repair.

## Verification

- Full source master compatibility, exact non-target byte preservation, unchanged
  anchors/advances and 8-grid new points.
- Winding/nondegenerate edges/no crossing straight segments at five weights.
-80 shaped-context checks at400/475/550/625/700: identical glyph sequence and
  positions, clear upper stacks and below marks, exact Arabic/Hebrew samples.
- Compiled ink changes restricted to the declared reverse consumer closure.
- Three Latin regression tests pass over the VF and four statics.
- Existing engineering suite retains exactly216 baseline failing subcases,
  with zero new or resolved failures. This is not a passing full suite.
- Active build and preflight results and final font identity are recorded with
  this batch. Preflight is an artifact check, not Google Fonts acceptance.

`baseline.json`, exact before/candidate XML, frozen baseline fonts, shaped rasters
and their receipts retain this trial. `prepare.py` only replays against the frozen
source hashes; `apply.py` refuses editor changes. Baseline fonts are test evidence,
not release files. This batch is a local checkpoint; pushing later Latin work
still awaits Eli's response to the outstanding push-authorization question.

Next: Bold circumflex/caron, then ring/breve/tilde and bottom marks. Preserve the
shared dotaccentcomb reversed-Nun calibration from the first LAT-001 batch.
