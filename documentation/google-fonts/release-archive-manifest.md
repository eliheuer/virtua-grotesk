# Release Archive Manifest

This generated report is the local manifest for the GitHub release/archive
planned for Google Fonts Packager `--latest-release` mode. It checks the
`source.files` paths from the downstream metadata preview and records the
local file state, sizes, and SHA-256 hashes that should match the final
release archive contents.

## Summary

- Mapping source: `documentation/google-fonts/google-fonts-downstream-package-preview.md`
- Selected source mode: `latest-release`
- Archive inputs expected: 4
- Archive inputs present locally: 4 / 4
- Missing archive inputs: 0
- Unsafe `source.files` paths: 0
- Duplicate `source.files` paths: 0
- Unsafe `dest_file` paths: 0
- Duplicate `dest_file` paths: 0
- Ignored archive inputs: 2
- Untracked archive inputs: 3
- Dirty archive inputs: 1
- Variable font newer than source/build inputs: no
- Newest source/build input: `build.sh`
- Local release archive: `dist/VirtuaGrotesk-1.000.zip`
- Preview release archive URL: `https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip`
- Preview release archive URL is GitHub release download `.zip`: yes
- Preview archive filename matches local archive: yes
- Local release archive exists: yes
- Local release archive contains expected files: yes
- Local release archive has extra files: no
- Local release archive has unsafe paths: no
- Local release archive hashes match source files: yes
- Local release archive metadata deterministic: yes
- Local release archive SHA-256: `7e174e10693f6ea4371720f0487a7cee67352f954ccd615b6abd8ecb5b252777`
- Suggested final release tag: `v1.000`
- Final GitHub release tag exists locally: no
- Final GitHub release archive URL recorded: pending

## Archive Inputs

| Source file | Destination in package | Purpose | Exists | Ignored | Tracked | Dirty | Size bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | license | yes | no | yes | no | 4399 | `98c008294f3e0b098a65f45ca5be5bc119afefcd38b29331874d2193c6cd1236` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | served variable font | yes | yes | no | no | 85952 | `dc72e50470ffe0034dfef7f796459b8019a1696e372bd1870985b11d7f6d4ad5` |
| `documentation/google-fonts/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | article HTML | yes | no | no | yes | 3389 | `492d00133ee66642319b6c64f930e720b8f8d813054d440b69417774548beaff` |
| `documentation/assets/readme-specimen.png` | `article/readme-specimen.png` | article image | yes | yes | no | no | 434000 | `7b2a4de1a90f5fd5b9f42e5757467a4f5168de2b89b9b29c3a493afd7052429c` |

## Local Release Archive

Run `make release-archive-build` to create `dist/VirtuaGrotesk-1.000.zip` from the current `source.files` mapping.

| Archive entry | Present | Size matches source | SHA-256 matches source | Deterministic metadata |
| --- | --- | --- | --- | --- |
| `OFL.txt` | yes | yes | yes | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | yes | yes | yes |
| `documentation/google-fonts/ARTICLE.en_us.html` | yes | yes | yes | yes |
| `documentation/assets/readme-specimen.png` | yes | yes | yes | yes |

## Final Release Gate

Before creating the GitHub release used by Google Fonts Packager:

1. Finish drawing/source work and rebuild the fonts.
2. Build the local review archive with `make release-archive-build`.
3. Regenerate this report with `make release-archive-check`.
4. Confirm every archive input above is present in the release archive at the same path.
5. Confirm the variable font hash here matches the released file.
6. Confirm the local release archive metadata is deterministic.
7. Confirm the GitHub release asset filename matches the preview `source.archive_url` and the URL is a release download ending in `.zip`.
8. Replace the pending downstream `source.commit` value and keep `source.archive_url` synchronized.
9. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check` and a no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.

Notes:

- The generated variable font may stay ignored in the public branch for this selected strategy.
- Article files can be committed or injected into the release archive, but Packager must be able to fetch them from the GitHub release download `.zip` URL.
- This report does not create a release or tag; it is a reproducibility checklist for the release/archive path.

References:

- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/upstream.html
