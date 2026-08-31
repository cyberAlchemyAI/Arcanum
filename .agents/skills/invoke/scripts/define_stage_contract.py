#!/usr/bin/env python3
"""Shared validation for current and historical Invoke Define receipts."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


CURRENT_STAGE_VERSION = "invoke.define-stage-receipt.v3"
CURRENT_STAGE_SCHEMA = "define-result-v3.schema.json"
CURRENT_PRODUCER_PATH = ".agents/skills/invoke/scripts/compile_define_source_v3.py"
CURRENT_ADMISSION_PATH = ".agents/skills/invoke/scripts/validate_define_bundle_admission.py"
CURRENT_OUTPUT_KINDS = (
    "semantic-context",
    "semantic-closure-receipt",
    "spec",
    "definitions",
    "definitions-view",
    "glossary",
    "layering",
    "template-selection",
    "dispatch-trace",
    "distill",
    "identity-denominator",
    "transport",
)
HISTORICAL_STAGE_VERSIONS = {
    "invoke.define-stage-receipt.v1",
    "invoke.define-stage-receipt.v2",
}
ADMISSION_CHECK_IDS = (
    "check:bundle-shape",
    "check:stage-receipt",
    "check:producer-identity",
    "check:schema-bindings",
    "check:ordered-inventory",
    "check:semantic-closure",
    "check:clean-replay",
    "check:definitions",
    "check:generated-views",
    "check:structural-schemas",
    "check:semantic-outcome",
    "check:authority-effect",
    "check:prior-admission",
)


def digest_without(document: dict[str, Any], field: str) -> str:
    projection = copy.deepcopy(document)
    projection.pop(field, None)
    return hashlib.sha256(
        json.dumps(
            projection,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def canonical_value_digest(value: Any) -> str:
    material = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_diagnostics(document: Any, schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} schema invalid at {'/'.join(map(str, error.path)) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def validate_stage_receipt(
    receipt: Any,
    repo_root: Path,
    schema_dir: Path,
) -> list[str]:
    """Admit only a current Define v3 stage receipt for a new PASS."""

    if not isinstance(receipt, dict):
        return ["Define PASS requires an exact Invoke-owned producer receipt"]
    version = receipt.get("schema_version")
    if version in HISTORICAL_STAGE_VERSIONS:
        return [f"{version} producer receipts are historical/read-only and cannot establish a new PASS"]
    if version != CURRENT_STAGE_VERSION:
        return [f"unsupported Define producer receipt version: {version!r}"]

    diagnostics: list[str] = []
    schema = json.loads((schema_dir / CURRENT_STAGE_SCHEMA).read_text(encoding="utf-8"))
    diagnostics.extend(schema_diagnostics(receipt, schema, "Define producer receipt"))
    if diagnostics:
        return diagnostics
    if receipt["receipt_digest"] != digest_without(receipt, "receipt_digest"):
        diagnostics.append("Define producer receipt digest mismatch")
    producer = repo_root / CURRENT_PRODUCER_PATH
    if not producer.is_file() or receipt["producer"]["sha256"] != file_sha256(producer):
        diagnostics.append("Define producer identity digest mismatch")
    received = [item["kind"] for item in receipt["outputs"]]
    if received != list(CURRENT_OUTPUT_KINDS) or len(received) != len(set(received)):
        diagnostics.append("Define producer output inventory mismatch")
    return diagnostics


def validate_admission_receipt(
    receipt: Any,
    producer: Any,
    repo_root: Path,
    schema_dir: Path,
) -> list[str]:
    """Validate an exact, current, drift-free Define bundle admission."""

    if not isinstance(receipt, dict):
        return ["Define PASS requires an exact independent bundle admission receipt"]
    if not isinstance(producer, dict):
        return ["Define admission cannot be evaluated without its stage receipt"]

    diagnostics: list[str] = []
    schema = json.loads(
        (schema_dir / "define-bundle-admission-receipt-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    diagnostics.extend(schema_diagnostics(receipt, schema, "Define bundle admission receipt"))
    if diagnostics:
        return diagnostics
    if receipt["receipt_digest"] != digest_without(receipt, "receipt_digest"):
        diagnostics.append("Define bundle admission receipt digest mismatch")
    installed = repo_root / CURRENT_ADMISSION_PATH
    if not installed.is_file() or receipt["validator"]["sha256"] != file_sha256(installed):
        diagnostics.append("Define bundle admission validator identity digest mismatch")

    expected_binding = {
        "receipt_id": producer.get("receipt_id"),
        "receipt_digest": producer.get("receipt_digest"),
        "profile_id": producer.get("profile_id"),
        "producer": producer.get("producer"),
    }
    if receipt["producer_binding"] != expected_binding:
        diagnostics.append("Define stage/admission producer binding mismatch")
    if receipt["stage_receipt_ref"] is None:
        diagnostics.append("Define admission does not exact-bind its stage receipt")

    expected_outputs = producer.get("outputs", [])
    admitted_outputs = receipt["output_inventory"][:12]
    if len(receipt["output_inventory"]) != 13:
        diagnostics.append("Define admission output inventory must contain exactly thirteen entries")
    elif receipt["output_inventory"][-1]["kind"] != "stage-receipt":
        diagnostics.append("Define admission output inventory lacks the terminal stage receipt")
    elif {
        key: receipt["output_inventory"][-1][key]
        for key in ("path", "sha256", "size")
    } != receipt["stage_receipt_ref"]:
        diagnostics.append("Define admission stage receipt ref/inventory mismatch")
    if len(expected_outputs) != len(admitted_outputs):
        diagnostics.append("Define stage/admission output inventory length mismatch")
    else:
        for stage_item, admission_item in zip(
            expected_outputs, admitted_outputs, strict=True
        ):
            if (
                stage_item["kind"] != admission_item["kind"]
                or Path(stage_item["path"]).name != Path(admission_item["path"]).name
                or stage_item["sha256"] != admission_item["sha256"]
                or stage_item["size"] != admission_item["size"]
            ):
                diagnostics.append("Define stage/admission output inventory mismatch")
                break
    if receipt["replay"]["source_ref"] != producer.get("source_ref"):
        diagnostics.append("Define stage/admission source binding mismatch")
    if receipt["structural_schema_refs"] != producer.get("structural_schema_refs"):
        diagnostics.append("Define stage/admission structural-schema binding mismatch")
    if receipt["bundle_digest"] != canonical_value_digest(receipt["output_inventory"]):
        diagnostics.append("Define admission bundle digest mismatch")

    checks = receipt["checks"]
    if [check["check_id"] for check in checks] != list(ADMISSION_CHECK_IDS):
        diagnostics.append("Define admission required check inventory mismatch")
    elif any(check["status"] != "pass" for check in checks):
        diagnostics.append("Define admission contains a non-PASS required check")

    drift = receipt["drift_analysis"]
    required_summary = {
        "evidence_state": "current",
        "semantic_state": "unchanged",
        "authority_state": "unchanged",
        "topology_state": "unchanged",
        "projection_state": "unchanged",
        "overall": "current",
    }
    if (
        receipt["result"] != "pass"
        or receipt["authority_effect"] != "none"
        or receipt["blockers"]
        or drift["differences"]
        or drift["compile_window"] != "current"
        or drift["summary"] != required_summary
        or receipt["replay"]["comparison"] != "pass"
    ):
        diagnostics.append("Define admission is not a current drift-free PASS")
    return diagnostics
