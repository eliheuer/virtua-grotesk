# LAT-001 batch19 · Florin

Adds `florin` (ƒ, U+0192) in Regular and Bold as purple drafts. Actual pinned Rubik
reference inspection shows an upright f with a descending left hook. Virtua's
new40-point contour retains its respective green f head and arm construction;
the bottom hook rotates the f head180 degrees, with its outer minimum at−256.
The Bold inner turn translates8 left, keeping the cubic intact while meeting the
existing lower stem104 instead of the upper112. The four right crossbar endpoint
x values extend4 units to land on8 in this new glyph only. All original donors,
including f and j, remain byte-identical. No external outlines copied.

Six source files: two new GLIFs plus four registration plists. All1781 other
existing sources unchanged, including326 Arabic reservations/master and all green
sources. Scratch snapshots, donor f bytes, source hashes, candidates and guarded
application receipt are retained. No feature, kerning or clipping-metric changes.

Regular: advance408=256+128+16+8; bounds(32,−256,376,768), bearings32/32.
Bold: advance456=256+128+64+8; bounds(48,−256,424,768), bearings48/32.
Top anchors(296,768)/(336,768); bottom(136,−256)/(184,−256). All new points,
anchors, advances and actual bearings on8; zero grid findings.

## Verification and visual evidence

95 scoped checks and12 Latin tests pass. All previous compiled glyph ink/advances
remain exact at400/475/550/625/700; master structure is compatible. Five-weight
signed profiles have no sampled reversals or proper polygon crossings. Each
master has eight tangent G1 curve/line joins retaining donor curvature jumps;
these are not G2, and numerical checks are not visual approval. Frozen engineering
runs reproduce exactly216 existing Hebrew failures with zero new failures.
Active preflight completes; active/scratch font tables match apart from head
timestamps. Preflight establishes artifact presence only.

Inspected whole FreeType/RAQM forms, marks, letter/currency contexts at400/550/700;
sequential DesignBot reading proofs at400/550/700 and224px enlarged endpoints.
The first enlarged panel rejected ink2px beyond its interior because the−256
hook descended lower than the previous glyph. The local renderer raises only
that proof baseline16px, retaining full outlines and its boundary assertions.
No font metrics were changed to disguise a proof-layout error.
[Large Bold proof](large-700.png).

Generated actual Diffenator3 stock context/coverage reports and a separately
labeled florin supplement using the same stock font and weight controls. Inspected
Virtua's stock coverage viewport (including eƒe) and identical supplement text in
Virtua/Rubik at400/550/700. Commands, exact font/report hashes, nine screenshots
and findings: [Diffenator review](diffenator/review.json). Local preview:
<http://127.0.0.1:60273/batch19/comparison/florin.html> (Old=Virtua, New=Rubik).
Arabic live proof60272 remains unchanged.

## Unresolved / next

The Bold stem is denser than Rubik, inheriting the green f. Compact head, hook
mass and default currency/letter spacing need human optical review. No donor
kerning copied blindly; this does not establish native-reader or all-language
approval. Existing Hebrew, subset/compound-mark, protected attachment and optical
spacing findings remain unresolved.

Pinned Rubik Latin gap5→4: ĸ ŉ ﬁ ﬂ. Other gaps remain182 Cyrillic,4 combining
marks,62 common symbols and102 Arabic presentation forms. These are codepoint
counts, not languages. Next bounded construction: kra, preserving green k donors;
then apostrophe-n and fi/fl, followed by independent release blockers.
Local checkpoint only; no push or release approval.
