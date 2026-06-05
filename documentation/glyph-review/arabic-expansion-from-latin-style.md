# Arabic Expansion From Latin Style

This note records the first local-first workflow for expanding a Latin
family with editable Arabic candidates. It is a prototype for
Runebender-Comfy, not final production drawing.

## Recommendation

Use deterministic donor normalization first, then add local vision-model
ranking after the proof output is useful. Do not train a LoRA until the
source-to-source prototype produces candidates worth comparing.

Why:

- UFO/designspace donor sources already provide editable vectors.
- Rubik Arabic is local, OFL, Google-Fonts-proven, and geometric enough
  to be a strong first donor for Virtua, but the workflow is generic: pass any
  appropriate OFL donor source with `--donor`.
- Variable-font compatibility can be checked immediately.
- Current font-generation models are more useful as visual advisors than
  as reliable UFO producers for Arabic contextual forms.

## Prototype Script

Script:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py --glyphs sample
./venv/bin/python scripts/build_donor_glyph_candidates.py --glyphs sample --write --force
```

Default target:

```text
sources/VirtuaGrotesk.designspace
```

Default donor:

```text
/Users/eli/GH/repos/rubik/sources/designspace/Rubik.designspace
```

Override the donor for another family:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --donor /path/to/OtherOFLDonor.designspace \
  --glyphs mark:red \
  --arabic-only \
  --output build/arabic-donor-candidates/other-donor-red-marked \
  --write --force
```

Default output:

```text
build/arabic-donor-candidates/rubik-to-virtua/
```

Generated files:

- `glyph-candidate-report.md`
- `glyph-candidate-report.json`
- `proofs/arabic-donor-candidate-proof.html`
- copied scratch UFO/designspace sources

The script writes only to `build/` unless a different output is passed.
It does not overwrite production Virtua sources.

## First Experiment

Implemented Rubik-to-Virtua sample batch:

```text
beh-ar, seen-ar, sad-ar, tah-ar, meem-ar, heh-ar,
peh-ar, keheh-ar, gaf-ar, farsiYeh-ar
```

Verification:

```bash
./venv/bin/python scripts/report_master_compatibility.py \
  build/arabic-donor-candidates/rubik-to-virtua/VirtuaGrotesk-Regular.ufo \
  build/arabic-donor-candidates/rubik-to-virtua/VirtuaGrotesk-Bold.ufo \
  build/arabic-donor-candidates/rubik-to-virtua/master-compatibility.md

./venv/bin/fontmake \
  -m build/arabic-donor-candidates/rubik-to-virtua/VirtuaGrotesk.designspace \
  -o variable \
  --output-path 'build/arabic-donor-candidates/rubik-to-virtua/VirtuaGroteskArabicCandidate[wght].ttf'
```

Result:

- scratch masters have 0 blocking compatibility mismatches;
- sampled transformed contours are rounded to even coordinates;
- scratch variable font builds;
- proof HTML is ready for visual review;
- no production UFO masters are changed.

## Runebender-Comfy Fit

No new ComfyUI node is needed to review this first output. Load the
scratch designspace directly with the existing Runebender font loader:

```text
build/arabic-donor-candidates/rubik-to-virtua/VirtuaGrotesk.designspace
```

After the script proves useful, wrap the same logic as:

```text
Runebender / Font / Glyph Candidate Builder
```

Inputs:

- `FONT` target
- donor source path
- glyph list or batch name
- transform preset
- write mode: scratch only

Outputs:

- candidate `FONT`
- proof `IMAGE` or HTML path
- report text/JSON

The node should stay a thin wrapper over the script logic so the
workflow remains debuggable outside ComfyUI.

## Next Research Pass

Compare transform presets before adding model work:

- `target-advance`: preserves target widths, may over-compress wide
  Arabic donors.
- `upm`: preserves donor proportions better, may exceed target rhythm.
- `same-as-y`: keeps donor proportions tied to target x-height/cap scale,
  likely too wide for Virtua but useful as a visual reference.

Once these proofs are useful, add a local vision-model ranking step that
scores candidates by expected cleanup time. Keep Runebender as the final
human editing surface.

## Selective Chunking

Do not replace all Arabic drawings blindly. The script accepts any
comma-separated glyph list or text file:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --glyphs beh-ar,theh-ar,peh-ar \
  --write --force
```

For the current unresolved Arabic review set:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --glyphs pending-review \
  --write --force
```

To protect hand-drawn glyphs, add them to:

```text
documentation/glyph-review/arabic-donor-preserve-glyphs.txt
```

Then run:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --glyphs pending-review \
  --exclude-glyphs documentation/glyph-review/arabic-donor-preserve-glyphs.txt \
  --output build/arabic-donor-candidates/rubik-to-virtua-pending-review \
  --write --force
```

## Red-Marked Replacement Batches

Runebender stores glyph labels in UFO `public.markColor`. Red is the
least painful batch marker for "replace this placeholder."

1. In Runebender, mark only Arabic glyphs that need total replacement as
   red.
2. Save the source.
3. Generate a scratch donor candidate from only those red Arabic marks:

```bash
./venv/bin/python scripts/build_donor_glyph_candidates.py \
  --glyphs mark:red \
  --arabic-only \
  --output build/arabic-donor-candidates/red-marked-arabic \
  --write --force
```

This leaves every unmarked glyph alone in the scratch copy. Existing
hand-drawn Arabic can stay unmarked or can be protected explicitly with
`--exclude-glyphs`.

## Agent Source Apply

Use ComfyUI or Runebender as the visual dry run, not necessarily as the final
writer. After the scratch candidate is reviewed, an agent can apply the chosen
candidate glyphs back to production sources without opening the GUI:

```bash
./venv/bin/python scripts/apply_donor_glyph_candidates.py \
  --report build/arabic-donor-candidates/red-marked-arabic/glyph-candidate-report.json \
  --glyphs report \
  --arabic-only
```

If the dry run reports only `would-apply`, write the same batch:

```bash
./venv/bin/python scripts/apply_donor_glyph_candidates.py \
  --report build/arabic-donor-candidates/red-marked-arabic/glyph-candidate-report.json \
  --glyphs report \
  --arabic-only \
  --write
```

This copies only matching `.glif` files listed as `status == candidate` in the
candidate report. It preserves the target mark colors by default, so red review
labels remain until the human clears them.
