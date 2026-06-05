# Google Fonts Decision Answer Sheet

This generated sheet is the quickest maintainer-facing place to answer
currently open Google Fonts onboarding decisions. It is priority-sorted from the
canonical question file and does not make decisions on the maintainer's
behalf.

Use this flow:

1. Answer a row here.
2. Record the accepted answer in `documentation/google-fonts/google-fonts-decisions.md`.
3. Apply the decision to the listed source, metadata, or downstream package surfaces.
4. Rerun `make preflight` so proof evidence and generated reports stay synchronized.

Canonical files:

- `documentation/google-fonts/google-fonts-decision-questions.md`
- `documentation/google-fonts/google-fonts-decisions.md`
- `documentation/google-fonts/decision-readiness.md`

## Priority 3

### PUA Icon Block

Why answer: Affects glyph scope, subsetting review, and whether PUA rationale belongs in the issue.

Question:

Should the private-use icon block ship in the first Google Fonts submission?

Current guidance/evidence:

Current local evidence:
- `documentation/google-fonts/pua-scope.md` reports 23 encoded PUA codepoints in every
  built font and both active source UFOs.
- The encoded PUA set currently uses selected codepoints in U+E000 through
  U+E021, plus U+F000 through U+F003; it is not a continuous encoded range.
- The local `google/fonts` checkout shows PUA precedent in shipped packages,
  including `ScheherazadeNew` and `Kedebideri` at U+F130/U+F131, but that is
  precedent for explicit rationale, not a blanket approval.
- `documentation/google-fonts/glyph-reachability.md` reports 17 unique unreachable glyphs;
  those warnings are Arabic helper/mark glyphs, not the encoded PUA glyphs.
- If the PUA block ships, the Google Fonts issue/PR should explain why private
  encoded symbols belong in the public catalog package.
- If the PUA block is deferred, remove or unencode it in both masters and
  regenerate `documentation/google-fonts/pua-scope.md`, `documentation/google-fonts/glyph-reachability.md`,
  and `documentation/google-fonts/fontspector-warnings.md`.

Recommended answer:
Defer or remove the PUA icon block for the first submission unless there is a
clear product reason to keep it.

Apply targets:

- source glyphset
- `documentation/google-fonts/google-fonts-submission-handoff.md`
- `documentation/google-fonts/google-fonts-metadata-review.md`

Maintainer answer:

```text
TBD by maintainer
```

### Kerning Scope

Why answer: Decides whether kerning warnings are blockers or explicitly deferred.

Question:

Should kerning be completed before the first Google Fonts PR?

Current guidance/evidence:

Current local evidence:
- `documentation/google-fonts/kerning-readiness.md` reports source kerning in both masters:
  Regular and Bold each have 77 pairs, 46 left groups, and 43 right groups.
- The generated variable font and static TTFs expose GPOS `kern`.
- Fontspector currently reports 0 `gpos_kerning_info` warnings.
- `make kerning-proof-check` runs Google Fonts `gftools qa --proof` and the
  latest HTML proof output covers Regular, Medium, SemiBold, and Bold.
- If kerning is completed now, source kerning needs to be compatible across
  masters and generated variable/static fonts should expose GPOS `kern`.
- If kerning is deferred, the deferral should be explicit in
  `documentation/google-fonts/google-fonts-decisions.md`, the Add Font issue, and the
  submission handoff, and the generated `gftools qa --proof` output should
  still be reviewed as the visual spacing/kerning proof.

Recommended answer:
Yes, if this is intended as a polished first public submission. If not, record
the deferral explicitly in the Google Fonts issue.

Apply targets:

- UFO kerning/groups/features
- `build.sh`
- `make kerning-proof-check`
- `documentation/google-fonts/kerning-readiness.md`
- `documentation/google-fonts/fontspector-warnings.md`

Maintainer answer:

```text
TBD by maintainer
```

References:

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
