# LAT-001 batch48 · Micro-sign assessment

Read-only at607ab7aa, with active fonts unchanged from6007487c. All1845 sources
and five active font hashes remain exact. Arabic326/master and green131 Regular/
74 Bold preserved. Exact u/p donor files, grades, geometry, anchors and hashes
are retained. Their recomputed14-member reverse closure per master has no Arabic
intersection. No active source/font changes, build, preflight or fresh package QA.

## Coverage and compatibility

Virtua lacks U00B5 MICRO SIGN and U03BC GREEK SMALL LETTER MU, with no existing
named or encoded donor for either. Pinned Rubik encodes U00B5 as uni00B5 but also
lacks U03BC; neither font encodes U039C. Direct HarfBuzz returns .notdef for both
lowercase characters in Virtua, and only for Greek mu in Rubik.

Micro sign has compatibility decomposition `<compat> 03BC`, not canonical
decomposition. NFD preserves it; NFKD and casefold change it to Greek mu and
lose the pinned Rubik coverage. Do not normalize text to repair this, alias an
ordinary u, or silently add Greek coverage. Official references inspected:
[Unicode Latin-1 chart](https://www.unicode.org/charts/PDF/U0080.pdf) and
[Greek chart](https://www.unicode.org/charts/PDF/U0370.pdf). Local Unicode and
HarfBuzz versions and exact normalization outputs are in assessment.json.

70 direct cases ×4 modes (raw/NFD/NFKD/casefold) at400/475/550/625/700 and30 real
in-memory text-subset cases retained. Subsets preserve full-font shaping in these
samples, including .notdef for missing characters; equality is not coverage.
Contexts include measurements, µm/µg/µs/µF, marks and ordinary u/p neighbors.

## Construction and actual proof review

Both u and p donors are green in both masters. Virtua u supplies the rounded
lower bowl, open top and right heel; p supplies the family descender reference.
Regular u has96-unit uprights and592 advance; Bold has192-unit uprights and720
advance. Protected Bold inner-bowl y124 is an inherited optical exception and
must not be snapped. Donor bytes and grades are frozen.

Full48px400/550/700 forms/measurement rows and224px400/700 detail images inspected.
Unsupported raster rows are labeled unavailable. Rubik micro has an upright left
descender and a u-like open bowl/right upright; it is a comparison, never an
outline source. Virtua Bold body is denser. Nine actual browser views inspected:
three controlled two-font fixtures plus six Diffenator target views. Controlled
Virtua micro uses visibly slanted fallback ink; Greek mu also receives fallback
ink in both columns. The fallback fonts were not identified. Diffenator shows
boxes for unsupported micro/mu, while Rubik's micro works. Generic Rubik cedilla
uses a right-side fallback position. Browser ink does not establish cmap support.
Font/image hashes and sampled scope are in proofs.json and browser-review.json.
Stock Diffenator generated; unchanged batch46 stock review is referenced, not
claimed repeated. No native-reader or human design approval.

## Next bounded draft

Prepare new purple `mu` U00B5 in Regular and Bold on scratch sources, preserving
all existing drawings. A candidate can retain the exact green u component and
extend its left stem toward the protected p descender depth, with compatible
clipped geometry on8. Inspect the lower bowl/descender union and Bold mass before
application; do not assume a simple extension is optically sufficient. Derive
all construction from Virtua, not Rubik. Preserve donor optical exceptions and
use deliberate new top/bottom anchors if mark attachment is added; do not inherit
u's bottom y0 blindly. Recompute current hashes/reservations first, then compiled
shaping, real subsets, five-weight interpolation and whole-font preservation.
No automatic U03BC alias, ordinary-u alias or compatibility substitution.

Batch47's separate digit-only sups proposal remains unapplied. Latest package
QA is batch46:12FAIL/10WARN/159PASS/10INFO/40SKIP;216 Hebrew failures and all serving,
soft-hyphen policy and optical blockers remain. Rubik gap328 is unchanged:
182 Cyrillic/44 Common/102 Arabic presentation forms. Local only/no push;
Arabic60272 and its current case/layout unchanged.

Preview: http://127.0.0.1:60273/batch48/comparison-400.html and
http://127.0.0.1:60273/batch48/comparison/micro.html.
