# Kerning Readiness

This generated report tracks the current Google Fonts kerning decision
surface. It records source kerning, generated font kerning tables, and
the Fontspector warning without changing spacing or drawing data.

## Summary

- Source kerning exists in at least one master: yes
- Source kerning exists in every master: no
- All built fonts expose GPOS `kern`: no
- All built static fonts expose GPOS `kern`: no
- Fontspector `gpos_kerning_info` warnings: 4
- `gftools qa --proof` importable: yes
- Latest `gftools qa --proof` HTML output present: yes
- Latest proof HTML file count: 16
- Latest proof covers expected instances: yes
- Decision status: open

## Source UFO Kerning

| UFO | kerning.plist | Pair count | Left groups | Right groups |
| --- | --- | --- | --- | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | no | 0 | 0 | 0 |
| `sources/VirtuaGrotesk-Bold.ufo` | yes | 77 | 46 | 43 |

## Built Font Kerning

| Font | `kern` table | GPOS `kern` feature | GPOS features |
| --- | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | no | yes | `kern` |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | no | no | `none` |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | no | no | `none` |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | no | no | `none` |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | no | no | `none` |

## Google Fonts Visual QA

This is part of the core QA process for Virtua Grotesk. Google Fonts
documentation separates automated checks from visual QA: the local
testing guide calls for checking kerning in local applications, and
the onboarder workflow says new-font QA includes proof review for
basic spacing and kerning. In current gftools this proof path is
exposed through `gftools qa --proof`.

| Tool or dependency | Ready |
| --- | --- |
| `venv/bin/gftools` | yes |
| `diffenator2` Python package | yes |
| `diff3proof` Python package | no |
| `gftools qa` importable | yes |
| Proof HTML files in `documentation/gftools-qa/Proof` | yes (16) |
| Proof covers Regular, Medium, SemiBold, Bold | yes |

Core proof command:

```bash
make kerning-proof-check
```

The Make target runs `gftools qa --proof` with `venv/bin` on `PATH`
so the Diffenator helper scripts installed by `gftools[qa]` can be
found by the generated Ninja proof steps.

`gftools qa --proof` also checks the live Google Fonts catalog at
`https://fonts.google.com/metadata/fonts` before rendering proofs.
Run it with network access available, or expect a DNS/connection
failure before any HTML proof files are refreshed.

Review the generated HTML before treating kerning, spacing, or a
kerning-deferral decision as final. The report is intentionally kept
under `documentation/gftools-qa/` and ignored by git because it is
generated evidence, not source.

If Google Fonts asks for browser-rendered image proofs, add `--imgs`
after the local Selenium/browser dependencies are installed.

## Apply After Maintainer Confirmation

- Decide whether kerning is required before the first Google Fonts PR.
- If kerning is in scope, make source kerning compatible across masters
  and verify generated variable and static fonts expose GPOS `kern`.
- Generate and review the `gftools qa --proof` HTML proof for spacing
  and kerning after kerning is added or explicitly deferred.
- If kerning is deferred, record the explicit reviewer-acceptable
  rationale in `documentation/google-fonts-decisions.md` and the
  submission handoff.
- Rerun `make preflight` and `make test` after kerning changes.

References:

- https://googlefonts.github.io/gf-guide/testing.html
- https://googlefonts.github.io/gf-guide/tools.html
- https://googlefonts.github.io/gf-guide/onboarder-workflow.html
