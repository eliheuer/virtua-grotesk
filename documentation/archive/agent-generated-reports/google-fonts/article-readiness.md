# Article Readiness

This generated report checks the Google Fonts Article draft against
the current Article guide requirements that can be verified locally.
It does not replace copy review by Google Fonts.

## Summary

- Article file: `documentation/google-fonts/ARTICLE.en_us.html`
- Article exists: yes
- Text length: 413 words
- More than 100 text characters: yes
- Around 500 words target met: yes
- Primary script target from metadata: `missing`
- Localized Arabic text present: yes
- Upstream repository link present: yes
- Placeholder upstream URL still present: no
- Images referenced: 1
- Referenced images exist locally: yes
- Raster images within 1.75 MB limit: yes
- Images meet 1000 px recommended width: yes
- Image license/provenance file exists: yes
- Article image sources covered by provenance file: 1 / 1
- Disallowed HTML tags: 0
- Forbidden HTML tags: 0

## HTML Tags

- Used tags: `a, figcaption, figure, img, p`
- Disallowed tags: `none`
- Forbidden tags: `none`

## Links

- `https://github.com/eliheuer/virtua-grotesk`

## Images

| Source | Exists locally | Size | Dimensions | Provenance documented |
| --- | --- | --- | --- | --- |
| `readme-specimen.png` | yes | 434000 bytes | 3072 x 2048 | yes |

## Apply Before Packaging

- Replace the placeholder upstream repository URL after the public URL
  decision is confirmed.
- Keep Article images in the downstream `article/` directory and keep
  `documentation/assets/image-license.txt` current for provenance review.
- Confirm whether Google Fonts wants additional Arabic/localized
  Article text for the `Arab` primary script before final packaging.
- If the package uses Article content, do not also ship a duplicate
  legacy `DESCRIPTION.en_us.html` unless Google Fonts asks for it.
- Rerun `make preflight` after Article text, image, or package
  source-mapping changes.

References:

- https://googlefonts.github.io/gf-guide/article.html
- https://googlefonts.github.io/gf-guide/package.html
