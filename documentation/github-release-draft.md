# GitHub Release Draft

This generated draft records the GitHub release command and checks needed
for the selected Google Fonts `latest-release` Packager path. It does
not create a tag, push a tag, publish a release, or contact GitHub.

## Summary

- Upstream URL: `https://github.com/eliheuer/virtua-grotesk`
- Current branch: `main`
- Current commit: `e30fc2fdfc541b2832ac6de68902eae8478fedcf`
- Current short commit: `e30fc2f`
- Source version: `1.000`
- Release tag: `v1.000`
- Release title: `Virtua Grotesk 1.000`
- Local tag already exists: no
- Working tree clean: no
- Local archive: `dist/VirtuaGrotesk-1.000.zip`
- Local archive exists: yes
- Local archive contains expected files: yes
- Local archive hashes match source files: no
- Local archive metadata deterministic: yes
- Local archive SHA-256: `47f70853bcfa606d0c9c8fee8bd4a334c93007fd8a3dc80c8837c9d617233e2a`
- Local archive has unsafe paths: no
- Preview archive filename matches local archive: yes
- Release notes file: `documentation/github-release-notes.md`
- Release notes source commit final: no
- Downstream preview archive URL: `https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip`
- Downstream preview archive URL contract: GitHub release download `.zip`
- Downstream preview source commit: `Pending final release/source commit`

## Release Asset Contract

| Source path in archive | Required by downstream `source.files` |
| --- | --- |
| `OFL.txt` | yes |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes |
| `documentation/ARTICLE.en_us.html` | yes |
| `documentation/readme-specimen.png` | yes |

## Draft Release Notes

```markdown
Virtua Grotesk 1.000 release candidate for Google Fonts onboarding.

This release archive contains the files referenced by downstream
`METADATA.pb` `source.files` for the selected latest-release Packager
path.

Source commit: e30fc2fdfc541b2832ac6de68902eae8478fedcf
Google Fonts source mode: latest-release

Archive contents:
- `OFL.txt`
- `fonts/variable/VirtuaGrotesk[wght].ttf`
- `documentation/ARTICLE.en_us.html`
- `documentation/readme-specimen.png`
```

## Final Command Draft

Run this only after drawing/source work is complete, the final source
commit is made, the `v1.000` tag is created and pushed, and
`make release-archive-verify` plus `make downstream-metadata-check`
both pass, the generated release notes `Source commit` matches the
final downstream `source.commit`, and the archive SHA-256 above is
the intended release asset.

```bash
gh release create v1.000 dist/VirtuaGrotesk-1.000.zip \
  --repo eliheuer/virtua-grotesk \
  --title "Virtua Grotesk 1.000" \
  --notes-file documentation/github-release-notes.md
```

## Post-Publish Verification

Run these checks after the GitHub release asset is uploaded and
before applying downstream metadata or running Packager. They verify
that the public release URL resolves to the same archive reviewed
locally.

```bash
gh release view v1.000 --repo eliheuer/virtua-grotesk
gh release download v1.000 --repo eliheuer/virtua-grotesk --pattern VirtuaGrotesk-1.000.zip --dir /tmp/virtua-grotesk-release-check
shasum -a 256 /tmp/virtua-grotesk-release-check/VirtuaGrotesk-1.000.zip
unzip -l /tmp/virtua-grotesk-release-check/VirtuaGrotesk-1.000.zip
./venv/bin/python scripts/verify_release_archive.py --archive /tmp/virtua-grotesk-release-check/VirtuaGrotesk-1.000.zip --expected-sha256 47f70853bcfa606d0c9c8fee8bd4a334c93007fd8a3dc80c8837c9d617233e2a
GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check
GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run
```

Expected SHA-256: `47f70853bcfa606d0c9c8fee8bd4a334c93007fd8a3dc80c8837c9d617233e2a`

The downloaded archive must contain exactly the `source.files` paths
listed in the Release Asset Contract above, and the downstream
`source.archive_url` must point at this uploaded GitHub release
download `.zip` asset before the no-PR Packager dry run.

## Before Publishing

1. Run `make preflight` from the final source commit.
2. Run `make release-archive-build` and `make release-archive-verify`.
3. Create and push the final tag with the same value recorded in downstream metadata.
4. Replace the pending downstream `source.commit` value with the final commit hash.
5. Regenerate this draft so the release notes `Source commit` matches the final downstream `source.commit`.
6. Confirm `source.archive_url` points to the uploaded GitHub release download `.zip` asset.
7. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`.
8. Run the no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.

References:

- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/making-pr.html
