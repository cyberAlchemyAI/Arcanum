#!/usr/bin/env python3
"""Validate one finalized execution-entry closure without granting authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from control_evidence_partition import validate_partition as validate_live_control_partition


ROOT = Path(__file__).resolve().parents[1]
PARTITION_SCHEMA = ROOT / "schemas/fast-entry-route-scope-partition-v1.schema.json"
CONTEXT_SCHEMA = ROOT / "schemas/native-context-admission-projection-v1.schema.json"
CONTEXT_FIELDS = {
    "writeProfile", "materialWrites", "executionOutputs", "allowedWrites",
    "validationCommands", "lifecycleOwner", "authorityClass", "publicationClass",
}
REHEARSAL_STAGES = [
    "wpra", "implementation-readiness", "context-builder", "mutation-admission",
    "governance-prepare", "closeout-preflight", "heterogeneous-owner-closeout",
    "terminal", "continuity",
]


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def is_exact_ref(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == {"path", "sha256", "size_bytes"}
        and isinstance(value.get("path"), str)
        and bool(value["path"])
        and isinstance(value.get("sha256"), str)
        and len(value["sha256"]) == 64
        and all(character in "0123456789abcdef" for character in value["sha256"])
        and isinstance(value.get("size_bytes"), int)
        and value["size_bytes"] >= 0
    )


def schema_failures(value: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_object(schema_path)
    return [
        f"{label} schema invalid at {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def validate_unit(unit: dict[str, Any], closure: dict[str, Any]) -> list[str]:
    unit_id = str(unit.get("unit_id", "<missing>"))
    failures: list[str] = []
    projection = unit.get("native_context_projection")
    partition = unit.get("route_scope_partition")
    if not isinstance(projection, dict):
        return [f"{unit_id}: native context projection missing"]
    if not isinstance(partition, dict):
        return [f"{unit_id}: route scope partition missing"]
    failures.extend(f"{unit_id}: {item}" for item in schema_failures(projection, CONTEXT_SCHEMA, "native context"))
    failures.extend(f"{unit_id}: {item}" for item in schema_failures(partition, PARTITION_SCHEMA, "route partition"))
    if failures:
        return failures

    contract = projection["execution_contract"]
    expected_fields = set(CONTEXT_FIELDS)
    version = projection["admission_schema_version"]
    if version == "1.3.0":
        expected_fields.add("transientOutputs")
    if set(contract) != expected_fields:
        failures.append(f"{unit_id}: execution contract field set is not exact")
    if projection["task_id"] != unit.get("task_id") or projection["swu_id"] != unit.get("unit_id"):
        failures.append(f"{unit_id}: native context identity mismatch")
    expected_contract = {
        "materialWrites": unit.get("material_writes", []),
        "executionOutputs": unit.get("executor_outputs", []),
        "allowedWrites": partition.get("executor_write_scopes", []),
        "validationCommands": [" ".join(item["argv"]) for item in unit.get("validation_contracts", [])],
        "lifecycleOwner": unit.get("lifecycle_owner"),
        "authorityClass": unit.get("authority_class"),
        "publicationClass": unit.get("publication_class"),
    }
    for field, expected in expected_contract.items():
        if contract.get(field) != expected:
            failures.append(f"{unit_id}: native context {field} mismatch")
    material = set(unit.get("material_writes", []))
    outputs = set(unit.get("executor_outputs", []))
    expected_profile = "material-bound" if material else "execution-output-only"
    if contract.get("writeProfile") != expected_profile:
        failures.append(f"{unit_id}: native context writeProfile mismatch")
    if version == "1.3.0":
        transients = set(contract.get("transientOutputs", []))
        if not transients or not transients <= outputs:
            failures.append(f"{unit_id}: v1.3 transientOutputs must be a nonempty subset of executionOutputs")
    elif "transientOutputs" in contract:
        failures.append(f"{unit_id}: v1.2 transientOutputs must be omitted")

    executor = set(partition["executor_write_scopes"])
    lifecycle = {item["path"] for item in partition["lifecycle_owner_scopes"]}
    terminal = {partition["terminal_receipt_scope"]}
    control_partition = partition.get("control_evidence_partition")
    control: set[str] = set()
    if control_partition is not None:
        try:
            validate_live_control_partition(
                control_partition,
                repository_root=Path.cwd(),
                attempt_id=control_partition.get("attempt_id", ""),
                forbidden_scopes=sorted(
                    executor
                    | lifecycle
                    | terminal
                    | set(contract.get("transientOutputs", []))
                ),
                revalidate_runtime=False,
            )
            control = set(control_partition["exact_union_scope"])
        except (OSError, ValueError) as error:
            failures.append(f"{unit_id}: {error}")
    exact = set(partition["exact_union_scope"])
    axes = (executor, lifecycle, terminal, control)
    if any(left & right for index, left in enumerate(axes) for right in axes[index + 1 :]):
        failures.append(f"{unit_id}: route scope axes overlap")
    if executor | lifecycle | terminal | control != exact:
        failures.append(f"{unit_id}: route exact union mismatch")
    if exact != set(unit.get("route_write_scope", [])):
        failures.append(f"{unit_id}: route write scope differs from partition")
    if executor != set(contract.get("allowedWrites", [])):
        failures.append(f"{unit_id}: admission writes differ from executor partition")
    if lifecycle & set(contract.get("allowedWrites", [])):
        failures.append(f"{unit_id}: lifecycle owner scope entered admission writes")
    if not set(unit.get("material_delta_classes", [])) <= set(closure.get("material_delta_classes", [])):
        failures.append(f"{unit_id}: material delta class is outside the material axis")
    if set(unit.get("lifecycle_closeout_delta_classes", [])) != set(closure.get("lifecycle_closeout_delta_classes", [])):
        failures.append(f"{unit_id}: lifecycle delta class mismatch")
    if set(unit.get("material_delta_classes", [])) & set(unit.get("lifecycle_closeout_delta_classes", [])):
        failures.append(f"{unit_id}: material and lifecycle delta axes overlap")
    if unit.get("owner_receipt_schema_identity") is None:
        failures.append(f"{unit_id}: owner receipt schema identity missing")
    return failures


def validate_document(document: dict[str, Any]) -> dict[str, Any]:
    closure = document.get("execution_entry_closure")
    units = document.get("units")
    failures: list[str] = []
    if not isinstance(closure, dict) or closure.get("schema_version") != "execution-entry-closure.v1":
        failures.append("versioned execution-entry closure missing")
        closure = {}
    if not isinstance(units, list) or not units:
        failures.append("closed unit frontier missing")
        units = []
    rehearsal = closure.get("consumer_rehearsal", {})
    if rehearsal.get("stages") != REHEARSAL_STAGES:
        failures.append("consumer rehearsal stage closure mismatch")
    if rehearsal.get("required_runs") != 2 or rehearsal.get("effect") != "deterministic-no-effect":
        failures.append("consumer rehearsal must be two-run and no-effect")
    if rehearsal.get("fixture_only_substitution") != "forbidden":
        failures.append("fixture-only consumer substitution is not forbidden")
    for unit in units:
        if not isinstance(unit, dict):
            failures.append("unit frontier contains a non-object")
            continue
        failures.extend(validate_unit(unit, closure))
    unit_ids = [item.get("unit_id") for item in units if isinstance(item, dict)]
    if len(unit_ids) != len(set(unit_ids)):
        failures.append("unit frontier contains duplicate unit identities")
    if rehearsal.get("exact_finalized_unit") not in unit_ids:
        failures.append("finalized rehearsal unit is outside the frontier")
    owner_identities = {item.get("lifecycle_owner") for item in units if isinstance(item, dict)}
    receipt_identities = {item.get("owner_receipt_schema_identity") for item in units if isinstance(item, dict)}
    if not owner_identities or any(
        not isinstance(identity, str) or not identity.strip()
        for identity in owner_identities
    ):
        failures.append("lifecycle owner frontier is incomplete")
    if not receipt_identities or any(
        not isinstance(identity, str) or not identity.strip()
        for identity in receipt_identities
    ):
        failures.append("owner receipt schema identity frontier is incomplete")
    semantic = closure.get("semantic_acceptance_binding", {})
    eligibility_blockers = []
    eligibility = semantic.get("eligibility_receipt")
    owner_acceptance = semantic.get("owner_acceptance_receipt")
    if semantic.get("required") is not True or eligibility is None:
        eligibility_blockers.append("REQUEST_EMISSION_ELIGIBILITY_BINDING_MISSING")
    elif not is_exact_ref(eligibility):
        eligibility_blockers.append("REQUEST_EMISSION_ELIGIBILITY_BINDING_MALFORMED")
    owner_acceptance_status = "pending" if owner_acceptance is None else "present"
    result = {
        "schema_version": "task-session.execution-entry-projection-validation.v1",
        "closure_result": "pass" if not failures else "block",
        "request_eligibility_result": "pass" if not eligibility_blockers else "block",
        "owner_acceptance_status": owner_acceptance_status,
        "selection_admission_authority": "absent",
        "unit_count": len(units),
        "owner_identities": sorted(str(item) for item in owner_identities),
        "owner_receipt_schema_identities": sorted(str(item) for item in receipt_identities),
        "failures": sorted(set(failures)),
        "request_eligibility_blockers": eligibility_blockers,
        "authority_effect": "none",
    }
    result["validation_digest"] = canonical_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--output")
    parser.add_argument("--require-request-eligibility", action="store_true")
    args = parser.parse_args()
    result = validate_document(load_object(Path(args.source)))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if result["closure_result"] != "pass":
        return 1
    return 1 if args.require_request_eligibility and result["request_eligibility_result"] != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
