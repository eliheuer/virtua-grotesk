# LAT-001 batch35 · Encoded soft-hyphen compatibility

Adds `softhyphen` U+00AD in Regular and Bold as an exact unchanged `hyphen`
component,440 advance and purple review color. Six source files: two new GLIFs
and contents/glyph-order/category registrations in both masters. All1817 other
existing source files, every previous GLIF, Arabic326/master and green131/74
sources remain byte-identical. No donor drawing, feature, anchor, metric or
kerning edits. This repairs direct-cmap/preserved-ignorable access; batch34
already showed correct normal browser discretionary hyphenation.

## Scope and verification

- `baseline.json`, `before-sources/`, `donor-sources/`, `candidate-sources/` and
  `dependencies.json` preserve exact source hashes and the recomputed closure.
  Hyphen/uni2010 reverse consumers are frozen. Donors remain yellow Regular/
  orange Bold; reuse preserves existing behavior and does not promote their
  design to green/reference status. The two wrappers have matching components.
- 209 scoped checks;4475 old VF glyph/weight and3579 old static glyph comparisons
  prove exact old ink and advances. Default HarfBuzz shaping stays identical,
  including unbroken soft-hyphen words and mixed-script preservation samples.
  Preserved-ignorable output now returns the hyphen ink at440 advance instead
  of `.notdef`.72 real-subset comparisons exercise both flag modes at five VF
  weights and four statics. FontTools strips names in default subsets; comparison
  maps serialized glyph IDs back to their retained original order and separately
  verifies subset soft-hyphen geometry. No special subset option hides differences.
- 27 Latin test methods plus two build-helper methods pass in active fonts.
  Frozen baseline and candidate reproduce the same216 Hebrew failures: zero new
  or resolved subcases. Integer-valued float formatting alone is normalized in
  failure comparison; raw evidence remains in `existing-regressions.json`.
- New wrapper width/component placement and actual bearings are on8; grid0.
  The exact donor's88-unit bar thickness,312-unit length and16-unit corners
  remain unchanged in both masters;440 advance has popcount5. The unchanged
  Bold bar remains much lighter than Rubik's Bold hyphen. This is an optical
  review finding, not a new weight design or approved exception.
- Whole forms/words at400/550/700 and224px endpoint details were inspected.
  Display-only font copies map a private-use diagnostic to U+00AD to make
  normally hidden ink visible. An initial proof accidentally retained an
  unrelated existing PUA in Before; the fixture was corrected to remove it and
  show explicit U+00AD-unavailable labels, then all corrected forms were reviewed.
  Active cmap entries outside U+00AD never changed. Display copies are not
  release/build inputs.
- Actual browser manual/none/no-wrap fixtures at400/550/700 give exactly the
  same line heights and word widths as batch34. Both Virtua and Rubik hide the
  unbroken U+00AD and show the discretionary break. Actual Diffenator supplement
  and first stock coverage viewport were inspected for both fonts at all three
  weights (12 screenshots, plus three controlled browser screenshots). This is
  one browser and sampled English behavior, not all-platform/native-reader approval.
- Preflight completed with sequential proof rendering. Active/scratch tables
  match except head timestamps. Old glyph IDs can shift after registration;
  source-feature identity and sampled shaping preservation do not mean binary
  layout tables are byte-identical. `table-delta.json` retains changed tables.

## Full online package QA: new policy warning retained

Fontspector1.9.0 unexcluded online package: **12 FAIL /10 WARN /159 PASS /
10 INFO /40 SKIP**. The12 FAIL records are exactly unchanged from batch33.
One PASS becomes WARN: `soft_hyphen` warns solely because U+00AD is encoded.
The official1.9.0 check recommends leaving discretionary hyphenation to shaping
engines and omitting this encoding. This matches batch34's browser evidence.
See [the check source](https://github.com/fonttools/fontspector/blob/v1.9.0/profile-universal/src/checks/soft_hyphen.rs)
and the locally inspected official source provenance in batch32/network-audit.json.

This is a real release-policy tradeoff between the explicitly requested Rubik
cmap compatibility target and the QA recommendation. It is **not an approved
release exception or a passing QA result**. The local purple compatibility
wrapper is retained for review; no automatic exclusion, severity override,
blank glyph or silent cmap removal hides the warning. Release disposition
(retain compatibility versus omit U+00AD) remains open while independent work
continues. Other warning differences are only package paths, shifted glyph IDs
or ordering of suggested subset names; exact raw deltas remain in
`package-failure-delta.json`.

Online QA used the same audited public metadata/link/name destinations as
batches32–33, with no font/package upload. Metadata/artwork remain provisional.
Serving-set failures U+0302/U+0331/U+0338/U+1EBC/U+1EBD and the216 Hebrew
engineering failures remain blockers. No unrelated subsets or exclusions added.

Rubik gap now339 encodings:182 Cyrillic,55 Common,102 Arabic presentation forms;
not language counts or visual approval. Next assess nonbreaking-hyphen U+2011
behavior separately (also absent from the pinned Rubik), then remaining Common
symbols. No automatic alias or new drawing follows solely from that assessment.
Arabic60272/current case/layout, Runebender and all protected dependencies are
unchanged. Local checkpoint only; no push, publication or licensing attestation.

## Evidence

Use `prepare.py`, canonical scratch `build.sh`, `verify.py`, `latin_check.py`,
`static_preservation.py`, `regressions.py` and `apply.py` only with frozen guards.
`compiled_proofs.py`/`detail.py` produce fixed images; `diffenator.py` produces
stock and labeled supplemental HTML. Source changes are in `changes.json`.
`browser-review.json` binds15 actual screenshots and measured comparisons to
font hashes. `qa-online/` binds the full package report and input hashes.

- [Diffenator supplement](http://127.0.0.1:60273/batch35/comparison/soft-hyphen.html)
- [Controlled browser400](http://127.0.0.1:60273/batch35/comparison-400.html)
