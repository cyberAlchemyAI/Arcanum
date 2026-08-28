#!/usr/bin/env python3
"""Compile one validated Define machine source into an atomic public bundle."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, shutil, tempfile
from pathlib import Path
from typing import Any, Callable
from jsonschema import Draft202012Validator

IDENTITY = "invoke.compile-define-source.v1"
PROFILE = "invoke.generic-spec-baseline.v1"
KINDS = {"spec":"spec","glossary":"glossary","layering":"layering","template_selection":"template-selection","dispatch_trace":"dispatch-trace","distill":"distill","identity_denominator":"identity-denominator","transport":"transport"}

def canonical_digest(value: Any, omit: str | None = None) -> str:
    value=copy.deepcopy(value)
    if omit: value.pop(omit,None)
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def exact_ref(path: Path, label: str | None = None) -> dict[str, Any]:
    b=path.read_bytes(); out={"path":label or path.as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"size":len(b)}
    return out

def verify_ref(repo: Path, ref: dict[str, Any], label: str) -> None:
    p=(repo/ref["path"]).resolve()
    try: p.relative_to(repo.resolve())
    except ValueError: raise ValueError(f"{label} escapes repository")
    if not p.is_file(): raise ValueError(f"{label} missing")
    if exact_ref(p,ref["path"]) != ref: raise ValueError(f"{label} exact ref is stale")

def schema_errors(doc: Any, schema: dict[str, Any]) -> list[str]:
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in Draft202012Validator(schema).iter_errors(doc)]

def compile_source(source_path: Path, output_dir: Path, repo_root: Path, schema_dir: Path, late_validator: Callable[[Path], None] | None = None) -> dict[str,Any]:
    if output_dir.exists(): raise ValueError("output directory must be absent")
    source=json.loads(source_path.read_text())
    source_schema=json.loads((schema_dir/"define-source-v1.schema.json").read_text())
    result_schema=json.loads((schema_dir/"define-result-v1.schema.json").read_text())
    errors=schema_errors(source,source_schema)
    if errors: raise ValueError("source schema invalid: "+"; ".join(errors))
    if source["discovery"]["kind"]=="artifact": verify_ref(repo_root,source["discovery"]["ref"],"discovery")
    if source["template_selection"]["selected"] not in source["template_selection"]["eligible"]: raise ValueError("selected profile is not eligible")
    if any(x["link_status"]!="linked" and not x["rationale"].strip() for x in source["glossary"]): raise ValueError("partial/no-match glossary link requires rationale")
    expected_layer="IMPLEMENTATION-LAYERING.md" if source["layering"]["kind"]=="seed" else "LAYERING-GAP.md"
    if source["output_contracts"]["layering"]!=expected_layer: raise ValueError("layering output contract mismatch")
    if source["identity_denominator"]["classification"]=="required":
        verify_ref(repo_root,source["identity_denominator"]["request_ref"],"identity request")
        verify_ref(repo_root,source["identity_denominator"]["result_ref"],"identity result")
        result=json.loads((repo_root/source["identity_denominator"]["result_ref"]["path"]).read_text())
        if result.get("verdict")!="pass": raise ValueError("identity denominator result is not pass")
    stage=Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.",dir=output_dir.parent))
    try:
        decl="\n\n".join(f"## {x['title']}\n\n{x['statement']}" for x in source["spec_declarations"])
        (stage/"SPEC.md").write_text(f"# {source['target']['id']}\n\n{source['target']['objective']}\n\n{decl}\n",encoding="utf-8")
        rows="\n".join(f"| {x['term']} | {x['definition']} | {x['link_status']} | {x['rationale'] or '-'} |" for x in source["glossary"])
        (stage/"GLOSSARY.md").write_text("# Glossary\n\n| Term | Definition | Link | Rationale |\n| --- | --- | --- | --- |\n"+rows+"\n",encoding="utf-8")
        if source["layering"]["kind"]=="seed": text=f"# Implementation Layering Seed\n\n- Decision: {source['layering']['decision']}\n- Minimum unit: {source['layering']['minimum_unit']}\n"
        else: text=f"# Implementation Layering Gap\n\n{source['layering']['rationale']}\n"
        (stage/expected_layer).write_text(text,encoding="utf-8")
        docs={
          "TEMPLATE-SELECTION-RECEIPT.json":{"schema_version":"invoke.define-template-selection.v1",**source["template_selection"],"result":"pass"},
          "DISPATCH-TRACE.json":{"schema_version":"invoke.define-dispatch-trace.v1",**source["dispatch_trace"],"result":"pass"},
          "DISTILL-RECEIPT.json":{"schema_version":"invoke.define-distill-classification.v1",**source["distill"],"result":"pass"},
          "IDENTITY-DENOMINATOR-RECEIPT.json":{"schema_version":"invoke.define-identity-classification.v1",**source["identity_denominator"],"result":"pass"},
          "DEFINE-TRANSPORT-REPORT.json":{"schema_version":"invoke.define-transport.v1","policy":source["transport_policy"],"result":"no-op","authority_effect":"none"}}
        for name,doc in docs.items(): (stage/name).write_text(json.dumps(doc,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        if late_validator: late_validator(stage)
        contracts=source["output_contracts"]
        outputs=[]
        for key,kind in KINDS.items():
            name=contracts[key]; outputs.append({"kind":kind,**exact_ref(stage/name,name)})
        script=Path(__file__).resolve()
        receipt={"schema_version":"invoke.define-stage-receipt.v1","receipt_id":f"define:{source['source_id']}:{canonical_digest(source)[:16]}","owner_capability":"invoke","mode":"define","producer":{"identity":IDENTITY,"path":"arcanum/spells/invoke/scripts/compile_define_source.py","sha256":hashlib.sha256(script.read_bytes()).hexdigest()},"profile_id":PROFILE,"source_ref":exact_ref(source_path,source_path.relative_to(repo_root).as_posix()),"outputs":outputs,"result":"pass","next_route":source["next_route"],"authority_effect":"none","receipt_digest":"0"*64}
        receipt["receipt_digest"]=canonical_digest(receipt,"receipt_digest")
        errors=schema_errors(receipt,result_schema)
        if errors: raise ValueError("result schema invalid: "+"; ".join(errors))
        (stage/contracts["stage_receipt"]).write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        os.replace(stage,output_dir)
        return receipt
    except Exception:
        shutil.rmtree(stage,ignore_errors=True); raise

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("--output-dir",required=True,type=Path); p.add_argument("--repo-root",default=".",type=Path); p.add_argument("--schema-dir",type=Path); a=p.parse_args()
    root=a.repo_root.resolve(); schemas=a.schema_dir or root/"arcanum/spells/invoke/schemas"
    try: receipt=compile_source(a.source.resolve(),a.output_dir.resolve(),root,schemas.resolve())
    except (OSError,ValueError,json.JSONDecodeError) as e: print(f"BLOCK: {e}"); return 2
    print(json.dumps(receipt,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
