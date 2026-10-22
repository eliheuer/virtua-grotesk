from pathlib import Path
import json,hashlib,os,re
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',b['scratch']));changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
for x in changes:
 old=(C/'before-sources'/x['path']).read_text();new=(S/x['path']).read_text();assert re.sub(r'\t<anchor name="caret_1"[^\n]*\n','',new)==old
before=TTFont(C/'assets/before.ttf');path=S/'fonts/variable/VirtuaGrotesk[wght].ttf';after=TTFont(path);(C/'assets/after.ttf').write_bytes(path.read_bytes());changed=[k for k in before.keys() if k!='GlyphOrder' and before.getTableData(k)!=after.getTableData(k)];print('Changed tables',changed)
assert set(changed)<= {'head','GDEF'},changed
checks=0;records=[]
for p in [path]+sorted((S/'fonts/ttf').glob('*.ttf')):
 f=TTFont(p);bp=C/'baseline-fonts'/p.relative_to(S/'fonts');bf=TTFont(bp)
 for w in ([400,475,550,625,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
  instance=instantiateVariableFont(f,{'wght':w},inplace=False) if 'fvar' in f else f
  carets=instance['GDEF'].table.LigCaretList
  for n,upper in [('fi',344),('fl',360)]:
   vals=carets.LigGlyph[carets.Coverage.glyphs.index(n)].CaretValue;expected=round(288+(upper-288)*(w-400)/300)
   assert len(vals)==1 and vals[0].Coordinate==expected,(p,w,n,vals[0].__dict__,expected)
   assert 0<expected<f['hmtx'][n][0];records.append({'font':p.name,'weight':w,'glyph':n,'caret':expected});checks+=1
 for text in ['fi fl ﬁ ﬂ','fine office affluence','fí fi̦ f́i fĺ f́l','ﬁ́ ﬁ̈ ﬂ̌','Ą́ ą́ Į́ į́','ببب ب','ھھھ ھ','שָׁלוֹם עוֹלָם']:
  for w in ([400,550,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
   assert shaped(bf,bp.read_bytes(),text,w)==shaped(f,p.read_bytes(),text,w),(p,text,w);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'changed_vf_tables':changed,'all_ink_metrics_shaping_tables_identical':True,'carets':records,'unchanged_source_files':len(b['sources'])-4},indent=2)+'\n');print(checks,'checks passed')
