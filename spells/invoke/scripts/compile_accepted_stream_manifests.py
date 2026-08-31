#!/usr/bin/env python3
"""Compile deterministic manifests for a nonempty stable Accepted Stream frontier."""
from __future__ import annotations
import argparse, hashlib, json, tempfile
from pathlib import Path
from jsonschema import Draft202012Validator
from accepted_stream_contract import ContractError, canonical_bytes, child_id
from validate_accepted_stream_producer_closure import validate_matrix

DEFAULT_MATRIX=Path("arcanum/spells/invoke/contracts/accepted-stream-producer-matrix-v1.json")

def compile_manifests(matrix: dict, stream_id: str, repo_root: Path) -> list[dict]:
    validate_matrix(matrix,repo_root); result=[]
    schema=json.loads((repo_root/"arcanum/spells/invoke/schemas/accepted-stream-unit-manifest-v1.schema.json").read_text())
    validator=Draft202012Validator(schema)
    for row in matrix["units"]:
        closure=hashlib.sha256(canonical_bytes({"producer_path":row["producer_path"],"validator_argv":row["validator_argv"],"source_selectors":row["source_selectors"],"output_paths":row["output_paths"],"failure_paths":row["failure_paths"]})).hexdigest()
        manifest={"schema_version":"invoke.accepted-stream-unit-manifest.v1","accepted_stream_id":stream_id,"child_id":child_id(stream_id,row["ordinal"],row["unit_id"]),"ordinal":row["ordinal"],"swu_id":row["unit_id"],"producer_id":row["producer_id"],"schema_ref":row["schema_ref"],"validator_argv":row["validator_argv"],"source_selectors":row["source_selectors"],"output_paths":row["output_paths"],"failure_paths":row["failure_paths"],"invocation_closure":closure}
        errors=sorted(validator.iter_errors(manifest),key=lambda e:list(e.path))
        if errors: raise ContractError(f"compiled manifest is invalid: {errors[0].message}")
        result.append(manifest)
    return result

def write_manifests(items:list[dict],output:Path)->None:
    output.mkdir(parents=True,exist_ok=False)
    for item in items: (output/f"{item['ordinal']:02d}-{item['swu_id']}.json").write_bytes(canonical_bytes(item)+b"\n")

def self_test(repo_root:Path)->None:
    matrix=json.loads((repo_root/DEFAULT_MATRIX).read_text()); good=compile_manifests(matrix,"a"*64,repo_root)
    if len(good)!=len(matrix["units"]) or [x["ordinal"] for x in good]!=[x["ordinal"] for x in matrix["units"]]: raise AssertionError("compiler denominator mismatch")
    mutations=[lambda x:x["units"].pop(),lambda x:x["units"].reverse(),lambda x:x["units"].__setitem__(1,{**x["units"][1],"producer_id":x["units"][0]["producer_id"]}),lambda x:x["units"][1].update(depends_on=["SWU-014"]),lambda x:x["units"][1].update(output_paths=x["units"][0]["output_paths"]),lambda x:x.update(matrix_digest="f"*64)]
    for mutate in mutations:
        candidate=json.loads(json.dumps(matrix)); mutate(candidate)
        try: compile_manifests(candidate,"a"*64,repo_root)
        except ContractError: continue
        raise AssertionError("negative fixture passed")
    with tempfile.TemporaryDirectory() as td:
        write_manifests(good,Path(td)/"manifests")
        if len(list((Path(td)/"manifests").glob("*.json")))!=len(good): raise AssertionError("not all manifests written")
    print(f"PASS SWU-MVLR-003 positive=1 negative=6 manifests={len(good)}")

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--validate-swu"); p.add_argument("--matrix",type=Path,default=DEFAULT_MATRIX); p.add_argument("--stream-id"); p.add_argument("--output",type=Path); a=p.parse_args(); root=Path.cwd()
    try:
        if a.validate_swu=="SWU-MVLR-003": self_test(root)
        elif a.stream_id and a.output:
            manifests=compile_manifests(json.loads(a.matrix.read_text()),a.stream_id,root); write_manifests(manifests,a.output); print(f"PASS manifests={len(manifests)}")
        else: p.error("provide --validate-swu SWU-MVLR-003 or --stream-id and --output")
    except (ContractError,AssertionError,KeyError,json.JSONDecodeError,OSError) as exc: print(f"BLOCK: {exc}"); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
