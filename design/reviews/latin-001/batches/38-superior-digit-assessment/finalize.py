from pathlib import Path
import hashlib,json
C=Path(__file__).resolve().parent;R=C.parents[4];a=json.loads((C/'assessment.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
current={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
assert current==a['source_hashes']
fonts={str(p.relative_to(R)):sha(p) for p in (R/'fonts').rglob('*.ttf')};assert fonts==a['active_fonts']
for w in [400,475,550,625,700]:
 rows={r['text']:r for r in a['tests'] if r['font']=='rubik' and r['weight']==w}
 assert rows['123']['modes']['sups']==rows['¹²³']['modes']['default']
screens={str(p.relative_to(C)):sha(p) for p in sorted((C/'browser').glob('*.png'))};assert len(screens)==15
(C/'browser-review.json').write_text(json.dumps({'weights':[400,550,700],'fonts':{n:v['sha256'] for n,v in a['fonts'].items()},'inspected_screenshots':screens,'scope':'Three controlled fixtures plus Diffenator target and stock first viewport in Virtua/Rubik. Slider weight governs despite Regular menu label. No exhaustive language or native-reader approval.','findings':['Controlled Virtua encoded superscripts display fallback ink; actual fallback font unidentified.','Diffenator Virtua encoded targets display missing-glyph boxes; Rubik encoded superiors visible.','Virtua sups remains ordinary figures; Rubik sups gives designed superior glyphs.','Preserve Virtua curved one flag and rounded three upper bowl; Rubik is comparison only.','Dense Bold and uneven stock spacing remain review issues.']},indent=2)+'\n')
(C/'final-identity.json').write_text(json.dumps({'baseline_head':a['head'],'all_source_hashes_unchanged':True,'source_count':len(current),'active_fonts_unchanged':fonts,'no_build_or_source_edit':True,'direct_cases':len(a['tests']),'direct_feature_modes_per_case':4,'subset_cases':len(json.loads((C/'subset-assessment.json').read_text())),'subset_modes_per_case':2,'browser_images':len(screens),'raster_images':5},indent=2)+'\n')
print('All',len(current),'sources and',len(fonts),'active font hashes exact; 15 browser images recorded.')
