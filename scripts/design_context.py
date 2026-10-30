#!/usr/bin/env python3
"""Retrieve scoped Virtua design context and verify its source/evidence identities.

Reading context never authorizes an edit or changes a glyph. All paths in the
catalog and emitted JSON are repository relative, so packets survive relocation.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
import plistlib
import sys
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OPERATIONS = ("inspect", "draw", "redraw", "curve-repair", "weight-transfer",
              "spacing", "kerning", "anchors", "components", "from-image")


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


def load_records(root):
    records = read_json(root / "design/catalog.json")["records"]
    records += [read_json(p) for p in sorted((root / "design/corrections/records").glob("*.json"))]
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate design record ID")
    return {r["id"]: r for r in records}


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


def closure(glyphs, names, reverse=False):
    result = set(names)
    while True:
        if reverse:
            added = {n for n, g in glyphs.items() if any(c["base"] in result for c in g["components"])}
        else:
            added = {c["base"] for n in result if n in glyphs for c in glyphs[n]["components"]}
        new = result | added
        if new == result:
            return result
        result = new


def glyph_script(name, glyph=None):
    cps = (glyph or {}).get("unicodes", [])
    if "-ar" in name or any("ARABIC" in unicodedata.name(chr(cp), "") for cp in cps):
        return "arabic"
    if "-hb" in name or any("HEBREW" in unicodedata.name(chr(cp), "") for cp in cps):
        return "hebrew"
    if name == "at" or name.startswith(("uni2", "uniE")):
        return "symbols"
    if any("LATIN" in unicodedata.name(chr(cp), "") for cp in cps) or (not cps and len(name.split(".")[0]) == 1 and name[:1].isascii() and name[:1].isalpha()):
        return "latin"
    return "symbols"


def select_records(records, names, scripts, operation, masters=None):
    selected = {}
    exact_tags = set()
    for rid, record in records.items():
        if masters and record.get("masters") and not set(masters).intersection(record["masters"]):
            continue
        hits = [n for n in names if any(fnmatch.fnmatchcase(n, p) for p in record.get("glyphs", []))]
        if record.get("always"):
            selected[rid] = "Shared design/safety contract"
        elif hits and (not record.get("operations") or operation in record["operations"] or any(n in record.get("glyphs", []) for n in hits)):
            selected[rid] = "Matches glyph: " + ", ".join(sorted(hits))
            exact_tags.update(record.get("tags", []))
        elif record["kind"] == "writing-system" and scripts.intersection(record.get("scripts", [])):
            selected[rid] = "Writing system: " + ", ".join(sorted(scripts))
    for rid, record in records.items():
        if record["kind"] in ("construction", "procedure", "reference", "system"):
            script_ok = not record.get("scripts") or bool(scripts.intersection(record["scripts"]))
            if script_ok and (operation in record.get("operations", []) or exact_tags.intersection(record.get("tags", []))):
                selected.setdefault(rid, "Relevant construction or operation: " + operation)
    # Explicit counterexamples are part of a lesson, even across writing systems.
    pending = list(selected)
    while pending:
        rid = pending.pop()
        for related in records[rid].get("related", []):
            if related not in records:
                raise ValueError(f"{rid}: unknown related record {related}")
            if related not in selected:
                selected[related] = f"Required example/exception for {rid}"
                pending.append(related)
    return selected


def reference_state(root, record):
    result = {"id": record["id"], "title": record["title"], "kind": record["kind"],
              "status": record["status"], "summary": record["summary"],
              "scope": {k: record.get(k, []) for k in ("glyphs", "masters", "scripts", "operations")},
              "limits": record.get("limits", ""), "evidence": []}
    if record.get("path"):
        path = local_path(root, record["path"])
        result["path"] = record["path"]
        result["text"] = path.read_text()
        result["sha256"] = digest(path)
    for evidence in record.get("evidence", []):
        item = dict(evidence)
        path = local_path(root, item["path"])
        item["available"] = path.is_file()
        item["hash_matches"] = path.is_file() and (not item.get("sha256") or digest(path) == item["sha256"])
        result["evidence"].append(item)
    if record["kind"] == "correction":
        for key in ("human_feedback", "interpretation", "application", "visual_verdict", "training_eligibility", "pairs", "excerpt_path"):
            result[key] = record.get(key)
    return result


def correction_inventory(root):
    return {relative(root, p): digest(p) for p in sorted((root / "design/corrections/records").glob("*.json"))}


def current_state(root):
    state = read_json(root / "design/reviews/current.json")
    state["active_source_status"] = [dict(item, matches_current=(local_path(root, item["path"]).is_file() and
                                      digest(local_path(root, item["path"])) == item["sha256"]))
                                     for item in state.get("active_sources", [])]
    return state


def build_packet(root, names, masters, operation):
    records = load_records(root)
    contract = read_json(root / "design/system/contract.json")
    inventories = {m: load_master(root, m, contract) for m in masters}
    scripts = {glyph_script(n, next((inv[n] for inv in inventories.values() if n in inv), None)) for n in names}
    # A changed donor's consumers may carry a more specific design decision.
    affected_names = set(names)
    for inv in inventories.values():
        affected_names.update(closure(inv, names, reverse=True))
    selected = select_records(records, affected_names, scripts, operation, masters)
    rendered_records = []
    state = current_state(root)
    warnings, targets, references, guards = [], [], [], {}
    for source in state.get("active_source_status", []):
        if not source["matches_current"]:
            warnings.append(f"Current review state is stale for {source['master']}/{source['glyph']}; inspect source changes before using its application claim")
    for rid, reason in selected.items():
        entry = reference_state(root, records[rid]); entry["why_selected"] = reason
        rendered_records.append(entry)
        for evidence in entry["evidence"]:
            if not evidence["hash_matches"]:
                warnings.append(f"{rid}: missing or changed evidence {evidence['path']}")
    wanted_references = set()
    for rid in selected:
        wanted_references.update(records[rid].get("reference_glyphs", []))
    for master, inv in inventories.items():
        for name in names:
            if name not in inv:
                targets.append({"glyph": name, "master": master, "missing": True})
                warnings.append(f"{master}/{name}: no source glyph; choose approved construction references before drafting")
                continue
            item = dict(inv[name])
            donors = closure(inv, [name]) - {name}
            consumers = closure(inv, [name], reverse=True) - {name}
            item["donors"] = sorted(donors)
            item["affected_consumers"] = sorted(consumers)
            item["protected_consumers"] = sorted(n for n in consumers if inv[n]["color"]["protected"])
            item["missing_donors"] = sorted(n for n in donors if n not in inv)
            targets.append(item)
            for n in donors | consumers | {name}:
                if n in inv: guards[inv[n]["path"]] = inv[n]["sha256"]
            if item["color"]["protected"] or item["protected_consumers"]:
                warnings.append(f"{master}/{name}: protected source or green dependent; explicit named exception required for an inherited change")
            if item["color"]["name"] in ("unknown", "conflict"):
                warnings.append(f"{master}/{name}: unclassified/conflicting color; no automatic editing permission")
            if item["missing_donors"]:
                warnings.append(f"{master}/{name}: missing component donors {item['missing_donors']}")
        for name in sorted(wanted_references):
            if name not in inv:
                references.append({"glyph": name, "master": master, "available": False})
                continue
            item = dict(inv[name]); item["available"] = True
            item["role"] = "Virtua construction reference" if item["color"]["reference_eligible"] else "Unavailable as approved reference; current grade does not qualify"
            references.append(item)
            for n in closure(inv, [name]):
                if n in inv: guards[inv[n]["path"]] = inv[n]["sha256"]
        ufo = root / f"sources/VirtuaGrotesk-{master}.ufo"
        for p in [ufo / "glyphs/contents.plist", *[x for x in ufo.iterdir() if x.is_file() and x.name != '.DS_Store']]:
            guards[relative(root, p)] = digest(p)
    for p in (root / "sources").iterdir():
        if p.is_file() and p.name != '.DS_Store': guards[relative(root, p)] = digest(p)
    for key in ["design/catalog.json", "design/system/contract.json", "design/reviews/current.json"]:
        guards[key] = digest(root / key)
    for rid in selected:
        record = records[rid]
        if record.get("path"):
            p = local_path(root, record["path"]); guards[relative(root, p)] = digest(p)
        for evidence in record.get("evidence", []):
            p = local_path(root, evidence["path"])
            if p.is_file(): guards[relative(root, p)] = digest(p)
        if record["kind"] == "correction":
            p = root / "design/corrections/records" / f"{rid}.json"
            guards[relative(root,p)] = digest(p)
    return {"schema_version": 1, "request": {"glyphs": names, "masters": masters, "operation": operation},
            "authorization": "Context is evidence, not permission. Follow the current user scope and recorded human decisions.",
            "current_work": state, "correction_inventory": correction_inventory(root),
            "contract": contract, "targets": targets, "references": references,
            "records": rendered_records, "warnings": warnings, "guard_hashes": guards}


def verify_packet(root, packet):
    if packet.get("schema_version") != 1 or not packet.get("guard_hashes"):
        raise ValueError("Not a version 1 context packet with source guards")
    changed = []
    if packet.get("correction_inventory") != correction_inventory(root):
        changed.append("design/corrections/records (index changed)")
    for value, expected in packet["guard_hashes"].items():
        path = local_path(root, value)
        if not path.is_file() or digest(path) != expected:
            changed.append(value)
    return changed


def validate_library(root):
    records = load_records(root)
    errors = []
    for rid, record in records.items():
        if record.get("schema_version", 1) != 1: errors.append(f"{rid}: unsupported schema version")
        for key in ("id", "kind", "title", "status", "summary"):
            if not record.get(key): errors.append(f"{rid}: missing {key}")
        for key in ("glyphs", "masters", "scripts", "operations", "tags", "related"):
            if not isinstance(record.get(key, []), list) or not all(isinstance(x, str) for x in record.get(key, [])):
                errors.append(f"{rid}: {key} must be a list of strings")
        if any(op not in OPERATIONS for op in record.get("operations", [])):
            errors.append(f"{rid}: unknown operation")
        if any(m not in ("Regular", "Bold") for m in record.get("masters", [])):
            errors.append(f"{rid}: unknown master")
        if record["kind"] == "correction":
            if record.get("training_eligibility") not in ("not-approved", "negative-example", "requires-curation", "approved-pair"):
                errors.append(f"{rid}: explicit training eligibility required")
            if record.get("visual_verdict") == "rejected" and record.get("training_eligibility") == "approved-pair":
                errors.append(f"{rid}: rejected candidate cannot be a positive pair")
            if record.get("training_eligibility") == "approved-pair" and not any(
                e["path"] == record.get("approval_evidence") and e.get("sha256") for e in record.get("evidence", [])):
                errors.append(f"{rid}: positive pair requires hashed approval evidence")
            if record.get("training_eligibility") == "approved-pair" and not record.get("pairs"):
                errors.append(f"{rid}: positive pair requires exact source pairs")
            for pair in record.get("pairs", []):
                if pair.get("master") not in ("Regular", "Bold") or not pair.get("before") or not pair.get("after"):
                    errors.append(f"{rid}: pair requires master and both sides")
                for side in ("before", "after"):
                    if pair.get(side) and not any(e["path"] == pair[side] and e.get("sha256") for e in record.get("evidence", [])):
                        errors.append(f"{rid}: {side} pair has no hashed evidence")
        if record.get("path") and not local_path(root, record["path"]).is_file():
            errors.append(f"{rid}: missing document {record['path']}")
        for related in record.get("related", []):
            if related not in records: errors.append(f"{rid}: missing related ID {related}")
        for evidence in record.get("evidence", []):
            if not evidence.get("sha256"): errors.append(f"{rid}: evidence must include SHA-256")
            path = local_path(root, evidence["path"])
            if not path.is_file(): errors.append(f"{rid}: missing evidence {evidence['path']}")
            elif evidence.get("sha256") and digest(path) != evidence["sha256"]:
                errors.append(f"{rid}: evidence hash mismatch {evidence['path']}")
    state = read_json(root / "design/reviews/current.json")
    if state.get("schema_version") != 1: errors.append("Invalid current review schema")
    for record in state.get("work", []):
        if not local_path(root, record["case"]).is_file(): errors.append(f"Missing current case: {record['case']}")
    snapshot = local_path(root, state["proof_snapshot"])
    if not (snapshot / "live-fonts.json").is_file(): errors.append("Current portable proof is missing")
    else:
        for role, record in read_json(snapshot / "live-fonts.json").items():
            for face in record.get("faces", [record]):
                path = (snapshot / face["url"]).resolve()
                if not path.is_relative_to(snapshot) or not path.is_file() or digest(path) != face["sha256"]:
                    errors.append(f"Current proof font mismatch: {role}")
    return errors


def markdown(packet):
    req = packet["request"]
    lines = ["# Virtua drawing context", "", f"Glyphs: {', '.join(req['glyphs'])}. Masters: {', '.join(req['masters'])}. Operation: {req['operation']}.",
             "", packet["authorization"], "", "## Current work", "", packet["current_work"]["summary"], "",
             "## Current source facts", ""]
    for g in packet["targets"]:
        if g.get("missing"):
            lines.append(f"- {g['master']}/{g['glyph']}: source absent."); continue
        lines += [f"- {g['master']}/{g['glyph']}: {g['color']['name']}; advance {g['advance']:g}; points {g['point_counts']}; {g['off_8_points']} inherited points off 8.",
                  f"  Source: `{g['path']}`; SHA-256 `{g['sha256']}`.",
                  f"  Components: {', '.join(g['donors']) or 'none'}; affected consumers: {', '.join(g['affected_consumers']) or 'none'}."]
    if packet["warnings"]:
        lines += ["", "## Scope and evidence warnings", ""] + ["- " + x for x in packet["warnings"]]
    lines += ["", "## Live reference sources", ""]
    for g in packet["references"]:
        lines.append(f"- {g['master']}/{g['glyph']}: {g.get('role', 'missing')}" + (f" — `{g['path']}` ({g['sha256'][:12]})." if g.get('path') else "."))
    for record in packet["records"]:
        lines += ["", f"## {record['title']} [{record['id']}]", "", f"State: {record['status']}. Selected because: {record['why_selected']}.", "", record["summary"]]
        if record.get("limits"): lines += ["", "Limits: " + record["limits"]]
        if record.get("text"): lines += ["", record["text"]]
        if record.get("human_feedback"): lines += ["", "Human feedback: " + record["human_feedback"]]
        if record.get("interpretation"): lines += ["", "Recorded interpretation: " + record["interpretation"]]
        if record["kind"] == "correction": lines += ["", f"Application: {record.get('application')}; visual verdict: {record.get('visual_verdict')}; training: {record.get('training_eligibility')}."]
        for e in record["evidence"]:
            lines.append(f"- {e.get('role', 'Evidence')}: `{e['path']}` ({'verified' if e['hash_matches'] else 'MISSING/CHANGED'}).")
            if e.get('source_path'): lines.append(f"  Original context: `{e['source_path']}`.")
    lines += ["", "Save a JSON packet with --json --output out/context.json and recheck with --verify out/context.json immediately before applying an authorized edit.", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--glyph", action="append", help="Glyph name; repeat for a bounded group")
    parser.add_argument("--master", choices=("Regular", "Bold", "both"), default="both")
    parser.add_argument("--operation", choices=OPERATIONS, default="inspect")
    parser.add_argument("--json", action="store_true", help="Machine-readable packet including source/evidence guards")
    parser.add_argument("--output", type=Path, help="Save packet to a file instead of stdout")
    parser.add_argument("--check", action="store_true", help="Validate library routes, correction evidence and portable proof")
    parser.add_argument("--status", action="store_true", help="Read current review state")
    parser.add_argument("--list", action="store_true", help="List discoverable design records")
    parser.add_argument("--verify", type=Path, help="Check a previously emitted JSON packet for changed input files")
    args = parser.parse_args(argv)
    try:
        if args.check:
            errors = validate_library(ROOT)
            print(json.dumps({"ok": not errors, "errors": errors}, indent=2) if args.json else ("\n".join(errors) if errors else "Design library and frozen proof verified"))
            return int(bool(errors))
        if args.verify:
            changed = verify_packet(ROOT, read_json(args.verify))
            print(json.dumps({"fresh": not changed, "changed": changed}, indent=2))
            return int(bool(changed))
        if args.status:
            text = json.dumps(current_state(ROOT), indent=2, ensure_ascii=False)
        elif args.list:
            text = "\n".join(f"{r['id']}\t{r['kind']}\t{r['title']}" for r in load_records(ROOT).values())
        else:
            if not args.glyph: parser.error("--glyph is required unless using --check, --status, --list or --verify")
            masters = ["Regular", "Bold"] if args.master == "both" else [args.master]
            packet = build_packet(ROOT, list(dict.fromkeys(args.glyph)), masters, args.operation)
            text = json.dumps(packet, indent=2, ensure_ascii=False) if args.json else markdown(packet)
        if args.output:
            path = args.output.resolve()
            if not path.is_relative_to(ROOT / "out"):
                parser.error("Generated packets belong under out/; use stdout for other consumers")
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text + "\n")
            print(path)
        else:
            print(text)
        return 0
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        print(f"Design context unavailable: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
