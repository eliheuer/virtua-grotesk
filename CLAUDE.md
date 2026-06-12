# CLAUDE.md

The canonical agent guidance for this repo lives in AGENTS.md (shared across
AI tools). It is imported here in full:

@AGENTS.md

## Claude Code specifics

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

- **drawbot-skia is the standard tool for all image generation** (proofs,
  specimens, quick checks). It is installed in `.venv` from
  `github.com/eliheuer/drawbot-skia` via `requirements.txt`, so `make proof`
  and `make specimen` work after a plain `make setup`. Setting
  `DRAWBOT_SKIA_REPO` in an ignored `local.mk` overrides it with a live
  checkout for drawbot development.
- For quick visual checks during glyph work, write a short drawbot-skia
  script that renders a PNG, save it to `~/Temp/`, and Read the PNG back.
  `openTypeFeatures(tnum=True)` etc. work, so feature substitutions can be
  verified visually too.
- After any glyph or feature change: `make build`, then verify the built fonts
  in `fonts/` directly (fontTools for tables/widths, uharfbuzz for shaping)
  rather than trusting the source edit.
