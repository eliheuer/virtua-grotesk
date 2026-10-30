# LAT-001 batch15 · Hcaron ascender attachment

Baseline `c7bab350`. The caron on ȟ overlapped the ascender in both masters.
Both hcaron composites now place the existing mark above the left stem:
Regular offset(-96,192), Bold(-48,192). The unchanged h reaches y768;
mark bottoms830/832 leave62/64 units, and their tops align at1024. Regular
advance592→584 matches its base; Bold remains672. Explicit outgoing top
anchors(120,1056)/(160,1056) support stacks. Bottom anchors(296,0)/(336,0)
preserve below-mark attachment. New offsets/anchors/widths are on8.

Two GLIFs and two feature files only. All1775 other source files, all base
and donor drawings, human grades and326 Arabic reservations/master are exact.
No green consumer or Arabic dependency is affected. No new outline drawing or
color assignment: existing orange/red wrapper grades remain human-owned.

## Compiled composition

A narrow `ccmp_hcaron` lookup composes h+caroncomb. An initial simple ligature
failed when a canonically reordered cedilla intervened. The final lookup uses
`UseMarkFilteringSet [caroncomb]` so other marks do not block the composition;
it does not change other Latin composition lookups. Full, decomposed and
missing-hcaron-cmap samples now agree, including tested above/below stacks.
This is a targeted repair, not a claim that all serving-subset failures are fixed.
The separate ogonek-plus-acute and protected g+comma-below issues remain queued.

## Whole-image review

Complete before/after forms and contextual letter strings at400/550/700,
plus224px/em endpoint details, were inspected. The attached flag-like mark is
now a separate, centered caron above the ascender. The h and caron silhouettes
are preserved; no new bump, notch or collision was observed in these contexts.
The Regular mark is lighter and narrower than Bold; its inherited taper and
the base weight contrast remain for human review, not approved by this fix.
The Regular mark overhangs left by24 units, like the existing stem-centered
circumflex family. Paired letter contexts remain clear in the inspected images.

Rubik lacks U+021F: encoded rows and large panels explicitly show unavailable.
Separate supported h+U+030C rows and h/ĥ/H/Ĥ/š/č/ž comparisons show actual Rubik
without font fallback. FreeType/RAQM complete rows supplement sequential raw
DesignBot reading/large proofs. Eight final image hashes are retained.

## Verification

- 135 scoped comparisons at400/475/550/625/700; full master topology compatible.
- Only hcaron compiled ink changes; all other glyph drawing commands are exact.
- No curves or donor shapes change. Five-weight clearance is62..64 units.
- Nine Latin test methods pass, including new attachment/canonical-fallback
 checks on the VF/four statics and clipping checks for the tested above stacks.
- Frozen engineering baseline reproduces exactly216 Hebrew failures; zero new
 or resolved failures. This is not a whole-suite pass.
- Active build/preflight complete. All five active fonts match scratch tables
 except head timestamps/checksum adjustment. No online Fontspector rerun.
- Grid gate retains23 inherited findings (19 Regular,4 Bold), all in unchanged
 donor/base geometry, donor anchors and donor metrics. New wrapper values and
 actual bearings are on8. Popcounts remain descriptive.

Exact baseline/source snapshots, dependency closure, hash-guarded application,
compiled fonts and proof receipts are retained. Arabic live proof unchanged.
Local checkpoint only; no push/publication or reader approval. Next: measured
I/l narrow-accent and K/c/k/t optical-width exceptions, then remaining Latin
coverage and independent technical blockers.
