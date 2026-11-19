# Worklog

Newest first. `AGENTS.md` gives the form of an entry.

## 2026-11-19, Claude Code

- Decided by Eli: the optical size includes spacing. Each side loses 24 units at 144 pt, and the change is complete at 72 pt. Arabic joins get shorter, and free sides inside Arabic words change as in Latin (R68).
- Decided by Eli: a grade axis from -200 to 200 that keeps every advance (R69). At 300 the letters of Regular collide.
- Done, not reviewed by Eli: `fgtools draft-optical-size --write` gave the four 144 pt masters the display spacing, and `fgtools draft-grade` added 16 grade masters and the `GRAD` axis. Both commands are uncommitted in fgtools. Every changed glyph is purple. A later run keeps a glyph that was corrected by hand.
- Done: Regular took the newer `feh_yeh-ar` and `tah-ar.medi` from Regular 144 pt, and Regular 144 pt took the newer `yeh-ar.fina` from Regular.
- Changed: `AGENTS.md` is now short bullets. `CONTEXT.md` is compact, with every rule and value kept, and its essay is in `README.md`. Agents may redraw yellow Arabic glyphs in every master without asking for each one, and mark them purple.
- Done: `make masters` calculates Thin, Black, the grade masters and the 144 pt masters from Regular and Bold. A calculated glyph has the digest of its outline in its lib (`garden.font.calculated`), and a glyph that was changed by hand stays. Thin follows for 238 glyphs and Black for 561; the others differ from the calculation and are kept.
- Done: every text in the proof has the optical size of its type size, and the Full Proof has a Grade page. A free side keeps a sidebearing of 8 units at 144 pt. Yellow glyphs are donors where no green glyph has the construction (R3).
- Open: a few Arabic joins keep their length at 144 pt, because they are short or not level (Regular 14 forms, Black 51). The command lists them. The kerning is unchanged at the tighter spacing, and the word space is tight in Bold and Black at 144 pt. `make test` passes with no FAIL. `make check-changes` has not run. No glyph is green.
