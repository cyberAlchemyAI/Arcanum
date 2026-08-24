#!/usr/bin/env python3
"""Deterministic Ontology Vault materialization and package checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REQUEST_SCHEMA_VERSION = "ontology-vault-materialization-request/v1"
DECISION_SCHEMA_VERSION = "ontology-vault-materialization-decision/v1"
INVOKE_BUSINESS_NODE_CONTRACT_V1 = "invoke-business-node/public-contract-v1"
INVOKE_BUSINESS_NODE_CONTRACT_V2 = "invoke-business-node/public-contract-v2"
INVOKE_BUSINESS_CONCEPT_FIELDS = {"name", "role", "meaning", "plain_language"}
INVOKE_BUSINESS_CONCEPT_ROLES = {
    "actor",
    "business rule",
    "capability",
    "outcome",
    "policy",
    "workflow",
}
INVOKE_BUSINESS_SCHEMA_AMENDMENT_ID = "SAW-INVOKE-BUSINESS-CONCEPT-V2-20260820"
INVOKE_SOURCE_REGROUNDING_ID = "SRG-INVOKE-SOURCE-20260824"
EVIDENCE_REF_PATTERN = re.compile(
    r"^(SRC-[A-Z0-9-]+)#L([1-9][0-9]*)-L([1-9][0-9]*)$"
)
EVIDENCE_SELECTOR_CANONICALIZATION = (
    "sha256(('\\n'.join(selected_lines) + '\\n').encode('utf-8'))"
)


class ContractError(ValueError):
    """Raised when a request does not satisfy the closed request contract."""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _canonical_record_sha256(record: dict[str, Any]) -> str:
    canonical = json.dumps(record, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _collect_line_evidence_refs(value: Any) -> list[str]:
    references: list[str] = []
    if isinstance(value, dict):
        for child in value.values():
            references.extend(_collect_line_evidence_refs(child))
    elif isinstance(value, list):
        for child in value:
            references.extend(_collect_line_evidence_refs(child))
    elif isinstance(value, str) and EVIDENCE_REF_PATTERN.fullmatch(value):
        references.append(value)
    return references


def _evidence_slice(path: Path, start: int, end: int) -> bytes:
    lines = path.read_text(encoding="utf-8").splitlines()
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"selector bounds invalid for {path}: L{start}-L{end}")
    return ("\n".join(lines[start - 1 : end]) + "\n").encode("utf-8")


def _require_exact_keys(value: dict[str, Any], expected: set[str], at: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ContractError(f"{at} keys mismatch; missing={missing}, extra={extra}")


def _require_bool_fields(value: dict[str, Any], fields: set[str], at: str) -> None:
    for field in fields:
        if not isinstance(value[field], bool):
            raise ContractError(f"{at}.{field} must be boolean")


def validate_materialization_request(request: dict[str, Any]) -> None:
    _require_exact_keys(
        request,
        {"schema_version", "intent", "scope", "state", "ownership"},
        "request",
    )
    if request["schema_version"] != REQUEST_SCHEMA_VERSION:
        raise ContractError("request.schema_version is unsupported")

    intent_fields = {"one_off", "durable", "reusable", "evolving", "package_requested"}
    _require_exact_keys(request["intent"], intent_fields, "request.intent")
    _require_bool_fields(request["intent"], intent_fields, "request.intent")

    scope_fields = {"ontology_type_count", "branch_count", "view_count", "bridge"}
    _require_exact_keys(request["scope"], scope_fields, "request.scope")
    for field in {"ontology_type_count", "branch_count", "view_count"}:
        value = request["scope"][field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ContractError(f"request.scope.{field} must be a non-negative integer")
    if not isinstance(request["scope"]["bridge"], bool):
        raise ContractError("request.scope.bridge must be boolean")

    state_fields = {
        "stable_identity_survives_run",
        "enriches_existing_ontology",
        "needs_schemas",
        "needs_source_bindings",
        "needs_human_navigation",
        "needs_reusable_projections",
        "runtime_profile_mutation",
        "invocation_evidence_only",
    }
    _require_exact_keys(request["state"], state_fields, "request.state")
    _require_bool_fields(request["state"], state_fields, "request.state")

    ownership_fields = {
        "owner_route",
        "package_root",
        "crosses_visibility_boundary",
        "visibility",
    }
    _require_exact_keys(request["ownership"], ownership_fields, "request.ownership")
    ownership = request["ownership"]
    for field in {"owner_route", "package_root"}:
        if ownership[field] is not None and not isinstance(ownership[field], str):
            raise ContractError(f"request.ownership.{field} must be string or null")
    if not isinstance(ownership["crosses_visibility_boundary"], bool):
        raise ContractError("request.ownership.crosses_visibility_boundary must be boolean")
    if ownership["visibility"] not in {None, "public", "private"}:
        raise ContractError("request.ownership.visibility must be public, private, or null")


def classify_materialization(request: dict[str, Any]) -> dict[str, Any]:
    validate_materialization_request(request)
    intent = request["intent"]
    scope = request["scope"]
    state = request["state"]
    ownership = request["ownership"]

    triggers: list[str] = []
    if any(intent[field] for field in ("durable", "reusable", "evolving", "package_requested")):
        triggers.append("explicit_durable_intent")
    if scope["branch_count"] > 1 or scope["view_count"] > 1:
        triggers.append("multiple_branches_or_views")
    if scope["bridge"]:
        triggers.append("bridge_requested")
    if state["stable_identity_survives_run"]:
        triggers.append("stable_identity_survives_run")
    if state["enriches_existing_ontology"]:
        triggers.append("enriches_existing_ontology")
    if any(
        state[field]
        for field in (
            "needs_schemas",
            "needs_source_bindings",
            "needs_human_navigation",
            "needs_reusable_projections",
        )
    ):
        triggers.append("reusable_surfaces_required")
    if state["runtime_profile_mutation"]:
        triggers.append("runtime_profile_mutates_owned_surface")

    blockers: list[str] = []
    if triggers:
        if not ownership["owner_route"]:
            blockers.append("package_owner_unresolved")
        if not ownership["package_root"]:
            blockers.append("package_output_unresolved")
        if ownership["crosses_visibility_boundary"] and not ownership["visibility"]:
            blockers.append("package_visibility_unresolved")
        result = "block" if blockers else "package-required"
    else:
        simple_allowed = all(
            (
                scope["ontology_type_count"] == 1,
                scope["branch_count"] == 1,
                scope["view_count"] <= 1,
                intent["one_off"],
                not state["enriches_existing_ontology"],
                not intent["reusable"],
                not intent["evolving"],
                not scope["bridge"],
                state["invocation_evidence_only"],
            )
        )
        if simple_allowed:
            result = "single-artifact-allowed"
        else:
            result = "block"
            blockers.append("materialization_intent_unresolved")

    return {
        "schema_version": DECISION_SCHEMA_VERSION,
        "result": result,
        "detected_triggers": triggers,
        "blockers": blockers,
        "owner_route": ownership["owner_route"],
        "package_root": ownership["package_root"],
        "visibility": ownership["visibility"],
        "authority_effect": "none",
        "ontology_state_write_allowed": result in {"single-artifact-allowed", "package-required"},
        "append_to_prior_run_artifact_allowed": False,
    }


def command_classify(args: argparse.Namespace) -> int:
    request = load_json(Path(args.request))
    try:
        result = classify_materialization(request)
    except (ContractError, KeyError, TypeError) as error:
        result = {
            "schema_version": DECISION_SCHEMA_VERSION,
            "result": "block",
            "detected_triggers": [],
            "blockers": ["invalid_materialization_request"],
            "error": str(error),
            "authority_effect": "none",
            "ontology_state_write_allowed": False,
            "append_to_prior_run_artifact_allowed": False,
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] != "block" else 1


def _walk(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield ("key", key)
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)
    elif isinstance(value, str):
        yield ("string", value)


def validate_public_export(policy: dict[str, Any], contracts: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if policy.get("authority_effect") != "none":
        errors.append("policy authority_effect must be none")
    if policy.get("arcanum_definition_authority") is not False:
        errors.append("policy must not claim Arcanum definition authority")
    if policy.get("ontology_decides_authority") is not False:
        errors.append("policy must state that ontology does not decide authority")
    if contracts.get("contract_id") != policy.get("contract_id"):
        errors.append("contract ID does not match policy")
    if contracts.get("authority_effect") != "none":
        errors.append("public contracts authority_effect must be none")
    if contracts.get("arcanum_definition_authority") is not False:
        errors.append("public contracts must not claim Arcanum definition authority")
    if contracts.get("ontology_decides_authority") is not False:
        errors.append("public contracts must state that ontology does not decide authority")

    allowed_definition_ids = policy.get("allowed_definition_ids", [])
    actual_definition_ids = [entry.get("origin_id") for entry in contracts.get("definitions", [])]
    if actual_definition_ids != allowed_definition_ids:
        errors.append("public definition IDs must exactly match the ordered allowlist")
    allowed_model_ids = policy.get("allowed_model_contract_ids", [])
    actual_model_ids = [entry.get("contract_id") for entry in contracts.get("model_contracts", [])]
    if actual_model_ids != allowed_model_ids:
        errors.append("public model contract IDs must exactly match the ordered allowlist")

    allowed_classes = set(policy.get("allowed_artifact_classes", []))
    for entry in [*contracts.get("definitions", []), *contracts.get("model_contracts", [])]:
        if entry.get("artifact_class") not in allowed_classes:
            errors.append(f"disallowed artifact class for {entry.get('origin_id') or entry.get('contract_id')}")
        if entry.get("authority_effect") != "none":
            errors.append(f"authority_effect must be none for {entry.get('origin_id') or entry.get('contract_id')}")

    forbidden_keys = set(policy.get("forbidden_public_keys", []))
    forbidden_fragments = [value.lower() for value in policy.get("forbidden_public_path_fragments", [])]
    for kind, value in _walk(contracts):
        if kind == "key" and value in forbidden_keys:
            errors.append(f"forbidden public key: {value}")
        if kind == "string":
            lowered = value.lower()
            for fragment in forbidden_fragments:
                if fragment in lowered:
                    errors.append(f"forbidden public path fragment: {fragment}")
                    break

    provenance = contracts.get("public_provenance", {})
    for field in policy.get("public_provenance_requires", []):
        if field not in provenance:
            errors.append(f"public provenance missing {field}")
    if provenance.get("authority_effect") != "none":
        errors.append("public provenance authority_effect must be none")
    return errors


def command_validate_export(args: argparse.Namespace) -> int:
    policy_path = Path(args.policy).resolve()
    contracts_path = Path(args.contracts).resolve()
    errors: list[str] = []
    for path in (policy_path, contracts_path):
        if path.is_symlink():
            errors.append(f"symbolic links are forbidden: {path}")
        if path.suffix != ".json":
            errors.append(f"public contract must be JSON: {path}")
        if path.exists() and path.stat().st_mode & 0o111:
            errors.append(f"public contract must not be executable: {path}")
    if not errors:
        errors.extend(validate_public_export(load_json(policy_path), load_json(contracts_path)))
    result = {
        "schema_version": "ontology-vault-cav2-public-export-validation/v1",
        "status": "pass" if not errors else "block",
        "policy": str(policy_path),
        "contracts": str(contracts_path),
        "checks": [
            "exact_definition_allowlist",
            "exact_model_contract_allowlist",
            "artifact_class_allowlist",
            "private_path_scrub",
            "authority_effect_ceiling",
            "ontology_owner_boundary",
            "non_executable_json_only"
        ],
        "errors": errors,
        "authority_effect": "none",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _public_package_files(package_root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in package_root.rglob("*")
            if path.is_file()
            and "receipts" not in path.relative_to(package_root).parts
            and "__pycache__" not in path.relative_to(package_root).parts
        ),
        key=lambda path: path.relative_to(package_root).as_posix(),
    )


def _package_material_digest(package_root: Path) -> tuple[str, list[dict[str, str]]]:
    inventory = [
        {
            "path": path.relative_to(package_root).as_posix(),
            "sha256": _sha256(path),
        }
        for path in _public_package_files(package_root)
    ]
    canonical = json.dumps(inventory, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest(), inventory


def _require_record_keys(
    records: list[dict[str, Any]],
    required: set[str],
    allowed: set[str],
    at: str,
    errors: list[str],
) -> None:
    for index, record in enumerate(records):
        keys = set(record)
        missing = sorted(required - keys)
        extra = sorted(keys - allowed)
        if missing or extra:
            errors.append(f"{at}[{index}] keys mismatch; missing={missing}, extra={extra}")


def validate_ontology_package(
    package_root: Path,
    repository_root: Path,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    required_files = {
        "README.md",
        "INDEX.md",
        "profile.json",
        "sources.json",
        "nodes/business.json",
        "nodes/system.json",
        "relations/business.json",
        "relations/system.json",
        "relations/bridge.json",
        "views/business.json",
        "views/system.json",
        "views/bridge.json",
        "residue.json",
        "extensions/operation-composition.json",
        "schemas/package.schema.json",
        "migration/preserved-identities.json",
        "history/legacy-validation.json",
        "scripts/validate.py",
    }
    for relative in sorted(required_files):
        path = package_root / relative
        if not path.is_file():
            errors.append(f"required package file missing: {relative}")
        elif path.is_symlink():
            errors.append(f"symbolic links are forbidden: {relative}")

    for path in package_root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symbolic links are forbidden: {path.relative_to(package_root)}")
        if path.is_file() and path.suffix.lower() in {".sh", ".exe", ".bat", ".ps1"}:
            errors.append(f"executable publication material is forbidden: {path.relative_to(package_root)}")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".py"}:
            text = path.read_text(encoding="utf-8").lower()
            for fragment in ("cyberalchemy-v2/", ".arcanum/", "projects/", "sessions/", "telemetry/"):
                if fragment in text:
                    errors.append(
                        f"private or unrelated path fragment {fragment!r} in {path.relative_to(package_root)}"
                    )

    if errors:
        return errors, {}

    try:
        profile = load_json(package_root / "profile.json")
        schema_document = load_json(package_root / "schemas/package.schema.json")
        sources_document = load_json(package_root / "sources.json")
        business_document = load_json(package_root / "nodes/business.json")
        system_document = load_json(package_root / "nodes/system.json")
        business_relations_document = load_json(package_root / "relations/business.json")
        system_relations_document = load_json(package_root / "relations/system.json")
        bridge_document = load_json(package_root / "relations/bridge.json")
        views = {
            "business": load_json(package_root / "views/business.json"),
            "system": load_json(package_root / "views/system.json"),
            "bridge": load_json(package_root / "views/bridge.json"),
        }
        residue_document = load_json(package_root / "residue.json")
        operations = load_json(package_root / "extensions/operation-composition.json")
        migration = load_json(package_root / "migration/preserved-identities.json")
        history = load_json(package_root / "history/legacy-validation.json")
    except (OSError, json.JSONDecodeError) as error:
        return [f"package JSON load failed: {error}"], {}

    if set(profile) != {
        "schema_version",
        "package_id",
        "subject",
        "status",
        "owner_route",
        "visibility",
        "ontology_types",
        "materialization",
        "contract_bindings",
        "authority",
        "validation",
    }:
        errors.append("profile.json does not have the closed profile shape")
    authority = profile.get("authority", {})
    if authority != {
        "effect": "none",
        "ontology_decides_authority": False,
        "arcanum_definition_authority": False,
        "promotion_status": "not_requested",
        "publication_status": "not_requested",
    }:
        errors.append("profile authority ceiling or non-authority boundary is invalid")
    if profile.get("visibility") != "public" or profile.get("status") != "candidate":
        errors.append("Invoke ontology package must remain a public candidate")
    triggers = set(profile.get("materialization", {}).get("triggers", []))
    required_triggers = {
        "multiple_branches_or_views",
        "bridge_requested",
        "stable_identity_survives_run",
        "enriches_existing_ontology",
        "reusable_surfaces_required",
    }
    if profile.get("materialization", {}).get("classification") != "package-required":
        errors.append("materialization classification must be package-required")
    if not required_triggers.issubset(triggers):
        errors.append("materialization triggers do not cover durable Invoke package intent")

    concept_schema = schema_document.get("$defs", {}).get("businessConceptV2", {})
    if concept_schema.get("additionalProperties") is not False:
        errors.append("business concept v2 schema must be closed")
    if set(concept_schema.get("properties", {})) != INVOKE_BUSINESS_CONCEPT_FIELDS:
        errors.append("business concept v2 schema fields do not match the runtime contract")
    if set(concept_schema.get("required", [])) != INVOKE_BUSINESS_CONCEPT_FIELDS:
        errors.append("business concept v2 schema required fields are incomplete")
    if set(concept_schema.get("properties", {}).get("role", {}).get("enum", [])) != INVOKE_BUSINESS_CONCEPT_ROLES:
        errors.append("business concept v2 schema role vocabulary does not match the runtime contract")
    expected_model_contract = {
        "binding": INVOKE_BUSINESS_NODE_CONTRACT_V2,
        "compatibility_invariants": [
            "concept.name == label",
            "concept.role == role",
        ],
        "record_schema": "#/$defs/businessNodeV2",
    }
    if schema_document.get("model_contracts", {}).get("business_node") != expected_model_contract:
        errors.append("business node v2 model contract binding or compatibility invariants are invalid")
    if schema_document.get("governed_files", {}).get("schema_amendment_witness") != (
        "migration/preserved-identities.json#schema_amendments/0"
    ):
        errors.append("business node v2 schema-amendment witness binding is unresolved")
    if schema_document.get("governed_files", {}).get("source_regrounding_witnesses") != (
        "migration/preserved-identities.json#source_regroundings"
    ):
        errors.append("source re-grounding witness binding is unresolved")
    if schema_document.get("governed_files", {}).get("evidence_selector_bindings") != (
        "migration/preserved-identities.json#evidence_selector_binding"
    ):
        errors.append("evidence selector binding is unresolved")

    sources = sources_document.get("sources", [])
    _require_record_keys(
        sources,
        {"id", "locator", "sha256", "posture", "selector", "visibility"},
        {"id", "locator", "sha256", "posture", "selector", "visibility"},
        "sources",
        errors,
    )
    source_ids = [record.get("id") for record in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source IDs are not unique")
    source_records = {record.get("id"): record for record in sources}
    source_paths: dict[str, Path] = {}
    for record in sources:
        locator = record.get("locator", "")
        source_path = (repository_root / locator).resolve()
        try:
            source_path.relative_to(repository_root.resolve())
        except ValueError:
            errors.append(f"source escapes public repository root: {locator}")
            continue
        if not source_path.is_file() or source_path.is_symlink():
            errors.append(f"source is missing or symbolic: {locator}")
        else:
            source_paths[record.get("id")] = source_path
            if _sha256(source_path) != record.get("sha256"):
                errors.append(f"source digest mismatch: {record.get('id')}")
        if record.get("visibility") != "public":
            errors.append(f"source is not public: {record.get('id')}")

    regrounding_required = {
        "affected_branches",
        "authority_effect",
        "business_projection_evidence_rebindings",
        "id",
        "owner_route",
        "selector_rewrites",
        "semantic_impact",
        "source_changes",
        "stable_ids_preserved",
        "status",
    }
    source_regroundings = migration.get("source_regroundings", [])
    _require_record_keys(
        source_regroundings,
        regrounding_required,
        regrounding_required,
        "source regroundings",
        errors,
    )
    matching_regroundings = [
        record
        for record in source_regroundings
        if record.get("id") == INVOKE_SOURCE_REGROUNDING_ID
    ]
    regrounding: dict[str, Any] = {}
    if len(matching_regroundings) != 1:
        errors.append("Invoke source re-grounding witness must occur exactly once")
    else:
        regrounding = matching_regroundings[0]
        if (
            regrounding.get("authority_effect") != "none"
            or regrounding.get("status") != "candidate"
            or regrounding.get("stable_ids_preserved") is not True
        ):
            errors.append("Invoke source re-grounding witness exceeds its candidate authority ceiling")
        if regrounding.get("affected_branches") != ["business", "system", "bridge"]:
            errors.append("Invoke source re-grounding branch traversal is incomplete")
        source_changes = regrounding.get("source_changes", [])
        if {change.get("source_id") for change in source_changes} != {
            "SRC-ROOT",
            "SRC-DEFINE",
            "SRC-PLAN",
        }:
            errors.append("Invoke source re-grounding source-change inventory is incomplete")
        for change in source_changes:
            if set(change) != {"source_id", "previous_sha256", "current_sha256"}:
                errors.append("Invoke source re-grounding source-change shape is invalid")
                continue
            source_record = source_records.get(change.get("source_id"), {})
            if change.get("current_sha256") != source_record.get("sha256"):
                errors.append(
                    f"Invoke source re-grounding current digest is stale: {change.get('source_id')}"
                )
            if change.get("previous_sha256") == change.get("current_sha256"):
                errors.append(
                    f"Invoke source re-grounding does not identify a digest change: {change.get('source_id')}"
                )
        selector_rewrites = regrounding.get("selector_rewrites", [])
        if len(selector_rewrites) != 11 or len(
            {(rewrite.get("from"), rewrite.get("to")) for rewrite in selector_rewrites}
        ) != 11:
            errors.append("Invoke source re-grounding selector rewrite inventory must contain eleven unique moves")
        for rewrite in selector_rewrites:
            if set(rewrite) != {"from", "to"} or not all(
                isinstance(rewrite.get(field), str)
                and EVIDENCE_REF_PATTERN.fullmatch(rewrite[field])
                for field in ("from", "to")
            ):
                errors.append("Invoke source re-grounding selector rewrite is invalid")
        rebindings = regrounding.get("business_projection_evidence_rebindings", [])
        for rebinding in rebindings:
            if set(rebinding) != {
                "node_id",
                "previous_evidence_refs",
                "current_evidence_refs",
            }:
                errors.append("business projection evidence rebinding shape is invalid")

    business_nodes = business_document.get("nodes", [])
    system_nodes = system_document.get("nodes", [])
    business_required = {
        "id", "label", "branch", "role", "concept", "model_binding", "scope", "owner_route",
        "candidate_status", "promotion_state", "authority_effect", "claim", "evidence_refs",
        "evidence_confidence", "commitment_confidence", "semantic_definition_refs", "provenance",
        "use_obligations", "challenge_contract", "residue", "invalidation_route", "forbidden_collapse",
    }
    system_required = {
        "id", "label", "branch", "role", "owner_route", "candidate_status", "authority_effect",
        "claim", "evidence_refs", "evidence_confidence", "commitment_confidence", "forbidden_collapse",
    }
    _require_record_keys(business_nodes, business_required, business_required, "business nodes", errors)
    _require_record_keys(system_nodes, system_required, system_required, "system nodes", errors)
    business_node_schema = schema_document.get("$defs", {}).get("businessNodeV2", {})
    if business_node_schema.get("additionalProperties") is not False:
        errors.append("business node v2 schema must be closed")
    if set(business_node_schema.get("properties", {})) != business_required:
        errors.append("business node v2 schema properties do not match the runtime contract")
    if set(business_node_schema.get("required", [])) != business_required:
        errors.append("business node v2 schema required fields do not match the runtime contract")
    if business_node_schema.get("properties", {}).get("model_binding", {}).get("const") != (
        INVOKE_BUSINESS_NODE_CONTRACT_V2
    ):
        errors.append("business node v2 schema model binding is invalid")
    all_nodes = [*business_nodes, *system_nodes]
    node_ids = [node.get("id") for node in all_nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("node IDs are not unique")
    if any(node.get("authority_effect") != "none" for node in all_nodes):
        errors.append("every node authority_effect must be none")
    if any(node.get("branch") != "business" or not node.get("id", "").startswith("B-") for node in business_nodes):
        errors.append("business branch polarity is invalid")
    if any(node.get("branch") != "system" or not node.get("id", "").startswith("S-") for node in system_nodes):
        errors.append("system branch polarity is invalid")
    for index, node in enumerate(business_nodes):
        at = f"business nodes[{index}]"
        if node.get("model_binding") != INVOKE_BUSINESS_NODE_CONTRACT_V2:
            errors.append(f"{at}.model_binding must use the v2 business-node contract")
        if node.get("candidate_status") != "candidate" or node.get("promotion_state") != "not_requested":
            errors.append(f"{at} exceeds the candidate business-node lifecycle posture")
        concept = node.get("concept")
        if not isinstance(concept, dict):
            errors.append(f"{at}.concept must be an object")
            continue
        concept_keys = set(concept)
        if concept_keys != INVOKE_BUSINESS_CONCEPT_FIELDS:
            missing = sorted(INVOKE_BUSINESS_CONCEPT_FIELDS - concept_keys)
            extra = sorted(concept_keys - INVOKE_BUSINESS_CONCEPT_FIELDS)
            errors.append(f"{at}.concept keys mismatch; missing={missing}, extra={extra}")
        for field in sorted(INVOKE_BUSINESS_CONCEPT_FIELDS):
            value = concept.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{at}.concept.{field} must be a non-empty string")
        if concept.get("name") != node.get("label"):
            errors.append(f"{at}.concept.name must equal the label compatibility projection")
        if concept.get("role") != node.get("role"):
            errors.append(f"{at}.concept.role must equal the role compatibility projection")
        if concept.get("role") not in INVOKE_BUSINESS_CONCEPT_ROLES:
            errors.append(f"{at}.concept.role is not an allowed business role")

    amendment_required = {
        "added_fields",
        "affected_files",
        "affected_node_ids",
        "authority_effect",
        "canonicalization",
        "current_rule",
        "field_moves",
        "from_binding",
        "id",
        "legacy_projection_sha256",
        "migration_impact",
        "proposed_rule",
        "rationale",
        "rollback",
        "scope",
        "status",
        "to_binding",
    }
    schema_amendments = migration.get("schema_amendments", [])
    _require_record_keys(
        schema_amendments,
        amendment_required,
        amendment_required,
        "schema amendments",
        errors,
    )
    matching_amendments = [
        amendment
        for amendment in schema_amendments
        if amendment.get("id") == INVOKE_BUSINESS_SCHEMA_AMENDMENT_ID
    ]
    if len(matching_amendments) != 1:
        errors.append("business node v2 schema-amendment witness must occur exactly once")
    else:
        amendment = matching_amendments[0]
        business_node_ids = [node.get("id") for node in business_nodes]
        if amendment.get("affected_node_ids") != business_node_ids:
            errors.append("business node v2 schema-amendment witness does not preserve ordered node IDs")
        if amendment.get("authority_effect") != "none" or amendment.get("status") != "candidate":
            errors.append("business node v2 schema-amendment witness exceeds its authority ceiling")
        if amendment.get("scope") != "nodes/business.json#nodes":
            errors.append("business node v2 schema-amendment witness scope is invalid")
        if amendment.get("from_binding") != INVOKE_BUSINESS_NODE_CONTRACT_V1:
            errors.append("business node v2 schema-amendment source binding is invalid")
        if amendment.get("to_binding") != INVOKE_BUSINESS_NODE_CONTRACT_V2:
            errors.append("business node v2 schema-amendment target binding is invalid")
        expected_added_fields = [
            "concept.meaning",
            "concept.name",
            "concept.plain_language",
            "concept.role",
        ]
        if amendment.get("added_fields") != expected_added_fields:
            errors.append("business node v2 schema-amendment added fields are invalid")
        expected_field_moves = [
            {
                "from": "label",
                "mode": "copied compatibility projection",
                "to": "concept.name",
            },
            {
                "from": "role",
                "mode": "copied compatibility projection",
                "to": "concept.role",
            },
        ]
        if amendment.get("field_moves") != expected_field_moves:
            errors.append("business node v2 compatibility projections are invalid")
        expected_canonicalization = (
            "sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode('utf-8'))"
        )
        if amendment.get("canonicalization") != expected_canonicalization:
            errors.append("business node v1 projection canonicalization is invalid")
        for field in ("current_rule", "proposed_rule", "rationale"):
            value = amendment.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"business node v2 schema-amendment {field} must be non-empty")
        expected_impact = {
            "business_node_count": len(business_nodes),
            "changed_branch": "business",
            "relations_changed": False,
            "shared_public_contract_changed": False,
            "stable_node_ids_preserved": True,
            "system_nodes_changed": False,
            "views_changed": False,
        }
        if amendment.get("migration_impact") != expected_impact:
            errors.append("business node v2 migration impact is invalid")
        rollback = amendment.get("rollback", {})
        if (
            rollback.get("history_preserved") is not True
            or not isinstance(rollback.get("rule"), str)
            or not rollback.get("rule", "").strip()
        ):
            errors.append("business node v2 rollback rule must preserve history and name the reverse path")
        required_affected_files = {
            "ontology/invoke/README.md",
            "ontology/invoke/INDEX.md",
            "ontology/invoke/nodes/business.json",
            "ontology/invoke/schemas/package.schema.json",
            "ontology/invoke/migration/preserved-identities.json",
            "arcana/ontology-vault/scripts/ontology_package.py",
            "arcana/ontology-vault/development/package-materialization/test_invoke_package.py",
        }
        if set(amendment.get("affected_files", [])) != required_affected_files:
            errors.append("business node v2 schema-amendment affected-file inventory is invalid")
        legacy_projection_sha256 = amendment.get("legacy_projection_sha256", {})
        if set(legacy_projection_sha256) != set(business_node_ids):
            errors.append("business node v2 legacy-projection digest inventory is incomplete")
        else:
            evidence_rebindings = {
                record.get("node_id"): record
                for record in regrounding.get("business_projection_evidence_rebindings", [])
            }
            for node in business_nodes:
                concept = node.get("concept")
                if not isinstance(concept, dict):
                    continue
                legacy_projection = dict(node)
                legacy_projection.pop("concept", None)
                legacy_projection["label"] = concept.get("name")
                legacy_projection["role"] = concept.get("role")
                legacy_projection["model_binding"] = INVOKE_BUSINESS_NODE_CONTRACT_V1
                rebinding = evidence_rebindings.get(node.get("id"))
                if rebinding:
                    if node.get("evidence_refs") != rebinding.get("current_evidence_refs"):
                        errors.append(
                            f"node {node.get('id')} does not match its current evidence rebinding"
                        )
                    legacy_projection["evidence_refs"] = rebinding.get("previous_evidence_refs")
                actual_digest = _canonical_record_sha256(legacy_projection)
                expected_digest = legacy_projection_sha256.get(node.get("id"))
                if actual_digest != expected_digest:
                    errors.append(f"node {node.get('id')} does not preserve its frozen v1 projection")

    contract_path = repository_root / profile.get("contract_bindings", {}).get("public_contracts", "")
    allowed_definition_ids: set[str] = set()
    if contract_path.is_file():
        public_contracts = load_json(contract_path)
        allowed_definition_ids = {entry["origin_id"] for entry in public_contracts.get("definitions", [])}
    else:
        errors.append("public ontology contract binding is unresolved")
    for node in business_nodes:
        refs = set(node.get("semantic_definition_refs", []))
        refs.update(node.get("invalidation_route", {}).get("definition_refs", []))
        refs.add(node.get("provenance", {}).get("definition_ref"))
        refs.add(node.get("challenge_contract", {}).get("definition_ref"))
        if not refs.issubset(allowed_definition_ids):
            errors.append(f"node {node.get('id')} uses a non-exported definition ID")

    relation_required = {
        "id", "type", "branch", "from", "to", "direction", "owner_route",
        "authority_effect", "evidence_refs", "forbidden_collapse",
    }
    bridge_required = {
        "id", "type", "branch", "from", "to", "direction", "owner_route",
        "authority_effect", "business_evidence_refs", "system_evidence_refs",
        "business_confidence", "system_confidence", "alignment_confidence",
        "alignment_state", "forbidden_collapse",
    }
    business_relations = business_relations_document.get("relations", [])
    system_relations = system_relations_document.get("relations", [])
    bridge_relations = bridge_document.get("relations", [])
    _require_record_keys(business_relations, relation_required, relation_required, "business relations", errors)
    _require_record_keys(system_relations, relation_required, relation_required, "system relations", errors)
    _require_record_keys(bridge_relations, bridge_required, bridge_required, "bridge relations", errors)
    relation_ids = [record.get("id") for record in [*business_relations, *system_relations, *bridge_relations]]
    if len(relation_ids) != len(set(relation_ids)):
        errors.append("relation IDs are not unique")
    known_nodes = set(node_ids)
    for record in [*business_relations, *system_relations, *bridge_relations]:
        if record.get("from") not in known_nodes or record.get("to") not in known_nodes:
            errors.append(f"relation endpoint does not resolve: {record.get('id')}")
        if record.get("authority_effect") != "none":
            errors.append(f"relation authority_effect must be none: {record.get('id')}")
    for record in business_relations:
        if record.get("branch") != "business" or not record.get("from", "").startswith("B-") or not record.get("to", "").startswith("B-"):
            errors.append(f"business relation polarity is invalid: {record.get('id')}")
    for record in system_relations:
        if record.get("branch") != "system" or not record.get("from", "").startswith("S-") or not record.get("to", "").startswith("S-"):
            errors.append(f"system relation polarity is invalid: {record.get('id')}")
    for record in bridge_relations:
        if record.get("branch") != "bridge" or not record.get("from", "").startswith("B-") or not record.get("to", "").startswith("S-"):
            errors.append(f"bridge polarity is invalid: {record.get('id')}")
        if not record.get("business_evidence_refs") or not record.get("system_evidence_refs"):
            errors.append(f"bridge evidence is not separated: {record.get('id')}")

    evidence_documents = [
        business_document,
        system_document,
        business_relations_document,
        system_relations_document,
        bridge_document,
        residue_document,
        operations,
    ]
    all_source_refs = sorted(
        {
            reference
            for document in evidence_documents
            for reference in _collect_line_evidence_refs(document)
        }
    )
    known_sources = set(source_ids)
    for reference in all_source_refs:
        if reference.split("#", 1)[0] not in known_sources:
            errors.append(f"unresolved source reference: {reference}")

    selector_binding = migration.get("evidence_selector_binding", {})
    if set(selector_binding) != {"bindings", "canonicalization", "schema_version"}:
        errors.append("evidence selector binding shape is invalid")
    if selector_binding.get("schema_version") != "arcanum.ontology.evidence-selector-binding.v1":
        errors.append("evidence selector binding schema version is invalid")
    if selector_binding.get("canonicalization") != EVIDENCE_SELECTOR_CANONICALIZATION:
        errors.append("evidence selector binding canonicalization is invalid")
    binding_records = selector_binding.get("bindings", [])
    _require_record_keys(
        binding_records,
        {"line_count", "ref", "slice_sha256"},
        {"line_count", "ref", "slice_sha256"},
        "evidence selector bindings",
        errors,
    )
    binding_refs = [record.get("ref") for record in binding_records]
    if binding_refs != all_source_refs or len(binding_refs) != len(set(binding_refs)):
        errors.append("evidence selector binding inventory mismatch")
    for binding in binding_records:
        reference = binding.get("ref", "")
        match = EVIDENCE_REF_PATTERN.fullmatch(reference)
        if not match:
            errors.append(f"evidence selector format invalid: {reference}")
            continue
        source_id, start_text, end_text = match.groups()
        source_path = source_paths.get(source_id)
        if source_path is None:
            continue
        start, end = int(start_text), int(end_text)
        try:
            selected = _evidence_slice(source_path, start, end)
        except ValueError:
            errors.append(f"evidence selector bounds invalid: {reference}")
            continue
        if binding.get("line_count") != end - start + 1:
            errors.append(f"evidence selector line count mismatch: {reference}")
        if hashlib.sha256(selected).hexdigest() != binding.get("slice_sha256"):
            errors.append(f"evidence selector slice digest mismatch: {reference}")

    relation_id_set = set(relation_ids)
    for branch, view in views.items():
        if view.get("branch") != branch:
            errors.append(f"view branch mismatch: {branch}")
        for reference in view.get("node_refs", []):
            if reference not in known_nodes:
                errors.append(f"view node reference does not resolve: {reference}")
        for reference in view.get("relation_refs", []):
            if reference not in relation_id_set:
                errors.append(f"view relation reference does not resolve: {reference}")
    if set(views["bridge"].get("imports", [])) != {"VIEW-INVOKE-BUSINESS", "VIEW-INVOKE-SYSTEM"}:
        errors.append("bridge view imports are not explicit")

    gaps = residue_document.get("gaps", [])
    gap_ids = [gap.get("id") for gap in gaps]
    if len(gap_ids) != len(set(gap_ids)):
        errors.append("residue IDs are not unique")
    known_gaps = set(gap_ids)
    for node in business_nodes:
        for residue in node.get("residue", []):
            if residue.get("gap_ref") not in known_gaps:
                errors.append(f"node residue does not resolve: {node.get('id')}")
    if residue_document.get("authority_boundary", {}).get("ontology_decides_authority") is not False:
        errors.append("residue authority boundary must deny ontology authority")

    operation_records = operations.get("operation_composition", {}).get("operations", [])
    deferred_records = operations.get("operation_composition", {}).get("deferred_operations", [])
    capability_records = operations.get("operation_composition", {}).get("supporting_capabilities", [])
    actual_operation_ids = [record.get("id") for record in operation_records]
    actual_deferred_ids = [record.get("id") for record in deferred_records]
    actual_capability_ids = [record.get("id") for record in capability_records]
    actual_phase_count = sum(len(record.get("phases", [])) for record in operation_records)

    operation_by_id = {record.get("id"): record for record in operation_records}
    usage_by_id = {
        record.get("operation"): record
        for record in operations.get("operation_composition", {}).get("capability_usage", [])
    }
    define_supports = {
        phase.get("support")
        for phase in operation_by_id.get("OP-DEFINE", {}).get("phases", [])
    }
    if "invoke:define-identity-denominator-validator" not in define_supports:
        errors.append("Define identity-denominator gate is missing")
    readiness_capabilities = {
        "CAP-WORK-PACK-READINESS-AUDIT",
        "CAP-IMPLEMENTATION-READINESS",
    }
    plan_supports = {
        phase.get("support")
        for phase in operation_by_id.get("OP-PLAN", {}).get("phases", [])
    }
    plan_conditionals = set(usage_by_id.get("OP-PLAN", {}).get("conditional", []))
    if not readiness_capabilities.issubset(set(actual_capability_ids)) or not readiness_capabilities.issubset(
        plan_supports
    ) or not readiness_capabilities.issubset(plan_conditionals):
        errors.append("Plan readiness capability binding is incomplete")
    invariants = operations.get("operation_composition", {}).get("invariants", [])
    if not any("preacceptance closure" in invariant.lower() for invariant in invariants):
        errors.append("preacceptance-closure invariant is missing")

    preserved = migration.get("preserved", {})
    expected_sets = {
        "business_node_ids": [node.get("id") for node in business_nodes],
        "system_node_ids": [node.get("id") for node in system_nodes],
        "business_relation_ids": [record.get("id") for record in business_relations],
        "system_relation_ids": [record.get("id") for record in system_relations],
        "bridge_relation_ids": [record.get("id") for record in bridge_relations],
        "active_operation_ids": actual_operation_ids,
        "deferred_operation_ids": actual_deferred_ids,
        "capability_ids": actual_capability_ids,
    }
    for field, actual in expected_sets.items():
        if preserved.get(field) != actual:
            errors.append(f"migration manifest does not preserve ordered {field}")
    if preserved.get("phase_count") != actual_phase_count:
        errors.append("migration manifest phase count does not match operation composition")

    validation_records = history.get("legacy_validations", [])
    if len(validation_records) != 3:
        errors.append("legacy validation history must contain three receipts")
    if any(record.get("authority_effect") != "none" or record.get("promotion_status") != "not_requested" for record in validation_records):
        errors.append("legacy validation history exceeds its authority ceiling")

    counts = {
        "sources": len(sources),
        "business_nodes": len(business_nodes),
        "system_nodes": len(system_nodes),
        "business_relations": len(business_relations),
        "system_relations": len(system_relations),
        "bridge_relations": len(bridge_relations),
        "gaps": len(gaps),
        "active_operations": len(operation_records),
        "deferred_operations": len(deferred_records),
        "capabilities": len(capability_records),
        "phases": actual_phase_count,
        "evidence_selectors": len(binding_records),
        "source_regroundings": len(source_regroundings),
    }
    return errors, counts


def command_validate_package(args: argparse.Namespace) -> int:
    package_root = Path(args.package_root).resolve()
    repository_root = Path(args.repository_root).resolve()
    errors, counts = validate_ontology_package(package_root, repository_root)
    material_digest = ""
    inventory: list[dict[str, str]] = []
    if package_root.is_dir():
        material_digest, inventory = _package_material_digest(package_root)
    receipt_path = package_root / "receipts" / f"validation-{material_digest[:16]}.json"
    checks = [
        "required_surfaces",
        "closed_record_shapes",
        "business_concept_v2_shape",
        "business_concept_compatibility",
        "business_node_v1_projection_preservation",
        "schema_amendment_witness",
        "source_digest_currency",
        "source_regrounding_witness",
        "evidence_selector_bounds",
        "evidence_selector_slice_binding",
        "mandatory_gate_regrounding",
        "stable_id_uniqueness",
        "relation_endpoint_closure",
        "branch_polarity",
        "separate_bridge_source_evidence",
        "view_reference_closure",
        "residue_reference_closure",
        "operation_composition_preservation",
        "authority_effect_ceiling",
        "public_private_path_scrub",
        "append_only_receipt_history",
    ]
    receipt = {
        "schema_version": "arcanum.ontology.package.validation-receipt.v1",
        "package_id": "arcanum.invoke.ontology",
        "material_digest": material_digest,
        "material_inventory": inventory,
        "status": "pass" if not errors else "block",
        "checks": checks,
        "counts": counts,
        "errors": errors,
        "authority_effect": "none",
        "promotion_status": "not_requested",
        "publication_status": "not_requested",
    }
    encoded_receipt = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.write_receipt and not errors:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        if receipt_path.exists():
            if receipt_path.read_text(encoding="utf-8") != encoded_receipt:
                errors.append("existing append-only receipt content does not match current validation")
        else:
            receipt_path.write_text(encoded_receipt, encoding="utf-8")
    elif not args.write_receipt:
        if not receipt_path.is_file():
            errors.append("current deterministic validation receipt is missing")
        elif receipt_path.read_text(encoding="utf-8") != encoded_receipt:
            errors.append("current deterministic validation receipt does not match package material")
    result = {
        "schema_version": "arcanum.ontology.package.validation-result.v1",
        "status": "pass" if not errors else "block",
        "package_root": str(package_root),
        "material_digest": material_digest,
        "receipt": str(receipt_path),
        "checks": checks,
        "counts": counts,
        "errors": errors,
        "authority_effect": "none",
        "promotion_status": "not_requested",
        "publication_status": "not_requested",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    classify_parser = subparsers.add_parser("classify")
    classify_parser.add_argument("--request", required=True)
    classify_parser.set_defaults(handler=command_classify)
    export_parser = subparsers.add_parser("validate-export")
    export_parser.add_argument("--policy", required=True)
    export_parser.add_argument("--contracts", required=True)
    export_parser.set_defaults(handler=command_validate_export)
    package_parser = subparsers.add_parser("validate-package")
    package_parser.add_argument("--package-root", required=True)
    package_parser.add_argument("--repository-root", required=True)
    package_parser.add_argument("--write-receipt", action="store_true")
    package_parser.set_defaults(handler=command_validate_package)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
