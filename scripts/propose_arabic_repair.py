#!/usr/bin/env python3
"""CPU-only experimental inference. Writes new scratch artifacts, never active fonts."""
import argparse
import hashlib
import json
import plistlib
from pathlib import Path
import xml.etree.ElementTree as ET

import torch
import masked_repair as mr
import variable_repair as vr

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'models/arabic-repair-hour-v1'


def propose(sample):
    manifest = json.loads((MODEL / 'manifest.json').read_text())
    checkpoint = MODEL / 'checkpoint.pt'
    if hashlib.sha256(checkpoint.read_bytes()).hexdigest() != manifest['checkpoint_sha256']:
        raise ValueError('Checkpoint hash mismatch')
    record, mask = sample['input'], sample['editable_mask']
    flat = mr.flatten(record)
    if record['master'] != 'Regular' or len(mask) != len(flat) or any(v not in (0, 1) for v in mask):
        raise ValueError('Requires Regular geometry and one explicit binary mask value per point')
    mr.checked(record['advance'], mr.COORD_MIN, mr.COORD_MAX)
    ex = vr.make_example(record, {i for i, value in enumerate(mask) if value}, {}, 'inference', 'scratch')
    torch.set_num_threads(1)
    saved = torch.load(checkpoint, map_location='cpu', weights_only=True)
    model = vr.VariableRepair()
    model.load_state_dict(saved['state_dict'])
    model.eval()
    with torch.inference_mode():
        x, neighbors, spatial, valid, editable, _ = vr.collate([ex])
        delta = (model(x, neighbors, spatial, valid, editable)[0] / 2).round() * 2
    return mr.reconstruct(ex, delta.tolist()), manifest


def scratch_ufo(path, before, after):
    (path / 'glyphs').mkdir(parents=True)
    def plist(name, value):
        (path / name).write_bytes(plistlib.dumps(value))
    plist('metainfo.plist', {'creator': 'org.virtua.scratch', 'formatVersion': 3})
    plist('layercontents.plist', [['public.default', 'glyphs']])
    plist('fontinfo.plist', {'familyName': 'EXPERIMENTAL Arabic repair — SCRATCH',
                           'styleName': 'Regular', 'unitsPerEm': 1024, 'ascender': 832, 'descender': -400})
    contents = {}
    for label, record in [('input', before), ('model', after)]:
        name = record['glyph'] + '.' + label
        glyph = ET.Element('glyph', name=name, format='2')
        ET.SubElement(glyph, 'advance', width=str(record['advance']))
        ET.SubElement(glyph, 'note').text = 'Experimental scratch; not approved. No Unicode alias or grade.'
        outline = ET.SubElement(glyph, 'outline')
        for contour in record['contours']:
            c = ET.SubElement(outline, 'contour')
            for point in contour:
                ET.SubElement(c, 'point', {k: str(v) for k, v in point.items() if k in ('x', 'y', 'type', 'smooth')})
        filename = label + '.glif'
        ET.ElementTree(glyph).write(path / 'glyphs' / filename, encoding='UTF-8', xml_declaration=True)
        contents[name] = filename
    plist('glyphs/contents.plist', contents)
    plist('lib.plist', {'public.glyphOrder': list(contents)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=MODEL / 'sample.json')
    parser.add_argument('--out', type=Path, default=ROOT / 'out/arabic-repair-demo')
    args = parser.parse_args()
    out = args.out.resolve()
    if not out.is_relative_to((ROOT / 'out').resolve()) or out.exists():
        raise ValueError('Output must be a new directory beneath this repository out/')
    sample = json.loads(args.input.read_text())
    prediction, manifest = propose(sample)
    out.mkdir(parents=True)
    (out / 'proposal.json').write_text(json.dumps(prediction, indent=2) + '\n')
    (out / 'receipt.json').write_text(json.dumps({'checkpoint_sha256': manifest['checkpoint_sha256'],
        'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
        'experimental': True, 'applied': False}, indent=2) + '\n')
    scratch_ufo(out / 'Review.ufo', sample['input'], prediction)
    print(out / 'Review.ufo')


if __name__ == '__main__':
    main()
