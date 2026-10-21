from pathlib import Path
import re,json,hashlib
C=Path('agent-proofs/cases/arabic-006/batches/08-lam-final');m=json.loads((C/'candidate.json').read_text());scratch=Path(m['scratch']);g=m['glyphs'][0];p=C/'candidate-sources'/g['path']
pts=[(32,0),(32,-176),(120,-272),(312,-272),(504,-272),(592,-176),(592,-8),(600,0),(744,0),(760,16),(760,80),(744,96),(688,96),(632,96),(592,136),(592,192),(592,752),(576,768),(512,768),(496,752),(496,0),(496,-128),(408,-168),(312,-168),(216,-168),(128,-128),(128,0),(128,64),(112,80),(48,80),(32,64)]
it=iter(pts)
def f(x):
 a,b=next(it);return f'<point x="{a}" y="{b}"'+x[1]
s=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',f,p.read_text()).replace('<advance width="736"/>','<advance width="744"/>');assert next(it,None) is None
p.write_text(s);(scratch/g['path']).write_text(s);g['candidate_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
(C/'refine.py').write_text(Path('/tmp/refine_lam_final.py').read_text())
p=C/'README.md';p.write_text('''# ARB-006 batch 08 — Final Lam correction (candidate)

Eli reports that Lam still has issues in the 700 joined proof (2026-10-21).
The leftmost joined form is thin, has a joining-bar step, and lacks its descending
bowl. Batch 07 repaired three forms but left this visible structural problem.
Do not call a family checked/completed merely because its edited roots pass.

Scope: `lam-ar.fina` in Regular and Bold, 31 matching points instead of 14.
Separate scratch candidate only: Regular is green and needs an explicit named
exception before active application. No active font source has been changed.
The descending bowl follows the family's isolated shape, with 96/160 stems,
104/176 bottom weight, 96/176 joining bars, 16-unit exposed chamfers and an
8-unit lower branch cut. The incoming arm has a separate 96-square tangent
turn. Regular geometry is deliberately constructed on 8 (including center312
and right edge592), rather than importing isolated Lam's off-grid coordinates.
Regular advance744; Bold824. Anchors unchanged. Both candidates are purple,
not a human grade. Lam–Alef is separate and still unresolved.
''')
p=Path('agent-proofs/FEEDBACK.md');p.write_text(p.read_text()+'''\n## Lam joined-form rejection — 2026-10-21\n\nEli reports continuing Lam issues in the batch 07 700 proof. Agent diagnosis:\nfinal Lam remained thin, stepped at the incoming join and missing its bowl.\nThe earlier report disclosed that defect but advancing the queue did not resolve\nthe visible joined-string failure. Batch 08 prepares a compatible final-form\nrepair in both masters; Regular's green protection still requires a named\nexception before application. Preserve Beh's recursive reservation throughout.\n''')
