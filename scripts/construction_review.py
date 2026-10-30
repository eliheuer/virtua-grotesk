#!/usr/bin/env python3
"""Read-only construction comparison and declared-constraint checks. Never grades art."""
import argparse
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import design_context as dc
from curve_lint import all_segments

ROOT = Path(__file__).resolve().parents[1]


def geometry(path):
    doc = ET.parse(path).getroot()
    if doc.findall('outline/component'):
        raise ValueError(f'{path}: component outlines need a resolved, separately guarded proof')
    contours = [[dict(x=float(p.get('x')), y=float(p.get('y')),
                      type=p.get('type'), smooth=p.get('smooth'), on=p.get('type') is not None)
                 for p in c.findall('point')] for c in doc.findall('outline/contour')]
    if any(p["type"] not in (None, "line", "curve") for c in contours for p in c):
        raise ValueError("Only closed line/cubic contours are supported; use a resolved proof")
    return doc, contours


def check_pair(before, candidate, constraints):
    """Constraints are human-readable claims, not an optical approval mechanism."""
    a, ac = geometry(before); b, bc = geometry(candidate)
    issues = []
    signature = lambda cs: [[p['type'] for p in c] for c in cs]
    if signature(ac) != signature(bc):
        return ['Point correspondence changed; remap constraints explicitly before checking']
    if not constraints:
        issues.append('No preservation constraints declared')
    for rule in constraints:
        if not rule.get('reason'):
            issues.append('Constraint missing construction reason')
        kind = rule['kind']
        if kind == 'metadata':
            for tag in ('advance', 'anchor', 'unicode'):
                if [e.attrib for e in a.findall(tag)] != [e.attrib for e in b.findall(tag)]:
                    issues.append(f'{tag} changed')
            continue
        ci = rule['contour']
        if kind == 'preserve_points':
            for i in rule['points']:
                if ac[ci][i] != bc[ci][i]: issues.append(f'Protected contour {ci} point {i} changed')
        elif kind == 'straight_run':
            i, j = rule['start'], rule['end']; p, q = bc[ci][i], bc[ci][j]
            if j != (i+1) % len(bc[ci]) or q['type'] != 'line' or p['type'] is None:
                issues.append('Declared straight run is not an adjacent on-curve line'); continue
            axis = rule['axis']; other = 'y' if axis == 'x' else 'x'
            if axis not in ('x', 'y'): raise ValueError('axis must be x or y')
            if p[axis] != q[axis]: issues.append(f'Straight run {i}:{j} no longer axis-aligned')
            if abs(q[other]-p[other]) < rule['min_length']:
                issues.append(f'Straight run {i}:{j} shorter than declared minimum {rule["min_length"]}')
        else:
            raise ValueError(f'Unknown constraint {kind}')
    return issues


def svg(path):
    _, contours = geometry(path)
    paths, nodes = [], []
    for ci, contour in enumerate(contours):
        segments = all_segments(contour)
        if not segments: continue
        x,y = segments[0][0]; commands = [f'M{x},{-y}']
        for p0,p1,p2,p3,line,*_ in segments:
            if line: commands.append(f'L{p3[0]},{-p3[1]}')
            else: commands.append(f'C{p1[0]},{-p1[1]} {p2[0]},{-p2[1]} {p3[0]},{-p3[1]}')
        paths.append('<path d="'+' '.join(commands)+' Z"/>')
        for i,p in enumerate(contour):
            nodes.append(f'<circle cx="{p["x"]}" cy="{-p["y"]}" r="5"/><text x="{p["x"]+8}" y="{-p["y"]-8}">{ci}:{i}</text>')
    # All cards share one viewBox; never normalize each glyph to its own bounds.
    return '<svg viewBox="-64 -900 1728 1300" role="img">'+''.join(paths)+'<g class="nodes">'+''.join(nodes)+'</g></svg>'


def render(root, plan):
    cards = []; errors = []
    for item in plan['items']:
        path = dc.local_path(root,item['path'])
        if dc.digest(path) != item['sha256']: raise ValueError(f'Stale outline: {item["path"]}')
        label = html.escape(item['label']); role = html.escape(item['role'])
        try: drawing = svg(path)
        except ValueError as e: drawing = '<p>'+html.escape(str(e))+'</p>'; errors.append(str(e))
        cards.append(f'<article><h2>{label}</h2><p>{role}</p>{drawing}<small>{html.escape(item["path"])}</small></article>')
    text = ''.join('<p><strong>'+label+':</strong> '+html.escape(plan.get(key) or 'Unfilled')+'</p>'
                   for key,label in [('status','Status'),('diagnosis','Diagnosis'),
                                     ('preserve_intent','Preserve'),('optical_exceptions','Optical exceptions')])
    return '''<!doctype html><meta charset="utf-8"><title>Virtua construction review</title>
<style>body{background:#222;color:#ddd;font:16px system-ui;margin:32px}h1{font-size:28px}h2{font-size:18px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}article{border-top:1px solid #888;min-width:0}small{overflow-wrap:anywhere}svg{width:100%;fill:#ddd}.nodes{display:none;fill:#888;font:22px monospace}.nodes circle{fill:#222;stroke:#ddd;stroke-width:2}body:has(#nodes:checked) .nodes{display:block}p{max-width:75ch}button{margin:12px}</style>
<h1>Construction review — not visual approval</h1><p>Read-only source outlines, shared em scale. Green donors establish construction; rejected drafts are counterexamples. These panels do not replace compiled text/reference-font proofs.</p>
<label><input type="checkbox" id="nodes"> Show contour:point indices</label>
'''+text+'<main>'+''.join(cards)+'</main>'


def make_plan(packet):
    items = []
    for item in packet['targets'] + packet['references']:
        if not item.get('path'): continue
        target = item in packet['targets']
        if not target and not item.get('color',{}).get('reference_eligible'): continue
        items.append({'path':item['path'], 'sha256':item['sha256'],
                      'label':f'{item["master"]} / {item["glyph"]}',
                      'role':'Working source; not approved' if target else 'Green construction reference'})
    return {'schema_version':1,'diagnosis':'', 'preserve_intent':'', 'optical_exceptions':'',
            'items':items,'pairs':[], 'status':'Unreviewed construction study; no drawing/application authorization'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--context',type=Path,required=True)
    ap.add_argument('--init',type=Path,help='Create a new study plan; never overwrites')
    ap.add_argument('--plan',type=Path)
    ap.add_argument('--html',type=Path)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args(); packet=dc.read_json(args.context)
    stale=dc.verify_packet(ROOT,packet)
    if stale: raise ValueError('Stale context: '+', '.join(stale))
    if args.init:
        with args.init.open('x') as f: json.dump(make_plan(packet),f,indent=2)
    plan=dc.read_json(args.plan or args.init)
    if args.html: args.html.write_text(render(ROOT,plan))
    if args.check:
        issues=[]
        for key in ['diagnosis','preserve_intent','optical_exceptions']:
            if not plan.get(key): issues.append(f'Missing {key}')
        if not plan.get('pairs'): issues.append('No bounded before/candidate pairs declared')
        for pair in plan.get('pairs',[]):
            paths=[]
            for key in ['before','candidate']:
                item=pair[key];path=dc.local_path(ROOT,item['path'])
                if dc.digest(path)!=item['sha256']: raise ValueError('Stale pair '+item['path'])
                paths.append(path)
            issues.extend(check_pair(*paths,pair['constraints']))
        print(json.dumps({'structural_issues':issues,'visual_approval':'not established','application_authorized':False},indent=2))
        return 1 if issues else 0
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (ValueError,KeyError,IndexError,OSError) as e: raise SystemExit(f'Construction review refused: {e}')
