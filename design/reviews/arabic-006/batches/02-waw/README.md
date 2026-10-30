# Batch 02 — Bold Waw

Baseline `b3cdbae3`. Applied working trial; no human grade assigned.

Bold `waw-ar` and `waw-ar.fina` now have a 160-unit head wall and tail thickness,
an open 128-unit counter, 16-unit terminal chamfers and 8-unit junction cuts.
The former Bold was essentially Regular weight. Advances are 704 / 800; the
hamza wrappers follow those base advances. Component offsets, anchors, hamza
outlines and all Regular source bytes are unchanged. Mark attachment remains a
separate follow-up; preserved anchor positions are not placement approval.

Required DesignBot rasters: `detail-400.png` and `detail-700.png`, both using
`بو و` at 192 px/em with all four references. Inspected both: Regular matches
its baseline; Bold no longer has a thin head or abrupt pinched connection beside
Beh. Its counter and tail aperture remain open, with no panel clipping. Waw's
upturned tail is retained from Virtua's existing design; the references use a
flatter or diagonal tail, so native-reader/design review remains relevant.

Build/preflight passed. `verification.json` records 133 shaping comparisons at
seven weights, source/master compatibility and compiled component closure.
Curve profiles have no sampled curvature reversals or zero-speed warnings.
Final bridge corners retain explicit cuts and are no longer marked smooth.
Grid findings are the four existing x=244 anchor positions in isolated Waw;
all new outline points and advances are on 8. No automatic grade or release
approval follows from these checks.
