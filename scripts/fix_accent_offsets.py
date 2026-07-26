import re, glob, os
TOP_MARKS={"acute","grave","circumflex","dieresis","tilde","macron","caron","breve","ring","hungarumlaut","dotaccent"}
def ink_center(path):
    xs=[float(x) for x in re.findall(r'point x="(-?[\d.]+)"',open(path).read())]
    return (min(xs)+max(xs))/2 if xs else None
def snap2(v): return int(round(v/2)*2)
for master in ["Regular","Bold"]:
    G=f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
    centers={}
    def center(name):
        if name not in centers:
            p=f"{G}/{name}.glif"; centers[name]=ink_center(p) if os.path.exists(p) else None
        return centers[name]
    fixed=0
    for gp in glob.glob(f"{G}/*.glif"):
        t=open(gp).read()
        comps=re.findall(r'<component base="([^"]+)"([^/]*)/>',t)
        if len(comps)!=2: continue
        (base,ba),(mark,ma)=comps
        if mark not in TOP_MARKS: continue
        bc,mc=center(base),center(mark)
        if bc is None or mc is None: continue
        newx=snap2(bc-mc)
        # replace the mark component's xOffset
        def repl(m):
            attrs=m.group(1)
            attrs=re.sub(r'\s*xOffset="[^"]*"','',attrs)
            return f'<component base="{mark}"{attrs} xOffset="{newx}"/>'
        t2=re.sub(rf'<component base="{re.escape(mark)}"([^/]*)/>', repl, t)
        if t2!=t: open(gp,"w").write(t2); fixed+=1
    print(f"{master}: recomputed {fixed} top-accent xOffsets")
