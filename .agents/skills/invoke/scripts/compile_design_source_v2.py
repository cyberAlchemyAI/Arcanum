#!/usr/bin/env python3
"""Compile one exact W2 candidate plus passing Distill evidence into a W3 bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from jsonschema import Draft202012Validator, RefResolver

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from project_design_artifact import (  # noqa: E402
    POLICY_PATH,
    PROCESS_PATH,
    PROFILE_PATH,
    digest_without,
    exact_ref,
    load_json,
)
from project_design_bundle import project_bundle  # noqa: E402


IDENTITY = "invoke.compile-design-source.v2"
OWNER = "invoke-design-producer"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_source_v2.py"
W2_PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_candidate.py"
STAGE_NAME = "INVOKE-DESIGN-STAGE-RECEIPT.json"
STAGE_IDS = (
    "bundle-closure-validation",
    "view-projection",
    "distill-evidence-validation",
    "bundle-output-closure",
    "late-finalization",
)
OUTPUTS = (
    ("design-artifact", "DESIGN.json"),
    ("architecture", "ARCHITECTURE.md"),
    ("selected-companions", "SELECTED-COMPANIONS.md"),
    ("glossary-consistency", "GLOSSARY-CONSISTENCY-REPORT.json"),
    ("planned-witnesses", "PLANNED-WITNESS-CONTRACTS.json"),
    ("layering", "IMPLEMENTATION-LAYERING.md"),
    ("template-selection", "TEMPLATE-SELECTION-RECEIPT.json"),
    ("dispatch-trace", "DISPATCH-TRACE.json"),
    ("distill", "DISTILL-RECEIPT.json"),
    ("scope-manifest", "DESIGN-SCOPE-MANIFEST.json"),
    ("denominator-receipt", "DESIGN-DENOMINATOR-RECEIPT.json"),
    ("selection-result", "DESIGN-SELECTION-RESULT.json"),
    ("coherence-receipt", "DESIGN-COHERENCE-RECEIPT.json"),
    ("transport", "DESIGN-TRANSPORT-REPORT.json"),
)
OUTPUT_CONTRACTS = {
    "design_artifact": "DESIGN.json",
    "architecture": "ARCHITECTURE.md",
    "selected_companions": "SELECTED-COMPANIONS.md",
    "glossary_consistency": "GLOSSARY-CONSISTENCY-REPORT.json",
    "planned_witnesses": "PLANNED-WITNESS-CONTRACTS.json",
    "layering": "IMPLEMENTATION-LAYERING.md",
    "template_selection": "TEMPLATE-SELECTION-RECEIPT.json",
    "dispatch_trace": "DISPATCH-TRACE.json",
    "distill": "DISTILL-RECEIPT.json",
    "scope_manifest": "DESIGN-SCOPE-MANIFEST.json",
    "denominator_receipt": "DESIGN-DENOMINATOR-RECEIPT.json",
    "selection_result": "DESIGN-SELECTION-RESULT.json",
    "coherence_receipt": "DESIGN-COHERENCE-RECEIPT.json",
    "transport": "DESIGN-TRANSPORT-REPORT.json",
    "stage_receipt": STAGE_NAME,
}
PROJECTED_SCHEMA_IDS = {
    "GLOSSARY-CONSISTENCY-REPORT.json": "https://arcanum.dev/schemas/invoke/design-glossary-consistency-report/v1",
    "PLANNED-WITNESS-CONTRACTS.json": "https://arcanum.dev/schemas/invoke/design-planned-witness-contracts/v1",
    "TEMPLATE-SELECTION-RECEIPT.json": "https://arcanum.dev/schemas/invoke/design-template-selection-receipt/v1",
    "DISPATCH-TRACE.json": "https://arcanum.dev/schemas/invoke/design-dispatch-trace/v1",
    "DESIGN-TRANSPORT-REPORT.json": "https://arcanum.dev/schemas/invoke/design-transport-report/v1",
}


class GovernedBlock(ValueError):
    def __init__(
        self,
        code: str,
        message: str,
        stage_index: int,
        selector: str | None = None,
        route: str = "repair-design-bundle",
    ):
        super().__init__(message)
        self.code = code
        self.stage_index = stage_index
        self.selector = selector
        self.route = route


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    if path.exists() or path.is_symlink():
        raise ValueError(f"attempt receipt must be absent: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def schema_store(schema_dir: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in schema_dir.glob("*.schema.json"):
        try:
            document = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if isinstance(document.get("$id"), str):
            result[document["$id"]] = document
    return result


def schema_errors(document: Any, schema: dict[str, Any], store: dict[str, dict[str, Any]]) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store)
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, resolver=resolver).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def safe_repo_path(root: Path, label: str, must_be_file: bool = True) -> Path:
    pure = PurePosixPath(label)
    if pure.is_absolute() or pure.as_posix() != label or "\\" in label or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise GovernedBlock("PATH_UNSAFE", f"unsafe repository-relative path: {label}", 0, label, "repair-w2-candidate")
    current = root.resolve()
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise GovernedBlock("PATH_UNSAFE", f"symlink path component is forbidden: {label}", 0, label, "repair-w2-candidate")
    try:
        current.relative_to(root.resolve())
    except ValueError as error:
        raise GovernedBlock("PATH_UNSAFE", f"path escapes repository: {label}", 0, label, "repair-w2-candidate") from error
    if must_be_file and not current.is_file():
        raise GovernedBlock("REFERENCE_UNAVAILABLE", f"bound file unavailable: {label}", 0, label, "repair-w2-candidate")
    return current


def verify_ref(root: Path, ref: dict[str, Any], stage_index: int = 0, route: str = "repair-w2-candidate") -> Path:
    try:
        path = safe_repo_path(root, ref["path"])
    except (KeyError, TypeError) as error:
        raise GovernedBlock("REFERENCE_UNAVAILABLE", "malformed exact reference", stage_index, None, route) from error
    data = path.read_bytes()
    if len(data) != ref.get("size") or hashlib.sha256(data).hexdigest() != ref.get("sha256"):
        raise GovernedBlock("REFERENCE_DIGEST_MISMATCH", f"bound bytes drifted: {ref['path']}", stage_index, ref["path"], route)
    return path


def size_bytes_ref(ref: dict[str, Any]) -> dict[str, Any]:
    return {"path": ref["path"], "sha256": ref["sha256"], "size_bytes": ref["size"]}


def output_ref(path: Path, kind: str, label: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    return {"kind": kind, "path": label or path.name, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def document_ref(path: Path, root: Path) -> dict[str, Any]:
    return exact_ref(path, root)


def validate_document(
    document: dict[str, Any],
    schema_id: str,
    digest_field: str | None,
    store: dict[str, dict[str, Any]],
    code: str,
    stage_index: int,
    route: str,
) -> None:
    if schema_id not in store:
        raise GovernedBlock("INSTALLED_CONTRACT_DRIFT", f"installed schema unavailable: {schema_id}", stage_index, schema_id, "repair-installed-contract")
    errors = schema_errors(document, store[schema_id], store)
    if errors:
        raise GovernedBlock(code, "; ".join(errors[:8]), stage_index, schema_id, route)
    if digest_field and document.get(digest_field) != digest_without(document, digest_field):
        raise GovernedBlock(code, f"self digest mismatch: {digest_field}", stage_index, digest_field, route)


def safe_absent_destination(path: Path, root: Path | None = None) -> Path:
    if not path.is_absolute():
        raise ValueError("destination paths must be absolute")
    lexical = Path(os.path.abspath(path))
    if lexical.exists() or lexical.is_symlink():
        raise ValueError(f"destination must be absent: {lexical}")
    if not lexical.parent.is_dir() or lexical.parent.is_symlink():
        raise ValueError(f"destination parent must be an existing regular directory: {lexical.parent}")
    current = Path(lexical.anchor)
    for part in lexical.parent.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination parent contains a symlink: {current}")
    if root is not None:
        try:
            lexical.relative_to(root.resolve())
        except ValueError as error:
            raise ValueError("output directory must be inside --repo-root") from error
    return lexical


def load_bound_json(root: Path, ref: dict[str, Any], stage: int, route: str) -> tuple[Path, dict[str, Any]]:
    path = verify_ref(root, ref, stage, route)
    try:
        return path, load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise GovernedBlock("REFERENCE_UNAVAILABLE", f"bound JSON unreadable: {ref['path']}: {error}", stage, ref.get("path"), route) from error


def preflight_candidate(
    closure: dict[str, Any], root: Path, store: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    receipt_path, receipt = load_bound_json(root, closure["candidate_receipt_ref"], 0, "repair-w2-candidate")
    validate_document(
        receipt,
        "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1",
        "receipt_digest",
        store,
        "W2_CANDIDATE_INVALID",
        0,
        "repair-w2-candidate",
    )
    if receipt["result"] != "pass" or receipt["next_route"] != "design-bundle-production":
        raise GovernedBlock("W2_CANDIDATE_INVALID", "W2 candidate receipt is not a bundle-production PASS", 0, closure["candidate_receipt_ref"]["path"], "repair-w2-candidate")
    installed_w2 = document_ref(root / W2_PRODUCER_PATH, root)
    if receipt["producer"]["sha256"] != installed_w2["sha256"]:
        raise GovernedBlock("W2_CANDIDATE_INVALID", "W2 candidate producer differs from the installed producer", 0, W2_PRODUCER_PATH, "repair-installed-contract")

    expected_bindings = {
        "process": document_ref(root / PROCESS_PATH, root),
        "profile": document_ref(root / PROFILE_PATH, root),
        "policy": document_ref(root / POLICY_PATH, root),
    }
    if receipt["bindings"] != expected_bindings:
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "W2 installed process/profile/policy bindings drifted", 0, "bindings", "repair-installed-contract")

    candidate_dir = receipt_path.parent
    names = {item.name for item in candidate_dir.iterdir()}
    expected_names = {"DESIGN.json", "DESIGN-COHERENCE-RECEIPT.json", "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json"}
    if names != expected_names or any(not (candidate_dir / name).is_file() or (candidate_dir / name).is_symlink() for name in names):
        raise GovernedBlock("W2_CANDIDATE_INVALID", "W2 candidate directory is not exactly the atomic three-file bundle", 0, candidate_dir.as_posix(), "repair-w2-candidate")
    if receipt_path.name != "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json":
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "candidate receipt filename is not canonical", 0, receipt_path.name, "repair-w2-candidate")
    observed = [
        output_ref(candidate_dir / "DESIGN.json", "design-artifact"),
        output_ref(candidate_dir / "DESIGN-COHERENCE-RECEIPT.json", "coherence-receipt"),
    ]
    if receipt["outputs"] != observed:
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "candidate output inventory differs from live bytes", 0, receipt_path.as_posix(), "repair-w2-candidate")

    source_path, source = load_bound_json(root, receipt["source_ref"], 0, "repair-w2-candidate")
    validate_document(source, "https://arcanum.dev/schemas/invoke/design-source/v1", "source_digest", store, "W2_CANDIDATE_INVALID", 0, "repair-w2-candidate")
    artifact_path = candidate_dir / "DESIGN.json"
    coherence_path = candidate_dir / "DESIGN-COHERENCE-RECEIPT.json"
    artifact = load_json(artifact_path)
    coherence = load_json(coherence_path)
    validate_document(artifact, "https://arcanum.dev/schemas/invoke/design-artifact/v1", "artifact_digest", store, "W2_CANDIDATE_INVALID", 0, "repair-w2-candidate")
    validate_document(coherence, "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1", "receipt_digest", store, "W2_CANDIDATE_INVALID", 0, "repair-w2-candidate")
    artifact_live_ref = document_ref(artifact_path, root)
    coherence_live_ref = document_ref(coherence_path, root)
    if coherence["verdict"] != "pass" or coherence["coherence_state"] != "pass" or coherence["bindings"]["design_artifact_ref"] != artifact_live_ref:
        raise GovernedBlock("W2_CANDIDATE_INVALID", "candidate coherence evidence is not exact PASS", 0, coherence_path.as_posix(), "repair-w2-candidate")
    if source["target_id"] != closure["target_id"] or artifact["target_id"] != closure["target_id"]:
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "closure, source, and artifact targets differ", 0, "target_id", "repair-w2-candidate")
    if artifact["evidence_bindings"]["design_source_ref"] != receipt["source_ref"] or coherence["bindings"]["design_source_ref"] != receipt["source_ref"]:
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "candidate source binding differs", 0, "design_source_ref", "repair-w2-candidate")
    if receipt["w1_production_receipt_ref"] != artifact["evidence_bindings"]["design_input_production_receipt_ref"]:
        raise GovernedBlock("W2_CANDIDATE_BINDING_MISMATCH", "candidate/W1 production receipt bindings differ", 0, "w1_production_receipt_ref", "repair-w2-candidate")
    verify_ref(root, receipt["w1_production_receipt_ref"], 0, "repair-w2-candidate")
    return {
        "receipt_path": receipt_path,
        "receipt": receipt,
        "candidate_dir": candidate_dir,
        "source_path": source_path,
        "source": source,
        "artifact_path": artifact_path,
        "artifact": artifact,
        "artifact_ref": artifact_live_ref,
        "coherence_path": coherence_path,
        "coherence": coherence,
        "coherence_ref": coherence_live_ref,
        "bindings": expected_bindings,
    }


def validate_distill(
    closure: dict[str, Any], candidate: dict[str, Any], root: Path, store: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    refs = closure["distill_evidence"]
    loaded: dict[str, tuple[Path, dict[str, Any]]] = {}
    for key in ("request_ref", "execution_receipt_ref", "validation_result_ref"):
        loaded[key] = load_bound_json(root, refs[key], 2, "repair-distill-evidence")
    request = loaded["request_ref"][1]
    execution = loaded["execution_receipt_ref"][1]
    validation = loaded["validation_result_ref"][1]
    for document, schema_id, code in (
        (request, "https://arcanum.dev/schemas/invoke/distill-run-request/1-0-0", "DISTILL_REQUEST_INVALID"),
        (execution, "https://arcanum.dev/schemas/invoke/distill-execution-receipt/1-0-0", "DISTILL_EXECUTION_RECEIPT_INVALID"),
        (validation, "https://arcanum.dev/schemas/invoke/distill-validation-result/1-0-0", "DISTILL_VALIDATION_RESULT_INVALID"),
    ):
        validate_document(document, schema_id, None, store, code, 2, "repair-distill-evidence")

    events_path = verify_ref(root, refs["events_ref"], 2, "repair-distill-evidence")
    events: list[dict[str, Any]] = []
    try:
        for line_number, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            value = json.loads(line)
            errors = schema_errors(value, store["https://arcanum.dev/schemas/invoke/distill-runtime-event/1-0-0"], store)
            if errors:
                raise GovernedBlock("DISTILL_EVENTS_INVALID", f"event line {line_number}: {'; '.join(errors[:4])}", 2, refs["events_ref"]["path"], "repair-distill-evidence")
            events.append(value)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GovernedBlock("DISTILL_EVENTS_INVALID", f"Distill JSONL is unreadable: {error}", 2, refs["events_ref"]["path"], "repair-distill-evidence") from error
    if not events or len({item["event_id"] for item in events}) != len(events):
        raise GovernedBlock("DISTILL_EVENTS_INVALID", "Distill event IDs are empty or duplicated", 2, refs["events_ref"]["path"], "repair-distill-evidence")
    if [item["sequence"] for item in events] != list(range(len(events))):
        raise GovernedBlock("DISTILL_EVENTS_INVALID", "Distill event sequence must be contiguous and ordered", 2, refs["events_ref"]["path"], "repair-distill-evidence")

    candidate_inputs = [
        size_bytes_ref(candidate["artifact_ref"]),
        size_bytes_ref(closure["candidate_receipt_ref"]),
    ]
    if request["invoke_mode"] != "design" or request["reviewed_inputs"] != candidate_inputs:
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill request must exact-bind the candidate artifact and candidate receipt in canonical order", 2, "reviewed_inputs", "repair-distill-evidence")
    request_ref_bytes = size_bytes_ref(refs["request_ref"])
    execution_ref_bytes = size_bytes_ref(refs["execution_receipt_ref"])
    if execution["request_ref"] != request_ref_bytes or execution["run_id"] != request["run_id"]:
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill request/execution identities differ", 2, "request_ref", "repair-distill-evidence")
    if validation["receipt_ref"] != execution_ref_bytes:
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill validation does not exact-bind the execution receipt", 2, "receipt_ref", "repair-distill-evidence")
    if execution["event_refs"] != [item["event_id"] for item in events] or any(item["run_id"] != request["run_id"] for item in events):
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill event inventory or run identity differs", 2, "event_refs", "repair-distill-evidence")
    if execution["reviewed_input_provenance"] != request["reviewed_inputs"]:
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill reviewed-input provenance differs from the request", 2, "reviewed_input_provenance", "repair-distill-evidence")
    event_ids = set(execution["event_refs"])
    if {item["role"] for item in execution["role_trace"]} != {"proposer", "balancer"}:
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill role trace must contain proposer and balancer", 2, "role_trace", "repair-distill-evidence")
    for item in execution["role_trace"]:
        if not set(item["evidence_refs"]) <= event_ids:
            raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill role trace cites unknown events", 2, "role_trace", "repair-distill-evidence")
        exact = {"path": item["result_ref"]["path"], "sha256": item["result_ref"]["sha256"], "size": item["result_ref"]["size_bytes"]}
        verify_ref(root, exact, 2, "repair-distill-evidence")
    for event in events:
        payload = event["payload_ref"]
        verify_ref(root, {"path": payload["path"], "sha256": payload["sha256"], "size": payload["size_bytes"]}, 2, "repair-distill-evidence")
    recomposed = execution["recomposition"]["result_ref"]
    verify_ref(root, {"path": recomposed["path"], "sha256": recomposed["sha256"], "size": recomposed["size_bytes"]}, 2, "repair-distill-evidence")
    technique_status = {item["technique"]: item["status"] for item in execution["technique_trace"]}
    if set(technique_status) != set(request["requested_techniques"]) or any(value == "failed" for value in technique_status.values()):
        raise GovernedBlock("DISTILL_BINDING_MISMATCH", "Distill technique trace does not close the requested denominator", 2, "technique_trace", "repair-distill-evidence")
    if (
        execution["verdict"] != "pass"
        or execution["gaps"]
        or execution["next_route"]["status"] != "ready"
        or validation["status"] != "pass"
        or any(item["status"] != "pass" for item in validation["checks"])
        or validation["diagnostics"]
        or validation["owned_gaps"]
    ):
        raise GovernedBlock("DISTILL_NOT_PASSING", "Distill execution and independent validation must both be clean PASS", 2, refs["validation_result_ref"]["path"], "repair-distill-evidence")
    return {
        "request": request,
        "execution": execution,
        "validation": validation,
        "events": events,
        "execution_path": loaded["execution_receipt_ref"][0],
    }


def blocker(error: GovernedBlock) -> dict[str, Any]:
    stage_id = STAGE_IDS[error.stage_index]
    return {
        "blocker_id": f"w3-blocker:{error.code.lower()}",
        "code": error.code,
        "message": str(error),
        "stage_id": stage_id,
        "selector": error.selector,
        "repair_route": error.route,
    }


def attempt_receipt(
    closure_ref: dict[str, Any],
    candidate_ref: dict[str, Any],
    producer_digest: str,
    error: GovernedBlock,
) -> dict[str, Any]:
    blocked = blocker(error)
    stage_results = []
    for index, stage_id in enumerate(STAGE_IDS):
        if index < error.stage_index:
            status, causes = "pass", []
        elif index == error.stage_index:
            status, causes = "block", [blocked["blocker_id"]]
        else:
            status, causes = "not_evaluable", [blocked["blocker_id"]]
        stage_results.append({"stage_id": stage_id, "status": status, "causal_blocker_ids": causes})
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v1",
        "schema_version": "invoke.design-bundle-attempt-receipt.v1",
        "receipt_id": f"design-w3-attempt:{closure_ref['sha256'][:24]}",
        "producer": {"identity": IDENTITY, "owner": OWNER, "path": PRODUCER_PATH, "sha256": producer_digest},
        "bundle_closure_ref": copy.deepcopy(closure_ref),
        "candidate_receipt_ref": copy.deepcopy(candidate_ref),
        "stage_results": stage_results,
        "outputs": [],
        "result": "block",
        "next_route": error.route,
        "blockers": [blocked],
        "evidence_ceiling": {
            "artifact_authored": False,
            "coherence_validated": False,
            "human_views_produced": False,
            "design_stage_pass": False,
            "plan_evidence": False,
            "registry_released": False,
            "mutation_runtime_ready": False,
            "acceptance": False,
            "execution": False,
            "publication": False,
            "deployment": False,
            "external_effect": False,
        },
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    return receipt


def stage_receipt(
    closure: dict[str, Any],
    closure_ref: dict[str, Any],
    candidate: dict[str, Any],
    producer_digest: str,
    next_route: str,
    outputs: list[dict[str, Any]],
) -> dict[str, Any]:
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-result/v2",
        "schema_version": "invoke.design-stage-receipt.v2",
        "receipt_id": f"design-w3:{closure_ref['sha256'][:24]}",
        "owner_capability": "invoke",
        "mode": "design",
        "target_id": closure["target_id"],
        "producer": {"identity": IDENTITY, "owner": OWNER, "path": PRODUCER_PATH, "sha256": producer_digest},
        "profile_id": "invoke.generic-design-baseline.v1",
        "activation_kind": "normal",
        "bindings": {
            "bundle_closure_ref": copy.deepcopy(closure_ref),
            "process_ref": copy.deepcopy(candidate["bindings"]["process"]),
            "profile_ref": copy.deepcopy(candidate["bindings"]["profile"]),
            "coherence_policy_ref": copy.deepcopy(candidate["bindings"]["policy"]),
            "w1_production_receipt_ref": copy.deepcopy(candidate["receipt"]["w1_production_receipt_ref"]),
            "candidate_production_receipt_ref": copy.deepcopy(closure["candidate_receipt_ref"]),
            "design_source_ref": copy.deepcopy(candidate["receipt"]["source_ref"]),
            "design_artifact_ref": copy.deepcopy(candidate["artifact_ref"]),
            "coherence_receipt_ref": copy.deepcopy(candidate["coherence_ref"]),
            "distill_evidence": copy.deepcopy(closure["distill_evidence"]),
        },
        "outputs": copy.deepcopy(outputs),
        "result": "pass",
        "selection_evidence_state": "design-validator-pass",
        "coherence_state": "pass",
        "human_views_state": "pass",
        "distill_state": "pass",
        "evidence_state": "design-stage-pass",
        "plan_evidence_state": "plan-evidence-pending",
        "next_route": next_route,
        "evidence_ceiling": {
            "artifact_authored": True,
            "coherence_validated": True,
            "human_views_produced": True,
            "design_stage_pass": True,
            "plan_evidence": False,
            "registry_released": False,
            "mutation_runtime_ready": False,
            "acceptance": False,
            "execution": False,
            "publication": False,
            "deployment": False,
            "external_effect": False,
        },
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    return receipt


def validate_staging(
    staging: Path,
    closure: dict[str, Any],
    closure_ref: dict[str, Any],
    candidate: dict[str, Any],
    producer_digest: str,
    next_route: str,
    projected: dict[str, bytes],
    store: dict[str, dict[str, Any]],
) -> None:
    expected_names = {name for _, name in OUTPUTS} | {STAGE_NAME}
    paths = {item.name: item for item in staging.iterdir()}
    if set(paths) != expected_names or any(not item.is_file() or item.is_symlink() for item in paths.values()):
        raise GovernedBlock("OUTPUT_INVENTORY_MISMATCH", "staged W3 inventory is not exactly fifteen regular files", 3, staging.as_posix())
    for name, schema_id in PROJECTED_SCHEMA_IDS.items():
        document = load_json(paths[name])
        digest_field = {
            "GLOSSARY-CONSISTENCY-REPORT.json": "report_digest",
            "PLANNED-WITNESS-CONTRACTS.json": "contract_set_digest",
            "TEMPLATE-SELECTION-RECEIPT.json": "receipt_digest",
            "DISPATCH-TRACE.json": "trace_digest",
            "DESIGN-TRANSPORT-REPORT.json": "report_digest",
        }[name]
        validate_document(document, schema_id, digest_field, store, "PROJECTION_SCHEMA_INVALID", 3, "repair-design-bundle")
    receipt = load_json(paths[STAGE_NAME])
    validate_document(receipt, "https://arcanum.dev/schemas/invoke/design-result/v2", "receipt_digest", store, "LATE_VALIDATION_FAILED", 4, "repair-installed-contract")
    observed = [output_ref(paths[name], kind) for kind, name in OUTPUTS]
    if receipt["outputs"] != observed:
        raise GovernedBlock("OUTPUT_INVENTORY_MISMATCH", "stage receipt inventory differs from staged bytes", 3, STAGE_NAME)
    if paths["DESIGN.json"].read_bytes() != candidate["artifact_path"].read_bytes():
        raise GovernedBlock("LATE_VALIDATION_FAILED", "staged DESIGN.json differs from the W2 candidate", 4, "DESIGN.json")
    copies = {
        "DESIGN-SCOPE-MANIFEST.json": candidate["artifact"]["evidence_bindings"]["scope_manifest_ref"],
        "DESIGN-DENOMINATOR-RECEIPT.json": candidate["artifact"]["evidence_bindings"]["denominator_receipt_ref"],
        "DESIGN-SELECTION-RESULT.json": candidate["artifact"]["evidence_bindings"]["selection_result_ref"],
        "DESIGN-COHERENCE-RECEIPT.json": candidate["coherence_ref"],
        "DISTILL-RECEIPT.json": closure["distill_evidence"]["execution_receipt_ref"],
    }
    for name, ref in copies.items():
        if paths[name].read_bytes() != verify_ref(candidate["root"], ref, 4, "repair-design-bundle").read_bytes():
            raise GovernedBlock("LATE_VALIDATION_FAILED", f"exact-copy output drifted: {name}", 4, name)
    for name, data in projected.items():
        if paths[name].read_bytes() != data:
            raise GovernedBlock("LATE_VALIDATION_FAILED", f"deterministic projection drifted: {name}", 4, name)
    expected_stage = stage_receipt(closure, closure_ref, candidate, producer_digest, next_route, observed)
    if receipt != expected_stage:
        raise GovernedBlock("LATE_VALIDATION_FAILED", "stage receipt cannot be rebuilt from current inputs", 4, STAGE_NAME)


def compile_bundle(
    closure_path: Path,
    root: Path,
    output_dir: Path,
    attempt_path: Path,
    schema_dir: Path,
    late_hook: Callable[[Path], None] | None = None,
) -> int:
    root = root.resolve()
    output_dir = safe_absent_destination(output_dir, root)
    attempt_path = safe_absent_destination(attempt_path)
    if attempt_path == output_dir or output_dir in attempt_path.parents or attempt_path in output_dir.parents:
        raise ValueError("attempt receipt and output directory must be disjoint")
    producer_digest = document_ref(root / PRODUCER_PATH, root)["sha256"]
    store = schema_store(schema_dir)
    required = {
        "https://arcanum.dev/schemas/invoke/design-bundle-closure/v1",
        "https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v1",
        "https://arcanum.dev/schemas/invoke/design-result/v2",
    } | set(PROJECTED_SCHEMA_IDS.values())
    if not required <= set(store):
        raise ValueError(f"installed W3 schemas unavailable: {sorted(required - set(store))}")
    try:
        closure_ref = document_ref(closure_path, root)
        closure = load_json(closure_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise ValueError(f"bundle closure is unavailable or malformed: {error}") from error
    candidate_ref = closure.get("candidate_receipt_ref")
    if not isinstance(candidate_ref, dict) or not {"path", "sha256", "size"} <= set(candidate_ref):
        raise ValueError("bundle closure lacks a usable candidate_receipt_ref")

    staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.staging-", dir=output_dir.parent))
    try:
        errors = schema_errors(closure, store["https://arcanum.dev/schemas/invoke/design-bundle-closure/v1"], store)
        if errors:
            raise GovernedBlock("BUNDLE_CLOSURE_SCHEMA_INVALID", "; ".join(errors[:8]), 0, closure_ref["path"], "repair-design-bundle")
        if closure["closure_digest"] != digest_without(closure, "closure_digest"):
            raise GovernedBlock("BUNDLE_CLOSURE_DIGEST_MISMATCH", "bundle closure self digest differs", 0, "closure_digest", "repair-design-bundle")
        if closure["output_contracts"] != OUTPUT_CONTRACTS:
            raise GovernedBlock("BUNDLE_CLOSURE_SCHEMA_INVALID", "bundle output contract differs from the fixed W3 inventory", 0, "output_contracts", "repair-design-bundle")
        candidate = preflight_candidate(closure, root, store)
        candidate["root"] = root
        distill = validate_distill(closure, candidate, root, store)
        try:
            next_route, projected = project_bundle(candidate["artifact"], candidate["coherence_ref"], candidate["artifact_ref"])
        except (KeyError, TypeError, ValueError) as error:
            code = "ROUTE_AMBIGUOUS" if "Spellcraft" in str(error) else "PROJECTION_FAILED"
            raise GovernedBlock(code, str(error), 1, "selected_companions", "repair-design-bundle") from error

        shutil.copyfile(candidate["artifact_path"], staging / "DESIGN.json")
        for name, data in projected.items():
            (staging / name).write_bytes(data)
        exact_copies = {
            "DISTILL-RECEIPT.json": distill["execution_path"],
            "DESIGN-SCOPE-MANIFEST.json": verify_ref(root, candidate["artifact"]["evidence_bindings"]["scope_manifest_ref"], 3),
            "DESIGN-DENOMINATOR-RECEIPT.json": verify_ref(root, candidate["artifact"]["evidence_bindings"]["denominator_receipt_ref"], 3),
            "DESIGN-SELECTION-RESULT.json": verify_ref(root, candidate["artifact"]["evidence_bindings"]["selection_result_ref"], 3),
            "DESIGN-COHERENCE-RECEIPT.json": candidate["coherence_path"],
        }
        for name, source in exact_copies.items():
            shutil.copyfile(source, staging / name)

        outputs = [output_ref(staging / name, kind) for kind, name in OUTPUTS]
        write_json(staging / STAGE_NAME, stage_receipt(closure, closure_ref, candidate, producer_digest, next_route, outputs))
        if late_hook:
            late_hook(staging)
        validate_staging(staging, closure, closure_ref, candidate, producer_digest, next_route, projected, store)
        if document_ref(closure_path, root) != closure_ref or document_ref(root / PRODUCER_PATH, root)["sha256"] != producer_digest:
            raise GovernedBlock("INSTALLED_CONTRACT_DRIFT", "closure or installed W3 producer changed during compilation", 4, PRODUCER_PATH, "repair-installed-contract")
        live_candidate = preflight_candidate(closure, root, store)
        if live_candidate["receipt"] != candidate["receipt"] or live_candidate["artifact_ref"] != candidate["artifact_ref"] or live_candidate["coherence_ref"] != candidate["coherence_ref"]:
            raise GovernedBlock("LATE_VALIDATION_FAILED", "W2 candidate changed during compilation", 4, candidate_ref["path"], "repair-w2-candidate")
        if output_dir.exists() or output_dir.is_symlink():
            raise GovernedBlock("PREEXISTING_DESTINATION", "output destination appeared during compilation", 4, output_dir.as_posix(), "repair-design-bundle")
        os.replace(staging, output_dir)
        return 0
    except GovernedBlock as error:
        shutil.rmtree(staging, ignore_errors=True)
        receipt = attempt_receipt(closure_ref, candidate_ref, producer_digest, error)
        errors = schema_errors(receipt, store["https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v1"], store)
        if errors:
            raise ValueError(f"cannot issue schema-valid W3 attempt receipt: {'; '.join(errors[:8])}") from error
        atomic_write_json(attempt_path, receipt)
        print(f"BLOCK [{error.code}]: {error}", file=sys.stderr)
        return 1
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("closure")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--attempt-receipt", required=True)
    parser.add_argument("--schema-dir")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    schema_dir = Path(args.schema_dir).resolve() if args.schema_dir else root / "arcanum/spells/invoke/schemas"
    try:
        return compile_bundle(
            Path(args.closure).resolve(),
            root,
            Path(args.output_dir),
            Path(args.attempt_receipt),
            schema_dir,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
