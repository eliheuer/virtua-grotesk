#!/usr/bin/env python3
"""Prepare the authorized HEB-005 trial only in a new out/qa scratch directory."""
import argparse, hashlib, json, re, shutil
from pathlib import Path

TARGETS = ['mem-hb','finalmem-hb','samekh-hb']
WIDTHS = {'mem-hb':608,'finalmem-hb':600,'samekh-hb':640}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def mem(b):
    r=656 if b else 560; c=448 if b else 368; i=464; bar=168 if b else 96
    join=304 if b else 224; leg=240 if b else 144
    top=432 if b else 496; ic=384 if b else 336
    return [[(320,0),(r-16,0),(r,16),(r,376 if b else 368,'line',True),
        (r,504 if b else 496,None),(r-(80 if b else 64),592,None),(c,592,'curve',True),
        (c-64,592,None),(join+32,568,None),(join,512,'curve'),(join-8,512),
        (join-48,576),(64,576),(48,560),(152,400),(48,16),(64,0),
        (leg-16,0),(leg,16),(304 if b else 240,272 if b else 400,'line',True),
        (336 if b else 256,400 if b else 464,None),(336 if b else 288,top,None),
        (ic,top,'curve',True),(ic+64,top,None),(i,400 if b else 464,None),
        (i,328 if b else 336,'curve',True),(i,bar+8),(i-8,bar),
        (320,bar),(304,bar-16),(304,16)]]

def finalmem(b):
    r=648 if b else 552; i=456; left=240 if b else 144; bar=168 if b else 96
    return [[(64,0),(r-16,0),(r,16),(r,360 if b else 352,'line',True),
        (r,488 if b else 480,None),(r-(80 if b else 64),576,None),
        (r-(208 if b else 192),576,'curve',True),(64,576),(48,560),(48,16)],
        [(i,bar+8),(i-8,bar),(left+8,bar),(left,bar+8),(left,576-bar-8),
        (left+8,576-bar),(r-(288 if b else 224),576-bar,'line',True),
        (r-(224 if b else 160),576-bar,None),(i,376 if b else 448,None),
        (i,304 if b else 320,'curve',True)]]

def samekh(b):
    c=352 if b else 320; r=664 if b else 592; left=40 if b else 48
    h=176 if b else 144; v=176 if b else 192; bar=144 if b else 96
    i=464 if b else 496; il=240 if b else 144; ih=64 if b else 96
    bottom=128 if b else 80; top=576-bar; tl=280 if b else 184
    return [[(c,-16,'curve',True),(c+h,-16,None),(r,288-v,None),(r,288,'curve',True),
        (r,464,None),(c+h,576,None),(c,576,'curve',True),
        (32,576),(16,560),(16,top+16),(32,top),(64 if b else 80,top),
        (72 if b else 88,top-8),(48 if b else 64,392 if b else 424,None),
        (left,344 if b else 352,None),(left,288,'curve',True),
        (left,288-v,None),(c-h,-16,None)],
        [(c,bottom,'curve',True),(c-ih,bottom,None),(il,192 if b else 160,None),
        (il,288,'curve',True),(il,368,None),(il+16,top-24,None),
        (tl-8,top-8,'curve'),(tl,top),(c,top,'line',True),(c+ih,top,None),
        (i,384 if b else 416,None),(i,288,'curve',True),
        (i,192 if b else 160,None),(c+ih,bottom,None)]]

def outline(contours):
    result=['\t<outline>']
    for points in contours:
        result.append('\t\t<contour>')
        for x,y,*extra in points:
            kind=extra[0] if extra else 'line'; smooth=len(extra)>1 and extra[1]
            a=f'x="{x}" y="{y}"'+(f' type="{kind}"' if kind else '')+(' smooth="yes"' if smooth else '')
            assert x%8==0 and y%8==0,(x,y)
            result.append('\t\t\t<point '+a+'/>')
        result.append('\t\t</contour>')
    return '\n'.join(result+['\t</outline>'])
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
        for n,fn in zip(TARGETS,[mem,finalmem,samekh]):
            rel=f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';p=out/rel;s=p.read_text()
            s,count=re.subn(r'\t<outline>.*?</outline>',lambda _:outline(fn(b)),s,flags=re.S);assert count==1
            width=WIDTHS[n]+((64 if n=='samekh-hb' else 96) if b else 0);s=re.sub(r'<advance width="\d+"/>',f'<advance width="{width}"/>',s)
            anchors=[]
            def anchor(match):
                name,x,y=match.groups();x=int(x);y=int(y)
                snap=lambda v:8*((v+4)//8)
                xx,yy=snap(x),snap(y)
                center={'mem-hb':(320,368),'finalmem-hb':(304,352),'samekh-hb':(320,352)}[n][int(b)]
                xx=center
                if name in ['hbHolam','hbCantAboveLeft']: xx=16 if n=='samekh-hb' else 48
                if name=='hbCantAboveRight': xx=width-(40 if b and n=='samekh-hb' else 48)
                if name=='hbCenter': yy=288
                if n=='mem-hb' and name in ['hbHolam','hbCantAbove','hbCantAboveLeft','hbCantAboveRight']: yy=592
                if n=='mem-hb' and name=='hbRafe': yy=688
                anchors.append({'name':name,'before':[x,y],'after':[xx,yy]})
                return f'<anchor name="{name}" x="{xx}" y="{yy}"/>'
            s=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,s)
            p.write_text(s);changed.append(rel);metadata.append({'path':rel,'sha256':sha(p),'width':width,'anchors':anchors})
    donors={}
    for m in ['Regular','Bold']:
        for n in ['n','o','H_','E_','kaf-hb','resh-hb']:
            p=root/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';donors[str(p.relative_to(root))]=sha(p)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'metadata':metadata,'donors':donors,'status':'scratch candidate; not applied'},indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
