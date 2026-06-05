#!/usr/bin/env python3
"""Create or report Arabic candidate glyphs across both Virtua UFO masters.

The script is deliberately conservative: dry-run is the default, and write mode
only creates candidate sources that still need human drawing/proof review.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "documentation/glyph-review/arabic-source-work-checklist.md"
UFO_PATHS = (
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
)
POSITIONAL_SUFFIXES = (".fina", ".init", ".medi")

UNICODES = {
    "plus": 0x002B,
    "less": 0x003C,
    "equal": 0x003D,
    "greater": 0x003E,
    "at": 0x0040,
    "bracketleft": 0x005B,
    "bracketright": 0x005D,
    "asciicircum": 0x005E,
    "grave": 0x0060,
    "braceleft": 0x007B,
    "bar": 0x007C,
    "braceright": 0x007D,
    "asciitilde": 0x007E,
    "cent": 0x00A2,
    "sterling": 0x00A3,
    "yen": 0x00A5,
    "copyright": 0x00A9,
    "guillemotleft": 0x00AB,
    "registered": 0x00AE,
    "degree": 0x00B0,
    "guillemotright": 0x00BB,
    "multiply": 0x00D7,
    "divide": 0x00F7,
    "arabicNumberSign": 0x0600,
    "arabicSignSanah": 0x0601,
    "arabicFootnoteMarker": 0x0602,
    "arabicSignSafha": 0x0603,
    "perMille-ar": 0x0609,
    "dateSeparator-ar": 0x060D,
    "smallHighTah-ar": 0x0615,
    "smallHighZain-ar": 0x0617,
    "invertedDamma-ar": 0x0657,
    "noonGhunna-ar": 0x0658,
    "tteheh-ar": 0x067A,
    "beeh-ar": 0x067B,
    "tehRing-ar": 0x067C,
    "tehThreedotsdown-ar": 0x067D,
    "tteh-ar": 0x0679,
    "peh-ar": 0x067E,
    "tcheh-ar": 0x0686,
    "ddal-ar": 0x0688,
    "rreh-ar": 0x0691,
    "jeh-ar": 0x0698,
    "seenSixdots-ar": 0x069C,
    "fehDotmovedbelow-ar": 0x06A2,
    "fehThreedotsbelow-ar": 0x06A5,
    "qafDotabove-ar": 0x06A7,
    "qafThreedotsabove-ar": 0x06A8,
    "keheh-ar": 0x06A9,
    "gaf-ar": 0x06AF,
    "hehDoachashmee-ar": 0x06BE,
    "hehGoal-ar": 0x06C1,
    "hehGoalHamzaabove-ar": 0x06C2,
    "tehMarbutaGoal-ar": 0x06C3,
    "farsiYeh-ar": 0x06CC,
    "yehBarree-ar": 0x06D2,
    "fullStop-ar": 0x06D4,
    "smallHighThreeDots-ar": 0x06DB,
    "zeroFarsi-ar": 0x06F0,
    "oneFarsi-ar": 0x06F1,
    "twoFarsi-ar": 0x06F2,
    "threeFarsi-ar": 0x06F3,
    "fourFarsi-ar": 0x06F4,
    "fiveFarsi-ar": 0x06F5,
    "sixFarsi-ar": 0x06F6,
    "sevenFarsi-ar": 0x06F7,
    "eightFarsi-ar": 0x06F8,
    "nineFarsi-ar": 0x06F9,
    "kehehThreedotsabove-ar": 0x0763,
    "guilsinglleft": 0x2039,
    "guilsinglright": 0x203A,
    "uni200C": 0x200C,
    "uni200D": 0x200D,
    "uni200F": 0x200F,
    "Euro": 0x20AC,
    "trademark": 0x2122,
    "dottedCircle": 0x25CC,
    "comma-ar": 0x060C,
    "semicolon-ar": 0x061B,
    "question-ar": 0x061F,
    "asterisk-ar": 0x066D,
    "percent-ar": 0x066A,
    "decimalseparator-ar": 0x066B,
    "thousandseparator-ar": 0x066C,
    "zero-ar": 0x0660,
    "one-ar": 0x0661,
    "two-ar": 0x0662,
    "three-ar": 0x0663,
    "four-ar": 0x0664,
    "five-ar": 0x0665,
    "six-ar": 0x0666,
    "seven-ar": 0x0667,
    "eight-ar": 0x0668,
    "nine-ar": 0x0669,
    "hamza-ar": 0x0621,
    "alefMadda-ar": 0x0622,
    "wawHamzaabove-ar": 0x0624,
    "yehHamzaabove-ar": 0x0626,
    "hah-ar": 0x062D,
    "reh-ar": 0x0631,
    "sad-ar": 0x0635,
    "tah-ar": 0x0637,
    "kaf-ar": 0x0643,
    "kashida-ar": 0x0640,
    "lam-ar": 0x0644,
    "meem-ar": 0x0645,
    "heh-ar": 0x0647,
    "alefMaksura-ar": 0x0649,
    "behDotless-ar": 0x066E,
    "qafDotless-ar": 0x066F,
    "alefWasla-ar": 0x0671,
    "noonghunna-ar": 0x06BA,
    "fehDotless-ar": 0x06A1,
    "parenleft-ar": 0xFD3E,
    "parenright-ar": 0xFD3F,
    "ellipsis": 0x2026,
    "exclamdown": 0x00A1,
    "questiondown": 0x00BF,
    "periodcentered": 0x00B7,
    "bullet": 0x2022,
    "numbersign": 0x0023,
    "backslash": 0x005C,
    "endash": 0x2013,
    "underscore": 0x005F,
    "quotesinglbase": 0x201A,
    "quoteleft": 0x2018,
    "quotedbl": 0x0022,
}

BASES = {
    "tteh-ar": "teh-ar",
    "tteheh-ar": "teh-ar",
    "beeh-ar": "behDotless-ar",
    "tehRing-ar": "teh-ar",
    "tehThreedotsdown-ar": "teh-ar",
    "peh-ar": "behDotless-ar",
    "tcheh-ar": "hah-ar",
    "ddal-ar": "dal-ar",
    "rreh-ar": "reh-ar",
    "jeh-ar": "reh-ar",
    "seenSixdots-ar": "seen-ar",
    "fehDotmovedbelow-ar": "fehDotless-ar",
    "fehThreedotsbelow-ar": "fehDotless-ar",
    "qafDotabove-ar": "qafDotless-ar",
    "qafThreedotsabove-ar": "qafDotless-ar",
    "keheh-ar": "kaf-ar",
    "gaf-ar": "kaf-ar",
    "hehDoachashmee-ar": "heh-ar",
    "hehGoal-ar": "heh-ar",
    "hehGoalHamzaabove-ar": "hehGoal-ar",
    "tehMarbutaGoal-ar": "tehMarbuta-ar",
    "farsiYeh-ar": "yeh-ar",
    "yehBarree-ar": "alefMaksura-ar",
    "kehehThreedotsabove-ar": "kaf-ar",
    "zeroFarsi-ar": "zero-ar",
    "oneFarsi-ar": "one-ar",
    "twoFarsi-ar": "two-ar",
    "threeFarsi-ar": "three-ar",
    "fourFarsi-ar": "four-ar",
    "fiveFarsi-ar": "five-ar",
    "sixFarsi-ar": "six-ar",
    "sevenFarsi-ar": "seven-ar",
    "eightFarsi-ar": "eight-ar",
    "nineFarsi-ar": "nine-ar",
    "perMille-ar": "percent-ar",
    "fullStop-ar": "period",
}

ADVANCE_WIDTHS = {
    "default": 600,
    "bar": 320,
    "braceleft": 360,
    "braceright": 360,
    "bracketleft": 320,
    "bracketright": 320,
    "dottedCircle": 600,
    "dateSeparator-ar": 300,
    "grave": 300,
    "asciicircum": 420,
    "asciitilde": 520,
    "at": 720,
    "copyright": 720,
    "registered": 720,
    "trademark": 760,
    "arabicNumberSign": 0,
    "arabicSignSanah": 0,
    "arabicFootnoteMarker": 0,
    "arabicSignSafha": 0,
    "beeh-ar": 600,
    "beeh-ar.fina": 600,
    "tteheh-ar": 600,
    "tteheh-ar.fina": 600,
    "tehRing-ar": 600,
    "tehRing-ar.fina": 600,
    "tehThreedotsdown-ar": 600,
    "tehThreedotsdown-ar.fina": 600,
    "peh-ar": 600,
    "peh-ar.fina": 600,
    "tcheh-ar": 600,
    "tcheh-ar.fina": 600,
    "tcheh-ar.medi": 600,
    "rreh-ar": 600,
    "jeh-ar": 600,
    "seenSixdots-ar": 864,
    "seenSixdots-ar.fina": 864,
    "fehDotmovedbelow-ar": 600,
    "fehDotmovedbelow-ar.fina": 600,
    "fehThreedotsbelow-ar": 600,
    "fehThreedotsbelow-ar.fina": 600,
    "qafDotabove-ar": 600,
    "qafDotabove-ar.fina": 600,
    "qafThreedotsabove-ar": 600,
    "qafThreedotsabove-ar.fina": 600,
    "keheh-ar": 680,
    "keheh-ar.init": 416,
    "keheh-ar.medi": 416,
    "gaf-ar": 680,
    "gaf-ar.init": 416,
    "gaf-ar.medi": 416,
    "hehDoachashmee-ar": 528,
    "hehDoachashmee-ar.init": 416,
    "hehGoal-ar": 528,
    "hehGoal-ar.init": 416,
    "hehGoalHamzaabove-ar": 528,
    "hehGoalHamzaabove-ar.init": 416,
    "tehMarbutaGoal-ar": 528,
    "tehMarbutaGoal-ar.fina": 528,
    "yehBarree-ar": 760,
    "yehBarree-ar.fina": 760,
    "kehehThreedotsabove-ar": 680,
    "kehehThreedotsabove-ar.fina": 680,
    "kehehThreedotsabove-ar.init": 416,
    "kehehThreedotsabove-ar.medi": 416,
    "smallHighTah-ar": 0,
    "smallHighZain-ar": 0,
    "invertedDamma-ar": 0,
    "noonGhunna-ar": 0,
    "smallHighThreeDots-ar": 0,
    "uni200C": 0,
    "uni200D": 0,
    "uni200F": 0,
    "comma-ar": 280,
    "semicolon-ar": 280,
    "question-ar": 480,
    "decimalseparator-ar": 280,
    "thousandseparator-ar": 280,
    "kashida-ar": 520,
}

GEOMETRIC_GLYPHS = {
    "plus",
    "less",
    "equal",
    "greater",
    "at",
    "bracketleft",
    "bracketright",
    "asciicircum",
    "grave",
    "braceleft",
    "bar",
    "braceright",
    "asciitilde",
    "cent",
    "sterling",
    "yen",
    "copyright",
    "registered",
    "degree",
    "multiply",
    "divide",
    "guillemotleft",
    "guillemotright",
    "guilsinglleft",
    "guilsinglright",
    "dottedCircle",
    "Euro",
    "trademark",
    "arabicNumberSign",
    "arabicSignSanah",
    "arabicFootnoteMarker",
    "arabicSignSafha",
    "perMille-ar",
    "dateSeparator-ar",
    "smallHighTah-ar",
    "smallHighZain-ar",
    "invertedDamma-ar",
    "noonGhunna-ar",
    "smallHighThreeDots-ar",
    "comma-ar",
    "semicolon-ar",
    "question-ar",
    "asterisk-ar",
    "percent-ar",
    "decimalseparator-ar",
    "thousandseparator-ar",
    "zero-ar",
    "one-ar",
    "two-ar",
    "three-ar",
    "four-ar",
    "five-ar",
    "six-ar",
    "seven-ar",
    "eight-ar",
    "nine-ar",
    "dotcenter-ar",
    "doublestroke-ar",
    "gafsarkashabove-ar",
    "gafsarkashcenter-ar",
    "miniKeheh-ar",
    "twodotsverticalabove-ar",
    "twodotsverticalbelow-ar",
    "twodotshorizontalbelow-ar",
    "threedotsdownabove-ar",
    "threedotsdownbelow-ar",
    "threedotsdowncenter-ar",
    "threedotsupbelow-ar",
    "wasla-ar",
    "hamza-ar",
    "hamzaaboveDamma-ar",
    "hamzaaboveDammatan-ar",
    "hamzaaboveFatha-ar",
    "hamzaaboveFathatan-ar",
    "hamzaaboveSukun-ar",
    "hamzabelowKasra-ar",
    "hamzabelowKasratan-ar",
    "shaddaAlefabove-ar",
    "shaddaDamma-ar",
    "shaddaDammatan-ar",
    "shaddaFatha-ar",
    "shaddaFathatan-ar",
    "shaddaKasra-ar",
    "shaddaKasratan-ar",
    "behDotless-ar",
    "behDotless-ar.fina",
    "fehDotless-ar",
    "fehDotless-ar.fina",
    "qafDotless-ar",
    "qafDotless-ar.fina",
    "hah-ar",
    "hah-ar.fina",
    "hah-ar.medi",
    "reh-ar",
    "sad-ar",
    "sad-ar.fina",
    "sad-ar.init",
    "sad-ar.medi",
    "tah-ar",
    "tah-ar.fina",
    "tah-ar.init",
    "tah-ar.medi",
    "kaf-ar",
    "kaf-ar.init",
    "kaf-ar.medi",
    "kashida-ar",
    "lam-ar",
    "meem-ar",
    "meem-ar.fina",
    "meem-ar.init",
    "meem-ar.medi",
    "heh-ar",
    "heh-ar.init",
    "noonghunna-ar",
    "noonghunna-ar.fina",
    "alefMadda-ar",
    "alefMadda-ar.fina",
    "alefWasla-ar",
    "alefWasla-ar.fina",
    "alefMaksura-ar",
    "alefMaksura-ar.fina",
    "alefMaksura-ar.init",
    "alefMaksura-ar.medi",
    "wawHamzaabove-ar",
    "wawHamzaabove-ar.fina",
    "yehHamzaabove-ar",
    "yehHamzaabove-ar.fina",
    "yehHamzaabove-ar.init",
    "yehHamzaabove-ar.medi",
    "lam_alef-ar",
    "lam_alefHamzaabove-ar",
    "lam_alefHamzaabove-ar.fina",
    "lam_alefHamzabelow-ar",
    "lam_alefHamzabelow-ar.fina",
    "lam_alefMadda-ar",
    "lam_alefMadda-ar.fina",
    "lam_alefWasla-ar",
    "lam_alefWasla-ar.fina",
    "ain-ar.fina",
    "alefHamzabelow-ar.fina",
    "seen-ar.medi",
    "waw-ar.fina",
    "parenleft-ar",
    "parenright-ar",
    "ellipsis",
    "exclamdown",
    "questiondown",
    "periodcentered",
    "bullet",
    "numbersign",
    "backslash",
    "endash",
    "underscore",
    "quotesinglbase",
    "quoteleft",
    "quotedbl",
    "peh-ar",
    "peh-ar.fina",
    "beeh-ar",
    "beeh-ar.fina",
    "beeh-ar.init",
    "beeh-ar.medi",
    "tteheh-ar",
    "tteheh-ar.fina",
    "tteheh-ar.init",
    "tteheh-ar.medi",
    "tehRing-ar",
    "tehRing-ar.fina",
    "tehRing-ar.init",
    "tehRing-ar.medi",
    "tehThreedotsdown-ar",
    "tehThreedotsdown-ar.fina",
    "tehThreedotsdown-ar.init",
    "tehThreedotsdown-ar.medi",
    "tcheh-ar",
    "tcheh-ar.fina",
    "tcheh-ar.medi",
    "rreh-ar",
    "jeh-ar",
    "seenSixdots-ar",
    "seenSixdots-ar.fina",
    "seenSixdots-ar.init",
    "seenSixdots-ar.medi",
    "fehDotmovedbelow-ar",
    "fehDotmovedbelow-ar.fina",
    "fehDotmovedbelow-ar.init",
    "fehDotmovedbelow-ar.medi",
    "fehThreedotsbelow-ar",
    "fehThreedotsbelow-ar.fina",
    "fehThreedotsbelow-ar.init",
    "fehThreedotsbelow-ar.medi",
    "qafDotabove-ar",
    "qafDotabove-ar.fina",
    "qafDotabove-ar.init",
    "qafDotabove-ar.medi",
    "qafThreedotsabove-ar",
    "qafThreedotsabove-ar.fina",
    "qafThreedotsabove-ar.init",
    "qafThreedotsabove-ar.medi",
    "keheh-ar",
    "keheh-ar.init",
    "keheh-ar.medi",
    "gaf-ar",
    "gaf-ar.init",
    "gaf-ar.medi",
    "hehDoachashmee-ar",
    "hehDoachashmee-ar.init",
    "hehGoal-ar",
    "hehGoal-ar.init",
    "hehGoalHamzaabove-ar",
    "hehGoalHamzaabove-ar.fina",
    "hehGoalHamzaabove-ar.init",
    "hehGoalHamzaabove-ar.medi",
    "tehMarbutaGoal-ar",
    "tehMarbutaGoal-ar.fina",
    "yehBarree-ar",
    "yehBarree-ar.fina",
    "kehehThreedotsabove-ar",
    "kehehThreedotsabove-ar.fina",
    "kehehThreedotsabove-ar.init",
    "kehehThreedotsabove-ar.medi",
    "zeroFarsi-ar",
    "oneFarsi-ar",
    "twoFarsi-ar",
    "threeFarsi-ar",
    "fourFarsi-ar",
    "fiveFarsi-ar",
    "sixFarsi-ar",
    "sevenFarsi-ar",
    "eightFarsi-ar",
    "nineFarsi-ar",
}

CORE_ARABIC_REMEDIATION_GLYPHS = (
    "dotcenter-ar",
    "doublestroke-ar",
    "gafsarkashabove-ar",
    "gafsarkashcenter-ar",
    "miniKeheh-ar",
    "twodotsverticalabove-ar",
    "twodotsverticalbelow-ar",
    "twodotshorizontalbelow-ar",
    "threedotsdownabove-ar",
    "threedotsdownbelow-ar",
    "threedotsdowncenter-ar",
    "threedotsupbelow-ar",
    "wasla-ar",
    "hamza-ar",
    "hamzaaboveDamma-ar",
    "hamzaaboveDammatan-ar",
    "hamzaaboveFatha-ar",
    "hamzaaboveFathatan-ar",
    "hamzaaboveSukun-ar",
    "hamzabelowKasra-ar",
    "hamzabelowKasratan-ar",
    "shaddaAlefabove-ar",
    "shaddaDamma-ar",
    "shaddaDammatan-ar",
    "shaddaFatha-ar",
    "shaddaFathatan-ar",
    "shaddaKasra-ar",
    "shaddaKasratan-ar",
    "behDotless-ar",
    "behDotless-ar.fina",
    "fehDotless-ar",
    "fehDotless-ar.fina",
    "qafDotless-ar",
    "qafDotless-ar.fina",
    "hah-ar",
    "hah-ar.fina",
    "hah-ar.medi",
    "reh-ar",
    "sad-ar",
    "sad-ar.fina",
    "sad-ar.init",
    "sad-ar.medi",
    "tah-ar",
    "tah-ar.fina",
    "tah-ar.init",
    "tah-ar.medi",
    "kaf-ar",
    "kaf-ar.init",
    "kaf-ar.medi",
    "kashida-ar",
    "lam-ar",
    "meem-ar",
    "meem-ar.fina",
    "meem-ar.init",
    "meem-ar.medi",
    "heh-ar",
    "heh-ar.init",
    "noonghunna-ar",
    "noonghunna-ar.fina",
    "alefMadda-ar",
    "alefMadda-ar.fina",
    "alefWasla-ar",
    "alefWasla-ar.fina",
    "alefMaksura-ar",
    "alefMaksura-ar.fina",
    "alefMaksura-ar.init",
    "alefMaksura-ar.medi",
    "wawHamzaabove-ar",
    "wawHamzaabove-ar.fina",
    "yehHamzaabove-ar",
    "yehHamzaabove-ar.fina",
    "yehHamzaabove-ar.init",
    "yehHamzaabove-ar.medi",
    "lam_alef-ar",
    "lam_alefHamzaabove-ar",
    "lam_alefHamzaabove-ar.fina",
    "lam_alefHamzabelow-ar",
    "lam_alefHamzabelow-ar.fina",
    "lam_alefMadda-ar",
    "lam_alefMadda-ar.fina",
    "lam_alefWasla-ar",
    "lam_alefWasla-ar.fina",
    "ain-ar.fina",
    "alefHamzabelow-ar.fina",
    "seen-ar.medi",
    "waw-ar.fina",
    "parenleft-ar",
    "parenright-ar",
    "ellipsis",
    "exclamdown",
    "questiondown",
    "periodcentered",
    "bullet",
    "numbersign",
    "backslash",
    "endash",
    "underscore",
    "quotesinglbase",
    "quoteleft",
    "quotedbl",
)

MANAGED_CODEPOINT_GLYPHS = {
    0x002B: ("plus",),
    0x003C: ("less",),
    0x003D: ("equal",),
    0x003E: ("greater",),
    0x0040: ("at",),
    0x005B: ("bracketleft",),
    0x005D: ("bracketright",),
    0x005E: ("asciicircum",),
    0x0060: ("grave",),
    0x007B: ("braceleft",),
    0x007C: ("bar",),
    0x007D: ("braceright",),
    0x007E: ("asciitilde",),
    0x00A2: ("cent",),
    0x00A3: ("sterling",),
    0x00A5: ("yen",),
    0x00A9: ("copyright",),
    0x00AB: ("guillemotleft",),
    0x00AE: ("registered",),
    0x00B0: ("degree",),
    0x00BB: ("guillemotright",),
    0x00D7: ("multiply",),
    0x00F7: ("divide",),
    0x0600: ("arabicNumberSign",),
    0x0601: ("arabicSignSanah",),
    0x0602: ("arabicFootnoteMarker",),
    0x0603: ("arabicSignSafha",),
    0x0609: ("perMille-ar",),
    0x060D: ("dateSeparator-ar",),
    0x060C: ("comma-ar",),
    0x061B: ("semicolon-ar",),
    0x061F: ("question-ar",),
    0x0615: ("smallHighTah-ar",),
    0x0617: ("smallHighZain-ar",),
    0x0657: ("invertedDamma-ar",),
    0x0658: ("noonGhunna-ar",),
    0x0660: ("zero-ar",),
    0x0661: ("one-ar",),
    0x0662: ("two-ar",),
    0x0663: ("three-ar",),
    0x0664: ("four-ar",),
    0x0665: ("five-ar",),
    0x0666: ("six-ar",),
    0x0667: ("seven-ar",),
    0x0668: ("eight-ar",),
    0x0669: ("nine-ar",),
    0x066A: ("percent-ar",),
    0x066B: ("decimalseparator-ar",),
    0x066C: ("thousandseparator-ar",),
    0x066D: ("asterisk-ar",),
    0x0679: ("tteh-ar", "tteh-ar.fina", "tteh-ar.init", "tteh-ar.medi"),
    0x067A: ("tteheh-ar", "tteheh-ar.fina", "tteheh-ar.init", "tteheh-ar.medi"),
    0x067B: ("beeh-ar", "beeh-ar.fina", "beeh-ar.init", "beeh-ar.medi"),
    0x067C: ("tehRing-ar", "tehRing-ar.fina", "tehRing-ar.init", "tehRing-ar.medi"),
    0x067D: ("tehThreedotsdown-ar", "tehThreedotsdown-ar.fina", "tehThreedotsdown-ar.init", "tehThreedotsdown-ar.medi"),
    0x067E: ("peh-ar", "peh-ar.fina", "peh-ar.init", "peh-ar.medi"),
    0x0686: ("tcheh-ar", "tcheh-ar.fina", "tcheh-ar.init", "tcheh-ar.medi"),
    0x0688: ("ddal-ar", "ddal-ar.fina"),
    0x0691: ("rreh-ar", "rreh-ar.fina"),
    0x0698: ("jeh-ar", "jeh-ar.fina"),
    0x069C: ("seenSixdots-ar", "seenSixdots-ar.fina", "seenSixdots-ar.init", "seenSixdots-ar.medi"),
    0x06A2: ("fehDotmovedbelow-ar", "fehDotmovedbelow-ar.fina", "fehDotmovedbelow-ar.init", "fehDotmovedbelow-ar.medi"),
    0x06A5: ("fehThreedotsbelow-ar", "fehThreedotsbelow-ar.fina", "fehThreedotsbelow-ar.init", "fehThreedotsbelow-ar.medi"),
    0x06A7: ("qafDotabove-ar", "qafDotabove-ar.fina", "qafDotabove-ar.init", "qafDotabove-ar.medi"),
    0x06A8: ("qafThreedotsabove-ar", "qafThreedotsabove-ar.fina", "qafThreedotsabove-ar.init", "qafThreedotsabove-ar.medi"),
    0x06A9: ("keheh-ar", "keheh-ar.fina", "keheh-ar.init", "keheh-ar.medi"),
    0x06AF: ("gaf-ar", "gaf-ar.fina", "gaf-ar.init", "gaf-ar.medi"),
    0x06BE: ("hehDoachashmee-ar", "hehDoachashmee-ar.fina", "hehDoachashmee-ar.init", "hehDoachashmee-ar.medi"),
    0x06C1: ("hehGoal-ar", "hehGoal-ar.fina", "hehGoal-ar.init", "hehGoal-ar.medi"),
    0x06C2: ("hehGoalHamzaabove-ar", "hehGoalHamzaabove-ar.fina", "hehGoalHamzaabove-ar.init", "hehGoalHamzaabove-ar.medi"),
    0x06C3: ("tehMarbutaGoal-ar", "tehMarbutaGoal-ar.fina"),
    0x06CC: ("farsiYeh-ar", "farsiYeh-ar.fina", "farsiYeh-ar.init", "farsiYeh-ar.medi"),
    0x06D2: ("yehBarree-ar", "yehBarree-ar.fina"),
    0x06D4: ("fullStop-ar",),
    0x06DB: ("smallHighThreeDots-ar",),
    0x06F0: ("zeroFarsi-ar",),
    0x06F1: ("oneFarsi-ar",),
    0x06F2: ("twoFarsi-ar",),
    0x06F3: ("threeFarsi-ar",),
    0x06F4: ("fourFarsi-ar",),
    0x06F5: ("fiveFarsi-ar",),
    0x06F6: ("sixFarsi-ar",),
    0x06F7: ("sevenFarsi-ar",),
    0x06F8: ("eightFarsi-ar",),
    0x06F9: ("nineFarsi-ar",),
    0x0763: ("kehehThreedotsabove-ar", "kehehThreedotsabove-ar.fina", "kehehThreedotsabove-ar.init", "kehehThreedotsabove-ar.medi"),
    0x2039: ("guilsinglleft",),
    0x203A: ("guilsinglright",),
    0x200C: ("uni200C",),
    0x200D: ("uni200D",),
    0x200F: ("uni200F",),
    0x20AC: ("Euro",),
    0x2122: ("trademark",),
    0x25CC: ("dottedCircle",),
}


@dataclass(frozen=True)
class WorkItem:
    glyph_name: str
    codepoint: int | None
    batch: str
    source_row: str


def read_contents(ufo_path: Path) -> dict[str, str]:
    return plistlib.loads((ufo_path / "glyphs" / "contents.plist").read_bytes())


def write_contents(ufo_path: Path, contents: dict[str, str]) -> None:
    (ufo_path / "glyphs" / "contents.plist").write_bytes(plistlib.dumps(contents, sort_keys=True))


def parse_worklist() -> list[WorkItem]:
    items: list[WorkItem] = []
    for line in CHECKLIST.read_text().splitlines():
        if not line.startswith("| U+"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 4:
            continue
        codepoint = int(cells[0].split()[0].removeprefix("U+"), 16)
        batch = batch_for_codepoint(codepoint)
        for glyph_name in re.findall(r"`([^`]+)`", cells[3]):
            glyph_codepoint = None if glyph_name.endswith(POSITIONAL_SUFFIXES) else UNICODES.get(glyph_name, codepoint)
            items.append(WorkItem(glyph_name, glyph_codepoint, batch, line))
    return items or managed_worklist()


def managed_worklist() -> list[WorkItem]:
    items: list[WorkItem] = []
    for codepoint, glyph_names in MANAGED_CODEPOINT_GLYPHS.items():
        for glyph_name in glyph_names:
            glyph_codepoint = None if glyph_name.endswith(POSITIONAL_SUFFIXES) else UNICODES.get(glyph_name, codepoint)
            items.append(WorkItem(glyph_name, glyph_codepoint, batch_for_codepoint(codepoint), "managed candidate glyph"))
    for glyph_name in CORE_ARABIC_REMEDIATION_GLYPHS:
        glyph_codepoint = None if glyph_name.endswith(POSITIONAL_SUFFIXES) else UNICODES.get(glyph_name)
        items.append(WorkItem(glyph_name, glyph_codepoint, "core-arabic-remediation", "managed no-contour remediation glyph"))
    return items


def split_markdown_row(line: str) -> list[str]:
    placeholder = "\uE000"
    protected = line.strip().strip("|").replace(r"\|", placeholder)
    return [cell.replace(placeholder, "|").strip() for cell in protected.split("|")]


def batch_for_codepoint(codepoint: int) -> str:
    if codepoint in {0x0615, 0x0617, 0x0657, 0x0658, 0x06DB}:
        return "arabic-marks"
    if 0x0660 <= codepoint <= 0x0669:
        return "arabic-digits"
    if 0x06F0 <= codepoint <= 0x06F9:
        return "farsi-digits"
    if codepoint in {0x0600, 0x0601, 0x0602, 0x0603, 0x0609, 0x060C, 0x060D, 0x061B, 0x061F, 0x066A, 0x066B, 0x066C, 0x066D, 0x06D4}:
        return "arabic-punctuation"
    if codepoint in {0x200C, 0x200D, 0x200F}:
        return "format-controls"
    if 0x0600 <= codepoint <= 0x077F:
        return "joining-letters"
    return "shared-punctuation"


def base_for(glyph_name: str) -> str | None:
    suffix = ""
    stem = glyph_name
    for candidate_suffix in POSITIONAL_SUFFIXES:
        if glyph_name.endswith(candidate_suffix):
            suffix = candidate_suffix
            stem = glyph_name[: -len(candidate_suffix)]
            break
    base_stem = BASES.get(stem)
    if not base_stem:
        return None
    return f"{base_stem}{suffix}"


def filename_for(glyph_name: str, contents: dict[str, str]) -> str:
    candidate = f"{glyph_name}.glif"
    used = {filename.lower() for filename in contents.values()}
    if candidate.lower() not in used:
        return candidate
    index = 1
    while True:
        candidate = f"{glyph_name}.{index:03d}.glif"
        if candidate.lower() not in used:
            return candidate
        index += 1


def create_empty_glif(glyph_name: str, codepoint: int | None, width: int) -> bytes:
    glyph = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    if codepoint is not None:
        ET.SubElement(glyph, "unicode", {"hex": f"{codepoint:04X}"})
    ET.SubElement(glyph, "advance", {"width": str(width)})
    return serialize_xml(glyph)


def create_geometric_glif(glyph_name: str, codepoint: int | None, width: int, bold: bool) -> bytes | None:
    thickness = 116 if bold else 80
    thin = 84 if bold else 56
    glyph = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    if codepoint is not None:
        ET.SubElement(glyph, "unicode", {"hex": f"{codepoint:04X}"})
    ET.SubElement(glyph, "advance", {"width": str(width)})
    outline = ET.SubElement(glyph, "outline")

    def rect(x: int, y: int, w: int, h: int) -> None:
        contour = ET.SubElement(outline, "contour")
        for px, py in ((x, y), (x + w, y), (x + w, y + h), (x, y + h)):
            ET.SubElement(contour, "point", {"x": str(px), "y": str(py), "type": "line"})

    def poly(points: list[tuple[int, int]]) -> None:
        contour = ET.SubElement(outline, "contour")
        for px, py in points:
            ET.SubElement(contour, "point", {"x": str(px), "y": str(py), "type": "line"})

    def dot(x: int, y: int, size: int | None = None) -> None:
        dot_size = size or (64 if bold else 48)
        rect(x - dot_size // 2, y - dot_size // 2, dot_size, dot_size)

    def three_dots_below(x: int, y: int = -88) -> None:
        dot(x - 56, y)
        dot(x + 56, y)
        dot(x, y - 64)

    def three_dots_above(x: int, y: int = 604) -> None:
        dot(x - 56, y)
        dot(x + 56, y)
        dot(x, y + 64)

    def two_dots_below(x: int, y: int = -88) -> None:
        dot(x - 48, y)
        dot(x + 48, y)

    def two_dots_vertical_below(x: int, y: int = -112) -> None:
        dot(x, y)
        dot(x, y + 76)

    def ring_above(x: int, y: int = 608) -> None:
        dot_size = 76 if bold else 60
        poly([(x, y + dot_size), (x + dot_size, y), (x, y - dot_size), (x - dot_size, y)])
        inner = dot_size // 2
        poly([(x, y + inner), (x - inner, y), (x, y - inner), (x + inner, y)])

    def hamza_above(x: int, y: int = 568) -> None:
        poly([(x - 80, y), (x + 64, y), (x + 80, y + 16), (x + 80, y + 48), (x + 64, y + 64), (x + 16, y + 64), (x - 8, y + 64), (x - 24, y + 80), (x - 24, y + 104), (x + 72, y + 104), (x + 88, y + 120), (x + 88, y + 152), (x + 72, y + 168), (x - 48, y + 168), (x - 96, y + 136), (x - 96, y + 88), (x - 56, y + 56), (x - 80, y + 56)])

    def draw_join_stem() -> None:
        rect(-24, 128, width + 48, thin)

    center = width // 2
    if glyph_name == "plus":
        rect(center - thickness // 2, 168, thickness, 408)
        rect(center - 204, 332, 408, thickness)
    elif glyph_name == "equal":
        rect(center - 204, 416, 408, thickness)
        rect(center - 204, 232, 408, thickness)
    elif glyph_name == "bar":
        rect(center - thickness // 2, -96, thickness, 896)
    elif glyph_name == "bracketleft":
        rect(80, -96, thickness, 896)
        rect(80, -96, 224, thickness)
        rect(80, 684, 224, thickness)
    elif glyph_name == "bracketright":
        rect(width - 80 - thickness, -96, thickness, 896)
        rect(width - 304, -96, 224, thickness)
        rect(width - 304, 684, 224, thickness)
    elif glyph_name == "braceleft":
        rect(96, -96, thickness, 896)
        rect(96, -96, 224, thickness)
        rect(96, 300, 180, thickness)
        rect(96, 684, 224, thickness)
    elif glyph_name == "braceright":
        rect(width - 96 - thickness, -96, thickness, 896)
        rect(width - 320, -96, 224, thickness)
        rect(width - 276, 300, 180, thickness)
        rect(width - 320, 684, 224, thickness)
    elif glyph_name == "less":
        poly([(448, 612), (512, 520), (232, 372), (512, 224), (448, 132), (112, 328), (112, 416)])
    elif glyph_name == "greater":
        poly([(152, 612), (88, 520), (368, 372), (88, 224), (152, 132), (488, 328), (488, 416)])
    elif glyph_name == "asciicircum":
        poly([(72, 520), (136, 440), (212, 608), (288, 440), (352, 520), (244, 744), (180, 744)])
    elif glyph_name == "grave":
        poly([(64, 744), (144, 744), (264, 520), (184, 520)])
    elif glyph_name == "asciitilde":
        poly([(72, 392), (72, 480), (184, 548), (296, 468), (408, 536), (408, 448), (296, 380), (184, 460)])
    elif glyph_name == "at":
        poly([(360, 640), (520, 604), (612, 492), (612, 332), (532, 220), (420, 196), (320, 228), (260, 316), (260, 432), (320, 520), (420, 520), (484, 452), (484, 300), (532, 300), (548, 440), (492, 548), (360, 584), (220, 540), (148, 412), (168, 276), (268, 168), (420, 132), (572, 176), (636, 260), (636, 172), (512, 88), (344, 76), (184, 132), (88, 268), (88, 444), (188, 584)])
        poly([(384, 452), (336, 452), (308, 408), (308, 340), (344, 292), (400, 292), (428, 340), (428, 408)])
    elif glyph_name == "cent":
        rect(center - thin // 2, 132, thin, 512)
        poly([(440, 548), (488, 488), (392, 488), (312, 488), (228, 424), (228, 320), (312, 256), (392, 256), (488, 256), (440, 196), (292, 196), (156, 300), (156, 444), (292, 548)])
    elif glyph_name == "sterling":
        rect(144, 308, 280, thickness)
        poly([(452, 584), (500, 520), (388, 520), (316, 520), (284, 464), (284, 132), (500, 132), (500, 68), (120, 68), (184, 132), (184, 464), (252, 584)])
    elif glyph_name == "yen":
        poly([(96, 584), (188, 584), (300, 400), (412, 584), (504, 584), (344, 332), (344, 132), (256, 132), (256, 332)])
        rect(148, 356, 304, thin)
        rect(148, 260, 304, thin)
    elif glyph_name in {"copyright", "registered"}:
        poly([(360, 660), (520, 612), (620, 492), (620, 328), (520, 208), (360, 160), (200, 208), (100, 328), (100, 492), (200, 612)])
        poly([(360, 572), (244, 540), (176, 456), (176, 364), (244, 280), (360, 248), (476, 280), (544, 364), (544, 456), (476, 540)])
        if glyph_name == "copyright":
            poly([(432, 456), (476, 408), (392, 408), (328, 408), (292, 372), (292, 336), (328, 300), (392, 300), (476, 300), (432, 252), (308, 252), (224, 328), (224, 416), (308, 504)])
        else:
            rect(292, 280, thin, 232)
            poly([(292, 512), (424, 512), (476, 464), (476, 408), (428, 364), (348, 364), (348, 424), (396, 424), (396, 452), (348, 452), (348, 280), (292, 280)])
            poly([(360, 364), (432, 280), (500, 280), (424, 364)])
    elif glyph_name == "degree":
        poly([(center - 88, 584), (center - 44, 660), (center + 44, 660), (center + 88, 584), (center + 44, 508), (center - 44, 508)])
    elif glyph_name == "multiply":
        poly([(156, 184), (240, 184), (332, 292), (424, 184), (508, 184), (384, 372), (508, 560), (424, 560), (332, 452), (240, 560), (156, 560), (280, 372)])
    elif glyph_name == "divide":
        rect(center - 204, 332, 408, thickness)
        dot = 72 if bold else 56
        rect(center - dot // 2, 524, dot, dot)
        rect(center - dot // 2, 164, dot, dot)
    elif glyph_name in {"guilsinglleft", "guillemotleft"}:
        poly([(width - 132, 568), (width - 64, 500), (width - 220, 372), (width - 64, 244), (width - 132, 176), (width - 352, 340), (width - 352, 404)])
        if glyph_name == "guillemotleft":
            poly([(width - 312, 568), (width - 244, 500), (width - 400, 372), (width - 244, 244), (width - 312, 176), (width - 532, 340), (width - 532, 404)])
    elif glyph_name in {"guilsinglright", "guillemotright"}:
        poly([(132, 568), (64, 500), (220, 372), (64, 244), (132, 176), (352, 340), (352, 404)])
        if glyph_name == "guillemotright":
            poly([(312, 568), (244, 500), (400, 372), (244, 244), (312, 176), (532, 340), (532, 404)])
    elif glyph_name == "dottedCircle":
        dot = 56 if bold else 40
        for x, y in ((300, 660), (448, 604), (520, 456), (484, 292), (344, 204), (184, 236), (80, 364), (108, 532)):
            rect(x - dot // 2, y - dot // 2, dot, dot)
    elif glyph_name == "perMille-ar":
        slash = thickness
        poly([(116, 160), (116 + slash, 160), (520, 584), (520 - slash, 584)])
        dot = 60 if bold else 44
        for x, y in ((156, 504), (388, 240), (504, 240)):
            rect(x - dot // 2, y - dot // 2, dot, dot)
    elif glyph_name == "arabicNumberSign":
        poly([(-168, 596), (-112, 652), (112, 652), (168, 596), (112, 540), (-112, 540)])
    elif glyph_name == "arabicSignSanah":
        poly([(-156, 544), (-96, 656), (96, 656), (156, 544), (84, 600), (-84, 600)])
    elif glyph_name == "arabicFootnoteMarker":
        poly([(-168, 620), (-104, 684), (-24, 632), (56, 684), (168, 572), (104, 508), (24, 560), (-56, 508)])
    elif glyph_name == "arabicSignSafha":
        poly([(-156, 644), (0, 700), (156, 644), (100, 540), (0, 588), (-100, 540)])
    elif glyph_name == "dateSeparator-ar":
        poly([(112, 156), (188, 156), (220, 584), (144, 584)])
    elif glyph_name == "smallHighTah-ar":
        rect(-32, 560, 64, 160)
        rect(-96, 560, 192, 72 if bold else 56)
    elif glyph_name == "smallHighZain-ar":
        dot_size = 52 if bold else 40
        poly([(-96, 616), (-32, 680), (96, 680), (32, 616)])
        rect(-dot_size // 2, 712, dot_size, dot_size)
    elif glyph_name == "invertedDamma-ar":
        dot_size = 52 if bold else 40
        poly([(-96, 704), (-40, 640), (40, 640), (96, 704), (40, 680), (-40, 680)])
        rect(-dot_size // 2, 584, dot_size, dot_size)
    elif glyph_name == "noonGhunna-ar":
        dot = 52 if bold else 40
        poly([(-112, 592), (-56, 656), (56, 656), (112, 592), (68, 544), (0, 592), (-68, 544)])
        rect(-dot // 2, 704, dot, dot)
    elif glyph_name == "smallHighThreeDots-ar":
        dot = 52 if bold else 40
        for x, y in ((-56, 640), (56, 640), (0, 704)):
            rect(x - dot // 2, y - dot // 2, dot, dot)
    elif glyph_name == "comma-ar":
        poly([(116, 132), (188, 132), (148, -56), (76, -56)])
    elif glyph_name == "semicolon-ar":
        dot(center, 356, 56 if bold else 44)
        poly([(116, 132), (188, 132), (148, -56), (76, -56)])
    elif glyph_name == "question-ar":
        poly([(132, 488), (184, 552), (312, 552), (396, 484), (396, 388), (328, 320), (280, 284), (280, 216), (200, 216), (200, 328), (272, 380), (316, 424), (292, 472), (204, 472)])
        dot(240, 88, 60 if bold else 48)
    elif glyph_name == "asterisk-ar":
        rect(center - thin // 2, 232, thin, 352)
        rect(center - 176, 384 - thin // 2, 352, thin)
        poly([(center - 140, 244), (center - 88, 220), (center + 140, 524), (center + 88, 548)])
        poly([(center - 140, 524), (center - 88, 548), (center + 140, 244), (center + 88, 220)])
    elif glyph_name == "percent-ar":
        slash = thickness
        poly([(116, 160), (116 + slash, 160), (520, 584), (520 - slash, 584)])
        dot = 72 if bold else 56
        rect(128, 492, dot, dot)
        rect(420, 196, dot, dot)
    elif glyph_name == "decimalseparator-ar":
        dot(center, 120, 56 if bold else 44)
    elif glyph_name == "thousandseparator-ar":
        dot(center, 472, 56 if bold else 44)
    elif glyph_name == "zero-ar":
        dot(center, 384, 76 if bold else 56)
    elif glyph_name == "one-ar":
        rect(center - thin // 2, 176, thin, 408)
        poly([(center - thin // 2, 584), (center + thin // 2, 584), (center + 80, 496), (center + 28, 452), (center - 32, 528)])
    elif glyph_name == "two-ar":
        poly([(132, 500), (204, 584), (384, 584), (468, 508), (468, 416), (384, 340), (252, 312), (188, 260), (480, 260), (480, 176), (112, 176), (112, 260), (188, 340), (328, 372), (384, 424), (360, 492), (220, 492)])
    elif glyph_name == "three-ar":
        poly([(124, 500), (196, 584), (396, 584), (476, 512), (432, 424), (356, 396), (448, 356), (496, 276), (416, 176), (184, 176), (108, 260), (360, 260), (412, 304), (352, 356), (224, 356), (224, 432), (344, 432), (392, 492)])
    elif glyph_name == "four-ar":
        rect(388, 176, thin, 408)
        poly([(112, 340), (360, 584), (452, 584), (204, 340)])
        rect(112, 316, 408, thin)
    elif glyph_name == "five-ar":
        poly([(300, 584), (456, 584), (512, 496), (512, 320), (456, 232), (144, 232), (88, 320), (88, 496), (144, 584)])
        poly([(300, 500), (188, 500), (172, 472), (172, 344), (188, 316), (412, 316), (428, 344), (428, 472), (412, 500)])
    elif glyph_name == "six-ar":
        poly([(148, 584), (508, 584), (508, 500), (288, 176), (196, 176), (408, 500), (148, 500)])
    elif glyph_name == "seven-ar":
        poly([(420, 584), (500, 520), (328, 176), (236, 176), (380, 472), (148, 472), (100, 536), (168, 584)])
    elif glyph_name == "eight-ar":
        poly([(300, 584), (428, 584), (508, 504), (508, 396), (428, 316), (300, 316), (172, 316), (92, 396), (92, 504), (172, 584)])
        poly([(300, 500), (220, 500), (176, 452), (220, 400), (300, 400), (380, 400), (424, 452), (380, 500)])
    elif glyph_name == "nine-ar":
        poly([(176, 584), (404, 584), (492, 500), (492, 340), (416, 232), (220, 176), (140, 240), (312, 288), (396, 356), (396, 460), (356, 500), (216, 500)])
    elif glyph_name == "dotcenter-ar":
        dot(center, 356, 64 if bold else 48)
    elif glyph_name == "doublestroke-ar":
        rect(center - 72, 120, thin, 520)
        rect(center + 24, 120, thin, 520)
    elif glyph_name in {"gafsarkashabove-ar", "gafsarkashcenter-ar", "miniKeheh-ar"}:
        y = 572 if glyph_name == "gafsarkashabove-ar" else 420
        poly([(center - 156, y), (center + 156, y + 96), (center + 188, y + 20), (center - 124, y - 76)])
    elif glyph_name in {"twodotsverticalabove-ar", "twodotsverticalbelow-ar"}:
        y = 612 if glyph_name.endswith("above-ar") else -84
        dot(center, y, 56 if bold else 44)
        dot(center, y + 80, 56 if bold else 44)
    elif glyph_name == "twodotshorizontalbelow-ar":
        dot(center - 48, -84, 56 if bold else 44)
        dot(center + 48, -84, 56 if bold else 44)
    elif glyph_name in {"threedotsdownabove-ar", "threedotsdownbelow-ar", "threedotsdowncenter-ar", "threedotsupbelow-ar"}:
        y = 612 if "above" in glyph_name else -84
        if glyph_name == "threedotsupbelow-ar":
            dot(center - 56, y, 56 if bold else 44)
            dot(center + 56, y, 56 if bold else 44)
            dot(center, y + 72, 56 if bold else 44)
        else:
            dot(center - 56, y + 72, 56 if bold else 44)
            dot(center + 56, y + 72, 56 if bold else 44)
            dot(center, y, 56 if bold else 44)
    elif glyph_name == "wasla-ar":
        poly([(center - 120, 648), (center - 40, 704), (center + 60, 704), (center + 128, 632), (center + 80, 576), (center + 24, 632), (center - 48, 632), (center - 92, 600)])
    elif glyph_name == "hamza-ar":
        poly([(center - 120, 336), (center + 72, 336), (center + 88, 352), (center + 88, 400), (center + 72, 416), (center + 8, 416), (center - 24, 416), (center - 40, 432), (center - 40, 464), (center - 40, 496), (center - 12, 520), (center + 52, 520), (center + 108, 520), (center + 136, 488), (center + 136, 440), (center + 64, 440), (center + 64, 456), (center + 36, 456), (center + 20, 456), (center + 8, 444), (center + 8, 428), (center + 8, 412), (center + 20, 400), (center + 36, 400), (center + 104, 400), (center + 120, 384), (center + 120, 352), (center + 104, 336)])
    elif glyph_name.startswith("hamzaabove") or glyph_name.startswith("hamzabelow"):
        dot_y = 604 if "Damma" in glyph_name else 568
        if glyph_name.startswith("hamzabelow"):
            dot_y = -100
        poly([(center - 120, dot_y), (center + 72, dot_y), (center + 88, dot_y + 16), (center + 88, dot_y + 56), (center + 72, dot_y + 72), (center + 8, dot_y + 72), (center - 24, dot_y + 72), (center - 40, dot_y + 88), (center - 40, dot_y + 112), (center + 92, dot_y + 112), (center + 108, dot_y + 128), (center + 108, dot_y + 168), (center + 92, dot_y + 184), (center - 56, dot_y + 184), (center - 112, dot_y + 152), (center - 112, dot_y + 96), (center - 72, dot_y + 56), (center - 120, dot_y + 56)])
        if "Dammatan" in glyph_name or "Fathatan" in glyph_name or "Kasratan" in glyph_name:
            rect(center - 140, dot_y + 220, 208, thin // 2)
        elif "Damma" in glyph_name:
            dot(center + 148, dot_y + 92, 44 if bold else 34)
        elif "Fatha" in glyph_name:
            rect(center - 140, dot_y + 220, 208, thin // 2)
        elif "Kasra" in glyph_name:
            rect(center - 140, dot_y - 64, 208, thin // 2)
        elif "Sukun" in glyph_name:
            dot(center + 148, dot_y + 92, 44 if bold else 34)
    elif glyph_name.startswith("shadda"):
        y = 612
        poly([(center - 120, y), (center - 72, y), (center - 32, y + 112), (center + 8, y), (center + 56, y), (center + 8, y + 184), (center - 32, y + 184)])
        if "Alefabove" in glyph_name:
            rect(center + 88, y, thin, 220)
        elif "Damma" in glyph_name:
            dot(center + 132, y + 120, 44 if bold else 34)
        elif "Fatha" in glyph_name:
            rect(center + 72, y + 196, 180, thin // 2)
        elif "Kasra" in glyph_name:
            rect(center + 72, y - 60, 180, thin // 2)
    elif glyph_name in {"behDotless-ar", "behDotless-ar.fina", "fehDotless-ar", "fehDotless-ar.fina", "qafDotless-ar", "qafDotless-ar.fina"}:
        poly([(72, 192), (132, 112), (width - 140, 112), (width - 64, 192), (width - 64, 348), (width - 152, 260), (172, 260), (72, 348)])
    elif glyph_name in {"hah-ar", "hah-ar.fina"}:
        poly([(104, 176), (184, 112), (420, 112), (520, 204), (508, 336), (420, 420), (232, 420), (152, 352), (196, 292), (356, 292), (412, 248), (376, 216), (184, 216)])
    elif glyph_name == "hah-ar.medi":
        draw_join_stem()
        poly([(136, 168), (216, 128), (448, 128), (520, 196), (492, 292), (376, 336), (240, 316), (184, 252), (244, 212), (388, 220), (420, 196), (392, 176)])
    elif glyph_name == "reh-ar":
        poly([(176, 472), (264, 472), (392, 308), (372, 196), (292, 100), (144, 64), (88, 128), (220, 172), (292, 244)])
    elif glyph_name in {"sad-ar", "sad-ar.fina"}:
        poly([(88, 176), (156, 112), (512, 112), (600, 192), (600, 352), (512, 432), (396, 432), (316, 360), (252, 432), (152, 432), (88, 368), (132, 304), (220, 304), (284, 248), (376, 304), (492, 304), (520, 260), (480, 220), (176, 220)])
    elif glyph_name in {"sad-ar.init", "sad-ar.medi"}:
        draw_join_stem()
        poly([(64, 176), (172, 304), (300, 304), (360, 244), (452, 304), (548, 304), (604, 248), (552, 184), (408, 184), (348, 232), (288, 184)])
    elif glyph_name in {"tah-ar", "tah-ar.fina"}:
        rect(132, 160, thin, 420)
        poly([(104, 176), (188, 112), (492, 112), (572, 192), (536, 272), (252, 272), (188, 224)])
    elif glyph_name in {"tah-ar.init", "tah-ar.medi"}:
        draw_join_stem()
        rect(132, 168, thin, 412)
        poly([(104, 176), (208, 256), (476, 256), (540, 200), (504, 152), (224, 152)])
    elif glyph_name in {"kaf-ar", "kaf-ar.init", "kaf-ar.medi"}:
        if glyph_name.endswith((".init", ".medi")):
            draw_join_stem()
            poly([(88, 168), (356, 168), (356, 244), (224, 244), (324, 352), (396, 352), (396, 428), (288, 428), (116, 248)])
        else:
            poly([(112, 160), (568, 160), (568, 240), (268, 240), (392, 372), (540, 372), (540, 452), (348, 452), (184, 288), (112, 288)])
    elif glyph_name == "kashida-ar":
        rect(-24, 128, width + 48, thin)
    elif glyph_name == "lam-ar":
        poly([(376, 680), (464, 680), (464, 196), (392, 92), (224, 64), (104, 128), (168, 204), (292, 172), (376, 220)])
    elif glyph_name in {"meem-ar", "meem-ar.fina"}:
        poly([(264, 500), (420, 500), (496, 424), (496, 268), (420, 192), (264, 192), (188, 268), (188, 424)])
        poly([(264, 396), (264, 296), (348, 252), (432, 296), (432, 396), (348, 440)])
    elif glyph_name in {"meem-ar.init", "meem-ar.medi"}:
        draw_join_stem()
        poly([(104, 168), (220, 312), (344, 312), (424, 232), (372, 152), (228, 152), (160, 208)])
        poly([(252, 252), (324, 252), (344, 216), (292, 196), (240, 216)])
    elif glyph_name in {"heh-ar", "heh-ar.init"}:
        if glyph_name.endswith(".init"):
            draw_join_stem()
        poly([(148, 260), (244, 416), (388, 416), (480, 300), (428, 168), (260, 152)])
        poly([(268, 320), (340, 320), (372, 268), (324, 216), (252, 232)])
    elif glyph_name in {"noonghunna-ar", "noonghunna-ar.fina"}:
        poly([(88, 192), (132, 128), (452, 128), (520, 192), (520, 332), (440, 252), (176, 252), (88, 332)])
    elif glyph_name in {"alefMadda-ar", "alefMadda-ar.fina", "alefWasla-ar", "alefWasla-ar.fina"}:
        rect(center - thin // 2, 112, thin, 568)
        if "Madda" in glyph_name:
            poly([(center - 112, 760), (center - 24, 816), (center + 72, 776), (center + 128, 824), (center + 168, 760), (center + 72, 704), (center - 24, 744), (center - 80, 704)])
        else:
            poly([(center - 120, 760), (center - 40, 816), (center + 60, 816), (center + 128, 744), (center + 80, 688), (center + 24, 744), (center - 48, 744), (center - 92, 712)])
    elif glyph_name in {"alefMaksura-ar", "alefMaksura-ar.fina", "alefMaksura-ar.init", "alefMaksura-ar.medi", "wawHamzaabove-ar", "wawHamzaabove-ar.fina", "yehHamzaabove-ar", "yehHamzaabove-ar.fina", "yehHamzaabove-ar.init", "yehHamzaabove-ar.medi"}:
        if glyph_name.endswith((".init", ".medi")):
            draw_join_stem()
            poly([(96, 176), (176, 128), (416, 128), (496, 196), (456, 264), (208, 264)])
        else:
            poly([(92, 176), (172, 112), (468, 112), (548, 192), (508, 272), (212, 272)])
        if "Hamzaabove" in glyph_name:
            poly([(center - 80, 536), (center + 64, 536), (center + 80, 552), (center + 80, 584), (center + 64, 600), (center + 16, 600), (center - 8, 600), (center - 24, 616), (center - 24, 640), (center + 72, 640), (center + 88, 656), (center + 88, 688), (center + 72, 704), (center - 48, 704), (center - 96, 672), (center - 96, 624), (center - 56, 592), (center - 80, 592)])
    elif glyph_name.startswith("lam_alef"):
        rect(192, 112, thin, 568)
        rect(388, 112, thin, 568)
        poly([(192, 112), (388 + thin, 112), (388 + thin, 196), (192, 196)])
        if "Madda" in glyph_name:
            poly([(220, 760), (308, 816), (404, 776), (460, 824), (500, 760), (404, 704), (308, 744), (252, 704)])
        elif "Wasla" in glyph_name:
            poly([(220, 760), (300, 816), (400, 816), (468, 744), (420, 688), (364, 744), (292, 744), (248, 712)])
        elif "Hamza" in glyph_name:
            poly([(248, 736), (392, 736), (408, 752), (408, 784), (392, 800), (344, 800), (320, 800), (304, 816), (304, 840), (400, 840), (416, 856), (416, 888), (400, 904), (280, 904), (232, 872), (232, 824), (272, 792), (248, 792)])
    elif glyph_name == "ain-ar.fina":
        poly([(112, 180), (188, 112), (456, 112), (560, 204), (520, 300), (384, 336), (272, 320), (204, 260), (268, 220), (420, 224), (456, 200), (416, 172)])
    elif glyph_name == "alefHamzabelow-ar.fina":
        rect(center - thin // 2, 112, thin, 568)
        poly([(center - 104, -132), (center + 40, -132), (center + 56, -116), (center + 56, -84), (center + 40, -68), (center - 8, -68), (center - 32, -68), (center - 48, -52), (center - 48, -28), (center + 48, -28), (center + 64, -12), (center + 64, 20), (center + 48, 36), (center - 72, 36), (center - 120, 4), (center - 120, -44), (center - 80, -76), (center - 104, -76)])
    elif glyph_name == "seen-ar.medi":
        draw_join_stem()
        rect(112, 184, thin, 116)
        rect(244, 184, thin, 116)
        rect(376, 184, thin, 116)
    elif glyph_name == "waw-ar.fina":
        poly([(196, 496), (348, 496), (444, 400), (444, 260), (360, 152), (196, 112), (108, 172), (244, 220), (328, 276), (328, 372), (292, 408), (216, 408)])
    elif glyph_name in {"parenleft-ar", "parenright-ar"}:
        if glyph_name == "parenleft-ar":
            poly([(width - 72, -96), (width - 152, -96), (width - 252, 96), (width - 280, 352), (width - 244, 608), (width - 140, 800), (width - 60, 800), (width - 144, 604), (width - 176, 352), (width - 152, 100)])
        else:
            poly([(72, -96), (152, -96), (252, 96), (280, 352), (244, 608), (140, 800), (60, 800), (144, 604), (176, 352), (152, 100)])
    elif glyph_name == "ellipsis":
        dot(center - 144, 64, 64 if bold else 48)
        dot(center, 64, 64 if bold else 48)
        dot(center + 144, 64, 64 if bold else 48)
    elif glyph_name == "exclamdown":
        dot(center, 548, 64 if bold else 48)
        rect(center - thin // 2, 0, thin, 420)
    elif glyph_name == "questiondown":
        dot(center, 548, 60 if bold else 48)
        poly([(width - 132, 148), (width - 184, 84), (width - 312, 84), (width - 396, 152), (width - 396, 248), (width - 328, 316), (width - 280, 352), (width - 280, 420), (width - 200, 420), (width - 200, 308), (width - 272, 256), (width - 316, 212), (width - 292, 164), (width - 204, 164)])
    elif glyph_name == "periodcentered":
        dot(center, 356, 64 if bold else 48)
    elif glyph_name == "bullet":
        dot(center, 356, 116 if bold else 88)
    elif glyph_name == "numbersign":
        rect(152, 172, thin, 408)
        rect(360, 172, thin, 408)
        rect(84, 292, 432, thin)
        rect(84, 452, 432, thin)
    elif glyph_name == "backslash":
        poly([(116, 584), (116 + thickness, 584), (520, 0), (520 - thickness, 0)])
    elif glyph_name == "endash":
        rect(96, 328, width - 192, thin)
    elif glyph_name == "underscore":
        rect(64, -96, width - 128, thin)
    elif glyph_name == "quotesinglbase":
        poly([(center - 32, 112), (center + 40, 112), (center, -76), (center - 72, -76)])
    elif glyph_name == "quoteleft":
        poly([(center + 32, 760), (center - 40, 760), (center, 572), (center + 72, 572)])
    elif glyph_name == "quotedbl":
        rect(center - 92, 520, thin // 2, 220)
        rect(center + 68, 520, thin // 2, 220)
    elif glyph_name in {"beeh-ar", "beeh-ar.fina", "tteheh-ar", "tteheh-ar.fina", "tehRing-ar", "tehRing-ar.fina", "tehThreedotsdown-ar", "tehThreedotsdown-ar.fina"}:
        poly([(88, 192), (132, 128), (452, 128), (520, 192), (520, 332), (440, 252), (176, 252), (88, 332)])
        if glyph_name.startswith("beeh"):
            two_dots_vertical_below(center)
        elif glyph_name.startswith("tteheh"):
            two_dots_vertical_below(center, 548)
        elif glyph_name.startswith("tehRing"):
            ring_above(center)
        else:
            three_dots_above(center)
    elif glyph_name in {"beeh-ar.init", "beeh-ar.medi", "tteheh-ar.init", "tteheh-ar.medi", "tehRing-ar.init", "tehRing-ar.medi", "tehThreedotsdown-ar.init", "tehThreedotsdown-ar.medi"}:
        draw_join_stem()
        poly([(96, 176), (176, 128), (416, 128), (496, 196), (456, 264), (208, 264)])
        if glyph_name.startswith("beeh"):
            two_dots_vertical_below(center)
        elif glyph_name.startswith("tteheh"):
            two_dots_vertical_below(center, 548)
        elif glyph_name.startswith("tehRing"):
            ring_above(center)
        else:
            three_dots_above(center)
    elif glyph_name in {"peh-ar", "peh-ar.fina"}:
        poly([(88, 192), (132, 128), (452, 128), (520, 192), (520, 332), (440, 252), (176, 252), (88, 332)])
        three_dots_below(center)
    elif glyph_name in {"tcheh-ar", "tcheh-ar.fina"}:
        poly([(104, 176), (180, 128), (440, 128), (520, 204), (508, 336), (420, 420), (232, 420), (152, 352), (196, 292), (356, 292), (412, 248), (376, 216), (184, 216)])
        three_dots_below(center)
    elif glyph_name == "tcheh-ar.medi":
        draw_join_stem()
        poly([(136, 168), (216, 128), (448, 128), (520, 196), (492, 292), (376, 336), (240, 316), (184, 252), (244, 212), (388, 220), (420, 196), (392, 176)])
        three_dots_below(center)
    elif glyph_name == "rreh-ar":
        poly([(176, 472), (264, 472), (392, 308), (372, 196), (292, 100), (144, 64), (88, 128), (220, 172), (292, 244)])
        poly([(268, 584), (396, 640), (424, 584), (296, 528)])
    elif glyph_name == "jeh-ar":
        poly([(176, 472), (264, 472), (392, 308), (372, 196), (292, 100), (144, 64), (88, 128), (220, 172), (292, 244)])
        three_dots_above(304, 560)
    elif glyph_name in {"seenSixdots-ar", "seenSixdots-ar.fina"}:
        poly([(72, 176), (144, 112), (640, 112), (776, 196), (736, 276), (592, 220), (144, 220)])
        rect(132, 216, thin, 124)
        rect(264, 216, thin, 124)
        rect(396, 216, thin, 124)
        three_dots_above(360)
        three_dots_below(360)
    elif glyph_name in {"seenSixdots-ar.init", "seenSixdots-ar.medi"}:
        draw_join_stem()
        rect(112, 184, thin, 116)
        rect(244, 184, thin, 116)
        rect(376, 184, thin, 116)
        three_dots_above(300)
        three_dots_below(300)
    elif glyph_name in {"fehDotmovedbelow-ar", "fehDotmovedbelow-ar.fina", "fehThreedotsbelow-ar", "fehThreedotsbelow-ar.fina", "qafDotabove-ar", "qafDotabove-ar.fina", "qafThreedotsabove-ar", "qafThreedotsabove-ar.fina"}:
        poly([(72, 192), (132, 112), (width - 140, 112), (width - 64, 192), (width - 64, 348), (width - 152, 260), (172, 260), (72, 348)])
        if glyph_name.startswith("fehDotmovedbelow"):
            dot(center, -88)
        elif glyph_name.startswith("fehThreedotsbelow"):
            three_dots_below(center)
        elif glyph_name.startswith("qafDotabove"):
            dot(center, 548)
        else:
            three_dots_above(center)
    elif glyph_name in {"fehDotmovedbelow-ar.init", "fehDotmovedbelow-ar.medi", "fehThreedotsbelow-ar.init", "fehThreedotsbelow-ar.medi", "qafDotabove-ar.init", "qafDotabove-ar.medi", "qafThreedotsabove-ar.init", "qafThreedotsabove-ar.medi"}:
        draw_join_stem()
        poly([(104, 168), (224, 296), (388, 296), (468, 220), (420, 152), (232, 152), (164, 208)])
        if glyph_name.startswith("fehDotmovedbelow"):
            dot(center, -88)
        elif glyph_name.startswith("fehThreedotsbelow"):
            three_dots_below(center)
        elif glyph_name.startswith("qafDotabove"):
            dot(center, 548)
        else:
            three_dots_above(center)
    elif glyph_name == "keheh-ar":
        poly([(112, 160), (568, 160), (568, 240), (268, 240), (392, 372), (540, 372), (540, 452), (348, 452), (184, 288), (112, 288)])
    elif glyph_name in {"keheh-ar.init", "keheh-ar.medi"}:
        draw_join_stem()
        poly([(88, 168), (356, 168), (356, 244), (224, 244), (324, 352), (396, 352), (396, 428), (288, 428), (116, 248)])
    elif glyph_name == "gaf-ar":
        poly([(112, 160), (568, 160), (568, 240), (268, 240), (392, 372), (540, 372), (540, 452), (348, 452), (184, 288), (112, 288)])
        poly([(248, 544), (560, 640), (592, 564), (280, 468)])
    elif glyph_name in {"gaf-ar.init", "gaf-ar.medi"}:
        draw_join_stem()
        poly([(88, 168), (356, 168), (356, 244), (224, 244), (324, 352), (396, 352), (396, 428), (288, 428), (116, 248)])
        poly([(144, 520), (392, 604), (420, 532), (172, 448)])
    elif glyph_name == "hehDoachashmee-ar":
        poly([(264, 500), (420, 500), (496, 424), (496, 268), (420, 192), (264, 192), (188, 268), (188, 424)])
        poly([(264, 396), (264, 296), (348, 252), (432, 296), (432, 396), (348, 440)])
    elif glyph_name == "hehDoachashmee-ar.init":
        draw_join_stem()
        poly([(104, 168), (220, 312), (344, 312), (424, 232), (372, 152), (228, 152), (160, 208)])
        poly([(252, 252), (324, 252), (344, 216), (292, 196), (240, 216)])
    elif glyph_name == "hehGoal-ar":
        poly([(104, 176), (176, 112), (360, 112), (464, 196), (464, 328), (392, 408), (272, 408), (208, 344), (236, 288), (344, 288), (376, 236), (332, 192), (184, 192)])
    elif glyph_name == "hehGoal-ar.init":
        draw_join_stem()
        poly([(88, 168), (196, 320), (336, 320), (416, 248), (388, 172), (236, 172), (168, 220)])
    elif glyph_name in {"hehGoalHamzaabove-ar", "hehGoalHamzaabove-ar.fina"}:
        poly([(104, 176), (176, 112), (360, 112), (464, 196), (464, 328), (392, 408), (272, 408), (208, 344), (236, 288), (344, 288), (376, 236), (332, 192), (184, 192)])
        hamza_above(center)
    elif glyph_name in {"hehGoalHamzaabove-ar.init", "hehGoalHamzaabove-ar.medi"}:
        draw_join_stem()
        poly([(88, 168), (196, 320), (336, 320), (416, 248), (388, 172), (236, 172), (168, 220)])
        hamza_above(center)
    elif glyph_name in {"tehMarbutaGoal-ar", "tehMarbutaGoal-ar.fina"}:
        poly([(104, 176), (176, 112), (360, 112), (464, 196), (464, 328), (392, 408), (272, 408), (208, 344), (236, 288), (344, 288), (376, 236), (332, 192), (184, 192)])
        two_dots_below(center, 548)
    elif glyph_name in {"yehBarree-ar", "yehBarree-ar.fina"}:
        poly([(132, 276), (212, 216), (500, 216), (652, 112), (600, 32), (384, 80), (196, 112), (84, 200)])
        poly([(500, 216), (672, 216), (720, 288), (664, 356), (528, 320)])
    elif glyph_name in {"kehehThreedotsabove-ar", "kehehThreedotsabove-ar.fina"}:
        poly([(112, 160), (568, 160), (568, 240), (268, 240), (392, 372), (540, 372), (540, 452), (348, 452), (184, 288), (112, 288)])
        three_dots_above(412)
    elif glyph_name in {"kehehThreedotsabove-ar.init", "kehehThreedotsabove-ar.medi"}:
        draw_join_stem()
        poly([(88, 168), (356, 168), (356, 244), (224, 244), (324, 352), (396, 352), (396, 428), (288, 428), (116, 248)])
        three_dots_above(288)
    elif glyph_name == "Euro":
        rect(100, 388, 312, thin)
        rect(100, 292, 280, thin)
        poly([(520, 552), (568, 488), (444, 488), (344, 488), (252, 420), (252, 304), (344, 236), (444, 236), (568, 236), (520, 172), (328, 172), (164, 292), (164, 432), (328, 552)])
    elif glyph_name == "trademark":
        rect(64, 528, 224, thin)
        rect(144 - thin // 2, 316, thin, 212)
        rect(352, 316, thin, 268)
        rect(592, 316, thin, 268)
        poly([(352, 584), (416, 584), (472, 440), (528, 584), (592, 584), (500, 316), (444, 316)])
    elif glyph_name == "zeroFarsi-ar":
        poly([(300, 520), (404, 520), (480, 444), (480, 340), (404, 264), (300, 264), (196, 264), (120, 340), (120, 444), (196, 520)])
        poly([(300, 444), (356, 444), (404, 396), (356, 340), (300, 340), (244, 340), (196, 396), (244, 444)])
    elif glyph_name == "oneFarsi-ar":
        rect(292 - thin // 2, 176, thin, 408)
        poly([(292 - thin // 2, 584), (292 + thin // 2, 584), (364, 492), (312, 448), (252, 524)])
    elif glyph_name == "twoFarsi-ar":
        poly([(156, 232), (444, 232), (500, 288), (476, 356), (340, 356), (256, 400), (300, 472), (440, 472), (496, 528), (440, 584), (240, 584), (168, 512), (188, 444), (276, 356), (156, 356), (100, 300)])
    elif glyph_name == "threeFarsi-ar":
        poly([(116, 232), (420, 232), (500, 300), (452, 380), (352, 380), (444, 452), (396, 532), (144, 532), (96, 468), (316, 468), (228, 396), (276, 320), (452, 320), (416, 296), (116, 296)])
    elif glyph_name == "fourFarsi-ar":
        poly([(116, 520), (184, 584), (432, 584), (500, 516), (500, 456), (428, 408), (500, 352), (500, 292), (432, 232), (184, 232), (116, 296), (356, 296), (416, 352), (340, 408), (416, 464), (356, 520)])
    elif glyph_name == "fiveFarsi-ar":
        poly([(300, 584), (456, 584), (512, 496), (512, 320), (456, 232), (144, 232), (88, 320), (88, 496), (144, 584)])
        poly([(300, 500), (188, 500), (172, 472), (172, 344), (188, 316), (412, 316), (428, 344), (428, 472), (412, 500)])
    elif glyph_name == "sixFarsi-ar":
        poly([(392, 584), (484, 584), (520, 520), (324, 232), (232, 232), (196, 296)])
        dot = 56 if bold else 44
        rect(152, 232, dot, dot)
    elif glyph_name == "sevenFarsi-ar":
        poly([(92, 584), (508, 584), (508, 500), (284, 232), (188, 232), (396, 500), (92, 500)])
    elif glyph_name == "eightFarsi-ar":
        poly([(92, 232), (508, 232), (508, 316), (284, 584), (188, 584), (396, 316), (92, 316)])
    elif glyph_name == "nineFarsi-ar":
        poly([(224, 584), (376, 584), (452, 508), (452, 428), (408, 372), (500, 232), (404, 232), (320, 352), (224, 352), (148, 428), (148, 508)])
        poly([(300, 512), (244, 512), (220, 484), (244, 424), (300, 424), (356, 424), (380, 484), (356, 512)])
    else:
        return None
    return serialize_xml(glyph)


def has_outline(source_path: Path) -> bool:
    root = ET.fromstring(source_path.read_bytes())
    outline = root.find("outline")
    if outline is None:
        return False
    return bool(outline.findall("contour") or outline.findall("component"))


def copy_candidate_glif(source_path: Path, glyph_name: str, codepoint: int | None) -> bytes:
    root = ET.fromstring(source_path.read_bytes())
    root.set("name", glyph_name)
    for unicode_node in list(root.findall("unicode")):
        root.remove(unicode_node)
    if codepoint is not None:
        root.insert(0, ET.Element("unicode", {"hex": f"{codepoint:04X}"}))
    return serialize_xml(root)


def serialize_xml(root: ET.Element) -> bytes:
    ET.indent(root, space="\t")
    xml = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml}\n'.encode()


def plan_item(item: WorkItem, ufo_path: Path, contents: dict[str, str], refresh_empty: bool) -> tuple[str, str | None]:
    if item.glyph_name in contents:
        glyph_path = ufo_path / "glyphs" / contents[item.glyph_name]
        if refresh_empty and item.glyph_name in GEOMETRIC_GLYPHS and not has_outline(glyph_path):
            return "refresh-geometric", None
        return "exists", None
    if item.glyph_name in GEOMETRIC_GLYPHS:
        return "create-geometric", None
    base_name = base_for(item.glyph_name)
    if base_name and base_name in contents:
        return "copy-base", base_name
    return "empty-review", None


def write_item(item: WorkItem, ufo_path: Path, contents: dict[str, str], action: str, base_name: str | None) -> None:
    glyphs_dir = ufo_path / "glyphs"
    filename = contents.get(item.glyph_name) or filename_for(item.glyph_name, contents)
    target_path = glyphs_dir / filename
    if action in {"create-geometric", "refresh-geometric"}:
        width = ADVANCE_WIDTHS.get(item.glyph_name, ADVANCE_WIDTHS["default"])
        if action == "refresh-geometric" and target_path.exists():
            root = ET.fromstring(target_path.read_bytes())
            advance = root.find("advance")
            if advance is not None and advance.attrib.get("width"):
                width = int(float(advance.attrib["width"]))
        is_bold = "Bold" in ufo_path.name
        data = create_geometric_glif(item.glyph_name, item.codepoint, width, is_bold)
        if data is None:
            raise ValueError(f"no geometric builder for {item.glyph_name}")
        target_path.write_bytes(data)
    elif action == "copy-base" and base_name:
        source_path = glyphs_dir / contents[base_name]
        target_path.write_bytes(copy_candidate_glif(source_path, item.glyph_name, item.codepoint))
    else:
        width = ADVANCE_WIDTHS.get(item.glyph_name, ADVANCE_WIDTHS["default"])
        target_path.write_bytes(create_empty_glif(item.glyph_name, item.codepoint, width))
    contents[item.glyph_name] = filename


def report(items: list[WorkItem], write: bool, refresh_empty: bool) -> tuple[str, int]:
    lines = [
        "# Arabic Candidate Glyph Plan",
        "",
        f"- Mode: {'write' if write else 'dry-run'}",
        f"- Worklist glyphs: {len(items)}",
        f"- UFO masters: {', '.join(path.relative_to(ROOT).as_posix() for path in UFO_PATHS)}",
        "",
    ]
    totals = {"exists": 0, "copy-base": 0, "empty-review": 0, "create-geometric": 0, "refresh-geometric": 0}
    auto_created: set[str] = set()
    review_needed: set[str] = set()
    hand_draw_needed: set[str] = set()
    compatibility_risks: set[str] = set()
    contents_by_ufo = {ufo_path: read_contents(ufo_path) for ufo_path in UFO_PATHS}

    by_batch: dict[str, list[WorkItem]] = {}
    for item in items:
        by_batch.setdefault(item.batch, []).append(item)

    for batch in sorted(by_batch):
        lines.extend([f"## {batch}", "", "| Glyph | Unicode | Regular action | Bold action | Notes |", "| --- | --- | --- | --- | --- |"])
        for item in by_batch[batch]:
            row_actions: list[str] = []
            notes: list[str] = []
            planned_actions: list[tuple[Path, str, str | None]] = []
            for ufo_path in UFO_PATHS:
                action, base_name = plan_item(item, ufo_path, contents_by_ufo[ufo_path], refresh_empty)
                planned_actions.append((ufo_path, action, base_name))
                totals[action] += 1
                if action == "copy-base":
                    row_actions.append(f"copy `{base_name}`")
                    notes.append("base candidate needs drawing/dot review")
                elif action == "create-geometric":
                    row_actions.append("create geometric candidate")
                    notes.append("deterministic geometric outline needs proof review")
                elif action == "refresh-geometric":
                    row_actions.append("refresh geometric candidate")
                    notes.append("empty placeholder replaced with deterministic outline")
                elif action == "empty-review":
                    row_actions.append("create empty review glyph")
                    notes.append("hand drawing required")
                else:
                    row_actions.append("exists")
            if row_actions[0] != row_actions[1]:
                compatibility_risks.add(item.glyph_name)
            glyph_actions = {action for _, action, _ in planned_actions}
            if glyph_actions - {"exists", "empty-review"}:
                auto_created.add(item.glyph_name)
            if "empty-review" in glyph_actions:
                hand_draw_needed.add(item.glyph_name)
            review_needed.add(item.glyph_name)
            if write:
                for ufo_path, action, base_name in planned_actions:
                    if action != "exists":
                        write_item(item, ufo_path, contents_by_ufo[ufo_path], action, base_name)
            codepoint = "" if item.codepoint is None else f"U+{item.codepoint:04X}"
            note = "; ".join(sorted(set(notes))) or "already present"
            lines.append(f"| `{item.glyph_name}` | {codepoint} | {row_actions[0]} | {row_actions[1]} | {note} |")
        lines.append("")

    if write:
        for ufo_path, contents in contents_by_ufo.items():
            write_contents(ufo_path, contents)

    lines.extend(
        [
            "## Summary",
            "",
            "Glyph-level buckets:",
            "",
            f"- Auto-created / would auto-create: {len(auto_created)}",
            f"- Review-needed: {len(review_needed)}",
            f"- Hand-draw-needed: {len(hand_draw_needed)}",
            f"- Compatibility-risk: {len(compatibility_risks)}",
            "",
            "Master-entry action counts:",
            "",
            f"- Existing master entries counted: {totals['exists']}",
            f"- Base-copy candidate entries counted: {totals['copy-base']}",
            f"- Geometric candidate entries counted: {totals['create-geometric']}",
            f"- Refreshed empty geometric entries counted: {totals['refresh-geometric']}",
            f"- Empty hand-review candidate entries counted: {totals['empty-review']}",
            f"- Compatibility-risk glyphs: {len(compatibility_risks)}",
            "",
            "Next commands:",
            "",
            "```bash",
            "make reports-only",
            "make preflight-only",
            "```",
        ]
    )
    return "\n".join(lines) + "\n", len(compatibility_risks)


def backup_sources() -> None:
    for ufo_path in UFO_PATHS:
        backup = ufo_path.with_name(f"{ufo_path.name}.arabic-candidate-backup")
        if backup.exists():
            shutil.rmtree(backup)
        shutil.copytree(ufo_path, backup)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="show the creation plan without editing sources")
    parser.add_argument("--write", action="store_true", help="create candidate glyphs in both UFO masters")
    parser.add_argument("--refresh-empty", action="store_true", help="replace existing empty managed candidates when deterministic outlines are available")
    parser.add_argument("--backup", action="store_true", help="backup UFOs before write mode")
    parser.add_argument("--output", type=Path, help="write the plan/report to this markdown file")
    args = parser.parse_args(argv)

    if args.dry_run and args.write:
        raise SystemExit("--dry-run and --write cannot be used together")
    if not CHECKLIST.exists():
        raise SystemExit(f"missing checklist: {CHECKLIST.relative_to(ROOT)}")
    if args.backup and not args.write:
        raise SystemExit("--backup only makes sense with --write")
    if args.write and args.backup:
        backup_sources()

    items = parse_worklist()
    text, risks = report(items, write=args.write, refresh_empty=args.refresh_empty)
    if args.output:
        args.output.write_text(text)
    else:
        sys.stdout.write(text)
    return 1 if risks else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
