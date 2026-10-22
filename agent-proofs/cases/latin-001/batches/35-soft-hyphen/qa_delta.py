from pathlib import Path
import json,re
C=Path(__file__).resolve().parent
before=json.loads((C.parent/'33-brokenbar/qa-online/fontspector.json').read_text());after=json.loads((C/'qa-online/fontspector.json').read_text())
def records(d,severities):
 return sorted([{'check':c['check_id'],**s} for sections in d['results'].values() for checks in sections.values() for c in checks for s in c['subresults'] if s['severity'] in severities],key=lambda x:json.dumps(x,sort_keys=True))
bf=records(before,['FAIL','ERROR']);af=records(after,['FAIL','ERROR']);bw=records(before,['WARN']);aw=records(after,['WARN'])
assert bf==af
key=lambda x:json.dumps(x,sort_keys=True)
new=[x for x in aw if key(x) not in {key(x) for x in bw}];gone=[x for x in bw if key(x) not in {key(x) for x in aw}]
raw_new,raw_gone=new,gone
def normalize(x):
 if isinstance(x,dict):return {k:normalize(v) for k,v in x.items() if k!='glyph_id'}
 if isinstance(x,list):return [normalize(v) for v in x]
 if isinstance(x,str):return re.sub(r'try adding one of: ([^\n]+)',lambda m:'try adding one of: '+', '.join(sorted(m[1].split(', '))),x.replace('2026-10-22-soft-hyphen','PACKAGE').replace('2026-10-22-brokenbar','PACKAGE'))
 return x
new=[x for x in aw if key(normalize(x)) not in {key(normalize(x)) for x in bw}]
gone=[x for x in bw if key(normalize(x)) not in {key(normalize(x)) for x in aw}]
assert len(new)==1 and new[0]['check']=='soft_hyphen' and not gone
(C/'package-failure-delta.json').write_text(json.dumps({'before':before['summary'],'after':after['summary'],'fail_error_records_exactly_unchanged':True,'new_warnings':new,'removed_warnings':gone,'raw_changed_warning_records':{'after':raw_new,'before':raw_gone},'normalization':'Package directory normalized, glyph_id omitted and suggestion order sorted for WARN comparison; names/geometry/positions/messages preserved. Old glyph ink and advances verified exactly in verification.json.','disposition':'Known presence-policy warning for explicitly requested U+00AD compatibility. No exclusions or automatic removal applied. Release policy choice remains unapproved.'},indent=2)+'\n')
print(after['summary'],'new warning:',new[0]['check'])
