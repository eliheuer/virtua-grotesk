#!/usr/bin/env python3
"""Read-only source scope, compiled scope and mark placement checks for HEB-003."""
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

TARGETS = {'bet-hb', 'kaf-hb', 'finalkaf-hb'}
COMPILED = {'bethb', 'kafhb', 'finalkafhb'}
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
        width = {'bet-hb':544, 'kaf-hb':480, 'finalkaf-hb':496}[after.get('name')] + (96 if bold else 0)
        assert int(after.find('advance').get('width')) == width
        anchors = []
        for a, b in zip(before.findall('anchor'), after.findall('anchor')):
            assert a.get('name') == b.get('name')
            delta = 0 if not bold or a.get('name') in ['hbHolam','hbCantAboveLeft'] else 96 if a.get('name') == 'hbCantAboveRight' else 48
            snap = lambda n: 8*((n+4)//8)
            expected_x = 208 if after.get('name')=='finalkaf-hb' and a.get('name') in ['hbBottom','hbMeteg','hbCantBelow','hbCantBelowRight'] else snap(int(a.get('x'))+delta)
            assert int(b.get('x')) == expected_x
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
        assert set(differences) == COMPILED | {'uniFB4C', 'uniFB4D'}, differences
        assert set(widths) == COMPILED, widths
        compiled[weight] = {'outlines_changed':differences, 'advances_changed':widths}
        for role, hfont in hfonts.items():
            hfont.set_variations({'wght':weight})
            for base in 'בכך':
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
    print(f'Validated {len(changed)} scratch glyphs, {result["glyph_weight_comparisons"]} compiled comparisons, {samples} mark pairs')


if __name__=='__main__': main()
