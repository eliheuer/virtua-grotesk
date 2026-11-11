---
name: font-qa
description: Check the UFO sources after an edit, without building. Master compatibility, grid, stroke targets, curves, kerning and anchors. Use before a review or when asked whether the sources are healthy. For compiled fonts use google-fonts-release.
---

# Check the sources

```sh
.venv/bin/python scripts/report_master_compatibility.py --check
make check-design GLYPHS="..."      # grid, stroke targets, composites
make check-changes                  # what changed since main
.venv/bin/python scripts/curve_lint.py Regular <glyph> --joins
```

Also look at metrics, glyph sets, anchors, kerning groups and pairs in both
masters. `documentation/design/system/verification.md` describes the checks for
each kind of source edit.

The checks find faults. They do not measure design quality, and a pass is not
approval. Source compatibility does not prove shaping: build and look at the
changed glyphs at 400, 550 and 700 (see the `build-and-proof` skill).
