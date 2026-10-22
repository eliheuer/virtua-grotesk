# LAT-001 batch18 · Long s

Adds `longs` (ſ, U+017F) in Regular and Bold. Each new24-point contour uses the
respective green f's exact head curves, left arm and stem, removing only its eight
right-arm points. The f donors are byte-identical. Both new glyphs are purple
pending human review; this is an encoded historical form, with no automatic s→ſ
substitution. No kerning or feature-source changes.

Six source files: two new GLIFs and four registration plists. All1779 other
existing source files remain exact, including326 Arabic reservations per master
and all green drawings. Scratch before sources, donor snapshots, baseline hashes,
candidate sources and guarded application receipt are retained here.

Regular advance344 (256+64+16+8), bounds24..320, bearings24/24.
Bold advance400 (256+128+16), bounds32..376, bearings32/24.
New points, anchors and spacing are all on8; both grid reports have zero findings.
Both retain y0..768; top anchors264/320 at768, bottom160/200 at0.

## Verification and actual images

90 scoped checks;11 Latin test methods pass. Master topology matches and all
existing compiled glyph ink/advances remain exact at400/475/550/625/700.
Five-weight signed profiles have no sampled reversals or proper polygon crossings.
The four tangent G1 curve/line joins per master retain their curvature jumps from
f; these are not G2 and a clean lint result is not visual approval. Frozen baseline
and scratch engineering runs reproduce exactly216 existing Hebrew failures, zero
new failures. Active preflight completes; active/scratch font tables match apart
from head timestamps. Preflight establishes artifact presence only.

Inspected whole FreeType/RAQM forms, marks and word rows at400/550/700, sequential
DesignBot reading rows at400/550/700 and enlarged224px endpoints. Rubik has actual
U017F support; Before panels explicitly say unavailable. [Large Bold proof](large-700.png).

Actual Diffenator3 browser review: generated stock context and coverage reports;
inspected the stock Virtua coverage viewport at400/550/700. Since its sample does
not include long s, a separate explicitly labeled supplement replaces only text
and heading, preserving stock font-switching/weight controls. Inspected this same
text in Virtua/Rubik at400/550/700. Commands, hashes, nine browser screenshots and
findings are in [diffenator](diffenator/review.json). Local preview:
<http://127.0.0.1:60273/batch18/comparison/longs.html> (Old=Virtua, New=Rubik).
Stock reports remain separate. Arabic live proof60272 is unchanged.

## Still unresolved

Bold is visibly denser than Rubik, inheriting the green f's192-unit lower stem.
The compact head and default pair spacing, particularly ſi/ſl and repeated ſ,
remain human-review items; no f kerning was copied blindly. Tested marks are clear,
but this does not certify historical-language usage or all combinations.

Pinned Rubik Latin missing count6→5: ĸ ŉ ƒ ﬁ ﬂ. Other gaps are unchanged:
182 Cyrillic,4 combining marks,62 common symbols and102 Arabic presentation forms.
These are codepoint counts, not language coverage. Existing216 Hebrew failures,
serving-subset failures, protected attachment and spacing exceptions remain open.
Next bounded coverage: inspect florin construction, then kra, apostrophe-n and
fi/fl; preserve all green donors. Local checkpoint only, no push or release claim.
