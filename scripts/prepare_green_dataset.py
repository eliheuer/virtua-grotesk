#!/usr/bin/env python3
"""Freeze a conservative green-only pilot corpus. Does not train or alter sources."""
import argparse, collections, hashlib, json, shutil, unicodedata
from pathlib import Path
import xml.etree.ElementTree as ET
import design_context as dc
ROOT=Path(__file__).resolve().parents[1]

def build(root, out):
    if out.exists(): raise ValueError('Output already exists; choose a new snapshot')
    contract=dc.read_json(root/'design/system/contract.json')
    masters={m:dc.load_master(root,m,contract) for m in ('Regular','Bold')}
    # Shared marks do not carry letter-body supervision in this pilot.
    shared_marks={n for records in masters.values() for n,r in records.items()
                  if '-ar' in n and (n.startswith(('dot','twodots','threedots')) or
                    (r['unicodes'] and all(unicodedata.category(chr(cp)).startswith('M') for cp in r['unicodes'])))}
    parent={n:n for records in masters.values() for n in records}
    def find(n):
        while parent[n]!=n: n=parent[n]
        return n
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b: parent[max(a,b)]=min(a,b)
    families={}
    # Conservative family ties across masters, suffix variants and canonical accents.
    for records in masters.values():
        for n,r in records.items():
            keys=[n.split('.')[0]]
            for cp in r['unicodes']:
                keys.append('unicode:'+unicodedata.normalize('NFD',chr(cp))[0])
            for key in keys:
                if key in families: union(n,families[key])
                families[key]=n
            for c in r['components']:
                if c['base'] in parent and c['base'] not in shared_marks and n not in shared_marks: union(n,c['base'])
    # Independent contours can share construction without component links.
    for family in [('beh','teh','theh','noon','yeh'),('jeem','hah','khah'),('dal','thal','ddal'),('reh','zain'),('seen','sheen'),('sad','dad'),('tah','zah'),('ain','ghain'),('feh','qaf'),('kaf','gaf'),('b','d','p','q'),('n','h','m','u')]:
        ns=[n for n in parent if n.split('.')[0].removesuffix('-ar').replace('Dotless','') in family]
        for n in ns[1:]:union(ns[0],n)
    # Identical contours also stay together, independent of glyph names.
    shapes={}
    for records in masters.values():
        for n,r in records.items():
            d=ET.parse(root/r['path']).find('outline')
            key=ET.tostring(d) if d is not None else None
            if key and r['contours']:
                if key in shapes:union(n,shapes[key])
                shapes[key]=n
    groups=collections.defaultdict(list)
    for n in parent:groups[find(n)].append(n)
    group_ids={n:hashlib.sha256('\n'.join(sorted(ns)).encode()).hexdigest()[:16] for ns in groups.values() for n in ns}
    test_groups={group_ids[n] for n in parent if n.split('.')[0] in ('seen-ar','sheen-ar')}
    validation_groups={group_ids[n] for n in parent if n.split('.')[0] in ('hah-ar','jeem-ar','khah-ar')}
    if test_groups & validation_groups: raise ValueError('Arabic holdout families unexpectedly connected')
    arabic_groups={group_ids[n] for n in parent if '-ar' in n}
    def split(n):
        group=group_ids[n]
        if group in test_groups: return 'test'
        if group in validation_groups: return 'validation'
        if group in arabic_groups: return 'train'
        v=int(group,16)%10
        return 'test' if v==0 else 'validation' if v==1 else 'train'
    def approved(r):
        c=r['color']
        return c['reference_eligible'] and c['label'] in (None,'green')
    rows=[];excluded=[];guards={}
    for master,records in masters.items():
        for n,r in records.items():
            guards[r['path']]=r['sha256']
            if not approved(r):excluded.append({'master':master,'glyph':n,'reason':'not unambiguously green','color':r['color']});continue
            if n in shared_marks:
                excluded.append({'master':master,'glyph':n,'reason':'shared mark: reference only, never body supervision'});continue
            closure=set();errors=[]
            def visit(name,stack):
                if name in stack: errors.append('component cycle');return
                if name not in records:errors.append('missing donor '+name);return
                if name in closure:return
                closure.add(name)
                if not approved(records[name]):errors.append('non-green donor '+name)
                for c in records[name]['components']:visit(c['base'],stack|{name})
            visit(n,set())
            if errors:excluded.append({'master':master,'glyph':n,'reason':errors});continue
            if r['components'] or not r['contours']:
                excluded.append({'master':master,'glyph':n,'reason':'composite/empty: reference only; direct-outline pilot'});continue
            d=ET.parse(root/r['path']);coords=[float(p.get(k)) for p in d.findall('.//point') for k in ('x','y')]
            if r['off_2_points'] or r['advance'] is None or r['advance']%2:
                excluded.append({'master':master,'glyph':n,'reason':'non-exact 2-unit codec; preserve human optics, no resnap'});continue
            rows.append({**r,'group':group_ids[n],'split':split(n),'dependencies':sorted(closure),
                         'range':[min(coords+[r['advance']]),max(coords+[r['advance']])],
                         'legacy_codec_compatible':all(-512<=v<=1280 for v in coords+[r['advance']])})
    pairs=[]
    a={r['glyph']:r for r in rows if r['master']=='Regular'};b={r['glyph']:r for r in rows if r['master']=='Bold'}
    for n in sorted(a.keys()&b.keys()):
        if a[n]['point_types']==b[n]['point_types']:
            pairs.append({'glyph':n,'group':group_ids[n],'split':split(n),'regular':a[n]['path'],'bold':b[n]['path']})
    for ns in groups.values():assert len({split(n) for n in ns})==1
    # Refuse a concurrent human save before freezing exact copies.
    for path,digest in guards.items():
        if dc.digest(root/path)!=digest:raise ValueError('Source changed: '+path)
    out.mkdir(parents=True)
    for r in rows:
        dest=out/r['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/r['path'],dest)
        assert dc.digest(dest)==r['sha256']
    summary={'eligible':len(rows),'pairs':len(pairs),'by_master_split':dict(collections.Counter(r['master']+'/'+r['split'] for r in rows)),
             'pairs_by_split':dict(collections.Counter(p['split'] for p in pairs)),
             'legacy_out_of_range':sum(not r['legacy_codec_compatible'] for r in rows),
             'coordinate_and_advance_range':[min(r['range'][0] for r in rows),max(r['range'][1] for r in rows)],
             'groups':len({r['group'] for r in rows}),'excluded':len(excluded),
             'arabic_by_master_split':dict(collections.Counter(r['master']+'/'+r['split'] for r in rows if '-ar' in r['glyph']))}
    manifest={'schema':1,'training_authorized':False,'split_status':'proposed explicit Arabic holdouts; awaiting user review',
              'policy':{'shared_marks':sorted(shared_marks),'shared_mark_rule':'Reference only: excluded from body supervision; mark edges do not merge body families',
                        'test':'Seen/Sheen family','validation':'Hah/Jeem/Khah family','training':'Other Arabic body groups; deterministic grouped split for non-Arabic'},
              'group_members':{group_ids[ns[0]]:sorted(ns) for ns in groups.values()},
              'summary':summary,'rows':rows,'pairs':pairs,'excluded':excluded,'source_guards':guards}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(summary,indent=2));return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();build(ROOT,args.out.resolve())
