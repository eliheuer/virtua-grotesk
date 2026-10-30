## FontSpector report

fontspector version: 1.9.0



## Checks with FATAL results

These must be addressed first.


<details><summary>[1] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/METADATA.pb</summary>
<div>


<details>
    <summary>💥 <b>ERROR</b> METADATA.pb: Designers are listed correctly on the Google Fonts catalog? (googlefonts/metadata/designer_profiles)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch designer info: error sending request for url (https://raw.githubusercontent.com/google/fonts/master/catalog/designers//eliheuer/info.pb) 
  
  

</div>
</details>


</div>
</details>


<details><summary>[2] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk</summary>
<div>


<details>
    <summary>💥 <b>ERROR</b> METADATA.pb subsets are correct? (googlefonts/metadata/subsets_correct)</summary>
    <div>








- 💥 **ERROR** Error: Something went wrong: Failed to fetch production metadata: Network("Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts)") 
  
  

</div>
</details>





<details>
    <summary>💥 <b>ERROR</b> Check if the axes match between the font and the Google Fonts version. (googlefonts/axes_match)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts) 
  
  

</div>
</details>


</div>
</details>


<details><summary>[5] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf</summary>
<div>


<details>
    <summary>💥 <b>ERROR</b> Familyname must be unique according to namecheck.fontdata.com (fontdata_namecheck)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to access: http://namecheck.fontdata.com/. error sending request for url (http://namecheck.fontdata.com/api/?q=Virtua+Grotesk) 
  
  

</div>
</details>





<details>
    <summary>💥 <b>ERROR</b> Check font follows the Google Fonts CJK vertical metric schema (googlefonts/cjk_vertical_metrics)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts) 
  
  

</div>
</details>





<details>
    <summary>💥 <b>ERROR</b> Version number has increased since previous release on Google Fonts? (googlefonts/version_bump)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts) 
  
  

</div>
</details>





<details>
    <summary>💥 <b>ERROR</b> Check font follows the Google Fonts vertical metric schema (googlefonts/vertical_metrics)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts) 
  
  

</div>
</details>





<details>
    <summary>💥 <b>ERROR</b> Check if the vertical metrics of a family are similar to the same
family hosted on Google Fonts. (googlefonts/vertical_metrics_regressions)</summary>
    <div>








- 💥 **ERROR** Error: A network error occurred: Failed to fetch metadata: error sending request for url (https://fonts.google.com/metadata/fonts) 
  
  

</div>
</details>


</div>
</details>







## All other checks




<details><summary>[2] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk</summary>
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
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Otomi, Mezquital, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Secoya, but although the font contained all the base exemplars for the language, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the poster lg sample text for language Siona, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the masthead partial sample text for language Ticuna, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* Ẽ (U+1EBC)
* ẽ (U+1EBD) [code: missing-subsetted]
  
  


- 🔥 **FAIL** The font has the following codepoints needed to render the specimen 16 sample text for language Ticuna, but although the font contained all the codepoints for the sample text, tofu will still be produced because the codepoints do not appear in any of the subsets arabic, hebrew, latin-ext, latin:

* ̱ (U+0331) [code: missing-subsetted]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>








- ⚠️ **WARN** out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: canadian-aboriginal, yi
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, cherokee, coptic, tifinagh
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
* U+0326 COMBINING COMMA BELOW: try adding math
... and 4 others

Or you can add the above codepoints to one of the subsets supported by the font: arabic, hebrew, latin, latin-ext, menu [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[1] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/article/ARTICLE.en_us.html</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Does DESCRIPTION file contain broken links? (googlefonts/description/broken_links)</summary>
    <div>








- 🔥 **FAIL** The following links are broken:

* https://github.com/eliheuer/virtua-grotesk (error: error sending request for url (https://github.com/eliheuer/virtua-grotesk)) [code: broken-links]
  
  

</div>
</details>


</div>
</details>


<details><summary>[1] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/METADATA.pb</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Does METADATA.pb copyright field contain broken links? (googlefonts/metadata/broken_links)</summary>
    <div>








- 🔥 **FAIL** The following links are broken:

* https://github.com/eliheuer/virtua-grotesk (error: error sending request for url (https://github.com/eliheuer/virtua-grotesk)) [code: broken-links]
  
  

</div>
</details>


</div>
</details>


<details><summary>[5] out/qa/2026-10-21-latin-breve-package/ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf</summary>
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






### Summary

| 💥 ERROR | 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|---|---|
| 8 | 12 | 6 | 10 | 156 | 36 | 
| 4% | 5% | 3% | 4% | 68% | 16% | 



