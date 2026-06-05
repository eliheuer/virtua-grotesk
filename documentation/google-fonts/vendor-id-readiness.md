# Vendor ID Readiness

This generated report tracks the OS/2 vendor ID decision surface for
Google Fonts onboarding. The maintainer-confirmed value is `FTGD`,
registered to Font Garden in Microsoft's registered font vendor list.

## Summary

- Source UFO vendor IDs: `FTGD`
- Generated font vendor IDs: `FTGD`
- Microsoft registered vendor entry confirmed: yes
- Confirmed vendor ID owner: `FTGD` = Font Garden
- Registered vendor list verification date: 2026-05-24
- Source UFO vendor IDs internally consistent: yes
- Generated font vendor IDs internally consistent: yes
- Source and generated vendor states aligned: yes
- Fontspector `googlefonts/vendor_id` warnings: 0
- Decision log status: decided
- Vendor ID decision unresolved: no
- Vendor ID apply helper present: yes
- Vendor ID apply helper validates four-character non-NONE IDs: yes
- Vendor ID apply helper dry-runs by default: yes

## Source UFOs

| UFO | openTypeOS2VendorID |
| --- | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | `FTGD` |
| `sources/VirtuaGrotesk-Bold.ufo` | `FTGD` |

## Generated Fonts

| Font | OS/2 achVendID | Status |
| --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | `FTGD` | confirmed registered: Font Garden |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | `FTGD` | confirmed registered: Font Garden |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | `FTGD` | confirmed registered: Font Garden |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | `FTGD` | confirmed registered: Font Garden |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | `FTGD` | confirmed registered: Font Garden |

## Applied Decision

- `FTGD` is applied in both active UFO `fontinfo.plist` files.
- The generated variable font and static QA fonts inherit `FTGD`.
- Fontspector currently reports 0 `googlefonts/vendor_id` warnings.
- Re-run `make vendor-id-check` after any source metadata or build changes.

References:

- https://googlefonts.github.io/gf-guide/qa.html
- https://github.com/fonttools/fontspector
- https://learn.microsoft.com/en-us/typography/vendors/
