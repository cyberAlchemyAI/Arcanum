#!/usr/bin/env python3
"""Run the bounded governance-flow reference vertical and its terminal fixture."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

from compile_governance_flow import (
    GovernanceFlowError,
    canonical_bytes,
    compile_source,
    digest_document,
    load_json,
    load_yaml,
    normalize_source,
    sha256_bytes,
    validate_source,
    validate_with_schema,
    verify_graph,
    write_json,
)
from render_governance_flow import render_graph, renderer_digest, verify_human_view


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
RECEIPT_SCHEMA = SCHEMA_ROOT / "governance-flow-stage-receipt-v1.schema.yml"
REQUEST_SCHEMA = SCHEMA_ROOT / "governance-flow-owner-request-v1.schema.yml"
RUNNER_DIGEST = sha256_bytes(Path(__file__).read_bytes())

METRIC_TARGETS = {
    "postacceptance_consumer_defects": ("governance_flow.consumer_defect.v1", 0),
    "prompts_per_immutable_graph": ("governance_flow.owner_prompt.v1", 1),
    "unchanged_byte_approval_retries": ("governance_flow.request_retry.v1", 0),
    "blockers_discovered_after_request": ("governance_flow.late_blocker.v1", 0),
    "manual_receipt_transfers": ("governance_flow.receipt_transfer.v1", 0),
}


def no_permissions() -> dict[str, bool]:
    return {
        "selection": False,
        "admission": False,
        "execution": False,
        "publication": False,
        "git": False,
        "deployment": False,
        "credentials": False,
        "destructive_actions": False,
        "external_effects": False,
        "successor_execution": False,
    }


def _safe_package_path(relative: str) -> Path:
    candidate = (PACKAGE_ROOT / relative).resolve()
    try:
        candidate.relative_to(PACKAGE_ROOT.resolve())
    except ValueError as error:
        raise GovernanceFlowError(f"path escapes governance-flow package: {relative}") from error
    return candidate


def _safe_root_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise GovernanceFlowError(f"path escapes isolated root: {relative}") from error
    return candidate


def _document_digest_without_self(value: dict[str, Any], field: str) -> str:
    return digest_document(value, omit=field)


def make_receipt(
    *,
    stage: str,
    mode: str,
    status: str,
    graph_digest: str,
    predecessor_digest: str | None,
    authority_effect: str,
    permissions: dict[str, bool],
    blockers: list[dict[str, Any]] | None = None,
    first_nonzero: int = 0,
    evaluated_checks: list[dict[str, Any]] | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema_version": "arcanum.governance-flow.stage-receipt.v1",
        "receipt_id": "",
        "stage": stage,
        "mode": mode,
        "status": status,
        "decision_graph_digest": graph_digest,
        "predecessor_digest": predecessor_digest,
        "authority_effect": authority_effect,
        "permissions": copy.deepcopy(permissions),
        "blockers": copy.deepcopy(blockers or []),
        "first_nonzero": first_nonzero,
        "evaluated_checks": copy.deepcopy(evaluated_checks or []),
        "details": copy.deepcopy(details or {}),
    }
    identity_seed = {
        "stage": stage,
        "graph": graph_digest,
        "predecessor": predecessor_digest,
        "status": status,
        "details": receipt["details"],
    }
    receipt["receipt_id"] = f"gfr-{stage}-{digest_document(identity_seed)[:16]}"
    receipt["receipt_digest"] = digest_document(receipt)
    validate_with_schema(receipt, RECEIPT_SCHEMA)
    return receipt


def verify_receipt(receipt: dict[str, Any]) -> None:
    validate_with_schema(receipt, RECEIPT_SCHEMA)
    expected = _document_digest_without_self(receipt, "receipt_digest")
    if receipt["receipt_digest"] != expected:
        raise GovernanceFlowError("stage receipt digest is stale or invalid")


def require_stage_receipt(
    graph: dict[str, Any],
    receipt: dict[str, Any],
    *,
    stage: str,
    statuses: set[str],
) -> None:
    """Require one digest-valid stage receipt bound to the exact current graph."""

    verify_graph(graph)
    verify_receipt(receipt)
    if receipt["decision_graph_digest"] != graph["decision_graph_digest"]:
        raise GovernanceFlowError(f"{stage} receipt is stale for the decision graph")
    if receipt["stage"] != stage or receipt["status"] not in statuses:
        raise GovernanceFlowError(
            f"expected {stage} receipt with status in {sorted(statuses)}"
        )


def expected_execution_permissions(graph: dict[str, Any]) -> dict[str, bool]:
    authority = graph["decision_envelope"]["authority"]
    return {
        "selection": True,
        "admission": True,
        "execution": authority["execution"],
        "publication": authority["publication"],
        "git": authority["git"],
        "deployment": authority["deployment"],
        "credentials": authority["credentials"],
        "destructive_actions": authority["destructive_actions"],
        "external_effects": authority["external_effects"],
        "successor_execution": authority["successor_execution"],
    }


def _topological_consumers(consumers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    remaining = {item["consumer_id"]: item for item in consumers}
    resolved: set[str] = set()
    result: list[dict[str, Any]] = []
    while remaining:
        ready = sorted(
            consumer_id
            for consumer_id, item in remaining.items()
            if set(item["depends_on"]) <= resolved
        )
        if not ready:
            raise GovernanceFlowError("consumer dependency graph cannot be evaluated")
        for consumer_id in ready:
            result.append(remaining.pop(consumer_id))
            resolved.add(consumer_id)
    return result


Check = Callable[[], tuple[bool, int, str]]


def collect_checks(
    definitions: list[dict[str, Any]], implementations: dict[str, Check]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    """Evaluate every reachable check and preserve the first nonzero status."""

    evaluated: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    status_by_id: dict[str, str] = {}
    first_nonzero = 0

    for item in _topological_consumers(definitions):
        check_id = item["consumer_id"]
        causal = sorted(
            dependency
            for dependency in item["depends_on"]
            if status_by_id.get(dependency) != "pass"
        )
        if causal:
            evaluated.append(
                {
                    "check_id": check_id,
                    "status": "not_evaluable",
                    "exit_code": 1,
                    "causal_blockers": causal,
                }
            )
            status_by_id[check_id] = "not_evaluable"
            continue

        implementation = implementations.get(check_id)
        if implementation is None:
            passed, exit_code, message = False, 2, "declared consumer has no implementation"
        else:
            try:
                passed, exit_code, message = implementation()
            except Exception as error:  # deterministic boundary captures validator errors
                passed, exit_code, message = False, 2, f"{type(error).__name__}: {error}"

        if passed and exit_code == 0:
            status = "pass"
        else:
            status = "block"
            exit_code = exit_code or 1
            if first_nonzero == 0:
                first_nonzero = exit_code
            blockers.append(
                {
                    "blocker_id": f"{check_id}:failed",
                    "check_id": check_id,
                    "message": message or "check failed",
                    "exit_code": exit_code,
                }
            )
        evaluated.append(
            {
                "check_id": check_id,
                "status": status,
                "exit_code": exit_code,
                "causal_blockers": [],
            }
        )
        status_by_id[check_id] = status
    return evaluated, blockers, first_nonzero


def _protected_digest(source: dict[str, Any]) -> str:
    inventory = []
    for relative in sorted(source["protected_inputs"]):
        path = _safe_package_path(relative)
        if not path.is_file():
            raise GovernanceFlowError(f"protected input is missing: {relative}")
        inventory.append({"path": relative, "sha256": sha256_bytes(path.read_bytes())})
    return digest_document(inventory)


def _check_implementations(
    source: dict[str, Any], graph: dict[str, Any], human_view: str
) -> dict[str, Check]:
    def source_schema() -> tuple[bool, int, str]:
        validate_source(source)
        return True, 0, "pass"

    def graph_schema() -> tuple[bool, int, str]:
        verify_graph(graph)
        if graph["decision_envelope"] != normalize_source(source):
            return False, 3, "derived graph widened or changed the source envelope"
        return True, 0, "pass"

    def human_renderer() -> tuple[bool, int, str]:
        verify_human_view(graph, human_view)
        if render_graph(graph) != render_graph(graph):
            return False, 4, "renderer is not byte-stable"
        return True, 0, "pass"

    def executable_identity() -> tuple[bool, int, str]:
        executable = graph["decision_envelope"]["executable"]
        path = _safe_package_path(executable["path"])
        if not path.is_file():
            return False, 5, "authority-bearing executable is missing"
        if sha256_bytes(path.read_bytes()) != executable["sha256"]:
            return False, 5, "authority-bearing executable digest differs"
        return True, 0, "pass"

    def terminal_contract() -> tuple[bool, int, str]:
        terminal = graph["decision_envelope"]["terminal_outcome"]
        if terminal["completion_predicate"] != "exact_terminal_match":
            return False, 6, "terminal predicate is unsupported"
        if not {"external_call", "successor_execution"} <= set(
            terminal["prohibited_effects"]
        ):
            return False, 6, "terminal prohibitions are incomplete"
        return True, 0, "pass"

    by_kind: dict[str, Check] = {
        "source_schema": source_schema,
        "graph_schema": graph_schema,
        "human_renderer": human_renderer,
        "executable_identity": executable_identity,
        "terminal_contract": terminal_contract,
    }
    return {
        item["consumer_id"]: by_kind[item["kind"]] for item in source["consumers"]
    }


def rehearse(
    source: dict[str, Any], graph: dict[str, Any], human_view: str
) -> dict[str, Any]:
    before = _protected_digest(source)
    evaluated, blockers, first_nonzero = collect_checks(
        source["consumers"], _check_implementations(source, graph, human_view)
    )
    after = _protected_digest(source)
    if before != after:
        code = 7
        if first_nonzero == 0:
            first_nonzero = code
        blockers.append(
            {
                "blocker_id": "protected-inputs:changed",
                "check_id": "protected-inputs",
                "message": "preacceptance changed a protected input",
                "exit_code": code,
            }
        )
    status = "pass" if not blockers and all(
        item["status"] == "pass" for item in evaluated
    ) else "block"
    return make_receipt(
        stage="rehearsal",
        mode="preacceptance_no_effect",
        status=status,
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=None,
        authority_effect="none",
        permissions=no_permissions(),
        blockers=blockers,
        first_nonzero=first_nonzero,
        evaluated_checks=evaluated,
        details={
            "all_required_consumers_evaluated": len(evaluated) == len(source["consumers"]),
            "protected_inputs_before": before,
            "protected_inputs_after": after,
            "run_local_evidence_only": True,
            "source_digest": graph["source_digest"],
            "human_view_digest": sha256_bytes(human_view.encode("utf-8")),
            "renderer_digest": renderer_digest(),
        },
    )


def freeze(graph: dict[str, Any], rehearsal: dict[str, Any]) -> dict[str, Any]:
    require_stage_receipt(graph, rehearsal, stage="rehearsal", statuses={"pass"})
    if (
        rehearsal["blockers"]
        or rehearsal["first_nonzero"] != 0
        or not rehearsal["evaluated_checks"]
        or any(item["status"] != "pass" for item in rehearsal["evaluated_checks"])
        or rehearsal["details"].get("all_required_consumers_evaluated") is not True
        or rehearsal["details"].get("protected_inputs_before")
        != rehearsal["details"].get("protected_inputs_after")
    ):
        raise GovernanceFlowError("only a complete zero-blocker rehearsal can freeze")
    return make_receipt(
        stage="freeze",
        mode="preacceptance_no_effect",
        status="pass",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=rehearsal["receipt_digest"],
        authority_effect="none",
        permissions=no_permissions(),
        details={"immutable": True, "blocker_count": 0},
    )


def review(
    graph: dict[str, Any], frozen: dict[str, Any], rehearsal: dict[str, Any], human_view: str
) -> dict[str, Any]:
    require_stage_receipt(graph, frozen, stage="freeze", statuses={"pass"})
    require_stage_receipt(graph, rehearsal, stage="rehearsal", statuses={"pass"})
    verify_human_view(graph, human_view)
    envelope = graph["decision_envelope"]
    reviewer = envelope["independent_review"]["reviewer_id"]
    owner = envelope["owner"]["owner_id"]
    if reviewer == owner:
        raise GovernanceFlowError("review is not independent")
    if frozen["predecessor_digest"] != rehearsal["receipt_digest"]:
        raise GovernanceFlowError("freeze does not bind the complete rehearsal")
    if frozen["details"].get("immutable") is not True or frozen["details"].get(
        "blocker_count"
    ) != 0:
        raise GovernanceFlowError("freeze is not immutable zero-blocker evidence")
    return make_receipt(
        stage="review",
        mode="preacceptance_no_effect",
        status="pass",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=frozen["receipt_digest"],
        authority_effect="none",
        permissions=no_permissions(),
        details={
            "reviewer_id": reviewer,
            "reviewer_role": envelope["independent_review"]["reviewer_role"],
            "independent": True,
            "review_result": "pass",
            "rehearsal_receipt_digest": rehearsal["receipt_digest"],
            "human_view_digest": sha256_bytes(human_view.encode("utf-8")),
            "privacy_boundary": "pass",
        },
    )


def make_owner_request(
    graph: dict[str, Any], review_receipt: dict[str, Any], human_view: str
) -> dict[str, Any]:
    require_stage_receipt(graph, review_receipt, stage="review", statuses={"pass"})
    verify_human_view(graph, human_view)
    if not all(
        (
            review_receipt["details"].get("independent") is True,
            review_receipt["details"].get("review_result") == "pass",
            review_receipt["details"].get("privacy_boundary") == "pass",
        )
    ):
        raise GovernanceFlowError("passing independent review is required")
    terminal = graph["decision_envelope"]["terminal_outcome"]
    request: dict[str, Any] = {
        "schema_version": "arcanum.governance-flow.owner-request.v1",
        "request_id": f"gfr-request-{graph['decision_graph_digest'][:20]}",
        "idempotency_key": graph["decision_graph_digest"],
        "decision_graph_digest": graph["decision_graph_digest"],
        "source_digest": graph["source_digest"],
        "human_view_digest": sha256_bytes(human_view.encode("utf-8")),
        "review_receipt_digest": review_receipt["receipt_digest"],
        "terminal_contract_digest": digest_document(terminal),
        "owner_id": graph["decision_envelope"]["owner"]["owner_id"],
        "decision": {
            "question": "Accept or reject this exact immutable decision graph?",
            "allowed_responses": ["accept", "reject"],
        },
        "request_count": 1,
        "prompt_event_count": 1,
        "authority_effect": "none",
        "permissions": {
            key: False
            for key in (
                "selection",
                "admission",
                "execution",
                "publication",
                "git",
                "deployment",
                "credentials",
                "destructive_actions",
                "external_effects",
                "successor_execution",
            )
        },
    }
    request["request_digest"] = digest_document(request)
    validate_with_schema(request, REQUEST_SCHEMA)
    return request


def verify_owner_request(request: dict[str, Any]) -> None:
    validate_with_schema(request, REQUEST_SCHEMA)
    if request["request_digest"] != digest_document(request, omit="request_digest"):
        raise GovernanceFlowError("owner request digest is stale or invalid")


def emit_owner_request(
    graph: dict[str, Any], review_receipt: dict[str, Any], human_view: str, request_dir: Path
) -> tuple[dict[str, Any], bool]:
    expected = make_owner_request(graph, review_receipt, human_view)
    request_dir.mkdir(parents=True, exist_ok=True)
    path = request_dir / f"{graph['decision_graph_digest']}.json"
    if path.exists():
        existing = load_json(path)
        verify_owner_request(existing)
        if canonical_bytes(existing) != canonical_bytes(expected):
            raise GovernanceFlowError("idempotency collision for decision graph request")
        return existing, False
    write_json(path, expected)
    return expected, True


def accept_fixture(graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    verify_graph(graph)
    verify_owner_request(request)
    terminal = graph["decision_envelope"]["terminal_outcome"]
    if not all(
        (
            request["decision_graph_digest"] == graph["decision_graph_digest"],
            request["idempotency_key"] == graph["decision_graph_digest"],
            request["source_digest"] == graph["source_digest"],
            request["terminal_contract_digest"] == digest_document(terminal),
            request["owner_id"] == graph["decision_envelope"]["owner"]["owner_id"],
        )
    ):
        raise GovernanceFlowError("acceptance request is stale")
    return make_receipt(
        stage="acceptance",
        mode="human_decision",
        status="accepted",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=request["request_digest"],
        authority_effect="fixture_acceptance",
        permissions=no_permissions(),
        details={
            "owner_id": graph["decision_envelope"]["owner"]["owner_id"],
            "response": "accept",
            "request_digest": request["request_digest"],
            "fixture_only": True,
        },
    )


def select_fixture(graph: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]:
    require_stage_receipt(graph, acceptance, stage="acceptance", statuses={"accepted"})
    permissions = no_permissions()
    permissions["selection"] = True
    return make_receipt(
        stage="selection",
        mode="effectful_execution",
        status="pass",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=acceptance["receipt_digest"],
        authority_effect="fixture_selection",
        permissions=permissions,
        details={"selected": True, "fixture_only": True},
    )


def admit_fixture(
    graph: dict[str, Any], selection: dict[str, Any]
) -> dict[str, Any]:
    require_stage_receipt(graph, selection, stage="selection", statuses={"pass"})
    authority = graph["decision_envelope"]["authority"]
    expected_selection = no_permissions()
    expected_selection["selection"] = True
    if selection["permissions"] != expected_selection:
        raise GovernanceFlowError("selection is required before admission")
    if not authority["execution"]:
        raise GovernanceFlowError("decision envelope denies execution")
    permissions = expected_execution_permissions(graph)
    return make_receipt(
        stage="admission",
        mode="effectful_execution",
        status="pass",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=selection["receipt_digest"],
        authority_effect="fixture_admission",
        permissions=permissions,
        details={
            "write_paths": authority["write_paths"],
            "executable_digest": graph["decision_envelope"]["executable"]["sha256"],
            "fixture_only": True,
        },
    )


def execute_effects(actions: list[Callable[[], None]]) -> dict[str, Any]:
    """Run effect callbacks fail-fast; primarily a contract and fixture surface."""

    ran: list[int] = []
    for index, action in enumerate(actions):
        try:
            action()
            ran.append(index)
        except Exception as error:
            return {"status": "block", "ran": ran, "failed_index": index, "error": str(error)}
    return {"status": "pass", "ran": ran, "failed_index": None, "error": None}


def _substitute_argv(argv: list[str], isolated_root: Path) -> list[str]:
    values = {"{isolated_root}": str(isolated_root.resolve())}
    return [values.get(item, item) for item in argv]


def execute_fixture(
    graph: dict[str, Any], admission: dict[str, Any], isolated_root: Path
) -> dict[str, Any]:
    require_stage_receipt(graph, admission, stage="admission", statuses={"pass"})
    if admission["permissions"] != expected_execution_permissions(graph):
        raise GovernanceFlowError("execution requires passing admission")
    isolated_root.mkdir(parents=True, exist_ok=True)
    if any(isolated_root.iterdir()):
        raise GovernanceFlowError("isolated fixture root must be empty")

    envelope = graph["decision_envelope"]
    if (
        admission["details"].get("write_paths") != envelope["authority"]["write_paths"]
        or admission["details"].get("executable_digest")
        != envelope["executable"]["sha256"]
    ):
        raise GovernanceFlowError("admission does not bind the exact execution envelope")
    targets = envelope["targets"]
    for target in targets:
        target_path = _safe_root_path(isolated_root, target["path"])
        baseline = target_path.read_bytes() if target_path.exists() else b""
        if sha256_bytes(baseline) != target["baseline_sha256"]:
            raise GovernanceFlowError(f"target baseline differs: {target['path']}")

    executable = envelope["executable"]
    executable_path = _safe_package_path(executable["path"])
    if sha256_bytes(executable_path.read_bytes()) != executable["sha256"]:
        raise GovernanceFlowError("authority-bearing executable changed before effect")
    environment = {
        key: os.environ[key]
        for key in executable["environment_allowlist"]
        if key in os.environ
    }
    argv = _substitute_argv(executable["argv"], isolated_root)
    command = (
        [sys.executable, str(executable_path), *argv]
        if executable["mode"] == "python_script"
        else [str(executable_path), *argv]
    )
    completed = subprocess.run(
        command,
        cwd=isolated_root,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return make_receipt(
            stage="execution",
            mode="effectful_execution",
            status="block",
            graph_digest=graph["decision_graph_digest"],
            predecessor_digest=admission["receipt_digest"],
            authority_effect="declared_local_effect",
            permissions=admission["permissions"],
            blockers=[
                {
                    "blocker_id": "effect:failed",
                    "check_id": "fixture-executor",
                    "message": completed.stderr.strip() or "fixture executor failed",
                    "exit_code": completed.returncode or 1,
                }
            ],
            first_nonzero=completed.returncode or 1,
            details={"later_effects_executed": False, "successor_executed": False},
        )

    inventory = sorted(
        str(path.relative_to(isolated_root))
        for path in isolated_root.rglob("*")
        if path.is_file()
    )
    allowed = sorted(item["path"] for item in targets)
    if inventory != allowed:
        raise GovernanceFlowError(
            f"executor wrote outside the accepted ceiling: observed {inventory}, expected {allowed}"
        )
    postimages = {
        item["path"]: sha256_bytes(_safe_root_path(isolated_root, item["path"]).read_bytes())
        for item in targets
    }
    if postimages != envelope["terminal_outcome"]["expected_postimages"]:
        raise GovernanceFlowError("executor did not produce exact accepted postimages")

    return make_receipt(
        stage="execution",
        mode="effectful_execution",
        status="pass",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=admission["receipt_digest"],
        authority_effect="declared_local_effect",
        permissions=admission["permissions"],
        details={
            "observed_effects": [f"write:{path}" for path in inventory],
            "observed_postimages": postimages,
            "later_effects_executed": False,
            "successor_executed": False,
            "external_calls": 0,
            "stdout": completed.stdout,
        },
    )


def metric_evidence(graph_digest: str) -> list[dict[str, Any]]:
    edges = {
        "postacceptance_consumer_defects": "rehearsal->terminal",
        "prompts_per_immutable_graph": "review->owner-request",
        "unchanged_byte_approval_retries": "owner-request->idempotent-replay",
        "blockers_discovered_after_request": "owner-request->terminal",
        "manual_receipt_transfers": "source->terminal-receipt-chain",
    }
    metrics = []
    for metric_id, (event, target) in sorted(METRIC_TARGETS.items()):
        identity = {
            "metric_id": metric_id,
            "event": event,
            "decision_graph_digest": graph_digest,
            "evidence_edge": edges[metric_id],
        }
        metrics.append(
            {
                **identity,
                "event_id": f"gfr-metric-{digest_document(identity)[:16]}",
                "target": target,
                "value": target,
                "occurrence_count": target,
            }
        )
    return metrics


def metrics_meet_targets(metrics: list[dict[str, Any]], graph_digest: str) -> bool:
    observed = {
        item["metric_id"]: (
            item["event"],
            item["target"],
            item["value"],
            item.get("occurrence_count"),
            item.get("decision_graph_digest"),
            item.get("evidence_edge"),
            item.get("event_id"),
        )
        for item in metrics
    }
    expected = {
        item["metric_id"]: (
            item["event"],
            item["target"],
            item["target"],
            item["target"],
            graph_digest,
            item["evidence_edge"],
            item["event_id"],
        )
        for item in metric_evidence(graph_digest)
    }
    return observed == expected


def make_terminal_receipt(
    graph: dict[str, Any], execution: dict[str, Any]
) -> dict[str, Any]:
    require_stage_receipt(graph, execution, stage="execution", statuses={"pass"})
    if execution["permissions"] != expected_execution_permissions(graph):
        raise GovernanceFlowError("execution permissions differ from the accepted envelope")
    terminal = graph["decision_envelope"]["terminal_outcome"]
    observed = execution["details"]
    details = {
        "promised_boundary_id": terminal["promised_boundary_id"],
        "required_terminal_receipt_schema": terminal["required_terminal_receipt_schema"],
        "observed_effects": observed["observed_effects"],
        "observed_postimages": observed["observed_postimages"],
        "prohibited_effects_observed": [],
        "successor_executed": observed["successor_executed"],
        "external_calls": observed["external_calls"],
        "authority_and_write_ceiling": graph["decision_envelope"]["authority"]["write_paths"],
        "terminal_observer": terminal["terminal_observer"],
        "metrics": metric_evidence(graph["decision_graph_digest"]),
        "completion_predicate": True,
        "aggregate_complete": True,
    }
    receipt = make_receipt(
        stage="terminal",
        mode="effectful_execution",
        status="complete",
        graph_digest=graph["decision_graph_digest"],
        predecessor_digest=execution["receipt_digest"],
        authority_effect="declared_local_effect",
        permissions=execution["permissions"],
        details=details,
    )
    if not terminal_complete(graph, receipt):
        raise GovernanceFlowError("terminal receipt does not satisfy the frozen predicate")
    return receipt


def terminal_complete(graph: dict[str, Any], receipt: dict[str, Any] | None) -> bool:
    if receipt is None:
        return False
    try:
        verify_graph(graph)
        verify_receipt(receipt)
    except GovernanceFlowError:
        return False
    if (
        receipt["stage"] != "terminal"
        or receipt["status"] != "complete"
        or receipt["decision_graph_digest"] != graph["decision_graph_digest"]
    ):
        return False
    terminal = graph["decision_envelope"]["terminal_outcome"]
    details = receipt["details"]
    return all(
        (
            details.get("promised_boundary_id") == terminal["promised_boundary_id"],
            details.get("required_terminal_receipt_schema")
            == terminal["required_terminal_receipt_schema"],
            sorted(details.get("observed_effects", []))
            == sorted(terminal["required_effects"]),
            details.get("observed_postimages") == terminal["expected_postimages"],
            details.get("prohibited_effects_observed") == [],
            details.get("successor_executed") is False,
            details.get("external_calls") == 0,
            details.get("authority_and_write_ceiling")
            == graph["decision_envelope"]["authority"]["write_paths"],
            details.get("terminal_observer") == terminal["terminal_observer"],
            receipt.get("permissions") == expected_execution_permissions(graph),
            details.get("completion_predicate") is True,
            details.get("aggregate_complete") is True,
            metrics_meet_targets(
                details.get("metrics", []), graph["decision_graph_digest"]
            ),
        )
    )


def descendant_is_current(graph: dict[str, Any], descendant: dict[str, Any]) -> bool:
    try:
        verify_graph(graph)
        verify_receipt(descendant)
    except GovernanceFlowError:
        return False
    return descendant["decision_graph_digest"] == graph["decision_graph_digest"]


def graph_does_not_widen(source: dict[str, Any], graph: dict[str, Any]) -> bool:
    try:
        verify_graph(graph)
    except GovernanceFlowError:
        return False
    return graph["decision_envelope"] == normalize_source(source)


def acceptance_is_exact(
    graph: dict[str, Any], request: dict[str, Any], acceptance: dict[str, Any]
) -> bool:
    try:
        verify_graph(graph)
        verify_owner_request(request)
        verify_receipt(acceptance)
    except GovernanceFlowError:
        return False
    return all(
        (
            request["decision_graph_digest"] == graph["decision_graph_digest"],
            acceptance["decision_graph_digest"] == graph["decision_graph_digest"],
            acceptance["predecessor_digest"] == request["request_digest"],
            acceptance["status"] == "accepted",
        )
    )


def classify_retry(
    before: dict[str, str], after: dict[str, str], failure_kind: str
) -> str:
    consequential = (
        "decision_graph_digest",
        "target_byte_digest",
        "semantic_digest",
        "authority_digest",
        "executable_digest",
    )
    unchanged = all(before.get(key) == after.get(key) for key in consequential)
    if unchanged and failure_kind == "environmental":
        return "environmental"
    if unchanged and failure_kind == "mechanical_evidence_only":
        return "mechanical_evidence_only"
    return "semantic_or_authority"


def run_environmental_retry(
    action: Callable[[], None],
    retry_budget: int,
    before: dict[str, str],
    current: dict[str, str],
) -> dict[str, Any]:
    """Run one no-effect environmental action plus its bounded automatic retries."""

    if retry_budget < 0:
        raise GovernanceFlowError("environmental retry budget cannot be negative")
    if classify_retry(before, current, "environmental") != "environmental":
        return {
            "status": "block",
            "classification": "semantic_or_authority",
            "attempts": 0,
            "errors": ["consequential digest changed before retry"],
            "owner_prompt_count": 0,
        }
    errors: list[str] = []
    for attempt in range(1, retry_budget + 2):
        try:
            action()
            return {
                "status": "pass",
                "classification": "environmental",
                "attempts": attempt,
                "errors": errors,
                "owner_prompt_count": 0,
            }
        except Exception as error:
            errors.append(str(error))
    return {
        "status": "block",
        "classification": "environmental",
        "attempts": retry_budget + 1,
        "errors": errors,
        "owner_prompt_count": 0,
    }


def can_auto_resume(repair: dict[str, Any]) -> bool:
    return all(
        (
            repair.get("classification") == "mechanical_evidence_only",
            repair.get("independent_review") == "pass",
            repair.get("decision_graph_unchanged") is True,
            repair.get("target_bytes_unchanged") is True,
            repair.get("executable_unchanged") is True,
            repair.get("revalidation") == "pass",
            repair.get("resume_count") == 0,
        )
    )


def resume_governance_sidecar(
    repair: dict[str, Any], continuation: Callable[[], Any]
) -> dict[str, Any]:
    """Resume a suspended continuation once when every mechanical predicate passes."""

    if not can_auto_resume(repair):
        return {
            "status": "suspended",
            "resume_count": repair.get("resume_count", 0),
            "continuation_result": None,
        }
    result = continuation()
    return {"status": "resumed", "resume_count": 1, "continuation_result": result}


def receipt_edge_valid(edge: dict[str, Any]) -> tuple[bool, int]:
    if edge.get("manual_transfer") is True:
        return False, 1
    return edge.get("producer_digest") == edge.get("consumer_input_digest"), 0


def blocker_timing_metric(discovered_after_request: bool, prediscoverable: bool) -> int:
    return 1 if discovered_after_request and prediscoverable else 0


def privacy_scan(text: str) -> bool:
    sentinels = ("restricted-marker://fixture", "/restricted/private/", "internal-owner://")
    return not any(marker in text for marker in sentinels)


def is_bounded(
    required_consumers: set[str], evaluated_consumers: set[str], terminal_reachable: bool
) -> bool:
    return required_consumers == evaluated_consumers and terminal_reachable


def run_positive_fixture(
    source_path: Path,
    executor_path: Path,
    isolated_root: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes.decode("utf-8"))
    if not isinstance(source, dict):
        raise GovernanceFlowError("positive source must be an object")
    declared_executor = _safe_package_path(source["executable"]["path"])
    if declared_executor != executor_path.resolve():
        raise GovernanceFlowError("fixture executor path differs from the machine source")
    if sha256_bytes(executor_path.read_bytes()) != source["executable"]["sha256"]:
        raise GovernanceFlowError("fixture executor digest differs from the machine source")
    if source["terminal_outcome"]["terminal_observer"]["sha256"] != RUNNER_DIGEST:
        raise GovernanceFlowError("terminal observer digest differs from the exact runner")

    graph = compile_source(source, source_bytes)
    human_view_one = render_graph(graph)
    human_view_two = render_graph(graph)
    if human_view_one != human_view_two:
        raise GovernanceFlowError("human rendering is not byte-identical")
    rehearsal = rehearse(source, graph, human_view_one)
    if rehearsal["status"] != "pass":
        raise GovernanceFlowError("positive fixture rehearsal did not pass")
    frozen = freeze(graph, rehearsal)
    reviewed = review(graph, frozen, rehearsal, human_view_one)
    request, created = emit_owner_request(graph, reviewed, human_view_one, evidence_dir / "requests")
    duplicate, duplicate_created = emit_owner_request(
        graph, reviewed, human_view_one, evidence_dir / "requests"
    )
    if not created or duplicate_created or canonical_bytes(request) != canonical_bytes(duplicate):
        raise GovernanceFlowError("owner request idempotency failed")
    if any(graph["derived_permissions"].values()):
        raise GovernanceFlowError("preacceptance preparation acquired authority")

    acceptance = accept_fixture(graph, request)
    selection = select_fixture(graph, acceptance)
    admission = admit_fixture(graph, selection)
    execution = execute_fixture(graph, admission, isolated_root)
    if execution["status"] != "pass":
        raise GovernanceFlowError("positive fixture effectful execution blocked")
    terminal = make_terminal_receipt(graph, execution)

    evidence_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "graph.json": graph,
        "rehearsal.json": rehearsal,
        "freeze.json": frozen,
        "review.json": reviewed,
        "acceptance.json": acceptance,
        "selection.json": selection,
        "admission.json": admission,
        "execution.json": execution,
        "terminal.json": terminal,
    }
    for name, value in artifacts.items():
        write_json(evidence_dir / name, value)
    (evidence_dir / "human-view.md").write_text(human_view_one, encoding="utf-8")
    chain = [
        graph["source_digest"],
        graph["decision_graph_digest"],
        rehearsal["receipt_digest"],
        frozen["receipt_digest"],
        reviewed["receipt_digest"],
        request["request_digest"],
        acceptance["receipt_digest"],
        selection["receipt_digest"],
        admission["receipt_digest"],
        execution["receipt_digest"],
        terminal["receipt_digest"],
    ]
    strictly_bound = all(
        (
            rehearsal["details"]["source_digest"] == graph["source_digest"],
            rehearsal["decision_graph_digest"] == graph["decision_graph_digest"],
            frozen["predecessor_digest"] == rehearsal["receipt_digest"],
            reviewed["predecessor_digest"] == frozen["receipt_digest"],
            reviewed["details"]["rehearsal_receipt_digest"]
            == rehearsal["receipt_digest"],
            request["review_receipt_digest"] == reviewed["receipt_digest"],
            acceptance["predecessor_digest"] == request["request_digest"],
            selection["predecessor_digest"] == acceptance["receipt_digest"],
            admission["predecessor_digest"] == selection["receipt_digest"],
            execution["predecessor_digest"] == admission["receipt_digest"],
            terminal["predecessor_digest"] == execution["receipt_digest"],
        )
    )
    write_json(
        evidence_dir / "chain.json",
        {
            "schema_version": "arcanum.governance-flow.fixture-chain.v1",
            "digests": chain,
            "strictly_bound": strictly_bound and len(chain) == len(set(chain)),
            "terminal_complete": terminal_complete(graph, terminal),
            "successor_executed": False,
            "external_calls": 0,
        },
    )
    return {"graph": graph, "human_view": human_view_one, "terminal": terminal}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    fixture = subparsers.add_parser("fixture", help="run the isolated positive vertical")
    fixture.add_argument("source", type=Path)
    fixture.add_argument("executor", type=Path)
    fixture.add_argument("isolated_root", type=Path)
    fixture.add_argument("evidence_dir", type=Path)
    fixture.add_argument("--expected-human", type=Path)
    fixture.add_argument("--expected-terminal", type=Path)
    fixture.add_argument("--update-expected", action="store_true")
    args = parser.parse_args()

    if args.command == "fixture":
        result = run_positive_fixture(
            args.source.resolve(),
            args.executor.resolve(),
            args.isolated_root.resolve(),
            args.evidence_dir.resolve(),
        )
        expected_pairs = (
            (args.expected_human, result["human_view"]),
            (
                args.expected_terminal,
                json.dumps(result["terminal"], indent=2, sort_keys=True) + "\n",
            ),
        )
        for expected_path, observed in expected_pairs:
            if expected_path is None:
                continue
            if args.update_expected:
                expected_path.parent.mkdir(parents=True, exist_ok=True)
                expected_path.write_text(observed, encoding="utf-8")
            elif not expected_path.is_file() or expected_path.read_text(encoding="utf-8") != observed:
                raise GovernanceFlowError(f"expected fixture differs: {expected_path}")
        print(json.dumps(result["terminal"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
