#!/usr/bin/env python3
"""HEB-001 v1. Explicit new scratch destination; never writes active sources."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


def point(x, y, kind='line', smooth=False):
    attrs = f'x="{x}" y="{y}"'
    if kind:
        attrs += f' type="{kind}"'
    if smooth:
        attrs += ' smooth="yes"'
    return f'\t\t\t<point {attrs}/>'


def dalet(bold):
    stem_right, stem_left, end, bottom = (440, 248, 504, 408) if bold else (416, 320, 480, 480)
    return [(stem_left,16),(stem_left+16,0),(stem_right-16,0),(stem_right,16),
            (stem_right,bottom-16),(stem_right+16,bottom),(end-16,bottom),
            (end,bottom+16),(end,560),(end-16,576),(80,576),(64,560),
            (64,bottom+16),(80,bottom),(stem_left-8,bottom),(stem_left,bottom-8)]


def resh(bold):
    # Outer shoulder: exact upper-right quadrant of green n, translated only.
    if bold:
        left,inner,right = 48,368,560
        outer=[(right,360,'line',True),(560,488,None),(480,576,None),(352,576,'curve',True)]
        inner_arc=[(272,408,'line',True),(336,408,None),(368,376,None),(368,304,'curve',True)]
        bottom=408
    else:
        left,inner,right = 64,408,504
        outer=[(right,352,'line',True),(504,480,None),(440,576,None),(312,576,'curve',True)]
        inner_arc=[(280,480,'line',True),(344,480,None),(408,448,None),(408,320,'curve',True)]
        bottom=480
    return [(inner,16),(inner+16,0),(right-16,0),(right,16)]+outer+[
        (left+16,576),(left,560),(left,bottom+16),(left+16,bottom)]+inner_arc


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[3]
    out=args.output.resolve()
    scratch_root=(root/'out/qa').resolve()
    if not out.is_relative_to(scratch_root) or out==scratch_root:
        parser.error('Use a new directory beneath repository out/qa')
    if out.exists():
        parser.error('Scratch destination already exists; choose a new one')
    if not args.write:
        print(f'Would snapshot sources/fonts and change only dalet-hb/resh-hb in both scratch masters at {out}')
        return
    evidence=Path(__file__).with_name('candidate-v1-evidence.json')
    if evidence.exists():
        expected=json.loads(evidence.read_text())['expected_before_source_hashes']
        drift=[rel for rel,digest in expected.items() if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest]
        if drift:
            parser.error('Source/reference drift from reviewed v1 baseline: '+', '.join(drift))
    out.mkdir(parents=True)
    shutil.copytree(root/'sources',out/'before-sources',ignore=shutil.ignore_patterns('archive','instance_ufos','build.ninja','.ninja_log','*.png'))
    shutil.copytree(out/'before-sources',out/'sources')
    shutil.copytree(root/'fonts',out/'before-fonts')
    shutil.copytree(root/'scripts',out/'scripts')
    for name in ['build.sh','OFL.txt','Makefile','requirements.txt']:
        shutil.copy2(root/name,out/name)
    (out/'.venv').symlink_to(root/'.venv',target_is_directory=True)
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (root/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts}
    changed=[]
    for master in ['Regular','Bold']:
        for name,fn in [('dalet-hb',dalet),('resh-hb',resh)]:
            rel=f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif'
            p=out/rel
            coords=fn(master=='Bold')
            assert all(x%8==0 and y%8==0 for x,y,*_ in coords)
            outline='\t<outline>\n\t\t<contour>\n'+'\n'.join(point(*v) for v in coords)+'\n\t\t</contour>\n\t</outline>'
            text,n=re.subn(r'\t<outline>.*?</outline>',lambda _:outline,p.read_text(),flags=re.S)
            assert n==1
            p.write_text(text)
            changed.append(rel)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'status':'scratch only; not approved for application'},indent=2)+'\n')
    print(out)


if __name__=='__main__':
    main()
