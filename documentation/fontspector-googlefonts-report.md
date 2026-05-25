## FontSpector report

fontspector version: 1.6.0






## Check results




<details><summary>[2] fonts/variable</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check Google Fonts glyph coverage. (googlefonts/glyph_coverage)</summary>
    <div>








- 🔥 **FAIL** fonts/variable/VirtuaGrotesk[wght].ttf missing required codepoints:

* 0x002B: PLUS SIGN
* 0x003C: LESS-THAN SIGN
* 0x003D: EQUALS SIGN
* 0x003E: GREATER-THAN SIGN
* 0x0040: COMMERCIAL AT
* 0x005B: LEFT SQUARE BRACKET
* 0x005D: RIGHT SQUARE BRACKET
* 0x005E: CIRCUMFLEX ACCENT
* 0x0060: GRAVE ACCENT
... and 210 others [code: missing-codepoints]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** fonts/variable/VirtuaGrotesk[wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+0021 EXCLAMATION MARK: try adding one of: cham, latin, masaram-gondi, syriac, gunjala-gondi, khmer, adlam, mongolian, thaana, math
* U+0022 QUOTATION MARK: try adding one of: wancho, masaram-gondi, cham, math, adlam, mongolian, khmer, latin
* U+0023 NUMBER SIGN: try adding one of: khmer, symbols, adlam, latin, math
* U+0024 DOLLAR SIGN: try adding one of: math, adlam, khmer, latin
* U+0025 PERCENT SIGN: try adding one of: gunjala-gondi, adlam, latin, masaram-gondi, math, khmer
* U+0026 AMPERSAND: try adding one of: latin, adlam, khmer, math
* U+0027 APOSTROPHE: try adding one of: adlam, latin, math, cham, warang-citi, masaram-gondi, khmer, gunjala-gondi, wancho
* U+0028 LEFT PARENTHESIS: try adding one of: latin, cham, gunjala-gondi, wancho, thaana, math, khmer, masaram-gondi, mongolian, syriac, adlam
* U+0029 RIGHT PARENTHESIS: try adding one of: thaana, khmer, latin, adlam, cham, gunjala-gondi, syriac, masaram-gondi, mongolian, wancho, math
... and 163 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[9] fonts/ttf/VirtuaGrotesk-SemiBold.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0621 (U+0621): found 0, expected one of: [1, 2]
* uni0625.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni0622.fina (unencoded): found 0, expected one of: [2]
* uni0671 (U+0671): found 0, expected one of: [2, 3, 76]
* uni0671.fina (unencoded): found 0, expected one of: [2, 3]
* uni066E (U+066E): found 0, expected one of: [1, 64]
* uni066E.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni062C (U+062C): found 0, expected one of: [2, 3, 76]
* uni062C.fina (unencoded): found 0, expected one of: [2, 3]
... and 95 others [code: no-contour]
  
  


- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0628 (U+0628): found 1, expected one of: [0, 2, 68]
* uni0628.fina (unencoded): found 1, expected one of: [2, 3, 5]
* uni062E.fina (unencoded): found 1, expected one of: [2, 3, 4]
* uni0632 (U+0632): found 1, expected one of: [2, 32]
* uni0636.fina (unencoded): found 1, expected one of: [3, 4, 5]
* uni0636.medi (unencoded): found 1, expected one of: [3, 4, 6]
* uni0636.init (unencoded): found 1, expected one of: [3, 5]
* uni0638.init (unencoded): found 1, expected one of: [3, 4, 5]
* uni0639 (U+0639): found 17, expected one of: [1, 2]
... and 4 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does GPOS table have kerning information? (gpos_kerning_info)</summary>
    <div>








- ⚠️ **WARN** GPOS table lacks kerning information. [code: lacks-kern-info]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>








- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>








- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni0647.medi.001
* twodotsverticalabovear
* twodotsverticalbelowar
* threedotsdownabovear
* threedotsdownbelowar
* threedotsdowncenterar
* threedotsupbelowar
* waslaar
* miniKehehar
... and 4 others [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. (dotted_circle)</summary>
    <div>








- ⚠️ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>








- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́The dot of soft dotted characters _should_ disappear in other cases, for example:

* í [code: soft-dotted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - uni066E.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0643.fina: X=825,Y=2.5 (should be at baseline 0?)
... and 13 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* M (U+004D): from (736.0, 16.0) to (736.0, 421.0) is colinear with segment from (736.0, 421.0) to (740.0, 577.0)
* M (U+004D): from (236.0, 577.0) to (240.0, 421.0) is colinear with segment from (240.0, 421.0) to (240.0, 16.0)
* x (U+0078): from (269.0, 393.0) to (412.0, 560.0) is colinear with segment from (412.0, 560.0) to (428.0, 576.0)
* x (U+0078): from (438.0, 0.0) to (422.0, 16.0) is colinear with segment from (422.0, 16.0) to (269.0, 197.0)
* z (U+007A): from (27.0, 80.0) to (37.0, 96.0) is colinear with segment from (37.0, 96.0) to (305.0, 453.0)
* z (U+007A): from (509.0, 496.0) to (499.0, 480.0) is colinear with segment from (499.0, 480.0) to (231.0, 123.0) [code: found-colinear-vectors]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* emdash (U+2014): Line(Line { p0: (80.0, 360.0), p1: (1088.0, 362.0) }) (angle: 0.11 degrees, expected: 0.00 degrees)
* emdash (U+2014): Line(Line { p0: (1088.0, 274.0), p1: (80.0, 272.0) }) (angle: -179.89 degrees, expected: -180.00 degrees)
* uniE010 (U+E010): Line(Line { p0: (66.0, 194.0), p1: (64.0, 718.0) }) (angle: 90.22 degrees, expected: 90.00 degrees) [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] fonts/ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check Google Fonts glyph coverage. (googlefonts/glyph_coverage)</summary>
    <div>








- 🔥 **FAIL** fonts/ttf/VirtuaGrotesk-Regular.ttf missing required codepoints:

* 0x002B: PLUS SIGN
* 0x003C: LESS-THAN SIGN
* 0x003D: EQUALS SIGN
* 0x003E: GREATER-THAN SIGN
* 0x0040: COMMERCIAL AT
* 0x005B: LEFT SQUARE BRACKET
* 0x005D: RIGHT SQUARE BRACKET
* 0x005E: CIRCUMFLEX ACCENT
* 0x0060: GRAVE ACCENT
... and 210 others [code: missing-codepoints]
  
  


- 🔥 **FAIL** fonts/ttf/VirtuaGrotesk-Medium.ttf missing required codepoints:

* 0x002B: PLUS SIGN
* 0x003C: LESS-THAN SIGN
* 0x003D: EQUALS SIGN
* 0x003E: GREATER-THAN SIGN
* 0x0040: COMMERCIAL AT
* 0x005B: LEFT SQUARE BRACKET
* 0x005D: RIGHT SQUARE BRACKET
* 0x005E: CIRCUMFLEX ACCENT
* 0x0060: GRAVE ACCENT
... and 210 others [code: missing-codepoints]
  
  


- 🔥 **FAIL** fonts/ttf/VirtuaGrotesk-SemiBold.ttf missing required codepoints:

* 0x002B: PLUS SIGN
* 0x003C: LESS-THAN SIGN
* 0x003D: EQUALS SIGN
* 0x003E: GREATER-THAN SIGN
* 0x0040: COMMERCIAL AT
* 0x005B: LEFT SQUARE BRACKET
* 0x005D: RIGHT SQUARE BRACKET
* 0x005E: CIRCUMFLEX ACCENT
* 0x0060: GRAVE ACCENT
... and 210 others [code: missing-codepoints]
  
  


- 🔥 **FAIL** fonts/ttf/VirtuaGrotesk-Bold.ttf missing required codepoints:

* 0x002B: PLUS SIGN
* 0x003C: LESS-THAN SIGN
* 0x003D: EQUALS SIGN
* 0x003E: GREATER-THAN SIGN
* 0x0040: COMMERCIAL AT
* 0x005B: LEFT SQUARE BRACKET
* 0x005D: RIGHT SQUARE BRACKET
* 0x005E: CIRCUMFLEX ACCENT
* 0x0060: GRAVE ACCENT
... and 210 others [code: missing-codepoints]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Regular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+0021 EXCLAMATION MARK: try adding one of: cham, latin, masaram-gondi, syriac, gunjala-gondi, khmer, adlam, mongolian, thaana, math
* U+0022 QUOTATION MARK: try adding one of: wancho, masaram-gondi, cham, math, adlam, mongolian, khmer, latin
* U+0023 NUMBER SIGN: try adding one of: khmer, symbols, adlam, latin, math
* U+0024 DOLLAR SIGN: try adding one of: math, adlam, khmer, latin
* U+0025 PERCENT SIGN: try adding one of: gunjala-gondi, adlam, latin, masaram-gondi, math, khmer
* U+0026 AMPERSAND: try adding one of: latin, adlam, khmer, math
* U+0027 APOSTROPHE: try adding one of: adlam, latin, math, cham, warang-citi, masaram-gondi, khmer, gunjala-gondi, wancho
* U+0028 LEFT PARENTHESIS: try adding one of: latin, cham, gunjala-gondi, wancho, thaana, math, khmer, masaram-gondi, mongolian, syriac, adlam
* U+0029 RIGHT PARENTHESIS: try adding one of: thaana, khmer, latin, adlam, cham, gunjala-gondi, syriac, masaram-gondi, mongolian, wancho, math
... and 163 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Medium.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+0021 EXCLAMATION MARK: try adding one of: cham, latin, masaram-gondi, syriac, gunjala-gondi, khmer, adlam, mongolian, thaana, math
* U+0022 QUOTATION MARK: try adding one of: wancho, masaram-gondi, cham, math, adlam, mongolian, khmer, latin
* U+0023 NUMBER SIGN: try adding one of: khmer, symbols, adlam, latin, math
* U+0024 DOLLAR SIGN: try adding one of: math, adlam, khmer, latin
* U+0025 PERCENT SIGN: try adding one of: gunjala-gondi, adlam, latin, masaram-gondi, math, khmer
* U+0026 AMPERSAND: try adding one of: latin, adlam, khmer, math
* U+0027 APOSTROPHE: try adding one of: adlam, latin, math, cham, warang-citi, masaram-gondi, khmer, gunjala-gondi, wancho
* U+0028 LEFT PARENTHESIS: try adding one of: latin, cham, gunjala-gondi, wancho, thaana, math, khmer, masaram-gondi, mongolian, syriac, adlam
* U+0029 RIGHT PARENTHESIS: try adding one of: thaana, khmer, latin, adlam, cham, gunjala-gondi, syriac, masaram-gondi, mongolian, wancho, math
... and 163 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-SemiBold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+0021 EXCLAMATION MARK: try adding one of: cham, latin, masaram-gondi, syriac, gunjala-gondi, khmer, adlam, mongolian, thaana, math
* U+0022 QUOTATION MARK: try adding one of: wancho, masaram-gondi, cham, math, adlam, mongolian, khmer, latin
* U+0023 NUMBER SIGN: try adding one of: khmer, symbols, adlam, latin, math
* U+0024 DOLLAR SIGN: try adding one of: math, adlam, khmer, latin
* U+0025 PERCENT SIGN: try adding one of: gunjala-gondi, adlam, latin, masaram-gondi, math, khmer
* U+0026 AMPERSAND: try adding one of: latin, adlam, khmer, math
* U+0027 APOSTROPHE: try adding one of: adlam, latin, math, cham, warang-citi, masaram-gondi, khmer, gunjala-gondi, wancho
* U+0028 LEFT PARENTHESIS: try adding one of: latin, cham, gunjala-gondi, wancho, thaana, math, khmer, masaram-gondi, mongolian, syriac, adlam
* U+0029 RIGHT PARENTHESIS: try adding one of: thaana, khmer, latin, adlam, cham, gunjala-gondi, syriac, masaram-gondi, mongolian, wancho, math
... and 163 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext [code: unreachable-subsetting]
  
  


- ⚠️ **WARN** fonts/ttf/VirtuaGrotesk-Bold.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+0021 EXCLAMATION MARK: try adding one of: cham, latin, masaram-gondi, syriac, gunjala-gondi, khmer, adlam, mongolian, thaana, math
* U+0022 QUOTATION MARK: try adding one of: wancho, masaram-gondi, cham, math, adlam, mongolian, khmer, latin
* U+0023 NUMBER SIGN: try adding one of: khmer, symbols, adlam, latin, math
* U+0024 DOLLAR SIGN: try adding one of: math, adlam, khmer, latin
* U+0025 PERCENT SIGN: try adding one of: gunjala-gondi, adlam, latin, masaram-gondi, math, khmer
* U+0026 AMPERSAND: try adding one of: latin, adlam, khmer, math
* U+0027 APOSTROPHE: try adding one of: adlam, latin, math, cham, warang-citi, masaram-gondi, khmer, gunjala-gondi, wancho
* U+0028 LEFT PARENTHESIS: try adding one of: latin, cham, gunjala-gondi, wancho, thaana, math, khmer, masaram-gondi, mongolian, syriac, adlam
* U+0029 RIGHT PARENTHESIS: try adding one of: thaana, khmer, latin, adlam, cham, gunjala-gondi, syriac, masaram-gondi, mongolian, wancho, math
... and 163 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[9] fonts/ttf/VirtuaGrotesk-Regular.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0621 (U+0621): found 0, expected one of: [1, 2]
* uni0625.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni0622.fina (unencoded): found 0, expected one of: [2]
* uni0671 (U+0671): found 0, expected one of: [2, 3, 76]
* uni0671.fina (unencoded): found 0, expected one of: [2, 3]
* uni066E (U+066E): found 0, expected one of: [1, 64]
* uni066E.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni062C (U+062C): found 0, expected one of: [2, 3, 76]
* uni062C.fina (unencoded): found 0, expected one of: [2, 3]
... and 95 others [code: no-contour]
  
  


- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0628 (U+0628): found 1, expected one of: [0, 2, 68]
* uni0628.fina (unencoded): found 1, expected one of: [2, 3, 5]
* uni062E.fina (unencoded): found 1, expected one of: [2, 3, 4]
* uni0632 (U+0632): found 1, expected one of: [2, 32]
* uni0636.fina (unencoded): found 1, expected one of: [3, 4, 5]
* uni0636.medi (unencoded): found 1, expected one of: [3, 4, 6]
* uni0636.init (unencoded): found 1, expected one of: [3, 5]
* uni0638.init (unencoded): found 1, expected one of: [3, 4, 5]
* uni0639 (U+0639): found 17, expected one of: [1, 2]
... and 4 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does GPOS table have kerning information? (gpos_kerning_info)</summary>
    <div>








- ⚠️ **WARN** GPOS table lacks kerning information. [code: lacks-kern-info]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>








- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>








- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni0647.medi.001
* twodotsverticalabovear
* twodotsverticalbelowar
* threedotsdownabovear
* threedotsdownbelowar
* threedotsdowncenterar
* threedotsupbelowar
* waslaar
* miniKehehar
... and 4 others [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. (dotted_circle)</summary>
    <div>








- ⚠️ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>








- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́The dot of soft dotted characters _should_ disappear in other cases, for example:

* í [code: soft-dotted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - uni066E.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0643.fina: X=825,Y=2.5 (should be at baseline 0?)
... and 13 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* M (U+004D): from (736.0, 16.0) to (736.0, 442.0) is colinear with segment from (736.0, 442.0) to (740.0, 610.0)
* M (U+004D): from (172.0, 610.0) to (176.0, 442.0) is colinear with segment from (176.0, 442.0) to (176.0, 16.0) [code: found-colinear-vectors]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* emdash (U+2014): Line(Line { p0: (80.0, 360.0), p1: (1088.0, 362.0) }) (angle: 0.11 degrees, expected: 0.00 degrees)
* emdash (U+2014): Line(Line { p0: (1088.0, 274.0), p1: (80.0, 272.0) }) (angle: -179.89 degrees, expected: -180.00 degrees)
* uniE010 (U+E010): Line(Line { p0: (66.0, 194.0), p1: (64.0, 718.0) }) (angle: 90.22 degrees, expected: 90.00 degrees) [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[9] fonts/ttf/VirtuaGrotesk-Bold.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0621 (U+0621): found 0, expected one of: [1, 2]
* uni0625.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni0622.fina (unencoded): found 0, expected one of: [2]
* uni0671 (U+0671): found 0, expected one of: [2, 3, 76]
* uni0671.fina (unencoded): found 0, expected one of: [2, 3]
* uni066E (U+066E): found 0, expected one of: [1, 64]
* uni066E.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni062C (U+062C): found 0, expected one of: [2, 3, 76]
* uni062C.fina (unencoded): found 0, expected one of: [2, 3]
... and 95 others [code: no-contour]
  
  


- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0628 (U+0628): found 1, expected one of: [0, 2, 68]
* uni0628.fina (unencoded): found 1, expected one of: [2, 3, 5]
* uni062E.fina (unencoded): found 1, expected one of: [2, 3, 4]
* uni0632 (U+0632): found 1, expected one of: [2, 32]
* uni0636.fina (unencoded): found 1, expected one of: [3, 4, 5]
* uni0636.medi (unencoded): found 1, expected one of: [3, 4, 6]
* uni0636.init (unencoded): found 1, expected one of: [3, 5]
* uni0638.init (unencoded): found 1, expected one of: [3, 4, 5]
* uni0639 (U+0639): found 17, expected one of: [1, 2]
... and 4 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does GPOS table have kerning information? (gpos_kerning_info)</summary>
    <div>








- ⚠️ **WARN** GPOS table lacks kerning information. [code: lacks-kern-info]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>








- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>








- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni0647.medi.001
* twodotsverticalabovear
* twodotsverticalbelowar
* threedotsdownabovear
* threedotsdownbelowar
* threedotsdowncenterar
* threedotsupbelowar
* waslaar
* miniKehehar
... and 4 others [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. (dotted_circle)</summary>
    <div>








- ⚠️ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>








- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́The dot of soft dotted characters _should_ disappear in other cases, for example:

* í [code: soft-dotted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - uni066E.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0643.fina: X=825,Y=2.5 (should be at baseline 0?)
... and 13 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* M (U+004D): from (736.0, 16.0) to (736.0, 410.0) is colinear with segment from (736.0, 410.0) to (740.0, 560.0)
* M (U+004D): from (268.0, 560.0) to (272.0, 410.0) is colinear with segment from (272.0, 410.0) to (272.0, 16.0)
* x (U+0078): from (272.0, 406.0) to (420.0, 560.0) is colinear with segment from (420.0, 560.0) to (436.0, 576.0)
* x (U+0078): from (446.0, 0.0) to (430.0, 16.0) is colinear with segment from (430.0, 16.0) to (272.0, 184.0)
* z (U+007A): from (24.0, 88.0) to (36.0, 104.0) is colinear with segment from (36.0, 104.0) to (296.0, 440.0)
* z (U+007A): from (536.0, 488.0) to (524.0, 472.0) is colinear with segment from (524.0, 472.0) to (264.0, 136.0) [code: found-colinear-vectors]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* emdash (U+2014): Line(Line { p0: (80.0, 360.0), p1: (1088.0, 362.0) }) (angle: 0.11 degrees, expected: 0.00 degrees)
* emdash (U+2014): Line(Line { p0: (1088.0, 274.0), p1: (80.0, 272.0) }) (angle: -179.89 degrees, expected: -180.00 degrees)
* uniE010 (U+E010): Line(Line { p0: (66.0, 194.0), p1: (64.0, 718.0) }) (angle: 90.22 degrees, expected: 90.00 degrees) [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>


<details><summary>[8] fonts/variable/VirtuaGrotesk[wght].ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0621 (U+0621): found 0, expected one of: [1, 2]
* uni0625.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni0622.fina (unencoded): found 0, expected one of: [2]
* uni0671 (U+0671): found 0, expected one of: [2, 3, 76]
* uni0671.fina (unencoded): found 0, expected one of: [2, 3]
* uni066E (U+066E): found 0, expected one of: [1, 64]
* uni066E.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni062C (U+062C): found 0, expected one of: [2, 3, 76]
* uni062C.fina (unencoded): found 0, expected one of: [2, 3]
... and 95 others [code: no-contour]
  
  


- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0628 (U+0628): found 1, expected one of: [0, 2, 68]
* uni0628.fina (unencoded): found 1, expected one of: [2, 3, 5]
* uni062E.fina (unencoded): found 1, expected one of: [2, 3, 4]
* uni0632 (U+0632): found 1, expected one of: [2, 32]
* uni0636.fina (unencoded): found 1, expected one of: [3, 4, 5]
* uni0636.medi (unencoded): found 1, expected one of: [3, 4, 6]
* uni0636.init (unencoded): found 1, expected one of: [3, 5]
* uni0638.init (unencoded): found 1, expected one of: [3, 4, 5]
* uni0639 (U+0639): found 17, expected one of: [1, 2]
... and 4 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure variable fonts include an avar table. (mandatory_avar_table)</summary>
    <div>








- ⚠️ **WARN** The font does not include an avar table.  If the progression rates of axes is linear and no user-mapping is expected, this is fine, and this check can be ignored or excluded. [code: missing-avar]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>








- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>








- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni0647.medi.001
* twodotsverticalabovear
* twodotsverticalbelowar
* threedotsdownabovear
* threedotsdownbelowar
* threedotsdowncenterar
* threedotsupbelowar
* waslaar
* miniKehehar
... and 4 others [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. (dotted_circle)</summary>
    <div>








- ⚠️ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>








- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́The dot of soft dotted characters _should_ disappear in other cases, for example:

* í [code: soft-dotted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - uni066E.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0643.fina: X=825,Y=2.5 (should be at baseline 0?)
... and 13 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph (outline_direction)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have a counter-clockwise outer contour:

* uni066E.medi has a counter-clockwise outer contour
* uni0628.medi has a counter-clockwise outer contour
* uni062A.medi has a counter-clockwise outer contour
* uni062B.medi has a counter-clockwise outer contour
* uni062C.init has a counter-clockwise outer contour
* uni062D.init has a counter-clockwise outer contour
* uni062E.init has a counter-clockwise outer contour
* uni062F (U+062F) has a counter-clockwise outer contour
* uni062F.fina has a counter-clockwise outer contour
... and 45 others [code: ccw-outer-contour]
  
  

</div>
</details>


</div>
</details>


<details><summary>[9] fonts/ttf/VirtuaGrotesk-Medium.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>








- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0621 (U+0621): found 0, expected one of: [1, 2]
* uni0625.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni0622.fina (unencoded): found 0, expected one of: [2]
* uni0671 (U+0671): found 0, expected one of: [2, 3, 76]
* uni0671.fina (unencoded): found 0, expected one of: [2, 3]
* uni066E (U+066E): found 0, expected one of: [1, 64]
* uni066E.fina (unencoded): found 0, expected one of: [1, 2, 3]
* uni062C (U+062C): found 0, expected one of: [2, 3, 76]
* uni062C.fina (unencoded): found 0, expected one of: [2, 3]
... and 95 others [code: no-contour]
  
  


- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni0628 (U+0628): found 1, expected one of: [0, 2, 68]
* uni0628.fina (unencoded): found 1, expected one of: [2, 3, 5]
* uni062E.fina (unencoded): found 1, expected one of: [2, 3, 4]
* uni0632 (U+0632): found 1, expected one of: [2, 32]
* uni0636.fina (unencoded): found 1, expected one of: [3, 4, 5]
* uni0636.medi (unencoded): found 1, expected one of: [3, 4, 6]
* uni0636.init (unencoded): found 1, expected one of: [3, 5]
* uni0638.init (unencoded): found 1, expected one of: [3, 4, 5]
* uni0639 (U+0639): found 17, expected one of: [1, 2]
... and 4 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does GPOS table have kerning information? (gpos_kerning_info)</summary>
    <div>








- ⚠️ **WARN** GPOS table lacks kerning information. [code: lacks-kern-info]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>








- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>








- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni0647.medi.001
* twodotsverticalabovear
* twodotsverticalbelowar
* threedotsdownabovear
* threedotsdownbelowar
* threedotsdowncenterar
* threedotsupbelowar
* waslaar
* miniKehehar
... and 4 others [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure dotted circle glyph is present and can attach marks. (dotted_circle)</summary>
    <div>








- ⚠️ **WARN** No dotted circle glyph present [code: missing-dotted-circle]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>








- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́The dot of soft dotted characters _should_ disappear in other cases, for example:

* í [code: soft-dotted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - uni066E.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni0628.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062A.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=299.5,Y=2.5 (should be at baseline 0?)
* - uni062B.medi: X=124.5,Y=2.5 (should be at baseline 0?)
* - uni0643.fina: X=825,Y=2.5 (should be at baseline 0?)
... and 13 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have colinear vectors:

* M (U+004D): from (736.0, 16.0) to (736.0, 431.0) is colinear with segment from (736.0, 431.0) to (740.0, 593.0)
* M (U+004D): from (204.0, 593.0) to (208.0, 431.0) is colinear with segment from (208.0, 431.0) to (208.0, 16.0)
* z (U+007A): from (29.0, 72.0) to (39.0, 88.0) is colinear with segment from (39.0, 88.0) to (315.0, 467.0)
* z (U+007A): from (483.0, 504.0) to (473.0, 488.0) is colinear with segment from (473.0, 488.0) to (197.0, 109.0) [code: found-colinear-vectors]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any semi-vertical or semi-horizontal lines? (outline_semi_vertical)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have semi-vertical/semi-horizontal lines:

* seven (U+0037): Line(Line { p0: (402.0, 643.0), p1: (45.0, 642.0) }) (angle: -179.84 degrees, expected: -180.00 degrees)
* emdash (U+2014): Line(Line { p0: (80.0, 360.0), p1: (1088.0, 362.0) }) (angle: 0.11 degrees, expected: 0.00 degrees)
* emdash (U+2014): Line(Line { p0: (1088.0, 274.0), p1: (80.0, 272.0) }) (angle: -179.89 degrees, expected: -180.00 degrees)
* uniE010 (U+E010): Line(Line { p0: (66.0, 194.0), p1: (64.0, 718.0) }) (angle: 90.22 degrees, expected: 90.00 degrees)
* seven.tf: Line(Line { p0: (402.0, 643.0), p1: (45.0, 642.0) }) (angle: -179.84 degrees, expected: -180.00 degrees) [code: found-semi-vertical]
  
  

</div>
</details>


</div>
</details>






### Summary

| 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|---|
| 10 | 49 | 38 | 479 | 311 | 
| 1% | 6% | 4% | 55% | 36% | 



