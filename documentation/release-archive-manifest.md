# Release Archive Manifest

This generated report is the local manifest for the GitHub release/archive
planned for Google Fonts Packager `--latest-release` mode. It checks the
`source.files` paths from the downstream metadata preview and records the
local file state, sizes, and SHA-256 hashes that should match the final
release archive contents.

## Summary

- Mapping source: `documentation/google-fonts-downstream-package-preview.md`
- Selected source mode: `latest-release`
- Archive inputs expected: 4
- Archive inputs present locally: 4 / 4
- Missing archive inputs: 0
- Unsafe `source.files` paths: 0
- Duplicate `source.files` paths: 0
- Unsafe `dest_file` paths: 0
- Duplicate `dest_file` paths: 0
- Ignored archive inputs: 1
- Untracked archive inputs: 1
- Dirty archive inputs: 0
- Variable font newer than source/build inputs: yes
- Newest source/build input: `sources/VirtuaGrotesk-Bold.ufo/glyphs/ogonek.glif`
- Local release archive: `dist/VirtuaGrotesk-1.000.zip`
- Preview release archive URL: `https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip`
- Preview release archive URL is GitHub release download `.zip`: yes
- Preview archive filename matches local archive: yes
- Local release archive exists: yes
- Local release archive contains expected files: yes
- Local release archive has extra files: no
- Local release archive has unsafe paths: no
- Local release archive hashes match source files: no
- Local release archive metadata deterministic: yes
- Local release archive SHA-256: `47f70853bcfa606d0c9c8fee8bd4a334c93007fd8a3dc80c8837c9d617233e2a`
- Suggested final release tag: `v1.000`
- Final GitHub release tag exists locally: no
- Final GitHub release archive URL recorded: pending

## Archive Inputs

| Source file | Destination in package | Purpose | Exists | Ignored | Tracked | Dirty | Size bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OFL.txt` | `OFL.txt` | license | yes | no | yes | no | 4399 | `98c008294f3e0b098a65f45ca5be5bc119afefcd38b29331874d2193c6cd1236` |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `VirtuaGrotesk[wght].ttf` | served variable font | yes | yes | no | no | 72984 | `e42f9de0d05750839281ab165ea1158b41677b0390631c97708a9d33cba92623` |
| `documentation/ARTICLE.en_us.html` | `article/ARTICLE.en_us.html` | article HTML | yes | no | yes | no | 3389 | `492d00133ee66642319b6c64f930e720b8f8d813054d440b69417774548beaff` |
| `documentation/readme-specimen.png` | `article/readme-specimen.png` | article image | yes | no | yes | no | 434000 | `7b2a4de1a90f5fd5b9f42e5757467a4f5168de2b89b9b29c3a493afd7052429c` |

## Local Release Archive

Run `make release-archive-build` to create `dist/VirtuaGrotesk-1.000.zip` from the current `source.files` mapping.

| Archive entry | Present | Size matches source | SHA-256 matches source | Deterministic metadata |
| --- | --- | --- | --- | --- |
| `OFL.txt` | yes | yes | yes | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | no | no | yes |
| `documentation/ARTICLE.en_us.html` | yes | yes | yes | yes |
| `documentation/readme-specimen.png` | yes | yes | yes | yes |

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
