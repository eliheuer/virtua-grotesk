# Live web proof

This is the default interface for **Virtua Design Review**. Start with the
[central workflow guide](../README.md) for the current
handoff, drawing context and recovery map. On 2026-10-19 Eli said the interface
was ready to move on after the custom-text editor pass. Continue improving it
through scoped feedback; the historical UI-pass notes below are not a standing
instruction to pause all font work.

## Start here

From the repository root:

```sh
make proof-web
```

Open the printed localhost URL (currently `http://127.0.0.1:60272/`). The launcher
verifies the local font snapshots, reuses the matching server if already
running, and otherwise serves only the review folder. It does not build fonts,
edit sources, or silently replace the before/applied snapshots. To validate
without starting a server:

```sh
.venv/bin/python agent-proofs/serve.py --check
```

Current case: [ARB-004](../cases/arabic-004/README.md), Fathatan placement in both masters.
Served files are under `agent-proofs/cases/arabic-004/working/`.
Previous Hebrew snapshots remain in their case folders.

## Mode names

The visible tabs are **Compare, Toggle, Waterfall, Text** (P025, revised by P037). Earlier notes below
use the former Switch / Sizes / Reading names. Internal data-mode identifiers
remain compare / switch / waterfall / reading. A rule above the bar separates
it from the glyph identities. P042 restores a thick active underline in place
of the inverted fill (superseding P039). The marker spans the tab label width
and joins the lower rule. Labels retain their original positions (Compare
flush with the content margin), shared baseline and UI size. Tabs stretch to
the bar's lower edge so the References control cannot leave a gap beneath the
marker. The original U tab gaps (U/2 on narrow screens) remain.
The masthead rule uses those same page-margin endpoints (P026). Rendering
explanations belong in Review Details, outside the control-to-proof interval;
the slider-to-caption rule interval stays U in Text as well as Compare.

Primary interface text uses one `--ui` size (currently 14 CSS px): navigation,
control labels and values, theme/reference toggles and font captions (P027).
P038 simplifies captions to Before, Applied, Rubik and Noto Sans Hebrew,
without repeated family names, Reference suffixes or status underlines.
Full snapshot identities remain in Review Details.
Allow natural wrapping when a caption cannot fit; never clip it or shrink its
role independently. Size omits the visible px suffix; numeric settings still
use CSS pixels. Headline and specimen scales remain separate from UI text.

The sample picker uses a custom listbox with the field's width, shared UI type,
U/2 option padding, two-gray active state and a thin selected tick (P028). It
replaces the platform popup, including its blue highlight and shadow. The hidden
selects retain sample values; one visible button/listbox follows the active mode.
Arrow keys, Home/End and initial-letter search move the active option; Enter or
Space commits, Escape cancels, Tab closes and continues, and outside clicks close.
The trigger reports expanded state; the focused listbox reports its active option
and selected value. Following P029, checkboxes retain 12 px boxes but use smaller
5 × 3 px border-box ticks with a 1.5 px stroke. The rotated mark fits within about
5.66 px, leaving over 2 px clearance inside each box edge; do not shrink the box
along with the mark. Their labels remain clickable. These component dimensions
are a review proposal. Unicode labels, footer, hints and diagnostics now also
use `--ui`; only headlines and actual specimens use different text sizes.

The themes have independent neutral palettes (P031–P032), not swapped colors:
light uses `#a8a8a8` paper with `#2e2e2e` ink; dark uses `#181818` paper with
`#dedede` ink. P033 adjusts light ink to the channel midpoint between #444444 and #181818.
Dark paper approximates the surrounding app area in Eli’s
screenshot (dominant RGB 23/23/23 and 25/25/25). Every palette value has equal
RGB channels. The four explicit theme tokens keep future adjustments separate.

## Code and evidence

Your Text opens a defined editor section below the controls (P041). Its top rule
is U below the slider centers and shares the page margins. The label sits U/2
below the rule; the textarea uses U/2 internal padding and the shared UI type at
1.5 line spacing. Height grows in U increments from 4U to 16U, then scrolls
internally. It shrinks when text is removed and recalculates on width changes.
There is no manual resize handle. Its one-pixel focus outline is inset so it
cannot extend beyond the margins or add a heavier external frame. Custom text
remains unchanged when moving between samples/modes; proof updates stay live.

- Edit `index.html`, `review.css` and `review.js` **in this directory**.
- `reading-samples.json` owns the original running-text corpus and explicit
  language/direction runs. `prepare.py` bundles it into `review-data.js`.
- The `glyphs` list in `review.js` owns each study glyph’s character and name;
  Unicode labels are derived from those characters for the heading and selector.
- `prepare.py` copies the interface and verified font snapshot into the served
  review folder. See [preparation commands](../../documentation/qa.md#live-browser-review).
  Generated asset URLs include content hashes so browser refreshes load matching
  HTML, scripts, styles and label fonts after an interface change.
- `live-fonts.json` records font hashes; `live-verification.json` records the
  prototype's checks. Keep new claims tied to the files actually reviewed.
- [Design review and feedback](../FEEDBACK.md) owns confirmed
  preferences. The HEB-002 record owns this case's feedback and evidence.

Ordinary builds remain ignored by Git. HEB-002's exact served fonts and licenses
are explicitly retained with the case so a fresh checkout can reopen it. Use
`cases/hebrew-002/layout-v3/snapshot.json` relative to `agent-proofs/` as the
preparation evidence; its font paths resolve relative to the manifest. Historical
receipts keep their original absolute paths. If any recorded asset is unavailable,
report that explicitly.
Never relabel the current font as an old or approved candidate snapshot. For a
new case, prepare new evidence and update the sample/title/state definitions
and launcher target deliberately; this first implementation is HEB-002-specific.

## UI/UX pass

Work in small, visually reviewed iterations. Keep the working prototype usable
between iterations, and record Eli's corrections before expanding the scope.

1. **Comparison layout:** make before/applied and references easy to scan in
   narrow panels and wide windows; keep labels attached to their samples and
   make equal size, weight and comparison state obvious.
2. **Controls and navigation:** improve glyph-group selection, size/weight
   adjustment, in-place switching, and oversized-text behavior. Check keyboard
   use, focus, RTL/mixed text, loading and missing-glyph states.
3. **Review state and feedback:** propose a way to save/reopen the exact sample,
   fonts, settings and comments. Keep suggestions distinct from approvals and
   preserve provenance when recording a correction.
4. **Validate together:** inspect actual browser output and test the interaction
   under review. Agree with Eli that the system is ready before resuming Hebrew.

These are work areas, not a frozen feature specification or blanket approval
of a visual redesign. Start with the current screen and Eli's next feedback.

## First UI pass — 2026-10-19

The implemented trial uses a shared four-column grid: sample selection occupies
two columns; weight and size occupy one each. Compare places before, applied,
Rubik and Noto in that order. The initial Switch layout gave Virtua two columns;
P034 supersedes that with three equal columns for Virtua, Rubik and Noto.
Before/Applied controls occupy the unused third row beneath Sample, centered
on the Weight slider track. P035 stretches its Before/Applied buttons into equal
halves across the Sample column. No separate toolbar pushes the proof downward;
“Press B to toggle” sits between Text and References in the mode bar, visible
only in Toggle. On narrow screens it wraps below the tabs beside References.
P036 aligns all mode-bar text on its actual baseline at the shared UI size.
References wraps its text separately from the checkbox so the checkbox cannot
determine the label's baseline; the checkbox stays centered alongside the text.
Below 600 CSS pixels the layout uses
two columns. The old repeated Size rows have been replaced by the continuous
Waterfall described below.

In narrow Toggle layouts with references, Virtua spans the first row and the
two references share the next. Without references, Toggle has one full-width
panel. The shared em fitting policy still applies; the narrower reference
columns determine the common size in the stacked layout.

The first pass used three weight shortcuts; the second pass removes those
preset rows. Weight remains continuous from 400 to 700 and size is 16–320 CSS px,
using numerical fields and sliders.
Captions share a height and sample baselines align without changing outline scale.
Oversized samples scroll together, including RTL samples. Grid shows the shared
columns and a spacing guide (now U/4 under P022). Font identities and
rendering details are collapsed beneath the proof. Settings are not yet persisted.

See the [case record](../cases/hebrew-002/README.md#first-uiux-pass--2026-10-19)
for the supplied references, verification and remaining review scope. This pass
is a proposal awaiting Eli’s feedback, not a new approved visual standard.

## Simplification pass — 2026-10-19

Follow P019/P020 in the design-review preferences: the font-name and study
headlines use the same responsive type token. Sample, weight and size values
share a row; keep settings visible once. The repeated sample/scale summary and
preset-button rows are removed. Applied/provisional state is a quiet footer
line; provenance and explanatory text are in Review Details. The earlier Size range control is superseded by P037; Waterfall omits the size
control entirely.

Dark paper is now `#282828` with `#dedede` ink, matching the neutral address-bar
gray sampled from Eli’s screenshot. Light remains `#dedede` / `#444444`. Each
theme uses two base grays. Keep historical exports and earlier captures intact.
See [the correction record](../cases/hebrew-002/README.md#second-uiux-pass--2026-10-19).

## Responsive fitting — 2026-10-19

P021 makes Fit the default for Compare and Switch. The displayed size is the
actual shared CSS em size, calculated from the widest required run and the
available columns. It never fits each font independently or scales the DOM.
P030 removes the old fixed-size cap: Fit grows as well as shrinks to fill the
columns and enlarges when References is disabled. The widest required run
determines the shared size, so narrower drawings retain their relative widths.
Turn Fit off to restore the separately remembered fixed size and inspect at that
scale with linked horizontal scrolling. Before/applied
measurements are both included in Switch so B does not change the fitted size.

Fitting recalculates after sample, weight, reference, mode and container-width
changes. Text wraps if it reaches the 16 px minimum. Waterfall now uses the descending adaptive sequence described below, rather
than the old ascending 24/32/48/72/96 rows. The selected group was checked in native
same-origin browser frames at 360, 480, 960 and 1440 CSS px, plus the live panel.
See [the case record](../cases/hebrew-002/README.md#responsive-fitting--2026-10-19).

## Continuous Waterfall (P037)

Waterfall replaces Size. Each font has one caption and one continuous vertical
stack. The first run uses the largest common em size fitting the available
columns; seven further logarithmic steps descend to 16 CSS px. Rounded duplicate
sizes collapse, so a narrow or long run can have fewer steps. These are internal
measurements, not visible pixel labels. References off widens and enlarges the
sequence. Every font uses the same sequence with a shared baseline per step.

Sample and Weight occupy equal halves of the control area; the inactive Size
field, Fit checkbox and size slider are absent. On narrow screens the controls
stack and the font columns wrap as intact waterfalls, preserving each caption
above its own samples. Labels and horizontal rules are not repeated between sizes.
Ink has U above the first sample and below the last; intermediate samples have
U/2 on each side, making U between steps. The eight-step progression and 16 px
endpoint are implementation choices for review, not immutable design rules.

## Spacing contract (P022)

Use the page’s side margin as **U**, defined once by `--space`. The current
responsive values are 32 px above 800 px, 24 px at 600–800 px, and 20 px below
600 px. Changing U changes its entire family of tokens together; do not add
independent component paddings to tune a screenshot.

| Relationship | Spacing |
| --- | --- |
| Page margins, headline padding, main section intervals | U |
| Column gutters, control row gaps, rule-to-caption spacing, footer inset | U/2 |
| Font-name to role gap, inline label gaps | U/4 |
| Fit field’s small horizontal safety inset | U/8 |
| Slider track to the value rule above and comparison rule below | U each |
| Sample ink field above the highest ink and below the lowest ink | U each |
| Wrapped comparison row separation | U, in addition to each sample field’s padding |

Control value boxes have height U + U/2 so native select text remains readable
at small widths. Font sizes, line metrics, border widths and slider-thumb shapes
are typography/control dimensions rather than arbitrary layout gaps. Headlines
and captions use native cap/baseline text-box trimming where supported.

For samples, browser TextMetrics measures ink ascent/descent. The first baseline
is shared across fonts, with U above the row’s maximum ascent and U below its
maximum descent (including wrapped lines). Only the native text’s vertical
position changes; equal em scale, advances, reference proportions and shaping
remain intact. Shorter glyphs naturally leave extra space above their own ink.
Canvas is used for measurement only; the visible sample remains live DOM text.
Do not replace this with per-font optical centering or a fixed em-height crop.

Grid shows shared columns and U/4 horizontal spacing guides. Before promoting
a layout change, inspect clean and guided output, check both slider intervals,
verify that marks/descenders and multiline text remain visible, and retain the
measured spacing with the case record. These checks support visual review;
Eli’s response determines whether the design works.

## Reading view and glyph identities (P023/P024)

Reading adds substantial original Hebrew and mixed Latin–Hebrew paragraphs to
this same case. All four fonts receive identical text. Weight is shared; size
is explicit (16–72 CSS px, initially 24), with line spacing 1.5 and zero added
tracking. Fit is disabled in Reading. Reading and glyph-inspection sizes are
remembered independently while the page is open. Paragraphs reflow naturally,
without justification, hyphenation, forced line matching or font-specific fitting.

Wide windows use four equal columns; below 1200 px the layout uses two, and below
600 px one. Reference paragraphs follow the Virtua pair in narrow layouts.
Sticky font captions identify long blocks during scrolling. The first baseline
aligns across fonts; paragraph height thereafter follows each font’s natural
wrapping. The margin-based spacing contract still governs section/paragraph gaps.

Each corpus has three paragraphs. The Hebrew corpus includes 212 occurrences of
he/het/tav; the mixed corpus includes 129. These are original diagnostic drafts,
not external reference quotations. The mixed passage defines Hebrew/English
paragraph directions and isolates names, dates, numbers and script transitions
with native bdi elements. Corpus coverage was checked against every frozen font;
custom unsupported text produces a notice instead of fallback. Record text and
settings with any future weight or spacing correction.

The study heading shows ה (He), ח (Het), ת (Tav), each with its Unicode value.
Individual selector entries include all three identifiers on one line. Keep the
metadata together when adapting this HEB-002-specific interface to a new group.

## Rendering contract

Use actual font files and native browser text, not specimen PNGs or a scaled
canvas. Keep two grays, Virtua labels, title case, close captions and a coherent
responsive grid. Preserve equal CSS em size, zero sample tracking and independent
font aliases. Fit uses one common reported size; never use per-font fitting or silent fallback.
Native browser metrics and rasterization apply; state that distinction when
comparing with historical DesignBot output. Screenshots document a browser state;
they are not the live renderer.

`make review` remains the separate Diffenator3 QA proof. `make proof` remains the
DesignBot print PDF. Neither replaces the live design-review interface, and
the live interface does not establish Google Fonts release readiness.

## Case-specific studies

`prepare.py` accepts optional `study` metadata in the evidence manifest:
`glyphs`, `presets`, `id`, `status`, and `note`. Font records may specify `label`.
HEB-003 demonstrates a current-only inspection: omit `before`, label `after`
Current, and the UI renders three reference-comparison columns and hides Toggle.
Existing HEB-002 manifests retain their original study and Before/Applied roles.
Use this configuration for new cases rather than editing the app's default
Hebrew sample identities or relabeling historical comparisons.


P043 (2026-10-19) supersedes older one-pixel divider and roomy controls notes:
structural rules and slider tracks use 2px rounded strokes; controls start U/2
below the menu, field height is U, label/row gap U/4, slider hit area U/2, and
bottom padding U/4. Thus the slider center has U/2 to each adjacent rule. Toggle
retains its U-high two-button control. The square checkboxes keep their existing
stroke and inset tick. Menu label positions and the content margin are unchanged.

P044 (2026-10-19): Open proofs in dark mode by default, including the initial
HTML paint. The Dark checkbox still allows switching to the neutral light palette.

## Long glyph identities

HEB-009’s marked forms exposed overflow from unwrapped descriptive names.
All study headings now use responsive identity columns (minimum 16rem, capped
by available width). Names wrap within their cell at the shared headline size;
Unicode labels align beneath each row. Narrow views reflow whole identities.
See HEB-009’s heading correction for the rendered check and exact widths.

Case evidence may supply a `reading` map to add or override named corpora at
preparation time. The Text picker uses those corpus labels and retains Your Text.
Glyph identities containing a base plus combining marks show every Unicode
codepoint, not just the first character (HEB-010). This changes metadata and
samples, not the specimen’s shaping, spacing or type scale.

## Script-specific studies

Set `study.language` (e.g. `ar`) and `study.readingDefault`. Specimen and
custom-text language tags follow the study. For non-Hebrew studies, provide the
`reading` corpus explicitly; Hebrew defaults are not injected. Supply all four
preset keys (`group`, `words`, `marks`, `latin`) with script-appropriate probes.
Arabic cases should expose contextual joining, real words, marks, and mixed
Arabic/Latin/numeral runs. Alef has isolated/final forms; do not invent initial
or medial Alef forms. Keep native shaping and zero added tracking.

Reference roles are optional and font names come from the evidence manifest.
Arabic uses Rubik and Noto Sans Arabic, with local font snapshots and OFL texts.
Noto's width axis stays at its native default 100; weight follows the shared
control. Same numerical weight does not imply visually matched darkness.
Historical Hebrew cases continue to use their own frozen Noto Sans Hebrew.

ARB-001 now includes four Arabic references: Rubik, Noto Sans Arabic, IBM Plex
Sans Arabic and Readex Pro. Additional reference keys are discovered from the
manifest. A family can provide `faces`, each with `path`, `sha256` and `weight`,
for genuine static weights; otherwise the existing single-file record is used.
Static families use native CSS weight matching, with synthesis disabled. Every
face is hashed independently. Six-panel comparisons reflow to two columns below
1440px; narrow Text remains one column. Historical four-panel layouts are intact.
