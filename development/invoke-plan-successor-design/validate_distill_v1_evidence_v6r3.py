#!/usr/bin/env python3
"""Independently validate the exact W2 V6R3 Distill v1 evidence package."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("distill_semantic_validator_v6r3", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    evidence = args.evidence_dir.resolve()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        raise ValueError("--output must be absent")
    request_path = evidence / "DISTILL-RUN-REQUEST.json"
    events_path = evidence / "DISTILL-EVENTS.jsonl"
    receipt_path = evidence / "DISTILL-EXECUTION-RECEIPT.json"
    request = json.loads(request_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    invoke = root / "arcanum/spells/invoke"
    sys.path.insert(0, str(invoke / "development"))
    semantic = load_module(invoke / "development/distill_semantic_validator.py")
    case = {"request": request, "receipt": receipt, "events_fixture": events_path.name}
    diagnostics: list[str] = []
    checks: list[str] = []
    try:
        semantic_result = semantic.validate_semantic_case(case, invoke / "schemas", evidence)
        checks.extend(semantic_result["checks"])
    except Exception as error:
        diagnostics.append(f"semantic validation failed: {error}")
    for reference in request["reviewed_inputs"]:
        target = root / reference["path"]
        if not target.is_file() or exact(target, root) != reference:
            diagnostics.append(f"reviewed input mismatch: {reference['path']}")
    if receipt["reviewed_input_provenance"] != request["reviewed_inputs"]:
        diagnostics.append("request and receipt reviewed-input provenance differ")
    if receipt["verdict"] != "pass" or receipt["gaps"] or receipt["next_route"]["status"] != "ready":
        diagnostics.append("execution receipt is not a clean Distill PASS")
    if {item["role"] for item in receipt["role_trace"]} != {"proposer", "balancer"}:
        diagnostics.append("role trace does not contain exactly proposer and balancer")
    for item in receipt["role_trace"]:
        reference = item["result_ref"]
        target = root / reference["path"]
        if not target.is_file() or exact(target, root) != reference:
            diagnostics.append(f"role result mismatch: {reference['path']}")
    recomposition = receipt["recomposition"]["result_ref"]
    recomposition_path = root / recomposition["path"]
    if not recomposition_path.is_file() or exact(recomposition_path, root) != recomposition:
        diagnostics.append("recomposition result mismatch")
    checks.extend(["reviewed_input_digest_and_size", "request_receipt_provenance_agrees", "role_result_refs_resolve", "recomposition_ref_resolves", "clean_pass_ceiling"])
    unique_checks = list(dict.fromkeys(checks))
    status = "pass" if not diagnostics else "block"
    result = {
        "schema_version": "1.0.0",
        "validation_result_id": "distill-validation:plan-successor-w2-v6r3",
        "validator_version": "plan-successor-v6r3.1",
        "receipt_ref": exact(receipt_path, root),
        "status": status,
        "checks": [{"check_id": item, "status": status, "evidence_refs": receipt["event_refs"]} for item in unique_checks],
        "diagnostics": diagnostics,
        "owned_gaps": [] if status == "pass" else ["distill-v6r3-validation-gap"],
        "mutation_handoff_allowed": False,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
