#!/usr/bin/env python3
"""Validate that an exact owner request received one exact accepted response."""

from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

import preacceptance_closure


ROOT=Path(__file__).resolve().parent.parent
def canonical_digest(value:Any)->str: return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def load(path:Path)->dict[str,Any]:
    value=json.loads(path.read_text(encoding="utf-8"));
    if not isinstance(value,dict): raise ValueError(f"JSON object required: {path}")
    return value
def exact_ref(root:Path,path:Path)->dict[str,Any]:
    data=path.read_bytes(); return {"path":path.resolve().relative_to(root.resolve()).as_posix(),"sha256":hashlib.sha256(data).hexdigest(),"size_bytes":len(data)}
def resolve(root:Path,raw:str)->Path:
    path=(root/raw).resolve(); path.relative_to(root.resolve()); return path
def requested_effect(request:dict[str,Any])->Any:
    if "requested_effect" in request: return request["requested_effect"]
    base=request.get("base_request",{})
    if isinstance(base,dict) and "requested_effect" in base: return base["requested_effect"]
    candidate=request.get("base_request_candidate",{})
    if isinstance(candidate,dict) and "requested_effect" in candidate: return candidate["requested_effect"]
    raise ValueError("owner request lacks a requested-effect binding")
def authority_write_ceiling(request:dict[str,Any])->list[str]:
    effect=requested_effect(request)
    if not isinstance(effect,dict): raise ValueError("owner request requested effect is not an object")
    ceiling=effect.get("authority_write_ceiling")
    if not isinstance(ceiling,list) or any(not isinstance(path,str) or not path for path in ceiling):
        raise ValueError("owner request lacks a typed authority-write ceiling")
    if len(ceiling)!=len(set(ceiling)): raise ValueError("owner request authority-write ceiling contains duplicates")
    return ceiling
def validate(root:Path,response_path:Path)->dict[str,Any]:
    response=load(response_path); schema=load(ROOT/"schemas/owner-acceptance-response-v1.schema.json")
    errors=sorted(Draft202012Validator(schema).iter_errors(response),key=lambda item:list(item.absolute_path))
    if errors: raise ValueError(f"owner acceptance response schema invalid: {errors[0].message}")
    request_path=resolve(root,response["request_ref"]["path"])
    if exact_ref(root,request_path)!=response["request_ref"]: raise ValueError("owner acceptance request reference is stale")
    request=load(request_path)
    request_blockers=preacceptance_closure.validate_emitted_request(root,request_path)
    if request_blockers: raise ValueError("canonical owner acceptance request invalid: "+"; ".join(request_blockers))
    request_id=request.get("request_id") or request.get("base_request",{}).get("request_id")
    if request_id!=response["request_id"]: raise ValueError("owner acceptance request id mismatch")
    if request.get("request_digest")!=response["request_digest"]: raise ValueError("owner acceptance request digest mismatch")
    if canonical_digest(requested_effect(request))!=response["requested_effect_digest"]: raise ValueError("owner acceptance requested-effect digest mismatch")
    if canonical_digest(authority_write_ceiling(request))!=response["authority_write_ceiling_digest"]: raise ValueError("owner acceptance authority-write-ceiling digest mismatch")
    expected_token=f"ACCEPT-{response['request_id']}-{response['request_digest']}"
    if response["authorization_token"]!=expected_token: raise ValueError("owner acceptance authorization token is not the exact canonical token")
    expected=dict(response); declared=expected.pop("response_digest")
    if canonical_digest(expected)!=declared: raise ValueError("owner acceptance response digest is not canonical")
    return {"result":"pass","request_id":response["request_id"],"request_digest":response["request_digest"],"attempt_id":response["attempt_id"],"response_digest":declared,"authority_write_ceiling_digest":response["authority_write_ceiling_digest"],"authority_effect":response["authority_effect"]}
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo-root",required=True); parser.add_argument("--response",required=True); args=parser.parse_args()
    try: result=validate(Path(args.repo_root).resolve(),resolve(Path(args.repo_root).resolve(),args.response))
    except (OSError,UnicodeError,ValueError) as error: print(json.dumps({"result":"block","diagnostics":[str(error)]},sort_keys=True)); return 2
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
