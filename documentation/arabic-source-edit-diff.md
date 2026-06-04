# Arabic Source Edit Diff

This generated report checks current worktree GLIF edits in the
active Regular and Bold source UFOs. Use it during hand drawing to
catch one-sided Arabic edits before relying on interpolation or
running the full after-drawing check.

## Summary

- Changed active source GLIF files: 104
- Changed Arabic-like GLIF names: 28
- Arabic-like Regular/Bold pairing gaps: 0
- Ready for paired-master review: yes

## Arabic-Like GLIF Edits

| Glyph file | Regular | Bold | Pairing |
| --- | --- | --- | --- |
| `ain-ar.glif` | `M` | `M` | paired |
| `alefM_aksura-ar.glif` | `M` | `M` | paired |
| `behD_otless-ar.glif` | `M` | `M` | paired |
| `eight-ar.glif` | `M` | `M` | paired |
| `eightFarsi-ar.glif` | `M` | `M` | paired |
| `farsiYeh-ar.glif` | `M` | `M` | paired |
| `fehD_otless-ar.glif` | `M` | `M` | paired |
| `five-ar.glif` | `M` | `M` | paired |
| `fiveFarsi-ar.glif` | `M` | `M` | paired |
| `four-ar.glif` | `M` | `M` | paired |
| `fourFarsi-ar.glif` | `M` | `M` | paired |
| `hah-ar.glif` | `M` | `M` | paired |
| `heh-ar.glif` | `M` | `M` | paired |
| `jeem-ar.glif` | `M` | `M` | paired |
| `kaf-ar.glif` | `M` | `M` | paired |
| `keheh-ar.glif` | `M` | `M` | paired |
| `lam_alef-ar.glif` | `M` | `M` | paired |
| `meem-ar.glif` | `M` | `M` | paired |
| `nine-ar.glif` | `M` | `M` | paired |
| `nineFarsi-ar.glif` | `M` | `M` | paired |
| `noonghunna-ar.glif` | `M` | `M` | paired |
| `qafD_otless-ar.glif` | `M` | `M` | paired |
| `reh-ar.glif` | `M` | `M` | paired |
| `sad-ar.glif` | `M` | `M` | paired |
| `shadda-ar.glif` | `M` | `M` | paired |
| `tah-ar.glif` | `M` | `M` | paired |
| `three-ar.glif` | `M` | `M` | paired |
| `threeFarsi-ar.glif` | `M` | `M` | paired |

## Use

- If a row is `one-sided`, inspect whether the same structural edit
  is needed in the other master before continuing.
- This check does not replace `make arabic-after-drawing-check`; it is
  a fast git-status guard for the middle of a drawing session.
