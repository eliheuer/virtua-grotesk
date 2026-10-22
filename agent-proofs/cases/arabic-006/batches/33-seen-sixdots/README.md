# Six-dot Seen: complete dot groups

Applied eight wrappers: seenSixdots-ar, .init, .medi and .fina in both masters.
Before: only an oversized downward upper triangle; the lower group was absent.
After: upward upper and downward lower triangles, each with three round dots.
The Seen component and all shared donors stay byte-identical. Local circles reuse
one contour from the corrected Tcheh donor (80-unit Regular,112-unit Bold diameter),
translated into six positions. The original base skeleton and curves are retained.
Regular initial/medial advances now match the Seen base,808/864. New composition
is purple, awaiting human review. Explicit top/bottom anchors clear the complete
new dot groups; other inherited base anchors remain as before.

Whole-image inspection: forms at400/550/700; enlarged isolated endpoints; joined
Meem contexts at700. Both triangles are readable, with separated dots and clear
space from the teeth/bowl. The lower group follows Noto's placement below the
teeth; Plex puts isolated/final dots below the bowl, a legitimate reference
variation retained for human review. The new dots are substantially smaller than
the earlier oversized groups. Regular Seen still has pronounced underside cusps,
and the broad Bold bowl/teeth proportions remain inherited review issues.
Rubik and Readex lack U069C and are explicitly unavailable in all comparisons.
A separate FreeType compiled render confirms the Bold isolated silhouette.

Verification: 50 shaping comparisons at five weights, only four compiled glyphs
change, matching six12point contours plus one unchanged base component in both
masters. No sampled dot reversals/kinks/intersections; G2 joins at dot extrema.
124 grid findings all belong to inherited Seen geometry/advances/topDots or
bottomDots anchors; every new local dot point and new top/bottom anchor is on8.
Scratch preflight passed. Full source hash guards preserved all34 Beh/Heh reserved
files, manual hamza, green drawings and every non-target source byte.

This is a first-pass composition repair, not human approval of Seen or Arabic.
