#!/usr/bin/env python3
"""Validate Refine's exact Invoke-owned Plan stage and readiness binding."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REFINE_ROOT = Path(__file__).resolve().parents[1]
BINDING_SCHEMAS = {
    "refine.invoke-plan-readiness-binding/v1":
        REFINE_ROOT / "schemas" / "invoke-plan-readiness-binding.schema.json",
    "refine.invoke-plan-readiness-binding/v2":
        REFINE_ROOT / "schemas" / "invoke-plan-readiness-binding-v2.schema.json",
}
STAGE_RECEIPT_SCHEMA = (
    REFINE_ROOT / "schemas" / "invoke-plan-stage-receipt-v1.schema.json"
)
READINESS_CANDIDATES = [
    REFINE_ROOT.parent / "implementation-readiness",
    REFINE_ROOT.parent.parent / "spells" / "implementation-readiness",
]
READINESS_ROOT = next(
    (candidate for candidate in READINESS_CANDIDATES if candidate.is_dir()),
    READINESS_CANDIDATES[0],
)
RECEIPT_SCHEMA = (
    READINESS_ROOT / "schemas" / "plan-readiness-preflight-receipt.schema.json"
)
REQUIRED_INVOKE_OUTPUT_KINDS = {
    "plan-artifact",
    "work-pack",
    "implementation-layering",
    "distill-validation",
    "invoke-result",
    "implementation-readiness-preflight",
}


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate(document: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(map(str, error.absolute_path)) or "<root>"
        raise ValueError(f"{label} at {location}: {error.message}")


def resolve_exact(root: Path, reference: dict[str, Any], label: str) -> Path:
    relative = Path(reference["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label} path must be normalized and repository-relative")
    target = (root / relative).resolve()
    resolved_root = root.resolve()
    try:
        target.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(f"{label} escapes the repository root") from error
    content = target.read_bytes()
    if len(content) != reference["size_bytes"]:
        raise ValueError(f"{label} size mismatch")
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError(f"{label} digest mismatch")
    return target


def validate_output_set(root: Path, outputs: list[dict[str, Any]]) -> None:
    kinds = [item["output_kind"] for item in outputs]
    if len(kinds) != len(set(kinds)):
        raise ValueError("Invoke Plan output kinds must be unique")
    missing = sorted(REQUIRED_INVOKE_OUTPUT_KINDS - set(kinds))
    if missing:
        raise ValueError("Invoke Plan stage receipt lacks required outputs: " + ", ".join(missing))
    for item in outputs:
        resolve_exact(root, item["artifact_ref"], f"Invoke output {item['output_kind']}")


def validate_v2_execution_candidate(
    root: Path, binding: dict[str, Any]
) -> dict[str, Any]:
    stage_path = resolve_exact(
        root, binding["invoke_plan_stage_receipt_ref"], "Invoke Plan stage receipt"
    )
    stage = load_json(stage_path)
    validate(stage, STAGE_RECEIPT_SCHEMA, "Invoke Plan stage receipt")
    projection = dict(stage)
    observed_digest = projection.pop("receipt_digest")
    if observed_digest != canonical_digest(projection):
        raise ValueError("Invoke Plan stage receipt digest mismatch")
    if stage["execution_designation"] != binding["execution_designation"]:
        raise ValueError("Invoke Plan stage execution designation mismatch")
    if stage["work_pack_id"] != binding["work_pack_id"]:
        raise ValueError("Invoke Plan stage Work Pack identity mismatch")
    if stage["invoke_outputs"] != binding["invoke_outputs"]:
        raise ValueError("Invoke Plan stage outputs differ from Refine binding")
    if stage["readiness_receipt_ref"] != binding["readiness_receipt_ref"]:
        raise ValueError("Invoke Plan stage readiness reference mismatch")
    validate_output_set(root, stage["invoke_outputs"])
    readiness_output = next(
        item for item in stage["invoke_outputs"]
        if item["output_kind"] == "implementation-readiness-preflight"
    )
    if readiness_output["artifact_ref"] != binding["readiness_receipt_ref"]:
        raise ValueError("Invoke output set does not bind the same readiness receipt")
    receipt_path = resolve_exact(
        root, binding["readiness_receipt_ref"], "readiness receipt"
    )
    receipt = load_json(receipt_path)
    validate(receipt, RECEIPT_SCHEMA, "Plan readiness receipt")
    if receipt["work_pack_id"] != binding["work_pack_id"]:
        raise ValueError("readiness receipt Work Pack identity mismatch")
    return {
        "status": "pass",
        "code": "REFINE_INVOKE_PLAN_STAGE_READY",
        "work_pack_id": binding["work_pack_id"],
        "invoke_plan_stage_receipt_ref": binding["invoke_plan_stage_receipt_ref"],
        "invoke_outputs": binding["invoke_outputs"],
        "readiness_receipt_ref": binding["readiness_receipt_ref"],
        "authority_effect": "none",
        "claim": "Invoke owns the exact terminal Plan stage and readiness evidence; Refine only consumes the byte-current binding.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        binding = load_json(args.binding)
        version = binding.get("schema_version")
        schema_path = BINDING_SCHEMAS.get(version)
        if schema_path is None:
            raise ValueError("unsupported Invoke Plan readiness binding version")
        validate(binding, schema_path, "Invoke Plan readiness binding")
        if binding["execution_designation"] == "non-executing":
            result = {
                "status": "not-applicable",
                "code": "NON_EXECUTING_PLAN",
                "work_pack_id": None,
                "invoke_plan_stage_receipt_ref": None,
                "readiness_receipt_ref": None,
                "authority_effect": "none",
                "claim": binding["non_execution_reason"],
            }
        elif version == "refine.invoke-plan-readiness-binding/v1":
            raise ValueError(
                "v1 is historical-read/non-executing only and cannot establish a new execution-candidate"
            )
        else:
            result = validate_v2_execution_candidate(
                args.repository_root.resolve(), binding
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
