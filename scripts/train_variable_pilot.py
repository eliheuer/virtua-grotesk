#!/usr/bin/env python3
"""One capped Regular-only variable-length pilot, frozen evaluation afterward."""
import argparse
import collections
import hashlib
import json
import random
import time
from pathlib import Path
import torch
import masked_repair as mr
import variable_repair as vr
import evaluate_masked_pilot as old
from frozen_green_dataset import load_split


def signature(e):
    return json.dumps([e['glyph'],e['coordinates'],e['editable_mask']],sort_keys=True)


def clean_wide(record,cohort):
    mask={i for i,(_,_,p) in enumerate(mr.flatten(record)) if 'type' not in p}
    if not mask:mask=set(range(len(mr.flatten(record))))
    return vr.make_example(record,mask,{},'clean-wide',cohort)


def run(snapshot,out):
    out=Path(out)
    if out.exists():raise ValueError('Never overwrite a pilot')
    root=Path(__file__).resolve().parents[1];guards=old.snapshot_files(root)
    train=[r for r in load_split(snapshot,old.MANIFEST,'train') if r['master']=='Regular' and '-ar' in r['glyph']]
    held=[r for r in load_split(snapshot,old.MANIFEST,'validation') if r['master']=='Regular' and r['glyph'] in old.HAH_RECIPES]
    if {r['group'] for r in train}&{r['group'] for r in held}:raise ValueError('Group leakage')
    rng=random.Random(731);training=[]
    for r in train:
        training.append(clean_wide(r,'train'))
        for _ in range(6):
            for mode in ('single','cluster','paired-x','paired-y','jitter'):
                ex=vr.synthetic(r,rng,mode);training.append(ex)
                # Matching mask, authentic green coordinates, zero residual; no invented smoothing target.
                training.append(vr.make_example(r,{i for i,v in enumerate(ex['editable_mask']) if v},{},'noop','train'))
    byname={r['glyph']:r for r in train+held};evaluation=[]
    for recipes,split in ((mr.RECIPES,'train'),(old.HAH_RECIPES,'validation')):
        for name,recipe in recipes.items():
            for mode in old.VARIANTS:
                e=old.make_example(byname[name],recipe,mode,split)
                e['cohort']='hah-probes' if split=='validation' else 'familiar-fixed-probes'
                evaluation.append(e)
    evaluation += [clean_wide(r,'hah-clean-wide') for r in held]
    evaluation += [clean_wide(r,'train-clean-wide') for r in train]
    fingerprints={signature(e) for e in training};rng_eval=random.Random(919)
    for name in mr.RECIPES:
        for i in range(6):
            for attempt in range(100):
                e=vr.synthetic(byname[name],rng_eval,'single' if i<3 else 'jitter','new-corruption-draw')
                if signature(e) not in fingerprints:break
            else:raise ValueError('Could not make a novel evaluation draw')
            e['mode']=f'new-draw-{i+1}';evaluation.append(e)
    out.mkdir(parents=True)
    config={'schema':vr.SCHEMA,'seed':83,'data_seed':731,'evaluation_seed':919,'max_steps':1800,'max_seconds':180,
            'batch_size':24,'lr':.001,'clean_loss_weight':2,'normalization':'fixed1024 units; no corpus-dependent variance scaling',
            'parameters':None,'train_drawings':len(train),'train_families':len({r['group'] for r in train}),
            'train_examples':len(training),'heldout_drawings':len(held),'heldout_families':len({r['group'] for r in held}),
            'train_points':sorted({len(mr.flatten(r)) for r in train}),'heldout_points':[len(mr.flatten(r)) for r in held],
            'torch':str(torch.__version__),'output':'tanh*32, hard mask, nearest2; no confidence filter or hidden fallback'}
    torch.set_num_threads(1);torch.manual_seed(83);torch.use_deterministic_algorithms(True)
    model=vr.VariableRepair();config['parameters']=sum(p.numel() for p in model.parameters())
    protocol={'config':config,'manifest_sha256':old.MANIFEST,'source_guards':guards,
              'evaluation_policy':'last checkpoint only; no validation selection, no test split, no tuning after results',
              'model_script_sha256':old.digest(vr.__file__),'runner_sha256':old.digest(__file__)}
    for name,data in [('protocol',protocol),('training',training),('evaluation',evaluation)]:
        (out/f'{name}.json').write_text(json.dumps(data)+'\n')
    # Precompute from training inputs only. Targets are a separate tensor.
    tensors=vr.collate(training)
    groups=collections.defaultdict(list)
    for i,e in enumerate(training):groups[e['group']].append(i)
    group_names=sorted(groups);draw=random.Random(83)
    optimizer=torch.optim.AdamW(model.parameters(),lr=config['lr'],weight_decay=.0001)
    start=time.monotonic();history=[]
    for step in range(1,config['max_steps']+1):
        ids=[draw.choice(groups[draw.choice(group_names)]) for _ in range(config['batch_size'])]
        x,nb,sp,v,m,y=[t[ids] for t in tensors]
        pred=model(x,nb,sp,v,m)
        clean=y.abs().sum((1,2)).eq(0).float()
        weights=1+clean
        per_example=(((pred-y)/16)**2*m.unsqueeze(-1)).sum((1,2))/(m.sum(1)*2).clamp_min(1)
        loss=(per_example*weights).mean()
        optimizer.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1);optimizer.step()
        if step%100==0 or step==1:
            row={'step':step,'seconds':time.monotonic()-start,'training_batch_loss':float(loss.detach())}
            history.append(row);print(json.dumps(row),flush=True)
        if time.monotonic()-start>=config['max_seconds']:break
    training_seconds=time.monotonic()-start
    torch.save({'state_dict':model.state_dict(),'config':config},out/'checkpoint.pt')
    saved=torch.load(out/'checkpoint.pt',map_location='cpu',weights_only=True)
    model=vr.VariableRepair();model.load_state_dict(saved['state_dict']);model.eval();model.requires_grad_(False)
    predictions=[];metrics=[]
    for ex in evaluation:
        x,nb,sp,v,m,y=vr.collate([ex])
        with torch.inference_mode():raw=model(x,nb,sp,v,m)[0]
        delta=(raw/2).round()*2;target=y[0];mask=m[0,:,None]
        result=mr.reconstruct(ex,delta.tolist())
        base=float((target.abs()*mask).sum()/(mask.sum()*2));err=float(((delta-target).abs()*mask).sum()/(mask.sum()*2))
        metric={'glyph':ex['glyph'],'mode':ex['mode'],'cohort':ex['cohort'],'point_count':len(ex['coordinates']),
                'exact_after_quantization':bool(delta.eq(target).all()),'masked_mae':err,'unchanged_input_masked_mae':base,
                'raw_masked_mae':float(((raw-target).abs()*mask).sum()/(mask.sum()*2)),
                'max_error':float((delta-target).abs().max()),'locked_deltas_zero':bool((delta*(1-mask)).eq(0).all()),
                'changed_points':int(delta.ne(0).any(-1).sum()),'outcome':'improved' if err<base else 'worse' if err>base else 'tied'}
        metrics.append(metric);predictions.append({'example':ex,'raw_predicted_deltas':raw.tolist(),'predicted_deltas':delta.tolist(),'prediction':result})
    aggregates={}
    for cohort in sorted({m['cohort'] for m in metrics}):
        rows=[m for m in metrics if m['cohort']==cohort]
        aggregates[cohort]={'count':len(rows),'exact':sum(r['exact_after_quantization'] for r in rows),
            **{k:sum(r['outcome']==k for r in rows) for k in ('improved','worse','tied')},
            'mean_case_mae':sum(r['masked_mae'] for r in rows)/len(rows),
            'mean_case_input_mae':sum(r['unchanged_input_masked_mae'] for r in rows)/len(rows)}
    assert old.snapshot_files(root)==guards,'Font/source changed'
    report={'evaluation_only':True,'model_kind':vr.SCHEMA,'checkpoint_path':str((out/'checkpoint.pt').resolve()),
            'checkpoint_sha256':old.digest(out/'checkpoint.pt'),'manifest_sha256':old.MANIFEST,'config':config,
            'steps':step,'training_seconds':training_seconds,'history':history,'metrics':metrics,'aggregates':aggregates,
            'protocol_sha256':old.digest(out/'protocol.json'),'training_sha256':old.digest(out/'training.json'),
            'evaluation_sha256':old.digest(out/'evaluation.json'),'font_source_files_unchanged':len(guards),
            'test_split_used':False,'validation_used_for_training_or_checkpoint_selection':False,'overnight_started':False}
    for name,data in [('report',report),('predictions',predictions)]:
        (out/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'steps':step,'seconds':training_seconds,'aggregates':aggregates},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--snapshot',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();run(a.snapshot,a.out)
