import sys,json,hashlib,time,plistlib,shutil
from pathlib import Path
ROOT=Path('/Users/eli/GH/repos/virtua-grotesk'); OUT=ROOT/'out/seen-model-test/control'
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
receipt={'model_files':{str(p):sha(p) for p in m.iterdir() if p.is_file()},'runs':[],'method':'Direct exact vector input; greedy raw decoder; no conform/grid postprocessing; not a critic or held-out benchmark'}
for rev in (0,):
 for master,weight in [('Regular',400)]:
  gd=ROOT/f'sources/VirtuaGrotesk-{master}.ufo/glyphs'; src=gd/plistlib.loads((gd/'contents.plist').read_bytes())['H']; dest=OUT/f'v{rev}-{master}-input.glif';shutil.copyfile(src,dest)
  class G:pass
  g=G();pen=RecordingPen();readGlyphFromString(src.read_text(),g,PointToSegmentPen(pen));ops=pen.value
  for mode in ('identity',):
   prefix=tk.header(v,v.id.get('N_H',v.id['UNK']) if mode=='identity' else v.id['UNK'],uni=0x48 if mode=='identity' else None)+[v.id[tk.WEIGHT_TOKEN[weight]],v.id['ADV'],v.coord(g.width)]+tk.outline_tokens(v,ops)+[v.id['SEP']]
   mx.random.seed(0);start=time.time();tokens=generate_candidate(model,v,prefix,0.0);cand=tk.decode_outline(v,tokens)
   path=OUT/f'v{rev}-{master}-{mode}.glif';path.write_text(ops_to_glif('seen-ar',int(g.width),cand,'0633'))
   row={'revision':rev,'master':master,'mode':mode,'input':str(dest.relative_to(ROOT)),'input_hash':sha(dest),'output':str(path.relative_to(ROOT)),'output_hash':sha(path),'seconds':time.time()-start,'input_ops':len(ops),'output_ops':len(cand),'prefix_tokens':len(prefix),'output_tokens':len(tokens),'input_iou':ink_iou(ops,cand),'heuristic_score':score_candidate(cand,ops)}
   receipt['runs'].append(row);(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2));print(row,flush=True)
