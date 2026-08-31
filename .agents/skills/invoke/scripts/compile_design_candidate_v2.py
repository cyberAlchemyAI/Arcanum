#!/usr/bin/env python3
"""Compile one normal W1 v2-bound Design source v2 into an atomic W2 v2 candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from design_successor_support import aliased_store, canonical_digest, load_module, schema_for_document, translate_identity
from project_design_artifact_v2 import project_design_artifact
from validate_design_coherence_v2 import validate_design_coherence


SCRIPT_DIR = Path(__file__).resolve().parent
IDENTITY = "invoke.compile-design-candidate.v2"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_candidate_v2.py"
W1_PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_input_bundle_v2.py"


def compile_candidate(
    source_path: Path,
    root: Path,
    output_dir: Path,
    attempt_receipt: Path,
    schema_dir: Path,
    late_validation_hook: Callable[[Path], None] | None = None,
) -> int:
    old = load_module("invoke_design_candidate_v1_compat", SCRIPT_DIR / "compile_design_candidate.py")
    original_make = old.make_receipt
    original_exact = old.exact_ref
    original_errors = old.schema_errors
    store = aliased_store(schema_dir)

    def exact_ref(path: Path, repo_root: Path) -> dict[str, Any]:
        if path.as_posix().endswith("arcanum/spells/invoke/scripts/compile_design_input_bundle.py"):
            path = repo_root / W1_PRODUCER_PATH
        return original_exact(path, repo_root)

    def make(*args: Any, **kwargs: Any) -> dict[str, Any]:
        receipt = original_make(*args, **kwargs)
        result = translate_identity(
            receipt,
            schema_uri="https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v2",
            schema_version="invoke.design-candidate-production-receipt.v2",
            digest_field="receipt_digest",
            identity=IDENTITY,
            path=PRODUCER_PATH,
            executable=Path(__file__),
        )
        result["receipt_id"] = result["receipt_id"].replace("design-w2:", "design-w2-v2:")
        result["receipt_digest"] = canonical_digest(result, "receipt_digest")
        return result

    def schema_errors(document: dict[str, Any], schema: dict[str, Any], selected_store: dict[str, dict[str, Any]]) -> list[str]:
        return original_errors(document, schema_for_document(document, schema, store), store)

    def coherence(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return validate_design_coherence(*args, **kwargs)
        except Exception as error:
            if isinstance(error, (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError)):
                raise old.ContractFailure("COHERENCE_BLOCKED", str(error), None, "repair-design-source") from error
            raise

    old.IDENTITY = IDENTITY
    old.PRODUCER_PATH = PRODUCER_PATH
    old.schema_store = lambda directory: store
    old.schema_errors = schema_errors
    old.exact_ref = exact_ref
    old.project_design_artifact = project_design_artifact
    old.validate_design_coherence = coherence
    old.make_receipt = make
    return old.compile_candidate(source_path, root, output_dir, attempt_receipt, schema_dir, late_validation_hook)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--attempt-receipt", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    try:
        return compile_candidate(args.source, root, args.output_dir, args.attempt_receipt, args.schema_dir or root / "arcanum/spells/invoke/schemas")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
