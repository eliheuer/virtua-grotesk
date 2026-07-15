"""Curve fairness lint: the checks stroke/grid lints can't see.

1. CREST CENTERING: in a 4-extrema arc run, the top/bottom crest x
   should sit at the midpoint of the side extrema (and side crest y at
   the midpoint of top/bottom) unless deliberately off. Flags offsets
   > TOL. This is the "egg-shaped counter" detector.
2. TENSION BREAKS: at every smooth on-curve point, the incoming and
   outgoing curvature magnitudes should be comparable; big ratios read
   as lumps even when everything is on-grid.

    ./.venv/bin/python scripts/curve_lint.py Bold b d o
    ./.venv/bin/python scripts/curve_lint.py Regular --all
"""
import argparse, math, re, os

TOL_CREST = 6
TENSION_RATIO = 2.6

def parse(src):
    conts=[]
    for cm in re.finditer(r'<contour>(.*?)</contour>', src, re.S):
        pts=[]
        for m in re.finditer(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
                             r'((?: type="(\w+)")?( smooth="yes")?)/>', cm.group(1)):
            pts.append(dict(x=float(m.group(1)), y=float(m.group(2)),
                            on=bool(m.group(4)), smooth=bool(m.group(5))))
        conts.append(pts)
    return conts

def bez(p0,p1,p2,p3,t):
    mt=1-t
    return (mt**3*p0[0]+3*mt*mt*t*p1[0]+3*mt*t*t*p2[0]+t**3*p3[0],
            mt**3*p0[1]+3*mt*mt*t*p1[1]+3*mt*t*t*p2[1]+t**3*p3[1])

def curvature(p0,p1,p2,p3,t):
    mt=1-t
    d1=(3*mt*mt*(p1[0]-p0[0])+6*mt*t*(p2[0]-p1[0])+3*t*t*(p3[0]-p2[0]),
        3*mt*mt*(p1[1]-p0[1])+6*mt*t*(p2[1]-p1[1])+3*t*t*(p3[1]-p2[1]))
    d2=(6*mt*(p2[0]-2*p1[0]+p0[0])+6*t*(p3[0]-2*p2[0]+p1[0]),
        6*mt*(p2[1]-2*p1[1]+p0[1])+6*t*(p3[1]-2*p2[1]+p1[1]))
    num=abs(d1[0]*d2[1]-d1[1]*d2[0]); den=(d1[0]**2+d1[1]**2)**1.5
    return num/den if den>1e-9 else 0.0

def segments(cont):
    n=len(cont); ons=[i for i,p in enumerate(cont) if p['on']]
    segs=[]
    for k in range(len(ons)):
        i0,i1=ons[k],ons[(k+1)%len(ons)]
        mid=[]; j=(i0+1)%n
        while j!=i1:
            mid.append(cont[j]); j=(j+1)%n
        if len(mid)==2:
            segs.append((cont[i0],mid[0],mid[1],cont[i1]))
    return segs

def lint_glyph(path, name):
    conts=parse(open(path).read())
    issues=[]
    for ci,cont in enumerate(conts):
        segs=segments(cont)
        if not segs: continue
        # crest centering: on-curve smooth extrema with H or V tangents
        ons=[p for p in cont if p['on']]
        h=[p for p in ons if p['smooth']]
        xs=[p['x'] for p in h]; ys=[p['y'] for p in h]
        if len(h)>=4:
            left=min(h,key=lambda p:p['x']); right=max(h,key=lambda p:p['x'])
            top=max(h,key=lambda p:p['y']); bot=min(h,key=lambda p:p['y'])
            if len({id(left),id(right),id(top),id(bot)})==4:
                midx=(left['x']+right['x'])/2
                midy=(top['y']+bot['y'])/2
                for crest,axis,mid in ((top,'x',midx),(bot,'x',midx),
                                       (left,'y',midy),(right,'y',midy)):
                    off=crest[axis]-mid
                    if abs(off)>TOL_CREST:
                        issues.append(f'contour {ci}: crest ({crest["x"]:g},{crest["y"]:g}) '
                                      f'off-center {axis} by {off:+.0f}')
        # tension breaks at smooth joints
        for k in range(len(segs)):
            a=segs[k]; b_=segs[(k+1)%len(segs)]
            if a[3] is not b_[0] or not a[3]['smooth']: continue
            ka=curvature(*[(p['x'],p['y']) for p in a],0.98)
            kb=curvature(*[(p['x'],p['y']) for p in b_],0.02)
            hi,lo=max(ka,kb),min(ka,kb)
            if lo>1e-6 and hi/lo>TENSION_RATIO:
                issues.append(f'contour {ci}: tension break at '
                              f'({a[3]["x"]:g},{a[3]["y"]:g}) ratio {hi/lo:.1f}')
    return issues

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('master',choices=['Regular','Bold'])
    ap.add_argument('glyphs',nargs='*')
    ap.add_argument('--all',action='store_true')
    a=ap.parse_args()
    gdir=f'sources/VirtuaGrotesk-{a.master}.ufo/glyphs'
    names=a.glyphs
    if a.all:
        import plistlib
        names=sorted(plistlib.load(open(f'{gdir}/contents.plist','rb')))
    bad=0
    for g in names:
        fn=g if g.islower() or len(g)>1 else g+'_'
        path=f'{gdir}/{fn}.glif'
        if not os.path.exists(path): continue
        issues=lint_glyph(path,g)
        if issues:
            bad+=1
            print(f'{a.master} {g}:')
            for i in issues: print('  '+i)
    print(f'{bad} glyphs flagged' if bad else 'all clean')

if __name__=='__main__':
    main()
