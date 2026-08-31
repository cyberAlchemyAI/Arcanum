#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,tempfile,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/post_produce_validation.py";s=importlib.util.spec_from_file_location("post",P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class T(unittest.TestCase):
 def setUp(self):self.t=tempfile.TemporaryDirectory();self.r=Path(self.t.name);(self.r/"out").mkdir();(self.r/"out/result.json").write_text("{}\n");self.cmd=[{"phase":"post-produce","argv":["python3","-c","import json;json.load(open('out/result.json'))"],"cwd":"."}]
 def tearDown(self):self.t.cleanup()
 def test_valid_actual_output_passes(self):self.assertEqual(m.validate("U",self.r,["out/result.json"],self.cmd)["result"],"pass")
 def test_missing_output_blocks(self):(self.r/"out/result.json").unlink();self.assertRaises(m.PostProduceBlock,m.validate,"U",self.r,["out/result.json"],self.cmd)
 def test_undeclared_output_blocks(self):self.assertRaises(m.PostProduceBlock,m.validate,"U",self.r,["out/result.json"],self.cmd,["out/result.json","out/extra.json"])
 def test_failed_validation_blocks(self):self.cmd[0]["argv"]=["python3","-c","raise SystemExit(7)"];self.assertRaises(m.PostProduceBlock,m.validate,"U",self.r,["out/result.json"],self.cmd)
if __name__=="__main__":unittest.main()
