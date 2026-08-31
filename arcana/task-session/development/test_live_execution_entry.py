#!/usr/bin/env python3
"""Focused end-to-end regressions for live preparation and early-block closure."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


TASK = Path(__file__).resolve().parent.parent
REPO = TASK.parents[2]
INVOKE = REPO / "arcanum/spells/invoke"
sys.path.insert(0, str(TASK / "scripts"))


def load_module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


FIXTURE = load_module(TASK / "development/validate-governance-runner.py", "live_entry_fixture")
TERMINALIZER = load_module(TASK / "scripts/terminalize_pre_execution_failure.py", "live_entry_terminalizer")
INPUT_CLOSURE = load_module(TASK / "scripts/invocation_input_closure.py", "live_entry_input_closure")
OWNER_FIXTURE = load_module(
    INVOKE / "development/preacceptance-closure/test_preacceptance_closure.py",
    "live_entry_owner_request_fixture",
)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data=path.read_bytes(); return {"path":path.relative_to(root).as_posix(),"sha256":hashlib.sha256(data).hexdigest(),"size_bytes":len(data)}


def executable_identity() -> dict[str, Any]:
    path=Path(sys.executable); data=path.read_bytes(); return {"path":str(path),"sha256":hashlib.sha256(data).hexdigest(),"size_bytes":len(data)}


def invocation(root: Path, runner: Path, argv: list[str], inputs: list[dict[str, Any]], owner_roots: list[str] | None = None) -> dict[str, Any]:
    relative=runner.relative_to(root).as_posix()
    if owner_roots is None:
        if relative.startswith("arcanum/arcana/task-session/"): owner_roots=["arcanum/arcana/task-session"]
        elif relative.startswith("arcanum/spells/invoke/"): owner_roots=["arcanum/spells/invoke"]
        else: owner_roots=[runner.parent.relative_to(root).as_posix()]
    closure_id="fixture-"+hashlib.sha256((relative+json.dumps(inputs,sort_keys=True)).encode()).hexdigest()[:16]
    closure=INPUT_CLOSURE.build(root,closure_id,owner_roots,inputs)
    closure_path=root/"scenario/input-closures"/f"{closure_id}.json"; write_json(closure_path,closure)
    return {"runner_ref":exact_ref(root,runner),"executable_identity":executable_identity(),"argv":argv,"cwd":".","input_closure_ref":exact_ref(root,closure_path),"input_refs":closure["input_refs"],"environment":{"PYTHONDONTWRITEBYTECODE":"1","TMPDIR":"/tmp"},"timeout_seconds":60,"max_output_bytes":1048576,"network_allowed":False,"external_effects_allowed":False}


class LiveExecutionEntryTests(unittest.TestCase):
    def setUp(self)->None:
        self.temp=tempfile.TemporaryDirectory(); base=Path(self.temp.name)
        self.repo=FIXTURE.scenario(base,TASK,TASK)
        shutil.copytree(TASK,self.repo/"arcanum/arcana/task-session",dirs_exist_ok=True)
        shutil.copytree(INVOKE,self.repo/"arcanum/spells/invoke",dirs_exist_ok=True)
        owner_fixture_support={*OWNER_FIXTURE.REAL_CONSUMER_ENTRYPOINTS}
        for _,paths in OWNER_FIXTURE.ENTRY_CONSUMERS.values(): owner_fixture_support.update(paths)
        owner_fixture_support.add("arcanum/arcana/continuation-router/schemas/work-pack-route-admission.schema.json")
        for relative in sorted(owner_fixture_support):
            source=REPO/relative; target=self.repo/relative
            target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target)
        producer=self.repo/"scenario/readiness-producer/produce_readiness.py"; producer.parent.mkdir(parents=True,exist_ok=True)
        producer.write_text("#!/usr/bin/env python3\nimport json, pathlib, sys\np=pathlib.Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps({'result':'pass'},sort_keys=True)+'\\n',encoding='utf-8')\n",encoding="utf-8")
        blocker=self.repo/"scenario/blocker.json"; write_json(blocker,{"code":"DELIBERATE_PRE_EXECUTION_BLOCK"})
        expected_bytes=(json.dumps({"result":"pass"},sort_keys=True)+"\n").encode()
        attempt="synthetic-run-003"
        run_dir="runs/run-1"
        controls=[
            {"path":"live/readiness.json","owner_capability":"work-pack-readiness-audit","write_class":"readiness-evidence","attempt_id":attempt,"baseline":{"state":"absent","sha256":None,"size_bytes":None},"expected_postimage_ref":{"path":"live/readiness.json","sha256":hashlib.sha256(expected_bytes).hexdigest(),"size_bytes":len(expected_bytes)},"runtime_revalidation":"exact-postimage-before-consume"},
        ]
        for index,phase in enumerate(("resolved","governed","admitted","ticketed","execution-received","reconciled"),start=1):
            controls.append({"path":f"{run_dir}/checkpoints/{index:02d}-{phase}.json","owner_capability":"task-session","write_class":"governance-checkpoint","attempt_id":attempt,"baseline":{"state":"absent","sha256":None,"size_bytes":None},"runtime_revalidation":"baseline-before-write"})
        for path,write_class in ((f"{run_dir}/execution-ticket.json","execution-ticket"),(f"{run_dir}/reconciliation.json","reconciliation-evidence"),(f"{run_dir}/commit-journal.json","commit-evidence"),(f"{run_dir}/commit-receipt.json","commit-evidence")):
            controls.append({"path":path,"owner_capability":"task-session","write_class":write_class,"attempt_id":attempt,"baseline":{"state":"absent","sha256":None,"size_bytes":None},"runtime_revalidation":"baseline-before-write"})
        preparation_receipt_path="live/preparation-receipt.json"
        controls.append({"path":preparation_receipt_path,"owner_capability":"task-session","write_class":"preparation-receipt","attempt_id":attempt,"baseline":{"state":"absent","sha256":None,"size_bytes":None},"runtime_revalidation":"baseline-before-write"})
        partition={"schema_version":"task-session.live-control-evidence-partition.v1","attempt_id":attempt,"repository_root":".","outputs":controls,"exact_union_scope":[item["path"] for item in controls]}
        partition_path=self.repo/"scenario/control-partition.json"; write_json(partition_path,partition)
        request_path=self.repo/"scenario/request.json"; request=json.loads(request_path.read_text())
        terminal="results/task-session-terminal.json"; owner_output="results/invoke-block-owner.json"; continuity="results/continuity.json"
        authority_ceiling=sorted({
            *partition["exact_union_scope"], terminal, owner_output, continuity,
            *request["execution_contract"]["allowed_writes"],
            *[item["path"] for item in request["execution_contract"].get("transient_outputs",[])],
        })
        owner_request,owner_graph_refs=OWNER_FIXTURE.build_canonical_owner_request_fixture(
            self.repo,
            request_id="OWNER-REQUEST-1",
            authority_write_ceiling=authority_ceiling,
        )
        owner=self.repo/"fixture/owner-request-v2.json"
        requested_effect=owner_request["base_request"]["requested_effect"]
        response=self.repo/"scenario/owner-response.json"
        response_document={"schema_version":"invoke.owner-acceptance-response.v1","response_id":"OWNER-RESPONSE-1","request_ref":exact_ref(self.repo,owner),"request_id":owner_request["request_id"],"request_digest":owner_request["request_digest"],"decision":"accepted","authorization_token":f"ACCEPT-{owner_request['request_id']}-{owner_request['request_digest']}","actor":{"capability":"owner","subject":"fixture-owner","provenance":"current-user-exact-token"},"requested_effect_digest":hashlib.sha256(json.dumps(requested_effect,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"authority_write_ceiling_digest":hashlib.sha256(json.dumps(authority_ceiling,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"attempt_id":attempt,"one_attempt_ceiling":1,"authority_effect":"accept-exact-request-for-one-attempt-only"}
        response_document["response_digest"]=hashlib.sha256(json.dumps(response_document,sort_keys=True,separators=(",",":")).encode()).hexdigest(); write_json(response,response_document)
        runner_path=self.repo/"arcanum/arcana/task-session/scripts/task-session-governance-runner.py"
        response_validator=self.repo/"arcanum/spells/invoke/scripts/validate_owner_acceptance_response.py"
        response_schema=self.repo/"arcanum/spells/invoke/schemas/owner-acceptance-response-v1.schema.json"
        owner_validation_inputs=[exact_ref(self.repo,path) for path in (response_validator,response_schema,response)] + owner_graph_refs
        producer_invocation=invocation(self.repo,producer,["{executable}","{runner}","live/readiness.json"],[exact_ref(self.repo,producer)])
        runner_inputs=[exact_ref(self.repo,path) for path in [runner_path,self.repo/"arcanum/arcana/task-session/scripts/control_evidence_partition.py",self.repo/"arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py",self.repo/"arcanum/arcana/task-session/schemas/governance-run-request.schema.json",self.repo/"arcanum/arcana/task-session/schemas/live-control-evidence-partition-v1.schema.json",self.repo/"arcanum/arcana/task-session/schemas/live-execution-entry-preparation-receipt-v1.schema.json",self.repo/"arcanum/arcana/task-session/schemas/execution-ticket.schema.json",self.repo/"arcanum/arcana/task-session/schemas/governance-phase-receipt.schema.json",self.repo/"arcanum/arcana/task-session/schemas/executor-receipt.schema.json",self.repo/"scenario/WORK-PACK.md",self.repo/"scenario/TASK.md",self.repo/"scenario/controls/evaluation.json",self.repo/"scenario/controls/admission.json",self.repo/"scenario/controls/preflight.json",partition_path]]
        governance={**invocation(self.repo,runner_path,["{executable}","{runner}","prepare","--repo-root","{repo_root}","--request","{request}","--run-dir","{run_dir}"],runner_inputs,["arcanum/arcana/task-session","arcanum/spells/implementation-readiness"]),"output_paths":[f"{run_dir}/checkpoints/01-resolved.json",f"{run_dir}/checkpoints/02-governed.json",f"{run_dir}/checkpoints/03-admitted.json",f"{run_dir}/checkpoints/04-ticketed.json",f"{run_dir}/execution-ticket.json"]}
        governance.pop("cwd")
        preparation={"schema_version":"task-session.live-execution-entry-preparation.v1","attempt_id":attempt,"control_evidence_partition_ref":exact_ref(self.repo,partition_path),"owner_acceptance_request_ref":exact_ref(self.repo,owner),"owner_acceptance_response_ref":exact_ref(self.repo,response),"authority_write_ceiling_digest":response_document["authority_write_ceiling_digest"],"owner_acceptance_validation":invocation(self.repo,response_validator,["{executable}","{runner}","--repo-root","{repo_root}","--response","{owner_response}"],owner_validation_inputs),"preparation_steps":[{"step_id":"readiness","owner_capability":"work-pack-readiness-audit","invocation":producer_invocation,"output_paths":["live/readiness.json"]}],"governance_runner":governance,"run_dir":run_dir,"preparation_receipt_path":preparation_receipt_path,"shadow_mode_supported":True}
        preparation_path=self.repo/"scenario/live-preparation.json"; write_json(preparation_path,preparation)
        lifecycle=[{"path":owner_output,"owner_capability":"invoke","write_class":"owner-closeout-receipt"},{"path":continuity,"owner_capability":"task-session","write_class":"continuity-cursor"}]
        request["control_evidence_partition"]=partition
        request["live_execution_entry_preparation_ref"]=exact_ref(self.repo,preparation_path)
        request["live_execution_entry_preparation_receipt_path"]=preparation_receipt_path
        request["fast_execution_entry"]={"request_ref":exact_ref(self.repo,owner),"receipt_ref":exact_ref(self.repo,owner),"route_scope_partition":{"schema_version":"task-session.fast-entry-route-scope-partition.v1","executor_write_scopes":request["execution_contract"]["allowed_writes"],"terminal_receipt_scope":terminal,"lifecycle_owner_scopes":lifecycle,"control_evidence_partition":partition,"exact_union_scope":[*request["execution_contract"]["allowed_writes"],terminal,*[item["path"] for item in lifecycle],*partition["exact_union_scope"]]}}
        request["closeout_contract"]["terminal_receipt_path"]=terminal
        profile={"schema_version":"task-session.pre-execution-failure-terminalization.v1","work_pack_id":"WP-SYNTHETIC","task_id":request["task_id"],"swu_id":request["swu_id"],"attempt_id":attempt,"owner_acceptance_request_ref":exact_ref(self.repo,owner),"owner_acceptance_response_ref":exact_ref(self.repo,response),"control_evidence_partition_ref":exact_ref(self.repo,partition_path),"failure_terminal_schema_ref":exact_ref(self.repo,self.repo/"arcanum/arcana/task-session/schemas/pre-execution-failure-terminal-receipt-v1.schema.json"),"invoke_owner_schema_ref":exact_ref(self.repo,self.repo/"arcanum/spells/invoke/schemas/pre-execution-block-owner-receipt-v1.schema.json"),"continuity_schema_ref":exact_ref(self.repo,self.repo/"arcanum/arcana/task-session/continuity.schema.json"),"blocker_refs":[exact_ref(self.repo,blocker)],"control_refs":[controls[0]["expected_postimage_ref"]],"terminal_receipt_path":terminal,"invoke_owner_receipt_path":owner_output,"continuity_cursor_path":continuity,"continuity_updated_at":"2026-01-01T00:00:00Z","requested_effect":"record-pre-execution-block-with-no-product-effect"}
        profile["blocker_fingerprint"]=TERMINALIZER.blocker_fingerprint(profile)
        request["failure_terminalization"]=profile; write_json(request_path,request)
        self.request=request_path; self.preparation=preparation_path

    def tearDown(self)->None: self.temp.cleanup()

    def command(self,repo:Path,*args:str)->subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable,*args],cwd=repo,check=False,capture_output=True,text=True,env={"PYTHONDONTWRITEBYTECODE":"1","TMPDIR":"/tmp"})

    def test_shadow_success_and_pre_execution_block_are_both_real(self)->None:
        failure=Path(self.temp.name)/"failure"; shutil.copytree(self.repo,failure)
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        success=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","shadow","--shadow-root",str(self.repo))
        self.assertEqual(success.returncode,0,success.stdout+success.stderr); self.assertEqual(len(json.loads(success.stdout)["observed_writes"]),7)
        coord=failure/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        stopped=self.command(failure,str(coord),"--repo-root",str(failure),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","shadow","--shadow-root",str(failure),"--stop-after","readiness")
        self.assertEqual(stopped.returncode,0,stopped.stdout+stopped.stderr)
        terminal=self.command(failure,str(failure/"arcanum/arcana/task-session/scripts/terminalize_pre_execution_failure.py"),"--repo-root",str(failure),"--request","scenario/request.json")
        self.assertEqual(terminal.returncode,0,terminal.stdout+terminal.stderr)
        owner=self.command(failure,str(failure/"arcanum/spells/invoke/scripts/handle_pre_execution_block.py"),"--repo-root",str(failure),"--request","scenario/request.json","--terminal-receipt","results/task-session-terminal.json")
        self.assertEqual(owner.returncode,0,owner.stdout+owner.stderr)
        cursor=self.command(failure,str(failure/"arcanum/arcana/task-session/scripts/emit_pre_execution_failure_continuity.py"),"--repo-root",str(failure),"--request","scenario/request.json","--terminal-receipt","results/task-session-terminal.json","--owner-receipt","results/invoke-block-owner.json")
        self.assertEqual(cursor.returncode,0,cursor.stdout+cursor.stderr); self.assertFalse((failure/"runs/run-1").exists())

    def test_early_block_closes_present_subset_without_requiring_future_controls(self)->None:
        partition_path=self.repo/"scenario/control-partition.json"
        partition=json.loads(partition_path.read_text())
        future_bytes=(json.dumps({"result":"future"},sort_keys=True)+"\n").encode()
        future={"path":"live/selection.json","owner_capability":"task-session","write_class":"selection-evidence","attempt_id":"synthetic-run-003","baseline":{"state":"absent","sha256":None,"size_bytes":None},"expected_postimage_ref":{"path":"live/selection.json","sha256":hashlib.sha256(future_bytes).hexdigest(),"size_bytes":len(future_bytes)},"runtime_revalidation":"exact-postimage-before-consume"}
        partition["outputs"].append(future); partition["exact_union_scope"].append(future["path"])
        write_json(partition_path,partition)
        partition_ref=exact_ref(self.repo,partition_path)
        request=json.loads(self.request.read_text())
        request["control_evidence_partition"]=partition
        route=request["fast_execution_entry"]["route_scope_partition"]
        route["control_evidence_partition"]=partition
        route["exact_union_scope"].append(future["path"])
        request["failure_terminalization"]["control_evidence_partition_ref"]=partition_ref
        request["failure_terminalization"]["blocker_fingerprint"]=TERMINALIZER.blocker_fingerprint(request["failure_terminalization"])
        write_json(self.request,request)
        readiness=self.repo/"live/readiness.json"
        readiness.parent.mkdir(parents=True,exist_ok=True)
        readiness.write_bytes((json.dumps({"result":"pass"},sort_keys=True)+"\n").encode())
        terminal=self.command(self.repo,str(self.repo/"arcanum/arcana/task-session/scripts/terminalize_pre_execution_failure.py"),"--repo-root",str(self.repo),"--request","scenario/request.json")
        self.assertEqual(terminal.returncode,0,terminal.stdout+terminal.stderr)
        receipt=json.loads((self.repo/"results/task-session-terminal.json").read_text())
        self.assertEqual(receipt["control_refs"],[partition["outputs"][0]["expected_postimage_ref"]])
        self.assertFalse((self.repo/"live/selection.json").exists())

    def test_wrong_attempt_blocks_before_first_write(self)->None:
        request=json.loads(self.request.read_text()); request["control_evidence_partition"]["attempt_id"]="wrong-attempt"; write_json(self.request,request)
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        completed=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","shadow","--shadow-root",str(self.repo))
        self.assertEqual(completed.returncode,2); self.assertFalse((self.repo/"live/readiness.json").exists()); self.assertFalse((self.repo/"runs/run-1").exists())

    def test_apply_materializes_exact_controls_once_and_replay_blocks(self)->None:
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        applied=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply")
        self.assertEqual(applied.returncode,0,applied.stdout+applied.stderr)
        receipt=json.loads(applied.stdout)
        self.assertEqual(receipt["mode"],"apply")
        self.assertEqual(receipt["authority_effect"],"accepted-control-preparation-only")
        self.assertEqual(len(receipt["observed_writes"]),7)
        first_states={path:(self.repo/path).read_bytes() for path in receipt["observed_writes"]}
        replay=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply")
        self.assertEqual(replay.returncode,2,replay.stdout+replay.stderr)
        self.assertEqual(json.loads(replay.stdout)["writes_performed"],0)
        self.assertEqual(first_states,{path:(self.repo/path).read_bytes() for path in receipt["observed_writes"]})

    def test_authorization_token_missing_first_letter_blocks_before_write(self)->None:
        response_path=self.repo/"scenario/owner-response.json"
        response=json.loads(response_path.read_text())
        self.assertTrue(response["authorization_token"].startswith("ACCEPT-"))
        response["authorization_token"]=response["authorization_token"][1:]
        response.pop("response_digest")
        response["response_digest"]=hashlib.sha256(json.dumps(response,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        write_json(response_path,response)
        response_ref=exact_ref(self.repo,response_path)
        preparation=json.loads(self.preparation.read_text())
        preparation["owner_acceptance_response_ref"]=response_ref
        for index,reference in enumerate(preparation["owner_acceptance_validation"]["input_refs"]):
            if reference["path"]=="scenario/owner-response.json": preparation["owner_acceptance_validation"]["input_refs"][index]=response_ref
        write_json(self.preparation,preparation)
        request=json.loads(self.request.read_text())
        request["failure_terminalization"]["owner_acceptance_response_ref"]=response_ref
        request["live_execution_entry_preparation_ref"]=exact_ref(self.repo,self.preparation)
        write_json(self.request,request)
        validator=self.repo/"arcanum/spells/invoke/scripts/validate_owner_acceptance_response.py"
        direct=self.command(self.repo,str(validator),"--repo-root",str(self.repo),"--response","scenario/owner-response.json")
        self.assertEqual(direct.returncode,2,direct.stdout+direct.stderr)
        self.assertIn("exact canonical token",direct.stdout)
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        completed=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply")
        self.assertEqual(completed.returncode,2,completed.stdout+completed.stderr)
        self.assertFalse((self.repo/"live/readiness.json").exists())
        self.assertFalse((self.repo/"runs/run-1").exists())

    def test_present_control_baseline_is_rejected_before_write(self)->None:
        partition_path=self.repo/"scenario/control-partition.json"
        partition=json.loads(partition_path.read_text())
        partition["outputs"][0]["baseline"]={"state":"present","sha256":"0"*64,"size_bytes":0}
        write_json(partition_path,partition)
        partition_ref=exact_ref(self.repo,partition_path)
        preparation=json.loads(self.preparation.read_text())
        preparation["control_evidence_partition_ref"]=partition_ref
        write_json(self.preparation,preparation)
        request=json.loads(self.request.read_text())
        request["control_evidence_partition"]=partition
        request["fast_execution_entry"]["route_scope_partition"]["control_evidence_partition"]=partition
        request["failure_terminalization"]["control_evidence_partition_ref"]=partition_ref
        request["live_execution_entry_preparation_ref"]=exact_ref(self.repo,self.preparation)
        write_json(self.request,request)
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        completed=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply")
        self.assertEqual(completed.returncode,2,completed.stdout+completed.stderr)
        self.assertIn("live control partition schema invalid",completed.stdout)
        self.assertFalse((self.repo/"live/readiness.json").exists())
        self.assertFalse((self.repo/"runs/run-1").exists())

    def test_input_closure_omission_extra_and_stale_ref_block_before_write(self)->None:
        mutations={
            "omitted-schema": lambda closure: closure["input_refs"].pop(
                next(index for index,item in enumerate(closure["input_refs"]) if item["path"].endswith("mutation-admission-receipt.schema.json"))
            ),
            "undeclared-extra": lambda closure: closure["input_refs"].append(exact_ref(self.repo,self.repo/"scenario/blocker.json")),
            "stale-ref": lambda closure: closure["input_refs"][0].update({"sha256":"0"*64}),
        }
        for case_id,mutate in mutations.items():
            with self.subTest(case_id=case_id):
                case=Path(self.temp.name)/f"closure-{case_id}"; shutil.copytree(self.repo,case)
                preparation_path=case/"scenario/live-preparation.json"
                preparation=json.loads(preparation_path.read_text())
                invocation_document=preparation["governance_runner"]
                closure_path=case/invocation_document["input_closure_ref"]["path"]
                closure=json.loads(closure_path.read_text())
                if case_id=="undeclared-extra":
                    mutate(closure)
                    closure["input_refs"][-1]=exact_ref(case,case/"scenario/blocker.json")
                else: mutate(closure)
                closure["input_refs"]=sorted(closure["input_refs"],key=lambda item:item["path"])
                closure.pop("closure_digest")
                closure["closure_digest"]=hashlib.sha256(json.dumps(closure,sort_keys=True,separators=(",",":")).encode()).hexdigest()
                write_json(closure_path,closure)
                invocation_document["input_closure_ref"]=exact_ref(case,closure_path)
                invocation_document["input_refs"]=closure["input_refs"]
                write_json(preparation_path,preparation)
                request_path=case/"scenario/request.json"; request=json.loads(request_path.read_text())
                request["live_execution_entry_preparation_ref"]=exact_ref(case,preparation_path); write_json(request_path,request)
                coordinator=case/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
                completed=self.command(case,str(coordinator),"--repo-root",str(case),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply")
                self.assertEqual(completed.returncode,2,completed.stdout+completed.stderr)
                self.assertFalse((case/"live/readiness.json").exists())
                self.assertFalse((case/"runs/run-1").exists())

    def test_live_topology_negative_matrix_blocks_before_first_write(self)->None:
        case_ids=(
            "missing-control-output", "extra-control-union", "wrong-owner", "wrong-class",
            "wrong-postimage-path", "wrong-output-attempt", "output-outside-partition",
            "baseline-drift", "symlink-ancestry", "live-root-substitution",
            "material-relabel", "lifecycle-relabel", "stale-executable", "stale-runner",
        )
        for case_id in case_ids:
            with self.subTest(case_id=case_id):
                case=Path(self.temp.name)/f"topology-{case_id}"; shutil.copytree(self.repo,case)
                partition_path=case/"scenario/control-partition.json"
                preparation_path=case/"scenario/live-preparation.json"
                request_path=case/"scenario/request.json"
                partition=json.loads(partition_path.read_text()); preparation=json.loads(preparation_path.read_text()); request=json.loads(request_path.read_text())
                output=partition["outputs"][0]
                if case_id=="missing-control-output": partition["outputs"].pop()
                elif case_id=="extra-control-union": partition["exact_union_scope"].append("live/undeclared.json")
                elif case_id=="wrong-owner": output["owner_capability"]="task-session"
                elif case_id=="wrong-class": output["write_class"]="context-evidence"
                elif case_id=="wrong-postimage-path": output["expected_postimage_ref"]["path"]="live/other.json"
                elif case_id=="wrong-output-attempt": output["attempt_id"]="wrong-attempt"
                elif case_id=="output-outside-partition": preparation["preparation_steps"][0]["output_paths"]=["live/outside.json"]
                elif case_id=="baseline-drift": write_json(case/"live/readiness.json",{"unexpected":"present"})
                elif case_id=="symlink-ancestry":
                    outside=Path(self.temp.name)/"outside-live"; outside.mkdir(exist_ok=True); (case/"live").symlink_to(outside,target_is_directory=True)
                elif case_id=="live-root-substitution": pass
                elif case_id in {"material-relabel","lifecycle-relabel"}:
                    replacement=(request["execution_contract"]["allowed_writes"][0] if case_id=="material-relabel" else request["fast_execution_entry"]["route_scope_partition"]["terminal_receipt_scope"])
                    old=output["path"]; output["path"]=replacement; output["expected_postimage_ref"]["path"]=replacement
                    partition["exact_union_scope"]=[replacement if path==old else path for path in partition["exact_union_scope"]]
                    preparation["preparation_steps"][0]["output_paths"]=[replacement]
                elif case_id=="stale-executable": preparation["owner_acceptance_validation"]["executable_identity"]["sha256"]="0"*64
                elif case_id=="stale-runner": preparation["governance_runner"]["runner_ref"]["sha256"]="0"*64
                if case_id not in {"output-outside-partition","stale-executable","stale-runner","live-root-substitution"}:
                    write_json(partition_path,partition)
                    partition_ref=exact_ref(case,partition_path)
                    preparation["control_evidence_partition_ref"]=partition_ref
                    request["control_evidence_partition"]=partition
                    request["fast_execution_entry"]["route_scope_partition"]["control_evidence_partition"]=partition
                    request["failure_terminalization"]["control_evidence_partition_ref"]=partition_ref
                    request["fast_execution_entry"]["route_scope_partition"]["exact_union_scope"]=sorted({
                        *request["execution_contract"]["allowed_writes"],
                        request["fast_execution_entry"]["route_scope_partition"]["terminal_receipt_scope"],
                        *[item["path"] for item in request["fast_execution_entry"]["route_scope_partition"]["lifecycle_owner_scopes"]],
                        *partition["exact_union_scope"],
                    })
                write_json(preparation_path,preparation)
                request["live_execution_entry_preparation_ref"]=exact_ref(case,preparation_path); write_json(request_path,request)
                coordinator=case/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
                args=[str(coordinator),"--repo-root",str(case),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","apply"]
                if case_id=="live-root-substitution":
                    args[-1]="shadow"; args.extend(["--shadow-root",str(case/"other-root")])
                completed=self.command(case,*args)
                self.assertEqual(completed.returncode,2,completed.stdout+completed.stderr)
                if case_id!="baseline-drift": self.assertFalse((case/"live/readiness.json").exists())
                self.assertFalse((case/"runs/run-1").exists())

    def test_failure_receipt_cannot_claim_unavailable_phase(self)->None:
        coordinator=self.repo/"arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py"
        stopped=self.command(self.repo,str(coordinator),"--repo-root",str(self.repo),"--request","scenario/request.json","--preparation","scenario/live-preparation.json","--mode","shadow","--shadow-root",str(self.repo),"--stop-after","readiness")
        self.assertEqual(stopped.returncode,0,stopped.stdout+stopped.stderr)
        terminalizer=self.repo/"arcanum/arcana/task-session/scripts/terminalize_pre_execution_failure.py"
        terminal=self.command(self.repo,str(terminalizer),"--repo-root",str(self.repo),"--request","scenario/request.json")
        self.assertEqual(terminal.returncode,0,terminal.stdout+terminal.stderr)
        terminal_path=self.repo/"results/task-session-terminal.json"; receipt=json.loads(terminal_path.read_text())
        receipt["phase_availability"]["admission"]=True; receipt.pop("receipt_digest")
        receipt["receipt_digest"]=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(",",":")).encode()).hexdigest(); write_json(terminal_path,receipt)
        owner=self.repo/"arcanum/spells/invoke/scripts/handle_pre_execution_block.py"
        blocked=self.command(self.repo,str(owner),"--repo-root",str(self.repo),"--request","scenario/request.json","--terminal-receipt","results/task-session-terminal.json")
        self.assertEqual(blocked.returncode,2,blocked.stdout+blocked.stderr)
        self.assertFalse((self.repo/"results/invoke-block-owner.json").exists())


if __name__=="__main__": unittest.main()
