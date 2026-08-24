#!/usr/bin/env python3
"""Validate the Task Session governance runner envelope family and fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SCHEMA_FILES = {
    "governance-run-request": "schemas/governance-run-request.schema.json",
    "execution-ticket": "schemas/execution-ticket.schema.json",
    "governance-phase-receipt": "schemas/governance-phase-receipt.schema.json",
    "executor-receipt": "schemas/executor-receipt.schema.json",
    "precloseout-execution-receipt": (
        "schemas/precloseout-execution-receipt.schema.json"
    ),
    "governance-terminal-receipt": (
        "schemas/governance-terminal-receipt.schema.json"
    ),
}
EXPECTED_SCHEMA_IDS = {
    "governance-run-request": (
        "https://arcanum.dev/schemas/task-session/governance-run-request/1-1-0"
    ),
    "execution-ticket": (
        "https://arcanum.dev/schemas/task-session/execution-ticket/1-1-0"
    ),
    "governance-phase-receipt": (
        "https://arcanum.dev/schemas/task-session/governance-phase-receipt/1-0-0"
    ),
    "executor-receipt": (
        "https://arcanum.dev/schemas/task-session/executor-receipt/1-0-0"
    ),
    "precloseout-execution-receipt": (
        "https://arcanum.dev/schemas/task-session/"
        "precloseout-execution-receipt/1-0-0"
    ),
    "governance-terminal-receipt": (
        "https://arcanum.dev/schemas/task-session/"
        "governance-terminal-receipt/1-0-0"
    ),
}
FIXTURE_FILE = "development/fixtures/governance-run-contract-cases.json"
VALIDATOR_FILE = "development/validate-governance-run-contracts.py"
EXPECTED_STAGED_FILES = sorted(
    [*SCHEMA_FILES.values(), FIXTURE_FILE, VALIDATOR_FILE]
)
TASK_SESSION_PREFIXES = (
    "arcanum/arcana/task-session/",
    "arcana/task-session/",
)
PHASES = [
    "resolved",
    "governed",
    "admitted",
    "ticketed",
    "execution-received",
    "reconciled",
    "closeout-joined",
    "observed",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {path}")
    return document


def normalize_material_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or "\x00" in normalized:
        raise ValueError(f"material path must be relative and bounded: {path}")
    for prefix in TASK_SESSION_PREFIXES:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :]
            break
    parts = Path(normalized).parts
    if not parts or ".." in parts:
        raise ValueError(f"material path escapes Task Session scope: {path}")
    return "/".join(parts)


def load_material_inventory(path: Path) -> list[str]:
    document = load_json(path)
    outputs = document.get("outputs")
    if not isinstance(outputs, list):
        raise ValueError("material inventory manifest requires an outputs array")
    inventory: list[str] = []
    for index, item in enumerate(outputs):
        if not isinstance(item, dict) or not isinstance(
            item.get("target_path"), str
        ):
            raise ValueError(
                f"material inventory output {index} requires target_path"
            )
        inventory.append(normalize_material_path(item["target_path"]))
    if len(inventory) != len(set(inventory)):
        raise ValueError("material inventory contains duplicate target paths")
    return sorted(inventory)


def exact_ref(path: str, digest_char: str = "a", size_bytes: int = 1) -> dict[str, Any]:
    return {
        "path": path,
        "sha256": digest_char * 64,
        "size_bytes": size_bytes,
    }


def owner(capability: str, subject: str) -> dict[str, str]:
    return {
        "capability": capability,
        "subject": subject,
    }


def command(command_id: str, script: str) -> dict[str, Any]:
    return {
        "command_id": command_id,
        "argv": ["python3", script],
        "cwd": ".",
        "timeout_seconds": 120,
        "max_output_bytes": 65536,
    }


def closeout_contract() -> dict[str, Any]:
    return {
        "required_owner_capabilities": [
            "continuation-router",
            "invoke",
        ],
        "continuation_policy": "emit-cursor-never-execute-successor",
        "terminal_receipt_path": "run/terminal-receipt.json",
    }


def build_documents() -> dict[str, dict[str, Any]]:
    request = {
        "schema_version": "task-session.governance-run-request.v1",
        "request_id": "request-example-001",
        "run_id": "run-example-001",
        "work_pack_ref": exact_ref("work-pack/WORK-PACK.md", "1", 101),
        "swu_ref": exact_ref("work-pack/tasks/TASK-EXAMPLE.md", "2", 102),
        "task_id": "TASK-EXAMPLE-01",
        "swu_id": "SWU-EXAMPLE-001",
        "control_refs": [
            exact_ref("run/context-pack.json", "3", 103),
        ],
        "execution_contract": {
            "allowed_writes": ["src/module.py"],
            "declared_outputs": ["results/output.json"],
            "validation_commands": [
                command("validate-module", "development/validate-module.py"),
            ],
            "timeout_seconds": 300,
            "max_output_bytes": 65536,
        },
        "owner_identity": owner("task-session", "task-session-runner"),
        "idempotency_key": "run-example-001:request",
        "closeout_contract": closeout_contract(),
    }
    ticket = {
        "schema_version": "task-session.execution-ticket.v1",
        "ticket_id": "ticket-example-001",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "request_ref": exact_ref("run/request.json", "4", 104),
        "predecessor_ref": {
            "phase": "admitted",
            "receipt_ref": exact_ref(
                "run/checkpoints/03-admitted.json", "5", 105
            ),
        },
        "control_refs": copy.deepcopy(request["control_refs"]),
        "baseline_inventory": [
            {
                "path": "src/module.py",
                "state": "present",
                "sha256": "6" * 64,
                "size_bytes": 106,
            }
        ],
        "allowed_writes": copy.deepcopy(
            request["execution_contract"]["allowed_writes"]
        ),
        "declared_outputs": copy.deepcopy(
            request["execution_contract"]["declared_outputs"]
        ),
        "validation_contracts": copy.deepcopy(
            request["execution_contract"]["validation_commands"]
        ),
        "executor_contract": {
            "owner_identity": owner(
                "implementation-executor", "bounded-native-executor"
            ),
            "argv": ["python3", "development/apply-example.py"],
            "cwd": ".",
            "environment_names": ["PATH"],
            "timeout_seconds": 300,
            "max_output_bytes": 65536,
            "expected_receipt_path": "run/executor-receipt.json",
            "expected_receipt_schema_ref": exact_ref(
                "schemas/executor-receipt.schema.json", "7", 107
            ),
        },
        "owner_identity": owner("task-session", "task-session-runner"),
        "idempotency_key": "run-example-001:ticket",
        "closeout_contract": closeout_contract(),
    }
    phase = {
        "schema_version": "task-session.governance-phase-receipt.v1",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "phase": "observed",
        "phase_index": 8,
        "predecessor": {
            "phase": "closeout-joined",
            "receipt_ref": exact_ref(
                "run/checkpoints/07-closeout-joined.json", "8", 108
            ),
        },
        "input_refs": [
            exact_ref("run/observation-request.json", "9", 109),
        ],
        "result": "pass",
        "output_refs": [
            exact_ref("run/observation-receipt.json", "b", 111),
        ],
        "owner_identity": owner("task-session", "task-session-runner"),
        "idempotency_key": "run-example-001:observed",
        "diagnostics": [],
    }
    executor = {
        "schema_version": "task-session.executor-receipt.v1",
        "receipt_id": "executor-receipt-example-001",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "ticket_ref": exact_ref("run/execution-ticket.json", "c", 112),
        "owner_identity": owner(
            "implementation-executor", "bounded-native-executor"
        ),
        "idempotency_key": "run-example-001:executor",
        "result": "pass",
        "touched_files": ["src/module.py"],
        "outputs": [
            exact_ref("results/output.json", "d", 113),
        ],
        "validation_results": [
            {
                **command("validate-module", "development/validate-module.py"),
                "exit_code": 0,
                "result": "pass",
            }
        ],
        "bounded_capture": {
            "max_output_bytes": 65536,
            "stdout_bytes": 64,
            "stderr_bytes": 0,
            "stdout_truncated": False,
            "stderr_truncated": False,
        },
        "terminal_sequence": {
            "sequence_number": 2,
            "receipt_path": "run/executor-receipt.json",
            "final_executor_write": True,
        },
        "residue": [],
    }
    terminal = {
        "schema_version": "task-session.governance-terminal-receipt.v1",
        "receipt_id": "terminal-receipt-example-001",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "request_ref": exact_ref("run/request.json", "4", 104),
        "ticket_ref": exact_ref("run/execution-ticket.json", "c", 112),
        "predecessor_ref": {
            "phase": "observed",
            "receipt_ref": exact_ref(
                "run/checkpoints/08-observed.json", "e", 114
            ),
        },
        "phase_receipts": [
            {
                "phase": name,
                "receipt_ref": exact_ref(
                    f"run/checkpoints/{index:02d}-{name}.json",
                    format(index, "x")[-1],
                    120 + index,
                ),
            }
            for index, name in enumerate(PHASES, start=1)
        ],
        "executor_receipt_ref": exact_ref(
            "run/executor-receipt.json", "f", 115
        ),
        "closeout_join": {
            "required_owner_capabilities": [
                "continuation-router",
                "invoke",
            ],
            "joined_owner_receipts": [
                {
                    "owner_capability": "continuation-router",
                    "receipt_ref": exact_ref(
                        "run/hooks/continuation-router.receipt.json", "1", 121
                    ),
                    "result": "pass",
                },
                {
                    "owner_capability": "invoke",
                    "receipt_ref": exact_ref(
                        "run/hooks/invoke-refresh.receipt.json", "2", 122
                    ),
                    "result": "pass",
                },
            ],
            "continuation": {
                "policy": "emit-cursor-never-execute-successor",
                "cursor_ref": exact_ref(
                    "run/continuity-cursor.json", "3", 123
                ),
                "successor_executed": False,
            },
        },
        "observation_ref": exact_ref(
            "run/observation-receipt.json", "b", 111
        ),
        "owner_identity": owner("task-session", "task-session-runner"),
        "idempotency_key": "run-example-001:terminal",
        "result": "pass",
        "output_refs": [
            exact_ref("results/output.json", "d", 113),
        ],
        "residue": [],
    }
    return {
        "governance-run-request": request,
        "execution-ticket": ticket,
        "governance-phase-receipt": phase,
        "executor-receipt": executor,
        "governance-terminal-receipt": terminal,
    }


def build_profile_documents() -> dict[str, dict[str, Any]]:
    """Build the selected profile while retaining build_documents() as legacy."""
    documents = build_documents()
    request = documents["governance-run-request"]
    ticket = documents["execution-ticket"]
    terminal = documents["governance-terminal-receipt"]
    request["admission_profile"] = "plan-once-selected-unit"
    request["plan_admission"] = {
        "plan_epoch_id": "epoch-aaaaaaaaaaaaaaaaaaaaaaaa",
        "unit_contract_digest": "1" * 64,
        "attempt_id": "attempt-profile-001",
        "selection_receipt_ref": exact_ref("run/selection.json", "2", 201),
        "mutation_admission_receipt_ref": exact_ref("run/admission.json", "3", 202),
        "admission_token": "4" * 64,
        "target_baseline_digest": "5" * 64,
        "validation_contract_digest": "6" * 64,
        "consumption_ledger_path": "run/admission-consumption.json",
    }
    request["closeout_contract"] = {
        "receipt_profile": "precloseout-execution-v1",
        "required_owner_capabilities": ["invoke"],
        "continuation_policy": "emit-cursor-never-execute-successor",
        "precloseout_execution_receipt_path": "run/precloseout-execution-receipt.json",
        "precloseout_execution_schema_ref": exact_ref(
            "schemas/precloseout-execution-receipt.schema.json", "a", 301
        ),
        "expected_owner_receipt_path": "run/hooks/invoke-refresh.receipt.json",
        "expected_owner_receipt_schema_ref": exact_ref(
            "schemas/invoke-refresh-receipt.schema.json", "c", 303
        ),
        "terminal_receipt_path": "run/terminal-receipt.json",
        "final_terminal_schema_ref": exact_ref(
            "schemas/governance-terminal-receipt.schema.json", "b", 302
        ),
    }
    ticket["admission_profile"] = "plan-once-selected-unit"
    ticket["plan_admission"] = {
        **copy.deepcopy(request["plan_admission"]),
        "target_baselines": [
            {
                "path": "src/module.py",
                "state": "present",
                "sha256": "7" * 64,
                "size_bytes": 207,
            }
        ],
    }
    ticket["closeout_contract"] = copy.deepcopy(request["closeout_contract"])
    terminal["admission_profile"] = "plan-once-selected-unit"
    terminal["consumed_admission"] = {
        "receipt_ref": copy.deepcopy(
            request["plan_admission"]["mutation_admission_receipt_ref"]
        ),
        "admission_token": request["plan_admission"]["admission_token"],
        "attempt_id": request["plan_admission"]["attempt_id"],
        "consumption_ledger_ref": exact_ref(
            "run/admission-consumption.json", "8", 208
        ),
    }
    terminal["receipt_profile"] = "precloseout-execution-v1"
    terminal["precloseout_execution_receipt_ref"] = exact_ref(
        "run/precloseout-execution-receipt.json", "9", 209
    )
    terminal["precloseout_execution_schema_ref"] = copy.deepcopy(
        request["closeout_contract"]["precloseout_execution_schema_ref"]
    )
    terminal["closeout_join"] = {
        "required_owner_capabilities": ["invoke"],
        "joined_owner_receipts": [
            {
                "owner_capability": "invoke",
                "receipt_ref": exact_ref("run/hooks/invoke-refresh.receipt.json", "a", 210),
                "result": "pass",
            }
        ],
        "continuation": {
            "policy": "emit-cursor-never-execute-successor",
            "cursor_ref": exact_ref("run/continuity-cursor.json", "b", 211),
            "successor_executed": False,
        },
    }
    precloseout = {
        "schema_version": "task-session.precloseout-execution-receipt.v1",
        "receipt_id": "precloseout-receipt-example-001",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "swu_id": request["swu_id"],
        "request_ref": copy.deepcopy(terminal["request_ref"]),
        "ticket_ref": copy.deepcopy(terminal["ticket_ref"]),
        "executor_receipt_ref": copy.deepcopy(terminal["executor_receipt_ref"]),
        "consumed_admission": copy.deepcopy(terminal["consumed_admission"]),
        "material_commit_ref": exact_ref("run/material-commit.json", "c", 212),
        "reconciliation_ref": exact_ref("run/reconciliation.json", "d", 213),
        "validation_receipt_ref": exact_ref("run/validation.json", "e", 214),
        "validation_contract_digest": request["plan_admission"]["validation_contract_digest"],
        "target_inventory_ref": exact_ref("run/target-inventory.json", "f", 215),
        "target_result_inventory_ref": exact_ref("run/target-result-inventory.json", "1", 216),
        "output_refs": copy.deepcopy(terminal["output_refs"]),
        "closeout_contract": {
            "route": "invoke:refresh:apply-approved",
            "owner_capability": "invoke",
            "source_receipt_path": request["closeout_contract"]["precloseout_execution_receipt_path"],
            "source_schema_ref": copy.deepcopy(request["closeout_contract"]["precloseout_execution_schema_ref"]),
            "target_inventory_ref": exact_ref("run/closeout-target-inventory.json", "2", 217),
            "expected_owner_receipt_path": request["closeout_contract"]["expected_owner_receipt_path"],
            "expected_owner_receipt_schema_ref": copy.deepcopy(request["closeout_contract"]["expected_owner_receipt_schema_ref"]),
            "final_terminal_receipt_path": request["closeout_contract"]["terminal_receipt_path"],
            "final_terminal_schema_ref": copy.deepcopy(request["closeout_contract"]["final_terminal_schema_ref"]),
            "allowed_delta_classes": ["evidence_added", "status_changed"],
            "continuation_policy": "emit-cursor-never-execute-successor",
        },
        "claim_state": "execution-validated-closeout-pending",
        "owner_identity": copy.deepcopy(request["owner_identity"]),
        "idempotency_key": "run-example-001:precloseout",
        "result": "pass",
        "residue": [],
    }
    documents["precloseout-execution-receipt"] = precloseout
    return documents


def precloseout_semantic_errors(documents: dict[str, dict[str, Any]]) -> list[str]:
    request = documents["governance-run-request"]
    ticket = documents["execution-ticket"]
    executor = documents["executor-receipt"]
    terminal = documents["governance-terminal-receipt"]
    precloseout = documents.get("precloseout-execution-receipt")
    errors: list[str] = []
    if precloseout is None:
        return ["precloseout-receipt: selected profile is missing its source receipt"]
    contract = request["closeout_contract"]
    if contract.get("receipt_profile") != "precloseout-execution-v1":
        errors.append("request: precloseout profile is missing")
    if ticket["closeout_contract"] != contract:
        errors.append("execution-ticket: precloseout closeout contract drift")
    if terminal.get("receipt_profile") != "precloseout-execution-v1":
        errors.append("terminal-receipt: precloseout sequence profile is missing")
    if terminal.get("precloseout_execution_schema_ref") != contract.get(
        "precloseout_execution_schema_ref"
    ):
        errors.append("terminal-receipt: precloseout schema identity drift")
    terminal_precloseout = terminal.get("precloseout_execution_receipt_ref", {})
    if terminal_precloseout.get("path") != contract.get(
        "precloseout_execution_receipt_path"
    ):
        errors.append("terminal-receipt: precloseout receipt path drift")
    if terminal_precloseout == terminal["executor_receipt_ref"]:
        errors.append("terminal-receipt: executor receipt cannot substitute for precloseout receipt")
    if precloseout["request_ref"] != terminal["request_ref"]:
        errors.append("precloseout-receipt: request identity drift")
    if precloseout["ticket_ref"] != terminal["ticket_ref"]:
        errors.append("precloseout-receipt: ticket identity drift")
    if precloseout["executor_receipt_ref"] != terminal["executor_receipt_ref"]:
        errors.append("precloseout-receipt: executor identity drift")
    if precloseout["output_refs"] != executor["outputs"]:
        errors.append("precloseout-receipt: output refs do not join executor outputs")
    if terminal["output_refs"] != precloseout["output_refs"]:
        errors.append("terminal-receipt: output refs do not join precloseout target outputs")
    if precloseout["owner_identity"] != request["owner_identity"]:
        errors.append("precloseout-receipt: task-session owner identity drift")
    for key in ("receipt_ref", "admission_token", "attempt_id", "consumption_ledger_ref"):
        if precloseout["consumed_admission"].get(key) != terminal["consumed_admission"].get(key):
            errors.append(f"precloseout-receipt: consumed admission {key} drift")
    plan = ticket.get("plan_admission", {})
    consumed = precloseout["consumed_admission"]
    if consumed.get("receipt_ref") != plan.get("mutation_admission_receipt_ref"):
        errors.append("precloseout-receipt: admission receipt drift from ticket")
    if consumed.get("admission_token") != plan.get("admission_token"):
        errors.append("precloseout-receipt: admission token drift from ticket")
    if consumed.get("attempt_id") != plan.get("attempt_id"):
        errors.append("precloseout-receipt: admission attempt drift from ticket")
    if precloseout["validation_contract_digest"] != plan.get("validation_contract_digest"):
        errors.append("precloseout-receipt: validation contract drift from ticket")
    precloseout_contract = precloseout["closeout_contract"]
    if precloseout_contract["source_receipt_path"] != terminal_precloseout.get("path"):
        errors.append("precloseout-receipt: Invoke source path drift")
    if precloseout_contract["source_schema_ref"] != terminal.get(
        "precloseout_execution_schema_ref"
    ):
        errors.append("precloseout-receipt: Invoke source schema drift")
    if precloseout_contract["final_terminal_receipt_path"] != contract.get(
        "terminal_receipt_path"
    ):
        errors.append("precloseout-receipt: final terminal path drift")
    if precloseout_contract["final_terminal_schema_ref"] != contract.get(
        "final_terminal_schema_ref"
    ):
        errors.append("precloseout-receipt: final terminal schema drift")
    if precloseout_contract["expected_owner_receipt_path"] != contract.get(
        "expected_owner_receipt_path"
    ):
        errors.append("precloseout-receipt: Invoke owner receipt path drift")
    if precloseout_contract["expected_owner_receipt_schema_ref"] != contract.get(
        "expected_owner_receipt_schema_ref"
    ):
        errors.append("precloseout-receipt: Invoke owner receipt schema drift")
    joined = terminal["closeout_join"]
    if joined["required_owner_capabilities"] != ["invoke"]:
        errors.append("terminal-receipt: selected profile requires Invoke-only closeout")
    joined_capabilities = [item["owner_capability"] for item in joined["joined_owner_receipts"]]
    if joined_capabilities != ["invoke"]:
        errors.append("terminal-receipt: selected profile must join exactly Invoke")
    if joined["joined_owner_receipts"][0]["receipt_ref"].get("path") != precloseout_contract[
        "expected_owner_receipt_path"
    ]:
        errors.append("terminal-receipt: Invoke owner receipt path drift")
    return errors


def documents_for_case(
    case: dict[str, Any],
    legacy_documents: dict[str, dict[str, Any]],
    profile_documents: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    family = case.get("family", "legacy")
    if family == "legacy":
        return legacy_documents
    if family == "precloseout-execution-v1":
        return profile_documents
    raise ValueError(f"unknown fixture family: {family}")


def schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        (
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: "
            f"{error.message}"
        )
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def resolve_pointer(document: Any, pointer: str) -> tuple[Any, str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer}")
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.split("/")[1:]
    ]
    if not parts:
        raise ValueError("root mutation is not supported")
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def apply_mutation(document: dict[str, Any], mutation: dict[str, Any]) -> None:
    parent, key = resolve_pointer(document, mutation["path"])
    operation = mutation["op"]
    if operation == "replace":
        if isinstance(parent, list):
            parent[int(key)] = copy.deepcopy(mutation["value"])
        else:
            parent[key] = copy.deepcopy(mutation["value"])
    elif operation == "remove":
        if isinstance(parent, list):
            parent.pop(int(key))
        else:
            del parent[key]
    elif operation == "remove-index":
        if not isinstance(parent, list):
            raise ValueError("remove-index requires an array parent")
        parent.pop(int(key))
    elif operation == "append":
        target = parent[int(key)] if isinstance(parent, list) else parent[key]
        if not isinstance(target, list):
            raise ValueError("append requires an array target")
        target.append(copy.deepcopy(mutation["value"]))
    elif operation == "add-property":
        if not isinstance(parent, dict):
            raise ValueError("add-property requires an object parent")
        if key in parent:
            raise ValueError("add-property may not replace an existing key")
        parent[key] = copy.deepcopy(mutation["value"])
    else:
        raise ValueError(f"unknown mutation operation: {operation}")


def semantic_errors(documents: dict[str, dict[str, Any]]) -> list[str]:
    request = documents["governance-run-request"]
    ticket = documents["execution-ticket"]
    phase = documents["governance-phase-receipt"]
    executor = documents["executor-receipt"]
    terminal = documents["governance-terminal-receipt"]
    errors: list[str] = []

    identity = (request["run_id"], request["task_id"], request["swu_id"])
    for name, document in documents.items():
        actual = (document["run_id"], document["task_id"], document["swu_id"])
        if actual != identity:
            errors.append(f"{name}: run/task/SWU identity drift")

    request_execution = request["execution_contract"]
    if ticket["allowed_writes"] != request_execution["allowed_writes"]:
        errors.append("execution-ticket: allowed_writes drift from request")
    if ticket["declared_outputs"] != request_execution["declared_outputs"]:
        errors.append("execution-ticket: declared_outputs drift from request")
    if ticket["validation_contracts"] != request_execution["validation_commands"]:
        errors.append("execution-ticket: validation contracts drift from request")
    if ticket["closeout_contract"] != request["closeout_contract"]:
        errors.append("execution-ticket: closeout contract drift from request")
    if request.get("admission_profile") == "plan-once-selected-unit":
        if ticket.get("admission_profile") != "plan-once-selected-unit":
            errors.append("execution-ticket: plan admission profile is missing")
        if terminal.get("admission_profile") != "plan-once-selected-unit":
            errors.append("terminal-receipt: plan admission profile is missing")
        request_plan = request.get("plan_admission", {})
        ticket_plan = ticket.get("plan_admission", {})
        for key in (
            "plan_epoch_id",
            "unit_contract_digest",
            "attempt_id",
            "selection_receipt_ref",
            "mutation_admission_receipt_ref",
            "admission_token",
            "target_baseline_digest",
            "validation_contract_digest",
            "consumption_ledger_path",
        ):
            if ticket_plan.get(key) != request_plan.get(key):
                errors.append(f"execution-ticket: plan admission {key} drift")
        consumed = terminal.get("consumed_admission", {})
        if consumed.get("receipt_ref") != ticket_plan.get(
            "mutation_admission_receipt_ref"
        ):
            errors.append("terminal-receipt: consumed admission receipt drift")
        if consumed.get("admission_token") != ticket_plan.get("admission_token"):
            errors.append("terminal-receipt: consumed admission token drift")
        if consumed.get("attempt_id") != ticket_plan.get("attempt_id"):
            errors.append("terminal-receipt: consumed admission attempt drift")
    if request.get("entry_profile") == "work-pack-fast-entry":
        if ticket.get("entry_profile") != "work-pack-fast-entry":
            errors.append("execution-ticket: fast-entry profile is missing")
        if terminal.get("entry_profile") != "work-pack-fast-entry":
            errors.append("terminal-receipt: fast-entry profile is missing")
        request_fast = request.get("fast_execution_entry", {})
        ticket_fast = ticket.get("fast_execution_entry", {})
        terminal_fast = terminal.get("fast_execution_entry", {})
        if ticket_fast.get("request_ref") != request_fast.get("request_ref"):
            errors.append("execution-ticket: fast-entry request identity drift")
        if ticket_fast.get("receipt_ref") != request_fast.get("receipt_ref"):
            errors.append("execution-ticket: fast-entry receipt identity drift")
        if terminal_fast != ticket_fast:
            errors.append("terminal-receipt: fast-entry provenance drift")

    allowed_writes = set(ticket["allowed_writes"])
    undeclared_touches = sorted(set(executor["touched_files"]) - allowed_writes)
    if undeclared_touches:
        errors.append(
            "executor-receipt: undeclared touched files "
            + ", ".join(undeclared_touches)
        )
    declared_outputs = set(ticket["declared_outputs"])
    executor_output_paths = {item["path"] for item in executor["outputs"]}
    undeclared_executor_outputs = sorted(executor_output_paths - declared_outputs)
    if undeclared_executor_outputs:
        errors.append(
            "executor-receipt: undeclared outputs "
            + ", ".join(undeclared_executor_outputs)
        )
    terminal_output_paths = {item["path"] for item in terminal["output_refs"]}
    if request["closeout_contract"].get("receipt_profile") != "precloseout-execution-v1":
        if terminal_output_paths != executor_output_paths:
            errors.append("terminal-receipt: output refs do not join executor outputs")

    if phase["phase"] != "observed" or phase["predecessor"]["phase"] != (
        "closeout-joined"
    ):
        errors.append("phase-receipt: observed checkpoint predecessor is invalid")
    if ticket["predecessor_ref"]["phase"] != "admitted":
        errors.append("execution-ticket: admitted predecessor is required")
    if terminal["predecessor_ref"]["phase"] != "observed":
        errors.append("terminal-receipt: observed predecessor is required")
    actual_phases = [item["phase"] for item in terminal["phase_receipts"]]
    if actual_phases != PHASES:
        errors.append("terminal-receipt: phase sequence is not exact and monotonic")

    required_owners = set(
        terminal["closeout_join"]["required_owner_capabilities"]
    )
    joined_owners = {
        item["owner_capability"]
        for item in terminal["closeout_join"]["joined_owner_receipts"]
    }
    if joined_owners != required_owners:
        errors.append("terminal-receipt: required owner receipts are not fully joined")
    if required_owners != set(
        request["closeout_contract"]["required_owner_capabilities"]
    ):
        errors.append("terminal-receipt: required closeout owners drift from request")
    if request["closeout_contract"].get("receipt_profile") == "precloseout-execution-v1":
        errors.extend(precloseout_semantic_errors(documents))
    return errors


def schema_contract_errors(
    schema: dict[str, Any], name: str, expected_schema_id: str
) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{name}: schema dialect is not Draft 2020-12")
    if schema.get("additionalProperties") is not False:
        errors.append(f"{name}: root envelope is not closed")
    schema_version = schema.get("properties", {}).get("schema_version", {})
    if not isinstance(schema_version, dict) or "const" not in schema_version:
        errors.append(f"{name}: schema_version is not const-bound")
    if schema.get("$id") != expected_schema_id:
        errors.append(
            f"{name}: schema ID must equal {expected_schema_id}"
        )

    def inspect(value: Any, path: str) -> None:
        if isinstance(value, dict):
            properties = value.get("properties")
            if isinstance(properties, dict) and "argv" in properties:
                argv = properties["argv"]
                if not isinstance(argv, dict) or argv.get("type") != "array":
                    errors.append(f"{name}:{path}/argv is not an array")
            forbidden = {"shell", "shell_command", "command_string"}
            if isinstance(properties, dict):
                present = sorted(forbidden.intersection(properties))
                if present:
                    errors.append(
                        f"{name}:{path} exposes shell-string fields {present}"
                    )
            for key, item in value.items():
                inspect(item, f"{path}/{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                inspect(item, f"{path}/{index}")

    inspect(schema, "<root>")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task-session-dir",
        help=(
            "Task Session tree containing the six schemas, fixture corpus, and "
            "validator; defaults to the tree containing this validator"
        ),
    )
    parser.add_argument(
        "--material-inventory-manifest",
        help=(
            "Optional producer material manifest whose exact target_path inventory "
            "must equal the seven SWU-owned targets"
        ),
    )
    args = parser.parse_args()

    task_session_dir = (
        Path(args.task_session_dir).resolve()
        if args.task_session_dir
        else Path(__file__).resolve().parents[1]
    )
    schemas = {
        name: load_json(task_session_dir / relative_path)
        for name, relative_path in SCHEMA_FILES.items()
    }
    fixtures = load_json(task_session_dir / FIXTURE_FILE)
    legacy_documents = build_documents()
    profile_documents = build_profile_documents()
    errors: list[str] = []
    positive_rows: list[tuple[str, bool]] = []
    negative_rows: list[tuple[str, bool]] = []
    semantic_rows: list[tuple[str, bool]] = []
    schema_contract_rows: list[tuple[str, bool]] = []

    expected_counts = fixtures["expected_counts"]
    for key, collection_name in (
        ("positive", "positive_cases"),
        ("negative", "negative_cases"),
        ("semantic_negative", "semantic_negative_cases"),
    ):
        actual = len(fixtures[collection_name])
        expected = expected_counts[key]
        if actual != expected:
            errors.append(
                f"fixture count drift for {collection_name}: "
                f"expected {expected}, got {actual}"
            )

    for name, schema in schemas.items():
        contract_issues = schema_contract_errors(
            schema, name, EXPECTED_SCHEMA_IDS[name]
        )
        mismatched_identity = copy.deepcopy(schema)
        mismatched_identity["$id"] = (
            EXPECTED_SCHEMA_IDS[name].rsplit("/", 1)[0] + "/9-9-9"
        )
        mismatch_issues = schema_contract_errors(
            mismatched_identity, name, EXPECTED_SCHEMA_IDS[name]
        )
        if not mismatch_issues:
            contract_issues.append(
                f"{name}: mismatched versioned schema ID unexpectedly passed"
            )
        passed = not contract_issues
        schema_contract_rows.append((name, passed))
        errors.extend(contract_issues)

    for case in fixtures["positive_cases"]:
        name = case["envelope"]
        documents = documents_for_case(case, legacy_documents, profile_documents)
        issues = schema_errors(documents[name], schemas[name])
        passed = not issues
        positive_rows.append((case["id"], passed))
        if not passed:
            errors.append(f"{case['id']}: " + "; ".join(issues))

    for family_name, documents in (
        ("legacy", legacy_documents),
        ("precloseout-execution-v1", profile_documents),
    ):
        positive_semantic_issues = semantic_errors(documents)
        if positive_semantic_issues:
            errors.extend(
                f"positive-envelope-family-{family_name}: {issue}"
                for issue in positive_semantic_issues
            )

    for case in fixtures["negative_cases"]:
        name = case["envelope"]
        documents = documents_for_case(case, legacy_documents, profile_documents)
        candidate = copy.deepcopy(documents[name])
        apply_mutation(candidate, case["mutation"])
        issues = schema_errors(candidate, schemas[name])
        passed = bool(issues)
        negative_rows.append((case["id"], passed))
        if not passed:
            errors.append(f"{case['id']}: negative case unexpectedly passed")

    for case in fixtures["semantic_negative_cases"]:
        source_documents = documents_for_case(
            case, legacy_documents, profile_documents
        )
        documents = copy.deepcopy(source_documents)
        mutation = case["mutation"]
        name = mutation["envelope"]
        apply_mutation(documents[name], mutation)
        schema_issues = schema_errors(documents[name], schemas[name])
        semantic_issues = semantic_errors(documents)
        passed = not schema_issues and bool(semantic_issues)
        semantic_rows.append((case["id"], passed))
        if not passed:
            if schema_issues:
                errors.append(
                    f"{case['id']}: semantic fixture became schema-invalid: "
                    + "; ".join(schema_issues)
                )
            else:
                errors.append(
                    f"{case['id']}: semantic negative case unexpectedly passed"
                )

    actual_owned_files = sorted(
        path
        for path in EXPECTED_STAGED_FILES
        if (task_session_dir / path).is_file()
    )
    inventory_mode = "declared-targets"
    actual_material_files = list(EXPECTED_STAGED_FILES)
    if args.material_inventory_manifest:
        inventory_mode = "producer-manifest"
        try:
            actual_material_files = load_material_inventory(
                Path(args.material_inventory_manifest).resolve()
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            actual_material_files = []
            errors.append(f"material inventory cannot be loaded: {error}")
    undeclared_outputs = sorted(
        set(actual_material_files) - set(EXPECTED_STAGED_FILES)
    )
    missing_outputs = sorted(
        set(EXPECTED_STAGED_FILES) - set(actual_owned_files)
    )
    if undeclared_outputs:
        errors.extend(
            f"undeclared staged output: {path}" for path in undeclared_outputs
        )
    if missing_outputs:
        errors.extend(f"missing staged output: {path}" for path in missing_outputs)
    if len(actual_material_files) != expected_counts["staged_files"]:
        errors.append(
            "material inventory count drift: "
            f"expected {expected_counts['staged_files']}, "
            f"got {len(actual_material_files)}"
        )

    positive_passed = sum(passed for _, passed in positive_rows)
    negative_passed = sum(passed for _, passed in negative_rows)
    semantic_passed = sum(passed for _, passed in semantic_rows)
    schema_contracts_passed = sum(passed for _, passed in schema_contract_rows)
    print(
        "RESULT "
        f"positive={positive_passed}/{len(positive_rows)} "
        f"negative={negative_passed}/{len(negative_rows)} "
        f"semantic_negative={semantic_passed}/{len(semantic_rows)} "
        f"schema_contracts={schema_contracts_passed}/{len(schema_contract_rows)} "
        f"undeclared_outputs={len(undeclared_outputs)} "
        f"inventory_mode={inventory_mode}"
    )
    for label, rows in (
        ("POSITIVE", positive_rows),
        ("NEGATIVE", negative_rows),
        ("SEMANTIC_NEGATIVE", semantic_rows),
        ("SCHEMA_CONTRACT", schema_contract_rows),
    ):
        for case_id, passed in rows:
            print(f"{label} {'PASS' if passed else 'BLOCK'} {case_id}")
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1

    manifest_payload = [
        {
            "path": path,
            "sha256": hashlib.sha256(
                (task_session_dir / path).read_bytes()
            ).hexdigest(),
            "size_bytes": (task_session_dir / path).stat().st_size,
        }
        for path in EXPECTED_STAGED_FILES
    ]
    manifest_digest = hashlib.sha256(
        json.dumps(
            manifest_payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    print(f"STAGED_MANIFEST_SHA256 {manifest_digest}")
    print(
        "EXPERIMENT_HARNESS not_run "
        "owner=later-work-pack reason=contract-matrix-only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
