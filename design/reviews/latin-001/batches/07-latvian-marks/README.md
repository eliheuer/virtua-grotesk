# LAT-001 batch07 · Latvian mark construction

Bottom-mark inspection found a construction error before any donor redraw:
Ģģ Ķķ Ļļ Ņņ Ŗŗ all used the cedilla component. Lowercase ģ even placed it
inside/under the descender. These twenty non-green wrappers now use Virtua's
existing comma accent; ģ uses its rotated form above the bowl. Existing base
components, base drawings, donor drawings and advances are unchanged. The
[Unicode Latin chapter](https://unicode.org/versions/Unicode18.0.0/core-spec/chapter-7/)
describes the rotated-above construction for lowercase ģ and floating comma
forms for the Latvian consonants. Actual Rubik whole-letter rasters supplied the
comparison. No reference outlines were copied.

Nine wrappers per master compensate the old134 versus new140 donor anchor and
round their local x offsets to8. This changes horizontal alignment by at most4
units. Lowercase ģ rotates the donor180 degrees with offsets(448,576) Regular
and(488,576) Bold. Its mark occupies y616–768,24 above the base bowl. Explicit
wrapper top anchors(312,800)/(352,800) clear that mark; bottom anchors at
(312,-216)/(352,-240) place additional below marks at the descender rather than
inside it. Incoming donor anchors, all base anchors and all widths remain intact.
New component offsets and explicit anchors are on8. New composite constructions
are purple drafts; no donor or protected grade changed.

Canonical ccmp rules in both feature files reconstruct these ten letters from
base+cedilla when a web subset omits their precomposed cmap entries. This is
canonical decomposition support, not a blanket substitution of cedillas in other
languages. French/Turkish/Romanian comparison strings retain their prior ink.

Whole attachment and reading rows at400/550/700 and224px/em endpoint letters
were inspected. The previous spurs are gone and ģ has a clear descender and an
above mark. **The inherited comma donor is visibly too light at Bold and has a
notched terminal; that drawing is the next bounded repair.** This batch corrects
construction without calling the donor finished. Base optical spacing and its
inherited grid exceptions remain separate work. Native-reader/design approval
has not been claimed.

Rubik lacks Ţ/ţ (U+0162/U+0163); those mixed comparison rows explicitly show it
unavailable. Supplemental supported-character rows use actual Rubik for all
stack samples. A deep extra cedilla under ģ was faint/missing in DesignBot's
Bold raster; independent FreeType/RAQM whole-text images at all three weights
confirm its compiled placement. HarfBuzz reports the extra cedilla at y-408..-240
at700, attached to the descender; the extra comma-below remains detached. The
independent images are retained as compiled-stacks-*.png. Do not mistake the
DesignBot discrepancy for source absence or general rendering correctness.

205 scoped shaping comparisons pass at five weights, including NFC/NFD equality,
missing-cmap fallback, unchanged advances, stack clearance, and unchanged
Arabic/Hebrew/unrelated cedilla text. All compiled ink changes are exactly the
ten wrappers; all1757 other source files are byte-identical. Both masters retain
compatible component structures. The326 Arabic reserved sources in each master,
all green bases, manual hamza and reversed-Nun compensation remain untouched.

Four Latin regression tests pass across the variable font and four statics,
including a new construction/fallback test. The frozen baseline reproduces the
same216 Hebrew engineering failures, with zero new or resolved failures.
Grid QA reports226 Regular/190 Bold findings: inherited donor/base geometry,
anchors, advances/bounds, plus the intentional rotated component transform.
New placement/explicit-anchor values pass8-grid assertions. No source curves
were changed. Active build/preflight completed; candidate and active variable
font tables match except head timestamps. Online Fontspector was not rerun.
Local checkpoint only, pending human review; no submission or publication.

Next: comma-accent donor weight/terminal quality, checking its now-expanded
consumer closure and preserving the rotated ģ placement; then cedilla/ogonek,
alternate carons and the maintained spacing/coverage/release queue.
