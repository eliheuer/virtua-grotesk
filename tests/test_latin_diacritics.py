"""Compiled Latin attachment regressions; run after build, including web fallback."""
import io
import os
from pathlib import Path
import unittest
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

ROOT=Path(os.environ.get('VIRTUA_FONT_QA_ROOT',Path(__file__).resolve().parents[1]))
NEW='ĈĉĜĝĤĥĴĵǼǽ'

def shaped(font,data,text,weight):
    h=hb.Font(hb.Face(data));h.set_variations({'wght':weight})
    b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(h,b)
    gs=font.getGlyphSet(location={'wght':weight} if 'fvar' in font else None)
    result=[];advance=0
    for g,p in zip(b.glyph_infos,b.glyph_positions):
        assert g.codepoint, text
        pen=BoundsPen(gs);gs[font.getGlyphName(g.codepoint)].draw(TransformPen(pen,(1,0,0,1,advance+p.x_offset,p.y_offset)))
        result.append(pen.bounds);advance+=p.x_advance
    return advance,result

class LatinDiacriticsTests(unittest.TestCase):
    def fonts(self):
        paths=[ROOT/'fonts/variable/VirtuaGrotesk[wght].ttf']+sorted((ROOT/'fonts/ttf').glob('*.ttf'))
        for path in paths:
            with TTFont(path) as font:
                yield path,font

    def test_combining_ink_matches_spacing_donors(self):
        # Extra component translations were invisible to presence/GPOS checks.
        names='acute grave circumflex macron breve dotaccent dieresis ring hungarumlaut caron cedilla ogonek commaaccent'.split()
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                gs=font.getGlyphSet(location={'wght':w} if 'fvar' in font else None)
                for name in names:
                    with self.subTest(font=path.name,weight=w,mark=name):
                        a=BoundsPen(gs);b=BoundsPen(gs);gs[name].draw(a);gs[name+'comb'].draw(b)
                        for x,y in zip(a.bounds,b.bounds):self.assertAlmostEqual(x,y,delta=1)

    def test_precomposed_and_multi_mark_stacks_clear(self):
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for text in ['ū́','ǘ','á́','Ņ̦','b́̂','b̄́']:
                    with self.subTest(font=path.name,weight=w,text=text):
                        _,bb=shaped(font,path.read_bytes(),text,w)
                        self.assertGreaterEqual(len(bb),2)
                        gap=bb[0][1]-bb[1][3] if text=='Ņ̦' else bb[-1][1]-bb[-2][3]
                        self.assertGreaterEqual(gap,16)

    def test_new_composites_survive_missing_cmap_fallback(self):
        for path,font in self.fonts():
            fallback=TTFont(path)
            for t in fallback['cmap'].tables:
                if t.isUnicode():
                    for c in NEW:t.cmap.pop(ord(c),None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for c in NEW:
                    with self.subTest(font=path.name,weight=w,char=c):
                        self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(font.getBestCmap()[ord(c)]),1)
                        self.assertEqual(shaped(font,path.read_bytes(),c,w),shaped(fallback,stream.getvalue(),c,w))

    def test_latvian_construction_and_canonical_fallback(self):
        letters='ĢģĶķĻļŅņŖŗ'
        for path,font in self.fonts():
            fallback=TTFont(path)
            for table in fallback['cmap'].tables:
                if table.isUnicode():
                    for char in letters:table.cmap.pop(ord(char),None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in letters:
                    with self.subTest(font=path.name,weight=w,char=char):
                        expected=shaped(font,path.read_bytes(),char,w)
                        self.assertEqual(expected,shaped(font,path.read_bytes(),unicodedata.normalize('NFD',char),w))
                        self.assertEqual(expected,shaped(fallback,stream.getvalue(),char,w))
                with self.subTest(font=path.name,weight=w,char='ģ'):
                    base=shaped(font,path.read_bytes(),'g',w)[1][0]
                    composite=shaped(font,path.read_bytes(),'ģ',w)[1][0]
                    # The mark is above g; a cedilla underneath its descender fails.
                    self.assertEqual(base[1],composite[1])
                    self.assertGreater(composite[3],base[3])
                    for text in ['ģ́','ģ̦']:
                        _,bounds=shaped(font,path.read_bytes(),text,w)
                        gap=bounds[1][1]-bounds[0][3] if text=='ģ́' else bounds[0][1]-bounds[1][3]
                        self.assertGreaterEqual(gap,16)

    def test_ogonek_construction_survives_canonical_fallback(self):
        letters='ĄąĘęĮįŲų'
        for path,font in self.fonts():
            fallback=TTFont(path)
            for table in fallback['cmap'].tables:
                if table.isUnicode():
                    for char in letters:table.cmap.pop(ord(char),None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in letters:
                    for suffix in ['', '́', '̨']:
                        with self.subTest(font=path.name,weight=w,char=char,suffix=suffix):
                            expected=shaped(font,path.read_bytes(),char+suffix,w)
                            self.assertEqual(expected,shaped(font,path.read_bytes(),unicodedata.normalize('NFD',char)+suffix,w))
                            # With an acute and a missing ogonek cmap entry, HarfBuzz
                            # may recompose to Aacute+ogonek before GSUB. That separate
                            # serving-subset failure is retained in LAT-001 batch10's
                            # subset-accent-followup.json, not claimed fixed here.
                            if suffix!='́':
                                self.assertEqual(expected,shaped(fallback,stream.getvalue(),char+suffix,w))

    def test_accented_vowels_keep_base_advances(self):
        # Stale wrapper widths made accented words uneven and subset fallback reflow.
        letters='áăâäàāąåãéěêëėèēęóôöòőõúûüùűūųů'
        for path,font in self.fonts():
            fallback=TTFont(path)
            for table in fallback['cmap'].tables:
                if table.isUnicode():
                    for char in letters:table.cmap.pop(ord(char),None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in letters:
                    base=unicodedata.normalize('NFD',char)[0]
                    with self.subTest(font=path.name,weight=w,char=char):
                        advance=shaped(font,path.read_bytes(),base,w)[0]
                        self.assertEqual(shaped(font,path.read_bytes(),char,w)[0],advance)
                        self.assertEqual(shaped(fallback,stream.getvalue(),char,w)[0],advance)

    def test_alternate_carons_and_canonical_fallback(self):
        letters='ĽďľŤť'
        for path,font in self.fonts():
            fallback=TTFont(path)
            for table in fallback['cmap'].tables:
                if table.isUnicode():
                    for char in letters:table.cmap.pop(ord(char),None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in letters:
                    with self.subTest(font=path.name,weight=w,char=char):
                        expected=shaped(font,path.read_bytes(),char,w)
                        self.assertEqual(expected,shaped(font,path.read_bytes(),unicodedata.normalize('NFD',char),w))
                        self.assertEqual(expected,shaped(fallback,stream.getvalue(),char,w))
                        _,bounds=shaped(font,path.read_bytes(),char+'́',w)
                        self.assertGreaterEqual(bounds[-1][1]-bounds[0][3],16)

    def test_below_mark_stacks_fit_windows_clipping_metrics(self):
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for text in ['b̧̧','Ç̧','ģ̧','ģ̦','b̨̨','Ą̨','į́']:
                    with self.subTest(font=path.name,weight=w,text=text):
                        _,bounds=shaped(font,path.read_bytes(),text,w)
                        self.assertGreaterEqual(min(b[1] for b in bounds if b),-font['OS/2'].usWinDescent)
