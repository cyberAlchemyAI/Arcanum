#!/usr/bin/env python3
"""Independently admit an exact Design v3 bundle by clean deterministic replay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

from compile_design_source_v3 import compile_bundle
from design_stage_contract_v2 import validate_stage_receipt
from design_successor_support import canonical_digest, load_module, load_store, translate_identity


SCRIPT_DIR = Path(__file__).resolve().parent
IDENTITY = "invoke.validate-design-bundle-admission.v2"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_bundle_admission_v2.py"


def validate_bundle(bundle: Path, root: Path, output: Path, schema_dir: Path) -> int:
    old = load_module("invoke_design_admission_v1_compat", SCRIPT_DIR / "validate_design_bundle_admission.py")
    original_load = old.load_json
    original_make = old.make_receipt
    store = load_store(schema_dir)

    def load_json_redirect(path: Path) -> dict[str, Any]:
        if path.parent.resolve() == schema_dir.resolve() and path.name == "design-bundle-admission-receipt-v1.schema.json":
            path = schema_dir / "design-bundle-admission-receipt-v2.schema.json"
        return original_load(path)

    def make(*args: Any, **kwargs: Any) -> dict[str, Any]:
        receipt = original_make(*args, **kwargs)
        result = translate_identity(
            receipt,
            schema_uri="https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2",
            schema_version="invoke.design-bundle-admission-receipt.v2",
            digest_field="receipt_digest",
            identity=IDENTITY,
            path=VALIDATOR_PATH,
            executable=Path(__file__),
        )
        result["receipt_id"] = result["receipt_id"].replace("design-admission:", "design-admission-v2:")
        result["receipt_digest"] = canonical_digest(result, "receipt_digest")
        return result

    class ResolverAwareValidator:
        def __init__(self, schema: dict[str, Any]):
            self._validator = Draft202012Validator(schema, resolver=RefResolver.from_schema(schema, store=store))

        def iter_errors(self, document: Any):
            return self._validator.iter_errors(document)

    old.IDENTITY = IDENTITY
    old.VALIDATOR_PATH = VALIDATOR_PATH
    old.load_json = load_json_redirect
    old.make_receipt = make
    old.validate_stage_receipt = validate_stage_receipt
    old.compile_bundle = compile_bundle
    old.Draft202012Validator = ResolverAwareValidator
    return old.validate_bundle(bundle, root, output, schema_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_dir", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    try:
        return validate_bundle(args.bundle_dir, root, args.output, args.schema_dir or root / "arcanum/spells/invoke/schemas")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
