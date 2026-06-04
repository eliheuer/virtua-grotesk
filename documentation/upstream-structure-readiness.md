# Upstream Structure Readiness

This generated report maps the repository to the Google Fonts upstream
structure and build-guide requirements that can be checked locally. It
does not claim that drawing, spacing, kerning, or script coverage is
complete.

## Summary

- Mandatory upstream paths present: 11 / 11
- AUTHORS.txt entries present: yes
- CONTRIBUTORS.txt entries present: yes
- OFL first line has copyright: yes
- README has short description: yes
- README has build instructions: yes
- README references an image: yes
- documentation/image-license.txt present: yes
- Active source inputs present: 4 / 4
- One-command build entrypoint present: yes
- `sources/config.yaml` uses gftools builder shape: yes
- build.sh invokes gftools builder: yes
- Expected generated font outputs present: 5 / 5
- Generated font outputs ignored by git: yes
- Generated source/build outputs ignored by git: yes
- Local venv ignored by git: yes
- Active source root UFOs: `VirtuaGrotesk-Bold.ufo, VirtuaGrotesk-Regular.ufo`
- Active source root designspaces: `VirtuaGrotesk.designspace`

## Mandatory Paths

| Path | Purpose | Exists | Ignored by git |
| --- | --- | --- | --- |
| `AUTHORS.txt` | author contact file | yes | no |
| `CONTRIBUTORS.txt` | contributor contact file | yes | no |
| `OFL.txt` | OFL license file | yes | no |
| `README.md` | project README | yes | no |
| `documentation` | expanded documentation and images | yes | no |
| `fonts` | generated font output directory | yes | yes |
| `fonts/ttf` | static TTF output directory | yes | yes |
| `fonts/variable` | variable TTF output directory | yes | yes |
| `sources` | source directory | yes | no |
| `requirements.txt` | Python requirements | yes | no |
| `.gitignore` | ignored local/generated files | yes | no |

## Active Source Inputs

| Path | Exists | Ignored by git |
| --- | --- | --- |
| `sources/config.yaml` | yes | no |
| `sources/VirtuaGrotesk.designspace` | yes | no |
| `sources/VirtuaGrotesk-Regular.ufo` | yes | no |
| `sources/VirtuaGrotesk-Bold.ufo` | yes | no |

## Generated Outputs

| Path | Exists | Ignored by git |
| --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | yes |
| `sources/instance_ufos` | yes | yes |
| `sources/.fontc-build` | yes | yes |
| `sources/build.ninja` | yes | yes |
| `sources/.ninja_log` | yes | yes |

## Documentation Inventory

- Documentation files: 133
- Article draft present: yes
- Description draft present: yes
- Image provenance present: yes
- README specimen image present: yes

## Apply Before Final Upstream Release

- Confirm whether generated fonts remain ignored, are committed on the
  public branch, or are exposed through a release/archive strategy.
- Keep generated build artifacts out of the source root except for
  documented, ignored local outputs.
- Rerun `make preflight` after build, documentation, source-layout,
  or package-source strategy changes.

References:

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/build.html
- https://github.com/googlefonts/googlefonts-project-template
