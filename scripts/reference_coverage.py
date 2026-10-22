#!/usr/bin/env python3
"""Compare pinned font cmaps without equating codepoints with language quality."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.unicodedata import script

def coverage(path):
    with TTFont(path) as font:
        return set(font.getBestCmap())

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--font',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();actual=coverage(a.font);reference=coverage(a.reference)
    missing=sorted(reference-actual)
    report={
        'font':{'path':str(a.font),'sha256':hashlib.sha256(a.font.read_bytes()).hexdigest(),'encoded':len(actual)},
        'reference':{'path':str(a.reference),'sha256':hashlib.sha256(a.reference.read_bytes()).hexdigest(),'encoded':len(reference)},
        'missing_by_script':dict(Counter(script(cp) for cp in missing)),
        'missing':[{'codepoint':f'U+{cp:04X}','character':chr(cp),'name':unicodedata.name(chr(cp),'Unnamed'),'script':script(cp),
                    'canonical_decomposition_available':bool(unicodedata.decomposition(chr(cp))) and all(ord(c) in actual for c in unicodedata.normalize('NFD',chr(cp))),
                    'arabic_presentation_form':0xFB50<=cp<=0xFDFF or 0xFE70<=cp<=0xFEFF} for cp in missing],
        'limits':'Cmap comparison only. Decomposition availability does not establish attachment, serving-subset reachability or reader approval. Presentation forms require a separate GSUB review; no automatic addition.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(len(missing),'missing encoded codepoints:',report['missing_by_script'])

if __name__=='__main__':main()
