#!/usr/bin/env python3
"""Validate actual postimages only after the selected producer has returned."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path, PurePosixPath

class PostProduceBlock(ValueError): pass
def resolve(root:Path,raw:str)->Path:
 p=PurePosixPath(raw)
 if p.is_absolute() or ".." in p.parts or "\\" in raw:raise PostProduceBlock(f"unsafe path: {raw}")
 return root.joinpath(*p.parts)
def ref(root:Path,raw:str)->dict:
 p=resolve(root,raw)
 if not p.is_file():raise PostProduceBlock(f"declared output missing: {raw}")
 b=p.read_bytes();return {"path":raw,"sha256":hashlib.sha256(b).hexdigest(),"size_bytes":len(b)}
def validate(unit_id:str,root:Path,declared:list[str],commands:list[dict],observed:list[str]|None=None)->dict:
 if not declared or len(declared)!=len(set(declared)):raise PostProduceBlock("declared outputs are empty or duplicated")
 observed=sorted(observed if observed is not None else declared);undeclared=sorted(set(observed)-set(declared))
 if undeclared:raise PostProduceBlock("undeclared outputs: "+", ".join(undeclared))
 postimages=[ref(root,p) for p in declared];results=[]
 for command in commands:
  if command.get("phase")!="post-produce":continue
  completed=subprocess.run(command["argv"],cwd=resolve(root,command["cwd"]),check=False,capture_output=True,text=True)
  results.append({"argv":command["argv"],"exit_code":completed.returncode})
  if completed.returncode!=0:raise PostProduceBlock(f"post-produce validation failed: {command['argv']}")
 if not results:raise PostProduceBlock("no post-produce validation command executed")
 return {"schema_version":"task-session.post-produce-validation-receipt.v1","unit_id":unit_id,"result":"pass","actual_postimages":postimages,"commands":results,"undeclared_outputs":[],"authority_effect":"none"}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--contract",type=Path,required=True);p.add_argument("--repo-root",type=Path,default=Path.cwd());a=p.parse_args();c=json.loads(a.contract.read_text())
 try: print(json.dumps(validate(c["unit_id"],a.repo_root,c["declared_outputs"],c["validation_commands"],c.get("observed_outputs")),sort_keys=True));return 0
 except (PostProduceBlock,OSError,json.JSONDecodeError) as exc:print(f"BLOCK: {exc}");return 2
if __name__=="__main__":raise SystemExit(main())
