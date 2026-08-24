#!/usr/bin/env python3
"""Validate the Invoke Plan readiness binding before Refine synthesis."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REFINE_ROOT = Path(__file__).resolve().parents[1]
BINDING_SCHEMA = REFINE_ROOT / "schemas" / "invoke-plan-readiness-binding.schema.json"
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


def resolve_exact(root: Path, reference: dict[str, Any]) -> Path:
    relative = Path(reference["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("readiness receipt path must be normalized and repository-relative")
    target = (root / relative).resolve()
    resolved_root = root.resolve()
    try:
        target.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError("readiness receipt escapes the repository root") from error
    content = target.read_bytes()
    if len(content) != reference["size_bytes"]:
        raise ValueError("readiness receipt size mismatch")
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError("readiness receipt digest mismatch")
    return target


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
        validate(binding, BINDING_SCHEMA, "Invoke Plan readiness binding")
        if binding["execution_designation"] == "non-executing":
            result = {
                "status": "not-applicable",
                "code": "NON_EXECUTING_PLAN",
                "work_pack_id": None,
                "readiness_receipt_ref": None,
                "authority_effect": "none",
                "claim": binding["non_execution_reason"],
            }
        else:
            receipt_path = resolve_exact(
                args.repository_root, binding["readiness_receipt_ref"]
            )
            receipt = load_json(receipt_path)
            validate(receipt, RECEIPT_SCHEMA, "Plan readiness receipt")
            if receipt["work_pack_id"] != binding["work_pack_id"]:
                raise ValueError("readiness receipt Work Pack identity mismatch")
            result = {
                "status": "pass",
                "code": "REFINE_PLAN_IMPLEMENTATION_READY",
                "work_pack_id": binding["work_pack_id"],
                "readiness_receipt_ref": binding["readiness_receipt_ref"],
                "authority_effect": "none",
                "claim": "Invoke Plan produced a validated implementation-ready candidate; execution acceptance and mutation admission remain separate.",
            }
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
