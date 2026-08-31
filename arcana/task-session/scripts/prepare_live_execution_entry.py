#!/usr/bin/env python3
"""Own the first repository-local write of an accepted Task Session attempt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

from control_evidence_partition import load_object, validate_partition
from invocation_input_closure import validate as validate_input_closure


ROOT = Path(__file__).resolve().parent.parent


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.resolve().relative_to(root.resolve()).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def resolve(root: Path, raw: str) -> Path:
    relative = PurePosixPath(raw)
    if relative.is_absolute() or ".." in relative.parts or "\\" in raw:
        raise ValueError(f"unsafe repository locator: {raw}")
    path = (root / relative).resolve()
    path.relative_to(root.resolve())
    return path


def read_exact(root: Path, reference: dict[str, Any]) -> dict[str, Any]:
    path = resolve(root, reference["path"])
    if not path.is_file() or exact_ref(root, path) != reference:
        raise ValueError(f"stale exact reference: {reference['path']}")
    return load_object(path)


def validate_schema(value: dict[str, Any], schema: Path, label: str) -> None:
    errors = sorted(Draft202012Validator(load_object(schema)).iter_errors(value), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        raise ValueError(f"{label} schema invalid at {'/'.join(map(str, first.absolute_path)) or '<root>'}: {first.message}")


def state(path: Path) -> dict[str, Any]:
    if not path.exists(): return {"state": "absent", "sha256": None, "size_bytes": None}
    if not path.is_file(): raise ValueError(f"non-file output state: {path}")
    data=path.read_bytes(); return {"state": "present", "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def snapshot(root: Path) -> dict[str, dict[str, Any]]:
    return {path.relative_to(root).as_posix(): state(path) for path in sorted(root.rglob("*")) if path.is_file() and "__pycache__" not in path.parts}


def substitute(argv: list[str], values: dict[str, str]) -> list[str]:
    rendered=[]
    for item in argv:
        for key,value in values.items(): item=item.replace("{"+key+"}",value)
        if "{" in item or "}" in item: raise ValueError(f"unresolved invocation placeholder: {item}")
        rendered.append(item)
    return rendered


def exact_executable(identity: dict[str, Any]) -> Path:
    path=Path(identity["path"])
    if not path.is_absolute() or not path.is_file(): raise ValueError("invocation executable identity is not an absolute file")
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=identity["sha256"] or len(data)!=identity["size_bytes"]: raise ValueError("invocation executable identity drift")
    return path


def validate_invocation_declaration(root: Path, invocation: dict[str, Any], label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    exact_executable(invocation["executable_identity"])
    closure=read_exact(root,invocation["input_closure_ref"])
    status=validate_input_closure(root,closure)
    if closure["input_refs"]!=invocation["input_refs"]: raise ValueError(f"{label} inline inputs differ from the exact input closure")
    by_path={item["path"]:item for item in closure["input_refs"]}
    if len(by_path)!=len(closure["input_refs"]): raise ValueError(f"{label} input closure paths are not unique")
    if by_path.get(invocation["runner_ref"]["path"])!=invocation["runner_ref"]: raise ValueError(f"{label} input closure omits its exact runner")
    return closure,status


def atomic_materialize(root: Path, raw: str, data: bytes, baseline: dict[str, Any]) -> dict[str, Any]:
    path=resolve(root,raw)
    if state(path)!=baseline: raise ValueError(f"live control baseline drift at materialization: {raw}")
    if baseline["state"]!="absent": raise ValueError(f"live control materialization requires an absent baseline: {raw}")
    path.parent.mkdir(parents=True,exist_ok=True)
    try: descriptor=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError as error: raise ValueError(f"concurrent live control write detected: {raw}") from error
    with os.fdopen(descriptor,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
    return exact_ref(root,path)


def run_isolated_invocation(root: Path, invocation: dict[str, Any], values: dict[str, str], outputs: set[str], label: str, dynamic_inputs: list[dict[str, Any]] | None = None) -> tuple[dict[str, Any], dict[str, bytes]]:
    executable=exact_executable(invocation["executable_identity"])
    closure,closure_status=validate_invocation_declaration(root,invocation,label)
    references=[*closure["input_refs"],*(dynamic_inputs or [])]
    by_path={item["path"]:item for item in references}
    if len(by_path)!=len(references): raise ValueError(f"{label} input closure contains duplicate or conflicting runtime inputs")
    if invocation["runner_ref"]["path"] not in by_path or by_path[invocation["runner_ref"]["path"]]!=invocation["runner_ref"]: raise ValueError(f"{label} input closure omits its exact runner")
    with tempfile.TemporaryDirectory(prefix="task-session-live-entry-") as directory:
        isolated=Path(directory)
        for reference in by_path.values():
            source=resolve(root,reference["path"])
            if exact_ref(root,source)!=reference: raise ValueError(f"{label} input drift: {reference['path']}")
            target=isolated/reference["path"]; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target)
        runner=isolated/invocation["runner_ref"]["path"]
        isolated_values={**values,"repo_root":str(isolated),"runner":str(runner),"executable":str(executable)}
        argv=substitute(invocation["argv"],isolated_values)
        if len(argv)<2 or argv[0]!=str(executable) or argv[1]!=str(runner): raise ValueError(f"{label} argv does not place exact executable and runner first")
        before=snapshot(isolated)
        environment=dict(invocation["environment"])
        completed=subprocess.run(argv,cwd=resolve(isolated,invocation.get("cwd",".")),check=False,capture_output=True,timeout=invocation["timeout_seconds"],env=environment)
        if len(completed.stdout)>invocation["max_output_bytes"] or len(completed.stderr)>invocation["max_output_bytes"]: raise ValueError(f"{label} output exceeded its bound")
        if completed.returncode!=0: raise ValueError(f"{label} failed with exit {completed.returncode}: {hashlib.sha256(completed.stderr).hexdigest()}")
        after=snapshot(isolated); changed={path for path in set(before)|set(after) if before.get(path)!=after.get(path)}
        if changed!=outputs: raise ValueError(f"{label} isolated transaction wrote outside exact outputs")
        postimages={path:(isolated/path).read_bytes() for path in outputs}
        receipt={"runner_ref":invocation["runner_ref"],"input_closure_ref":invocation["input_closure_ref"],"input_closure_digest":closure_status["closure_digest"],"input_count":closure_status["input_count"]+len(dynamic_inputs or []),"executable_identity":invocation["executable_identity"],"argv":argv,"environment_names":sorted(environment),"timeout_seconds":invocation["timeout_seconds"],"max_output_bytes":invocation["max_output_bytes"],"network_allowed":False,"external_effects_allowed":False,"stdout_sha256":hashlib.sha256(completed.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(completed.stderr).hexdigest(),"exit_code":completed.returncode}
        return receipt,postimages


def prepare(root: Path, request_path: Path, preparation_path: Path, mode: str, shadow_root: Path | None, stop_after: str | None = None) -> dict[str, Any]:
    if mode=="shadow":
        if shadow_root is None or shadow_root.resolve()!=root.resolve(): raise ValueError("shadow mode requires --shadow-root equal to the isolated repository root")
    elif shadow_root is not None: raise ValueError("apply mode forbids --shadow-root")
    if stop_after is not None and mode != "shadow": raise ValueError("a deliberate preparation stop is shadow-only")
    request=load_object(request_path); validate_schema(request,ROOT/"schemas/governance-run-request.schema.json","governance request")
    preparation=load_object(preparation_path); validate_schema(preparation,ROOT/"schemas/live-execution-entry-preparation-v1.schema.json","live preparation")
    if request.get("live_execution_entry_preparation_ref")!=exact_ref(root,preparation_path): raise ValueError("governance request does not bind the exact live preparation manifest")
    if preparation["attempt_id"]!=request["run_id"]: raise ValueError("live preparation attempt differs from governance request")
    profile=request.get("failure_terminalization",{}); owner_ref=preparation.get("owner_acceptance_request_ref"); response_ref=preparation.get("owner_acceptance_response_ref")
    if not isinstance(owner_ref,dict) or not isinstance(response_ref,dict): raise ValueError("accepted owner request/response references are missing")
    if profile.get("owner_acceptance_request_ref")!=owner_ref or profile.get("owner_acceptance_response_ref")!=response_ref:
        raise ValueError("live preparation and failure terminalization bind different owner decision artifacts")
    owner_request=read_exact(root,owner_ref); response=read_exact(root,response_ref)
    if response.get("attempt_id")!=request["run_id"] or response.get("request_ref")!=owner_ref: raise ValueError("owner acceptance response does not bind this exact attempt/request")
    if response.get("request_id")!=owner_request.get("request_id") or response.get("request_digest")!=owner_request.get("request_digest"):
        raise ValueError("owner acceptance response identity differs from the canonical request")
    if response.get("authority_write_ceiling_digest")!=preparation["authority_write_ceiling_digest"]:
        raise ValueError("live preparation authority-write ceiling differs from accepted response")
    partition=read_exact(root,preparation["control_evidence_partition_ref"])
    if request.get("control_evidence_partition")!=partition: raise ValueError("live preparation partition differs from governance request")
    route=request.get("fast_execution_entry",{}).get("route_scope_partition",{})
    forbidden=[*request["execution_contract"]["allowed_writes"],*[item["path"] for item in request["execution_contract"].get("transient_outputs",[])],route.get("terminal_receipt_scope",request["closeout_contract"]["terminal_receipt_path"]),*[item["path"] for item in route.get("lifecycle_owner_scopes",[])]]
    validate_partition(partition,repository_root=root,attempt_id=request["run_id"],forbidden_scopes=forbidden,run_dir=preparation["run_dir"],revalidate_runtime=False)
    validate_invocation_declaration(root,preparation["owner_acceptance_validation"],"owner acceptance validation")
    for step in preparation["preparation_steps"]:
        validate_invocation_declaration(root,step["invocation"],f"preparation {step['step_id']}")
    runner_declaration={**preparation["governance_runner"],"cwd":"."}; runner_declaration.pop("output_paths")
    validate_invocation_declaration(root,runner_declaration,"governance runner")
    for item in partition["outputs"]:
        if state(resolve(root,item["path"]))!=item["baseline"]: raise ValueError(f"live preparation baseline drift before first write: {item['path']}")
    control_by_path={item["path"]:item for item in partition["outputs"]}
    values={"python":sys.executable,"repo_root":str(root),"request":request_path.resolve().relative_to(root).as_posix(),"owner_request":owner_ref["path"],"owner_response":response_ref["path"],"run_dir":preparation["run_dir"]}
    owner_validation,_=run_isolated_invocation(root,preparation["owner_acceptance_validation"],values,set(),"owner acceptance validation")
    all_declared_step_outputs:set[str]=set(); step_receipts=[]
    class_by_step={"readiness":{"readiness-evidence"},"selection":{"selection-evidence"},"fast-entry":{"fast-entry-evidence"},"context":{"context-evidence"},"admission":{"admission-evidence"}}
    for step in preparation["preparation_steps"]:
        outputs=set(step["output_paths"])
        if outputs & all_declared_step_outputs: raise ValueError("live preparation steps duplicate an output")
        all_declared_step_outputs|=outputs
        for path in outputs:
            item=control_by_path.get(path)
            if item is None or item["owner_capability"]!=step["owner_capability"] or item["write_class"] not in class_by_step[step["step_id"]]: raise ValueError(f"live preparation owner/class mismatch: {path}")
        invocation,postimages=run_isolated_invocation(root,step["invocation"],values,outputs,f"preparation {step['step_id']}")
        for path in outputs:
            expected=control_by_path[path].get("expected_postimage_ref")
            data=postimages[path]
            observed={"path":path,"sha256":hashlib.sha256(data).hexdigest(),"size_bytes":len(data)}
            if expected is None or observed!=expected: raise ValueError(f"preparation postimage mismatch: {path}")
        materialized=[atomic_materialize(root,path,postimages[path],control_by_path[path]["baseline"]) for path in sorted(outputs)]
        step_receipts.append({"step_id":step["step_id"],"owner_capability":step["owner_capability"],"output_paths":sorted(outputs),"invocation":invocation})
        if stop_after == step["step_id"]:
            return {"schema_version":"task-session.live-execution-entry-preparation-receipt.v1","result":"deliberate-pre-execution-stop","mode":"shadow","attempt_id":request["run_id"],"stop_after":stop_after,"owner_acceptance_validation":owner_validation,"steps":step_receipts,"observed_writes":sorted(all_declared_step_outputs),"partition_ref":preparation["control_evidence_partition_ref"],"authority_effect":"none"}
    preparation_receipt_path=preparation["preparation_receipt_path"]
    receipt_control=control_by_path.get(preparation_receipt_path)
    if receipt_control is None or receipt_control["owner_capability"]!="task-session" or receipt_control["write_class"]!="preparation-receipt": raise ValueError("live preparation receipt lacks its exact control scope")
    step_output_refs=[exact_ref(root,resolve(root,path)) for path in sorted(all_declared_step_outputs)]
    preparation_receipt={"schema_version":"task-session.live-execution-entry-preparation-receipt.v1","result":"pass","attempt_id":request["run_id"],"request_ref":exact_ref(root,request_path),"owner_acceptance_request_ref":owner_ref,"owner_acceptance_response_ref":response_ref,"authority_write_ceiling_digest":preparation["authority_write_ceiling_digest"],"partition_ref":preparation["control_evidence_partition_ref"],"step_outputs":step_output_refs,"effect":"accepted-control-preparation-only"}
    preparation_receipt["receipt_digest"]=hashlib.sha256(json.dumps(preparation_receipt,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    validate_schema(preparation_receipt,ROOT/"schemas/live-execution-entry-preparation-receipt-v1.schema.json","live preparation receipt")
    preparation_ref=atomic_materialize(root,preparation_receipt_path,(json.dumps(preparation_receipt,indent=2,sort_keys=True)+"\n").encode(),receipt_control["baseline"])
    runner=preparation["governance_runner"]; runner_outputs=set(runner["output_paths"])
    for path in runner_outputs:
        item=control_by_path.get(path)
        if item is None or item["owner_capability"]!="task-session" or item["write_class"] not in {"governance-checkpoint","execution-ticket"}: raise ValueError(f"governance runner output is not typed control evidence: {path}")
    runner_invocation={**runner,"cwd":"."}; runner_invocation.pop("output_paths")
    runner_receipt,runner_postimages=run_isolated_invocation(
        root,
        runner_invocation,
        values,
        runner_outputs,
        "governance runner",
        dynamic_inputs=[preparation_ref, exact_ref(root, request_path), *step_output_refs],
    )
    for path in sorted(runner_outputs): atomic_materialize(root,path,runner_postimages[path],control_by_path[path]["baseline"])
    total_changed=all_declared_step_outputs|runner_outputs|{preparation_receipt_path}
    if not total_changed<=set(partition["exact_union_scope"]): raise ValueError("live coordinator write topology escaped its exact partition")
    return {"schema_version":"task-session.live-execution-entry-preparation-receipt.v1","result":"pass","mode":mode,"attempt_id":request["run_id"],"owner_acceptance_validation":owner_validation,"preparation_receipt_ref":preparation_ref,"steps":step_receipts,"governance_runner":runner_receipt,"observed_writes":sorted(total_changed),"partition_ref":preparation["control_evidence_partition_ref"],"authority_effect":"none" if mode=="shadow" else "accepted-control-preparation-only"}


def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo-root",required=True); parser.add_argument("--request",required=True); parser.add_argument("--preparation",required=True); parser.add_argument("--mode",choices=["apply","shadow"],required=True); parser.add_argument("--shadow-root"); parser.add_argument("--stop-after",choices=["readiness","selection","fast-entry","context","admission"]); args=parser.parse_args()
    try:
        root=Path(args.repo_root).resolve(); result=prepare(root,resolve(root,args.request),resolve(root,args.preparation),args.mode,Path(args.shadow_root).resolve() if args.shadow_root else None,args.stop_after)
    except (OSError,UnicodeError,ValueError,subprocess.TimeoutExpired) as error:
        print(json.dumps({"result":"block","diagnostics":[str(error)],"writes_performed":0},sort_keys=True)); return 2
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
