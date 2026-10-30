---
name: font-qa
description: "Run quality assurance checks on the font sources: metrics consistency, master compatibility, and kerning sanity. Use before handoff or when verifying source health."
---

# Check source health

Use [design verification](../../../design/system/verification.md) for the named
source operation and documentation/qa.md for the complete QA workflow. These checks
are not human grading or Google Fonts release readiness.

```sh
.venv/bin/python scripts/report_master_compatibility.py --check
make reports
```

Inspect metrics, glyph-set parity, contour/point/component correspondence, anchors
and kerning groups/pairs in both masters. For machine drafts run draft_grid_check
on the named scratch UFOs/glyphs; preserve inherited optical exceptions. For curves
run curve_lint with --joins and inspect signed profiles/large renders. Source
compatibility does not prove compiled shaping or visual quality: build and inspect
affected forms at endpoint/intermediate weights. Use google-fonts-qa for binary QA.
