#!/usr/bin/env python3
"""Emit deterministic selector-only continuity after a pre-execution block."""

from __future__ import annotations

import argparse, hashlib, json, os
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker


ROOT=Path(__file__).resolve().parent.parent
def load(path:Path)->dict[str,Any]:
    value=json.loads(path.read_text(encoding="utf-8"));
    if not isinstance(value,dict): raise ValueError(f"JSON object required: {path}")
    return value
def resolve(root:Path,raw:str)->Path:
    path=(root/raw).resolve(); path.relative_to(root.resolve()); return path
def exact_ref(root:Path,path:Path)->dict[str,Any]:
    data=path.read_bytes(); return {"path":path.resolve().relative_to(root.resolve()).as_posix(),"sha256":hashlib.sha256(data).hexdigest(),"size_bytes":len(data)}
def canonical_digest(value:Any)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def validate_receipt_digest(value:dict[str,Any],label:str)->None:
    projection=dict(value); declared=projection.pop("receipt_digest",None)
    if declared!=canonical_digest(projection): raise ValueError(f"{label} receipt digest is not canonical")
def atomic_create(path:Path,data:bytes)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError:
        if path.read_bytes()!=data: raise ValueError(f"continuity cursor conflicts: {path}")
        return
    with os.fdopen(fd,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
def emit(root:Path,request_path:Path,terminal_path:Path,owner_path:Path)->dict[str,Any]:
    request=load(request_path); profile=request["failure_terminalization"]; terminal=load(terminal_path); owner=load(owner_path)
    terminal_schema=resolve(root,profile["failure_terminal_schema_ref"]["path"]); owner_schema=resolve(root,profile["invoke_owner_schema_ref"]["path"]); continuity_schema=resolve(root,profile["continuity_schema_ref"]["path"])
    for schema_path,reference in ((terminal_schema,profile["failure_terminal_schema_ref"]),(owner_schema,profile["invoke_owner_schema_ref"]),(continuity_schema,profile["continuity_schema_ref"])):
        if exact_ref(root,schema_path)!=reference: raise ValueError("failure continuity schema identity drift")
    terminal_errors=list(Draft202012Validator(load(terminal_schema)).iter_errors(terminal)); owner_errors=list(Draft202012Validator(load(owner_schema)).iter_errors(owner))
    if terminal_errors or owner_errors: raise ValueError("failure continuity input receipt schema invalid")
    validate_receipt_digest(terminal,"Task Session failure"); validate_receipt_digest(owner,"Invoke block owner")
    if terminal["blocker_fingerprint"]!=profile["blocker_fingerprint"] or owner["blocker_fingerprint"]!=profile["blocker_fingerprint"]: raise ValueError("continuity blocker fingerprint mismatch")
    if owner["task_session_failure_receipt_ref"]!=exact_ref(root,terminal_path): raise ValueError("continuity owner receipt is not bound to terminal receipt")
    cursor={"schema_version":"task-session.continuity.v1","session_id":profile["attempt_id"],"updated_at":profile["continuity_updated_at"],"scope_root":".","work_pack":request["work_pack_ref"]["path"],"source_swu":profile["swu_id"],"source_result":"BLOCK","source_receipt":profile["terminal_receipt_path"],"closeout_owner_receipt":profile["invoke_owner_receipt_path"],"next_swu":None,"next_route":None,"blocker_fingerprint":profile["blocker_fingerprint"],"source_receipt_profile":"pre-execution-failure-terminalization-v1","owner_closeout_state":"unavailable-pre-execution","attempt_id":profile["attempt_id"],"authority_effect":"none"}
    errors=sorted(Draft202012Validator(load(continuity_schema),format_checker=FormatChecker()).iter_errors(cursor),key=lambda item:list(item.absolute_path))
    if errors: raise ValueError(f"failure continuity schema invalid: {errors[0].message}")
    output=resolve(root,profile["continuity_cursor_path"]); atomic_create(output,(json.dumps(cursor,indent=2,sort_keys=True)+"\n").encode())
    return {"result":"block","continuity_ref":exact_ref(root,output),"writes_performed":1}
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo-root",required=True); parser.add_argument("--request",required=True); parser.add_argument("--terminal-receipt",required=True); parser.add_argument("--owner-receipt",required=True); args=parser.parse_args()
    try:
        root=Path(args.repo_root).resolve(); result=emit(root,resolve(root,args.request),resolve(root,args.terminal_receipt),resolve(root,args.owner_receipt))
    except (KeyError,OSError,UnicodeError,ValueError) as error:
        print(json.dumps({"result":"block","diagnostics":[str(error)],"writes_performed":0},sort_keys=True)); return 2
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
