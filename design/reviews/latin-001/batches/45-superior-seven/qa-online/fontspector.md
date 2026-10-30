## FontSpector report

fontspector version: 1.9.0






## Check results




<details><summary>[3] out/qa/2026-10-22-superior-seven/ofl/virtuagrotesk</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Tofu should not be shown in sample texts. (googlefonts/tofu)</summary>
    <div>








- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Aleut, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̂ (U+0302) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Amarakaeri, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the poster md sample text for language Chickasaw, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Guarani, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ẽ (U+1EBD) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Yanomamö, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ẽ (U+1EBD) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the poster md sample text for language Central Mazahua, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the poster sm sample text for language Central Mazahua, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̸ (U+0338) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Otomi, Mezquital, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Secoya, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the poster lg sample text for language Siona, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the masthead partial sample text for language Ticuna, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ẽ (U+1EBD)
* Ẽ (U+1EBC) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Ticuna, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> METADATA.pb subsets are correct? (googlefonts/metadata/subsets_correct)</summary>
    <div>








- ⚠️ **WARN** Please remove 'latin-ext' from METADATA.pb since less than 20% of its glyphs are supported by this font file. [code: unsupported-subset]
  
  


- ⚠️ **WARN** Please remove 'arabic' from METADATA.pb since less than 50% of its glyphs are supported by this font file. [code: unsupported-subset]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** out/qa/2026-10-22-superior-seven/ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: canadian-aboriginal, yi
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, cherokee, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+030A COMBINING RING ABOVE: try adding one of: syriac, duployan
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0312 COMBINING TURNED COMMA ABOVE: try adding math
... and 15 others

Or you can add the above codepoints to one of the subsets supported by the font: arabic, hebrew, latin, latin-ext, menu [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[6] out/qa/2026-10-22-superior-seven/ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf</summary>
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
* perMillear (U+0609): found 6, expected one of: [0, 4] [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Detect any interpolation issues in the font. (interpolation_issues)</summary>
    <div>








- ⚠️ **WARN** Interpolation issue in uni0645.medi: Kink in contour 0 at node 20 [code: interpolation-issue]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? (soft_hyphen)</summary>
    <div>








- ⚠️ **WARN** This font has a 'Soft Hyphen' character. [code: softhyphen]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>








- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages           |
|-------------------------------------------------------------------|---------------------|
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish) |
|   The following auxiliary characters are missing from the font: Ǥ |                     |
|   The following auxiliary characters are missing from the font: Ʒ |                     |
|   The following auxiliary characters are missing from the font: Ǯ |                     |
|   The following auxiliary characters are missing from the font: ǥ |                     |
|   The following auxiliary characters are missing from the font: ʒ |                     |
|   The following auxiliary characters are missing from the font: ǯ |                     | [code: warning-language-shaping]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? (outline_alignment_miss)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have on-curve points which have potentially incorrect y coordinates:

* - S (U+0053): X=481.5,Y=-2.5 (should be at baseline 0?)
* - b (U+0062): X=254,Y=2.5 (should be at baseline 0?)
* - d (U+0064): X=386,Y=2.5 (should be at baseline 0?)
* - uni066E.fina: X=963.5,Y=2.5 (should be at baseline 0?)
* - uni066E.fina: X=788.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=289.5,Y=2.5 (should be at baseline 0?)
* - uni066E.medi: X=122.5,Y=2.5 (should be at baseline 0?)
* - uni0628.fina: X=963.5,Y=2.5 (should be at baseline 0?)
* - uni0628.fina: X=788.5,Y=2.5 (should be at baseline 0?)
... and 88 others [code: found-misalignments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>








- ⚠️ **WARN** The following glyphs have overlapping path segments:

* uni0633.medi: Quad(QuadBez { p0: (576.0, -16.0), p1: (576.0, -16.0), p2: (576.0, -16.0) }) has the same coordinates as a previous segment.
* uni0634.medi: Quad(QuadBez { p0: (576.0, -16.0), p1: (576.0, -16.0), p2: (576.0, -16.0) }) has the same coordinates as a previous segment.
* iogonek (U+012F): Line(Line { p0: (88.0, 0.0), p1: (152.0, 0.0) }) has the same coordinates as a previous segment.
* seenSixdotsar.medi: Quad(QuadBez { p0: (576.0, -16.0), p1: (576.0, -16.0), p2: (576.0, -16.0) }) has the same coordinates as a previous segment. [code: overlapping-path-segments]
  
  

</div>
</details>


</div>
</details>


<details><summary>[1] out/qa/2026-10-22-superior-seven/ofl/virtuagrotesk/METADATA.pb</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> METADATA.pb: Designers are listed correctly on the Google Fonts catalog? (googlefonts/metadata/designer_profiles)</summary>
    <div>








- ⚠️ **WARN** It seems that eliheuer is still not listed on the designers catalog. Please submit a photo and a link to a webpage where people can learn more about the work of this designer/typefoundry. [code: profile-not-found]
  
  

</div>
</details>


</div>
</details>






### Summary

| 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|---|
| 12 | 10 | 10 | 159 | 40 | 
| 5% | 4% | 4% | 69% | 17% | 



