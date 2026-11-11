#!/usr/bin/env python3
"""Read only a reviewed frozen snapshot; never fall back to live font sources."""
import argparse,hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET

def load_split(snapshot, expected_sha256, split):
    snapshot=Path(snapshot).resolve();path=snapshot/'manifest.json'
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected_sha256:raise ValueError('Manifest identity mismatch')
    manifest=json.loads(path.read_text());groups={};seen=set();records=[]
    if split not in ('train','validation','test'):raise ValueError('Unknown split')
    for r in manifest['rows']:
        key=(r['master'],r['glyph'])
        if key in seen:raise ValueError('Duplicate example')
        seen.add(key)
        if groups.setdefault(r['group'],r['split'])!=r['split']:raise ValueError('Group leakage')
        if not r['color']['reference_eligible'] or r['components']:raise ValueError('Unapproved or composite target')
        if r['glyph'] in manifest['policy']['shared_marks']:raise ValueError('Shared mark in body targets')
        p=(snapshot/r['path']).resolve()
        if not p.is_relative_to(snapshot):raise ValueError('Path escapes frozen snapshot')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Frozen glyph identity mismatch')
        if r['split']==split:
            d=ET.parse(p);records.append({'glyph':r['glyph'],'master':r['master'],'group':r['group'],'source_sha256':r['sha256'],
                'advance':r['advance'],'contours':[[dict(point.attrib) for point in c.findall('point')] for c in d.findall('outline/contour')]})
    return records

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('snapshot',type=Path);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--split',choices=['train','validation','test'],required=True);a=ap.parse_args()
    for r in load_split(a.snapshot,a.manifest_sha256,a.split):print(json.dumps(r))
