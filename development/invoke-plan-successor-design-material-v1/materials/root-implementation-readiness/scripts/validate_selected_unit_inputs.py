#!/usr/bin/env python3
"""Validate selected-unit live inputs without requiring future outputs."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path, PurePosixPath
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/selected-unit-admission-v1.schema.json"
class AdmissionBlock(ValueError): pass

def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def resolve(repo: Path, raw: str) -> Path:
    pure=PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or "\\" in raw: raise AdmissionBlock(f"unsafe path: {raw}")
    target=repo.joinpath(*pure.parts)
    probe=target
    while not probe.exists() and probe!=repo: probe=probe.parent
    try: probe.resolve(strict=True).relative_to(repo.resolve(strict=True))
    except (ValueError,FileNotFoundError): raise AdmissionBlock(f"path escapes repository: {raw}") from None
    return target

def validate(contract: dict, repo: Path) -> dict:
    schema=json.loads(SCHEMA.read_text()); Draft202012Validator.check_schema(schema)
    errors=sorted(Draft202012Validator(schema).iter_errors(contract),key=lambda e:list(e.path))
    if errors: raise AdmissionBlock(f"schema: {errors[0].message}")
    runner=resolve(repo,contract["runner"]["path"])
    if not runner.is_file() or digest(runner)!=contract["runner"]["sha256"]: raise AdmissionBlock("runner identity mismatch")
    seen=set()
    for target in contract["targets"]:
        raw=target["path"]
        if raw in seen: raise AdmissionBlock(f"duplicate target: {raw}")
        seen.add(raw); path=resolve(repo,raw); disposition=target["disposition"]; baseline=target["baseline_sha256"]
        if disposition=="create":
            if baseline is not None: raise AdmissionBlock(f"create target has baseline: {raw}")
            if path.exists() and target["collision_policy"]=="fail-if-exists": raise AdmissionBlock(f"create collision: {raw}")
            if not path.parent.exists(): raise AdmissionBlock(f"create parent missing: {raw}")
        elif disposition=="transient":
            if baseline is not None or not path.parent.exists(): raise AdmissionBlock(f"transient target invalid: {raw}")
        else:
            if not path.is_file() or baseline is None or digest(path)!=baseline: raise AdmissionBlock(f"live baseline mismatch: {raw}")
    create_paths={item["path"] for item in contract["targets"] if item["disposition"]=="create"}
    for command in contract["validation_commands"]:
        cwd=resolve(repo,command["cwd"])
        if not cwd.is_dir(): raise AdmissionBlock(f"command cwd missing: {command['cwd']}")
        if command["phase"]=="pre-execution":
            for token in command["argv"][1:]:
                if token in create_paths: raise AdmissionBlock(f"pre-execution command consumes future output: {token}")
    return {"schema_version":"implementation-readiness.selected-unit-admission-receipt.v1","unit_id":contract["unit_id"],"result":"pass","create_targets":sorted(create_paths),"post_produce_commands":sum(c["phase"]=="post-produce" for c in contract["validation_commands"]),"outputs_validated":False,"authority_effect":"none"}

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--contract",type=Path,required=True);p.add_argument("--repo-root",type=Path,default=Path.cwd());a=p.parse_args()
    try: print(json.dumps(validate(json.loads(a.contract.read_text()),a.repo_root),sort_keys=True));return 0
    except (AdmissionBlock,OSError,json.JSONDecodeError) as exc: print(f"BLOCK: {exc}");return 2
if __name__=="__main__":raise SystemExit(main())
