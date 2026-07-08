# Source UFO Metadata

This report records metadata from the active UFO sources. Use it with `documentation/source/generated-font-metadata.md` to confirm that source metadata and built binary metadata stay aligned.

## Summary

| UFO | Family | Style | Version | Glyphs | features.fea |
| --- | --- | --- | --- | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | Virtua Grotesk | Regular | 1.0 | 690 | yes |
| `sources/VirtuaGrotesk-Bold.ufo` | Virtua Grotesk | Bold | 1.0 | 690 | yes |

## Metrics

| UFO | UPM | Ascender | Descender | x-height | Cap height | Typo asc/desc/gap | Win asc/desc | hhea asc/desc/gap |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | 1024 | 768 | -256 | 576 | 768 | 1024/-296/0 | 1094/438 | 1024/-296/0 |
| `sources/VirtuaGrotesk-Bold.ufo` | 1024 | 768 | -256 | 576 | 768 | 1024/-296/0 | 1094/438 | 1024/-296/0 |

## License and Embedding

| UFO | Copyright | License | License URL | Manufacturer URL | OS/2 fsType source | Vendor ID |
| --- | --- | --- | --- | --- | --- | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk) | This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org | https://openfontlicense.org | https://github.com/eliheuer/virtua-grotesk | unset | FTGD |
| `sources/VirtuaGrotesk-Bold.ufo` | Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk) | This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org | https://openfontlicense.org | https://github.com/eliheuer/virtua-grotesk | unset | FTGD |

## Review Notes

- `openTypeOS2Type` should remain unset so generated fonts are installable.
- Vendor ID should remain the maintainer-confirmed registered value `FTGD` for Font Garden.
- Copyright should match `OFL.txt` line 1 and generated name ID 0.
- Source metrics should match the generated vertical metrics report.
