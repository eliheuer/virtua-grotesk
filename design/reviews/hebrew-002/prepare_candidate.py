#!/usr/bin/env python3
"""HEB-002 scratch candidate. Never writes the active UFOs."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


def shoulder(right, bold):
    # Exact green n outer quadrant, translated; resh's reviewed inner arc.
    if bold:
        return [(right,360,'line',True),(right,488,None),
                (right-80,576,None),(right-208,576,'curve',True)]
    return [(right,352,'line',True),(right,480,None),
            (right-64,576,None),(right-192,576,'curve',True)]


def inner(right, bold):
    if bold:
        return [(right-288,408,'line',True),(right-224,408,None),
                (right-192,376,None),(right-192,304,'curve',True)]
    return [(right-224,480,'line',True),(right-160,480,None),
            (right-96,448,None),(right-96,320,'curve',True)]


def stem_bottom(right, bold):
    inside = right-(192 if bold else 96)
    return [(inside,16),(inside+16,0),(right-16,0),(right,16)]


def he(bold):
    right = 616 if bold else 520
    bar_bottom = 408 if bold else 480
    roof = stem_bottom(right,bold)+shoulder(right,bold)+[
        (72,576),(56,560),(56,bar_bottom+16),(72,bar_bottom)]+inner(right,bold)
    left, edge, top = (64,256,304) if bold else (64,160,376)
    leg = [(left,16),(left+16,0),(edge-16,0),(edge,16),
           (edge,top-16),(edge-16,top),(left+16,top),(left,top-16)]
    return [roof,leg]


def het(bold):
    right = 632 if bold else 536
    left,edge,bar_bottom = (56,248,408) if bold else (56,152,480)
    return [stem_bottom(right,bold)+shoulder(right,bold)+[
        (left+16,576),(left,560),(left,16),(left+16,0),
        (edge-16,0),(edge,16),(edge,bar_bottom-8),
        (edge+8,bar_bottom)]+inner(right,bold)]


def tav(bold):
    right = 672 if bold else 576
    bar_bottom = 408 if bold else 480
    # Green j hook construction translated +40 x, +200 y. For this new
    # machine draft, Bold's optical points are adapted to 8 while retaining
    # its horizontal/vertical tangents. The green donor is never modified.
    if bold:
        outer_leg,inner_leg = 104,296
        hook = [(104,152,'line',True),(104,144,None),(96,136,None),
                (88,136,'curve',True),(32,136),(16,120),(16,16),(32,0),
                (112,0,'line',True),(208,0,None),(296,40,None),(296,152,'curve',True)]
    else:
        outer_leg,inner_leg = 120,216
        hook = [(120,136,'line',True),(120,104,None),(104,80,None),
                (80,80,'curve',True),(32,80),(16,64),(16,16),(32,0),
                (64,0,'line',True),(160,0,None),(216,24,None),(216,152,'curve',True)]
    return [stem_bottom(right,bold)+shoulder(right,bold)+[
        (40,576),(24,560),(24,bar_bottom+16),(40,bar_bottom),
        (outer_leg-8,bar_bottom),(outer_leg,bar_bottom-8)]+hook+[
        (inner_leg,bar_bottom-8),(inner_leg+8,bar_bottom)]+inner(right,bold)]


def point(x,y,kind='line',smooth=False):
    attrs=f'x="{x}" y="{y}"'
    if kind: attrs+=f' type="{kind}"'
    if smooth: attrs+=' smooth="yes"'
    return f'\t\t\t<point {attrs}/>'


def outline(contours):
    return '\t<outline>\n'+''.join('\t\t<contour>\n'+'\n'.join(point(*p) for p in c)+'\n\t\t</contour>\n' for c in contours)+'\t</outline>'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--write',action='store_true')
    a=p.parse_args(); root=Path(__file__).resolve().parents[3]; out=a.output.resolve()
    allowed=(root/'out/qa').resolve()
    if not out.is_relative_to(allowed) or out==allowed or out.exists():
        p.error('Choose a new directory under out/qa')
    if not a.write:
        print(f'Would prepare six scratch glyphs at {out}');return
    sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    evidence=json.loads(Path(__file__).with_name('evidence.json').read_text())
    for rel,entry in evidence['target_sources'].items():
        if sha(root/rel)!=entry['sha256']:p.error(f'Target drift: {rel}')
    references=json.loads(Path(__file__).with_name('reference-sources.json').read_text())
    for rel,entry in references.items():
        if sha(root/rel)!=entry['sha256']:p.error(f'Reference drift: {rel}; remeasure before rebuilding this trial')
    out.mkdir(parents=True)
    shutil.copytree(root/'sources',out/'before-sources',ignore=shutil.ignore_patterns('archive','instance_ufos','build.ninja','.ninja_log','*.png'))
    shutil.copytree(out/'before-sources',out/'sources')
    shutil.copytree(root/'fonts',out/'before-fonts')
    shutil.copytree(root/'scripts',out/'scripts')
    shutil.copytree(root/'tests',out/'tests')
    for n in ['build.sh','Makefile','requirements.txt','OFL.txt']:shutil.copy2(root/n,out/n)
    (out/'.venv').symlink_to(root/'.venv',target_is_directory=True)
    (out/'documentation/proofs').mkdir(parents=True)
    (out/'documentation/source').mkdir(parents=True)
    hashes={str(f.relative_to(root)):sha(f) for f in (root/'sources').rglob('*') if f.is_file() and 'archive' not in f.parts}
    changed=[]
    for master in ['Regular','Bold']:
        bold=master=='Bold'
        for name,fn in [('he-hb',he),('het-hb',het),('tav-hb',tav)]:
            rel=f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif';f=out/rel
            contours=fn(bold)
            assert all(x%8==0 and y%8==0 for c in contours for x,y,*_ in c)
            text,n=re.subn(r'\t<outline>.*?</outline>',lambda _:outline(contours),f.read_text(),flags=re.S);assert n==1
            advance={'he-hb':576,'het-hb':592,'tav-hb':632}[name]+(96 if bold else 0)
            text=re.sub(r'<advance width="\d+"/>',f'<advance width="{advance}"/>',text)
            def anchor(m):
                delta=0 if not bold or m[1] in ['hbHolam','hbCantAboveLeft'] else 96 if m[1]=='hbCantAboveRight' else 48
                # Round ties upward; preserve anchor identity and check shaping.
                snap=lambda value:8*((value+4)//8)
                return f'<anchor name="{m[1]}" x="{snap(int(m[2])+delta)}" y="{snap(int(m[3]))}"/>'
            text=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,text)
            f.write_text(text);changed.append(rel)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'status':'scratch only; application not authorized','reference_glyphs':['n','j','H','E','dalet-hb','resh-hb']},indent=2)+'\n')
    print(out)


if __name__=='__main__':main()
