#!/usr/bin/env python3
"""Create conservative GF Latin Core composite candidates in both UFO masters.

Dry-run is the default. Write mode only creates component-based glyphs from
existing Virtua bases and accent helpers, so the result is a reviewable
coverage candidate rather than final drawing approval.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
UFO_PATHS = (
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
)


@dataclass(frozen=True)
class Candidate:
    glyph_name: str
    codepoint: int
    base_name: str
    accent_name: str
    case: str


@dataclass(frozen=True)
class Helper:
    glyph_name: str
    codepoint: int | None
    width: int
    contours: tuple[tuple[tuple[int, int], ...], ...] = ()
    component_base: str | None = None


@dataclass(frozen=True)
class Component:
    base_name: str
    x_offset: int = 0
    y_offset: int = 0
    x_scale: float | None = None
    y_scale: float | None = None


@dataclass(frozen=True)
class ComponentCandidate:
    glyph_name: str
    codepoint: int
    width: int
    components: tuple[Component, ...]


COMBINING_MARKS = {
    "gravecomb": (0x0300, "grave"),
    "acutecomb": (0x0301, "acute"),
    "circumflexcomb": (0x0302, "circumflex"),
    "tildecomb": (0x0303, "tilde"),
    "macroncomb": (0x0304, "macron"),
    "brevecomb": (0x0306, "breve"),
    "dotaccentcomb": (0x0307, "dotaccent"),
    "dieresiscomb": (0x0308, "dieresis"),
    "ringcomb": (0x030A, "ring"),
    "hungarumlautcomb": (0x030B, "hungarumlaut"),
    "caroncomb": (0x030C, "caron"),
    "commaaccentcomb": (0x0326, "commaaccent"),
    "cedillacomb": (0x0327, "cedilla"),
    "ogonekcomb": (0x0328, "ogonek"),
}

COMBINING_ANCHORS = {
    "acutecomb": (150, 638, "_top"),
}


HELPERS = [
    Helper(
        "circumflex",
        0x02C6,
        420,
        (((72, 520), (136, 440), (212, 608), (288, 440), (352, 520), (244, 744), (180, 744)),),
    ),
    Helper(
        "tilde",
        0x02DC,
        520,
        (((72, 392), (184, 460), (296, 380), (408, 448), (408, 536), (296, 468), (184, 548), (72, 480)),),
    ),
    Helper("macron", 0x00AF, 360, (((48, 676), (312, 676), (312, 724), (48, 724)),)),
    Helper(
        "breve",
        0x02D8,
        360,
        (
            (
                (48, 760),
                (112, 760),
                (136, 704),
                (180, 688),
                (224, 704),
                (248, 760),
                (312, 760),
                (284, 652),
                (212, 608),
                (148, 608),
                (76, 652),
            ),
        ),
    ),
    Helper("dotaccent", 0x02D9, 240, (((80, 640), (160, 640), (160, 720), (80, 720)),)),
    Helper(
        "dieresis",
        0x00A8,
        360,
        (
            ((56, 640), (136, 640), (136, 720), (56, 720)),
            ((224, 640), (304, 640), (304, 720), (224, 720)),
        ),
    ),
    Helper(
        "ring",
        0x02DA,
        300,
        (
            ((72, 632), (228, 632), (228, 788), (72, 788)),
            ((120, 680), (180, 680), (180, 740), (120, 740)),
        ),
    ),
    Helper(
        "caron",
        0x02C7,
        420,
        (((72, 728), (136, 808), (212, 640), (288, 808), (352, 728), (244, 504), (180, 504)),),
    ),
    Helper("caron.alt", None, 260, (((92, 520), (156, 520), (196, 744), (196, 800), (132, 800), (132, 744)),)),
    Helper(
        "hungarumlaut",
        0x02DD,
        440,
        (
            ((72, 638), (116, 638), (132, 654), (224, 800), (224, 816), (208, 832), (124, 832), (108, 816), (56, 670), (56, 654)),
            ((248, 638), (292, 638), (308, 654), (400, 800), (400, 816), (384, 832), (300, 832), (284, 816), (232, 670), (232, 654)),
        ),
    ),
    Helper(
        "cedilla",
        0x00B8,
        260,
        (((72, -168), (152, -168), (196, -92), (176, -16), (128, 0), (96, -40), (124, -48), (140, -84), (116, -120), (72, -120)),),
    ),
    Helper(
        "ogonek",
        0x02DB,
        260,
        (((176, -168), (96, -168), (60, -124), (68, -72), (132, 0), (180, 0), (132, -72), (128, -108), (176, -120)),),
    ),
    Helper("commaaccent", None, 260, (((92, -192), (156, -192), (188, -72), (172, -40), (108, -40), (124, -72)),)),
]


ACCENTED_CANDIDATES = [
    Candidate("Agrave", 0x00C0, "A", "grave", "upper"),
    Candidate("Egrave", 0x00C8, "E", "grave", "upper"),
    Candidate("Igrave", 0x00CC, "I", "grave", "upper"),
    Candidate("Ograve", 0x00D2, "O", "grave", "upper"),
    Candidate("Ugrave", 0x00D9, "U", "grave", "upper"),
    Candidate("Wgrave", 0x1E80, "W", "grave", "upper"),
    Candidate("Ygrave", 0x1EF2, "Y", "grave", "upper"),
    Candidate("agrave", 0x00E0, "a", "grave", "lower"),
    Candidate("egrave", 0x00E8, "e", "grave", "lower"),
    Candidate("igrave", 0x00EC, "dotlessi", "grave", "lower"),
    Candidate("ograve", 0x00F2, "o", "grave", "lower"),
    Candidate("ugrave", 0x00F9, "u", "grave", "lower"),
    Candidate("wgrave", 0x1E81, "w", "grave", "lower"),
    Candidate("ygrave", 0x1EF3, "y", "grave", "lower"),
    Candidate("Cacute", 0x0106, "C", "acute", "upper"),
    Candidate("Eacute", 0x00C9, "E", "acute", "upper"),
    Candidate("Iacute", 0x00CD, "I", "acute", "upper"),
    Candidate("Lacute", 0x0139, "L", "acute", "upper"),
    Candidate("Nacute", 0x0143, "N", "acute", "upper"),
    Candidate("Oacute", 0x00D3, "O", "acute", "upper"),
    Candidate("Racute", 0x0154, "R", "acute", "upper"),
    Candidate("Sacute", 0x015A, "S", "acute", "upper"),
    Candidate("Uacute", 0x00DA, "U", "acute", "upper"),
    Candidate("Wacute", 0x1E82, "W", "acute", "upper"),
    Candidate("Yacute", 0x00DD, "Y", "acute", "upper"),
    Candidate("Zacute", 0x0179, "Z", "acute", "upper"),
    Candidate("cacute", 0x0107, "c", "acute", "lower"),
    Candidate("eacute", 0x00E9, "e", "acute", "lower"),
    Candidate("iacute", 0x00ED, "dotlessi", "acute", "lower"),
    Candidate("lacute", 0x013A, "l", "acute", "lower"),
    Candidate("nacute", 0x0144, "n", "acute", "lower"),
    Candidate("oacute", 0x00F3, "o", "acute", "lower"),
    Candidate("racute", 0x0155, "r", "acute", "lower"),
    Candidate("sacute", 0x015B, "s", "acute", "lower"),
    Candidate("uacute", 0x00FA, "u", "acute", "lower"),
    Candidate("wacute", 0x1E83, "w", "acute", "lower"),
    Candidate("yacute", 0x00FD, "y", "acute", "lower"),
    Candidate("zacute", 0x017A, "z", "acute", "lower"),
    Candidate("Acircumflex", 0x00C2, "A", "circumflex", "upper"),
    Candidate("Ecircumflex", 0x00CA, "E", "circumflex", "upper"),
    Candidate("Icircumflex", 0x00CE, "I", "circumflex", "upper"),
    Candidate("Ocircumflex", 0x00D4, "O", "circumflex", "upper"),
    Candidate("Ucircumflex", 0x00DB, "U", "circumflex", "upper"),
    Candidate("Wcircumflex", 0x0174, "W", "circumflex", "upper"),
    Candidate("Ycircumflex", 0x0176, "Y", "circumflex", "upper"),
    Candidate("acircumflex", 0x00E2, "a", "circumflex", "lower"),
    Candidate("ecircumflex", 0x00EA, "e", "circumflex", "lower"),
    Candidate("icircumflex", 0x00EE, "dotlessi", "circumflex", "lower"),
    Candidate("ocircumflex", 0x00F4, "o", "circumflex", "lower"),
    Candidate("ucircumflex", 0x00FB, "u", "circumflex", "lower"),
    Candidate("wcircumflex", 0x0175, "w", "circumflex", "lower"),
    Candidate("ycircumflex", 0x0177, "y", "circumflex", "lower"),
    Candidate("Atilde", 0x00C3, "A", "tilde", "upper"),
    Candidate("Ntilde", 0x00D1, "N", "tilde", "upper"),
    Candidate("Otilde", 0x00D5, "O", "tilde", "upper"),
    Candidate("atilde", 0x00E3, "a", "tilde", "lower"),
    Candidate("ntilde", 0x00F1, "n", "tilde", "lower"),
    Candidate("otilde", 0x00F5, "o", "tilde", "lower"),
    Candidate("Adieresis", 0x00C4, "A", "dieresis", "upper"),
    Candidate("Edieresis", 0x00CB, "E", "dieresis", "upper"),
    Candidate("Idieresis", 0x00CF, "I", "dieresis", "upper"),
    Candidate("Odieresis", 0x00D6, "O", "dieresis", "upper"),
    Candidate("Udieresis", 0x00DC, "U", "dieresis", "upper"),
    Candidate("Wdieresis", 0x1E84, "W", "dieresis", "upper"),
    Candidate("Ydieresis", 0x0178, "Y", "dieresis", "upper"),
    Candidate("adieresis", 0x00E4, "a", "dieresis", "lower"),
    Candidate("edieresis", 0x00EB, "e", "dieresis", "lower"),
    Candidate("idieresis", 0x00EF, "dotlessi", "dieresis", "lower"),
    Candidate("odieresis", 0x00F6, "o", "dieresis", "lower"),
    Candidate("udieresis", 0x00FC, "u", "dieresis", "lower"),
    Candidate("wdieresis", 0x1E85, "w", "dieresis", "lower"),
    Candidate("ydieresis", 0x00FF, "y", "dieresis", "lower"),
    Candidate("Amacron", 0x0100, "A", "macron", "upper"),
    Candidate("Emacron", 0x0112, "E", "macron", "upper"),
    Candidate("Imacron", 0x012A, "I", "macron", "upper"),
    Candidate("Umacron", 0x016A, "U", "macron", "upper"),
    Candidate("amacron", 0x0101, "a", "macron", "lower"),
    Candidate("emacron", 0x0113, "e", "macron", "lower"),
    Candidate("imacron", 0x012B, "dotlessi", "macron", "lower"),
    Candidate("umacron", 0x016B, "u", "macron", "lower"),
    Candidate("Abreve", 0x0102, "A", "breve", "upper"),
    Candidate("Gbreve", 0x011E, "G", "breve", "upper"),
    Candidate("abreve", 0x0103, "a", "breve", "lower"),
    Candidate("gbreve", 0x011F, "g", "breve", "lower"),
    Candidate("Aring", 0x00C5, "A", "ring", "upper"),
    Candidate("Uring", 0x016E, "U", "ring", "upper"),
    Candidate("aring", 0x00E5, "a", "ring", "lower"),
    Candidate("uring", 0x016F, "u", "ring", "lower"),
    Candidate("Cdotaccent", 0x010A, "C", "dotaccent", "upper"),
    Candidate("Edotaccent", 0x0116, "E", "dotaccent", "upper"),
    Candidate("Gdotaccent", 0x0120, "G", "dotaccent", "upper"),
    Candidate("Idotaccent", 0x0130, "I", "dotaccent", "upper"),
    Candidate("Zdotaccent", 0x017B, "Z", "dotaccent", "upper"),
    Candidate("cdotaccent", 0x010B, "c", "dotaccent", "lower"),
    Candidate("edotaccent", 0x0117, "e", "dotaccent", "lower"),
    Candidate("gdotaccent", 0x0121, "g", "dotaccent", "lower"),
    Candidate("zdotaccent", 0x017C, "z", "dotaccent", "lower"),
    Candidate("Aogonek", 0x0104, "A", "ogonek", "upper"),
    Candidate("Eogonek", 0x0118, "E", "ogonek", "upper"),
    Candidate("Iogonek", 0x012E, "I", "ogonek", "upper"),
    Candidate("Uogonek", 0x0172, "U", "ogonek", "upper"),
    Candidate("aogonek", 0x0105, "a", "ogonek", "lower"),
    Candidate("eogonek", 0x0119, "e", "ogonek", "lower"),
    Candidate("iogonek", 0x012F, "dotlessi", "ogonek", "lower"),
    Candidate("uogonek", 0x0173, "u", "ogonek", "lower"),
    Candidate("Ccedilla", 0x00C7, "C", "cedilla", "upper"),
    Candidate("Gcedilla", 0x0122, "G", "cedilla", "upper"),
    Candidate("Kcedilla", 0x0136, "K", "cedilla", "upper"),
    Candidate("Lcedilla", 0x013B, "L", "cedilla", "upper"),
    Candidate("Ncedilla", 0x0145, "N", "cedilla", "upper"),
    Candidate("Scedilla", 0x015E, "S", "cedilla", "upper"),
    Candidate("ccedilla", 0x00E7, "c", "cedilla", "lower"),
    Candidate("gcedilla", 0x0123, "g", "cedilla", "lower"),
    Candidate("kcedilla", 0x0137, "k", "cedilla", "lower"),
    Candidate("lcedilla", 0x013C, "l", "cedilla", "lower"),
    Candidate("ncedilla", 0x0146, "n", "cedilla", "lower"),
    Candidate("scedilla", 0x015F, "s", "cedilla", "lower"),
    Candidate("Ccaron", 0x010C, "C", "caron", "upper"),
    Candidate("Dcaron", 0x010E, "D", "caron", "upper"),
    Candidate("Ecaron", 0x011A, "E", "caron", "upper"),
    Candidate("Lcaron", 0x013D, "L", "caron.alt", "upper"),
    Candidate("Ncaron", 0x0147, "N", "caron", "upper"),
    Candidate("Rcaron", 0x0158, "R", "caron", "upper"),
    Candidate("Scaron", 0x0160, "S", "caron", "upper"),
    Candidate("Tcaron", 0x0164, "T", "caron.alt", "upper"),
    Candidate("Zcaron", 0x017D, "Z", "caron", "upper"),
    Candidate("ccaron", 0x010D, "c", "caron", "lower"),
    Candidate("dcaron", 0x010F, "d", "caron.alt", "lower"),
    Candidate("ecaron", 0x011B, "e", "caron", "lower"),
    Candidate("lcaron", 0x013E, "l", "caron.alt", "lower"),
    Candidate("ncaron", 0x0148, "n", "caron", "lower"),
    Candidate("rcaron", 0x0159, "r", "caron", "lower"),
    Candidate("scaron", 0x0161, "s", "caron", "lower"),
    Candidate("tcaron", 0x0165, "t", "caron.alt", "lower"),
    Candidate("zcaron", 0x017E, "z", "caron", "lower"),
    Candidate("Ohungarumlaut", 0x0150, "O", "hungarumlaut", "upper"),
    Candidate("Uhungarumlaut", 0x0170, "U", "hungarumlaut", "upper"),
    Candidate("ohungarumlaut", 0x0151, "o", "hungarumlaut", "lower"),
    Candidate("uhungarumlaut", 0x0171, "u", "hungarumlaut", "lower"),
    Candidate("Scommaaccent", 0x0218, "S", "commaaccent", "upper"),
    Candidate("Tcommaaccent", 0x021A, "T", "commaaccent", "upper"),
    Candidate("scommaaccent", 0x0219, "s", "commaaccent", "lower"),
    Candidate("tcommaaccent", 0x021B, "t", "commaaccent", "lower"),
]


COMPONENT_CANDIDATES = [
    ComponentCandidate("section", 0x00A7, 560, (Component("S", 0, 80), Component("S", 0, -160))),
    ComponentCandidate("ordfeminine", 0x00AA, 600, (Component("a", 0, 208),)),
    ComponentCandidate("paragraph", 0x00B6, 640, (Component("P", 0, 0), Component("bar", 408, 0))),
    ComponentCandidate("ordmasculine", 0x00BA, 600, (Component("o", 0, 208),)),
    ComponentCandidate("AE", 0x00C6, 880, (Component("A", 0, 0), Component("E", 360, 0))),
    ComponentCandidate("Eth", 0x00D0, 680, (Component("D", 0, 0), Component("hyphen", 0, 300))),
    ComponentCandidate("Oslash", 0x00D8, 704, (Component("O", 0, 0), Component("slash", 0, 0))),
    ComponentCandidate("Thorn", 0x00DE, 640, (Component("P", 0, 0), Component("I", 0, 0))),
    ComponentCandidate("germandbls", 0x00DF, 600, (Component("B", 0, -128),)),
    ComponentCandidate("ae", 0x00E6, 864, (Component("a", 0, 0), Component("e", 304, 0))),
    ComponentCandidate("eth", 0x00F0, 576, (Component("o", 0, 0), Component("hyphen", 48, 344), Component("slash", 0, 0))),
    ComponentCandidate("oslash", 0x00F8, 576, (Component("o", 0, 0), Component("slash", 0, 0))),
    ComponentCandidate("thorn", 0x00FE, 576, (Component("p", 0, 0),)),
    ComponentCandidate("Dcroat", 0x0110, 680, (Component("D", 0, 0), Component("hyphen", 0, 300))),
    ComponentCandidate("dcroat", 0x0111, 576, (Component("d", 0, 0), Component("hyphen", 0, 360))),
    ComponentCandidate("Hbar", 0x0126, 704, (Component("H", 0, 0), Component("hyphen", 64, 348))),
    ComponentCandidate("hbar", 0x0127, 576, (Component("h", 0, 0), Component("hyphen", 0, 360))),
    ComponentCandidate("Lslash", 0x0141, 608, (Component("L", 0, 0), Component("slash", -80, -48))),
    ComponentCandidate("lslash", 0x0142, 608, (Component("l", 0, 0), Component("slash", -80, -48))),
    ComponentCandidate("OE", 0x0152, 928, (Component("O", 0, 0), Component("E", 432, 0))),
    ComponentCandidate("oe", 0x0153, 864, (Component("o", 0, 0), Component("e", 304, 0))),
    ComponentCandidate("Germandbls", 0x1E9E, 640, (Component("B", 0, 0),)),
    ComponentCandidate("quotedblbase", 0x201E, 360, (Component("comma", 24, -80), Component("comma", 160, -80))),
]


def contents_path(ufo_path: Path) -> Path:
    return ufo_path / "glyphs" / "contents.plist"


def read_contents(ufo_path: Path) -> dict[str, str]:
    return plistlib.loads(contents_path(ufo_path).read_bytes())


def write_contents(ufo_path: Path, contents: dict[str, str]) -> None:
    contents_path(ufo_path).write_bytes(plistlib.dumps(contents, sort_keys=True))


def glif_path(ufo_path: Path, contents: dict[str, str], glyph_name: str) -> Path | None:
    filename = contents.get(glyph_name)
    if not filename:
        return None
    return ufo_path / "glyphs" / filename


def glyph_width(path: Path) -> int:
    root = ET.parse(path).getroot()
    advance = root.find("advance")
    if advance is None:
        return 0
    return int(round(float(advance.attrib.get("width", "0"))))


def file_name_for(glyph_name: str) -> str:
    if glyph_name and glyph_name[0].isupper():
        return f"{glyph_name[0]}_{glyph_name[1:]}.glif"
    return f"{glyph_name}.glif"


def accent_offset(base_width: int, accent_width: int, case: str) -> tuple[int, int]:
    optical_shift = 10 if case == "upper" else 44
    y_offset = 144 if case == "upper" else 2
    return round((base_width - accent_width) / 2 + optical_shift), y_offset


def indent_xml(element: ET.Element) -> None:
    ET.indent(element, space="\t")


def serialize(root: ET.Element) -> bytes:
    indent_xml(root)
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="utf-8")


def combining_glif(glyph_name: str, codepoint: int, accent_name: str) -> bytes:
    glyph = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    ET.SubElement(glyph, "unicode", {"hex": f"{codepoint:04X}"})
    anchor = COMBINING_ANCHORS.get(glyph_name)
    if anchor is not None:
        x, y, name = anchor
        ET.SubElement(glyph, "anchor", {"x": str(x), "y": str(y), "name": name})
    outline = ET.SubElement(glyph, "outline")
    ET.SubElement(outline, "component", {"base": accent_name})
    return serialize(glyph)


def helper_glif(helper: Helper) -> bytes:
    glyph = ET.Element("glyph", {"name": helper.glyph_name, "format": "2"})
    if helper.codepoint is not None:
        ET.SubElement(glyph, "unicode", {"hex": f"{helper.codepoint:04X}"})
    ET.SubElement(glyph, "advance", {"width": str(helper.width)})
    outline = ET.SubElement(glyph, "outline")
    if helper.component_base is not None:
        ET.SubElement(outline, "component", {"base": helper.component_base})
    for contour_points in helper.contours:
        contour = ET.SubElement(outline, "contour")
        for x, y in contour_points:
            ET.SubElement(contour, "point", {"x": str(x), "y": str(y), "type": "line"})
    return serialize(glyph)


def composite_glif(
    candidate: Candidate,
    base_width: int,
    accent_width: int,
) -> bytes:
    glyph = ET.Element("glyph", {"name": candidate.glyph_name, "format": "2"})
    ET.SubElement(glyph, "unicode", {"hex": f"{candidate.codepoint:04X}"})
    ET.SubElement(glyph, "advance", {"width": str(base_width)})
    outline = ET.SubElement(glyph, "outline")
    ET.SubElement(outline, "component", {"base": candidate.base_name})
    x_offset, y_offset = accent_offset(base_width, accent_width, candidate.case)
    ET.SubElement(
        outline,
        "component",
        {
            "base": candidate.accent_name,
            "xOffset": str(x_offset),
            "yOffset": str(y_offset),
        },
    )
    return serialize(glyph)


def component_candidate_glif(candidate: ComponentCandidate) -> bytes:
    glyph = ET.Element("glyph", {"name": candidate.glyph_name, "format": "2"})
    ET.SubElement(glyph, "unicode", {"hex": f"{candidate.codepoint:04X}"})
    ET.SubElement(glyph, "advance", {"width": str(candidate.width)})
    outline = ET.SubElement(glyph, "outline")
    for component in candidate.components:
        attrs = {"base": component.base_name}
        if component.x_offset:
            attrs["xOffset"] = str(component.x_offset)
        if component.y_offset:
            attrs["yOffset"] = str(component.y_offset)
        if component.x_scale is not None:
            attrs["xScale"] = f"{component.x_scale:.4g}"
        if component.y_scale is not None:
            attrs["yScale"] = f"{component.y_scale:.4g}"
        ET.SubElement(outline, "component", attrs)
    return serialize(glyph)


def process_ufo(ufo_path: Path, write: bool, refresh: bool) -> list[str]:
    contents = read_contents(ufo_path)
    virtual_widths: dict[str, int] = {}
    rows: list[str] = []

    for helper in HELPERS:
        if helper.glyph_name in contents:
            rows.append(f"exists {ufo_path.name} {helper.glyph_name}")
            if write and refresh:
                filename = contents[helper.glyph_name]
                (ufo_path / "glyphs" / filename).write_bytes(helper_glif(helper))
                virtual_widths[helper.glyph_name] = helper.width
            continue
        if helper.component_base is not None and helper.component_base not in contents:
            rows.append(
                f"missing-prerequisite {ufo_path.name} {helper.glyph_name}: "
                f"{helper.component_base}"
            )
            continue
        filename = file_name_for(helper.glyph_name)
        codepoint = f" U+{helper.codepoint:04X}" if helper.codepoint is not None else ""
        rows.append(f"create {ufo_path.name} {helper.glyph_name}{codepoint}")
        if write:
            (ufo_path / "glyphs" / filename).write_bytes(helper_glif(helper))
        contents[helper.glyph_name] = filename
        virtual_widths[helper.glyph_name] = helper.width

    for glyph_name, (codepoint, accent_name) in COMBINING_MARKS.items():
        if glyph_name in contents:
            rows.append(f"exists {ufo_path.name} {glyph_name}")
            if write and refresh:
                filename = contents[glyph_name]
                (ufo_path / "glyphs" / filename).write_bytes(
                    combining_glif(glyph_name, codepoint, accent_name)
                )
            continue
        if accent_name not in contents:
            rows.append(f"missing-prerequisite {ufo_path.name} {glyph_name}: {accent_name}")
            continue
        filename = file_name_for(glyph_name)
        rows.append(f"create {ufo_path.name} {glyph_name} U+{codepoint:04X} from {accent_name}")
        if write:
            (ufo_path / "glyphs" / filename).write_bytes(combining_glif(glyph_name, codepoint, accent_name))
        contents[glyph_name] = filename

    for candidate in ACCENTED_CANDIDATES:
        if candidate.glyph_name in contents:
            rows.append(f"exists {ufo_path.name} {candidate.glyph_name}")
            if write and refresh:
                base_path = glif_path(ufo_path, contents, candidate.base_name)
                accent_path = glif_path(ufo_path, contents, candidate.accent_name)
                if base_path is not None and accent_path is not None:
                    base_width = glyph_width(base_path)
                    if candidate.accent_name in virtual_widths:
                        accent_width = virtual_widths[candidate.accent_name]
                    else:
                        accent_width = glyph_width(accent_path)
                    filename = contents[candidate.glyph_name]
                    (ufo_path / "glyphs" / filename).write_bytes(
                        composite_glif(candidate, base_width, accent_width)
                    )
            continue
        base_path = glif_path(ufo_path, contents, candidate.base_name)
        accent_path = glif_path(ufo_path, contents, candidate.accent_name)
        if base_path is None or accent_path is None:
            missing = ", ".join(
                name
                for name, path in (
                    (candidate.base_name, base_path),
                    (candidate.accent_name, accent_path),
                )
                if path is None
            )
            rows.append(f"missing-prerequisite {ufo_path.name} {candidate.glyph_name}: {missing}")
            continue
        base_width = glyph_width(base_path)
        if candidate.accent_name in virtual_widths:
            accent_width = virtual_widths[candidate.accent_name]
        else:
            accent_width = glyph_width(accent_path)
        filename = file_name_for(candidate.glyph_name)
        rows.append(
            "create "
            f"{ufo_path.name} {candidate.glyph_name} U+{candidate.codepoint:04X} "
            f"from {candidate.base_name}+{candidate.accent_name}"
        )
        if write:
            (ufo_path / "glyphs" / filename).write_bytes(
                composite_glif(candidate, base_width, accent_width)
            )
        contents[candidate.glyph_name] = filename

    for candidate in COMPONENT_CANDIDATES:
        missing = [component.base_name for component in candidate.components if component.base_name not in contents]
        if candidate.glyph_name in contents:
            rows.append(f"exists {ufo_path.name} {candidate.glyph_name}")
            if write and refresh and not missing:
                filename = contents[candidate.glyph_name]
                (ufo_path / "glyphs" / filename).write_bytes(
                    component_candidate_glif(candidate)
                )
            continue
        if missing:
            rows.append(
                f"missing-prerequisite {ufo_path.name} {candidate.glyph_name}: "
                f"{', '.join(missing)}"
            )
            continue
        filename = file_name_for(candidate.glyph_name)
        rows.append(f"create {ufo_path.name} {candidate.glyph_name} U+{candidate.codepoint:04X}")
        if write:
            (ufo_path / "glyphs" / filename).write_bytes(
                component_candidate_glif(candidate)
            )
        contents[candidate.glyph_name] = filename

    if write:
        write_contents(ufo_path, contents)
    return rows


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write missing candidates")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="with --write, rewrite existing generated candidates from the current recipes",
    )
    args = parser.parse_args(argv[1:])

    for ufo_path in UFO_PATHS:
        print(f"# {ufo_path.relative_to(ROOT)}")
        for row in process_ufo(ufo_path, args.write, args.refresh):
            print(row)
        print()
    if not args.write:
        print("Dry run only. Re-run with --write to create missing candidate composites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
