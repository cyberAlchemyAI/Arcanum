#!/usr/bin/env python3
"""Control one approved finite frontier without executing Task Session itself."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import runpy
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


SCRIPT_ROOT = Path(__file__).resolve().parent
SPELL_ROOT = SCRIPT_ROOT.parent
CONFIG_SCHEMA = SPELL_ROOT / "schemas" / "chain-config.schema.json"
TRANSITION_SCHEMA = SPELL_ROOT / "schemas" / "chain-transition.schema.json"
NO_OP_SCHEMA = SPELL_ROOT / "schemas" / "closeout-no-op-proof.schema.json"
RUNTIME_PATHS = runpy.run_path(
    str(SCRIPT_ROOT / "task_session_until_blocker_runtime_paths.py"),
    run_name="task_session_until_blocker_runtime_paths_for_chain",
)
capability_root = RUNTIME_PATHS["capability_root"]
WPRA_ROOT = capability_root("work-pack-readiness-audit", "spells")
TASK_SESSION_ROOT = capability_root("task-session", "arcana")
WPRA_SCHEMA_ROOT = WPRA_ROOT / "schemas"
WPRA_SELECTION_REQUEST_SCHEMA = WPRA_SCHEMA_ROOT / "selection-request.schema.json"
WPRA_SELECTION_RECEIPT_SCHEMA = WPRA_SCHEMA_ROOT / "selection-receipt.schema.json"
TASK_SESSION_SCHEMA_ROOT = TASK_SESSION_ROOT / "schemas"
MUTATION_REQUEST_SCHEMA = (
    TASK_SESSION_SCHEMA_ROOT / "mutation-admission-request.schema.json"
)
MUTATION_RECEIPT_SCHEMA = (
    TASK_SESSION_SCHEMA_ROOT / "mutation-admission-receipt.schema.json"
)
MUTATION_VERIFIER = (
    TASK_SESSION_ROOT / "scripts" / "verify-mutation-readiness.py"
)
RISK_ORDER = {
    "read-only": 0,
    "bounded-write": 1,
    "browser": 2,
    "network": 3,
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {path}")
    return document


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def schema_errors(document: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    return [
        f"{label} invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def resolve_inside(root: Path, raw_path: str, must_exist: bool) -> Path:
    if (
        not raw_path
        or "\x00" in raw_path
        or "$" in raw_path
        or "*" in raw_path
        or "?" in raw_path
        or "\\" in raw_path
    ):
        raise ValueError(f"unsafe path: {raw_path}")
    path = PurePosixPath(raw_path)
    if path.is_absolute() or PureWindowsPath(raw_path).is_absolute() or ".." in path.parts:
        raise ValueError(f"path escapes repository: {raw_path}")
    root = root.resolve()
    try:
        candidate = (root / str(path)).resolve(strict=must_exist)
    except FileNotFoundError as error:
        raise ValueError(f"missing path: {raw_path}") from error
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"symlink or path escape: {raw_path}") from error
    return candidate


def verify_exact_ref(root: Path, reference: dict[str, Any]) -> Path:
    path = resolve_inside(root, reference["path"], must_exist=True)
    if not path.is_file():
        raise ValueError(f"exact artifact is not a file: {reference['path']}")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError(f"digest mismatch: {reference['path']}")
    if len(content) != reference["size_bytes"]:
        raise ValueError(f"size mismatch: {reference['path']}")
    return path


def block(code: str, claim: str, *, next_route: str | None = None) -> dict[str, Any]:
    return {
        "status": "BLOCK",
        "terminal_code": code,
        "claim": claim,
        "next_task_session_selector": None,
        "next_route": next_route,
        "authority_effect": "none",
    }


def json_clone(value: Any) -> Any:
    return json.loads(json.dumps(value))


def load_exact_document(root: Path, reference: dict[str, Any]) -> dict[str, Any]:
    return load_json(verify_exact_ref(root, reference))


def is_exact_ref(value: Any) -> bool:
    path = value.get("path") if isinstance(value, dict) else None
    sha256 = value.get("sha256") if isinstance(value, dict) else None
    size = value.get("size_bytes") if isinstance(value, dict) else None
    return (
        isinstance(value, dict)
        and set(value) == {"path", "sha256", "size_bytes"}
        and isinstance(path, str)
        and bool(path)
        and not any(marker in path for marker in ("\x00", "$", "*", "?", "\\"))
        and not PurePosixPath(path).is_absolute()
        and not PureWindowsPath(path).is_absolute()
        and ".." not in PurePosixPath(path).parts
        and isinstance(sha256, str)
        and re.fullmatch(r"[0-9a-f]{64}", sha256) is not None
        and isinstance(size, int)
        and not isinstance(size, bool)
        and size >= 0
    )


def is_camel_exact_ref(value: Any) -> bool:
    path = value.get("path") if isinstance(value, dict) else None
    sha256 = value.get("sha256") if isinstance(value, dict) else None
    size = value.get("sizeBytes") if isinstance(value, dict) else None
    return (
        isinstance(value, dict)
        and set(value) >= {"path", "sha256", "sizeBytes"}
        and isinstance(path, str)
        and bool(path)
        and not any(marker in path for marker in ("\x00", "$", "*", "?", "\\"))
        and not PurePosixPath(path).is_absolute()
        and not PureWindowsPath(path).is_absolute()
        and ".." not in PurePosixPath(path).parts
        and isinstance(sha256, str)
        and re.fullmatch(r"[0-9a-f]{64}", sha256) is not None
        and isinstance(size, int)
        and not isinstance(size, bool)
        and size >= 0
    )


def snake_ref(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": value["path"],
        "sha256": value["sha256"],
        "size_bytes": value["sizeBytes"],
    }


def wpra_selection_errors(
    request: dict[str, Any],
    receipt: dict[str, Any],
    *,
    manifest_ref: dict[str, Any],
    audit_config_path: str,
    manifest: dict[str, Any],
    binding: dict[str, Any],
    repository_root: Path | None = None,
) -> list[str]:
    errors = schema_errors(
        request, WPRA_SELECTION_REQUEST_SCHEMA, "selection request"
    ) + schema_errors(receipt, WPRA_SELECTION_RECEIPT_SCHEMA, "selection receipt")
    explicit = request.get("explicitConfirmation")
    execution_intent = request.get("executionIntentBinding")
    lifecycle = request.get("lifecycleEligibility")
    dependencies = request.get("dependencyReceipts")
    if request.get("manifestRef") != manifest_ref:
        errors.append("selection request does not bind the exact manifest")
    if request.get("auditConfigPath") != audit_config_path:
        errors.append("selection request does not name the exact audit config")
    if (
        request.get("taskId") != binding.get("task_id")
        or request.get("swuId") != binding.get("swu_id")
    ):
        errors.append("selection request task or SWU differs from the unit binding")
    if not isinstance(lifecycle, dict) or lifecycle.get("eligible") is not True:
        errors.append("selection request is not lifecycle eligible")
    if not isinstance(dependencies, list):
        errors.append("selection request dependency receipts are not a list")
        dependencies = []
    dependency_refs = [
        item.get("artifactRef") for item in dependencies if isinstance(item, dict)
    ]
    if len(dependency_refs) != len(dependencies) or any(
        not is_exact_ref(item) for item in dependency_refs
    ):
        errors.append("selection request has a non-exact dependency receipt")
    lifecycle_refs = lifecycle.get("evidenceRefs", []) if isinstance(lifecycle, dict) else []
    if not isinstance(lifecycle_refs, list) or any(
        not is_exact_ref(item) for item in lifecycle_refs
    ):
        errors.append("selection request has non-exact lifecycle evidence")
        lifecycle_refs = []
    if repository_root is not None:
        for label, reference in (
            [("dependency receipt", item) for item in dependency_refs]
            + [("lifecycle evidence", item) for item in lifecycle_refs]
        ):
            if not is_exact_ref(reference):
                continue
            try:
                verify_exact_ref(repository_root, reference)
            except (OSError, ValueError) as error:
                errors.append(f"{label}: {error}")

    if isinstance(explicit, dict):
        intent_source = "explicit-confirmation"
        intent_digest = digest(explicit)
    elif isinstance(execution_intent, dict):
        intent_source = "execution-intent-binding"
        intent_digest = digest(execution_intent)
    else:
        intent_source = "invalid"
        intent_digest = None

    expected = {
        "selectionVerdict": "select",
        "terminalCode": "SELECTION_READY",
        "planEpochId": manifest.get("plan_epoch_id"),
        "canonicalSemanticDigest": manifest.get("canonical_semantic_digest"),
        "manifestDigest": manifest_ref.get("sha256"),
        "unitContractDigest": manifest.get("unit_contract_digests", {}).get(
            binding.get("unit_id")
        ),
        "taskId": binding.get("task_id"),
        "swuId": binding.get("swu_id"),
        "selectionIntentSource": intent_source,
        "authorityEffect": "none",
        "mutationReady": False,
        "requestDigest": digest(request),
        "explicitConfirmationDigest": (
            digest(explicit) if isinstance(explicit, dict) else None
        ),
        "lifecycleEligibilityDigest": digest(lifecycle) if isinstance(lifecycle, dict) else None,
    }
    expected["selectionIntentDigest"] = intent_digest
    for field, value in expected.items():
        if receipt.get(field) != value:
            errors.append(f"selection receipt field differs: {field}")
    dependency_digests = [
        item["sha256"] for item in dependency_refs if is_exact_ref(item)
    ]
    if receipt.get("dependencyReceiptDigests") != dependency_digests:
        errors.append("selection receipt dependency digests differ")
    if receipt.get("reasons") != []:
        errors.append("selected receipt contains reasons")
    return errors


def chain_config_approval_projection(config: dict[str, Any]) -> dict[str, Any]:
    """Return the non-circular config surface an epoch owner approves."""
    approved_epoch = json_clone(config["approved_epoch"])
    approved_epoch.pop("decision_gate_approval_receipt_ref", None)
    keys = (
        "schema_version",
        "chain_id",
        "scope_id",
        "manifest_ref",
        "audit_report_ref",
        "wpra_v2",
        "finite_frontier",
        "run_budget",
        "risk_ceiling",
        "allowed_task_session_flags",
        "persistence",
        "compensation",
        "admission_window",
    )
    projection = {
        key: json_clone(config[key]) for key in keys if key in config
    }
    projection["approved_epoch"] = approved_epoch
    return projection


def wpra_approval_errors(
    approval: dict[str, Any],
    config: dict[str, Any],
) -> list[str]:
    approved = config["approved_epoch"]
    wpra = config["wpra_v2"]
    expected = {
        "schema_version": "task-session-until-blocker.epoch-approval/v1",
        "approval_status": "approved",
        "approval_owner_ref": approved["approval_owner_ref"],
        "plan_epoch_id": approved["epoch_id"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": approved["canonical_semantic_digest"],
        "source_snapshot_digest": approved["source_snapshot_digest"],
        "manifest_ref": config["manifest_ref"],
        "audit_config_ref": wpra["audit_config_ref"],
        "execution_contracts_ref": wpra["execution_contracts_ref"],
        "authority_effect": "chain-selection-only",
    }
    if "admission_window" in config:
        expected.update(
            admission_window=config["admission_window"],
            finite_frontier=config["finite_frontier"],
            run_budget=config["run_budget"],
            risk_ceiling=config["risk_ceiling"],
            chain_config_projection_digest=digest(
                chain_config_approval_projection(config)
            ),
        )
    return [
        f"epoch approval field differs: {field}"
        for field, value in expected.items()
        if approval.get(field) != value
    ]


def projected_validation_contracts(items: Any) -> Any:
    if not isinstance(items, list):
        return items
    keys = {"command_id", "argv", "cwd", "timeout_seconds", "max_output_bytes"}
    return [{key: item[key] for key in keys if key in item} for item in items]


def normalize_dependency_ids(
    values: Any, swu_to_unit: dict[str, str]
) -> list[str] | None:
    if not isinstance(values, list):
        return None
    return [swu_to_unit.get(value, value) for value in values]


def safe_relative_path(value: Any, *, suffix: str | None = None) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or any(marker in value for marker in ("\x00", "$", "*", "?", "\\"))
        or PurePosixPath(value).is_absolute()
        or PureWindowsPath(value).is_absolute()
        or ".." in PurePosixPath(value).parts
    ):
        return False
    return suffix is None or value.endswith(suffix)


def ascii_fold(value: Any) -> str | None:
    if not isinstance(value, str) or not value or not value.isascii():
        return None
    return value.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))


def valid_selected_unit_task_target(target: Any, unit_id: str) -> bool:
    """Validate one safe relative Markdown selector bound to one frontier unit."""
    if not isinstance(target, str) or target.count("#") != 1:
        return False
    base, fragment = target.split("#", 1)
    folded_fragment = ascii_fold(fragment)
    folded_unit = ascii_fold(unit_id)
    return (
        safe_relative_path(base, suffix=".md")
        and folded_fragment is not None
        and folded_fragment == folded_unit
    )


def validate_bound_schema(
    root: Path, reference: Any, label: str
) -> dict[str, Any]:
    if not is_exact_ref(reference):
        raise ValueError(f"{label} is not an exact schema reference")
    schema = load_json(verify_exact_ref(root, reference))
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise ValueError(f"{label} is not a valid JSON Schema: {error}") from error
    return schema


def bind_wpra_documents(
    manifest: dict[str, Any],
    config: dict[str, Any],
    documents: dict[str, dict[str, Any]],
    task_routes: dict[str, dict[str, Any]],
    closeout_routes: dict[str, dict[str, Any]],
    repository_root: Path,
    admitted_frontier: list[str] | None = None,
) -> dict[str, Any]:
    audit_config = documents["audit_config"]
    contracts_document = documents["execution_contracts"]
    nested_contracts = contracts_document.get("execution_contracts")
    if nested_contracts is not None and not isinstance(nested_contracts, dict):
        raise ValueError("WPRA nested execution contracts are not an object")
    nested_profile = isinstance(nested_contracts, dict)
    contracts = nested_contracts if nested_profile else contracts_document
    contract_selector_prefix = "/execution_contracts" if nested_profile else ""
    handoff = documents["selection_handoff"]
    frontier = manifest["ready_frontier"]
    admitted = frontier if admitted_frontier is None else admitted_frontier
    if audit_config.get("schema_version") != "2.0.0":
        raise ValueError("WPRA audit config is not v2")
    if (
        audit_config.get("admission_timing") != "selected-unit-at-task-session"
        or contracts.get("admission_timing") != "selected-unit-at-task-session"
    ):
        raise ValueError("WPRA admission timing is not selected-unit-at-task-session")
    if (
        contracts.get("authority_effect") != "none"
        or contracts.get("mutation_ready") is not False
    ):
        raise ValueError("WPRA execution contracts exceed planning authority")
    if audit_config.get("execution_policy", {}).get("allowed_routes") != manifest.get(
        "allowed_routes"
    ) or contracts.get("execution_policy", {}).get("allowed_routes") != manifest.get(
        "allowed_routes"
    ):
        raise ValueError("WPRA route policy differs across frozen artifacts")
    work_pack_target = audit_config.get("execution_policy", {}).get("work_pack_id")
    if not work_pack_target or (closeout_routes and any(
        route.get("target") != work_pack_target for route in closeout_routes.values()
    )):
        raise ValueError("WPRA closeout target differs from the work pack")
    if (
        handoff.get("plan_epoch_id") != manifest.get("plan_epoch_id")
        or handoff.get("ready_frontier") != frontier
        or handoff.get("allowed_routes_digest") != manifest.get("allowed_routes_digest")
        or handoff.get("authority_effect") != "none"
        or handoff.get("mutation_ready") is not False
        or handoff.get("selection_required") is not True
    ):
        raise ValueError("WPRA selection handoff differs from the manifest")

    execution_bindings = audit_config.get("execution_bindings")
    contract_units = contracts.get("units")
    closeout_bindings = audit_config.get("closeout_bindings")
    if not all(isinstance(value, list) for value in (
        execution_bindings, contract_units, closeout_bindings
    )):
        raise ValueError("WPRA unit bindings are not arrays")
    if not (
        len(execution_bindings) == len(contract_units) == len(closeout_bindings) == len(frontier)
    ):
        raise ValueError("WPRA unit binding counts differ from the frontier")
    if set(manifest.get("unit_contract_digests", {})) != set(frontier):
        raise ValueError("WPRA unit contract digest coverage differs from the frontier")
    if any(
        not isinstance(value, str) or len(value) != 64
        for value in manifest["unit_contract_digests"].values()
    ):
        raise ValueError("WPRA unit contract digest is malformed")

    contract_by_unit = {item.get("unit_id"): item for item in contract_units}
    binding_by_unit = {item.get("unit_id"): item for item in execution_bindings}
    closeout_by_unit = {item.get("unit_id"): item for item in closeout_bindings}
    if (
        set(contract_by_unit) != set(frontier)
        or set(binding_by_unit) != set(frontier)
        or set(closeout_by_unit) != set(frontier)
    ):
        raise ValueError("WPRA unit IDs do not cover the frontier exactly")
    swu_to_unit = {
        item.get("swu_id"): item.get("unit_id") for item in contract_units
    }
    normalized_bindings: list[dict[str, Any]] = []
    all_normalized_bindings: list[dict[str, Any]] = []
    contracts_ref = config["wpra_v2"]["execution_contracts_ref"]
    for index, unit_id in enumerate(frontier):
        binding = binding_by_unit[unit_id]
        contract = contract_by_unit[unit_id]
        closeout = closeout_by_unit[unit_id]
        comparisons = {
            "task_id": contract.get("task_id"),
            "swu_id": contract.get("swu_id"),
            "lifecycle_owner": contract.get("lifecycle_owner"),
            "authority_class": contract.get("authority_class"),
            "publication_class": contract.get("publication_class"),
            "attempt_contract": contract.get("attempt_contract"),
            "material_writes": contract.get("material_writes"),
            "execution_outputs": contract.get("execution_outputs"),
            "allowed_writes": contract.get("allowed_writes"),
        }
        if any(binding.get(field) != value for field, value in comparisons.items()):
            raise ValueError(f"WPRA unit projection differs for {unit_id}")
        contract_command = dict(contract.get("command", {}))
        contract_command.pop("contract_type", None)
        if binding.get("command") != contract_command:
            raise ValueError(f"WPRA command differs for {unit_id}")
        if projected_validation_contracts(contract.get("validation_contracts")) != binding.get(
            "validation_contracts"
        ):
            raise ValueError(f"WPRA validation contracts differ for {unit_id}")
        if not isinstance(binding.get("material_package"), dict) or not isinstance(
            binding.get("byte_baselines"), list
        ):
            raise ValueError(f"WPRA material or baseline binding is absent for {unit_id}")
        gate_contract = contract.get("gate_contract")
        if (
            not isinstance(gate_contract, dict)
            or not isinstance(gate_contract.get("selection_requires"), list)
            or not isinstance(gate_contract.get("execution_requires"), list)
            or not gate_contract.get("on_unsatisfied")
            or not gate_contract.get("completion_rule")
        ):
            raise ValueError(f"WPRA gate contract is incomplete for {unit_id}")
        terminal_policy = contract.get("terminal_write_policy")
        if (
            not isinstance(terminal_policy, dict)
            or terminal_policy.get("create_mode") != "exclusive-create"
            or terminal_policy.get("first_terminal") != "preserve-never-overwrite"
            or terminal_policy.get("successor_execution") is not False
        ):
            raise ValueError(f"WPRA terminal policy is incomplete for {unit_id}")
        if normalize_dependency_ids(contract.get("dependencies"), swu_to_unit) != binding.get(
            "dependencies"
        ):
            raise ValueError(f"WPRA dependencies differ for {unit_id}")
        successor = contract.get("canonical_successor")
        expected_successors = (
            [swu_to_unit.get(successor, successor)] if successor is not None else None
        )
        observed_successors = binding.get("canonical_successors")
        terminal_successor = successor is None and observed_successors in (
            [], ["__complete__"], ["__window_complete__"]
        )
        if not terminal_successor and observed_successors != expected_successors:
            raise ValueError(f"WPRA successor differs for {unit_id}")
        task_route = task_routes.get(unit_id)
        if unit_id in admitted:
            if task_route is None:
                raise ValueError(f"WPRA Task Session route is absent for {unit_id}")
            if task_route.get("write_scope") != binding.get("allowed_writes"):
                raise ValueError(f"WPRA Task Session write scope differs for {unit_id}")
            if task_route.get("expected_receipt") != contract.get(
                "receipt_contract", {}
            ).get("path"):
                raise ValueError(f"WPRA terminal route differs for {unit_id}")
        elif task_route is not None:
            raise ValueError(f"WPRA Task Session route exceeds the admission window: {unit_id}")
        receipt_contract = contract.get("receipt_contract", {})
        closeout_contract = contract.get("closeout_contract", {})
        if nested_profile:
            if receipt_contract.get("receipt_profile") != "precloseout-execution-v1":
                raise ValueError(f"WPRA receipt profile differs for {unit_id}")
            schema_refs = {
                "precloseout execution schema": receipt_contract.get(
                    "precloseout_execution_schema_ref"
                ),
                "final terminal schema": receipt_contract.get(
                    "final_terminal_schema_ref"
                ),
                "closeout owner schema": closeout_contract.get(
                    "expected_owner_receipt_schema_ref"
                ),
                "continuation state schema": closeout_contract.get(
                    "continuation_state_schema_ref"
                ),
                "Continuation Router schema": closeout_contract.get(
                    "continuation_router_schema_ref"
                ),
            }
            for label, schema_ref in schema_refs.items():
                validate_bound_schema(
                    repository_root, schema_ref, f"{unit_id} {label}"
                )
            required_paths = {
                "terminal path": receipt_contract.get("path"),
                "precloseout path": receipt_contract.get(
                    "precloseout_execution_receipt_path"
                ),
                "target inventory path": closeout_contract.get(
                    "target_inventory_path"
                ),
                "owner receipt path": closeout_contract.get(
                    "expected_owner_receipt"
                ),
                "continuation state path": closeout_contract.get(
                    "continuation_state_path"
                ),
                "Router receipt path": closeout_contract.get(
                    "continuation_router_verification_receipt"
                ),
            }
            if any(
                not safe_relative_path(path)
                for path in required_paths.values()
            ):
                missing = ", ".join(
                    label
                    for label, path in required_paths.items()
                    if not safe_relative_path(path)
                )
                raise ValueError(
                    f"WPRA closeout paths are absent or unsafe for {unit_id}: {missing}"
                )
            target_inventory = closeout_contract.get("target_inventory")
            allowed_deltas = closeout_contract.get("allowed_delta_classes")
            validation_commands = closeout_contract.get("validation_commands")
            if (
                not isinstance(target_inventory, list)
                or not target_inventory
                or len(target_inventory) != len(set(target_inventory))
                or any(not safe_relative_path(path) for path in target_inventory)
                or closeout_contract.get("continuation_state_path")
                not in target_inventory
            ):
                raise ValueError(f"WPRA closeout inventory is incomplete for {unit_id}")
            if (
                not isinstance(allowed_deltas, list)
                or not allowed_deltas
                or len(allowed_deltas) != len(set(allowed_deltas))
                or any(not isinstance(value, str) or not value for value in allowed_deltas)
            ):
                raise ValueError(f"WPRA closeout delta policy is incomplete for {unit_id}")
            if not isinstance(validation_commands, list) or not validation_commands:
                raise ValueError(f"WPRA closeout validation is incomplete for {unit_id}")
            if (
                closeout_contract.get("route") != "invoke:refresh:apply-approved"
                or closeout_contract.get("continuation_policy")
                != "emit-cursor-never-execute-successor"
            ):
                raise ValueError(f"WPRA closeout lifecycle differs for {unit_id}")
            closeout_route = closeout_routes.get(unit_id) or {
                "route_id": f"audit-bound-closeout-{unit_id}",
                "frontier_swu": unit_id,
                "capability": "invoke",
                "mode": "refresh",
                "target": work_pack_target,
                "write_scope": json_clone(target_inventory),
                "effect_class": "repository-local-reversible",
                "required_inputs": [
                    receipt_contract["precloseout_execution_receipt_path"]
                ],
                "expected_receipt": closeout_contract["expected_owner_receipt"],
            }
        else:
            closeout_route = closeout_routes.get(unit_id)
        if unit_id in admitted:
            if closeout_route is None:
                raise ValueError(f"WPRA closeout route is absent for {unit_id}")
            if closeout_route.get("write_scope") != closeout_contract.get(
                "target_inventory"
            ):
                raise ValueError(f"WPRA closeout inventory differs for {unit_id}")
            if closeout_route.get("expected_receipt") != closeout_contract.get(
                "expected_owner_receipt"
            ):
                raise ValueError(f"WPRA closeout receipt differs for {unit_id}")
        owner_ref = closeout.get("owner_receipt_contract_ref", {})
        if (
            owner_ref.get("artifact_ref") != contracts_ref
            or owner_ref.get("selector")
            != f"{contract_selector_prefix}/units/{index}/closeout_contract"
        ):
            raise ValueError(f"WPRA closeout contract ref differs for {unit_id}")
        if nested_profile:
            delta_ref = closeout.get("allowed_delta_policy_ref", {})
            if (
                delta_ref.get("artifact_ref") != contracts_ref
                or delta_ref.get("selector")
                != (
                    f"{contract_selector_prefix}/units/{index}/"
                    "closeout_contract/allowed_delta_classes"
                )
            ):
                raise ValueError(f"WPRA allowed delta ref differs for {unit_id}")
        normalized = json_clone(binding)
        normalized.update(
            unit_contract_digest=manifest["unit_contract_digests"][unit_id],
            contract_projection=(
                "nested-selected-unit-precloseout-v1"
                if nested_profile
                else "flat-inline-closeout-v1"
            ),
            task_route=json_clone(task_route),
            closeout_route=json_clone(closeout_route),
            gate_contract=json_clone(contract.get("gate_contract", {})),
            terminal_modes=json_clone(contract.get("terminal_modes", [])),
            terminal_write_policy=json_clone(contract.get("terminal_write_policy", {})),
            receipt_contract=json_clone(contract.get("receipt_contract", {})),
            closeout_contract=json_clone(contract.get("closeout_contract", {})),
        )
        all_normalized_bindings.append(normalized)
        if unit_id in admitted:
            normalized_bindings.append(normalized)

    normalized = dict(manifest)
    normalized["epoch_binding"] = {
        "epoch_id": manifest["plan_epoch_id"],
        "audit_projection_digest": config["approved_epoch"]["audit_projection_digest"],
        "canonical_semantic_digest": manifest["canonical_semantic_digest"],
        "source_snapshot_digest": manifest["source_snapshot_digest"],
    }
    normalized["canonical_plan_graph"] = {"finite_frontier": admitted}
    normalized["execution_bindings"] = normalized_bindings
    normalized["all_execution_bindings"] = all_normalized_bindings
    normalized["closeout_bindings"] = [
        json_clone(closeout_by_unit[unit_id]) for unit_id in admitted
    ]
    normalized["wpra_v2_bound"] = True
    normalized["wpra_initial_selection"] = admitted[0]
    if admitted != frontier:
        normalized["fresh_epoch_boundary"] = True
        normalized["fresh_epoch_ready_frontier"] = json_clone(frontier)
        normalized["fresh_epoch_successor"] = (
            frontier[1] if len(frontier) > 1 else None
        )
    return normalized


def normalize_plan_semantic_manifest(
    manifest: dict[str, Any],
    config: dict[str, Any],
    audit_report: dict[str, Any] | None,
    wpra_documents: dict[str, dict[str, Any]] | None = None,
    repository_root: Path | None = None,
) -> dict[str, Any]:
    """Adapt a WPRA v2 manifest without weakening its frozen bindings."""
    if "epoch_binding" in manifest:
        return manifest

    required = {
        "manifest_id",
        "plan_epoch_id",
        "canonical_semantic_digest",
        "source_snapshot_digest",
        "ready_frontier",
        "completion_continuity",
        "allowed_routes",
        "allowed_routes_digest",
    }
    missing = sorted(name for name in required if name not in manifest)
    if missing:
        raise ValueError(f"WPRA v2 manifest missing: {', '.join(missing)}")
    if audit_report is None:
        raise ValueError("WPRA v2 manifest requires an exact audit report reference")

    approved = config["approved_epoch"]
    report_snapshot = audit_report.get("source_snapshot")
    report_checks = {
        "verdict": config["audit_verdict"],
        "flags": config["audit_flags"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": approved["canonical_semantic_digest"],
    }
    mismatches = [
        name for name, expected in report_checks.items()
        if audit_report.get(name) != expected
    ]
    if (
        not isinstance(report_snapshot, dict)
        or report_snapshot.get("digest") != approved["source_snapshot_digest"]
    ):
        mismatches.append("source_snapshot_digest")
    if audit_report.get("manifest") != manifest:
        mismatches.append("manifest")
    if mismatches:
        raise ValueError(
            "WPRA v2 audit report differs from approved epoch: "
            + ", ".join(mismatches)
        )
    if manifest["manifest_id"] != f"psm-{approved['audit_projection_digest'][:24]}":
        raise ValueError("WPRA v2 manifest id does not bind the audit projection")

    frontier = manifest["ready_frontier"]
    if (
        not isinstance(frontier, list)
        or not frontier
        or any(not isinstance(unit, str) or not unit for unit in frontier)
        or len(frontier) != len(set(frontier))
    ):
        raise ValueError("WPRA v2 ready frontier is not a unique non-empty sequence")
    continuity = manifest["completion_continuity"]
    if not isinstance(continuity, dict) or (
        continuity.get("plan_epoch_id") != manifest["plan_epoch_id"]
        or continuity.get("work_pack_semantic_digest")
        != manifest["canonical_semantic_digest"]
        or continuity.get("next_unit") != frontier[0]
        or continuity.get("authority_effect") != "none"
    ):
        raise ValueError("WPRA v2 continuity binding is invalid")
    if digest(manifest["allowed_routes"]) != manifest["allowed_routes_digest"]:
        raise ValueError("WPRA v2 allowed routes digest mismatch")

    admission_window = config.get("admission_window")
    admitted_frontier = frontier
    if admission_window is not None:
        selected = admission_window.get("selected_unit")
        if (
            admission_window.get("mode") != "fresh-current-unit"
            or selected != frontier[0]
            or config.get("finite_frontier") != [selected]
            or config.get("run_budget", {}).get("max_task_session_requests") != 1
        ):
            raise ValueError("fresh epoch window is not bound to the current unit")
        if admission_window.get("observed_ready_frontier_digest") != digest(frontier):
            raise ValueError("fresh epoch window ready-frontier digest differs")
        admitted_frontier = [selected]

    def valid_task_target(target: Any, unit_id: str) -> bool:
        """Accept a legacy unit selector or one strict ``base#unit`` selector."""
        if target == unit_id:
            return True
        if not isinstance(target, str):
            return False
        base, marker, fragment = target.partition("#")
        return (
            target.count("#") == 1
            and bool(base)
            and marker == "#"
            and fragment == unit_id
        )

    current_v2 = isinstance(config.get("wpra_v2"), dict)
    if current_v2 and ("wpra_v2" not in config or wpra_documents is None):
        raise ValueError("current WPRA v2 routes require exact config and contract bindings")
    if current_v2:
        if repository_root is None:
            raise ValueError("current WPRA v2 requires a repository root")
        audit_config = wpra_documents.get("audit_config", {})
        contracts_document = wpra_documents.get("execution_contracts", {})
        contracts_projection = contracts_document.get(
            "execution_contracts", contracts_document
        )
        if (
            audit_config.get("admission_timing")
            != "selected-unit-at-task-session"
            or not isinstance(contracts_projection, dict)
            or contracts_projection.get("admission_timing")
            != "selected-unit-at-task-session"
        ):
            raise ValueError(
                "config.wpra_v2 is not bound to selected-unit admission"
            )

    task_routes: dict[str, dict[str, Any]] = {}
    closeout_routes: dict[str, dict[str, Any]] = {}
    for route in manifest["allowed_routes"]:
        if not isinstance(route, dict):
            raise ValueError("WPRA v2 allowed route is not an object")
        unit_id = route.get("frontier_swu")
        if unit_id not in frontier:
            raise ValueError("WPRA v2 allowed route is outside the ready frontier")
        if route.get("effect_class") != "repository-local-reversible":
            raise ValueError("WPRA v2 allowed route has an unsafe effect class")
        if route.get("capability") == "task-session":
            legacy_task = not current_v2 and route.get(
                "mode"
            ) == "execute" and valid_task_target(
                route.get("target"), unit_id
            )
            current_task = (
                current_v2
                and (
                    (
                        route.get("mode") == "execute-one-swu"
                        and safe_relative_path(route.get("target"), suffix=".md")
                    )
                    or (
                        route.get("mode") == "execute"
                        and valid_selected_unit_task_target(
                            route.get("target"), unit_id
                        )
                    )
                )
            )
            if (not legacy_task and not current_task) or unit_id in task_routes:
                raise ValueError("WPRA v2 Task Session route is ambiguous or invalid")
            task_routes[unit_id] = route
        elif route.get("capability") == "invoke":
            legacy_closeout = (
                route.get("mode") == "refresh-apply-approved"
                and route.get("target") == f"{unit_id}-closeout"
            )
            current_closeout = (
                route.get("mode") == "refresh"
                and isinstance(route.get("target"), str)
                and bool(route["target"])
            )
            if (not legacy_closeout and not current_closeout) or unit_id in closeout_routes:
                raise ValueError("WPRA v2 closeout route is ambiguous or invalid")
            closeout_routes[unit_id] = route
        else:
            raise ValueError("WPRA v2 allowed route has an unsupported capability")
    if set(task_routes) != set(admitted_frontier):
        raise ValueError("WPRA v2 Task Session routes do not cover the admitted frontier exactly")
    # WPRA v2 binds Task Session routes in the frozen manifest. Its closeout
    # contract is owned by the audited configuration, not necessarily emitted
    # as a second inline route. If a future projection does include inline
    # closeout routes, they must still cover the same frontier exactly.
    if closeout_routes and set(closeout_routes) != set(admitted_frontier):
        raise ValueError("WPRA v2 closeout routes do not cover the admitted frontier exactly")
    if current_v2:
        if closeout_routes and set(closeout_routes) != set(admitted_frontier):
            raise ValueError("current WPRA v2 closeout routes do not cover the admitted frontier")
        assert wpra_documents is not None
        return bind_wpra_documents(
            manifest,
            config,
            wpra_documents,
            task_routes,
            closeout_routes,
            repository_root,
            admitted_frontier,
        )

    normalized = dict(manifest)
    normalized["epoch_binding"] = {
        "epoch_id": manifest["plan_epoch_id"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": manifest["canonical_semantic_digest"],
        "source_snapshot_digest": manifest["source_snapshot_digest"],
    }
    normalized["canonical_plan_graph"] = {"finite_frontier": frontier}
    normalized["execution_bindings"] = [
        {
            "unit_id": unit_id,
            # WPRA v2 permits only repository-local reversible Task Session routes.
            "command": {"risk_class": "bounded-write"},
        }
        for unit_id in frontier
    ]
    # V2 does not carry a static exact closeout-contract digest. PASS closeouts
    # remain supported through owner/router joins; NO_OP continues to block
    # unless a future v2 manifest adds an exact closeout-contract binding.
    normalized["closeout_bindings"] = []
    return normalized


def preflight(
    config: dict[str, Any], repository_root: Path
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        manifest_path = verify_exact_ref(repository_root, config["manifest_ref"])
        approval = load_exact_document(
            repository_root,
            config["approved_epoch"]["decision_gate_approval_receipt_ref"],
        )
        manifest = load_json(manifest_path)
        audit_report = None
        if "audit_report_ref" in config:
            audit_report = load_json(
                verify_exact_ref(repository_root, config["audit_report_ref"])
            )
        wpra_documents = None
        if "wpra_v2" in config:
            wpra_documents = {
                name.removesuffix("_ref"): load_exact_document(
                    repository_root, reference
                )
                for name, reference in config["wpra_v2"].items()
            }
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return None, block("FROZEN_INPUT_MISMATCH", str(error))
    try:
        manifest = normalize_plan_semantic_manifest(
            manifest, config, audit_report, wpra_documents, repository_root
        )
    except ValueError as error:
        return None, block("MANIFEST_SHAPE_INVALID", str(error))

    if manifest.get("wpra_v2_bound"):
        assert wpra_documents is not None
        approval_errors = wpra_approval_errors(approval, config)
        if approval_errors:
            return None, block("EPOCH_APPROVAL_INVALID", "; ".join(approval_errors))
        first_binding = manifest["execution_bindings"][0]
        selection_errors = wpra_selection_errors(
            wpra_documents["initial_selection_request"],
            wpra_documents["initial_selection_receipt"],
            manifest_ref=config["manifest_ref"],
            audit_config_path=config["wpra_v2"]["audit_config_ref"]["path"],
            manifest=manifest,
            binding=first_binding,
            repository_root=repository_root,
        )
        if selection_errors:
            return None, block(
                "SELECTION_EVIDENCE_INVALID", "; ".join(selection_errors)
            )

    if (
        manifest.get("authority_effect") != "none"
        or manifest.get("mutation_ready") is not False
        or manifest.get("selected_unit") is not None
    ):
        return None, block(
            "MANIFEST_AUTHORITY_INVALID",
            "manifest must remain no-authority, non-mutation-ready, and unselected",
        )
    if config["audit_verdict"] not in {"pass", "flag"}:
        return None, block("AUDIT_VERDICT_NOT_ALLOWED", "audit verdict is not consumable")
    if any(flag != "observability-residue" for flag in config["audit_flags"]):
        return None, block("FLAG_CLASS_NOT_ALLOWED", "audit flag class is not allowed")
    if config["audit_verdict"] == "flag" and not config["audit_flags"]:
        return None, block("FLAG_CLASS_MISSING", "flag verdict has no named flag class")

    approved = config["approved_epoch"]
    epoch = manifest.get("epoch_binding", {})
    comparisons = {
        "epoch_id": approved["epoch_id"],
        "audit_projection_digest": approved["audit_projection_digest"],
        "canonical_semantic_digest": approved["canonical_semantic_digest"],
        "source_snapshot_digest": approved["source_snapshot_digest"],
    }
    mismatches = [
        name for name, expected in comparisons.items() if epoch.get(name) != expected
    ]
    if mismatches:
        return None, block(
            "EPOCH_BINDING_MISMATCH",
            f"approved epoch differs from manifest: {', '.join(mismatches)}",
        )
    if approved["approval_status"] != "approved":
        return None, block("EPOCH_APPROVAL_MISSING", "epoch approval is absent")

    manifest_frontier = (
        manifest.get("canonical_plan_graph", {}).get("finite_frontier")
    )
    if manifest_frontier != config["finite_frontier"]:
        return None, block(
            "FRONTIER_MISMATCH",
            "configured frontier differs from the audited manifest frontier",
        )
    budget = config["run_budget"]["max_task_session_requests"]
    if budget > len(config["finite_frontier"]):
        return None, block(
            "BUDGET_INVALID",
            "request budget exceeds the finite audited frontier",
        )
    ceiling = RISK_ORDER[config["risk_ceiling"]]
    for unit in manifest.get("execution_bindings", []):
        risk = unit.get("command", {}).get("risk_class")
        if risk not in RISK_ORDER or RISK_ORDER[risk] > ceiling:
            return None, block(
                "RISK_CEILING_EXCEEDED",
                f"unit {unit.get('unit_id')} exceeds the approved risk ceiling",
            )
    return manifest, {
        "status": "PASS",
        "terminal_code": "CHAIN_PREFLIGHT_READY",
        "claim": "approved finite epoch is consumable",
        "next_task_session_selector": config["finite_frontier"][0],
        "next_route": "task-session",
        "authority_effect": "none",
    }


def initial_state(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "chain_id": config["chain_id"],
        "epoch_id": config["approved_epoch"]["epoch_id"],
        "manifest_digest": config["approved_epoch"]["audit_projection_digest"],
        "frontier": config["finite_frontier"],
        "visited": [],
        "cursors": [],
        "request_count": 0,
        "last_transition_digest": None,
        "last_selector": None,
        "status": "ACTIVE",
        "next_selector": config["finite_frontier"][0],
        "stop_code": None,
        "authority_effect": "none",
    }


def admit_next_request(
    config: dict[str, Any], manifest: dict[str, Any], state: dict[str, Any]
) -> dict[str, Any]:
    if state["status"] == "COMPLETE":
        if state.get("stop_code") == "FRESH_EPOCH_REQUIRED":
            return {
                "status": "COMPLETE",
                "terminal_code": "FRESH_EPOCH_REQUIRED",
                "claim": "the approved current-unit epoch is closed",
                "next_task_session_selector": None,
                "next_fresh_epoch_unit": manifest.get("fresh_epoch_successor"),
                "next_route": "work-pack-readiness-audit",
                "authority_effect": "none",
            }
        return {
            "status": "COMPLETE",
            "terminal_code": "CHAIN_COMPLETE",
            "claim": "every approved-frontier unit has a joined closeout",
            "next_task_session_selector": None,
            "next_route": None,
            "authority_effect": "none",
        }
    if state["status"] == "BLOCK":
        return block("CHAIN_ALREADY_BLOCKED", "chain is already terminal")
    if state["epoch_id"] != config["approved_epoch"]["epoch_id"]:
        return block("EPOCH_BINDING_MISMATCH", "state epoch differs from approval")
    if state["frontier"] != config["finite_frontier"]:
        return block("FRONTIER_DRIFT", "persisted frontier differs from approval")
    if state["request_count"] >= config["run_budget"]["max_task_session_requests"]:
        return block("BUDGET_EXHAUSTED", "approved request budget is exhausted")
    selector = state["next_selector"]
    if selector is None or selector in state["visited"]:
        return block("SELECTOR_INVALID", "no novel approved selector is available")
    bound = next(
        (
            unit
            for unit in manifest["execution_bindings"]
            if unit["unit_id"] == selector
        ),
        None,
    )
    if bound is None:
        return block("SELECTOR_OUTSIDE_MANIFEST", "selector is absent from manifest")
    if RISK_ORDER[bound["command"]["risk_class"]] > RISK_ORDER[config["risk_ceiling"]]:
        return block("RISK_CEILING_EXCEEDED", "selector exceeds approved risk")
    return {
        "status": "READY",
        "terminal_code": "NEXT_SELECTOR_READY",
        "claim": "exactly one approved Task Session request is legal",
        "next_task_session_selector": selector,
        "request_ordinal": state["request_count"] + 1,
        "next_route": "task-session",
        "authority_effect": "none",
    }


def value_at(document: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in document:
            return document[name]
    return None


def binding_for(manifest: dict[str, Any], unit_id: str) -> dict[str, Any] | None:
    return next(
        (
            item
            for item in manifest.get(
                "all_execution_bindings", manifest.get("execution_bindings", [])
            )
            if item.get("unit_id") == unit_id
        ),
        None,
    )


def bound_schema_errors(
    root: Path,
    document: dict[str, Any],
    schema_ref: Any,
    label: str,
) -> list[str]:
    try:
        schema = validate_bound_schema(root, schema_ref, f"{label} schema")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]
    return [
        f"{label} invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def projected_closeout_receipt_errors(
    root: Path,
    terminal: dict[str, Any],
    terminal_ref: dict[str, Any],
    owner: dict[str, Any],
    owner_ref: dict[str, Any],
    router_ref: Any,
    current: dict[str, Any],
    successor: dict[str, Any] | None,
) -> list[str]:
    """Join the selected-unit precloseout lifecycle from its frozen schemas."""
    errors: list[str] = []
    receipt = current.get("receipt_contract", {})
    closeout = current.get("closeout_contract", {})
    errors.extend(
        bound_schema_errors(
            root,
            terminal,
            receipt.get("final_terminal_schema_ref"),
            "final terminal receipt",
        )
    )
    errors.extend(
        bound_schema_errors(
            root,
            owner,
            closeout.get("expected_owner_receipt_schema_ref"),
            "closeout owner receipt",
        )
    )
    for field, expected in {
        "task_id": current.get("task_id"),
        "swu_id": current.get("swu_id"),
        "receipt_profile": "precloseout-execution-v1",
    }.items():
        if terminal.get(field) != expected:
            errors.append(f"final terminal receipt field differs: {field}")
    if terminal.get("result") not in {"pass", "flag"}:
        errors.append("final terminal receipt is not passing or flagged")

    precloseout_ref = terminal.get("precloseout_execution_receipt_ref")
    if (
        not is_exact_ref(precloseout_ref)
        or precloseout_ref.get("path")
        != receipt.get("precloseout_execution_receipt_path")
    ):
        errors.append("final terminal receipt does not bind the precloseout receipt")
        precloseout = None
    else:
        try:
            precloseout = load_exact_document(root, precloseout_ref)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            precloseout = None
    if terminal.get("precloseout_execution_schema_ref") != receipt.get(
        "precloseout_execution_schema_ref"
    ):
        errors.append("final terminal receipt binds a different precloseout schema")
    if precloseout is not None:
        errors.extend(
            bound_schema_errors(
                root,
                precloseout,
                receipt.get("precloseout_execution_schema_ref"),
                "precloseout execution receipt",
            )
        )
        for field, expected in {
            "task_id": current.get("task_id"),
            "swu_id": current.get("swu_id"),
            "claim_state": "execution-validated-closeout-pending",
            "result": "pass",
        }.items():
            if precloseout.get(field) != expected:
                errors.append(f"precloseout receipt field differs: {field}")
        projected = precloseout.get("closeout_contract", {})
        expected_projected = {
            "route": closeout.get("route"),
            "owner_capability": "invoke",
            "source_receipt_path": receipt.get(
                "precloseout_execution_receipt_path"
            ),
            "source_schema_ref": receipt.get(
                "precloseout_execution_schema_ref"
            ),
            "expected_owner_receipt_path": closeout.get(
                "expected_owner_receipt"
            ),
            "expected_owner_receipt_schema_ref": closeout.get(
                "expected_owner_receipt_schema_ref"
            ),
            "final_terminal_receipt_path": receipt.get("path"),
            "final_terminal_schema_ref": receipt.get(
                "final_terminal_schema_ref"
            ),
            "allowed_delta_classes": closeout.get("allowed_delta_classes"),
            "continuation_policy": closeout.get("continuation_policy"),
        }
        for field, expected in expected_projected.items():
            if projected.get(field) != expected:
                errors.append(f"precloseout closeout contract differs: {field}")
        target_inventory_ref = projected.get("target_inventory_ref")
        if (
            not is_exact_ref(target_inventory_ref)
            or target_inventory_ref.get("path")
            != closeout.get("target_inventory_path")
        ):
            errors.append("precloseout target inventory differs from the contract")
        else:
            try:
                verify_exact_ref(root, target_inventory_ref)
            except (OSError, ValueError) as error:
                errors.append(str(error))

    owner_expected = {
        "work_pack_id": current.get("closeout_route", {}).get("target"),
        "task_id": current.get("task_id"),
        "swu_id": current.get("swu_id"),
        "authority_effect": "none",
    }
    for field, expected in owner_expected.items():
        if owner.get(field) != expected:
            errors.append(f"closeout owner receipt field differs: {field}")
    if owner.get("result") not in {"pass", "no-op"}:
        errors.append("closeout owner receipt is not passing")
    if owner.get("precloseout_source_ref") != precloseout_ref:
        errors.append("closeout owner does not bind the precloseout receipt")
    if owner.get("router_verification_receipt_ref") != router_ref:
        errors.append("closeout owner does not bind the Router receipt")
    final_owner_write = owner.get("final_owner_write", {})
    if (
        final_owner_write.get("path") != closeout.get("expected_owner_receipt")
        or final_owner_write.get("owner_capability") != "invoke"
        or final_owner_write.get("completed") is not True
    ):
        errors.append("closeout owner final write differs from the contract")
    owner_projection = dict(owner)
    observed_owner_digest = owner_projection.pop("receipt_digest", None)
    if observed_owner_digest != digest(owner_projection):
        errors.append("closeout owner receipt digest differs")

    continuation_ref = owner.get("continuation_state_ref")
    if (
        not is_exact_ref(continuation_ref)
        or continuation_ref.get("path") != closeout.get("continuation_state_path")
    ):
        errors.append("closeout owner does not bind the continuation state")
        continuation = None
    else:
        try:
            continuation = load_exact_document(root, continuation_ref)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            continuation = None
    if continuation is not None:
        errors.extend(
            bound_schema_errors(
                root,
                continuation,
                closeout.get("continuation_state_schema_ref"),
                "continuation state",
            )
        )
        expected_successor = successor.get("swu_id") if successor else None
        continuation_expected = {
            "work_pack_id": current.get("closeout_route", {}).get("target"),
            "completed_swu": current.get("swu_id"),
            "invoke_closeout_receipt_ref": owner_ref,
            "router_verification_receipt_ref": router_ref,
            "next_swu": expected_successor,
            "execution_started": False,
            "authority_effect": "none",
        }
        for field, expected in continuation_expected.items():
            if continuation.get(field) != expected:
                errors.append(f"continuation state field differs: {field}")

    if (
        not is_exact_ref(router_ref)
        or router_ref.get("path")
        != closeout.get("continuation_router_verification_receipt")
    ):
        errors.append("Router receipt does not match the closeout contract")
        router = None
    else:
        try:
            router = load_exact_document(root, router_ref)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            router = None
    if router is not None:
        errors.extend(
            bound_schema_errors(
                root,
                router,
                closeout.get("continuation_router_schema_ref"),
                "Continuation Router receipt",
            )
        )
        if continuation is not None and router.get(
            "returned_next_route"
        ) != continuation.get("next_owner"):
            errors.append("Router next route differs from the continuation state")

    closeout_join = terminal.get("closeout_join", {})
    if closeout_join.get("required_owner_capabilities") != ["invoke"]:
        errors.append("final terminal owner capability differs")
    joined = closeout_join.get("joined_owner_receipts", [])
    if not isinstance(joined, list) or not any(
        isinstance(item, dict)
        and item.get("owner_capability") == "invoke"
        and item.get("receipt_ref") == owner_ref
        and item.get("result") == owner.get("result")
        for item in joined
    ):
        errors.append("final terminal does not join the Invoke owner receipt")
    terminal_continuation = closeout_join.get("continuation", {})
    if (
        terminal_continuation.get("policy")
        != "emit-cursor-never-execute-successor"
        or terminal_continuation.get("cursor_ref") != continuation_ref
        or terminal_continuation.get("successor_executed") is not False
    ):
        errors.append("final terminal continuation join differs")
    return errors


def terminal_receipt_errors(
    root: Path,
    terminal: dict[str, Any],
    reference: dict[str, Any],
    current: dict[str, Any],
    successor: dict[str, Any] | None,
    manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    allowed = {
        "schema_version", "receipt_id", "work_pack_id", "unit_id", "swu_id",
        "task_id", "result", "terminal_mode", "validation", "evidence_refs",
        "dependency_dispositions", "blockers", "successor", "authority_effect",
        "mutation_ready",
    }
    if set(terminal) != allowed:
        errors.append("terminal receipt does not use the closed WPRA shape")
    work_pack_id = current.get("closeout_route", {}).get("target")
    expected = {
        "work_pack_id": work_pack_id,
        "unit_id": current.get("unit_id"),
        "swu_id": current.get("swu_id"),
        "task_id": current.get("task_id"),
        "result": "pass",
        "authority_effect": "none",
        "mutation_ready": False,
    }
    for field, value in expected.items():
        if terminal.get(field) != value:
            errors.append(f"terminal receipt field differs: {field}")
    if not isinstance(terminal.get("schema_version"), str) or not terminal.get(
        "receipt_id"
    ):
        errors.append("terminal receipt identity is absent")
    if terminal.get("terminal_mode") not in current.get("terminal_modes", []):
        errors.append("terminal receipt mode is outside the unit contract")
    expected_successor = successor.get("swu_id") if successor else None
    if terminal.get("successor") != {
        "unit_id": expected_successor,
        "execution_started": False,
    }:
        errors.append("terminal receipt successor differs from the unit contract")
    if terminal.get("blockers") != []:
        errors.append("passing terminal receipt contains blockers")

    validation = terminal.get("validation")
    commands = validation.get("command_results") if isinstance(validation, dict) else None
    if not isinstance(validation, dict) or validation.get("status") != "pass" or not isinstance(
        commands, list
    ):
        errors.append("terminal validation is not passing")
        commands = []
    expected_commands = {
        item.get("command_id") for item in current.get("validation_contracts", [])
    }
    if {item.get("command_id") for item in commands if isinstance(item, dict)} != expected_commands:
        errors.append("terminal validation command coverage differs")
    evidence = terminal.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence:
        errors.append("terminal receipt has no exact evidence")
        evidence = []
    for item in commands:
        if not isinstance(item, dict) or item.get("status") != "pass":
            errors.append("terminal command result is not passing")
            continue
        evidence.append(item.get("evidence_ref"))
    for item in evidence:
        if not is_exact_ref(item):
            errors.append("terminal evidence reference is not exact")
            continue
        try:
            verify_exact_ref(root, item)
        except (OSError, ValueError) as error:
            errors.append(str(error))

    dispositions = terminal.get("dependency_dispositions")
    if not isinstance(dispositions, list):
        errors.append("terminal dependency dispositions are absent")
        dispositions = []
    expected_dependencies = {
        binding_for(manifest, unit_id).get("swu_id"): binding_for(
            manifest, unit_id
        )
        for unit_id in current.get("dependencies", [])
        if binding_for(manifest, unit_id) is not None
    }
    if {item.get("dependency_id") for item in dispositions if isinstance(item, dict)} != set(
        expected_dependencies
    ):
        errors.append("terminal dependency disposition coverage differs")
    for item in dispositions:
        if not isinstance(item, dict):
            errors.append("terminal dependency disposition is invalid")
            continue
        dependency = expected_dependencies.get(item.get("dependency_id"))
        dependency_ref = item.get("receipt_ref")
        if (
            dependency is None
            or not is_exact_ref(dependency_ref)
            or dependency_ref.get("path")
            != dependency.get("receipt_contract", {}).get("path")
        ):
            errors.append("terminal dependency disposition differs from the frozen route")
            continue
        try:
            verify_exact_ref(root, dependency_ref)
        except (OSError, ValueError) as error:
            errors.append(str(error))
    return errors


def closeout_owner_errors(
    owner: dict[str, Any],
    terminal_ref: dict[str, Any],
    current: dict[str, Any],
    successor: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    allowed = {
        "schema_version", "receipt_id", "work_pack_id", "unit_id", "swu_id",
        "terminal_receipt_ref", "result", "lifecycle_owner_validation",
        "target_inventory", "next_route", "blockers", "authority_effect",
        "successor_executed",
    }
    if set(owner) != allowed:
        errors.append("closeout owner receipt does not use the closed WPRA shape")
    contract = current.get("closeout_contract", {})
    expected_successor = successor.get("swu_id") if successor else None
    expected_route = {
        "unit_id": expected_successor,
        "capability": "task-session" if successor else None,
        "mode": "execute-one-swu" if successor else None,
    }
    expected = {
        "work_pack_id": current.get("closeout_route", {}).get("target"),
        "unit_id": current.get("unit_id"),
        "swu_id": current.get("swu_id"),
        "terminal_receipt_ref": terminal_ref,
        "result": "pass",
        "target_inventory": contract.get("target_inventory"),
        "next_route": expected_route,
        "blockers": [],
        "authority_effect": "none",
        "successor_executed": False,
    }
    for field, value in expected.items():
        if owner.get(field) != value:
            errors.append(f"closeout owner receipt field differs: {field}")
    if not isinstance(owner.get("schema_version"), str) or not owner.get("receipt_id"):
        errors.append("closeout owner receipt identity is absent")
    lifecycle = owner.get("lifecycle_owner_validation")
    if not isinstance(lifecycle, dict) or lifecycle.get("status") != "pass":
        errors.append("closeout lifecycle owner validation is not passing")
    else:
        if lifecycle.get("allowed_delta_policy") != contract.get("allowed_delta_policy"):
            errors.append("closeout allowed delta policy differs")
        if lifecycle.get("baseline_status") not in {"exact-absent", "exact-present"}:
            errors.append("closeout baseline status is invalid")
    return errors


def _camel_matches_snake(camel: Any, snake: dict[str, Any]) -> bool:
    return is_camel_exact_ref(camel) and snake_ref(camel) == snake


def mutation_admission_errors(
    root: Path,
    request: dict[str, Any],
    receipt: dict[str, Any],
    selection_ref: dict[str, Any],
    selection_dependencies: list[dict[str, Any]],
    config: dict[str, Any],
    manifest: dict[str, Any],
    successor: dict[str, Any],
) -> list[str]:
    errors = schema_errors(
        request, MUTATION_REQUEST_SCHEMA, "mutation admission request"
    ) + schema_errors(receipt, MUTATION_RECEIPT_SCHEMA, "mutation admission receipt")
    plan = (
        request.get("planAdmission")
        if isinstance(request.get("planAdmission"), dict)
        else {}
    )
    dependency_frontier = request.get("dependencyFrontier", [])
    expected_dependencies = [
        {
            "dependencyId": item.get("dependencyId"),
            "artifactRef": {
                "path": item["artifactRef"]["path"],
                "sha256": item["artifactRef"]["sha256"],
                "sizeBytes": item["artifactRef"]["size_bytes"],
            },
        }
        for item in selection_dependencies
        if isinstance(item, dict) and is_exact_ref(item.get("artifactRef"))
    ]
    if dependency_frontier != expected_dependencies:
        errors.append("mutation dependency frontier differs from selected evidence")
    if not _camel_matches_snake(plan.get("planManifest"), config["manifest_ref"]):
        errors.append("mutation request plan manifest differs")
    if not _camel_matches_snake(plan.get("selectionReceipt"), selection_ref):
        errors.append("mutation request selection receipt differs")
    expected_request = {
        "schemaVersion": "1.2.0",
        "admissionProfile": "plan-once-selected-unit",
        "taskId": successor.get("task_id"),
        "swuId": successor.get("swu_id"),
        "materialWrites": successor.get("material_writes"),
        "executionOutputs": successor.get("execution_outputs"),
        "allowedWrites": successor.get("allowed_writes"),
        "lifecycleOwner": successor.get("lifecycle_owner"),
        "authorityClass": successor.get("authority_class"),
        "publicationClass": successor.get("publication_class"),
    }
    for field, value in expected_request.items():
        if request.get(field) != value:
            errors.append(f"mutation request field differs: {field}")
    if request.get("executionMode") not in {"routed-mutation", "reusable-mutation"}:
        errors.append("mutation execution mode is not routed")
    task_target = successor.get("task_route", {}).get("target")
    accepted_control_targets = {task_target}
    if (
        successor.get("contract_projection")
        == "nested-selected-unit-precloseout-v1"
        and isinstance(task_target, str)
        and task_target.count("#") == 1
    ):
        accepted_control_targets.add(task_target.split("#", 1)[0])
    if not accepted_control_targets.intersection({
        item.get("path") for item in request.get("controlArtifacts", [])
        if isinstance(item, dict)
    }):
        errors.append("mutation controls omit the frozen Task Session target")

    validation_contracts = successor.get("validation_contracts")
    validation_digest = digest(validation_contracts)
    expected_plan = {
        "planEpochId": manifest.get("plan_epoch_id"),
        "unitContractDigest": successor.get("unit_contract_digest"),
        "structuredValidationContracts": validation_contracts,
        "validationContractDigest": validation_digest,
    }
    for field, value in expected_plan.items():
        if plan.get(field) != value:
            errors.append(f"mutation plan admission field differs: {field}")
    baselines = (
        plan.get("targetBaselines")
        if isinstance(plan.get("targetBaselines"), list)
        else []
    )
    expected_baseline_paths = set(
        successor.get("material_writes")
        if successor.get("material_writes")
        else successor.get("execution_outputs") or []
    )
    if {item.get("path") for item in baselines if isinstance(item, dict)} != expected_baseline_paths:
        errors.append("mutation target baseline inventory differs")
    try:
        verifier = runpy.run_path(
            str(MUTATION_VERIFIER), run_name="task_session_mutation_readiness"
        )
        resolved = verifier["resolve_mutation_admission"](
            request, root, load_json(MUTATION_REQUEST_SCHEMA)
        )
        if resolved != receipt:
            errors.append("mutation admission receipt differs from canonical resolution")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f"canonical mutation admission cannot be resolved: {error}")
    return errors


def wpra_successor_errors(
    config: dict[str, Any],
    manifest: dict[str, Any],
    transition: dict[str, Any],
    state: dict[str, Any],
    repository_root: Path | None,
    expected_selector: str,
    expected_successor: str | None,
) -> list[str]:
    errors: list[str] = []
    if repository_root is None:
        return ["repository root is required for WPRA evidence joins"]
    current = binding_for(manifest, expected_selector)
    if current is None:
        return ["current WPRA binding is absent"]
    terminal_ref = transition.get("terminal_receipt_ref")
    expected_terminal = current.get("receipt_contract", {}).get("path")
    if not is_exact_ref(terminal_ref) or terminal_ref.get("path") != expected_terminal:
        errors.append("terminal receipt does not match the exact unit contract")
        terminal = None
    else:
        try:
            terminal = load_exact_document(repository_root, terminal_ref)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            terminal = None
    successor = binding_for(manifest, expected_successor) if expected_successor else None
    projected_profile = (
        current.get("contract_projection")
        == "nested-selected-unit-precloseout-v1"
    )
    if terminal is not None and not projected_profile:
        errors.extend(
            terminal_receipt_errors(
                repository_root, terminal, terminal_ref, current, successor, manifest
            )
        )

    closeout = transition.get("closeout", {})
    owner_ref = closeout.get("owner_receipt_ref")
    expected_owner = current.get("closeout_contract", {}).get("expected_owner_receipt")
    if not is_exact_ref(owner_ref) or owner_ref.get("path") != expected_owner:
        errors.append("closeout owner receipt does not match the unit contract")
        owner = None
    else:
        try:
            owner = load_exact_document(repository_root, owner_ref)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            owner = None
    if expected_successor is not None and successor is None:
        errors.append("successor binding is absent")
        return errors
    router_ref = closeout.get("continuation_router_verification_receipt_ref")
    if terminal is not None and owner is not None and projected_profile:
        errors.extend(
            projected_closeout_receipt_errors(
                repository_root,
                terminal,
                terminal_ref,
                owner,
                owner_ref,
                router_ref,
                current,
                successor,
            )
        )
    elif owner is not None:
        errors.extend(closeout_owner_errors(owner, terminal_ref, current, successor))
    if not projected_profile:
        target_inventory = current.get("closeout_contract", {}).get("target_inventory", [])
        router_paths = [
            path for path in target_inventory
            if path != current.get("closeout_contract", {}).get("expected_owner_receipt")
        ]
        if (
            not is_exact_ref(router_ref)
            or len(router_paths) != 1
            or router_ref.get("path") != router_paths[0]
        ):
            errors.append("NEXT-ROUTE receipt does not match the frozen closeout inventory")
        else:
            try:
                router = load_exact_document(repository_root, router_ref)
                if owner is None or router != owner.get("next_route"):
                    errors.append("NEXT-ROUTE receipt differs from the accepted owner route")
            except (OSError, ValueError, json.JSONDecodeError) as error:
                errors.append(str(error))

    if expected_successor is None:
        return errors
    assert successor is not None
    satisfied = set(state.get("visited", [])) | {expected_selector}
    if not set(successor.get("dependencies", [])).issubset(satisfied):
        errors.append("successor dependencies are not joined")
    if manifest.get("fresh_epoch_boundary") is True:
        # The next unit is declared and dependency-checked here, but its
        # selection and mutation evidence must come from a new WPRA epoch.
        return errors
    evidence = transition.get("wpra_v2_evidence")
    if not isinstance(evidence, dict):
        errors.append("WPRA successor evidence is absent from the transition")
        return errors
    request_ref = evidence.get("selection_request_ref")
    receipt_ref = evidence.get("selection_receipt_ref")
    mutation_request_ref = evidence.get("mutation_admission_request_ref")
    mutation_ref = evidence.get("mutation_admission_receipt_ref")
    refs = (request_ref, receipt_ref, mutation_request_ref, mutation_ref)
    if not all(is_exact_ref(item) for item in refs):
        errors.append("successor admission refs are not exact")
        return errors
    required_inputs = successor.get("task_route", {}).get("required_inputs", [])
    if successor.get("contract_projection") != "nested-selected-unit-precloseout-v1":
        selection_paths = [path for path in required_inputs if path.endswith("/SELECTION-RECEIPT.json")]
        mutation_paths = [path for path in required_inputs if path.endswith("/MUTATION-ADMISSION-RECEIPT.json")]
        if (
            len(selection_paths) != 1
            or len(mutation_paths) != 1
            or receipt_ref["path"] != selection_paths[0]
            or mutation_ref["path"] != mutation_paths[0]
            or request_ref["path"]
            != str(PurePosixPath(selection_paths[0]).with_name("SELECTION-REQUEST.json"))
            or mutation_request_ref["path"]
            != str(PurePosixPath(mutation_paths[0]).with_name("MUTATION-ADMISSION-REQUEST.json"))
        ):
            errors.append("successor evidence paths differ from the frozen Task Session route")
            return errors
    try:
        request = load_exact_document(repository_root, request_ref)
        receipt = load_exact_document(repository_root, receipt_ref)
        mutation_request = load_exact_document(repository_root, mutation_request_ref)
        mutation = load_exact_document(repository_root, mutation_ref)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(str(error))
        return errors
    errors.extend(
        wpra_selection_errors(
            request,
            receipt,
            manifest_ref=config["manifest_ref"],
            audit_config_path=config["wpra_v2"]["audit_config_ref"]["path"],
            manifest=manifest,
            binding=successor,
            repository_root=repository_root,
        )
    )
    dependency_items = request.get("dependencyReceipts", [])
    dependency_by_id = {
        item.get("dependencyId"): item.get("artifactRef")
        for item in dependency_items if isinstance(item, dict)
    }
    expected_dependency_ids: set[str] = set()
    for unit_id in successor.get("dependencies", []):
        dependency = binding_for(manifest, unit_id)
        if dependency is None:
            errors.append(f"successor dependency binding is absent: {unit_id}")
            continue
        dependency_id = dependency.get("swu_id")
        dependency_path = (
            dependency.get("closeout_contract", {}).get("expected_owner_receipt")
            if successor.get("contract_projection")
            == "nested-selected-unit-precloseout-v1"
            else dependency.get("receipt_contract", {}).get("path")
        )
        expected_dependency_ids.add(dependency_id)
        if dependency_path not in required_inputs:
            errors.append(f"frozen Task Session route omits dependency: {dependency_id}")
        reference = dependency_by_id.get(dependency_id)
        if not is_exact_ref(reference) or reference.get("path") != dependency_path:
            errors.append(f"selection dependency differs: {dependency_id}")
    for gate in successor.get("gate_contract", {}).get("selection_requires", []):
        expected_dependency_ids.add(gate)
        reference = dependency_by_id.get(gate)
        if not is_exact_ref(reference):
            errors.append(f"successor selection gate is not evidenced: {gate}")
            continue
        gate_unit = gate.split("-", 1)[0]
        gated = binding_for(manifest, gate_unit)
        if gate.endswith("-closeout-pass"):
            expected_path = (
                gated.get("closeout_contract", {}).get("expected_owner_receipt")
                if gated else None
            )
            if reference.get("path") != expected_path:
                errors.append(f"closeout gate receipt differs: {gate}")
            else:
                try:
                    gate_receipt = load_exact_document(repository_root, reference)
                    if gate_receipt.get("result") != "pass" or gate_receipt.get(
                        "lifecycle_owner_validation", {}
                    ).get("status") != "pass":
                        errors.append(f"closeout gate is not passing: {gate}")
                except (OSError, ValueError, json.JSONDecodeError) as error:
                    errors.append(str(error))
    if set(dependency_by_id) != expected_dependency_ids:
        errors.append("selection dependency and gate inventory differs")
    errors.extend(
        mutation_admission_errors(
            repository_root,
            mutation_request,
            mutation,
            receipt_ref,
            dependency_items,
            config,
            manifest,
            successor,
        )
    )
    return errors


def _exact_inventory(items: list[dict[str, str]]) -> list[tuple[str, str]]:
    return sorted((item["path"], item["sha256"]) for item in items)


def validate_no_op(
    proof: Any,
    *,
    selector: str,
    expected_successor: str | None,
    manifest: dict[str, Any],
    verification_receipt: dict[str, Any] | None,
) -> list[str]:
    errors = schema_errors(proof, NO_OP_SCHEMA, "NO_OP proof")
    if errors:
        return errors
    assert isinstance(proof, dict)
    if proof["unit_id"] != selector:
        errors.append("NO_OP proof unit does not match selector")
    if _exact_inventory(proof["before_inventory"]) != _exact_inventory(
        proof["after_inventory"]
    ):
        errors.append("NO_OP before and after inventories differ")
    closeout = next(
        (
            item
            for item in manifest["closeout_bindings"]
            if item["unit_id"] == selector
        ),
        None,
    )
    expected_contract = (
        closeout.get("owner_receipt_contract_ref", {}).get("artifact_ref")
        if closeout
        else None
    )
    if proof["closeout_contract_ref"] != expected_contract:
        errors.append("NO_OP proof is not bound to the approved closeout contract")
    router = proof["continuation_router_verification"]
    if router["canonical_successor"] != expected_successor:
        errors.append("NO_OP proof successor differs from the finite frontier")
    if verification_receipt is None or router["receipt_ref"] != verification_receipt:
        errors.append("NO_OP proof does not join the supplied router verification")
    return errors


def evaluate_transition(
    config: dict[str, Any],
    manifest: dict[str, Any],
    transition: dict[str, Any],
    state: dict[str, Any],
    repository_root: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    next_state = json.loads(json.dumps(state))
    input_errors = schema_errors(transition, TRANSITION_SCHEMA, "transition")
    if input_errors:
        next_state.update(status="BLOCK", next_selector=None, stop_code="TRANSITION_INVALID")
        return block("TRANSITION_INVALID", "; ".join(input_errors)), next_state

    admission = admit_next_request(config, manifest, state)
    if admission["status"] != "READY":
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code=admission["terminal_code"],
        )
        return admission, next_state

    expected_selector = admission["next_task_session_selector"]
    expected_ordinal = admission["request_ordinal"]
    transition_payload = dict(transition)
    supplied_digest = transition_payload.pop("transition_digest")
    transition_digest = digest(transition_payload)
    next_state["request_count"] += 1
    next_state["last_transition_digest"] = transition_digest
    next_state["last_selector"] = transition["selector"]

    if supplied_digest is not None and supplied_digest != transition_digest:
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code="TRANSITION_DIGEST_MISMATCH",
        )
        return block(
            "TRANSITION_DIGEST_MISMATCH",
            "supplied transition digest is not canonical",
        ), next_state

    checks = (
        (
            transition["chain_id"] != config["chain_id"],
            "CHAIN_ID_MISMATCH",
            "transition chain id differs from configuration",
        ),
        (
            transition["epoch_id"] != state["epoch_id"],
            "EPOCH_BINDING_MISMATCH",
            "transition epoch differs from persisted state",
        ),
        (
            transition["previous_transition_digest"]
            != state["last_transition_digest"],
            "TRANSITION_LINK_MISMATCH",
            "transition does not hash-link to the current chain head",
        ),
        (
            transition["request_ordinal"] != expected_ordinal,
            "REQUEST_ORDINAL_MISMATCH",
            "transition request ordinal is not the next durable ordinal",
        ),
        (
            transition["selector"] != expected_selector,
            "SELECTOR_OUT_OF_ORDER",
            "transition selector is not the unique expected selector",
        ),
        (
            transition["cursor"] in state["cursors"],
            "CURSOR_REPEATED",
            "continuity cursor was already consumed",
        ),
        (
            transition["observed_frontier_digest"]
            != digest(config["finite_frontier"]),
            "FRONTIER_DRIFT",
            "transition observed a different finite frontier",
        ),
    )
    for failed, code, claim in checks:
        if failed:
            next_state.update(status="BLOCK", next_selector=None, stop_code=code)
            return block(code, claim), next_state

    bound = next(
        unit
        for unit in manifest["execution_bindings"]
        if unit["unit_id"] == expected_selector
    )
    if (
        transition["risk_class"] != bound["command"]["risk_class"]
        or RISK_ORDER[transition["risk_class"]] > RISK_ORDER[config["risk_ceiling"]]
    ):
        next_state.update(
            status="BLOCK",
            next_selector=None,
            stop_code="RISK_CEILING_EXCEEDED",
        )
        return block(
            "RISK_CEILING_EXCEEDED",
            "transition risk differs from or exceeds the approved binding",
        ), next_state

    next_state["cursors"].append(transition["cursor"])

    if transition["task_session_result"] == "FLAG":
        flags = transition["task_session_flags"]
        if not flags or any(
            flag not in config["allowed_task_session_flags"] for flag in flags
        ):
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="FLAG_CLASS_NOT_ALLOWED"
            )
            return block(
                "FLAG_CLASS_NOT_ALLOWED",
                "Task Session flag is absent or outside the approval allowlist",
            ), next_state
    elif transition["task_session_flags"]:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="FLAG_STATUS_MISMATCH"
        )
        return block(
            "FLAG_STATUS_MISMATCH",
            "Task Session flags are present without a FLAG result",
        ), next_state

    if transition["task_session_result"] == "BLOCK":
        compensation = config["compensation"]
        next_state.update(status="BLOCK", next_selector=None)
        if compensation["mode"] == "owner-routed":
            next_state["stop_code"] = "COMPENSATION_OWNER_ROUTE_REQUIRED"
            return block(
                "COMPENSATION_OWNER_ROUTE_REQUIRED",
                "chain stopped before compensation; the named owner must decide",
                next_route=compensation["owner_ref"],
            ), next_state
        next_state["stop_code"] = "TASK_SESSION_BLOCK"
        return block("TASK_SESSION_BLOCK", "Task Session returned BLOCK"), next_state

    closeout = transition["closeout"]
    current_index = len(state["visited"])
    expected_successor = (
        manifest.get("fresh_epoch_successor")
        if manifest.get("fresh_epoch_boundary") is True
        else (
            config["finite_frontier"][current_index + 1]
            if current_index + 1 < len(config["finite_frontier"])
            else None
        )
    )
    if closeout["result"] == "PASS":
        if (
            closeout["owner_receipt_ref"] is None
            or closeout["continuation_router_verification_receipt_ref"] is None
            or closeout["no_op_proof"] is not None
        ):
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="OWNER_JOIN_MISSING"
            )
            return block(
                "OWNER_JOIN_MISSING",
                "PASS closeout requires owner and router receipts only",
            ), next_state
    elif closeout["result"] == "NO_OP":
        errors = validate_no_op(
            closeout["no_op_proof"],
            selector=expected_selector,
            expected_successor=expected_successor,
            manifest=manifest,
            verification_receipt=closeout[
                "continuation_router_verification_receipt_ref"
            ],
        )
        if errors or closeout["owner_receipt_ref"] is not None:
            next_state.update(
                status="BLOCK", next_selector=None, stop_code="NO_OP_PROOF_INVALID"
            )
            return block("NO_OP_PROOF_INVALID", "; ".join(errors) or "owner receipt conflicts with NO_OP"), next_state
    else:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="CLOSEOUT_BLOCK"
        )
        return block("CLOSEOUT_BLOCK", "closeout returned BLOCK"), next_state

    successor = transition["successor"]
    if successor["scope_digest"] != config["approved_epoch"]["audit_projection_digest"]:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_SCOPE_MISMATCH"
        )
        return block(
            "SUCCESSOR_SCOPE_MISMATCH",
            "successor scope differs from the approved projection",
        ), next_state
    expected_count = 0 if expected_successor is None else 1
    if successor["candidate_count"] != expected_count:
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_NON_UNIQUE"
        )
        return block(
            "SUCCESSOR_NON_UNIQUE",
            "successor candidate count is not exact",
        ), next_state
    if manifest.get("wpra_v2_bound"):
        wpra_errors = wpra_successor_errors(
            config,
            manifest,
            transition,
            state,
            repository_root,
            expected_selector,
            expected_successor,
        )
        if wpra_errors:
            next_state.update(
                status="BLOCK",
                next_selector=None,
                stop_code="SUCCESSOR_ADMISSION_INVALID",
            )
            return block(
                "SUCCESSOR_ADMISSION_INVALID", "; ".join(wpra_errors)
            ), next_state
    if (
        successor["unit_id"] != expected_successor
        or successor["declared"] is not True
        or successor["dependency_ready"] is not True
    ):
        next_state.update(
            status="BLOCK", next_selector=None, stop_code="SUCCESSOR_INVALID"
        )
        return block(
            "SUCCESSOR_INVALID",
            "successor is missing, out of order, undeclared, or not dependency-ready",
        ), next_state

    next_state["visited"].append(expected_selector)
    fresh_epoch_required = (
        manifest.get("fresh_epoch_boundary") is True
        and expected_successor is not None
    )
    next_state["next_selector"] = None if fresh_epoch_required else expected_successor
    if fresh_epoch_required:
        next_state.update(status="COMPLETE", stop_code="FRESH_EPOCH_REQUIRED")
        status = "COMPLETE"
        code = "FRESH_EPOCH_REQUIRED"
        next_route = "work-pack-readiness-audit"
    elif expected_successor is None:
        next_state.update(status="COMPLETE", stop_code="CHAIN_COMPLETE")
        status = "COMPLETE"
        code = "CHAIN_COMPLETE"
        next_route = None
    else:
        next_state.update(status="ACTIVE", stop_code=None)
        status = "PASS"
        code = "NEXT_SELECTOR_READY"
        next_route = "task-session"
    return {
        "status": status,
        "terminal_code": code,
        "claim": "transition joined and finite frontier advanced",
        "transition_digest": transition_digest,
        "next_task_session_selector": (
            None if fresh_epoch_required else expected_successor
        ),
        "next_fresh_epoch_unit": (
            expected_successor if fresh_epoch_required else None
        ),
        "next_route": next_route,
        "authority_effect": "none",
    }, next_state


def exclusive_write_json(path: Path, document: dict[str, Any]) -> None:
    payload = json.dumps(document, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, payload)
    finally:
        os.close(descriptor)


def open_chain_state(
    config: dict[str, Any], manifest: dict[str, Any], repository_root: Path
) -> tuple[Path, dict[str, Any]]:
    state_dir = resolve_inside(
        repository_root, config["state_directory"], must_exist=False
    )
    state_dir.mkdir(parents=True, exist_ok=True)
    transitions_dir = state_dir / "transitions"
    transitions_dir.mkdir(exist_ok=True)
    chain_path = state_dir / "chain.json"
    config_projection = {
        "chain_id": config["chain_id"],
        "scope_id": config["scope_id"],
        "epoch_id": config["approved_epoch"]["epoch_id"],
        "manifest_digest": config["approved_epoch"]["audit_projection_digest"],
        "frontier": config["finite_frontier"],
        "budget": config["run_budget"],
        "risk_ceiling": config["risk_ceiling"],
    }
    chain_record = {
        "schema_version": "1.0.0",
        "config_digest": digest(config),
        "projection_digest": digest(config_projection),
        "projection": config_projection,
    }
    if not chain_path.exists():
        try:
            exclusive_write_json(chain_path, chain_record)
        except FileExistsError:
            pass
    if load_json(chain_path) != chain_record:
        raise ValueError("existing chain record differs from approved configuration")

    records = sorted(transitions_dir.glob("*.json"))
    if not records:
        return transitions_dir, initial_state(config)
    expected_ordinals = [f"{index:06d}.json" for index in range(1, len(records) + 1)]
    if [path.name for path in records] != expected_ordinals:
        raise ValueError("transition ledger has a gap or unexpected filename")
    state = initial_state(config)
    for path in records:
        record = load_json(path)
        transition = record.get("transition")
        if not isinstance(transition, dict):
            raise ValueError("transition ledger record lacks replay payload")
        if record.get("transition_id") != transition.get("transition_id"):
            raise ValueError("transition ledger identity differs from payload")
        if record.get("previous_transition_digest") != state.get(
            "last_transition_digest"
        ) or transition.get("previous_transition_digest") != state.get(
            "last_transition_digest"
        ):
            raise ValueError("transition ledger hash link is broken")
        receipt, next_state = evaluate_transition(
            config, manifest, transition, state, repository_root
        )
        if record.get("transition_digest") != next_state.get(
            "last_transition_digest"
        ):
            raise ValueError("transition ledger digest differs from replay")
        if record.get("receipt") != receipt:
            raise ValueError("transition ledger receipt differs from replay")
        if record.get("state_after") != next_state:
            raise ValueError("transition ledger state differs from replay")
        state = next_state
    return transitions_dir, state


def persist_transition(
    transitions_dir: Path,
    transition: dict[str, Any],
    receipt: dict[str, Any],
    state: dict[str, Any],
) -> Path:
    ordinal = state["request_count"]
    path = transitions_dir / f"{ordinal:06d}.json"
    record = {
        "schema_version": "1.0.0",
        "transition_id": transition["transition_id"],
        "transition_digest": state["last_transition_digest"],
        "previous_transition_digest": transition["previous_transition_digest"],
        "transition": json_clone(transition),
        "receipt": receipt,
        "state_after": state,
    }
    exclusive_write_json(path, record)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--transition", type=Path)
    return parser.parse_args()


def discover_repository_root(config_path: Path) -> Path:
    current = config_path.resolve().parent
    while current.parent != current and not (current / ".git").exists():
        current = current.parent
    if not (current / ".git").exists():
        raise ValueError("repository root could not be discovered")
    return current


def main() -> int:
    args = parse_args()
    config = load_json(args.config)
    errors = schema_errors(config, CONFIG_SCHEMA, "chain config")
    if errors:
        raise SystemExit("\n".join(errors))
    repository_root = discover_repository_root(args.config)
    manifest, preflight_receipt = preflight(config, repository_root)
    if manifest is None:
        print(json.dumps(preflight_receipt, sort_keys=True))
        return 2
    try:
        transitions_dir, state = open_chain_state(config, manifest, repository_root)
    except ValueError as error:
        print(json.dumps(block("CHAIN_STATE_INVALID", str(error)), sort_keys=True))
        return 2
    if args.transition is None:
        receipt = admit_next_request(config, manifest, state)
        print(json.dumps(receipt, sort_keys=True))
        return 0 if receipt["status"] in {"READY", "COMPLETE"} else 2
    transition = load_json(args.transition)
    receipt, next_state = evaluate_transition(
        config, manifest, transition, state, repository_root
    )
    if next_state["request_count"] == state["request_count"]:
        print(json.dumps(receipt, sort_keys=True))
        return 2
    try:
        ledger_path = persist_transition(
            transitions_dir, transition, receipt, next_state
        )
    except FileExistsError:
        receipt = block(
            "TRANSITION_COLLISION",
            "exclusive-create refused an existing transition ordinal",
        )
        print(json.dumps(receipt, sort_keys=True))
        return 2
    receipt["ledger_path"] = str(ledger_path.relative_to(repository_root))
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] in {"PASS", "COMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
