#!/usr/bin/env python3
"""Read-only source scope, compiled scope and mark placement checks for HEB-002."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
import pathops

TARGETS = {'he-hb', 'het-hb', 'tav-hb'}
COMPILED = {'hehb', 'hethb', 'tavhb'}
WEIGHTS = list(range(400, 701, 50))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    out = args.candidate.resolve()
    root = Path(__file__).resolve().parents[3]
    scope = json.loads((out/'scope.json').read_text())
    for rel, digest in scope['source_hashes'].items():
        assert sha(root/rel) == digest, f'Active source drift: {rel}'
    changed = []
    metadata = []
    for before in (out/'before-sources').rglob('*'):
        if not before.is_file(): continue
        relative = before.relative_to(out/'before-sources')
        after = out/'sources'/relative
        if sha(before) != sha(after): changed.append('sources/'+str(relative))
    assert set(changed) == set(scope['changed_files']), changed
    for rel in changed:
        before = ET.parse(out/'before-sources'/Path(rel).relative_to('sources')).getroot()
        after = ET.parse(out/rel).getroot()
        assert ET.tostring(before.find('lib')) == ET.tostring(after.find('lib'))
        assert ET.tostring(before.find('unicode')) == ET.tostring(after.find('unicode'))
        bold = 'Bold.ufo' in rel
        width = {'he-hb':576, 'het-hb':592, 'tav-hb':632}[after.get('name')] + (96 if bold else 0)
        assert int(after.find('advance').get('width')) == width
        anchors = []
        for a, b in zip(before.findall('anchor'), after.findall('anchor')):
            assert a.get('name') == b.get('name')
            delta = 0 if not bold or a.get('name') in ['hbHolam','hbCantAboveLeft'] else 96 if a.get('name') == 'hbCantAboveRight' else 48
            snap = lambda n: 8*((n+4)//8)
            assert int(b.get('x')) == snap(int(a.get('x'))+delta)
            assert int(b.get('y')) == snap(int(a.get('y')))
            anchors.append({'name':a.get('name'), 'before':[int(a.get(k)) for k in ('x','y')], 'after':[int(b.get(k)) for k in ('x','y')]})
        metadata.append({'path':rel, 'before_width':before.find('advance').get('width'), 'after_width':width, 'anchors':anchors})
    fonts = {role: TTFont(out/f'{folder}/variable/VirtuaGrotesk[wght].ttf') for role, folder in [('before','before-fonts'),('candidate','fonts')]}
    hfonts = {role: hb.Font(hb.Face((out/f'{folder}/variable/VirtuaGrotesk[wght].ttf').read_bytes())) for role, folder in [('before','before-fonts'),('candidate','fonts')]}
    assert fonts['before'].getGlyphOrder() == fonts['candidate'].getGlyphOrder()
    compiled, collision, samples = {}, [], 0
    for weight in WEIGHTS:
        sets = {role: font.getGlyphSet(location={'wght':weight}) for role, font in fonts.items()}
        differences, widths = [], []
        for name in fonts['before'].getGlyphOrder():
            runs = []
            for glyphs in sets.values():
                pen = DecomposingRecordingPen(glyphs)
                glyphs[name].draw(pen)
                runs.append(pen.value)
            if runs[0] != runs[1]: differences.append(name)
            if sets['before'][name].width != sets['candidate'][name].width: widths.append(name)
        assert set(differences) == COMPILED, differences
        assert set(widths) == COMPILED, widths
        compiled[weight] = {'outlines_changed':differences, 'advances_changed':widths}
        for role, hfont in hfonts.items():
            hfont.set_variations({'wght':weight})
            for base in 'החת':
                for mark in '\u05b8\u05b7\u05b5\u05bc\u0591\u05bd\u05bf':
                    buffer = hb.Buffer(); buffer.add_str(base+mark); buffer.guess_segment_properties(); hb.shape(hfont,buffer)
                    assert all(i.codepoint for i in buffer.glyph_infos)
                    paths=[]; cursor=0
                    for info, position in zip(buffer.glyph_infos, buffer.glyph_positions):
                        name=fonts[role].getGlyphName(info.codepoint)
                        path=pathops.Path()
                        pen=TransformPen(path.getPen(),(1,0,0,1,cursor+position.x_offset,position.y_offset))
                        sets[role][name].draw(pen)
                        paths.append(path)
                        cursor+=position.x_advance
                    assert len(paths)==2, (base,mark,role,weight)
                    overlap=pathops.op(paths[0],paths[1],pathops.PathOp.INTERSECTION)
                    if abs(overlap.area)>0.01: collision.append({'role':role,'weight':weight,'text':base+mark,'area':overlap.area})
                    samples+=1
    assert not collision, collision
    result={'source_files_guarded':len(scope['source_hashes']), 'only_six_scratch_sources_changed':changed,
            'colors_and_unicode_preserved':True, 'metadata':metadata, 'compiled_scope':compiled,
            'glyph_weight_comparisons':len(fonts['before'].getGlyphOrder())*len(WEIGHTS),
            'mark_collision_checks':{'samples':samples, 'collisions':collision},
            'fonts':{role:{'path':str(font.reader.file.name),'sha256':sha(Path(font.reader.file.name))} for role,font in fonts.items()}}
    (out/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    # Raw-color audit avoids the legacy grid_lint assumption that any color
    # other than red or green is orange. This is an inventory, not permission.
    records=[]
    for master in ['Regular','Bold']:
        gdir=root/f'sources/VirtuaGrotesk-{master}.ufo/glyphs'
        for name, filename in plistlib.loads((gdir/'contents.plist').read_bytes()).items():
            glyph=ET.parse(gdir/filename).getroot()
            lib=glyph.find('lib'); color=None
            if lib is not None:
                color=plistlib.loads(b'<plist>'+ET.tostring(lib.find('dict'))+b'</plist>').get('public.markColor')
            points=glyph.findall('./outline/contour/point')
            off2=sum(any(float(p.get(axis))%2 for axis in ('x','y')) for p in points)
            off8=sum(any(float(p.get(axis))%8 for axis in ('x','y')) for p in points)
            advance=glyph.find('advance'); width=float(advance.get('width',0)) if advance is not None else 0
            if off2 or off8 or width%8:
                records.append({'master':master,'glyph':name,'color':color,'off2_points':off2,'off8_points':off8,'off8_advance':bool(width%8)})
    audit={'scope':'All active default-layer GLIF outlines and advances; not anchors, components, kerning, curves or visual quality. No mutations.',
           'off2_points':sum(r['off2_points'] for r in records),
           'glyph_masters_with_off2_points':sum(bool(r['off2_points']) for r in records),
           'off8_advances':sum(r['off8_advance'] for r in records), 'records':records}
    (out/'active-grid-inventory.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k!='records'},indent=2))
    print(f'Validated {len(changed)} scratch glyphs, {result["glyph_weight_comparisons"]} compiled comparisons, {samples} mark pairs')


if __name__=='__main__': main()
