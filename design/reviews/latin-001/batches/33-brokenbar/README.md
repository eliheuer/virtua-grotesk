# LAT-001 batch33 · Broken bar

Adds brokenbar U00A6 in Regular/Bold as two compatible eight-point clipped
vertical segments. Advance320; strokes96/160; bearings112/80. Lower segment
spans y-128–256 and upper448–848, leaving192 units clear. Both retain16-unit
corner cuts. Every new point, bearing and advance is on8; zero grid findings.
Green I/H provide stem/chamfer context. Their100/192-unit stems and optical
coordinates remain untouched. Existing yellow/orange bar is diagnostic context,
not a copied outline donor. The new form shares its vertical span and advance,
but its strokes are16 units thicker. No reference outlines copied.

U00A6 has no canonical decomposition; it stays a separate encoded glyph from
U007C vertical line. No feature, kerning, anchor, metric or normalization alias
changes were made. New glyphs are purple, pending human grading.

## Whole-image review

Before drafting, inspected actual Virtua green I/H and bar alongside Rubik's
bar/broken bar. Complete48px forms and reading rows at400/550/700,224px endpoint
details, and actual Diffenator same-text supplement plus stock first viewport
at all three weights were inspected. The192-unit gap stays open and clearly
distinguishes the form from the solid bar. Virtua's broken bar is taller and
more widely split than Rubik; default spacing, height and stroke balance remain
human optical-review items. Generic accents retain right-side fallback and are
not a centered attachment claim. Stock mixed text remains uneven and Bold dense;
only the first stock viewport was sampled, not exhaustive language approval.
The stock sample omits U00A6, so the labeled supplement is retained. Arabic live
proof60272 and its case/layout remain unchanged.

## Verification

Six source files: two new GLIFs and four registration plists. All1815 other
existing source files and every previous GLIF/human grade remain exact, including
326 reserved Arabic recursive glyphs/master and131 Regular/74 Bold green sources.
Frozen before assets, scratch candidates, dependency closure and current hash
guards precede surgical application. Compatible8+8-point structures, compiled
clockwise contours and no proper crossings at five sampled weights. No cubics.

135 scoped checks,4470 exact old VF glyph/weight ink/advance comparisons,3575
old static glyph ink/advance comparisons.26 Latin methods plus2 build helpers
pass.216 baseline Hebrew failures reproduce unchanged, zero new failures or
resolutions. Active/scratch tables match except head. Preflight, including the
sequential raw DesignBot print proof, completed; this is not release approval.

Fresh online unexcluded Fontspector1.9.0 package:12 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP, exact failure records identical to batch32. Existing serving-set
reachability and protected-source warnings remain; no exclusions or false subset
declarations added. Public lookup egress was inspected in batch32/network-audit.json;
no metadata or network-destination change was introduced here. Package metadata/
artwork remain provisional and unapproved; QA uses the VF.

Pinned Rubik gap340 encodings:182 Cyrillic,56 Common,102 Arabic presentation
forms. Latin/combining parity is not complete language coverage or visual approval.
Next soft-hyphen U00AD behavior assessment: inspect default-ignorable shaping,
existing hyphen sources/reservations and actual browser line breaking before
adding any encoding or claiming support. Then independent Common-symbol gaps
and release blockers. Local only; no push/publication.

Preview: http://127.0.0.1:60273/batch33/comparison/brokenbar.html
