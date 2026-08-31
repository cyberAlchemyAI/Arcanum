#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, tempfile, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/validate_selected_unit_inputs.py"
s=importlib.util.spec_from_file_location("selected",P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class T(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.r=Path(self.t.name);(self.r/"bin").mkdir();(self.r/"out").mkdir();(self.r/"bin/runner.py").write_text("pass\n")
  self.c={"schema_version":"implementation-readiness.selected-unit-admission.v1","unit_id":"SWU-GENERIC-001","repository_root":".","targets":[{"path":"out/future.json","disposition":"create","collision_policy":"fail-if-exists","baseline_sha256":None}],"validation_commands":[{"phase":"post-produce","argv":["python3","out/future.json"],"cwd":"."}],"runner":{"path":"bin/runner.py","sha256":hashlib.sha256((self.r/"bin/runner.py").read_bytes()).hexdigest()}}
 def tearDown(self):self.t.cleanup()
 def test_absent_create_output_is_ready(self):
  x=m.validate(self.c,self.r);self.assertEqual(x["result"],"pass");self.assertFalse(x["outputs_validated"])
 def test_collision_blocks(self):
  (self.r/"out/future.json").write_text("x");self.assertRaises(m.AdmissionBlock,m.validate,self.c,self.r)
 def test_update_requires_exact_baseline(self):
  self.c["targets"][0].update(disposition="update",collision_policy="not-applicable",baseline_sha256="0"*64);self.assertRaises(m.AdmissionBlock,m.validate,self.c,self.r)
 def test_future_output_cannot_be_preexecution_input(self):
  self.c["validation_commands"][0]["phase"]="pre-execution";self.assertRaises(m.AdmissionBlock,m.validate,self.c,self.r)
if __name__=="__main__":unittest.main()
