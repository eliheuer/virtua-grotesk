#!/usr/bin/env python3
"""Variable-length local-graph residual model; input geometry only, fixed unit scales."""
import copy
import random
import torch
from torch import nn
import masked_repair as mr

SCHEMA='virtua-variable-repair-v1'


def make_example(record, selected, shifts, mode, cohort):
    ex={'schema':SCHEMA,'glyph':record['glyph'],'master':record['master'],'group':record['group'],
        'source_sha256':record['source_sha256'],'mode':mode,'cohort':cohort,'synthetic':True,
        'input':copy.deepcopy(record),'target':copy.deepcopy(record),'coordinates':[],
        'target_deltas':[],'editable_mask':[],'point_types':[],'contour_starts':[]}
    for i,(ci,pi,p) in enumerate(mr.flatten(ex['input'])):
        dx,dy=shifts.get(i,(0,0))
        if i not in selected and (dx or dy):raise ValueError('Corruption outside mask')
        xy=[mr.checked(float(p[a])+d,mr.COORD_MIN,mr.COORD_MAX) for a,d in zip(('x','y'),(dx,dy))]
        for a,v in zip(('x','y'),xy):p[a]=str(v)
        ex['coordinates'].append(xy);ex['target_deltas'].append([-dx,-dy])
        ex['editable_mask'].append(int(i in selected));ex['point_types'].append(p.get('type','offcurve'))
        ex['contour_starts'].append(int(pi==0))
    return ex


def synthetic(record,rng,mode,cohort='train'):
    flat=mr.flatten(record);handles=[i for i,(_,_,p) in enumerate(flat) if 'type' not in p]
    # Straight-only shapes supply identity controls, never fabricated curve handles.
    if not handles: return make_example(record,set(range(len(flat))),{},mode,cohort)
    center=rng.choice(handles);cx,cy=(float(flat[center][2][a]) for a in ('x','y'))
    nearest=sorted(handles,key=lambda i:(float(flat[i][2]['x'])-cx)**2+(float(flat[i][2]['y'])-cy)**2)
    selected=set(nearest[:min(len(handles),rng.choice([4,6,8]))]);shifts={}
    amplitude=lambda:rng.choice([-20,-12,-4,4,12,20])
    if mode=='single':shifts[center]=(amplitude(),amplitude())
    elif mode=='cluster':
        dx,dy=amplitude(),amplitude()
        shifts={i:(dx,dy) for i in selected}
    elif mode in ('paired-x','paired-y'):
        amp=amplitude();axis=0 if mode=='paired-x' else 1
        # Spatial groups are synthetic recipes, not inferred inner/outer labels.
        ordered=sorted(selected,key=lambda i:float(flat[i][2][('x','y')[axis]]))
        for j,i in enumerate(ordered):
            d=amp if j<len(ordered)/2 else -amp
            shifts[i]=(d,0) if axis==0 else (0,d)
    elif mode=='jitter':shifts={i:(amplitude(),amplitude()) for i in selected}
    elif mode!='noop':raise ValueError('Unknown corruption')
    return make_example(record,selected,shifts,mode,cohort)


def features(ex):
    """Cyclic same-contour neighbors and spatial nonlocal neighbors; no target reads."""
    xy=ex['coordinates'];n=len(xy)
    if not 1<=n<=512:raise ValueError('Point count outside pilot resource limit; no truncation')
    starts=[i for i,v in enumerate(ex['contour_starts']) if v]+[n]
    if starts[0]!=0:raise ValueError('Missing contour start')
    neighbors=[None]*n
    for start,end in zip(starts,starts[1:]):
        size=end-start
        for i in range(start,end):neighbors[i]=[start+(i-start+d)%size for d in (-2,-1,1,2)]
    kinds={'line':(1,0,0),'curve':(0,1,0),'offcurve':(0,0,1)}
    rows=[];spatial=[]
    for i,(x,y) in enumerate(xy):
        if ex['point_types'][i] not in kinds:raise ValueError('Unsupported point type')
        local=neighbors[i]
        other=[j for j in range(n) if j not in set(local+[i])]
        near=sorted(other,key=lambda j:(xy[j][0]-x)**2+(xy[j][1]-y)**2)[:3]
        near+=( [i]*(3-len(near)) );spatial.append(near)
        row=[x/1024,y/1024,ex['input']['advance']/1024,*kinds[ex['point_types'][i]],ex['editable_mask'][i]]
        for j in local+near:row.extend([(xy[j][0]-x)/1024,(xy[j][1]-y)/1024])
        rows.append(row)
    return rows,neighbors,spatial


def collate(examples):
    n=max(len(e['coordinates']) for e in examples);xs=[];ns=[];ss=[];valid=[];mask=[];targets=[]
    for e in examples:
        x,nb,sp=features(e);m=len(x);pad=n-m
        xs.append(x+[[0]*21 for _ in range(pad)]);ns.append(nb+[[0]*4 for _ in range(pad)]);ss.append(sp+[[0]*3 for _ in range(pad)])
        valid.append([1]*m+[0]*pad);mask.append(e['editable_mask']+[0]*pad)
        targets.append(e['target_deltas']+[[0,0] for _ in range(pad)])
    return (torch.tensor(xs,dtype=torch.float32),torch.tensor(ns),torch.tensor(ss),
            torch.tensor(valid,dtype=torch.float32),torch.tensor(mask,dtype=torch.float32),torch.tensor(targets,dtype=torch.float32))


class VariableRepair(nn.Module):
    def __init__(self):
        super().__init__()
        self.encode=nn.Sequential(nn.Linear(21,64),nn.GELU(),nn.Linear(64,64),nn.GELU())
        self.head=nn.Sequential(nn.Linear(64*4,96),nn.GELU(),nn.Linear(96,64),nn.GELU(),nn.Linear(64,2))
        nn.init.zeros_(self.head[-1].weight);nn.init.zeros_(self.head[-1].bias)

    def forward(self,x,neighbors,spatial,valid,mask):
        h=self.encode(x);batch=torch.arange(h.shape[0],device=h.device)[:,None,None]
        local=h[batch,neighbors].mean(2);near=h[batch,spatial].mean(2)
        pooled=(h*valid.unsqueeze(-1)).sum(1)/valid.sum(1,keepdim=True)
        context=pooled[:,None,:].expand_as(h)
        delta=torch.tanh(self.head(torch.cat([h,local,near,context],-1)))*32
        return delta*mask.unsqueeze(-1)*valid.unsqueeze(-1)
