# LAT-001 batch22 · Fi/fl coverage and shaping

Adds fi/fl (U+FB01/U+FB02) in Regular and Bold. Exact green f and i stem geometry,
and existing l geometry, are copied into new purple glyphs; donors remain unchanged.
Fi has32+8 points and fl32+16. Crossbars overlap the second stem32 units; fi extends
its head across the i stem without a separate dot. Advances are528/656 for fi and
560/672 for fl; all new points, anchors and spacing on8, zero grid findings.

The first Bold fl trial was rejected from the whole enlarged image: its f head
closed against l, producing a tiny hole/notch. `iterations/01-tight-bold` retains
that trial. The applied Bold l moves to x424 (shift352), leaving48 units above the
crossbar; Regular opening40. Bold fi stem gap increases64to96. All cubic donor
geometry remains exact; inherited tangent G1 curvature jumps are not corrected.

Ten sources change: four new GLIFs, four registration plists and two feature files.
All1785 other existing sources,326 Arabic recursive donors/master and all green
source bytes remain exact. Before/candidate hashes and guarded application are
retained. All previous compiled glyph ink/advances remain exact. New `liga`
substitutes plain fi/fl; disabling it preserves original pairs. GDEF ligature
classification and numbered top/bottom anchors support attachment. Intervening
marks deliberately prevent replacement. Earlier soft-dotted/composition rules
can prevent fi+above-mark ligation; encoded ﬁ+mark is separately tested, not
claimed equal to every decomposed sequence. No donor kerning is inherited.

## Verification and image review

165 scoped comparisons and15 Latin test methods pass. The same216 Hebrew failing
subcases reproduce before/after, with zero new or resolved failures. Active build
and preflight completed; active and scratch font tables match except timestamps.
Five-weight source profiles have no sampled reversals/proper within-contour
crossings. Intentional inter-contour bar overlap is retained in compiled fonts:
PathOps diagnostic union gives one contour with no enclosed counter for each
ligature at400/475/550/625/700 (`compiled-union.json`); this does not rewrite fonts.

Whole forms, reading and word rasters400/550/700 and224px endpoint details were
inspected. Real Diffenator stock coverage first viewport and labeled same-text
ligature supplement were inspected in Virtua and Rubik at400/550/700. Stock
context reports are generated, not exhaustively language-reviewed. Font/report
hashes and screenshots are in `diffenator/`. Arabic live proof60272 is unchanged.
Preview: http://127.0.0.1:60273/batch22/comparison/ligatures.html (Old=Virtua,
New=Rubik; slider value governs weight despite the Regular menu label).

## Remaining findings

The revised fl opening stays visible at all sampled weights. Bold remains dense;
new ligature pair spacing and f+fi/f+fl rhythm need optical review. No dedicated
ffi/ffl drawings are added. Existing uneven stock-text spacing and protected base
proportions are not approved by these additions. Purple means pending human review.

Pinned Rubik comparison now has no missing Latin-script encoded codepoints;
350 other encodings remain:182 Cyrillic,4 combining,62 common symbols and102 Arabic
presentation forms. This is not full language coverage or release readiness.
Next inspect remaining combining marks and serving-subset normalization, then
independent symbols and release blockers. Keep narrow I/l, off8 human widths,
Tbar/long-s/florin/kra pair spacing, protected g+comma collision and Hebrew baseline
failures open. Local checkpoint only; no push or publication.
