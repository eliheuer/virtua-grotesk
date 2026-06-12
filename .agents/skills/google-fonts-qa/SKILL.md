---
name: google-fonts-qa
description: Run and document Google Fonts QA (Fontspector googlefonts profile and related checks) before packaging a font family.
---

# /google-fonts-qa

Run and document Google Fonts QA for a font family. This skill covers the
repeatable checks that should happen before packaging, and it keeps drawing
quality separate from packaging mechanics.

## Usage
`/google-fonts-qa [fontspector|glyphsets|proof|kerning|metadata|all]`

Default: `all`

## Fontspector

1. Build fonts from the active sources.
2. Run Fontspector's `googlefonts` profile on the generated TTFs.
3. Save the report in a durable location under `documentation/`.
4. Classify every FAIL and WARN:
   - fix now,
   - drawing/source blocker,
   - maintainer decision,
   - reviewer-approved exception,
   - false positive or tool limitation with evidence.
5. Do not treat a warning as harmless just because the build succeeds.
6. Separate loose-font warnings from package-context warnings. Run a temporary
   `METADATA.pb` probe when warnings involve subsets, reachability, source
   metadata, or downstream package shape.
   - Loose-font runs can repeat one metadata problem once per font binary.
     Report that count honestly, but use the package-context probe to find the
     real downstream warning floor for the variable-font package.
7. Do not chase a lower warning count by dropping an intended serving subset.
   If removing `arabic`, `latin-ext`, or another subset lowers WARN count but
   makes intended glyphs unreachable, keep the honest package scope and record
   the remaining blockers instead.
8. For zero-warning work, split the queue into:
   - mechanical metadata/package fixes,
   - glyphset coverage needed to satisfy subset thresholds,
   - drawing/source findings such as contour-count heuristics,
   - warnings that should be accepted only with maintainer/reviewer evidence.
9. State whether an honest zero-warning result is possible with the current
   intended scope. If not, record the current package-context floor and the
   specific choices needed to reach zero: broader coverage, narrower reviewed
   metadata scope, or reviewer acceptance.
   Split the plan into:
   - a release-scope path that preserves intended support and carries reviewer
     evidence for any remaining package-context warnings,
   - a true zero-warning path that names the larger glyphset expansion or
     approved metadata-scope change required to make the warning count zero.
10. If an intended script subset still fails a Fontspector subset-threshold
    warning, document the gap explicitly. The honest path is usually to expand
    glyphset coverage, defer the script scope, or record reviewer evidence; do
    not silently remove the script from metadata while the font still intends to
   serve it.
11. For reachability warnings on support codepoints such as U+0237, U+200F,
    U+20B9, or U+25CC, test any proposed cmap removal or metadata "rescue"
    subset in package context before adopting it. Removing required support
    codepoints can trigger different warnings, and adding broad subsets such as
    `hebrew` or `symbols` only to cover a helper codepoint can increase
    `subsets_correct` warnings and misrepresent the family scope.
12. Treat "zero warnings" as a release-quality goal, not a number to game. If
    reaching zero requires hundreds of additional subset codepoints or dropping
    the primary non-Latin scope, record the warning floor and defer the zero
    state to a larger coverage pass or reviewer decision.

Portable command shape:

```bash
make test
make warnings-check
make metadata-warning-check
make zero-warning-check
# or:
fontspector check-googlefonts fonts/variable/*.ttf fonts/ttf/*.ttf
```

## Glyphset Coverage

1. Determine intended script scope for the first submission.
2. Compare generated font cmaps against `googlefonts/glyphsets`.
3. Track missing codepoints by glyphset and by source glyph work needed.
4. For non-Latin scripts, also track marks, anchors, shaping behavior, and
   script-specific review requirements. Cmap coverage alone is not enough.
5. Keep reusable reports for:
   - missing Latin Core,
   - missing script-specific core set,
   - source work checklist,
   - shaping smoke test,
   - mark/anchor readiness.

## Non-Latin Candidate Drawing Workflow

Use deterministic candidate generation before trying model training or direct
outline generation. For each missing non-Latin codepoint:

1. Convert codepoint gaps into source glyph names for both masters.
2. Reuse existing family-native bases, dots, marks, and punctuation first.
3. Run candidate generation dry by default; write only after the dry-run report
   shows the intended auto-created, review-needed, hand-draw-needed, and
   compatibility-risk buckets.
4. Assign Unicode values only to encoded default glyphs; positional forms and
   helper glyphs should normally stay unencoded.
5. Verify the script is idempotent after creation: a clean dry run should report
   existing entries, zero candidates left to create, and zero compatibility-risk
   entries.
6. Treat generated candidates as review scaffolds, not production drawings.

For Arabic specifically, keep these checks distinct:

- Arabic Core cmap coverage,
- default/fina/init/medi source presence in both masters,
- master-compatible contours/components/anchors,
- dotted circle and required mark glyphs,
- `mark`/`mkmk` GPOS,
- HarfBuzz shaping smoke strings with no `.notdef`,
- mechanical visual-risk audit for blank visible glyphs, `.notdef` mappings,
  suspicious advances, extreme bounds, and sidebearing outliers,
- focused visual-risk proof for any audit rows that need fast inspection in
  isolated and shaped script context,
- contour/no-contour cleanup proofing,
- compact manual-review batches that group visual proof rows with related
  contour decisions,
- native-reader or script-specialist visual review.

When `contour_count` reports non-Latin forms, create an editor queue that maps
Fontspector production glyph names back to source glyph names. Include both
masters' contour, point, and component counts before editing. Only add or remove
contours when the design review says the drawing is wrong; preserve master
compatibility and rerun the contour proof after each small batch. Keep a
decision log with explicit statuses such as `pending`, `fix-now`, `fixed`,
`accepted`, and `deferred`; use a guarded helper when possible so regenerated
reports do not erase manual decisions.

Test contour-normalization ideas against the built variable and static fonts,
not just source geometry. A merge that looks cleaner in the UFO can expand the
warning surface if static overlap removal and variable interpolation handle the
shape differently. When an experiment increases all-font contour rows, restore
the previous source shape and keep the finding pending until visual/script
review supports a real redraw or an accepted style divergence.

For hand cleanup, generate a compact batch report after the dashboard and proof
artifacts exist. Group structural glyph checks, marks, dot-stack helpers, and
RTL text/spacing separately so reviewers can record decisions in short passes
instead of scanning every wide table. Each batch should list the source logs,
related proof/dashboard evidence, current status counts, and exact guarded
update commands for both visual review rows and contour-decision rows.

When a reviewer is ready to work, generate a one-page drawing-session checklist
that starts with source/editor readiness checks, then lists the active batch,
the proof files to open, guarded pass/fix/defer commands, likely Regular and
Bold source GLIF targets, and the rebuild/report/preflight loop. Add a fast
source-edit diff report for multi-master source work so one-sided non-Latin
GLIF edits are visible before the full build or master-compatibility check.
Add a source-structure checkpoint for unresolved review rows before hand
editing starts. It should follow the UFO `contents.plist` filename mapping,
inspect every active master, count contours/components/points, and report
missing source files plus paired-master structure mismatches.
Keep the review log as the canonical record. If the reviewer will close
multiple rows at once, optionally provide a blank TSV template as a temporary
entry form plus a validating batch updater that dry-runs by default and rejects
bad statuses or duplicate keys before any write. Pair it with an apply-check
target that writes the canonical review log, regenerates reports, and reruns preflight
so recorded review decisions and generated evidence cannot drift.

When Fontspector reports unreachable helper glyphs, do not blindly delete source
helpers. First classify whether they are reachable through Unicode, GSUB output,
or component references. If helpers are source-only, either decompose them out of
generated fonts, mark them as skip-export in sources, or document why they must
remain.

For non-Latin visual risk, add a small generated audit before full human proof
review. It should inspect built fonts, not source assumptions, and flag:

- visible codepoints that map to `.notdef` or have no outline,
- non-mark glyphs with zero or negative advances,
- marks or letters that exceed expected vertical margins,
- large negative sidebearings or obvious clipping risks.

Treat the audit as a triage tool. Blank visible glyphs and `.notdef` mappings
are likely source/build bugs; sidebearing and vertical-bound rows are review
prompts. When sidebearing rows appear, generate a focused HTML proof that embeds
the built fonts and shows each risky glyph in isolated and shaped context across
all weights. Record the review outcome in the visual review log; do not edit
Arabic or another joining script only because an LTR sidebearing heuristic looks
large.

## Visual Proof Review

1. Generate proof output after build-output, spacing, kerning, or scope changes.
2. Use `gftools qa --proof` when preparing for Google Fonts review.
3. Confirm every expected instance and proof type exists.
4. For non-Latin scripts, run the visual-risk audit and focused proof before
   the full proof review so the highest-risk glyphs are easy to inspect.
5. Keep a human review checklist that records:
   - proof generation date,
   - fonts reviewed,
   - proof files reviewed,
   - spacing findings,
   - kerning findings,
   - visual-risk proof findings,
   - script-specific findings,
   - accepted deferrals.

Portable command shape:

```bash
gftools qa --proof fonts/variable/FamilyName[wght].ttf fonts/ttf/*.ttf
```

If `gftools qa --proof` needs live catalog access for comparisons, note that
network/auth failures are environmental and should not be confused with font
QA results.

## Kerning

1. Check source kerning in every master.
2. Check built GPOS `kern` coverage in every output font.
3. Run proof output and review visually.
4. Either finish kerning before the first PR or record an explicit maintainer
   deferral and explain the Google Fonts review impact in the issue/PR handoff.
5. Do not mark kerning final until both source data and proof review agree.

## Variable Font Metadata

Review at least:

- `name` table family/style/full/PostScript names,
- license strings and URLs,
- version strings,
- `OS/2.fsType`,
- `OS/2` vendor ID,
- `fvar` axis tags, bounds, default, and instance names,
- `STAT` table presence and style linking,
- `meta` `dlng` and `slng` when script metadata is needed,
- `avar` decision for variable axes.

## Final QA Evidence

Before handoff, there should be a current evidence chain from generated fonts
to reports:

- build output exists and is fresh,
- Fontspector report exists and has classified results,
- glyphset coverage reports exist,
- proof output exists and has human review status,
- metadata reports reflect generated binaries, not source assumptions,
- final blocker report points to every relevant report.
