# Goal: Arabic Expansion From Latin Style

Build a practical local workflow that takes a font with finished Latin glyphs but no Arabic, then creates editable Arabic candidate glyphs that match the Latin weight, rhythm, and drawing style closely enough to reduce manual drawing time.

## Context

Primary test family: `/Users/eli/GH/repos/virtua-grotesk`

Editor/workflow target: `/Users/eli/GH/repos/runebender-comfy`

Reference donor source: `/Users/eli/GH/repos/rubik/sources/designspace/Rubik.designspace`

The output should support ComfyUI + Runebender editing. Do not design a cloud-only workflow.

## Product Outcome

Create a reusable prototype that can:

1. Load a target UFO/designspace with Latin drawings.
2. Load one or more OFL Arabic donor fonts.
3. Select matching Arabic glyphs from donors.
4. Normalize donor glyphs into the target font coordinate system.
5. Adjust candidates toward the Latin style.
6. Write a scratch candidate UFO/designspace or Runebender-Comfy `FONT`.
7. Generate proof overlays for review.
8. Keep final edits human-approved in Runebender.

## Important Constraint

Do not treat donor outlines or AI output as final drawings. The goal is better placeholders/candidates that are faster to edit.

If donor outlines materially survive into final sources, document OFL attribution and derivative-source implications. If final drawings are substantially redrawn, document reference-assisted use.

## Research Questions

- What is the fastest local-first path: deterministic donor normalization, local vision ranking, LoRA/post-training, or a mix?
- Which Google Fonts Arabic families are the best donors for geometric Latin sans families like Virtua Grotesk?
- Can Rubik Arabic be normalized into Virtua's 1024 UPM, 768 cap, 576 x-height rhythm with useful results?
- What ComfyUI node shape is needed after the script prototype works?
- Which existing font-generation models are worth trying locally, and which are too research-heavy for today?

## Preferred Architecture

Start as a script, then wrap proven logic as a node.

Prototype script:

`scripts/build_donor_glyph_candidates.py`

Expected inputs:

- target designspace/UFO path
- donor designspace/UFO path
- glyph list or glyphset name
- output scratch dir
- transform preset, e.g. `geometric-sans-arabic`

Expected outputs:

- scratch candidate UFO/designspace
- JSON/Markdown report
- overlay proofs

Future ComfyUI node:

`Runebender / Font / Glyph Candidate Builder`

Inputs:

- `FONT` target
- donor path
- glyph list/batch
- transform preset
- write mode: scratch only

Outputs:

- candidate `FONT`
- proof `IMAGE`
- report text/JSON

## Steps

1. Inspect `runebender-comfy` workspace/FONT APIs.
2. Inspect Rubik and Virtua metrics, names, and Arabic coverage.
3. Build a donor-glyph mapping for the current Arabic target set.
4. Implement deterministic normalization:
   - UPM scale to target
   - vertical metric alignment
   - width and sidebearing transfer rules
   - even-coordinate rounding
   - optional target dot/component replacement
5. Generate overlay proofs:
   - current target placeholder
   - raw donor
   - transformed candidate
6. Run existing build/proof checks where possible.
7. Decide whether a ComfyUI node is justified and define its minimal API.

## Success Criteria For Today

- A concrete recommendation exists for deterministic vs local-model vs LoRA.
- A script/node plan exists with exact inputs and outputs.
- At least one Rubik-to-Virtua Arabic candidate experiment is specified or implemented.
- The workflow keeps Runebender-Comfy as the editing surface.
- No production Virtua sources are overwritten by experimental candidates.

## Non-Goals Today

- Do not train a LoRA unless the deterministic prototype is already working.
- Do not overwrite production UFO masters.
- Do not promise final Arabic quality from AI alone.
- Do not add a large ComfyUI node before the reusable script logic is proven.
