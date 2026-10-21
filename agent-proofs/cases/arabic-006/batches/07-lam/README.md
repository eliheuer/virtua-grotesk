# ARB-006 batch 07 — Bold Lam repair

Applied working drafts under the standing autonomous authorization. Human review
is pending. This is a partial Lam repair, not a completed Arabic family.

## Exact scope and construction

Bold `lam-ar`, `lam-ar.init`, `lam-ar.medi`, plus the advances of five inherited
final Lam–Alef wrappers. Eight GLIFs total, marked purple. Regular, final Lam,
green glyphs, manual hamza and all 18 reserved Beh/component files are unchanged.
`candidate.json` / `applied.json` record full baseline hashes and dependency scope;
`before-sources/` and `candidate-sources/` retain exact XML.

The protected Regular skeleton and local 160-unit Bold stem / 176-unit joining
bar convention govern this trial, not external outlines. Isolated Lam previously
retained a 96-unit Regular stroke and an advance narrower than its ink. It now
has 160-unit sides, a 176-unit bottom, 32-unit sidebearings and advance 704.
Its inner and outer bowls keep horizontal/vertical extrema and matched curvature
at their respective bottom joins. Initial Lam has a 96-square inner return,
160-unit stem, 16-unit cap cuts and advance 320. Medial Lam uses paired 80-square
inner turns, 16-unit exposed cuts and a shallow 32-high lower relief with a
16-unit flat. That relief preserves the compatible Regular skeleton without
the old negative dip and degenerate vertical notch. Its advance is 448.
Lam–Alef wrappers at x=256 have advance 704. Component offsets, donors and
anchors were not changed. These dimensions are a local trial, not new style law.

## Checked evidence

- Variable and four static fonts built. Preflight completed; zero blocking
  master mismatches. Compatibility report records 497 expected width differences.
- 252 before/working shaping comparisons at seven weights preserve glyph IDs
  and clusters; changed advances agree with compiled widths. Compiled changes
  are limited to these eight affected glyphs. See `verification.json`.
- Signed profiles remove three sampled reversals and two smooth-node kinks.
  No sampled proper contour crossings or new curve faults. Bowl cubic joins
  are G2; curve/straight joins are G1, with explicit chamfer/relief corners.
  This is diagnostic evidence, not a guarantee of Arabic correctness.
- New outline coordinates, widths and sidebearings are on 8. Eight pre-existing
  anchor-x exceptions (106 in initial, 226 in medial) are preserved and reported
  by `grid.json`; the full grid gate therefore does not pass. Attachment work is later.
- Actually inspected `lam-400.png`, `lam-550.png`, `lam-700.png`,
  `lam-alef-700.png` with all four references, plus all three `*-large.png`
  source-scale details. The repaired curves are open and continuous, the cap
  cuts are consistent, and no lumpy inner return or crossing was seen in the
  changed roots. 550 is an actual variable instance; Plex explicitly uses 500,
  its nearest supplied static face. Font/image hash receipts accompany PNGs.
- Large raw DesignBot jobs must run sequentially: concurrent calls reused
  temporary state. The missing/mismatched initial/medial outputs were rerendered
  sequentially and checked against the actual glyph forms.

## Unresolved, visible in the proof

Final Lam in both masters is a turning stem without the descending bowl shown
by all four references. Its Regular is green and lacks compatible points for a
correct bowl; leave it unchanged until a named structural exception. As a result,
the joined three-Lam string still ends in a thin, wrong final form. Do not mistake
this partial repair for a correct full string.

Lam–Alef remains structurally wrong: the final is parallel stems rather than a
proper ligature, and the isolated has an overly crossed/hourglass silhouette.
The five wrapper width corrections only address inherited metrics; they do not
fix that design. Regular final wrappers inherit green geometry. A later bounded
ligature pass needs protected-source scope resolved before structural edits.

Next independent family: Meem. Recompute grades, recursive green descendants,
Beh reservation and current hashes before editing. Do not silently revisit
protected Lam structure or the user's Beh work.

The browser proof was reloaded and checked at 700; `browser-700.jpg` records
the visible viewport. Full reference panels are recorded in the raster sheets.
