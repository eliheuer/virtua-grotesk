from pathlib import Path
import unittest,io,json
import tests.test_built_font_engineering as t
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;R=C.parents[2];B=Path((C/'baseline-rebuild-path.txt').read_text().strip())
a=TTFont(C/'assets/before.ttf');b=TTFont(B/'fonts/variable/VirtuaGrotesk[wght].ttf')
assert all(a.getTableData(k)==b.getTableData(k) for k in a.keys() if k not in ['GlyphOrder','head'])
class Result(unittest.TestResult):
 def __init__(self):super().__init__();self.records=[]
 def addSubTest(self,test,subtest,err):
  super().addSubTest(test,subtest,err)
  if err:self.records.append({'test':test._testMethodName,'params':str(subtest.params),'message':str(err[1])})
 def addFailure(self,test,err):super().addFailure(test,err);self.records.append({'test':test._testMethodName,'message':str(err[1])})
 def addError(self,test,err):super().addError(test,err);self.records.append({'test':test._testMethodName,'error':str(err[1])})
reports={}
for name,root in [('before',B),('after',R)]:
 t.ROOT=root;t.VF=root/'fonts/variable/VirtuaGrotesk[wght].ttf';r=Result();unittest.defaultTestLoader.loadTestsFromTestCase(t.BuiltFontEngineeringTests).run(r);reports[name]={'tests':r.testsRun,'failures':r.records}
key=lambda x:json.dumps(x,sort_keys=True);before={key(x) for x in reports['before']['failures']};after={key(x) for x in reports['after']['failures']}
reports['new_failures']=[json.loads(s) for s in sorted(after-before)];reports['resolved_failures']=[json.loads(s) for s in sorted(before-after)]
(C/'existing-regressions.json').write_text(json.dumps(reports,indent=2)+'\n');print({k:len(v['failures']) for k,v in reports.items() if isinstance(v,dict)},'new',len(after-before),'resolved',len(before-after));assert not reports['new_failures']
