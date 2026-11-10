import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from train_variable_pilot import run

class PilotLimits(unittest.TestCase):
    def test_rejects_unbounded_runs_before_io(self):
        for steps,seconds in [(0,1),(100001,1),(1,0),(1,1801)]:
            with self.subTest(steps=steps,seconds=seconds),self.assertRaises(ValueError):
                run('/nonexistent','/nonexistent',max_steps=steps,max_seconds=seconds)

    def test_extended_run_still_bounded_before_io(self):
        for steps,seconds in [(2000001,3600),(100,7201)]:
            with self.subTest(steps=steps,seconds=seconds),self.assertRaises(ValueError):
                run('/nonexistent','/nonexistent',max_steps=steps,max_seconds=seconds,extended_run=True)
