## Arabic letter dots are near-circular

Eli clarified on 2026-10-21 that Arabic letter dots should be close to perfect
circles, following the [published grid system](https://elih.net/blog/virtua-grotesk/).
Do not transfer the Hebrew mark treatment into Arabic letter dots or introduce
tilt, unequal width/height, or skewed extrema handles. Use four symmetric cubic
quarters with horizontal/vertical tangent handles and equal radii, respecting
the 8-unit machine grid. Preserve green human optical coordinates on the 2-grid.
Circular dots have no sharp corners to chamfer. This specifies letter-dot shape;
it is not an instruction to make every Arabic vowel mark circular.

[ARB-005 dot correction](../reviews/arabic-005/round-dots/README.md)
records the first trial: Bold diameter 224, radius 112 and handles 64, all on 8.
Those dimensions are a local candidate, not a mandated size for every dot or
weight. Measure radial deviation and inspect at text size; a circle-like box
alone does not establish circular curvature. Existing approved Regular dots
and attachment placement are preserved.
