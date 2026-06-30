# Google Fonts Readiness

The finish line for Virtua Grotesk: a clean, complete Latin + Arabic variable
font published on Google Fonts. This is the living tracker the workflow drives
toward — update it as items close. The orientation in `AGENTS.md` points here.

## Definition of done

Virtua Grotesk is ready to submit when:

1. `make test` (Fontspector `googlefonts` profile) is **clean with no excludes** —
   the deferred checks in `scripts/check_gf_fonts.sh` are all removed and passing.
2. Masters interpolate (the master-compatibility report is clean) and the
   variable + static builds are clean.
3. `METADATA.pb` and the downstream `ofl/virtuagrotesk/` layout exist (produced
   by `/google-fonts-packaging`).
4. A PR to `google/fonts` is open and passing Google Fonts onboarding QA.

**The honest progress metric is the exclude list in `check_gf_fonts.sh`.** Every
exclude removed is a step closer; zero excludes means the drawing/QA work is
done. Do not re-add an exclude to force a green `make test` — the excludes are
the to-do list, not a setting.

## Where we are

Done:

- **Latin** — GF Latin Core complete (0 missing of 319 codepoints), broad
  accented Latin.
- **Masters interpolate** cleanly (0 blocking mismatches; width-only diffs are
  expected).
- **Kerning** — both masters kerned (Regular + Bold) over the same group set.
- **Arabic shaping** — the OpenType layer is built in both masters
  (`sources/*/features.fea`): `languagesystem arab dflt`, `init`/`medi`/`fina`
  positional substitution, `ccmp` mark composition, `mark`/`mkmk` positioning.
- **Pipeline** — build (`make build`), the GF QA gate (`make test`), proofs
  (`make proof` / `make specimen`), reports (`make reports`).

Remaining work, in priority order:

## 1. Arabic outline cleanup — TOP PRIORITY

The Arabic glyphs are drawn and shape correctly; their outlines need a cleanup
pass. The gate **excludes four checks** for this (`check_gf_fonts.sh`):
`outline_alignment_miss`, `outline_colinear_vectors`, `outline_semi_vertical`,
`contour_count`. Finishing Arabic = making those four pass with the excludes
removed.

The constraint that makes this delicate: **both masters must stay structurally
identical** (same contours, point counts, point types) or the variable build
breaks. Cleanup cannot just boolean-remove overlaps per master; it must keep
Regular and Bold in lockstep.

The loop:

1. **See the flagged glyphs.** Run the gate without the four Arabic excludes
   (temporarily drop those `--exclude-checkid` lines, or run Fontspector
   directly) to get the list of Arabic glyphs and exactly what each check
   reports. That list is the burn-down.
2. **Triage by issue.** Overlapping parts and wrong `contour_count` are the
   structural ones (they also threaten master compatibility); alignment /
   colinear / semi-vertical are point hygiene.
3. **Fix each glyph, both masters together.** Pick per glyph:
   - **Re-trace via `img2bez masters`** when there is a clean reference image —
     it produces interpolation-compatible Regular + Bold in one command, which is
     exactly the constraint here. Best for glyphs that were traced originally.
   - **Hand-clean in Runebender** (`make runebender`), mirroring every structural
     change across both masters. Best for small fixes.
4. **Validate.** `make reports` (master-compat clean) → `make build` →
   `make proof` → re-run the gate. The glyph is done when its checks pass.
5. **Repeat** until the four checks pass for the whole Arabic set, then **delete
   those excludes** from `check_gf_fonts.sh`.

### Current worklist (from the gate, 2026-06-30)

Running the gate with the four Arabic outline checks re-enabled shows the work is
small and specific. Two of the four already pass; only two have issues. The
report uses production names (`uniXXXX.fina`), not the UFO's friendly `beh-ar`
names — map them by codepoint.

- **`outline_colinear_vectors`, `outline_semi_vertical` — already passing.**
  Verify on the full `make test` font set, then delete these two excludes.
- **`contour_count` — 4 glyphs** (real drawing fixes; mirror across both masters):
  - `uni062C.fina` (jeem final): 4 contours, expected 2–3 — remove an overlap /
    stray contour.
  - `uni062D.fina` (hah final): 3, expected 1–2 — same.
  - `uni0635.init` (sad initial): 1, expected 2 — a contour is missing
    (dot/counter); add it.
  - `uni0636.init` (dad initial): 2, expected 3–5 — under-built; check the
    reference.
- **`outline_alignment_miss` — ~16 glyphs**, all on-curve points sitting 1–2.5
  units off the baseline (e.g. `uni0633.medi` Y=1, `uni0637.fina` Y=2.5,
  `uni0649`/`uni064A` Y=−1). Snap those near-zero Y coordinates to exactly 0 in
  both masters — bulk / scriptable, not redraws.

### Separate quick fix (not Arabic, currently FAILing the gate)

`whitespace_widths` FAIL: `space` is 200 units but `nbspace` (U+00A0) is 256 —
they must be equal. Set them to one value in both masters. This FAIL is outside
the excludes, so it blocks a clean `make test` independently of Arabic.

## 2. Latin language coverage (`shape_languages`)

`googlefonts/glyphsets/shape_languages` is excluded pending Latin extras (mark
anchors over ogonek / dotaccent bases, breve / macron composites). Add the
missing anchors / composites, keep masters compatible, remove the exclude.

## 3. Metadata + packaging

There is no `METADATA.pb` yet, and the repo is upstream-shaped, not the
`ofl/virtuagrotesk/` layout Google Fonts needs. Run `/google-fonts-packaging` to
produce `METADATA.pb` and the downstream layout; that also clears the
`googlefonts/metadata/unreachable_subsetting` exclude (it needs a real
`METADATA.pb` with the Arabic subset declared).

## 4. The submission

With zero excludes and packaging done, open the PR to `google/fonts` and work
through GF onboarding QA (`/google-fonts-onboarding`, `/google-fonts-qa`). The
`DESCRIPTION.en_us.html`, `ARTICLE.en_us.html`, `OFL.txt`, `AUTHORS.txt`, and
`CONTRIBUTORS.txt` are already prepared (`documentation/google-fonts/`, repo
root).

## Guardrails (every change)

- **Master compatibility is sacred.** `make reports` →
  `documentation/source/master-compatibility.md` must stay clean; mirror every
  structural edit across both masters.
- **Re-run `make preflight`** after drawing, kerning, or build changes, and
  re-review proofs.
- **The excludes are the to-do list.** Removing them is progress; re-adding them
  is hiding work.
