#!/usr/bin/env python3
"""Validate the candidate Invoke precloseout Refresh owner-closeout contract.

This harness validates only typed receipt shape and cross-field bindings.  It
does not run Refresh, materialize a package, consume admission, execute a Task
Session, or write a closeout artifact.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REQUIRED_VALIDATION_KINDS = {
    "source-precloseout",
    "material-reconciliation",
    "target-validation",
}


def receipt_projection_digest(receipt: dict[str, Any]) -> str:
    """Return the closed, non-self-referential receipt digest.

    The canonical projection removes only ``receipt_digest``.  The containing
    receipt file is deliberately not self-hashed; its exact bytes are bound by
    the final Task Session terminal receipt after Invoke has written it.
    """
    projection = copy.deepcopy(receipt)
    projection.pop("receipt_digest", None)
    encoded = json.dumps(
        projection,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(receipt: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        "schema invalid at "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(receipt),
            key=lambda error: list(error.path),
        )
    ]


def semantic_errors(
    receipt: dict[str, Any], source_precloseout: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    source = receipt["precloseout_source"]

    if receipt["receipt_digest"] != receipt_projection_digest(receipt):
        errors.append("receipt digest does not match canonical receipt projection")

    if source["receipt_ref"] != source_precloseout["receipt_ref"]:
        errors.append("precloseout receipt ref does not match supplied source")
    if source["schema_ref"] != source_precloseout["schema_ref"]:
        errors.append("precloseout schema ref does not match supplied source")
    if receipt["task_identity"] != source_precloseout["task_identity"]:
        errors.append(
            "task identity does not match supplied precloseout source"
        )
    if source["task_identity"] != source_precloseout["task_identity"]:
        errors.append(
            "embedded precloseout task identity does not match supplied source"
        )
    if receipt["final_owner_write"]["output_ref"] != receipt["closeout_output"]:
        errors.append(
            "final owner write does not equal declared closeout output"
        )
    if receipt["closeout_output"]["path"] == source["receipt_ref"]["path"]:
        errors.append("declared closeout output aliases precloseout source")

    validation_ids = [
        entry["validation_id"] for entry in receipt["validation_inventory"]
    ]
    if len(validation_ids) != len(set(validation_ids)):
        errors.append("validation inventory contains duplicate validation_id")
    validation_kinds = {
        entry["kind"] for entry in receipt["validation_inventory"]
    }
    missing_kinds = sorted(REQUIRED_VALIDATION_KINDS - validation_kinds)
    if missing_kinds:
        errors.append(
            "validation inventory missing required kind: "
            + ", ".join(missing_kinds)
        )
    return errors


def mutate(
    receipt: dict[str, Any], mutation: str
) -> dict[str, Any]:
    result = copy.deepcopy(receipt)
    if mutation == "none":
        return result
    if mutation == "no-op-result":
        result["result"] = "no-op"
    elif mutation == "source-receipt-ref-drift":
        result["precloseout_source"]["receipt_ref"]["sha256"] = "8" * 64
    elif mutation == "source-schema-ref-drift":
        result["precloseout_source"]["schema_ref"]["sha256"] = "9" * 64
    elif mutation == "task-identity-drift":
        result["task_identity"]["attempt_id"] = "attempt-002"
    elif mutation == "owner-capability-drift":
        result["owner_identity"]["capability"] = "task-session"
    elif mutation == "owner-mutation-mode-drift":
        result["owner_identity"]["mutation_mode"] = "proposal-only"
    elif mutation == "owner-activation-drift":
        result["owner_identity"]["activation_source"] = "direct-user"
    elif mutation == "closeout-output-drift":
        result["closeout_output"]["path"] = (
            "arcanum/arcana/ux-evidence-validator/development/work-packs/"
            "uev-deterministic-kernel/results/SWU-UEV-001-RESULT.json"
        )
    elif mutation == "final-owner-write-drift":
        result["final_owner_write"]["output_ref"]["path"] = (
            "arcanum/arcana/ux-evidence-validator/development/work-packs/"
            "uev-deterministic-kernel/closeout/SWU-UEV-002-REFRESH-RECEIPT.json"
        )
    elif mutation == "missing-validation-kind":
        result["validation_inventory"] = [
            entry
            for entry in result["validation_inventory"]
            if entry["kind"] != "target-validation"
        ]
    elif mutation == "duplicate-validation-id":
        result["validation_inventory"][1]["validation_id"] = (
            result["validation_inventory"][0]["validation_id"]
        )
    elif mutation == "validation-result-drift":
        result["validation_inventory"][0]["result"] = "block"
    elif mutation == "result-drift":
        result["result"] = "block"
    elif mutation == "final-owner-write-incomplete":
        result["final_owner_write"]["completed"] = False
    elif mutation == "receipt-digest-drift":
        result["receipt_digest"] = "0" * 64
        return result
    elif mutation == "unsafe-source-parent-traversal":
        result["precloseout_source"]["receipt_ref"]["path"] = "../private/receipt.json"
    elif mutation == "unsafe-schema-absolute-path":
        result["precloseout_source"]["schema_ref"]["path"] = "/tmp/schema.json"
    elif mutation == "unsafe-closeout-drive-path":
        result["closeout_output"]["path"] = "C:/temp/receipt.json"
        result["final_owner_write"]["output_ref"]["path"] = "C:/temp/receipt.json"
    else:
        raise ValueError(f"unknown fixture mutation: {mutation}")
    if mutation != "none":
        result["receipt_digest"] = receipt_projection_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    args = parser.parse_args()

    fixtures = load_json(args.fixtures)
    schema = load_json(args.schema)
    failures: list[str] = []

    for case in fixtures["cases"]:
        receipt = mutate(fixtures["base_receipt"], case["mutation"])
        errors = schema_errors(receipt, schema)
        if not errors:
            errors.extend(
                semantic_errors(receipt, fixtures["source_precloseout"])
            )
        actual = "pass" if not errors else "fail"
        expected = case["expected"]
        expected_error = case.get("expected_error")
        matches = actual == expected and (
            expected_error is None
            or any(expected_error in error for error in errors)
        )
        if matches:
            print(f"PASS {case['id']}: {actual}")
        else:
            failures.append(case["id"])
            print(
                f"FAIL {case['id']}: expected {expected} "
                f"error={expected_error!r}; got {actual} "
                f"errors={json.dumps(errors, sort_keys=True)}"
            )

    if failures:
        print(f"RESULT block {len(failures)}/{len(fixtures['cases'])} failed")
        return 1
    print(f"RESULT pass {len(fixtures['cases'])}/{len(fixtures['cases'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
