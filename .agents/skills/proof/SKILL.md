---
name: proof
description: Generate and review the multi-page PDF proof for Virtua Grotesk.
---

# Proof

Run `make proof` from the repository root. It builds the fonts and runs
`designbot proof` on `fonts/variable/VirtuaGrotesk[wght].ttf`, writing
`documentation/proofs/proof.pdf`.

For an explicitly supplied font, use:

```sh
designbot proof "<font-path>" --output "<output.pdf>"
```

Render and inspect the PDF before summarizing its pages or visual quality.
Report the output path and any visible issues. Do not infer page contents from
an old fixed page list; designbot generates the proof from the font.
