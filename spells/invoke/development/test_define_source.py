#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path

INVOKE=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location("compile_define_source",INVOKE/"scripts/compile_define_source.py")
assert SPEC and SPEC.loader
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

class DefineProducerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name); (self.repo/"inputs").mkdir()
        self.discovery=self.repo/"inputs/discovery.md"; self.discovery.write_text("discovery\n")
        self.source=self.repo/"DEFINE-SOURCE.json"; self.out=self.repo/"out"
        self.base={
          "schema_version":"invoke.define-source.v1","source_id":"DEFINE-FIXTURE-001","target":{"id":"Generic Capability","objective":"Establish one generic public specification baseline."},
          "discovery":{"kind":"artifact","ref":self.ref(self.discovery,"inputs/discovery.md")},
          "template_selection":{"profile_id":"invoke.generic-spec-baseline.v1","selected":"invoke.generic-spec-baseline.v1","eligible":["invoke.generic-spec-baseline.v1"],"tie":False},
          "spec_declarations":[{"id":"D-001","title":"Boundary","statement":"The capability remains repository-local and authority-free."}],
          "glossary":[{"term":"baseline","definition":"A validated starting contract.","link_status":"no-match","rationale":"No upstream glossary is selected."}],
          "layering":{"kind":"gap","rationale":"Layering is deferred to a later planning mode."},
          "dispatch_trace":{"techniques":["sequence","owner_boundary_check"]},
          "distill":{"classification":"not-required","rationale":"The Define target is one narrow specification unit."},
          "identity_denominator":{"classification":"not-applicable","rationale":"No canonical ID-to-label denominator is asserted."},
          "output_contracts":{"spec":"SPEC.md","glossary":"GLOSSARY.md","layering":"LAYERING-GAP.md","template_selection":"TEMPLATE-SELECTION-RECEIPT.json","dispatch_trace":"DISPATCH-TRACE.json","distill":"DISTILL-RECEIPT.json","identity_denominator":"IDENTITY-DENOMINATOR-RECEIPT.json","transport":"DEFINE-TRANSPORT-REPORT.json","stage_receipt":"INVOKE-DEFINE-STAGE-RECEIPT.json"},
          "transport_policy":{"append_existing_only":True,"upstream_mutation":False,"targets":[]},"next_route":"design"}
    def tearDown(self): self.tmp.cleanup()
    def ref(self,p,label):
        b=p.read_bytes(); return {"path":label,"sha256":hashlib.sha256(b).hexdigest(),"size":len(b)}
    def write(self,d): self.source.write_text(json.dumps(d,indent=2)+"\n")
    def compile(self,d,late=None): self.write(d); return M.compile_source(self.source,self.out,self.repo,INVOKE/"schemas",late)
    def test_positive_is_atomic_and_deterministic(self):
        r=self.compile(copy.deepcopy(self.base)); self.assertEqual("pass",r["result"]); self.assertEqual(9,len(list(self.out.iterdir())))
        first={p.name:p.read_bytes() for p in self.out.iterdir()}; out2=self.repo/"out2"; M.compile_source(self.source,out2,self.repo,INVOKE/"schemas"); self.assertEqual(first,{p.name:p.read_bytes() for p in out2.iterdir()})
    def test_schema_and_policy_negatives_leave_output_absent(self):
        mutations=[]
        for fn in [
          lambda d:d.update(discovery={"kind":"waiver","waiver_reason":"short"}),
          lambda d:d["template_selection"].update(tie=True),
          lambda d:d["template_selection"].update(profile_id="legacy.profile"),
          lambda d:d["glossary"][0].update(rationale=""),
          lambda d:d.update(layering={"kind":"gap","rationale":"short"}),
          lambda d:d.update(dispatch_trace={"techniques":[]}),
          lambda d:d.update(distill={"classification":"not-required","rationale":"short"}),
          lambda d:d.update(identity_denominator={"classification":"required"}),
          lambda d:d["transport_policy"].update(targets=["upstream.md"]),
          lambda d:d["transport_policy"].update(upstream_mutation=True),
        ]:
            d=copy.deepcopy(self.base); fn(d); mutations.append(d)
        for i,d in enumerate(mutations):
            with self.subTest(i=i):
                self.out=self.repo/f"bad-{i}"; self.write(d)
                with self.assertRaises(ValueError): M.compile_source(self.source,self.out,self.repo,INVOKE/"schemas")
                self.assertFalse(self.out.exists())
    def test_stale_denominator_collision_and_late_failure_are_atomic(self):
        request=self.repo/"inputs/request.json"; request.write_text("{}\n")
        result=self.repo/"inputs/result.json"; result.write_text('{"verdict":"pass"}\n')
        d=copy.deepcopy(self.base); d["identity_denominator"]={"classification":"required","request_ref":self.ref(request,"inputs/request.json"),"result_ref":self.ref(result,"inputs/result.json")}
        d["identity_denominator"]["result_ref"]["sha256"]="0"*64
        self.write(d)
        with self.assertRaisesRegex(ValueError,"stale"): M.compile_source(self.source,self.out,self.repo,INVOKE/"schemas")
        self.assertFalse(self.out.exists())
        self.out.mkdir()
        with self.assertRaisesRegex(ValueError,"absent"): M.compile_source(self.source,self.out,self.repo,INVOKE/"schemas")
        self.out.rmdir(); d=copy.deepcopy(self.base)
        with self.assertRaisesRegex(RuntimeError,"late"): self.compile(d,lambda _:(_ for _ in ()).throw(RuntimeError("late failure")))
        self.assertFalse(self.out.exists())

if __name__=="__main__": unittest.main(verbosity=2)
