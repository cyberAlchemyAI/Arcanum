#!/usr/bin/env python3
"""Compile one Design input closure v2 into an atomic W1 v2 bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, RefResolver

from design_successor_support import canonical_digest, load_module, load_store, translate_identity
from validate_design_input_closure_v2 import validate_input_closure


SCRIPT_DIR = Path(__file__).resolve().parent
IDENTITY = "invoke.compile-design-input-bundle.v2"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_input_bundle_v2.py"
SCHEMA_REDIRECT = {
    "design-input-closure-receipt-v1.schema.json": "design-input-closure-receipt-v2.schema.json",
    "design-input-production-receipt-v1.schema.json": "design-input-production-receipt-v2.schema.json",
}


def compile_bundle(
    source_path: Path,
    repository_root: Path,
    output_dir: Path,
    attempt_receipt: Path,
    schema_dir: Path,
    late_validator: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    old = load_module("invoke_design_w1_v1_compat", SCRIPT_DIR / "compile_design_input_bundle.py")
    original_load = old.load_json
    original_build = old.build_production_receipt
    store = load_store(schema_dir)

    def redirected_load(path: Path) -> dict[str, Any]:
        selected = schema_dir / SCHEMA_REDIRECT[path.name] if path.parent.resolve() == schema_dir.resolve() and path.name in SCHEMA_REDIRECT else path
        return original_load(selected)

    def build(*args: Any, **kwargs: Any) -> dict[str, Any]:
        receipt = original_build(*args, **kwargs)
        result = translate_identity(
            receipt,
            schema_uri="https://arcanum.dev/schemas/invoke/design-input-production-receipt/v2",
            schema_version="invoke.design-input-production-receipt.v2",
            digest_field="receipt_digest",
            identity=IDENTITY,
            path=PRODUCER_PATH,
            executable=Path(__file__),
        )
        result["receipt_id"] = result["receipt_id"].replace("design-w1:", "design-w1-v2:")
        result["receipt_digest"] = canonical_digest(result, "receipt_digest")
        return result

    def validate_receipt(receipt: dict[str, Any], schemas: dict[str, dict[str, Any]]) -> None:
        schema = store["https://arcanum.dev/schemas/invoke/design-input-production-receipt/v2"]
        resolver = RefResolver.from_schema(schema, store=store)
        errors = [error.message for error in Draft202012Validator(schema, resolver=resolver).iter_errors(receipt)]
        if errors:
            raise ValueError("production receipt v2 schema invalid: " + "; ".join(errors[:12]))
        if receipt["receipt_digest"] != canonical_digest(receipt, "receipt_digest"):
            raise ValueError("production receipt v2 digest is stale")

    old.IDENTITY = IDENTITY
    old.PRODUCER_PATH = PRODUCER_PATH
    old.__file__ = str(Path(__file__).resolve())
    old.load_json = redirected_load
    old.validate_input_closure = validate_input_closure
    old.build_production_receipt = build
    old.validate_production_receipt = validate_receipt
    return old.compile_bundle(source_path, repository_root, output_dir, attempt_receipt, schema_dir, late_validator)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("closure", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--attempt-receipt", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    schema_dir = args.schema_dir or SCRIPT_DIR.parent / "schemas"
    try:
        receipt = compile_bundle(args.closure, args.repo_root, args.output_dir, args.attempt_receipt, schema_dir)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
