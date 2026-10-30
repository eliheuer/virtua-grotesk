# LAT-001 batch47 · Complete superior-family assessment

Read-only at6007487c. All1845 source files and five active font hashes remain
exact. Arabic326/master, green131 Regular/74 Bold and human grades preserved.
The recomputed ordinary/tabular/superior figure reverse closure has30 members
per master and no Arabic intersection. No candidate font/source change, build,
preflight or fresh package QA is claimed.

## Current behavior

Both pinned fonts encode all ten superior digits. Virtua still has no `sups`,
`pnum`, `numr`, `frac` or `subs` feature. Its ordinary figures are proportional;
`tnum` substitutes ten `.tf` forms. Requesting `sups` alone has no effect;
`tnum+sups` keeps ordinary tabular forms. Rubik maps all ten digits to its encoded
superiors with `sups`; adding `tnum` leaves those same proportional superiors.
Rubik's sups lookup19 precedes tnum30; Virtua tnum is lookup5. Exact maps retained
in the feature-lookup JSON files. Lookup order matters, not feature-tag order.

60 direct full-font cases ×8 modes at400/475/550/625/700, plus90 real in-memory
subset cases ×8 modes are retained in assessment.json (480+720 shaped outputs).
Modes cover default, sups, tnum, tnum+sups, pnum+sups, numr, frac and subs;
texts include full families, repeated figures, letters/ligatures, fractions and
marks. Default subset options omit optional sups/tnum behavior on plain digits;
explicit retention of those features or all features preserves the tested Rubik
superior conversion. Explicitly encoded superiors survive text subsetting.
Default subset behavior is not proof that the full font lacks a feature.
NFD preserves encoded superiors; NFKD becomes0123456789 and loses the distinction.

The complete Virtua superior advances, in digit order, are:

| Weight | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 400 | 368 | 232 | 328 | 352 | 352 | 352 | 360 | 328 | 368 | 360 |
| 700 | 416 | 264 | 352 | 376 | 384 | 392 | 400 | 360 | 416 | 400 |

These are designed proportional figures, not tabular superiors. Full48px family/
feature rasters at400/550/700 and224px endpoint details inspected. Three actual
controlled browser pages plus six actual Diffenator same-text views inspected.
No CSS size/position simulation. All ten forms are legible in the sampled rows;
Regular is lighter than Rubik, and the curved1/3/6/7/9 follow Virtua construction.
Bold weight/width balance, shallow eight upper counter and pair rhythm remain
human optical-review findings. Whole-family availability does not approve them.
Stock Diffenator proof generated; same-font batch46 stock review is referenced,
not claimed repeated. Browser evidence binds nine screenshots to font hashes.

## Bounded feature proposal, not applied

The [OpenType sups specification](https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt#tag-sups)
refreshed2026-10-22 describes an optional substitution into designed superior
forms. A separate engineering batch can expose all ten existing superior figures
without redrawing them: map both ordinary zero–nine and their `.tf` counterparts
to the same proportional superior0–9 forms. Supporting both input classes avoids
losing the conversion when tabular substitution runs first. Validate compiled
lookup ordering and joint activation, real subset retention, marks, encoded
idempotence, default text and all-script preservation at VF/static weights.
Do not advertise tabular superior widths, superior letters, numr/dnom, fractions
or subs from this digit-only proposal. Do not silently change `aalt` or existing
figure drawings to implement it. This proposal is not a completed feature.

Serving-subset reachability is separate: feature closure does not justify false
math declarations or erase the encoded-codepoint warning. Latest full online
package QA remains batch46:12FAIL/10WARN/159PASS/10INFO/40SKIP.216 Hebrew baseline
failures, soft-hyphen retain/omit choice, optical issues and other release gates
remain open. Rubik gap328 remains182 Cyrillic/44 Common/102 Arabic presentation
forms; no coverage or release claim changed.

Next independent Common work: micro sign U00B5 donor/reference/compatibility
assessment. Keep the digit-only sups proposal for a separate bounded feature
batch. Local only/no push; Arabic60272/current case/layout unchanged.

Preview: http://127.0.0.1:60273/batch47/comparison-400.html and
http://127.0.0.1:60273/batch47/comparison/superior-family.html.
