# LAT-001 batch26 · Combining turned comma above

Baseline `94d80d04`. Adds U+0312 (`commaturnedabovecomb`) in Regular/Bold;
active application is a purple draft, not human approval. No push.

The [Unicode combining-mark chart](https://www.unicode.org/charts/PDF/U0300.pdf)
identifies U+0312 as turned comma above/cedilla above and notes Latvian use but
not decomposition. Therefore g+U0312 is not forced to equal precomposed ģ;
the existing batch07 Latvian constructions remain exact.

## Construction and protection

Eight-point clipped diagonals copy Virtua's commaaccent geometry through180°,
with x=288−x and y=576−y. Incoming top(144,576), outgoing top(144,800), zero
advance. Ink y616–776; Regular x96–192, Bold x80–208. All new values on8.
The existing soft-dotted above-mark class gains this mark, preserving dot removal
on i/j/iogonek even with intervening below marks. No donor or base edits.

Eight source files: two new GLIFs, four registration plists and two features.
All1,789 other existing sources remain exact, including every existing GLIF,
326 Arabic recursive sources/master and131/74 green glyphs. Full hashes,
consumer closures, before sources, candidates and guarded application retained.
New contours are compatible and strictly convex at400/475/550/625/700;
line corners are intentional. No cubic curvature score applies. Zero grid findings.

## Evidence

165 scoped checks plus4,410 existing compiled glyph/weight comparisons preserve
all old ink and advances. Eighteen Latin tests pass against scratch and active
fonts; the same216 baseline Hebrew failures recur with zero new failures.
Preflight completes, and all five active/scratch font tables match except head.
Six focused Fontspector checks pass: soft_dotted, dotted_circle, three GDEF mark
checks and outline_direction. This is not a full package QA rerun; batch25's
10 FAIL/9 WARN package evidence predates this addition.

Inspected complete48px forms/words at400/550/700 and224px endpoint letters,
plus actual Diffenator stock first viewport and same-text supplement in both
Virtua and Rubik at all three weights. Screenshots/hashes and fonts retained.
Before rows explicitly unavailable for U+0312. New mark is compact/light compared
with Rubik and follows the current Virtua comma design; proportions remain for
human review. Sampled letters and upper stacks remain clear. Existing dense Bold,
heavy g/j construction and uneven longer-text spacing are unchanged review items.
Rubik's synthetic acute-over-U0312 overlaps; Virtua separates it vertically.
Generic g+U0312 retains protected base anchors, differing slightly from local ģ.
No exhaustive language, native-reader, or release approval is claimed.

Preview: http://127.0.0.1:60273/batch26/comparison/turned-comma.html
Old=Virtua/New=Rubik. Arabic60272 remains unchanged.

Pinned Rubik cmap gap is349 encodings:182 Cyrillic,3 combining (U0335/U0337/U0338),
62 Common,102 Arabic presentation forms; zero Latin-script gap. These are not
language counts. Next inspect the three overlay marks' attachment behavior,
then independent common symbols and technical blockers. Existing protected
attachment, optical-spacing and serving-subset findings remain open.
