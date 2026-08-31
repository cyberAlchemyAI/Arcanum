#!/usr/bin/env python3
"""Validate exact, acyclic, one-producer-per-unit Accepted Stream closure."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from accepted_stream_contract import ContractError, canonical_bytes, normalize_repo_path

REQUIRED_FIELDS={"unit_id","ordinal","producer_id","producer_path","schema_ref","validator_argv","source_selectors","output_paths","failure_paths","depends_on"}

def validate_matrix(matrix: dict, repo_root: Path) -> None:
    if matrix.get("schema_version")!="invoke.accepted-stream-producer-matrix.v1": raise ContractError("wrong matrix schema")
    units=matrix.get("units")
    if not isinstance(units,list) or not units: raise ContractError("matrix must contain at least one unit")
    ids=[]; producers=[]; outputs=[]
    prior_ordinal=-1
    for unit in units:
        if set(unit)!=REQUIRED_FIELDS: raise ContractError("producer row fields are not exact")
        ordinal=unit["ordinal"]
        if not isinstance(ordinal,int) or isinstance(ordinal,bool) or ordinal<=prior_ordinal: raise ContractError("matrix ordinal order mismatch")
        if not isinstance(unit["unit_id"],str) or not unit["unit_id"].startswith("SWU-") or len(unit["unit_id"])<=4: raise ContractError("matrix unit identity is invalid")
        ids.append(unit["unit_id"]); producers.append(unit["producer_id"])
        normalize_repo_path(repo_root,unit["producer_path"],allow_missing=False)
        normalize_repo_path(repo_root,unit["schema_ref"],allow_missing=False)
        if not unit["validator_argv"] or not all(isinstance(x,str) and x for x in unit["validator_argv"]): raise ContractError("validator argv is empty")
        for field in ("source_selectors","output_paths","failure_paths"):
            if not unit[field]: raise ContractError(f"{field} is empty")
            for path in unit[field]: normalize_repo_path(repo_root,path)
        outputs.extend(unit["output_paths"]+unit["failure_paths"])
        if any(dep in ids and dep not in ids[:-1] for dep in unit["depends_on"]): raise ContractError("forward or cyclic dependency")
        prior_ordinal=ordinal
    if len(set(ids))!=len(ids) or len(set(producers))!=len(producers): raise ContractError("duplicate unit or producer")
    if len(set(outputs))!=len(outputs): raise ContractError("duplicate output ownership")
    expected=matrix.get("matrix_digest"); unsigned={k:v for k,v in matrix.items() if k!="matrix_digest"}
    import hashlib
    actual=hashlib.sha256(canonical_bytes(unsigned)).hexdigest()
    if expected!=actual: raise ContractError("matrix digest mismatch")

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("matrix",type=Path); a=p.parse_args()
    try:
        matrix=json.loads(a.matrix.read_text()); validate_matrix(matrix,Path.cwd()); print(f"PASS producer-closure units={len(matrix['units'])}")
    except (ContractError,KeyError,json.JSONDecodeError) as exc: print(f"BLOCK: {exc}"); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
