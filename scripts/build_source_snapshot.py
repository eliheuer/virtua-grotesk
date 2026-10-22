#!/usr/bin/env python3
"""Build a consistent temporary source snapshot without changing editor glyph order.

Per-master feature coordinates make fontTools merge GPOS tables. That merge
requires the same glyph order in every master; source editor orders can differ.
Normalize only the copied lib.plist ordering. All live source files stay intact.
"""
from contextlib import contextmanager
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import yaml

@contextmanager
def build_snapshot(config_path):
    config_path=Path(config_path).resolve()
    config=yaml.safe_load(config_path.read_text())
    source_root=config_path.parent
    with tempfile.TemporaryDirectory(prefix='virtua-build-') as temporary:
        target=(Path(temporary)/'sources').resolve()
        shutil.copytree(source_root,target,ignore=shutil.ignore_patterns('archive','instance_ufos','build.ninja','.ninja_log'))
        for designspace in config['sources']:
            path=target/designspace
            if path.suffix!='.designspace':
                raise ValueError('Snapshot build currently requires designspace inputs')
            doc=ET.parse(path)
            masters=[(path.parent/s.get('filename')).resolve() for s in doc.findall('sources/source')]
            if not masters or any(not p.is_relative_to(target) for p in masters):
                raise ValueError('Designspace sources must be within the copied source directory')
            # First source is the current default Regular master; preserve its order.
            first=plistlib.loads((masters[0]/'lib.plist').read_bytes())['public.glyphOrder']
            all_names=set()
            for master in masters:
                all_names.update(plistlib.loads((master/'glyphs/contents.plist').read_bytes()))
            order=list(dict.fromkeys(first))+sorted(all_names-set(first))
            for master in masters:
                lib=master/'lib.plist';text=lib.read_text()
                match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S)
                if not match:raise ValueError(f'Missing glyph order in {lib}')
                values=''.join('\n\t\t<string>'+n+'</string>' for n in order)
                lib.write_text(text[:match.end(1)]+values+text[match.end(2):])
        config['outputDir']=str((source_root/config.get('outputDir','../fonts')).resolve())
        copied=target/config_path.name
        copied.write_text(yaml.safe_dump(config,sort_keys=False))
        yield copied

if __name__=='__main__':
    import sys
    with build_snapshot(sys.argv[1]) as config:
        subprocess.run(['gftools','builder',str(config)],check=True)
