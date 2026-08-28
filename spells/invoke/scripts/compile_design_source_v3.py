#!/usr/bin/env python3
"""Compile one W2 v2 candidate plus passing Distill evidence into a W3 v3 bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from design_successor_support import aliased_store, canonical_digest, load_module, schema_for_document, translate_identity


SCRIPT_DIR = Path(__file__).resolve().parent
IDENTITY = "invoke.compile-design-source.v3"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_source_v3.py"
W2_PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_candidate_v2.py"


def compile_bundle(
    closure_path: Path,
    root: Path,
    output_dir: Path,
    attempt_path: Path,
    schema_dir: Path,
    late_validation_hook: Callable[[Path], None] | None = None,
) -> int:
    old = load_module("invoke_design_w3_v2_compat", SCRIPT_DIR / "compile_design_source_v2.py")
    original_attempt = old.attempt_receipt
    original_stage = old.stage_receipt
    original_errors = old.schema_errors
    store = aliased_store(schema_dir)

    def attempt(*args: Any, **kwargs: Any) -> dict[str, Any]:
        receipt = original_attempt(*args, **kwargs)
        result = translate_identity(
            receipt,
            schema_uri="https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v2",
            schema_version="invoke.design-bundle-attempt-receipt.v2",
            digest_field="receipt_digest",
            identity=IDENTITY,
            path=PRODUCER_PATH,
            executable=Path(__file__),
        )
        result["receipt_id"] = result["receipt_id"].replace("design-w3-attempt:", "design-w3-v3-attempt:")
        result["receipt_digest"] = canonical_digest(result, "receipt_digest")
        return result

    def stage(*args: Any, **kwargs: Any) -> dict[str, Any]:
        receipt = original_stage(*args, **kwargs)
        result = translate_identity(
            receipt,
            schema_uri="https://arcanum.dev/schemas/invoke/design-result/v3",
            schema_version="invoke.design-stage-receipt.v3",
            digest_field="receipt_digest",
            identity=IDENTITY,
            path=PRODUCER_PATH,
            executable=Path(__file__),
        )
        result["receipt_id"] = result["receipt_id"].replace("design-w3:", "design-w3-v3:")
        result["receipt_digest"] = canonical_digest(result, "receipt_digest")
        return result

    def schema_errors(document: dict[str, Any], schema: dict[str, Any], selected_store: dict[str, dict[str, Any]]) -> list[str]:
        return original_errors(document, schema_for_document(document, schema, store), store)

    old.IDENTITY = IDENTITY
    old.PRODUCER_PATH = PRODUCER_PATH
    old.W2_PRODUCER_PATH = W2_PRODUCER_PATH
    old.schema_store = lambda directory: store
    old.schema_errors = schema_errors
    old.attempt_receipt = attempt
    old.stage_receipt = stage
    return old.compile_bundle(closure_path, root, output_dir, attempt_path, schema_dir, late_validation_hook)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("closure", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--attempt-receipt", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    try:
        return compile_bundle(args.closure, root, args.output_dir, args.attempt_receipt, args.schema_dir or root / "arcanum/spells/invoke/schemas")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
