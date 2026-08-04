#!/usr/bin/env python3
"""Lane manifest for the Arabic completion pass.

Classifies every red (and unmarked) Arabic glyph into a production lane:

  lane 1  recompose   — pure component recipe from green/derived parts
  lane 2  derive      — scripted geometry derivation (tail weld, entry-stub
                        add/remove, dot-strip, mirror/copy)
  lane 3  skeleton    — genuinely new drawing (Rubik topology, green style)
  lane 4  symbol      — digits/punctuation/parametric (symbol_gen lane)

The recipe strings are the plan, not executable code — the lane runners
consume this manifest. Coverage is self-checked: any red glyph without a
rule is reported loudly.

Usage:
    ./.venv/bin/python scripts/arabic_lanes.py [--json build/arabic-lanes.json]
"""

import argparse
import json
import pathlib
import plistlib
import re
import sys
from collections import OrderedDict

REPO = pathlib.Path(__file__).resolve().parent.parent
UFO = REPO / "sources" / "VirtuaGrotesk-Regular.ufo"

# Ordered (pattern, lane, recipe) rules. First match wins. Patterns are
# full-match regexes over glyph names.
RULES = [
    # ---- dot-cluster parts: arrangements of the green dots (lane 2 script)
    (r"twodots(vertical|horizontal)(above|below)-ar", 2,
     "arrange green dotabove/dotbelow (160-dot, 96 gap) per orientation"),
    (r"threedotsdown(above|below|center)-ar", 2,
     "mirror/shift green threedotsupabove-ar into the target band"),
    (r"threedotsupbelow-ar", 2,
     "green threedotsupabove-ar translated to below band"),
    (r"dotcenter-ar", 2, "green dotabove-ar recentered at math axis"),

    # ---- beh/tooth family ------------------------------------------------
    (r"behDotless-ar", 2, "TAIL#1 beh-boat: behDotless-ar.init + boat tail"),
    (r"behDotless-ar\.fina", 2, "TAIL#1: behDotless-ar.medi + boat tail"),
    (r"(beh|teh|theh|peh|veh|tteh)-ar(\.fina)?", 1,
     "skeleton (behDotless/fehDotless isol|fina) + dots/mark component"),
    (r"beeh-ar(\.(init|medi|fina))?", 1,
     "behDotless form + twodotsverticalbelow-ar"),
    (r"tteheh-ar(\.(init|medi|fina))?", 1,
     "behDotless form + twodotsverticalabove-ar"),
    (r"tehThreedotsdown-ar(\.(init|medi|fina))?", 1,
     "behDotless form + threedotsdownabove-ar"),
    (r"tehRing-ar(\.(init|medi|fina))?", 1,
     "behDotless form + ring part (SMALL#ring, lane 3 small)"),
    (r"noon-ar", 1, "noonghunna-ar + dotabove-ar"),
    (r"noon-ar\.fina", 1, "noonghunna-ar.fina + dotabove-ar (exists, unmark)"),
    (r"noonghunna-ar(\.fina)?", 3,
     "TAIL#2 noon-bowl: deep round cup, Rubik topology, stroke 96/112"),
    (r"noonGhunna-ar", 2, "copy of noonghunna-ar (isol, U+06BA)"),

    # ---- seen/sad/tah ----------------------------------------------------
    (r"seen-ar\.medi", 2, "seen-ar.init + right entry stub (init->medi rule)"),
    (r"seen-ar(\.fina)?", 2, "TAIL#3 seen-tail: seen-ar.init/.medi + bowl"),
    (r"sheen-ar(\.(init|medi|fina))?", 1, "seen form + threedotsupabove-ar"),
    (r"seenSixdots-ar(\.(init|medi|fina))?", 1,
     "seen form + 2x threedotsdown clusters"),
    (r"sad-ar\.(init|medi)", 3,
     "SKEL sad: seen teeth grammar + big flat loop, Rubik proportions"),
    (r"sad-ar(\.fina)?", 2, "TAIL#3: sad-ar.init/.medi + seen tail"),
    (r"dad-ar(\.(init|medi|fina))?", 1, "sad form + dotabove-ar"),
    (r"tah-ar\.(init|medi)?", 3,
     "SKEL tah: sad loop + alef stem (one skeleton, all four positions)"),
    (r"tah-ar(\.fina)?", 3, "SKEL tah (isol/fina share the init/medi body)"),
    (r"zah-ar(\.(init|medi|fina))?", 1, "tah form + dotabove-ar"),

    # ---- hah family ------------------------------------------------------
    (r"hah-ar\.medi", 3, "SKEL hah.medi: hah.init + angled entry (Rubik)"),
    (r"hah-ar(\.fina)?", 3,
     "TAIL#4 hah-bowl: deep descender bowl under hah.init head"),
    (r"(jeem|khah)-ar(\.(medi|fina))?", 1, "hah form + dot component"),
    (r"tcheh-ar(\.(medi|fina))?", 1, "hah form + threedotsdowncenter-ar"),

    # ---- ain family ------------------------------------------------------
    (r"ain-ar(\.fina)?", 3,
     "TAIL#5 ain-bowl: deep open bowl; isol re-draw (existing red is off)"),
    (r"ghain-ar(\.fina)?", 1, "ain form + dotabove-ar"),

    # ---- feh/qaf ---------------------------------------------------------
    (r"fehDotless-ar(\.fina)?", 2,
     "TAIL#1: feh bowl (green fehDotless.init/medi) + boat tail"),
    (r"feh-ar(\.fina)?", 1, "fehDotless form + dotabove-ar"),
    (r"qafDotless-ar(\.fina)?", 3,
     "TAIL#6 qaf-round-tail: feh bowl + deep round tail (waw/reh DNA)"),
    (r"qaf-ar(\.fina)?", 1, "qafDotless form + twodotshorizontalabove-ar"),
    (r"qafDotabove-ar(\.(init|medi|fina))?", 1,
     "fehDotless/qafDotless form + dotabove-ar"),
    (r"qafThreedotsabove-ar(\.(init|medi|fina))?", 1,
     "fehDotless/qafDotless form + threedotsupabove-ar"),
    (r"fehDotmovedbelow-ar(\.(init|medi|fina))?", 1,
     "fehDotless form + dotbelow-ar"),
    (r"fehThreedotsbelow-ar(\.(init|medi|fina))?", 1,
     "fehDotless form + threedotsdownbelow-ar"),

    # ---- waw / reh / dal -------------------------------------------------
    (r"waw-ar\.fina", 2, "green waw-ar + entry stub"),
    (r"wawHamzaabove-ar(\.fina)?", 1, "waw form + hamzaabove-ar"),
    (r"reh-ar", 2, "green reh-ar.fina minus entry stub (isol head)"),
    (r"(zain|thal)-ar(\.fina)?", 1, "reh/dal form + dotabove-ar"),
    (r"jeh-ar", 1, "reh-ar + threedotsupabove-ar"),
    (r"rreh-ar", 1, "reh-ar + smallHighTah-ar (rreh-ar.fina is green)"),

    # ---- kaf / gaf -------------------------------------------------------
    (r"kaf-ar(\.(init|medi))?", 3,
     "SKEL kaf: isol swash body + init/medi vertical form with sarkash"),
    (r"keheh-ar(\.(init|medi))?", 2,
     "kaf skeleton without hamza-mark (regen red drawings from SKEL kaf)"),
    (r"kehehThreedotsabove-ar(\.(init|medi))?", 1,
     "keheh form + threedotsupabove-ar"),
    (r"gaf-ar(\.(init|medi))?", 1,
     "keheh form + gafsarkash part (gaf-ar.fina is green)"),
    (r"gafsarkash(above|center)-ar", 3,
     "SMALL sarkash bar part (from green gaf-ar.fina upper bar)"),
    (r"miniKeheh-ar", 3, "SMALL mark: scaled keheh sign"),

    # ---- lam / lam_alef --------------------------------------------------
    (r"lam-ar", 2, "green lam-ar.init stem + lam-ar.fina bowl (weld)"),
    (r"lam_alef-ar", 2, "green lam_alef-ar.fina minus entry stub"),
    (r"lam_alef(Hamzaabove|Hamzabelow|Madda|Wasla)-ar(\.fina)?", 1,
     "lam_alef form + mark component"),

    # ---- meem / heh / yeh ------------------------------------------------
    (r"meem-ar(\.(init|medi|fina))?", 3,
     "SKEL meem: round knot + straight descender tail, all four positions"),
    (r"heh-ar(\.(init|fina))?", 3,
     "SKEL heh: isol two-story, init open form, fina teardrop (medi green)"),
    (r"tehMarbuta-ar(\.fina)?", 1, "heh isol/fina + twodotshorizontalabove-ar"),
    (r"hehGoal-ar(\.init)?", 2, "heh skeleton, goal variant (Rubik hehgoal)"),
    (r"hehGoalHamzaabove-ar(\.(init|medi|fina))?", 1,
     "hehGoal form + hamzaabove-ar"),
    (r"tehMarbutaGoal-ar(\.fina)?", 1, "hehGoal form + dots"),
    (r"hehDoachashmee-ar(\.init)?", 2,
     "from green hehDoachashmee.medi/.fina family (regen isol/init)"),
    (r"alefMaksura-ar(\.fina)?", 2,
     "green yeh-ar.fina minus dot contours; isol = fina minus entry"),
    (r"alefMaksura-ar\.(init|medi)", 2,
     "copy behDotless-ar.init/.medi (dotless yeh tooth)"),
    (r"farsiYeh-ar", 2, "copy alefMaksura-ar (isol)"),
    (r"yeh-ar", 1, "alefMaksura-ar + twodotshorizontalbelow-ar"),
    (r"yehHamzaabove-ar(\.(init|medi|fina))?", 1,
     "alefMaksura/behDotless form + hamzaabove-ar"),
    (r"yehBarree-ar(\.fina)?", 3,
     "SKEL yehBarree: wide flat swept stroke (Rubik yehbarree)"),

    # ---- alef variants & hamza -------------------------------------------
    (r"alef(Madda|Wasla)-ar(\.fina)?", 1, "alef form + madda/wasla mark"),
    (r"alefHamzabelow-ar\.fina", 1, "alef-ar.fina + hamzabelow-ar"),
    (r"hamza-ar", 2, "green hamzaabove-ar scaled ~1.3x seated on baseline"),
    (r"(alefabove|alefbelow)-ar", 3, "SMALL mark: miniature alef bar"),

    # ---- harakat (small marks) -------------------------------------------
    (r"(fatha|kasra)-ar", 3, "SMALL mark: 45-deg slanted bar (Rubik angle)"),
    (r"damma-ar", 3, "SMALL mark: miniature waw (green waw DNA)"),
    (r"sukun-ar", 3, "SMALL mark: small open circle/chamfered ring"),
    (r"shadda-ar", 3, "SMALL mark: small w-form (Rubik shadda)"),
    (r"madda-ar", 3, "SMALL mark: flat swept tilde"),
    (r"wasla-ar", 3, "SMALL mark: miniature sad-head"),
    (r"(fathatan|kasratan)-ar", 1, "2x fatha/kasra stacked"),
    (r"dammatan-ar", 1, "damma + tail flick OR 2x damma per Rubik"),
    (r"invertedDamma-ar", 2, "damma-ar flipped (regen red drawing)"),
    (r"hamzaabove(Fatha|Fathatan|Damma|Dammatan|Sukun)-ar", 1,
     "hamzaabove-ar + mark stacked"),
    (r"hamzabelow(Kasra|Kasratan)-ar", 1, "hamzabelow-ar + mark stacked"),
    (r"shadda(Fatha|Fathatan|Damma|Dammatan|Kasra|Kasratan|Alefabove)-ar", 1,
     "shadda-ar + mark stacked"),
    (r"smallHigh(Tah|Zain|ThreeDots)-ar", 2,
     "regen from parent shapes scaled (tah head, zain, 3-dots)"),

    # ---- digits ----------------------------------------------------------
    (r"(zero|one|two|three|four|five|six|seven|eight|nine)-ar", 4,
     "Arabic-Indic digit: draw per Rubik proportions, math grammar strokes"),
    (r"(zero|one|two|three|seven|eight|nine)Farsi-ar", 2,
     "copy/adjust Arabic-Indic digit"),
    (r"(four|five|six)Farsi-ar", 4, "distinct Farsi digit drawing"),

    # ---- punctuation & signs ---------------------------------------------
    (r"(comma|semicolon)-ar", 2, "mirror/rotate Latin comma/semicolon"),
    (r"question-ar", 2, "mirror Latin question (keep Virtua chamfers)"),
    (r"(percent|perMille)-ar", 4, "Arabic percent: Latin DNA, Rubik layout"),
    (r"paren(left|right)-ar", 2, "swap Latin parenright/parenleft"),
    (r"asterisk-ar", 4, "Arabic star (8-point), math grammar"),
    (r"fullStop-ar", 2, "regen from Latin period at Arabic size"),
    (r"(decimalseparator|thousandseparator|dateSeparator)-ar", 4,
     "small separator marks per Unicode chart + Rubik"),
    (r"kashida-ar", 4, "tatweel: plain baseline bar, joining width"),
    (r"doublestroke-ar", 4, "U+0602-ish sign part / footnote stroke"),
    (r"arabic(FootnoteMarker|NumberSign|SignSafha|SignSanah)", 3,
     "ornate sign — DEFER-CANDIDATE: check GF glyphset requirement first"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=pathlib.Path,
                    default=REPO / "build" / "arabic-lanes.json")
    args = ap.parse_args()

    contents = plistlib.loads((UFO / "glyphs" / "contents.plist").read_bytes())
    targets = []
    for name, fn in sorted(contents.items()):
        if "-ar" not in name and not name.startswith("arabic"):
            continue
        text = (UFO / "glyphs" / fn).read_text()
        m = re.search(r"markColor</key>\s*<string>([^<]+)", text)
        color = m.group(1) if m else None
        if color and color.startswith("0.09"):
            continue  # green: approved, never touch
        state = ("empty" if "<contour" not in text and "<component" not in text
                 else "composite" if "<component" in text else "drawn")
        targets.append((name, state))

    manifest = OrderedDict()
    unmatched = []
    for name, state in targets:
        for pat, lane, recipe in RULES:
            if re.fullmatch(pat, name):
                manifest[name] = {"lane": lane, "state": state,
                                  "recipe": recipe}
                break
        else:
            unmatched.append(name)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(manifest, indent=1))

    counts = {}
    for rec in manifest.values():
        counts[rec["lane"]] = counts.get(rec["lane"], 0) + 1
    print(f"targets: {len(targets)}  classified: {len(manifest)}")
    for lane in sorted(counts):
        label = {1: "recompose", 2: "derive", 3: "skeleton", 4: "symbol"}[lane]
        print(f"  lane {lane} {label:10s} {counts[lane]}")
    skels = sorted(n for n, r in manifest.items() if r["lane"] == 3)
    print(f"\nlane-3 drawings ({len(skels)}):")
    for n in skels:
        print(f"  {n:34s} {manifest[n]['recipe']}")
    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}): {' '.join(unmatched)}")
        return 1
    print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
