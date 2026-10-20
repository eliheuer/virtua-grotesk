# HEB-002 — He, Het and Tav

Date: 2026-10-19. Status: **candidate v2 applied; live proof UI pass ready to move on**.
Eli confirmed readiness after the custom-text editor pass and requested a durable,
agent-neutral workflow map. See [Virtua Design Review](../../README.md) for the
handoff and next-session instructions. No new glyph edits are part of that handoff.
Scope: `he-hb`, `het-hb`, `tav-hb` in Regular and Bold. The six approved drawings
are now active; review colors remain unchanged. The initial comparison below is historical;
[the candidate review](#candidate-v2--8-grid-review) records the accepted trial.
See [the application receipt](application-v2.json) for current verification.

## Initial feedback and scope

Eli approved the refined DesignBot layout as the standard, asked to see the next
Hebrew group beside Rubik and Noto, and requested proposed corrections. This
authorizes inspection and comparison; preparation/application of a drawing
candidate remains the next decision. The later mixed Latin–Hebrew running-text
review and Arabic sequence are recorded in the [shared workflow](../../FEEDBACK.md#next-phases).

## Initial comparison

Within each sample read right to left: he ה, het ח, tav ת. Columns are current
Virtua, Rubik and Noto Sans Hebrew; rows are weights 400, 550 and 700. References
reuse the exact cached binaries from HEB-001, not newly fetched releases.

| Sheet | Light | Dark |
| --- | --- | --- |
| He, Het and Tav | [Light](01-form-light.png) | [Dark](01-form-dark.png) |
| Reading Texture | [Light](02-text-light.png) | [Dark](02-text-dark.png) |
| Latin and Hebrew | [Light](03-weight-light.png) | [Dark](03-weight-dark.png) |

The form and Latin-context sheets use a fixed 160 px/em for all fonts and
scripts. This explicit group-wide size fits the three letters in each column;
there is no per-font scaling. Reading samples use 44, 32 and 24 px/em. Weight
coordinates are checkpoints, not optical weight matches. The word line includes
yod, whose existing Bold weight makes the uneven Virtua texture particularly clear.

## Measurements and findings

The three source outlines and advances are identical between masters. Compiled
outlines are also identical at 400, 550 and 700. Their lack of weight growth is
real, not a rendering or variation-selection problem.

| Glyph | Advance, both masters | Straight stems | Flat top bar | Other detail |
| --- | ---: | --- | ---: | --- |
| He | 574 | Left 84; right 86 | 78 | Detached leg ends at y=374; underside of roof y=498 |
| Het | 588 | Left 86; right 88 | 80 | Closed upper-left connection |
| Tav | 630 | Left 88 in straight section; right 86 | 80 | Leftmost ink x=14; right sidebearing 56 |

All flat tops sit at y=576. Regular labels are orange. Bold labels are blue
(`0.27,0.44,1,1`), although these GLIFs contain standalone contours, not components.
Do not reinterpret blue as AI-generated or silently recolor them. A future
candidate must preserve the useful existing design and report any structural edits.

Agent visual assessment: these are a coherent next family because their roofs
and right shoulders connect naturally to the reviewed resh. Regular is lighter
than the provisional pair; Bold is severely underweight. Their sharp, unbeveled
terminals also lack Virtua's characteristic finish. Rubik and Noto demonstrate
weight growth and the distinct left-side structures, but their exact proportions
and corner treatments are not targets to copy. Both scoped curve-lint runs are
clean; the proposed shoulder refinement is a design judgment, not a claimed lint failure.

## Proposed scratch changes

1. **Weight progression:** use the reviewed pair's 96/192-unit stems and 96/168
   flat bars as a starting trial, checked against live green Latin. Keep these
   provisional, allowing a different optical balance after review. Build a real
   Bold with compatible outlines and inspect the midpoint.
2. **Common construction:** make the roof/right-shoulder weight coherent with
   resh and the green Latin shoulder references. Preserve each letter's identity;
   add 16-unit chamfers to appropriate exposed straight corners, with smooth
   curves through the shoulder. Avoid mechanically copying one whole glyph.
3. **He:** preserve a clearly detached left leg, with an open gap that remains
   obvious at small sizes and Bold. Evaluate leg height and thickness together.
4. **Het:** keep the left leg joined to the roof while opening the counter enough
   to prevent the heavier junction from becoming a dark plug.
5. **Tav:** retain the recognizable left foot, but give its curve, terminal and
   projection a more deliberate relationship to the stems. Check the tight left
   bearing in text before proposing a spacing change.

Begin with the current height, advances and anchors; report any necessary spacing
change separately rather than hiding it in an outline edit. Proof the six scratch
GLIFs against the unchanged current font, references, Latin and the applied pair,
including small text, midpoint, and mark attachment. `hedagesh-hb` and
`tavdagesh-hb` are standalone outlines, so changes will not propagate to them;
show them as dependent review targets and name any later edit scope explicitly.

Question for the next candidate: can these three share the provisional pair's
weight and finish while preserving he/het distinction and tav's characteristic foot?

## Initial comparison verification and reproduction

[Evidence](evidence.json) records source and font identities, reference provenance,
render commands and selected output hashes. All six final sheets and three grid
overlays were visually inspected. Font coverage, axis, palette and ink-bound checks
pass. The extended renderer reproduces all six approved HEB-001 v2 pages pixel
for pixel. All 1,759 source files match the already-applied snapshot; no build or
full release-QA rerun was needed for this read-only font review.

Use the [standard runner](../../../documentation/qa.md#standard-designbot-comparison-workflow) with
`--group he-het-tav`, supplying the current VF to both Virtua arguments. This
current-only group has three columns and no candidate column. The retained JSON
contains the exact invocation and input hashes. The long-text specimen is a later
design task with Eli, not part of this group comparison.


## Candidate authorization and style clarification — 2026-10-19

Eli: “make the he, het and tav candidate in both masters using the Latin and
dalet/resh weight as reference. Keep it in scratch and show me the before and
after next to Rubik and Noto.” Also: “the whole font uses a consistent chamfer
style similar to the font replica.” Eli then requested persistent design context.

Interpretation: six named scratch GLIFs, including the blue Bold sources; preserve
existing useful structures and review colors. Application to active sources is
not authorized. The outline screenshot attached in chat confirms straight bevels
combined with controlled curves. Its supplied Desktop path was unavailable during
this run, so it is not copied here. It was not calibrated or traced; dimensions
and borrowed curve runs come from live green UFO outlines.

The canonical design context is now explicit in
[DESIGN.md](../../../DESIGN.md#applying-the-drawing-style-across-scripts): green
Virtua is the construction authority; Rubik/Noto are script references. Record
confirmed reusable style there and provisional glyph decisions here. No new
parallel design specification is needed.

First scratch trial (v1, superseded by the grid correction below): 96/192 stems and 96/168 roof bars, with 16-unit exposed chamfers
and 8-unit internal cuts. He keeps two contours; het and tav each keep one.
Shoulders reuse green n's exact outer quadrant by translation and the applied
resh's inner-arc construction. Tav's foot reuses green j's hook translated
+40 x and +200 y, including its deliberate Bold optical coordinates. Its foot
thickness is therefore 80 Regular and 132 Bold, not forced to the roof thickness.

To avoid closing the two-stem counters, this trial adds 96 units to each Bold
advance. Regular advances remain 574, 588, 630; Bold becomes
670, 684, 726. Bold central anchors move +48 x, right-side cantillation anchors
+96 x; left-side anchors and every anchor y remain unchanged. These spacing and
anchor choices are part of the scratch proposal, not approved global rules.


## Candidate v2 — 8-grid review

Eli's follow-up: new drawings must conform to the published pop-count and
power-of-two grid system by default, so future human-approved green drawings
can contribute useful training data. [The article](https://elih.net/blog/virtua-grotesk/)
and DESIGN.md distinguish positional lattice from measurement decomposition.
The first trial's inherited off-8 widths and Bold j optical coordinates did not
meet the machine-draft rule. V2 corrects those in scratch; the green donors and
all active sources remain untouched.

### Construction and spacing

- Regular/Bold stems: **96/192**; roof bars: **96/168**. Weight is provisional.
- Exposed straight corners: **16-unit, 45-degree chamfers**, both masters.
  Tight internal joins use **8**. Green H/E are the corner references.
- Outer shoulders retain the translated green n quadrant. Inner shoulders use
  the applied resh construction. Both remain smooth at their tangent nodes.
- Tav's foot follows green j's hook construction. Regular is an exact translated
  curve run. Bold adapts j's 4-grid optical coordinates to an 8-grid draft while
  keeping horizontal/vertical tangents. Foot thickness is **80/136**. This is
  an explicit adaptation, not a claim that every donor coordinate is copied.
- He retains a **104-unit roof-to-leg gap** in each master. Het remains joined;
  tav retains its projecting foot. All flat tops are at y=576.

| Glyph | Advance before, both | Candidate Regular | Candidate Bold | Left/right sidebearings, both |
| --- | ---: | ---: | ---: | --- |
| He | 574 | 576 | 672 | 56 / 56 |
| Het | 588 | 592 | 688 | 56 / 56 |
| Tav | 630 | 632 | 728 | 16 / 56 |

Bold adds 96 advance units relative to Regular to preserve counter space.
These advances have popcounts 2/3 (he), 3/4 (het), and 5/5 (tav), respectively.
They are intentionally retained on the 8-grid for the proposed spacing; reducing
the popcount alone would not justify changing that spacing.
Before snapping to 8, Bold central anchors move +48 x and right cantillation
anchors +96 x; left anchors retain their positions. All candidate anchors then
land on 8, with at most a 4-unit adjustment per coordinate. The full before/after
anchor table is in [validation](candidate-v2-validation.json). This includes
hbCenter y=332→336 for he/tav. Nothing is hidden as an outline-only change.

### Review sheets

All references use the same px/em and weight coordinates within a row; these
coordinates are not claims of equal optical weight. The labels use Virtua;
rendering is DesignBot Rust, two reversible grays, title case and tight headlines.

| Sheet | Light | Dark |
| --- | --- | --- |
| Before, candidate, Rubik and Noto | [Light](candidate-v2-01-form-light.png) | [Dark](candidate-v2-01-form-dark.png) |
| Reading texture | [Light](candidate-v2-02-text-light.png) | [Dark](candidate-v2-02-text-dark.png) |
| Green Latin and candidate Hebrew | [Light](candidate-v2-03-weight-light.png) | [Dark](candidate-v2-03-weight-dark.png) |
| He detail | [Light](candidate-v2-04-detail-he-light.png) | [Dark](candidate-v2-04-detail-he-dark.png) |
| Het detail | [Light](candidate-v2-05-detail-het-light.png) | [Dark](candidate-v2-05-detail-het-dark.png) |
| Tav detail | [Light](candidate-v2-06-detail-tav-light.png) | [Dark](candidate-v2-06-detail-tav-dark.png) |
| Marks and related forms | [Light](candidate-v2-07-marks-light.png) | [Dark](candidate-v2-07-marks-dark.png) |

Agent assessment: the candidate brings these letters into Virtua's chamfered
construction and corrects the absent Bold weight growth. He remains visibly
detached; tav's foot is deliberate and compatible across weights. The heavy
texture should still be judged by Eli beside the green Latin and later running
text. No glyph is graded or approved by this assessment.

The bottom line of each marks sample shows **unchanged precomposed he/tav with
dagesh** (U+FB34/U+FB4A). These are standalone drawings and do not inherit the
plain-letter corrections. They need a named follow-up if this direction is
approved. Normal decomposed base-plus-mark shaping uses the new candidate bases.

### Checks and retained evidence

[Evidence](candidate-v2-evidence.json) ties the proofs, source snapshots, donor
hashes and exact font binaries together. Reproduce with `prepare_candidate.py
--output <new out/qa directory> --write`, then build inside that directory.
The script rejects drift in target or reference sources rather than silently
claiming the same trial. `validate_candidate.py <directory>` verifies scope,
compiled changes and mark intersections. The standard renderer invocation is
retained in the evidence JSON.

- Strict source grid: **six glyph-masters pass**, all 160 outline points,
  handles, 60 anchors, advances and actual sidebearings on 8. Popcount remains
  descriptive, with no arbitrary maximum or human grade.
- Both curve-lint runs clean; full master compatibility has **0 blockers**.
- Scratch build/preflight succeeds: VF, four statics, main PDF and reports.
  Artifact presence alone is not release approval.
- **25 unit tests pass**, including five tests for the draft gate.
- **6,048 compiled glyph/weight comparisons**: only he, het and tav outlines
  and advances differ, across seven weights. All 1,759 active source files
  match the frozen input hashes. Colors and Unicode assignments are preserved.
- Hebrew shaping audit passes; **294 base/mark checks** across baseline and
  candidate at seven weights have no ink intersections. This is not exhaustive
  script or native-reader review.
- Scoped Fontspector 1.9.0 outline/overlap/interpolation run: **19 PASS, 13 WARN,
  8 SKIP, 0 FAIL**, identical findings to the baseline. No new warnings and no
  exclusions added. This is not a full Google Fonts release QA run.
- All 14 final images and the layout-grid overlay inspected. Six default dalet/resh layout regression images
  remain pixel-identical to the approved design.

### Existing grid debt and training boundary

The [active-source inventory](candidate-v2-active-grid-inventory.json) found
**1,369 off-2 outline points across 154 glyph/master pairs** and **311 off-8
advances**. It covers default-layer source points and advances, not every
component transform, anchor, kerning value or design property. Raw review colors
are preserved in the inventory. The older grid lint conflates several colors
with orange, so its color labels must not be used as permission to edit.

This audit does not authorize automatic snapping of green drawings. Review
existing violations in scoped batches, keep intentional on-2 optical corrections
separate from genuine off-2 defects, and preserve curves and the evidence trail.
HEB-002 is still an ungraded machine draft. Its before/candidate GLIF snapshots,
source identities and proofs are retained here so Eli's later corrections can
be captured as an explicit draft-to-approved pair rather than mislabeled as
already-good training data.


## Application approval and specimen correction — 2026-10-19

Eli: “this looks good! you can apply these,” followed by a request to stop
Hebrew expansion and redesign the specimens. Applied exactly the six approved
GLIF snapshots; colors stay unchanged. See [application receipt](application-v2.json).

The prior specimen layout is superseded for future work: labels were too far
from samples, the grid did not produce clear grouping, and negative space felt
unconsidered. The next layout must bring labels into direct relationship with
their content and organize comparison rows with a coherent rail and columns.
This is a new layout proposal, not an approved visual result.


## Specimen layout v3 and supplied references — 2026-10-19

State: **new layout proposal awaiting Eli's review**. The glyph application is
approved and complete; further Hebrew drawing is paused while the presentation
is refined. The first v3 render was further adjusted after Eli supplied eight
reference images and asked for a grid that can be toggled in DesignBot.

The references show related ideas rather than one template to copy: compact
caption groups beside large forms; consistent column and row gutters; strong
size hierarchy; common alignment lines; and large empty regions used to separate
content groups. The poster-grid screenshots explicitly distinguish content
modules from a finer baseline grid. The Experimental Jetset covers demonstrate
close relationships between text and dominant letterforms. Colored artwork,
all-caps and repeated slashes in those references do not supersede Eli's earlier
palette and casing preferences.

The eight references were supplied in chat as Screenshot 2026-10-19 at
1.04.51 PM, 1.05.03 PM, 1.02.42 PM, 1.03.09 PM, 1.03.30 PM, 1.03.44 PM,
1.04.11 PM and 1.04.46 PM. The supplied Desktop files were unavailable to this
checkout; these notes describe the visible attachments, not retained image files
or calibrated measurements.

Implementation:

- Shorter 1600 × 1120 page; 80 px outside margins. A 128 px weight-label rail
  and 32 px gutter put the comparison field at x=240.
- Four columns of 296 px with 32 px gutters; three-column sheets use 384 px
  columns with 64 px gutters. Labels sit directly above the comparison field;
  weight labels sit beside the relevant sample rows.
- Body modules run from y=312 to y=1016: three 192 px rows with 64 px gutters,
  or two 304 px rows with 96 px gutters for enlarged details. Rules fall at
  gutter centers. This geometry drives both layout and overlay.
- Separate 8 px baseline guides. `--grid` shows structure; `--baseline-grid`
  adds baselines; omit both for clean output. Direct Rust rendering accepts
  `GRID_VIEW=0`, `1` or `baseline`.
- Virtua captions remain Regular, title case and two grays. The headline is
  reduced to 56 px, tracked −0.02 em. The main letterform sample now uses the
  contiguous string `החת` at a common 136 px/em; the old spaced 120 px/em
  sample remains in historical v2 evidence. No font is individually fitted.

The new local proof viewer switches among the three main sheets, both themes
and off/structural/baseline guide modes. These are DesignBot-rendered PNGs;
the viewer does not substitute browser font rendering for specimen shaping.
The viewer and retained exports are in [layout-v3](layout-v3/index.html).
These controls are a local review aid, not a new native DesignBot application UI.

The earlier v2 recipe and images are retained. No numerical layout or pixel check
constitutes aesthetic approval; Eli's next feedback should revise this record.

### V3 verification

Retained [clean letterforms](layout-v3/clean/01-form-light.png),
[structural grid](layout-v3/structure/01-form-light.png), and
[baseline grid](layout-v3/baseline/01-form-dark.png) are exports of the
[same frozen Rust recipe](layout-v3/recipe.rs). The viewer switches those exports;
it does not reshape the samples. All 14 clean pages were inspected, with the
three comparison pages and grid variants checked separately. No clipping or
label collisions were seen. This is an agent review, not Eli's layout approval.

The initial parallel export attempt collided in DesignBot's shared script
cache: a successful process wrote another invocation's output. Those results
were discarded and all 26 exports regenerated sequentially. The runner now
serializes DesignBot subprocesses with a local file lock. Output dimensions,
neutral opaque palette, font identities and hashes are checked for each set.

The browser viewer was checked for sheet selection, light/dark, structure,
baselines, and switching guides off. Open `layout-v3/index.html` locally, or
serve that folder with a local HTTP server. The labels font in `layout-v3/fonts/`
is an ignored local build copy; recreate it from `fonts/ttf/VirtuaGrotesk-Regular.ttf`
after a fresh checkout. The PNG specimens already include their labels.

## Live browser review — 2026-10-19

Eli questioned the move from images to a web view, then explicitly requested
live rendering throughout: “we don’t have to do the images.” The previous viewer
only scaled PNGs. At the inspected 455 px panel width, its 1600 px sheet was
reduced to 28.4%; a 22 px label became approximately 6.3 CSS px high. That was
a presentation defect, not evidence of a bad outline.

The same [local entry point](layout-v3/index.html) now renders the four verified
font files directly. The old viewer is retained as `layout-v3/image-viewer.html`.
No glyph sources or font binaries were changed in this pass. Live comparison
preserves equal em size and native browser metrics; the browser handles shaping
and rasterization. It is visually distinct from DesignBot's fixed raster output.

The prototype borrows the useful interaction ideas of
[Diffenator3 / diff3proof](https://github.com/googlefonts/diffenator3): browser
proofs, variation settings and switching between font revisions. The installed
local diff3proof template was inspected; this custom interface does not execute
Diffenator checks or copy its implementation. Existing QA remains separate.

The first audit found: (1) severe downscaling and unreadable captions, (2) no
independent specimen size/weight controls, (3) unclear distinction between image
viewing and live type. The live view addresses those findings with responsive
columns, readable labels, equal-size native text, in-place switching and explicit
renderer identification. The exact visual treatment remains a trial for Eli.

Validation includes font-hash verification, supported-character checks, three
weight presets, size changes, before/applied button and B-key switching, custom
text, missing-character feedback, reference visibility, grid and dark mode.
A generated screenshot is review evidence, not a specimen-image dependency.
See [live comparison](layout-v3/live-compare.png) and the preserved
[previous viewer](layout-v3/viewer-before-live.png). Browser behavior was checked
in the in-app browser; this is not a cross-browser or native-reader signoff.

### Direction confirmed; drawing paused

On 2026-10-19 Eli confirmed that live web review is easier to work with than the
images and should be the default. Eli requested an intensive UI/UX pass before
continuing Hebrew, and clear discovery instructions for other agents. The
current work plan and launch instructions are maintained in the
[web-proof guide](../../app/README.md), linked from AGENTS.md,
the root README, the documentation index and the rendering skill. This approves
the workflow direction, not the current layout as final. No glyphs changed in
this documentation and launcher pass.

## First UI/UX pass — 2026-10-19

Eli requested a careful Swiss grid and supplied four Klim Die Grotesk screenshots
(14:03:07, 14:03:22, 14:03:39 and 14:03:52). The useful direction is compact
controls aligned with specimens, close labels, clear type hierarchy and deliberate
negative space. The orange palette, sales navigation and specimen text are not
part of the request. Two grays and Virtua labels remain required.

The audit found that the previous controls occupied roughly 500 px vertically,
references fell below the comparison, and Sizes required reading down a whole
font column before reaching the next font. The new trial reduces the control
area, uses a common four-column structure and compares each size across fonts.
Compare keeps before/applied adjacent to Rubik/Noto; Switch preserves reference
positions while toggling Virtua. Weight and size have numerical fields, sliders
and shortcuts. Grid exposes the page columns and an 8 px spacing guide.

Baseline alignment adjusts line-box offsets only; em size, outlines and tracking
remain unchanged. Equal caption heights prevent wrapped names from displacing
samples. RTL overflow starts at the reading edge and scrolling is synchronized.
Unsupported characters still block rendering per font rather than falling back.

Actual in-app browser inspection covered the current panel widths (approximately
658–774 CSS px), light/dark, guides, Compare, Switch and B shortcut, Sizes,
intermediate weights, presets, slider keyboard input, custom mixed text and
missing-character feedback. Baselines agreed within browser subpixel rounding;
RTL horizontal scrolling produced matching offsets in all four samples. Wide
windows, the below-600 two-column breakpoint, other browsers and prolonged use
still need visual review. No font sources were changed by this UI pass.

Evidence: [light comparison](layout-v3/ui-pass-01-light.png),
[dark grid](layout-v3/ui-pass-01-dark-grid.png),
[verification](layout-v3/ui-pass-01-verification.json). Canonical code and launch
instructions remain in the [web-proof guide](../../app/README.md).
The implementation is proposed and agent-checked; Eli has not approved this
layout as final. Hebrew drawing remains paused.

## Second UI/UX pass — 2026-10-19

Eli said the interface was improving but the headline hierarchy and control area
still felt messy. Requested corrections: give “Virtua Grotesk” the same headline
size as “He, Het and Tav”; darken the background to match the supplied address
bar; simplify to core information. The screenshot’s address-bar fill measures
roughly RGB 40/40/40 (`#282828`), with small gradient variation. P019/P020 record
these directions for later agents.

Both headlines now share one responsive size, leading and tracking token. The
sample, weight and size values align on a single row. Numerical fields and
sliders remain; preset rows, the repeated sample/size summary, the study eyebrow
and the extra masthead subtitle are removed. Applied/provisional state moves to
a quiet footer, with provenance and longer explanations inside Review Details.
In Sizes, the size control shows its actual range. The grid is quieter and uses
the same shared columns; keyboard focus remains visible. Dark paper is
`#282828` / ink `#dedede`; the light palette remains unchanged.

This implements the requested direction; the exact revised layout remains open
for feedback. Glyph scope: none. Font snapshots retain their recorded identities.
Actual browser checks cover matched headline styles, equal sample scale and
baselines, numerical controls, B switching with references, Sizes, light/dark,
guides and expandable details at the current panel width. Wider/narrower and
cross-browser visual review remain pending.

Evidence: [dark](layout-v3/ui-pass-02-dark.png),
[light](layout-v3/ui-pass-02-light.png),
[grid](layout-v3/ui-pass-02-grid.png),
[verification](layout-v3/ui-pass-02-verification.json).

## Responsive fitting — 2026-10-19

Eli’s 15:15:45 screenshot showed the three-glyph run clipped in every narrow
column. Requested correction: “make this responsive to fit the available space.”
P021 supersedes default scrolling for live comparison.

Fit is now on by default. A native-font measurement calculates one shared size
for all visible fonts, including both Virtua revisions when switching. The size
readout shows the actual rendered size; the current fixed-size setting caps
automatic enlargement. Turning Fit off restores the numerical/slider controls
and linked scrolling. Responsive fitting changes CSS font size, never outline
geometry or per-font scale. Text wraps if fitting reaches 16 px. Size studies
keep their explicit em sizes and reduce columns when a run needs more width.

The current panel’s group sample fits at 76 px instead of clipping at 128 px.
Native same-origin frame checks at 360/480/960/1440 px produced shared sizes
72/102/100/128 px, respectively, with no page or sample horizontal overflow.
The 360 px layout was visually inspected; larger frame widths were measured.
The live panel and large size-study rows were visually inspected. Also checked:
long custom text wrapping at 16 px, stable B switching at 76 px, and opting out
to fixed 128 px. Browser warning/error log was empty. No glyph work occurred.

Evidence: [fitted group](layout-v3/ui-pass-03-fit.png),
[narrow layout](layout-v3/ui-pass-03-narrow.png),
[verification](layout-v3/ui-pass-03-verification.json).

## Unified spacing — 2026-10-19

Eli’s annotated 15:23:23 screenshot identifies inconsistent headline, section,
slider and sample gaps. The requested system uses the side margin as a base
unit, with halves and multiples for every space. P022 records that direction.

The CSS now derives layout spacing from one responsive U: 32 px wide, 24 px
medium, 20 px narrow. Gutters and smaller gaps use U/2; caption gaps use U/4.
Headline padding, controls, row intervals, footer and guides use the same tokens.
Native select/value fields retain sufficient text height at the narrow breakpoint.
There are no extra proof-row/footer paddings stacked beneath the sample.

The old sample box included asymmetric native-font leading. Browser ink metrics
now place the shared baseline inside a field with U above the maximum ink ascent
and U below the maximum descent. This preserves equal em size and baseline,
rather than independently centering each reference. Marks and wrapped-line
height are included. Headline/caption line-box trimming removes metric padding
from those relationships in the current browser. Visible text remains native.

Checks: native frames at 360/480/736/960/1440 px, with no horizontal overflow.
The slider’s measured upper/lower intervals equal U in every case: 20/20, 20/20,
24/24, 32/32 and 32/32 px. The sample ink field has a minimum top inset U and
bottom inset U; naturally shorter reference forms retain their proportions.
Also visually inspected: current panel, narrow/medium frames, Bold marked
Hebrew, wrapped Latin/Hebrew with descenders, Switch and Sizes. Wider frames
were measured rather than visually inspected in full. This is a proposed
implementation of the requested system, still open to layout feedback.

Evidence: [clean dark](layout-v3/ui-pass-04-dark.png),
[clean light](layout-v3/ui-pass-04-light.png),
[grid](layout-v3/ui-pass-04-grid.png),
[narrow](layout-v3/ui-pass-04-narrow.png),
[verification](layout-v3/ui-pass-04-verification.json).
The maintained [spacing contract](../../app/README.md#spacing-contract-p022)
owns the component mapping for future edits. Glyph scope: none.

## Running text and glyph identities — 2026-10-19

Eli requested large blocks of running text during glyph work (15:34:30 reference),
then asked for Hebrew forms, Latin names and Unicode together in the study
heading (15:37:46/15:37:56 references). P023/P024 record both directions. This
moves the first text prototype earlier than the previous alphabet-first plan.

Reading now provides three original Hebrew paragraphs and three mixed-language
paragraphs, identical across before/applied, Rubik and Noto. The initial size is
24 CSS px with 36 px leading; size can be changed from 16 to 72 and weight from
400 to 700. Fit is disabled. Equal-width columns reflow 4/2/1 by available width.
Paragraphs wrap naturally, allowing text density, spacing and script transitions
to be compared. English phrases and numbers use explicit bidi isolation. The
shared first baseline is aligned; later paragraph endings reflect natural reflow.
The corpus is maintained in reading-samples.json and bundled by prepare.py.

The heading now groups each Hebrew form with its Latin name and a smaller code
point. Individual glyph selector entries contain the same three identifiers.
Both derive from one metadata list, avoiding mismatched names or code points.

Checks include actual Hebrew and mixed-paragraph inspection in Virtua, Rubik and
Noto; matching text, size/leading, column widths and first baselines; corpus cmap
coverage; responsive 360/736/1440 native-frame checks; Unicode identity labels;
size and weight changes; mode-size restoration; custom text and unsupported
character feedback. The current narrow/medium layout was visually inspected;
wide layouts were measured. Sources and font snapshots are unchanged. This is
an implemented prototype for feedback, not approval of Hebrew editorial content
or a completed typographic design review.

Evidence: [Reading](layout-v3/ui-pass-05-reading.png),
[light Reading](layout-v3/ui-pass-05-reading-light.png),
[glyph identities](layout-v3/ui-pass-05-glyph-labels.png),
[narrow](layout-v3/ui-pass-05-narrow.png),
[verification](layout-v3/ui-pass-05-verification.json).

## Mode naming and separation — 2026-10-19

Eli requested Compare / Toggle / Size / Text and a horizontal rule above the
mode bar (15:52:11 screenshot). Those visible names are implemented; internal
mode identifiers retain their existing behavior. The new top rule shares the
comparison width, and U/2 padding balances the bar’s upper/lower insets. This
correction is recorded as P025. The live browser was inspected after preparation;
mode switching, font snapshots and JavaScript syntax were checked.

Evidence: [updated navigation](layout-v3/ui-pass-06-navigation.png).

## Inset rule and Text control spacing — 2026-10-19

Eli requested a margin-aligned masthead divider and removal of the distracting
reflow explanation/extra gap below the sliders (16:18:46 screenshot). P026
records the correction. The masthead rule now spans only the content width.
Text rendering information moves into Review Details rather than occupying a
separate row in the proof controls.

The Text gap measured 64.79 px at U=24: the reflow line added 16.80 px of text
height plus a 24 px bottom margin. Removing that row returns the gap to U=24,
matching the track-to-field interval above. Compare already used that interval.
The live result and both mode transitions were inspected after preparation.

Verification also exposed cached JavaScript being reused with new HTML.
Preparation now versions scripts, styles, data and the label font by content
hash. A fresh reload and Compare/Text transitions load the proof successfully.

Evidence: [corrected Text controls](layout-v3/ui-pass-07-controls.png).

## Unified interface typography — 2026-10-19

Eli requested inline family/role captions, no Applied underline, no px suffix
on Size, and the navigation text size for control labels and values (16:41:41
screenshot). Recorded as P027. All these primary UI elements now share the
14 CSS px `--ui` token across breakpoints. Captions use a center dot and wrap
only when the available width requires it. Headline and font specimen sizes
retain their separate purposes. No glyph sources or font snapshots changed.

Evidence: [unified typography](layout-v3/ui-pass-08-typography.png).

## Sample menu and checkbox refinement — 2026-10-19

Eli rejected the platform dropdown's appearance and oversized checkbox marks
(16:46:35 screenshot). P028 records the direction. The proposed replacement is
a field-width listbox with restrained rules, no shadow, inverted two-gray active
state, shared UI typography and U/2 option insets. All checkbox boxes are 12 px
with finer inset ticks, including Fit. The label remains part of each hit target.

The live menu was inspected in light and dark themes. Pointer selection, arrow
navigation and Enter, Escape without committing, Tab to Weight, and the Your Text
field were exercised. Font snapshots are unchanged; no drawing edits are included.

Evidence: [dark menu](layout-v3/ui-pass-09-menu-dark.png),
[light menu](layout-v3/ui-pass-09-menu-light.png).

## Checkbox clearance and Unicode size — 2026-10-19

Eli clarified that smaller marks means greater margin inside each checkbox,
not thinner strokes (16:52:20 screenshot). The prior border construction added
stroke outside its stated size. The replacement explicitly uses border-box
dimensions: 5 × 3 px with a 1.5 px stroke inside an unchanged 12 px checkbox.
The rotated mark occupies about 5.66 px, leaving over 2 px inside the border.
P029 records this correction rather than treating the lighter marks as approved.

The Unicode labels were still 12 px; they now share the navigation's 14 px UI
token. Remaining footer/hint/diagnostic size overrides were removed too, keeping
the distinction between UI, headline and specimen type. The live computed sizes
were checked, and the smaller inset ticks were visually inspected.

Evidence: [corrected tick clearance and labels](layout-v3/ui-pass-10-inset.png).

## Fill comparison columns by default — 2026-10-19

Eli requested larger default Compare samples that fill their columns and grow
when References is disabled (16:58:19 and 16:58:50 screenshots). P030 supersedes
the earlier implementation's fixed-size cap. Fit now measures the runs at one
em and calculates the largest common size that fits every required column,
including both revisions in Toggle. It is independent of the fixed-size control.
Relative widths and shared baselines are preserved rather than stretching each
font separately. The existing 16 px minimum remains for long wrapping samples.

In the live panel, he grew from the previous 128 px cap to 272 px with references
and 638 px without references. All visible fonts shared the reported size and
baseline, with no horizontal overflow. Fit off restored the independent 128 px
setting; Toggle stayed at 272 px for both revisions. Marks fitted at 32 px without
horizontal overflow. These measurements describe this window, not fixed defaults.
No font sources or snapshot files were changed.

Evidence: [four columns](layout-v3/ui-pass-11-fit-four.png),
[two columns](layout-v3/ui-pass-11-fit-two.png),
[measurements](layout-v3/ui-pass-11-verification.json).

## Mid-gray light paper — 2026-10-19

Eli found light mode too bright and requested paper closer to a mid-tone gray
(P031). Light paper is now #a8a8a8 instead of #dedede, retaining #444444 ink.
The exact shade is an implementation choice for review. Dark mode is unchanged.

Live inspection also exposed a fractional-width fitting edge case: rounded
clientWidth allowed Noto to wrap at 266 px in this panel. Fit now uses the
actual fractional column width; at 265 px all four runs remain on one line.
No sources or font snapshots changed.

Evidence: [mid-gray light proof](layout-v3/ui-pass-12-gray.png).

## Independent neutral palettes — 2026-10-19

Eli requested darker charcoal closer to the surrounding app area and independent
light/dark colors, all without saturation (17:05:32 screenshot, P032). The
supplied screenshot's surrounding area is dominated by neutral RGB 23 and 25.
The proposed charcoal is #181818: light uses it for ink on #a8a8a8 paper; dark
uses it for paper with #dedede ink. Four separate CSS tokens define the palettes
instead of swapping two values. All RGB channels are equal.

Both live themes were visually inspected and their computed RGB values verified.
Font sources and snapshots are unchanged.

Evidence: [light](layout-v3/ui-pass-13-neutral-light.png),
[dark](layout-v3/ui-pass-13-neutral-dark.png).

## Light ink midpoint — 2026-10-19

Eli found #181818 too dark on the light background and requested a halfway
point toward the previous #444444. Light ink is now #2e2e2e, the exact
RGB-channel midpoint (P033). Light paper and the dark palette are unchanged.

Evidence: [midpoint light ink](layout-v3/ui-pass-14-midpoint.png).

## Toggle spacing pass — 2026-10-19

Eli considers Compare satisfactory for now and requested a Toggle margin pass
(P034). The 17:17:24 screenshot attachment was unavailable; the current live
Toggle page was inspected directly. Its separate revision toolbar introduced
an extra vertical interval, while the 2:1:1 panel allocation left disproportionate
empty space beside Virtua and constrained the common fitted scale.

Before/Applied now occupies Sample's unused slider row. The selector center
matches the Weight track center; the proof starts at exactly the same height
as Compare. The floating B hint moves into Review Details and the selector's
tooltip. Desktop Toggle uses three equal columns; narrow layouts retain the
full-width Virtua row with references beneath. Compare's layout is unchanged.

Live checks found equal panel widths, identical selector/slider centers, and
identical caption top, fitted size and baseline for Before/Applied. The B
shortcut returns to Applied. Compare retains four panels with the revision
control hidden and the same proof top. This layout remains a review proposal.
Font sources and snapshots are unchanged.

Evidence: [Toggle layout](layout-v3/ui-pass-15-toggle.png),
[measurements](layout-v3/ui-pass-15-verification.json).

## Full-width revision selector — 2026-10-19

Eli requested the Before/Applied selector span its column and suggested placing
the keyboard hint between Text and References (P035). The selector now fills the
Sample field width, with equal button halves. “Press B to toggle” appears only
in Toggle's mode bar and wraps beneath the tabs on narrow screens.

Live measurement confirmed identical Sample/selector widths and equal buttons.
B changes the revision; both selector and hint disappear in Compare. The proof
spacing and three-column Toggle layout are retained. No font files changed.

Evidence: [full-width selector and shortcut](layout-v3/ui-pass-16-toggle-controls.png).

## Shared mode-bar baseline — 2026-10-19

Eli identified References as misaligned and possibly smaller (17:28:30
screenshot, P036). Its size was already 14 px, but its centered flex layout and
untrimmed anonymous text used different vertical metrics than the tabs. The
mode bar and navigation now align on text baselines. References has a separate
trimmed text span; the checkbox centers independently instead of setting that
baseline. No individual pixel offset is used.

Live computed type is 14 px for tabs, hint and References. Their alphabetic
baselines match within browser rounding (about 0.001 px in this panel).

Evidence: [aligned mode bar](layout-v3/ui-pass-17-baseline.png).

## Continuous Waterfall — 2026-10-19

Eli rejected the repeated Size rows and broken inactive size controls (17:29:24
screenshot). P037 records the requested Waterfall: one label per font, the largest
common size fitting the available width first, then descending samples without
visible pixel sizes or repeated separators. Sample and Weight now occupy equal
control columns; the Size/Fit controls are omitted in this mode.

The implementation gives each font one intact vertical stack. Eight logarithmic
steps descend to 16 px, collapsing rounded duplicates. These numerical choices
remain adjustable. Each step shares its em size and baseline across all fonts.
U/2 ink insets between samples give U of space; first/last outside insets stay U.
Narrow layouts wrap whole font stacks rather than interleaving unlabeled rows.

The live waterfall was inspected through its smallest samples. Four labels appear
once; no pixel labels remain. In this panel the sequence began at 266 px with
references and 625 px without them. Bold and marked samples fit without horizontal
overflow. Compare, Toggle and Text restored their controls and normal contents on
mode changes. No font source or snapshot changes are included.

Evidence: [top and controls](layout-v3/ui-pass-18-waterfall-top.png),
[complete descending field](layout-v3/ui-pass-18-waterfall-bottom.png),
[measurements](layout-v3/ui-pass-18-verification.json).

## Concise column captions — 2026-10-19

Eli requested Before, Applied, Rubik and Noto Sans Hebrew, removing repeated
Virtua names and Reference suffixes (17:38:13 screenshot, P038). The shared
panel renderer now uses these captions across Compare, Toggle, Waterfall and
Text; Review Details preserves full family names and snapshot hashes. All four
captions were verified on one line at the shared UI size in the live Waterfall.

Evidence: [simplified captions](layout-v3/ui-pass-19-captions.png).

## Inverted active mode — 2026-10-19

Eli requested a clearer selected-view indicator after noticing the underline
separate from the bottom rule (17:45:48 screenshot, P039). Active tabs now use
inverted paper/ink, matching the revision selector. The old underline is removed.
The mode bar uses U/2 outside insets, U/4 vertical tab padding and U/2 horizontal
padding. References and the shortcut hint retain the same text size and baseline.
Both light and dark active states were visually inspected.

Evidence: [inverted mode tab](layout-v3/ui-pass-20-active-mode.png).

## Restore mode-bar grid after selection styling — 2026-10-19

Eli identified a regression in P039: horizontal tab padding moved Compare off
the established margin. P040 records the requirement to preserve existing
alignments when refining a component. Padding-based highlighting was replaced
with a decorative pseudo-element around a trimmed label. Text stays on its
original grid; the fill does not consume layout width. Original label gaps
and vertical insets were restored.

Live assertions across Compare, Toggle, Waterfall and Text confirmed Compare,
Sample and rule left edges are identical, and every tab shares References’
baseline. All four modes loaded their proof. The selection fill remains inverted.
No font files changed.

Evidence: [restored alignment](layout-v3/ui-pass-21-restored-grid.png),
[mode regression checks](layout-v3/ui-pass-21-verification.json).

## Your Text editor — 2026-10-19

Eli requested a usable editor with a clear divider below the sliders, coherent
label placement, no native resize handle, consistent rule weights and preserved
margins (17:54:51 screenshot, P041). The current entered text and weight/size
settings were read before refreshing and restored after the implementation.

The editor is now a section with a margin-aligned top rule, U/2 heading inset,
and a padded input at the shared UI text size. The input grows/shrinks in U
increments from 4U to 16U, then scrolls internally; the manual resize grip is
removed. Its focus outline uses the same one-pixel stroke as the divider and
sits inside the input bounds. The proof updates while editing as before.

Live geometry confirmed editor, section and Sample left edges match, the right
edge stays inside the section, and the slider-center/divider interval is U.
Computed focus and divider strokes match. Eight lines grew the input, 24 lines
reached its scrolling cap, and two lines shrank it back. Light and dark states
were inspected. The original text survives preset/mode switches; Compare keeps
its margin alignment and four panels, while preset reading text hides the
editor. Original custom text and settings are restored for review. No font
sources or snapshots changed.

Evidence: [editor with preserved text](layout-v3/ui-pass-22-custom-editor.png),
[geometry and behavior checks](layout-v3/ui-pass-22-verification.json).
