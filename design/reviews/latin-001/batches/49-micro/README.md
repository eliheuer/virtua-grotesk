# LAT-001 batch49 · Micro sign

New purple `mu` U00B5 in Regular and Bold, from baseline9d0d097e. Six source
files: two GLIFs and four registrations. All1841 other existing source files,
every previous GLIF, Arabic326/master and green131 Regular/74 Bold remain exact.
Recomputed green u/p reverse closure14/master has no Arabic intersection. Exact
before/candidate/donor sources and guarded application receipts retained. No
feature-source, kerning, existing-anchor or existing-metric edits. Glyph IDs and
automatically compiled layout coverage change; no layout-table identity claim.

## Construction and rejected trial

The unchanged green u component supplies all four cubics, top terminals, bowl,
heel and width. One new compatible8-point clipped left-stem extension creates
the descender. Advances592/720, bearings72, stroke widths96/192;16-unit cuts.
Top overlap reaches320; final lower edge−200 matches actual protected p in both
masters. The first−256 trial was56 units deeper than p and looked too long in
the224px comparison; it is retained in trial-long-descender. An initial proof
row used unsupported U0323 and was corrected to supported U0331; Rubik's missing
U0331 remains explicitly unavailable/boxed, not replaced with comparison ink.

New top anchors296/360,576 center marks on the body; bottom120/168,−200 centers
marks under the descender. New values on8. Grid reports retain three inherited
Bold u y124 findings at points6/7/8, not new noise. Those green optical values are
unchanged. Popcount is descriptive:72=64+8,96=64+32,192=128+64,200=128+64+8;
advance592=512+64+16 and720=512+128+64+16. No green snapping.

Scratch decomposition/profile uses exact inherited u curves. Four cubics per
master, no sampled curvature reversals; inherited heel corner and Bold outer
bottom G1 curvature jump remain. Signed comb inspected; no new curve-fit claim.
Diagnostic PathOps union at400/475/550/625/700 gives one contour with open top and
no enclosed counter. Sources/VF retain intentional overlap; canonical VF-derived
statics remove it. Compatibility report passes for the new pair.

## Verification and proof scope

125 scoped checks plus4535 exact old VF glyph/weight ink/advance comparisons,
3627 old static comparisons,54 real-subset/NFD cases,28 Latin methods and two
build-helper methods pass. A new regression checks body advance, descender
alignment and compiled mark positioning at five VF/four static weights.
Acute/dieresis clear body by at least48; comma/macron below clear descender by
at least40; cedilla touches at−200. These are sampled attachment contracts, not
universal combining-mark approval. The wide macron extends left of the narrow
stem; retain this for optical review. Greek U03BC remains absent. NFD preserves
micro; NFKD/casefold mapping to Greek mu remains an unsupported-text distinction,
not a repair or automatic alias.

Frozen before/after engineering reports retain the same216 Hebrew failure
subcases, zero new/resolved numerical failures. Active build and sequential
DesignBot proof/reports/preflight complete; preflight is artifact presence only.
Active/scratch font tables match except head. Exact hashes are in final-identity.

Whole48px forms and measurement/word rows400/550/700,224px endpoint details,
signed comb and12 actual Diffenator target/stock first-viewport screenshots were
inspected against Rubik. New form has the intended upright left descender and
open u-like body. Revised depth matches p; Bold remains dense with a strong heel
and wide stem. Body mass, µm/µg/µs/µF/default pairs and small-size optics remain
human review. Stock text retains uneven rhythm and dense Bold. Rubik marks can
use right-side placement; new anchors differ deliberately. No copied Rubik
outline, human grade or native-reader approval. Arabic live proof60272 unchanged.

## Package state and next work

Full online unexcluded Fontspector1.9.0 package:
12FAIL/10WARN/159PASS/10INFO/40SKIP. Failure records exactly match batch46;
no new semantic warnings. Raw glyph-ID/path/suggestion-order differences retained
in package-failure-delta.json. Existing serving reachability, math-only superior
encodings, soft-hyphen retain/omit policy, protected Arabic findings and216 Hebrew
engineering failures remain open. Metadata/artwork stay provisional; package VF
only. No exclusion/subset declaration changes. Public metadata/link QA requests
follow the unchanged source-audited batch32 destinations; no font/package upload.
[Official QA guide](https://googlefonts.github.io/gf-guide/qa.html) refreshed.

Pinned Rubik gap327:182 Cyrillic,43 Common,102 Arabic presentation forms. Latin/
combining coverage is not reader approval or complete language parity. Next:
assess U2044 fraction slash and encoded fractions U00BC/U00BD/U00BE, including
existing figure construction, normalization, numr/dnom/frac interactions and
protected reverse consumers before a bounded draft. Do not reuse elevated
superiors blindly as fraction numerators. Separate digit-only sups proposal
remains unapplied. Local only/no push.

Preview: http://127.0.0.1:60273/batch49/comparison/micro.html
(Old=Virtua/New=Rubik; slider controls weight despite Regular menu label).
