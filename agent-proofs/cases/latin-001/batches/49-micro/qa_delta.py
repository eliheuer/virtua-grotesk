from pathlib import Path
import json,re
C=Path(__file__).resolve().parent
before=json.loads((C.parent/'46-superior-eight/qa-online/fontspector.json').read_text());after=json.loads((C/'qa-online/fontspector.json').read_text())
def records(d,severities):
 return sorted([{'check':c['check_id'],**s} for sections in d['results'].values() for checks in sections.values() for c in checks for s in c['subresults'] if s['severity'] in severities],key=lambda x:json.dumps(x,sort_keys=True))
bf=records(before,['FAIL','ERROR']);af=records(after,['FAIL','ERROR']);bw=records(before,['WARN']);aw=records(after,['WARN'])
def failure_normalize(x):
 x=dict(x);parts=x['message'].split('\n\n* ')
 if len(parts)==2:x['message']=parts[0]+'\n\n* '+'\n* '.join(sorted(parts[1].split('\n* ')))
 return x
assert sorted(map(failure_normalize,bf),key=lambda x:json.dumps(x,sort_keys=True))==sorted(map(failure_normalize,af),key=lambda x:json.dumps(x,sort_keys=True))
key=lambda x:json.dumps(x,sort_keys=True)
new=[x for x in aw if key(x) not in {key(x) for x in bw}];gone=[x for x in bw if key(x) not in {key(x) for x in aw}]
raw_new,raw_gone=new,gone
def normalize(x):
 if isinstance(x,dict):return {k:normalize(v) for k,v in x.items() if k!='glyph_id'}
 if isinstance(x,list):return [normalize(v) for v in x]
 if isinstance(x,str):return re.sub(r'try adding one of: ([^\n]+)',lambda m:'try adding one of: '+', '.join(sorted(m[1].split(', '))),x.replace('2026-10-22-superior-eight','PACKAGE').replace('2026-10-22-micro','PACKAGE'))
 return x
new=[x for x in aw if key(normalize(x)) not in {key(normalize(x)) for x in bw}]
gone=[x for x in bw if key(normalize(x)) not in {key(normalize(x)) for x in aw}]
assert not new and not gone,(new,gone)
(C/'package-failure-delta.json').write_text(json.dumps({'before':before['summary'],'after':after['summary'],'fail_error_records_exactly_unchanged':bf==af,'failure_meaning_unchanged':True,'raw_failure_delta':{'before':[x for x in bf if x not in af],'after':[x for x in af if x not in bf]},'new_warnings':new,'removed_warnings':gone,'raw_changed_warning_records':{'after':raw_new,'before':raw_gone},'normalization':'Ticuna failure codepoint bullets sorted for semantic comparison; raw records retained. Package directory normalized, glyph_id omitted and suggestion order sorted for WARN comparison; names/geometry/positions/messages preserved. Old glyph ink and advances verified exactly in verification.json.','disposition':'No new semantic warnings. Failure meanings unchanged from batch46; soft-hyphen policy and unreachable-subsetting warnings remain. No exclusions or metadata changes.'},indent=2)+'\n')
print(after['summary'], 'new semantic warnings:', len(new))
