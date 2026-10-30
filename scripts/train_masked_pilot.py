#!/usr/bin/env python3
"""Explicitly invoked, capped TRAIN-only memorization pilot. Never edits font sources."""
import argparse,copy,hashlib,json,time
from pathlib import Path
import torch
from torch import nn
import masked_repair as mr
from frozen_green_dataset import load_split

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run(snapshot,manifest_sha,examples_path,out,max_steps=3000,max_seconds=120):
 out=Path(out)
 if out.exists():raise ValueError('Output exists; refusing to overwrite')
 if not 1<=max_steps<=3000 or not 0<max_seconds<=1800:raise ValueError('Pilot cap exceeded')
 records=load_split(snapshot,manifest_sha,'train');byname={r['glyph']:r for r in records if r['master']=='Regular'}
 es=json.loads(Path(examples_path).read_text())
 expected=[mr.example(byname[n],r,m) for n,r in mr.RECIPES.items() for m in ('noop','pinch','bulge')]
 if es!=expected:raise ValueError('Examples do not match frozen TRAIN recipes')
 root=Path(__file__).resolve().parents[1]
 guards={str(p.relative_to(root)):digest(p) for p in (root/'sources').rglob('*') if p.is_file()}
 torch.manual_seed(17);torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 batch=mr.collate(es);features=torch.tensor(batch['features'],dtype=torch.float32)
 # Numeric input only: no glyph names, mode labels or green target coordinates.
 x=features.flatten(1);mean=x.mean(0);scale=x.std(0,unbiased=False).clamp_min(.01);x=(x-mean)/scale
 y=torch.tensor(batch['target_deltas'],dtype=torch.float32)
 mask=torch.tensor(batch['loss_mask'],dtype=torch.float32).unsqueeze(-1)
 points=y.shape[1]
 model=nn.Sequential(nn.Linear(x.shape[1],128),nn.GELU(),nn.Linear(128,128),nn.GELU(),nn.Linear(128,points*2),nn.Tanh())
 optimizer=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=.0001)
 out.mkdir(parents=True);(out/'source-guards.json').write_text(json.dumps(guards))
 config={'seed':17,'device':'cpu','torch':str(torch.__version__),'parameters':sum(p.numel() for p in model.parameters()),'max_steps':max_steps,'max_seconds':max_seconds,'input_features':list(features.shape),'points':points,'normalization':'TRAIN input mean/std floor0.01','output':'tanh *64, hard editable mask; nearest2-unit quantization for scratch reconstruction','task':'memorize nine TRAIN examples, not generalization'}
 (out/'config.json').write_text(json.dumps(config,indent=2))
 start=time.monotonic();history=[];stable=0;reason='step cap';step=0
 for step in range(1,max_steps+1):
  model.train();optimizer.zero_grad();pred=model(x).reshape_as(y)*64
  loss=(((pred-y)/16)**2*mask).sum()/(mask.sum()*2);loss.backward();optimizer.step()
  if step%25==0 or step==1:
   model.eval()
   with torch.no_grad():p=model(x).reshape_as(y)*64*mask;err=(p-y).abs()*mask
   maximum=float(err.max());mae=float(err.sum()/(mask.sum()*2));history.append({'step':step,'seconds':time.monotonic()-start,'masked_mae':mae,'max_error':maximum})
   print(json.dumps(history[-1]),flush=True)
   stable=stable+1 if maximum<.5 else 0
   if stable>=3:reason='all training residuals within0.5 units for3 checks';break
  if time.monotonic()-start>=max_seconds:reason='time cap';break
 model.eval()
 torch.save({'state_dict':model.state_dict(),'mean':mean,'scale':scale,'config':config},out/'checkpoint.pt')
 saved=torch.load(out/'checkpoint.pt',map_location='cpu',weights_only=True);model.load_state_dict(saved['state_dict'])
 with torch.no_grad():raw=model((features.flatten(1)-saved['mean'])/saved['scale']).reshape_as(y)*64*mask
 predictions=[];metrics=[]
 for i,e in enumerate(es):
  n=len(e['coordinates']);d=(raw[i,:n]/2).round()*2
  reconstructed=mr.reconstruct(e,d.tolist());target=torch.tensor(e['target_deltas']);err=(d-target).abs()
  m=torch.tensor(e['editable_mask']).unsqueeze(-1);base=(target.abs()*m).sum()/(m.sum()*2)
  metrics.append({'glyph':e['glyph'],'mode':e['mode'],'exact_after_quantization':bool(torch.equal(d,target)),
    'masked_mae':float((err*m).sum()/(m.sum()*2)),'unchanged_input_masked_mae':float(base),'max_error':float(err.max()),
    'locked_deltas_zero':bool((d*(1-m)).eq(0).all())})
  predictions.append({'example':e,'raw_predicted_deltas':raw[i,:n].tolist(),'predicted_deltas':d.tolist(),'prediction':reconstructed})
 changed=[p for p,h in guards.items() if not (root/p).exists() or digest(root/p)!=h]
 report={'config':config,'manifest_sha256':manifest_sha,'examples_sha256':digest(examples_path),'checkpoint_sha256':digest(out/'checkpoint.pt'),
   'script_sha256':digest(__file__),'steps':step,'seconds':time.monotonic()-start,'stop_reason':reason,'history':history,'metrics':metrics,
   'source_files_checked':len(guards),'changed_sources':changed,'validation_used':False,'test_used':False,'overnight_started':False}
 (out/'predictions.json').write_text(json.dumps(predictions,indent=2));(out/'report.json').write_text(json.dumps(report,indent=2))
 if changed:raise ValueError('Sources changed concurrently; inspect before proceeding')
 print(json.dumps({'steps':step,'exact_examples':sum(m['exact_after_quantization'] for m in metrics),'count':len(metrics),'seconds':report['seconds']}))

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--snapshot',required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--examples',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();run(a.snapshot,a.manifest_sha256,a.examples,a.out)
