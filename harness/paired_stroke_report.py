#!/usr/bin/env python3
"""Read-only paired-edge widths. Explicit branch pairs prevent spiral cross-gap matches.

Use alongside curve_profile.py and a filled proof. Width ranges are observations,
never pass thresholds or optical grades. A changed GLIF requires a reviewed plan.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np


def bezier(c, t):
    return (1-t)**3*c[0] + 3*(1-t)**2*t*c[1] + 3*(1-t)*t*t*c[2] + t**3*c[3]


def normal_hits(edge, opposite, t):
    origin = bezier(edge, t)
    tangent = 3*((1-t)**2*(edge[1]-edge[0]) + 2*t*(1-t)*(edge[2]-edge[1]) + t*t*(edge[3]-edge[2]))
    speed = np.linalg.norm(tangent)
    if speed < 1e-9:
        return {'status': 'undefined_tangent', 'hits': []}
    tangent /= speed
    coeff = [(-opposite[0]+3*opposite[1]-3*opposite[2]+opposite[3]) @ tangent,
             (3*opposite[0]-6*opposite[1]+3*opposite[2]) @ tangent,
             (-3*opposite[0]+3*opposite[1]) @ tangent,
             (opposite[0]-origin) @ tangent]
    if max(abs(v) for v in coeff) < 1e-9:
        return {'status': 'coincident_normal', 'hits': []}
    roots = np.roots(np.trim_zeros(np.array(coeff), 'f'))
    parameters = []
    for s in roots:
        if abs(s.imag) < 1e-7 and -1e-7 <= s.real <= 1+1e-7:
            q = float(np.clip(s.real, 0, 1))
            if not any(abs(q-old) < 1e-6 for old in parameters):
                parameters.append(q)
    hits = [{'opposite_t': s, 'point': bezier(opposite, s).tolist(),
             'width': float(np.linalg.norm(bezier(opposite, s)-origin))} for s in parameters]
    return {'status': 'unique' if len(hits)==1 else 'missing' if not hits else 'ambiguous',
            'origin': origin.tolist(), 'hits': hits}


def cubic(contour, index):
    p = [contour[(index+i) % len(contour)] for i in range(4)]
    if p[0].get('type') is None or any(q.get('type') for q in p[1:3]) or p[3].get('type') != 'curve':
        raise ValueError(f'point {index} does not start an explicit cubic')
    return np.array([[float(q.attrib['x']),float(q.attrib['y'])] for q in p])


def report(glif, plan):
    digest = hashlib.sha256(glif.read_bytes()).hexdigest()
    if digest != plan['sha256']:
        raise ValueError('GLIF changed: review branch pairing and update the plan hash explicitly')
    root = ET.parse(glif)
    if root.find('.//component') is not None:
        raise ValueError('resolve components on scratch before measurement')
    contours = [list(c) for c in root.findall('outline/contour')]
    rows = []
    for pair in plan['pairs']:
        contour = contours[pair['contour']]
        edge, opposite = (cubic(contour, pair[k]) for k in ['edge_start', 'opposite_start'])
        samples = [{'t':float(t), **normal_hits(edge, opposite, t)} for t in np.linspace(.05,.95,37)]
        widths = [s['hits'][0]['width'] for s in samples if s['status']=='unique']
        rows.append({**pair, 'unique_samples':len(widths),
                     'range_of_unique_samples': [min(widths),max(widths)] if widths else None,
                     'samples':samples})
    return {'glif':str(glif.resolve()), 'sha256':digest,
            'method':'37 normal intersections on explicitly paired cubics, t=.05 to .95. Ambiguous and missing hits retained; no nearest-branch guess. Local geometry only, not whole-stroke extrema or optical approval.',
            'optical_intent':plan.get('optical_intent'), 'pairs':rows}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('glif',type=Path);parser.add_argument('plan',type=Path);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.resolve() in [args.glif.resolve(), args.plan.resolve()]:
        parser.error('output must not overwrite either input')
    result=report(args.glif,json.loads(args.plan.read_text()))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f"{len(result['pairs'])} explicit pairs; geometric report only, no grade")

if __name__=='__main__':main()
