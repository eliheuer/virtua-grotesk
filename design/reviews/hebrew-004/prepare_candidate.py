#!/usr/bin/env python3
"""Prepare the authorized HEB-004 trial only in a new out/qa scratch directory."""
import argparse, hashlib, json, re, shutil
from pathlib import Path

TARGETS = ['pe-hb','finalpe-hb']
WIDTHS = {'pe-hb':600,'finalpe-hb':608}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def geometry(b,final=False):
    r=744 if b else 552; i=552 if b else 456
    c=472 if b else 328; h=168 if b else 128; v=168 if b else 184
    ic=440 if b else 304; ih=64 if b else 88; iv=96 if b else 128
    bar=144 if b else 96; left=48; inside=240 if b else 144
    tip=384 if b else 288; low=208 if b else 240; high=320 if b else 336
    # One continuous contour retains the original inward stroke. The bowl's
    # horizontal handles come from Kaf, translated to make room for that stroke.
    if final:
        pts=[(i,-168),(i+16,-184),(r-16,-184),(r,-168),(r,288,'line',True)]
    else:
        pts=[(c,0,'line',True),(c+h,0,None),(r,288-v,None),(r,288,'curve',True)]
    pts += [(r,288+v,None),(c+h,576,None),(c,576,'curve',True),
            (left+16,576),(left,560),(left,low+16),(left+16,low),
            (tip-16,low),(tip,low+16),(tip,high-16),(tip-16,high),
            (inside+8,high),(inside,high+8),(inside,576-bar-8),
            (inside+8,576-bar),(ic,576-bar,'line',True),
            (ic+ih,576-bar,None),(i,288+iv,None),(i,288,'curve',True)]
    if not final:
        pts += [(i,288-iv,None),(ic+ih,bar,None),(ic,bar,'curve',True),
                (left+16,bar),(left,bar-16),(left,16),(left+16,0)]
    return pts

def pe(b): return geometry(b)
def finalpe(b): return geometry(b,True)
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
        for n,fn in zip(TARGETS,[pe,finalpe]):
            rel=f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';p=out/rel;s=p.read_text()
            s,count=re.subn(r'\t<outline>.*?</outline>',lambda _:outline(fn(b)),s,flags=re.S);assert count==1
            width=WIDTHS[n]+(192 if b else 0);s=re.sub(r'<advance width="\d+"/>',f'<advance width="{width}"/>',s)
            anchors=[]
            def anchor(match):
                name,x,y=match.groups();x=int(x);y=int(y)
                snap=lambda v:8*((v+4)//8)
                xx,yy=snap(x),snap(y)
                if name in ['hbHolam','hbCantAboveLeft']: xx=48
                elif name=='hbCantAboveRight': xx=744 if b else 552
                elif name=='hbCenter': xx,yy=(344,376) if b else (264,408)
                else: xx=400 if b else 296
                anchors.append({'name':name,'before':[x,y],'after':[xx,yy]})
                return f'<anchor name="{name}" x="{xx}" y="{yy}"/>'
            s=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,s)
            p.write_text(s);changed.append(rel);metadata.append({'path':rel,'sha256':sha(p),'width':width,'anchors':anchors})
    donors={}
    for m in ['Regular','Bold']:
        for n in ['n','o','H_','E_','kaf-hb','finalkaf-hb']:
            p=root/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';donors[str(p.relative_to(root))]=sha(p)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'metadata':metadata,'donors':donors,'status':'scratch candidate; not applied'},indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
