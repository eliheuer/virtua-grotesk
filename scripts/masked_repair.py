#!/usr/bin/env python3
"""Frozen-data adapter for bounded synthetic repair. No training or source writes."""
import argparse,copy,hashlib,json,math
from pathlib import Path
from frozen_green_dataset import load_split

SCHEMA='virtua-masked-repair-v1'
COORD_MIN,COORD_MAX,DELTA_MAX=-1024,2048,64
# Explicit paired boundaries. These are perturbation recipes, not design rules.
RECIPES={
 'behDotless-ar':{'outer':[(0,1),(0,2)],'inner':[(0,17),(0,18)],'axis':0,'description':'Left bowl handles; stems, terminals and flat floor locked'},
 'meem-ar':{'outer':[(0,9),(0,10),(0,11),(0,12),(0,13)],'inner':[(1,1),(1,2),(1,3),(1,4),(1,5)],'axis':0,'description':'Right bowl boundaries; left stem and tail locked'},
 'reh-ar.fina':{'outer':[(0,17),(0,18)],'inner':[(0,9),(0,10)],'axis':0,'description':'Paired descending-bowl handles; joining edge and terminal locked'},
}

def checked(value, lower, upper):
 if not math.isfinite(value) or not lower<=value<=upper or value%2:raise ValueError('Non-exact or out-of-range value')
 return value

def flatten(record):
 return [(ci,pi,p) for ci,c in enumerate(record['contours']) for pi,p in enumerate(c)]

def example(record,recipe,mode):
 if record['master']!='Regular':raise ValueError('Regular-only pilot')
 input_record=copy.deepcopy(record);maskpoints=set(map(tuple,recipe['outer']+recipe['inner']))
 outer=set(map(tuple,recipe['outer']));inner=set(map(tuple,recipe['inner']))
 if outer&inner or not outer or not inner:raise ValueError('Need distinct paired boundaries')
 valid={(ci,pi) for ci,pi,p in flatten(record)}
 if not maskpoints<=valid:raise ValueError('Recipe point correspondence mismatch')
 if mode not in ('noop','pinch','bulge'):raise ValueError('Unknown mode')
 amp={'noop':0,'pinch':-16,'bulge':16}[mode];axis=('x','y')[recipe['axis']]
 for ci,pi,p in flatten(input_record):
  if (ci,pi) in maskpoints:p[axis]=str(float(p[axis])+(amp if (ci,pi) in outer else -amp))
 coords=[];deltas=[];mask=[];types=[];starts=[]
 for (ci,pi,src),(_,_,target) in zip(flatten(input_record),flatten(record)):
  xy=[checked(float(src[a]),COORD_MIN,COORD_MAX) for a in ('x','y')]
  delta=[checked(float(target[a])-v,-DELTA_MAX,DELTA_MAX) for a,v in zip(('x','y'),xy)]
  coords.append(xy);deltas.append(delta);mask.append(int((ci,pi) in maskpoints));types.append(src.get('type','offcurve'));starts.append(int(pi==0))
 checked(record['advance'],COORD_MIN,COORD_MAX)
 return {'schema':SCHEMA,'glyph':record['glyph'],'master':'Regular','group':record['group'],
   'source_sha256':record['source_sha256'],'mode':mode,'description':recipe['description'],
   'input':input_record,'target':record,'coordinates':coords,'target_deltas':deltas,
   'editable_mask':mask,'point_types':types,'contour_starts':starts,'synthetic':True}

def reconstruct(ex,predicted_deltas):
 if len(predicted_deltas)!=len(ex['coordinates']):raise ValueError('Point count mismatch')
 result=copy.deepcopy(ex['input'])
 for i,(_,_,p) in enumerate(flatten(result)):
  ds=predicted_deltas[i]
  if len(ds)!=2:raise ValueError('Expected x/y deltas')
  for a,d in zip(('x','y'),ds):
   checked(d,-DELTA_MAX,DELTA_MAX)
   if not ex['editable_mask'][i] and d!=0:raise ValueError('Locked point changed')
   p[a]=str(checked(float(p[a])+d,COORD_MIN,COORD_MAX))
 return result

def collate(examples):
 """Plain arrays consumable by MLX/PyTorch; padding contributes no loss.
 Input contains whole glyph coordinates, type, contour start and editable flag.
 Targets are coordinate residuals; no target geometry is put into input features.
 """
 if not examples:raise ValueError('Empty batch')
 n=max(len(e['coordinates']) for e in examples)
 batch={'features':[],'target_deltas':[],'attention_mask':[],'loss_mask':[]}
 for e in examples:
  features=[]
  for xy,kind,start,edit in zip(e['coordinates'],e['point_types'],e['contour_starts'],e['editable_mask']):
   if kind not in ('line','curve','offcurve'):raise ValueError('Unsupported point type')
   features.append([xy[0]/2048,xy[1]/2048,e['input']['advance']/2048,
                    int(kind=='line'),int(kind=='curve'),int(kind=='offcurve'),start,edit])
  count=len(features);pad=n-count
  batch['features'].append(features+[[0]*8 for _ in range(pad)])
  batch['target_deltas'].append(copy.deepcopy(e['target_deltas'])+[[0,0] for _ in range(pad)])
  batch['attention_mask'].append([1]*count+[0]*pad)
  batch['loss_mask'].append(e['editable_mask']+[0]*pad)
 return batch

def prepare(snapshot,digest,out):
 out=Path(out)
 if out.exists():raise ValueError('Output exists; never overwrite a reviewed sample')
 records=load_split(snapshot,digest,'train');byname={r['glyph']:r for r in records if r['master']=='Regular'}
 examples=[]
 for name,recipe in RECIPES.items():
  if name not in byname:raise ValueError('Recipe must name a frozen TRAIN Regular glyph: '+name)
  for mode in ('noop','pinch','bulge'):examples.append(example(byname[name],recipe,mode))
 out.mkdir(parents=True)
 (out/'examples.json').write_text(json.dumps(examples,indent=2)+'\n')
 (out/'batch.json').write_text(json.dumps(collate(examples))+'\n')
 receipt={'schema':SCHEMA,'manifest_sha256':digest,'training_started':False,'source_split':'train',
  'examples':len(examples),'independent_glyphs':len(RECIPES),'modes':['noop','pinch','bulge'],
  'coordinates':[COORD_MIN,COORD_MAX,2],'deltas':[-DELTA_MAX,DELTA_MAX,2],
  'recipe_sha256':hashlib.sha256(json.dumps(RECIPES,sort_keys=True).encode()).hexdigest(),
  'examples_sha256':hashlib.sha256((out/'examples.json').read_bytes()).hexdigest()}
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('snapshot');ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 print(json.dumps(prepare(a.snapshot,a.manifest_sha256,a.out),indent=2))
