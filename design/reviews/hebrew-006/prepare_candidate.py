#!/usr/bin/env python3
"""Prepare the authorized HEB-006 trial only in a new out/qa scratch directory."""
import argparse, hashlib, json, re, shutil
from pathlib import Path

TARGETS = ['yod-hb','vav-hb','zayin-hb','nun-hb','finalnun-hb']
WIDTHS = {'yod-hb':240,'vav-hb':240,'zayin-hb':304,'nun-hb':336,'finalnun-hb':240}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def stem(b, bottom):
    l=72; r=264 if b else 168
    return [[(l+16,bottom),(r-16,bottom),(r,bottom+16),(r,560),
             (r-16,576),(l+16,576),(l,560),(l,bottom+16)]]
def yod(b): return stem(b,240)
def vav(b): return stem(b,0)
def finalnun(b): return stem(b,-128)
def zayin(b):
    # A level crown with a shallow, parallel offset into the straight stem.
    # Rubik informs the structure; Virtua's 16-unit cuts and weights remain.
    l=136 if b else 88; r=328 if b else 184; edge=416 if b else 288
    bar=144 if b else 96; underside=576-bar; sy=underside-128
    return [[(l+16,0),(r-16,0),(r,16),(r,sy,'line',True),
        (r,sy+64,None),(r+8,underside-32,None),(r+24,underside,'curve'),
        (edge-16,underside),(edge,underside+16),(edge,560),
        (edge-16,576),(32,576),(16,560),(16,underside+16),
        (32,underside),(l+24,underside),
        (l+8,underside-32,None),(l,sy+64,None),(l,sy,'curve',True),(l,16)]]
def nun(b):
    r=376 if b else 280; i=184; bar=168 if b else 96; top=576-bar
    return [[(32,0),(r-16,0),(r,16),(r,360 if b else 352,'line',True),
        (r,488 if b else 480,None),(r-(80 if b else 64),576,None),
        (r-(208 if b else 192),576,'curve',True),
        (48,576),(32,560),(32,top+16),(48,top),
        (r-(288 if b else 224),top,'line',True),
        (r-(224 if b else 160),top,None),(i,376 if b else 448,None),
        (i,304 if b else 320,'curve',True),(i,bar+8),(i-8,bar),
        (32,bar),(16,bar-16),(16,16)]]

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
        for n,fn in zip(TARGETS,[yod,vav,zayin,nun,finalnun]):
            rel=f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';p=out/rel;s=p.read_text()
            s,count=re.subn(r'\t<outline>.*?</outline>',lambda _:outline(fn(b)),s,flags=re.S);assert count==1
            width=WIDTHS[n]+((128 if n=='zayin-hb' else 96) if b else 0);s=re.sub(r'<advance width="\d+"/>',f'<advance width="{width}"/>',s)
            anchors=[]
            def anchor(match):
                name,x,y=match.groups();x=int(x);y=int(y)
                snap=lambda v:8*((v+4)//8)
                xx,yy=snap(x),snap(y)
                center={'yod-hb':(120,168),'vav-hb':(120,168),'finalnun-hb':(120,168),'zayin-hb':(136,232),'nun-hb':(144,192)}[n][int(b)]
                xx=center
                if name=='hbCenter':
                    xx=0 if n in ['yod-hb','vav-hb','finalnun-hb'] else ((88 if b else 40) if n=='zayin-hb' else 96)
                    yy=320 if n in ['yod-hb','vav-hb','finalnun-hb'] else 288
                if name=='hbHolam': xx=center if n=='vav-hb' else (72 if n in ['yod-hb','finalnun-hb'] else (16 if n=='zayin-hb' else 32)); yy=576
                if name in ['hbCantAbove','hbCantAboveLeft','hbCantAboveRight']: yy=576
                if name=='hbCantAboveLeft': xx=72 if n in ['yod-hb','vav-hb','finalnun-hb'] else 16
                if name=='hbCantAboveRight': xx=width-(72 if n in ['yod-hb','vav-hb','finalnun-hb'] else (16 if n=='zayin-hb' else 56))
                if name=='hbRafe': yy=672
                anchors.append({'name':name,'before':[x,y],'after':[xx,yy]})
                return f'<anchor name="{name}" x="{xx}" y="{yy}"/>'
            s=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,s)
            p.write_text(s);changed.append(rel);metadata.append({'path':rel,'sha256':sha(p),'width':width,'anchors':anchors})
    donors={}
    for m in ['Regular','Bold']:
        for n in ['n','H_','E_','resh-hb','finalkaf-hb']:
            p=root/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif';donors[str(p.relative_to(root))]=sha(p)
    (out/'scope.json').write_text(json.dumps({'source_hashes':hashes,'changed_files':changed,'metadata':metadata,'donors':donors,'status':'scratch candidate; not applied'},indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
