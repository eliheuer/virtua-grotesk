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
                            # Above/below glyph ordering can differ after normalization,
                            # but positioned ink and advance must match.
                            actual=shaped(fallback,stream.getvalue(),char+suffix,w)
                            self.assertEqual(expected[0],actual[0])
                            self.assertEqual(sorted(expected[1]),sorted(actual[1]))


    def test_ogonek_stacks_survive_real_subsetting(self):
        from fontTools import subset
        letters='ĄąĘęĮįŲų'
        for path,font in self.fonts():
            fallback=TTFont(path)
            options=subset.Options(); options.layout_features=['*']
            sub=subset.Subsetter(options=options)
            sub.populate(unicodes=set(font.getBestCmap())-set(map(ord,letters)))
            sub.subset(fallback)
            stream=io.BytesIO(); fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in letters:
                    for suffix in ['́','̀','̂','̃','̄','̆','̇','̈','̊','̋','̌','́́','̧́']:
                        for text in [char+suffix,unicodedata.normalize('NFD',char+suffix)]:
                            with self.subTest(font=path.name,weight=w,text=text):
                                expected=shaped(font,path.read_bytes(),text,w)
                                actual=shaped(fallback,stream.getvalue(),text,w)
                                self.assertEqual(expected[0],actual[0])
                                self.assertEqual(sorted(expected[1]),sorted(actual[1]))

    def test_accented_letters_keep_base_advances(self):
        # Stale wrapper widths made accented words uneven and subset fallback reflow.
        letters='áăâäàāąåãéěêëėèēęóôöòőõúûüùűūųůÁĂÂÄÀĀĄÅÃĎĞĢĠĹĻŃŇŅÑÓÔÖÒŐÕŔŘŚŠŞȘŢȚÚÛÜÙŰŪŲŮẂŴẄẀÝŶŸỲŹŽŻğģġįńňņñŕřśšşșẃŵẅẁýŷÿỳźžż'
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

    def test_hcaron_ascender_attachment_and_fallback(self):
        for path,font in self.fonts():
            fallback=TTFont(path)
            for table in fallback['cmap'].tables:
                if table.isUnicode():table.cmap.pop(0x21f,None)
            stream=io.BytesIO();fallback.save(stream)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                with self.subTest(font=path.name,weight=w):
                    gs=font.getGlyphSet(location={'wght':w} if 'fvar' in font else None)
                    # The existing mark's local y translation is verified in compiled ink.
                    pen=BoundsPen(gs);gs['hcaron'].draw(pen)
                    self.assertGreaterEqual(pen.bounds[3],1024)
                    self.assertEqual(shaped(font,path.read_bytes(),'ȟ',w)[0],shaped(font,path.read_bytes(),'h',w)[0])
                    for text in ['ȟ','ȟ́','ȟ̌','ḩ̌']:
                        expected=shaped(font,path.read_bytes(),text,w)
                        self.assertEqual(expected,shaped(font,path.read_bytes(),unicodedata.normalize('NFD',text),w))
                        self.assertEqual(expected,shaped(fallback,stream.getvalue(),text,w))
                    for text in ['ȟ́','ȟ̌']:
                        _,bb=shaped(font,path.read_bytes(),text,w)
                        self.assertGreaterEqual(bb[-1][1]-bb[0][3],32)
                        self.assertLessEqual(max(b[3] for b in bb),font['OS/2'].usWinAscent)

    def test_crossed_t_coverage_and_mark_attachment(self):
        # Newly encoded letters must remain GPOS bases at every shipped weight.
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for char in 'Ŧŧ':
                    with self.subTest(font=path.name,weight=w,char=char):
                        name=font.getBestCmap()[ord(char)]
                        self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(name),1)
                        advance,base=shaped(font,path.read_bytes(),char,w)
                        for marks in ['́','̈','̌','̂́','̧́']:
                            actual,bounds=shaped(font,path.read_bytes(),char+marks,w)
                            self.assertEqual(actual,advance)
                            self.assertGreaterEqual(len(bounds),2)
                            self.assertGreaterEqual(bounds[-1][1]-base[0][3],16)
                            self.assertLessEqual(max(b[3] for b in bounds),font['OS/2'].usWinAscent)

    def test_long_s_coverage_and_mark_attachment(self):
        # Historical long s is encoded independently, without replacing ordinary s.
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                with self.subTest(font=path.name,weight=w):
                    name=font.getBestCmap()[0x17f]
                    self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(name),1)
                    advance,base=shaped(font,path.read_bytes(),'ſ',w)
                    self.assertNotEqual(base,shaped(font,path.read_bytes(),'s',w)[1])
                    for marks in ['́','̈','̌','̂́','̧́']:
                        actual,bounds=shaped(font,path.read_bytes(),'ſ'+marks,w)
                        self.assertEqual(actual,advance)
                        self.assertGreaterEqual(bounds[-1][1]-base[0][3],16)
                        self.assertLessEqual(max(b[3] for b in bounds),font['OS/2'].usWinAscent)

    def test_florin_descender_and_mark_attachment(self):
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                with self.subTest(font=path.name,weight=w):
                    name=font.getBestCmap()[0x192]
                    self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(name),1)
                    advance,base=shaped(font,path.read_bytes(),'ƒ',w)
                    self.assertEqual(base[0][1],-256)
                    for mark in ['́','̈','̌','̦']:
                        actual,bounds=shaped(font,path.read_bytes(),'ƒ'+mark,w)
                        self.assertEqual(actual,advance)
                        if mark=='̦':self.assertGreaterEqual(base[0][1]-bounds[-1][3],16)
                        else:self.assertGreaterEqual(bounds[-1][1]-base[0][3],16)
                        self.assertGreaterEqual(min(b[1] for b in bounds),-font['OS/2'].usWinDescent)

    def test_kra_xheight_and_mark_attachment(self):
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                with self.subTest(font=path.name,weight=w):
                    name=font.getBestCmap()[0x138]
                    self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(name),1)
                    advance,base=shaped(font,path.read_bytes(),'ĸ',w)
                    self.assertEqual(base[0][3],576)
                    self.assertNotEqual(base,shaped(font,path.read_bytes(),'k',w)[1])
                    for mark in ['́','̈','̌','̂́','̦']:
                        actual,bounds=shaped(font,path.read_bytes(),'ĸ'+mark,w)
                        self.assertEqual(actual,advance)
                        if mark=='̦':self.assertGreaterEqual(base[0][1]-bounds[-1][3],16)
                        else:self.assertGreaterEqual(bounds[-1][1]-base[0][3],16)

    def test_apostrophe_n_component_and_marks(self):
        for path,font in self.fonts():
            data=path.read_bytes()
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                with self.subTest(font=path.name,weight=w):
                    self.assertEqual(font.getBestCmap()[0x149], 'napostrophe')
                    gs=font.getGlyphSet(location={'wght':w} if 'fvar' in font else None)
                    shift=80+(w-400)/300*16
                    self.assertAlmostEqual(gs['napostrophe'].width,gs['n'].width+shift,delta=1)
                    adv,boxes=shaped(font,data,'ŉ',w)
                    self.assertEqual(len(boxes),1)
                    self.assertEqual(boxes[0][3],792)
                    adv2,marked=shaped(font,data,'ŉ\u0301',w)
                    self.assertEqual(adv,adv2)
                    self.assertGreaterEqual(marked[1][1]-marked[0][3],16)
                    self.assertEqual(len(shaped(font,data,'ʼn',w)[1]),2)

    def test_standard_f_ligatures_and_mark_components(self):
        for path,font in self.fonts():
            data=path.read_bytes()
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                def glyph_names(text,features=None):
                    h=hb.Font(hb.Face(data));h.set_variations({'wght':w})
                    b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(h,b,features or {})
                    return [font.getGlyphName(g.codepoint) for g in b.glyph_infos]
                for encoded,name in [('ﬁ','fi'),('ﬂ','fl')]:
                    with self.subTest(font=path.name,weight=w,ligature=name):
                        self.assertEqual(font.getBestCmap()[ord(encoded)],name)
                        self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs[name],2)
                        self.assertEqual(glyph_names(name),[name])
                        self.assertEqual(glyph_names(name,{'liga':False}),list(name))
                        self.assertNotIn(name,glyph_names('f\u0301'+name[1]))
                        self.assertEqual(shaped(font,data,name,w),shaped(font,data,encoded,w))
                        advance,boxes=shaped(font,data,encoded+'\u0301',w)
                        self.assertGreaterEqual(boxes[1][1]-boxes[0][3],16)
                        self.assertGreater(boxes[1][0],boxes[0][0]+200)
                        advance2,below=shaped(font,data,name+'\u0326',w)
                        self.assertEqual(advance,advance2)
                        self.assertGreaterEqual(below[0][1]-below[-1][3],16)

    def test_standard_ligature_carets_interpolate(self):
        from fontTools.varLib.instancer import instantiateVariableFont
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                instance=instantiateVariableFont(font,{'wght':w},inplace=False) if 'fvar' in font else font
                carets=instance['GDEF'].table.LigCaretList
                for name,bold in [('fi',344),('fl',360)]:
                    with self.subTest(font=path.name,weight=w,ligature=name):
                        self.assertIn(name,carets.Coverage.glyphs)
                        values=carets.LigGlyph[carets.Coverage.glyphs.index(name)].CaretValue
                        self.assertEqual(len(values),1)
                        self.assertEqual(values[0].Coordinate,round(288+(bold-288)*(w-400)/300))
                        self.assertGreater(values[0].Coordinate,0)
                        self.assertLess(values[0].Coordinate,instance['hmtx'][name][0])

    def test_turned_comma_above_soft_dots_and_stacks(self):
        for path,font in self.fonts():
            data=path.read_bytes();name=font.getBestCmap()[0x312]
            self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs[name],3)
            self.assertEqual(font['hmtx'][name][0],0)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for base in ['a','g','h','i','j','į']:
                    with self.subTest(font=path.name,weight=w,base=base):
                        advance,boxes=shaped(font,data,base+'̒',w)
                        self.assertEqual(len(boxes),2)
                        self.assertGreaterEqual(boxes[1][1]-boxes[0][3],24)
                        stacked,bb=shaped(font,data,base+'̒́',w)
                        self.assertEqual(advance,stacked)
                        self.assertGreaterEqual(bb[-1][1]-bb[-2][3],24)
                        self.assertLessEqual(bb[-1][3],font['OS/2'].usWinAscent)
                        if base in ['i','j','į']:
                            for marks in ['̒','̧̒']:
                                hf=hb.Font(hb.Face(data));hf.set_variations({'wght':w})
                                buf=hb.Buffer();buf.add_str(base+marks);buf.guess_segment_properties();hb.shape(hf,buf)
                                names=[font.getGlyphName(g.codepoint) for g in buf.glyph_infos]
                                self.assertEqual(names[0],{'i':'idotless','j':'jdotless','į':'dotlessiogonek'}[base])

    def test_short_stroke_overlay_centers_and_preserves_accents(self):
        for path,font in self.fonts():
            data=path.read_bytes();name=font.getBestCmap()[0x335]
            self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs[name],3)
            self.assertEqual(font['hmtx'][name][0],0)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for base in ['a','o','h','i','j','á','ā','ą','ȟ','A','O','Ą']:
                    with self.subTest(font=path.name,weight=w,base=base):
                        advance,boxes=shaped(font,data,base+'̵',w)
                        self.assertEqual(advance,shaped(font,data,base,w)[0])
                        self.assertEqual(len(boxes),2)
                        self.assertAlmostEqual((boxes[1][1]+boxes[1][3])/2,384 if base.isupper() else 288,delta=1)
                        if base=='o':
                            self.assertAlmostEqual((boxes[1][0]+boxes[1][2])/2,320+(w-400)/300*32,delta=1)
                        for mark in ['́','̧','̒']:
                            _,combined=shaped(font,data,base+'̵'+mark,w)
                            _,ordinary=shaped(font,data,base+mark,w)
                            self.assertEqual(sorted(combined[:1]+combined[2:]),sorted(ordinary))

    def test_short_overlay_narrow_letters_do_not_touch_following_n(self):
        for path,font in self.fonts():
            data=path.read_bytes()
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for base in ['i','j','l','f','fi','fl','ﬁ','ﬂ']:
                    with self.subTest(font=path.name,weight=w,base=base):
                        _,boxes=shaped(font,data,base+'̵n',w)
                        self.assertGreaterEqual(boxes[-1][0]-boxes[-2][2],16)

    def test_short_slash_overlay_placement_and_neighbor_clearance(self):
        for path,font in self.fonts():
            data=path.read_bytes();name=font.getBestCmap()[0x337]
            self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs[name],3)
            self.assertEqual(font['hmtx'][name][0],0)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for base in ['a','o','h','i','j','á','ā','ą','A','O','Ą']:
                    with self.subTest(font=path.name,weight=w,base=base):
                        advance,boxes=shaped(font,data,base+'̷',w)
                        self.assertEqual(advance,shaped(font,data,base,w)[0])
                        self.assertAlmostEqual((boxes[1][1]+boxes[1][3])/2,384 if base.isupper() else 288,delta=1)
                        for mark in ['́','̧','̒']:
                            _,combined=shaped(font,data,base+'̷'+mark,w)
                            _,ordinary=shaped(font,data,base+mark,w)
                            self.assertEqual(sorted(combined[:1]+combined[2:]),sorted(ordinary))
                for base in ['i','j','l','f','fi','fl','ﬁ','ﬂ']:
                    with self.subTest(font=path.name,weight=w,narrow=base):
                        _,boxes=shaped(font,data,base+'̷n',w)
                        self.assertGreaterEqual(boxes[-1][0]-boxes[-2][2],16)

    def test_long_solidus_overlay_negation_and_attachment(self):
        for path,font in self.fonts():
            data=path.read_bytes();name=font.getBestCmap()[0x338]
            self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs[name],3)
            self.assertEqual(font['hmtx'][name][0],0)
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for encoded,base in [('≠','='),('≮','<'),('≯','>')]:
                    with self.subTest(font=path.name,weight=w,negation=encoded):
                        self.assertEqual(shaped(font,data,encoded,w),shaped(font,data,base+'̸',w))
                        advance,boxes=shaped(font,data,encoded,w)
                        self.assertEqual(advance,shaped(font,data,base,w)[0])
                        body=shaped(font,data,base,w)[1][0]
                        self.assertLess(boxes[-1][1],body[1])
                        self.assertGreater(boxes[-1][3],body[3])
                        if len(boxes)==2:
                            self.assertAlmostEqual((boxes[1][0]+boxes[1][2])/2,(body[0]+body[2])/2,delta=4)
                for base in ['a','o','h','i','j','á','ā','ą','A','O','Ą']:
                    with self.subTest(font=path.name,weight=w,base=base):
                        advance,boxes=shaped(font,data,base+'̸',w)
                        self.assertEqual(advance,shaped(font,data,base,w)[0])
                        self.assertAlmostEqual((boxes[1][1]+boxes[1][3])/2,384 if base.isupper() else 288,delta=1)
                        for mark in ['́','̧','̒']:
                            _,combined=shaped(font,data,base+'̸'+mark,w)
                            _,ordinary=shaped(font,data,base+mark,w)
                            self.assertEqual(sorted(combined[:1]+combined[2:]),sorted(ordinary))
                for base in ['i','j','l','f','fi','fl','ﬁ','ﬂ']:
                    with self.subTest(font=path.name,weight=w,narrow=base):
                        _,boxes=shaped(font,data,base+'̸n',w)
                        self.assertGreaterEqual(boxes[-1][0]-boxes[-2][2],16)

    def test_notequal_encoding_and_missing_cmap_fallback(self):
        for path,font in self.fonts():
            data=path.read_bytes();name=font.getBestCmap()[0x2260]
            self.assertEqual(font['hmtx'][name][0],font['hmtx'][font.getBestCmap()[ord('=')]][0])
            # Remove only the encoding: HarfBuzz must still render canonical NFD.
            fallback=TTFont(io.BytesIO(data))
            for table in fallback['cmap'].tables:
                if table.isUnicode():table.cmap.pop(0x2260,None)
            buf=io.BytesIO();fallback.save(buf);fd=buf.getvalue()
            from fontTools import subset
            options=subset.Options();options.layout_features=['*'];options.glyph_names=True
            sf=TTFont(io.BytesIO(data));ss=subset.Subsetter(options=options)
            ss.populate(text='≠A B1 + 3');ss.subset(sf)
            sb=io.BytesIO();sf.save(sb);sd=sb.getvalue()
            self.assertNotIn(0x2260,sf.getBestCmap())
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                for text in ['≠','A ≠ B','1 + 1 ≠ 3']:
                    with self.subTest(font=path.name,weight=w,text=text):
                        self.assertEqual(shaped(font,data,text,w),shaped(font,data,unicodedata.normalize('NFD',text),w))
                        adv,boxes=shaped(font,data,text,w);fa,fb=shaped(fallback,fd,text,w)
                        self.assertEqual(adv,fa)
                        # Split fallback components have the same total ink bounds.
                        bounds=lambda seq:(min(b[0] for b in seq if b),min(b[1] for b in seq if b),max(b[2] for b in seq if b),max(b[3] for b in seq if b))
                        self.assertEqual(bounds(boxes),bounds(fb))
                        sa,sboxes=shaped(sf,sd,text,w)
                        self.assertEqual(adv,sa)
                        self.assertEqual(bounds(boxes),bounds(sboxes))

    def test_plusminus_lower_bar_stays_separate_and_not_sign_is_visible(self):
        from fontTools.pens.recordingPen import DecomposingRecordingPen
        for path,font in self.fonts():
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                gs=font.getGlyphSet(location={'wght':w} if 'fvar' in font else None)
                with self.subTest(font=path.name,weight=w):
                    name=font.getBestCmap()[0xB1]
                    pen=DecomposingRecordingPen(gs);gs[name].draw(pen)
                    contours=[]
                    for op,points in pen.value:
                        if op=='moveTo':contours.append(list(points))
                        elif op=='lineTo':contours[-1].extend(points)
                    self.assertEqual(len(contours),2)
                    ranges=sorted((min(y for x,y in c),max(y for x,y in c)) for c in contours)
                    self.assertGreaterEqual(ranges[1][0]-ranges[0][1],40)
                    for text in ['±','¬']:
                        advance,boxes=shaped(font,path.read_bytes(),text,w)
                        self.assertEqual(advance,600)
                        self.assertEqual(len(boxes),1)
                        self.assertGreater(boxes[0][3]-boxes[0][1],160)
                        self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(font.getBestCmap()[ord(text)],1),1)

    def test_inequality_symbols_keep_clear_lower_bars(self):
        for path,font in self.fonts():
            data=path.read_bytes()
            for w in ([400,475,550,625,700] if 'fvar' in font else [font['OS/2'].usWeightClass]):
                gs=font.getGlyphSet(location={'wght':w} if 'fvar' in font else None)
                for cp in [0x2264,0x2265]:
                    with self.subTest(font=path.name,weight=w,cp=hex(cp)):
                        name=font.getBestCmap()[cp]
                        self.assertEqual(font['GDEF'].table.GlyphClassDef.classDefs.get(name),1)
                        from fontTools.pens.recordingPen import DecomposingRecordingPen
                        pen=DecomposingRecordingPen(gs);gs[name].draw(pen);contours=[]
                        for op,pts in pen.value:
                            if op=='moveTo':contours.append([pts[0]])
                            elif op=='lineTo':contours[-1].append(pts[0])
                        self.assertEqual(len(contours),2)
                        contours.sort(key=lambda p:min(y for x,y in p))
                        self.assertGreaterEqual(min(y for x,y in contours[1])-max(y for x,y in contours[0]),40)
                        self.assertEqual(shaped(font,data,chr(cp),w)[0],600)
                for base,encoded in [('≤','≰'),('≥','≱')]:
                    with self.subTest(font=path.name,weight=w,negation=encoded):
                        expected=shaped(font,data,base+'̸',w)
                        self.assertEqual(shaped(font,data,encoded,w),expected)
                        self.assertEqual(expected[0],600)
                        self.assertLess(expected[1][1][1],expected[1][0][1])
                        self.assertGreater(expected[1][1][3],expected[1][0][3])
                # No programming-language sequence substitution was introduced.
                self.assertEqual(len(shaped(font,data,'<=',w)[1]),2)
                self.assertEqual(len(shaped(font,data,'>=',w)[1]),2)
