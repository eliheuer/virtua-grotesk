from pathlib import Path
import json,unittest
import tests.test_latin_diacritics as t
C=Path(__file__).resolve().parent;S=Path(json.loads((C/'baseline.json').read_text())['scratch']);t.ROOT=S;t.VF=S/'fonts/variable/VirtuaGrotesk[wght].ttf'
with (C/'latin-tests.log').open('w') as f:
 r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(t))
assert r.wasSuccessful()
print(r.testsRun,'Latin methods pass')
