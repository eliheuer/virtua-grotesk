#!/usr/bin/env python3
"""Prepare the authorized HEB-003 trial only in a new out/qa scratch directory."""
import argparse, hashlib, json, re, shutil
from pathlib import Path

TARGETS = ['bet-hb','kaf-hb','finalkaf-hb']
WIDTHS = {'bet-hb':544,'kaf-hb':480,'finalkaf-hb':496}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def shoulder(r,b):
    return [(r,360 if b else 352,'line',True),(r,488 if b else 480,None),
            (r-(80 if b else 64),576,None),(r-(208 if b else 192),576,'curve',True)]
def inner(r,b):
    return [(r-(288 if b else 224),408 if b else 480,'line',True),
            (r-(224 if b else 160),408 if b else 480,None),
            (r-(192 if b else 96),376 if b else 448,None),
            (r-(192 if b else 96),304 if b else 320,'curve',True)]
def bet(b):
    r=560 if b else 464; foot=r+64; bar=168 if b else 96; edge=r-(192 if b else 96)
    return [(32,0),(foot-16,0),(foot,16),(foot,bar-16),(foot-16,bar),
            (r+8,bar),(r,bar+8)]+shoulder(r,b)+[
            (56,576),(40,560),(40,576-bar+16),(56,576-bar)]+inner(r,b)+[
            (edge,bar+8),(edge-8,bar),(32,bar),(16,bar-16),(16,16)]
def kaf(b):
    r=528 if b else 432; center=256 if b else 208; handle=168 if b else 128
    vertical=168 if b else 184; i=336; ic=224 if b else 184; ih=64 if b else 88
    iv=80 if b else 128; bar=168 if b else 96
    return [(center,0,'line',True),(center+handle,0,None),(r,288-vertical,None),
            (r,288,'curve',True),(r,288+vertical,None),(center+handle,576,None),
            (center,576,'curve',True),(32,576),(16,560),(16,576-bar+16),
            (32,576-bar),(ic,576-bar,'line',True),(ic+ih,576-bar,None),
            (i,288+iv,None),(i,288,'curve',True),(i,288-iv,None),
            (ic+ih,bar,None),(ic,bar,'curve',True),(32,bar),(16,bar-16),(16,16),(32,0)]
def finalkaf(b):
    r=536 if b else 440;i=r-(192 if b else 96);bottom=-184;bar=168 if b else 96
    return [(i,bottom+16),(i+16,bottom),(r-16,bottom),(r,bottom+16)]+shoulder(r,b)+[
            (32,576),(16,560),(16,576-bar+16),(32,576-bar)]+inner(r,b)
def outline(points):
    lines=[]
    for x,y,*extra in points:
        kind=extra[0] if extra else 'line'; smooth=len(extra)>1 and extra[1]
        a=f'x="{x}" y="{y}"'+(f' type="{kind}"' if kind else '')+(' smooth="yes"' if smooth else '')
        assert x%8==0 and y%8==0
        lines.append('\t\t\t<point '+a+'/>')
    return '\t<outline>\n\t\t<contour>\n'+'\n'.join(lines)+'\n\t\t</contour>\n\t</outline>'
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    root=Path(__file__).resolve().parents[3];out=args.output.resolve();allowed=root/'out/qa'
    if not out.is_relative_to(allowed) or out==allowed or out.exists():parser.error('Use a new directory inside out/qa')
    for r in json.loads(Path(__file__).with_name('source-inspection.json').read_text()):
        assert sha(root/r['path'])==r['sha256'],r['path']
    for rel,digest in json.loads(Path(__file__).with_name('reference-sources.json').read_text()).items():
        assert sha(root/rel)==digest, f'Donor drift: {rel}'
    out.mkdir(parents=True)
    shutil.copytree(root/'sources',out/'before-sources',ignore=shutil.ignore_patterns('archive','instance_ufos','build.ninja','.ninja_log','*.png'))
    shutil.copytree(out/'before-sources',out/'sources');shutil.copytree(root/'fonts',out/'before-fonts')
    for d in ['scripts','tests']:shutil.copytree(root/d,out/d)
    for n in ['build.sh','Makefile','requirements.txt','OFL.txt','README.md','AUTHORS.txt']:
        if (root/n).exists():shutil.copy2(root/n,out/n)
    (out/'.venv').symlink_to(root/'.venv',target_is_directory=True)
    shutil.copytree(root/'documentation',out/'documentation',ignore=shutil.ignore_patterns('*.png','*.pdf','*.ttf','*.woff2','social-assets'))
    hashes={str(f.relative_to(root)):sha(f) for f in (root/'sources').rglob('*') if f.is_file() and 'archive' not in f.parts}
    changed=[];metadata=[]
    for m in ['Regular','Bold']:
        b=m=='Bold'
        for n,fn in zip(TARGETS,[bet,kaf,finalkaf]):
            rel=f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';p=out/rel;s=p.read_text()
            s,count=re.subn(r'\t<outline>.*?</outline>',lambda _:outline(fn(b)),s,flags=re.S);assert count==1
            width=WIDTHS[n]+(96 if b else 0);s=re.sub(r'<advance width="\d+"/>',f'<advance width="{width}"/>',s)
            anchors=[]
            def anchor(match):
                name,x,y=match.groups();x=int(x);y=int(y)
                delta=0 if not b or name in ['hbHolam','hbCantAboveLeft'] else 96 if name=='hbCantAboveRight' else 48
                snap=lambda v:8*((v+4)//8);xx,yy=snap(x+delta),snap(y)
                # Final kaf's below marks sit beside the descender: keep clearance
                # from its inner edge at 344 rather than shifting them into it.
                if n=='finalkaf-hb' and name in ['hbBottom','hbMeteg','hbCantBelow','hbCantBelowRight']: xx=208
                anchors.append({'name':name,'before':[x,y],'after':[xx,yy]})
                return f'<anchor name="{name}" x="{xx}" y="{yy}"/>'
            s=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,s)
            p.write_text(s);changed.append(rel);metadata.append({'path':rel,'sha256':sha(p),'width':width,'anchors':anchors})
    donors={}
    for m in ['Regular','Bold']:
        for n in ['n','o','H_','E_','resh-hb']:
            p=root/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';donors[str(p.relative_to(root))]=sha(p)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'metadata':metadata,'donors':donors,'status':'scratch candidate; not applied'},indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
