#!/usr/bin/env python3
"""Resolve Invoke capability ceilings without collapsing evidence axes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class CapabilityStatusError(ValueError):
    pass


INVOKE_ROOT = Path(__file__).resolve().parent.parent
if str(INVOKE_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(INVOKE_ROOT / "scripts"))

from design_stage_contract_v2 import (  # noqa: E402
    validate_admission_receipt as validate_design_admission_contract,
    validate_stage_receipt as validate_design_stage_contract,
)
from define_stage_contract import (  # noqa: E402
    ADMISSION_CHECK_IDS as DEFINE_ADMISSION_CHECK_IDS,
    validate_admission_receipt as validate_define_admission_contract,
    validate_stage_receipt as validate_define_stage_contract,
)

REPO_ROOT = INVOKE_ROOT.parents[2]


def canonical_digest(document: dict[str, Any], omitted: str) -> str:
    projection = {key: value for key, value in document.items() if key != omitted}
    return hashlib.sha256(
        json.dumps(
            projection,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def canonical_value_digest(value: Any) -> str:
    return hashlib.sha256(
        (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
    ).hexdigest()
def validate_design_producer_receipt(receipt: Any) -> list[str]:
    return validate_design_stage_contract(
        receipt,
        REPO_ROOT,
        INVOKE_ROOT / "schemas",
    )


def validate_design_admission_receipt(receipt: Any, producer: Any) -> list[str]:
    return validate_design_admission_contract(
        receipt,
        producer,
        REPO_ROOT,
        INVOKE_ROOT / "schemas",
    )


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(document: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} schema invalid at {'/'.join(map(str, error.path)) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def axis(status: Any, evidence: list[str], diagnostics: list[str]) -> dict[str, Any]:
    return {
        "status": status,
        "evidence": evidence,
        "diagnostics": sorted(set(diagnostics)),
    }


def _valid_material_receipt(
    receipt: dict[str, Any] | None,
    material_schema: dict[str, Any],
) -> tuple[bool, list[str]]:
    if receipt is None:
        return False, ["material-package receipt missing"]
    diagnostics = schema_errors(receipt, material_schema, "material-package receipt")
    if diagnostics:
        return False, diagnostics
    requirements = {
        "patchVerdict": "pass",
        "mutationHandoff": "ready",
        "dependencyResult": "pass",
        "ownerBoundaryResult": "pass",
        "publicationBoundaryResult": "pass",
    }
    for field, expected in requirements.items():
        if receipt.get(field) != expected:
            diagnostics.append(f"material-package receipt {field} is not {expected}")
    if receipt.get("reasons"):
        diagnostics.append("material-package receipt contains rejection reasons")
    if not receipt.get("validatedPaths"):
        diagnostics.append("material-package receipt has no validated paths")
    if not receipt.get("validationCommands"):
        diagnostics.append("material-package receipt has no validation commands")
    return not diagnostics, diagnostics


def resolve_capability_status(
    request: dict[str, Any],
    capabilities: dict[str, Any],
    capability_sha256: str,
    request_schema: dict[str, Any],
    result_schema: dict[str, Any],
    material_schema: dict[str, Any],
) -> dict[str, Any]:
    request_failures = schema_errors(request, request_schema, "capability request")
    if request_failures:
        raise CapabilityStatusError("; ".join(request_failures))
    if capabilities.get("schema_version") != "1.0.0":
        raise CapabilityStatusError("mode capability schema version must be 1.0.0")
    expected_axes = {
        "artifact_authored",
        "registry_released",
        "mutation_runtime_ready",
    }
    if set(capabilities.get("status_axes", {})) != expected_axes:
        raise CapabilityStatusError("mode capability table must declare exactly three status axes")

    mode = request["mode"]
    rules = capabilities.get("modes", {}).get(mode)
    if not isinstance(rules, dict):
        raise CapabilityStatusError(f"unknown Invoke mode: {mode}")
    deferred = rules.get("implementation_status") == "deferred"

    artifact_receipt = request.get("artifact_receipt")
    artifact_diagnostics: list[str] = []
    artifact_evidence: list[str] = []
    if deferred:
        artifact_status = "unsupported"
        artifact_diagnostics.append(f"Invoke mode {mode} is deferred")
        if artifact_receipt is not None:
            artifact_diagnostics.append("artifact receipt cannot enable a deferred mode")
    elif artifact_receipt is None:
        artifact_status = "block"
        artifact_diagnostics.append("artifact receipt missing")
    elif artifact_receipt["mode"] != mode:
        artifact_status = "block"
        artifact_diagnostics.append("artifact receipt mode mismatch")
    elif mode == "define" and artifact_receipt["status"] == "pass":
        producer_receipt = artifact_receipt.get("producer_receipt")
        artifact_diagnostics.extend(
            validate_define_stage_contract(
                producer_receipt,
                REPO_ROOT,
                INVOKE_ROOT / "schemas",
            )
        )
        artifact_diagnostics.extend(
            validate_define_admission_contract(
                artifact_receipt.get("producer_admission_receipt"),
                producer_receipt,
                REPO_ROOT,
                INVOKE_ROOT / "schemas",
            )
        )
        if artifact_diagnostics:
            artifact_status = "block"
            artifact_diagnostics.append(
                "historical or generic Define artifact receipts cannot establish a new PASS"
            )
        else:
            artifact_status = "pass"
            artifact_evidence = [
                artifact_receipt["receipt_id"],
                artifact_receipt["producer_receipt"]["receipt_id"],
                artifact_receipt["producer_admission_receipt"]["receipt_id"],
            ]
    elif mode == "design" and artifact_receipt["status"] == "pass":
        producer_receipt = artifact_receipt.get("producer_receipt")
        artifact_diagnostics.extend(validate_design_producer_receipt(producer_receipt))
        artifact_diagnostics.extend(
            validate_design_admission_receipt(
                artifact_receipt.get("producer_admission_receipt"), producer_receipt
            )
        )
        if artifact_diagnostics:
            artifact_status = "block"
            artifact_diagnostics.append(
                "historical or generic Design artifact receipts cannot establish a new PASS"
            )
        else:
            artifact_status = "pass"
            artifact_evidence = [
                artifact_receipt["receipt_id"],
                artifact_receipt["producer_receipt"]["receipt_id"],
                artifact_receipt["producer_admission_receipt"]["receipt_id"],
            ]
    else:
        artifact_status = artifact_receipt["status"]
        artifact_evidence = [artifact_receipt["receipt_id"]]

    registry_receipt = request.get("registry_receipt")
    registry_diagnostics: list[str] = []
    registry_evidence: list[str] = []
    registry_status = False
    if deferred:
        registry_diagnostics.append(f"Invoke mode {mode} is deferred")
        if registry_receipt is not None:
            registry_diagnostics.append("registry receipt cannot release a deferred mode")
    elif registry_receipt is None:
        registry_diagnostics.append("registry owner receipt missing")
    else:
        if registry_receipt["mode"] != mode:
            registry_diagnostics.append("registry receipt mode mismatch")
        if registry_receipt["capability_sha256"] != capability_sha256:
            registry_diagnostics.append("registry receipt capability digest mismatch")
        if not registry_diagnostics:
            registry_status = True
            registry_evidence = [registry_receipt["receipt_id"]]

    material_receipt = request.get("material_package_receipt")
    runtime_receipt = request.get("runtime_receipt")
    runtime_diagnostics: list[str] = []
    runtime_evidence: list[str] = []
    runtime_status = False
    if deferred or rules.get("mutation_handoff_allowed") == "never":
        runtime_diagnostics.append(f"Invoke mode {mode} is not mutation-runtime-capable")
        if material_receipt is not None or runtime_receipt is not None:
            runtime_diagnostics.append("runtime evidence cannot enable a deferred mode")
    else:
        material_valid, material_diagnostics = _valid_material_receipt(
            material_receipt, material_schema
        )
        runtime_diagnostics.extend(material_diagnostics)
        if runtime_receipt is None:
            runtime_diagnostics.append("mode runtime receipt missing")
        else:
            if runtime_receipt["mode"] != mode:
                runtime_diagnostics.append("mode runtime receipt mode mismatch")
            if runtime_receipt["capability_sha256"] != capability_sha256:
                runtime_diagnostics.append("mode runtime receipt capability digest mismatch")
            if material_valid and material_receipt is not None:
                if runtime_receipt["material_package_id"] != material_receipt["packageId"]:
                    runtime_diagnostics.append("runtime/material package ID mismatch")
                if runtime_receipt["material_package_digest"] != material_receipt["packageDigest"]:
                    runtime_diagnostics.append("runtime/material package digest mismatch")
            required_gates = set(rules.get("runtime_required_gates", []))
            received_gates: dict[str, dict[str, Any]] = {}
            for gate in runtime_receipt["gates"]:
                if gate["gate"] in received_gates:
                    runtime_diagnostics.append(f"duplicate runtime gate: {gate['gate']}")
                received_gates[gate["gate"]] = gate
            if set(received_gates) != required_gates:
                runtime_diagnostics.append(
                    "mode runtime gates mismatch: "
                    f"expected {sorted(required_gates)}, got {sorted(received_gates)}"
                )
            for gate_name, gate in received_gates.items():
                if gate["status"] != "pass":
                    runtime_diagnostics.append(f"mode runtime gate blocked: {gate_name}")
        if material_valid and runtime_receipt is not None and not runtime_diagnostics:
            runtime_status = True
            runtime_evidence = [
                f"material-package:{material_receipt['packageId']}",
                runtime_receipt["receipt_id"],
            ]

    output = {
        "schema_version": "invoke.capability-status.result.v1",
        "mode": mode,
        "capability_sha256": capability_sha256,
        "artifact_authored": axis(
            artifact_status, artifact_evidence, artifact_diagnostics
        ),
        "registry_released": axis(
            registry_status, registry_evidence, registry_diagnostics
        ),
        "mutation_runtime_ready": axis(
            runtime_status, runtime_evidence, runtime_diagnostics
        ),
    }
    output_failures = schema_errors(output, result_schema, "capability result")
    if output_failures:
        raise CapabilityStatusError("; ".join(output_failures))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--capabilities", required=True)
    parser.add_argument("--request-schema", required=True)
    parser.add_argument("--result-schema", required=True)
    parser.add_argument("--material-receipt-schema", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    capability_path = Path(args.capabilities)
    try:
        output = resolve_capability_status(
            load_json(Path(args.request)),
            load_json(capability_path),
            file_sha256(capability_path),
            load_json(Path(args.request_schema)),
            load_json(Path(args.result_schema)),
            load_json(Path(args.material_receipt_schema)),
        )
    except (OSError, json.JSONDecodeError, CapabilityStatusError) as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return 2

    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
