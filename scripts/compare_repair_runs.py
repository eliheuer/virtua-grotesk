#!/usr/bin/env python3
"""Compare repair evaluations only when their complete frozen inputs match."""
import argparse
import hashlib
import json
from pathlib import Path


def compare(before, after):
    before,after=Path(before),Path(after)
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    if digest(before/'evaluation.json')!=digest(after/'evaluation.json'):
        raise ValueError('Evaluation inputs differ; paired comparison refused')
    a=json.loads((before/'report.json').read_text());b=json.loads((after/'report.json').read_text())
    key=lambda m:(m['cohort'],m['glyph'],m['mode'])
    am={key(m):m for m in a['metrics']};bm={key(m):m for m in b['metrics']}
    if len(am)!=len(a['metrics']) or len(bm)!=len(b['metrics']) or am.keys()!=bm.keys():
        raise ValueError('Evaluation identities differ or repeat')
    rows=[]
    for k in am:
        x,y=am[k],bm[k];delta=y['masked_mae']-x['masked_mae']
        rows.append({'cohort':k[0],'glyph':k[1],'mode':k[2],
                     'before_mae':x['masked_mae'],'after_mae':y['masked_mae'],
                     'change':'better' if delta<0 else 'worse' if delta>0 else 'same'})
    cohorts={}
    for c in sorted({r['cohort'] for r in rows}):
        rs=[r for r in rows if r['cohort']==c]
        cohorts[c]={'count':len(rs),**{v:sum(r['change']==v for r in rs) for v in ('better','worse','same')}}
    return {'before_checkpoint':a['checkpoint_sha256'],'after_checkpoint':b['checkpoint_sha256'],
            'evaluation_sha256':digest(before/'evaluation.json'),'paired':True,'cohorts':cohorts,'rows':rows}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('before');p.add_argument('after');p.add_argument('--out',required=True)
    a=p.parse_args();r=compare(a.before,a.after);Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['cohorts'],indent=2))
