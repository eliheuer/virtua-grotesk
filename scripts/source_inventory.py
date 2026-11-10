#!/usr/bin/env python3
"""Read master glyph records, mark colors and file digests from the UFO sources.

Reading never changes a source file. Paths are repository relative.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import plistlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def local_path(root, value):
    path = (root / value.split("#", 1)[0]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {value}")
    return path


def relative(root, path):
    return str(path.resolve().relative_to(root.resolve()))


def color_state(lib, contract):
    label = lib.get("com.runebender.markLabel")
    raw = lib.get("public.markColor")
    matched = None
    try:
        rgba = tuple(float(v.strip()) for v in raw.split(",")) if raw else ()
        for name, rule in contract["colors"].items():
            if any(len(rgba) == 4 and all(abs(a-b) < 0.015 for a,b in zip(rgba, variant))
                   for variant in rule["rgba"]):
                matched = name
                break
    except (ValueError, AttributeError):
        pass
    conflict = bool(label and (label not in contract["colors"] or (matched and label != matched)))
    name = "conflict" if conflict else matched or (label if label in contract["colors"] else "unknown")
    # A conflicting green signal still protects the source, but cannot approve
    # its use as a reference. Never infer reference status from an unknown RGBA.
    return {"name": name, "label": label, "rgba": raw,
            "protected": label == "green" or matched == "green",
            "reference_eligible": name == "green" and matched == "green",
            "policy": contract["colors"].get(name, {}).get("policy", "Classify before editing or reference use")}


def load_master(root, master, contract):
    ufo = root / f"sources/VirtuaGrotesk-{master}.ufo"
    contents = plistlib.loads((ufo / "glyphs/contents.plist").read_bytes())
    glyphs = {}
    for name, filename in contents.items():
        path = ufo / "glyphs" / filename
        doc = ET.parse(path).getroot()
        lib = doc.find("lib/dict")
        values = plistlib.loads(b'<plist version="1.0">'+ET.tostring(lib)+b'</plist>') if lib is not None else {}
        contours = doc.findall("outline/contour")
        points = doc.findall("outline/contour/point")
        advance = doc.find("advance")
        glyphs[name] = {
            "glyph": name, "master": master, "path": relative(root, path),
            "sha256": digest(path), "color": color_state(values, contract),
            "unicodes": [int(u.get("hex"), 16) for u in doc.findall("unicode")],
            "advance": float(advance.get("width", 0)) if advance is not None else None,
            "contours": len(contours), "point_counts": [len(c.findall("point")) for c in contours],
            "point_types": [[p.get("type", "offcurve") for p in c.findall("point")] for c in contours],
            "off_8_points": sum(any(float(p.get(a, 0)) % 8 for a in ("x", "y")) for p in points),
            "off_2_points": sum(any(float(p.get(a, 0)) % 2 for a in ("x", "y")) for p in points),
            "components": [c.attrib for c in doc.findall("outline/component")],
            "anchors": [a.attrib for a in doc.findall("anchor")],
        }
    return glyphs

