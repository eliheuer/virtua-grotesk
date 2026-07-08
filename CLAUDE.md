# CLAUDE.md

The canonical agent guidance for this repo lives in AGENTS.md (shared across
AI tools). It is imported here in full:

@AGENTS.md

## Claude Code specifics

- **Do not credit yourself in commits.** No `Co-Authored-By: Claude` trailers,
  no "Generated with Claude Code" lines — plain commit messages only.

- Skills are canonical in `.agents/skills/` and exposed to Claude Code via the
  `.claude/skills` symlink. **Edit skills only in `.agents/skills/`** — never
  create separate copies under `.claude/`.
- The slash commands referenced in AGENTS.md (`/build-font`, `/proof`,
  `/edit-glyph`, `/draw-outline`, `/kerning`, `/compare-reference`, `/font-qa`,
  `/render-specimen`) are those skills.
- Always use `./.venv/bin/python` — the system Python lacks fontTools,
  uharfbuzz, etc. Run `make setup` if `.venv/` is missing.

## Source-editing footguns (learned the hard way)

- **Never save these UFOs through defcon/ufoLib `font.save()`.** It rewrites
  `contents.plist`, `lib.plist`, and glif XML in a different style, producing
  thousand-line noise diffs. Instead, write `.glif` XML directly in the repo's
  native style: tabs for indentation, double-quoted attributes, no space
  before `/>`, attribute order `x`, `y`, `type`, `smooth`.
- New glyphs must be registered in **three places per master**:
  `glyphs/contents.plist`, `public.glyphOrder` in `lib.plist`, and the glif
  file itself. Edit the plists surgically (matching existing tab formatting),
  not via a UFO library.
- Both masters must keep identical contour/point structure for every glyph or
  the variable build breaks (see Master Compatibility Warning above).

## Seeing your work (visual verification)

- **designbot (Rust) is the standard tool for all image generation** (proofs,
  specimens, quick checks) — `designbot --render <script.rs> --output <path>`;
  the output extension picks the format (png/gif/mp4/pdf). Install from the
  local checkout: `cargo install --path designbot-cli` in
  `~/GH/repos/designbot`. `make proof` / `make specimen` run the ports in
  `scripts/designbot/`.
- For quick visual checks during glyph work, write a short designbot script
  that renders a PNG, save it to `~/Temp/`, and Read the PNG back. Scripts
  can read UFO glyphs directly (`designbot::norad` + `draw_path`); for the
  harness canvas frame use `harness/designbot/glyph_canvas.rs` (glyphbox /
  sheet modes) instead of writing a new renderer. Note: no openTypeFeatures
  support yet — verify feature substitutions with uharfbuzz on the built font.
- After any glyph or feature change: `make build`, then verify the built fonts
  in `fonts/` directly (fontTools for tables/widths, uharfbuzz for shaping)
  rather than trusting the source edit.
