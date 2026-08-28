#!/usr/bin/env python3
"""Validate Design source/artifact v2 coherence under the unchanged public policy."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver

from design_successor_support import aliased_store, canonical_digest, load_module, load_store, schema_for_document, translate_identity
from project_design_artifact_v2 import project_design_artifact


SCRIPT_DIR = Path(__file__).resolve().parent
IDENTITY = "invoke.validate-design-coherence.v2"
VALIDATOR_PATH = "arcanum/spells/invoke/scripts/validate_design_coherence_v2.py"
W1_PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_input_bundle_v2.py"


def validate_design_coherence(
    source_path: Path,
    artifact_path: Path,
    artifact_ref: dict[str, Any],
    root: Path,
    schema_dir: Path,
) -> dict[str, Any]:
    old = load_module("invoke_design_coherence_v1_compat", SCRIPT_DIR / "validate_design_coherence.py")
    raw_store = load_store(schema_dir)
    store = aliased_store(schema_dir)
    original_errors = old.schema_errors

    def schema_errors(document: dict[str, Any], schema: dict[str, Any], selected_store: dict[str, dict[str, Any]]) -> list[str]:
        return original_errors(document, schema_for_document(document, schema, store), store)

    old.schema_store = lambda _: store
    old.schema_errors = schema_errors
    old.project_design_artifact = project_design_artifact
    old.W1_PRODUCER_PATH = W1_PRODUCER_PATH
    receipt = old.validate_design_coherence(source_path, artifact_path, artifact_ref, root, schema_dir)
    result = translate_identity(
        receipt,
        schema_uri="https://arcanum.dev/schemas/invoke/design-coherence-receipt/v2",
        schema_version="invoke.design-coherence-receipt.v2",
        digest_field="receipt_digest",
        identity=IDENTITY,
        path=VALIDATOR_PATH,
        executable=Path(__file__),
    )
    result["receipt_id"] = result["receipt_id"].replace("design-w2-coherence:", "design-w2-coherence-v2:")
    result["receipt_digest"] = canonical_digest(result, "receipt_digest")
    schema = raw_store["https://arcanum.dev/schemas/invoke/design-coherence-receipt/v2"]
    resolver = RefResolver.from_schema(schema, store=raw_store)
    errors = [error.message for error in Draft202012Validator(schema, resolver=resolver).iter_errors(result)]
    if errors:
        raise old.ContractFailure("COHERENCE_BLOCKED", "; ".join(errors[:12]), "coherence-receipt", "repair-installed-contract")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    schema_dir = args.schema_dir or SCRIPT_DIR.parent / "schemas"
    old = load_module("invoke_design_coherence_v1_cli", SCRIPT_DIR / "validate_design_coherence.py")
    try:
        receipt = validate_design_coherence(args.source, args.artifact, old.exact_ref(args.artifact, root), root, schema_dir)
        output = Path(os.path.abspath(args.output))
        if output.exists() or output.is_symlink() or not output.parent.is_dir():
            raise ValueError("output must be absent with an existing parent")
        fd, temporary = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(receipt, handle, indent=2, sort_keys=True, ensure_ascii=False)
                handle.write("\n")
            os.replace(temporary, output)
        except Exception:
            Path(temporary).unlink(missing_ok=True)
            raise
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, KeyError) as error:
        print(f"ERROR: {error}")
        return 2
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
