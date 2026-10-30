# LAT-001 batch27 · Short stroke overlay and variable layout build

Adds U+0335 SHORT STROKE OVERLAY in Regular/Bold, plus an unencoded narrow
variant. This is an overstruck diacritic, not a new base letter or spacing dash
([Unicode combining marks chart](https://www.unicode.org/charts/PDF/U0300.pdf)).
The compatible eight-point clipped bars use512/256-unit lengths,64/96-unit
weights and16-unit corner cuts. Points, anchors and explicit attachment values
are on8. Both glyphs are purple pending human review. Existing glyph outlines,
anchors, advances and human grades remain untouched.

## Placement and rejected trials

A separate Latin overlay lookup centers marks on unaccented letter bodies;
lowercase y288, capitals384, dotted circle432. It includes alternate bases
such as a.bold and numbered fi/fl components. Ordinary above/below marks keep
their existing placement. Contextual ccmp selects the shorter bar on narrow
letters and encoded ligature endings. The first wide-only trial reached into
neighboring letters and was rejected after whole-image review; retained under
iterations/wide-trial. This is Latin attachment scope; generic Arabic/Hebrew
overlay behavior is not claimed. No protected base anchors were added.

## Build repair required by per-master GPOS

The masters have different editor glyph orders. Previously identical feature
text could compile once, but distinct overlay coordinates forced per-master
GPOS merge and exposed InconsistentGlyphOrder. build_source_snapshot.py copies
sources to a temporary directory and normalizes only the copied glyph order;
live UFO ordering and all existing GLIF bytes remain unchanged. Two focused
tests cover preservation/cleanup and external-source rejection.

The old static path also compiled Regular's explicit feature coordinates into
heavier instances. Named instances in config.yaml now use gftools' variable-font
instancer, so coordinates interpolate correctly. Standard overlap removal and
integer serialization change outline representations in406/548/538/433 old
static glyphs at400/500/600/700. All old static advances are unchanged. Each
new static's complete glyph geometry matches a separately serialized,
overlap-removed VF instance. The old VF geometry/advances are exact in4415
comparisons. Static before/after Latin, Arabic and Hebrew raster rows were
inspected at all four weights; these are sampled checks, not pixel equality or
approval of protected Arabic forms. static-build-comparison.json records scope.

## Evidence and preservation

Eleven source files: four new GLIFs, four registration plists, two features and
config.yaml. All1790 other existing source files remain byte-identical, including
326 Arabic recursive reservations per master and131/74 green sources. Exact
before/candidate snapshots, dependencies and hash-guarded application retained.
Build helper, build entry point and tests are separately scoped changes.

765 scoped checks,4415 prior glyph/weight comparisons,20 Latin test methods and
two snapshot-helper tests pass. Narrow-letter neighbor tests run at five VF
weights and all statics. The existing216 Hebrew failure subcases reproduce;
only integer-valued float formatting (18.0 versus18) is normalized for comparing
messages, with raw results retained. No new numerical failures. Four new
glyph-masters have zero grid findings. Source contours are convex line polygons;
there are no cubic curves to score. Preflight and active/scratch identity are
recorded separately; preflight is not visual approval.

Complete48px forms/words at400/550/700 and224px endpoint details were inspected.
Actual Diffenator stock first viewport and labeled short-stroke supplement were
inspected in both Virtua and Rubik at400/550/700. Hashes/screenshots are in
diffenator/review.json. Rubik's default placements are comparison evidence,
not copied outlines or placement templates. Bold density, fixed-bar proportions
and pair rhythm still need human optical review.

Full online unexcluded Fontspector1.9.0 on the final candidate package remains
10 FAIL /9 WARN /160 PASS /10 INFO /40 SKIP. qa-wide-trial retains the earlier
trial; qa-online is final. Serving-set failures for U0302/U0331/U1EBC/U1EBD remain.
No metadata/subset declarations or exclusions changed. Package metadata/artwork
remain provisional; statics are not part of that downstream VF-package run.

Pinned Rubik gap now348 encodings:182 Cyrillic,2 combining overlays (U0337/0338),
62 Common and102 Arabic presentation forms. Latin cmap gap remains zero; this
is not full language coverage or release readiness. Next the two slash overlays,
then independent common symbols and release blockers. Preserve Arabic60272;
this batch is local only, with no push/publication.

Preview: http://127.0.0.1:60273/batch27/comparison/short-stroke.html
