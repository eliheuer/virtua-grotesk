"""Regression cases for context retrieval, protection and evidence integrity."""
import copy
import importlib.util
import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import design_context as dc
import glyph_ai_harness as harness
import symbol_gen

class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = dc.load_records(ROOT)
        cls.contract = dc.read_json(ROOT / 'design/system/contract.json')

    def selected(self, name, script, operation, masters=None):
        return dc.select_records(self.records, {name}, {script}, operation, masters)

    def test_seen_negative_and_live_green_donors(self):
        packet = dc.build_packet(ROOT, ['seen-ar'], ['Regular','Bold'], 'curve-repair')
        records = {r['id']: r for r in packet['records']}
        self.assertEqual(records['seen-v4-rejected']['visual_verdict'], 'rejected')
        self.assertEqual(records['seen-v4-rejected']['training_eligibility'], 'negative-example')
        for name in ('seen-ar.init', 'seen-ar.medi'):
            ref = next(g for g in packet['references'] if g['glyph']==name and g['master']=='Regular')
            self.assertTrue(ref['color']['reference_eligible'])
            self.assertEqual(dc.digest(ROOT/ref['path']), ref['sha256'])
        self.assertIn('anchor-seen-splice', records)
        self.assertNotIn('anchor-dollar', records)
        self.assertNotIn('anchor-arabic-attachments', records)
        self.assertEqual(dc.verify_packet(ROOT,packet), [])

    def test_weight_transfer_includes_counterexample(self):
        selected=self.selected('zayin-hb','hebrew','weight-transfer',['Bold'])
        self.assertIn('zayin-bold-02',selected)
        self.assertIn('hamza-bold-01',selected)
        self.assertNotIn('zayin-regular-01',selected)

    def test_intent_and_rejection_are_retrievable(self):
        self.assertIn('final-yeh-preserve',self.selected('yeh-ar.fina','arabic','redraw'))
        self.assertIn('at-rejected',self.selected('at','symbols','curve-repair'))
        self.assertNotIn('anchor-arabic-attachments',self.selected('kaf-ar','arabic','spacing'))
        self.assertIn('anchor-arabic-attachments',self.selected('kaf-ar','arabic','anchors'))

    def test_symbol_names_do_not_route_to_latin(self):
        self.assertEqual(dc.glyph_script('dollar',{'unicodes':[0x24]}),'symbols')
        self.assertEqual(dc.glyph_script('Aacute',{'unicodes':[0xc1]}),'latin')
        self.assertEqual(dc.glyph_script('seen-ar.init'),'arabic')

    def test_green_variants_and_conflicting_labels(self):
        for color in ['0,1,0,1','0.09,0.72,0.44,1']:
            self.assertTrue(dc.color_state({'public.markColor':color},self.contract)['reference_eligible'])
            state=dc.color_state({'public.markColor':color,'com.runebender.markLabel':'red'},self.contract)
            self.assertTrue(state['protected']);self.assertFalse(state['reference_eligible'])
        for color in ['1,1,0,1','0.54,0.44,0.88,1','unknown']:
            self.assertFalse(dc.color_state({'public.markColor':color},self.contract)['reference_eligible'])
        self.assertFalse(dc.color_state({'public.markColor':'0.3,0.8,0.3,1','com.runebender.markLabel':'green'},self.contract)['reference_eligible'])

    def test_recursive_consumers_and_cycles(self):
        inv={'base':{'components':[]},'accent':{'components':[{'base':'base'}]},'green':{'components':[{'base':'accent'}]},'cycle':{'components':[{'base':'cycle'}]}}
        self.assertEqual(dc.closure(inv,['base'],reverse=True),{'base','accent','green'})
        self.assertEqual(dc.closure(inv,['green']),{'base','accent','green'})
        self.assertEqual(dc.closure(inv,['cycle']),{'cycle'})

    def test_new_glyph_fallback_is_explicit(self):
        packet=dc.build_packet(ROOT,['nonexistent-ar'],['Regular'],'draw')
        self.assertTrue(packet['targets'][0]['missing'])
        self.assertTrue(any('no source glyph' in w for w in packet['warnings']))
        self.assertIn('arabic',{r['id'] for r in packet['records']})

    def test_library_hashes_and_pair_validation(self):
        self.assertEqual(dc.validate_library(ROOT),[])
        bad=copy.deepcopy(self.records)
        bad['seen-v4-rejected']['training_eligibility']='approved-pair'
        with patch.object(dc,'load_records',return_value=bad):
            errors=dc.validate_library(ROOT)
        self.assertTrue(any('rejected candidate' in e for e in errors))
        bad=copy.deepcopy(self.records)
        bad['hamza-bold-01']['evidence']=[]
        with patch.object(dc,'load_records',return_value=bad):
            self.assertTrue(any('no hashed evidence' in e for e in dc.validate_library(ROOT)))

    def test_stale_source_and_new_correction_invalidate_packet(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'design/corrections/records').mkdir(parents=True)
            source=root/'donor.glif';source.write_text('before')
            packet={'schema_version':1,'guard_hashes':{'donor.glif':dc.digest(source)},'correction_inventory':{}}
            self.assertEqual(dc.verify_packet(root,packet),[])
            source.write_text('human edit')
            self.assertIn('donor.glif',dc.verify_packet(root,packet))
            (root/'design/corrections/records/new.json').write_text('{}')
            self.assertIn('design/corrections/records (index changed)',dc.verify_packet(root,packet))
            with self.assertRaises(ValueError):dc.local_path(root,'../outside')

    def test_harness_refuses_unapproved_reference_before_rendering(self):
        with tempfile.TemporaryDirectory() as d, patch.object(harness,'render_glyph_png') as render:
            with self.assertRaises(SystemExit):
                harness.prepare_run('seen-ar',['seen-ar'],['regular','bold'],Path(d)/'new','baseline:cap')
            render.assert_not_called()
        self.assertEqual(harness.mark_role('0,1,0,1'),'good-reference')
        self.assertNotEqual(harness.mark_role('1,0.86,0.2,1'),'orange-mark')

    def test_harness_packet_carries_context_and_stale_trace_stops_before_writing(self):
        def rendered(master, glyph, path):
            return {'master':master, 'glyph':glyph, 'path':str(path)}
        with tempfile.TemporaryDirectory() as d, patch.object(harness,'render_glyph_png',side_effect=rendered):
            run=Path(d)/'packet'
            manifest=harness.prepare_run('seen-ar',['n'],['regular','bold'],run,'-256:576')
            self.assertEqual(json.loads(manifest.read_text())['schema'],'virtua-grotesk.glyph-ai-run.v2')
            self.assertEqual(dc.verify_packet(ROOT,json.loads((run/'context.json').read_text())),[])
            self.assertIn('Seen v4',(run/'context.md').read_text())
            with patch.object(harness,'verify_packet',return_value=['changed donor']):
                with self.assertRaises(SystemExit):harness.trace_run(run,'img2bez')
            self.assertFalse((run/'trace').exists())

    def test_harness_joint_trace_uses_calibrated_fit_and_report(self):
        command=harness.img2bez_command('test',{'fit':'-16:592'},Path('/scratch'))
        self.assertEqual(command[:2],['img2bez','masters'])
        self.assertIn('-16:592',command)
        self.assertEqual(command.count('--image'),2)
        self.assertIn('--fail-on-low-confidence',command)

class SymbolOutputTests(unittest.TestCase):
    def test_no_implicit_active_source_write_and_purple_output(self):
        with patch.object(symbol_gen, 'OUTPUT_ROOT', None):
            with self.assertRaises(ValueError):
                symbol_gen.write('Regular','equal','003D',600,[])
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve()
            with patch.object(symbol_gen,'REPO',root), patch.object(symbol_gen,'OUTPUT_ROOT',root/'out/scratch'):
                path=symbol_gen.write('Regular','test',None,512,[[(0,0),(64,0),(64,64),(0,64)]])
                self.assertIn('0.54,0.44,0.88,1',path.read_text())
                self.assertTrue(path.is_relative_to(root/'out'))
                with self.assertRaises(ValueError):
                    symbol_gen.write('Regular','test',None,512,[[(0,0),(64,0),(64,64),(0,64)]])

class CompatibilityGateTests(unittest.TestCase):
    def test_mismatch_fails_but_report_only_remains_available(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name,ptype in [('Regular','line'),('Bold','curve')]:
                g=root/name/'glyphs';g.mkdir(parents=True)
                (g/'contents.plist').write_bytes(plistlib.dumps({'test':'test.glif'}))
                (g/'test.glif').write_text(f'<glyph name="test"><advance width="500"/><outline><contour><point x="0" y="0" type="{ptype}"/></contour></outline></glyph>')
            cmd=[sys.executable,str(ROOT/'scripts/report_master_compatibility.py'),str(root/'Regular'),str(root/'Bold')]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertEqual(subprocess.run(cmd+['--check'],capture_output=True).returncode,1)

if __name__=='__main__':unittest.main()
