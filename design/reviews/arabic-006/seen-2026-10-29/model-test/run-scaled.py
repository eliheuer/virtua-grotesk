import sys,json,hashlib,time,plistlib,shutil
from pathlib import Path
ROOT=Path('/Users/eli/GH/repos/virtua-grotesk'); OUT=ROOT/'out/seen-model-test/scaled'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,'/Users/eli/GH/repos/font-garden-lab')
import mlx.core as mx
mx.set_default_device(mx.cpu)
from glyphlab import tokenizer as tk
from glyphlab.model import GlyphLM
from glyphlab.sketch2glyph import generate_candidate,ops_to_glif,ink_iou,score_candidate
from fontTools.ufoLib.glifLib import readGlyphFromString
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_hashes={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'sources').rglob('*') if p.is_file()}
(OUT/'source-hashes.json').write_text(json.dumps(source_hashes))
m=Path.home()/'.runebender/models/virtua-12m-sketch'; cfg=json.loads((m/'config.json').read_text());v=tk.Vocab.load(str(m/'vocab.txt'))
model=GlyphLM(cfg['vocab_size'],dims=cfg['dims'],heads=cfg['heads'],layers=cfg['layers'],max_len=cfg['max_len']);model.load_weights(str(m/'weights.safetensors'));model.eval()
receipt={'model_files':{str(p):sha(p) for p in m.iterdir() if p.is_file()},'runs':[],'method':'Uniform scale 0.75, quantize to existing 2-unit vocabulary, restore output by inverse scale; no conform; greedy; not a critic or held-out benchmark'}
for rev in (4,6):
 for master,weight in [('Regular',400),('Bold',700)]:
  src=ROOT/f'design/reviews/arabic-006/seen-2026-10-29/revision{rev}/{master}.glif'; dest=OUT/f'v{rev}-{master}-input.glif';shutil.copyfile(src,dest)
  class G:pass
  g=G();pen=RecordingPen();readGlyphFromString(src.read_text(),g,PointToSegmentPen(pen));original_ops=pen.value
  ops=[(op,tuple((tk.snap(x*0.75),tk.snap(y*0.75)) for x,y in pts)) for op,pts in original_ops]
  for mode in ('identity','faithful'):
   prefix=tk.header(v,v.id.get('N_seen-ar',v.id['UNK']) if mode=='identity' else v.id['UNK'],uni=0x633 if mode=='identity' else None)+[v.id[tk.WEIGHT_TOKEN[weight]],v.id['ADV'],v.coord(g.width*0.75)]+tk.outline_tokens(v,ops)+[v.id['SEP']]
   mx.random.seed(0);start=time.time();tokens=generate_candidate(model,v,prefix,0.0);cand=tk.decode_outline(v,tokens)
   path=OUT/f'v{rev}-{master}-{mode}.glif';restored=[(op,tuple((x/0.75,y/0.75) for x,y in pts)) for op,pts in cand]
   path.write_text(ops_to_glif('seen-ar',int(g.width),restored,'0633').replace('0.27,0.44,1,1','0.54,0.44,0.88,1'))
   row={'revision':rev,'master':master,'mode':mode,'input':str(dest.relative_to(ROOT)),'input_hash':sha(dest),'output':str(path.relative_to(ROOT)),'output_hash':sha(path),'seconds':time.time()-start,'input_ops':len(ops),'output_ops':len(cand),'prefix_tokens':len(prefix),'output_tokens':len(tokens),'input_iou':ink_iou(ops,cand),'heuristic_score':score_candidate(cand,ops)}
   receipt['runs'].append(row);(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2));print(row,flush=True)
