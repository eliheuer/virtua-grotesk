#!/usr/bin/env python3
"""Fixed-checkpoint development evaluation; no optimizer, font writes or clipping."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import torch
from torch import nn
import masked_repair as mr
from frozen_green_dataset import load_split

MANIFEST = 'a4135c690ecb830987fa6dd873a4e645508da71e20abe74eeb8f2397d9c76e19'
CHECKPOINT = '184436f31b6e9122f4920c0b56f4b50c4c5d77fd26f7bc3d5ef8321a379092d9'
# Fixed before inference: shared left-crown boundary handles, not terminal points.
HAH_RECIPES = {
    'hah-ar.init': {'outer': [(0,12),(0,13)], 'inner': [(0,19),(0,20)]},
    'hah-ar.medi': {'outer': [(0,23),(0,24)], 'inner': [(0,30),(0,31)]},
    'hah-ar.fina': {'outer': [(0,30),(0,31)], 'inner': [(0,37),(0,38)]},
}
VARIANTS = {
    'noop': (0,0,0),
    'paired-x-minus8': (0,-8,8),
    'paired-x-plus8': (0,8,-8),
    'paired-x-minus24': (0,-24,24),
    'paired-x-plus24': (0,24,-24),
    'paired-y-plus16': (1,16,-16),
    'outer-only-x-plus16': (0,16,0),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot_files(root):
    return {str(p.relative_to(root)): digest(p)
            for folder in ('sources','fonts') for p in (root/folder).rglob('*') if p.is_file()}


def make_example(record, recipe, mode, split):
    recipe = {**recipe, 'axis': 0, 'description': 'Fixed paired-boundary development evaluation'}
    ex = mr.example(record, recipe, 'noop')
    axis, outer_delta, inner_delta = VARIANTS[mode]
    outer, inner = set(map(tuple,recipe['outer'])), set(map(tuple,recipe['inner']))
    for i,(ci,pi,p) in enumerate(mr.flatten(ex['input'])):
        delta = outer_delta if (ci,pi) in outer else inner_delta if (ci,pi) in inner else 0
        key = ('x','y')[axis]
        value = mr.checked(float(p[key])+delta, mr.COORD_MIN,mr.COORD_MAX)
        p[key] = str(value)
        ex['coordinates'][i][axis] = value
        ex['target_deltas'][i][axis] = -delta
    ex['mode'],ex['split'] = mode,split
    ex['cohort'] = 'heldout-hah' if split=='validation' else 'training-noop-control' if mode=='noop' else 'unfamiliar-corruption'
    return ex


def input_tensor(ex, points):
    count = len(ex['coordinates'])
    if count>points:
        raise ValueError(f'Unsupported point count {count}>{points}; no truncation')
    batch = mr.collate([ex])
    features = batch['features'][0] + [[0]*8 for _ in range(points-count)]
    return torch.tensor([features], dtype=torch.float32).flatten(1)


def run(snapshot, checkpoint_path, out):
    out = Path(out)
    if out.exists():
        raise ValueError('Refusing to overwrite fixed evaluation')
    if digest(checkpoint_path)!=CHECKPOINT:
        raise ValueError('Unreviewed checkpoint')
    root=Path(__file__).resolve().parents[1]
    guards=snapshot_files(root)
    train={r['glyph']:r for r in load_split(snapshot,MANIFEST,'train') if r['master']=='Regular'}
    val={r['glyph']:r for r in load_split(snapshot,MANIFEST,'validation') if r['master']=='Regular'}
    examples=[]
    for records,recipes,split in ((train,mr.RECIPES,'train'),(val,HAH_RECIPES,'validation')):
        for name,recipe in recipes.items():
            for mode in VARIANTS:
                examples.append(make_example(records[name],recipe,mode,split))
    torch.set_num_threads(1)
    saved=torch.load(checkpoint_path,map_location='cpu',weights_only=True)
    points=saved['config']['points']
    protocol={'checkpoint_sha256':CHECKPOINT,'manifest_sha256':MANIFEST,
              'variants':VARIANTS,'train_recipes':mr.RECIPES,'heldout_recipes':HAH_RECIPES,
              'examples':len(examples),'point_limit':points,'optimizer_steps':0,
              'padding':'zero to36; no point reordering, truncation or topology adaptation',
              'cohorts':'three known training glyphs, one held-out Hah family with three forms; not independent families',
              'test_split_used':False,'source_guards':guards}
    out.mkdir(parents=True)
    # Freeze protocol and inputs before the first prediction. No outcome-driven reselection.
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    (out/'examples.json').write_text(json.dumps(examples,indent=2)+'\n')
    model=nn.Sequential(nn.Linear(points*8,128),nn.GELU(),nn.Linear(128,128),nn.GELU(),nn.Linear(128,points*2),nn.Tanh())
    model.load_state_dict(saved['state_dict']);model.eval();model.requires_grad_(False)
    predictions=[];metrics=[];unsupported=[]
    for ex in examples:
        if len(ex['coordinates'])>points:
            unsupported.append({'example':ex,'reason':f'{len(ex["coordinates"])} points exceeds fixed {points}-point input; no prediction'})
            continue
        features=input_tensor(ex,points)
        with torch.inference_mode():
            raw=model((features-saved['mean'])/saved['scale']).reshape(points,2)[:len(ex['coordinates'])]*64
        mask=torch.tensor(ex['editable_mask']).unsqueeze(-1)
        raw=raw*mask
        delta=(raw/2).round()*2
        result=mr.reconstruct(ex,delta.tolist())
        target=torch.tensor(ex['target_deltas'])
        base=float((target.abs()*mask).sum()/(mask.sum()*2))
        error=float(((delta-target).abs()*mask).sum()/(mask.sum()*2))
        metrics.append({'glyph':ex['glyph'],'mode':ex['mode'],'cohort':ex['cohort'],
                        'exact_after_quantization':bool(delta.eq(target).all()),
                        'masked_mae':error,'unchanged_input_masked_mae':base,
                        'raw_masked_mae':float(((raw-target).abs()*mask).sum()/(mask.sum()*2)),
                        'max_error':float((delta-target).abs().max()),
                        'locked_deltas_zero':bool((delta*(1-mask)).eq(0).all()),
                        'outcome':'improved' if error<base else 'worse' if error>base else 'tied'})
        predictions.append({'example':ex,'raw_predicted_deltas':raw.tolist(),'predicted_deltas':delta.tolist(),'prediction':result})
    aggregates={}
    for cohort in sorted({m['cohort'] for m in metrics}):
        rows=[m for m in metrics if m['cohort']==cohort]
        aggregates[cohort]={'count':len(rows),'exact':sum(m['exact_after_quantization'] for m in rows),
            **{k:sum(m['outcome']==k for m in rows) for k in ('improved','worse','tied')},
            'mean_case_mae':sum(m['masked_mae'] for m in rows)/len(rows),
            'mean_case_unchanged_input_mae':sum(m['unchanged_input_masked_mae'] for m in rows)/len(rows)}
    assert snapshot_files(root)==guards,'Font/source file set or hashes changed'
    assert digest(checkpoint_path)==CHECKPOINT,'Checkpoint changed'
    report={'evaluation_only':True,'checkpoint_path':str(Path(checkpoint_path).resolve()),
            'checkpoint_sha256':CHECKPOINT,'manifest_sha256':MANIFEST,'script_sha256':digest(__file__),
            'protocol_sha256':digest(out/'protocol.json'),'examples_sha256':digest(out/'examples.json'),
            'steps':0,'metrics':metrics,'aggregates':aggregates,'unsupported_count':len(unsupported),
            'font_and_source_files_unchanged':len(guards),'overnight_started':False,'test_split_used':False}
    for name,value in [('predictions',predictions),('unsupported',unsupported),('report',report)]:
        (out/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({'aggregates':aggregates,'unsupported':len(unsupported)},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();run(a.snapshot,a.checkpoint,a.out)
