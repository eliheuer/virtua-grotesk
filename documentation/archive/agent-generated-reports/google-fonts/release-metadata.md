# Release Metadata

This generated report ties the release checklist to current source UFO
versions and built font name ID 5 values. Use it before tagging the
upstream source state for Google Fonts packaging.

## Summary

- Source version: `1.000`
- Expected built name ID 5 prefix: `Version 1.000`
- Suggested first-submission tag: `v1.000`
- Built fonts match source version: yes

## Source UFO Versions

| Source | versionMajor | versionMinor | Version string |
| --- | ---: | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist` | 1 | 0 | `1.000` |
| `sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist` | 1 | 0 | `1.000` |

## Built Font Versions

| Font | name ID 5 | Matches source version |
| --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `Version 1.000` | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | yes |

## Before Tagging

- Confirm the version strategy decision in `documentation/google-fonts/google-fonts-decisions.md`.
- Confirm the final upstream tag and commit in `documentation/google-fonts/google-fonts-release-checklist.md`.
- Regenerate this report with `make preflight` after changing source or build versions.
