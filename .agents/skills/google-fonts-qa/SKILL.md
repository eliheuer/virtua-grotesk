---
name: google-fonts-qa
description: Run or interpret Google Fonts checks on compiled fonts or downstream packages, including coverage, shaping, and proof evidence. Use for release QA and Fontspector findings; use font-qa for source-only checks.
---

# Google Fonts QA

Read `documentation/qa.md` for this repo's commands and current tool baseline.
Refresh [the official QA guide](https://googlefonts.github.io/gf-guide/qa.html)
and use the installed CLI help for syntax.

For source QA, build from the active sources. For an explicit supplied binary
or package audit, inspect those exact inputs without replacing them with a
local rebuild. Record source revision/modifications when known, binary
hashes, tool versions, and network availability. Use `make qa-full` for the
unexcluded profile; `QA_NETWORK=offline` explicitly skips network checks.
`make test` is only the development gate and retains exclusions.

For an assembled downstream family, run:

```sh
make qa-package PACKAGE=/path/to/ofl/virtuagrotesk
```

Package QA must receive the metadata, license, article, and font inputs; passing
only TTFs can omit package checks. Check the JSON report, not just terminal
output. Report severity counts and skips without confusing repeated per-font
results with unique defects.

Classify findings as source/drawing, compiled metadata, package context,
maintainer choice, or evidenced tool limitation. Preserve intended subsets.
A narrower metadata scope that suppresses warnings is not a fix. Inspect
contour-count heuristics before drawing changes; preserve both-master structure
and protected glyphs. Real empty visible characters must not pass as coverage.

Check the compiled cmap against the intended glyphsets, plus actual outline
presence. Review GDEF/GPOS/GSUB, mark attachment, joining, RTL/mixed text,
spacing, and interpolation. Include native-reader review for shipped scripts.
Table presence and a smoke string do not establish script quality.

Generate current proofs with `make review`/`make proof`, or use
`gftools qa -f FONT.ttf --proof --rust -o out/gfqa` after checking local help.
Inspect actual rendered output before claiming visual QA. Record which weights,
scripts, and contexts were reviewed and which remain pending.

FAIL or worse blocks the configured gate; WARN stays visible for human review.
Document reviewer-approved exceptions with their rationale and affected files.
Do not change exclusions, delete cmap entries, or relabel glyphs merely to
produce a cleaner result.

## Scope and completion

Read-only review requests produce findings without source edits. For preparation
or repair requests, complete authorized engineering work and verify it. A
pending human decision does not block independent checks or fixes. Preserve
existing session approvals; ask only for missing choices that change the result.

Finish with the source/artifact identity, checks actually run, observed results,
and remaining decisions. Do not claim readiness from file presence or report
counts alone, and do not rerun a build merely for a documentation-only change.

## Evidence integrity

Use a separate `QA_REPORT_DIR` for materially different runs. The wrapper saves
arguments, tool version, input hashes, and the checkout HEAD alongside the JSON.
For a supplied package, checkout HEAD is execution context, not proof of where
its fonts came from; record unknown or supplied provenance explicitly.
Check report creation and hashes before using results. Treat missing or stale
reports and tool execution errors as failed verification, not a passing QA run.
