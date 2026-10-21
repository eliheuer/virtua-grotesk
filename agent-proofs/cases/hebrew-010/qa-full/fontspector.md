## FontSpector report

fontspector version: 1.9.0






## Check results




<details><summary>[6] fonts/ttf/VirtuaGrotesk-SemiBold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni06440623 (unencoded): found 4, expected one of: [2, 3]
* twodotsverticalabovear (unencoded): found 1, expected one of: [2, 4]
* invertedDammaar (U+0657): found 3, expected one of: [1, 2]
* perMillear (U+0609): found 6, expected one of: [0, 4]
* seenSixdotsar (U+069C): found 4, expected one of: [5, 7, 9]
* smallHighTahar (U+0615): found 1, expected one of: [2, 3, 4]
* smallHighZainar (U+0617): found 1, expected one of: [2] [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ | * fr_Latn (French)           |
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* uni0637.fina: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0637.medi: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0637.init: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0638.fina: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0638.medi: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0638.init: from (72.0, 771.0) to (105.0, 768.0) is colinear with segment from (105.0, 768.0) to (183.0, 768.0)
* uni0647.fina: from (401.0, 111.0) to (389.0, 308.0) is colinear with segment from (389.0, 308.0) to (389.0, 316.0)
* uni0629.fina: from (401.0, 111.0) to (389.0, 308.0) is colinear with segment from (389.0, 308.0) to (389.0, 316.0)
* Itilde (U+0128): from (-12.0, 906.0) to (4.0, 918.0) is colinear with segment from (4.0, 918.0) to (100.0, 986.0)
... and 15 others [code: found-colinear-vectors]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? (outline_jaggy_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have jaggy segments:

* uni0635 (U+0635): Line(Line { p0: (788.0, 421.0), p1: (768.0, 113.0) })/Line(Line { p0: (768.0, 113.0), p1: (773.0, 152.0) }) = 3.5904704278819617 degrees
* uni0636 (U+0636): Line(Line { p0: (788.0, 421.0), p1: (768.0, 113.0) })/Line(Line { p0: (768.0, 113.0), p1: (773.0, 152.0) }) = 3.5904704278819617 degrees
* uni0646.fina: Line(Line { p0: (624.0, 272.0), p1: (604.0, 112.0) })/Line(Line { p0: (604.0, 112.0), p1: (609.0, 149.0) }) = 0.5710353731150118 degrees
* uni06BA.fina: Line(Line { p0: (624.0, 272.0), p1: (604.0, 112.0) })/Line(Line { p0: (604.0, 112.0), p1: (609.0, 149.0) }) = 0.5710353731150118 degrees
* uni0647.fina: Line(Line { p0: (523.0, 419.0), p1: (503.0, 112.0) })/Line(Line { p0: (503.0, 112.0), p1: (508.0, 149.0) }) = 3.968694758071248 degrees
* uni0647.fina: Line(Line { p0: (396.0, 149.0), p1: (401.0, 111.0) })/Line(Line { p0: (401.0, 111.0), p1: (389.0, 308.0) }) = 4.0100664566076984 degrees
* uni0647.medi: Line(Line { p0: (47.0, 149.0), p1: (52.0, 111.0) })/Line(Line { p0: (52.0, 111.0), p1: (47.0, 240.0) }) = 5.276202086531984 degrees
* uni0647.medi: Line(Line { p0: (159.0, 240.0), p1: (153.0, 111.0) })/Line(Line { p0: (153.0, 111.0), p1: (159.0, 149.0) }) = 6.309625848829209 degrees
* uni0629.fina: Line(Line { p0: (523.0, 419.0), p1: (503.0, 112.0) })/Line(Line { p0: (503.0, 112.0), p1: (508.0, 149.0) }) = 3.968694758071248 degrees
... and 15 others [code: found-jaggy-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have overlapping path segments:

* invertedDammaar (U+0657): Quad(QuadBez { p0: (124.0, 923.5), p1: (125.0, 923.0), p2: (122.0, 925.0) }) has the same coordinates as a previous segment. [code: overlapping-path-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* uni0635 (U+0635): Line(Line { p0: (42.0, -70.0), p1: (40.0, 167.0) }) (angle: 90.48 degrees, expected: 90.00 degrees)
* uni0636 (U+0636): Line(Line { p0: (42.0, -70.0), p1: (40.0, 167.0) }) (angle: 90.48 degrees, expected: 90.00 degrees)
* uni0639.fina: Line(Line { p0: (641.0, 104.0), p1: (845.0, 105.0) }) (angle: 0.28 degrees, expected: 0.00 degrees)
* uni063A.fina: Line(Line { p0: (641.0, 104.0), p1: (845.0, 105.0) }) (angle: 0.28 degrees, expected: 0.00 degrees) [code: found-semi-vertical]



</div>
</details>


</div>
</details>


<details><summary>[4] fonts/ttf/VirtuaGrotesk-Regular.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Directory name in GFonts repo structure must
    match NameID 1 of the regular. (googlefonts/repo/dirname_matches_nameid_1)</summary>
    <div>








- 🔥 **FAIL** Family name on the name table ('Virtua Grotesk') does not match directory name in the repo structure ('ttf'). Expected 'virtuagrotesk'. [code: mismatch]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0647.init (unencoded): found 2, expected one of: [1, 3]
* uni0654064C (unencoded): found 5, expected one of: [3, 6]
* perMillear (U+0609): found 6, expected one of: [0, 4]
* seenSixdotsar (U+069C): found 4, expected one of: [5, 7, 9]
* smallHighTahar (U+0615): found 1, expected one of: [2, 3, 4] [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ | * fr_Latn (French)           |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* Itilde (U+0128): from (-52.0, 906.0) to (-36.0, 918.0) is colinear with segment from (-36.0, 918.0) to (60.0, 986.0)
* itilde (U+0129): from (-44.0, 714.0) to (-28.0, 726.0) is colinear with segment from (-28.0, 726.0) to (68.0, 794.0)
* Utilde (U+0168): from (204.0, 906.0) to (220.0, 918.0) is colinear with segment from (220.0, 918.0) to (316.0, 986.0)
* utilde (U+0169): from (128.0, 714.0) to (144.0, 726.0) is colinear with segment from (144.0, 726.0) to (240.0, 794.0)
* Etilde (U+1EBC): from (192.0, 906.0) to (208.0, 918.0) is colinear with segment from (208.0, 918.0) to (304.0, 986.0)
* etilde (U+1EBD): from (144.0, 714.0) to (160.0, 726.0) is colinear with segment from (160.0, 726.0) to (256.0, 794.0)
* Atilde (U+00C3): from (190.0, 906.0) to (206.0, 918.0) is colinear with segment from (206.0, 918.0) to (302.0, 986.0)
* Ntilde (U+00D1): from (220.0, 906.0) to (236.0, 918.0) is colinear with segment from (236.0, 918.0) to (332.0, 986.0)
* Otilde (U+00D5): from (232.0, 906.0) to (248.0, 918.0) is colinear with segment from (248.0, 918.0) to (344.0, 986.0)
... and 5 others [code: found-colinear-vectors]



</div>
</details>


</div>
</details>


<details><summary>[7] fonts/ttf/VirtuaGrotesk-Bold.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni06440623 (unencoded): found 4, expected one of: [2, 3]
* uni06440625 (unencoded): found 4, expected one of: [2, 3]
* uni061F (U+061F): found 1, expected one of: [2, 64]
* twodotsverticalabovear (unencoded): found 1, expected one of: [2, 4]
* uni0651 (U+0651): found 3, expected one of: [1, 2]
* uni0651064B (unencoded): found 5, expected one of: [3, 4]
* uni0651064D (unencoded): found 5, expected one of: [3, 4]
* uni0651064E (unencoded): found 4, expected one of: [2, 3]
* uni0651064F (unencoded): found 5, expected one of: [2, 3, 4]
... and 6 others [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              |
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ | * fr_Latn (French)           |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* Itilde (U+0128): from (8.0, 906.0) to (24.0, 918.0) is colinear with segment from (24.0, 918.0) to (120.0, 986.0)
* itilde (U+0129): from (-12.0, 714.0) to (4.0, 726.0) is colinear with segment from (4.0, 726.0) to (100.0, 794.0)
* Utilde (U+0168): from (228.0, 906.0) to (244.0, 918.0) is colinear with segment from (244.0, 918.0) to (340.0, 986.0)
* utilde (U+0169): from (192.0, 714.0) to (208.0, 726.0) is colinear with segment from (208.0, 726.0) to (304.0, 794.0)
* Etilde (U+1EBC): from (208.0, 906.0) to (224.0, 918.0) is colinear with segment from (224.0, 918.0) to (320.0, 986.0)
* etilde (U+1EBD): from (160.0, 714.0) to (176.0, 726.0) is colinear with segment from (176.0, 726.0) to (272.0, 794.0)
* Atilde (U+00C3): from (228.0, 906.0) to (244.0, 918.0) is colinear with segment from (244.0, 918.0) to (340.0, 986.0)
* Ntilde (U+00D1): from (244.0, 906.0) to (260.0, 918.0) is colinear with segment from (260.0, 918.0) to (356.0, 986.0)
* Otilde (U+00D5): from (264.0, 906.0) to (280.0, 918.0) is colinear with segment from (280.0, 918.0) to (376.0, 986.0)
... and 5 others [code: found-colinear-vectors]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph (outline_direction)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have a counter-clockwise outer contour:

* gafsarkashabovear has a path with no bounds (probably a single point)
* gafar (U+06AF) has a path with no bounds (probably a single point)
* gafar.init has a path with no bounds (probably a single point)
* gafar.medi has a path with no bounds (probably a single point) [code: ccw-outer-contour]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? (outline_jaggy_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have jaggy segments:

* uni0631.fina: Line(Line { p0: (540.0, 320.0), p1: (514.0, 122.0) })/Line(Line { p0: (514.0, 122.0), p1: (522.0, 176.0) }) = 0.9460828419573434 degrees
* uni0632.fina: Line(Line { p0: (540.0, 320.0), p1: (514.0, 122.0) })/Line(Line { p0: (514.0, 122.0), p1: (522.0, 176.0) }) = 0.9460828419573434 degrees
* uni0639.fina: Line(Line { p0: (414.0, 104.0), p1: (420.0, 176.0) })/Line(Line { p0: (420.0, 176.0), p1: (412.0, 110.0) }) = 2.1475854282982483 degrees
* uni0639.fina: Line(Line { p0: (644.0, 110.0), p1: (638.0, 176.0) })/Line(Line { p0: (638.0, 176.0), p1: (642.0, 108.0) }) = 1.8279682443051597 degrees
* uni063A.fina: Line(Line { p0: (414.0, 104.0), p1: (420.0, 176.0) })/Line(Line { p0: (420.0, 176.0), p1: (412.0, 110.0) }) = 2.1475854282982483 degrees
* uni063A.fina: Line(Line { p0: (644.0, 110.0), p1: (638.0, 176.0) })/Line(Line { p0: (638.0, 176.0), p1: (642.0, 108.0) }) = 1.8279682443051597 degrees
* uni0641 (U+0641): Line(Line { p0: (250.0, 176.0), p1: (686.0, 176.0) })/Quad(QuadBez { p0: (686.0, 176.0), p1: (622.0, 185.0), p2: (571.0, 211.5) }) = 8.004728857292882 degrees
* uni06A4 (U+06A4): Line(Line { p0: (250.0, 176.0), p1: (686.0, 176.0) })/Quad(QuadBez { p0: (686.0, 176.0), p1: (622.0, 185.0), p2: (571.0, 211.5) }) = 8.004728857292882 degrees
* uni06A1 (U+06A1): Line(Line { p0: (250.0, 176.0), p1: (686.0, 176.0) })/Quad(QuadBez { p0: (686.0, 176.0), p1: (622.0, 185.0), p2: (571.0, 211.5) }) = 8.004728857292882 degrees
... and 30 others [code: found-jaggy-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have overlapping path segments:

* gafsarkashabovear: Quad(QuadBez { p0: (178.0, 668.0), p1: (178.0, 668.0), p2: (178.0, 668.0) }) has the same coordinates as a previous segment.
* gafar (U+06AF): Quad(QuadBez { p0: (489.0, 894.0), p1: (489.0, 894.0), p2: (489.0, 894.0) }) has the same coordinates as a previous segment.
* gafar.init: Quad(QuadBez { p0: (259.0, 894.0), p1: (259.0, 894.0), p2: (259.0, 894.0) }) has the same coordinates as a previous segment.
* gafar.medi: Quad(QuadBez { p0: (371.0, 894.0), p1: (371.0, 894.0), p2: (371.0, 894.0) }) has the same coordinates as a previous segment. [code: overlapping-path-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* uni0635 (U+0635): Line(Line { p0: (30.0, -70.0), p1: (28.0, 176.0) }) (angle: 90.47 degrees, expected: 90.00 degrees)
* uni0636 (U+0636): Line(Line { p0: (30.0, -70.0), p1: (28.0, 176.0) }) (angle: 90.47 degrees, expected: 90.00 degrees)
* section (U+00A7): Line(Line { p0: (88.0, 41.0), p1: (213.0, 42.0) }) (angle: 0.46 degrees, expected: 0.00 degrees) [code: found-semi-vertical]



</div>
</details>


</div>
</details>


<details><summary>[1] fonts/variable</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** fonts/variable/VirtuaGrotesk[wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 127 others

Or you can add the above codepoints to one of the subsets supported by the font: hebrew, latin-ext, latin [code: unreachable-subsetting]



</div>
</details>


</div>
</details>


<details><summary>[2] fonts/variable/VirtuaGrotesk[wght].ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0645.medi (unencoded): found 4, expected one of: [2]
* uni0647.init (unencoded): found 2, expected one of: [1, 3]
* uni0654064C (unencoded): found 5, expected one of: [3, 6]
* perMillear (U+0609): found 6, expected one of: [0, 4]
* seenSixdotsar (U+069C): found 4, expected one of: [5, 7, 9] [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              |
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ | * fr_Latn (French)           |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              | [code: warning-language-shaping]



</div>
</details>


</div>
</details>


<details><summary>[5] fonts/ttf/VirtuaGrotesk-Medium.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0647.init (unencoded): found 2, expected one of: [1, 3]
* uni0654064C (unencoded): found 5, expected one of: [3, 6]
* perMillear (U+0609): found 6, expected one of: [0, 4]
* seenSixdotsar (U+069C): found 4, expected one of: [5, 7, 9]
* smallHighTahar (U+0615): found 1, expected one of: [2, 3, 4] [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ | * fr_Latn (French)           |
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ŧ |                              |
|   The following auxiliary characters are missing from the font: ŧ |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* uni0651064C: from (42.0, 987.0) to (74.0, 985.0) is colinear with segment from (74.0, 985.0) to (76.0, 985.0)
* uni0651064C: from (232.0, 987.0) to (264.0, 985.0) is colinear with segment from (264.0, 985.0) to (266.0, 985.0)
* Itilde (U+0128): from (-32.0, 906.0) to (-16.0, 918.0) is colinear with segment from (-16.0, 918.0) to (80.0, 986.0)
* itilde (U+0129): from (-33.0, 714.0) to (-17.0, 726.0) is colinear with segment from (-17.0, 726.0) to (79.0, 794.0)
* Utilde (U+0168): from (212.0, 906.0) to (228.0, 918.0) is colinear with segment from (228.0, 918.0) to (324.0, 986.0)
* utilde (U+0169): from (149.0, 714.0) to (165.0, 726.0) is colinear with segment from (165.0, 726.0) to (261.0, 794.0)
* Etilde (U+1EBC): from (197.0, 906.0) to (213.0, 918.0) is colinear with segment from (213.0, 918.0) to (309.0, 986.0)
* etilde (U+1EBD): from (149.0, 714.0) to (165.0, 726.0) is colinear with segment from (165.0, 726.0) to (261.0, 794.0)
* Atilde (U+00C3): from (203.0, 906.0) to (219.0, 918.0) is colinear with segment from (219.0, 918.0) to (315.0, 986.0)
... and 7 others [code: found-colinear-vectors]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? (outline_jaggy_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have jaggy segments:

* uni06440627: Quad(QuadBez { p0: (174.5, 150.5), p1: (160.0, 128.0), p2: (157.0, 108.0) })/Line(Line { p0: (157.0, 108.0), p1: (163.0, 123.0) }) = 13.270643876403643 degrees
* uni06440627: Line(Line { p0: (338.0, 123.0), p1: (345.0, 107.0) })/Quad(QuadBez { p0: (345.0, 107.0), p1: (337.0, 131.0), p2: (325.0, 152.0) }) = 5.194428907734729 degrees
* uni06440623: Quad(QuadBez { p0: (174.5, 150.5), p1: (160.0, 128.0), p2: (157.0, 108.0) })/Line(Line { p0: (157.0, 108.0), p1: (163.0, 123.0) }) = 13.270643876403643 degrees
* uni06440623: Line(Line { p0: (338.0, 123.0), p1: (345.0, 107.0) })/Quad(QuadBez { p0: (345.0, 107.0), p1: (337.0, 131.0), p2: (325.0, 152.0) }) = 5.194428907734729 degrees
* uni06440625: Quad(QuadBez { p0: (174.5, 150.5), p1: (160.0, 128.0), p2: (157.0, 108.0) })/Line(Line { p0: (157.0, 108.0), p1: (163.0, 123.0) }) = 13.270643876403643 degrees
* uni06440625: Line(Line { p0: (338.0, 123.0), p1: (345.0, 107.0) })/Quad(QuadBez { p0: (345.0, 107.0), p1: (337.0, 131.0), p2: (325.0, 152.0) }) = 5.194428907734729 degrees
* uni06440622: Quad(QuadBez { p0: (174.5, 150.5), p1: (160.0, 128.0), p2: (157.0, 108.0) })/Line(Line { p0: (157.0, 108.0), p1: (163.0, 123.0) }) = 13.270643876403643 degrees
* uni06440622: Line(Line { p0: (338.0, 123.0), p1: (345.0, 107.0) })/Quad(QuadBez { p0: (345.0, 107.0), p1: (337.0, 131.0), p2: (325.0, 152.0) }) = 5.194428907734729 degrees
* uni06440671: Quad(QuadBez { p0: (174.5, 150.5), p1: (160.0, 128.0), p2: (157.0, 108.0) })/Line(Line { p0: (157.0, 108.0), p1: (163.0, 123.0) }) = 13.270643876403643 degrees
... and 5 others [code: found-jaggy-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* uni0637.fina: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0637.medi: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0637.init: Line(Line { p0: (552.0, 220.0), p1: (936.0, 217.0) }) (angle: -0.45 degrees, expected: 0.00 degrees)
* uni0637.init: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0638.fina: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0638.medi: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0638.init: Line(Line { p0: (552.0, 220.0), p1: (936.0, 217.0) }) (angle: -0.45 degrees, expected: 0.00 degrees)
* uni0638.init: Line(Line { p0: (936.0, 338.0), p1: (552.0, 335.0) }) (angle: -179.55 degrees, expected: -180.00 degrees)
* uni0639.fina: Line(Line { p0: (641.0, 100.0), p1: (839.0, 101.0) }) (angle: 0.29 degrees, expected: 0.00 degrees)
... and 1 others [code: found-semi-vertical]



</div>
</details>


</div>
</details>


<details><summary>[1] fonts/ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Regular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 127 others

Or you can add the above codepoints to one of the subsets supported by the font: hebrew, latin-ext, latin [code: unreachable-subsetting]




- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Medium.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 127 others

Or you can add the above codepoints to one of the subsets supported by the font: hebrew, latin-ext, latin [code: unreachable-subsetting]




- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-SemiBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 127 others

Or you can add the above codepoints to one of the subsets supported by the font: hebrew, latin-ext, latin [code: unreachable-subsetting]




- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Bold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 127 others

Or you can add the above codepoints to one of the subsets supported by the font: hebrew, latin-ext, latin [code: unreachable-subsetting]



</div>
</details>


</div>
</details>






### Summary

| 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP |
| ---|---|---|---|---|
| 1 | 28 | 39 | 525 | 299 |
| 0% | 3% | 4% | 59% | 34% |
