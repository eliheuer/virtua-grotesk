# LAT-001 batch37 · Generic currency sign

Adds purple `currency` U+00A4 in Regular and Bold, with608 advances and56/48
bearings. Six source files: two GLIFs and four registration plists. All1819 other
existing source files, every old GLIF/grade, Arabic326/master and green131/74
sources remain exact. No existing feature, anchor, kerning or font metric changes.

## Construction and visual review

The new symbol uses a round ring and four clipped diagonal arms. Green O/o/zero
supply Virtua construction/weight context; donor bytes are frozen, not edited.
Multiply and dollar are context only, not green references. Rubik was inspected
before drafting (`reference.png`) and used only for comparison, never outlines.

Six compatible source contours: two12-point cubic circles and four8-point arms.
Center304,352, outer radius208/handle112; counter radius128/96 and handles72/56.
Cardinal ring weights80/112; diagonal arm normal weights90.5/113.1, global16-unit
cap cuts. Advance608 =512+64+32 (popcount3). All new points/spacing on8; zero grid
findings. Full bounds56..552/y104..600 Regular,48..560/y96..608 Bold.

Whole48px forms/price words at400/550/700,224px endpoint images and signed curve
combs were inspected. The counter stays open and the four arms remain legible.
The compact currency is slightly higher relative to figures than Rubik; arm
projection, symbol/alphabet weight balance and default pair spacing remain
human optical review. Generic acute/cedilla use right-side fallback; no new
centered math/currency mark attachment is claimed. Existing Bold density and
uneven mixed-text spacing remain unresolved.

Actual Diffenator stock coverage first viewport and labeled same-text currency
supplement were inspected in both fonts at400/550/700 (12 screenshots).
`browser-review.json` binds hashes and scope. This is sampled visual review,
not human grading or exhaustive/native-reader approval. Old=working Virtua,
New=Rubik; slider values govern weights despite the Regular menu label.

## Engineering and QA

- 120 scoped checks and4480 exact old VF glyph/weight ink/advance comparisons.
  All existing compiled drawings and advances preserved. Static preservation:
  896 Bold/896 Medium/895 Regular/896 SemiBold =3583 comparisons.
- 27 Latin methods plus two build-helper methods pass against active fonts.
  Frozen baseline and candidate reproduce exactly216 Hebrew failures, with zero
  new/resolved subcases; raw failure evidence retained. This is not a passing
  whole engineering suite.
- Eight cubic extrema joins/master are G2; five-weight signed profiles show no
  sampled reversal warnings or within-contour proper crossings. Intentional
  ring/arm overlaps are retained in the VF. Diagnostic PathOps union has two
  contours (connected outer silhouette and one counter) at all five weights;
  static build uses the canonical VF instancing/overlap removal path.
- Scratch preparation, current hashes and full dependency reservations were
  checked before surgical application. Active/scratch font tables match except
  head timestamps. Source order normalization remains temporary. Preflight
  completed with raw DesignBot rendering sequentially; presence alone is not QA.
- Full online unexcluded Fontspector1.9.0 package remains **12 FAIL/10 WARN/
  159 PASS/10 INFO/40 SKIP**. Exact FAIL records unchanged from35; no new semantic
  warnings. WARN comparison only normalizes shifted glyph IDs, package paths
  and suggested-subset ordering; raw changed records remain. No exclusions or
  metadata/subset edits. Existing soft_hyphen release retain/omit choice and
  serving reachability failures remain open. Public network destinations are
  unchanged from the audited batch32 workflow; no font/package upload.

`baseline.json`, exact donor/before/candidate sources, `changes.json`,
`dependencies.json`, `application.json` and `final-identity.json` preserve
provenance. `grid.json`, curve/union reports, compiled proofs and QA inputs bind
claims to checked bytes. The initial Diffenator command lacked its output parent;
that fixture setup was fixed before any browser review. No drawing iteration
was needed after this bounded scratch candidate's visual inspection.

Rubik gap338 encodings:182 Cyrillic,54 Common,102 Arabic presentation forms;
not language counts or approval. Next inspect existing superior-digit donors
and superscript U00B9/U00B2/U00B3 coverage before proposing new drawings or aliases.
Preserve all protected bases and optical metrics. Arabic60272/current case/layout
and Runebender remain unchanged. Local checkpoint only; no push/publication.

[Diffenator comparison](http://127.0.0.1:60273/batch37/comparison/currency.html)
